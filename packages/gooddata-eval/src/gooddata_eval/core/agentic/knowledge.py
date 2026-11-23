# (C) 2026 GoodData Corporation
"""Agentic knowledge evaluation runner.

Each run is a fresh conversation that sends `expected_output.setup_turns` in order, then the
question (no simulated user), and grades the answer to the question with `AgenticKnowledgeEvaluator`.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from gooddata_eval.core.agentic._failed_runs import build_failed_runs
from gooddata_eval.core.agentic._gate import (
    DEFAULT_GATE,
    EvalGate,
    gate_passed,
    log_gate_scores,
    stamp_gate_metadata,
)
from gooddata_eval.core.agentic._outcome import (
    agentic_success,
    attach_labels,
    chat_failure_exit,
    failure_message_head,
    label_runs,
    mark_unscored_run,
    raise_agentic_failure,
)
from gooddata_eval.core.agentic._trace_linker import (
    RunIdentity,
    RunTraceContext,
    SubmitTraceLink,
    conversations_to_link,
    open_item_trace,
    run_trace_link_inline,
    submit_trace_scoring,
    utc_now,
)
from gooddata_eval.core.chat.sse_client import ChatClient, ChatError
from gooddata_eval.core.config import ReasoningEffort
from gooddata_eval.core.evaluators._llm_judge import JudgeResponseError
from gooddata_eval.core.evaluators.base import ItemEvaluation
from gooddata_eval.core.evaluators.knowledge import AgenticKnowledgeEvaluator, item_turns
from gooddata_eval.core.langfuse.item_scope import item_scope
from gooddata_eval.core.models import (
    AgenticAssertionError,
    AgenticEvalOutcome,
    ChatResult,
    DatasetItem,
    LoopExit,
    ReasoningStepEvent,
    ToolCallEvent,
    build_latency_breakdown,
    shift_and_index_events,
)
from gooddata_eval.core.timing import PhaseTimings, log_timer, run_latency_s, sum_timings

_DEFAULT_K = 1
# Code checks that gate the verdict; each is its own Langfuse score, to split retrieval from reasoning.
CODE_CHECKS = (
    "knowledge_searched",
    "expected_documents_found",
    "forbidden_documents_absent",
    "expected_source_found",
    "answered",
)


@dataclass
class KnowledgeRunResult:
    """Outcome of one K-run conversation."""

    conversation_id: str
    evaluation: ItemEvaluation
    turn_results: list[ChatResult] = field(default_factory=list)
    reasoning_steps: list[str] = field(default_factory=list)
    response_id: str | None = None
    timings: PhaseTimings = field(default_factory=PhaseTimings)
    run_latency_s: float = 0.0
    # All turns, rebased onto one timeline.
    tool_call_events: list[ToolCallEvent] = field(default_factory=list)
    reasoning_step_events: list[ReasoningStepEvent] = field(default_factory=list)
    # Set when a turn or the conversation creation failed; such a run is not graded.
    chat_error: str | None = None
    exit_reason: LoopExit | None = None

    @property
    def judge_error(self) -> str | None:
        """Why the judge left a run without a verdict; None when it graded or was not asked.

        `grade_rubric` sets `evaluation.error` only when every code check held and no gating
        criterion got a readable verdict, so the judge's verdict was the one still open.
        """
        return self.evaluation.error if self.chat_error is None else None

    @property
    def passed(self) -> bool:
        return self.chat_error is None and self.evaluation.passed


@dataclass
class AgenticKnowledgeSummary:
    """Aggregated outcome of K runs for one knowledge item."""

    run_results: list[KnowledgeRunResult]
    pass_at_k: bool
    pass_power_k: bool
    best: KnowledgeRunResult


def _turn_events(turn_results: list[ChatResult]) -> tuple[list[ToolCallEvent], list[ReasoningStepEvent], list[str]]:
    """Tool events, reasoning events and reasoning steps of the given turns, on one timeline."""
    tool_events: list[ToolCallEvent] = []
    reasoning_events: list[ReasoningStepEvent] = []
    reasoning_steps: list[str] = []
    offsets = (0.0, 0, 0)
    for result in turn_results:
        offsets = shift_and_index_events(
            result, turn_offset=offsets[0], tool_index_offset=offsets[1], reasoning_index_offset=offsets[2]
        )
        tool_events += result.tool_call_events or []
        reasoning_events += result.reasoning_step_events or []
        reasoning_steps += result.reasoning_steps or []
    return tool_events, reasoning_events, reasoning_steps


def _failed_run(
    conversation_id: str, message: str, turn_results: list[ChatResult], agent_s: float, exit_reason: LoopExit
) -> KnowledgeRunResult:
    """A run that never reached its last answer, kept so completed runs survive.

    The completed turns keep their events, so the latency breakdown still covers them.
    """
    tool_events, reasoning_events, reasoning_steps = _turn_events(turn_results)
    return KnowledgeRunResult(
        exit_reason=exit_reason,
        conversation_id=conversation_id,
        evaluation=ItemEvaluation(passed=False, rank_key=(-1, 0.0), detail={}, error=message),
        turn_results=turn_results,
        reasoning_steps=reasoning_steps,
        timings=PhaseTimings(agent_s=agent_s),
        run_latency_s=agent_s,
        tool_call_events=tool_events,
        reasoning_step_events=reasoning_events,
        chat_error=message,
    )


def _run_single_knowledge(
    client: ChatClient,
    evaluator: AgenticKnowledgeEvaluator,
    conversation_id: str,
    item: DatasetItem,
    turns: list[str],
) -> KnowledgeRunResult:
    agent_started = time.monotonic()
    turn_results: list[ChatResult] = []
    for turn in turns:
        try:
            turn_results.append(client.send_message(conversation_id, turn))
        except ChatError as exc:  # noqa: PERF203 -- one failed turn ends this run only
            message = f"chat failed on turn {len(turn_results) + 1}/{len(turns)}: {exc}"
            elapsed = time.monotonic() - agent_started
            return _failed_run(conversation_id, message, turn_results, elapsed, chat_failure_exit(exc))
    agent_elapsed = time.monotonic() - agent_started

    judge_started = time.monotonic()
    evaluation = evaluator.evaluate(item, turn_results)
    judge_elapsed = time.monotonic() - judge_started
    log_timer(f"[timer] knowledge {conversation_id} agent {agent_elapsed:.2f}s, judge {judge_elapsed:.2f}s")

    tool_events, reasoning_events, reasoning_steps = _turn_events(turn_results)
    return KnowledgeRunResult(
        conversation_id=conversation_id,
        evaluation=evaluation,
        turn_results=turn_results,
        reasoning_steps=reasoning_steps,
        response_id=turn_results[-1].response_id,
        timings=PhaseTimings(agent_s=agent_elapsed, judge_s=judge_elapsed),
        run_latency_s=agent_elapsed + judge_elapsed,
        tool_call_events=tool_events,
        reasoning_step_events=reasoning_events,
    )


def run_agentic_knowledge(
    host: str,
    token: str,
    workspace_id: str,
    question: str,
    expected_output: Any,
    k: int = _DEFAULT_K,
    initial_conversation_id: str | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    agent_id: str | None = None,
    user_context: dict[str, Any] | None = None,
    dataset_item_id: str = "",
    dataset_name: str = "agent_knowledge",
) -> AgenticKnowledgeSummary:
    """Run the knowledge item K times, each on a fresh conversation, and return a summary.

    Raises:
        ValueError: The item is invalid; raised before any request.
    """
    item = DatasetItem(
        id=dataset_item_id or "agentic_knowledge",
        dataset_name=dataset_name,
        test_kind="agentic_knowledge",
        question=question,
        expected_output=expected_output,
    )
    AgenticKnowledgeEvaluator.validate(item)
    all_turns = item_turns(item)
    client = ChatClient(
        host=host,
        token=token,
        workspace_id=workspace_id,
        reasoning_effort=reasoning_effort,
        agent_id=agent_id,
        user_context=user_context,
    )
    run_results: list[KnowledgeRunResult] = []
    try:
        evaluator = AgenticKnowledgeEvaluator()
        for run_idx in range(k):
            owned = not (run_idx == 0 and initial_conversation_id is not None)
            if owned:
                try:
                    conv_id = client.create_conversation()
                except Exception as exc:  # noqa: BLE001 -- a lost conversation must not discard completed runs
                    message = f"conversation creation failed: {exc}"
                    run_results.append(_failed_run("", message, [], 0.0, LoopExit.CHAT_ERROR))
                    continue
            else:
                conv_id = str(initial_conversation_id)
            try:
                run_results.append(_run_single_knowledge(client, evaluator, conv_id, item, all_turns))
            finally:
                if owned:
                    client.delete_conversation(conv_id)
    finally:
        client.close()

    # Chat failures and judge failures both leave a run without a verdict.
    scored = [r for r in run_results if r.chat_error is None and r.judge_error is None]
    pass_at_k = any(r.passed for r in scored)
    pass_power_k = len(scored) == len(run_results) and bool(scored) and all(r.passed for r in scored)
    best = max(scored or run_results, key=lambda r: r.evaluation.rank_key)
    return AgenticKnowledgeSummary(run_results=run_results, pass_at_k=pass_at_k, pass_power_k=pass_power_k, best=best)


def _run_detail(run: KnowledgeRunResult) -> dict:
    """Diagnostics for one run: evaluation detail, latency breakdown, chat error."""
    detail = dict(run.evaluation.detail)
    if run.chat_error is not None:
        detail["chat_error"] = run.chat_error
    detail["latency_breakdown"] = build_latency_breakdown(run.tool_call_events, run.reasoning_step_events)
    return detail


def _check_scores(run: KnowledgeRunResult) -> dict[str, bool]:
    """Per-run Langfuse scores: `knowledge_pass` plus each code check the run recorded."""
    detail = run.evaluation.detail
    checks = {name: detail[name] for name in CODE_CHECKS if isinstance(detail.get(name), bool)}
    return {"knowledge_pass": run.evaluation.passed, **checks}


def _quality_checks(run: KnowledgeRunResult) -> dict[str, bool]:
    """Every bool verdict in the detail: code checks and judge criteria, no `knowledge_pass`.

    Same set as `rank_key` quality and the report's `quality_score`, so nothing counts twice.
    """
    return {name: value for name, value in run.evaluation.detail.items() if isinstance(value, bool)}


def _failure_reason(run: KnowledgeRunResult) -> str:
    """Failed gating checks as `name=False`, plus the judge or chat error."""
    detail = run.evaluation.detail
    failed = [
        f"{name}=False"
        for name, value in detail.items()
        if value is False and (name in CODE_CHECKS or name.startswith(("include_", "exclude_")))
    ]
    parts = [", ".join(failed)] if failed else []
    if run.evaluation.error:
        parts.append(run.evaluation.error)
    return "; ".join(parts) or "criteria not satisfied"


class KnowledgeAssertionError(AgenticAssertionError):
    """Raised when an agentic knowledge evaluation fails."""


def evaluate_agentic_knowledge(
    host: str,
    token: str,
    workspace_id: str,
    question: str,
    expected_output: Any,
    k: int = _DEFAULT_K,
    initial_conversation_id: str | None = None,
    gate: EvalGate = DEFAULT_GATE,
    agent_id: str | None = None,
    user_context: dict[str, Any] | None = None,
    langfuse: object | None = None,
    dataset_item_id: str = "",
    dataset_name: str = "agent_knowledge",
    run_timestamp: str | None = None,
    model_version_override: str | None = None,
    run_metadata_extra: dict | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    submit_trace_link: SubmitTraceLink = run_trace_link_inline,
) -> AgenticEvalOutcome:
    """Run the evaluation, log to Langfuse, and raise KnowledgeAssertionError on failure."""
    identity = RunIdentity(
        host,
        token,
        workspace_id,
        dataset_name,
        run_timestamp,
        model_version_override,
        run_metadata_extra,
        reasoning_effort,
    )
    langfuse, window_start, scope = open_item_trace(langfuse, identity, dataset_item_id, suffix_runs=k > 1)
    with item_scope(scope):
        summary = run_agentic_knowledge(
            host=host,
            token=token,
            workspace_id=workspace_id,
            question=question,
            expected_output=expected_output,
            k=k,
            initial_conversation_id=initial_conversation_id,
            reasoning_effort=reasoning_effort,
            agent_id=agent_id,
            user_context=user_context,
            dataset_item_id=dataset_item_id,
            dataset_name=dataset_name,
        )

    # Before the Langfuse scores, so a run the judge could not grade gets its ERROR marker there.
    run_labels = label_runs(summary.run_results, passed=lambda r: r.passed, judge_error=lambda r: r.judge_error)

    if langfuse is not None and dataset_item_id:
        window_end = utc_now()

        def _write_scores(ctx: RunTraceContext) -> None:
            stamp_gate_metadata(ctx.run_metadata, k=len(summary.run_results), gate=gate)
            for run_idx, run in enumerate(summary.run_results):
                if run.chat_error is not None:
                    continue
                if run.judge_error is not None:
                    # No verdict: a knowledge_pass=0 would publish a failure nobody assessed.
                    mark_unscored_run(ctx, run_idx, run.conversation_id, run_labels.error_label(run_idx))
                    continue
                pt = ctx.trace(run.conversation_id)
                scores = _check_scores(run)
                with ctx.observe(pt, run_idx, conversation_id=run.conversation_id, output=scores) as tid:
                    for name, value in scores.items():
                        ctx.score(tid, name=name, value=float(value), data_type="BOOLEAN")
                    ctx.quality(
                        tid,
                        strict_checks=_quality_checks(run),
                        latency_sec=pt.latency if pt else None,
                        cost_usd=pt.total_cost if pt else None,
                    )
                    log_gate_scores(ctx, tid, gate=gate, pass_at_k=summary.pass_at_k, pass_power_k=summary.pass_power_k)

        submit_trace_scoring(
            submit_trace_link,
            identity,
            langfuse=langfuse,
            dataset_item_id=dataset_item_id,
            conversation_ids=conversations_to_link(
                [r.conversation_id for r in summary.run_results if r.chat_error is None and r.judge_error is None],
                [r.conversation_id for r in summary.run_results if r.judge_error is not None],
            ),
            window_start=window_start,
            window_end=window_end,
            suffix_runs=k > 1,
            write_scores=_write_scores,
            scope=scope,
            item_input=question,
        )

    best = summary.best
    unscored = [r.judge_error for r in summary.run_results if r.judge_error is not None]
    detail = _run_detail(best)
    if unscored:
        detail["unscored_runs"] = len(unscored)
        detail["judge_errors"] = unscored
    timings = sum_timings([r.timings for r in summary.run_results])
    runs_passed = sum(1 for r in summary.run_results if r.passed)
    runs_effective = len(summary.run_results)
    run_latencies_s = [r.run_latency_s for r in summary.run_results]
    failed_runs = build_failed_runs(summary.run_results, labels=run_labels, detail=_run_detail)

    if unscored and not any(r.chat_error is None and r.judge_error is None for r in summary.run_results):
        # No run got a verdict: the item is a harness error, not K failures.
        error = JudgeResponseError(
            f"judge returned no readable verdict for any of the {len(unscored)} graded run(s): " + " | ".join(unscored)
        )
        error.reasoning_steps = best.reasoning_steps
        error.conversation_id = best.conversation_id
        error.response_id = best.response_id
        error.detail = detail
        error.runs_passed = runs_passed
        error.runs_effective = runs_effective
        error.failed_runs = failed_runs
        error.run_latencies_s = run_latencies_s
        error.best_run_latency_s = run_latency_s(best.timings)
        error.timings = timings
        attach_labels(error, run_labels, gate)
        raise error

    if not gate_passed(gate, pass_at_k=summary.pass_at_k, pass_power_k=summary.pass_power_k):
        head = failure_message_head(gate, run_labels, runs_passed, failed_runs, len(unscored))
        raise_agentic_failure(
            KnowledgeAssertionError,
            f"Knowledge answer failed for '{dataset_item_id or question}'. {head} {_failure_reason(best)}",
            harness_error=run_labels.harness_error_record,
            shadow=run_labels.shadow(gate),
            reasoning_steps=best.reasoning_steps,
            conversation_id=best.conversation_id,
            response_id=best.response_id,
            detail=detail,
            runs_passed=runs_passed,
            runs_effective=runs_effective,
            failed_runs=failed_runs,
            run_latencies_s=run_latencies_s,
            best_run_latency_s=run_latency_s(best.timings),
            timings=timings,
        )
    return agentic_success(
        shadow=run_labels.shadow(gate),
        reasoning_steps=best.reasoning_steps,
        conversation_id=best.conversation_id,
        response_id=best.response_id,
        detail=detail,
        runs_passed=runs_passed,
        runs_effective=runs_effective,
        failed_runs=failed_runs,
        run_latencies_s=run_latencies_s,
        best_run_latency_s=run_latency_s(best.timings),
        timings=timings,
    )

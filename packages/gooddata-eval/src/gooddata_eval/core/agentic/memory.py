# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic AI memory evaluation runner (`agentic_memory`).

One question per run, graded twice:
- code: the memory items gen-ai injected into the turn's prompt (`applyMemory` detail of the
  turn's items, read from `/items`) hold every `memory_input.injected` title and no
  `memory_input.not_injected` title;
- judge: the answer text against the item's expected output.

gen-ai records the details of a turn only while the `enableGenAiInteractionIntelligence` feature
flag is on for the organization, and `applyMemory` only when the turn injected an item:
- a turn with other details and no `applyMemory` injected nothing;
- a turn with no detail at all cannot be checked: the run fails with a message naming the flag.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

import httpx

from gooddata_eval.core.agentic._failed_runs import build_failed_runs
from gooddata_eval.core.agentic._failure_message import FailedCheck, failed_check_records
from gooddata_eval.core.agentic._gate import (
    DEFAULT_GATE,
    EvalGate,
    gate_passed,
    log_gate_scores,
    stamp_gate_metadata,
)
from gooddata_eval.core.agentic._outcome import (
    agentic_detail,
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
from gooddata_eval.core.chat.render import render_answer_text
from gooddata_eval.core.chat.sse_client import ADHOC_VIZ_ID, ChatClient, ChatError
from gooddata_eval.core.config import ReasoningEffort
from gooddata_eval.core.evaluators._llm_judge import JudgeResponseError, LLMJudge, score_run
from gooddata_eval.core.langfuse.item_scope import item_scope
from gooddata_eval.core.models import (
    AgenticAssertionError,
    AgenticEvalOutcome,
    ChatResult,
    DatasetItem,
    LoopExit,
    MemoryInput,
    ReasoningStepEvent,
    ToolCallEvent,
    build_latency_breakdown,
)
from gooddata_eval.core.timing import PhaseTimings, log_timer, sum_timings

_DEFAULT_K = 1
_TEST_KIND = "agentic_memory"
_APPLY_MEMORY = "applyMemory"
_FLAG = "enableGenAiInteractionIntelligence"

# Own copy of the general-question judge steps: a change there must not move this kind's verdicts.
_MEMORY_EVALUATION_STEPS: list[str] = [
    (
        "Read the EXPECTED OUTPUT carefully. It describes what a correct response to the INPUT should convey — "
        "this may include specific facts, figures, key concepts, or analytical conclusions. "
        "Use it as the ground truth for evaluation."
    ),
    (
        "Check that the ACTUAL OUTPUT genuinely attempts to answer the question. "
        "Return FAIL (0) if the chatbot refuses, says it cannot answer, or deflects a legitimate analytical question."
    ),
    (
        "Check whether the key facts, figures, or concepts described in the EXPECTED OUTPUT "
        "are present and correctly represented in the ACTUAL OUTPUT. "
        "Exact wording is not required — focus on conceptual and factual alignment. "
        "Return FAIL (0) if important information from the EXPECTED OUTPUT is missing or contradicted."
    ),
    (
        "Do not penalize the chatbot for providing additional relevant context, richer explanations, "
        "or different but equivalent phrasing. "
        "Focus only on whether the core answer aligns with the EXPECTED OUTPUT."
    ),
    (
        "If the ACTUAL OUTPUT is empty, null, or contains only an error message unrelated to the question, "
        "return FAIL (0)."
    ),
    (
        "Return PASS (1) if the chatbot's response is factually and conceptually aligned with the EXPECTED OUTPUT. "
        "Return FAIL (0) otherwise."
    ),
]


@dataclass
class MemoryRunResult:
    """One run: the answer, the judge's verdict and the memory gen-ai injected."""

    conversation_id: str
    actual_output: str
    judge_passed: bool
    reasoning: str
    # Titles of the memory items injected into the turn's prompt; None when they could not be read.
    applied_memory: list[str] | None
    memory_error: str | None
    reasoning_steps: list[str] = field(default_factory=list)
    response_id: str | None = None
    timings: PhaseTimings = field(default_factory=PhaseTimings)
    # An unreadable judge response leaves the run ungraded, as in the general-question kind.
    judge_error: str | None = None
    tool_call_events: list[ToolCallEvent] = field(default_factory=list)
    reasoning_step_events: list[ReasoningStepEvent] = field(default_factory=list)
    run_latency_s: float = 0.0
    # Set when the chat turn itself failed (no final answer, timeout, chat error): the run is a
    # failure with neither check run.
    chat_error: str | None = None
    exit_reason: LoopExit | None = None

    @property
    def memory_passed(self) -> bool:
        return self.memory_error is None and self.chat_error is None

    @property
    def memory_check(self) -> str:
        """The name the memory check is reported under: `memory_read` when the injected memory
        is unknown, which is not a wrong injection."""
        return "memory_read" if self.applied_memory is None else "memory_injected"

    @property
    def passed(self) -> bool:
        return self.judge_passed and self.memory_passed

    @property
    def ungraded(self) -> bool:
        """No verdict: the judge could not grade and the memory check passed. A failed memory
        check decides the run on its own, so that run is a failure whatever the judge did."""
        return self.judge_error is not None and self.memory_passed


@dataclass
class AgenticMemorySummary:
    """Aggregated outcome of K runs of one memory item."""

    run_results: list[MemoryRunResult]
    pass_at_k: bool
    pass_power_k: bool
    best: MemoryRunResult

    @property
    def scored_run_results(self) -> list[MemoryRunResult]:
        return [r for r in self.run_results if not r.ungraded]

    @property
    def judge_errors(self) -> list[str]:
        return [r.judge_error for r in self.run_results if r.ungraded and r.judge_error is not None]


class MemoryAssertionError(AgenticAssertionError):
    """Raised when a memory evaluation fails."""


def _turn_details(items: list[dict[str, Any]], response_id: str | None) -> list[dict[str, Any]]:
    return [
        item["detail"]
        for item in items
        if isinstance(item.get("detail"), dict) and (response_id is None or item.get("responseId") == response_id)
    ]


def applied_memory_titles(items: list[dict[str, Any]], response_id: str | None) -> list[str] | None:
    """Titles from the `applyMemory` detail of the turn `response_id`, in retrieval order.

    Empty when the turn has other details and no `applyMemory`: it injected no memory.
    None when the turn has no detail at all: gen-ai did not record them (flag off).
    """
    details = _turn_details(items, response_id)
    if not details:
        return None
    titles: list[str] = []
    for detail in details:
        if detail.get("category") != _APPLY_MEMORY:
            continue
        raw = detail.get("items")
        entries = raw if isinstance(raw, list) else []
        titles += [e["title"] for e in entries if isinstance(e, dict) and isinstance(e.get("title"), str)]
    return titles


_NOT_RECORDED = (
    f"the turn recorded no detail, so the injected memory is unknown: is the {_FLAG} feature flag on "
    "for the organization?"
)


def memory_check_error(spec: MemoryInput, applied: list[str] | None) -> str | None:
    """Why the injected memory does not match `spec`; None when it does."""
    if applied is None:
        return _NOT_RECORDED
    missing = [t for t in spec.injected if t not in applied]
    unwanted = [t for t in spec.not_injected if t in applied]
    problems = []
    if missing:
        problems.append(f"not injected: {missing}")
    if unwanted:
        problems.append(f"injected but must not be: {unwanted}")
    return "; ".join(problems) or None


def _render_turn(chat_result: ChatResult) -> str:
    """The answer text, plus one line per chart the turn created.

    The judge reads text only. An answer that is a chart and a closing line would read as no
    answer at all, and the judge would fail it whatever the item grades.
    """
    objects = chat_result.created_visualizations.objects if chat_result.created_visualizations else []
    charts = [
        f'[The answer shows a chart: "{viz.title or "untitled"}" ({viz.type})]'
        for viz in objects
        if viz.id != ADHOC_VIZ_ID
    ]
    return "\n\n".join(chunk for chunk in (*charts, render_answer_text(chat_result)) if chunk)


def _run_single(
    client: ChatClient, judge: LLMJudge, conversation_id: str, item: DatasetItem, spec: MemoryInput
) -> MemoryRunResult:
    item_started = time.monotonic()
    try:
        chat_result = client.send_message(conversation_id, item.question)
    except ChatError as exc:
        # The agent's own failure: this run fails, the other runs of the item still count.
        elapsed = time.monotonic() - item_started
        partial = exc.partial_result
        return MemoryRunResult(
            conversation_id=conversation_id,
            actual_output="",
            judge_passed=False,
            reasoning="",
            applied_memory=None,
            memory_error=None,
            timings=PhaseTimings(agent_s=elapsed),
            tool_call_events=list(partial.tool_call_events or []) if partial else [],
            reasoning_step_events=list(partial.reasoning_step_events or []) if partial else [],
            run_latency_s=elapsed,
            chat_error=f"chat failed: {exc}",
            exit_reason=chat_failure_exit(exc),
        )
    actual_output = _render_turn(chat_result)
    agent_elapsed = time.monotonic() - item_started
    log_timer(f"[timer] memory {conversation_id} GoodData response complete after {agent_elapsed:.2f}s")

    # The memory check reads the stored items. Without them the injected memory is unknown: the
    # run fails with the exit `chat_error`, as in the agent-switcher kind, not as a wrong injection.
    exit_reason = None
    try:
        applied = applied_memory_titles(client.list_items(conversation_id), chat_result.response_id)
        memory_error = memory_check_error(spec, applied)
    except (httpx.HTTPError, ValueError) as e:
        applied, memory_error = None, f"reading the conversation items failed: {type(e).__name__}: {e}"
    if applied is None:
        exit_reason = LoopExit.CHAT_ERROR

    judge_started = time.monotonic()
    verdict = score_run(
        judge, input=item.question, expected_output=str(item.expected_output), actual_output=actual_output
    )
    judge_elapsed = time.monotonic() - judge_started
    return MemoryRunResult(
        conversation_id=conversation_id,
        actual_output=actual_output,
        judge_passed=verdict.passed,
        reasoning=verdict.reasoning,
        applied_memory=applied,
        memory_error=memory_error,
        reasoning_steps=list(chat_result.reasoning_steps or []),
        response_id=chat_result.response_id,
        timings=PhaseTimings(agent_s=agent_elapsed, judge_s=judge_elapsed),
        judge_error=verdict.error,
        tool_call_events=list(chat_result.tool_call_events or []),
        reasoning_step_events=list(chat_result.reasoning_step_events or []),
        run_latency_s=time.monotonic() - item_started,
        exit_reason=exit_reason,
    )


def _memory_spec(item: DatasetItem) -> MemoryInput:
    if item.memory_input is None:
        raise ValueError(f"{_TEST_KIND} item {item.id!r} has no memory_input")
    if not str(item.expected_output or "").strip():
        raise ValueError(f"{_TEST_KIND} item {item.id!r} has no expected_output for the judge")
    return item.memory_input


def _dataset_item(dataset_item: DatasetItem | dict, dataset_name: str) -> DatasetItem:
    """The item as a DatasetItem; a dict is the item as stored in a fixture file."""
    if isinstance(dataset_item, DatasetItem):
        return dataset_item
    return DatasetItem.model_validate(
        {"id": "", "test_kind": _TEST_KIND, "expected_output": "", **dataset_item, "dataset_name": dataset_name}
    )


def run_agentic_memory(
    host: str,
    token: str,
    workspace_id: str,
    dataset_item: DatasetItem,
    k: int = _DEFAULT_K,
    reasoning_effort: ReasoningEffort | None = None,
    agent_id: str | None = None,
) -> AgenticMemorySummary:
    """Run one memory item K times, each in its own conversation.

    Raises:
        ValueError: the item has no `memory_input`, or k is below 1. Raised before any chat request.
    """
    if k < 1:
        raise ValueError(f"k must be at least 1, got {k}")
    spec = _memory_spec(dataset_item)
    client = ChatClient(
        host=host,
        token=token,
        workspace_id=workspace_id,
        reasoning_effort=reasoning_effort,
        agent_id=agent_id,
        user_context=dataset_item.user_context,
    )
    judge = LLMJudge(_MEMORY_EVALUATION_STEPS)
    run_results: list[MemoryRunResult] = []
    try:
        for _ in range(k):
            conv_id = client.create_conversation()
            try:
                run_results.append(_run_single(client, judge, conv_id, dataset_item, spec))
            finally:
                client.delete_conversation(conv_id)
    finally:
        client.close()

    # As in the general-question kind: pass@K ignores ungraded runs, pass^K counts them as unverified.
    scored = [r for r in run_results if not r.ungraded]
    pass_at_k = any(r.passed for r in scored)
    pass_power_k = len(scored) == len(run_results) and bool(scored) and all(r.passed for r in scored)
    best = max(scored or run_results, key=lambda r: (r.passed, r.memory_passed, r.judge_passed))
    return AgenticMemorySummary(run_results=run_results, pass_at_k=pass_at_k, pass_power_k=pass_power_k, best=best)


def _run_detail(run: MemoryRunResult) -> dict:
    return {
        "judge_passed": run.judge_passed,
        "judge_reasoning": run.reasoning,
        "memory_passed": run.memory_passed,
        "applied_memory": run.applied_memory,
        "actual_output": run.actual_output,
        **({"chat_error": run.chat_error} if run.chat_error is not None else {}),
        "latency_breakdown": build_latency_breakdown(run.tool_call_events, run.reasoning_step_events),
    }


def _failed_checks(run: MemoryRunResult) -> list[dict]:
    checks = []
    if run.chat_error is not None:
        return failed_check_records([FailedCheck("chat_turn", actual=run.chat_error)])
    if run.memory_error is not None:
        checks.append(FailedCheck(run.memory_check, actual=run.memory_error))
    if run.judge_error is None and not run.judge_passed:
        checks.append(FailedCheck("memory_answer_pass", part="judge", actual=run.reasoning))
    return failed_check_records(checks)


def _attach_diagnostics(
    error: JudgeResponseError,
    best: MemoryRunResult,
    detail: dict,
    failed_runs: list[dict],
    runs_passed: int,
    runs_effective: int,
    run_latencies_s: list[float],
    best_run_latency_s: float | None,
) -> None:
    """The report payload of an item no run of which the judge could grade."""
    error.reasoning_steps = best.reasoning_steps
    error.conversation_id = best.conversation_id
    error.response_id = best.response_id
    error.detail = detail
    error.runs_passed = runs_passed
    error.runs_effective = runs_effective
    error.failed_runs = failed_runs
    error.run_latencies_s = run_latencies_s
    error.best_run_latency_s = best_run_latency_s


def evaluate_agentic_memory(
    host: str,
    token: str,
    workspace_id: str,
    dataset_item: DatasetItem | dict,
    k: int = _DEFAULT_K,
    agent_id: str | None = None,
    langfuse: object | None = None,
    dataset_item_id: str | None = None,
    dataset_name: str = "memory",
    run_timestamp: str | None = None,
    model_version_override: str | None = None,
    run_metadata_extra: dict | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    submit_trace_link: SubmitTraceLink = run_trace_link_inline,
    gate: EvalGate = DEFAULT_GATE,
) -> AgenticEvalOutcome:
    """Run a memory item K times, log to Langfuse, and raise MemoryAssertionError when the gate fails.

    Args:
        host: GoodData host URL.
        token: API token.
        workspace_id: Workspace the conversations run in.
        dataset_item: The item, or the item as stored, carrying `memory_input` and optionally `user_context`.
        k: Runs per item; each creates its own conversation.
        agent_id: Agent the conversations are created with; the default agent when None.
        langfuse: Langfuse client; built from the LANGFUSE_* environment when None.
        dataset_item_id: Langfuse item id; the item's own `id` when None.
        dataset_name: Langfuse dataset name; prefixes the experiment run name.
        run_timestamp: Shared run timestamp for the run name.
        model_version_override: Model-version tag for the run.
        run_metadata_extra: Extra experiment-run metadata.
        reasoning_effort: Sent on every message.
        submit_trace_link: How the Langfuse block is run; inline by default.
        gate: `any` (pass@K) or `power` (pass^K).

    Raises:
        MemoryAssertionError: the gate did not pass.
        JudgeResponseError: the judge returned no readable verdict for any run.
        ValueError: the item has no valid `memory_input`, raised before any request.
    """
    item = _dataset_item(dataset_item, dataset_name)
    _memory_spec(item)
    item_id = item.id if dataset_item_id is None else dataset_item_id
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
    langfuse, window_start, scope = open_item_trace(langfuse, identity, item_id, suffix_runs=k > 1)
    with item_scope(scope):
        summary = run_agentic_memory(
            host=host,
            token=token,
            workspace_id=workspace_id,
            dataset_item=item,
            k=k,
            reasoning_effort=reasoning_effort,
            agent_id=agent_id,
        )

    run_labels = label_runs(
        summary.run_results,
        passed=lambda r: not r.ungraded and r.passed,
        judge_error=lambda r: r.judge_error if r.ungraded else None,
    )

    if langfuse is not None and item_id:
        window_end = utc_now()

        def _write_scores(ctx: RunTraceContext) -> None:
            stamp_gate_metadata(ctx.run_metadata, k=len(summary.run_results), gate=gate)
            for run_idx, run in enumerate(summary.run_results):
                if run.ungraded:
                    mark_unscored_run(ctx, run_idx, run.conversation_id, run_labels.error_label(run_idx))
                    continue
                pt = ctx.trace(run.conversation_id)
                with ctx.observe(
                    pt, run_idx, conversation_id=run.conversation_id, output={"memory_pass": run.passed}
                ) as tid:
                    ctx.score(tid, name="memory_pass", value=float(run.passed), data_type="BOOLEAN")
                    if run.chat_error is not None:
                        # Neither check ran: only the run's verdict is recorded.
                        log_gate_scores(
                            ctx, tid, gate=gate, pass_at_k=summary.pass_at_k, pass_power_k=summary.pass_power_k
                        )
                        continue
                    ctx.score(tid, name=run.memory_check, value=float(run.memory_passed), data_type="BOOLEAN")
                    if run.judge_error is None:
                        ctx.score(tid, name="memory_answer_pass", value=float(run.judge_passed), data_type="BOOLEAN")
                    log_gate_scores(ctx, tid, gate=gate, pass_at_k=summary.pass_at_k, pass_power_k=summary.pass_power_k)
                    ctx.quality(
                        tid,
                        strict_checks={
                            run.memory_check: run.memory_passed,
                            **({"memory_answer_pass": run.judge_passed} if run.judge_error is None else {}),
                        },
                        latency_sec=pt.latency if pt else None,
                        cost_usd=pt.total_cost if pt else None,
                    )

        submit_trace_scoring(
            submit_trace_link,
            identity,
            langfuse=langfuse,
            dataset_item_id=item_id,
            conversation_ids=conversations_to_link(
                [r.conversation_id for r in summary.scored_run_results],
                [r.conversation_id for r in summary.run_results if r.ungraded],
            ),
            window_start=window_start,
            window_end=window_end,
            suffix_runs=k > 1,
            write_scores=_write_scores,
            scope=scope,
            item_input=item.question,
        )

    item_timings = sum_timings([r.timings for r in summary.run_results])
    unscored = summary.judge_errors
    runs_passed = sum(1 for r in summary.scored_run_results if r.passed)
    runs_effective = len(summary.run_results)
    run_latencies_s = [r.run_latency_s for r in summary.run_results]
    best = summary.best
    detail = agentic_detail(
        best.tool_call_events,
        best.reasoning_step_events,
        judge_passed=best.judge_passed,
        judge_reasoning=best.reasoning,
        memory_passed=best.memory_passed,
        applied_memory=best.applied_memory,
        actual_output=best.actual_output,
        **({"unscored_runs": len(unscored), "judge_errors": unscored} if unscored else {}),
    )
    failed_runs = build_failed_runs(
        summary.run_results, labels=run_labels, detail=_run_detail, failed_checks=_failed_checks
    )
    # The run's own wall time: it includes the /items read, which `timings` does not.
    best_run_latency_s = best.run_latency_s

    if not summary.scored_run_results:
        error = JudgeResponseError(
            f"judge returned no readable verdict for any of the {len(summary.run_results)} run(s): "
            + " | ".join(unscored)
        )
        _attach_diagnostics(
            error, best, detail, failed_runs, runs_passed, runs_effective, run_latencies_s, best_run_latency_s
        )
        error.timings = item_timings
        attach_labels(error, run_labels, gate)
        raise error

    if not gate_passed(gate, pass_at_k=summary.pass_at_k, pass_power_k=summary.pass_power_k):
        gate_note = failure_message_head(gate, run_labels, runs_passed, failed_runs, len(unscored))
        raise_agentic_failure(
            MemoryAssertionError,
            f"Memory assertion failed. {gate_note} {best.chat_error + '; ' if best.chat_error else ''}"
            f"memory: {best.memory_error or 'ok'}; "
            f"judge passed={best.judge_passed}. Reasoning: {best.reasoning}",
            harness_error=run_labels.harness_error_record,
            shadow=run_labels.shadow(gate),
            reasoning_steps=best.reasoning_steps,
            conversation_id=best.conversation_id,
            response_id=best.response_id,
            detail=detail,
            timings=item_timings,
            runs_passed=runs_passed,
            runs_effective=runs_effective,
            failed_runs=failed_runs,
            run_latencies_s=run_latencies_s,
            best_run_latency_s=best_run_latency_s,
        )
    return agentic_success(
        shadow=run_labels.shadow(gate),
        reasoning_steps=best.reasoning_steps,
        conversation_id=best.conversation_id,
        response_id=best.response_id,
        detail=detail,
        timings=item_timings,
        runs_passed=runs_passed,
        runs_effective=runs_effective,
        failed_runs=failed_runs,
        run_latencies_s=run_latencies_s,
        best_run_latency_s=best_run_latency_s,
    )

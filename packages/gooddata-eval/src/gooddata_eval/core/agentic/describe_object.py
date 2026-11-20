# (C) 2026 GoodData Corporation. All rights reserved.
"""Describe or explain an analytics object in the chat, as a user asks on the Analyze page.

One question, no `userContext`: the agent has to find the object in the workspace itself.
Each of the K runs opens its own conversation; the gate decides the item.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from gooddata_eval.core.agentic._failed_runs import build_failed_runs
from gooddata_eval.core.agentic._gate import (
    DEFAULT_GATE,
    EvalGate,
    gate_failure_note,
    gate_passed,
    log_gate_scores,
    stamp_gate_metadata,
)
from gooddata_eval.core.agentic._trace_linker import (
    RunIdentity,
    RunTraceContext,
    SubmitTraceLink,
    open_trace_window,
    run_trace_link_inline,
    submit_trace_scoring,
    utc_now,
)
from gooddata_eval.core.chat.render import render_answer_text
from gooddata_eval.core.chat.sse_client import ChatClient, ChatError
from gooddata_eval.core.config import ReasoningEffort
from gooddata_eval.core.evaluators.base import ItemEvaluation
from gooddata_eval.core.evaluators.describe_object import evaluate_answer, make_judges
from gooddata_eval.core.models import AgenticAssertionError, AgenticEvalOutcome, ChatResult, build_latency_breakdown
from gooddata_eval.core.timing import PhaseTimings


@dataclass
class DescribeRun:
    conversation_id: str
    result: ChatResult | None = None
    error: str | None = None
    evaluation: ItemEvaluation | None = None
    agent_s: float = 0.0
    judge_s: float = 0.0
    tool_names: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.error is None and self.evaluation is not None and self.evaluation.passed


def _run_once(client: ChatClient, question: str, expected: dict[str, Any], judge_model: str | None) -> DescribeRun:
    try:
        conversation_id = client.create_conversation()
    except Exception as exc:  # noqa: BLE001 -- a lost conversation must not discard completed runs
        return DescribeRun("", error=f"conversation creation failed: {exc}")
    run = DescribeRun(conversation_id)
    started = time.monotonic()
    try:
        run.result = client.send_message(conversation_id, question)
    except ChatError as exc:
        run.error = f"chat failed: {exc}"
    finally:
        run.agent_s = time.monotonic() - started
        client.delete_conversation(conversation_id)
    if run.result is not None:
        run.tool_names = [e.function_name for e in run.result.tool_call_events]
        positive, violation = make_judges(judge_model)
        judged = time.monotonic()
        run.evaluation = evaluate_answer(
            question=question,
            answer=render_answer_text(run.result),
            tool_names=run.tool_names,
            expected=expected,
            positive_judge=positive,
            violation_judge=violation,
        )
        run.judge_s = time.monotonic() - judged
    return run


def _run_detail(run: DescribeRun) -> dict[str, Any]:
    detail: dict[str, Any] = dict(run.evaluation.detail) if run.evaluation else {}
    detail["tools"] = run.tool_names
    if run.error:
        detail["chat_error"] = run.error
    if run.result is not None:
        detail["latency_breakdown"] = build_latency_breakdown(
            run.result.tool_call_events, run.result.reasoning_step_events
        )
    return detail


class DescribeObjectAssertionError(AgenticAssertionError):
    """Raised when an agentic describe-object evaluation fails."""


def evaluate_agentic_describe_object(
    host: str,
    token: str,
    workspace_id: str,
    question: str,
    expected_output: dict[str, Any],
    k: int = 1,
    gate: EvalGate = DEFAULT_GATE,
    agent_id: str | None = None,
    langfuse: object | None = None,
    dataset_item_id: str = "",
    dataset_name: str = "agent_describe_objects",
    run_timestamp: str | None = None,
    model_version_override: str | None = None,
    run_metadata_extra: dict | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    submit_trace_link: SubmitTraceLink = run_trace_link_inline,
    judge_model: str | None = None,
) -> AgenticEvalOutcome:
    """Ask K times, grade each answer, log to Langfuse, raise DescribeObjectAssertionError on failure."""
    langfuse, window_start = open_trace_window(langfuse)
    client = ChatClient(
        host=host, token=token, workspace_id=workspace_id, reasoning_effort=reasoning_effort, agent_id=agent_id
    )
    try:
        runs = [_run_once(client, question, expected_output, judge_model) for _ in range(k)]
    finally:
        client.close()

    scored = [r for r in runs if r.error is None]
    pass_at_k = any(r.passed for r in scored)
    pass_power_k = bool(scored) and len(scored) == len(runs) and all(r.passed for r in scored)

    if langfuse is not None and dataset_item_id:
        window_end = utc_now()

        def _write_scores(ctx: RunTraceContext) -> None:
            stamp_gate_metadata(ctx.run_metadata, k=len(runs), gate=gate)
            for run_idx, run in enumerate(runs):
                if run.error is not None:
                    continue
                pt = ctx.trace(run.conversation_id)
                with ctx.observe(pt, run_idx) as tid:
                    ctx.score(tid, name="describe_pass", value=float(run.passed), data_type="BOOLEAN")
                    ctx.quality(
                        tid,
                        strict_checks={"describe_pass": run.passed},
                        latency_sec=pt.latency if pt else None,
                        cost_usd=pt.total_cost if pt else None,
                    )
                    log_gate_scores(ctx, tid, gate=gate, pass_at_k=pass_at_k, pass_power_k=pass_power_k)

        submit_trace_scoring(
            submit_trace_link,
            RunIdentity(
                host,
                token,
                workspace_id,
                dataset_name,
                run_timestamp,
                model_version_override,
                run_metadata_extra,
                reasoning_effort,
            ),
            langfuse=langfuse,
            dataset_item_id=dataset_item_id,
            conversation_ids=[r.conversation_id for r in scored],
            window_start=window_start,
            window_end=window_end,
            suffix_runs=len(runs) > 1,
            write_scores=_write_scores,
            item_input=question,
        )

    best = max(runs, key=lambda r: (r.passed, r.evaluation.rank_key if r.evaluation else (-2, 0.0)))
    timings = PhaseTimings()
    for run in runs:
        timings = timings + PhaseTimings(agent_s=run.agent_s, judge_s=run.judge_s)
    runs_passed = sum(1 for r in runs if r.passed)
    failed_runs = build_failed_runs(runs, passed=lambda r: r.passed, detail=_run_detail)
    reasoning = list(best.result.reasoning_steps or []) if best.result else []
    response_id = best.result.response_id if best.result else None

    if not gate_passed(gate, pass_at_k=pass_at_k, pass_power_k=pass_power_k):
        reason = best.error or (best.evaluation.error if best.evaluation and best.evaluation.error else None)
        error = DescribeObjectAssertionError(
            f"Describe object failed for {question!r}. {gate_failure_note(gate, runs_passed, len(runs))}: "
            f"{reason or 'criteria not satisfied'}"
        )
        error.reasoning_steps = reasoning
        error.conversation_id = best.conversation_id
        error.response_id = response_id
        error.detail = _run_detail(best)
        error.timings = timings
        error.runs_passed = runs_passed
        error.runs_effective = len(runs)
        error.failed_runs = failed_runs
        error.run_latencies_s = [r.agent_s + r.judge_s for r in runs]
        raise error

    return AgenticEvalOutcome(
        reasoning_steps=reasoning,
        conversation_id=best.conversation_id,
        response_id=response_id,
        detail=_run_detail(best),
        timings=timings,
        runs_passed=runs_passed,
        runs_effective=len(runs),
        failed_runs=failed_runs,
        run_latencies_s=[r.agent_s + r.judge_s for r in runs],
    )

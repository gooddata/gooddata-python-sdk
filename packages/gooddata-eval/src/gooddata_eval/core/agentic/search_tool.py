# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic search-tool evaluation runner (single-turn)."""

from __future__ import annotations

from dataclasses import dataclass, field

from gooddata_eval.core.agentic._trace_linker import (
    RunIdentity,
    RunTraceContext,
    SubmitTraceLink,
    open_trace_window,
    run_trace_link_inline,
    submit_trace_scoring,
    utc_now,
)
from gooddata_eval.core.chat.sse_client import ChatClient
from gooddata_eval.core.config import ReasoningEffort
from gooddata_eval.core.models import (
    AgenticAssertionError,
    AgenticEvalOutcome,
    ReasoningStepEvent,
    ToolCallEvent,
    build_latency_breakdown,
)

_DEFAULT_K = 1


def _tool_selection(tool_call_events: list[ToolCallEvent]) -> bool:
    """Return True if search_objects was called."""
    return any(tc.function_name == "search_objects" for tc in tool_call_events)


def _tool_correctness(tool_call_events: list[ToolCallEvent], expected_tool_call: dict) -> bool:
    """Return True if the search_objects call arguments match expected.

    List fields (e.g. keywords, object_types) use subset matching: all expected
    values must appear in the actual call, but the agent may include extras.
    """
    for tc in tool_call_events:
        if tc.function_name == "search_objects":
            args = tc.parsed_arguments() or {}
            for key, exp_val in expected_tool_call.items():
                act_val = args.get(key)
                if isinstance(exp_val, list) and isinstance(act_val, list):
                    if not set(exp_val).issubset(set(act_val)):
                        return False
                elif isinstance(exp_val, str) and isinstance(act_val, str):
                    if exp_val.lower() not in act_val.lower() and act_val.lower() not in exp_val.lower():
                        return False
                elif exp_val != act_val:
                    return False
            return True
    return False


@dataclass
class SearchResult:
    """Outcome of one K-run search-tool evaluation."""

    conversation_id: str
    tool_selected: bool
    tool_correct: bool
    tool_call_names: list[str]
    reasoning_steps: list[str] = field(default_factory=list)
    response_id: str | None = None
    tool_call_events: list[ToolCallEvent] = field(default_factory=list)
    reasoning_step_events: list[ReasoningStepEvent] = field(default_factory=list)


@dataclass
class AgenticSearchSummary:
    """Aggregated outcome of K runs for search-tool evaluation."""

    run_results: list[SearchResult]
    pass_at_k: bool
    pass_power_k: bool
    best: SearchResult


def run_agentic_search_tool(
    host: str,
    token: str,
    workspace_id: str,
    question: str,
    expected_tool_call: dict,
    k: int = _DEFAULT_K,
    initial_conversation_id: str | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    agent_id: str | None = None,
) -> AgenticSearchSummary:
    """Run the search-tool agentic evaluation K times (single-turn each)."""
    run_results: list[SearchResult] = []

    client = ChatClient(
        host=host, token=token, workspace_id=workspace_id, reasoning_effort=reasoning_effort, agent_id=agent_id
    )
    try:
        conv_id_0 = initial_conversation_id if initial_conversation_id is not None else client.create_conversation()
        try:
            chat_result = client.send_message(conv_id_0, question)
            tcs = chat_result.tool_call_events or []
            selected = _tool_selection(tcs)
            correct = selected and _tool_correctness(tcs, expected_tool_call)
            run_results.append(
                SearchResult(
                    conversation_id=conv_id_0,
                    tool_selected=selected,
                    tool_correct=correct,
                    tool_call_names=[tc.function_name for tc in tcs],
                    reasoning_steps=list(chat_result.reasoning_steps or []),
                    response_id=chat_result.response_id,
                    tool_call_events=list(chat_result.tool_call_events or []),
                    reasoning_step_events=list(chat_result.reasoning_step_events or []),
                )
            )
        finally:
            if initial_conversation_id is None:
                client.delete_conversation(conv_id_0)

        for _ in range(1, k):
            conv_id = client.create_conversation()
            try:
                chat_result = client.send_message(conv_id, question)
                tcs = chat_result.tool_call_events or []
                selected = _tool_selection(tcs)
                correct = selected and _tool_correctness(tcs, expected_tool_call)
                run_results.append(
                    SearchResult(
                        conversation_id=conv_id,
                        tool_selected=selected,
                        tool_correct=correct,
                        tool_call_names=[tc.function_name for tc in tcs],
                        reasoning_steps=list(chat_result.reasoning_steps or []),
                        response_id=chat_result.response_id,
                        tool_call_events=list(chat_result.tool_call_events or []),
                        reasoning_step_events=list(chat_result.reasoning_step_events or []),
                    )
                )
            finally:
                client.delete_conversation(conv_id)
    finally:
        client.close()

    # Pass requires only tool_selected — tool_correct is a Langfuse quality metric.
    # This matches the original Tavern behavior where only missing the tool call failed the test.
    pass_at_k = any(r.tool_selected for r in run_results)
    pass_power_k = all(r.tool_selected for r in run_results)
    best = max(run_results, key=lambda r: (r.tool_correct, r.tool_selected))
    return AgenticSearchSummary(
        run_results=run_results,
        pass_at_k=pass_at_k,
        pass_power_k=pass_power_k,
        best=best,
    )


class SearchToolAssertionError(AgenticAssertionError):
    """Raised when a search-tool evaluation fails."""


def evaluate_agentic_search_tool(
    host: str,
    token: str,
    workspace_id: str,
    question: str,
    expected_tool_call: dict,
    k: int = _DEFAULT_K,
    initial_conversation_id: str | None = None,
    agent_id: str | None = None,
    langfuse: object | None = None,
    dataset_item_id: str = "",
    dataset_name: str = "search",
    run_timestamp: str | None = None,
    model_version_override: str | None = None,
    run_metadata_extra: dict | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    submit_trace_link: SubmitTraceLink = run_trace_link_inline,
) -> AgenticEvalOutcome:
    """Run search-tool evaluation, log to Langfuse, and raise SearchToolAssertionError on failure.

    Returns the best run's outcome (reasoning_steps, conversation_id, response_id) as an
    AgenticEvalOutcome on success; on failure the same three values are attached to the
    raised exception as ``.reasoning_steps``/``.conversation_id``/``.response_id``.
    """
    langfuse, window_start = open_trace_window(langfuse)
    summary = run_agentic_search_tool(
        host=host,
        token=token,
        workspace_id=workspace_id,
        question=question,
        expected_tool_call=expected_tool_call,
        k=k,
        initial_conversation_id=initial_conversation_id,
        reasoning_effort=reasoning_effort,
        agent_id=agent_id,
    )

    if langfuse is not None and dataset_item_id:
        # Pinned on the calling thread: a deferred poll must not widen its query window.
        window_end = utc_now()

        def _write_scores(ctx: RunTraceContext) -> None:

            for run_idx, run in enumerate(summary.run_results):
                pt = ctx.trace(run.conversation_id)
                with ctx.observe(pt, run_idx) as tid:
                    ctx.score(tid, name="tool_selection", value=float(run.tool_selected), data_type="BOOLEAN")
                    ctx.score(tid, name="tool_correctness", value=float(run.tool_correct), data_type="BOOLEAN")
                    ctx.quality(
                        tid,
                        strict_checks={"tool_selection": run.tool_selected},
                        latency_sec=pt.latency if pt else None,
                        cost_usd=pt.total_cost if pt else None,
                    )

        # Before the pass@K raise: a failing item's scores are the ones worth having.
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
            conversation_ids=[r.conversation_id for r in summary.run_results],
            window_start=window_start,
            window_end=window_end,
            suffix_runs=len(summary.run_results) > 1,
            write_scores=_write_scores,
        )

    runs_passed = sum(1 for r in summary.run_results if r.tool_selected)
    runs_effective = len(summary.run_results)

    best = summary.best
    detail = {
        "tool_selected": best.tool_selected,
        "tool_correct": best.tool_correct,
        "tool_call_names": best.tool_call_names,
        "latency_breakdown": build_latency_breakdown(best.tool_call_events, best.reasoning_step_events),
    }

    if not summary.pass_at_k:
        exc = SearchToolAssertionError(
            f"Search tool assertion failed. "
            f"tool_selected={best.tool_selected}, tool_correct={best.tool_correct}. "
            f"Tool calls made: {best.tool_call_names}"
        )
        exc.reasoning_steps = best.reasoning_steps
        exc.conversation_id = best.conversation_id
        exc.response_id = best.response_id
        exc.detail = detail
        exc.runs_passed = runs_passed
        exc.runs_effective = runs_effective
        raise exc
    return AgenticEvalOutcome(
        runs_passed=runs_passed,
        runs_effective=runs_effective,
        reasoning_steps=best.reasoning_steps,
        conversation_id=best.conversation_id,
        response_id=best.response_id,
        detail=detail,
    )

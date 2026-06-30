# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic search-tool evaluation runner (single-turn)."""

from __future__ import annotations

from dataclasses import dataclass

from gooddata_eval.core.chat.sse_client import ChatClient
from gooddata_eval.core.models import ToolCallEvent

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
) -> AgenticSearchSummary:
    """Run the search-tool agentic evaluation K times (single-turn each)."""
    run_results: list[SearchResult] = []

    client = ChatClient(host=host, token=token, workspace_id=workspace_id)
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


class SearchToolAssertionError(AssertionError):
    """Raised when a search-tool evaluation fails."""

    __tracebackhide__ = True


def evaluate_agentic_search_tool(
    host: str,
    token: str,
    workspace_id: str,
    question: str,
    expected_tool_call: dict,
    k: int = _DEFAULT_K,
    initial_conversation_id: str | None = None,
    langfuse: object | None = None,
    dataset_item_id: str = "",
    dataset_name: str = "search",
    run_timestamp: str | None = None,
    model_version_override: str | None = None,
) -> None:
    """Run search-tool evaluation, log to Langfuse, and raise SearchToolAssertionError on failure."""
    from datetime import datetime as _dt  # noqa: PLC0415
    from datetime import timezone as _tz  # noqa: PLC0415

    from gooddata_eval.core.agentic._langfuse import try_make_langfuse_client  # noqa: PLC0415

    if langfuse is None:
        langfuse = try_make_langfuse_client()
    window_start = _dt.now(_tz.utc)
    summary = run_agentic_search_tool(
        host=host,
        token=token,
        workspace_id=workspace_id,
        question=question,
        expected_tool_call=expected_tool_call,
        k=k,
        initial_conversation_id=initial_conversation_id,
    )

    if langfuse is not None and dataset_item_id:
        from gooddata_eval.core.agentic._langfuse import (  # noqa: PLC0415
            build_run_context,
            find_traces_per_conversation,
            log_quality_and_value_scores,
            observe,
            score_safe,
        )

        run_name_base, run_metadata = build_run_context(
            host,
            token,
            workspace_id,
            dataset_name,
            run_timestamp,
            model_version_override,
        )
        traces_by_conv = find_traces_per_conversation(
            langfuse,
            [r.conversation_id for r in summary.run_results],
            window_start,
        )
        suffix_needed = len(summary.run_results) > 1
        for run_idx, run in enumerate(summary.run_results):
            pt = traces_by_conv.get(run.conversation_id)
            run_name = f"{run_name_base}_run{run_idx}" if suffix_needed else run_name_base
            with observe(langfuse, pt.id if pt else None, dataset_item_id, run_name, run_metadata) as tid:
                score_safe(langfuse, tid, name="tool_selection", value=float(run.tool_selected), data_type="BOOLEAN")
                score_safe(langfuse, tid, name="tool_correctness", value=float(run.tool_correct), data_type="BOOLEAN")
                log_quality_and_value_scores(
                    langfuse,
                    tid,
                    strict_checks={"tool_selection": run.tool_selected},
                    latency_sec=pt.latency if pt else None,
                    cost_usd=pt.total_cost if pt else None,
                )

    if not summary.pass_at_k:
        best = summary.best
        raise SearchToolAssertionError(
            f"Search tool assertion failed. "
            f"tool_selected={best.tool_selected}, tool_correct={best.tool_correct}. "
            f"Tool calls made: {best.tool_call_names}"
        )

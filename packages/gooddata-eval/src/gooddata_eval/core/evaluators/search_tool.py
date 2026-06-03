# (C) 2026 GoodData Corporation
"""Evaluator for search_tool: agent must call the catalog search with expected parameters."""

from gooddata_eval.core.evaluators.base import ItemEvaluation
from gooddata_eval.core.models import ChatResult, DatasetItem


def _args_match(actual_args: dict, expected_args: dict) -> bool:
    if sorted(actual_args.get("keywords") or []) != sorted(expected_args.get("keywords") or []):
        return False
    if sorted(actual_args.get("object_types") or []) != sorted(expected_args.get("object_types") or []):
        return False
    if actual_args.get("limit") != expected_args.get("limit"):
        return False
    return actual_args.get("emit_widget") == expected_args.get("emit_widget")


class SearchToolEvaluator:
    test_kind = "search_tool"

    def evaluate(self, item: DatasetItem, chat_result: ChatResult) -> ItemEvaluation:
        expected_call = (item.expected_output or {}).get("tool_call", {})
        expected_fn = expected_call.get("function_name", "search_objects")
        expected_args = expected_call.get("function_arguments", {})

        matching_events = [ev for ev in chat_result.tool_call_events if ev.function_name == expected_fn]
        tool_selection = len(matching_events) > 0
        tool_correctness = any(_args_match(ev.parsed_arguments(), expected_args) for ev in matching_events)

        # tool_selection is the hard gate; tool_correctness is scored but not blocking
        return ItemEvaluation(
            passed=tool_selection,
            rank_key=(int(tool_selection), int(tool_correctness)),
            detail={
                "tool_selection": tool_selection,
                "tool_correctness": tool_correctness,
                "expected_function": expected_fn,
                "calls_found": len(matching_events),
            },
        )

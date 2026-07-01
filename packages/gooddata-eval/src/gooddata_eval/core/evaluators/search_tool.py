# (C) 2026 GoodData Corporation
"""Evaluator for search_tool: agent must call the catalog search with expected parameters."""

from gooddata_eval.core.evaluators.base import ItemEvaluation
from gooddata_eval.core.models import ChatResult, DatasetItem


def _normalize_str_list(value: object, *, lowercase: bool = False) -> list[str]:
    # Arguments come from raw model-emitted JSON, so a malformed tool call may
    # contain non-string entries. Drop them defensively so bad input scores as a
    # mismatch instead of raising and aborting the whole evaluation.
    if not isinstance(value, list):
        return []
    items = [item for item in value if isinstance(item, str)]
    return sorted(item.lower() if lowercase else item for item in items)


def _args_match(actual_args: dict, expected_args: dict) -> bool:
    # Only keywords and object_types determine semantic correctness.
    # limit is optional with a server-side default; emit_widget was renamed to
    # user_requested_search in the tool schema — neither affects search quality.
    actual_kw = _normalize_str_list(actual_args.get("keywords"), lowercase=True)
    expected_kw = _normalize_str_list(expected_args.get("keywords"), lowercase=True)
    if actual_kw != expected_kw:
        return False
    return _normalize_str_list(actual_args.get("object_types")) == _normalize_str_list(
        expected_args.get("object_types")
    )


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

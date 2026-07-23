# (C) 2026 GoodData Corporation
"""Evaluator for metric_skill: agent must create the correct metric via create_metric tool call."""

from gooddata_eval.core.evaluators.base import ItemEvaluation
from gooddata_eval.core.models import ChatResult, DatasetItem


def _find_create_metric(chat_result: ChatResult):
    for ev in chat_result.tool_call_events:
        if ev.function_name == "create_metric":
            return ev
    return None


def _unwrap_result(raw: dict) -> dict:
    """Unwrap the tool result payload: {"data": {...}} -> {...}."""
    return raw.get("data", raw)


class MetricSkillEvaluator:
    test_kind = "metric_skill"

    def evaluate(self, item: DatasetItem, chat_result: ChatResult) -> ItemEvaluation:
        expected = item.expected_output
        tool_event = _find_create_metric(chat_result)

        if tool_event is None:
            return ItemEvaluation(
                passed=False,
                rank_key=(False, False, False),
                detail={"metric_created": False, "maql_correct": False, "format_correct": False, "metric_id": None},
            )

        result = tool_event.parsed_result()
        payload = _unwrap_result(result) if result else {}

        actual_maql = payload.get("maql", "")
        actual_format = payload.get("format", "")
        expected_maql = expected.get("maql", "")
        expected_format = expected.get("format", "")

        maql_correct = actual_maql == expected_maql
        format_correct = actual_format == expected_format
        passed = maql_correct and format_correct

        return ItemEvaluation(
            passed=passed,
            rank_key=(passed, int(maql_correct), int(format_correct)),
            detail={
                "metric_created": True,
                "maql_correct": maql_correct,
                "format_correct": format_correct,
                "expected_maql": expected_maql,
                "actual_maql": actual_maql,
                "expected_format": expected_format,
                "actual_format": actual_format,
                # The real id of the metric this run created, straight from the
                # create_metric tool result — lets a caller (e.g. a cleanup step)
                # delete the exact object created instead of diffing the workspace
                # catalog before/after and guessing by name.
                "metric_id": payload.get("metric_id"),
            },
        )

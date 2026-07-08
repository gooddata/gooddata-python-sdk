# (C) 2026 GoodData Corporation
"""Evaluator for alert_skill: agent must create the correct metric alert."""

import re
from typing import Any

from gooddata_eval.core.evaluators._deep_subset import deep_subset
from gooddata_eval.core.evaluators.base import ItemEvaluation
from gooddata_eval.core.models import ChatResult, DatasetItem

_TRIGGER_MAP = {"Every time": "ALWAYS", "One time": "ONCE"}


def _coerce_number(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _extract_metric_id(metric_str: str) -> str | None:
    match = re.search(r"\(([^)]+)\)\s*$", metric_str)
    return match.group(1) if match else None


def _check_threshold(expected: dict, actual_args: dict) -> bool:
    operator = expected.get("Operator", "")
    if operator == "ANOMALY":
        return True
    if "Threshold_from" in expected or "Threshold_to" in expected:
        exp_from = _coerce_number(expected.get("Threshold_from"))
        exp_to = _coerce_number(expected.get("Threshold_to"))
        act_from = _coerce_number(
            actual_args["threshold_from"] if "threshold_from" in actual_args else actual_args.get("from")
        )
        act_to = _coerce_number(actual_args["threshold_to"] if "threshold_to" in actual_args else actual_args.get("to"))
        return exp_from == act_from and exp_to == act_to
    if "Threshold" in expected:
        exp = _coerce_number(expected["Threshold"])
        act = _coerce_number(actual_args["threshold"] if "threshold" in actual_args else actual_args.get("value"))
        return exp == act
    return True


class AlertSkillEvaluator:
    test_kind = "alert_skill"

    def evaluate(self, item: DatasetItem, chat_result: ChatResult) -> ItemEvaluation:
        expected = item.expected_output
        tool_event = next(
            (ev for ev in chat_result.tool_call_events if ev.function_name == "create_metric_alert"),
            None,
        )

        if tool_event is None:
            return ItemEvaluation(
                passed=False,
                rank_key=(False,) * 7,
                detail={"alert_created": False},
            )

        args = tool_event.parsed_arguments()

        operator_correct = True
        threshold_correct = True
        trigger_correct = True
        filters_correct = True
        metric_correct = True
        recipients_correct = True

        if "Operator" in expected:
            operator_correct = args.get("operator") == expected["Operator"]

        if any(k in expected for k in ("Threshold", "Threshold_from", "Threshold_to")):
            threshold_correct = _check_threshold(expected, args)

        if "Trigger" in expected:
            expected_trigger = _TRIGGER_MAP.get(expected["Trigger"], expected["Trigger"])
            # Omitted/null trigger persists as the product default ALWAYS ("Every time").
            actual_trigger = args.get("trigger") or "ALWAYS"
            trigger_correct = actual_trigger == expected_trigger

        if "Filters" in expected:
            actual_filters = args.get("filters") or []
            filters_correct = deep_subset(expected["Filters"], actual_filters)

        if "Metric" in expected:
            expected_id = _extract_metric_id(expected["Metric"])
            actual_metric = args.get("metric") or args.get("metricId") or args.get("metric_id")
            metric_correct = expected_id is not None and actual_metric == expected_id

        if "Recipient(s)" in expected:
            exp_recips = sorted(r.strip() for r in expected["Recipient(s)"].split(",") if r.strip())
            act_recips = sorted(args.get("recipients") or args.get("externalRecipients") or [])
            recipients_correct = exp_recips == act_recips

        passed = all(
            [
                operator_correct,
                threshold_correct,
                trigger_correct,
                filters_correct,
                metric_correct,
                recipients_correct,
            ]
        )

        return ItemEvaluation(
            passed=passed,
            rank_key=(
                passed,
                int(operator_correct),
                int(threshold_correct),
                int(trigger_correct),
                int(filters_correct),
                int(metric_correct),
                int(recipients_correct),
            ),
            detail={
                "alert_created": True,
                "operator_correct": operator_correct,
                "threshold_correct": threshold_correct,
                "trigger_correct": trigger_correct,
                "filters_correct": filters_correct,
                "metric_correct": metric_correct,
                "recipients_correct": recipients_correct,
            },
        )

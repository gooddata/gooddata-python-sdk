# (C) 2026 GoodData Corporation
import json

from gooddata_eval.core.evaluators import get_evaluator
from gooddata_eval.core.models import ChatResult, DatasetItem


def _item(expected_output: dict) -> DatasetItem:
    return DatasetItem(
        id="alert-001",
        dataset_name="d",
        test_kind="alert_skill",
        question="Alert me when revenue drops below 20000.",
        expected_output=expected_output,
    )


def _chat_with_alert(args: dict) -> ChatResult:
    return ChatResult.model_validate(
        {
            "toolCallEvents": [
                {"functionName": "create_metric_alert", "functionArguments": json.dumps(args), "result": "{}"}
            ]
        }
    )


def test_alert_evaluator_passes_on_exact_match():
    expected = {
        "Operator": "LESS_THAN",
        "Threshold": "20000",
        "Trigger": "Every time",
        "Metric": "Revenue (revenue)",
    }
    actual_args = {
        "operator": "LESS_THAN",
        "threshold": 20000,
        "trigger": "ALWAYS",
        "metric": "revenue",
    }
    result = get_evaluator("alert_skill").evaluate(_item(expected), _chat_with_alert(actual_args))
    assert result.passed is True


def test_alert_evaluator_fails_wrong_operator():
    expected = {"Operator": "LESS_THAN", "Threshold": "20000", "Trigger": "Every time"}
    actual_args = {"operator": "GREATER_THAN", "threshold": 20000, "trigger": "ALWAYS"}
    result = get_evaluator("alert_skill").evaluate(_item(expected), _chat_with_alert(actual_args))
    assert result.passed is False
    assert result.detail["operator_correct"] is False


def test_alert_evaluator_skips_absent_field():
    # Threshold not in expected -> not checked -> passes despite wrong threshold in actual
    expected = {"Operator": "LESS_THAN", "Trigger": "Every time"}
    actual_args = {"operator": "LESS_THAN", "trigger": "ALWAYS", "threshold": 99999}
    result = get_evaluator("alert_skill").evaluate(_item(expected), _chat_with_alert(actual_args))
    assert result.passed is True


def test_alert_evaluator_defaults_missing_trigger_to_always():
    # The agent may omit `trigger` (or send null) -> backend default is ALWAYS,
    # so an "Every time" expectation must still pass instead of a false-negative.
    expected = {"Operator": "GREATER_THAN", "Threshold": "150", "Trigger": "Every time"}
    ev = get_evaluator("alert_skill")

    absent = ev.evaluate(_item(expected), _chat_with_alert({"operator": "GREATER_THAN", "threshold": 150}))
    assert absent.passed is True
    assert absent.detail["trigger_correct"] is True

    null = ev.evaluate(
        _item(expected), _chat_with_alert({"operator": "GREATER_THAN", "threshold": 150, "trigger": None})
    )
    assert null.passed is True
    assert null.detail["trigger_correct"] is True


def test_alert_evaluator_fails_when_no_tool_call():
    result = get_evaluator("alert_skill").evaluate(
        _item({"Operator": "LESS_THAN"}), ChatResult.model_validate({"textResponse": "here is the alert"})
    )
    assert result.passed is False
    assert result.detail["alert_created"] is False

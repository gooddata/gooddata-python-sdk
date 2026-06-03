# (C) 2026 GoodData Corporation
from gooddata_eval.core.evaluators import get_evaluator
from gooddata_eval.core.models import ChatResult, DatasetItem


def _item():
    return DatasetItem(
        id="metric-001",
        dataset_name="d",
        test_kind="metric_skill",
        question="Create a metric for average order value.",
        expected_output={
            "maql": "SELECT AVG({metric/order_value})",
            "format": "#,##0.00",
        },
    )


def _chat_with_metric(maql: str, fmt: str) -> ChatResult:
    result_json = (
        f'{{"data": {{"maql": "{maql}", "format": "{fmt}", '
        f'"metric_id": "avg_order_value", "title": "Average Order Value"}}}}'
    )
    return ChatResult.model_validate(
        {"toolCallEvents": [{"functionName": "create_metric", "functionArguments": "{}", "result": result_json}]}
    )


def test_metric_evaluator_passes_on_exact_match():
    ev = get_evaluator("metric_skill")
    result = ev.evaluate(_item(), _chat_with_metric("SELECT AVG({metric/order_value})", "#,##0.00"))
    assert result.passed is True
    assert result.detail["maql_correct"] is True
    assert result.detail["format_correct"] is True


def test_metric_evaluator_fails_wrong_maql():
    ev = get_evaluator("metric_skill")
    result = ev.evaluate(_item(), _chat_with_metric("SELECT {metric/order_value}", "#,##0.00"))
    assert result.passed is False
    assert result.detail["maql_correct"] is False
    assert result.detail["format_correct"] is True


def test_metric_evaluator_fails_when_no_tool_call():
    ev = get_evaluator("metric_skill")
    empty = ChatResult.model_validate({"textResponse": "here is how to create it"})
    result = ev.evaluate(_item(), empty)
    assert result.passed is False
    assert result.detail["metric_created"] is False

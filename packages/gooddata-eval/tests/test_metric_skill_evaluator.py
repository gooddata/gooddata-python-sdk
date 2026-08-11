# (C) 2026 GoodData Corporation
from unittest.mock import Mock

import pytest
from gooddata_eval.core.agentic.metric_skill import EvalEnvironmentError, _assert_expected_metrics_absent
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
    assert result.detail["metric_id"] == "avg_order_value"


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
    assert result.detail["metric_id"] is None


def _sdk_with_metrics(*metric_ids: str) -> Mock:
    sdk = Mock()
    sdk._client.entities_api.get_all_entities_metrics.return_value = Mock(data=[Mock(id=mid) for mid in metric_ids])
    return sdk


def test_precheck_passes_on_clean_workspace():
    _assert_expected_metrics_absent(_sdk_with_metrics("net_sales"), "ws", [{"metric_id": "average_order_value"}])


def test_precheck_rejects_leftover_metric():
    sdk = _sdk_with_metrics("net_sales", "average_order_value")
    with pytest.raises(EvalEnvironmentError, match="average_order_value"):
        _assert_expected_metrics_absent(sdk, "ws", [{"metric_id": "average_order_value"}])


def test_precheck_is_not_an_assertion_error():
    assert not issubclass(EvalEnvironmentError, AssertionError)


def test_precheck_skips_when_metric_listing_fails():
    sdk = Mock()
    sdk._client.entities_api.get_all_entities_metrics.side_effect = RuntimeError("boom")
    _assert_expected_metrics_absent(sdk, "ws", [{"metric_id": "average_order_value"}])


def test_precheck_noop_without_expected_metric_id():
    sdk = Mock()
    _assert_expected_metrics_absent(sdk, "ws", [{"maql": "SELECT 1"}])
    sdk._client.entities_api.get_all_entities_metrics.assert_not_called()

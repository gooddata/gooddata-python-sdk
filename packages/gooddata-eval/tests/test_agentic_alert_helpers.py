# (C) 2026 GoodData Corporation
"""Tests for the pure helper functions in agentic/alert_skill.py.

These cover the matching/parsing logic that the alert-skill run loop relies on,
independent of any ChatClient.
"""
import json

from gooddata_eval.core.agentic._catalog import CatalogMetricAlert
from gooddata_eval.core.agentic.alert_skill import (
    _check_filters,
    _check_metric,
    _check_recipients,
    _check_threshold,
    _check_trigger,
    _deep_subset,
    _extract_alert_call,
    _is_asking_clarification,
    _normalize_expected_output,
    _parse_metric_id,
    _parse_recipients,
    _to_number,
)
from gooddata_eval.core.models import ToolCallEvent


def test_to_number_coerces_int_float_and_none():
    assert _to_number("10") == 10
    assert _to_number("10.5") == 10.5
    assert _to_number(None) is None
    assert _to_number("not-a-number") is None


def test_parse_metric_id_extracts_trailing_parenthetical():
    assert _parse_metric_id("Revenue (revenue)") == "revenue"
    assert _parse_metric_id("no parens") is None
    assert _parse_metric_id(None) is None


def test_parse_recipients_splits_on_comma_and_semicolon():
    assert _parse_recipients("a@x.com, b@x.com; c@x.com") == ["a@x.com", "b@x.com", "c@x.com"]
    assert _parse_recipients(None) is None


def test_deep_subset():
    assert _deep_subset({"a": 1}, {"a": 1, "b": 2}) is True
    assert _deep_subset({"a": 2}, {"a": 1}) is False
    assert _deep_subset([1, 2], [1, 2]) is True
    assert _deep_subset([1], [1, 2]) is False  # length mismatch


def test_check_threshold_single_and_between():
    single = CatalogMetricAlert(operator="LESS_THAN", threshold=100)
    assert _check_threshold(single, {"threshold": "100"}) is True
    assert _check_threshold(single, {"threshold": 99}) is False

    between = CatalogMetricAlert(operator="BETWEEN", threshold_from=1, threshold_to=10)
    assert _check_threshold(between, {"from_value": 1, "to_value": 10}) is True
    assert _check_threshold(between, {"fromValue": 1, "toValue": 9}) is False


def test_check_trigger_always_and_mapped():
    always = CatalogMetricAlert(trigger="ALWAYS")
    assert _check_trigger(always, {"trigger": "ALWAYS"}) is True
    assert _check_trigger(always, {"trigger": "Every time"}) is True
    once = CatalogMetricAlert(trigger="ONCE")
    assert _check_trigger(once, {"trigger": "One time"}) is True  # display mapped to API
    assert _check_trigger(once, {"trigger": "ALWAYS"}) is False


def test_check_filters_metric_recipients():
    no_filter = CatalogMetricAlert()
    assert _check_filters(no_filter, {}) is True  # nothing expected
    with_filter = CatalogMetricAlert(filters=[{"k": "v"}])
    assert _check_filters(with_filter, {"filters": [{"k": "v"}]}) is True
    assert _check_filters(with_filter, {}) is False

    metric = CatalogMetricAlert(metric_id="revenue")
    assert _check_metric(metric, {"metric_id": "Revenue (revenue)"}) is True
    assert _check_metric(metric, {"metricId": "other"}) is False

    recips = CatalogMetricAlert(recipients=["a@x.com"])
    assert _check_recipients(recips, {"recipients": ["a@x.com"]}) is True
    assert _check_recipients(recips, {"external_recipients": json.dumps(["a@x.com"])}) is True
    assert _check_recipients(recips, {"recipients": ["b@x.com"]}) is False


def test_normalize_expected_output_display_format():
    alert = _normalize_expected_output(
        {
            "Operator": "LESS_THAN",
            "Threshold": 10000,
            "Trigger": "Every time",
            "Metric": "Revenue (revenue)",
            "Recipient(s)": "a@x.com; b@x.com",
            "Time window/Filters": "All time",
        }
    )
    assert alert.operator == "LESS_THAN"
    assert alert.metric_id == "revenue"
    assert alert.recipients == ["a@x.com", "b@x.com"]
    assert alert.filters is None  # "All time" → no filter


def test_extract_alert_call():
    events = [
        ToolCallEvent.model_validate(
            {
                "functionName": "create_metric_alert",
                "functionArguments": json.dumps({"operator": "LESS_THAN"}),
                "result": json.dumps({"data": {"id": "alert-99"}}),
            }
        )
    ]
    alert_id, args, called = _extract_alert_call(events)
    assert called is True
    assert alert_id == "alert-99"
    assert args["operator"] == "LESS_THAN"

    none_id, none_args, not_called = _extract_alert_call([])
    assert not_called is False and none_id is None and none_args == {}


def test_is_asking_clarification():
    assert _is_asking_clarification("Which metric?") is True
    assert _is_asking_clarification("Could you specify") is True
    assert _is_asking_clarification("") is False
    assert _is_asking_clarification("Done.") is False

# (C) 2026 GoodData Corporation
from __future__ import annotations

from gooddata_sdk import (
    Attribute,
    CompoundMetricValueFilter,
    MetricValueComparisonCondition,
    MetricValueRangeCondition,
)
from gooddata_sdk.compute.model.base import ObjId


def test_compound_metric_value_filter_to_api_model():
    f = CompoundMetricValueFilter(
        metric="local_id1",
        conditions=[
            MetricValueComparisonCondition(operator="GREATER_THAN", value=10),
            MetricValueRangeCondition(operator="BETWEEN", from_value=2, to_value=3),
        ],
        treat_nulls_as=0,
    )

    assert f.is_noop() is False
    assert f.as_api_model().to_dict() == {
        "compound_measure_value_filter": {
            "conditions": [
                {"comparison": {"operator": "GREATER_THAN", "value": 10.0}},
                {"range": {"_from": 2.0, "operator": "BETWEEN", "to": 3.0}},
            ],
            "measure": {"local_identifier": "local_id1"},
            "treat_null_values_as": 0,
        }
    }


def test_compound_metric_value_filter_noop_when_no_conditions():
    f = CompoundMetricValueFilter(metric=ObjId(type="metric", id="metric.id"), conditions=[])
    assert f.is_noop() is True


def test_compound_metric_value_filter_with_dimensionality_to_api_model():
    f = CompoundMetricValueFilter(
        metric="local_id1",
        conditions=[
            MetricValueComparisonCondition(operator="GREATER_THAN", value=10),
        ],
        dimensionality=["local_id3", Attribute(local_id="local_id4", label="label.id")],
    )

    assert f.dimensionality == ["local_id3", "local_id4"]
    assert f.as_api_model().to_dict() == {
        "compound_measure_value_filter": {
            "conditions": [
                {"comparison": {"operator": "GREATER_THAN", "value": 10.0}},
            ],
            "dimensionality": [
                {"local_identifier": "local_id3"},
                {"local_identifier": "local_id4"},
            ],
            "measure": {"local_identifier": "local_id1"},
        }
    }


def test_compound_metric_value_filter_with_dimensionality_mixed_ids():
    f = CompoundMetricValueFilter(
        metric="local_id1",
        conditions=[
            MetricValueComparisonCondition(operator="GREATER_THAN", value=10),
        ],
        dimensionality=["local_id3", ObjId(type="label", id="label.id")],
        treat_nulls_as=0,
    )

    assert f.as_api_model().to_dict() == {
        "compound_measure_value_filter": {
            "conditions": [
                {"comparison": {"operator": "GREATER_THAN", "value": 10.0}},
            ],
            "dimensionality": [
                {"local_identifier": "local_id3"},
                {"identifier": {"id": "label.id", "type": "label"}},
            ],
            "measure": {"local_identifier": "local_id1"},
            "treat_null_values_as": 0,
        }
    }


def test_compound_metric_value_filter_without_dimensionality_omits_field():
    f = CompoundMetricValueFilter(
        metric="local_id1",
        conditions=[
            MetricValueComparisonCondition(operator="GREATER_THAN", value=10),
        ],
    )

    assert f.dimensionality is None
    assert "dimensionality" not in f.as_api_model().to_dict()["compound_measure_value_filter"]

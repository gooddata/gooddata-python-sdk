# (C) 2021 GoodData Corporation
from __future__ import annotations

import json
import os

import pytest
from gooddata_sdk import AllMetricValueFilter, Attribute, MetricValueFilter, ObjId, SimpleMetric

_current_dir = os.path.dirname(os.path.abspath(__file__))


def _scenario_to_snapshot_name(scenario: str):
    return f"{scenario.replace(' ', '_')}.snapshot.json"


_simple_measure = SimpleMetric(local_id="local_id2", item=ObjId(type="metric", id="metric_id"))
_attribute = Attribute(local_id="local_id4", label="label.id")

description_labels = {
    "local_id1": "Local ID",
    "metric.id": "Metric ID",
}

test_metric_value_filter = [
    [
        "comparison filter using local id",
        MetricValueFilter(
            metric="local_id1",
            operator="EQUAL_TO",
            values=10,
        ),
        "Local ID: = 10.0",
    ],
    [
        "comparison filter using object id",
        MetricValueFilter(
            metric=ObjId(type="metric", id="metric.id"),
            operator="EQUAL_TO",
            values=10.0,
        ),
        "Metric ID: = 10.0",
    ],
    [
        "comparison filter with treat nulls as",
        MetricValueFilter(metric="local_id1", operator="EQUAL_TO", values=10, treat_nulls_as=1),
        "Local ID: = 10.0",
    ],
    [
        "range filter",
        MetricValueFilter(metric="local_id1", operator="BETWEEN", values=(2, 3)),
        "Local ID: between 2 - 3",
    ],
    [
        "range filter with treat nulls as",
        MetricValueFilter(metric="local_id1", operator="BETWEEN", values=(2, 3), treat_nulls_as=1),
        "Local ID: between 2 - 3",
    ],
]


@pytest.mark.parametrize("scenario,filter", [sublist[:2] for sublist in test_metric_value_filter])
def test_attribute_filters_to_api_model(scenario, filter, snapshot):
    # it is essential to define snapshot dir using absolute path, otherwise snapshots cannot be found when
    # running in tox
    snapshot.snapshot_dir = os.path.join(_current_dir, "metric_value_filter")

    snapshot.assert_match(
        json.dumps(filter.as_api_model().to_dict(), indent=4, sort_keys=True) + "\n",
        _scenario_to_snapshot_name(scenario),
    )


@pytest.mark.parametrize("scenario,filter,description", test_metric_value_filter)
def test_date_filters_description(scenario, filter, description):
    assert filter.description(description_labels) == description


def test_all_metric_value_filter_description():
    assert AllMetricValueFilter(metric="local_id1").description(description_labels) == "Local ID: All"
    assert (
        AllMetricValueFilter(metric=ObjId(type="metric", id="metric.id")).description(description_labels)
        == "Metric ID: All"
    )


def test_cannot_create_api_model_from_all_metric_value_filter():
    """
    Analogy to AllTimeFilter test_cannot_create_api_model_from_all_time_filter() in test_date_filters.py
    """
    with pytest.raises(NotImplementedError):
        f = AllMetricValueFilter(metric="local_id1")
        f.as_api_model()

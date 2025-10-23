# (C) 2021 GoodData Corporation
from __future__ import annotations

import json
import os

import pytest
from gooddata_sdk import ObjId, PositiveAttributeFilter, SimpleMetric

_current_dir = os.path.dirname(os.path.abspath(__file__))


def _scenario_to_snapshot_name(scenario: str):
    return f"{scenario.replace(' ', '_')}.snapshot.json"


test_simple_metrics = [
    [
        "simple metric using MAQL metric",
        SimpleMetric(local_id="test", item=ObjId(type="metric", id="metric_id")),
    ],
    [
        "simple metric using MAQL metric and compute ratio",
        SimpleMetric(
            local_id="test",
            item=ObjId(type="metric", id="metric_id"),
            compute_ratio=True,
        ),
    ],
    [
        "simple metric using fact and default agg",
        SimpleMetric(local_id="test", item=ObjId(type="fact", id="fact_id")),
    ],
    [
        "simple metric using fact and custom agg",
        SimpleMetric(local_id="test", item=ObjId(type="fact", id="fact_id"), aggregation="AVG"),
    ],
    [
        "simple metric using fact compute ratio",
        SimpleMetric(local_id="test", item=ObjId(type="fact", id="fact_id"), compute_ratio=True),
    ],
    [
        "simple metric with filters",
        SimpleMetric(
            local_id="test",
            item=ObjId(type="fact", id="fact_id"),
            filters=[PositiveAttributeFilter(label="label_local_id", values=["val1", "val2"])],
        ),
    ],
]


@pytest.mark.parametrize("scenario,metric", test_simple_metrics)
def test_simple_metric_to_api_model(scenario, metric: SimpleMetric, snapshot):
    # it is essential to define snapshot dir using absolute path, otherwise snapshots cannot be found when
    # running in tox
    snapshot.snapshot_dir = os.path.join(_current_dir, "simple_metric")

    snapshot.assert_match(
        json.dumps(metric.as_api_model().to_dict(), indent=4, sort_keys=True),
        _scenario_to_snapshot_name(scenario),
    )

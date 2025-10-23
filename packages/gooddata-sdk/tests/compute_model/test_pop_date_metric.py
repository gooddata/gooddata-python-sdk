# (C) 2021 GoodData Corporation
from __future__ import annotations

import json
import os

import pytest
from gooddata_sdk import Attribute, ObjId, PopDate, PopDateMetric, SimpleMetric

_current_dir = os.path.dirname(os.path.abspath(__file__))
_simple_metric = SimpleMetric(local_id="master_metric_id", item=ObjId(type="metric", id="metric_id"))
_attribute = Attribute(local_id="local_id4", label="label2.id")


def _scenario_to_snapshot_name(scenario: str):
    return f"{scenario.replace(' ', '_')}.snapshot.json"


test_pop_date_metrics = [
    [
        "with master metric by local id",
        PopDateMetric(
            local_id="local_id1",
            metric="master_metric_id",
            date_attributes=[PopDate(attribute=ObjId(type="label", id="label.id"), periods_ago=1)],
        ),
    ],
    [
        "with master metric passed by value",
        PopDateMetric(
            local_id="local_id1",
            metric=_simple_metric,
            date_attributes=[PopDate(attribute=ObjId(type="label", id="label.id"), periods_ago=1)],
        ),
    ],
    [
        "with date attribute passed by value",
        PopDateMetric(
            local_id="local_id1",
            metric=_simple_metric,
            date_attributes=[PopDate(attribute=_attribute, periods_ago=1)],
        ),
    ],
    [
        "with multiple pop date attributes",
        PopDateMetric(
            local_id="local_id1",
            metric=_simple_metric,
            date_attributes=[
                PopDate(attribute=ObjId(type="label", id="label1.id"), periods_ago=1),
                PopDate(attribute=_attribute, periods_ago=2),
            ],
        ),
    ],
]


@pytest.mark.parametrize("scenario,metric", test_pop_date_metrics)
def test_simple_metric_to_api_model(scenario, metric: PopDateMetric, snapshot):
    # it is essential to define snapshot dir using absolute path, otherwise snapshots cannot be found when
    # running in tox
    snapshot.snapshot_dir = os.path.join(_current_dir, "pop_date_metric")

    snapshot.assert_match(
        json.dumps(metric.as_api_model().to_dict(), indent=4, sort_keys=True),
        _scenario_to_snapshot_name(scenario),
    )

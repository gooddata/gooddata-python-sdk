# (C) 2021 GoodData Corporation
from __future__ import annotations

import json
import os

import pytest
from gooddata_sdk import ObjId, PopDateDataset, PopDatesetMetric, SimpleMetric

_current_dir = os.path.dirname(os.path.abspath(__file__))
_simple_metric = SimpleMetric(local_id="master_metric_id", item=ObjId(type="metric", id="metric_id"))


def _scenario_to_snapshot_name(scenario: str):
    return f"{scenario.replace(' ', '_')}.snapshot.json"


test_pop_date_metrics = [
    [
        "with master metric by local id",
        PopDatesetMetric(
            local_id="local_id1",
            metric="master_metric_id",
            date_datasets=[PopDateDataset(dataset=ObjId(type="dataset", id="dataset.id"), periods_ago=1)],
        ),
    ],
    [
        "with master metric passed by value",
        PopDatesetMetric(
            local_id="local_id1",
            metric=_simple_metric,
            date_datasets=[PopDateDataset(dataset=ObjId(type="dataset", id="dataset.id"), periods_ago=1)],
        ),
    ],
    [
        "with date dataset by str",
        PopDatesetMetric(
            local_id="local_id1",
            metric="master_metric_id",
            date_datasets=[PopDateDataset(dataset="dataset.id", periods_ago=1)],
        ),
    ],
    [
        "with multiple date datasets",
        PopDatesetMetric(
            local_id="local_id1",
            metric="master_metric_id",
            date_datasets=[
                PopDateDataset(dataset=ObjId(type="dataset", id="dataset1.id"), periods_ago=1),
                PopDateDataset(dataset="dataset2.id", periods_ago=2),
            ],
        ),
    ],
]


@pytest.mark.parametrize("scenario,metric", test_pop_date_metrics)
def test_simple_metric_to_api_model(scenario, metric: PopDatesetMetric, snapshot):
    # it is essential to define snapshot dir using absolute path, otherwise snapshots cannot be found when
    # running in tox
    snapshot.snapshot_dir = os.path.join(_current_dir, "pop_dataset_metric")

    snapshot.assert_match(
        json.dumps(metric.as_api_model().to_dict(), indent=4, sort_keys=True),
        _scenario_to_snapshot_name(scenario),
    )

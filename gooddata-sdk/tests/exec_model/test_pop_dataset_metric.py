import json
import os

import pytest

from gooddata_sdk import (
    PopDatesetMeasure,
    PopDateDataset,
    ObjId,
    SimpleMeasure,
)

_current_dir = os.path.dirname(os.path.abspath(__file__))
_simple_metric = SimpleMeasure(
    local_id="master_metric_id", item=ObjId(type="metric", id="metric_id")
)


def _scenario_to_snapshot_name(scenario: str):
    return f"{scenario.replace(' ', '_')}.snapshot.json"


test_pop_date_metrics = [
    [
        "with master metric by local id",
        PopDatesetMeasure(
            local_id="local_id1",
            measure="master_metric_id",
            date_datasets=[
                PopDateDataset(
                    dataset=ObjId(type="dataset", id="dataset.id"), periods_ago=1
                )
            ],
        ),
    ],
    [
        "with master metric passed by value",
        PopDatesetMeasure(
            local_id="local_id1",
            measure=_simple_metric,
            date_datasets=[
                PopDateDataset(
                    dataset=ObjId(type="dataset", id="dataset.id"), periods_ago=1
                )
            ],
        ),
    ],
    [
        "with date dataset by str",
        PopDatesetMeasure(
            local_id="local_id1",
            measure="master_metric_id",
            date_datasets=[PopDateDataset(dataset="dataset.id", periods_ago=1)],
        ),
    ],
    [
        "with multiple date datasets",
        PopDatesetMeasure(
            local_id="local_id1",
            measure="master_metric_id",
            date_datasets=[
                PopDateDataset(
                    dataset=ObjId(type="dataset", id="dataset1.id"), periods_ago=1
                ),
                PopDateDataset(dataset="dataset2.id", periods_ago=2),
            ],
        ),
    ],
]


@pytest.mark.parametrize("scenario,metric", test_pop_date_metrics)
def test_simple_metric_to_api_model(scenario, metric: PopDatesetMeasure, snapshot):
    # it is essential to define snapshot dir using absolute path, otherwise snapshots cannot be found when
    # running in tox
    snapshot.snapshot_dir = os.path.join(_current_dir, "pop_dataset_metric")

    snapshot.assert_match(
        json.dumps(metric.as_api_model().to_dict(), indent=4, sort_keys=True),
        _scenario_to_snapshot_name(scenario),
    )

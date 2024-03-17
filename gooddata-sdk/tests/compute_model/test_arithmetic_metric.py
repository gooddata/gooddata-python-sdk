# (C) 2021 GoodData Corporation
from __future__ import annotations

import json
import os

import pytest
from gooddata_sdk import ArithmeticMetric, ObjId, SimpleMetric

_current_dir = os.path.dirname(os.path.abspath(__file__))


def _scenario_to_snapshot_name(scenario: str):
    return f"{scenario.replace(' ', '_')}.snapshot.json"


_simple_metric1 = SimpleMetric(local_id="local_id1", item=ObjId(type="metric", id="metric1.id"))
_simple_metric2 = SimpleMetric(local_id="local_id2", item=ObjId(type="metric", id="metric2.id"))


test_arithmetic_metric = [
    [
        "with operands using local id",
        ArithmeticMetric(
            local_id="arithmetic_local_id",
            operator="SUM",
            operands=["local_id1", "local_id2"],
        ),
    ],
    [
        "with operands using metrics by value",
        ArithmeticMetric(
            local_id="arithmetic_local_id",
            operator="SUM",
            operands=[_simple_metric1, _simple_metric2],
        ),
    ],
]


@pytest.mark.parametrize("scenario,metric", test_arithmetic_metric)
def test_attribute_filters_to_api_model(scenario, metric, snapshot):
    # it is essential to define snapshot dir using absolute path, otherwise snapshots cannot be found when
    # running in tox
    snapshot.snapshot_dir = os.path.join(_current_dir, "arithmetic_metric")

    snapshot.assert_match(
        json.dumps(metric.as_api_model().to_dict(), indent=4, sort_keys=True),
        _scenario_to_snapshot_name(scenario),
    )

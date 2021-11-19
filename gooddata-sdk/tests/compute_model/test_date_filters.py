# (C) 2021 GoodData Corporation
from __future__ import annotations

import json
import os

import pytest

from gooddata_sdk import AbsoluteDateFilter, AllTimeFilter, ObjId, RelativeDateFilter

_current_dir = os.path.dirname(os.path.abspath(__file__))


def _scenario_to_snapshot_name(scenario: str):
    return f"{scenario.replace(' ', '_')}.snapshot.json"


test_filters = [
    [
        "absolute date filter",
        AbsoluteDateFilter(
            dataset=ObjId(type="dataset", id="dataset.id"),
            from_date="2021/1/1",
            to_date="2021/1/2",
        ),
    ],
    [
        "relative date filter",
        RelativeDateFilter(
            dataset=ObjId(type="dataset", id="dataset.id"),
            granularity="DAY",
            from_shift=-10,
            to_shift=-1,
        ),
    ],
]


@pytest.mark.parametrize("scenario,filter", test_filters)
def test_attribute_filters_to_api_model(scenario, filter, snapshot):
    # it is essential to define snapshot dir using absolute path, otherwise snapshots cannot be found when
    # running in tox
    snapshot.snapshot_dir = os.path.join(_current_dir, "date_filters")

    snapshot.assert_match(
        json.dumps(filter.as_api_model().to_dict(), indent=4, sort_keys=True),
        _scenario_to_snapshot_name(scenario),
    )


def test_cannot_create_api_model_from_all_time_filter():
    """As All time filter from GoodData.CN does not contain from and to fields,
    we are not sure how to make valid model from it. We prefer to fail, until
    we decide what to do with this situation.
    """
    with pytest.raises(NotImplementedError):
        f = AllTimeFilter()
        f.as_api_model()

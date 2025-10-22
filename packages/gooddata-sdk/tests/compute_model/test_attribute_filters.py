# (C) 2021 GoodData Corporation
from __future__ import annotations

import json
import os

import pytest
from gooddata_sdk import NegativeAttributeFilter, ObjId, PositiveAttributeFilter

_current_dir = os.path.dirname(os.path.abspath(__file__))


def _scenario_to_snapshot_name(scenario: str):
    return f"{scenario.replace(' ', '_')}.snapshot.json"


description_labels = {
    "label.id": "Label ID",
    "local_id": "Local ID",
}

test_filters = [
    ["empty positive attribute filter", PositiveAttributeFilter(label="local_id"), "Local ID: All"],
    [
        "positive filter using local id",
        PositiveAttributeFilter(label="local_id", values=["val1", "val2"]),
        "Local ID: val1, val2",
    ],
    [
        "positive filter using object id",
        PositiveAttributeFilter(label=ObjId(type="label", id="label.id"), values=["val1", "val2"]),
        "Label ID: val1, val2",
    ],
    [
        "empty negative attribute filter",
        NegativeAttributeFilter(label="local_id", values=[]),
        "Local ID: All",
    ],
    [
        "negative filter using local id",
        NegativeAttributeFilter(label="local_id", values=["val1", "val2"]),
        "Local ID: All except val1, val2",
    ],
    [
        "negative filter using object id",
        NegativeAttributeFilter(label=ObjId(type="label", id="label.id"), values=["val1", "val2"]),
        "Label ID: All except val1, val2",
    ],
]


@pytest.mark.parametrize("scenario,filter", [sublist[:2] for sublist in test_filters])
def test_attribute_filters_to_api_model(scenario, filter, snapshot):
    # it is essential to define snapshot dir using absolute path, otherwise snapshots cannot be found when
    # running in tox
    snapshot.snapshot_dir = os.path.join(_current_dir, "attribute_filters")

    snapshot.assert_match(
        json.dumps(filter.as_api_model().to_dict(), indent=4, sort_keys=True),
        _scenario_to_snapshot_name(scenario),
    )


@pytest.mark.parametrize("scenario,filter,description", test_filters)
def test_attribute_filters_description(scenario, filter, description):
    assert filter.description(description_labels) == description


def test_empty_negative_filter_is_noop():
    f = NegativeAttributeFilter(label="test", values=[])

    assert f.is_noop() is True


def test_empty_positive_filter_is_not_noop():
    f = PositiveAttributeFilter(label="test")

    assert f.is_noop() is False

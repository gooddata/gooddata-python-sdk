# (C) 2021 GoodData Corporation
from __future__ import annotations

import json
import os

import pytest
from gooddata_sdk import MatchAttributeFilter, NegativeAttributeFilter, ObjId, PositiveAttributeFilter

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
    # running from a different working directory
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


test_match_filters = [
    [
        "match contains filter using local id",
        MatchAttributeFilter(label="local_id", literal="foo", match_type="CONTAINS"),
        "Local ID: contains foo",
    ],
    [
        "match contains filter using object id",
        MatchAttributeFilter(label=ObjId(type="label", id="label.id"), literal="bar", match_type="CONTAINS"),
        "Label ID: contains bar",
    ],
    [
        "match starts with filter",
        MatchAttributeFilter(label="local_id", literal="prefix", match_type="STARTS_WITH"),
        "Local ID: starts with prefix",
    ],
    [
        "match ends with filter",
        MatchAttributeFilter(label="local_id", literal="suffix", match_type="ENDS_WITH"),
        "Local ID: ends with suffix",
    ],
    [
        "negated contains filter",
        MatchAttributeFilter(label="local_id", literal="foo", match_type="CONTAINS", negate=True),
        "Local ID: not contains foo",
    ],
    [
        "negated starts with filter",
        MatchAttributeFilter(label="local_id", literal="prefix", match_type="STARTS_WITH", negate=True),
        "Local ID: not starts with prefix",
    ],
    [
        "negated ends with filter",
        MatchAttributeFilter(label="local_id", literal="suffix", match_type="ENDS_WITH", negate=True),
        "Local ID: not ends with suffix",
    ],
    [
        "case sensitive contains filter",
        MatchAttributeFilter(label="local_id", literal="Foo", match_type="CONTAINS", case_sensitive=True),
        "Local ID: contains Foo",
    ],
    [
        "negated case sensitive starts with filter",
        MatchAttributeFilter(
            label="local_id", literal="Pre", match_type="STARTS_WITH", negate=True, case_sensitive=True
        ),
        "Local ID: not starts with Pre",
    ],
]


@pytest.mark.parametrize("scenario,filter", [sublist[:2] for sublist in test_match_filters])
def test_match_attribute_filters_to_api_model(scenario, filter, snapshot):
    # it is essential to define snapshot dir using absolute path, otherwise snapshots cannot be found when
    # running from a different working directory
    snapshot.snapshot_dir = os.path.join(_current_dir, "attribute_filters")

    snapshot.assert_match(
        json.dumps(filter.as_api_model().to_dict(), indent=4, sort_keys=True),
        _scenario_to_snapshot_name(scenario),
    )


@pytest.mark.parametrize("scenario,filter,description", test_match_filters)
def test_match_attribute_filters_description(scenario, filter, description):
    assert filter.description(description_labels) == description


def test_match_filter_empty_literal_is_noop():
    f = MatchAttributeFilter(label="test", literal="", match_type="CONTAINS")
    assert f.is_noop() is True


def test_match_filter_non_empty_literal_is_not_noop():
    f = MatchAttributeFilter(label="test", literal="foo", match_type="CONTAINS")
    assert f.is_noop() is False


def test_negated_match_filter_empty_literal_is_not_noop():
    f = MatchAttributeFilter(label="test", literal="", match_type="CONTAINS", negate=True)
    assert f.is_noop() is False


def test_match_filter_invalid_match_type():
    with pytest.raises(ValueError, match="Match type must be one of"):
        MatchAttributeFilter(label="test", literal="foo", match_type="INVALID")


def test_match_filter_equality():
    f1 = MatchAttributeFilter(label="test", literal="foo", match_type="CONTAINS")
    f2 = MatchAttributeFilter(label="test", literal="foo", match_type="CONTAINS")
    assert f1 == f2


def test_match_filter_inequality_different_match_type():
    f1 = MatchAttributeFilter(label="test", literal="foo", match_type="CONTAINS")
    f2 = MatchAttributeFilter(label="test", literal="foo", match_type="STARTS_WITH")
    assert f1 != f2


def test_match_filter_inequality_different_negate():
    f1 = MatchAttributeFilter(label="test", literal="foo", match_type="CONTAINS")
    f2 = MatchAttributeFilter(label="test", literal="foo", match_type="CONTAINS", negate=True)
    assert f1 != f2


def test_match_filter_inequality_different_case_sensitive():
    f1 = MatchAttributeFilter(label="test", literal="foo", match_type="CONTAINS")
    f2 = MatchAttributeFilter(label="test", literal="foo", match_type="CONTAINS", case_sensitive=True)
    assert f1 != f2

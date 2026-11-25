# (C) 2026 GoodData Corporation
import pytest
from gooddata_eval.core.evaluators._deep_subset import deep_subset


def test_deep_subset_scalar_equal():
    assert deep_subset("LESS_THAN", "LESS_THAN") is True


def test_deep_subset_scalar_unequal():
    assert deep_subset("LESS_THAN", "GREATER_THAN") is False


def test_deep_subset_dict_subset():
    assert deep_subset({"a": 1}, {"a": 1, "b": 2}) is True


def test_deep_subset_dict_missing_key():
    assert deep_subset({"a": 1, "c": 3}, {"a": 1, "b": 2}) is False


def test_deep_subset_list_order_insensitive():
    expected = [{"type": "positive", "val": "EMEA"}]
    actual = [{"type": "positive", "val": "EMEA", "extra": "x"}]
    assert deep_subset(expected, actual) is True


def test_deep_subset_list_length_mismatch():
    assert deep_subset([1, 2], [1]) is False


def test_deep_subset_nested():
    expected = {"filter": {"in": {"values": ["abc"]}}}
    actual = {"filter": {"in": {"values": ["abc"]}, "extra": True}}
    assert deep_subset(expected, actual) is True


@pytest.mark.parametrize(
    ("expected", "actual", "matches"),
    [
        pytest.param(500, "500", True, id="int-and-numeric-string"),
        pytest.param(0.15, "0.15", True, id="float-and-numeric-string"),
        pytest.param(500, "500.0", True, id="int-and-float-string"),
        pytest.param("500", 500, True, id="numeric-string-and-int"),
        pytest.param(9007199254740993, "9007199254740993", True, id="large-int-and-its-string"),
        pytest.param({"threshold": 10000}, {"threshold": "10000", "operator": "LESS_THAN"}, True, id="tool-args"),
        pytest.param(500, "501", False, id="different-value"),
        pytest.param(9007199254740992, "9007199254740993", False, id="large-int-off-by-one"),
        pytest.param(500, "five hundred", False, id="non-numeric-string"),
        pytest.param("500", "500.0", False, id="two-strings-stay-exact"),
        pytest.param(True, "1", False, id="bool-is-not-a-number"),
    ],
)
def test_deep_subset_number_matches_numeric_string(expected, actual, matches):
    assert deep_subset(expected, actual) is matches

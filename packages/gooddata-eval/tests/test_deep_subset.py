# (C) 2026 GoodData Corporation
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

# (C) 2021 GoodData Corporation
from __future__ import annotations

import json
import os

import pytest

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), "resources"))


def load_vis_obj(filename):
    """
    Given a filename containing
    :param filename:
    :return:
    """
    with open(filename) as f:
        content = json.load(f)

        return dict(
            id="test_vis_obj",
            attributes=dict(
                type="visualizationObject",
                title="test visualization object",
                content=content,
            ),
        )


def _test_vis_obj(relative_file):
    return load_vis_obj(os.path.join(__location__, relative_file))


@pytest.fixture()
def one_metric_two_attributes():
    return _test_vis_obj("one_metric_two_attributes.json")


@pytest.fixture()
def single_attribute():
    return _test_vis_obj("single_attribute.json")


@pytest.fixture()
def two_metrics_multiple_attribute_buckets():
    return _test_vis_obj("two_metrics_multiple_attribute_buckets.json")


@pytest.fixture()
def with_arithmetic_metric():
    return _test_vis_obj("with_arithmetic_metric.json")


@pytest.fixture()
def with_metric_value_filter():
    return _test_vis_obj("with_metric_value_filter.json")

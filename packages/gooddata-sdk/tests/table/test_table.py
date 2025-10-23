# (C) 2021 GoodData Corporation
from __future__ import annotations

import json
from pathlib import Path

import pytest
from gooddata_sdk import Attribute, GoodDataSdk, ObjId, PositiveAttributeFilter, SimpleMetric, Visualization, table
from tests_support.vcrpy_utils import get_vcr

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"
_snapshot_dir = _current_dir / "snapshots"
_vis_objs_dir = _fixtures_dir / "vis_objs"


def load_json(path):
    with path.open("r") as f:
        return json.load(f)


def _visualization_filename_to_snapshot_name(path):
    return path.name.replace(".json", ".snapshot.json")


@gd_vcr.use_cassette(str(_fixtures_dir / "table_with_just_attribute.yaml"))
def test_table_with_just_attribute(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    table = sdk.tables.for_items(test_config["workspace"], items=[Attribute(local_id="attr1", label="region")])

    values = list(result["attr1"] for result in table.read_all())

    assert values == ["Midwest", "Northeast", "South", "Unknown", "West"]


@gd_vcr.use_cassette(str(_fixtures_dir / "table_with_just_metric.yaml"))
def test_table_with_just_measure(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    table = sdk.tables.for_items(
        test_config["workspace"],
        items=[SimpleMetric(local_id="metric1", item=ObjId(type="metric", id="order_amount"))],
    )

    values = list(result["metric1"] for result in table.read_all())

    assert len(values) == 1
    assert values[0] > 0


@gd_vcr.use_cassette(str(_fixtures_dir / "table_with_attribute_and_metric.yaml"))
def test_table_with_attribute_and_metric(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    table = sdk.tables.for_items(
        test_config["workspace"],
        items=[
            Attribute(local_id="attr1", label="region"),
            SimpleMetric(local_id="metric1", item=ObjId(type="metric", id="order_amount")),
        ],
    )

    values = list((result["attr1"], result["metric1"]) for result in table.read_all())
    assert len(values) == 5


@gd_vcr.use_cassette(str(_fixtures_dir / "table_with_attribute_metric_and_filter.yaml"))
def test_table_with_attribute_metric_and_filter(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    table = sdk.tables.for_items(
        test_config["workspace"],
        items=[
            Attribute(local_id="attr1", label="region"),
            SimpleMetric(local_id="metric1", item=ObjId(type="metric", id="order_amount")),
        ],
        filters=[PositiveAttributeFilter(label="attr1", values=["Unknown", "Northeast"])],
    )

    values = list((result["attr1"], result["metric1"]) for result in table.read_all())
    assert len(values) == 2


@gd_vcr.use_cassette(str(_fixtures_dir / "table_with_attribute_show_all_values.yaml"))
def test_table_with_attribute_show_all_values(test_config: dict):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    # get number of months for which demo model contains data
    dates_table = sdk.tables.for_items(
        test_config["workspace"],
        items=[
            Attribute(local_id="attr1", label="date.month"),
            SimpleMetric(local_id="metric1", item=ObjId(type="fact", id="quantity")),
        ],
    )
    date_values_count = len([result["attr1"] for result in dates_table.read_all()])

    table_counts = dict()
    for show_all_values in [True, False]:
        table = sdk.tables.for_items(
            test_config["workspace"],
            items=[
                Attribute(local_id="attr1", label="date.month", show_all_values=show_all_values),
                SimpleMetric(local_id="metric1", item=ObjId(type="fact", id="quantity")),
            ],
            filters=[PositiveAttributeFilter(label=ObjId(type="label", id="order_status"), values=["Canceled"])],
        )
        table_counts[show_all_values] = len([result["attr1"] for result in table.read_all()])

    # table result with show_all_values=True has all dates (even if value is missing due to filtering)
    # only values missing at the beginning and end of range ar filtered out
    assert table_counts[True] <= date_values_count
    # there are filtered dates when show_all_values is False
    assert table_counts[True] > table_counts[False]


@pytest.mark.parametrize("filename", [f.absolute() for f in _vis_objs_dir.iterdir()])
def test_pivot_to_exec_def(filename, snapshot):
    """
    The test makes use of visualisation object json fixtures contained in `_vis_objs_dir`.

    All the input vis objects contain:
    - 2 metrics in columns
    - 3 row attrs
    - no columns attrs.
    Any additional vis object fields are expressed in abbreviations.

    Abbreviations explanation:
    1rt = 1 row total
    1rrt = 1 row running total
    1ct = 1 col total
    1crt = 1 col running total
    1cattr = 1 additional col attributes
    """
    vis_obj = load_json(filename)
    visualization = Visualization(vis_obj)

    exec_def = table._get_exec_for_pivot(visualization)
    result = exec_def.as_api_model().to_dict()

    snapshot.snapshot_dir = _snapshot_dir

    snapshot.assert_match(json.dumps(result, indent=4), filename.name.replace(".json", ".snapshot.json"))

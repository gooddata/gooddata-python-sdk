# (C) 2021 GoodData Corporation
from __future__ import annotations

from pathlib import Path

from tests_support.vcrpy_utils import get_vcr

from gooddata_sdk import Attribute, GoodDataSdk, ObjId, PositiveAttributeFilter, SimpleMetric

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"


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

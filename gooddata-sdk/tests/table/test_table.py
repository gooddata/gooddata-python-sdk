# (C) 2021 GoodData Corporation
from __future__ import annotations

from pathlib import Path

import vcr

from gooddata_sdk import Attribute, GoodDataSdk, ObjId, PositiveAttributeFilter, SimpleMetric
from tests import VCR_MATCH_ON

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"

gd_vcr = vcr.VCR(filter_headers=["authorization", "user-agent"], serializer="json", match_on=VCR_MATCH_ON)


@gd_vcr.use_cassette(str(_fixtures_dir / "table_with_just_attribute.json"))
def test_table_with_just_attribute(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    table = sdk.tables.for_items(
        test_config["workspace"], items=[Attribute(local_id="attr1", label="customers.region")]
    )

    values = list(result["attr1"] for result in table.read_all())

    assert values == ["Midwest", "Northeast", "South", "Unknown", "West"]


@gd_vcr.use_cassette(str(_fixtures_dir / "table_with_just_metric.json"))
def test_table_with_just_measure(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    table = sdk.tables.for_items(
        test_config["workspace"],
        items=[SimpleMetric(local_id="metric1", item=ObjId(type="metric", id="order_amount"))],
    )

    values = list(result["metric1"] for result in table.read_all())

    assert len(values) == 1
    assert values[0] > 0


@gd_vcr.use_cassette(str(_fixtures_dir / "table_with_attribute_and_metric.json"))
def test_table_with_attribute_and_metric(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    table = sdk.tables.for_items(
        test_config["workspace"],
        items=[
            Attribute(local_id="attr1", label="customers.region"),
            SimpleMetric(local_id="metric1", item=ObjId(type="metric", id="order_amount")),
        ],
    )

    values = list((result["attr1"], result["metric1"]) for result in table.read_all())
    assert len(values) == 5


@gd_vcr.use_cassette(str(_fixtures_dir / "table_with_attribute_metric_and_filter.json"))
def test_table_with_attribute_metric_and_filter(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    table = sdk.tables.for_items(
        test_config["workspace"],
        items=[
            Attribute(local_id="attr1", label="customers.region"),
            SimpleMetric(local_id="metric1", item=ObjId(type="metric", id="order_amount")),
        ],
        filters=[PositiveAttributeFilter(label="attr1", values=["Unknown", "Northeast"])],
    )

    values = list((result["attr1"], result["metric1"]) for result in table.read_all())
    assert len(values) == 2

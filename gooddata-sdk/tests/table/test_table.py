# (C) 2021 GoodData Corporation
from __future__ import annotations

import os

import vcr

from gooddata_sdk import Attribute, GoodDataSdk, ObjId, PositiveAttributeFilter, SimpleMetric
from tests import TEST_HOST, TEST_WORKSPACE, test_token

_current_dir = os.path.dirname(os.path.abspath(__file__))
_fixtures_dir = os.path.join(_current_dir, "fixtures")

gd_vcr = vcr.VCR(filter_headers=["authorization"], serializer="json")

_regions = [
    "Aargau",
    "Basel-Landschaft",
    "Basel-Stadt",
    "Bern",
    "Fribourg",
    "Geneva",
    "Glarus",
    "Graubünden",
    "Jura",
    "Lucerne",
    "Neuchâtel",
    "Nidwalden",
    "Obwalden",
    "Schaffhausen",
    "Schwyz",
    "Solothurn",
    "St. Gallen",
    "Thurgau",
    "Ticino",
    "Uri",
    "Valais",
    "Vaud",
    "Zug",
    "Zürich",
]


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "table_with_just_attribute.json"))
def test_table_with_just_attribute():
    sdk = GoodDataSdk.create(host_=TEST_HOST, token_=test_token())
    table = sdk.tables.for_items(TEST_WORKSPACE, items=[Attribute(local_id="attr1", label="region.region_name")])

    values = list(result["attr1"] for result in table.read_all())

    assert values == _regions


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "table_with_just_metric.json"))
def test_table_with_just_measure():
    sdk = GoodDataSdk.create(host_=TEST_HOST, token_=test_token())
    table = sdk.tables.for_items(
        TEST_WORKSPACE,
        items=[SimpleMetric(local_id="metric1", item=ObjId(type="metric", id="claim-amount"))],
    )

    values = list(result["metric1"] for result in table.read_all())

    assert len(values) == 1
    assert values[0] > 0


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "table_with_attribute_and_metric.json"))
def test_table_with_attribute_and_metric():
    sdk = GoodDataSdk.create(host_=TEST_HOST, token_=test_token())
    table = sdk.tables.for_items(
        TEST_WORKSPACE,
        items=[
            Attribute(local_id="attr1", label="region.region_name"),
            SimpleMetric(local_id="metric1", item=ObjId(type="metric", id="claim-amount")),
        ],
    )

    values = list((result["attr1"], result["metric1"]) for result in table.read_all())
    assert len(values) == len(_regions)


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "table_with_attribute_metric_and_filter.json"))
def test_table_with_attribute_metric_and_filter():
    sdk = GoodDataSdk.create(host_=TEST_HOST, token_=test_token())
    table = sdk.tables.for_items(
        TEST_WORKSPACE,
        items=[
            Attribute(local_id="attr1", label="region.region_name"),
            SimpleMetric(local_id="metric1", item=ObjId(type="metric", id="claim-amount")),
        ],
        filters=[PositiveAttributeFilter(label="attr1", values=["Aargau", "Bern", "Vaud"])],
    )

    values = list((result["attr1"], result["metric1"]) for result in table.read_all())
    assert len(values) == 3

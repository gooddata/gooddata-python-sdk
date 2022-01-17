# (C) 2021 GoodData Corporation
from pathlib import Path

import vcr
from numpy import float64

from gooddata_pandas import SeriesFactory
from gooddata_sdk import PositiveAttributeFilter
from tests import VCR_MATCH_ON

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"

gd_vcr = vcr.VCR(filter_headers=["authorization", "user-agent"], serializer="json", match_on=VCR_MATCH_ON)


@gd_vcr.use_cassette(str(_fixtures_dir / "simple_index_metric_series.json"))
def test_simple_index_metric_series(gds: SeriesFactory):
    series = gds.indexed(
        index_by=dict(reg="label/customers.region"),
        data_by="fact/order_lines.price",
    )

    assert len(series) == 5
    assert series.values.dtype == float64


@gd_vcr.use_cassette(str(_fixtures_dir / "simple_index_label_series.json"))
def test_simple_index_label_series(gds: SeriesFactory):
    series = gds.indexed(
        index_by=dict(reg="label/customers.region"),
        data_by="label/customers.region",
    )

    assert len(series) == 5
    assert series["Midwest"] == "Midwest"


@gd_vcr.use_cassette(str(_fixtures_dir / "simple_index_filtered_series.json"))
def test_simple_index_filtered_series(gds: SeriesFactory):
    series = gds.indexed(
        index_by=dict(reg="label/customers.region"),
        data_by="label/products.category",
        filter_by=[
            PositiveAttributeFilter(label="label/customers.region", values=["Midwest"]),
            PositiveAttributeFilter(label="label/products.category", values=["Clothing"]),
        ],
    )

    assert len(series) == 1
    assert series["Midwest"] == "Clothing"


@gd_vcr.use_cassette(str(_fixtures_dir / "multi_index_metric_series.json"))
def test_multi_index_metric_series(gds: SeriesFactory):
    series = gds.indexed(
        index_by=dict(reg="label/customers.region", category="label/products.category"),
        data_by="fact/order_lines.price",
    )

    assert len(series) == 17
    assert len(series["Northeast"]) == 4
    assert len(series["Unknown"]) == 1
    assert series.values.dtype == float64


@gd_vcr.use_cassette(str(_fixtures_dir / "multi_index_filtered_series.json"))
def test_multi_index_filtered_series(gds: SeriesFactory):
    series = gds.indexed(
        index_by=dict(reg="label/customers.region", category="label/products.category"),
        data_by="fact/order_lines.price",
        filter_by=PositiveAttributeFilter(label="category", values=["Clothing"]),
    )

    assert len(series) == 5

    index_list = series.keys().to_list()
    index_list.sort()
    assert index_list == [
        ("Midwest", "Clothing"),
        ("Northeast", "Clothing"),
        ("South", "Clothing"),
        ("Unknown", "Clothing"),
        ("West", "Clothing"),
    ]
    assert len(series["Midwest"]) == 1
    assert series.values.dtype == float64

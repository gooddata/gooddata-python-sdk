# (C) 2021 GoodData Corporation
import os

import vcr
from numpy import float64

from gooddata_pandas import SeriesFactory
from gooddata_sdk import PositiveAttributeFilter
from tests import TEST_DATA_REGIONS

_current_dir = os.path.dirname(os.path.abspath(__file__))
_fixtures_dir = os.path.join(_current_dir, "fixtures")

gd_vcr = vcr.VCR(filter_headers=["authorization"], serializer="json")


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "simple_index_metric_series.json"))
def test_simple_index_metric_series(gds: SeriesFactory):
    series = gds.indexed(
        index_by=dict(reg="label/region.region_name"),
        data_by="fact/region.region_crime_rate",
    )

    assert len(series) == len(TEST_DATA_REGIONS)
    assert series.values.dtype == float64


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "simple_index_label_series.json"))
def test_simple_index_label_series(gds: SeriesFactory):
    series = gds.indexed(
        index_by=dict(reg="label/region.region_name"),
        data_by="label/region.region_code",
    )

    assert len(series) == len(TEST_DATA_REGIONS)
    assert series["Bern"] == "BE"


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "simple_index_filtered_series.json"))
def test_simple_index_filtered_series(gds: SeriesFactory):
    series = gds.indexed(
        index_by=dict(reg="label/region.region_name"),
        data_by="label/region.region_code",
        filter_by=PositiveAttributeFilter(label="reg", in_values=["Bern"]),
    )

    assert len(series) == 1
    assert series["Bern"] == "BE"


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "multi_index_metric_series.json"))
def test_multi_index_metric_series(gds: SeriesFactory):
    series = gds.indexed(
        index_by=dict(
            reg="label/region.region_name", prod="label/product.product_name"
        ),
        data_by="fact/coverage.coverage_risk_score",
    )

    # different regions have different number of insurance products. the sub-index for that region will only
    # have as many entries as there are used products
    assert len(series["Aargau"]) == 2
    assert len(series["Bern"]) == 1
    assert len(series["Zürich"]) == 3
    assert series.values.dtype == float64


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "multi_index_filtered_series.json"))
def test_multi_index_filtered_series(gds: SeriesFactory):
    series = gds.indexed(
        index_by=dict(
            reg="label/region.region_name", prod="label/product.product_name"
        ),
        data_by="fact/coverage.coverage_risk_score",
        filter_by=PositiveAttributeFilter(label="prod", in_values=["Hybrid"]),
    )

    # only two regions have the 'Hybrid' product filtered above. each sub-index for each region will contain
    # exactly one key Hybrid
    assert len(series) == 2
    assert len(series["St. Gallen"]) == 1
    assert len(series["Zürich"]) == 1
    assert series.values.dtype == float64

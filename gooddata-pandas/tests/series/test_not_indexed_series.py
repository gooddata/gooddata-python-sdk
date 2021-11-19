# (C) 2021 GoodData Corporation
import os

import vcr
from numpy import float64

from gooddata_pandas import SeriesFactory
from gooddata_sdk import ObjId, PositiveAttributeFilter
from tests import TEST_DATA_REGIONS

_current_dir = os.path.dirname(os.path.abspath(__file__))
_fixtures_dir = os.path.join(_current_dir, "fixtures")

gd_vcr = vcr.VCR(filter_headers=["authorization"], serializer="json")


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "not_indexed_metric_series.json"))
def test_not_indexed_metric_series(gds: SeriesFactory):
    series = gds.not_indexed(data_by="fact/region.region_crime_rate")

    # having metric with no granularity will return series with single item
    assert len(series) == 1
    assert series.values.dtype == float64


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "not_indexed_label_series.json"))
def test_not_index_label_series(gds: SeriesFactory):
    series = gds.not_indexed(data_by="label/region.region_name")

    assert len(series) == len(TEST_DATA_REGIONS)
    assert series[0] == "Aargau"
    assert series[23] == "Zürich"


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "not_indexed_metric_series_with_granularity.json"))
def test_not_indexed_metric_series_with_granularity(gds: SeriesFactory):
    series = gds.not_indexed(
        granularity=dict(reg="label/region.region_name"),
        data_by="fact/region.region_crime_rate",
    )

    assert len(series) == len(TEST_DATA_REGIONS)
    assert series.values.dtype == float64


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "not_indexed_label_series_with_granularity.json"))
def test_not_index_label_series_with_granularity(gds: SeriesFactory):
    series = gds.not_indexed(
        granularity=dict(reg="label/region.region_name"),
        data_by="label/product.product_name",
    )

    # just a rough rub; getting series of products on the region granularity leads to series containing
    # an assorted listing of products used in the different regions. there is 1:N relationship there. just
    # checking the series is longer than number of regions
    assert len(series) > len(TEST_DATA_REGIONS)


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "not_indexed_filtered_metric_series.json"))
def test_not_indexed_filtered_metric_series(gds: SeriesFactory):
    # crime rate across all regions
    not_filtered_series = gds.not_indexed(data_by="fact/region.region_crime_rate")
    # crime rate just in Bern
    filtered_series = gds.not_indexed(
        data_by="fact/region.region_crime_rate",
        filter_by=PositiveAttributeFilter(label=ObjId(type="label", id="region.region_name"), in_values=["Bern"]),
    )

    # having metric with no granularity will return series with single item
    assert len(filtered_series) == 1
    # the filtered crime rate should be lower than rate in all regions
    assert filtered_series[0] < not_filtered_series[0]

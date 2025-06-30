# (C) 2021 GoodData Corporation
from pathlib import Path

from gooddata_pandas import SeriesFactory
from gooddata_sdk import ObjId, PositiveAttributeFilter
from numpy import float64
from tests_support.vcrpy_utils import get_vcr

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"


@gd_vcr.use_cassette(str(_fixtures_dir / "not_indexed_metric_series.yaml"))
def test_not_indexed_metric_series(gds: SeriesFactory):
    series = gds.not_indexed(data_by="fact/price")

    # having metric with no granularity will return series with single item
    assert len(series) == 1
    assert series.values.dtype == float64


@gd_vcr.use_cassette(str(_fixtures_dir / "not_indexed_label_series.yaml"))
def test_not_index_label_series(gds: SeriesFactory):
    series = gds.not_indexed(data_by="label/region")

    assert len(series) == 5
    assert series[0] == "Midwest"
    assert series[4] == "West"


@gd_vcr.use_cassette(str(_fixtures_dir / "not_indexed_metric_series_with_granularity.yaml"))
def test_not_indexed_metric_series_with_granularity(gds: SeriesFactory):
    series = gds.not_indexed(
        granularity=dict(reg="label/region"),
        data_by="fact/price",
    )

    assert len(series) == 5
    assert series.values.dtype == float64


@gd_vcr.use_cassette(str(_fixtures_dir / "not_indexed_label_series_with_granularity.yaml"))
def test_not_index_label_series_with_granularity(gds: SeriesFactory):
    series = gds.not_indexed(
        granularity=dict(reg="label/region"),
        data_by="label/products.category",
    )

    # just a rough rub; getting series of products on the region granularity leads to series containing
    # an assorted listing of products used in the different regions. there is 1:N relationship there.
    assert len(series) == 17


@gd_vcr.use_cassette(str(_fixtures_dir / "not_indexed_filtered_metric_series.yaml"))
def test_not_indexed_filtered_metric_series(gds: SeriesFactory):
    # price across all regions
    not_filtered_series = gds.not_indexed(data_by="fact/price")
    # price just in Unknown
    filtered_series = gds.not_indexed(
        data_by="fact/price",
        filter_by=PositiveAttributeFilter(label=ObjId(type="label", id="region"), values=["Unknown"]),
    )

    # having metric with no granularity will return series with single item
    assert len(filtered_series) == 1
    # the filtered crime rate should be lower than rate in all regions
    assert filtered_series[0] < not_filtered_series[0]

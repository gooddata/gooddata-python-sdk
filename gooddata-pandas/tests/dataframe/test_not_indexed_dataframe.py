# (C) 2021 GoodData Corporation
import os

import vcr

from gooddata_pandas import DataFrameFactory
from gooddata_sdk import PositiveAttributeFilter
from tests import TEST_DATA_REGIONS

_current_dir = os.path.dirname(os.path.abspath(__file__))
_fixtures_dir = os.path.join(_current_dir, "fixtures")

gd_vcr = vcr.VCR(filter_headers=["authorization"], serializer="json")


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "not_indexed_metrics.json"))
def test_not_indexed_metrics(gdf: DataFrameFactory):
    df = gdf.not_indexed(
        columns=dict(
            crime_rate="fact/region.region_crime_rate",
            safety_scale="fact/region.region_safety_scale",
        )
    )

    assert len(df) == 1
    assert len(df.columns) == 2
    assert df.columns[0] == "crime_rate"
    assert df.columns[1] == "safety_scale"


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "not_indexed_metrics_and_labels.json"))
def test_not_indexed_metrics_and_labels(gdf: DataFrameFactory):
    df = gdf.not_indexed(
        columns=dict(
            reg="label/region.region_name",
            crime_rate="fact/region.region_crime_rate",
            safety_scale="fact/region.region_safety_scale",
        )
    )

    assert len(df) == len(TEST_DATA_REGIONS)
    assert len(df.columns) == 3
    assert df.columns[0] == "reg"
    assert df.columns[1] == "crime_rate"
    assert df.columns[2] == "safety_scale"


@gd_vcr.use_cassette(
    os.path.join(_fixtures_dir, "not_indexed_filtered_metrics_and_labels.json")
)
def test_not_indexed_filtered_metrics_and_labels(gdf: DataFrameFactory):
    df = gdf.not_indexed(
        columns=dict(
            reg="label/region.region_name",
            crime_rate="fact/region.region_crime_rate",
            safety_scale="fact/region.region_safety_scale",
        ),
        filter_by=[PositiveAttributeFilter(label="reg", in_values=["Bern"])],
    )

    assert len(df) == 1
    assert len(df.columns) == 3
    assert df.columns[0] == "reg"
    assert df.columns[1] == "crime_rate"
    assert df.columns[2] == "safety_scale"

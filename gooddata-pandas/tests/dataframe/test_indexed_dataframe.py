# (C) 2021 GoodData Corporation
import os

import vcr

from gooddata_pandas import DataFrameFactory
from gooddata_sdk import PositiveAttributeFilter
from tests import TEST_DATA_REGIONS

_current_dir = os.path.dirname(os.path.abspath(__file__))
_fixtures_dir = os.path.join(_current_dir, "fixtures")

gd_vcr = vcr.VCR(filter_headers=["authorization"], serializer="json")


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "simple_index_metrics.json"))
def test_simple_index_metrics(gdf: DataFrameFactory):
    df = gdf.indexed(
        index_by=dict(reg="label/region.region_name"),
        columns=dict(
            crime_rate="fact/region.region_crime_rate",
            safety_scale="fact/region.region_safety_scale",
        ),
    )

    assert len(df) == len(TEST_DATA_REGIONS)
    assert len(df.columns) == 2
    assert df.columns[0] == "crime_rate"
    assert df.columns[1] == "safety_scale"


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "simple_index_metrics_and_label.json"))
def test_simple_index_metrics_and_label(gdf: DataFrameFactory):
    df = gdf.indexed(
        index_by=dict(reg="label/region.region_name"),
        columns=dict(
            crime_rate="fact/region.region_crime_rate",
            safety_scale="fact/region.region_safety_scale",
            region_code="label/region.region_code",
        ),
    )

    assert len(df) == len(TEST_DATA_REGIONS)
    assert len(df.columns) == 3
    assert df.columns[0] == "crime_rate"
    assert df.columns[1] == "safety_scale"
    assert df.columns[2] == "region_code"


@gd_vcr.use_cassette(
    os.path.join(_fixtures_dir, "simple_index_filtered_metrics_and_label.json")
)
def test_simple_index_filtered_metrics_and_label(gdf: DataFrameFactory):
    df = gdf.indexed(
        index_by=dict(reg="label/region.region_name"),
        columns=dict(
            crime_rate="fact/region.region_crime_rate",
            safety_scale="fact/region.region_safety_scale",
            region_code="label/region.region_code",
        ),
        filter_by=[PositiveAttributeFilter(label="reg", in_values=["Bern"])],
    )

    assert len(df) == 1
    assert len(df.columns) == 3
    assert df.columns[0] == "crime_rate"
    assert df.columns[1] == "safety_scale"
    assert df.columns[2] == "region_code"


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "multi_index_metrics.json"))
def test_multi_index_metrics(gdf: DataFrameFactory):
    df = gdf.indexed(
        index_by=dict(
            reg="label/region.region_name", prod="label/product.product_name"
        ),
        columns=dict(
            claim_amount="metric/claim-amount", claim_count="metric/claim-count"
        ),
    )

    assert len(df) > len(TEST_DATA_REGIONS)
    assert len(df.columns) == 2
    assert df.index.names[0] == "reg"
    assert df.index.names[1] == "prod"
    assert df.columns[0] == "claim_amount"
    assert df.columns[1] == "claim_count"


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "multi_index_metrics_and_label.json"))
def test_multi_index_metrics_and_label(gdf: DataFrameFactory):
    df = gdf.indexed(
        index_by=dict(
            reg="label/region.region_name", prod="label/product.product_name"
        ),
        columns=dict(
            claim_amount="metric/claim-amount",
            claim_count="metric/claim-count",
            region_code="label/region.region_code",
        ),
    )

    assert len(df) > len(TEST_DATA_REGIONS)
    assert len(df.columns) == 3
    assert df.index.names[0] == "reg"
    assert df.index.names[1] == "prod"
    assert df.columns[0] == "claim_amount"
    assert df.columns[1] == "claim_count"
    assert df.columns[2] == "region_code"


@gd_vcr.use_cassette(
    os.path.join(_fixtures_dir, "multi_index_filtered_metrics_and_label.json")
)
def test_multi_index_filtered_metrics_and_label(gdf: DataFrameFactory):
    df = gdf.indexed(
        index_by=dict(
            reg="label/region.region_name", prod="label/product.product_name"
        ),
        columns=dict(
            claim_amount="metric/claim-amount",
            claim_count="metric/claim-count",
            region_code="label/region.region_code",
        ),
        filter_by=[PositiveAttributeFilter(label="reg", in_values=["Bern"])],
    )

    assert len(df) == 1
    assert len(df.columns) == 3
    assert df.index.names[0] == "reg"
    assert df.index.names[1] == "prod"
    assert df.columns[0] == "claim_amount"
    assert df.columns[1] == "claim_count"
    assert df.columns[2] == "region_code"


@gd_vcr.use_cassette(
    os.path.join(_fixtures_dir, "multi_index_filtered_metrics_and_label_reuse.json")
)
def test_multi_index_filtered_metrics_and_label_reuse(gdf: DataFrameFactory):
    # note here: if a single label is reused in both index and columns, that label will be used in computation
    # just once. the first-found occurrence will be used in computation. local id of the attribute will be
    # the key in the dict where the label was first found
    #
    # this has implications when referencing label by local id
    df = gdf.indexed(
        index_by=dict(
            reg_idx="label/region.region_name", prod="label/product.product_name"
        ),
        columns=dict(
            claim_amount="metric/claim-amount",
            claim_count="metric/claim-count",
            reg="label/region.region_name",
        ),
        filter_by=[PositiveAttributeFilter(label="reg_idx", in_values=["Bern"])],
    )

    assert len(df) == 1
    assert len(df.columns) == 3
    assert df.index.names[0] == "reg_idx"
    assert df.index.names[1] == "prod"
    assert df.columns[0] == "claim_amount"
    assert df.columns[1] == "claim_count"
    assert df.columns[2] == "reg"

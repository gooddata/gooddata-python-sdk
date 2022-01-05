# (C) 2021 GoodData Corporation
import os

import pytest
import vcr

from gooddata_pandas import DataFrameFactory
from gooddata_sdk import Attribute, MetricValueFilter, ObjId, PositiveAttributeFilter
from tests import TEST_DATA_REGIONS

_current_dir = os.path.dirname(os.path.abspath(__file__))
_fixtures_dir = os.path.join(_current_dir, "fixtures")

gd_vcr = vcr.VCR(filter_headers=["authorization"], serializer="json")

index_types = [
    "region_name",
    "label/region.region_name",
    dict(reg="label/region.region_name"),
    Attribute(local_id="abcd", label=ObjId(id="region.region_name", type="label")),
    ObjId(id="region.region_name", type="label"),
]


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "simple_index_metrics.json"))
@pytest.mark.parametrize("index", index_types)
def test_simple_index_metrics(gdf: DataFrameFactory, index):
    df = gdf.indexed(
        index_by=index,
        columns=dict(
            region_name="label/region.region_name",
            crime_rate="fact/region.region_crime_rate",
            safety_scale="fact/region.region_safety_scale",
        ),
    )

    assert len(df) == len(TEST_DATA_REGIONS)
    assert len(df.columns) == 3
    assert df.columns[0] == "region_name"
    assert df.columns[1] == "crime_rate"
    assert df.columns[2] == "safety_scale"


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "simple_index_metrics.json"))
def test_simple_index_metrics_no_duplicate_index_col(gdf: DataFrameFactory):
    df = gdf.indexed(
        index_by="label/region.region_name",
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
    columns = {
        "Crime rate": "fact/region.region_crime_rate",
        "Safety scale ($special$%^&)": "fact/region.region_safety_scale",
        "Region code ($special$%^&)": "label/region.region_code",
    }
    df = gdf.indexed(
        index_by=dict(reg="label/region.region_name"),
        columns=columns,
    )

    assert len(df) == len(TEST_DATA_REGIONS)
    assert len(df.columns) == 3
    assert df.columns[0] == "Crime rate"
    assert df.columns[1] == "Safety scale ($special$%^&)"
    assert df.columns[2] == "Region code ($special$%^&)"


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "simple_index_filtered_metrics_and_label.json"))
def test_simple_index_filtered_metrics_and_label(gdf: DataFrameFactory):
    df = gdf.indexed(
        index_by=dict(reg="label/region.region_name"),
        columns=dict(
            crime_rate="fact/region.region_crime_rate",
            safety_scale="fact/region.region_safety_scale",
            region_code="label/region.region_code",
        ),
        filter_by=[
            # Label referenced by localIdentifier
            PositiveAttributeFilter(label="reg", values=["Bern"]),
            # Label referenced by full ID
            PositiveAttributeFilter(label="label/region.region_name", values=["Bern"]),
            # Label referenced by ObjId
            PositiveAttributeFilter(label=ObjId(id="region.region_name", type="label"), values=["Bern"]),
            # label referenced by index in columns
            PositiveAttributeFilter(label="region_code", values=["BE"]),
            MetricValueFilter(metric="crime_rate", operator="GREATER_THAN", values=0),
        ],
    )

    assert len(df) == 1
    assert len(df.columns) == 3
    assert df.columns[0] == "crime_rate"
    assert df.columns[1] == "safety_scale"
    assert df.columns[2] == "region_code"


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "multi_index_metrics.json"))
def test_multi_index_metrics(gdf: DataFrameFactory):
    df = gdf.indexed(
        index_by=dict(reg="label/region.region_name", prod="label/product.product_name"),
        columns=dict(claim_amount="metric/claim-amount", claim_count="metric/claim-count"),
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
        index_by=dict(reg="label/region.region_name", prod="label/product.product_name"),
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


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "multi_index_filtered_metrics_and_label.json"))
def test_multi_index_filtered_metrics_and_label(gdf: DataFrameFactory):
    df = gdf.indexed(
        index_by=dict(reg="label/region.region_name", prod="label/product.product_name"),
        columns=dict(
            claim_amount="metric/claim-amount",
            claim_count="metric/claim-count",
            region_code="label/region.region_code",
        ),
        filter_by=[PositiveAttributeFilter(label="reg", values=["Bern"])],
    )

    assert len(df) == 1
    assert len(df.columns) == 3
    assert df.index.names[0] == "reg"
    assert df.index.names[1] == "prod"
    assert df.columns[0] == "claim_amount"
    assert df.columns[1] == "claim_count"
    assert df.columns[2] == "region_code"


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "multi_index_filtered_metrics_and_label_reuse.json"))
def test_multi_index_filtered_metrics_and_label_reuse(gdf: DataFrameFactory):
    # note here: if a single label is reused in both index and columns, that label will be used in computation
    # just once. the first-found occurrence will be used in computation. local id of the attribute will be
    # the key in the dict where the label was first found
    #
    # this has implications when referencing label by local id
    df = gdf.indexed(
        index_by=dict(reg_idx="label/region.region_name", prod="label/product.product_name"),
        columns=dict(
            claim_amount="metric/claim-amount",
            claim_count="metric/claim-count",
            reg="label/region.region_name",
        ),
        filter_by=[PositiveAttributeFilter(label="reg_idx", values=["Bern"])],
    )

    assert len(df) == 1
    assert len(df.columns) == 3
    assert df.index.names[0] == "reg_idx"
    assert df.index.names[1] == "prod"
    assert df.columns[0] == "claim_amount"
    assert df.columns[1] == "claim_count"
    assert df.columns[2] == "reg"

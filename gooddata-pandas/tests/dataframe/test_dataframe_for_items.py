# (C) 2021 GoodData Corporation
from pathlib import Path

import vcr

from gooddata_pandas import DataFrameFactory

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"

gd_vcr = vcr.VCR(filter_headers=["authorization"], serializer="json")


@gd_vcr.use_cassette(str(_fixtures_dir / "dataframe_for_items.json"))
def test_dataframe_for_items(gdf: DataFrameFactory):
    df = gdf.for_items(
        items=dict(
            reg="label/region.region_name",
            prod="label/product.product_name",
            claim_amount="metric/claim-amount",
            claim_count="metric/claim-count",
        )
    )

    assert len(df.index.names) == 2
    assert len(df.columns) == 2
    assert df.index.names[0] == "reg"
    assert df.index.names[1] == "prod"
    assert df.columns[0] == "claim_amount"
    assert df.columns[1] == "claim_count"


@gd_vcr.use_cassette(str(_fixtures_dir / "dataframe_for_items_no_index.json"))
def test_dataframe_for_items_no_index(gdf: DataFrameFactory):
    df = gdf.for_items(
        items=dict(
            reg="label/region.region_name",
            prod="label/product.product_name",
            claim_amount="metric/claim-amount",
            claim_count="metric/claim-count",
        ),
        auto_index=False,
    )

    assert df.columns[0] == "reg"
    assert df.columns[1] == "prod"
    assert df.columns[2] == "claim_amount"
    assert df.columns[3] == "claim_count"

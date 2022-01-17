# (C) 2021 GoodData Corporation
from pathlib import Path

import vcr

from gooddata_pandas import DataFrameFactory
from tests import VCR_MATCH_ON

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"

gd_vcr = vcr.VCR(filter_headers=["authorization", "user-agent"], serializer="json", match_on=VCR_MATCH_ON)


@gd_vcr.use_cassette(str(_fixtures_dir / "dataframe_for_items.json"))
def test_dataframe_for_items(gdf: DataFrameFactory):
    df = gdf.for_items(
        items=dict(
            reg="label/customers.region",
            category="label/products.category",
            price="fact/order_lines.price",
            order_amount="metric/order_amount",
        )
    )

    assert len(df.index.names) == 2
    assert len(df.columns) == 2
    assert df.index.names[0] == "reg"
    assert df.index.names[1] == "category"
    assert df.columns[0] == "price"
    assert df.columns[1] == "order_amount"


@gd_vcr.use_cassette(str(_fixtures_dir / "dataframe_for_items_no_index.json"))
def test_dataframe_for_items_no_index(gdf: DataFrameFactory):
    df = gdf.for_items(
        items=dict(
            reg="label/customers.region",
            category="label/products.category",
            price="fact/order_lines.price",
            order_amount="metric/order_amount",
        ),
        auto_index=False,
    )

    assert df.columns[0] == "reg"
    assert df.columns[1] == "category"
    assert df.columns[2] == "price"
    assert df.columns[3] == "order_amount"

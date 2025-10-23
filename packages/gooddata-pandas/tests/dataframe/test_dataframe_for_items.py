# (C) 2021 GoodData Corporation
from pathlib import Path

from gooddata_pandas import DataFrameFactory
from tests_support.vcrpy_utils import get_vcr

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"


@gd_vcr.use_cassette(str(_fixtures_dir / "dataframe_for_items.yaml"))
def test_dataframe_for_items(gdf: DataFrameFactory):
    df = gdf.for_items(
        items=dict(
            reg="label/region",
            category="label/products.category",
            price="fact/price",
            order_amount="metric/order_amount",
        )
    )

    assert len(df.index.names) == 2
    assert len(df.columns) == 2
    assert df.index.names[0] == "reg"
    assert df.index.names[1] == "category"
    assert df.columns[0] == "price"
    assert df.columns[1] == "order_amount"


@gd_vcr.use_cassette(str(_fixtures_dir / "dataframe_for_items_no_index.yaml"))
def test_dataframe_for_items_no_index(gdf: DataFrameFactory):
    df = gdf.for_items(
        items=dict(
            reg="label/region",
            category="label/products.category",
            price="fact/price",
            order_amount="metric/order_amount",
        ),
        auto_index=False,
    )

    assert df.columns[0] == "reg"
    assert df.columns[1] == "category"
    assert df.columns[2] == "price"
    assert df.columns[3] == "order_amount"

# (C) 2021 GoodData Corporation
from pathlib import Path

from gooddata_pandas import DataFrameFactory
from tests_support.vcrpy_utils import get_vcr

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"


@gd_vcr.use_cassette(str(_fixtures_dir / "dataframe_for_visualization_date.yaml"))
def test_dataframe_for_visualization_date(gdf: DataFrameFactory):
    # 2 metrics grouped by date dimension with data for last 12 months
    # exact numbers cannot be checked as date data are changed each AIO build
    df = gdf.for_visualization(visualization_id="customers_trend")

    assert len(df) == 12
    assert len(df.index.names) == 1
    assert df.index.name == "date.month"
    assert df.index.dtype.name == "datetime64[ns]"
    assert len(df.columns) == 2
    assert df.columns[0] == "amount_of_active_customers"
    assert df.columns[1] == "revenue_per_customer"


@gd_vcr.use_cassette(str(_fixtures_dir / "dataframe_for_visualization.yaml"))
def test_dataframe_for_visualization(gdf: DataFrameFactory):
    # 4 metrics grouped by 2 attributes, filters are set to all
    df = gdf.for_visualization(visualization_id="revenue_and_quantity_by_product_and_category")

    assert df.index.names[0] == "products.category"
    assert df.index.names[1] == "product_name"
    assert df.columns[0] == "quantity"
    assert df.columns[1] == "price"
    assert df.columns[2] == "percent_revenue_in_category"
    assert df.columns[3] == "revenue"


@gd_vcr.use_cassette(str(_fixtures_dir / "dataframe_for_visualization_no_index.yaml"))
def test_dataframe_for_visualization_no_index(gdf: DataFrameFactory):
    # 4 metrics grouped by 2 attributes, filters are set to all
    df = gdf.for_visualization(visualization_id="revenue_and_quantity_by_product_and_category", auto_index=False)

    assert df.columns[0] == "products.category"
    assert df.columns[1] == "product_name"
    assert df.columns[2] == "quantity"
    assert df.columns[3] == "price"
    assert df.columns[4] == "percent_revenue_in_category"
    assert df.columns[5] == "revenue"

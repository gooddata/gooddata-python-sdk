# (C) 2021 GoodData Corporation
from pathlib import Path

import vcr

from gooddata_pandas import DataFrameFactory
from tests import VCR_MATCH_ON

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"

gd_vcr = vcr.VCR(filter_headers=["authorization", "user-agent"], serializer="json", match_on=VCR_MATCH_ON)


@gd_vcr.use_cassette(str(_fixtures_dir / "dataframe_for_insight_date.json"))
def test_dataframe_for_insight_date(gdf: DataFrameFactory):
    # 2 metrics grouped by date dimension with data for last 12 months
    # exact numbers cannot be checked as date data are changed each AIO build
    df = gdf.for_insight(insight_id="customers_trend")

    assert len(df) == 12
    assert len(df.index.names) == 1
    assert df.index.name == "date.month"
    assert df.index.dtype.name == "datetime64[ns]"
    assert len(df.columns) == 2
    assert df.columns[0] == "amount_of_active_customers"
    assert df.columns[1] == "revenue_per_customer"


@gd_vcr.use_cassette(str(_fixtures_dir / "dataframe_for_insight.json"))
def test_dataframe_for_insight(gdf: DataFrameFactory):
    # 4 metrics grouped by 2 attributes, filters are set to all
    df = gdf.for_insight(insight_id="revenue_and_quantity_by_product_and_category")

    assert df.index.names[0] == "products.category"
    assert df.index.names[1] == "products.product_name"
    assert df.columns[0] == "order_lines.quantity"
    assert df.columns[1] == "order_lines.price"
    assert df.columns[2] == "percent_revenue_in_category"
    assert df.columns[3] == "revenue"


@gd_vcr.use_cassette(str(_fixtures_dir / "dataframe_for_insight_no_index.json"))
def test_dataframe_for_insight_no_index(gdf: DataFrameFactory):
    # 4 metrics grouped by 2 attributes, filters are set to all
    df = gdf.for_insight(insight_id="revenue_and_quantity_by_product_and_category", auto_index=False)

    assert df.columns[0] == "products.category"
    assert df.columns[1] == "products.product_name"
    assert df.columns[2] == "order_lines.quantity"
    assert df.columns[3] == "order_lines.price"
    assert df.columns[4] == "percent_revenue_in_category"
    assert df.columns[5] == "revenue"

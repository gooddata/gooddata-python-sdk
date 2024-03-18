# (C) 2021 GoodData Corporation
from pathlib import Path

import pytest
from gooddata_pandas import DataFrameFactory
from gooddata_sdk import Attribute, MetricValueFilter, ObjId, PositiveAttributeFilter
from tests_support.vcrpy_utils import get_vcr

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"


index_types = [
    # reference to the columns key
    "region",
    dict(reg="region"),
    # label_id, i.e. obj id without "label/" prefix - index can reference only attributes
    "region",
    dict(region="region"),
    # object identifier in string form
    "label/region",
    dict(reg="label/region"),
    # Attribute instance
    Attribute(local_id="abcd", label=ObjId(id="region", type="label")),
    dict(region=Attribute(local_id="abcd", label=ObjId(id="region", type="label"))),
    # ObjId instance
    ObjId(id="region", type="label"),
    dict(region=ObjId(id="region", type="label")),
]


@gd_vcr.use_cassette(str(_fixtures_dir / "simple_index_metrics.yaml"))
@pytest.mark.parametrize("index", index_types)
def test_simple_index_metrics(gdf: DataFrameFactory, index):
    df = gdf.indexed(
        index_by=index,
        columns=dict(
            region="label/region",
            category="label/products.category",
            price="fact/price",
        ),
    )

    assert len(df) == 17
    assert len(df.columns) == 3
    assert df.columns[0] == "region"
    assert df.columns[1] == "category"
    assert df.columns[2] == "price"


@gd_vcr.use_cassette(str(_fixtures_dir / "simple_index_metrics_no_duplicate.yaml"))
def test_simple_index_metrics_no_duplicate_index_col(gdf: DataFrameFactory):
    df = gdf.indexed(
        index_by="label/region",
        columns=dict(
            price="fact/price",
            quantity="fact/quantity",
        ),
    )

    assert len(df) == 5
    assert len(df.columns) == 2
    assert df.columns[0] == "price"
    assert df.columns[1] == "quantity"


@gd_vcr.use_cassette(str(_fixtures_dir / "simple_index_metrics_and_label.yaml"))
def test_simple_index_metrics_and_label(gdf: DataFrameFactory):
    columns = {
        "Price": "fact/price",
        "Quantity ($special$%^&)": "fact/quantity",
        "Region code ($special$%^&)": "label/region",
    }
    df = gdf.indexed(
        index_by=dict(reg="label/region"),
        columns=columns,
    )

    assert len(df) == 5
    assert len(df.columns) == 3
    for df_col_name, col_name in zip(df.columns, columns.keys()):
        assert df_col_name == col_name


@gd_vcr.use_cassette(str(_fixtures_dir / "simple_index_filtered_metrics_and_label.yaml"))
def test_simple_index_filtered_metrics_and_label(gdf: DataFrameFactory):
    df = gdf.indexed(
        index_by=dict(reg="label/region"),
        columns=dict(
            price="fact/price",
            quantity="fact/quantity",
            category="label/products.category",
        ),
        filter_by=[
            # Label referenced by localIdentifier
            PositiveAttributeFilter(label="reg", values=["Midwest"]),
            # Label referenced by full ID
            PositiveAttributeFilter(label="label/region", values=["Midwest"]),
            # Label referenced by ObjId
            PositiveAttributeFilter(label=ObjId(id="region", type="label"), values=["Midwest"]),
            # label referenced by index in columns
            PositiveAttributeFilter(label="category", values=["Clothing"]),
            MetricValueFilter(metric="price", operator="GREATER_THAN", values=100),
        ],
    )

    assert len(df) == 1
    assert len(df.columns) == 3
    assert df.columns[0] == "price"
    assert df.columns[1] == "quantity"
    assert df.columns[2] == "category"


@gd_vcr.use_cassette(str(_fixtures_dir / "multi_index_metrics.yaml"))
def test_multi_index_metrics(gdf: DataFrameFactory):
    df = gdf.indexed(
        index_by=dict(reg="label/region", category="label/products.category"),
        columns=dict(order_amount="metric/order_amount", order_count="metric/amount_of_orders"),
    )

    assert len(df) == 17
    assert len(df.columns) == 2
    assert df.index.names[0] == "reg"
    assert df.index.names[1] == "category"
    assert df.columns[0] == "order_amount"
    assert df.columns[1] == "order_count"


@gd_vcr.use_cassette(str(_fixtures_dir / "multi_index_metrics_and_label.yaml"))
def test_multi_index_metrics_and_label(gdf: DataFrameFactory):
    df = gdf.indexed(
        index_by=dict(reg="label/region", category="label/products.category"),
        columns=dict(
            order_amount="metric/order_amount",
            order_count="metric/amount_of_orders",
            state="label/state",
        ),
    )

    assert len(df) > 17
    assert len(df.columns) == 3
    assert df.index.names[0] == "reg"
    assert df.index.names[1] == "category"
    assert df.columns[0] == "order_amount"
    assert df.columns[1] == "order_count"
    assert df.columns[2] == "state"


@gd_vcr.use_cassette(str(_fixtures_dir / "multi_index_filtered_metrics_and_label.yaml"))
def test_multi_index_filtered_metrics_and_label(gdf: DataFrameFactory):
    df = gdf.indexed(
        index_by=dict(reg="label/region", category="label/products.category"),
        columns=dict(
            order_amount="metric/order_amount",
            order_count="metric/amount_of_orders",
            state="label/state",
        ),
        filter_by=[
            PositiveAttributeFilter(label="reg", values=["Northeast"]),
            MetricValueFilter(metric="order_count", operator="GREATER_THAN", values=50),
        ],
    )

    assert len(df) == 3
    assert len(df.columns) == 3
    assert df.index.names[0] == "reg"
    assert df.index.names[1] == "category"
    assert df.columns[0] == "order_amount"
    assert df.columns[1] == "order_count"
    assert df.columns[2] == "state"


@gd_vcr.use_cassette(str(_fixtures_dir / "multi_index_filtered_metrics_and_label_reuse.yaml"))
def test_multi_index_filtered_metrics_and_label_reuse(gdf: DataFrameFactory):
    # note here: if a single label is reused in both index and columns, that label will be used in computation
    # just once. the first-found occurrence will be used in computation. local id of the attribute will be
    # the key in the dict where the label was first found
    #
    # this has implications when referencing label by local id
    df = gdf.indexed(
        index_by=dict(reg="label/region", category="label/products.category"),
        columns=dict(
            order_amount="metric/order_amount",
            order_count="metric/amount_of_orders",
            reg="label/region",
        ),
        filter_by=[PositiveAttributeFilter(label="reg", values=["Midwest"])],
    )

    assert len(df) == 4
    assert len(df.columns) == 3
    assert df.index.names[0] == "reg"
    assert df.index.names[1] == "category"
    assert df.columns[0] == "order_amount"
    assert df.columns[1] == "order_count"
    assert df.columns[2] == "reg"


@gd_vcr.use_cassette(str(_fixtures_dir / "empty_indexed_dataframe.yaml"))
def test_empty_indexed_dataframe(gdf: DataFrameFactory):
    df = gdf.indexed(
        index_by="label/product_name",
        columns=dict(
            amount_of_top_customers="metric/amount_of_top_customers",
            total_revenue="metric/total_revenue-no_filters",
        ),
    )

    assert df.empty
    assert df.columns[0] == "amount_of_top_customers"
    assert df.columns[1] == "total_revenue"

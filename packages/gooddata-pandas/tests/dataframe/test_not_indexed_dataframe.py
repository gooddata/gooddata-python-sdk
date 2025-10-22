# (C) 2021 GoodData Corporation
from pathlib import Path

from gooddata_pandas import DataFrameFactory
from gooddata_sdk import ObjId, PositiveAttributeFilter, RelativeDateFilter, SimpleMetric
from tests_support.vcrpy_utils import get_vcr

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"


@gd_vcr.use_cassette(str(_fixtures_dir / "not_indexed_metrics.yaml"))
def test_not_indexed_metrics(gdf: DataFrameFactory):
    df = gdf.not_indexed(
        columns=dict(
            order_amount="metric/order_amount",
            order_count="metric/amount_of_orders",
        )
    )

    assert len(df) == 1
    assert len(df.columns) == 2
    assert df.columns[0] == "order_amount"
    assert df.columns[1] == "order_count"


@gd_vcr.use_cassette(str(_fixtures_dir / "not_indexed_metrics_and_labels.yaml"))
def test_not_indexed_metrics_and_labels(gdf: DataFrameFactory):
    df = gdf.not_indexed(
        columns=dict(
            reg="label/region",
            order_amount="metric/order_amount",
            order_count="metric/amount_of_orders",
        )
    )

    assert len(df) == 5
    assert len(df.columns) == 3
    assert df.columns[0] == "reg"
    assert df.columns[1] == "order_amount"
    assert df.columns[2] == "order_count"


@gd_vcr.use_cassette(str(_fixtures_dir / "not_indexed_filtered_metrics_and_labels.yaml"))
def test_not_indexed_filtered_metrics_and_labels(gdf: DataFrameFactory):
    df = gdf.not_indexed(
        columns=dict(
            reg="label/region",
            order_amount="metric/order_amount",
            order_count="metric/amount_of_orders",
        ),
        filter_by=[PositiveAttributeFilter(label="reg", values=["Midwest"])],
    )

    assert len(df) == 1
    assert len(df.columns) == 3
    assert df.columns[0] == "reg"
    assert df.columns[1] == "order_amount"
    assert df.columns[2] == "order_count"


@gd_vcr.use_cassette(str(_fixtures_dir / "empty_not_indexed_dataframe.yaml"))
def test_empty_not_indexed_dataframe(gdf: DataFrameFactory):
    df = gdf.not_indexed(
        columns=dict(
            product_name="label/product_name",
            amount_of_top_customers="metric/amount_of_top_customers",
            total_revenue="metric/total_revenue-no_filters",
        ),
    )

    assert df.empty
    assert df.columns[0] == "product_name"
    assert df.columns[1] == "amount_of_top_customers"
    assert df.columns[2] == "total_revenue"


@gd_vcr.use_cassette(str(_fixtures_dir / "filtered_empty_df.yaml"))
def test_filter_empty_df(gdf: DataFrameFactory):
    my_metric = SimpleMetric(local_id="m_revenue", item=ObjId(id="revenue", type="metric"))
    my_filter = RelativeDateFilter(
        dataset=ObjId(id="date", type="dataset"),
        granularity="YEAR",
        from_shift=1,
        to_shift=2,
    )
    df = gdf.not_indexed(columns=dict(my_metric=my_metric), filter_by=[my_filter])
    assert df.empty
    assert df.columns[0] == "my_metric"

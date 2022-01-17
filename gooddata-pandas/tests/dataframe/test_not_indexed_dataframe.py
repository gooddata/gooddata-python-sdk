# (C) 2021 GoodData Corporation
from pathlib import Path

import vcr

from gooddata_pandas import DataFrameFactory
from gooddata_sdk import PositiveAttributeFilter
from tests import VCR_MATCH_ON

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"

gd_vcr = vcr.VCR(filter_headers=["authorization", "user-agent"], serializer="json", match_on=VCR_MATCH_ON)


@gd_vcr.use_cassette(str(_fixtures_dir / "not_indexed_metrics.json"))
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


@gd_vcr.use_cassette(str(_fixtures_dir / "not_indexed_metrics_and_labels.json"))
def test_not_indexed_metrics_and_labels(gdf: DataFrameFactory):
    df = gdf.not_indexed(
        columns=dict(
            reg="label/customers.region",
            order_amount="metric/order_amount",
            order_count="metric/amount_of_orders",
        )
    )

    assert len(df) == 5
    assert len(df.columns) == 3
    assert df.columns[0] == "reg"
    assert df.columns[1] == "order_amount"
    assert df.columns[2] == "order_count"


@gd_vcr.use_cassette(str(_fixtures_dir / "not_indexed_filtered_metrics_and_labels.json"))
def test_not_indexed_filtered_metrics_and_labels(gdf: DataFrameFactory):
    df = gdf.not_indexed(
        columns=dict(
            reg="label/customers.region",
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

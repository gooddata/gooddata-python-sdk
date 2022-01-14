# (C) 2021 GoodData Corporation
from pathlib import Path

import vcr

from gooddata_pandas import DataFrameFactory

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"

gd_vcr = vcr.VCR(filter_headers=["authorization"], serializer="json")

_PREMIUM_REVENUE_STRUCTURE = "f7fef745-7269-454e-982e-e1d7d3eed81f"
"""
Simple insight with 2 labels and one metric
"""


@gd_vcr.use_cassette(str(_fixtures_dir / "dataframe_for_insight.json"))
def test_dataframe_for_insight(gdf: DataFrameFactory):
    df = gdf.for_insight(insight_id=_PREMIUM_REVENUE_STRUCTURE)

    assert df.index.names[0] == "car.car_make"
    assert df.index.names[1] == "customer.customer_age_group"
    assert df.columns[0] == "premium-revenue"


@gd_vcr.use_cassette(str(_fixtures_dir / "dataframe_for_insight_no_index.json"))
def test_dataframe_for_insight_no_index(gdf: DataFrameFactory):
    df = gdf.for_insight(insight_id=_PREMIUM_REVENUE_STRUCTURE, auto_index=False)

    assert df.columns[0] == "car.car_make"
    assert df.columns[1] == "customer.customer_age_group"
    assert df.columns[2] == "premium-revenue"

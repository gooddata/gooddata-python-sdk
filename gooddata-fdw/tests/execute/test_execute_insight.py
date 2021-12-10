# (C) 2021 GoodData Corporation
import os

import vcr

from gooddata_fdw import GoodDataForeignDataWrapper

_current_dir = os.path.dirname(os.path.abspath(__file__))
_fixtures_dir = os.path.join(_current_dir, "fixtures")

gd_vcr = vcr.VCR(filter_headers=["authorization"], serializer="json")


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "execute_insight_all_columns.json"))
def test_execute_insight_all_columns(fdw_options_for_insight, test_insight_columns):
    fdw = GoodDataForeignDataWrapper(fdw_options_for_insight, test_insight_columns)

    results = list(row for row in fdw.execute([], ["car_car_make", "customer_customer_age_group", "premium_revenue"]))

    assert len(results) == 146
    first_row = results[0]

    assert "car_car_make" in first_row
    assert "customer_customer_age_group" in first_row
    assert "premium_revenue" in first_row


@gd_vcr.use_cassette(os.path.join(_fixtures_dir, "execute_insight_some_columns.json"))
def test_execute_insight_some_columns(fdw_options_for_insight, test_insight_columns):
    fdw = GoodDataForeignDataWrapper(fdw_options_for_insight, test_insight_columns)

    results = list(row for row in fdw.execute([], ["premium_revenue"]))

    # selecting only some cols behaves like in normal table - the cardinality is same, the result rows
    # contain just the selected cols

    assert len(results) == 146
    first_row = results[0]

    assert "car_car_make" not in first_row
    assert "customer_customer_age_group" not in first_row
    assert "premium_revenue" in first_row

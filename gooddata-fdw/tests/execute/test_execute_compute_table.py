# (C) 2021 GoodData Corporation
import os

import vcr

from gooddata_fdw import GoodDataForeignDataWrapper

_current_dir = os.path.dirname(os.path.abspath(__file__))
_fixtures_dir = os.path.join(_current_dir, "fixtures")

gd_vcr = vcr.VCR(filter_headers=["authorization"], serializer="json")


@gd_vcr.use_cassette(
    os.path.join(_fixtures_dir, "execute_compute_table_all_columns.json")
)
def test_execute_compute_table_all_columns(
    fdw_options_for_compute_table, test_compute_table_columns
):
    fdw = GoodDataForeignDataWrapper(
        fdw_options_for_compute_table, test_compute_table_columns
    )

    results = list(
        row
        for row in fdw.execute(
            None, ["coverage_lifetime", "claim_amount", "car_make", "car_model"]
        )
    )

    # this is cardinality when selecting on finest granularity (all labels in compute table)
    assert len(results) == 101
    first_row = results[0]

    assert "coverage_lifetime" in first_row
    assert "claim_amount" in first_row
    assert "car_make" in first_row
    assert "car_model" in first_row


@gd_vcr.use_cassette(
    os.path.join(_fixtures_dir, "execute_compute_table_metrics_only.json")
)
def test_execute_compute_table_metrics_only(
    fdw_options_for_compute_table, test_compute_table_columns
):
    fdw = GoodDataForeignDataWrapper(
        fdw_options_for_compute_table, test_compute_table_columns
    )

    results = list(
        row for row in fdw.execute(None, ["coverage_lifetime", "claim_amount"])
    )

    # selecting just metrics means no granularity and full aggregation of the metric values
    assert len(results) == 1
    first_row = results[0]

    assert "coverage_lifetime" in first_row
    assert "claim_amount" in first_row


@gd_vcr.use_cassette(
    os.path.join(_fixtures_dir, "execute_compute_table_with_reduced_granularity.json")
)
def test_execute_compute_table_with_reduced_granularity(
    fdw_options_for_compute_table, test_compute_table_columns
):
    fdw = GoodDataForeignDataWrapper(
        fdw_options_for_compute_table, test_compute_table_columns
    )

    results = list(
        row
        for row in fdw.execute(None, ["car_make", "coverage_lifetime", "claim_amount"])
    )

    # selecting on reduced granularity (1 label instead of both) means the metric values are aggregated for
    # that one label only - cardinality differs again
    assert len(results) == 46
    first_row = results[0]

    assert "car_make" in first_row
    assert "coverage_lifetime" in first_row
    assert "claim_amount" in first_row

# (C) 2021 GoodData Corporation
from pathlib import Path

import vcr

from gooddata_fdw import GoodDataForeignDataWrapper
from tests import VCR_MATCH_ON

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"

gd_vcr = vcr.VCR(filter_headers=["authorization", "user-agent"], serializer="json", match_on=VCR_MATCH_ON)


@gd_vcr.use_cassette(str(_fixtures_dir / "execute_compute_table_all_columns.json"))
def test_execute_compute_table_all_columns(fdw_options_for_compute_table, test_compute_table_columns):
    fdw = GoodDataForeignDataWrapper(fdw_options_for_compute_table, test_compute_table_columns)

    results = list(row for row in fdw.execute([], test_compute_table_columns.keys()))

    # this is cardinality when selecting on finest granularity (all labels in compute table)
    assert len(results) == 18
    first_row = results[0]
    assert len(first_row) == len(test_compute_table_columns)
    for column in test_compute_table_columns:
        assert column in first_row


@gd_vcr.use_cassette(str(_fixtures_dir / "execute_compute_table_metrics_only.json"))
def test_execute_compute_table_metrics_only(fdw_options_for_compute_table, test_compute_table_columns):
    fdw = GoodDataForeignDataWrapper(fdw_options_for_compute_table, test_compute_table_columns)

    fact_metric_columns = ["order_lines_quantity", "order_lines_price", "percent_revenue_in_category", "revenue"]
    results = list(row for row in fdw.execute([], fact_metric_columns))

    # selecting just metrics means no granularity and full aggregation of the metric values
    assert len(results) == 1
    first_row = results[0]
    assert len(first_row) == len(fact_metric_columns)
    for column in fact_metric_columns:
        assert column in first_row


@gd_vcr.use_cassette(str(_fixtures_dir / "execute_compute_table_with_reduced_granularity.json"))
def test_execute_compute_table_with_reduced_granularity(fdw_options_for_compute_table, test_compute_table_columns):
    fdw = GoodDataForeignDataWrapper(fdw_options_for_compute_table, test_compute_table_columns)

    test_columns = ["products_category", "order_lines_quantity", "revenue"]
    results = list(row for row in fdw.execute([], test_columns))

    # selecting on reduced granularity (1 label instead of both) means the metric values are aggregated for
    # that one label only - cardinality differs again
    assert len(results) == 4
    first_row = results[0]
    assert len(first_row) == len(test_columns)
    for column in test_columns:
        assert column in first_row

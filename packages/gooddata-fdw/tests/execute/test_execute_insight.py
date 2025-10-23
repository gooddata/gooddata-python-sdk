# (C) 2021 GoodData Corporation
from pathlib import Path

from gooddata_fdw import GoodDataForeignDataWrapper
from tests_support.vcrpy_utils import get_vcr

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"


@gd_vcr.use_cassette(str(_fixtures_dir / "execute_insight_all_columns.yaml"))
def test_execute_insight_all_columns(fdw_options_for_insight, test_insight_columns):
    fdw = GoodDataForeignDataWrapper(fdw_options_for_insight, test_insight_columns)

    results = list(row for row in fdw.execute([], test_insight_columns.keys()))

    assert len(results) == 18
    first_row = results[0]
    assert len(first_row) == len(test_insight_columns)
    for column in test_insight_columns:
        assert column in first_row


@gd_vcr.use_cassette(str(_fixtures_dir / "execute_insight_some_columns.yaml"))
def test_execute_insight_some_columns(fdw_options_for_insight, test_insight_columns):
    fdw = GoodDataForeignDataWrapper(fdw_options_for_insight, test_insight_columns)

    results = list(row for row in fdw.execute([], ["revenue"]))

    # selecting only some cols behaves like in normal table - the cardinality is same, the result rows
    # contain just the selected cols

    assert len(results) == 18
    first_row = results[0]
    assert len(first_row) == 1
    assert "revenue" in first_row

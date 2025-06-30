# (C) 2022 GoodData Corporation
from collections import OrderedDict
from datetime import date
from unittest import mock

import pytest
from gooddata_fdw.environment import ColumnDefinition
from gooddata_fdw.result_reader import InsightTableResultReader, TableResultReader


@pytest.fixture
def table_columns():
    columns = OrderedDict()
    columns["coverage_lifetime"] = ColumnDefinition(
        column_name="coverage_lifetime",
        type_name="DECIMAL(15,5)",
        options=dict(id="fact/coverage.coverage_lifetime", local_id="1"),
    )
    columns["claim_amount"] = ColumnDefinition(
        column_name="claim_amount",
        type_name="DECIMAL(15,5)",
        options=dict(id="metric/claim-amount", local_id="2"),
    )
    columns["car_make"] = ColumnDefinition(
        column_name="car_make",
        type_name="VARCHAR(255)",
        options=dict(id="label/car.car_make", local_id="3"),
    )
    columns["datetime"] = ColumnDefinition(
        column_name="datetime",
        type_name="DATE",
        options=dict(id="label/datetime.day", local_id="4"),
    )

    return columns


def test_table_result_reader(table_columns):
    executor_output = [
        {
            "coverage_lifetime": 125.5,
            "claim_amount": "55.6",
            "car_make": "A",
            "datetime": "2021-03-15",
        },
    ]
    expected = [
        {
            "coverage_lifetime": 125.5,
            "claim_amount": "55.6",
            "car_make": "A",
            "datetime": date(2021, 3, 15),
        },
    ]
    exec_table_mock = mock.Mock(name="ExecTableMock", spec=["read_all"])
    exec_table_mock.read_all.return_value = executor_output
    tr = TableResultReader(table_columns)
    result = list(tr.read_all_rows(exec_table_mock))

    assert len(result) == len(expected)
    for result_row, expected_row in zip(result, expected):
        assert result_row == expected_row


def test_insight_table_result_reader(table_columns):
    executor_output = [
        {"1": 125.5, "2": "55.6", "3": "A", "4": "2021-03-15"},
    ]
    query_columns = ["coverage_lifetime", "car_make", "datetime"]
    expected = [
        {"coverage_lifetime": 125.5, "car_make": "A", "datetime": date(2021, 3, 15)},
    ]
    exec_table_mock = mock.Mock(name="ExecTableMock", spec=["read_all"])
    exec_table_mock.read_all.return_value = executor_output
    tr = InsightTableResultReader(table_columns, query_columns)
    result = list(tr.read_all_rows(exec_table_mock))

    assert len(result) == len(expected)
    for result_row, expected_row in zip(result, expected):
        assert result_row == expected_row

# (C) 2021 GoodData Corporation

import datetime
from collections import OrderedDict

import pytest
from gooddata_fdw.environment import ColumnDefinition, Qual
from gooddata_fdw.filter import MAX_DATE, MIN_DATE, extract_filters_from_quals
from gooddata_sdk import AbsoluteDateFilter, ObjId, PositiveAttributeFilter

start_date = datetime.date(2021, 1, 1)
end_date = datetime.date(2021, 2, 1)


@pytest.fixture
def test_filter_columns():
    columns = OrderedDict()
    # attribute
    columns["car_model"] = ColumnDefinition(
        column_name="car_model",
        type_name="VARCHAR(255)",
        options=dict(id="label/car.car_model"),
    )
    # DATE dimension
    columns["datetime"] = ColumnDefinition(
        column_name="datetime",
        type_name="DATE",
        options=dict(id="label/datetime.day"),
    )

    return columns


test_data = [
    [
        [Qual("datetime", ">=", start_date), Qual("car_model", ("=", True), ["Tesla", "Škoda"])],
        [
            AbsoluteDateFilter(ObjId("datetime", "dataset"), "2021-01-01", MAX_DATE),
            PositiveAttributeFilter("car_model", ["Tesla", "Škoda"]),
        ],
    ],
    [
        # This represents SQL BETWEEN operation
        [Qual("datetime", ">=", start_date), Qual("datetime", "<=", end_date)],
        [
            AbsoluteDateFilter(ObjId("datetime", "dataset"), "2021-01-01", MAX_DATE),
            AbsoluteDateFilter(ObjId("datetime", "dataset"), MIN_DATE, "2021-02-02"),
        ],
    ],
    [
        [Qual("datetime", "=", start_date)],
        [
            AbsoluteDateFilter(ObjId("datetime", "dataset"), "2021-01-01", "2021-01-02"),
        ],
    ],
    [
        [Qual("datetime", ">", start_date), Qual("datetime", "<", end_date)],
        [
            AbsoluteDateFilter(ObjId("datetime", "dataset"), "2021-01-02", MAX_DATE),
            AbsoluteDateFilter(ObjId("datetime", "dataset"), MIN_DATE, "2021-02-01"),
        ],
    ],
]


@pytest.mark.parametrize("quals,expected", test_data)
def test_quals(test_filter_columns, quals, expected):
    filters = extract_filters_from_quals(quals, test_filter_columns)

    assert filters == expected

# (C) 2021 GoodData Corporation

import datetime

import pytest

from gooddata_fdw.environment import Qual
from gooddata_fdw.fdw import MAX_DATE, MIN_DATE, GoodDataForeignDataWrapper
from gooddata_sdk.compute_model import AbsoluteDateFilter, ObjId, PositiveAttributeFilter

start_date = datetime.date(2021, 1, 1)
end_date = datetime.date(2021, 2, 1)


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
def test_quals(fdw_options_for_compute_table, test_compute_table_columns, quals, expected):
    fdw = GoodDataForeignDataWrapper(fdw_options_for_compute_table, test_compute_table_columns)
    filters = fdw.extract_filters_from_quals(quals)

    assert filters == expected

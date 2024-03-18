# (C) 2022 GoodData Corporation
import gooddata_fdw.column_validation as col_val
import pytest
from gooddata_fdw.environment import ColumnDefinition


@pytest.mark.parametrize(
    "table_columns,query_columns",
    [
        (dict(a=1, b=2), []),
        (dict(a=1, b=2), ["a"]),
        (dict(a=1, b=2), ["a", "b"]),
    ],
    ids=["empty", "one", "two"],
)
def test_validate_columns_in_table_def_ok(table_columns, query_columns):
    col_val.validate_columns_in_table_def(table_columns, query_columns)


@pytest.mark.parametrize(
    "table_columns,query_columns",
    [
        (dict(a=1, b=2), ["c"]),
        (dict(a=1, b=2), ["a", "c"]),
    ],
    ids=["wrong", "mixed-wrong"],
)
def test_validate_columns_in_table_def_exc(table_columns, query_columns):
    with pytest.raises(ValueError):
        col_val.validate_columns_in_table_def(table_columns, query_columns)


@pytest.mark.parametrize(
    "validator,column_def",
    [
        (col_val.LocalIdOptionValidator(), ColumnDefinition("n", "t", dict(local_id="lid"))),
        (col_val.IdOptionValidator(mandatory=True), ColumnDefinition("n", "t", dict(id="metric/claim-amount"))),
        (col_val.IdOptionValidator(mandatory=False), ColumnDefinition("n", "t", dict(id="fact/fact-amount"))),
        (col_val.IdOptionValidator(mandatory=False), ColumnDefinition("n", "t", dict(id="label/label-amount"))),
        (col_val.IdOptionValidator(mandatory=False), ColumnDefinition("n", "t", dict(local_id="lid"))),
    ],
    ids=["local-id", "id-mandatory", "id-optional-is1", "id-optional-is2", "id-optional-miss"],
)
def test_column_validation_ok(validator, column_def):
    validator.validate("n", column_def)


@pytest.mark.parametrize(
    "validator,column_def",
    [
        (col_val.LocalIdOptionValidator(), ColumnDefinition("n", "t", dict(id="dummy"))),
        (col_val.IdOptionValidator(mandatory=True), ColumnDefinition("n", "t", dict())),
        (col_val.IdOptionValidator(mandatory=False), ColumnDefinition("n", "t", dict(id="nonsense/fact-amount"))),
    ],
    ids=["local-id", "id-mandatory", "id-optional"],
)
def test_column_validation_exc(validator, column_def):
    with pytest.raises(ValueError):
        validator.validate("n", column_def)

# (C) 2022 GoodData Corporation
from __future__ import annotations

from collections.abc import Generator
from typing import Any

from gooddata_sdk import ExecutionTable
from gooddata_sdk.type_converter import DBTypeConverterStore

import gooddata_fdw.column_validation as col_valid
from gooddata_fdw.environment import ColumnDefinition


class TableResultReader:
    def __init__(self, table_columns: dict[str, ColumnDefinition]) -> None:
        self._table_columns = table_columns

    def read_all_rows(self, table: ExecutionTable) -> Generator[dict[str, Any], None, None]:
        for result_row in table.read_all():
            yield self._process_row(result_row)

    def _process_row(self, row: dict[str, Any]) -> dict[str, Any]:
        return {k: self._sanitize_value(k, v) for k, v in row.items()}

    def _sanitize_value(self, column_name: str, value: Any) -> Any:
        """Alter the value to comply with postgres data type"""
        if not isinstance(value, str):
            return value

        type_name = self._table_columns[column_name].base_type_name
        converter = DBTypeConverterStore.find_converter(type_name.lower())
        return converter.to_type(value)


class InsightTableResultReader(TableResultReader):
    def __init__(self, table_columns: dict[str, ColumnDefinition], query_columns: list[str]) -> None:
        super().__init__(table_columns)
        self._query_columns = query_columns
        col_valid.validate_columns_in_table_def(self._table_columns, self._query_columns)

        self._col_to_local_id = {c.column_name: c.options["local_id"] for c in self._table_columns.values()}

    def _process_row(self, row: dict[str, Any]) -> dict[str, Any]:
        return {
            column_name: self._sanitize_value(column_name, row[self._col_to_local_id[column_name]])
            for column_name in self._query_columns
        }

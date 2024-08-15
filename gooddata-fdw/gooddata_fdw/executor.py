# (C) 2022 GoodData Corporation
from __future__ import annotations

from collections.abc import Generator
from typing import Any, NamedTuple, Optional

from gooddata_sdk import GoodDataSdk

import gooddata_fdw.column_validation as col_val
from gooddata_fdw import column_utils
from gooddata_fdw.environment import ColumnDefinition, Qual
from gooddata_fdw.filter import extract_filters_from_quals
from gooddata_fdw.options import ServerOptions, TableOptions
from gooddata_fdw.result_reader import InsightTableResultReader, TableResultReader


class InitData(NamedTuple):
    sdk: GoodDataSdk
    server_options: ServerOptions
    table_options: TableOptions
    columns: dict[str, ColumnDefinition]


class Executor:
    def __init__(self, inputs: InitData, column_validators: list[col_val.ColumnValidator]) -> None:
        self._sdk = inputs.sdk
        self._table_columns = inputs.columns
        self._column_validators = column_validators

    @classmethod
    def can_react(cls, inputs: InitData) -> bool:
        return False

    def validate_columns_def(self) -> None:
        for column_name, column_def in self._table_columns.items():
            for validator in self._column_validators:
                validator.validate(column_name, column_def)

    def execute(
        self, quals: list[Qual], columns: list[str], sort_keys: Optional[list[Any]] = None
    ) -> Generator[dict[str, Any], None, None]:
        raise NotImplementedError()


class InsightExecutor(Executor):
    _COLUMN_VALIDATORS = [col_val.LocalIdOptionValidator(), col_val.IdOptionValidator(mandatory=False)]

    def __init__(self, inputs: InitData) -> None:
        super().__init__(inputs, self._COLUMN_VALIDATORS)
        self._workspace = inputs.table_options.workspace

        assert inputs.table_options.insight is not None
        self._insight = inputs.table_options.insight

        self._table_columns = inputs.columns

    @classmethod
    def can_react(cls, inputs: InitData) -> bool:
        return inputs.table_options.insight is not None

    def execute(
        self, quals: list[Qual], columns: list[str], sort_keys: Optional[list[Any]] = None
    ) -> Generator[dict[str, Any], None, None]:
        results_reader = InsightTableResultReader(self._table_columns, columns)
        insight = self._sdk.visualizations.get_visualization(self._workspace, self._insight)
        table = self._sdk.tables.for_visualization(self._workspace, insight)

        return results_reader.read_all_rows(table)


class ComputeExecutor(Executor):
    _COLUMN_VALIDATORS: list[col_val.ColumnValidator] = [col_val.IdOptionValidator(mandatory=True)]

    def __init__(self, inputs: InitData) -> None:
        super().__init__(inputs, self._COLUMN_VALIDATORS)
        self._workspace = inputs.table_options.workspace
        self._results_reader = TableResultReader(self._table_columns)

    @classmethod
    def can_react(cls, inputs: InitData) -> bool:
        return inputs.table_options.compute is not None

    def execute(
        self, quals: list[Qual], columns: list[str], sort_keys: Optional[list[Any]] = None
    ) -> Generator[dict[str, Any], None, None]:
        col_val.validate_columns_in_table_def(self._table_columns, columns)
        items = [column_utils.table_col_as_computable(self._table_columns[col_name]) for col_name in columns]
        # TODO: push down more filters that are included in quals
        filters = extract_filters_from_quals(quals, self._table_columns)
        table = self._sdk.tables.for_items(self._workspace, items, filters)

        return self._results_reader.read_all_rows(table)


class CustomExecutor(Executor):
    _COLUMN_VALIDATORS: list[col_val.ColumnValidator] = [col_val.IdOptionValidator(mandatory=True)]

    def __init__(self, inputs: InitData) -> None:
        super().__init__(inputs, self._COLUMN_VALIDATORS)
        self._workspace = inputs.table_options.workspace
        self._results_reader = TableResultReader(self._table_columns)

    @classmethod
    def can_react(cls, inputs: InitData) -> bool:
        return True

    def execute(
        self, quals: list[Qual], columns: list[str], sort_keys: Optional[list[Any]] = None
    ) -> Generator[dict[str, Any], None, None]:
        items = [column_utils.table_col_as_computable(col) for col in self._table_columns.values()]
        # TODO: pushdown more filters that are included in quals
        filters = extract_filters_from_quals(quals, self._table_columns)
        table = self._sdk.tables.for_items(self._workspace, items, filters)

        return self._results_reader.read_all_rows(table)


class ExecutorFactory:
    # Order is important - first executor supporting InitData is used
    _SUPPOERTED_EXECUTORS = [InsightExecutor, ComputeExecutor, CustomExecutor]

    @classmethod
    def create(cls, inputs: InitData) -> Executor:
        for executor in cls._SUPPOERTED_EXECUTORS:
            if executor.can_react(inputs):
                return executor(inputs)

        raise ValueError(f"No executor supports initial data {str(inputs)}")

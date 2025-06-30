# (C) 2021 GoodData Corporation
from __future__ import annotations

import traceback
from typing import Any, Optional

from gooddata_sdk import GoodDataSdk

from gooddata_fdw import __version__
from gooddata_fdw.environment import ColumnDefinition, ForeignDataWrapper, Qual, TableDefinition
from gooddata_fdw.executor import ExecutorFactory, InitData
from gooddata_fdw.import_workspace import ImporterInitData, WorkspaceImportersLocator
from gooddata_fdw.options import ImportSchemaOptions, ServerOptions, TableOptions
from gooddata_fdw.pg_logging import _log_debug, _log_error, _log_info

USER_AGENT = f"gooddata-fdw/{__version__}"
"""Extra segment of the User-Agent header that will be appended to standard gooddata-sdk user agent."""


class GoodDataForeignDataWrapper(ForeignDataWrapper):
    def __init__(self, options: dict[str, str], columns: dict[str, ColumnDefinition]) -> None:
        super().__init__(options, columns)
        _log_debug(f"initializing (options={options}, columns={columns})")

        # Table options contain also foreign server options
        self._server_options = ServerOptions(options)
        self._table_options = TableOptions(options)

        self._columns = columns
        gd_sdk = GoodDataSdk.create(
            self._server_options.host, self._server_options.token, USER_AGENT, Host=self._server_options.headers_host
        )

        self._executor = ExecutorFactory.create(InitData(gd_sdk, self._server_options, self._table_options, columns))
        self._executor.validate_columns_def()

    def execute(self, quals: list[Qual], columns: list[str], sortkeys: Optional[list[Any]] = None):  # type: ignore
        _log_debug(f"query in fdw with {self._server_options}; {self._table_options}; columns {columns}; quals={quals}")
        try:
            return self._executor.execute(quals, columns, sortkeys)
        except Exception as e:
            _log_error(traceback.format_exc())
            raise e

    @classmethod
    def import_schema(
        cls,
        schema: str,
        srv_options: dict[str, str],
        options: dict[str, str],
        restriction_type: Optional[str],
        restricts: list[str],
    ) -> list[TableDefinition]:  # type: ignore
        _log_info(
            f"import fdw {schema} (srv_options={srv_options}, "
            f"options={options}, restriction_type={restriction_type}, restricts={restricts})"
        )

        try:
            server_options = ServerOptions(srv_options)
            import_options = ImportSchemaOptions(options)

            importer_classes = WorkspaceImportersLocator.locate(import_options.object_type)

            _sdk = GoodDataSdk.create(
                server_options.host, server_options.token, USER_AGENT, Host=server_options.headers_host
            )
            init_data = ImporterInitData(_sdk, schema, server_options, import_options, restriction_type, restricts)
            tables = []
            for importer_class in importer_classes:
                instance = importer_class(init_data)
                tables += instance.import_tables()
            return tables
        except Exception as e:
            _log_error(traceback.format_exc())
            raise e

    @property
    def rowid_column(self):  # type: ignore
        return super().rowid_column

    def insert(self, values):  # type: ignore
        return super().insert(values)

    def update(self, oldvalues, newvalues):  # type: ignore
        return super().update(oldvalues, newvalues)

    def delete(self, oldvalues):  # type: ignore
        return super().delete(oldvalues)

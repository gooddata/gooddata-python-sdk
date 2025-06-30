# (C) 2021 GoodData Corporation
"""
This file exists because multicorn is not available as proper stand-alone python package that one could install
and then use the different data types during testing.

The multicorn python code is part of the PostgreSQL extension installation.

Thus here is the layer of indirection that tries to import multicorn code and if that is not
present (likely during test run) it will use stub implementations.

The stubbing only happens if the FDW code is called during test execution. Otherwise the import error is raised
as usual to prevent some wicked behavior on mis-configured PostgreSQL.
"""

from __future__ import annotations

from typing import Any, Optional, Union

try:
    import multicorn
    from multicorn import utils

    ForeignDataWrapper = multicorn.ForeignDataWrapper
    TableDefinition = multicorn.TableDefinition
    ColumnDefinition = multicorn.ColumnDefinition
    Qual = multicorn.Qual
    log_to_postgres = utils.log_to_postgres
except ImportError as e:
    # determine if running as part of test suite
    # see: https://stackoverflow.com/questions/25188119/test-if-code-is-executed-from-within-a-py-test-session
    #
    # this is ideal solution. the one with using pytest_configure() is tricky because trying to set some
    # package-specific global variable would inevitably lead to evaluation of __init__ which imports the FDW code
    # which will then try to import from this file before the variable is even set
    import sys

    if "pytest" not in sys.modules and "sphinx" not in sys.modules:
        # multicorn stuff cannot be imported & the FDW code is not currently under test or as documentation build.
        # in that case raise the error normally.
        raise e

    def _log_to_console(msg: str, level: int) -> None:
        from logging import getLevelName

        print(f"{getLevelName(level)}: {msg}")

    log_to_postgres = _log_to_console

    class ColumnDefinitionStub:
        def __init__(self, column_name: str, type_name: str, options: dict[str, str]) -> None:
            self.column_name = column_name
            self.type_name = type_name
            self.base_type_name = type_name
            self.options = options

    ColumnDefinition = ColumnDefinitionStub

    class QualStub:
        def __init__(self, field_name: str, operator: Union[str, tuple[str, str]], value: Any) -> None:
            self.field_name = field_name
            self.operator = operator
            self.value = value

    Qual = QualStub

    class TableDefinitionStub:
        def __init__(
            self,
            table_name: str,
            columns: list[ColumnDefinition],  # type: ignore
            options: dict[str, str],  # type: ignore
        ) -> None:
            self.table_name = table_name
            self.columns = columns
            self.options = options
            self.col_idx = dict([(c.column_name, c) for c in columns])  # type: ignore

    TableDefinition = TableDefinitionStub

    class ForeignDataWrapperStub:
        def __init__(self, options: dict[str, str], columns: dict[str, ColumnDefinition]) -> None:  # type: ignore
            self.options = options
            self.columns = columns

        @classmethod
        def import_schema(
            cls,
            schema: str,
            srv_options: dict[str, str],
            options: dict[str, str],
            restriction_type: Optional[str],
            restricts: list[str],
        ) -> list[TableDefinition]:  # type: ignore
            return NotImplemented

        def execute(self, quals: list[Qual], columns: list[str], sortkeys: Optional[list[Any]] = None):  # type: ignore
            pass

    ForeignDataWrapper = ForeignDataWrapperStub

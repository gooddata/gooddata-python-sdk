# (C) 2023 GoodData Corporation
from __future__ import annotations

from typing import Type

import attr

from gooddata_api_client.model.scan_sql_response import ScanSqlResponse as ApiScanSqlResponse
from gooddata_api_client.model.sql_column import SqlColumn
from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class ScanSqlColumn(Base):
    data_type: str
    name: str

    @staticmethod
    def client_class() -> Type[SqlColumn]:
        return SqlColumn


@attr.s(auto_attribs=True, kw_only=True)
class ScanSqlResponse(Base):
    columns: list[ScanSqlColumn]
    data_preview: list[list[str]]

    @staticmethod
    def client_class() -> Type[ApiScanSqlResponse]:
        return ApiScanSqlResponse

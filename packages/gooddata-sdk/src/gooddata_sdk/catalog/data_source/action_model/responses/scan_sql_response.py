# (C) 2023 GoodData Corporation
from __future__ import annotations

import attr
from gooddata_api_client.model.scan_sql_response import ScanSqlResponse as ApiScanSqlResponse

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.data_source.action_model.sql_column import SqlColumn


@attr.s(auto_attribs=True, kw_only=True)
class ScanSqlResponse(Base):
    columns: list[SqlColumn]
    data_preview: list[list[str | None]] | None = None

    @staticmethod
    def client_class() -> type[ApiScanSqlResponse]:
        return ApiScanSqlResponse

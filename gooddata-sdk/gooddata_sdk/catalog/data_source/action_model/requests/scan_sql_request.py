# (C) 2023 GoodData Corporation
from __future__ import annotations

import attr
from gooddata_api_client.model.scan_sql_request import ScanSqlRequest as ApiScanSqlRequest

from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class ScanSqlRequest(Base):
    sql: str

    @staticmethod
    def client_class() -> type[ApiScanSqlRequest]:
        return ApiScanSqlRequest

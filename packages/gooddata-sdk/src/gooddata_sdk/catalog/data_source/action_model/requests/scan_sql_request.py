# (C) 2023 GoodData Corporation
from __future__ import annotations

from attrs import define
from gooddata_api_client.model.scan_sql_request import ScanSqlRequest as ApiScanSqlRequest

from gooddata_sdk.catalog.base import Base


@define(kw_only=True)
class ScanSqlRequest(Base):
    sql: str

    @staticmethod
    def client_class() -> type[ApiScanSqlRequest]:
        return ApiScanSqlRequest

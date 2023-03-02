# (C) 2023 GoodData Corporation
from __future__ import annotations

from typing import List, Optional, Type

import attr

from gooddata_api_client.model.scan_sql_response import ScanSqlResponse as ApiScanSqlResponse
from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.data_source.action_model.sql_column import SqlColumn


@attr.s(auto_attribs=True, kw_only=True)
class ScanSqlResponse(Base):
    columns: List[SqlColumn]
    data_preview: Optional[List[List[Optional[str]]]] = None

    @staticmethod
    def client_class() -> Type[ApiScanSqlResponse]:
        return ApiScanSqlResponse

# (C) 2023 GoodData Corporation
from __future__ import annotations

from attrs import define
from gooddata_api_client.model.sql_column import SqlColumn as ApiSqlColumn

from gooddata_sdk.catalog.base import Base


@define(kw_only=True)
class SqlColumn(Base):
    data_type: str
    name: str

    @staticmethod
    def client_class() -> type[ApiSqlColumn]:
        return ApiSqlColumn

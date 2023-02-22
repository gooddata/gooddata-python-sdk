# (C) 2023 GoodData Corporation
from __future__ import annotations

from typing import Type

import attr

from gooddata_api_client.model.sql_column import SqlColumn as ApiSqlColumn
from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class SqlColumn(Base):
    data_type: str
    name: str

    @staticmethod
    def client_class() -> Type[ApiSqlColumn]:
        return ApiSqlColumn

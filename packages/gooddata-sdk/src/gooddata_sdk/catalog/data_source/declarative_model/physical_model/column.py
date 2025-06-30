# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Optional

import attr
from gooddata_api_client.model.declarative_column import DeclarativeColumn

from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeColumn(Base):
    name: str
    data_type: str
    is_primary_key: Optional[bool] = None
    referenced_table_id: Optional[str] = None
    referenced_table_column: Optional[str] = None

    @staticmethod
    def client_class() -> type[DeclarativeColumn]:
        return DeclarativeColumn

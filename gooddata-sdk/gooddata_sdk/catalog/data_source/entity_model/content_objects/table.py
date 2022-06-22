# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import List, Optional

import attr

from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDataSourceTable(Base):
    id: str
    type: str
    attributes: CatalogDataSourceTableAttributes


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDataSourceTableAttributes(Base):
    columns: List[CatalogDataSourceTableColumn]
    name_prefix: Optional[str] = None
    path: Optional[List[str]] = None
    type: Optional[str] = None


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDataSourceTableColumn(Base):
    name: str
    data_type: str
    is_primary_key: Optional[bool] = None
    referenced_table_column: Optional[str] = None
    referenced_table_id: Optional[str] = None

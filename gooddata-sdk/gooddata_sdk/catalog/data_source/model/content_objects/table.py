# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any, List

from gooddata_sdk.catalog.entity import CatalogEntity


class CatalogDataSourceTable(CatalogEntity):
    @property
    def table_type(self) -> str:
        return self._e["type"]

    @property
    def path(self) -> List[str]:
        return self._e["path"]

    @property
    def columns(self) -> List[CatalogDataSourceTableColumn]:
        return [CatalogDataSourceTableColumn(c) for c in self._e["columns"]]

    @property
    def username(self) -> str:
        return self._e["username"]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, path={str(self.path)})"


class CatalogDataSourceTableColumn:
    def __init__(self, column: dict[str, Any]) -> None:
        self._c = column

    @property
    def name(self) -> str:
        return self._c["name"]

    @property
    def data_type(self) -> str:
        return self._c["dataType"]

    @property
    def referenced_table_id(self) -> str:
        return self._c["referencedTableId"]

    @property
    def referenced_table_column(self) -> str:
        return self._c["referencedTableColumn"]

    @property
    def primary_key(self) -> str:
        return self._c["primaryKey"]

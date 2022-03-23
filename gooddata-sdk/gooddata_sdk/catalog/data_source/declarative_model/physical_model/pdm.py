# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any

from gooddata_metadata_client.model.declarative_tables import DeclarativeTables
from gooddata_sdk.catalog.data_source.declarative_model.physical_model.table import CatalogDeclarativeTable


class CatalogDeclarativeTables:
    def __init__(
        self,
        tables: list[CatalogDeclarativeTable],
    ):
        self.tables = tables

    @classmethod
    def from_api(cls, entity: dict[str, list[Any]]) -> CatalogDeclarativeTables:
        tables = [CatalogDeclarativeTable.from_api(v) for v in entity["tables"]] if entity.get("tables") else []
        return cls(tables)

    def to_api(self) -> DeclarativeTables:
        return DeclarativeTables(tables=[v.to_api() for v in self.tables])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogDeclarativeTables):
            return False
        return self.tables == other.tables

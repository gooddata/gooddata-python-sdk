# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any, Optional

from gooddata_metadata_client.model.declarative_column import DeclarativeColumn


class CatalogDeclarativeColumn:
    def __init__(
        self,
        name: str,
        data_type: str,
        is_primary_key: Optional[bool],
        referenced_table_id: Optional[str],
        referenced_table_column: Optional[str],
    ):
        self.name = name
        self.data_type = data_type
        self.is_primary_key = is_primary_key
        self.referenced_table_id = referenced_table_id
        self.referenced_table_column = referenced_table_column

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDeclarativeColumn:
        return cls(
            name=entity["name"],
            data_type=entity["data_type"],
            is_primary_key=entity.get("is_primary_key"),
            referenced_table_id=entity.get("referenced_table_id"),
            referenced_table_column=entity.get("referenced_table_column"),
        )

    def to_api(self) -> DeclarativeColumn:
        kwargs: dict[str, Any] = dict()
        if self.is_primary_key is not None:
            kwargs["is_primary_key"] = self.is_primary_key
        if self.referenced_table_id is not None:
            kwargs["referenced_table_id"] = self.referenced_table_id
        if self.referenced_table_column is not None:
            kwargs["referenced_table_column"] = self.referenced_table_column
        return DeclarativeColumn(name=self.name, data_type=self.data_type, **kwargs)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogDeclarativeColumn):
            return False
        return (
            self.name == other.name
            and self.data_type == other.data_type
            and self.is_primary_key == other.is_primary_key
            and self.referenced_table_id == other.referenced_table_id
            and self.referenced_table_column == other.referenced_table_column
        )

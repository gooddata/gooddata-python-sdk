# (C) 2022 GoodData Corporation
from __future__ import annotations

import builtins
from pathlib import Path
from typing import Optional

import attr
from gooddata_api_client.model.declarative_table import DeclarativeTable

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.data_source.declarative_model.physical_model.column import CatalogDeclarativeColumn
from gooddata_sdk.utils import read_layout_from_file, write_layout_to_file


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeTable(Base):
    id: str
    type: str
    path: list[str]
    columns: list[CatalogDeclarativeColumn]
    name_prefix: Optional[str] = None

    @staticmethod
    def client_class() -> builtins.type[DeclarativeTable]:
        return DeclarativeTable

    def store_to_disk(self, pdm_folder: Path) -> None:
        table_dict = self.to_api().to_dict(camel_case=True)
        table_file_path = pdm_folder / f"{self.id}.yaml"
        write_layout_to_file(table_file_path, table_dict)

    @classmethod
    def load_from_disk(cls, table_file_path: Path) -> CatalogDeclarativeTable:
        table_data = read_layout_from_file(table_file_path)
        return CatalogDeclarativeTable.from_dict(table_data)

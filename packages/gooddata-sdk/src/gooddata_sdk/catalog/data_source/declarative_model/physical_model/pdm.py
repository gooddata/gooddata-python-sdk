# (C) 2022 GoodData Corporation
from __future__ import annotations

from pathlib import Path

import attr
from gooddata_api_client.model.declarative_tables import DeclarativeTables

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.data_source.declarative_model.physical_model.table import CatalogDeclarativeTable
from gooddata_sdk.utils import create_directory

LAYOUT_PDM_DIR = "pdm"


def get_pdm_folder(data_source_folder: Path) -> Path:
    return data_source_folder / LAYOUT_PDM_DIR


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeTables(Base):
    tables: list[CatalogDeclarativeTable] = attr.field(factory=list)

    @staticmethod
    def client_class() -> type[DeclarativeTables]:
        return DeclarativeTables

    def store_to_disk(self, data_source_folder: Path) -> None:
        pdm_folder = get_pdm_folder(data_source_folder)
        create_directory(pdm_folder)
        for table in self.tables:
            table.store_to_disk(pdm_folder)

    @classmethod
    def load_from_disk(cls, data_source_folder: Path) -> CatalogDeclarativeTables:
        pdm_folder = get_pdm_folder(data_source_folder)
        table_files = sorted([p for p in pdm_folder.glob("*.yaml")])
        tables = [CatalogDeclarativeTable.load_from_disk(table_file) for table_file in table_files]
        return cls(tables=tables)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogScanResultPdm(Base):
    pdm: CatalogDeclarativeTables = CatalogDeclarativeTables()
    # Just informative hints. Create appropriate classes later if needed.
    warnings: list[dict] = attr.field(factory=list)

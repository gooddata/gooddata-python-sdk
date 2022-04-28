# (C) 2022 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from typing import Any

from gooddata_metadata_client.model.declarative_tables import DeclarativeTables
from gooddata_sdk.catalog.data_source.declarative_model.physical_model.table import CatalogDeclarativeTable
from gooddata_sdk.utils import create_directory, read_layout_from_file

LAYOUT_PDM_DIR = "pdm"


def get_pdm_folder(data_source_folder: Path) -> Path:
    return data_source_folder / LAYOUT_PDM_DIR


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

    def store_to_disk(self, data_source_folder: Path) -> None:
        pdm_folder = get_pdm_folder(data_source_folder)
        create_directory(pdm_folder)
        for table in self.tables:
            table.store_to_disk(pdm_folder)

    @classmethod
    def from_dict(cls, data: dict[str, Any], camel_case: bool = True) -> CatalogDeclarativeTables:
        """
        :param data:    Data loaded for example from the file.
        :param camel_case:  True if the variable names in the input
                        data are serialized names as specified in the OpenAPI document.
                        False if the variables names in the input data are python
                        variable names in PEP-8 snake case.
        :return:    DeclarativeTables object.
        """
        declarative_data_sources = DeclarativeTables.from_dict(data, camel_case)
        return cls.from_api(declarative_data_sources)

    @staticmethod
    def load_from_disk(data_source_folder: Path) -> dict:
        pdm_folder = get_pdm_folder(data_source_folder)
        table_files = sorted([p for p in pdm_folder.glob("*.yaml")])
        tables = []
        for table_file in table_files:
            tables.append(read_layout_from_file(table_file))
        return {"tables": tables}

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogDeclarativeTables):
            return False
        return self.tables == other.tables


class CatalogScanResultPdm:
    def __init__(
        self,
        pdm: CatalogDeclarativeTables,
        # Just informative hints. Create appropriate classes later if needed.
        warnings: list[dict],
    ):
        self.pdm = pdm
        self.warnings = warnings

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogScanResultPdm:
        tables = CatalogDeclarativeTables.from_api(entity.get("pdm", {"tables": []}))
        warnings = entity.get("warnings", [])
        return cls(pdm=tables, warnings=warnings)

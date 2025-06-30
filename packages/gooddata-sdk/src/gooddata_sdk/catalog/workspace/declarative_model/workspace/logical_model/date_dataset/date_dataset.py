# (C) 2022 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from typing import Optional

import attr
from gooddata_api_client.model.declarative_date_dataset import DeclarativeDateDataset
from gooddata_api_client.model.granularities_formatting import GranularitiesFormatting

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.utils import read_layout_from_file, write_layout_to_file

LAYOUT_DATE_INSTANCES_DIR = "date_instances"


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeDateDataset(Base):
    id: str
    title: str
    granularities_formatting: CatalogGranularitiesFormatting
    granularities: list[str]
    description: Optional[str] = None
    tags: Optional[list[str]] = None

    @staticmethod
    def client_class() -> type[DeclarativeDateDataset]:
        return DeclarativeDateDataset

    def store_to_disk(self, date_instances_folder: Path) -> None:
        date_instance_file = date_instances_folder / f"{self.id}.yaml"
        write_layout_to_file(date_instance_file, self.to_api().to_dict(camel_case=True))

    @classmethod
    def load_from_disk(cls, date_instance_file: Path) -> CatalogDeclarativeDateDataset:
        date_instance_layout = read_layout_from_file(date_instance_file)
        return cls.from_dict(date_instance_layout, camel_case=True)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogGranularitiesFormatting(Base):
    title_base: str
    title_pattern: str

    @staticmethod
    def client_class() -> type[GranularitiesFormatting]:
        return GranularitiesFormatting

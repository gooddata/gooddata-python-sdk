# (C) 2023 GoodData Corporation
from pathlib import Path

import attr
from gooddata_api_client.model.declarative_dataset_extension import DeclarativeDatasetExtension

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.data_filter_references import (
    CatalogDeclarativeWorkspaceDataFilterReferences,
)
from gooddata_sdk.utils import read_layout_from_file, write_layout_to_file

LAYOUT_DATASET_EXTENSIONS_DIR = "dataset_extensions"


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeDatasetExtension(Base):
    id: str
    workspace_data_filter_references: list[CatalogDeclarativeWorkspaceDataFilterReferences]

    @staticmethod
    def client_class() -> type[DeclarativeDatasetExtension]:
        return DeclarativeDatasetExtension

    def store_to_disk(self, dataset_extension_folder: Path) -> None:
        dataset_extension_file = dataset_extension_folder / f"{self.id}.yaml"
        write_layout_to_file(dataset_extension_file, self.to_api().to_dict(camel_case=True))

    @classmethod
    def load_from_disk(cls, dataset_extension_file: Path) -> "CatalogDeclarativeDatasetExtension":
        dataset_extension_layout = read_layout_from_file(dataset_extension_file)
        return cls.from_dict(dataset_extension_layout, camel_case=True)

# (C) 2022 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from typing import Any

from gooddata_metadata_client.model.declarative_ldm import DeclarativeLdm
from gooddata_metadata_client.model.declarative_model import DeclarativeModel
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.dataset.dataset import (
    LAYOUT_DATASETS_DIR,
    CatalogDeclarativeDataset,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.date_dataset.date_dataset import (
    LAYOUT_DATE_INSTANCES_DIR,
    CatalogDeclarativeDateDataset,
)
from gooddata_sdk.utils import create_directory, get_sorted_yaml_files

LAYOUT_LDM_DIR = "ldm"


class CatalogDeclarativeModel:
    def __init__(self, ldm: CatalogDeclarativeLdm = None):
        self.ldm = ldm

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDeclarativeModel:
        ldm = CatalogDeclarativeLdm.from_api(entity["ldm"]) if entity.get("ldm") else None
        return cls(ldm)

    def to_api(self) -> DeclarativeModel:
        kwargs: dict[str, Any] = dict()
        if self.ldm:
            kwargs["ldm"] = self.ldm.to_api()
        return DeclarativeModel(**kwargs)

    @classmethod
    def from_dict(cls, data: dict[str, Any], camel_case: bool = True) -> CatalogDeclarativeModel:
        """
        :param data:    Data loaded for example from the file.
        :param camel_case:  True if the variable names in the input
                        data are serialized names as specified in the OpenAPI document.
                        False if the variables names in the input data are python
                        variable names in PEP-8 snake case.
        :return:    CatalogDeclarativeModel object.
        """
        declarative_model = DeclarativeModel.from_dict(data, camel_case)
        return cls.from_api(declarative_model)

    def store_to_disk(self, workspace_folder: Path) -> None:
        if self.ldm is not None:
            self.ldm.store_to_disk(workspace_folder)

    def modify_mapped_data_source(self, data_source_mapping: dict) -> None:
        if self.ldm is not None:
            for dataset in self.ldm.datasets:
                if dataset.data_source_table_id is not None:
                    data_source_id = dataset.data_source_table_id.data_source_id
                    if data_source_id in data_source_mapping:
                        dataset.data_source_table_id.data_source_id = data_source_mapping[data_source_id]

    @classmethod
    def load_from_disk(cls, workspace_folder: Path) -> CatalogDeclarativeModel:
        ldm = CatalogDeclarativeLdm.load_from_disk(workspace_folder)
        return cls(ldm=ldm)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogDeclarativeModel):
            return False
        return self.ldm == other.ldm


class CatalogDeclarativeLdm:
    def __init__(
        self,
        datasets: list[CatalogDeclarativeDataset] = None,
        date_instances: list[CatalogDeclarativeDateDataset] = None,
    ):
        self.datasets = datasets or []
        self.date_instances = date_instances or []

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDeclarativeLdm:
        datasets = [CatalogDeclarativeDataset.from_api(v) for v in entity["datasets"]] if entity.get("datasets") else []
        date_instances = (
            [CatalogDeclarativeDateDataset.from_api(v) for v in entity["date_instances"]]
            if entity.get("date_instances")
            else []
        )
        return cls(datasets, date_instances)

    def to_api(self) -> DeclarativeLdm:
        kwargs: dict[str, Any] = {
            "datasets": [v.to_api() for v in self.datasets],
            "date_instances": [v.to_api() for v in self.date_instances],
        }
        return DeclarativeLdm(**kwargs)

    @staticmethod
    def get_ldm_folder(workspace_folder: Path) -> Path:
        folder = workspace_folder / LAYOUT_LDM_DIR
        create_directory(folder)
        return folder

    @staticmethod
    def get_datasets_folder(ldm_folder: Path) -> Path:
        folder = ldm_folder / LAYOUT_DATASETS_DIR
        create_directory(folder)
        return folder

    @staticmethod
    def get_date_instances_folder(ldm_folder: Path) -> Path:
        folder = ldm_folder / LAYOUT_DATE_INSTANCES_DIR
        create_directory(folder)
        return folder

    def store_to_disk(self, workspace_folder: Path) -> None:
        ldm_folder = self.get_ldm_folder(workspace_folder)
        datasets_folder = self.get_datasets_folder(ldm_folder)
        date_instances_folder = self.get_date_instances_folder(ldm_folder)

        for dataset in self.datasets:
            dataset.store_to_disk(datasets_folder)
        for date_instance in self.date_instances:
            date_instance.store_to_disk(date_instances_folder)

    @classmethod
    def load_from_disk(cls, workspace_folder: Path) -> CatalogDeclarativeLdm:
        ldm_folder = cls.get_ldm_folder(workspace_folder)
        datasets_folder = cls.get_datasets_folder(ldm_folder)
        date_instances_folder = cls.get_date_instances_folder(ldm_folder)

        dataset_files = get_sorted_yaml_files(datasets_folder)
        date_instance_files = get_sorted_yaml_files(date_instances_folder)

        datasets = [CatalogDeclarativeDataset.load_from_disk(dataset_file) for dataset_file in dataset_files]
        date_instances = [
            CatalogDeclarativeDateDataset.load_from_disk(date_instance_file)
            for date_instance_file in date_instance_files
        ]
        return cls(datasets=datasets, date_instances=date_instances)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogDeclarativeLdm):
            return False
        return self.datasets == other.datasets and self.date_instances == other.date_instances

# (C) 2022 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from typing import Optional

import attr
from gooddata_api_client.model.declarative_ldm import DeclarativeLdm
from gooddata_api_client.model.declarative_model import DeclarativeModel

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.dataset.dataset import (
    LAYOUT_DATASETS_DIR,
    CatalogDeclarativeDataset,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.dataset_extensions.dataset_extension import (  # noqa: E501
    LAYOUT_DATASET_EXTENSIONS_DIR,
    CatalogDeclarativeDatasetExtension,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.date_dataset.date_dataset import (
    LAYOUT_DATE_INSTANCES_DIR,
    CatalogDeclarativeDateDataset,
)
from gooddata_sdk.utils import create_directory, get_sorted_yaml_files

LAYOUT_LDM_DIR = "ldm"


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeModel(Base):
    ldm: Optional[CatalogDeclarativeLdm] = None

    @staticmethod
    def client_class() -> type[DeclarativeModel]:
        return DeclarativeModel

    def store_to_disk(self, workspace_folder: Path) -> None:
        if self.ldm is not None:
            self.ldm.store_to_disk(workspace_folder)

    @classmethod
    def load_from_disk(cls, workspace_folder: Path) -> CatalogDeclarativeModel:
        ldm = CatalogDeclarativeLdm.load_from_disk(workspace_folder)
        return cls(ldm=ldm)

    def remove_wdf_refs(self) -> None:
        if self.ldm:
            self.ldm.remove_wdf_refs()

    def change_wdf_refs_id(self, mapping: dict[str, str]) -> None:
        if self.ldm:
            self.ldm.change_wdf_refs_id(mapping)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeLdm(Base):
    datasets: list[CatalogDeclarativeDataset] = attr.field(factory=list)
    date_instances: list[CatalogDeclarativeDateDataset] = attr.field(factory=list)
    dataset_extensions: Optional[list[CatalogDeclarativeDatasetExtension]] = None

    @staticmethod
    def client_class() -> type[DeclarativeLdm]:
        return DeclarativeLdm

    @staticmethod
    def get_ldm_folder(workspace_folder: Path) -> Path:
        folder = workspace_folder / LAYOUT_LDM_DIR
        return folder

    @staticmethod
    def create_ldm_folder(workspace_folder: Path) -> Path:
        folder = workspace_folder / LAYOUT_LDM_DIR
        create_directory(folder)
        return folder

    @staticmethod
    def get_datasets_folder(ldm_folder: Path) -> Path:
        folder = ldm_folder / LAYOUT_DATASETS_DIR
        return folder

    @staticmethod
    def create_datasets_folder(ldm_folder: Path) -> Path:
        folder = ldm_folder / LAYOUT_DATASETS_DIR
        create_directory(folder)
        return folder

    @staticmethod
    def get_date_instances_folder(ldm_folder: Path) -> Path:
        folder = ldm_folder / LAYOUT_DATE_INSTANCES_DIR
        return folder

    @staticmethod
    def create_date_instances_folder(ldm_folder: Path) -> Path:
        folder = ldm_folder / LAYOUT_DATE_INSTANCES_DIR
        create_directory(folder)
        return folder

    @staticmethod
    def get_dataset_extensions_folder(ldm_folder: Path) -> Path:
        folder = ldm_folder / LAYOUT_DATASET_EXTENSIONS_DIR
        return folder

    @staticmethod
    def create_dataset_extensions_folder(ldm_folder: Path) -> Path:
        folder = ldm_folder / LAYOUT_DATASET_EXTENSIONS_DIR
        create_directory(folder)
        return folder

    def store_to_disk(self, workspace_folder: Path) -> None:
        ldm_folder = self.create_ldm_folder(workspace_folder)
        datasets_folder = self.create_datasets_folder(ldm_folder)
        date_instances_folder = self.create_date_instances_folder(ldm_folder)

        for dataset in self.datasets:
            dataset.store_to_disk(datasets_folder)
        for date_instance in self.date_instances:
            date_instance.store_to_disk(date_instances_folder)
        # Note: should be defaulted to an empty list in the future
        if self.dataset_extensions:
            dataset_extensions_folder = self.create_dataset_extensions_folder(ldm_folder)
            for dataset_extension in self.dataset_extensions:
                dataset_extension.store_to_disk(dataset_extensions_folder)

    @classmethod
    def load_from_disk(cls, workspace_folder: Path) -> CatalogDeclarativeLdm:
        ldm_folder = cls.get_ldm_folder(workspace_folder)
        datasets_folder = cls.get_datasets_folder(ldm_folder)
        date_instances_folder = cls.get_date_instances_folder(ldm_folder)
        dataset_extensions_folder = cls.get_dataset_extensions_folder(ldm_folder)

        dataset_files = get_sorted_yaml_files(datasets_folder)
        date_instance_files = get_sorted_yaml_files(date_instances_folder)
        dataset_extensions_files = get_sorted_yaml_files(dataset_extensions_folder)

        datasets = [CatalogDeclarativeDataset.load_from_disk(dataset_file) for dataset_file in dataset_files]
        date_instances = [
            CatalogDeclarativeDateDataset.load_from_disk(date_instance_file)
            for date_instance_file in date_instance_files
        ]
        dataset_extensions = (
            [
                CatalogDeclarativeDatasetExtension.load_from_disk(dataset_extensions_file)
                for dataset_extensions_file in dataset_extensions_files
            ]
            if dataset_extensions_folder.exists()
            else None
        )
        return cls(datasets=datasets, date_instances=date_instances, dataset_extensions=dataset_extensions)

    def modify_mapped_data_source(self, data_source_mapping: Optional[dict]) -> CatalogDeclarativeLdm:
        """LDM contains data source ID - is mapped to this data source.
        You may decide to migrate to different data source containing the same physical data model
        (e.g. change the DB engine, but keep the model).
        This function helps you to replace any set of data source IDs with new set of IDs
        (ready for multiple DS per workspace).

        Example:
        ```
        data_source_mapping = {"postgresql": "snowflake"}
        ldm = sdk.catalog_workspace_content.get_declarative_ldm(workspace_id)
        ldm.modify_mapped_data_source(data_source_mapping)
        # When migrating to Snowflake, we need to change the case of table/column names as well
        ldm.change_tables_columns_case(upper_case=True)
        sdk.catalog_workspace_content.put_declarative_ldm(workspace_id, ldm)

        # Chaining approach is also possible:
        ```
        sdk.catalog_workspace_content.put_declarative_ldm(
            workspace_id,
            sdk.catalog_workspace_content.get_declarative_ldm(workspace_id)\\
                .modify_mapped_data_source(data_source_mapping)\\
                .change_tables_columns_case(upper_case=True)
        )

        Args:
            data_source_mapping (dict):
                Key value pairs representing which DS(key) should be replaced by which DS(value).
                If mapping is empty, noop
                  - helps to chaining approach,
                    devs do not have to implement IFs if one of inputs in the chaining is optional.

        Returns:
            self
        """
        if self.datasets is not None and data_source_mapping:
            for dataset in self.datasets:
                if dataset.data_source_table_id is not None:
                    data_source_id = dataset.data_source_table_id.data_source_id
                    if data_source_id in data_source_mapping:
                        dataset.data_source_table_id.data_source_id = data_source_mapping[data_source_id]
                if dataset.sql is not None:
                    data_source_id = dataset.sql.data_source_id
                    if data_source_id in data_source_mapping:
                        dataset.sql.data_source_id = data_source_mapping[data_source_id]
        return self

    @staticmethod
    def _change_case(object_name: str, upper_case: bool) -> str:
        if upper_case:
            return object_name.upper()
        else:
            return object_name.lower()

    def change_tables_columns_case(self, upper_case: Optional[bool] = None) -> CatalogDeclarativeLdm:
        """Change case (to lower/upper-case) of all physical objects mapped in the LDM.
        Namely mapped table names and column names.
        Default is to change everything to upper-case.
        This is handy if you migrate e.g. from PostgreSQL to Snowflake,
        which is the only DB having upper-case as default.
        Instead of enclosing all (lower-cased) object names in all DDLs during the migration,
        you can use this function to change the case in GoodData LDM.
        If you specify upper-case=False, the function changes the case to lower-case
        (e.g. migration from Snowflake back to PostgreSQL).

        Examples can be found in the DOC of modify_mapped_data_source() method.

        Args:
            upper_case (bool):
                If True, all tables/columns names are changes to upper-case, otherwise to lower-case.
                If None, noop.
                  - helps to chaining approach,
                    devs do not have to implement IFs if one of inputs in the chaining is optional.

        Returns:
            self
        """
        if self.datasets is not None and upper_case is not None:
            for dataset in self.datasets:
                if dataset.data_source_table_id and dataset.data_source_table_id.id:
                    dataset.data_source_table_id.id = self._change_case(dataset.data_source_table_id.id, upper_case)
                if dataset.attributes:
                    for attribute in dataset.attributes:
                        if attribute.source_column:
                            attribute.source_column = self._change_case(attribute.source_column, upper_case)
                        if attribute.sort_column:
                            attribute.sort_column = self._change_case(attribute.sort_column, upper_case)
                        for label in attribute.labels:
                            if label.source_column:
                                label.source_column = self._change_case(label.source_column, upper_case)
                if dataset.facts:
                    for fact in dataset.facts:
                        if fact.source_column:
                            fact.source_column = self._change_case(fact.source_column, upper_case)
                for reference in dataset.references:
                    if reference.source_columns is not None:
                        new_columns = [
                            self._change_case(reference_column, upper_case)
                            for reference_column in reference.source_columns
                        ]
                        reference.source_columns = new_columns
                    elif reference.sources is not None:
                        for reference_source in reference.sources:
                            reference_source.column = self._change_case(reference_source.column, upper_case)
        return self

    def remove_wdf_refs(self) -> None:
        for dataset in self.datasets:
            dataset.workspace_data_filter_references = None

    def change_wdf_refs_id(self, mapping: dict[str, str]) -> None:
        for dataset in self.datasets:
            if dataset.workspace_data_filter_references:
                for wdf_ref in dataset.workspace_data_filter_references:
                    wdf_ref.filter_id.id = mapping[wdf_ref.filter_id.id]

        if self.dataset_extensions:
            for dataset_extension in self.dataset_extensions:
                if dataset_extension.workspace_data_filter_references:
                    for wdf_ref in dataset_extension.workspace_data_filter_references:
                        wdf_ref.filter_id.id = mapping[wdf_ref.filter_id.id]

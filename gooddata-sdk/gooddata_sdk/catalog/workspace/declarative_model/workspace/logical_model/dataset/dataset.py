# (C) 2022 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from typing import Optional

import attr
from gooddata_api_client.model.data_source_table_identifier import DataSourceTableIdentifier
from gooddata_api_client.model.declarative_attribute import DeclarativeAttribute
from gooddata_api_client.model.declarative_dataset import DeclarativeDataset
from gooddata_api_client.model.declarative_dataset_sql import DeclarativeDatasetSql
from gooddata_api_client.model.declarative_fact import DeclarativeFact
from gooddata_api_client.model.declarative_label import DeclarativeLabel
from gooddata_api_client.model.declarative_reference import DeclarativeReference
from gooddata_api_client.model.declarative_reference_source import DeclarativeReferenceSource
from gooddata_api_client.model.declarative_workspace_data_filter_column import DeclarativeWorkspaceDataFilterColumn

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.identifier import CatalogGrainIdentifier, CatalogLabelIdentifier, CatalogReferenceIdentifier
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.data_filter_references import (
    CatalogDeclarativeWorkspaceDataFilterReferences,
)
from gooddata_sdk.utils import read_layout_from_file, write_layout_to_file

LAYOUT_DATASETS_DIR = "datasets"


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeDataset(Base):
    id: str
    title: str
    grain: list[CatalogGrainIdentifier]
    references: list[CatalogDeclarativeReference]
    description: Optional[str] = None
    attributes: Optional[list[CatalogDeclarativeAttribute]] = None
    facts: Optional[list[CatalogDeclarativeFact]] = None
    data_source_table_id: Optional[CatalogDataSourceTableIdentifier] = None
    sql: Optional[CatalogDeclarativeDatasetSql] = None
    tags: Optional[list[str]] = None
    workspace_data_filter_columns: Optional[list[CatalogDeclarativeWorkspaceDataFilterColumn]] = None
    workspace_data_filter_references: Optional[list[CatalogDeclarativeWorkspaceDataFilterReferences]] = None

    @staticmethod
    def client_class() -> type[DeclarativeDataset]:
        return DeclarativeDataset

    def store_to_disk(self, datasets_folder: Path) -> None:
        dataset_file = datasets_folder / f"{self.id}.yaml"
        write_layout_to_file(dataset_file, self.to_api().to_dict(camel_case=True))

    @classmethod
    def load_from_disk(cls, dataset_file: Path) -> CatalogDeclarativeDataset:
        dataset_layout = read_layout_from_file(dataset_file)
        return cls.from_dict(dataset_layout, camel_case=True)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeAttribute(Base):
    id: str
    title: str
    source_column: str
    labels: list[CatalogDeclarativeLabel]
    source_column_data_type: Optional[str] = None
    default_view: Optional[CatalogLabelIdentifier] = None
    sort_column: Optional[str] = None
    sort_direction: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None

    @staticmethod
    def client_class() -> type[DeclarativeAttribute]:
        return DeclarativeAttribute


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeFact(Base):
    id: str
    title: str
    source_column: str
    source_column_data_type: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None

    @staticmethod
    def client_class() -> type[DeclarativeFact]:
        return DeclarativeFact


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDataSourceTableIdentifier(Base):
    id: str
    data_source_id: str
    path: Optional[list[str]] = None

    @staticmethod
    def client_class() -> type[DataSourceTableIdentifier]:
        return DataSourceTableIdentifier


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeDatasetSql(Base):
    statement: str
    data_source_id: str

    @staticmethod
    def client_class() -> type[DeclarativeDatasetSql]:
        return DeclarativeDatasetSql


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeLabel(Base):
    id: str
    title: str
    source_column: str
    source_column_data_type: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None
    value_type: Optional[str] = None

    @staticmethod
    def client_class() -> type[DeclarativeLabel]:
        return DeclarativeLabel


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeReference(Base):
    identifier: CatalogReferenceIdentifier
    multivalue: bool
    source_columns: Optional[list[str]] = None
    source_column_data_types: Optional[list[str]] = None
    sources: Optional[list[CatalogDeclarativeReferenceSource]] = None

    @staticmethod
    def client_class() -> type[DeclarativeReference]:
        return DeclarativeReference


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeWorkspaceDataFilterColumn(Base):
    name: str
    data_type: str

    @staticmethod
    def client_class() -> type[DeclarativeWorkspaceDataFilterColumn]:
        return DeclarativeWorkspaceDataFilterColumn


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeReferenceSource(Base):
    column: str
    target: CatalogGrainIdentifier
    data_type: Optional[str] = None

    @staticmethod
    def client_class() -> type[DeclarativeReferenceSource]:
        return DeclarativeReferenceSource

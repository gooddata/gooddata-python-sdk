# (C) 2022 GoodData Corporation
from __future__ import annotations

from pathlib import Path

import attr
import attrs
from attrs import define
from gooddata_api_client.model.data_source_table_identifier import DataSourceTableIdentifier
from gooddata_api_client.model.declarative_aggregated_fact import DeclarativeAggregatedFact
from gooddata_api_client.model.declarative_attribute import DeclarativeAttribute
from gooddata_api_client.model.declarative_dataset import DeclarativeDataset
from gooddata_api_client.model.declarative_dataset_sql import DeclarativeDatasetSql
from gooddata_api_client.model.declarative_fact import DeclarativeFact
from gooddata_api_client.model.declarative_label import DeclarativeLabel
from gooddata_api_client.model.declarative_label_translation import DeclarativeLabelTranslation
from gooddata_api_client.model.declarative_reference import DeclarativeReference
from gooddata_api_client.model.declarative_reference_source import DeclarativeReferenceSource
from gooddata_api_client.model.declarative_source_fact_reference import DeclarativeSourceFactReference
from gooddata_api_client.model.declarative_workspace_data_filter_column import DeclarativeWorkspaceDataFilterColumn
from gooddata_api_client.model.geo_area_config import GeoAreaConfig
from gooddata_api_client.model.geo_collection_identifier import GeoCollectionIdentifier

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.identifier import (
    CatalogFactIdentifier,
    CatalogGrainIdentifier,
    CatalogLabelIdentifier,
    CatalogReferenceIdentifier,
)
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
    description: str | None = None
    attributes: list[CatalogDeclarativeAttribute] | None = None
    facts: list[CatalogDeclarativeFact] | None = None
    aggregated_facts: list[CatalogDeclarativeAggregatedFact] | None = attrs.field(factory=list)
    precedence: int | None = None
    data_source_table_id: CatalogDataSourceTableIdentifier | None = None
    sql: CatalogDeclarativeDatasetSql | None = None
    tags: list[str] | None = None
    workspace_data_filter_columns: list[CatalogDeclarativeWorkspaceDataFilterColumn] | None = None
    workspace_data_filter_references: list[CatalogDeclarativeWorkspaceDataFilterReferences] | None = None

    @staticmethod
    def client_class() -> type[DeclarativeDataset]:
        return DeclarativeDataset

    def store_to_disk(self, datasets_folder: Path, sort: bool = False) -> None:
        dataset_file = datasets_folder / f"{self.id}.yaml"
        write_layout_to_file(dataset_file, self.to_api().to_dict(camel_case=True), sort=sort)

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
    source_column_data_type: str | None = None
    default_view: CatalogLabelIdentifier | None = None
    sort_column: str | None = None
    sort_direction: str | None = None
    description: str | None = None
    tags: list[str] | None = None
    is_hidden: bool | None = None
    locale: str | None = None
    is_nullable: bool | None = None
    null_value: str | None = None

    @staticmethod
    def client_class() -> type[DeclarativeAttribute]:
        return DeclarativeAttribute


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeFact(Base):
    id: str
    title: str
    source_column: str
    source_column_data_type: str | None = None
    description: str | None = None
    tags: list[str] | None = None
    is_hidden: bool | None = None
    is_nullable: bool | None = None
    null_value: str | None = None

    @staticmethod
    def client_class() -> type[DeclarativeFact]:
        return DeclarativeFact


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeSourceFactReference(Base):
    operation: str
    reference: CatalogFactIdentifier

    @staticmethod
    def client_class() -> type[DeclarativeSourceFactReference]:
        return DeclarativeSourceFactReference


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeAggregatedFact(Base):
    id: str
    source_column: str
    source_fact_reference: CatalogDeclarativeSourceFactReference | None = None
    source_column_data_type: str | None = None
    description: str | None = None
    tags: list[str] | None = None
    is_nullable: bool | None = None
    null_value: str | None = None

    @staticmethod
    def client_class() -> type[DeclarativeAggregatedFact]:
        return DeclarativeAggregatedFact


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDataSourceTableIdentifier(Base):
    id: str
    data_source_id: str
    path: list[str] | None = None

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
class CatalogDeclarativeLabelTranslation(Base):
    locale: str
    source_column: str

    @staticmethod
    def client_class() -> type[DeclarativeLabelTranslation]:
        return DeclarativeLabelTranslation


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeLabel(Base):
    id: str
    title: str
    source_column: str
    source_column_data_type: str | None = None
    description: str | None = None
    tags: list[str] | None = None
    value_type: str | None = None
    is_hidden: bool | None = None
    locale: str | None = None
    translations: list[CatalogDeclarativeLabelTranslation] | None = None
    geo_area_config: CatalogGeoAreaConfig | None = None
    is_nullable: bool | None = None
    null_value: str | None = None

    @staticmethod
    def client_class() -> type[DeclarativeLabel]:
        return DeclarativeLabel


@define(auto_attribs=True, kw_only=True)
class CatalogGeoAreaConfig(Base):
    collection: CatalogGeoCollectionIdentifier

    @staticmethod
    def client_class() -> type[GeoAreaConfig]:
        return GeoAreaConfig


@define(auto_attribs=True, kw_only=True)
class CatalogGeoCollectionIdentifier(Base):
    id: str
    kind: str | None = None

    @staticmethod
    def client_class() -> type[GeoCollectionIdentifier]:
        return GeoCollectionIdentifier


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeReference(Base):
    identifier: CatalogReferenceIdentifier
    multivalue: bool
    source_columns: list[str] | None = None
    source_column_data_types: list[str] | None = None
    sources: list[CatalogDeclarativeReferenceSource] | None = None
    is_nullable: bool | None = None
    null_value: str | None = None

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
    data_type: str | None = None

    @staticmethod
    def client_class() -> type[DeclarativeReferenceSource]:
        return DeclarativeReferenceSource

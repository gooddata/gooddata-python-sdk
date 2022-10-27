# (C) 2022 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from typing import Any, List, Optional, Type

import attr

from gooddata_api_client.model.declarative_data_source import DeclarativeDataSource
from gooddata_api_client.model.declarative_data_sources import DeclarativeDataSources
from gooddata_api_client.model.test_definition_request import TestDefinitionRequest
from gooddata_sdk.catalog.base import Base, value_in_allowed
from gooddata_sdk.catalog.data_source.declarative_model.physical_model.pdm import CatalogDeclarativeTables
from gooddata_sdk.catalog.entity import TokenCredentialsFromFile
from gooddata_sdk.catalog.parameter import CatalogParameter
from gooddata_sdk.catalog.permission.declarative_model.permission import CatalogDeclarativeDataSourcePermission
from gooddata_sdk.utils import create_directory, read_layout_from_file, write_layout_to_file

BIGQUERY_TYPE = "BIGQUERY"
LAYOUT_DATA_SOURCES_DIR = "data_sources"


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeDataSources(Base):
    data_sources: List[CatalogDeclarativeDataSource]

    def to_api(self, credentials: Optional[dict[str, Any]] = None) -> DeclarativeDataSources:
        data_sources = []
        client_class = self.client_class()
        credentials = credentials if credentials is not None else dict()
        for data_source in self.data_sources:
            if data_source.id in credentials:
                if data_source.type == BIGQUERY_TYPE:
                    token = TokenCredentialsFromFile.token_from_file(credentials[data_source.id])
                    data_sources.append(data_source.to_api(token=token))
                else:
                    data_sources.append(data_source.to_api(password=credentials[data_source.id]))
            else:
                data_sources.append(data_source.to_api())
        return client_class(data_sources=data_sources)

    @staticmethod
    def client_class() -> Type[DeclarativeDataSources]:
        return DeclarativeDataSources

    @staticmethod
    def data_sources_folder(layout_organization_folder: Path) -> Path:
        return layout_organization_folder / LAYOUT_DATA_SOURCES_DIR

    def store_to_disk(self, layout_organization_folder: Path) -> None:
        data_sources_folder = self.data_sources_folder(layout_organization_folder)
        create_directory(data_sources_folder)
        for data_source in self.data_sources:
            data_source.store_to_disk(data_sources_folder)

    @classmethod
    def load_from_disk(cls, layout_organization_folder: Path) -> CatalogDeclarativeDataSources:
        data_sources_folder = cls.data_sources_folder(layout_organization_folder)
        data_source_ids = sorted([p.stem for p in data_sources_folder.iterdir() if p.is_dir()])
        data_sources = []
        for data_source_id in data_source_ids:
            data_sources.append(CatalogDeclarativeDataSource.load_from_disk(data_sources_folder, data_source_id))
        return cls(data_sources=data_sources)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeDataSource(Base):
    id: str
    name: str
    type: str = attr.field(validator=value_in_allowed)
    url: Optional[str] = None
    schema: str
    enable_caching: Optional[bool] = None
    pdm: CatalogDeclarativeTables = CatalogDeclarativeTables()
    cache_path: Optional[List[str]] = None
    username: Optional[str] = None
    parameters: Optional[List[CatalogParameter]] = None
    decoded_parameters: Optional[List[CatalogParameter]] = None
    permissions: List[CatalogDeclarativeDataSourcePermission] = attr.field(factory=list)

    def to_test_request(
        self,
        password: Optional[str] = None,
        token: Optional[str] = None,
    ) -> TestDefinitionRequest:
        kwargs: dict[str, Any] = {"schema": self.schema}
        if password is not None:
            kwargs["password"] = password
        if token is not None:
            kwargs["token"] = token
        if self.username is not None:
            kwargs["username"] = self.username
        return TestDefinitionRequest(type=self.type, url=self.url, **kwargs)

    @staticmethod
    def client_class() -> Type[DeclarativeDataSource]:
        return DeclarativeDataSource

    @staticmethod
    def data_source_folder(data_sources_folder: Path, data_source_id: str) -> Path:
        data_source_folder = data_sources_folder / data_source_id
        create_directory(data_source_folder)
        return data_source_folder

    def to_api(
        self, password: Optional[str] = None, token: Optional[str] = None, include_nested_structures: bool = True
    ) -> DeclarativeDataSource:
        dictionary = self._get_snake_dict()
        if not include_nested_structures:
            del dictionary["pdm"]
        if password is not None:
            dictionary["password"] = password
        if token is not None:
            dictionary["token"] = token
        return self.client_class().from_dict(dictionary)

    def store_to_disk(self, data_sources_folder: Path) -> None:
        data_source_folder = self.data_source_folder(data_sources_folder, self.id)
        file_path = data_source_folder / f"{self.id}.yaml"
        data_source_dict = self.to_api(include_nested_structures=False).to_dict(camel_case=True)

        write_layout_to_file(file_path, data_source_dict)

        if self.pdm is not None:
            self.pdm.store_to_disk(data_source_folder)

    @classmethod
    def load_from_disk(cls, data_sources_folder: Path, data_source_id: str) -> CatalogDeclarativeDataSource:
        data_source_folder = data_sources_folder / data_source_id
        data_source_file_path = data_source_folder / f"{data_source_id}.yaml"
        pdm = CatalogDeclarativeTables.load_from_disk(data_source_folder)
        data_source_dict = read_layout_from_file(data_source_file_path)
        data_source = CatalogDeclarativeDataSource.from_dict(data_source_dict)
        data_source.pdm = pdm
        return data_source

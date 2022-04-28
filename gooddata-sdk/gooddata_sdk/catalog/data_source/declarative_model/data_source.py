# (C) 2022 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from gooddata_metadata_client.model.declarative_data_source import DeclarativeDataSource
from gooddata_metadata_client.model.declarative_data_sources import DeclarativeDataSources
from gooddata_scan_client.model.test_definition_request import TestDefinitionRequest
from gooddata_sdk.catalog.data_source.declarative_model.physical_model.pdm import CatalogDeclarativeTables
from gooddata_sdk.catalog.entity import CatalogTypeEntity, TokenCredentialsFromFile
from gooddata_sdk.catalog.permissions.permission import CatalogDeclarativeDataSourcePermission
from gooddata_sdk.utils import create_directory, read_layout_from_file, write_layout_to_file

BIGQUERY_TYPE = "BIGQUERY"
LAYOUT_DATA_SOURCES_DIR = "data_sources"


class CatalogDeclarativeDataSources:
    def __init__(self, data_sources: list[CatalogDeclarativeDataSource]):
        self.data_sources = data_sources

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDeclarativeDataSources:
        data_sources = [CatalogDeclarativeDataSource.from_api(v) for v in entity["data_sources"]]
        return cls(data_sources)

    def to_api(self, credentials: dict[str, Any] = None) -> DeclarativeDataSources:
        data_sources = []
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
        return DeclarativeDataSources(data_sources=data_sources)

    @classmethod
    def from_dict(cls, data: dict[str, Any], camel_case: bool = True) -> CatalogDeclarativeDataSources:
        """
        :param data:    Data loaded for example from the file.
        :param camel_case:  True if the variable names in the input
                        data are serialized names as specified in the OpenAPI document.
                        False if the variables names in the input data are python
                        variable names in PEP-8 snake case.
        :return:    CatalogDeclarativeDataSources object.
        """
        declarative_data_sources = DeclarativeDataSources.from_dict(data, camel_case)
        return cls.from_api(declarative_data_sources)

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
        return cls.from_dict({"dataSources": data_sources})

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogDeclarativeDataSources):
            return False
        return self.data_sources == other.data_sources


class CatalogDeclarativeDataSource(CatalogTypeEntity):
    def __init__(
        self,
        id: str,
        type: str,
        name: str,
        url: str,
        schema: str,
        enable_caching: Optional[bool],
        pdm: Optional[CatalogDeclarativeTables],
        cache_path: Optional[list[str]] = None,
        username: Optional[str] = None,
        permissions: list[CatalogDeclarativeDataSourcePermission] = None,
    ):
        super(CatalogDeclarativeDataSource, self).__init__(id, type)
        self.schema = schema
        self.enable_caching = enable_caching
        self.cache_path = cache_path
        self.name = name
        self.url = url
        self.pdm = pdm
        self.username = username
        self.permissions = permissions if permissions is not None else []

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDeclarativeDataSource:
        permissions = [
            CatalogDeclarativeDataSourcePermission.from_api(permission) for permission in entity.get("permissions", [])
        ]
        pdm = CatalogDeclarativeTables.from_api(entity["pdm"]) if entity.get("pdm") else None
        return cls(
            id=entity["id"],
            name=entity["name"],
            url=entity["url"],
            type=entity["type"],
            enable_caching=entity.get("enable_caching"),
            schema=entity["schema"],
            pdm=pdm,
            cache_path=entity.get("cache_path"),
            username=entity.get("username"),
            permissions=permissions,
        )

    def to_api(
        self,
        password: Optional[str] = None,
        token: Optional[str] = None,
        include_nested_structures: bool = True,
    ) -> DeclarativeDataSource:
        kwargs: dict[str, Any] = {"permissions": [permission.to_api() for permission in self.permissions]}
        if self.enable_caching is not None:
            kwargs["enable_caching"] = self.enable_caching
        if self.cache_path is not None:
            kwargs["cache_path"] = self.cache_path
        if self.pdm is not None and include_nested_structures:
            kwargs["pdm"] = self.pdm.to_api()
        if self.username is not None:
            kwargs["username"] = self.username
        if password is not None:
            kwargs["password"] = password
        if token is not None:
            kwargs["token"] = token
        return DeclarativeDataSource(
            id=self.id,
            name=self.name,
            url=self.url,
            type=self.type,
            schema=self.schema,
            **kwargs,
        )

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
    def data_source_folder(data_sources_folder: Path, data_source_id: str) -> Path:
        data_source_folder = data_sources_folder / data_source_id
        create_directory(data_source_folder)
        return data_source_folder

    def store_to_disk(self, data_sources_folder: Path) -> None:
        data_source_folder = self.data_source_folder(data_sources_folder, self.id)
        file_path = data_source_folder / f"{self.id}.yaml"
        data_source_dict = self.to_api(include_nested_structures=False).to_dict(camel_case=True)

        write_layout_to_file(file_path, data_source_dict)

        if self.pdm is not None:
            self.pdm.store_to_disk(data_source_folder)

    @staticmethod
    def load_from_disk(data_sources_folder: Path, data_source_id: str) -> dict:
        data_source_folder = data_sources_folder / data_source_id
        data_source_file_path = data_source_folder / f"{data_source_id}.yaml"
        pdm = CatalogDeclarativeTables.load_from_disk(data_source_folder)
        data_source = read_layout_from_file(data_source_file_path)
        data_source["pdm"] = pdm
        return data_source

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogDeclarativeDataSource):
            return False
        return (
            self.id == other.id
            and self.name == other.name
            and self.url == other.url
            and self.type == other.type
            and self.enable_caching == other.enable_caching
            and self.schema == other.schema
            and self.cache_path == other.cache_path
            and self.pdm == other.pdm
        )

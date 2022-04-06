# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any, Optional

from gooddata_metadata_client.model.declarative_data_source import DeclarativeDataSource
from gooddata_metadata_client.model.declarative_data_sources import DeclarativeDataSources
from gooddata_scan_client.model.test_definition_request import TestDefinitionRequest
from gooddata_sdk.catalog.data_source.declarative_model.physical_model.pdm import CatalogDeclarativeTables
from gooddata_sdk.catalog.entity import CatalogTypeEntity, TokenCredentialsFromFile

BIGQUERY_TYPE = "BIGQUERY"


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
    ):
        super(CatalogDeclarativeDataSource, self).__init__(id, type)
        self.schema = schema
        self.enable_caching = enable_caching
        self.cache_path = cache_path
        self.name = name
        self.url = url
        self.pdm = pdm
        self.username = username

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDeclarativeDataSource:
        return cls(
            id=entity["id"],
            name=entity["name"],
            url=entity["url"],
            type=entity["type"],
            enable_caching=entity.get("enable_caching"),
            schema=entity["schema"],
            pdm=CatalogDeclarativeTables.from_api(entity["pdm"]) if entity.get("pdm") else None,
            cache_path=entity.get("cache_path"),
            username=entity.get("username"),
        )

    def to_api(
        self,
        password: Optional[str] = None,
        token: Optional[str] = None,
    ) -> DeclarativeDataSource:
        kwargs: dict[str, Any] = {}
        if self.enable_caching is not None:
            kwargs["enable_caching"] = self.enable_caching
        if self.cache_path is not None:
            kwargs["cache_path"] = self.cache_path
        if self.pdm is not None:
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

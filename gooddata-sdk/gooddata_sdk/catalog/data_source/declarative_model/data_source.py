# (C) 2022 GoodData Corporation
from __future__ import annotations

import builtins
from pathlib import Path
from typing import Any, Optional, Union
from warnings import warn

import attr
from gooddata_api_client.model.declarative_data_source import DeclarativeDataSource
from gooddata_api_client.model.declarative_data_sources import DeclarativeDataSources
from gooddata_api_client.model.test_definition_request import TestDefinitionRequest

from gooddata_sdk.catalog.base import Base, value_in_allowed
from gooddata_sdk.catalog.entity import ClientSecretCredentialsFromFile, TokenCredentialsFromFile
from gooddata_sdk.catalog.parameter import CatalogParameter
from gooddata_sdk.catalog.permission.declarative_model.permission import CatalogDeclarativeDataSourcePermission
from gooddata_sdk.utils import create_directory, get_ds_credentials, read_layout_from_file, write_layout_to_file

BIGQUERY_TYPE = "BIGQUERY"
DATABRICKS_TYPE = "DATABRICKS"
LAYOUT_DATA_SOURCES_DIR = "data_sources"


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeDataSources(Base):
    data_sources: list[CatalogDeclarativeDataSource]

    def _inject_base(self, credentials: dict[str, Any]) -> DeclarativeDataSources:
        data_sources = []
        client_class = self.client_class()
        for data_source in self.data_sources:
            if data_source.id in credentials:
                if data_source.type == BIGQUERY_TYPE:
                    token = TokenCredentialsFromFile.token_from_file(credentials[data_source.id])
                    data_sources.append(data_source.to_api(token=token))
                elif data_source.type == DATABRICKS_TYPE:
                    if data_source.client_id and data_source.client_id.strip():
                        client_secret = ClientSecretCredentialsFromFile.client_secret_from_file(
                            credentials[data_source.id]
                        )
                        data_sources.append(data_source.to_api(client_secret=client_secret))
                    else:
                        token = TokenCredentialsFromFile.token_from_file(
                            file_path=credentials[data_source.id], base64_encode=False
                        )
                        data_sources.append(data_source.to_api(token=token))
                else:
                    data_sources.append(data_source.to_api(password=credentials[data_source.id]))
            else:
                data_sources.append(data_source.to_api())
        return client_class(data_sources=data_sources)

    def _inject_credentials_legacy(self, credentials: dict[str, Any]) -> DeclarativeDataSources:
        return self._inject_base(credentials)

    def _inject_credentials_aac(self, config_file: Union[str, Path]) -> DeclarativeDataSources:
        ds_ids = {ds.id for ds in self.data_sources}
        credentials = get_ds_credentials(config_file)
        missing = set(credentials.keys()).difference(ds_ids)
        if len(missing) > 0:
            warn(
                f"The following data sources are missing credentials: {missing}.",
                UserWarning,
                stacklevel=2,
            )
        return self._inject_base(credentials)

    def to_api(
        self, credentials: Optional[dict[str, Any]] = None, config_file: Optional[Union[str, Path]] = None
    ) -> DeclarativeDataSources:
        client_class = self.client_class()
        if credentials is not None and config_file is not None:
            raise ValueError("Only one of credentials or config_file should be provided")
        if credentials is None and config_file is None:
            return client_class(data_sources=[data_source.to_api() for data_source in self.data_sources])
        if credentials is not None:
            return self._inject_credentials_legacy(credentials)
        if config_file is not None:
            return self._inject_credentials_aac(config_file)

    @staticmethod
    def client_class() -> type[DeclarativeDataSources]:
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
        data_sources = [
            CatalogDeclarativeDataSource.load_from_disk(data_sources_folder, data_source_id)
            for data_source_id in data_source_ids
        ]
        return cls(data_sources=data_sources)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeDataSource(Base):
    id: str
    name: str
    type: str = attr.field(validator=value_in_allowed)
    url: Optional[str] = None
    schema: str
    cache_strategy: Optional[str] = None
    username: Optional[str] = None
    parameters: Optional[list[CatalogParameter]] = None
    decoded_parameters: Optional[list[CatalogParameter]] = None
    permissions: list[CatalogDeclarativeDataSourcePermission] = attr.field(factory=list)
    client_id: Optional[str] = None

    def to_test_request(
        self,
        password: Optional[str] = None,
        token: Optional[str] = None,
        private_key: Optional[str] = None,
        private_key_passphrase: Optional[str] = None,
        client_secret: Optional[str] = None,
    ) -> TestDefinitionRequest:
        kwargs: dict[str, Any] = {"schema": self.schema}
        if password is not None:
            kwargs["password"] = password
        if token is not None:
            kwargs["token"] = token
        if self.username is not None:
            kwargs["username"] = self.username
        if private_key is not None:
            kwargs["private_key"] = private_key
        if private_key_passphrase is not None:
            kwargs["private_key_passphrase"] = private_key
        if self.client_id is not None:
            kwargs["client_id"] = self.client_id
        if client_secret is not None:
            kwargs["client_secret"] = client_secret
        if self.parameters is not None:
            kwargs["parameters"] = [param.to_data_source_parameter() for param in self.parameters]

        return TestDefinitionRequest(type=self.type, url=self.url, **kwargs)

    @staticmethod
    def client_class() -> builtins.type[DeclarativeDataSource]:
        return DeclarativeDataSource

    @staticmethod
    def data_source_folder(data_sources_folder: Path, data_source_id: str) -> Path:
        data_source_folder = data_sources_folder / data_source_id
        create_directory(data_source_folder)
        return data_source_folder

    def to_api(
        self,
        password: Optional[str] = None,
        token: Optional[str] = None,
        private_key: Optional[str] = None,
        private_key_passphrase: Optional[str] = None,
        client_secret: Optional[str] = None,
    ) -> DeclarativeDataSource:
        dictionary = self._get_snake_dict()
        if password is not None:
            dictionary["password"] = password
        if token is not None:
            dictionary["token"] = token
        if private_key is not None:
            dictionary["private_key"] = private_key
        if private_key_passphrase is not None:
            dictionary["private_key_passphrase"] = private_key_passphrase
        if client_secret is not None:
            dictionary["client_secret"] = client_secret
        return self.client_class().from_dict(dictionary)

    def store_to_disk(self, data_sources_folder: Path) -> None:
        data_source_folder = self.data_source_folder(data_sources_folder, self.id)
        file_path = data_source_folder / f"{self.id}.yaml"
        data_source_dict = self.to_api().to_dict(camel_case=True)

        write_layout_to_file(file_path, data_source_dict)

    @classmethod
    def load_from_disk(cls, data_sources_folder: Path, data_source_id: str) -> CatalogDeclarativeDataSource:
        data_source_folder = data_sources_folder / data_source_id
        data_source_file_path = data_source_folder / f"{data_source_id}.yaml"
        data_source_dict = read_layout_from_file(data_source_file_path)
        data_source = CatalogDeclarativeDataSource.from_dict(data_source_dict)
        return data_source

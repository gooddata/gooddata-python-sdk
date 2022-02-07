# (C) 2022 GoodData Corporation
from __future__ import annotations

import functools
from typing import List

import gooddata_metadata_client.apis as metadata_apis
from gooddata_metadata_client.exceptions import NotFoundException
from gooddata_sdk.catalog.data_source.model.content_objects.table import CatalogDataSourceTable
from gooddata_sdk.catalog.data_source.model.data_source import (
    CatalogDataSource,
    CatalogDataSourceToken,
    CatalogDataSourceUserPwd,
    encode_bigquery_token,
    make_bigquery_url,
    make_snowflake_url,
    make_standard_url,
)
from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.utils import load_all_entities


class CatalogDataSourceService:
    def __init__(self, api_client: GoodDataApiClient) -> None:
        self._client = api_client
        self._entities_api = metadata_apis.EntitiesApi(api_client.metadata_client)

    def list_data_sources(self) -> List[CatalogDataSource]:
        get_data_sources = functools.partial(
            self._entities_api.get_all_entities_data_sources,
            _check_return_type=False,
        )
        data_sources = load_all_entities(get_data_sources)
        return [CatalogDataSource.from_api(ds) for ds in data_sources.data]

    def list_data_source_tables(self, data_source: str) -> List[CatalogDataSourceTable]:
        get_data_source_tables = functools.partial(
            self._entities_api.get_all_entities_data_source_tables,
            data_source,
            _check_return_type=False,
        )
        data_source_tables = load_all_entities(get_data_source_tables)
        return [CatalogDataSourceTable(dst) for dst in data_source_tables.data]

    def create_or_update_data_source(
        self,
        data_source: CatalogDataSource,
    ) -> None:
        try:
            self._entities_api.get_entity_data_sources(data_source.id)
            self._entities_api.update_entity_data_sources(
                data_source.id,
                data_source.to_api(),
            )
        except NotFoundException:
            self._entities_api.create_entity_data_sources(data_source.to_api())

    def create_or_update_standard_data_source(
        self,
        data_source_base: CatalogDataSourceUserPwd,
        host: str,
        port: int,
        db_name: str,
        db_engine: str,
        data_source_type: str,
    ) -> None:
        self.create_or_update_data_source(
            CatalogDataSource(
                id=data_source_base.id,
                name=data_source_base.name,
                url=make_standard_url(db_engine, host, port, db_name, params=data_source_base.url_params),
                schema=data_source_base.schema,
                username=data_source_base.username,
                password=data_source_base.password,
                data_source_type=data_source_type,
            )
        )

    def create_or_update_postgres_data_source(
        self,
        data_source_base: CatalogDataSourceUserPwd,
        host: str,
        db_name: str,
        port: int = 5432,
    ) -> None:
        self.create_or_update_standard_data_source(
            data_source_base, host, port, db_name, db_engine="postgresql", data_source_type="POSTGRESQL"
        )

    def create_or_update_redshift_data_source(
        self,
        data_source_base: CatalogDataSourceUserPwd,
        host: str,
        db_name: str,
        port: int = 5439,
    ) -> None:
        self.create_or_update_standard_data_source(
            data_source_base, host, port, db_name, db_engine="redshift", data_source_type="REDSHIFT"
        )

    def create_or_update_vertica_data_source(
        self,
        data_source_base: CatalogDataSourceUserPwd,
        host: str,
        db_name: str,
        port: int = 5433,
    ) -> None:
        self.create_or_update_standard_data_source(
            data_source_base, host, port, db_name, db_engine="vertica", data_source_type="VERTICA"
        )

    def create_or_update_snowflake_data_source(
        self,
        data_source_base: CatalogDataSourceUserPwd,
        account: str,
        warehouse: str,
        db_name: str,
    ) -> None:
        self.create_or_update_data_source(
            CatalogDataSource(
                id=data_source_base.id,
                name=data_source_base.name,
                url=make_snowflake_url(account, warehouse, db_name, params=data_source_base.url_params),
                schema=data_source_base.schema,
                username=data_source_base.username,
                password=data_source_base.password,
                data_source_type="SNOWFLAKE",
            )
        )

    def create_or_update_bigquery_data_source(
        self,
        data_source_base: CatalogDataSourceToken,
        project_id: str,
    ) -> None:
        token = encode_bigquery_token(data_source_base.token_path)
        self.create_or_update_data_source(
            CatalogDataSource(
                id=data_source_base.id,
                name=data_source_base.name,
                url=make_bigquery_url(project_id, params=data_source_base.url_params),
                # Schema is used as DefaultDataset
                schema=data_source_base.schema,
                token=token,
                data_source_type="BIGQUERY",
            )
        )

    def delete_data_source(self, data_source_id: str) -> None:
        self._entities_api.delete_entity_data_sources(data_source_id)

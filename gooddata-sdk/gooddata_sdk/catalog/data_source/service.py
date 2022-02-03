# (C) 2022 GoodData Corporation
from __future__ import annotations

import functools
from typing import List

import gooddata_metadata_client.apis as metadata_apis
from gooddata_sdk.catalog.data_source.model.content_objects.table import CatalogDataSourceTable
from gooddata_sdk.catalog.data_source.model.data_source import CatalogDataSource
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
        return [CatalogDataSource(ds) for ds in data_sources.data]

    def list_data_source_tables(self, data_source: str) -> List[CatalogDataSourceTable]:
        get_data_source_tables = functools.partial(
            self._entities_api.get_all_entities_data_source_tables,
            data_source,
            _check_return_type=False,
        )
        data_source_tables = load_all_entities(get_data_source_tables)
        return [CatalogDataSourceTable(dst) for dst in data_source_tables.data]

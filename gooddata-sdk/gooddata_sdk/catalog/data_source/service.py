# (C) 2022 GoodData Corporation
from __future__ import annotations

import functools
from typing import List

import gooddata_metadata_client.apis as metadata_apis
from gooddata_metadata_client.exceptions import NotFoundException
from gooddata_sdk.catalog.data_source.action_requests.ldm_request import CatalogGenerateLdmRequest
from gooddata_sdk.catalog.data_source.model.content_objects.table import CatalogDataSourceTable
from gooddata_sdk.catalog.data_source.model.data_source import CatalogDataSource
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.ldm import CatalogDeclarativeModel
from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.utils import load_all_entities


class CatalogDataSourceService:
    def __init__(self, api_client: GoodDataApiClient) -> None:
        self._client = api_client
        self._entities_api = metadata_apis.EntitiesApi(api_client.metadata_client)
        self._actions_api = metadata_apis.ActionsApi(api_client.metadata_client)

    def list_data_sources(self) -> List[CatalogDataSource]:
        get_data_sources = functools.partial(
            self._entities_api.get_all_entities_data_sources,
            _check_return_type=False,
        )
        data_sources = load_all_entities(get_data_sources)
        return [CatalogDataSource.from_api(ds) for ds in data_sources.data]

    def get_data_source(self, data_source_id: str) -> CatalogDataSource:
        return CatalogDataSource.from_api(self._entities_api.get_entity_data_sources(data_source_id).data)

    def list_data_source_tables(self, data_source_id: str) -> List[CatalogDataSourceTable]:
        get_data_source_tables = functools.partial(
            self._entities_api.get_all_entities_data_source_tables,
            data_source_id,
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

    def delete_data_source(self, data_source_id: str) -> None:
        self._entities_api.delete_entity_data_sources(data_source_id)

    def patch_data_source_attributes(self, data_source_id: str, attributes: dict) -> None:
        # TODO - workaround solution getting data source type from backend
        #      - once backend accepts empty value in this field (enum), remove this code
        current_ds = self.get_data_source(data_source_id)
        attributes["type"] = attributes.get("type", current_ds.data_source_type)

        self._entities_api.patch_entity_data_sources(
            data_source_id, CatalogDataSource.to_api_patch(data_source_id, attributes)
        )

    def generate_logical_model(
        self, data_source_id: str, generate_ldm_request: CatalogGenerateLdmRequest
    ) -> CatalogDeclarativeModel:
        return CatalogDeclarativeModel.from_api(
            self._actions_api.generate_logical_model(data_source_id, generate_ldm_request.to_api())
        )

    def register_upload_notification(self, data_source_id: str) -> None:
        self._actions_api.register_upload_notification(data_source_id)

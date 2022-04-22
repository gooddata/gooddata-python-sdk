# (C) 2022 GoodData Corporation
from __future__ import annotations

import functools
import os.path
from pathlib import Path
from typing import Any, List, Optional

import gooddata_metadata_client.apis as metadata_apis
import gooddata_scan_client.apis as scan_client_apis
from gooddata_metadata_client.exceptions import NotFoundException
from gooddata_sdk.catalog.catalog_service_base import CatalogServiceBase
from gooddata_sdk.catalog.data_source.action_requests.ldm_request import CatalogGenerateLdmRequest
from gooddata_sdk.catalog.data_source.declarative_model.data_source import BIGQUERY_TYPE, CatalogDeclarativeDataSources
from gooddata_sdk.catalog.data_source.entity_model.content_objects.table import CatalogDataSourceTable
from gooddata_sdk.catalog.data_source.entity_model.data_source import CatalogDataSource
from gooddata_sdk.catalog.entity import TokenCredentialsFromFile
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.ldm import CatalogDeclarativeModel
from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.utils import load_all_entities, read_layout_from_file


class CatalogDataSourceService(CatalogServiceBase):
    def __init__(self, api_client: GoodDataApiClient) -> None:
        super(CatalogDataSourceService, self).__init__(api_client)
        self._actions_api = metadata_apis.ActionsApi(api_client.metadata_client)
        self._scan_api = scan_client_apis.ActionsApi(api_client.scan_client)

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

    def get_declarative_data_sources(self) -> CatalogDeclarativeDataSources:
        return CatalogDeclarativeDataSources.from_api(self._layout_api.get_data_sources_layout())

    def put_declarative_data_sources(
        self,
        declarative_data_sources: CatalogDeclarativeDataSources,
        credentials_path: Optional[Path] = None,
        test_data_sources: bool = False,
    ) -> None:
        if test_data_sources:
            self.test_data_sources_connection(declarative_data_sources, credentials_path)
        credentials = self._credentials_from_file(credentials_path) if credentials_path is not None else dict()
        self._layout_api.put_data_sources_layout(declarative_data_sources.to_api(credentials))

    @staticmethod
    def _credentials_from_file(credentials_path: Path) -> dict[str, Any]:
        data = read_layout_from_file(credentials_path)
        if data.get("data_sources") is None:
            raise ValueError("The file has a wrong structure. There should be a root key 'data_sources'.")
        if len(data["data_sources"]) == 0:
            raise ValueError("There are no pairs of data source id and token.")
        credentials = data["data_sources"]
        return credentials

    def test_data_sources_connection(
        self, declarative_data_sources: CatalogDeclarativeDataSources, credentials_path: Optional[Path] = None
    ) -> None:
        credentials = self._credentials_from_file(credentials_path) if credentials_path is not None else dict()
        errors: dict[str, str] = dict()
        for declarative_data_source in declarative_data_sources.data_sources:
            if credentials.get(declarative_data_source.id) is not None:
                if declarative_data_source.type == BIGQUERY_TYPE:
                    token = TokenCredentialsFromFile.token_from_file(credentials[declarative_data_source.id])
                    response = self._scan_api.test_data_source_definition(
                        declarative_data_source.to_test_request(token=token)
                    )
                else:
                    response = self._scan_api.test_data_source_definition(
                        declarative_data_source.to_test_request(password=credentials[declarative_data_source.id])
                    )
            else:
                response = self._scan_api.test_data_source_definition(declarative_data_source.to_test_request())
            if not response.successful:
                errors[declarative_data_source.id] = response.error
        if len(errors) != 0:
            message = []
            for k, v in errors.items():
                message.append(f"Test connection for data source id {k} ended with the following error {v}.")
            raise ValueError("\n".join(message))

    def store_declarative_data_sources(self, layout_root_path: Path = Path(os.path.curdir)) -> None:
        self.get_declarative_data_sources().store_to_disk(self.layout_organization_folder(layout_root_path))

    def load_declarative_data_sources(
        self, layout_root_path: Path = Path(os.path.curdir)
    ) -> CatalogDeclarativeDataSources:
        return CatalogDeclarativeDataSources.load_from_disk(self.layout_organization_folder(layout_root_path))

    def load_and_put_declarative_data_sources(
        self,
        layout_root_path: Path = Path(os.path.curdir),
        credentials_path: Optional[Path] = None,
        test_data_sources: bool = False,
    ) -> None:
        data_sources = self.load_declarative_data_sources(layout_root_path)
        self.put_declarative_data_sources(data_sources, credentials_path, test_data_sources)

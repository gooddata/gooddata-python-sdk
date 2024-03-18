# (C) 2022 GoodData Corporation
from __future__ import annotations

from pathlib import Path

from gooddata_api_client import apis
from gooddata_api_client.model.json_api_organization_out_document import JsonApiOrganizationOutDocument

from gooddata_sdk.catalog.organization.entity_model.organization import CatalogOrganization
from gooddata_sdk.client import GoodDataApiClient

LAYOUT_ROOT_FOLDER = "gooddata_layouts"


class CatalogServiceBase:
    def __init__(self, api_client: GoodDataApiClient) -> None:
        self._client = api_client
        self._entities_api: apis.EntitiesApi = api_client.entities_api
        self._layout_api: apis.LayoutApi = api_client.layout_api
        self._actions_api: apis.ActionsApi = api_client.actions_api
        self._user_management_api: apis.UserManagementApi = api_client.user_management_api

    def get_organization(self) -> CatalogOrganization:
        # The generated client does work properly with redirecting APIs
        # This switch makes it work
        self._entities_api.get_organization_endpoint.settings["response_type"] = (JsonApiOrganizationOutDocument,)
        result = self._entities_api.get_organization().data
        return CatalogOrganization.from_api(result)

    @property
    def organization_id(self) -> str:
        return self.get_organization().id

    def layout_organization_folder(self, layout_root_path: Path) -> Path:
        return layout_root_path / LAYOUT_ROOT_FOLDER / self.organization_id

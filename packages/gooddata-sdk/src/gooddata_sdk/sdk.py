# (C) 2021 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from typing import Optional

from gooddata_sdk.catalog.data_source.service import CatalogDataSourceService
from gooddata_sdk.catalog.export.service import ExportService
from gooddata_sdk.catalog.organization.service import CatalogOrganizationService
from gooddata_sdk.catalog.permission.service import CatalogPermissionService
from gooddata_sdk.catalog.user.service import CatalogUserService
from gooddata_sdk.catalog.workspace.content_service import CatalogWorkspaceContentService
from gooddata_sdk.catalog.workspace.service import CatalogWorkspaceService
from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.compute.service import ComputeService
from gooddata_sdk.support import SupportService
from gooddata_sdk.table import TableService
from gooddata_sdk.utils import PROFILES_FILE_PATH, profile_content
from gooddata_sdk.visualization import VisualizationService


class GoodDataSdk:
    """Top-level class that wraps all the functionality together."""

    @classmethod
    def create_from_profile(cls, profile: str = "default", profiles_path: Path = PROFILES_FILE_PATH) -> GoodDataSdk:
        """Convenient method to initialize the SDK from config file.

        Args:
            profile (str, optional):
                Profile Name. Defaults to "default".
            profiles_path (Path, optional):
                File path for the profiles. Defaults to PROFILES_FILE_PATH.

        Returns:
            GoodDataSdk:
                Initialized SDK.
        """
        content = profile_content(profile, profiles_path)
        client = GoodDataApiClient(**content)
        return cls(client)

    @classmethod
    def create(
        cls,
        host_: str,
        token_: str,
        extra_user_agent_: Optional[str] = None,
        *,
        executions_cancellable: bool = False,
        **custom_headers_: Optional[str],
    ) -> GoodDataSdk:
        """
        Create common GoodDataApiClient and return new GoodDataSdk instance.
        Custom headers are filtered. Headers with None value are removed. It simplifies usage because headers
        can be created directly from optional values.

        This is preferred way of creating GoodDataSdk, when no tweaks are needed.
        """
        filtered_headers = {key: value for key, value in custom_headers_.items() if value is not None}
        client = GoodDataApiClient(
            host_,
            token_,
            custom_headers=filtered_headers,
            extra_user_agent=extra_user_agent_,
            executions_cancellable=executions_cancellable,
        )
        return cls(client)

    def __init__(self, client: GoodDataApiClient) -> None:
        """Take instance of GoodDataApiClient and return new GoodDataSdk instance.

        Useful when customized GoodDataApiClient is needed. Usually users should use
        `GoodDataSdk.create` classmethod.
        """
        self._client = client

        self._catalog_workspace = CatalogWorkspaceService(self._client)
        self._catalog_workspace_content = CatalogWorkspaceContentService(self._client)
        self._catalog_data_source = CatalogDataSourceService(self._client)
        self._catalog_organization = CatalogOrganizationService(self._client)
        self._catalog_user = CatalogUserService(self._client)
        self._compute = ComputeService(self._client)
        self._visualizations = VisualizationService(self._client)
        self._tables = TableService(self._client)
        self._support = SupportService(self._client)
        self._catalog_permission = CatalogPermissionService(self._client)
        self._export = ExportService(self._client)

    @property
    def catalog_workspace(self) -> CatalogWorkspaceService:
        return self._catalog_workspace

    @property
    def catalog_workspace_content(self) -> CatalogWorkspaceContentService:
        return self._catalog_workspace_content

    @property
    def catalog_data_source(self) -> CatalogDataSourceService:
        return self._catalog_data_source

    @property
    def catalog_organization(self) -> CatalogOrganizationService:
        return self._catalog_organization

    @property
    def compute(self) -> ComputeService:
        return self._compute

    @property
    def visualizations(self) -> VisualizationService:
        return self._visualizations

    @property
    def tables(self) -> TableService:
        return self._tables

    @property
    def support(self) -> SupportService:
        return self._support

    @property
    def catalog_user(self) -> CatalogUserService:
        return self._catalog_user

    @property
    def catalog_permission(self) -> CatalogPermissionService:
        return self._catalog_permission

    @property
    def export(self) -> ExportService:
        return self._export

    @property
    def client(self) -> GoodDataApiClient:
        return self._client

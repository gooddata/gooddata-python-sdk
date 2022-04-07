# (C) 2021 GoodData Corporation
from __future__ import annotations

from typing import Optional

from gooddata_sdk.catalog.data_source.service import CatalogDataSourceService
from gooddata_sdk.catalog.organization.service import CatalogOrganizationService
from gooddata_sdk.catalog.workspace.service import CatalogWorkspaceContentService, CatalogWorkspaceService
from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.compute.service import ComputeService
from gooddata_sdk.insight import InsightService
from gooddata_sdk.support import SupportService
from gooddata_sdk.table import TableService


class GoodDataSdk:
    """Top-level class that wraps all the functionality together."""

    @classmethod
    def create(
        cls,
        host_: str,
        token_: str,
        extra_user_agent_: Optional[str] = None,
        **custom_headers_: Optional[str],
    ) -> GoodDataSdk:
        """
        Create common GoodDataApiClient and return new GoodDataSdk instance.
        Custom headers are filtered. Headers with None value are removed. It simplifies usage because headers
        can be created directly from optional values.

        This is preferred way of creating GoodDataSdk, when no tweaks are needed.
        """
        filtered_headers = {key: value for key, value in custom_headers_.items() if value is not None}
        client = GoodDataApiClient(host_, token_, custom_headers=filtered_headers, extra_user_agent=extra_user_agent_)
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
        self._compute = ComputeService(self._client)
        self._insights = InsightService(self._client)
        self._tables = TableService(self._client)
        self._support = SupportService(self._client)

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
    def insights(self) -> InsightService:
        return self._insights

    @property
    def tables(self) -> TableService:
        return self._tables

    @property
    def support(self) -> SupportService:
        return self._support

# (C) 2024 GoodData Corporation
from __future__ import annotations

from gooddata_api_client import apis

from gooddata_sdk.catalog.analytics_catalog.model.trending_objects import (
    CatalogTrendingObjectsResult,
)
from gooddata_sdk.client import GoodDataApiClient


class CatalogSmartFunctionsService:
    """Service for accessing AI smart functions in the Analytics Catalog."""

    def __init__(self, api_client: GoodDataApiClient) -> None:
        self._client = api_client
        self._smart_functions_api: apis.SmartFunctionsApi = api_client.smart_functions_api

    def get_trending_objects(self, workspace_id: str) -> CatalogTrendingObjectsResult:
        """Return trending objects for the given workspace.

        Args:
            workspace_id: Workspace identifier.

        Returns:
            CatalogTrendingObjectsResult containing a list of trending objects.
        """
        result = self._smart_functions_api.trending_objects(
            workspace_id=workspace_id,
            _check_return_type=False,
        )
        return CatalogTrendingObjectsResult.from_api_model(result)

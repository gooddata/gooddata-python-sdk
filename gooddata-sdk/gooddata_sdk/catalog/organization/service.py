# (C) 2022 GoodData Corporation
from __future__ import annotations

from gooddata_sdk.catalog.catalog_service_base import CatalogServiceBase
from gooddata_sdk.client import GoodDataApiClient


class CatalogOrganizationService(CatalogServiceBase):
    def __init__(self, api_client: GoodDataApiClient) -> None:
        super(CatalogOrganizationService, self).__init__(api_client)

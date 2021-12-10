# (C) 2021 GoodData Corporation
from __future__ import annotations

from gooddata_sdk.catalog import CatalogService
from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.compute import ComputeService
from gooddata_sdk.insight import InsightService
from gooddata_sdk.table import TableService


class GoodDataSdk:
    """Top-level class that wraps all the functionality together."""

    @classmethod
    def new(cls, host, token, custom_headers=None, extra_user_agent=None):
        """Create common GoodDataApiClient and return new GoodDataSdk instance.

        This is preffered way of creating GoodDataSdk, when no tweaks are needed.
        """
        client = GoodDataApiClient(
            host,
            token,
            custom_headers=custom_headers,
            extra_user_agent=extra_user_agent,
        )
        return cls(client)

    def __init__(self, client: GoodDataApiClient):
        """Take instance of GoodDataApiClient and return new GoodDataSdk instance.

        Useful when customized GoodDataApiClient is needed. Usually users should use
        `GoodDataSdk.new` classmethod.
        """
        self._client = client

        self._catalog = CatalogService(self._client)
        self._compute = ComputeService(self._client)
        self._insights = InsightService(self._client)
        self._tables = TableService(self._client)

    @property
    def catalog(self) -> CatalogService:
        return self._catalog

    @property
    def compute(self) -> ComputeService:
        return self._compute

    @property
    def insights(self) -> InsightService:
        return self._insights

    @property
    def tables(self) -> TableService:
        return self._tables


def create_sdk(host: str, token: str, user_agent: str, headers_host: str = None):
    """Return GoodDataSdk instance."""
    headers = {"X-GDC-VALIDATE-RELATIONS": "true"}
    if headers_host:
        headers["Host"] = headers_host
    client = GoodDataApiClient(host, token, custom_headers=headers, extra_user_agent=user_agent)
    return GoodDataSdk(client)

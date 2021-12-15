# (C) 2021 GoodData Corporation
from __future__ import annotations

from typing import Optional

import gooddata_afm_client as afm_client
import gooddata_metadata_client as metadata_client
import gooddata_scan_client as scan_client

USER_AGENT = "gooddata-python-sdk/0.1"


class GoodDataApiClient:
    """Provide access to metadata and afm services."""

    def __init__(
        self,
        host: str,
        token: str,
        custom_headers: Optional[dict[str, str]] = None,
        extra_user_agent: Optional[str] = None,
    ) -> None:
        """Take url, token for connecting to GoodData.CN.

        HTTP requests made by this class may be enriched by `custom_headers` dict
        containing header names as keys and header values as dict values.

        `extra_user_agent` is optional string to be added to default http User-Agent
        header. This takes precedence over custom_headers setting.
        """
        self._hostname = host
        self._token = token
        self._custom_headers = custom_headers or {}

        user_agent = f"{USER_AGENT} {extra_user_agent}" if extra_user_agent is not None else USER_AGENT

        self._metadata_config = metadata_client.Configuration(host=host)
        self._metadata_client = metadata_client.ApiClient(
            configuration=self._metadata_config,
            header_name="Authorization",
            header_value=f"Bearer {token}",
        )
        self._metadata_client.default_headers["X-Requested-With"] = "XMLHttpRequest"
        for header_name, header_value in self._custom_headers.items():
            self._metadata_client.default_headers[header_name] = header_value
        self._metadata_client.user_agent = user_agent

        self._scan_config = scan_client.Configuration(host=host)
        self._scan_client = scan_client.ApiClient(
            configuration=self._scan_config,
            header_name="Authorization",
            header_value=f"Bearer {token}",
        )
        self._scan_client.default_headers["X-Requested-With"] = "XMLHttpRequest"
        for header_name, header_value in self._custom_headers.items():
            self._scan_client.default_headers[header_name] = header_value
        self._scan_client.user_agent = user_agent

        self._afm_config = afm_client.Configuration(host=host)
        self._afm_client = afm_client.ApiClient(
            configuration=self._afm_config,
            header_name="Authorization",
            header_value=f"Bearer {token}",
        )
        self._afm_client.default_headers["X-Requested-With"] = "XMLHttpRequest"
        for header_name, header_value in self._custom_headers.items():
            self._afm_client.default_headers[header_name] = header_value
        self._afm_client.user_agent = user_agent

    @property
    def afm_client(self) -> afm_client.ApiClient:
        return self._afm_client

    @property
    def metadata_client(self) -> metadata_client.ApiClient:
        return self._metadata_client

    @property
    def scan_client(self) -> scan_client.ApiClient:
        return self._scan_client

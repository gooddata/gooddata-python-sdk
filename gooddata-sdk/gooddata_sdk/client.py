# (C) 2021 GoodData Corporation
""" Module containing a class that provides access to metadata and afm services.
"""

from __future__ import annotations

from typing import Optional
from warnings import warn

import gooddata_afm_client as afm_client
import gooddata_api_client as api_client
import gooddata_api_client.apis as apis
import gooddata_metadata_client as metadata_client
import gooddata_scan_client as scan_client
from gooddata_sdk import __version__

USER_AGENT = f"gooddata-python-sdk/{__version__}"


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

        self._api_config = api_client.Configuration(host=host)
        self._api_client = api_client.ApiClient(
            configuration=self._api_config,
            header_name="Authorization",
            header_value=f"Bearer {token}",
        )
        self._set_default_headers(self._api_client.default_headers)
        for header_name, header_value in self._custom_headers.items():
            self._api_client.default_headers[header_name] = header_value
        self._api_client.user_agent = user_agent

        self._entities_api = apis.EntitiesApi(self._api_client)
        self._layout_api = apis.LayoutApi(self._api_client)
        self._actions_api = apis.ActionsApi(self._api_client)

        # The initialization below will be deleted with version 2.0
        self._metadata_config = metadata_client.Configuration(host=host)
        self._metadata_client = metadata_client.ApiClient(
            configuration=self._metadata_config,
            header_name="Authorization",
            header_value=f"Bearer {token}",
        )
        self._set_default_headers(self._metadata_client.default_headers)
        for header_name, header_value in self._custom_headers.items():
            self._metadata_client.default_headers[header_name] = header_value
        self._metadata_client.user_agent = user_agent

        self._scan_config = scan_client.Configuration(host=host)
        self._scan_client = scan_client.ApiClient(
            configuration=self._scan_config,
            header_name="Authorization",
            header_value=f"Bearer {token}",
        )
        self._set_default_headers(self._scan_client.default_headers)
        for header_name, header_value in self._custom_headers.items():
            self._scan_client.default_headers[header_name] = header_value
        self._scan_client.user_agent = user_agent

        self._afm_config = afm_client.Configuration(host=host)
        self._afm_client = afm_client.ApiClient(
            configuration=self._afm_config,
            header_name="Authorization",
            header_value=f"Bearer {token}",
        )
        self._set_default_headers(self._afm_client.default_headers)
        for header_name, header_value in self._custom_headers.items():
            self._afm_client.default_headers[header_name] = header_value
        self._afm_client.user_agent = user_agent

    @staticmethod
    def _set_default_headers(headers: dict) -> None:
        headers["X-Requested-With"] = "XMLHttpRequest"
        headers["X-GDC-VALIDATE-RELATIONS"] = "true"

    @property
    def custom_headers(self) -> dict[str, str]:
        return self._custom_headers

    @property
    def afm_client(self) -> afm_client.ApiClient:
        warn(
            "This property is deprecated and it will be removed in PythonSDK 2.0. "
            "Please use entities_api, layout_api, actions_api properties instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._afm_client

    @property
    def metadata_client(self) -> metadata_client.ApiClient:
        warn(
            "This property is deprecated and it will be removed in PythonSDK 2.0. "
            "Please use entities_api, layout_api, actions_api properties instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._metadata_client

    @property
    def scan_client(self) -> scan_client.ApiClient:
        warn(
            "This property is deprecated and it will be removed in PythonSDK 2.0. "
            "Please use entities_api, layout_api, actions_api properties instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._scan_client

    @property
    def entities_api(self) -> apis.EntitiesApi:
        return self._entities_api

    @property
    def layout_api(self) -> apis.LayoutApi:
        return self._layout_api

    @property
    def actions_api(self) -> apis.ActionsApi:
        return self._actions_api

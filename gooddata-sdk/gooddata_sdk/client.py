# (C) 2021 GoodData Corporation
"""Module containing a class that provides access to metadata and afm services."""

from __future__ import annotations

from typing import Optional

import gooddata_api_client as api_client
import requests
from gooddata_api_client import apis

from gooddata_sdk import __version__
from gooddata_sdk.utils import HttpMethod

USER_AGENT = f"gooddata-python-sdk/{__version__}"


class GoodDataApiClient:
    """Provide access to metadata and afm services."""

    def __init__(
        self,
        host: str,
        token: str,
        custom_headers: Optional[dict[str, str]] = None,
        extra_user_agent: Optional[str] = None,
        executions_cancellable: bool = False,
    ) -> None:
        """Take url, token for connecting to GoodData.CN.

        HTTP requests made by this class may be enriched by `custom_headers` dict
        containing header names as keys and header values as dict values.

        `extra_user_agent` is optional string to be added to default http User-Agent
        header. This takes precedence over custom_headers setting.

        `executions_cancellable` is a flag that sets all executions computed through this client as cancellable.
        In case a request for a result is interrupted, the GD server will try to free resources like killing sql queries
        related to the given execution.
        """
        self._hostname = host
        self._token = token
        self._custom_headers = custom_headers or {}
        self._default_headers = {"Accept-Encoding": "br, gzip, deflate"}

        user_agent = f"{USER_AGENT} {extra_user_agent}" if extra_user_agent is not None else USER_AGENT

        self._api_config = api_client.Configuration(host=host)
        self._api_client = api_client.ApiClient(
            configuration=self._api_config,
            header_name="Authorization",
            header_value=f"Bearer {token}",
        )
        self._set_default_headers(self._api_client.default_headers)
        for header_name, header_value in self._default_headers.items():
            self._api_client.default_headers[header_name] = header_value
        for header_name, header_value in self._custom_headers.items():
            self._api_client.default_headers[header_name] = header_value
        self._api_client.user_agent = user_agent

        self._entities_api = apis.EntitiesApi(self._api_client)
        self._layout_api = apis.LayoutApi(self._api_client)
        self._actions_api = apis.ActionsApi(self._api_client)
        self._user_management_api = apis.UserManagementApi(self._api_client)
        self._executions_cancellable = executions_cancellable

    def _do_post_request(
        self,
        data: bytes,
        endpoint: str,
        content_type: str,
    ) -> requests.Response:
        """Perform a POST request to a specified endpoint.

        Args:
            data (bytes): The data to be sent in the POST request.
            endpoint (str): The endpoint URL to which the request is made.
            content_type (str): The content type of the data being sent.

        Returns:
            None
        """
        if not self._hostname.endswith("/"):
            endpoint = f"/{endpoint}"

        response = requests.post(
            url=f"{self._hostname}{endpoint}",
            headers={
                "Content-Type": content_type,
                "Authorization": f"Bearer {self._token}",
            },
            data=data,
        )

        return response

    def do_request(
        self,
        data: bytes,
        endpoint: str,
        content_type: str,
        method: HttpMethod,
    ) -> requests.Response:
        """Perform an HTTP request using the specified method.

        Args:
            data (bytes): The data to be sent in the request.
            endpoint (str): The endpoint URL to which the request is made.
            content_type (str): The content type of the data being sent.
            method (HttpMethod): The HTTP method to be used for the request.

        Returns:
            None

        Raises:
            NotImplementedError: If the specified HTTP method is not supported.
        """
        if method == HttpMethod.POST:
            self._do_post_request(data, endpoint, content_type)
        else:
            raise NotImplementedError("Currently only supports the POST method.")

    @staticmethod
    def _set_default_headers(headers: dict) -> None:
        headers["X-Requested-With"] = "XMLHttpRequest"
        headers["X-GDC-VALIDATE-RELATIONS"] = "true"

    @property
    def custom_headers(self) -> dict[str, str]:
        return self._custom_headers

    @property
    def entities_api(self) -> apis.EntitiesApi:
        return self._entities_api

    @property
    def layout_api(self) -> apis.LayoutApi:
        return self._layout_api

    @property
    def actions_api(self) -> apis.ActionsApi:
        return self._actions_api

    @property
    def user_management_api(self) -> apis.UserManagementApi:
        return self._user_management_api

    @property
    def executions_cancellable(self) -> bool:
        return self._executions_cancellable

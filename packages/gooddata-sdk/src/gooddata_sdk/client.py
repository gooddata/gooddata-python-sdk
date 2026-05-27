# (C) 2021 GoodData Corporation
"""Module containing a class that provides access to metadata and afm services."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path

import gooddata_api_client as api_client
import requests
from gooddata_api_client import apis
from requests.adapters import HTTPAdapter
from urllib3.exceptions import MaxRetryError
from urllib3.util.retry import Retry

from gooddata_sdk import __version__
from gooddata_sdk.utils import HttpMethod

logger = logging.getLogger(__name__)

USER_AGENT = f"gooddata-python-sdk/{__version__}"

DEFAULT_RETRY_ALLOWED_METHODS: frozenset[str] = frozenset(
    ["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST", "PATCH"]
)


@dataclass(frozen=True)
class GoodDataApiClientRetryConfig:
    """Retry policy for transient HTTP failures.

    The same policy is applied to both transport paths:
    - the generated `gooddata-api-client` (via `urllib3` `Retry`)
    - the direct `requests`-based POST in `GoodDataApiClient._do_post_request`
      (via `HTTPAdapter` mounted on a `Session`)

    `Retry-After` from the server is honoured automatically; `backoff_factor`
    only applies when that header is absent.
    """

    max_retries: int = 10
    backoff_factor: float = 0.5
    backoff_max: float = 60.0
    status_forcelist: tuple[int, ...] = (429,)
    allowed_methods: frozenset[str] = field(default_factory=lambda: DEFAULT_RETRY_ALLOWED_METHODS)


class _LoggingRetry(Retry):
    """Retry that logs each rate-limit hit and final exhaustion.

    Logs at WARNING when a configured status (HTTP 429 by default) is
    received and a retry is scheduled, and at ERROR when retries are
    exhausted. Other retry causes (connection errors, redirects, etc.)
    are left to urllib3's own logging.
    """

    def increment(  # type: ignore[override]
        self,
        method=None,
        url=None,
        response=None,
        error=None,
        _pool=None,
        _stacktrace=None,
    ):
        if response is not None and response.status in self.status_forcelist:
            logger.warning(
                "GoodData API rate-limited: %s %s -> %s; Retry-After=%s; retries left=%s",
                method,
                url,
                response.status,
                response.headers.get("Retry-After"),
                self.total,
            )
            try:
                return super().increment(method, url, response, error, _pool, _stacktrace)
            except MaxRetryError:
                logger.error(
                    "GoodData API rate-limit retries exhausted: %s %s -> %s",
                    method,
                    url,
                    response.status,
                )
                raise
        return super().increment(method, url, response, error, _pool, _stacktrace)


def _build_urllib3_retry(retry_config: GoodDataApiClientRetryConfig) -> Retry:
    return _LoggingRetry(
        total=retry_config.max_retries,
        connect=0,
        read=0,
        other=0,
        status=retry_config.max_retries,
        backoff_factor=retry_config.backoff_factor,
        backoff_max=retry_config.backoff_max,
        status_forcelist=retry_config.status_forcelist,
        allowed_methods=retry_config.allowed_methods,
        respect_retry_after_header=True,
        raise_on_status=False,
    )


class GoodDataApiClient:
    """Provide access to metadata and afm services."""

    def __init__(
        self,
        host: str,
        token: str,
        custom_headers: dict[str, str] | None = None,
        extra_user_agent: str | None = None,
        executions_cancellable: bool = False,
        ssl_ca_cert: str | None = None,
        proxy: str | None = None,
        retry_config: GoodDataApiClientRetryConfig | None = None,
    ) -> None:
        """Take url, token for connecting to GoodData.CN.

        HTTP requests made by this class may be enriched by `custom_headers` dict
        containing header names as keys and header values as dict values.

        `extra_user_agent` is optional string to be added to default http User-Agent
        header. This takes precedence over custom_headers setting.

        `executions_cancellable` is a flag that sets all executions computed through this client as cancellable.
        In case a request for a result is interrupted, the GD server will try to free resources like killing sql queries
        related to the given execution.

        `proxy` is optional URL of an HTTP(S) proxy (e.g. ``http://proxy:8080``).
        When not set, the standard ``HTTPS_PROXY`` / ``https_proxy`` / ``HTTP_PROXY`` /
        ``http_proxy`` environment variables are checked automatically.

        `retry_config` controls retry behaviour for transient HTTP failures
        (HTTP 429 by default). When omitted, sensible defaults are used and
        ``Retry-After`` is honoured automatically.
        """
        self._hostname = host
        self._token = token
        self._custom_headers = custom_headers or {}
        self._default_headers = {"Accept-Encoding": "br, gzip, deflate"}

        user_agent = f"{USER_AGENT} {extra_user_agent}" if extra_user_agent is not None else USER_AGENT

        if ssl_ca_cert is not None:
            ssl_ca_cert_path = Path(ssl_ca_cert)
            if not ssl_ca_cert_path.exists():
                raise ValueError(
                    f"ssl_ca_cert file path specified but the file does not exist. Path: {ssl_ca_cert_path}."
                )

        if proxy is None:
            proxy = (
                os.environ.get("HTTPS_PROXY")
                or os.environ.get("https_proxy")
                or os.environ.get("HTTP_PROXY")
                or os.environ.get("http_proxy")
                or None
            )

        self._retry_config = retry_config or GoodDataApiClientRetryConfig()
        self._retry = _build_urllib3_retry(self._retry_config)

        self._api_config = api_client.Configuration(host=host, ssl_ca_cert=ssl_ca_cert)
        self._api_config.retries = self._retry
        if proxy:
            self._api_config.proxy = proxy
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

        self._session = requests.Session()
        adapter = HTTPAdapter(max_retries=_build_urllib3_retry(self._retry_config))
        self._session.mount("http://", adapter)
        self._session.mount("https://", adapter)

        self._entities_api = apis.EntitiesApi(self._api_client)
        self._layout_api = apis.LayoutApi(self._api_client)
        self._actions_api = apis.ActionsApi(self._api_client)
        self._user_management_api = apis.UserManagementApi(self._api_client)
        self._appearance_api = apis.AppearanceApi(self._api_client)
        self._ai_lake_api = apis.AILakeApi(self._api_client)
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

        response = self._session.post(
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
            requests.Response: The response from the HTTP request.

        Raises:
            NotImplementedError: If the specified HTTP method is not supported.
        """
        if method == HttpMethod.POST:
            return self._do_post_request(data, endpoint, content_type)
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
    def appearance_api(self) -> apis.AppearanceApi:
        return self._appearance_api

    @property
    def ai_lake_api(self) -> apis.AILakeApi:
        return self._ai_lake_api

    @property
    def executions_cancellable(self) -> bool:
        return self._executions_cancellable

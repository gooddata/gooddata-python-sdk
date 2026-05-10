# (C) 2021 GoodData Corporation
import os
from unittest import mock

from gooddata_sdk import GoodDataApiClient, GoodDataSdk


def test_http_headers_precedence():
    c = GoodDataApiClient(
        "host",
        "token",
        custom_headers={"User-Agent": "not-this"},
        extra_user_agent="yes",
    )
    agent = c._api_client.default_headers["User-Agent"]
    assert agent.startswith("gooddata")
    assert agent.endswith("yes")


class TestProxy:
    """Proxy configuration for the underlying urllib3 pool manager."""

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_no_proxy_when_env_empty(self):
        c = GoodDataApiClient("https://example.com", "token")
        assert c._api_config.proxy is None

    def test_explicit_proxy(self):
        c = GoodDataApiClient("https://example.com", "token", proxy="http://myproxy:8080")
        assert c._api_config.proxy == "http://myproxy:8080"

    @mock.patch.dict(os.environ, {"HTTPS_PROXY": "http://envproxy:3128"}, clear=True)
    def test_proxy_from_https_proxy_env(self):
        c = GoodDataApiClient("https://example.com", "token")
        assert c._api_config.proxy == "http://envproxy:3128"

    @mock.patch.dict(os.environ, {"https_proxy": "http://lower:3128"}, clear=True)
    def test_proxy_from_lowercase_https_proxy_env(self):
        c = GoodDataApiClient("https://example.com", "token")
        assert c._api_config.proxy == "http://lower:3128"

    @mock.patch.dict(os.environ, {"HTTP_PROXY": "http://httpproxy:3128"}, clear=True)
    def test_proxy_from_http_proxy_env(self):
        c = GoodDataApiClient("https://example.com", "token")
        assert c._api_config.proxy == "http://httpproxy:3128"

    @mock.patch.dict(
        os.environ,
        {
            "HTTPS_PROXY": "http://preferred:3128",
            "HTTP_PROXY": "http://fallback:3128",
        },
        clear=True,
    )
    def test_https_proxy_takes_precedence_over_http_proxy(self):
        c = GoodDataApiClient("https://example.com", "token")
        assert c._api_config.proxy == "http://preferred:3128"

    @mock.patch.dict(os.environ, {"HTTPS_PROXY": "http://envproxy:3128"}, clear=True)
    def test_explicit_proxy_overrides_env(self):
        c = GoodDataApiClient("https://example.com", "token", proxy="http://explicit:8080")
        assert c._api_config.proxy == "http://explicit:8080"

    def test_sdk_create_with_explicit_proxy(self):
        sdk = GoodDataSdk.create("https://example.com", "token", proxy="http://myproxy:8080")
        assert sdk.client._api_config.proxy == "http://myproxy:8080"

    @mock.patch.dict(os.environ, {"HTTPS_PROXY": "http://envproxy:3128"}, clear=True)
    def test_sdk_create_picks_up_env_proxy(self):
        sdk = GoodDataSdk.create("https://example.com", "token")
        assert sdk.client._api_config.proxy == "http://envproxy:3128"

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_sdk_create_no_proxy_when_env_empty(self):
        sdk = GoodDataSdk.create("https://example.com", "token")
        assert sdk.client._api_config.proxy is None

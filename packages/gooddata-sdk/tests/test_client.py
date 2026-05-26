# (C) 2021 GoodData Corporation
import os
from unittest import mock

from gooddata_sdk import GoodDataApiClient, GoodDataApiClientRetryConfig, GoodDataSdk
from urllib3.util.retry import Retry


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


class TestGoodDataApiClientRetryConfig:
    """Retry/back-off config propagates to both transport paths."""

    def test_defaults_match_public_rate_limit_contract(self):
        c = GoodDataApiClient("https://example.com", "token")
        retry = c._api_config.retries
        assert isinstance(retry, Retry)
        assert retry.total == 10
        assert retry.backoff_factor == 0.5
        assert 429 in retry.status_forcelist
        assert retry.respect_retry_after_header is True
        for method in ("GET", "POST", "PUT", "PATCH", "DELETE"):
            assert method in retry.allowed_methods

    def test_custom_retry_config_overrides_defaults(self):
        cfg = GoodDataApiClientRetryConfig(
            max_retries=3,
            backoff_factor=2.0,
            status_forcelist=(429, 503),
            allowed_methods=frozenset(["GET", "HEAD"]),
        )
        c = GoodDataApiClient("https://example.com", "token", retry_config=cfg)
        retry = c._api_config.retries
        assert retry.total == 3
        assert retry.backoff_factor == 2.0
        assert retry.status_forcelist == (429, 503)
        assert retry.allowed_methods == frozenset(["GET", "HEAD"])

    def test_session_adapter_uses_same_retry_policy(self):
        c = GoodDataApiClient("https://example.com", "token")
        for scheme in ("http://", "https://"):
            adapter = c._session.get_adapter(scheme + "example.com")
            assert adapter.max_retries.total == c._retry_config.max_retries
            assert adapter.max_retries.status_forcelist == c._retry_config.status_forcelist

    def test_sdk_wraps_client_with_custom_retry_config(self):
        cfg = GoodDataApiClientRetryConfig(max_retries=2)
        client = GoodDataApiClient("https://example.com", "token", retry_config=cfg)
        sdk = GoodDataSdk(client)
        assert sdk.client._api_config.retries.total == 2

    def test_rate_limit_hit_logs_warning(self):
        c = GoodDataApiClient("https://example.com", "token")
        retry = c._api_config.retries
        fake_response = mock.Mock(status=429, headers={"Retry-After": "2"})
        with mock.patch("gooddata_sdk.client.logger") as mock_logger:
            retry.increment(method="POST", url="/api/v1/entities/users", response=fake_response)
        assert mock_logger.warning.called
        fmt = mock_logger.warning.call_args.args[0]
        assert "rate-limited" in fmt
        assert mock_logger.error.called is False

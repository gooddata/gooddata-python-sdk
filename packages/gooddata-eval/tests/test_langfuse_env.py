# (C) 2026 GoodData Corporation
from __future__ import annotations

import base64

import httpx
import pytest
from gooddata_eval._version import __version__
from gooddata_eval.core.langfuse._env import (
    basic_auth_header,
    credentials_present,
    make_http_client,
    resolve_base_url,
    resource_attributes,
    user_agent,
)

_GITHUB_ENV = {
    "GITHUB_ACTIONS": "true",
    "GITHUB_RUN_ID": "18273645",
    "GITHUB_SHA": "0123456789abcdef0123456789abcdef01234567",
    "GITHUB_WORKFLOW": "AI agent tests (staging)",
    "GITHUB_REF_NAME": "master",
    "GITHUB_EVENT_NAME": "schedule",
}


@pytest.fixture
def outside_ci(monkeypatch):
    for name in _GITHUB_ENV:
        monkeypatch.delenv(name, raising=False)


@pytest.fixture
def in_ci(monkeypatch):
    for name, value in _GITHUB_ENV.items():
        monkeypatch.setenv(name, value)


def test_resolve_base_url_prefers_base_url_over_host(monkeypatch):
    monkeypatch.setenv("LANGFUSE_BASE_URL", "https://base.example.com")
    monkeypatch.setenv("LANGFUSE_HOST", "https://host.example.com")
    assert resolve_base_url() == "https://base.example.com"


def test_resolve_base_url_falls_back_to_host(monkeypatch):
    monkeypatch.delenv("LANGFUSE_BASE_URL", raising=False)
    monkeypatch.setenv("LANGFUSE_HOST", "https://host.example.com")
    assert resolve_base_url() == "https://host.example.com"


def test_resolve_base_url_default(monkeypatch):
    monkeypatch.delenv("LANGFUSE_BASE_URL", raising=False)
    monkeypatch.delenv("LANGFUSE_HOST", raising=False)
    assert resolve_base_url() == "https://us.cloud.langfuse.com"


def test_resolve_base_url_strips_trailing_slash(monkeypatch):
    monkeypatch.setenv("LANGFUSE_BASE_URL", "https://base.example.com/")
    assert resolve_base_url() == "https://base.example.com"


def test_credentials_present_true(monkeypatch):
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-test")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-test")
    assert credentials_present() is True


def test_credentials_present_false_when_missing(monkeypatch):
    monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-test")
    assert credentials_present() is False


def test_basic_auth_header_missing_credentials_raises(monkeypatch):
    monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
    monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
    with pytest.raises(RuntimeError, match="credentials"):
        basic_auth_header()


def test_basic_auth_header_encodes_credentials(monkeypatch):
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-test")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-test")
    header = basic_auth_header()
    assert header.startswith("Basic ")
    assert base64.b64decode(header.removeprefix("Basic ")).decode() == "pk-test:sk-test"


def test_make_http_client_uses_resolved_base_url_and_auth(monkeypatch):
    monkeypatch.setenv("LANGFUSE_BASE_URL", "https://base.example.com")
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-test")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-test")

    client = make_http_client(timeout=5)
    try:
        assert str(client.base_url).rstrip("/") == "https://base.example.com"
        assert client.headers["Authorization"].startswith("Basic ")
    finally:
        client.close()


def test_a_ci_run_names_the_package_its_run_and_short_sha(in_ci):
    assert user_agent() == f"gooddata-eval/{__version__} (ci; run=18273645; sha=0123456789ab)"


def test_outside_ci_the_user_agent_falls_back_to_local(outside_ci):
    assert user_agent() == f"gooddata-eval/{__version__} (local; run=local; sha=local)"


@pytest.mark.parametrize("value", ["", "18273645\r\nX-Injected: 1", "run id"])
def test_a_blank_or_unsafe_run_id_falls_back_to_local(outside_ci, monkeypatch, value):
    monkeypatch.setenv("GITHUB_RUN_ID", value)
    assert "run=local;" in user_agent()


def test_every_request_of_the_http_client_carries_the_user_agent(in_ci, monkeypatch):
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-test")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-test")
    sent: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(request)
        return httpx.Response(200, json={})

    with make_http_client(timeout=5, transport=httpx.MockTransport(handler)) as client:
        client.get("/api/public/v2/observations")

    assert sent[0].headers["User-Agent"] == user_agent()


def test_a_ci_run_puts_its_github_context_on_the_resource(in_ci):
    assert resource_attributes() == {
        "service.name": "gooddata-eval",
        "service.version": __version__,
        "github.run_id": "18273645",
        "github.workflow": "AI agent tests (staging)",
        "github.ref_name": "master",
        "github.event_name": "schedule",
    }


def test_outside_ci_the_resource_names_only_the_service(outside_ci):
    assert resource_attributes() == {"service.name": "gooddata-eval", "service.version": __version__}

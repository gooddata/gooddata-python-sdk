# (C) 2026 GoodData Corporation
from __future__ import annotations

import base64

import pytest
from gooddata_eval.core.langfuse._env import basic_auth_header, credentials_present, make_http_client, resolve_base_url


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
        assert str(client.base_url) == "https://base.example.com"
        assert client.headers["Authorization"].startswith("Basic ")
    finally:
        client.close()

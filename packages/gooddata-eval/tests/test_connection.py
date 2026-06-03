# (C) 2026 GoodData Corporation
import pytest
from gooddata_eval.core.connection import ConnectionError_, resolve_connection


def test_resolve_connection_prefers_explicit_token(monkeypatch):
    monkeypatch.delenv("GOODDATA_TOKEN", raising=False)
    host, token = resolve_connection(host="https://h", token="t123", profile=None)
    assert (host, token) == ("https://h", "t123")


def test_resolve_connection_uses_env_token(monkeypatch):
    monkeypatch.setenv("GOODDATA_TOKEN", "envtok")
    host, token = resolve_connection(host="https://h", token=None, profile=None)
    assert token == "envtok"


def test_resolve_connection_uses_profile(monkeypatch):
    monkeypatch.setattr(
        "gooddata_eval.core.connection.profile_content",
        lambda profile: {"host": "https://from-profile", "token": "ptok"},
    )
    host, token = resolve_connection(host=None, token=None, profile="default")
    assert (host, token) == ("https://from-profile", "ptok")


def test_resolve_connection_missing_host_raises(monkeypatch):
    monkeypatch.delenv("GOODDATA_TOKEN", raising=False)
    with pytest.raises(ConnectionError_, match="host"):
        resolve_connection(host=None, token="t", profile=None)


def test_resolve_connection_missing_token_raises(monkeypatch):
    monkeypatch.delenv("GOODDATA_TOKEN", raising=False)
    with pytest.raises(ConnectionError_, match="token"):
        resolve_connection(host="https://h", token=None, profile=None)

# (C) 2026 GoodData Corporation
from pathlib import Path

import pytest

from tests._fake_langfuse import FakeLangfuse


@pytest.fixture
def fixtures_dir() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def fake_langfuse(monkeypatch: pytest.MonkeyPatch):
    """A running fake Langfuse server with the real client's env vars pointed at it."""
    with FakeLangfuse() as server:
        monkeypatch.setenv("LANGFUSE_BASE_URL", server.base_url)
        monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-fake")
        monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-fake")
        monkeypatch.delenv("LANGFUSE_HOST", raising=False)
        yield server

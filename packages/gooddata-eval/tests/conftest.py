# (C) 2026 GoodData Corporation
from pathlib import Path

import pytest

from tests._fake_langfuse import FakeLangfuse


@pytest.fixture
def fixtures_dir() -> Path:
    return Path(__file__).parent / "fixtures"


# gd-eval reads connection and retry settings from the environment, so a developer
# shell that exports them (as a real eval run must) would otherwise rewrite what
# these tests expect -- e.g. GOODDATA_EVAL_CHAT_MAX_RETRIES=1 turns the expected
# 6 attempts into 2. CI has none of them set, so this is a no-op there.
_LEAKY_ENV = (
    "GOODDATA_TOKEN",
    "GOODDATA_HOST",
    "GOODDATA_PROFILE",
    "GOODDATA_EVAL_CHAT_MAX_RETRIES",
    "GOODDATA_EVAL_CHAT_INITIAL_BACKOFF_S",
    "GOODDATA_EVAL_CHAT_BACKOFF_FACTOR",
    "GOODDATA_EVAL_CHAT_MAX_BACKOFF_S",
    "GOODDATA_EVAL_CHAT_TURN_TIMEOUT_S",
    "GOODDATA_EVAL_CHAT_ITEM_TIMEOUT_S",
)


@pytest.fixture(autouse=True)
def _isolate_gooddata_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in _LEAKY_ENV:
        monkeypatch.delenv(name, raising=False)


@pytest.fixture
def fake_langfuse(monkeypatch: pytest.MonkeyPatch):
    """A running fake Langfuse server with the real client's env vars pointed at it."""
    with FakeLangfuse() as server:
        monkeypatch.setenv("LANGFUSE_BASE_URL", server.base_url)
        monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-fake")
        monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-fake")
        monkeypatch.delenv("LANGFUSE_HOST", raising=False)
        yield server

# (C) 2026 GoodData Corporation
from pathlib import Path

import pytest


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

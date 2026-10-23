# (C) 2026 GoodData Corporation
"""Bounded exponential-backoff retry shared by the gen-ai HTTP clients.

The budget is read from the ``GOODDATA_EVAL_CHAT_*`` environment on every call, so the chat
and takeaway clients retune together.
"""

from __future__ import annotations

import logging
import os
import time
from collections.abc import Callable
from typing import TypeVar

_log = logging.getLogger(__name__)

T = TypeVar("T")

# 500 is here on evidence, not on principle: in one visualization eval batch it hard-failed
# 10 of 56 runs with zero retry attempts, and every affected question scored normally when the
# same question/model ran again the next day -- i.e. transient gen-ai faults, not deterministic
# server bugs. A genuinely deterministic 500 still terminates, just after the bounded backoff.
RETRYABLE_STATUS_CODES: frozenset[int] = frozenset({429, 500, 502, 503, 504})


def int_env(name: str, default: int) -> int:
    """Read an int from the environment, falling back to ``default`` when unset or blank."""
    raw = os.getenv(name)
    return int(raw) if raw else default


def float_env(name: str, default: float) -> float:
    """Read a float from the environment, falling back to ``default`` when unset or blank."""
    raw = os.getenv(name)
    return float(raw) if raw else default


# Retry budget defaults, giving a ~2 min worst-case cap per send (5/10/20/40/60s).
# Each is overridable via env so CI can retune without cutting a new release --
# read per call rather than at import, so an exported value cannot silently
# rewrite what a test that patches these attributes expects.
_MAX_RETRIES_DEFAULT = 5
_INITIAL_BACKOFF_S_DEFAULT = 5.0
_BACKOFF_FACTOR_DEFAULT = 2.0
_MAX_BACKOFF_S_DEFAULT = 60.0


def retry_transient(operation: Callable[[], T], *, is_retryable: Callable[[Exception], bool]) -> T:
    """Run ``operation``; retry retryable failures with bounded exponential backoff."""
    max_retries = int_env("GOODDATA_EVAL_CHAT_MAX_RETRIES", _MAX_RETRIES_DEFAULT)
    delay = float_env("GOODDATA_EVAL_CHAT_INITIAL_BACKOFF_S", _INITIAL_BACKOFF_S_DEFAULT)
    factor = float_env("GOODDATA_EVAL_CHAT_BACKOFF_FACTOR", _BACKOFF_FACTOR_DEFAULT)
    max_backoff = float_env("GOODDATA_EVAL_CHAT_MAX_BACKOFF_S", _MAX_BACKOFF_S_DEFAULT)
    for attempt in range(max_retries + 1):  # 0..N => N retries + 1 initial attempt
        try:
            return operation()
        except Exception as exc:  # noqa: PERF203 — retry loop: per-attempt try/except is intentional
            if attempt == max_retries or not is_retryable(exc):
                raise
            sleep_s = min(delay, max_backoff)
            _log.warning(
                "Transient gen-ai error (attempt %d/%d): %s; retrying in %.0fs",
                attempt + 1,
                max_retries + 1,
                exc,
                sleep_s,
            )
            time.sleep(sleep_s)
            delay *= factor
    raise AssertionError("unreachable")  # loop either returns or raises

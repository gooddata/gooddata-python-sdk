# (C) 2026 GoodData Corporation. All rights reserved.
"""Read-back of the two sinks the agentic_obfuscation kind asserts on.

* conversation DB -- the stored copy, read over the same API the UI uses on reload.
* Langfuse -- every trace of the conversation's session, with full observation input/output.

Unlike the trace linking in ``_langfuse``, nothing here swallows an error: an absence
assertion over a sink that was never read would pass for the wrong reason, so every failure
to read raises :class:`SinkUnavailableError`.
"""

from __future__ import annotations

import os
import time
from collections.abc import Callable, Sequence
from typing import Any

import httpx

from gooddata_eval.core.agentic._obfuscation_check import contains

_LANGFUSE_TIMEOUT_ENV = "GD_EVAL_OBFUSCATION_LANGFUSE_TIMEOUT_SEC"
_DEFAULT_LANGFUSE_TIMEOUT_SEC = 60.0
TRACE_NOT_FOUND = "TRACE_NOT_FOUND"
_DB_TIMEOUT_SEC = 60.0
_POLL_INTERVAL_SEC = 5.0


class SinkUnavailableError(AssertionError):
    """A sink could not be read, so nothing may be concluded from its contents."""


class _LangfuseReadError(SinkUnavailableError):
    """Langfuse answered a read with an error: the sink was not read, which is not an empty sink."""


class TraceNotFoundError(SinkUnavailableError):
    """Langfuse holds no trace for the conversation's session once the wait is over.

    Kept apart from a trace that arrived incomplete: it points at the export leg (a dropped
    batch, a disabled trace flag, the wrong Langfuse project), not at masking.
    """


def _poll(
    read: Callable[[], Any],
    done: Callable[[Any], bool],
    timeout_sec: float,
    what: str,
    shape: Callable[[Any], Any] = lambda doc: doc,
    sleep: Callable[[float], None] = time.sleep,
) -> Any:
    """Read until ``done`` holds and one further read has the same ``shape``.

    On timeout a non-empty document is still returned, so the verdict can say why it is
    incomplete (a missing anchor, a redacted trace); only an empty one raises.
    """
    deadline = time.monotonic() + timeout_sec
    previous: Any = None
    while True:
        current = read()
        if done(current) and previous is not None and shape(current) == previous:
            return current
        previous = shape(current) if done(current) else None
        if time.monotonic() >= deadline:
            if done(current) or current:
                return current
            raise SinkUnavailableError(f"{what}: not complete after {timeout_sec:.0f}s")
        sleep(_POLL_INTERVAL_SEC)


def read_conversation_db(
    http: httpx.Client,
    conversations_url: str,
    conversation_id: str,
    anchors: Sequence[str],
) -> dict[str, Any]:
    """The stored conversation (record + every item), once every turn's anchor is persisted.

    ``http`` carries the GoodData credentials. ``anchors`` may be empty for a rejected turn,
    where nothing is expected to be stored.
    """
    base = f"{conversations_url.rstrip('/')}/{conversation_id}"

    def get(url: str) -> Any:
        try:
            resp = http.get(url, headers={"Accept": "application/json"})
        except httpx.TimeoutException:
            raise
        except httpx.HTTPError as exc:
            raise SinkUnavailableError(f"GET {url}: {exc}") from exc
        if resp.status_code >= 400:
            raise SinkUnavailableError(f"GET {url} -> {resp.status_code}: {resp.text[:300]}")
        try:
            return resp.json()
        except ValueError as exc:
            raise SinkUnavailableError(f"GET {url}: the body is not JSON") from exc

    def read() -> dict[str, Any] | None:
        try:
            items = get(f"{base}/items").get("items", [])
            if not items and anchors:
                return None
            return {"conversation": get(base), "items": items}
        except httpx.TimeoutException:
            # A slow read is not a missing conversation: poll again until the deadline decides.
            return None

    return _poll(
        read,
        lambda doc: doc is not None and all(contains(doc["items"], a) for a in anchors),
        _DB_TIMEOUT_SEC,
        f"conversation {conversation_id} read-back",
    )


def read_langfuse_session(
    langfuse: Any,
    conversation_id: str,
    anchors: Sequence[str],
    *,
    allow_empty: bool = False,
) -> list[dict[str, Any]] | None:
    """Every trace of the session with its observations, once every turn's anchor shows up.

    ``langfuse`` is an ``HttpxLangfuseClient``. ``allow_empty`` is for a rejected turn, which
    may export no trace; it then returns ``None`` after the timeout.
    """
    if langfuse is None:
        raise SinkUnavailableError("no Langfuse client: set LANGFUSE_PUBLIC_KEY / LANGFUSE_SECRET_KEY")
    timeout_sec = float(os.environ.get(_LANGFUSE_TIMEOUT_ENV) or _DEFAULT_LANGFUSE_TIMEOUT_SEC)
    timed_out = 0

    def read() -> list[dict[str, Any]]:
        nonlocal timed_out
        try:
            return [langfuse.get_trace(trace_id) for trace_id in langfuse.session_trace_ids(conversation_id)]
        except httpx.TimeoutException:
            # A slow read is not a missing trace: poll again until the deadline decides.
            timed_out += 1
            return []
        except httpx.HTTPError as exc:
            raise _LangfuseReadError(f"Langfuse session {conversation_id}: {exc}") from exc
        except (ValueError, LookupError, TypeError) as exc:
            # A body that is not JSON, a row without an id, a listing past its page cap: read, but
            # not readable.
            raise _LangfuseReadError(f"Langfuse session {conversation_id}: unreadable response ({exc!r})") from exc

    def done(traces: list[dict[str, Any]]) -> bool:
        return bool(traces) and all(contains(traces, a) for a in anchors)

    try:
        # Latency and cost keep updating on a finished trace, so "settled" means no new trace
        # and no new observation since the last read.
        return _poll(
            read,
            done,
            timeout_sec,
            f"Langfuse session {conversation_id}",
            shape=lambda traces: [(t.get("id"), len(t.get("observations") or [])) for t in traces],
        )
    except _LangfuseReadError:
        # A failed read says nothing about the export: never "no trace", never "none expected".
        raise
    except SinkUnavailableError as exc:
        if allow_empty:
            return None
        slow = f" ({timed_out} read(s) timed out)" if timed_out else ""
        raise TraceNotFoundError(
            f"{TRACE_NOT_FOUND}: no Langfuse trace for session {conversation_id} after {timeout_sec:.0f}s{slow}"
        ) from exc

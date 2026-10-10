# (C) 2026 GoodData Corporation
"""One eval item's Langfuse experiment scope, carried to gen-ai as W3C baggage.

With ``GOODDATA_EVAL_JOIN_GENAI_TRACE`` on, every chat request of an item tells gen-ai which
trace and parent to open its spans under, and which experiment item they belong to. gen-ai
then builds its turn inside gd-eval's experiment trace instead of a trace of its own, and
gd-eval exports the matching root span afterwards.

The trace id and the root span id are derived from the conversation id, so the sender and
the deferred scorer (which runs on another thread, with no access to the sender's context)
agree on them without passing anything between threads.
"""

from __future__ import annotations

import contextvars
import hashlib
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import quote

from gooddata_eval.core.config import env_flag
from gooddata_eval.core.langfuse.experiment import experiment_id_for

JOIN_ENV_VAR = "GOODDATA_EVAL_JOIN_GENAI_TRACE"

# The environment the langfuse SDK forces on every span that carries the root-observation
# baggage key. gd-eval's root must use the same one, or Langfuse splits the trace.
SDK_EXPERIMENT_ENVIRONMENT = "sdk-experiment"

TRACE_ID_KEY = "langfuse_trace_id"
ROOT_OBSERVATION_ID_KEY = "langfuse_experiment_item_root_observation_id"
EXPERIMENT_ID_KEY = "langfuse_experiment_id"
EXPERIMENT_NAME_KEY = "langfuse_experiment_name"
EXPERIMENT_DATASET_ID_KEY = "langfuse_experiment_dataset_id"
EXPERIMENT_ITEM_ID_KEY = "langfuse_experiment_item_id"


def join_enabled() -> bool:
    return env_flag(JOIN_ENV_VAR)


@dataclass(frozen=True)
class ItemTraceScope:
    """What every run of one dataset item needs to join its Langfuse experiment.

    ``run_metadata`` rides along so the deferred scorer reuses the name resolved before
    the run instead of resolving it again (an unpinned run timestamp would differ).
    """

    base_name: str
    suffix_runs: bool
    dataset_id: str
    item_id: str
    run_metadata: dict[str, Any] = field(default_factory=dict, compare=False)

    def run_name(self, run_idx: int) -> str:
        """Same rule as ``RunTraceContext.run_name``."""
        return f"{self.base_name}_run{run_idx}" if self.suffix_runs else self.base_name


_SCOPE: contextvars.ContextVar[ItemTraceScope | None] = contextvars.ContextVar("gd_eval_item_scope", default=None)


@contextmanager
def item_scope(scope: ItemTraceScope | None) -> Iterator[None]:
    """Make ``scope`` the current item's scope for the duration of the block. None is a no-op."""
    if scope is None:
        yield
        return
    token = _SCOPE.set(scope)
    try:
        yield
    finally:
        _SCOPE.reset(token)


def current_scope() -> ItemTraceScope | None:
    """The scope of the item running on this thread, or None when joining is off."""
    return _SCOPE.get() if join_enabled() else None


def trace_ids_for(conversation_id: str) -> tuple[str, str]:
    """``(trace_id, root_span_id)`` for a conversation: 32 and 16 lowercase hex, both nonzero.

    The trace id is the langfuse SDK's ``create_trace_id(seed=conversation_id)``. The span id
    is hashed from a different seed, because the SDK's observation-id recipe on the same seed
    would just be the trace id's first half.
    """
    trace_id = hashlib.sha256(conversation_id.encode("utf-8")).digest()[:16].hex()
    span_id = hashlib.sha256(f"{conversation_id}:root".encode()).digest()[:8].hex()
    # An all-zero id is invalid in OTel; a sha256 prefix is never zero in practice.
    return trace_id if int(trace_id, 16) else "0" * 31 + "1", span_id if int(span_id, 16) else "0" * 15 + "1"


def baggage_entries(scope: ItemTraceScope, run_name: str, conversation_id: str) -> list[str]:
    """The W3C baggage members that put one run's gen-ai spans under its experiment item."""
    trace_id, span_id = trace_ids_for(conversation_id)
    return [
        f"{TRACE_ID_KEY}={trace_id}",
        f"{ROOT_OBSERVATION_ID_KEY}={span_id}",
        f"{EXPERIMENT_ID_KEY}={experiment_id_for(run_name)}",
        f"{EXPERIMENT_NAME_KEY}={quote(run_name, safe='')}",
        f"{EXPERIMENT_DATASET_ID_KEY}={quote(scope.dataset_id, safe='')}",
        f"{EXPERIMENT_ITEM_ID_KEY}={quote(scope.item_id, safe='')}",
    ]


@dataclass(frozen=True)
class JoinedRun:
    """The experiment a joined conversation's gen-ai spans were told they belong to."""

    run_name: str
    dataset_id: str


# Conversations whose gen-ai turns reported the trace id gd-eval asked for, with the number of
# such turns. Process-wide: written by the item thread that sent the turn, read by the
# trace-link thread that scores it, and released once the conversation's root is exported.
_JOINED: dict[str, tuple[JoinedRun, int]] = {}
_JOINED_LOCK = threading.Lock()


def mark_joined(conversation_id: str, run: JoinedRun) -> None:
    """Record one more turn of ``conversation_id`` that gen-ai put in the requested trace."""
    with _JOINED_LOCK:
        turns = _JOINED.get(conversation_id, (run, 0))[1]
        _JOINED[conversation_id] = (run, turns + 1)


def joined_run(conversation_id: str | None) -> JoinedRun | None:
    if not conversation_id:
        return None
    with _JOINED_LOCK:
        entry = _JOINED.get(conversation_id)
    return entry[0] if entry else None


def joined_turns(conversation_id: str) -> int:
    """How many of the conversation's turns gen-ai reported in the requested trace."""
    with _JOINED_LOCK:
        entry = _JOINED.get(conversation_id)
    return entry[1] if entry else 0


def release_joined(conversation_id: str) -> None:
    with _JOINED_LOCK:
        _JOINED.pop(conversation_id, None)

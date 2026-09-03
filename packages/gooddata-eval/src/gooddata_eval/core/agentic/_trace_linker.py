# (C) 2026 GoodData Corporation. All rights reserved.
"""Runs Langfuse trace lookup and scoring off the evaluation's critical path.

Polling for a gen-ai trace waits on Langfuse ingestion and produces no pass/fail verdict,
so charging it to the item's latency both slows the run and misreports the agent's own
response time. ``run_trace_link_inline`` (the default) stays synchronous so direct callers
behave exactly as before; the CLI runner injects a ``BackgroundTraceLinker`` and drains it
before any report is rendered, so scores are still final before the command finishes.
"""

from __future__ import annotations

import contextvars
import logging
import threading
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Protocol

from gooddata_eval.core._output import emit_line

_log = logging.getLogger(__name__)

# A unit of deferred Langfuse work: find the traces for one item's conversations and
# write its scores. Takes no arguments and returns nothing -- each evaluate_agentic_*
# closes over whatever its own scoring needs.
TraceLinkTask = Callable[[], None]


class SubmitTraceLink(Protocol):
    """How an ``evaluate_agentic_*`` hands its Langfuse block off.

    ``item_id`` is only used for attributing the task's cost and naming it in warnings;
    the task itself already closes over everything it needs.
    """

    def __call__(self, task: TraceLinkTask, *, item_id: str = "") -> None: ...


# A trace poll is almost entirely waiting on ingestion, so the queue is run as wide as it
# gets, bounded only so a huge dataset cannot open a thread per item.
_MAX_WORKERS = 16


def warn_from_worker(message: str) -> None:
    """Write one warning line to stdout, safe to call from a linking worker."""
    emit_line(message)


# True only while a linking task runs on its caller's critical path -- the only thing that
# separates the two retry budgets in _langfuse: a batched poll blocks nobody and can wait
# minutes, an inline one is charged to whoever called evaluate_agentic_*. A ContextVar, not
# a flag, because worker threads start with a fresh context: the batched pool reads False
# for free, and the inline case is scoped to exactly the call that set it.
_INLINE_LINKING: contextvars.ContextVar[bool] = contextvars.ContextVar("gd_eval_inline_trace_link", default=False)


def linking_is_inline() -> bool:
    """Whether the trace poll running right now sits on its caller's critical path."""
    return _INLINE_LINKING.get()


def run_trace_link_inline(task: TraceLinkTask, *, item_id: str = "") -> None:
    """Run the linking task on the calling thread -- the default for every evaluate_agentic_*.

    ``linking_is_inline`` keeps this path on the smaller, pre-batching retry budget.
    """
    token = _INLINE_LINKING.set(True)
    try:
        task()
    finally:
        _INLINE_LINKING.reset(token)


# The signal a running batched poll watches to stop sleeping, visible only on the worker
# thread running that poll: BackgroundTraceLinker._run sets it for the task's duration. A
# ContextVar rather than a module global, for the same reason as _INLINE_LINKING: the inline
# path never sets it, so nobody can cancel a poll charged to its own caller, and an
# interrupted drain's set Event lives on with exactly the workers it was meant for -- there is
# no shared slot for it to linger in and stop the next --model pass or a later inline link.
_CANCEL: contextvars.ContextVar[threading.Event | None] = contextvars.ContextVar(
    "gd_eval_trace_link_cancel", default=None
)


def link_cancel_event() -> threading.Event | None:
    """The cancellation signal for the batched poll running on this thread, or None."""
    return _CANCEL.get()


def utc_now() -> datetime:
    """Now, in UTC. One spelling, so a pinned trace window cannot drift by timezone."""
    return datetime.now(timezone.utc)


def open_trace_window(langfuse: Any) -> tuple[Any, datetime]:
    """Resolve the Langfuse client for this item and pin the start of its trace window.

    The client falls back to the ambient LANGFUSE_* credentials, so direct library and
    tavern callers still link traces without being handed one. ``window_start`` is taken
    before the agent runs, so the window brackets exactly this item's conversations.
    """
    from gooddata_eval.core.agentic._langfuse import try_make_langfuse_client  # noqa: PLC0415

    return (try_make_langfuse_client() if langfuse is None else langfuse), utc_now()


@dataclass(frozen=True)
class RunIdentity:
    """Everything ``build_run_context`` needs to name and describe one eval run.

    Built on the calling thread and captured by value, so a deferred task never reaches
    back into the evaluation's own objects to resolve a name.
    """

    host: str
    token: str
    workspace_id: str
    dataset_name: str
    run_timestamp: str | None
    model_version_override: str | None
    run_metadata_extra: dict | None
    reasoning_effort: Any


@dataclass(frozen=True)
class RunTraceContext:
    """One item's resolved Langfuse run identity, its traces, and how to score them.

    Carries the ``_langfuse`` module and the client so a kind's scoring body needs neither
    -- otherwise all eight repeat the same deferred import and thread ``langfuse`` and
    ``dataset_item_id`` through every call.
    """

    run_metadata: dict
    _lf: Any
    _client: Any
    _dataset_item_id: str
    _base_name: str
    _suffix_runs: bool
    _traces: dict[str, Any]

    def run_name(self, run_idx: int) -> str:
        """Dataset-run name for one run, suffixed only when the item has more than one."""
        return f"{self._base_name}_run{run_idx}" if self._suffix_runs else self._base_name

    def trace(self, conversation_id: str) -> Any:
        """The trace picked for a conversation, or None when the poll never found one."""
        return self._traces.get(conversation_id)

    def observe(self, trace: Any, run_idx: int) -> Any:
        """Attach this run to its dataset-run item, yielding the trace id to score against.

        ``trace`` may be None -- a conversation whose trace never showed up is still
        observed, so the run appears in the experiment with its scores orphaned rather than
        missing entirely.
        """
        return self._lf.observe(
            self._client,
            trace.id if trace else None,
            self._dataset_item_id,
            self.run_name(run_idx),
            self.run_metadata,
        )

    def score(self, trace_id: Any, *, name: str, value: Any, data_type: str) -> None:
        """Write one score, swallowing Langfuse failures the way ``score_safe`` always has."""
        self._lf.score_safe(self._client, trace_id, name=name, value=value, data_type=data_type)

    def quality(self, trace_id: Any, *, strict_checks: dict, latency_sec: Any, cost_usd: Any) -> None:
        """Write the derived quality/value scores for one run."""
        self._lf.log_quality_and_value_scores(
            self._client, trace_id, strict_checks=strict_checks, latency_sec=latency_sec, cost_usd=cost_usd
        )


def submit_trace_scoring(
    submit_trace_link: SubmitTraceLink,
    identity: RunIdentity,
    *,
    langfuse: Any,
    dataset_item_id: str,
    conversation_ids: list[str],
    window_start: datetime,
    window_end: datetime,
    suffix_runs: bool,
    write_scores: Callable[[RunTraceContext], None],
) -> None:
    """Defer one item's whole Langfuse block: resolve its run context, then write scores.

    Deferred as a unit because ``build_run_context``'s workspace lookup and
    ``find_traces_per_conversation``'s ingestion-lag poll are both round trips publishing an
    already-decided verdict, so neither belongs on the item's clock. Every caller pins
    ``window_end`` before calling: a deferred poll must not widen its own query window.
    """

    def _link_traces() -> None:
        from gooddata_eval.core.agentic import _langfuse  # noqa: PLC0415

        base_name, run_metadata = _langfuse.build_run_context(
            identity.host,
            identity.token,
            identity.workspace_id,
            identity.dataset_name,
            identity.run_timestamp,
            identity.model_version_override,
            identity.run_metadata_extra,
            identity.reasoning_effort,
        )
        traces = _langfuse.find_traces_per_conversation(langfuse, conversation_ids, window_start, window_end)
        write_scores(
            RunTraceContext(run_metadata, _langfuse, langfuse, dataset_item_id, base_name, suffix_runs, traces)
        )

    submit_trace_link(_link_traces, item_id=dataset_item_id)


class BackgroundTraceLinker:
    """Collects trace-linking tasks during the run and executes them all at ``drain``.

    Batched, not fired on submit: Langfuse ingestion lags by tens of seconds to minutes, so
    a poll issued the instant its conversation ended is the one least likely to find
    anything. Holding the queue until the agent phase ends gives every trace the length of
    the run to appear. Task failures are logged and swallowed -- a Langfuse outage has never
    been allowed to fail an eval run.
    """

    def __init__(self, max_workers: int = _MAX_WORKERS, clock: Callable[[], float] = time.monotonic) -> None:
        self._max_workers = max_workers
        self._clock = clock
        self._queue: list[tuple[TraceLinkTask, str]] = []
        self.durations: dict[str, float] = {}
        # The drain in flight's signal, so abandon() can reach its workers.
        self._cancel: threading.Event | None = None

    def submit(self, task: TraceLinkTask, *, item_id: str = "") -> None:
        """Queue the task. Nothing runs until ``drain``."""
        self._queue.append((task, item_id))

    @property
    def pending(self) -> int:
        """How many links are queued and waiting for ``drain``."""
        return len(self._queue)

    def _run(self, task: TraceLinkTask, item_id: str, cancel: threading.Event) -> None:
        # Runs on the worker thread, so this scopes the signal to exactly this task: a worker
        # still polling after drain() has raised keeps reading the same (set) event, and
        # nothing outside the pool ever sees it.
        token = _CANCEL.set(cancel)
        started = self._clock()
        try:
            task()
        except Exception as exc:
            _log.warning("Langfuse trace linking failed for item %s: %s", item_id or "?", exc)
            warn_from_worker(f"warning: Langfuse trace linking failed for item '{item_id}': {exc}")
        finally:
            # Recorded on the failure path too: an item whose poll exhausted its budget and
            # then errored is precisely the one whose Langfuse cost the report should show.
            self.durations[item_id] = self._clock() - started
            _CANCEL.reset(token)

    def drain(self) -> None:
        """Run every queued link in parallel and wait for the batch to finish."""
        queue, self._queue = self._queue, []
        if not queue:
            return
        # NOT a `with` block, for the same reason the item pool in cli/agentic_runner.py is
        # not: __exit__ is shutdown(wait=True) with cancel_futures left False, so a Ctrl-C
        # mid-batch would run every QUEUED poll -- almost entirely time.sleep -- to
        # completion first. abandon() cannot help here (the queue moved into `queue` above),
        # so the cancellation has to happen on the pool itself.
        pool = ThreadPoolExecutor(max_workers=min(len(queue), self._max_workers), thread_name_prefix="trace-link")
        cancel = threading.Event()
        self._cancel = cancel
        try:
            for task, item_id in queue:
                pool.submit(self._run, task, item_id, cancel)
            pool.shutdown(wait=True)
        except BaseException:
            # Signalled BEFORE the shutdown: cancel_futures only drops what has not started,
            # and a poll already running sits in a backoff sleep until its deadline -- which
            # the interpreter then waits out, because it joins executor workers at exit. So a
            # Ctrl-C could hang for the whole batch budget. This wakes them instead.
            cancel.set()
            pool.shutdown(wait=False, cancel_futures=True)
            raise
        finally:
            self._cancel = None

    def abandon(self) -> None:
        """Discard the queue without running it.

        For the interrupt path: nothing has started yet, so Ctrl-C costs nothing rather
        than making the user sit through a batch of retrying polls.
        """
        self._queue.clear()
        if self._cancel is not None:
            # Only when a drain is in flight on another thread; harmless then too.
            self._cancel.set()

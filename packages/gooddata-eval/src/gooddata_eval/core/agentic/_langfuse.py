# (C) 2026 GoodData Corporation. All rights reserved.
"""Shared Langfuse helpers for agentic evaluation runners."""

from __future__ import annotations

import logging
import os
import threading
import time
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from typing import Any

from gooddata_eval.core.agentic._trace_linker import link_cancel_event, linking_is_inline, warn_from_worker
from gooddata_eval.core.config import ReasoningEffort, env_flag, normalize_reasoning_effort
from gooddata_eval.core.langfuse._env import credentials_present
from gooddata_eval.core.langfuse.client import HttpxLangfuseClient
from gooddata_eval.core.langfuse.experiment import (
    ExperimentItem,
    ExperimentRun,
    ScoreTarget,
    build_experiment_root_span,
)

# Part of this module's public surface: external callers import both names from here.
from gooddata_eval.core.langfuse.observations import TraceSummary as _TraceObj  # noqa: F401
from gooddata_eval.core.langfuse.otlp import Span

_log = logging.getLogger(__name__)


def make_langfuse_client() -> HttpxLangfuseClient:
    """Create a Langfuse client from standard env vars. No external SDK required."""
    return HttpxLangfuseClient()


def langfuse_credentials_present() -> bool:
    """Whether the environment could build a Langfuse client.

    Separate from ``try_make_langfuse_client`` so a caller can ask the question without
    opening an httpx client it does not intend to use.
    """
    return credentials_present()


def try_make_langfuse_client() -> HttpxLangfuseClient | None:
    """Create Langfuse client from env vars; return None if credentials are missing."""
    try:
        return make_langfuse_client()
    except RuntimeError:
        return None


# ---------------------------------------------------------------------------

SKIP_ENV_VAR = "TAVERN_E2E_SKIP_TRACE_LINK"

# Run names whose experiment assembly has already been reported as impossible. A 404 from
# dataset-items means the dataset item id is not in Langfuse, which is a property of the
# dataset and not of the attempt -- so it recurs identically for every item and every run
# of that dataset, and reporting it per conversation buries the run's real output under
# dozens of copies of the same HTTP error. Guarded by a lock because linking runs on the
# drain pool's worker threads.
_UNLINKABLE_RUNS: set[str] = set()
_UNLINKABLE_RUNS_LOCK = threading.Lock()


def _first_report_for_run(run_name: str) -> bool:
    """True the first time this run is seen, False afterwards. Thread-safe."""
    # A run is suffixed _run0.._runK per K, one per pass over the same dataset; the cause
    # is shared across all of them, so collapse to the base name.
    base = run_name.rsplit("_run", 1)[0]
    with _UNLINKABLE_RUNS_LOCK:
        if base in _UNLINKABLE_RUNS:
            return False
        _UNLINKABLE_RUNS.add(base)
        return True


_MAX_LATENCY_SEC = 60.0
_MAX_COST_USD = 0.05
_QUALITY_WEIGHT = 0.6
_SPEED_WEIGHT = 0.2
_COST_WEIGHT = 0.2

_INITIAL_DELAY = 0.5
_BACKOFF = 1.6
# Ceiling on any single backoff sleep, so a long budget is spent on many steady retries
# rather than one enormous final wait.
_MAX_DELAY = 15.0
# Budget for one item's batched poll, which blocks nobody. Sized against Langfuse ingestion
# lag on us.cloud, which runs from tens of seconds to several minutes. Shared across the
# item's conversations, so the batch tail does not grow with --runs.
_LINK_BUDGET_SEC = 120.0
# Budget for a poll that is NOT batched: a direct library caller (the tavern e2e suite) gets
# run_trace_link_inline, so the wait lands on the test that triggered it, under a step
# timeout. Deliberately tighter than _LINK_BUDGET_SEC: no inline caller should pay for a
# budget sized for the CLI's batched tail.
_INLINE_LINK_BUDGET_SEC = 35.0
# Sanity bound so the retry loop can never spin: the deadline is wall-clock and only the
# sleeps advance it. Comfortably above the ~12 attempts the budget actually affords.
_MAX_ATTEMPTS = 20
_WINDOW_PADDING_SEC = 2
_FETCH_LIMIT = 100


def get_model_version(
    host: str,
    token: str,
    workspace_id: str,
    override: str | None = None,
) -> str:
    """Return model version: explicit override > workspace active LLM provider."""
    if override:
        return override
    try:
        from gooddata_sdk import GoodDataSdk  # noqa: PLC0415

        sdk = GoodDataSdk.create(host, token)
        setting = sdk.catalog_workspace.get_workspace_setting(workspace_id, "activeLlmProvider")
        model = (setting.content or {}).get("defaultModelId") or None
        if model:
            return model
    except Exception:
        pass
    return ""


def _matches_session(trace: Any, session_id: str) -> bool:
    """Whether a trace belongs to the conversation, by sessionId or by its metadata."""
    sid = getattr(trace, "session_id", None)
    if isinstance(sid, str) and sid == session_id:
        return True
    metadata = getattr(trace, "metadata", None)
    return isinstance(metadata, dict) and metadata.get("conversation_id") == session_id


def _fetch_traces_for_session(
    langfuse: Any,
    session_id: str,
    window_start: datetime,
    window_end: datetime,
    pad: timedelta,
) -> list[Any]:
    """Fetch traces filtered by sessionId (gen-ai sets sessionId = conversationId)."""
    kwargs: dict[str, Any] = {
        "from_timestamp": window_start - pad,
        "to_timestamp": window_end + pad,
        "limit": _FETCH_LIMIT,
    }
    # Langfuse v4+ SDKs and the httpx client take session_id as a server-side filter; older
    # SDKs do not, and then the page is the whole window.
    try:
        import inspect  # noqa: PLC0415

        sig = inspect.signature(langfuse.api.trace.list)
        if "session_id" in sig.parameters:
            kwargs["session_id"] = session_id
    except Exception:
        pass
    response = langfuse.api.trace.list(**kwargs)
    # A post-check, not a fallback: the Langfuse API drops a query parameter it does not know
    # rather than rejecting it, and an unfiltered page would hand the caller's max-latency
    # pick a stranger's trace with no warning. On a server that did filter it is a no-op.
    return [t for t in (response.data or []) if _matches_session(t, session_id)]


# Longest a running poll may stay asleep after cancellation is signalled. Without a bound,
# a Ctrl-C mid-drain waits out the rest of that poll's backoff -- up to _MAX_DELAY per sleep
# and _LINK_BUDGET_SEC overall -- because the interpreter joins executor workers at exit.
_CANCEL_CHECK_SEC = 0.5


def _wait_between_attempts(delay: float) -> bool:
    """Wait ``delay`` before the next poll attempt. False means "stop polling".

    Outside a batched drain nobody can cancel the wait -- an inline poll is charged to the
    caller that asked for it -- so it stays a single sleep. Inside a drain the wait is served
    in slices, so an interrupt is noticed within ``_CANCEL_CHECK_SEC`` rather than after the
    whole backoff. Slicing keeps the total unchanged, so the retry ladder is unaffected.
    """
    cancel = link_cancel_event()
    if cancel is None:
        time.sleep(delay)
        return True
    remaining = delay
    while remaining > 0:
        if cancel.is_set():
            return False
        step = min(_CANCEL_CHECK_SEC, remaining)
        time.sleep(step)
        remaining -= step
    return not cancel.is_set()


def find_traces_per_conversation(
    langfuse: Any,
    conversation_ids: list[str],
    window_start: datetime,
    window_end: datetime | None = None,
    deadline: float | None = None,
) -> dict[str, Any]:
    """Poll Langfuse until traces matching all conversation_ids are found or retries exhaust.

    ``window_end`` bounds the trace query and should be pinned by the caller to the moment
    the conversations ended. It matters because this poll is normally deferred onto a
    worker thread (see ``agentic/_trace_linker.py``): defaulting it to "now" would stretch
    the window by however long the task waited in the queue, and the reader pages at 500
    rows over at most four pages and then keeps the newest ``_FETCH_LIMIT`` traces of what
    that returns, so a wide enough window can push the wanted trace off the page. Defaults
    to now only for direct callers that poll immediately.
    """
    if env_flag(SKIP_ENV_VAR):
        # The one place the switch is announced: ``observe`` also honours it but stays
        # silent, so a run says once that its Langfuse work was turned off rather than
        # once per item. Left unsaid entirely, an eval run with no scores looks like
        # Langfuse is broken.
        warn_from_worker(
            f"[langfuse] trace linking SKIPPED by {SKIP_ENV_VAR}: "
            f"{len(conversation_ids)} conversation(s) will not be linked or scored in Langfuse. "
            f"Unset it to link traces."
        )
        return dict.fromkeys(conversation_ids)

    by_conv: dict[str, Any] = dict.fromkeys(conversation_ids)
    window_end = window_end or datetime.now(timezone.utc)
    pad = timedelta(seconds=_WINDOW_PADDING_SEC)

    # One budget for the whole item. Per conversation it would multiply by --runs, and the
    # batch tail is meant to be bounded by the budget however many runs an item has.
    budget = _INLINE_LINK_BUDGET_SEC if linking_is_inline() else _LINK_BUDGET_SEC
    stop_at = deadline if deadline is not None else time.monotonic() + budget

    for cid in conversation_ids:
        cancel = link_cancel_event()
        if cancel is not None and cancel.is_set():
            # The run is being interrupted; the remaining conversations are not worth a
            # round trip, and their scores were never going to be written.
            break
        delay = _INITIAL_DELAY
        found: list[Any] = []
        for _attempt in range(_MAX_ATTEMPTS):
            # Attempt first, sleep only between attempts: a trace that is already ingested
            # when we look must cost nothing, which is the common case once linking is
            # batched to the end of the run.
            try:
                found = _fetch_traces_for_session(langfuse, cid, window_start, window_end, pad)
            except Exception as exc:
                _log.debug("Langfuse trace fetch failed for %s: %s", cid, exc)
            if found or time.monotonic() + delay > stop_at:
                break
            if not _wait_between_attempts(delay):
                break
            delay = min(delay * _BACKOFF, _MAX_DELAY)
        if found:
            by_conv[cid] = max(found, key=lambda t: getattr(t, "latency", None) or 0.0)
        else:
            _log.warning(
                "[langfuse] No trace found for conversation %s in window [%s, %s]", cid, window_start, window_end
            )
            warn_from_worker(f"[langfuse] WARNING: no trace found for conversation {cid}")

    return by_conv


def _span_window(trace: Any, window: tuple[datetime, datetime] | None) -> tuple[datetime, datetime]:
    """When gd-eval's span starts and ends: the gen-ai turn it describes, else the item's
    trace window, else this instant.

    The only clock read on the linking path, and deliberately here rather than in the
    deferred task, whose run time says nothing about when the agent answered.
    """
    start = getattr(trace, "start_time", None)
    end = getattr(trace, "end_time", None)
    if start is not None and end is not None:
        return start, end
    if window is not None:
        return window
    now = datetime.now(timezone.utc)
    return now, now


def _experiment_root_span(
    trace_id: str | None,
    dataset_item_id: str,
    dataset_id: str,
    run_name: str,
    run_metadata: dict[str, Any],
    *,
    trace: Any,
    window: tuple[datetime, datetime] | None,
    conversation_id: str | None,
    item_input: Any,
    output: Any,
) -> Span:
    """gd-eval's own root span for one (dataset item, run) -- the whole experiment item."""
    start, end = _span_window(trace, window)
    session_id = conversation_id or getattr(trace, "session_id", None)
    tags = tuple(tag for tag in ("gd-eval", run_metadata.get("testing_framework")) if tag)
    return build_experiment_root_span(
        ExperimentRun(run_name, dataset_id, run_metadata or None),
        ExperimentItem(
            dataset_item_id,
            input={"question": item_input} if item_input is not None else {"dataset_item_id": dataset_item_id},
            output=output,
        ),
        start=start,
        end=end,
        # Never the gen-ai trace's own name: the two traces sit side by side in Langfuse and
        # only the prefix says which of them gd-eval wrote.
        trace_name=f"gd-eval: {str(item_input)[:80]}" if item_input else f"gd-eval: {dataset_item_id}",
        session_id=session_id,
        version=run_metadata.get("model_version"),
        tags=tags,
        observation_metadata={
            "gen_ai_trace_id": trace_id,
            "gen_ai_latency_s": getattr(trace, "latency", None),
            "gen_ai_cost_usd": getattr(trace, "total_cost", None),
            "conversation_id": session_id,
        },
        trace_metadata={"dataset_name": run_metadata.get("dataset_name"), "run_name": run_name},
        environment=os.environ.get("LANGFUSE_TRACING_ENVIRONMENT"),
    )


@contextmanager
def observe(
    langfuse: Any,
    trace_id: str | None,
    dataset_item_id: str,
    run_name: str,
    run_metadata: dict[str, Any] | None = None,
    *,
    trace: Any = None,
    window: tuple[datetime, datetime] | None = None,
    conversation_id: str | None = None,
    item_input: Any = None,
    output: Any = None,
) -> Iterator[ScoreTarget | None]:
    """Export gd-eval's experiment root span for one run and yield where to score it.

    A run belongs to a Langfuse experiment through the attributes on that span, so the span
    IS the run item. The yielded target names both the gen-ai trace and the span; either
    half may be missing, and ``score_safe`` writes to whichever are there.
    """
    fallback = ScoreTarget(trace_id) if trace_id else None
    # isinstance, not hasattr: a MagicMock answers every attribute, and the skill suites
    # hand this one exactly that.
    if not isinstance(langfuse, HttpxLangfuseClient):
        yield fallback
        return

    # The operational off-switch for the whole agentic Langfuse write path, so it has to
    # cover the span export and the scores as well as the poll that already announced it.
    # Yielding None rather than the trace id is what stops ``score_safe`` writing: the
    # flag is also how an operator gets through a run with Langfuse unreachable, and a
    # score write would then fail per item.
    if env_flag(SKIP_ENV_VAR):
        yield None
        return

    try:
        dataset_id = langfuse.dataset_id_for_item(dataset_item_id)
    except Exception as exc:
        _log.warning("Failed to resolve dataset item %s for run %s: %s", dataset_item_id, run_name, exc)
        warn_from_worker(
            f"[langfuse] WARNING: failed to resolve dataset item {dataset_item_id!r} for run {run_name!r}: {exc}"
        )
        yield fallback
        return

    if dataset_id is None:
        if _first_report_for_run(run_name):
            # Say what it means and what to do, once. A raw 404 names an endpoint, which
            # tells the reader nothing about the cause being their --dataset.
            _log.warning("Dataset item %s is not in Langfuse; run %s cannot be assembled.", dataset_item_id, run_name)
            warn_from_worker(
                f"[langfuse] WARNING: dataset item {dataset_item_id!r} does not exist in Langfuse, "
                f"so the run {run_name!r} cannot be assembled (404 from dataset-items). "
                f"Scores ARE still written to the traces themselves -- only the per-run grouping "
                f"used to compare models is missing. This is what happens when --dataset points at "
                f"a local folder: its item ids are local, not Langfuse dataset item ids. Use "
                f"--langfuse-dataset to get comparable runs, or set {SKIP_ENV_VAR}=1 to skip linking "
                f"altogether. Further occurrences for this run are suppressed."
            )
        yield fallback
        return

    span = _experiment_root_span(
        trace_id,
        dataset_item_id,
        dataset_id,
        run_name,
        run_metadata or {},
        trace=trace,
        window=window,
        conversation_id=conversation_id,
        item_input=item_input,
        output=output,
    )
    try:
        langfuse.export_spans([span])
    except Exception as exc:
        _log.warning("Failed to export the experiment span for run %s: %s", run_name, exc)
        warn_from_worker(
            f"[langfuse] WARNING: failed to export experiment span run={run_name} item={dataset_item_id}: {exc}"
        )
        yield fallback
        return

    if trace_id is None:
        _log.warning(
            "No gen-ai trace found for dataset run %s; scores go to the gd-eval experiment span only.", run_name
        )
    yield ScoreTarget(trace_id, span.trace_id, span.span_id)


def score_safe(langfuse: Any, trace_id: Any, **kwargs: Any) -> None:
    """Create one Langfuse score per destination the target names, ignoring errors.

    ``observation_id`` is sent only for the experiment span, so the gen-ai write stays the
    call every client already accepts.
    """
    if not trace_id:
        return
    targets = trace_id.destinations() if isinstance(trace_id, ScoreTarget) else [(str(trace_id), None)]
    for target_id, observation_id in targets:
        extra = {"observation_id": observation_id} if observation_id else {}
        try:
            langfuse.create_score(trace_id=target_id, **kwargs, **extra)
        except Exception as exc:
            _log.warning("Failed to log score %s: %s", kwargs.get("name"), exc)


def log_quality_and_value_scores(
    langfuse: Any,
    trace_id: str | None,
    strict_checks: dict[str, bool],
    latency_sec: float | None = None,
    cost_usd: float | None = None,
) -> None:
    """Log composite quality_score and value_score to Langfuse."""
    if not strict_checks or not trace_id:
        return
    passed = sum(1 for v in strict_checks.values() if v)
    total = len(strict_checks)
    quality = passed / total
    score_safe(
        langfuse,
        trace_id,
        name="quality_score",
        value=quality,
        data_type="NUMERIC",
        comment=f"{passed}/{total} strict checks passed",
    )
    speed = 0.0 if latency_sec is None else max(0.0, 1.0 - latency_sec / _MAX_LATENCY_SEC)
    cost_factor = 0.0 if cost_usd is None else max(0.0, 1.0 - cost_usd / _MAX_COST_USD)
    value = _QUALITY_WEIGHT * quality + _SPEED_WEIGHT * speed + _COST_WEIGHT * cost_factor
    latency_str = "unknown" if latency_sec is None else f"{latency_sec:.2f}s"
    cost_str = "unknown" if cost_usd is None else f"${cost_usd:.4f}"
    score_safe(
        langfuse,
        trace_id,
        name="value_score",
        value=value,
        data_type="NUMERIC",
        comment=(
            f"{_QUALITY_WEIGHT}*quality({quality:.2f}) + "
            f"{_SPEED_WEIGHT}*speed({speed:.2f}) + "
            f"{_COST_WEIGHT}*cost({cost_factor:.2f}); "
            f"latency={latency_str}; cost={cost_str}"
        ),
    )


def build_run_context(
    host: str,
    token: str,
    workspace_id: str,
    dataset_name: str,
    run_timestamp: str | None,
    model_version_override: str | None,
    run_metadata_extra: dict[str, Any] | None = None,
    reasoning_effort: ReasoningEffort | None = None,
) -> tuple[str, dict[str, Any]]:
    """Return (run_name_base, run_metadata) with model version resolved from workspace API.

    Args:
        host: GoodData host URL.
        token: API token used to resolve the workspace model version.
        workspace_id: Workspace whose active LLM provider is read when no override is given.
        dataset_name: Langfuse dataset name; used as the run-name prefix.
        run_timestamp: Shared run timestamp for the run name (falls back to the current time).
        model_version_override: Explicit model-version tag; when set it wins over the
            workspace lookup.
        run_metadata_extra: Optional extra key/values added to the dataset-run metadata
            (e.g. a testing-framework tag or a CI run id for scoping). Default None keeps
            behavior unchanged. The SDK-derived model_version is applied last and cannot
            be overwritten by this dict.
        reasoning_effort: Effort the run requested, stamped into both the run name and
            the metadata so effort-varying runs stay comparable side by side.
    """
    effort = normalize_reasoning_effort(reasoning_effort)
    model = get_model_version(host, token, workspace_id, model_version_override)
    ts = run_timestamp or datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base = f"{dataset_name}_{ts}"
    if model:
        base = f"{base}_{model}"
    # Part of the run name, not just metadata: two runs that differ only by effort would
    # otherwise collide on the same name and be indistinguishable in the report.
    if effort:
        base = f"{base}_effort-{effort.lower()}"
    # Caller supplies its own run tags (e.g. testing_framework); model_version is applied
    # last so the SDK-derived value cannot be overwritten by run_metadata_extra.
    metadata: dict[str, Any] = dict(run_metadata_extra) if run_metadata_extra else {}
    if effort:
        metadata["reasoning_effort"] = effort
    if model:
        metadata["model_version"] = model
    return base, metadata

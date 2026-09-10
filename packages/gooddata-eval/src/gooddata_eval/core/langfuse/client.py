# (C) 2026 GoodData Corporation
"""Minimal httpx Langfuse client: scores, OTLP export, dataset lookups and trace reads.

No Langfuse SDK, so it works on every Python version the package supports.
"""

from __future__ import annotations

import threading
import time
import uuid
from datetime import datetime, timezone
from typing import Any

import httpx

from gooddata_eval.core.langfuse import _env, observations, otlp
from gooddata_eval.core.langfuse.experiment import (
    ExperimentItem,
    ExperimentRun,
    ScoreTarget,
    build_experiment_root_span,
)
from gooddata_eval.core.langfuse.observations import TraceSummary

_SCORES_PATH = "/api/public/scores"
_OTLP_PATH = "/api/public/otel/v1/traces"

_MAX_SCORE_ATTEMPTS = 3
_DEFAULT_RETRY_DELAY = 0.5
_MAX_RETRY_DELAY = 5.0


def _is_retryable(resp: httpx.Response) -> bool:
    return resp.status_code == 429 or resp.status_code >= 500


def _retry_delay(resp: httpx.Response) -> float:
    """Seconds to wait before the next attempt, from `Retry-After` when the server names one.

    Unparsable, negative or NaN values fall back to the default; the cap bounds the wait so a
    throttled score cannot hold a linking worker for long.
    """
    try:
        asked_for = float(resp.headers.get("Retry-After", ""))
    except ValueError:
        return _DEFAULT_RETRY_DELAY
    if not asked_for >= 0:
        return _DEFAULT_RETRY_DELAY
    return min(asked_for, _MAX_RETRY_DELAY)


class _TraceListResult:
    def __init__(self, data: list[TraceSummary]) -> None:
        self.data = data


class _TraceAPI:
    """The `api.trace.list` shape external callers duck-type, served from observations."""

    def __init__(self, owner: HttpxLangfuseClient) -> None:
        self._owner = owner

    def list(
        self, from_timestamp: Any, to_timestamp: Any, limit: int, session_id: str | None = None
    ) -> _TraceListResult:
        """List traces in a window, optionally narrowed to one session server-side.

        ``session_id`` is what makes ``limit`` a non-issue. Without it the window holds every
        trace, newest-first, so an eval workspace busy enough to put more than ``limit``
        traces inside one item's window pushes that item's OWN (oldest) trace off the page --
        it then polls its whole retry budget against a page that can never contain it, and
        the score orphans. Named ``session_id`` because ``_fetch_traces_for_session`` probes
        for exactly that parameter; gen-ai sets sessionId = conversationId.
        """
        return _TraceListResult(
            self._owner.list_traces(from_time=from_timestamp, to_time=to_timestamp, limit=limit, session_id=session_id)
        )


class _DatasetRunItemsAPI:
    """`api.dataset_run_items.create` for external callers on the dataset-run vocabulary: a v4 run is one span."""

    def __init__(self, owner: HttpxLangfuseClient) -> None:
        self._owner = owner

    def create(
        self,
        run_name: str,
        dataset_item_id: str,
        trace_id: str,
        metadata: dict | None = None,
        run_description: str = "",
    ) -> ScoreTarget:
        """Export one experiment root span for `dataset_item_id` and return where to score it.

        The span is its own trace, so `trace_id` is carried as metadata and is NOT what an
        experiment-item score attaches to -- Langfuse reads those off the root observation.
        The returned target names both, and `score_safe` writes to each; scoring the bare
        `trace_id` instead reaches the gen-ai trace only and leaves the run item unscored.
        """
        dataset_id = self._owner.dataset_id_for_item(dataset_item_id)
        if dataset_id is None:
            raise LookupError(f"dataset item {dataset_item_id!r} not found in Langfuse")
        now = datetime.now(timezone.utc)
        span = build_experiment_root_span(
            ExperimentRun(run_name, dataset_id, metadata, run_description or None),
            ExperimentItem(dataset_item_id, input={"dataset_item_id": dataset_item_id}),
            start=now,
            end=now,
            trace_name=f"gd-eval: {dataset_item_id}",
            tags=("gd-eval",),
            observation_metadata={"gen_ai_trace_id": trace_id},
            trace_metadata={"run_name": run_name},
        )
        self._owner.export_spans([span])
        return ScoreTarget(trace_id, span.trace_id, span.span_id)


class _LangfuseAPI:
    def __init__(self, owner: HttpxLangfuseClient) -> None:
        self.trace = _TraceAPI(owner)
        self.dataset_run_items = _DatasetRunItemsAPI(owner)


class HttpxLangfuseClient:
    """Langfuse client over httpx, built from the standard Langfuse environment variables."""

    def __init__(self, *, timeout: float = 10.0, transport: httpx.BaseTransport | None = None) -> None:
        self._http = _env.make_http_client(timeout=timeout, transport=transport)
        self._dataset_ids: dict[str, str | None] = {}
        self._dataset_ids_lock = threading.Lock()
        self.api = _LangfuseAPI(self)

    def create_score(
        self,
        trace_id: str,
        name: str,
        value: float,
        data_type: str,
        comment: str | None = None,
        observation_id: str | None = None,
    ) -> None:
        """Attach one score to a trace, or to a single observation inside it."""
        body: dict[str, Any] = {
            "id": str(uuid.uuid4()),
            "traceId": trace_id,
            "name": name,
            # A BOOLEAN score goes over the wire as 1.0/0.0 whatever its Python type: the
            # sink's compute_scores yields int 1/0 and the agentic path float 1.0/0.0.
            "value": (1.0 if value else 0.0) if data_type == "BOOLEAN" else value,
            "dataType": data_type,
        }
        if comment:
            body["comment"] = comment
        if observation_id:
            body["observationId"] = observation_id
        resp = self._http.post(_SCORES_PATH, json=body)
        for _retry in range(_MAX_SCORE_ATTEMPTS - 1):
            if not _is_retryable(resp):
                break
            time.sleep(_retry_delay(resp))
            resp = self._http.post(_SCORES_PATH, json=body)
        resp.raise_for_status()

    def export_spans(self, spans: list[otlp.Span]) -> None:
        """Export spans to Langfuse over OTLP/HTTP JSON. Raises on a refused or rejected export."""
        resp = self._http.post(
            _OTLP_PATH,
            json=otlp.encode_export_request(spans),
            headers={"x-langfuse-ingestion-version": "4"},
        )
        otlp.parse_export_response(resp)

    def dataset_id_for_item(self, item_id: str) -> str | None:
        """The Langfuse dataset an item belongs to, or None when the id is not a Langfuse item.

        Cached because a run resolves the same handful of datasets once per item, from the
        linking pool's worker threads.
        """
        with self._dataset_ids_lock:
            if item_id in self._dataset_ids:
                return self._dataset_ids[item_id]
        resp = self._http.get(f"/api/public/dataset-items/{item_id}")
        if resp.status_code == 404:
            dataset_id = None
        else:
            resp.raise_for_status()
            dataset_id = resp.json().get("datasetId")
        with self._dataset_ids_lock:
            self._dataset_ids[item_id] = dataset_id
        return dataset_id

    def list_traces(
        self, *, from_time: Any, to_time: Any, limit: int, session_id: str | None = None
    ) -> list[TraceSummary]:
        return observations.list_traces_in_window(
            self._http, from_time=from_time, to_time=to_time, limit=limit, session_id=session_id
        )

    def flush(self) -> None:
        pass  # no client-side batching

    def close(self) -> None:
        self._http.close()

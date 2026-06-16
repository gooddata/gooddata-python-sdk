# (C) 2026 GoodData Corporation. All rights reserved.
"""Shared Langfuse helpers for agentic evaluation runners."""

from __future__ import annotations

import base64
import logging
import os
import time
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from typing import Any

import httpx

_log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# httpx-based Langfuse client — Python 3.14 safe (no Langfuse SDK required)
# ---------------------------------------------------------------------------


class _TraceObj:
    """Duck-type wrapper around a raw Langfuse trace dict."""

    def __init__(self, raw: dict) -> None:
        self.id: str = raw.get("id", "")
        self.metadata: dict = raw.get("metadata") or {}
        self.session_id: str | None = raw.get("sessionId") or raw.get("session_id")
        self.latency: float = float(raw.get("latency") or 0.0)
        self.total_cost: float = float(raw.get("totalCost") or raw.get("total_cost") or 0.0)


class _TraceListResult:
    def __init__(self, data: list[_TraceObj]) -> None:
        self.data = data


class _TraceAPI:
    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def list(self, from_timestamp: Any, to_timestamp: Any, limit: int) -> _TraceListResult:
        def _ts(v: Any) -> str:
            return v.isoformat() if hasattr(v, "isoformat") else str(v)

        resp = self._client.get(
            "/api/public/traces",
            params={"fromTimestamp": _ts(from_timestamp), "toTimestamp": _ts(to_timestamp), "limit": limit},
        )
        resp.raise_for_status()
        return _TraceListResult([_TraceObj(t) for t in resp.json().get("data", [])])


class _DatasetRunItemsAPI:
    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def create(
        self,
        run_name: str,
        dataset_item_id: str,
        trace_id: str,
        metadata: dict | None = None,
        run_description: str = "",
    ) -> None:
        self._client.post(
            "/api/public/dataset-run-items",
            json={
                "runName": run_name,
                "datasetItemId": dataset_item_id,
                "traceId": trace_id,
                "metadata": metadata or {},
                "runDescription": run_description,
            },
        ).raise_for_status()


class _LangfuseAPI:
    def __init__(self, client: httpx.Client) -> None:
        self.trace = _TraceAPI(client)
        self.dataset_run_items = _DatasetRunItemsAPI(client)


class HttpxLangfuseClient:
    """Minimal Langfuse client using httpx — works on Python 3.14 (no Langfuse SDK needed)."""

    def __init__(self) -> None:
        host = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com").rstrip("/")
        pub = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
        sec = os.environ.get("LANGFUSE_SECRET_KEY", "")
        if not pub or not sec:
            raise RuntimeError(
                "Langfuse credentials not set. "
                "Export LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY before using --langfuse."
            )
        creds = base64.b64encode(f"{pub}:{sec}".encode()).decode()
        self._http = httpx.Client(
            base_url=host,
            headers={"Authorization": f"Basic {creds}"},
            timeout=10,
        )
        self.api = _LangfuseAPI(self._http)

    def create_score(
        self,
        trace_id: str,
        name: str,
        value: float,
        data_type: str,
        comment: str | None = None,
    ) -> None:
        now = datetime.now(timezone.utc).isoformat()
        # Langfuse API requires numeric value for BOOLEAN type (1.0/0.0), not JSON booleans
        if isinstance(value, bool):
            value = 1.0 if value else 0.0
        body: dict[str, Any] = {
            "id": str(uuid.uuid4()),
            "traceId": trace_id,
            "name": name,
            "value": value,
            "dataType": data_type,
        }
        if comment:
            body["comment"] = comment
        self._http.post(
            "/api/public/ingestion",
            json={"batch": [{"id": str(uuid.uuid4()), "timestamp": now, "type": "score-create", "body": body}]},
        ).raise_for_status()

    def update_trace_version(self, trace_id: str, version: str) -> None:
        """Upsert the trace version field via the ingestion endpoint."""
        now = datetime.now(timezone.utc).isoformat()
        self._http.post(
            "/api/public/ingestion",
            json={
                "batch": [
                    {
                        "id": str(uuid.uuid4()),
                        "timestamp": now,
                        "type": "trace-create",
                        "body": {"id": trace_id, "version": version},
                    }
                ]
            },
        ).raise_for_status()

    def flush(self) -> None:
        pass  # no client-side batching

    def close(self) -> None:
        self._http.close()


def make_langfuse_client() -> HttpxLangfuseClient:
    """Create a Langfuse client from standard env vars. No external SDK required."""
    return HttpxLangfuseClient()


def try_make_langfuse_client() -> HttpxLangfuseClient | None:
    """Create Langfuse client from env vars; return None if credentials are missing."""
    try:
        return make_langfuse_client()
    except RuntimeError:
        return None


# ---------------------------------------------------------------------------

SKIP_ENV_VAR = "TAVERN_E2E_SKIP_TRACE_LINK"

_MAX_LATENCY_SEC = 60.0
_MAX_COST_USD = 0.05
_QUALITY_WEIGHT = 0.6
_SPEED_WEIGHT = 0.2
_COST_WEIGHT = 0.2

_INITIAL_DELAY = 0.5
_MAX_ATTEMPTS = 8
_BACKOFF = 1.6
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
    # Langfuse v4+ supports sessionId as a direct filter; older SDK / httpx path may not.
    try:
        import inspect  # noqa: PLC0415

        sig = inspect.signature(langfuse.api.trace.list)
        if "session_id" in sig.parameters:
            kwargs["session_id"] = session_id
    except Exception:
        pass
    response = langfuse.api.trace.list(**kwargs)
    traces = response.data or []
    # If sessionId filter was not applied server-side, filter locally.
    if "session_id" not in kwargs:
        traces = [
            t
            for t in traces
            if (isinstance(getattr(t, "session_id", None), str) and t.session_id == session_id)
            or (isinstance(getattr(t, "metadata", None), dict) and t.metadata.get("conversation_id") == session_id)
        ]
    return traces


def find_traces_per_conversation(
    langfuse: Any,
    conversation_ids: list[str],
    window_start: datetime,
) -> dict[str, Any]:
    """Poll Langfuse until traces matching all conversation_ids are found or retries exhaust."""
    if bool(os.environ.get(SKIP_ENV_VAR)):
        return dict.fromkeys(conversation_ids)

    by_conv: dict[str, Any] = dict.fromkeys(conversation_ids)
    window_end = datetime.now(timezone.utc)
    pad = timedelta(seconds=_WINDOW_PADDING_SEC)

    for cid in conversation_ids:
        delay = _INITIAL_DELAY
        found: list[Any] = []
        for _ in range(_MAX_ATTEMPTS):
            time.sleep(delay)
            try:
                found = _fetch_traces_for_session(langfuse, cid, window_start, window_end, pad)
            except Exception as exc:
                _log.debug("Langfuse trace fetch failed for %s: %s", cid, exc)
            if found:
                break
            delay *= _BACKOFF
        if found:
            by_conv[cid] = max(found, key=lambda t: getattr(t, "latency", None) or 0.0)
        else:
            _log.warning(
                "[langfuse] No trace found for conversation %s in window [%s, %s]", cid, window_start, window_end
            )
            print(f"[langfuse] WARNING: no trace found for conversation {cid}", flush=True)

    return by_conv


def _set_trace_version(langfuse: Any, trace_id: str, version: str) -> None:
    """Write model version into the Langfuse trace version field."""
    try:
        if hasattr(langfuse, "update_trace_version"):
            # HttpxLangfuseClient path
            langfuse.update_trace_version(trace_id, version)
        elif hasattr(langfuse, "trace"):
            # Langfuse Python SDK path (v2+)
            langfuse.trace(id=trace_id, version=version)
    except Exception as exc:
        _log.warning("Failed to set trace version %r on %s: %s", version, trace_id, exc)


@contextmanager
def observe(
    langfuse: Any,
    trace_id: str | None,
    dataset_item_id: str,
    run_name: str,
    run_metadata: dict[str, Any] | None = None,
) -> Iterator[str | None]:
    """Create a Langfuse dataset run item and yield the trace_id."""
    if trace_id is not None:
        try:
            langfuse.api.dataset_run_items.create(
                run_name=run_name,
                dataset_item_id=dataset_item_id,
                trace_id=trace_id,
                metadata=run_metadata or {"testing_framework": "tavern-e2e"},
                run_description="",
            )
            _log.debug(
                "[langfuse] Created dataset run item: run=%s trace=%s item=%s", run_name, trace_id, dataset_item_id
            )
        except Exception as exc:
            _log.warning("Failed to link trace %s to run %s: %s", trace_id, run_name, exc)
            print(
                f"[langfuse] WARNING: failed to create dataset run item run={run_name} trace={trace_id} item={dataset_item_id}: {exc}",
                flush=True,
            )
        model_version = (run_metadata or {}).get("model_version")
        if model_version:
            _set_trace_version(langfuse, trace_id, model_version)
    else:
        _log.warning("No trace found for dataset run %s; scores will be orphaned.", run_name)
    yield trace_id


def score_safe(langfuse: Any, trace_id: str | None, **kwargs: Any) -> None:
    """Create a Langfuse score, ignoring errors."""
    if not trace_id:
        return
    try:
        langfuse.create_score(trace_id=trace_id, **kwargs)
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
) -> tuple[str, dict[str, Any]]:
    """Return (run_name_base, run_metadata) with model version resolved from workspace API."""
    model = get_model_version(host, token, workspace_id, model_version_override)
    ts = run_timestamp or datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base = f"{dataset_name}_{ts}"
    if model:
        base = f"{base}_{model}"
    metadata: dict[str, Any] = {"testing_framework": "tavern-e2e"}
    if model:
        metadata["model_version"] = model
    return base, metadata

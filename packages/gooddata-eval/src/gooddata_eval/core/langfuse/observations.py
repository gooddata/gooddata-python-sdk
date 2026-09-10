# (C) 2026 GoodData Corporation
"""Trace summaries read from the Langfuse v4 observations endpoint."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import httpx

_OBSERVATIONS_PATH = "/api/public/v2/observations"
# Everything a TraceSummary needs: core (ids, times, parent), basic (sessionId), usage
# (totalCost), metrics (latency), metadata.
_FIELDS = "core,basic,usage,metrics,metadata"


def _parse_time(value: Any) -> datetime | None:
    """Parse an ISO 8601 timestamp into a timezone-aware datetime; anything else is None."""
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=timezone.utc)


def _iso(value: Any) -> str:
    return value.isoformat() if hasattr(value, "isoformat") else str(value)


class TraceSummary:
    """One Langfuse trace, seen through its root observation row or a legacy trace dict.

    An observation row identifies its trace by ``traceId`` and itself by ``id``; a legacy
    trace dict carries the trace id in ``id`` and has no root observation.
    """

    def __init__(self, raw: dict, *, total_cost: float | None = None) -> None:
        trace_id = raw.get("traceId")
        self.id: str = trace_id or raw.get("id") or ""
        self.root_observation_id: str | None = raw.get("id") if trace_id else None
        self.metadata: dict = raw.get("metadata") or {}
        self.session_id: str | None = raw.get("sessionId") or raw.get("session_id")
        self.latency: float = float(raw.get("latency") or 0.0)
        own_cost = raw.get("totalCost") or raw.get("total_cost")
        self.total_cost: float = float((own_cost if total_cost is None else total_cost) or 0.0)
        self.start_time: datetime | None = _parse_time(raw.get("startTime"))
        self.end_time: datetime | None = _parse_time(raw.get("endTime"))


def summarize_traces(rows: list[dict]) -> list[TraceSummary]:
    """Fold observation rows into one summary per trace, in order of first appearance.

    The root is the row without a parent observation; it carries the trace's session,
    metadata and latency. Cost is summed over all of the trace's rows, because on a gen-ai
    conversation the root has no cost of its own and the model calls under it do. A trace
    whose root is not on the page is dropped -- a poll that catches a conversation
    mid-ingestion sees children only, and those describe no complete trace.
    """
    order: list[str] = []
    roots: dict[str, dict] = {}
    costs: dict[str, float] = {}
    for row in rows:
        trace_id = row.get("traceId")
        if not trace_id:
            continue
        if trace_id not in costs:
            order.append(trace_id)
            costs[trace_id] = 0.0
        costs[trace_id] += float(row.get("totalCost") or 0.0)
        if not row.get("parentObservationId"):
            roots.setdefault(trace_id, row)
    return [TraceSummary(roots[tid], total_cost=costs[tid]) for tid in order if tid in roots]


def list_traces_in_window(
    http: httpx.Client,
    *,
    from_time: Any,
    to_time: Any,
    limit: int,
    session_id: str | None,
    page_size: int | None = None,
    max_pages: int | None = None,
) -> list[TraceSummary]:
    """List up to ``limit`` traces whose observations start inside the window, newest first.

    ``session_id`` is sent whenever it is not None -- an empty id is a real filter value that
    matches nothing, and dropping it would return the whole window for the caller to throw
    away, page after page.

    It also sets how deep the read goes. A filtered window holds one conversation and is
    exhausted in a page or two; an unfiltered one holds every trace the workspace produced
    in the same minutes, so it is read at the API's maximum page and twice as many pages.
    """
    if page_size is None:
        page_size = 500 if session_id is not None else 1000
    if max_pages is None:
        max_pages = 4 if session_id is not None else 8

    params: dict[str, Any] = {
        "fromStartTime": _iso(from_time),
        "toStartTime": _iso(to_time),
        "fields": _FIELDS,
        "limit": page_size,
    }
    if session_id is not None:
        params["sessionId"] = session_id

    rows: list[dict] = []
    summaries: list[TraceSummary] = []
    cursor: str | None = None
    for _page in range(max_pages):
        resp = http.get(_OBSERVATIONS_PATH, params=params if cursor is None else {**params, "cursor": cursor})
        resp.raise_for_status()
        body = resp.json()
        rows.extend(body.get("data") or [])
        # Re-folded per page: a trace's root and its children can straddle a page boundary.
        summaries = summarize_traces(rows)
        cursor = (body.get("meta") or {}).get("cursor")
        if not cursor or len(summaries) >= limit:
            break
    return summaries[:limit]

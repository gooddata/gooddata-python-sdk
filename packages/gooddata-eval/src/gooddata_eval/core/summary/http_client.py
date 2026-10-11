# (C) 2026 GoodData Corporation
"""HTTP client for the dedicated dashboard-summary endpoint.

Unlike the conversational chat skill, this endpoint executes the AFM for each
visualization server-side and returns a plain synchronous JSON summary — no SSE
stream and no client-side ``result_id`` wrangling. The response is adapted into
a ``ChatResult`` (summary text -> ``text_response``) so the existing
LLM-as-judge evaluators can score it unchanged.

Endpoint (gen-ai service):
    POST /api/v1/ai/workspaces/{workspace_id}/summary

If the route is ever renamed (e.g. to ``/summarize``), change ``_PATH`` only.
"""

import time

import httpx

from gooddata_eval.core.models import ChatResult, DatasetItem
from gooddata_eval.core.timing import note_trace_latency

_PATH = "/api/v1/ai/workspaces/{workspace_id}/summary"


class SummaryClient:
    """Single-shot client for the dashboard-summary endpoint."""

    def __init__(self, host: str, token: str, workspace_id: str, *, timeout: float = 300.0):
        self._url = f"{host.rstrip('/')}{_PATH.format(workspace_id=workspace_id)}"
        self._auth = {"Authorization": f"Bearer {token}"}
        self._client = httpx.Client(timeout=timeout)

    def ask(self, item: DatasetItem) -> ChatResult:
        """Request a summary for one dataset item and adapt it to a ChatResult."""
        si = item.summary_input
        if si is None:
            raise ValueError(f"dashboard_summary item '{item.id}' is missing required 'summary_input'.")

        body: dict = {"dashboardId": si.dashboard_id}
        if si.visualizations is not None:
            body["visualizations"] = si.visualizations
        if si.filter_context is not None:
            body["filterContext"] = si.filter_context
        if si.tab_id is not None:
            body["tabId"] = si.tab_id
        if si.format_hint is not None:
            body["formatHint"] = si.format_hint

        started = time.monotonic()
        resp = self._client.post(self._url, json=body, headers={**self._auth, "Content-Type": "application/json"})
        resp.raise_for_status()
        data = resp.json()
        elapsed = time.monotonic() - started
        summary = data.get("summary") or ""
        result = ChatResult.model_validate({"textResponse": summary})
        # The request is this item's one trace, timed like a chat turn so the single-shot latency
        # covers dashboard_summary on the same footing.
        result.turn_wall_clock_sec = elapsed
        note_trace_latency(elapsed)
        return result

    def close(self) -> None:
        self._client.close()

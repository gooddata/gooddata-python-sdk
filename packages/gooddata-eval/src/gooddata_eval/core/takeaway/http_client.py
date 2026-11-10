# (C) 2026 GoodData Corporation
"""HTTP client for the AI Publisher takeaway endpoint.

Like the dashboard-summary endpoint, it executes each visualization server-side and
returns plain synchronous JSON. The response is adapted into a ``ChatResult``
(takeaway text -> ``text_response``); the whole response body is kept on
``raw_response`` so the evaluator can tell a ``noData`` answer from an empty takeaway.

Endpoint (gen-ai service):
    POST /api/v1/ai/workspaces/{workspace_id}/takeaway

The request DTO rejects unknown keys and nulls are not sent, so every unset optional
field is omitted rather than sent as ``null``.
"""

from typing import Any

import httpx

from gooddata_eval.core._retry import RETRYABLE_STATUS_CODES, retry_transient
from gooddata_eval.core.models import ChatResult, DatasetItem, TakeawayInput, TakeawayVisualization

_PATH = "/api/v1/ai/workspaces/{workspace_id}/takeaway"


def _visualization_body(visualization: str | TakeawayVisualization) -> str | dict[str, Any]:
    if isinstance(visualization, str):
        return visualization
    return {"visualizationId": visualization.visualization_id, "filters": visualization.filters}


# Failures that say nothing about the request. A read timeout is left out: the page was
# being computed, and retrying spends the whole timeout again on every attempt.
_RETRYABLE_TRANSPORT_ERRORS = (httpx.ConnectError, httpx.ConnectTimeout, httpx.RemoteProtocolError, httpx.PoolTimeout)


def _is_retryable(exc: Exception) -> bool:
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in RETRYABLE_STATUS_CODES
    return isinstance(exc, _RETRYABLE_TRANSPORT_ERRORS)


def _request_body(ti: TakeawayInput) -> dict[str, Any]:
    body: dict[str, Any] = {}
    if ti.agent_id is not None:
        body["agentId"] = ti.agent_id
    instructions = {
        key: value
        for key, value in (
            ("document", ti.instructions.document),
            ("slot", ti.instructions.slot),
            ("formatHint", ti.instructions.format_hint),
        )
        if value is not None
    }
    if instructions:
        body["instructions"] = instructions
    if ti.max_characters is not None:
        body["maxCharacters"] = ti.max_characters
    body["data"] = {
        "visualizations": [_visualization_body(v) for v in ti.visualizations],
        "filterContext": ti.filter_context,
    }
    return body


class TakeawayClient:
    """Single-shot client for the takeaway endpoint."""

    def __init__(self, host: str, token: str, workspace_id: str, *, timeout: float = 120.0):
        self._url = f"{host.rstrip('/')}{_PATH.format(workspace_id=workspace_id)}"
        self._auth = {"Authorization": f"Bearer {token}"}
        self._client = httpx.Client(timeout=timeout)

    def ask(self, item: DatasetItem) -> ChatResult:
        """Request a takeaway for one dataset item and adapt it to a ChatResult.

        Raises:
            ValueError: The item carries no `takeaway_input`.
            httpx.HTTPStatusError: The endpoint answered non-2xx; the message carries the
                status code and the response body. Transient statuses and connection
                failures are retried first, with the chat client's backoff and budget.
        """
        ti = item.takeaway_input
        if ti is None:
            raise ValueError(f"document_takeaway item '{item.id}' is missing required 'takeaway_input'.")

        body = _request_body(ti)

        def _post() -> httpx.Response:
            resp = self._client.post(self._url, json=body, headers={**self._auth, "Content-Type": "application/json"})
            if not resp.is_success:
                raise httpx.HTTPStatusError(
                    f"Takeaway request failed with {resp.status_code} for {self._url}: {resp.text}",
                    request=resp.request,
                    response=resp,
                )
            return resp

        data = retry_transient(_post, is_retryable=_is_retryable).json()
        return ChatResult(text_response=data.get("takeaway") or "", raw_response=data)

    def close(self) -> None:
        self._client.close()

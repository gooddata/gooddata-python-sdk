# (C) 2026 GoodData Corporation. All rights reserved.
"""Workspace access the metric-skill evaluator needs beyond the chat: the metrics, a test execution, the conversation
history.

Metrics are read through the SDK's entity API. Restores go through the metric entity endpoint, never through the
agent's ``create_metric`` tool: that tool writes its defaults over any field it is not given, so a restore through it
would change the metric it tries to restore.
"""

from __future__ import annotations

import functools
from collections.abc import Callable
from typing import Any

import httpx
from gooddata_api_client.exceptions import ApiException, NotFoundException
from gooddata_sdk import GoodDataSdk
from gooddata_sdk.utils import load_all_entities

from gooddata_eval.core._retry import RETRYABLE_STATUS_CODES, is_retryable_request_error, retry_transient
from gooddata_eval.core.agentic._clarification import _page_with_retry

_METRICS = "/api/v1/entities/workspaces/{ws}/metrics"
_EXECUTE = "/api/v1/actions/workspaces/{ws}/execution/afm/execute"
_ITEMS = "/api/v1/ai/workspaces/{ws}/chat/conversations/{conversation_id}/items"
_JSON_API = "application/vnd.gooddata.api+json"
# Every attribute a metric write accepts except areRelationsValid, which the server computes.
_WRITABLE = ("title", "description", "tags", "content", "isHidden", "isHiddenFromKda", "conditionalFormatting")


class WorkspaceReadError(RuntimeError):
    """The harness could not read the workspace or the conversation, so the run cannot be scored."""


class _TransientStatus(Exception):
    """A request answered with a retryable status; carries the response for the final report."""

    def __init__(self, response: httpx.Response):
        super().__init__(f"HTTP {response.status_code}")
        self.response = response


def _is_transient_request(exc: Exception) -> bool:
    return isinstance(exc, _TransientStatus) or is_retryable_request_error(exc)


class MetricWorkspace:
    """Reads and restores one workspace's metrics, executes a metric, and reads a conversation's items."""

    def __init__(self, host: str, token: str, workspace_id: str, sdk: GoodDataSdk, *, timeout: float = 60.0):
        self._base = host.rstrip("/")
        self._ws = workspace_id
        self._entities = sdk._client.entities_api
        self._auth = {"Authorization": f"Bearer {token}"}
        self._client = httpx.Client(timeout=timeout)
        # Metrics a run could not put back; while any is listed, later runs are not driven.
        self.unrestored: list[str] = []

    def close(self) -> None:
        self._client.close()

    def list_metrics(self) -> dict[str, dict]:
        """Every metric of the workspace, as metric id -> entity attributes.

        Raises:
            WorkspaceReadError: A page could not be read after the transient retries.
        """
        list_page = functools.partial(self._entities.get_all_entities_metrics, self._ws, _check_return_type=False)
        try:
            data = load_all_entities(functools.partial(_page_with_retry, list_page)).data
        except (ApiException, httpx.HTTPError, OSError) as exc:
            raise WorkspaceReadError(f"could not list metrics: {exc}") from exc
        out: dict[str, dict] = {}
        for obj in data:
            # A row the run could not restore from makes the snapshot useless, so it fails the snapshot.
            attributes = obj.get("attributes") if isinstance(obj, dict) else None
            if not isinstance(obj, dict) or not obj.get("id") or not isinstance(attributes, dict):
                raise WorkspaceReadError(f"could not list metrics: unreadable row {obj!r}")
            if not isinstance(attributes.get("content"), dict) or not attributes["content"].get("maql"):
                raise WorkspaceReadError(f"could not list metrics: metric {obj['id']!r} has no MAQL")
            out[obj["id"]] = attributes
        return out

    def get_metric(self, metric_id: str) -> dict | None:
        """One metric's entity attributes, or None when it does not exist.

        Raises:
            WorkspaceReadError: The lookup failed for a reason other than a 404.
        """
        try:
            doc = self._entities.get_entity_metrics(self._ws, metric_id, _check_return_type=False)
        except NotFoundException:
            return None
        except (ApiException, httpx.HTTPError, OSError) as exc:
            raise WorkspaceReadError(f"could not read metric {metric_id}: {exc}") from exc
        # The document is a model even with _check_return_type=False; only its data is a plain dict.
        data = doc.get("data") if isinstance(doc, dict) else getattr(doc, "data", None)
        attributes = data.get("attributes") if isinstance(data, dict) else None
        if not isinstance(attributes, dict):
            raise WorkspaceReadError(f"could not read metric {metric_id}: no attributes in {data!r}")
        return attributes

    def restore_metric(self, metric_id: str, attributes: dict, *, exists: bool) -> bool:
        """Write a metric back to the given attributes, retrying transient failures; True on success.

        A failure is printed, not raised: the caller reports it as a harness error.
        """
        body = {
            "data": {
                "id": metric_id,
                "type": "metric",
                "attributes": {k: attributes[k] for k in _WRITABLE if attributes.get(k) is not None},
            }
        }
        base = f"{self._base}{_METRICS.format(ws=self._ws)}"
        headers = {**self._auth, "Content-Type": _JSON_API}

        def _send() -> httpx.Response:
            if exists:
                resp = self._client.put(f"{base}/{metric_id}", json=body, headers=headers)
            else:
                resp = self._client.post(base, json=body, headers=headers)
            if resp.status_code in RETRYABLE_STATUS_CODES:
                raise _TransientStatus(resp)
            return resp

        try:
            resp = retry_transient(_send, is_retryable=_is_transient_request)
        except _TransientStatus as exc:
            resp = exc.response
        except httpx.HTTPError as exc:
            print(f"[CLEANUP] Could not restore metric {metric_id}: {exc}")
            return False
        if not resp.is_success:
            print(f"[CLEANUP] Could not restore metric {metric_id}: HTTP {resp.status_code} {resp.text[:200]}")
        return resp.is_success

    def execute_metric(self, metric_id: str) -> str | None:
        """Compute the metric alone; None when it computes, else the reason the platform gave.

        Only a 4xx rejection is a reason. A rate limit (429) or a service fault (5xx) is retried, and one that
        outlasts the retries is raised: it says nothing about the metric.

        Raises:
            WorkspaceReadError: The request did not reach the platform, the platform did not serve it, or its
                answer was unreadable.
        """
        afm = {
            "execution": {
                "measures": [
                    {
                        "localIdentifier": "m",
                        "definition": {"measure": {"item": {"identifier": {"id": metric_id, "type": "metric"}}}},
                    }
                ],
                "attributes": [],
                "filters": [],
            },
            "resultSpec": {"dimensions": [{"localIdentifier": "d", "itemIdentifiers": ["measureGroup"]}]},
        }
        url = f"{self._base}{_EXECUTE.format(ws=self._ws)}"

        def _served(step: str, send: Callable[[], httpx.Response]) -> httpx.Response:
            """The response once it is no rate limit or service fault, retrying those; raises when they persist."""

            def _attempt() -> httpx.Response:
                resp = send()
                if resp.status_code in RETRYABLE_STATUS_CODES:
                    raise _TransientStatus(resp)
                return resp

            try:
                resp = retry_transient(_attempt, is_retryable=_is_transient_request)
            except _TransientStatus as exc:
                resp = exc.response
            if resp.status_code in RETRYABLE_STATUS_CODES or resp.status_code >= 500:
                raise WorkspaceReadError(f"could not execute metric {metric_id}: {step} HTTP {resp.status_code}")
            return resp

        try:
            resp = _served(
                "execute",
                lambda: self._client.post(url, json=afm, headers={**self._auth, "Content-Type": "application/json"}),
            )
            if not resp.is_success:
                return f"execute: HTTP {resp.status_code} {resp.text[:300]}"
            body = resp.json()
            response = body.get("executionResponse") if isinstance(body, dict) else None
            links = response.get("links") if isinstance(response, dict) else None
            result_id = links.get("executionResult") if isinstance(links, dict) else None
            if not isinstance(result_id, str) or not result_id:
                raise WorkspaceReadError(f"could not execute metric {metric_id}: no executionResult in {body!r}"[:400])
            result = _served("result", lambda: self._client.get(f"{url}/result/{result_id}", headers=self._auth))
            if not result.is_success:
                return f"result: HTTP {result.status_code} {result.text[:300]}"
            computed = result.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise WorkspaceReadError(f"could not execute metric {metric_id}: {type(exc).__name__}: {exc}") from exc
        if not isinstance(computed, dict) or not isinstance(computed.get("data"), list):
            # A computed result carries its data list, empty or not; a 200 without one proves no computation.
            raise WorkspaceReadError(f"could not execute metric {metric_id}: no data list in {str(computed)[:200]}")
        return None

    def conversation_items(self, conversation_id: str) -> list[dict[str, Any]]:
        """The conversation's stored items, oldest first.

        Raises:
            WorkspaceReadError: The items could not be read.
        """
        try:
            resp = self._client.get(
                f"{self._base}{_ITEMS.format(ws=self._ws, conversation_id=conversation_id)}", headers=self._auth
            )
            resp.raise_for_status()
            body = resp.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise WorkspaceReadError(f"could not read conversation {conversation_id}: {exc}") from exc
        key = next((k for k in ("items", "data") if isinstance(body, dict) and k in body), None)
        items = body[key] if key is not None else None
        if not isinstance(items, list):
            # A shape without its items list would read as a conversation with no suggestions, and pass.
            raise WorkspaceReadError(f"conversation {conversation_id}: no items list in {str(body)[:200]}")
        return items


def last_suggestions(items: list[dict[str, Any]]) -> dict | None:
    """The suggestions of the latest assistant item that carries them."""
    for item in reversed(items):
        content = item.get("content") if isinstance(item, dict) else None
        if isinstance(content, dict) and isinstance(content.get("suggestions"), dict):
            return content["suggestions"]
    return None

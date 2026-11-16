# (C) 2026 GoodData Corporation
"""HTTP client for the Analytics Catalog title/description generation endpoints.

Endpoints (afm-exec-api, served by gen-ai):
    POST /api/v1/actions/workspaces/{workspace_id}/ai/analyticsCatalog/generateTitle
    POST /api/v1/actions/workspaces/{workspace_id}/ai/analyticsCatalog/generateDescription

Both take ``{"objectType", "objectId"}`` and answer ``{"title"|"description", "note"}``.
The generated text becomes ``ChatResult.text_response``; the whole response body is kept
on ``raw_response`` with two extra keys the evaluator reads: ``output`` (which field was
asked for) and ``unusable_retries``. A placeholder ``"string"`` is dropped from both the
text and the note.

A 200 answer can carry no usable text: a null value with a null note, or the literal
schema placeholder ``"string"``. The endpoint is asked again once in that case, and the
retry is recorded, so a run reports the answer a user gets after one regenerate click.
A null value that comes with a note is the endpoint declining on purpose and is kept.
"""

from typing import Any

import httpx

from gooddata_eval.core._retry import is_retryable_request_error, retry_transient
from gooddata_eval.core.models import CatalogInput, ChatResult, DatasetItem

_PATH = "/api/v1/actions/workspaces/{workspace_id}/ai/analyticsCatalog/{action}"
_ACTIONS = {"title": "generateTitle", "description": "generateDescription"}
_PLACEHOLDER = "string"


def is_unusable(data: dict[str, Any], output: str) -> bool:
    """Whether a 200 answer carries neither a generated text nor a reason for its absence."""
    value = data.get(output)
    note = data.get("note")
    if value == _PLACEHOLDER:
        return True
    return not value and not note


class CatalogMetadataClient:
    """Single-shot client for the Analytics Catalog generate endpoints."""

    def __init__(self, host: str, token: str, workspace_id: str, *, timeout: float = 120.0, unusable_retries: int = 1):
        self._base = host.rstrip("/")
        self._workspace_id = workspace_id
        self._auth = {"Authorization": f"Bearer {token}"}
        self._client = httpx.Client(timeout=timeout)
        self._unusable_retries = unusable_retries

    def ask(self, item: DatasetItem) -> ChatResult:
        """Generate the title or description an item asks for and adapt it to a ChatResult.

        Raises:
            ValueError: The item carries no `catalog_input`.
            httpx.HTTPStatusError: As `request`.
        """
        ci = item.catalog_input
        if ci is None:
            raise ValueError(f"catalog_metadata item '{item.id}' is missing required 'catalog_input'.")
        return self.request(ci)

    def request(self, ci: CatalogInput) -> ChatResult:
        """Generate one text and adapt it to a ChatResult.

        Raises:
            httpx.HTTPStatusError: The endpoint answered non-2xx after the transient retries.
        """
        url = f"{self._base}{_PATH.format(workspace_id=self._workspace_id, action=_ACTIONS[ci.output])}"
        body = {"objectType": ci.object_type, "objectId": ci.object_id}

        def _post() -> httpx.Response:
            resp = self._client.post(url, json=body, headers={**self._auth, "Content-Type": "application/json"})
            if not resp.is_success:
                raise httpx.HTTPStatusError(
                    f"Catalog generate request failed with {resp.status_code} for {url}: {resp.text}",
                    request=resp.request,
                    response=resp,
                )
            return resp

        retries = 0
        data: dict[str, Any] = retry_transient(_post, is_retryable=is_retryable_request_error).json()
        while is_unusable(data, ci.output) and retries < self._unusable_retries:
            retries += 1
            data = retry_transient(_post, is_retryable=is_retryable_request_error).json()
        value = data.get(ci.output)
        text = value if isinstance(value, str) and value != _PLACEHOLDER else ""
        # The placeholder is no reason either: a declined answer must carry a real note.
        note = data.get("note") if data.get("note") != _PLACEHOLDER else None
        return ChatResult(
            text_response=text,
            raw_response={**data, "note": note, "output": ci.output, "unusable_retries": retries},
        )

    def close(self) -> None:
        self._client.close()

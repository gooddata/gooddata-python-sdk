# (C) 2026 GoodData Corporation
"""Load a dataset from Langfuse via the REST API.

Uses httpx (already a base dependency) instead of the Langfuse Python SDK so the
integration works on all Python versions, including 3.14, where the Langfuse SDK's
Pydantic-v1 shims break at import time.

Credentials are read from the standard Langfuse environment variables:
  LANGFUSE_PUBLIC_KEY   — your public key (pk-lf-...)
  LANGFUSE_SECRET_KEY   — your secret key (sk-lf-...)
  LANGFUSE_HOST         — base URL, e.g. https://us.cloud.langfuse.com (default)
"""

import base64
import os
from typing import Any

import httpx

from gooddata_eval.core.models import DatasetItem

_DEFAULT_HOST = "https://cloud.langfuse.com"
_PAGE_SIZE = 100


def _make_client() -> httpx.Client:
    """Build an httpx client with Langfuse basic-auth headers."""
    host = os.environ.get("LANGFUSE_HOST", _DEFAULT_HOST).rstrip("/")
    pub = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
    sec = os.environ.get("LANGFUSE_SECRET_KEY", "")
    if not pub or not sec:
        raise RuntimeError(
            "Langfuse credentials not set. "
            "Export LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY before using --langfuse-dataset."
        )
    creds = base64.b64encode(f"{pub}:{sec}".encode()).decode()
    return httpx.Client(base_url=host, headers={"Authorization": f"Basic {creds}"}, timeout=30)


def _question_from_input(raw_input: Any) -> str:
    if isinstance(raw_input, str):
        return raw_input
    if isinstance(raw_input, dict):
        question = raw_input.get("question")
        if isinstance(question, str):
            return question
    raise ValueError(f"Unsupported Langfuse item input shape: {raw_input!r}")


def _item_from_raw(raw: dict, *, dataset_name: str, test_kind: str) -> DatasetItem:
    """Map a Langfuse REST API dataset-item dict to a DatasetItem."""
    # REST API returns camelCase: expectedOutput, not expected_output
    expected_output = raw.get("expectedOutput") or raw.get("expected_output")
    resolved_kind = test_kind
    if isinstance(expected_output, dict) and isinstance(expected_output.get("test_kind"), str):
        resolved_kind = expected_output["test_kind"]
    return DatasetItem(
        id=str(raw["id"]),
        dataset_name=raw.get("datasetName") or dataset_name,
        test_kind=resolved_kind,
        question=_question_from_input(raw.get("input")),
        expected_output=expected_output,
    )


def load_langfuse_dataset(name: str, *, default_test_kind: str = "visualization") -> list[DatasetItem]:
    """Pull all items from a Langfuse dataset by name via the REST API.

    Args:
        name: The Langfuse dataset name (as shown in the Langfuse UI).
        default_test_kind: Fallback test_kind when the item doesn't specify one.

    Returns:
        Parsed dataset items.

    Raises:
        RuntimeError: Missing Langfuse credentials or dataset not found.
    """
    items: list[dict] = []
    page = 1
    with _make_client() as client:
        while True:
            resp = client.get(
                "/api/public/dataset-items",
                params={"datasetName": name, "limit": _PAGE_SIZE, "page": page},
            )
            if resp.status_code == 404:
                raise RuntimeError(
                    f"Langfuse dataset '{name}' not found. "
                    "Check the dataset name and that your credentials are correct."
                )
            resp.raise_for_status()
            data = resp.json()
            batch = data.get("data", [])
            items.extend(batch)
            total = (data.get("meta") or {}).get("totalItems", len(items))
            if len(items) >= total or len(batch) < _PAGE_SIZE:
                break
            page += 1

    if not items:
        raise ValueError(f"Langfuse dataset '{name}' exists but contains no items.")

    return [_item_from_raw(raw, dataset_name=name, test_kind=default_test_kind) for raw in items]

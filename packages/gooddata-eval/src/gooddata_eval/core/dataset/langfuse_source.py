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
from typing import Any, TypeVar, cast

import httpx

from gooddata_eval.core.models import DatasetItem, SummaryInput

_DEFAULT_HOST = "https://cloud.langfuse.com"
_PAGE_SIZE = 100

_T = TypeVar("_T")


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


def _first_of(wanted: type[_T], key: str, *sources: Any) -> _T | None:
    """First source that is a dict carrying a `wanted` value under `key`, in priority order.

    Langfuse items have no dedicated field for any of the things we look up this way, so
    each one is accepted from whichever of the item's objects carries it.
    """
    for source in sources:
        if isinstance(source, dict):
            value = source.get(key)
            if isinstance(value, wanted):
                return value
    return None


def _summary_input_from_raw(raw: dict, expected_output: Any) -> SummaryInput | None:
    """Locate a dashboard_summary item's `summary_input`."""
    candidate = _first_of(dict, "summary_input", raw.get("input"), raw.get("metadata"), expected_output)
    return SummaryInput.model_validate(candidate) if candidate is not None else None


def _user_context_from_raw(raw: dict) -> dict[str, Any] | None:
    """Locate an item's `user_context` -- relayed verbatim as the chat request's `userContext`.

    Like `summary_input`, Langfuse has no dedicated field for it, so accept it from the
    item input object or the item metadata. An item carrying an attachment (a WIDGET or
    VIEW descriptor) is meaningless without it: it degrades into a bare question the
    agent has no way to answer, and then fails for a reason that has nothing to do with
    what the item was written to test. So this has to survive the round trip.
    """
    found = _first_of(dict, "user_context", raw.get("input"), raw.get("metadata"))
    return cast("dict[str, Any]", found) if found is not None else None


def _infer_test_kind(expected_output: object, default: str, metadata: object = None) -> str:
    """Resolve test_kind: an explicit declaration first, then expected_output's structure.

    Precedence: `expectedOutput.test_kind`, then `metadata.test_kind`, then the shape of
    expected_output, then `default` (the CLI's --kind). Both explicit forms beat
    structural inference. Metadata matters because an item judged by a natural-language
    rubric has a plain *string* expectedOutput, which gives the structure checks below
    nothing to read -- metadata is the only place such a dataset can carry its own kind.
    """
    eo: dict[str, Any] | None = cast("dict[str, Any]", expected_output) if isinstance(expected_output, dict) else None
    # An explicit declaration wins over structure, expected_output ahead of metadata.
    # A blank declaration is not a declaration: "" would beat both the structural checks
    # below and the CLI default, and the item would be skipped as an unsupported kind.
    # Checked one source at a time so a blank expectedOutput.test_kind does not hide a real
    # metadata.test_kind behind it.
    for source in (eo, metadata):
        declared = _first_of(str, "test_kind", source)
        if declared and declared.strip():
            return declared.strip()
    if eo is None:
        return default
    # {"visualization": {...}} or {"visualization": [...]} → production agentic vis
    if eo.get("visualization") is not None:
        return "vis_agentic"
    # {"expected_outputs": [...]} → experimental multi-candidate agentic vis
    if isinstance(eo.get("expected_outputs"), list):
        return "agentic_visualization"
    return default


def _item_from_raw(raw: dict, *, dataset_name: str, test_kind: str) -> DatasetItem:
    """Map a Langfuse REST API dataset-item dict to a DatasetItem."""
    # REST API returns camelCase: expectedOutput, not expected_output
    expected_output = raw.get("expectedOutput") or raw.get("expected_output")
    resolved_kind = _infer_test_kind(expected_output, test_kind, raw.get("metadata"))
    return DatasetItem(
        id=str(raw["id"]),
        dataset_name=raw.get("datasetName") or dataset_name,
        test_kind=resolved_kind,
        question=_question_from_input(raw.get("input")),
        expected_output=expected_output,
        summary_input=_summary_input_from_raw(raw, expected_output),
        user_context=_user_context_from_raw(raw),
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

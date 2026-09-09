# (C) 2026 GoodData Corporation
"""Pure OTLP/HTTP JSON encoding for the Langfuse ingestion endpoint. No HTTP here."""

from __future__ import annotations

import json
import secrets
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

from gooddata_eval._version import __version__

if TYPE_CHECKING:
    import httpx

# Observation (span-level) attributes.
ATTR_OBSERVATION_TYPE = "langfuse.observation.type"
ATTR_OBSERVATION_INPUT = "langfuse.observation.input"
ATTR_OBSERVATION_OUTPUT = "langfuse.observation.output"
ATTR_OBSERVATION_METADATA_PREFIX = "langfuse.observation.metadata"

# Trace-wide attributes, copied onto every span of the trace.
ATTR_TRACE_NAME = "langfuse.trace.name"
ATTR_SESSION_ID = "langfuse.session.id"
ATTR_TRACE_TAGS = "langfuse.trace.tags"
ATTR_TRACE_METADATA_PREFIX = "langfuse.trace.metadata"
ATTR_VERSION = "langfuse.version"
ATTR_ENVIRONMENT = "langfuse.environment"

# Experiment attributes, present on every span of an experiment item's trace.
ATTR_EXPERIMENT_ID = "langfuse.experiment.id"
ATTR_EXPERIMENT_NAME = "langfuse.experiment.name"
ATTR_EXPERIMENT_DATASET_ID = "langfuse.experiment.dataset.id"
ATTR_EXPERIMENT_DESCRIPTION = "langfuse.experiment.description"
ATTR_EXPERIMENT_METADATA_PREFIX = "langfuse.experiment.metadata"

# Experiment item attributes, root span only.
ATTR_EXPERIMENT_ITEM_ID = "langfuse.experiment.item.id"
ATTR_EXPERIMENT_ITEM_ROOT_OBSERVATION_ID = "langfuse.experiment.item.root_observation_id"
ATTR_EXPERIMENT_ITEM_EXPECTED_OUTPUT = "langfuse.experiment.item.expected_output"
ATTR_EXPERIMENT_ITEM_METADATA_PREFIX = "langfuse.experiment.item.metadata"

_SERVICE_NAME = "gooddata-eval"
_EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)


def new_trace_id() -> str:
    return uuid.uuid4().hex


def new_span_id() -> str:
    return secrets.token_hex(8)


def unix_nano(dt: datetime) -> str:
    """Nanoseconds since the epoch as a decimal string. Naive datetimes are treated as UTC."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    delta = dt - _EPOCH
    nanos = (delta.days * 86400 + delta.seconds) * 1_000_000_000 + delta.microseconds * 1000
    return str(nanos)


def otlp_attribute(key: str, value: Any) -> dict[str, Any]:
    """Encode one key/value pair as an OTLP attribute, typed by the Python value's type.

    `bool` is checked before `int` because `bool` is an `int` subclass.
    """
    if isinstance(value, bool):
        return {"key": key, "value": {"boolValue": value}}
    if isinstance(value, int):
        return {"key": key, "value": {"intValue": str(value)}}
    if isinstance(value, float):
        return {"key": key, "value": {"doubleValue": value}}
    if isinstance(value, str):
        return {"key": key, "value": {"stringValue": value}}
    if isinstance(value, (list, tuple)) and all(isinstance(item, str) for item in value):
        return {"key": key, "value": {"arrayValue": {"values": [{"stringValue": item} for item in value]}}}
    return {"key": key, "value": {"stringValue": json.dumps(value, default=str)}}


def flatten_metadata(prefix: str, mapping: dict[str, Any] | None) -> list[dict[str, Any]]:
    """Flatten a metadata mapping into dotted `prefix.<key>` attributes, dropping `None` values.

    Scalars are typed via `otlp_attribute`; nested dicts and lists are encoded as a JSON string.
    """
    if not mapping:
        return []
    attributes = []
    for key, value in mapping.items():
        if value is None:
            continue
        full_key = f"{prefix}.{key}"
        if isinstance(value, (dict, list, tuple)):
            attributes.append({"key": full_key, "value": {"stringValue": json.dumps(value, default=str)}})
        else:
            attributes.append(otlp_attribute(full_key, value))
    return attributes


@dataclass
class Span:
    trace_id: str
    span_id: str
    name: str
    start: datetime
    end: datetime
    attributes: list[dict[str, Any]]
    status_code: int = 1


def encode_export_request(
    spans: list[Span], *, scope_name: str = _SERVICE_NAME, scope_version: str = __version__
) -> dict[str, Any]:
    """Build the OTLP/JSON export request body for `POST /api/public/otel/v1/traces`."""
    otlp_spans = [
        {
            "traceId": span.trace_id,
            "spanId": span.span_id,
            "name": span.name,
            "kind": 1,
            "startTimeUnixNano": unix_nano(span.start),
            "endTimeUnixNano": unix_nano(span.end),
            "status": {"code": span.status_code},
            "attributes": span.attributes,
        }
        for span in spans
    ]
    return {
        "resourceSpans": [
            {
                "resource": {"attributes": [{"key": "service.name", "value": {"stringValue": _SERVICE_NAME}}]},
                "scopeSpans": [{"scope": {"name": scope_name, "version": scope_version}, "spans": otlp_spans}],
            }
        ]
    }


def parse_export_response(resp: httpx.Response) -> None:
    """Raise on a failed or partially-rejected export; return `None` on success."""
    if not (200 <= resp.status_code < 300):
        raise RuntimeError(f"Langfuse OTLP export failed: {resp.status_code} {resp.text[:300]}")
    if not resp.content:
        return None
    try:
        body = resp.json()
    except ValueError:
        return None
    if not isinstance(body, dict):
        return None
    partial = body.get("partialSuccess")
    if isinstance(partial, dict) and _rejected_spans(partial) > 0:
        raise RuntimeError(f"Langfuse OTLP export partially rejected: {partial.get('errorMessage', '')}")
    return None


def _rejected_spans(partial: dict[str, Any]) -> int:
    """`partialSuccess.rejectedSpans`, an int64 that OTLP/JSON may encode as a decimal string."""
    try:
        return int(partial.get("rejectedSpans") or 0)
    except (TypeError, ValueError):
        return 0

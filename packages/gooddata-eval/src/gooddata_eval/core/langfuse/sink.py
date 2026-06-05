# (C) 2026 GoodData Corporation
"""Langfuse scoring sink — posts evaluation results via the Langfuse REST API."""

from __future__ import annotations

import base64
import os
import sys
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

import httpx

_MAX_LATENCY_S = 60.0
_QUALITY_WEIGHT = 0.6
_SPEED_WEIGHT = 0.2

if TYPE_CHECKING:
    from gooddata_eval.core.runner import ItemReport


def compute_scores(
    pass_at_k: bool,
    avg_latency_s: float,
    best_detail: dict[str, Any],
) -> dict[str, float]:
    """Compute Langfuse score values from an ItemReport.

    Returns a dict with keys: pass_at_k, quality_score, value_score, latency_s.
    quality_score = fraction of bool-valued keys in best_detail that are True.
    Falls back to pass_at_k if no bool keys exist (text evaluators).
    """
    bool_checks = {k: v for k, v in best_detail.items() if isinstance(v, bool)}
    quality = sum(1 for v in bool_checks.values() if v) / len(bool_checks) if bool_checks else 1.0 if pass_at_k else 0.0

    speed = max(0.0, 1.0 - avg_latency_s / _MAX_LATENCY_S)
    value = _QUALITY_WEIGHT * quality + _SPEED_WEIGHT * speed

    return {
        "pass_at_k": 1 if pass_at_k else 0,
        "quality_score": round(quality, 4),
        "value_score": round(value, 4),
        "latency_s": round(avg_latency_s, 3),
    }


class LangfuseSink:
    """Posts evaluation results to Langfuse via the ingestion REST API."""

    def __init__(self, dataset_name: str, run_name: str, model_id: str = "", provider_type: str = ""):
        self._dataset_name = dataset_name
        self._run_name = run_name
        self._model_id = model_id
        self._provider_type = provider_type
        host = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com").rstrip("/")
        pub = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
        sec = os.environ.get("LANGFUSE_SECRET_KEY", "")
        if not pub or not sec:
            raise RuntimeError(
                "Langfuse credentials not set. Export LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY to use --langfuse."
            )
        creds = base64.b64encode(f"{pub}:{sec}".encode()).decode()
        self._host = host
        self._auth_header = f"Basic {creds}"

    def log_item(self, report: ItemReport, *, dataset_item_id: str) -> None:
        """Send trace + dataset-run-item + scores for one evaluated item.

        Swallows all errors — Langfuse failures never abort the eval run.
        """
        trace_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()
        scores = compute_scores(
            pass_at_k=report.pass_at_k,
            avg_latency_s=report.avg_latency_s,
            best_detail=report.best_detail,
        )

        # Each ingestion event needs a top-level id (dedup) and timestamp
        # in addition to the body-level id/timestamp for the trace/score itself.
        def _event(event_type: str, body: dict[str, Any]) -> dict[str, Any]:
            return {"id": str(uuid.uuid4()), "timestamp": now, "type": event_type, "body": body}

        batch: list[dict[str, Any]] = [
            _event(
                "trace-create",
                {
                    "id": trace_id,
                    "timestamp": now,
                    "name": f"gd-eval: {report.question[:80]}",
                    # Expose the model on a first-class trace field so Langfuse
                    # dashboards can filter / break down by it ("Version"); trace
                    # metadata is not available as a breakdown dimension.
                    "version": self._model_id or None,
                    "input": {"question": report.question},
                    "output": report.best_detail,
                    "metadata": {
                        "dataset_name": report.dataset_name,
                        "test_kind": report.test_kind,
                        "item_id": report.id,
                        "model": self._model_id,
                        "provider_type": self._provider_type,
                    },
                    "tags": [t for t in [report.test_kind, self._provider_type] if t],
                },
            ),
        ]

        score_defs = [
            ("pass_at_k", scores["pass_at_k"], "BOOLEAN"),
            ("quality_score", scores["quality_score"], "NUMERIC"),
            ("value_score", scores["value_score"], "NUMERIC"),
            ("latency_s", scores["latency_s"], "NUMERIC"),
        ]
        for name, value, data_type in score_defs:
            batch.append(
                _event(
                    "score-create",
                    {
                        "id": str(uuid.uuid4()),
                        "traceId": trace_id,
                        "name": name,
                        "value": value,
                        "dataType": data_type,
                    },
                )
            )

        try:
            with httpx.Client(
                base_url=self._host,
                headers={"Authorization": self._auth_header},
                timeout=10,
            ) as client:
                resp = client.post("/api/public/ingestion", json={"batch": batch})
                resp.raise_for_status()
                # The ingestion endpoint returns HTTP 200 even when individual events
                # fail — per-event errors are in the response body.
                body = resp.json()
                errors = body.get("errors") or []
                for err in errors:
                    print(
                        f"warning: Langfuse event failed for item '{report.id}': "
                        f"type={err.get('error')} status={err.get('status')} id={err.get('id')}",
                        file=sys.stderr,
                    )
        except Exception as exc:
            print(f"warning: Langfuse ingestion failed for item '{report.id}': {exc}", file=sys.stderr)

        # Link trace to dataset run via the dedicated endpoint (simpler than ingestion —
        # does not require datasetId/runId; creates the run by name if absent).
        try:
            with httpx.Client(
                base_url=self._host,
                headers={"Authorization": self._auth_header},
                timeout=10,
            ) as client:
                r = client.post(
                    "/api/public/dataset-run-items",
                    json={
                        "runName": self._run_name,
                        "runDescription": (
                            f"{self._provider_type}/{self._model_id}"
                            if self._provider_type and self._model_id
                            else self._model_id or ""
                        ),
                        "metadata": {
                            "model": self._model_id,
                            "provider_type": self._provider_type,
                        },
                        "datasetItemId": dataset_item_id,
                        "traceId": trace_id,
                    },
                )
                r.raise_for_status()
        except Exception as exc:
            print(f"warning: Langfuse dataset-run-item failed for item '{report.id}': {exc}", file=sys.stderr)

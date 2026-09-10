# (C) 2026 GoodData Corporation
"""Langfuse scoring sink — writes single-shot evaluation results as Langfuse experiments over OTLP."""

from __future__ import annotations

import os
import sys
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Any

from gooddata_eval.core.langfuse.client import HttpxLangfuseClient
from gooddata_eval.core.langfuse.experiment import ExperimentItem, ExperimentRun, build_experiment_root_span

_MAX_LATENCY_S = 60.0
_QUALITY_WEIGHT = 0.6
_SPEED_WEIGHT = 0.2

if TYPE_CHECKING:
    import httpx

    from gooddata_eval.core.config import ReasoningEffort
    from gooddata_eval.core.langfuse.otlp import Span
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
    """Writes evaluation results to Langfuse as an experiment root span plus four scores."""

    def __init__(
        self,
        dataset_name: str,
        run_name: str,
        model_id: str = "",
        provider_type: str = "",
        reasoning_effort: ReasoningEffort | None = None,
        *,
        transport: httpx.BaseTransport | None = None,
    ):
        self._dataset_name = dataset_name
        self._run_name = run_name
        self._model_id = model_id
        self._provider_type = provider_type
        self._reasoning_effort = reasoning_effort
        self._client = HttpxLangfuseClient(timeout=10.0, transport=transport)
        self._warned_unlinkable = False

    def _resolve_run(self, report: ItemReport, dataset_item_id: str) -> ExperimentRun | None:
        """The experiment this item belongs to, or None when it cannot be assembled.

        A lookup exception is reported every time (it may be transient); the item genuinely
        not being a Langfuse dataset item is reported once per sink, since it recurs
        identically for every item of the same --dataset.
        """
        dataset_id: str | None = None
        try:
            dataset_id = self._client.dataset_id_for_item(dataset_item_id)
        except Exception as exc:
            print(f"warning: Langfuse dataset item lookup failed for item '{report.id}': {exc}", file=sys.stderr)
            return None
        if dataset_id is None:
            if not self._warned_unlinkable:
                self._warned_unlinkable = True
                print(
                    f"warning: Langfuse dataset item '{dataset_item_id}' not found; "
                    f"run '{self._run_name}' is not assembled as an experiment",
                    file=sys.stderr,
                )
            return None
        description = (
            f"{self._provider_type}/{self._model_id}"
            if self._provider_type and self._model_id
            else self._model_id or None
        )
        return ExperimentRun(
            self._run_name,
            dataset_id,
            {
                "model": self._model_id,
                "provider_type": self._provider_type,
                "reasoning_effort": self._reasoning_effort,
            },
            description=description,
        )

    def _build_span(self, report: ItemReport, dataset_item_id: str, run: ExperimentRun | None) -> Span:
        end = datetime.now(timezone.utc)
        start = end - timedelta(seconds=report.avg_latency_s)
        # "gd-eval" leads, exactly as on the agentic path, so one tag filter in Langfuse
        # finds both single-shot and agentic traces this package wrote.
        tags = tuple(
            t
            for t in (
                "gd-eval",
                report.test_kind,
                self._provider_type,
                f"effort-{self._reasoning_effort.lower()}" if self._reasoning_effort else None,
            )
            if t
        )
        return build_experiment_root_span(
            run,
            ExperimentItem(
                dataset_item_id,
                input={"question": report.question},
                output=report.best_detail,
                metadata={"test_kind": report.test_kind},
            ),
            start=start,
            end=end,
            trace_name=f"gd-eval: {report.question[:80]}",
            version=self._model_id or None,
            tags=tags,
            trace_metadata={
                "dataset_name": report.dataset_name,
                "test_kind": report.test_kind,
                "item_id": report.id,
                "model": self._model_id,
                "provider_type": self._provider_type,
                "reasoning_effort": self._reasoning_effort,
            },
            environment=os.environ.get("LANGFUSE_TRACING_ENVIRONMENT"),
        )

    def log_item(self, report: ItemReport, *, dataset_item_id: str) -> None:
        """Export one experiment root span plus its four scores for an evaluated item.

        Swallows all errors — Langfuse failures never abort the eval run.
        """
        scores = compute_scores(
            pass_at_k=report.pass_at_k,
            avg_latency_s=report.avg_latency_s,
            best_detail=report.best_detail,
        )
        run = self._resolve_run(report, dataset_item_id)
        span = self._build_span(report, dataset_item_id, run)

        try:
            self._client.export_spans([span])
        except Exception as exc:
            print(f"warning: Langfuse span export failed for item '{report.id}': {exc}", file=sys.stderr)
            return

        score_defs = [
            ("pass_at_k", scores["pass_at_k"], "BOOLEAN"),
            ("quality_score", scores["quality_score"], "NUMERIC"),
            ("value_score", scores["value_score"], "NUMERIC"),
            ("latency_s", scores["latency_s"], "NUMERIC"),
        ]
        for name, value, data_type in score_defs:
            try:
                self._client.create_score(
                    trace_id=span.trace_id,
                    observation_id=span.span_id,
                    name=name,
                    value=value,
                    data_type=data_type,
                )
            except Exception as exc:  # noqa: PERF203 — one score's failure must not skip the rest
                print(f"warning: Langfuse score '{name}' failed for item '{report.id}': {exc}", file=sys.stderr)

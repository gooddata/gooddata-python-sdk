# (C) 2026 GoodData Corporation. All rights reserved.
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CatalogMetricAlert:
    """Eval fixture schema for create_metric_alert tool arguments.

    This is an eval-specific type, not a gooddata-sdk API entity. It holds the
    flat expected output from a YAML fixture and is never serialised to the API.
    """

    operator: str = "GREATER_THAN"
    """Comparison operator: GREATER_THAN, LESS_THAN, EQUAL_TO, BETWEEN, NOT_BETWEEN."""
    threshold: float | int | None = None
    """Threshold value for single-sided operators (GREATER_THAN, LESS_THAN, EQUAL_TO)."""
    threshold_from: float | int | None = None
    """Lower bound for BETWEEN / NOT_BETWEEN operators."""
    threshold_to: float | int | None = None
    """Upper bound for BETWEEN / NOT_BETWEEN operators."""
    trigger: str = "not specified"
    """Alert trigger mode: ALWAYS, ONCE, or 'not specified' (defaults to ALWAYS)."""
    metric_id: str | None = None
    """Identifier of the metric the alert monitors."""
    recipients: list[str] = field(default_factory=list)
    """List of recipient email addresses."""
    filters: list | str | None = None
    """Attribute filters applied to the alert condition."""

    @classmethod
    def from_dict(cls, d: dict) -> CatalogMetricAlert:
        """Build a CatalogMetricAlert from a canonical (lowercase-key) dict."""
        recipients_raw = d.get("recipients") or []
        if isinstance(recipients_raw, str):
            recipients = [r.strip() for r in recipients_raw.replace(";", ",").split(",") if r.strip()]
        else:
            recipients = list(recipients_raw)
        return cls(
            operator=d.get("operator", "GREATER_THAN"),
            threshold=d.get("threshold"),
            threshold_from=d.get("threshold_from"),
            threshold_to=d.get("threshold_to"),
            trigger=d.get("trigger", "not specified"),
            metric_id=d.get("metric_id"),
            recipients=recipients,
            filters=d.get("filters"),
        )

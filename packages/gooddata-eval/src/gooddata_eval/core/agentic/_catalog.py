# (C) 2026 GoodData Corporation. All rights reserved.
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class AnomalyDetectionGranularity(str, Enum):
    """Detection intervals an anomaly alert accepts.

    Mirrors gen-ai's enum of the same name; `StrEnum` is unavailable on the 3.10 floor, so
    the `str` mixin carries the comparison against the raw tool argument.
    """

    HOUR = "HOUR"
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
    QUARTER = "QUARTER"
    YEAR = "YEAR"

    @classmethod
    def parse(cls, value: object) -> AnomalyDetectionGranularity | None:
        """Coerce a fixture value, or None when the fixture states none.

        Raises ValueError on an unknown interval: fixtures are hand-written, and a typo has
        to fail before the run spends an API call rather than score the item against an
        interval the product cannot produce.
        """
        if value is None:
            return None
        candidate = str(value).strip().upper()
        if not candidate:
            return None
        try:
            return cls(candidate)
        except ValueError:
            expected = ", ".join(member.value for member in cls)
            raise ValueError(f"Invalid granularity {value!r}; expected one of {expected}.") from None


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
    attributes: list | None = None
    """Expected group-by attributes; ``None`` means the fixture states no expectation."""
    granularity: AnomalyDetectionGranularity | None = None
    """Detection interval for an ANOMALY alert (DAY/WEEK/MONTH/...). Not a date filter."""
    comparison: dict[str, str | int | float | None] | None = None
    """Expected period comparison as ``create_metric_alert`` argument names; ``None`` means unasserted."""
    title: str | None = None
    """Alert name the user asked for; ``None`` means unasserted."""
    dashboard_id: str | None = None
    """Dashboard the alert must be bound to; ``None`` means unasserted."""
    expect_alert: bool = True
    """``False``: the request names nothing the alert can monitor, so no alert may be proposed or created."""
    sensitivity: str | None = None
    """ANOMALY sensitivity (LOW/MEDIUM/HIGH); ``None`` means unasserted."""
    trigger_interval: str | None = None
    """Interval of a ONCE_PER_INTERVAL trigger (DAY/WEEK/MONTH/QUARTER/YEAR); ``None`` means unasserted."""
    date_dataset_id: str | None = None
    """Date dataset an ANOMALY alert detects on; ``None`` means unasserted."""
    setup_turns: tuple[str, ...] = ()
    """Messages sent in the same conversation before the question, not scored."""
    alternatives: tuple[CatalogMetricAlert, ...] = ()
    """Complete expectations any one of which passes (``any_of``); empty means this one alone."""
    check_first_proposal: tuple[str, ...] = ()
    """Fields (``filters``, ``recipients``) also scored on the first proposal, before the simulated user replies."""

    @classmethod
    def from_dict(cls, d: dict) -> CatalogMetricAlert:
        """Build a CatalogMetricAlert with the parsing and validation a dataset item's expected_output gets."""
        # Imported here: alert_skill imports this module.
        from gooddata_eval.core.agentic.alert_skill import _normalize_expected_output  # noqa: PLC0415

        return _normalize_expected_output(d)

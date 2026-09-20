# (C) 2026 GoodData Corporation
"""What a validation run has to say: one finding per problem, collected into a report."""

from __future__ import annotations

import enum
from typing import Any

from attrs import define, field


class Severity(enum.Enum):
    """How much a finding is worth acting on.

    The split is not about how serious the consequence is -- it is about how certain the
    SDK can be that something is wrong.

    ``ERROR`` is reserved for things that are broken no matter how the visualization
    format evolves: a sort that points at a bucket item which does not exist is wrong
    today and stays wrong when a new chart type ships next month.

    ``WARNING`` covers everything the SDK merely does not recognise -- a chart type or a
    bucket name outside the sets it knows. Those sets are a snapshot of a format owned
    elsewhere, so an unrecognised value far more often means "this SDK is older than
    your platform" than "your content is broken". Refusing on that basis would make
    every new chart type an SDK bug, which is why it never rises above a warning.
    """

    ERROR = "error"
    WARNING = "warning"

    def __str__(self) -> str:
        return self.value


@define(kw_only=True, frozen=True)
class Finding:
    """One problem found in one object.

    Attributes:
        severity: see :class:`Severity` -- whether this is provably wrong or merely unrecognised.
        code: stable machine-readable identifier, e.g. ``"dangling_local_id"``. Callers filter
            and suppress on this, so it is part of the API and does not change with wording.
        message: what is wrong, in a sentence, naming the offending value.
        object_id: id of the object the finding belongs to, when known.
        location: where inside the object, as a dotted/indexed path -- ``"content.sorts[0]"``.
            Pointing at the exact element is most of what makes a finding actionable.
    """

    severity: Severity
    code: str
    message: str
    object_id: str | None = None
    location: str | None = None

    def __str__(self) -> str:
        where = " ".join(part for part in (self.object_id, self.location) if part)
        return f"{self.severity}: {self.message}" + (f" [{where}]" if where else "")


@define(kw_only=True)
class ValidationReport:
    """Findings from validating one or more objects.

    Truthiness follows ``ok``: a report with only warnings is still a pass, so
    ``if not report:`` reads as "something is provably broken" rather than "something was
    mentioned". Warnings are advisory by construction (see :class:`Severity`) and must not
    fail a caller that treats the report as a boolean.
    """

    findings: list[Finding] = field(factory=list)

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.severity is Severity.ERROR]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity is Severity.WARNING]

    @property
    def ok(self) -> bool:
        """True when nothing is provably broken. Warnings do not make a report fail."""
        return not self.errors

    def __bool__(self) -> bool:
        return self.ok

    def __len__(self) -> int:
        return len(self.findings)

    def extend(self, findings: list[Finding]) -> ValidationReport:
        """Add findings in place and return self, so builders can chain."""
        self.findings.extend(findings)
        return self

    def raise_for_errors(self) -> None:
        """Raise :class:`ValidationError` when anything is provably broken; warnings pass."""
        if not self.ok:
            raise ValidationError(self)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "findings": [
                {
                    "severity": str(f.severity),
                    "code": f.code,
                    "message": f.message,
                    "objectId": f.object_id,
                    "location": f.location,
                }
                for f in self.findings
            ],
        }

    def format(self) -> str:
        """Human-readable summary, errors first. Empty report renders as a single OK line."""
        if not self.findings:
            return "OK: no findings."
        lines = [str(f) for f in self.errors] + [str(f) for f in self.warnings]
        lines.append(f"{len(self.errors)} error(s), {len(self.warnings)} warning(s).")
        return "\n".join(lines)


class ValidationError(Exception):
    """Raised by :meth:`ValidationReport.raise_for_errors`.

    Its own type, deliberately: a caller that opts into validation has to be able to tell a
    rejected object from a failed HTTP call, and catching the SDK's transport errors must
    never swallow this.
    """

    def __init__(self, report: ValidationReport) -> None:
        self.report = report
        super().__init__(report.format())

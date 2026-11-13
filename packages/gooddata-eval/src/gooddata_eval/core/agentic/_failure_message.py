# (C) 2026 GoodData Corporation
"""The head of an agentic kind's failure message: the gate result, then every failing run.

Each kind's assertion message describes its BEST run, which on a partial gate failure (some
of the K runs passed) is a passing run: every check reads True and the reason the item
failed is nowhere in the message. This module renders the part that is missing -- for each
failing run its index, why its loop stopped and the checks it failed, with expected/actual
where the kind knows them -- from the same ``failed_runs`` records the item reports, so the
message and the triage data cannot disagree about which runs failed or why.

One renderer for every kind on purpose: the readers of these messages (people and the
triage tooling) look for one shape, whatever the capability under test.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Any

__all__ = ["FailedCheck", "cap_failed_checks", "failed_check_records", "failing_runs_note", "failure_head"]

# A value longer than this is cut: the message is one line per run, and the whole value is in
# the run's detail anyway.
_MAX_VALUE_CHARS = 160


class _Unset(Enum):
    UNSET = "unset"


_UNSET = _Unset.UNSET


@dataclass(frozen=True)
class FailedCheck:
    """One check a run failed, with the expected/actual pair when the kind knows it.

    ``label`` narrows the check when one name covers several parts, e.g. the ``date`` part of
    ``filters_correct``.
    """

    name: str
    expected: Any = _UNSET
    actual: Any = _UNSET
    label: str | None = None

    def as_record(self) -> dict[str, Any]:
        """The JSON-ready form written into a failing run's ``failed_checks``."""
        record: dict[str, Any] = {"name": self.name}
        if self.label is not None:
            record["label"] = self.label
        if self.expected is not _UNSET:
            record["expected"] = self.expected
        if self.actual is not _UNSET:
            record["actual"] = self.actual
        return record


def failed_check_records(checks: Iterable[FailedCheck]) -> list[dict[str, Any]]:
    """``checks`` as the records ``failed_runs[].failed_checks`` holds."""
    return [check.as_record() for check in checks]


def _text(value: Any) -> str:
    text = value if isinstance(value, str) else json.dumps(value, default=str, ensure_ascii=False, sort_keys=True)
    return " ".join(text.split())


def _value(value: Any) -> str:
    if value is None or value == [] or value == {} or value == "":
        return "none"
    text = _text(value)
    return text if len(text) <= _MAX_VALUE_CHARS else text[: _MAX_VALUE_CHARS - 3] + "..."


def cap_failed_checks(records: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """``records`` with every expected/actual value cut to what the message shows of it.

    A check's values can be whole filter or bucket structures, repeated for every failing run
    of every item; the record keeps the same ``_MAX_VALUE_CHARS`` the message does. A value
    that fits stays as it is, JSON and all; a longer one becomes its cut text. The run's
    ``detail`` holds the full values.
    """
    capped: list[dict[str, Any]] = []
    for record in records:
        entry = dict(record)
        for key in ("expected", "actual"):
            if key in entry and len(_text(entry[key])) > _MAX_VALUE_CHARS:
                entry[key] = _value(entry[key])
        capped.append(entry)
    return capped


def _render_check(record: Mapping[str, Any]) -> str:
    name = str(record.get("name", "?"))
    parts: list[str] = []
    if "expected" in record:
        parts.append(f"expected {_value(record['expected'])}")
    if "actual" in record:
        parts.append(f"actual {_value(record['actual'])}")
    label = record.get("label")
    if not parts and label is None:
        return name
    inner = ", ".join(parts)
    if label is not None:
        inner = f"{label}: {inner}" if inner else str(label)
    return f"{name}[{inner}]"


def _render_run(record: Mapping[str, Any], runs_total: int) -> str:
    outcome = record.get("outcome")
    status = "FAIL"
    if isinstance(outcome, Mapping) and outcome.get("status") == "error":
        status = f"ERROR {outcome.get('source') or ''}".rstrip()
    exit_reason = record.get("exit_reason")
    head = f"run {record.get('run_index', '?')}/{runs_total} {status}"
    if exit_reason:
        head += f" (loop exit: {exit_reason})"
    checks = record.get("failed_checks")
    if checks:
        return f"{head}: {', '.join(_render_check(c) for c in checks)}"
    if checks is not None:
        return f"{head}: no failing check recorded"
    return head


def failing_runs_note(failed_runs: Sequence[Mapping[str, Any]], runs_total: int) -> str:
    """Every failing run on one line each, joined with ``; ``. Empty when no run failed."""
    return "; ".join(_render_run(record, runs_total) for record in failed_runs)


def failure_head(gate_note: str, failed_runs: Sequence[Mapping[str, Any]], runs_total: int) -> str:
    """``gate_note`` followed by the failing runs, ready to start a kind's assertion message.

    Returns ``gate_note`` unchanged when there is no failing run to list, so a kind that
    builds no ``failed_runs`` keeps its message exactly as before.
    """
    note = failing_runs_note(failed_runs, runs_total)
    return f"{gate_note} Failing runs: {note}." if note else gate_note

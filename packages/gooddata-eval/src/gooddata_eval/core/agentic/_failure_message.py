# (C) 2026 GoodData Corporation
"""The head of an agentic kind's failure message: the gate result, then every failing run.

Each kind's assertion message describes its BEST run, which on a partial gate failure (some
of the K runs passed) is a passing run: every check reads True and the reason the item
failed is nowhere in the message. This module renders the part that is missing -- for each
failing run its index, why its loop stopped and the checks it failed, with expected/actual
where the kind knows them -- from the same ``failed_runs`` records the item reports, so the
message and the triage data cannot disagree about which runs failed or why.

One renderer for every kind that labels its runs, on purpose: the readers of these messages
(people and the triage tooling) look for one shape, whatever the capability under test.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Any

from gooddata_eval.core.outcome import UNKNOWN_REASON, OutcomeStatus

__all__ = [
    "FailedCheck",
    "cap_failed_checks",
    "failed_check_records",
    "failed_checks_from",
    "failing_runs_note",
    "failure_head",
    "judge_failed_checks",
]

# A value longer than this is cut: the message is one line per run, and the whole value is in
# the run's detail anyway.
_MAX_VALUE_CHARS = 160

# The failing runs together are cut past this, at a run boundary: K runs of a kind with a dozen
# checks would otherwise put tens of thousands of characters into one assertion message. Every
# run is in ``failed_runs`` whatever the message shows.
_MAX_FAILING_RUNS_CHARS = 2000


class _Unset(Enum):
    UNSET = "unset"


_UNSET = _Unset.UNSET


@dataclass(frozen=True)
class FailedCheck:
    """One check a run failed, with the expected/actual pair when the kind knows it.

    ``part`` narrows the check when one name covers several parts, e.g. the ``date`` part of
    ``filters_correct``.
    """

    name: str
    expected: Any = _UNSET
    actual: Any = _UNSET
    part: str | None = None

    def as_record(self) -> dict[str, Any]:
        """The JSON-ready form written into a failing run's ``failed_checks``."""
        record: dict[str, Any] = {"name": self.name}
        if self.part is not None:
            record["part"] = self.part
        if self.expected is not _UNSET:
            record["expected"] = self.expected
        if self.actual is not _UNSET:
            record["actual"] = self.actual
        return record


def failed_check_records(checks: Iterable[FailedCheck]) -> list[dict[str, Any]]:
    """``checks`` as the records ``failed_runs[].failed_checks`` holds."""
    return [check.as_record() for check in checks]


def failed_checks_from(checks: Mapping[str, bool], *, prerequisite: str | None = None) -> list[dict[str, Any]]:
    """The records of the checks in ``checks`` that read False, by name, in their order.

    ``prerequisite`` names the check every other one depends on, e.g. ``alert_created``. When it
    failed, the others read False only because there was nothing to check, so it alone is named.
    """
    if prerequisite is not None and checks.get(prerequisite) is False:
        return failed_check_records([FailedCheck(prerequisite)])
    return failed_check_records(FailedCheck(name) for name, ok in checks.items() if not ok)


def judge_failed_checks(name: str, *, passed: bool, judge_error: str | None, reasoning: Any) -> list[dict[str, Any]]:
    """The judge's verdict ``name`` on a run it failed, with its reasoning as the actual value.

    Empty when the judge passed the run, or could not grade it: a run with no verdict failed no
    judge check.
    """
    if judge_error is not None or passed:
        return []
    return failed_check_records([FailedCheck(name, part="judge", actual=reasoning)])


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
    part = record.get("part")
    if not parts and part is None:
        return name
    inner = ", ".join(parts)
    if part is not None:
        inner = f"{part}: {inner}" if inner else str(part)
    return f"{name}[{inner}]"


def _render_run(record: Mapping[str, Any], runs_total: int) -> str:
    outcome = record.get("outcome")
    head = f"run {record.get('run_index', '?')}/{runs_total}"
    exit_reason = record.get("exit_reason")
    errored = isinstance(outcome, Mapping) and outcome.get("status") == OutcomeStatus.ERROR.value
    if errored:
        # A harness error: the reason (simulated_user_failed, judge_failed) is the diagnosis.
        # Its checks are still listed: the simulated user is also asked after an answer that
        # was already final, and what that answer missed is the only way to tell.
        head += f" ERROR ({outcome.get('reason') or UNKNOWN_REASON})"
    else:
        head += " FAIL" + (f" (loop exit: {exit_reason})" if exit_reason else "")
    checks = record.get("failed_checks")
    if checks:
        return f"{head}: {', '.join(_render_check(c) for c in checks)}"
    if checks is not None and not errored:
        return f"{head}: no failing check recorded"
    return head


def failing_runs_note(failed_runs: Sequence[Mapping[str, Any]], runs_total: int) -> str:
    """Every failing run, joined with ``; ``. Empty when no run failed.

    Past ``_MAX_FAILING_RUNS_CHARS`` the runs left are counted instead of rendered. The first
    run is always shown, cut to that length if it alone is longer.
    """
    shown: list[str] = []
    length = 0
    for index, record in enumerate(failed_runs):
        text = _render_run(record, runs_total)
        if shown and length + len("; ") + len(text) > _MAX_FAILING_RUNS_CHARS:
            more = len(failed_runs) - index
            shown.append(f"{more} more failing run(s) in failed_runs")
            break
        if not shown and len(text) > _MAX_FAILING_RUNS_CHARS:
            text = text[: _MAX_FAILING_RUNS_CHARS - 3] + "..."
        shown.append(text)
        length += len(text) + (len("; ") if len(shown) > 1 else 0)
    return "; ".join(shown)


def failure_head(gate_note: str, failed_runs: Sequence[Mapping[str, Any]], runs_total: int) -> str:
    """``gate_note`` followed by the failing runs, ready to start a kind's assertion message.

    Returns ``gate_note`` unchanged when there is no failing run to list, which is the whole
    head of a kind that builds no ``failed_runs``.
    """
    note = failing_runs_note(failed_runs, runs_total)
    return f"{gate_note} Failing runs: {note}." if note else gate_note

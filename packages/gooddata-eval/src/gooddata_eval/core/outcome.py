# (C) 2026 GoodData Corporation
"""One label per run: PASS, FAIL, or ERROR when the test harness, not the agent, failed.

A run can end in a way that is the harness's fault: the simulated user's own model call
fails, or the judge cannot grade the answer. Scored as usual, such a run reads as an agent
failure. ``classify_run`` names the difference, in one place for every kind.

The labels decide no verdict. A run labelled ERROR still counts as a run that did not pass,
so a gate, a pass rate or a trend reads the same with or without them. The labels only tell
a reader why a run did not pass. ``shadow_verdict`` records what a candidate rule that leaves
ERROR runs out of the gate would have given, so that rule can be judged on real nights
before anyone adopts it.

The rule is fail-closed. A run is ERROR only for a cause on ``_ERROR_EXITS`` or a judge
failure that left the run without a verdict, causes a customer would not hit. That is not
proof the agent was blameless: the simulated user is also asked after an answer that was
already final, so an ERROR run still lists the checks it failed. Anything else, including a
chat API error and an unknown exit, is FAIL.

An item can also be ERROR before its first run: a kind that prepares its own input (it runs the
stored executions of a dashboard's widgets) could not prepare it, for a cause on ``SETUP_ERRORS``.
No chat is sent then, so there is no run to label; ``setup_error`` is that item's outcome.
"""

from __future__ import annotations

import math
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Any

from gooddata_eval.core.config import normalize_gate
from gooddata_eval.core.models import LoopExit

__all__ = [
    "EVAL_ERROR_SCORE",
    "JUDGE_FAILED",
    "Outcome",
    "OutcomeStatus",
    "SETUP_ERRORS",
    "SHADOW_MIN_SCORED_SHARE",
    "UNKNOWN_REASON",
    "classify_run",
    "item_outcome",
    "setup_error",
    "shadow_verdict",
]


class OutcomeStatus(str, Enum):
    """What one run, or one item, amounts to."""

    PASS = "pass"
    FAIL = "fail"
    ERROR = "error"
    """The test harness failed, so the run says nothing about the agent."""


@dataclass(frozen=True)
class Outcome:
    """A status and a machine-readable reason, e.g. ``simulated_user_failed``."""

    status: OutcomeStatus
    reason: str | None = None

    @classmethod
    def passed(cls) -> Outcome:
        return cls(OutcomeStatus.PASS)

    @classmethod
    def failed(cls, reason: str | None = None) -> Outcome:
        return cls(OutcomeStatus.FAIL, reason)

    @classmethod
    def error(cls, reason: str) -> Outcome:
        return cls(OutcomeStatus.ERROR, reason)

    @property
    def is_error(self) -> bool:
        return self.status is OutcomeStatus.ERROR

    def as_record(self) -> dict[str, Any]:
        """The JSON-ready form written into ``failed_runs[].outcome`` and onto the exception."""
        return {"status": self.status.value, "reason": self.reason}


EVAL_ERROR_SCORE = "eval_error"
"""The extra Langfuse score (NUMERIC, 1) an ERROR run gets, its comment the reason. The
run's other scores are written as always."""

JUDGE_FAILED = "judge_failed"
"""The reason of a run the judge or scorer could not grade."""

DATA_BASELINE_CHANGED = "data_baseline_changed"
"""The data under the item differs from the baseline the item stores."""

WIDGET_EXECUTION_FAILED = "widget_execution_failed"
"""A stored widget execution of the item could not be run, or its result could not be read."""

SETUP_ERRORS: frozenset[str] = frozenset({DATA_BASELINE_CHANGED, WIDGET_EXECUTION_FAILED})
"""The only causes that make an item an ERROR before any run. Like ``_ERROR_EXITS`` they are on the
harness path: the agent was never asked."""

UNKNOWN_REASON = "unknown"
"""The reason shown for an ERROR that carries none."""

SHADOW_MIN_SCORED_SHARE = 0.5
"""The share of an item's K runs the candidate rule needs scored, rounded up, before it judges
the item: ceil(K/2). A placeholder until real nights say what it should be."""

# The only loop exits that make a run an ERROR. A chat API error stays a FAIL: it is on the
# product path, and a customer would hit it too.
_ERROR_EXITS: frozenset[LoopExit] = frozenset({LoopExit.SIMULATED_USER_FAILED})


def classify_run(exit_reason: LoopExit | str | None, *, passed: bool, judge_error: str | None = None) -> Outcome:
    """The label of one run, from whether it passed, why its loop stopped and its judge.

    A run that passed is PASS whatever its exit: its checks held on what the agent produced.
    A run whose judge failed is ERROR (``judge_failed``). The caller passes ``judge_error`` only
    when the judge's verdict was the one still open: a run that already failed another check is
    a FAIL whatever the judge would have said. A run is ERROR too when its exit is on
    ``_ERROR_EXITS``. Every other run is FAIL, its reason the exit (or None for a kind whose
    loop records none). An exit string that is not a ``LoopExit`` value is kept as the reason
    of a FAIL rather than raising: an unknown cause is never an error.
    """
    if passed:
        return Outcome.passed()
    if judge_error is not None:
        return Outcome.error(JUDGE_FAILED)
    loop_exit: LoopExit | None
    if isinstance(exit_reason, LoopExit) or exit_reason is None:
        loop_exit = exit_reason
    else:
        try:
            loop_exit = LoopExit(exit_reason)
        except ValueError:
            return Outcome.failed(exit_reason)
    if loop_exit in _ERROR_EXITS:
        return Outcome.error(loop_exit.value)
    return Outcome.failed(loop_exit.value if loop_exit is not None else None)


def setup_error(reason: str) -> Outcome:
    """The outcome of an item whose input could not be prepared, so that no run happened.

    Raises:
        ValueError: ``reason`` is not on ``SETUP_ERRORS``: a new cause is added there on purpose.
    """
    if reason not in SETUP_ERRORS:
        raise ValueError(f"{reason!r} is not a setup error; known: {sorted(SETUP_ERRORS)}")
    return Outcome.error(reason)


def item_outcome(outcomes: Sequence[Outcome]) -> Outcome | None:
    """ERROR when every run of the item is ERROR, with the most frequent reason; else None.

    Of reasons equally frequent, the alphabetically first is named, so the label is stable.

    None means the item keeps the verdict its gate gave it. An item with some ERROR runs is
    not an ERROR: its other runs were scored, and its message names the ERROR runs.
    """
    if not outcomes or not all(o.is_error for o in outcomes):
        return None
    reasons = Counter(o.reason or UNKNOWN_REASON for o in outcomes)
    return Outcome.error(max(sorted(reasons), key=lambda reason: reasons[reason]))


def shadow_verdict(outcomes: Sequence[Outcome], gate: str | None) -> dict[str, Any]:
    """What the candidate phase-2 rule would give this item. Recorded, never used.

    The rule leaves ERROR runs out of K. With fewer scored runs left than
    ``SHADOW_MIN_SCORED_SHARE`` of K the item is ``error``; otherwise ``gate`` is applied to
    the scored runs. The verdict is an ``OutcomeStatus`` value.
    """
    scored = [o for o in outcomes if not o.is_error]
    passes = sum(1 for o in scored if o.status is OutcomeStatus.PASS)
    if not scored or len(scored) < math.ceil(len(outcomes) * SHADOW_MIN_SCORED_SHARE):
        verdict = OutcomeStatus.ERROR
    elif normalize_gate(gate) == "power":
        verdict = OutcomeStatus.PASS if passes == len(scored) else OutcomeStatus.FAIL
    else:
        verdict = OutcomeStatus.PASS if passes else OutcomeStatus.FAIL
    return {"verdict": verdict.value, "runs_scored": len(scored), "runs_total": len(outcomes)}

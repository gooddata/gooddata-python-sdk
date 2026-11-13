# (C) 2026 GoodData Corporation
"""One outcome per run: PASS, FAIL, or ERROR when the run says nothing about the agent.

A run of an agentic kind can end in a way that is the harness's or the platform's fault,
not the agent's: the simulated user's own model call fails, or the chat call still fails
after its retries. Scored as usual, such a run reads as an agent failure. ``Outcome`` names
the difference, and ``outcome_from_loop_exit`` is the one place a ``LoopExit`` is mapped to
it, for every kind.

The mapping is always computed and always recorded in ``failed_runs[].outcome``. It decides
a verdict only when ``GD_EVAL_ERROR_OUTCOME`` is on (``error_outcome_enabled``); see
``gate_outcomes`` for what changes then. Off, every verdict is the one the kind computed
before this module existed.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from gooddata_eval.core.config import error_outcome_enabled, normalize_gate
from gooddata_eval.core.models import EvalHarnessError, LoopExit

__all__ = [
    "EVAL_ERROR_SCORE",
    "ErrorSource",
    "EvalHarnessError",
    "GateVerdict",
    "Outcome",
    "OutcomeStatus",
    "error_outcome_enabled",
    "excluded_runs_note",
    "gate_outcomes",
    "outcome_from_loop_exit",
]


class OutcomeStatus(str, Enum):
    """What one run, or one item, amounts to."""

    PASS = "pass"
    FAIL = "fail"
    ERROR = "error"
    """Says nothing about the agent: the run is not scored."""


class ErrorSource(str, Enum):
    """Whose fault an ERROR is."""

    HARNESS = "harness"
    """gooddata-eval itself, e.g. its simulated user."""

    INFRA = "infra"
    """Something between the eval and the platform: tracing, obfuscation, the network."""

    BACKEND = "backend"
    """The GoodData side answered with an error after every retry."""


@dataclass(frozen=True)
class Outcome:
    """PASS, FAIL with an optional reason, or ERROR with its source and reason."""

    status: OutcomeStatus
    source: ErrorSource | None = None
    reason: str | None = None

    @classmethod
    def passed(cls) -> Outcome:
        return cls(OutcomeStatus.PASS)

    @classmethod
    def failed(cls, reason: str | None = None) -> Outcome:
        return cls(OutcomeStatus.FAIL, reason=reason)

    @classmethod
    def error(cls, source: ErrorSource, reason: str) -> Outcome:
        return cls(OutcomeStatus.ERROR, source=source, reason=reason)

    @property
    def is_scored(self) -> bool:
        """Whether the run counts towards the gate's K."""
        return self.status is not OutcomeStatus.ERROR

    def as_record(self) -> dict[str, Any]:
        """The JSON-ready form written into ``failed_runs[].outcome``."""
        return {
            "status": self.status.value,
            "source": self.source.value if self.source is not None else None,
            "reason": self.reason,
        }


EVAL_ERROR_SCORE = "eval_error"
"""The Langfuse score (NUMERIC, 1) an ERROR run or errored item gets instead of any verdict
score, with ``GD_EVAL_ERROR_OUTCOME`` on. Readers of the experiment rely on the name."""


# Every LoopExit that makes a run an ERROR, with its source and reason. A member not listed
# here ends a run the agent is accountable for, which is then scored as PASS or FAIL.
_ERROR_EXITS: dict[LoopExit, tuple[ErrorSource, str]] = {
    LoopExit.SIMULATED_USER_FAILED: (ErrorSource.HARNESS, "the simulated user failed to reply"),
    LoopExit.CHAT_ERROR: (ErrorSource.BACKEND, "the chat call failed after its retries"),
    LoopExit.NOT_RUN: (ErrorSource.HARNESS, "the run never started"),
}


def outcome_from_loop_exit(exit_reason: LoopExit | str | None, *, passed: bool) -> Outcome:
    """The outcome of one run, from why its loop stopped and whether it passed its checks.

    ``SUCCESS``, ``BUDGET_EXHAUSTED``, ``AGENT_SILENT``, ``AGENT_TIMEOUT`` and
    ``TURN_INCOMPLETE`` are scored: PASS or FAIL.
    ``SIMULATED_USER_FAILED`` and ``NOT_RUN`` are ERROR(harness), ``CHAT_ERROR`` is
    ERROR(backend). ``None`` (a kind whose loop records no exit) is scored.

    A run that passed is PASS whatever its exit: its checks held on what the agent produced,
    so the run is evidence about the agent even when the conversation ended abnormally.

    Raises:
        ValueError: ``exit_reason`` is a string that is not a ``LoopExit`` value.
    """
    if passed:
        return Outcome.passed()
    loop_exit = LoopExit(exit_reason) if isinstance(exit_reason, str) else exit_reason
    error = _ERROR_EXITS.get(loop_exit) if loop_exit is not None else None
    if error is not None:
        return Outcome.error(*error)
    return Outcome.failed(f"loop exit: {loop_exit.value}" if loop_exit is not None else None)


@dataclass(frozen=True)
class GateVerdict:
    """An item's verdict over its runs' outcomes, ERROR runs left out of K."""

    outcome: Outcome
    """PASS or FAIL from the gate over the scored runs; ERROR when no run was scored."""
    runs_total: int
    runs_scored: int
    runs_passed: int
    pass_at_k: bool
    pass_power_k: bool
    excluded: tuple[tuple[int, Outcome], ...] = field(default=())
    """``(run_index, outcome)`` of every ERROR run, 1-based, in run order."""


def gate_outcomes(outcomes: Sequence[Outcome], gate: str | None) -> GateVerdict:
    """Apply ``gate`` to the scored runs only.

    ERROR runs are left out of K: ``[ERROR, PASS, PASS]`` under pass^K is pass^2 over the two
    scored runs. With no scored run left the item is ERROR, whatever the gate.
    """
    excluded = tuple((index, o) for index, o in enumerate(outcomes, start=1) if not o.is_scored)
    scored = [o for o in outcomes if o.is_scored]
    runs_passed = sum(1 for o in scored if o.status is OutcomeStatus.PASS)
    pass_at_k = runs_passed > 0
    pass_power_k = bool(scored) and runs_passed == len(scored)
    if not scored:
        reasons = "; ".join(sorted({o.reason or "" for _, o in excluded}))
        item = Outcome.error(_dominant_source(excluded), f"no scored run: {reasons}")
    elif pass_power_k if normalize_gate(gate) == "power" else pass_at_k:
        item = Outcome.passed()
    else:
        item = Outcome.failed()
    return GateVerdict(
        outcome=item,
        runs_total=len(outcomes),
        runs_scored=len(scored),
        runs_passed=runs_passed,
        pass_at_k=pass_at_k,
        pass_power_k=pass_power_k,
        excluded=excluded,
    )


def _dominant_source(excluded: Sequence[tuple[int, Outcome]]) -> ErrorSource:
    counts = Counter(o.source for _, o in excluded if o.source is not None)
    return counts.most_common(1)[0][0] if counts else ErrorSource.HARNESS


def excluded_runs_note(verdict: GateVerdict) -> str:
    """E.g. ``1 run excluded (harness error): run 1/3 the simulated user failed to reply.``

    Empty when no run was excluded.
    """
    if not verdict.excluded:
        return ""
    sources = Counter(o.source.value if o.source is not None else "unknown" for _, o in verdict.excluded)
    if len(sources) == 1:
        kinds = f"{next(iter(sources))} error"
    else:
        kinds = ", ".join(f"{n} {source} error" for source, n in sorted(sources.items()))
    n = len(verdict.excluded)
    runs = "; ".join(f"run {index}/{verdict.runs_total} {o.reason}" for index, o in verdict.excluded)
    return f"{n} run{'s' if n != 1 else ''} excluded ({kinds}): {runs}."

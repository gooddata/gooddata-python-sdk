# (C) 2026 GoodData Corporation
"""The common tail of every ``evaluate_agentic_*`` function.

Before this module, each of the agentic evaluators hand-wrote the same block: copy
``reasoning_steps``/``conversation_id``/``response_id``/``detail``/``runs_passed``/
``runs_effective``/``best_run_latency_s`` (and sometimes ``timings``) either onto a
raised exception or into the returned ``AgenticEvalOutcome``. Eleven independent copies
of the same ~7 lines meant a new universal field needed eleven edits, not one, and
nothing failed loudly when a copy was missed -- exactly what happened to ``timings``
(see ``AgenticAssertionError``'s docstring: "while it lived in eight copies, two
declared timings and six did not") and again to ``best_run_latency_s`` (every agentic
kind silently reported it as ``null`` until this was noticed and fixed kind-by-kind).

``agentic_detail`` has the same motivation for the ``detail`` dict's timeline fields:
``timeline_detail`` builds both ``latency_breakdown`` and ``tool_calls`` from the same
events so they stay index-aligned, but roughly half the evaluators called
``build_latency_breakdown`` directly and silently never got a ``tool_calls`` key.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, NoReturn

from gooddata_eval.core.agentic._failure_message import failure_head
from gooddata_eval.core.agentic._gate import gate_failure_note
from gooddata_eval.core.config import error_outcome_enabled
from gooddata_eval.core.models import (
    AgenticAssertionError,
    AgenticEvalOutcome,
    EvalHarnessError,
    LoopExit,
    ReasoningStepEvent,
    ToolCallEvent,
    timeline_detail,
)
from gooddata_eval.core.outcome import (
    Outcome,
    OutcomeStatus,
    excluded_runs_note,
    gate_outcomes,
    outcome_from_loop_exit,
)
from gooddata_eval.core.timing import PhaseTimings

__all__ = [
    "RunsVerdict",
    "agentic_detail",
    "agentic_success",
    "gate_head",
    "raise_agentic_failure",
    "resolve_runs",
    "run_loop_exit",
    "run_outcome",
]


def run_loop_exit(run: Any) -> LoopExit | None:
    """The run's ``LoopExit``, or None for a kind whose run records none."""
    value = getattr(run, "exit_reason", None)
    if isinstance(value, LoopExit):
        return value
    if isinstance(value, Enum):
        value = value.value
    try:
        return LoopExit(value) if isinstance(value, str) else None
    except ValueError:
        return None


def run_outcome(run: Any, *, passed: bool) -> Outcome:
    """One run's ``Outcome``: ``outcome_from_loop_exit`` over the run's own exit."""
    return outcome_from_loop_exit(run_loop_exit(run), passed=passed)


@dataclass(frozen=True)
class RunsVerdict:
    """What an agentic kind gates on, with ``GD_EVAL_ERROR_OUTCOME`` applied or not.

    Off, every field is what the kind computed before outcomes existed: the counts are over
    every run and ``pass_at_k``/``pass_power_k`` are the kind's own. On, ERROR runs are left
    out: ``runs_effective`` is the number of scored runs, and ``errored`` is set when there is
    none.
    """

    pass_at_k: bool
    pass_power_k: bool
    runs_passed: int
    runs_effective: int
    runs_total: int
    errored: bool = False
    excluded_note: str = ""
    item_outcome: Outcome | None = None
    excluded_runs: list[dict] = field(default_factory=list)

    def exception_cls(
        self, assertion_cls: type[AgenticAssertionError]
    ) -> type[AgenticAssertionError | EvalHarnessError]:
        """``EvalHarnessError`` for an item with no scored run, ``assertion_cls`` otherwise."""
        return EvalHarnessError if self.errored else assertion_cls

    def detail(self) -> dict[str, Any]:
        """The extra ``detail`` field the flag adds: the runs it left out. Empty when off."""
        return {"excluded_runs": self.excluded_runs} if self.excluded_runs else {}

    @property
    def outcome_record(self) -> dict[str, Any] | None:
        return self.item_outcome.as_record() if self.item_outcome is not None else None


def resolve_runs(
    run_results: Sequence[Any],
    *,
    passed: Callable[[Any], bool],
    gate: str | None,
    pass_at_k: bool,
    pass_power_k: bool,
) -> RunsVerdict:
    """The verdict inputs of an item, from its runs; see ``RunsVerdict``.

    ``pass_at_k``/``pass_power_k`` are the kind's own, returned unchanged with the flag off.
    """
    total = len(run_results)
    if not error_outcome_enabled():
        return RunsVerdict(
            pass_at_k=pass_at_k,
            pass_power_k=pass_power_k,
            runs_passed=sum(1 for r in run_results if passed(r)),
            runs_effective=total,
            runs_total=total,
        )
    verdict = gate_outcomes([run_outcome(r, passed=passed(r)) for r in run_results], gate)
    return RunsVerdict(
        pass_at_k=verdict.pass_at_k,
        pass_power_k=verdict.pass_power_k,
        runs_passed=verdict.runs_passed,
        runs_effective=verdict.runs_scored,
        runs_total=total,
        errored=verdict.outcome.status is OutcomeStatus.ERROR,
        excluded_note=excluded_runs_note(verdict),
        item_outcome=verdict.outcome,
        excluded_runs=[
            {
                "run_index": index,
                "exit_reason": getattr(run_loop_exit(run_results[index - 1]), "value", None),
                "outcome": outcome.as_record(),
            }
            for index, outcome in verdict.excluded
        ],
    )


def gate_head(gate: str | None, runs: RunsVerdict, failed_runs: Sequence[dict]) -> str:
    """The start of a kind's failure message: the gate result, then every failing run.

    With the flag off this is ``gate_failure_note`` followed by the failing runs. On, the runs
    left out of K follow the gate note, and an item with no scored run says so instead.
    """
    if runs.errored:
        note = f"No scored run, item errored: {runs.excluded_note}"
    else:
        note = gate_failure_note(gate, runs.runs_passed, runs.runs_effective)
        if runs.excluded_note:
            note = f"{note} {runs.excluded_note}"
    return failure_head(note, failed_runs, runs.runs_total)


def agentic_detail(
    tool_call_events: list[ToolCallEvent],
    reasoning_step_events: list[ReasoningStepEvent] | None,
    **kind_specific: Any,
) -> dict:
    """A kind's full ``detail`` dict: its own fields plus the universal timeline ones.

    ``kind_specific`` comes first in the merge so a kind can never accidentally shadow
    ``latency_breakdown``/``tool_calls`` with a same-named field of its own.
    """
    return {**kind_specific, **timeline_detail(tool_call_events, reasoning_step_events)}


def raise_agentic_failure(
    exception_cls: type[AgenticAssertionError | EvalHarnessError],
    message: str,
    *,
    reasoning_steps: list[str],
    conversation_id: str,
    response_id: str | None,
    detail: dict,
    runs_passed: int,
    runs_effective: int,
    best_run_latency_s: float | None,
    timings: PhaseTimings | None = None,
    failed_runs: list[dict] | None = None,
    run_latencies_s: list[float] | None = None,
    outcome: dict[str, Any] | None = None,
) -> NoReturn:
    """Build ``exception_cls(message)`` with every common field attached, and raise it.

    ``exception_cls`` must be an ``AgenticAssertionError`` subclass -- that base class is
    what declares these fields as legal targets (see its docstring) -- or ``EvalHarnessError``,
    which declares the same ones plus ``outcome``. A kind whose own
    "no verdict at all" branch raises a bare ``JudgeResponseError`` instead (not a subclass)
    does not go through this helper for that branch.

    ``timings`` stays optional: only the three kinds that track per-run ``PhaseTimings``
    (general_question, metric_skill, dashboard_skill) pass one -- the rest keep their
    own ``PhaseTimings()`` zero default, same as before this helper existed. ``failed_runs``
    and ``run_latencies_s`` are likewise optional: not every kind has built them by the
    time it raises.
    """
    exc = exception_cls(message)
    exc.reasoning_steps = reasoning_steps
    exc.conversation_id = conversation_id
    exc.response_id = response_id
    exc.detail = detail
    exc.runs_passed = runs_passed
    exc.runs_effective = runs_effective
    exc.best_run_latency_s = best_run_latency_s
    if timings is not None:
        exc.timings = timings
    if failed_runs is not None:
        exc.failed_runs = failed_runs
    if run_latencies_s is not None:
        exc.run_latencies_s = run_latencies_s
    if outcome is not None and isinstance(exc, EvalHarnessError):
        exc.outcome = outcome
    raise exc


def agentic_success(
    *,
    reasoning_steps: list[str],
    conversation_id: str | None,
    response_id: str | None,
    detail: dict,
    runs_passed: int,
    runs_effective: int,
    best_run_latency_s: float | None,
    timings: PhaseTimings | None = None,
    failed_runs: list[dict] | None = None,
    run_latencies_s: list[float] | None = None,
) -> AgenticEvalOutcome:
    """The success-path mirror of ``raise_agentic_failure`` -- same fields, same shape."""
    kwargs: dict[str, Any] = {
        "reasoning_steps": reasoning_steps,
        "conversation_id": conversation_id,
        "response_id": response_id,
        "detail": detail,
        "runs_passed": runs_passed,
        "runs_effective": runs_effective,
        "best_run_latency_s": best_run_latency_s,
    }
    if timings is not None:
        kwargs["timings"] = timings
    if failed_runs is not None:
        kwargs["failed_runs"] = failed_runs
    if run_latencies_s is not None:
        kwargs["run_latencies_s"] = run_latencies_s
    return AgenticEvalOutcome(**kwargs)

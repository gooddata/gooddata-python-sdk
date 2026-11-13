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
from gooddata_eval.core.chat.sse_client import TurnIncompleteError, TurnTimeoutError
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
    EVAL_ERROR_SCORE,
    Outcome,
    OutcomeStatus,
    excluded_runs_note,
    gate_outcomes,
    outcome_from_loop_exit,
)
from gooddata_eval.core.timing import PhaseTimings

__all__ = [
    "CHAT_FAILURE_EXITS",
    "EVAL_ERROR_SCORE",
    "RunsVerdict",
    "agentic_detail",
    "agentic_success",
    "chat_failure_exit",
    "gate_head",
    "log_eval_error_score",
    "raise_agentic_failure",
    "recorded_run_outcome",
    "resolve_runs",
    "run_loop_exit",
    "run_outcome",
]


CHAT_FAILURE_EXITS = frozenset({LoopExit.CHAT_ERROR, LoopExit.AGENT_TIMEOUT, LoopExit.TURN_INCOMPLETE})
"""Every exit ``chat_failure_exit`` can return: the loop stopped because a chat call raised."""


def chat_failure_exit(exc: BaseException) -> LoopExit:
    """The ``LoopExit`` for a run whose chat call raised ``exc``.

    ``TurnTimeoutError`` and ``TurnIncompleteError`` subclass ``ChatError`` but are the
    agent's own failures -- too slow, or no final answer -- so they get exits the run is
    scored on. Anything else a kind catches there (a transport fault, a 5xx after its
    retries) is ``CHAT_ERROR``, which ``core/outcome.py`` makes an ERROR(backend) when
    ``GD_EVAL_ERROR_OUTCOME`` is on.
    """
    if isinstance(exc, TurnTimeoutError):
        return LoopExit.AGENT_TIMEOUT
    if isinstance(exc, TurnIncompleteError):
        return LoopExit.TURN_INCOMPLETE
    return LoopExit.CHAT_ERROR


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


def recorded_run_outcome(run: Any) -> Outcome:
    """The outcome a failing run's record carries: what the gate counted it as.

    With ``GD_EVAL_ERROR_OUTCOME`` on that is ``run_outcome``. Off, the gate counts every run,
    so a run that ended on a harness or backend exit was a failure like any other and is
    recorded as FAIL, its exit kept in the reason.
    """
    outcome = run_outcome(run, passed=False)
    if outcome.status is OutcomeStatus.ERROR and not error_outcome_enabled():
        loop_exit = run_loop_exit(run)
        return Outcome.failed(f"loop exit: {loop_exit.value}" if loop_exit is not None else None)
    return outcome


@dataclass(frozen=True)
class RunsVerdict:
    """What an agentic kind gates on, with ``GD_EVAL_ERROR_OUTCOME`` applied or not.

    Off, every field is what the kind computed before outcomes existed: the counts are over
    every run, ``pass_at_k``/``pass_power_k`` are the kind's own and ``runs_scored`` is None.
    On, ERROR runs are left out of the gate: ``runs_scored`` is the number of scored runs, and
    ``errored`` is set when there is none. ``runs_effective`` is the runs executed either way,
    so per-run latency and the gate's K keep counting the runs that took time.
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
    runs_scored: int | None = None
    excluded: tuple[tuple[int, Outcome], ...] = ()
    """``(run_index, outcome)`` of every run left out of the gate, 1-based. Empty when off."""

    @property
    def excluded_indexes(self) -> frozenset[int]:
        """The 1-based indexes of the runs left out of the gate. Empty with the flag off."""
        return frozenset(index for index, _ in self.excluded)

    def excluded_outcome(self, run_index: int) -> Outcome | None:
        """The ERROR outcome of run ``run_index`` (1-based) when it was left out, else None."""
        return dict(self.excluded).get(run_index)

    def exception_cls(
        self, assertion_cls: type[AgenticAssertionError]
    ) -> type[AgenticAssertionError | EvalHarnessError]:
        """``EvalHarnessError`` for an item with no scored run, ``assertion_cls`` otherwise."""
        return EvalHarnessError if self.errored else assertion_cls

    def message_lead(self, assertion_lead: str, kind: str) -> str:
        """How a kind's failure message starts: ``assertion_lead``, or for an item with no
        scored run (``EvalHarnessError``) ``"<kind> item could not be scored."``, since no
        assertion about the agent was made."""
        return f"{kind} item could not be scored." if self.errored else assertion_lead

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
        runs_effective=total,
        runs_total=total,
        runs_scored=verdict.runs_scored,
        excluded=verdict.excluded,
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
        excluded = len(runs.excluded)
        note = gate_failure_note(gate, runs.runs_passed, runs.runs_total - excluded, runs_excluded=excluded)
        if runs.excluded_note:
            note = f"{note} {runs.excluded_note}"
    # A run left out of the gate is named once, in the excluded note, not again as failing.
    excluded_indexes = runs.excluded_indexes
    failing = [r for r in failed_runs if r.get("run_index") not in excluded_indexes]
    return failure_head(note, failing, runs.runs_total)


def log_eval_error_score(ctx: Any, trace_id: Any, outcome: Outcome) -> None:
    """Mark one run left out of the gate (``GD_EVAL_ERROR_OUTCOME`` on) as an error.

    The run gets ``eval_error`` = 1, its comment ``<source>: <reason>``, and no pass, gate,
    strict-check or quality score: any of those would read as a verdict on the agent, which
    the run is not. An item whose runs all errored therefore has no gate score at all.
    """
    source = outcome.source.value if outcome.source is not None else "unknown"
    ctx.score(trace_id, name=EVAL_ERROR_SCORE, value=1, data_type="NUMERIC", comment=f"{source}: {outcome.reason}")


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
    runs_scored: int | None = None,
) -> NoReturn:
    """Build ``exception_cls(message)`` with every common field attached, and raise it.

    ``exception_cls`` must be an ``AgenticAssertionError`` subclass -- that base class is
    what declares these fields as legal targets (see its docstring) -- or ``EvalHarnessError``,
    which declares the same ones plus ``outcome``. A kind whose own
    "no verdict at all" branch raises a bare ``JudgeResponseError`` instead (not a subclass)
    does not go through this helper for that branch.

    ``runs_scored`` is set only with ``GD_EVAL_ERROR_OUTCOME`` on: the runs the gate was
    applied to, where ``runs_effective`` stays the runs executed.

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
    if runs_scored is not None:
        exc.runs_scored = runs_scored
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
    runs_scored: int | None = None,
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
    if runs_scored is not None:
        kwargs["runs_scored"] = runs_scored
    return AgenticEvalOutcome(**kwargs)

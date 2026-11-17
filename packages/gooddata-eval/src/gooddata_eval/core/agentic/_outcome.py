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
from dataclasses import dataclass
from enum import Enum
from typing import Any, NoReturn

from gooddata_eval.core.agentic._failure_message import failure_head
from gooddata_eval.core.agentic._gate import gate_failure_note
from gooddata_eval.core.chat.sse_client import TurnIncompleteError, TurnTimeoutError
from gooddata_eval.core.models import (
    AgenticAssertionError,
    AgenticEvalOutcome,
    LoopExit,
    ReasoningStepEvent,
    ToolCallEvent,
    timeline_detail,
)
from gooddata_eval.core.outcome import EVAL_ERROR_SCORE, Outcome, classify_run, item_outcome, shadow_verdict
from gooddata_eval.core.timing import PhaseTimings

__all__ = [
    "CHAT_FAILURE_EXITS",
    "EVAL_ERROR_SCORE",
    "RunLabels",
    "agentic_detail",
    "agentic_success",
    "attach_labels",
    "chat_failure_exit",
    "gate_head",
    "label_runs",
    "log_eval_error_score",
    "mark_unscored_run",
    "raise_agentic_failure",
    "run_exit_reason",
    "run_outcome",
]


CHAT_FAILURE_EXITS = frozenset({LoopExit.CHAT_ERROR, LoopExit.AGENT_TIMEOUT, LoopExit.TURN_INCOMPLETE})
"""Every exit ``chat_failure_exit`` can return: the loop stopped because a chat call raised."""


def chat_failure_exit(exc: BaseException) -> LoopExit:
    """The ``LoopExit`` for a run whose chat call raised ``exc``.

    ``TurnTimeoutError`` and ``TurnIncompleteError`` subclass ``ChatError`` but are the
    agent's own failures -- too slow, or no final answer -- so they get exits of their own
    instead of reading as a chat API fault. Anything else a kind catches there (a gen-ai
    error event, a broken stream, a 5xx after its retries) is ``CHAT_ERROR``. All three are
    FAIL in ``core/outcome.py``: a customer hits each of them too.
    """
    if isinstance(exc, TurnTimeoutError):
        return LoopExit.AGENT_TIMEOUT
    if isinstance(exc, TurnIncompleteError):
        return LoopExit.TURN_INCOMPLETE
    return LoopExit.CHAT_ERROR


def run_exit_reason(run: Any) -> str | None:
    """The run's ``exit_reason`` as a string, or None for a kind whose run records none."""
    value = getattr(run, "exit_reason", None)
    if isinstance(value, Enum):
        return str(value.value)
    return value if isinstance(value, str) else None


JudgeErrorOf = Callable[[Any], str | None]
"""How a kind reads a run's judge failure. The default reads ``run.judge_error``; a kind whose
``judge_error`` also reports a product-path failure passes the judge's own error instead."""


def _default_judge_error(run: Any) -> str | None:
    value = getattr(run, "judge_error", None)
    return value if isinstance(value, str) else None


def run_outcome(run: Any, *, passed: bool, judge_error: JudgeErrorOf | None = None) -> Outcome:
    """One run's label: ``classify_run`` over the run's exit and its judge failure, if any."""
    error = (judge_error or _default_judge_error)(run)
    return classify_run(run_exit_reason(run), passed=passed, judge_error=error if isinstance(error, str) else None)


@dataclass(frozen=True)
class RunLabels:
    """The label of every run of an item, in run order.

    The labels decide nothing: the kind gates on its own pass_at_k/pass_power_k, and an
    ERROR run counts as a run that did not pass. They only say why a run did not pass, and
    whether the whole item is a harness error (``item_outcome``).
    """

    outcomes: tuple[Outcome, ...]

    def errored_run(self, run_index: int) -> Outcome | None:
        """The ERROR label of run ``run_index`` (0-based), or None when the run is not one."""
        outcome = self.outcomes[run_index] if 0 <= run_index < len(self.outcomes) else None
        return outcome if outcome is not None and outcome.is_error else None

    @property
    def item_outcome(self) -> Outcome | None:
        """ERROR when every run errored, else None (see ``core.outcome.item_outcome``)."""
        return item_outcome(self.outcomes)

    @property
    def outcome_record(self) -> dict[str, Any] | None:
        """``item_outcome`` as the record the exception carries, or None."""
        outcome = self.item_outcome
        return outcome.as_record() if outcome is not None else None

    def shadow(self, gate: str | None) -> dict[str, Any]:
        """The phase-2 candidate verdict, recorded on the exception and never used."""
        return shadow_verdict(self.outcomes, gate)


def label_runs(
    run_results: Sequence[Any], *, passed: Callable[[Any], bool], judge_error: JudgeErrorOf | None = None
) -> RunLabels:
    """The ``RunLabels`` of an item's runs; ``passed`` is the kind's own per-run verdict."""
    return RunLabels(tuple(run_outcome(r, passed=passed(r), judge_error=judge_error) for r in run_results))


def attach_labels(exc: BaseException, labels: RunLabels, gate: str | None) -> None:
    """Set ``outcome`` (only when every run errored) and ``shadow`` on an exception a kind
    raises by hand -- the counterpart of the two ``raise_agentic_failure`` arguments."""
    outcome = labels.outcome_record
    if outcome is not None:
        exc.outcome = outcome  # ty: ignore[unresolved-attribute]
    exc.shadow = labels.shadow(gate)  # ty: ignore[unresolved-attribute]


def gate_head(
    gate: str | None, labels: RunLabels, runs_passed: int, failed_runs: Sequence[dict], runs_ungraded: int = 0
) -> str:
    """The start of a kind's failure message: the gate result, then every failing run.

    An item whose every run errored says so first, so a reader sees at once that the agent
    was never scored. The gate note itself is the one the item was judged by.
    """
    runs_total = len(labels.outcomes)
    note = gate_failure_note(gate, runs_passed, runs_total, runs_ungraded)
    item = labels.item_outcome
    if item is not None:
        note = f"Harness error, no run was scored ({item.reason}). {note}"
    return failure_head(note, failed_runs, runs_total)


def log_eval_error_score(ctx: Any, trace_id: Any, outcome: Outcome) -> None:
    """Mark one ERROR run in Langfuse: ``eval_error`` = 1, its comment the reason.

    An extra score only. The run's pass, gate, check and quality scores are written as
    always, so nothing read from Langfuse changes; the marker says why the run failed.
    """
    ctx.score(trace_id, name=EVAL_ERROR_SCORE, value=1, data_type="NUMERIC", comment=outcome.reason)


def mark_unscored_run(ctx: Any, run_idx: int, conversation_id: str, error: Outcome | None) -> None:
    """Langfuse for a run that gets no verdict scores (its judge or its request failed).

    A harness ERROR (``error``, from ``RunLabels.errored_run``) gets its run root with the
    ``eval_error`` marker; any other unscored run only keeps its root, as before.
    """
    if error is None:
        ctx.export_unscored(run_idx, conversation_id)
        return
    with ctx.observe(ctx.trace(conversation_id), run_idx, conversation_id=conversation_id) as tid:
        log_eval_error_score(ctx, tid, error)


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
    exception_cls: type[AgenticAssertionError],
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
    shadow: dict[str, Any] | None = None,
) -> NoReturn:
    """Build ``exception_cls(message)`` with every common field attached, and raise it.

    ``exception_cls`` must be an ``AgenticAssertionError`` subclass -- that base class is
    what declares these fields as legal targets (see its docstring). A kind whose own
    "no verdict at all" branch raises a bare ``JudgeResponseError`` instead (not a subclass)
    does not go through this helper for that branch.

    ``outcome`` is set only when every run errored (``RunLabels.outcome_record``), and
    ``shadow`` is the phase-2 candidate verdict (``RunLabels.shadow``); both are labels a
    runner reads, neither changes the failure.

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
    if outcome is not None:
        exc.outcome = outcome
    if shadow is not None:
        exc.shadow = shadow
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

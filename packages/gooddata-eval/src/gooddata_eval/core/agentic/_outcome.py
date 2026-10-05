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

from typing import Any, NoReturn

from gooddata_eval.core.models import (
    AgenticAssertionError,
    AgenticEvalOutcome,
    ReasoningStepEvent,
    ToolCallEvent,
    timeline_detail,
)
from gooddata_eval.core.timing import PhaseTimings

__all__ = ["agentic_detail", "agentic_success", "raise_agentic_failure"]


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
    failed_runs: list[dict] | None = None,
    timings: PhaseTimings | None = None,
) -> NoReturn:
    """Build ``exception_cls(message)`` with every common field attached, and raise it.

    ``exception_cls`` must be an ``AgenticAssertionError`` subclass -- that base class is
    what declares these fields as legal targets (see its docstring). A kind whose own
    "no verdict at all" branch raises a bare ``JudgeResponseError`` instead (not a subclass)
    does not go through this helper for that branch.

    ``timings`` stays optional: only the three kinds that track per-run ``PhaseTimings``
    (general_question, metric_skill, dashboard_skill) pass one -- the rest keep their
    own ``PhaseTimings()`` zero default, same as before this helper existed.
    """
    exc = exception_cls(message)
    exc.reasoning_steps = reasoning_steps
    exc.conversation_id = conversation_id
    exc.response_id = response_id
    exc.detail = detail
    exc.runs_passed = runs_passed
    exc.runs_effective = runs_effective
    exc.best_run_latency_s = best_run_latency_s
    # Same motivation as every other field here, and the same history: it lived in one
    # hand-written copy per kind and four kinds silently never built it at all. Optional,
    # because a kind that drives its fixture once has no failing run to record.
    if failed_runs is not None:
        exc.failed_runs = failed_runs
    if timings is not None:
        exc.timings = timings
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
    failed_runs: list[dict] | None = None,
    timings: PhaseTimings | None = None,
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
    if failed_runs is not None:
        kwargs["failed_runs"] = failed_runs
    if timings is not None:
        kwargs["timings"] = timings
    return AgenticEvalOutcome(**kwargs)

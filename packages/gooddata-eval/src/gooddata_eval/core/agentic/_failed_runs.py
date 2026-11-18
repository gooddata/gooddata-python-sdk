# (C) 2026 GoodData Corporation. All rights reserved.
"""Per-run failure records for the agentic evaluators.

``core/runner.py`` records one of these for every failing run of a single-shot item. The
agentic kinds cannot reuse it: each of them drives its own K-loop inside the evaluator and
hands ``cli/agentic_runner`` a single aggregate per item, so by the time the runner sees
the result the individual attempts are already collapsed into ``best``. The runs themselves
are not lost -- every kind keeps its ``run_results`` list -- they simply never leave the
evaluator. This turns that list into the same records the single-shot path writes.

Keys mirror ``core.runner._failed_run_record`` so one consumer can read ``failed_runs`` from
either path without branching on test kind. ``tool_call_count``/``tool_names``/``tool_calls``
are the addition: the agentic kinds capture tool calls per run, and an agent that produced a
final answer having made no tool call at all answered from the model's own knowledge rather
than from the workspace -- a distinction no other recorded field exposes.

``tool_calls`` holds each call's arguments and result, in the shape of ``build_tool_calls``.
It is recorded for every kind whose run result keeps ``tool_call_events``, including the
kinds whose ``detail`` has no ``tool_calls``. A run result without that list, such as a
document takeaway run, records an empty list.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

from gooddata_eval.core.agentic._failure_message import cap_failed_checks
from gooddata_eval.core.agentic._outcome import RunLabels, run_exit_reason, run_outcome
from gooddata_eval.core.models import build_tool_calls
from gooddata_eval.core.outcome import OutcomeStatus


def build_failed_runs(
    run_results: Sequence[Any],
    *,
    detail: Callable[[Any], dict],
    labels: RunLabels | None = None,
    passed: Callable[[Any], bool] | None = None,
    failed_checks: Callable[[Any], list[dict]] | None = None,
) -> list[dict]:
    """One record per run that did not pass, in the order the runs happened.

    A kind that labels its runs passes its ``labels`` (from ``label_runs``, in run order):
    they say which runs did not pass and are the ``outcome`` of each record, so the records,
    the failure message and the Langfuse ``eval_error`` marker read one set of labels. A kind
    that does not label its runs passes ``passed`` instead, and each record's ``outcome`` is
    worked out here from the run alone. Exactly one of the two is given.

    ``passed`` and ``detail`` are supplied by the caller because neither is uniform across
    kinds: guardrail reads ``run.passed`` while visualization reads
    ``run.eval_result.strict_pass``, and each kind's diagnostic dict is its own. Everything
    read here directly goes through ``getattr`` with a default, so a kind whose run result
    lacks a field (no response id, no tool capture) records a null instead of raising. The
    events inside ``tool_call_events`` are the exception: ``build_tool_calls`` reads them as
    ``ToolCallEvent``s, so a run that has the list must hold real events in it.

    A run the judge could not grade is recorded like any other non-passing run, with its
    ``error`` set to the run's ``judge_error``. That matches ``core/runner.py``, which also
    records ungraded runs; the verdict-level accounting of ungraded runs stays with the
    caller's ``unscored_runs``.

    ``exit_reason`` is the run's ``LoopExit`` value, or null for a kind whose loop records
    none, and ``outcome`` its ``core.outcome.Outcome`` record: ERROR when the harness failed
    (its simulated user, or its judge when the judge's verdict was the one still open), FAIL
    otherwise. ``error`` and ``outcome`` can differ: a run that failed a fixed check and whose
    judge also broke has ``error`` set and is a FAIL. The label decides nothing; the run counts
    as not passed either way.

    ``failed_checks`` is written only when the caller supplies it: a missing key means the
    kind does not name its failing checks, while an empty list would claim the run failed
    none. Its expected/actual values are capped in size; the run's ``detail`` keeps them whole.
    """
    if (labels is None) == (passed is None):
        raise ValueError("build_failed_runs takes exactly one of labels and passed")
    if labels is not None and len(labels.outcomes) != len(run_results):
        raise ValueError(f"{len(labels.outcomes)} labels for {len(run_results)} runs")
    records: list[dict] = []
    for run_index, run in enumerate(run_results, start=1):
        if labels is not None:
            outcome = labels.outcomes[run_index - 1]
        else:
            outcome = run_outcome(run, passed=passed is not None and passed(run))
        if outcome.status is OutcomeStatus.PASS:
            continue
        tool_calls = list(getattr(run, "tool_call_events", None) or [])
        reasoning_steps = list(getattr(run, "reasoning_steps", None) or [])
        record: dict[str, Any] = {
            "run_index": run_index,
            "passed": False,
            "error": getattr(run, "judge_error", None),
            "detail": detail(run),
            "conversation_id": getattr(run, "conversation_id", None),
            "response_id": getattr(run, "response_id", None),
            "reasoning_step_count": len(reasoning_steps),
            "reasoning_steps": reasoning_steps,
            "tool_call_count": len(tool_calls),
            "tool_names": [getattr(e, "function_name", None) for e in tool_calls],
            "tool_calls": build_tool_calls(tool_calls),
            "exit_reason": run_exit_reason(run),
            "outcome": outcome.as_record(),
        }
        if failed_checks is not None:
            record["failed_checks"] = cap_failed_checks(failed_checks(run))
        records.append(record)
    return records

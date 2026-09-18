# (C) 2026 GoodData Corporation. All rights reserved.
"""Per-run failure records for the agentic evaluators.

``core/runner.py`` records one of these for every failing run of a single-shot item. The
agentic kinds cannot reuse it: each of them drives its own K-loop inside the evaluator and
hands ``cli/agentic_runner`` a single aggregate per item, so by the time the runner sees
the result the individual attempts are already collapsed into ``best``. The runs themselves
are not lost -- every kind keeps its ``run_results`` list -- they simply never leave the
evaluator. This turns that list into the same records the single-shot path writes.

Keys mirror ``core.runner._failed_run_record`` so one consumer can read ``failed_runs`` from
either path without branching on test kind. ``tool_call_count``/``tool_names`` are the
addition: the agentic kinds capture tool calls per run, and an agent that produced a final
answer having made no tool call at all answered from the model's own knowledge rather than
from the workspace -- a distinction no other recorded field exposes.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any


def build_failed_runs(
    run_results: Sequence[Any],
    *,
    passed: Callable[[Any], bool],
    detail: Callable[[Any], dict],
) -> list[dict]:
    """One record per run that did not pass, in the order the runs happened.

    ``passed`` and ``detail`` are supplied by the caller because neither is uniform across
    kinds: guardrail reads ``run.passed`` while visualization reads
    ``run.eval_result.strict_pass``, and each kind's diagnostic dict is its own. Everything
    read here directly goes through ``getattr`` with a default, so a kind whose run result
    lacks a field (no response id, no tool capture) records a null instead of raising.

    A run that could not be graded is recorded like any other non-passing run, with its
    ``error`` set. That matches ``core/runner.py``, which also records ungraded runs; the
    verdict-level accounting of ungraded runs stays with the caller's ``unscored_runs``.
    Kinds name that field differently -- the judge failing to grade a run
    (``judge_error``) and the chat call itself failing (``chat_error``) are both "this run
    produced no verdict" as far as a reader of ``failed_runs`` is concerned -- so both are
    read here and whichever the kind sets wins.
    """
    records: list[dict] = []
    for run_index, run in enumerate(run_results, start=1):
        if passed(run):
            continue
        error = getattr(run, "judge_error", None) or getattr(run, "chat_error", None)
        tool_calls = list(getattr(run, "tool_call_events", None) or [])
        reasoning_steps = list(getattr(run, "reasoning_steps", None) or [])
        records.append(
            {
                "run_index": run_index,
                "passed": False,
                "error": error,
                "detail": detail(run),
                "conversation_id": getattr(run, "conversation_id", None),
                "response_id": getattr(run, "response_id", None),
                "reasoning_step_count": len(reasoning_steps),
                "reasoning_steps": reasoning_steps,
                "tool_call_count": len(tool_calls),
                "tool_names": [getattr(e, "function_name", None) for e in tool_calls],
            }
        )
    return records

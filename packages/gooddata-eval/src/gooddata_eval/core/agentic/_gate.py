# (C) 2026 GoodData Corporation
"""Which of pass@K / pass^K decides an item, and how both reach Langfuse."""

from __future__ import annotations

from typing import Any

from gooddata_eval.core.config import DEFAULT_GATE, EvalGate, normalize_gate

__all__ = [
    "DEFAULT_GATE",
    "EvalGate",
    "gate_failure_note",
    "gate_label",
    "gate_passed",
    "log_gate_scores",
    "normalize_gate",
    "stamp_gate_metadata",
]


def gate_passed(gate: str | None, *, pass_at_k: bool, pass_power_k: bool) -> bool:
    """Whether the item passes under ``gate``."""
    return pass_power_k if normalize_gate(gate) == "power" else pass_at_k


def gate_label(gate: str | None, k: int) -> str:
    """Short name for the gate, e.g. ``pass^3`` or ``pass@2``."""
    return f"pass^{k}" if normalize_gate(gate) == "power" else f"pass@{k}"


def gate_failure_note(gate: str | None, runs_passed: int, runs_total: int, runs_ungraded: int = 0) -> str:
    """Gate and how many runs met it, for the assertion message.

    Needed because the message body describes the BEST run, which under pass^K can be a run
    that passed — so the reported detail on its own looks like a pass.

    An ungraded run counts in runs_total but can never count in runs_passed, so the remainder
    is not evidence of instability — saying so would blame the agent for a judge outage.
    """
    label = gate_label(gate, runs_total)
    note = f"Gate {label} failed: {runs_passed}/{runs_total} runs passed"
    if runs_ungraded:
        return f"{note}, {runs_ungraded} ungraded."
    if normalize_gate(gate) == "power" and runs_passed:
        return f"{note} — unstable, not a clean failure."
    return f"{note}."


def log_gate_scores(ctx: Any, trace_id: Any, *, gate: str | None, pass_at_k: bool, pass_power_k: bool) -> None:
    """Log both candidate verdicts and the one that decided.

    The names carry no K on purpose: `pass_at_2` becomes `pass_at_3` the moment K changes,
    splitting every Langfuse view built on the old name.
    """
    ctx.score(trace_id, name="pass_at_k", value=pass_at_k, data_type="BOOLEAN")
    ctx.score(trace_id, name="pass_power_k", value=pass_power_k, data_type="BOOLEAN")
    ctx.score(
        trace_id,
        name="gate_passed",
        value=gate_passed(gate, pass_at_k=pass_at_k, pass_power_k=pass_power_k),
        data_type="BOOLEAN",
    )


def stamp_gate_metadata(metadata: dict, *, k: int, gate: str | None) -> dict:
    """Record K and the gate on the dataset-run metadata (mutates and returns it)."""
    metadata["eval_k"] = k
    metadata["eval_gate"] = normalize_gate(gate)
    return metadata

# (C) 2026 GoodData Corporation
"""Render a human-readable console report using rich."""

from rich.console import Console
from rich.table import Table

from gooddata_eval.core.runner import EvalReport


def render_console(report: EvalReport, *, console: Console | None = None) -> str:
    """Render the report to the console and return the rendered text.

    Passing a Console lets callers print to stdout; the returned string aids testing.
    """
    out = console or Console(record=True, width=120)

    table = Table(title=f"Evaluation — model={report.model} workspace={report.workspace_id}")
    table.add_column("Item")
    table.add_column("Kind")
    table.add_column("Result")
    table.add_column("Runs")
    table.add_column("Latency")
    table.add_column("Avg/run")
    table.add_column("Quality")
    table.add_column("Notes")

    for item in report.items:
        if item.skipped:
            result, notes = "SKIPPED", f"test_kind '{item.test_kind}' not supported in this phase"
        elif item.error:
            result, notes = "ERROR", item.error
        elif item.pass_at_k:
            result, notes = "PASS", ""
        else:
            # Evaluator-agnostic: report whichever boolean checks came back False
            # (visualization uses metrics_correct/…; dashboard_summary uses
            # include_*/exclude_*/rubric_*). Falls back to a generic message.
            failing = [k for k, v in item.best_detail.items() if v is False]
            notes = "failed: " + ", ".join(failing) if failing else "did not pass strict checks"
            result = "FAIL"
        latency = "-" if item.runs == 0 else f"{item.latency_s:.2f}s"
        avg = "-" if item.runs == 0 else f"{item.avg_latency_s:.2f}s"
        quality = "-" if item.skipped else f"{item.quality_score:.0%}"
        table.add_row(item.id, item.test_kind, result, str(item.runs), latency, avg, quality, notes)

    out.print(table)
    out.print(
        f"\nSummary: {report.passed}/{report.total} passed "
        f"({report.skipped} skipped, {report.errored} errored) "
        f"avg quality {report.avg_quality_score:.0%} "
        f"in {report.latency_s:.2f}s (avg {report.avg_latency_s:.2f}s/run)"
    )
    return out.export_text() if out.record else ""

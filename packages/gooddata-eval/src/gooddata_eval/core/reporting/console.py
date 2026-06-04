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
            d = item.best_detail
            failing = [
                k
                for k in ("metrics_correct", "dimensions_correct", "filters_correct", "viz_type_hard")
                if d.get(k) is False
            ]
            notes = "failed: " + ", ".join(failing) if failing else "no visualization created"
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


def render_comparison(reports: list[EvalReport], *, console: Console | None = None) -> str:
    """Render a side-by-side comparison for multiple model runs.

    Winner is selected by (pass_rate, avg_quality_score, -avg_latency_s) —
    higher pass rate first, then quality, then lower latency as final tiebreaker.
    Returns an empty string when fewer than two reports are provided.
    """
    if len(reports) < 2:
        return ""

    out = console or Console(record=True, width=120)

    table = Table(title="Model Comparison")
    table.add_column("Model")
    table.add_column("Passed")
    table.add_column("Quality")
    table.add_column("Avg/run")
    table.add_column("Total time")

    for r in reports:
        evaluated = r.total - r.skipped
        pass_pct = f"{r.passed / evaluated:.0%}" if evaluated else "—"
        model_label = f"{r.provider_name}/{r.model}" if r.provider_name else r.model or "?"
        table.add_row(
            model_label,
            f"{r.passed}/{r.total} ({pass_pct})",
            f"{r.avg_quality_score:.0%}",
            f"{r.avg_latency_s:.2f}s",
            f"{r.latency_s:.0f}s",
        )

    out.print(table)

    evaluated_reports = [r for r in reports if r.total > 0]
    if evaluated_reports:
        winner = max(
            evaluated_reports,
            key=lambda r: (
                r.passed / r.total if r.total else 0,
                r.avg_quality_score,
                -r.avg_latency_s,  # lower latency wins when pass rate and quality tie
            ),
        )
        runner_up = max(
            (r for r in evaluated_reports if r is not winner),
            key=lambda r: r.passed / r.total if r.total else 0,
            default=None,
        )
        delta = ""
        if runner_up and runner_up.total > 0:
            delta_items = winner.passed - runner_up.passed
            delta_quality = winner.avg_quality_score - runner_up.avg_quality_score
            delta = f"  (+{delta_items} item(s) passed, +{delta_quality:.0%} quality)"
        winner_label = f"{winner.provider_name}/{winner.model}" if winner.provider_name else winner.model or "?"
        out.print(f"\n[bold]Winner: {winner_label}[/bold]{delta}")

    return out.export_text() if out.record else ""

# (C) 2026 GoodData Corporation
"""Build and write machine-readable reports (single-model or multi-model)."""

from pathlib import Path

import orjson

from gooddata_eval.core.runner import EvalReport


def _build_run_dict(report: EvalReport) -> dict:
    return {
        "model": report.model,
        "workspace_id": report.workspace_id,
        "summary": {
            "total": report.total,
            "passed": report.passed,
            "failed": report.total - report.passed - report.skipped,
            "skipped": report.skipped,
            "errored": report.errored,
            "latency_s": round(report.latency_s, 3),
            "avg_latency_s": round(report.avg_latency_s, 3),
        },
        "items": {
            item.id: {
                "dataset_name": item.dataset_name,
                "test_kind": item.test_kind,
                "question": item.question,
                "pass_at_k": item.pass_at_k,
                "skipped": item.skipped,
                "error": item.error,
                "runs": item.runs,
                "latency_s": round(item.latency_s, 3),
                "avg_latency_s": round(item.avg_latency_s, 3),
                "detail": item.best_detail,
            }
            for item in report.items
        },
    }


def _build_comparison_entry(report: EvalReport) -> dict:
    total = report.total
    passed = report.passed
    return {
        "provider_name": report.provider_name,
        "passed": passed,
        "total": total,
        "pass_rate": round(passed / total, 4) if total else 0.0,
        "avg_quality_score": round(report.avg_quality_score, 4),
        "avg_latency_s": round(report.avg_latency_s, 3),
        "total_latency_s": round(report.latency_s, 3),
    }


def _run_key(report: EvalReport) -> str:
    """Collision-free key matching the console comparison table label."""
    return f"{report.provider_name}/{report.model}" if report.provider_name else report.model or "?"


def build_multi_model_report(reports: list[EvalReport]) -> dict:
    """Build the nested multi-model JSON report (used for single-model runs too)."""
    return {
        "models": [_run_key(r) for r in reports],
        "runs": {_run_key(r): _build_run_dict(r) for r in reports},
        "comparison": {_run_key(r): _build_comparison_entry(r) for r in reports},
    }


def write_multi_model_report(reports: list[EvalReport], path: Path) -> None:
    Path(path).write_bytes(orjson.dumps(build_multi_model_report(reports), option=orjson.OPT_INDENT_2))


# Backward-compatible aliases so existing callers keep working.
def build_json_report(report: EvalReport) -> dict:
    return _build_run_dict(report)


def write_json_report(report: EvalReport, path: Path) -> None:
    write_multi_model_report([report], path)

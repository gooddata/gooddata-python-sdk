# (C) 2026 GoodData Corporation
"""Build and write the machine-readable JSON report, keyed by item id."""

from pathlib import Path

import orjson

from gooddata_eval.core.runner import EvalReport


def build_json_report(report: EvalReport) -> dict:
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


def write_json_report(report: EvalReport, path: Path) -> None:
    path = Path(path)
    path.write_bytes(orjson.dumps(build_json_report(report), option=orjson.OPT_INDENT_2))

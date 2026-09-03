# (C) 2026 GoodData Corporation
"""Build and write machine-readable reports (single-model or multi-model)."""

from pathlib import Path

import orjson

from gooddata_eval.core.runner import EvalReport
from gooddata_eval.core.timing import PhaseTimings


def _build_run_dict(report: EvalReport) -> dict:
    return {
        "model": report.model,
        "workspace_id": report.workspace_id,
        "summary": {
            "total": report.total,
            "passed": report.passed,
            # pass^K across the dataset. A large gap from `passed` means the models are
            # inconsistent rather than wrong, which pass@K alone cannot show.
            "passed_all_runs": report.passed_all_runs,
            # Counted explicitly rather than by subtraction: an errored item has
            # pass_at_k False and skipped False, so subtraction would count it as both a
            # failure and an error. A judge fault is an error, not K failures.
            "failed": sum(1 for i in report.items if not i.pass_at_k and not i.skipped and i.error is None),
            "skipped": report.skipped,
            "errored": report.errored,
            "latency_s": round(report.latency_s, 3),
            "avg_latency_s": round(report.avg_latency_s, 3),
            "wall_clock_s": round(report.wall_clock_s, 3),
        },
        "items": {
            item.id: {
                "dataset_name": item.dataset_name,
                "test_kind": item.test_kind,
                "question": item.question,
                "pass_at_k": item.pass_at_k,
                "skipped": item.skipped,
                "error": item.error,
                # What actually ran, not the requested K: agentic_conversation runs once.
                "runs": item.runs_total,
                "latency_s": round(item.latency_s, 3),
                "avg_latency_s": round(item.avg_latency_s, 3),
                # Beside `runs`, not folded into it: "4 of 5 passed" is a different fact
                # from pass_at_k and the only one that separates a reliable item from a
                # coin-flip. pass_power_k is the unanimity flag beside it, and
                # runs_ungraded says how many runs pass@K was NOT computed over.
                "runs_passed": item.runs_passed,
                "runs_ungraded": item.runs_ungraded,
                "pass_power_k": item.pass_power_k,
                "best_run_latency_s": (
                    round(item.best_run_latency_s, 3) if item.best_run_latency_s is not None else None
                ),
                # Additive to latency_s, never folded into it: langfuse_s is measured off
                # the item's critical path (see agentic/_trace_linker.py), so summing the
                # four would over-count the item's latency.
                "latency_breakdown_s": PhaseTimings(
                    agent_s=item.agent_latency_s,
                    judge_s=item.judge_latency_s,
                    simulated_user_s=item.simulated_user_latency_s,
                    langfuse_s=item.langfuse_latency_s,
                ).as_dict(),
                "detail": item.best_detail,
                "conversation_id": item.conversation_id,
                "response_id": item.response_id,
                "reasoning": item.reasoning_steps,
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

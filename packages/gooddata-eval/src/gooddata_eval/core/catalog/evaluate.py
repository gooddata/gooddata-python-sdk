# (C) 2026 GoodData Corporation
"""Entry point for evaluating one catalog_metadata item K times, for the Tavern shim.

The CLI evaluates catalog items through the single-shot runner; CI goes through
``evaluate_catalog_metadata``, which owns the K-run loop, the gate and the Langfuse
experiment item the same way ``evaluate_document_takeaway`` does, so the nightly report
reads it unchanged.

The generate endpoints return no conversation id, so there is no gen-ai trace to link:
every score is written to gd-eval's own experiment span.

A run whose request still fails transiently after the client's retries (5xx, 429, a
connection failure or a read timeout) is recorded as an errored run and left ungraded;
the item raises it only when no run completed. Any other 4xx (no AI entitlement, invalid
body) or an unsupported URL scheme is a setup problem and raises on the first run.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

import httpx

from gooddata_eval.core._retry import is_transient
from gooddata_eval.core.agentic._failed_runs import build_failed_runs
from gooddata_eval.core.agentic._gate import (
    DEFAULT_GATE,
    EvalGate,
    gate_failure_note,
    gate_passed,
    log_gate_scores,
    stamp_gate_metadata,
)
from gooddata_eval.core.agentic._trace_linker import (
    RunIdentity,
    RunTraceContext,
    SubmitTraceLink,
    open_trace_window,
    run_trace_link_inline,
    submit_trace_scoring,
    utc_now,
)
from gooddata_eval.core.catalog.http_client import CatalogMetadataClient
from gooddata_eval.core.config import ReasoningEffort
from gooddata_eval.core.evaluators._llm_judge import JudgeResponseError
from gooddata_eval.core.evaluators.base import ItemEvaluation
from gooddata_eval.core.evaluators.catalog_metadata import CatalogMetadataEvaluator
from gooddata_eval.core.models import AgenticAssertionError, AgenticEvalOutcome, ChatResult, DatasetItem
from gooddata_eval.core.timing import PhaseTimings, sum_timings

_TEST_KIND = "catalog_metadata"
_COUNT_SCORES = ("word_count", "unusable_retries")


class CatalogMetadataAssertionError(AgenticAssertionError):
    """Raised when a catalog_metadata evaluation fails its gate."""


@dataclass
class _CatalogRun:
    chat_result: ChatResult
    evaluation: ItemEvaluation
    latency_s: float
    timings: PhaseTimings
    request_error: httpx.HTTPError | None = None

    @property
    def judge_error(self) -> str | None:
        return self.evaluation.error

    @property
    def checks(self) -> dict[str, bool]:
        return {k: v for k, v in self.evaluation.detail.items() if isinstance(v, bool)}


def _dataset_item(dataset_item: dict, dataset_name: str) -> DatasetItem:
    item = DatasetItem.model_validate(
        {"id": "", "test_kind": _TEST_KIND, "expected_output": {}, **dataset_item, "dataset_name": dataset_name}
    )
    if item.catalog_input is None:
        raise ValueError(f"catalog_metadata item '{item.id}' is missing required 'catalog_input'.")
    return item


def _run_once(client: CatalogMetadataClient, evaluator: CatalogMetadataEvaluator, item: DatasetItem) -> _CatalogRun:
    started = time.monotonic()
    try:
        chat_result = client.ask(item)
    except httpx.HTTPError as exc:
        if not is_transient(exc):
            raise
        elapsed = time.monotonic() - started
        error = f"{type(exc).__name__}: {exc}"
        evaluation = ItemEvaluation(passed=False, rank_key=(-2, 0.0), detail={"request_error": error}, error=error)
        return _CatalogRun(ChatResult(), evaluation, elapsed, PhaseTimings(agent_s=elapsed), request_error=exc)
    asked = time.monotonic()
    evaluation = evaluator.evaluate(item, chat_result)
    judged = time.monotonic()
    return _CatalogRun(
        chat_result, evaluation, asked - started, PhaseTimings(agent_s=asked - started, judge_s=judged - asked)
    )


def evaluate_catalog_metadata(
    *,
    host: str,
    token: str,
    workspace_id: str,
    dataset_item: dict,
    dataset_name: str,
    run_timestamp: str | None,
    model_version_override: str | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    k: int = 1,
    gate: EvalGate = DEFAULT_GATE,
    run_metadata_extra: dict | None = None,
    langfuse: object | None = None,
    submit_trace_link: SubmitTraceLink = run_trace_link_inline,
    client: CatalogMetadataClient | None = None,
    evaluator: CatalogMetadataEvaluator | None = None,
) -> AgenticEvalOutcome:
    """Generate the item's title or description K times, grade each, log to Langfuse, and raise on a failed gate.

    Args:
        host: GoodData host URL.
        token: API token.
        workspace_id: Workspace the catalog object lives in.
        dataset_item: The item as stored: `id`, `question`, `expected_output`, `catalog_input`.
        dataset_name: Langfuse dataset name; prefixes the experiment run name.
        run_timestamp: Shared run timestamp for the run name.
        model_version_override: Model-version tag for the run; the workspace's active LLM
            provider otherwise.
        reasoning_effort: Only names the run: the generate endpoints have no reasoning option.
        k: Runs per item.
        gate: `any` (pass@K) or `power` (pass^K).
        run_metadata_extra: Extra experiment-run metadata, e.g. `testing_framework`.
        langfuse: Langfuse client; built from the LANGFUSE_* environment when None.
        submit_trace_link: How the Langfuse block is run; inline by default.
        client: Catalog client to use instead of one built from host/token/workspace.
        evaluator: Evaluator to use instead of a default one.

    Raises:
        CatalogMetadataAssertionError: the gate did not pass.
        ValueError: the item has no `catalog_input` or an `expected_output` the evaluator
            cannot read, raised before any request.
        httpx.HTTPError: the endpoint refused with a non-transient 4xx, or no run completed;
            the message carries status and body.
        JudgeResponseError: the judge returned no readable verdict for any run.
    """
    item = _dataset_item(dataset_item, dataset_name)
    evaluator = evaluator or CatalogMetadataEvaluator()
    evaluator.validate(item)
    own_client = client is None
    catalog_client = client or CatalogMetadataClient(host=host, token=token, workspace_id=workspace_id)
    langfuse, window_start = open_trace_window(langfuse)
    try:
        runs = [_run_once(catalog_client, evaluator, item) for _ in range(k)]
    finally:
        if own_client:
            catalog_client.close()

    completed = [r for r in runs if r.request_error is None]
    if not completed:
        raise runs[-1].request_error or RuntimeError("no catalog_metadata run completed")
    graded = [r for r in runs if r.judge_error is None]
    pass_at_k = any(r.evaluation.passed for r in graded)
    pass_power_k = all(r.evaluation.passed for r in runs)

    if langfuse is not None and item.id:
        window_end = utc_now()

        def _write_scores(ctx: RunTraceContext) -> None:
            stamp_gate_metadata(ctx.run_metadata, k=len(runs), gate=gate)
            for run_idx, run in enumerate(runs):
                if run.judge_error is not None:
                    continue
                with ctx.observe(None, run_idx, output=run.chat_result.raw_response) as tid:
                    for name, value in run.checks.items():
                        ctx.score(tid, name=name, value=float(value), data_type="BOOLEAN")
                    for name in _COUNT_SCORES:
                        if name in run.evaluation.detail:
                            ctx.score(tid, name=name, value=run.evaluation.detail[name], data_type="NUMERIC")
                    ctx.score(
                        tid, name="catalog_metadata_pass", value=float(run.evaluation.passed), data_type="BOOLEAN"
                    )
                    log_gate_scores(ctx, tid, gate=gate, pass_at_k=pass_at_k, pass_power_k=pass_power_k)
                    ctx.quality(tid, strict_checks=run.checks, latency_sec=run.latency_s, cost_usd=None)

        submit_trace_scoring(
            submit_trace_link,
            RunIdentity(
                host,
                token,
                workspace_id,
                dataset_name,
                run_timestamp,
                model_version_override,
                run_metadata_extra,
                reasoning_effort,
            ),
            langfuse=langfuse,
            dataset_item_id=item.id,
            conversation_ids=[],
            window_start=window_start,
            window_end=window_end,
            suffix_runs=len(runs) > 1,
            write_scores=_write_scores,
            item_input=item.question,
        )

    item_timings = sum_timings([r.timings for r in runs])
    unscored = [r.judge_error for r in runs if r.judge_error is not None]
    request_errors = [r.judge_error for r in runs if r.request_error is not None and r.judge_error is not None]
    judge_errors = [r.judge_error for r in completed if r.judge_error is not None]
    best = max(completed, key=lambda r: r.evaluation.rank_key)
    runs_passed = sum(1 for r in runs if r.evaluation.passed)
    detail: dict[str, Any] = {
        **best.evaluation.detail,
        **({"unscored_runs": len(unscored)} if unscored else {}),
        **({"judge_errors": judge_errors} if judge_errors else {}),
        **({"request_errors": request_errors} if request_errors else {}),
    }
    failed_runs = build_failed_runs(runs, passed=lambda r: r.evaluation.passed, detail=lambda r: r.evaluation.detail)

    def _attach(exc: CatalogMetadataAssertionError | JudgeResponseError) -> None:
        exc.reasoning_steps = []
        exc.conversation_id = ""
        exc.response_id = None
        exc.timings = item_timings
        exc.detail = detail
        exc.runs_passed = runs_passed
        exc.runs_effective = len(runs)
        exc.failed_runs = failed_runs

    if not graded:
        if request_errors:
            causes = [
                *([f"judge returned no readable verdict for {len(judge_errors)} run(s)"] if judge_errors else []),
                f"request failed for {len(request_errors)} run(s)",
            ]
            message = f"no run of {len(runs)} could be graded: {', '.join(causes)}: "
        else:
            message = f"judge returned no readable verdict for any of the {len(runs)} run(s): "
        exc_judge = JudgeResponseError(message + " | ".join(unscored))
        _attach(exc_judge)
        raise exc_judge

    if not gate_passed(gate, pass_at_k=pass_at_k, pass_power_k=pass_power_k):
        failed = [name for name, ok in best.checks.items() if not ok]
        parts = [
            "Catalog metadata assertion failed.",
            gate_failure_note(gate, runs_passed, len(runs), len(unscored)),
            *([f"Failed checks: {', '.join(failed)}."] if failed else []),
            *([f"Request errors: {' | '.join(request_errors)}"] if request_errors else []),
            f"Generated: {best.chat_result.text_response!r}",
        ]
        exc = CatalogMetadataAssertionError(" ".join(parts))
        _attach(exc)
        raise exc
    return AgenticEvalOutcome(
        detail=detail,
        timings=item_timings,
        runs_passed=runs_passed,
        runs_effective=len(runs),
        failed_runs=failed_runs,
    )

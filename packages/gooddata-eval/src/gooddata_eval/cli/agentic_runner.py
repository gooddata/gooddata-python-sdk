# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic evaluation runner for gd-eval CLI — handles multi-turn agentic test kinds."""

from __future__ import annotations

import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, TypedDict

from gooddata_eval.core.agentic._langfuse import make_langfuse_client
from gooddata_eval.core.agentic._trace_linker import BackgroundTraceLinker, SubmitTraceLink, run_trace_link_inline
from gooddata_eval.core.agentic.alert_skill import evaluate_agentic_alert_skill
from gooddata_eval.core.agentic.conversation import ConversationFixture, evaluate_agentic_conversation
from gooddata_eval.core.agentic.general_question import evaluate_agentic_general_question
from gooddata_eval.core.agentic.guardrail import evaluate_agentic_guardrail
from gooddata_eval.core.agentic.kda_skill import evaluate_agentic_kda_skill
from gooddata_eval.core.agentic.metric_skill import evaluate_agentic_metric_skill
from gooddata_eval.core.agentic.search_tool import evaluate_agentic_search_tool
from gooddata_eval.core.agentic.visualization import evaluate_agentic_visualization
from gooddata_eval.core.config import ReasoningEffort
from gooddata_eval.core.models import AgenticEvalOutcome, CreatedVisualization, DatasetItem
from gooddata_eval.core.runner import EvalReport, ItemReport


class _LfKw(TypedDict, total=False):
    langfuse: Any
    dataset_item_id: str
    dataset_name: str
    run_timestamp: str
    model_version_override: str | None
    reasoning_effort: ReasoningEffort | None
    submit_trace_link: SubmitTraceLink


AGENTIC_TEST_KINDS = frozenset(
    {
        "vis_agentic",  # production: expected_output.visualization (single/multi CreatedVisualization)
        "agentic_visualization",  # experimental: expected_output.expected_outputs (multi-candidate)
        "agentic_metric_skill",
        "agentic_alert_skill",
        "agentic_search",
        "agentic_general_question",
        "agentic_guardrail",
        "agentic_conversation",
        "agentic_kda_skill",
    }
)


# Kinds cleared to run several at a time. An EXPLICIT allowlist, not a subtraction: nothing
# in this package can prove a kind is read-only, because the mutation happens server-side in
# whichever tools the agent decides to call. So each entry here is a reviewed judgement, and
# anything absent -- including a kind added later -- runs serially. Slow is a recoverable
# mistake; two runs sharing a workspace mid-mutation corrupts eval results silently and
# reads like a model regression.
#
#   agentic_general_question, agentic_guardrail  answer questions only, no tool writes
#   agentic_search                               search_objects, read-only by definition
#   vis_agentic, agentic_visualization           visualizations come back as AAC proposals
#                                                in the chat response; nothing is persisted
#                                                and neither module has cleanup code
PARALLEL_SAFE_TEST_KINDS = frozenset(
    {
        "agentic_general_question",
        "agentic_guardrail",
        "agentic_search",
        "vis_agentic",
        "agentic_visualization",
    }
)

# Everything else. metric_skill and alert_skill demonstrably create workspace objects (they
# carry delete_entity_metrics / delete_entity_automations cleanup) and metric_skill._delete_metric
# records that a leaked metric gets reused by a later test. agentic_conversation drives the
# metric skill. agentic_kda_skill is here on suspicion rather than proof: it triggers
# create_key_driver_analysis with no cleanup, and while the evaluator only ever reads that
# call's ARGUMENTS -- never a created object id -- whether the platform persists anything is
# unverified. Move it to the allowlist once someone confirms it does not.
WORKSPACE_MUTATING_TEST_KINDS = frozenset(AGENTIC_TEST_KINDS) - PARALLEL_SAFE_TEST_KINDS


def runs_in_parallel(test_kind: str) -> bool:
    """True only for kinds explicitly cleared for concurrent execution."""
    return test_kind in PARALLEL_SAFE_TEST_KINDS


def _parse_visualization_expected(expected_output: Any) -> list[CreatedVisualization]:
    """Parse expected_output into a list of CreatedVisualization candidates.

    Accepts:
      {"expected_outputs": [{"visualization": {...}}, ...]}  <- agentic fixture format
      {"visualization": {...}} or {"visualization": [{...}]}  <- single/multi candidate
      [{"visualization": {...}}, ...]                          <- bare list
    """
    if isinstance(expected_output, dict):
        raw_list = expected_output.get("expected_outputs")
        if raw_list is not None:
            return [
                CreatedVisualization.model_validate(v.get("visualization", v) if isinstance(v, dict) else v)
                for v in raw_list
            ]
        raw_viz = expected_output.get("visualization")
        if raw_viz is not None:
            if isinstance(raw_viz, list):
                return [CreatedVisualization.model_validate(v) for v in raw_viz]
            return [CreatedVisualization.model_validate(raw_viz)]
    if isinstance(expected_output, list):
        return [
            CreatedVisualization.model_validate(v.get("visualization", v) if isinstance(v, dict) else v)
            for v in expected_output
        ]
    raise ValueError(
        f"Cannot parse agentic_visualization expected_output: {type(expected_output).__name__}. "
        'Expected {"expected_outputs": [...]} or {"visualization": {...}}.'
    )


def _dispatch_agentic(
    item: DatasetItem,
    host: str,
    token: str,
    workspace_id: str,
    k: int,
    langfuse: Any,
    run_ts: str,
    model_version_override: str | None,
    reasoning_effort: ReasoningEffort | None = None,
    agent_id: str | None = None,
    submit_trace_link: SubmitTraceLink = run_trace_link_inline,
) -> AgenticEvalOutcome:
    """Call the appropriate evaluate_agentic_* function for the item's test_kind.

    Every evaluate_agentic_* function returns an AgenticEvalOutcome (reasoning_steps,
    conversation_id, response_id, detail) on success and attaches the same four attributes
    to its raised *AssertionError on failure -- no kind is exempt.
    """
    kind = item.test_kind
    eo = item.expected_output
    lf_kw: _LfKw = {
        "langfuse": langfuse,
        "dataset_item_id": item.id,
        "dataset_name": item.dataset_name,
        "run_timestamp": run_ts,
        "model_version_override": model_version_override,
        "reasoning_effort": reasoning_effort,
        "submit_trace_link": submit_trace_link,
    }

    if kind in ("vis_agentic", "agentic_visualization"):
        return evaluate_agentic_visualization(
            host=host,
            token=token,
            workspace_id=workspace_id,
            question=item.question,
            expected_outputs=_parse_visualization_expected(eo),
            k=k,
            agent_id=agent_id,
            **lf_kw,
        )
    elif kind == "agentic_metric_skill":
        return evaluate_agentic_metric_skill(
            host=host,
            token=token,
            workspace_id=workspace_id,
            question=item.question,
            expected_output=eo if isinstance(eo, (dict, list)) else {},
            k=k,
            agent_id=agent_id,
            **lf_kw,
        )
    elif kind == "agentic_alert_skill":
        return evaluate_agentic_alert_skill(
            host=host,
            token=token,
            workspace_id=workspace_id,
            question=item.question,
            expected_output=eo if isinstance(eo, dict) else {},
            k=k,
            agent_id=agent_id,
            **lf_kw,
        )
    elif kind == "agentic_search":
        eo_dict = eo if isinstance(eo, dict) else {}
        tool_call = eo_dict.get("tool_call", {})
        expected_args = tool_call.get("function_arguments", eo_dict)
        return evaluate_agentic_search_tool(
            host=host,
            token=token,
            workspace_id=workspace_id,
            question=item.question,
            expected_tool_call=expected_args,
            k=k,
            agent_id=agent_id,
            **lf_kw,
        )
    elif kind == "agentic_general_question":
        return evaluate_agentic_general_question(
            host=host,
            token=token,
            workspace_id=workspace_id,
            question=item.question,
            expected_output=eo if isinstance(eo, str) else str(eo),
            k=k,
            agent_id=agent_id,
            user_context=item.user_context,
            **lf_kw,
        )
    elif kind == "agentic_guardrail":
        return evaluate_agentic_guardrail(
            host=host,
            token=token,
            workspace_id=workspace_id,
            question=item.question,
            expected_output=eo if isinstance(eo, str) else str(eo),
            k=k,
            agent_id=agent_id,
            **lf_kw,
        )
    elif kind == "agentic_kda_skill":
        return evaluate_agentic_kda_skill(
            host=host,
            token=token,
            workspace_id=workspace_id,
            question=item.question,
            expected_output=eo if isinstance(eo, dict) else {},
            k=k,
            agent_id=agent_id,
            **lf_kw,
        )
    elif kind == "agentic_conversation":
        fixture_data = eo.get("fixture") or eo if isinstance(eo, dict) else {}
        return evaluate_agentic_conversation(
            host=host,
            token=token,
            workspace_id=workspace_id,
            fixture=ConversationFixture.model_validate(fixture_data),
            agent_id=agent_id,
            **lf_kw,
        )
    else:
        raise ValueError(f"Unknown agentic test kind: {kind!r}")


def _apply_run_counts(item_report: ItemReport, source: Any) -> None:
    """Copy how many runs passed, and how many actually ran, onto the item report.

    Kinds that report neither keep the requested K and a 0 count, which reads as "not
    instrumented" rather than "nothing passed" because ``pass_power_k`` is only consulted
    for an item that already passed.
    """
    runs_passed = getattr(source, "runs_passed", None)
    if runs_passed is not None:
        item_report.runs_passed = runs_passed
    effective = getattr(source, "runs_effective", None)
    if effective:
        # Only when the kind knows better than K -- agentic_conversation runs once.
        item_report.runs_effective = effective


def _apply_timings(item_report: ItemReport, timings: Any) -> None:
    """Copy an outcome's phase breakdown onto the item report, if the kind recorded one.

    Kinds with no phase instrumentation pass None and keep their 0.0 defaults rather than
    reporting invented numbers.
    """
    if timings is None:
        return
    item_report.agent_latency_s = timings.agent_s
    item_report.judge_latency_s = timings.judge_s
    item_report.simulated_user_latency_s = timings.simulated_user_s


def run_agentic_items(
    items: list[DatasetItem],
    host: str,
    token: str,
    workspace_id: str,
    *,
    k: int = 2,
    model_version: str | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    use_langfuse: bool = False,
    run_ts: str,
    on_item_start: Any = None,
    on_item_done: Any = None,
    agent_id: str | None = None,
    concurrency: int = 1,
) -> EvalReport:
    """Run agentic items through evaluate_agentic_* and return an EvalReport.

    ``concurrency`` > 1 runs PARALLEL_SAFE_TEST_KINDS items simultaneously.
    WORKSPACE_MUTATING_TEST_KINDS items always run one at a time, and in a separate phase
    from the parallel ones -- a metric being created and dropped mid-run would otherwise be
    visible to a catalog-reading item running alongside it.

    Results are collected in dataset order regardless of completion order.
    """
    langfuse = make_langfuse_client() if use_langfuse else None

    report = EvalReport(model=model_version)
    total = len(items)
    # Trace linking runs here rather than inside each evaluate_agentic_*, so an item's
    # Langfuse poll overlaps the NEXT item's agent call instead of extending its own
    # latency. Drained below before this function returns, so every score is written
    # before the caller renders a report or decides an exit code.
    linker = BackgroundTraceLinker()
    _t0 = time.perf_counter()

    def _process_item(index: int, item: DatasetItem) -> ItemReport:
        if on_item_start is not None:
            try:
                on_item_start(index, total, item)
            except Exception:
                pass

        item_report = ItemReport(
            id=item.id,
            dataset_name=item.dataset_name,
            test_kind=item.test_kind,
            question=item.question,
        )
        t0 = time.perf_counter()
        try:
            outcome = _dispatch_agentic(
                item,
                host,
                token,
                workspace_id,
                k,
                langfuse,
                run_ts,
                model_version,
                reasoning_effort,
                agent_id,
                submit_trace_link=linker.submit,
            )
            if isinstance(outcome, AgenticEvalOutcome):
                reasoning_steps = outcome.reasoning_steps
                conversation_id = outcome.conversation_id
                response_id = outcome.response_id
                detail = outcome.detail
            else:
                reasoning_steps, conversation_id, response_id, detail = outcome, None, None, {}
            item_report.pass_at_k = True
            item_report.runs = k
            item_report.reasoning_steps = reasoning_steps or []
            item_report.conversation_id = conversation_id
            item_report.response_id = response_id
            item_report.best_detail = detail or {}
            _apply_timings(item_report, getattr(outcome, "timings", None))
            _apply_run_counts(item_report, outcome)
        except AssertionError as exc:
            item_report.pass_at_k = False
            item_report.runs = k
            item_report.reasoning_steps = getattr(exc, "reasoning_steps", None) or []
            item_report.conversation_id = getattr(exc, "conversation_id", None)
            item_report.response_id = getattr(exc, "response_id", None)
            item_report.best_detail = getattr(exc, "detail", None) or {}
            _apply_timings(item_report, getattr(exc, "timings", None))
            _apply_run_counts(item_report, exc)
            print(f"[agentic] {item.id} FAIL: {exc}", flush=True)
        except Exception as exc:
            item_report.error = f"{type(exc).__name__}: {exc}"
            item_report.runs = 0
            # An item that errored still measured whatever it got through, and those are
            # the most useful numbers on the report -- an item unevaluable because its
            # judge broke should not also report the agent as costing 0s. Kinds that
            # attach no timings to the exception keep their 0.0 defaults.
            _apply_timings(item_report, getattr(exc, "timings", None))
        finally:
            item_report.latency_s = time.perf_counter() - t0

        if on_item_done is not None:
            try:
                on_item_done(index, total, item_report)
            except Exception:
                pass

        return item_report

    concurrency = max(1, concurrency)
    indexed = list(enumerate(items, start=1))
    if concurrency > 1:
        parallel = [(i, it) for i, it in indexed if runs_in_parallel(it.test_kind)]
        serial = [(i, it) for i, it in indexed if not runs_in_parallel(it.test_kind)]
        if not parallel and serial:
            blocked = ", ".join(sorted({it.test_kind for _, it in serial}))
            print(
                f"warning: --concurrency {concurrency} has no effect here; every item is a "
                f"workspace-mutating kind ({blocked}) and those always run one at a time.",
                file=sys.stderr,
            )
    else:
        parallel, serial = [], indexed

    results: dict[int, ItemReport] = {}
    try:
        # Two phases, never interleaved: a mutating item creating and dropping a metric
        # mid-run would otherwise be visible to a catalog-reading item beside it.
        if parallel:
            # NOT a `with` block. ThreadPoolExecutor.__exit__ is shutdown(wait=True) with
            # cancel_futures left False, so an interrupt raised in this thread while it
            # waits on as_completed runs every QUEUED item to completion before the
            # KeyboardInterrupt is honoured. cancel_futures drops whatever has not started; the handful already in flight
            # cannot be cancelled (the interpreter joins those worker threads at exit
            # regardless), so this bounds the wait at one wave rather than the dataset.
            pool = ThreadPoolExecutor(max_workers=concurrency, thread_name_prefix="agentic")
            try:
                futures = {pool.submit(_process_item, i, it): i for i, it in parallel}
                for future in as_completed(futures):
                    results[futures[future]] = future.result()
            except BaseException:
                pool.shutdown(wait=False, cancel_futures=True)
                raise
            else:
                pool.shutdown(wait=True)
        for i, it in serial:
            results[i] = _process_item(i, it)
        report.items.extend(results[i] for i in sorted(results))
    except BaseException:
        # Ctrl-C, or anything else escaping the loop: drop the queued polls rather than
        # make the user sit through them (see BackgroundTraceLinker.abandon).
        linker.abandon()
        raise

    # Blocks until every deferred trace link has finished: "async" here means the poll
    # overlaps other items' work, never that the command finishes before scores are final.
    if linker.pending:
        # Said before the wait, not after. The batch runs once the last item is done and
        # can take tens of seconds waiting on Langfuse ingestion; without this the
        # terminal sits silent right after the final item and looks hung.
        print(
            f"[langfuse] linking traces for {linker.pending} item(s); waiting on Langfuse ingestion...",
            flush=True,
        )
    _link_t0 = time.perf_counter()
    linker.drain()
    _link_elapsed = time.perf_counter() - _link_t0
    for finished in report.items:
        finished.langfuse_latency_s = linker.durations.get(finished.id, 0.0)
    if linker.durations:
        # Surfaces whether the retry budget is binding. A slowest close to
        # _langfuse._LINK_BUDGET_SEC means links are timing out and scores are being
        # orphaned -- read it together with any "no trace found for conversation" warnings.
        slowest = max(linker.durations.values())
        print(
            f"[langfuse] trace linking finished in {_link_elapsed:.1f}s "
            f"for {len(linker.durations)} item(s); slowest {slowest:.1f}s",
            flush=True,
        )
    report.wall_clock_s = time.perf_counter() - _t0

    if langfuse is not None:
        try:
            langfuse.flush()
            langfuse.close()
        except Exception:
            pass

    return report

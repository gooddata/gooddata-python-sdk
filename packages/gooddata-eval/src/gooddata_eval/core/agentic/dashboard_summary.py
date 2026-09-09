# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic dashboard-summary evaluation runner.

Covers the path a user actually takes: the dashboard's "Summarize" menu item drops them
into the assistant with "Summarize this dashboard" pre-filled, so the summary is produced
by the conversational ``dashboard_summary`` skill, not by the dedicated
``POST /api/v1/ai/workspaces/{ws}/summary`` endpoint the ``dashboard_summary`` test kind
exercises. That endpoint sits behind its own feature flag (``ENABLE_GEN_AI_HEADLESS_SUMMARY``)
and serves API/embedding consumers; the two share an idea and nothing else.

The skill reads the dashboard from ``userContext.view.dashboard`` and collects only the
widgets that carry a ``result_id`` -- a widget without one is dropped from the summarize
scope entirely, which is why sending a bare dashboard id gets "no dashboard charts were
provided" and sending descriptors without results gets "these visualizations need to be
reloaded". In the browser the ids exist because the client has already rendered the
widgets. Here we do the same thing deliberately: walk the dashboard's layout, execute each
insight, and hand back the result ids that execution produced.

Scoring is unchanged from the single-shot kind -- ``DashboardSummaryEvaluator`` grades free
text against the fixture's ``must_include``/``must_not_include``/``rubric``, so it does not
care which transport produced the summary.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

import httpx
from gooddata_sdk import GoodDataSdk

from gooddata_eval.core.agentic._trace_linker import (
    RunIdentity,
    RunTraceContext,
    SubmitTraceLink,
    open_trace_window,
    run_trace_link_inline,
    submit_trace_scoring,
    utc_now,
)
from gooddata_eval.core.chat.sse_client import ChatClient, ChatError
from gooddata_eval.core.config import ReasoningEffort
from gooddata_eval.core.evaluators.base import ItemEvaluation
from gooddata_eval.core.evaluators.summary import DashboardSummaryEvaluator
from gooddata_eval.core.models import (
    AgenticAssertionError,
    AgenticEvalOutcome,
    DatasetItem,
    ReasoningStepEvent,
    ToolCallEvent,
    build_latency_breakdown,
)
from gooddata_eval.core.timing import PhaseTimings, log_timer

_DEFAULT_K = 1

# What the "Summarize" menu item pre-fills, used when no question is supplied. A fixture's
# own question wins: it is the localized or paraphrased wording under test, and the dispatch
# passes it through for exactly that reason. This is the default for direct callers only.
_DEFAULT_PROMPT = "Summarize this dashboard"


@dataclass
class DashboardWidget:
    """One insight widget of a dashboard, as the assistant needs to see it."""

    widget_id: str
    title: str
    visualization_id: str
    # None when the execution failed. Mirrors the browser, where a widget that did not
    # render carries no result and is therefore left out of the summarize scope.
    result_id: str | None = None


def _insight_widgets(content: dict) -> list[DashboardWidget]:
    """Every insight widget in a dashboard's layout, in document order.

    Walks the whole document rather than a fixed path: dashboards nest widgets in
    sections, and tab-based ones nest those again under ``tabs``, so the depth is not
    known ahead of time. Widgets whose insight carries no identifier are skipped -- a
    rich-text or unresolved widget has nothing to execute.
    """
    widgets: list[DashboardWidget] = []
    seen: set[str] = set()

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            insight = node.get("insight")
            if isinstance(insight, dict):
                identifier = insight.get("identifier")
                viz_id = identifier.get("id") if isinstance(identifier, dict) else None
                if viz_id:
                    widget_id = str(node.get("localIdentifier") or viz_id)
                    if widget_id not in seen:
                        seen.add(widget_id)
                        widgets.append(
                            DashboardWidget(
                                widget_id=widget_id,
                                title=str(node.get("title") or viz_id),
                                visualization_id=str(viz_id),
                            )
                        )
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(content)
    return widgets


def _execute_widget(sdk: GoodDataSdk, workspace_id: str, visualization_id: str) -> str:
    """Execute one saved visualization and return the result id its execution produced.

    Reuses the table service's own pivot/non-pivot split so the execution matches what the
    client would run for that visualization; only the result id is wanted, not the data.

    ``sdk.tables.for_visualization`` is the public equivalent, but it reads the whole result
    into an ExecutionTable and returns that instead of the response -- which discards the one
    field wanted here and pays for every row to do it. Two of the three helpers it delegates
    to are private, so they are checked up front: ``gooddata-sdk`` is depended on as
    ``~=1.74.0`` and a patch release may rename them, which would otherwise surface as an
    AttributeError on the first widget of a run rather than as a dependency problem.
    """
    import gooddata_sdk.table as table_module  # noqa: PLC0415 -- private helpers, imported at use site

    missing = [
        name
        for name in ("_vis_is_table", "_get_exec_for_pivot", "get_exec_for_non_pivot")
        if not hasattr(table_module, name)
    ]
    if missing:
        raise RuntimeError(
            f"gooddata_sdk.table no longer provides {', '.join(missing)}, so a dashboard widget cannot be "
            "executed for its result id. The installed gooddata-sdk has moved these helpers -- either pin it "
            "back or port _execute_widget onto whatever replaced them."
        )

    visualization = sdk.visualizations.get_visualization(workspace_id, visualization_id)
    is_pivot = table_module._vis_is_table(visualization) or visualization.has_bucket_of_type(
        table_module.BucketType.ROWS
    )
    exec_def = (
        table_module._get_exec_for_pivot(visualization)
        if is_pivot
        else table_module.get_exec_for_non_pivot(visualization)
    )
    return sdk.compute.for_exec_def(workspace_id, exec_def).result_id


def _fetch_dashboard(host: str, token: str, workspace_id: str, dashboard_id: str) -> tuple[str | None, dict]:
    """The dashboard's title and layout document.

    Read over plain HTTP rather than through ``entities_api``: the generated client
    validates the entity's timestamp fields with a regex and raises
    ``TypeError: expected string or bytes-like object, got 'datetime.datetime'`` on the
    response, so the typed accessor cannot read a dashboard at all today.
    """
    url = f"{host.rstrip('/')}/api/v1/entities/workspaces/{workspace_id}/analyticalDashboards/{dashboard_id}"
    resp = httpx.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=120.0)
    resp.raise_for_status()
    attributes = resp.json()["data"]["attributes"]
    return attributes.get("title"), attributes.get("content") or {}


def build_dashboard_user_context(
    sdk: GoodDataSdk,
    host: str,
    token: str,
    workspace_id: str,
    dashboard_id: str,
    *,
    only_visualizations: list[str] | None = None,
    max_widgets: int | None = None,
) -> tuple[dict, list[DashboardWidget]]:
    """Assemble the ``userContext`` for one dashboard, executing its widgets to get result ids.

    Returns the context and the widgets it describes, each carrying the result id its
    execution produced or None if that execution failed. A failed widget is still returned
    (reporting needs to know the summary was partial) but is left out of the context, since
    the skill would drop it anyway.

    A dashboard of thirty widgets costs thirty executions per item, so both arguments exist
    to bound that -- at the price of summarizing less than the user would see.
    ``only_visualizations`` keeps just the named visualizations, which is what a fixture sets
    (via ``summary_input.visualizations``, the same field and meaning the headless endpoint
    gives it) because naming the widgets a rubric asserts on stays stable as the dashboard
    grows. ``max_widgets`` truncates in layout order and is a blunt cap for direct callers.
    """
    title, content = _fetch_dashboard(host, token, workspace_id, dashboard_id)

    widgets = _insight_widgets(content)
    if only_visualizations is not None:
        wanted = set(only_visualizations)
        widgets = [w for w in widgets if w.visualization_id in wanted or w.widget_id in wanted]
    if max_widgets is not None:
        widgets = widgets[:max_widgets]

    for widget in widgets:
        try:
            widget.result_id = _execute_widget(sdk, workspace_id, widget.visualization_id)
        except Exception as exc:  # noqa: BLE001, PERF203 -- one dead widget must not lose the whole summary
            log_timer(f"[dashboard_summary] widget '{widget.widget_id}' failed to execute: {exc}")

    context = {
        "view": {
            "dashboard": {
                "id": dashboard_id,
                "title": title,
                "widgets": [
                    {
                        "widgetId": w.widget_id,
                        "title": w.title,
                        "widgetType": "insight",
                        "visualizationId": w.visualization_id,
                        "resultId": w.result_id,
                    }
                    for w in widgets
                    if w.result_id is not None
                ],
            }
        }
    }
    return context, widgets


@dataclass
class DashboardSummaryRunResult:
    """Outcome of one K-run conversation for a dashboard summary."""

    conversation_id: str
    actual_output: str
    evaluation: ItemEvaluation
    widgets_total: int
    widgets_executed: int
    reasoning_steps: list[str] = field(default_factory=list)
    response_id: str | None = None
    timings: PhaseTimings = field(default_factory=PhaseTimings)
    tool_call_events: list[ToolCallEvent] = field(default_factory=list)
    reasoning_step_events: list[ReasoningStepEvent] = field(default_factory=list)
    # Set when the chat call itself failed. Such a run has no summary to grade, so it is
    # recorded rather than raised -- raising would discard the K-runs already completed.
    chat_error: str | None = None

    @property
    def passed(self) -> bool:
        return self.chat_error is None and self.evaluation.passed


@dataclass
class AgenticDashboardSummarySummary:
    """Aggregated outcome of K runs for one dashboard-summary item."""

    run_results: list[DashboardSummaryRunResult]
    pass_at_k: bool
    pass_power_k: bool
    best: DashboardSummaryRunResult


def _failed_run(
    conversation_id: str, message: str, widgets: list[DashboardWidget], agent_s: float
) -> DashboardSummaryRunResult:
    """A run that never produced a summary, recorded so the completed runs survive."""
    return DashboardSummaryRunResult(
        conversation_id=conversation_id,
        actual_output="",
        evaluation=ItemEvaluation(passed=False, rank_key=(-1, 0.0), detail={}, error=message),
        widgets_total=len(widgets),
        widgets_executed=sum(1 for w in widgets if w.result_id is not None),
        timings=PhaseTimings(agent_s=agent_s),
        chat_error=message,
    )


def _run_single_dashboard_summary(
    client: ChatClient,
    evaluator: DashboardSummaryEvaluator,
    conversation_id: str,
    item: DatasetItem,
    user_context: dict,
    widgets: list[DashboardWidget],
    prompt: str,
) -> DashboardSummaryRunResult:
    widgets_total = len(widgets)
    widgets_executed = sum(1 for w in widgets if w.result_id is not None)

    agent_started = time.monotonic()
    try:
        chat_result = client.send_message(conversation_id, prompt, user_context=user_context)
    except ChatError as exc:
        return _failed_run(conversation_id, f"chat failed: {exc}", widgets, time.monotonic() - agent_started)
    agent_elapsed = time.monotonic() - agent_started

    judge_started = time.monotonic()
    evaluation = evaluator.evaluate(item, chat_result)
    judge_elapsed = time.monotonic() - judge_started
    log_timer(
        f"[timer] dashboard_summary {conversation_id} agent {agent_elapsed:.2f}s, judge {judge_elapsed:.2f}s "
        f"({widgets_executed}/{widgets_total} widgets executed)"
    )

    return DashboardSummaryRunResult(
        conversation_id=conversation_id,
        actual_output=str(evaluation.detail.get("actual_output", "")),
        evaluation=evaluation,
        widgets_total=widgets_total,
        widgets_executed=widgets_executed,
        reasoning_steps=list(chat_result.reasoning_steps or []),
        response_id=chat_result.response_id,
        timings=PhaseTimings(agent_s=agent_elapsed, judge_s=judge_elapsed),
        tool_call_events=list(chat_result.tool_call_events or []),
        reasoning_step_events=list(chat_result.reasoning_step_events or []),
    )


def run_agentic_dashboard_summary(
    host: str,
    token: str,
    workspace_id: str,
    dashboard_id: str,
    expected_output: Any,
    question: str = _DEFAULT_PROMPT,
    k: int = _DEFAULT_K,
    max_iterations: int = 1,  # noqa: ARG001 -- single-turn kind; accepted so the runner can dispatch uniformly
    initial_conversation_id: str | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    agent_id: str | None = None,
    only_visualizations: list[str] | None = None,
    max_widgets: int | None = None,
    dataset_item_id: str = "",
    dataset_name: str = "dashboard_summary",
) -> AgenticDashboardSummarySummary:
    """Run the agentic dashboard-summary evaluation K times and return a summary.

    The widgets are executed ONCE and their result ids reused across all K runs: they
    identify cached executions, so re-running them per K would multiply the most expensive
    part of the item without changing what the assistant sees.
    """
    client = ChatClient(
        host=host, token=token, workspace_id=workspace_id, reasoning_effort=reasoning_effort, agent_id=agent_id
    )
    sdk = GoodDataSdk.create(host, token)
    evaluator = DashboardSummaryEvaluator()
    item = DatasetItem(
        id=dataset_item_id or dashboard_id,
        dataset_name=dataset_name,
        test_kind="agentic_dashboard_summary",
        question=question,
        expected_output=expected_output,
    )
    run_results: list[DashboardSummaryRunResult] = []

    try:
        context_started = time.monotonic()
        user_context, widgets = build_dashboard_user_context(
            sdk,
            host,
            token,
            workspace_id,
            dashboard_id,
            only_visualizations=only_visualizations,
            max_widgets=max_widgets,
        )
        log_timer(
            f"[timer] dashboard_summary {dashboard_id} context built in "
            f"{time.monotonic() - context_started:.2f}s ({len(widgets)} widgets)"
        )

        conv_id_0 = initial_conversation_id if initial_conversation_id is not None else client.create_conversation()
        try:
            run_results.append(
                _run_single_dashboard_summary(client, evaluator, conv_id_0, item, user_context, widgets, question)
            )
        finally:
            if initial_conversation_id is None:
                client.delete_conversation(conv_id_0)

        for _ in range(1, k):
            try:
                conv_id = client.create_conversation()
            except Exception as exc:  # noqa: BLE001 -- a lost conversation must not discard completed runs
                # Same contract as the ChatError path below: this line used to sit outside any
                # handler, so a transient failure here on run 2 of 3 threw away run 1.
                run_results.append(_failed_run("", f"conversation creation failed: {exc}", widgets, 0.0))
                continue
            try:
                run_results.append(
                    _run_single_dashboard_summary(client, evaluator, conv_id, item, user_context, widgets, question)
                )
            finally:
                client.delete_conversation(conv_id)
    finally:
        client.close()

    scored = [r for r in run_results if r.chat_error is None]
    pass_at_k = any(r.passed for r in scored)
    pass_power_k = len(scored) == len(run_results) and bool(scored) and all(r.passed for r in scored)
    best = max(scored or run_results, key=lambda r: r.evaluation.rank_key)
    return AgenticDashboardSummarySummary(
        run_results=run_results,
        pass_at_k=pass_at_k,
        pass_power_k=pass_power_k,
        best=best,
    )


def _detail(summary: AgenticDashboardSummarySummary) -> dict:
    best = summary.best
    detail = dict(best.evaluation.detail)
    # How much of the dashboard the summary actually covered. A summary graded against a
    # rubric that mentions a widget which never executed fails for a reason that has
    # nothing to do with the agent, so the ratio has to be visible in the report.
    detail["widgets_total"] = best.widgets_total
    detail["widgets_executed"] = best.widgets_executed
    if best.chat_error is not None:
        detail["chat_error"] = best.chat_error
    detail["latency_breakdown"] = build_latency_breakdown(best.tool_call_events, best.reasoning_step_events)
    return detail


class DashboardSummaryAssertionError(AgenticAssertionError):
    """Raised when an agentic dashboard-summary evaluation fails."""


def evaluate_agentic_dashboard_summary(
    host: str,
    token: str,
    workspace_id: str,
    dashboard_id: str,
    expected_output: Any,
    question: str = _DEFAULT_PROMPT,
    k: int = _DEFAULT_K,
    initial_conversation_id: str | None = None,
    agent_id: str | None = None,
    langfuse: object | None = None,
    dataset_item_id: str = "",
    dataset_name: str = "dashboard_summary",
    run_timestamp: str | None = None,
    model_version_override: str | None = None,
    run_metadata_extra: dict | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    submit_trace_link: SubmitTraceLink = run_trace_link_inline,
    only_visualizations: list[str] | None = None,
    max_widgets: int | None = None,
) -> AgenticEvalOutcome:
    """Run the evaluation, log to Langfuse, and raise DashboardSummaryAssertionError on failure."""
    langfuse, window_start = open_trace_window(langfuse)
    summary = run_agentic_dashboard_summary(
        host=host,
        token=token,
        workspace_id=workspace_id,
        dashboard_id=dashboard_id,
        expected_output=expected_output,
        question=question,
        k=k,
        initial_conversation_id=initial_conversation_id,
        reasoning_effort=reasoning_effort,
        agent_id=agent_id,
        only_visualizations=only_visualizations,
        max_widgets=max_widgets,
        dataset_item_id=dataset_item_id,
        dataset_name=dataset_name,
    )

    if langfuse is not None and dataset_item_id:
        window_end = utc_now()

        def _write_scores(ctx: RunTraceContext) -> None:
            for run_idx, run in enumerate(summary.run_results):
                if run.chat_error is not None:
                    # The chat never produced a summary, so there is no verdict: writing
                    # 0.0 would publish a content failure the judge never assessed.
                    continue
                pt = ctx.trace(run.conversation_id)
                with ctx.observe(pt, run_idx) as tid:
                    ctx.score(
                        tid, name="dashboard_summary_pass", value=float(run.evaluation.passed), data_type="BOOLEAN"
                    )
                    ctx.quality(
                        tid,
                        strict_checks={"dashboard_summary_pass": run.evaluation.passed},
                        latency_sec=pt.latency if pt else None,
                        cost_usd=pt.total_cost if pt else None,
                    )

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
            dataset_item_id=dataset_item_id,
            # A run whose chat failed is skipped above, so polling for its trace would only
            # spend the item's shared retry budget on scores that never get written.
            conversation_ids=[r.conversation_id for r in summary.run_results if r.chat_error is None],
            window_start=window_start,
            window_end=window_end,
            suffix_runs=len(summary.run_results) > 1,
            write_scores=_write_scores,
        )

    best = summary.best
    detail = _detail(summary)
    timings = PhaseTimings()
    for run in summary.run_results:
        timings = timings + run.timings
    runs_passed = sum(1 for r in summary.run_results if r.passed)

    if not summary.pass_at_k:
        error = DashboardSummaryAssertionError(
            f"Dashboard summary failed for '{dashboard_id}' "
            f"({best.widgets_executed}/{best.widgets_total} widgets executed): "
            f"{best.evaluation.error or 'criteria not satisfied'}"
        )
        error.reasoning_steps = best.reasoning_steps
        error.conversation_id = best.conversation_id
        error.response_id = best.response_id
        error.detail = detail
        error.timings = timings
        error.runs_passed = runs_passed
        error.runs_effective = len(summary.run_results)
        raise error

    return AgenticEvalOutcome(
        reasoning_steps=best.reasoning_steps,
        conversation_id=best.conversation_id,
        response_id=best.response_id,
        detail=detail,
        timings=timings,
        runs_passed=runs_passed,
        runs_effective=len(summary.run_results),
    )

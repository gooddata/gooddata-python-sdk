# (C) 2026 GoodData Corporation. All rights reserved.
"""Chat summary of a widget or a dashboard, sent the way the UI sends it.

The UI's "Summarize" items (widget menu, dashboard or tab menu) open the assistant with a
fixed question and a `userContext` that describes the dashboard on screen: its definition,
the live filter bar, the active tab, and every widget with the result id it rendered and
the filters that reached it. The skills read the data through those result ids.

A result id is a key into a result cache and expires, so an item cannot store one. It
stores the UI's `userContext` without result ids, plus each widget's execution (the AFM
and result spec the UI ran, filters included). Before each conversation the executions
run again and the fresh result ids go back into the context. Nothing here resolves
filters: the stored execution already carries the filters the widget rendered with, which
is the only way a KPI's comparison measures, a chart's dimensions and a widget that
ignores the dashboard date filter all stay as the user saw them.
"""

from __future__ import annotations

import copy
import time
from dataclasses import dataclass, field
from typing import Any, cast

import httpx

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
from gooddata_eval.core.chat.render import render_answer_text
from gooddata_eval.core.chat.sse_client import ChatClient, ChatError
from gooddata_eval.core.config import ReasoningEffort
from gooddata_eval.core.evaluators.base import ItemEvaluation
from gooddata_eval.core.evaluators.chat_summary import SummaryScope, evaluate_turn, make_judges
from gooddata_eval.core.models import (
    AgenticAssertionError,
    AgenticEvalOutcome,
    AgenticSummaryInput,
    ChatResult,
    WidgetExecution,
    build_latency_breakdown,
)
from gooddata_eval.core.timing import PhaseTimings, log_timer

# The questions the UI pre-fills. An item's own question wins.
WIDGET_QUESTION = 'Summarize the visualization "{title}"'
DASHBOARD_QUESTION = "Summarize this dashboard"

_EXECUTE_TIMEOUT_S = 120.0


def execute_widget(client: httpx.Client, workspace_id: str, execution: WidgetExecution) -> str:
    """Run one stored execution and return the id of the result it produced."""
    body: dict[str, Any] = {"execution": execution.afm, "resultSpec": execution.result_spec}
    resp = client.post(f"/api/v1/actions/workspaces/{workspace_id}/execution/afm/execute", json=body)
    resp.raise_for_status()
    return str(resp.json()["executionResponse"]["links"]["executionResult"])


def execute_widgets(
    host: str, token: str, workspace_id: str, executions: dict[str, WidgetExecution]
) -> dict[str, str | None]:
    """Fresh result ids per widget id; None for a widget whose execution failed.

    A failed widget is kept with None rather than raised: the UI sends a widget that did
    not render without a result id, and the summary is still asked for.
    """
    result_ids: dict[str, str | None] = {}
    with httpx.Client(
        base_url=host.rstrip("/"), headers={"Authorization": f"Bearer {token}"}, timeout=_EXECUTE_TIMEOUT_S
    ) as client:
        for widget_id, execution in executions.items():
            try:
                result_ids[widget_id] = execute_widget(client, workspace_id, execution)
            except (httpx.HTTPError, KeyError) as exc:  # noqa: PERF203 -- one dead widget must not lose the item
                log_timer(f"[chat_summary] widget '{widget_id}' failed to execute: {exc}")
                result_ids[widget_id] = None
    return result_ids


def _has_values(data: Any) -> bool:
    if isinstance(data, list):
        return any(_has_values(v) for v in data)
    return data is not None


def widgets_with_data(host: str, token: str, workspace_id: str, result_ids: dict[str, str | None]) -> set[str]:
    """Widget ids whose result holds at least one value; a result that cannot be read counts as empty."""
    with_data: set[str] = set()
    with httpx.Client(
        base_url=host.rstrip("/"), headers={"Authorization": f"Bearer {token}"}, timeout=_EXECUTE_TIMEOUT_S
    ) as client:
        for widget_id, result_id in result_ids.items():
            if not result_id:
                continue
            try:
                resp = client.get(f"/api/v1/actions/workspaces/{workspace_id}/execution/afm/execute/result/{result_id}")
                resp.raise_for_status()
            except httpx.HTTPError as exc:  # noqa: PERF203 -- read the next widget anyway
                log_timer(f"[chat_summary] result of widget '{widget_id}' unreadable: {exc}")
                continue
            if _has_values(resp.json().get("data")):
                with_data.add(widget_id)
    return with_data


def referenced_widget_ids(user_context: dict[str, Any]) -> list[str]:
    return [
        str(o.get("id"))
        for group in user_context.get("referencedObjects") or []
        if isinstance(group, dict)
        for o in group.get("objects") or []
        if isinstance(o, dict) and o.get("type") == "WIDGET"
    ]


def is_kpi(execution: WidgetExecution) -> bool:
    """A KPI (headline): no attributes and one result dimension holding only the measures.

    A chart of measures only (donut, waterfall, bullet) has no attributes either, but lays the
    measures out on a second dimension. Without a result spec, no attributes is all there is.
    """
    if execution.afm.get("attributes"):
        return False
    dims = execution.result_spec.get("dimensions")
    if not isinstance(dims, list) or not dims:
        return True
    return len(dims) == 1 and isinstance(dims[0], dict) and dims[0].get("itemIdentifiers") == ["measureGroup"]


def summary_scope(
    summary_input: AgenticSummaryInput, user_context: dict[str, Any], with_data: set[str]
) -> SummaryScope:
    """What the summarized widgets are: the referenced ones for a widget summary, all for a dashboard."""
    executions = summary_input.executions
    in_scope = referenced_widget_ids(user_context) if summary_input.scope == "widget" else list(executions)
    in_scope = [w for w in in_scope if w in executions]
    kpi_only = bool(in_scope) and all(is_kpi(executions[w]) for w in in_scope)
    return SummaryScope(
        scope=summary_input.scope,
        kpi_only=kpi_only,
        all_empty=not any(w in with_data for w in in_scope),
    )


def _widgets(user_context: dict[str, Any]) -> list[dict[str, Any]]:
    view = user_context.get("view")
    dashboard = view.get("dashboard") if isinstance(view, dict) else None
    widgets = dashboard.get("widgets") if isinstance(dashboard, dict) else None
    if not isinstance(widgets, list):
        return []
    return [cast(dict[str, Any], w) for w in widgets if isinstance(w, dict)]


def with_result_ids(user_context: dict[str, Any], result_ids: dict[str, str | None]) -> dict[str, Any]:
    """A copy of the stored context with each widget's fresh result id.

    A widget with no fresh result id is sent without the key, as the UI sends a widget
    that did not render. A stored result id is always dropped: it has expired.
    """
    context = copy.deepcopy(user_context)
    for widget in _widgets(context):
        widget.pop("resultId", None)
        result_id = result_ids.get(str(widget.get("widgetId", "")))
        if result_id:
            widget["resultId"] = result_id
    return context


def missing_executions(user_context: dict[str, Any], executions: dict[str, WidgetExecution]) -> list[str]:
    """Insight widgets of the context with no stored execution: they would reach the agent without data."""
    return [
        str(w.get("widgetId"))
        for w in _widgets(user_context)
        if w.get("widgetType", "insight") != "richText" and str(w.get("widgetId")) not in executions
    ]


def default_question(summary_input: AgenticSummaryInput, user_context: dict[str, Any]) -> str:
    """The UI's pre-filled question: the referenced widget's title, or the dashboard one."""
    if summary_input.scope == "dashboard":
        return DASHBOARD_QUESTION
    referenced = set(referenced_widget_ids(user_context))
    titles = [str(w.get("title")) for w in _widgets(user_context) if str(w.get("widgetId")) in referenced]
    if len(titles) != 1:
        raise ValueError(
            f"A widget summary needs exactly one referenced widget to phrase the UI question, found {len(titles)}; "
            "set the item question instead."
        )
    return WIDGET_QUESTION.format(title=titles[0])


@dataclass
class SummaryTurn:
    """One question and what the agent answered to it."""

    question: str
    result: ChatResult | None = None
    error: str | None = None
    agent_s: float = 0.0


@dataclass
class SummaryConversation:
    """One run: the summary turn and its follow-ups, in order."""

    conversation_id: str
    turns: list[SummaryTurn] = field(default_factory=list)
    widgets_total: int = 0
    widgets_executed: int = 0
    scope: SummaryScope | None = None
    # One verdict per answered turn, set by evaluate_chat_summary.
    evaluations: list[ItemEvaluation] = field(default_factory=list)
    judge_s: float = 0.0

    @property
    def chat_error(self) -> str | None:
        return next((t.error for t in self.turns if t.error), None)


def run_summary_conversation(
    client: ChatClient,
    conversation_id: str,
    questions: list[str],
    user_context: dict[str, Any],
) -> list[SummaryTurn]:
    """Send the summary question and each follow-up in one conversation, with the same context.

    The UI keeps the dashboard context attached for every message of the conversation, so
    the follow-ups carry it too. A failed turn ends the conversation: a later answer would
    rest on a turn the agent never answered.
    """
    turns: list[SummaryTurn] = []
    for question in questions:
        started = time.monotonic()
        try:
            result = client.send_message(conversation_id, question, user_context=user_context)
        except ChatError as exc:
            turns.append(SummaryTurn(question, error=f"chat failed: {exc}", agent_s=time.monotonic() - started))
            break
        turns.append(SummaryTurn(question, result=result, agent_s=time.monotonic() - started))
    return turns


def run_chat_summary(
    host: str,
    token: str,
    workspace_id: str,
    summary_input: AgenticSummaryInput,
    user_context: dict[str, Any],
    question: str | None = None,
    k: int = 1,
    reasoning_effort: ReasoningEffort | None = None,
    agent_id: str | None = None,
) -> list[SummaryConversation]:
    """Run the item K times; each run executes the widgets again and opens its own conversation.

    The executions run per run, not once per item: K runs that share result ids would all
    read one cached result, and a result that expires between runs would fail the later ones
    for a reason unrelated to the agent.
    """
    missing = missing_executions(user_context, summary_input.executions)
    if missing:
        raise ValueError(f"No stored execution for widgets {missing}; capture them with the item.")
    first = question or default_question(summary_input, user_context)
    questions = [first] + [f.question for f in summary_input.follow_ups]
    client = ChatClient(
        host=host, token=token, workspace_id=workspace_id, reasoning_effort=reasoning_effort, agent_id=agent_id
    )
    runs: list[SummaryConversation] = []
    try:
        for _ in range(k):
            result_ids = execute_widgets(host, token, workspace_id, summary_input.executions)
            scope = summary_scope(summary_input, user_context, widgets_with_data(host, token, workspace_id, result_ids))
            context = with_result_ids(user_context, result_ids)
            try:
                conversation_id = client.create_conversation()
            except Exception as exc:  # noqa: BLE001 -- a lost conversation must not discard completed runs
                runs.append(SummaryConversation("", [SummaryTurn(first, error=f"conversation creation failed: {exc}")]))
                continue
            try:
                turns = run_summary_conversation(client, conversation_id, questions, context)
            finally:
                client.delete_conversation(conversation_id)
            runs.append(
                SummaryConversation(
                    conversation_id,
                    turns,
                    widgets_total=len(result_ids),
                    widgets_executed=sum(1 for r in result_ids.values() if r),
                    scope=scope,
                )
            )
    finally:
        client.close()
    return runs


def _tool_names(result: ChatResult | None) -> list[str]:
    return [e.function_name for e in (result.tool_call_events if result else [])]


def grade_conversation(
    run: SummaryConversation,
    *,
    scenario: str,
    expected_outputs: list[dict[str, Any]],
    judge_model: str | None = None,
) -> bool:
    """Grade every turn of one run; the run passes when every turn passes.

    `expected_outputs[0]` grades the summary, the rest the follow-ups in order. A run whose
    chat failed has no verdict: its error is recorded and nothing is graded.
    """
    if run.chat_error is not None:
        return False
    positive, violation = make_judges(judge_model)
    started = time.monotonic()
    for index, turn in enumerate(run.turns):
        expected = expected_outputs[index] if index < len(expected_outputs) else {}
        run.evaluations.append(
            evaluate_turn(
                judge_input=f"{scenario}\nQuestion of this turn: {turn.question}",
                answer=render_answer_text(turn.result) if turn.result else "",
                tool_names=_tool_names(turn.result),
                expected=expected,
                scope=run.scope if index == 0 else None,
                positive_judge=positive,
                violation_judge=violation,
            )
        )
    run.judge_s = time.monotonic() - started
    return run_passed(run)


def run_passed(run: SummaryConversation) -> bool:
    return run.chat_error is None and bool(run.evaluations) and all(e.passed for e in run.evaluations)


def _turn_detail(run: SummaryConversation, index: int) -> dict[str, Any]:
    turn = run.turns[index]
    entry: dict[str, Any] = {"question": turn.question}
    if index < len(run.evaluations):
        evaluation = run.evaluations[index]
        entry.update(evaluation.detail)
        if evaluation.error:
            entry["error"] = evaluation.error
    elif turn.error:
        entry["error"] = turn.error
    return entry


def _run_detail(run: SummaryConversation) -> dict[str, Any]:
    """One run's diagnosis, flat like the other kinds' detail.

    - summary turn: its keys at the top level (`actual_output`, `shape_ok`, `must_include_0`, ...)
    - follow-up i (from 1): the same keys prefixed `followup_<i>_`
    """
    detail: dict[str, Any] = {}
    for index in range(len(run.turns)):
        prefix = f"followup_{index}_" if index else ""
        detail.update({f"{prefix}{key}": value for key, value in _turn_detail(run, index).items()})
    detail["widgets_total"] = run.widgets_total
    detail["widgets_executed"] = run.widgets_executed
    if run.scope is not None:
        detail["scope"] = {"scope": run.scope.scope, "kpi_only": run.scope.kpi_only, "all_empty": run.scope.all_empty}
    if run.chat_error is not None:
        detail["chat_error"] = run.chat_error
    events = [ev for t in run.turns if t.result for ev in t.result.tool_call_events]
    steps = [ev for t in run.turns if t.result for ev in t.result.reasoning_step_events]
    detail["latency_breakdown"] = build_latency_breakdown(events, steps)
    return detail


def _run_latency(run: SummaryConversation) -> float:
    return sum(t.agent_s for t in run.turns) + run.judge_s


def _last_result(run: SummaryConversation) -> ChatResult | None:
    return next((t.result for t in reversed(run.turns) if t.result), None)


class ChatSummaryAssertionError(AgenticAssertionError):
    """Raised when an agentic chat-summary evaluation fails."""


def evaluate_agentic_summary(
    host: str,
    token: str,
    workspace_id: str,
    scenario: str,
    summary_input: AgenticSummaryInput,
    user_context: dict[str, Any],
    expected_output: dict[str, Any],
    k: int = 1,
    gate: EvalGate = DEFAULT_GATE,
    agent_id: str | None = None,
    langfuse: object | None = None,
    dataset_item_id: str = "",
    dataset_name: str = "agent_summary",
    run_timestamp: str | None = None,
    model_version_override: str | None = None,
    run_metadata_extra: dict | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    submit_trace_link: SubmitTraceLink = run_trace_link_inline,
    judge_model: str | None = None,
) -> AgenticEvalOutcome:
    """Run the item K times, grade every turn, log to Langfuse, raise ChatSummaryAssertionError on failure.

    `scenario` is the item's readable line (its `question`), which the judge reads as INPUT;
    the text sent to the agent is `summary_input.question` or the UI's pre-filled one.
    """
    langfuse, window_start = open_trace_window(langfuse)
    runs = run_chat_summary(
        host,
        token,
        workspace_id,
        summary_input,
        user_context,
        question=summary_input.question,
        k=k,
        reasoning_effort=reasoning_effort,
        agent_id=agent_id,
    )
    expected_outputs = [expected_output] + [
        f.expected_output if isinstance(f.expected_output, dict) else {} for f in summary_input.follow_ups
    ]
    for run in runs:
        grade_conversation(run, scenario=scenario, expected_outputs=expected_outputs, judge_model=judge_model)

    scored = [r for r in runs if r.chat_error is None]
    pass_at_k = any(run_passed(r) for r in scored)
    pass_power_k = bool(scored) and len(scored) == len(runs) and all(run_passed(r) for r in scored)

    if langfuse is not None and dataset_item_id:
        window_end = utc_now()

        def _write_scores(ctx: RunTraceContext) -> None:
            stamp_gate_metadata(ctx.run_metadata, k=len(runs), gate=gate)
            for run_idx, run in enumerate(runs):
                if run.chat_error is not None:
                    # No answer, so no verdict: a 0.0 would publish a failure nobody graded.
                    continue
                pt = ctx.trace(run.conversation_id)
                with ctx.observe(pt, run_idx) as tid:
                    ctx.score(tid, name="summary_pass", value=float(run_passed(run)), data_type="BOOLEAN")
                    ctx.quality(
                        tid,
                        strict_checks={"summary_pass": run_passed(run)},
                        latency_sec=pt.latency if pt else None,
                        cost_usd=pt.total_cost if pt else None,
                    )
                    log_gate_scores(ctx, tid, gate=gate, pass_at_k=pass_at_k, pass_power_k=pass_power_k)

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
            conversation_ids=[r.conversation_id for r in scored],
            window_start=window_start,
            window_end=window_end,
            suffix_runs=len(runs) > 1,
            write_scores=_write_scores,
            item_input=scenario,
        )

    best = max(runs, key=lambda r: (run_passed(r), sum(e.passed for e in r.evaluations)))
    best_result = _last_result(best)
    timings = PhaseTimings()
    for run in runs:
        timings = timings + PhaseTimings(agent_s=sum(t.agent_s for t in run.turns), judge_s=run.judge_s)
    runs_passed = sum(1 for r in runs if run_passed(r))
    failed_runs = build_failed_runs(runs, passed=run_passed, detail=_run_detail)
    reasoning = list(best_result.reasoning_steps or []) if best_result else []

    if not gate_passed(gate, pass_at_k=pass_at_k, pass_power_k=pass_power_k):
        failing = next((e for e in best.evaluations if not e.passed), None)
        reason = best.chat_error or (failing.error if failing and failing.error else "criteria not satisfied")
        error = ChatSummaryAssertionError(
            f"Chat summary failed for '{scenario}'. {gate_failure_note(gate, runs_passed, len(runs))} "
            f"({best.widgets_executed}/{best.widgets_total} widgets executed): {reason}"
        )
        error.reasoning_steps = reasoning
        error.conversation_id = best.conversation_id
        error.response_id = best_result.response_id if best_result else None
        error.detail = _run_detail(best)
        error.timings = timings
        error.runs_passed = runs_passed
        error.runs_effective = len(runs)
        error.failed_runs = failed_runs
        error.run_latencies_s = [_run_latency(r) for r in runs]
        raise error

    return AgenticEvalOutcome(
        reasoning_steps=reasoning,
        conversation_id=best.conversation_id,
        response_id=best_result.response_id if best_result else None,
        detail=_run_detail(best),
        timings=timings,
        runs_passed=runs_passed,
        runs_effective=len(runs),
        failed_runs=failed_runs,
        run_latencies_s=[_run_latency(r) for r in runs],
    )

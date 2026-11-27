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

from gooddata_eval.core._retry import is_retryable_request_error, retry_transient
from gooddata_eval.core.agentic._failed_runs import build_failed_runs
from gooddata_eval.core.agentic._gate import (
    DEFAULT_GATE,
    EvalGate,
    gate_passed,
    log_gate_scores,
    stamp_gate_metadata,
)
from gooddata_eval.core.agentic._outcome import (
    agentic_detail,
    agentic_success,
    attach_labels,
    chat_failure_exit,
    failure_message_head,
    label_runs,
    mark_unscored_run,
    raise_agentic_failure,
)
from gooddata_eval.core.agentic._trace_linker import (
    RunIdentity,
    RunTraceContext,
    SubmitTraceLink,
    conversations_to_link,
    open_trace_window,
    run_trace_link_inline,
    submit_trace_scoring,
    utc_now,
)
from gooddata_eval.core.chat.render import render_answer_text
from gooddata_eval.core.chat.sse_client import ChatClient, ChatError
from gooddata_eval.core.config import ReasoningEffort
from gooddata_eval.core.evaluators._llm_judge import JudgeResponseError
from gooddata_eval.core.evaluators.base import ItemEvaluation
from gooddata_eval.core.evaluators.chat_summary import (
    CODE_CHECKS,
    SummaryScope,
    evaluate_turn,
    make_judges,
    validate_expected,
)
from gooddata_eval.core.evaluators.chat_summary_figures import Table, tables_from_tool_calls
from gooddata_eval.core.models import (
    AgenticAssertionError,
    AgenticEvalOutcome,
    AgenticSummaryInput,
    ChatResult,
    LoopExit,
    WidgetBaseline,
    WidgetExecution,
)
from gooddata_eval.core.outcome import DATA_BASELINE_CHANGED, WIDGET_EXECUTION_FAILED, setup_error
from gooddata_eval.core.timing import PhaseTimings, log_timer, run_latency_s

# The questions the UI pre-fills. An item's own question wins.
WIDGET_QUESTION = 'Summarize the visualization "{title}"'
DASHBOARD_QUESTION = "Summarize this dashboard"

_EXECUTE_TIMEOUT_S = 120.0


def execute_widget(client: httpx.Client, workspace_id: str, execution: WidgetExecution) -> str:
    """Run one stored execution and return the id of the result it produced; a 429/5xx is retried."""
    body: dict[str, Any] = {"execution": execution.afm, "resultSpec": execution.result_spec}

    def _post() -> httpx.Response:
        resp = client.post(f"/api/v1/actions/workspaces/{workspace_id}/execution/afm/execute", json=body)
        resp.raise_for_status()
        return resp

    resp = retry_transient(_post, is_retryable=is_retryable_request_error)
    return str(resp.json()["executionResponse"]["links"]["executionResult"])


def execute_widgets(
    host: str, token: str, workspace_id: str, executions: dict[str, WidgetExecution]
) -> dict[str, str | None]:
    """Fresh result ids per widget id; None for a widget whose execution failed.

    A failed widget is kept with None rather than raised, so the caller can name every failed
    widget at once; `run_chat_summary` stops the item on any of them (`WidgetExecutionError`).
    """
    result_ids: dict[str, str | None] = {}
    with httpx.Client(
        base_url=host.rstrip("/"), headers={"Authorization": f"Bearer {token}"}, timeout=_EXECUTE_TIMEOUT_S
    ) as client:
        for widget_id, execution in executions.items():
            try:
                result_ids[widget_id] = execute_widget(client, workspace_id, execution)
            except (httpx.HTTPError, KeyError, ValueError) as exc:  # one dead widget must not lose the item
                log_timer(f"[chat_summary] widget '{widget_id}' failed to execute: {exc}")
                result_ids[widget_id] = None
    return result_ids


def _has_values(data: Any) -> bool:
    if isinstance(data, list):
        return any(_has_values(v) for v in data)
    return data is not None


def fetch_results(
    host: str, token: str, workspace_id: str, result_ids: dict[str, str | None]
) -> dict[str, dict[str, Any] | None]:
    """Each widget's result body; None for a widget without a result or whose result cannot be read."""
    results: dict[str, dict[str, Any] | None] = {}
    with httpx.Client(
        base_url=host.rstrip("/"), headers={"Authorization": f"Bearer {token}"}, timeout=_EXECUTE_TIMEOUT_S
    ) as client:
        for widget_id, result_id in result_ids.items():
            results[widget_id] = None
            if not result_id:
                continue
            url = f"/api/v1/actions/workspaces/{workspace_id}/execution/afm/execute/result/{result_id}"

            def _get(url: str = url) -> httpx.Response:
                resp = client.get(url)
                resp.raise_for_status()
                return resp

            try:
                body = retry_transient(_get, is_retryable=is_retryable_request_error).json()
            except (httpx.HTTPError, ValueError) as exc:  # read the next widget anyway
                log_timer(f"[chat_summary] result of widget '{widget_id}' unreadable: {exc}")
                continue
            results[widget_id] = body if isinstance(body, dict) else None
    return results


def widgets_with_data(results: dict[str, dict[str, Any] | None]) -> set[str]:
    """Widget ids whose result holds at least one value; a result that cannot be read counts as empty."""
    return {w for w, body in results.items() if body is not None and _has_values(body.get("data"))}


def _values(data: Any) -> list[float]:
    if isinstance(data, list):
        return [v for item in data for v in _values(item)]
    if isinstance(data, (int, float)) and not isinstance(data, bool):
        return [float(data)]
    if isinstance(data, str):
        try:
            return [float(data)]
        except ValueError:
            return []
    return []


def baseline_of(result: dict[str, Any] | None) -> WidgetBaseline:
    """The baseline an item stores for a widget, from its result body (None = no result)."""
    if result is None:
        return WidgetBaseline(has_data=False, row_count=0, value_sum=0.0)
    data = result.get("data")
    paging = result.get("paging") or {}
    total = paging.get("total") if isinstance(paging, dict) else None
    rows = int(total[0]) if isinstance(total, list) and total else (len(data) if isinstance(data, list) else 0)
    return WidgetBaseline(has_data=_has_values(data), row_count=rows, value_sum=round(sum(_values(data)), 6))


def baseline_problems(
    executions: dict[str, WidgetExecution], results: dict[str, dict[str, Any] | None], titles: dict[str, str]
) -> list[str]:
    """One line per widget whose data differs from the baseline the item stores."""
    problems: list[str] = []
    for widget_id, execution in executions.items():
        expected = execution.baseline
        if expected is None:
            continue
        actual = baseline_of(results.get(widget_id))
        changes = [
            f"{name} {getattr(expected, name)} → {getattr(actual, name)}"
            for name in ("has_data", "row_count")
            if getattr(expected, name) != getattr(actual, name)
        ]
        if abs(expected.value_sum - actual.value_sum) > max(1e-6, abs(expected.value_sum) * 1e-9):
            changes.append(f"value_sum {expected.value_sum:,.2f} → {actual.value_sum:,.2f}")
        if changes:
            problems.append(f'widget "{titles.get(widget_id, widget_id)}": ' + ", ".join(changes))
    return problems


class SetupError(Exception):
    """The item's input could not be prepared; `reason` is one of `outcome.SETUP_ERRORS`."""

    reason = ""
    headline = ""

    def __init__(self, problems: list[str]):
        self.problems = problems
        super().__init__("; ".join(problems))


class DataBaselineError(SetupError):
    """The data under the item differs from the baseline it was made with."""

    reason = DATA_BASELINE_CHANGED
    headline = "the widget data changed"


class WidgetExecutionError(SetupError):
    """A stored execution did not run or its result could not be read: nothing can be said about its data."""

    reason = WIDGET_EXECUTION_FAILED
    headline = "a stored widget execution failed"


def execution_problems(
    executions: dict[str, WidgetExecution],
    result_ids: dict[str, str | None],
    results: dict[str, dict[str, Any] | None],
    titles: dict[str, str],
) -> list[str]:
    """One line per widget that has no result id or whose result has no readable body."""
    problems: list[str] = []
    for widget_id in executions:
        if result_ids.get(widget_id) is None:
            problems.append(f'widget "{titles.get(widget_id, widget_id)}": the execution failed')
        elif results.get(widget_id) is None:
            problems.append(f'widget "{titles.get(widget_id, widget_id)}": the result could not be read')
    return problems


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
    exit_reason: LoopExit | None = None  # set when the chat call raised


@dataclass
class SummaryConversation:
    """One run: the summary turn and its follow-ups, in order."""

    conversation_id: str
    turns: list[SummaryTurn] = field(default_factory=list)
    widgets_total: int = 0
    widgets_executed: int = 0
    scope: SummaryScope | None = None
    filter_years: set[int] = field(default_factory=set)
    known_text: list[str] = field(default_factory=list)
    # One verdict per answered turn, set by evaluate_chat_summary.
    evaluations: list[ItemEvaluation] = field(default_factory=list)
    judge_s: float = 0.0

    @property
    def chat_error(self) -> str | None:
        return next((t.error for t in self.turns if t.error), None)

    @property
    def exit_reason(self) -> LoopExit | None:
        """How the run's chat ended when a call raised; None for a run that got every answer."""
        return next((t.exit_reason for t in self.turns if t.exit_reason is not None), None)

    @property
    def judge_error(self) -> str | None:
        """Why the judge left the run without a verdict, when its verdict was the one still open.

        None when a code check or a graded criterion already failed the run, or the run has no answer.
        """
        if self.chat_error is not None:
            return None
        errors = [e.error for e in self.evaluations if not e.passed and e.error and e.error != "empty answer"]
        decided = [e for e in self.evaluations if not e.passed and not (e.error and e.error != "empty answer")]
        code_failed = any(e.detail.get(key) is False for e in self.evaluations for key in CODE_CHECKS)
        return errors[0] if errors and not decided and not code_failed else None


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
            turns.append(
                SummaryTurn(
                    question,
                    error=f"chat failed: {exc}",
                    agent_s=time.monotonic() - started,
                    exit_reason=chat_failure_exit(exc),
                )
            )
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
            results = fetch_results(host, token, workspace_id, result_ids)
            titles = {str(w.get("widgetId")): str(w.get("title")) for w in _widgets(user_context)}
            failed = execution_problems(summary_input.executions, result_ids, results, titles)
            if failed:
                raise WidgetExecutionError(failed)
            problems = baseline_problems(summary_input.executions, results, titles)
            if problems:
                raise DataBaselineError(problems)
            scope = summary_scope(summary_input, user_context, widgets_with_data(results))
            context = with_result_ids(user_context, result_ids)
            try:
                conversation_id = client.create_conversation()
            except (
                ChatError,
                httpx.HTTPError,
                ValueError,
            ) as exc:  # a lost conversation must not discard completed runs
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
                    filter_years=filter_years(user_context),
                    known_text=known_text(user_context),
                )
            )
    finally:
        client.close()
    return runs


def _tool_names(result: ChatResult | None) -> list[str]:
    return [e.function_name for e in (result.tool_call_events if result else [])]


def filter_years(user_context: dict[str, Any]) -> set[int]:
    """Years of the absolute date filters on screen: the filter bar and each widget's filters."""
    view = user_context.get("view")
    dashboard = view.get("dashboard") if isinstance(view, dict) else None
    found: list[dict[str, Any]] = []
    if isinstance(dashboard, dict):
        found += [vf.get("filter") for vf in dashboard.get("viewFilters") or [] if isinstance(vf, dict)]
    for widget in _widgets(user_context):
        found += [f for f in widget.get("filters") or [] if isinstance(f, dict)]
    years: set[int] = set()
    for f in found:
        if not isinstance(f, dict):
            continue
        bounds = [str(f.get(k, ""))[:4] for k in ("from", "to")]
        if all(b.isdigit() for b in bounds):
            years |= set(range(int(bounds[0]), int(bounds[1]) + 1))
    return years


def known_text(user_context: dict[str, Any]) -> list[str]:
    """Names on screen that may hold digits ("Top 10 Spenders", "1-3M"): never read as figures."""
    texts: list[str] = []
    view = user_context.get("view")
    dashboard = view.get("dashboard") if isinstance(view, dict) else None
    if isinstance(dashboard, dict):
        texts.append(str(dashboard.get("title", "")))
        for vf in dashboard.get("viewFilters") or []:
            flt = vf.get("filter") if isinstance(vf, dict) else None
            state = flt.get("state") if isinstance(flt, dict) else None
            if isinstance(state, dict):
                texts += [str(v) for values in state.values() if isinstance(values, list) for v in values]
    texts += [str(w.get("title", "")) for w in _widgets(user_context)]
    return [t for t in texts if t]


def judge_input(scenario: str, turns: list[SummaryTurn], index: int) -> str:
    """What the judge reads as INPUT for turn `index`.

    - summary turn: the scenario line and its question
    - follow-up: also the conversation before it, in full, so a criterion can compare the
      answer with what the assistant said earlier
    """
    lines = [scenario]
    if index:
        lines.append("Conversation before this turn:")
        for turn in turns[:index]:
            lines.append(f"USER: {turn.question}")
            lines.append(f"ASSISTANT: {render_answer_text(turn.result) if turn.result else ''}")
    lines.append(f"Question of this turn: {turns[index].question}")
    return "\n".join(lines)


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
    tables: list[Table] = []
    for index, turn in enumerate(run.turns):
        expected = expected_outputs[index] if index < len(expected_outputs) else {}
        # a follow-up answers from every table read so far in the conversation
        tables = tables + tables_from_tool_calls(turn.result.tool_call_events if turn.result else [])
        run.evaluations.append(
            evaluate_turn(
                judge_input=judge_input(scenario, run.turns, index),
                answer=render_answer_text(turn.result) if turn.result else "",
                tool_names=_tool_names(turn.result),
                expected=expected,
                scope=run.scope if index == 0 else None,
                positive_judge=positive,
                violation_judge=violation,
                tables=tables,
                filter_years=run.filter_years,
                known_text=run.known_text,
            )
        )
    run.judge_s = time.monotonic() - started
    return run_passed(run)


def run_passed(run: SummaryConversation) -> bool:
    """Every turn answered and every turn's checks passed."""
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
    return agentic_detail(events, steps, **detail)


def _run_latency(run: SummaryConversation) -> float:
    return sum(t.agent_s for t in run.turns) + run.judge_s


def _last_result(run: SummaryConversation) -> ChatResult | None:
    return next((t.result for t in reversed(run.turns) if t.result), None)


class ChatSummaryAssertionError(AgenticAssertionError):
    """Raised when an agentic chat-summary evaluation fails."""


def _setup_error(scenario: str, exc: SetupError) -> ChatSummaryAssertionError:
    """An ERROR item: its executions failed or its data changed, so no chat ran and nothing was graded."""
    reason = "\n".join(exc.problems)
    error = ChatSummaryAssertionError(f"Chat summary not run for '{scenario}': {exc.headline}.\n{reason}")
    error.reasoning_steps = []
    error.conversation_id = ""
    error.response_id = None
    key = "data_baseline" if isinstance(exc, DataBaselineError) else "widgets_executed"
    error.detail = {key: False, f"{key}_reason": reason}
    error.timings = PhaseTimings()
    error.runs_passed = 0
    error.runs_effective = 0
    error.failed_runs = []
    error.run_latencies_s = []
    error.harness_error = setup_error(exc.reason).as_record()
    return error


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
    dataset_name: str = "chat_summary",
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
    validate_expected(expected_output, "item")
    for n, follow_up in enumerate(summary_input.follow_ups, start=1):
        validate_expected(follow_up.expected_output, f"follow-up {n}")
    langfuse, window_start = open_trace_window(langfuse)
    try:
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
    except SetupError as exc:
        raise _setup_error(scenario, exc) from exc
    expected_outputs = [expected_output] + [
        f.expected_output if isinstance(f.expected_output, dict) else {} for f in summary_input.follow_ups
    ]
    for run in runs:
        grade_conversation(run, scenario=scenario, expected_outputs=expected_outputs, judge_model=judge_model)

    scored = [r for r in runs if r.chat_error is None and r.judge_error is None]
    pass_at_k = any(run_passed(r) for r in scored)
    pass_power_k = bool(runs) and all(run_passed(r) for r in runs)
    # Before the Langfuse scores, so a run the judge could not grade gets its ERROR marker there.
    run_labels = label_runs(runs, passed=run_passed)

    if langfuse is not None and dataset_item_id:
        window_end = utc_now()

        def _write_scores(ctx: RunTraceContext) -> None:
            stamp_gate_metadata(ctx.run_metadata, k=len(runs), gate=gate)
            for run_idx, run in enumerate(runs):
                if run.chat_error is not None or run.judge_error is not None:
                    # No verdict: a 0.0 would publish a failure nobody graded.
                    mark_unscored_run(ctx, run_idx, run.conversation_id, run_labels.error_label(run_idx))
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
            conversation_ids=conversations_to_link(
                [r.conversation_id for r in scored],
                [r.conversation_id for r in runs if r not in scored],
            ),
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
    failed_runs = build_failed_runs(runs, labels=run_labels, detail=_run_detail)
    reasoning = list(best_result.reasoning_steps or []) if best_result else []
    run_latencies_s = [_run_latency(r) for r in runs]
    best_latency = run_latency_s(PhaseTimings(agent_s=sum(t.agent_s for t in best.turns), judge_s=best.judge_s))
    detail = _run_detail(best)
    unscored = [r.judge_error for r in runs if r.judge_error is not None]
    if unscored:
        detail["unscored_runs"] = len(unscored)
        detail["judge_errors"] = unscored

    if unscored and not scored:
        # No run got a verdict: the item is a harness error, not K failures.
        error = JudgeResponseError(
            f"judge returned no readable verdict for any of the {len(unscored)} graded run(s): " + " | ".join(unscored)
        )
        error.reasoning_steps = reasoning
        error.conversation_id = best.conversation_id
        error.response_id = best_result.response_id if best_result else None
        error.detail = detail
        error.runs_passed = runs_passed
        error.runs_effective = len(runs)
        error.failed_runs = failed_runs
        error.run_latencies_s = run_latencies_s
        error.best_run_latency_s = best_latency
        error.timings = timings
        attach_labels(error, run_labels, gate)
        raise error

    if not gate_passed(gate, pass_at_k=pass_at_k, pass_power_k=pass_power_k):
        failing = next((e for e in best.evaluations if not e.passed), None)
        reason = best.chat_error or (failing.error if failing and failing.error else "criteria not satisfied")
        head = failure_message_head(gate, run_labels, runs_passed, failed_runs, len(unscored))
        raise_agentic_failure(
            ChatSummaryAssertionError,
            f"Chat summary failed for '{scenario}'. {head} "
            f"({best.widgets_executed}/{best.widgets_total} widgets executed): {reason}",
            harness_error=run_labels.harness_error_record,
            shadow=run_labels.shadow(gate),
            reasoning_steps=reasoning,
            conversation_id=best.conversation_id,
            response_id=best_result.response_id if best_result else None,
            detail=detail,
            runs_passed=runs_passed,
            runs_effective=len(runs),
            failed_runs=failed_runs,
            run_latencies_s=run_latencies_s,
            best_run_latency_s=best_latency,
            timings=timings,
        )
    return agentic_success(
        shadow=run_labels.shadow(gate),
        reasoning_steps=reasoning,
        conversation_id=best.conversation_id,
        response_id=best_result.response_id if best_result else None,
        detail=detail,
        runs_passed=runs_passed,
        runs_effective=len(runs),
        failed_runs=failed_runs,
        run_latencies_s=run_latencies_s,
        best_run_latency_s=best_latency,
        timings=timings,
    )

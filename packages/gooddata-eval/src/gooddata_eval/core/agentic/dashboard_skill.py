# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic dashboard-skill evaluation runner."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

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
from gooddata_eval.core.chat.sse_client import ChatClient
from gooddata_eval.core.config import ReasoningEffort
from gooddata_eval.core.models import (
    AgenticAssertionError,
    AgenticEvalOutcome,
    ChatResult,
    ReasoningStepEvent,
    ToolCallEvent,
    build_latency_breakdown,
    shift_and_index_events,
)
from gooddata_eval.core.timing import PhaseTimings, log_timer, sum_timings

_DEFAULT_K = 1
# Matches kda_skill and visualization. The reply this loop sends is built from the expectation
# and is byte-identical every turn, so the extra rounds are not there to say anything new --
# they are slack for a turn that produced nothing. A turn can come back empty or answer without
# drafting for reasons that are not the model's, and with a tight cap that one wasted turn
# spends the only reply the case had; the run then fails as "no draft" when nothing was wrong
# with the agent. Fewer than metric_skill's seven because those rounds do carry new content:
# its reply is generated per turn by an LLM.
#
# The cost of the slack is that four turns at ChatClient's 300s read timeout exceed the 720s
# per-test timeout gdc-nas derives for a k=1 dataset, so a run that stalls on every turn is cut
# short by pytest rather than by this loop. Measured turns are nowhere near that -- a two-turn
# case completes in about four minutes -- so the ceiling only binds when something is already
# badly wrong.
_DEFAULT_MAX_ITERATIONS = 4

_DRAFT_TOOL = "draft_dashboard"
_SET_SKILLS_TOOL = "set_skills"
_BUILDER_SKILL = "dashboard_builder"


def _norm(text: str) -> str:
    """Case- and whitespace-insensitive form used for every title comparison."""
    return " ".join(text.split()).casefold()


def _extract_draft_result(tool_call_events: list[ToolCallEvent]) -> dict | None:
    """Result payload of the ``draft_dashboard`` call that produced a draft.

    Takes the most recent *successful* call: when the agent retries after a rejected
    draft, the earlier failed attempt must not shadow the one that worked.
    """
    for tc in reversed(tool_call_events):
        if tc.function_name != _DRAFT_TOOL or not tc.result:
            continue
        result_data = tc.parsed_result()
        if not isinstance(result_data, dict):
            continue
        payload = result_data.get("data", result_data)
        if not isinstance(payload, dict) or payload.get("status") != "success":
            continue
        return payload
    return None


def _builder_skill_activated(tool_call_events: list[ToolCallEvent]) -> bool:
    """Whether any ``set_skills`` result activated the dashboard-builder skill.

    Diagnostic only, deliberately outside ``strict_pass``: a mis-route already fails on the
    missing draft, and gating on this would turn any future route that skips ``set_skills``
    into a false failure. Reported so such a failure reads as a mis-route rather than as a
    model that simply did not draft.
    """
    for tc in tool_call_events:
        if tc.function_name != _SET_SKILLS_TOOL or not tc.result:
            continue
        result_data = tc.parsed_result()
        if not isinstance(result_data, dict):
            continue
        payload = result_data.get("data", result_data)
        skills = payload.get("skills_to_activate") if isinstance(payload, dict) else None
        if isinstance(skills, list) and _BUILDER_SKILL in skills:
            return True
    return False


def _expected_type(expected_output: dict) -> str:
    """The response part the expectation names. One source, so message and lookup agree."""
    return str(expected_output.get("type") or "dashboard")


def _extract_dashboard_part(chat_result: ChatResult, part_type: str) -> dict | None:
    """The response part of ``part_type``, e.g. ``dashboard``.

    That type is in the SSE client's known-part set but has no dedicated accumulator, so it
    arrives in ``unhandled_parts`` verbatim and is read back by type. Taken from the end for
    the same reason ``_extract_draft_result`` does: a turn that drafts and then refines must
    be read as the state it left behind, not the one it passed through.
    """
    for part in reversed(chat_result.unhandled_parts):
        if isinstance(part, dict) and part.get("type") == part_type:
            return part
    return None


def _widgets_of(dashboard: dict) -> list[dict]:
    """Every widget of the draft, flattened across tabs and sections.

    Charts are matched dashboard-wide on purpose: the expectation names charts, not a layout,
    so which tab one lands on is the agent's call. The date filter is deliberately the
    opposite -- ``_check_date_range`` requires *every* tab to match. That is defensive rather
    than observed: ``draft_dashboard`` copies one filter onto every tab unconditionally, so a
    draft cannot currently disagree with itself across tabs, and the per-tab check is there to
    notice if that ever stops being true.

    Only ``tabs`` is read. That is sound for a draft, which ``draft_dashboard`` always builds
    tabbed, but an AAC v2 document carries its layout in root ``sections`` instead, so an
    editing dataset cannot reuse this as it stands.
    """
    return [
        widget
        for tab in dashboard.get("tabs") or []
        for section in tab.get("sections") or []
        for widget in section.get("widgets") or []
    ]


def _check_visualizations(widgets: list[dict], new_ids: set[str], expected: list[dict]) -> tuple[list[str], list[str]]:
    """Match every expected chart against the draft; extra charts the agent added are allowed.

    Returns ``(failures, title_notes)``.

    An entry with an ``id`` is an existing chart and is matched on that id alone: the id is
    the chart's identity, while the widget title is ``title_override or fallback_title`` and
    the override is the model's own choice, so requiring it adds flake without signal. A
    title that differs is still reported, as a note rather than a failure.

    ``id: null`` marks a chart the agent had to author, whose real id is generated at run
    time. It has no identity to match on, so the title *is* the match — taken among the
    authored charts only, without which an existing chart of the same title would satisfy it.
    """
    failures: list[str] = []
    title_notes: list[str] = []
    for exp in expected:
        exp_id = exp.get("id")
        exp_title = str(exp.get("title") or "")
        if exp_id is not None:
            matches = [w for w in widgets if w.get("visualization") == exp_id]
            if not matches:
                failures.append(f"missing existing chart id={exp_id!r} title={exp_title!r}")
            elif not any(_norm(str(w.get("title") or "")) == _norm(exp_title) for w in matches):
                # Every title the id appears under: the same chart can be placed twice, and
                # naming only the first would hide the rest.
                titles = ", ".join(repr(w.get("title")) for w in matches)
                title_notes.append(f"chart {exp_id!r} is titled {titles}, expected {exp_title!r}")
        elif not any(
            w.get("visualization") in new_ids and _norm(str(w.get("title") or "")) == _norm(exp_title) for w in widgets
        ):
            failures.append(
                f"missing authored chart title={exp_title!r}"
                + ("" if new_ids else " (the response listed no authored charts)")
            )
    return failures, title_notes


def _check_references(widgets: list[dict], known_ids: set[str]) -> list[str]:
    """Report widgets whose id the response's references never carried.

    Diagnostic, never a gate. gen-ai rejects a draft naming an unresolvable visualization
    before it can succeed (``reject_unverified``), so this cannot catch an invented id. What
    it does catch is reference building having degraded to an empty list on the way out --
    a platform fault, which must not be scored as the agent's.
    """
    notes: list[str] = []
    for widget in widgets:
        viz_id = widget.get("visualization")
        if viz_id is not None and viz_id not in known_ids:
            notes.append(f"the response's references do not carry {viz_id!r} (widget {widget.get('title')!r})")
    return notes


def _check_date_range(dashboard: dict, expected: dict | None) -> list[str]:
    """The date filter of every tab must match the expectation.

    A draft always carries a date filter, so ``expected is None`` (all time) means the tab
    filter has neither bound — absent keys, not null ones.
    """
    tabs = dashboard.get("tabs") or []
    if not tabs:
        return ["draft has no tabs to read a date filter from"]
    failures: list[str] = []
    for tab in tabs:
        tab_id = tab.get("id")
        date_filter = (tab.get("filters") or {}).get("date") or {}
        if expected is None:
            if "from" in date_filter or "to" in date_filter:
                failures.append(
                    f"tab {tab_id!r}: expected all time, got from={date_filter.get('from')!r} "
                    f"to={date_filter.get('to')!r}"
                )
            continue
        failures.extend(
            f"tab {tab_id!r}: date {key} expected {expected.get(key)!r}, got {date_filter.get(key)!r}"
            for key in ("granularity", "from", "to")
            if date_filter.get(key) != expected.get(key)
        )
    return failures


def _date_range_text(date_range: dict | None) -> str:
    """Render a date range the way a user would say it, for the simulated reply.

    Raises:
        ValueError: the range is a shape no case has needed yet. Deliberately loud — a
            silently mis-rendered range would be answered as a passing run on the wrong
            dashboard.
    """
    if date_range is None:
        return "all time"
    granularity = str(date_range.get("granularity", "")).lower()
    start, end = date_range.get("from"), date_range.get("to")
    if start == 0 and end == 0:
        return f"this {granularity}"
    if start == -1 and end == -1:
        return f"last {granularity}"
    raise ValueError(f"unsupported date_range for the simulated user: {date_range!r}")


def build_simulated_reply(expected_output: dict) -> str:
    """Build the reply the simulated user sends when the agent asks back instead of drafting.

    Deterministic and LLM-free: the only things the agent still needs are the charts and the
    date range, and both are already in the expectation. A fixed reply also keeps a failure
    attributable to the agent rather than to a simulated user that phrased things differently
    each run.
    """
    visualizations = expected_output.get("visualizations") or []
    existing = [str(v.get("title", "")) for v in visualizations if v.get("id") is not None]
    authored = [str(v.get("title", "")) for v in visualizations if v.get("id") is None]

    segments: list[str] = []
    if existing:
        segments.append(", ".join(existing))
    segments.extend(f'a new chart titled "{title}"' for title in authored)

    return (
        f"Please use these charts: {', and '.join(segments)}. "
        f"Date range: {_date_range_text(expected_output.get('date_range'))}. "
        f"Anything else is up to you. Please create the dashboard now."
    )


def _min_new_visualizations(expected_output: dict) -> int:
    """Lower bound on the number of charts the agent must author.

    Read here and nowhere else, so the value the fixture check accepts and the value the
    score compares against cannot drift apart.

    Raises:
        ValueError: the bound is not a number, or is negative — a negative bound would make
            the comparison true for any count and switch the check off without saying so.
    """
    raw = expected_output.get("min_new_visualizations") or 0
    try:
        value = int(raw)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"min_new_visualizations is not a number: {raw!r}") from exc
    if value < 0:
        raise ValueError(f"min_new_visualizations must not be negative, got {value}")
    return value


def _validate_expectation(expected_output: dict) -> None:
    """Reject a fixture the run could not score meaningfully, before the first API call.

    An empty ``visualizations`` would make every chart check pass vacuously, and a date range
    the simulated user cannot phrase would otherwise surface only on the branch where the
    agent asks back — passing or crashing depending on what the model chose to do that run.

    Raises:
        ValueError: the expectation is unusable.
    """
    if not expected_output.get("visualizations"):
        raise ValueError("expected_output lists no visualizations; every chart check would pass vacuously")
    _date_range_text(expected_output.get("date_range"))
    _min_new_visualizations(expected_output)


@dataclass
class DashboardEvaluation:
    """Per-run outcome of the dashboard-skill checks.

    ``strict_checks`` is what the run is scored on, and every entry in it is something the
    agent decided. ``skill_activated`` and ``references_carried`` are reported beside it but
    never gate: the first can be false on a route that pins skills instead of calling
    ``set_skills``, and the second reflects gen-ai's reference building rather than the
    agent's choices. ``notes`` carries the same kind of observation for titles.
    """

    drafted: bool
    part_present: bool
    charts_matched: bool
    date_range_correct: bool
    new_visualizations_met: bool
    skill_activated: bool = False
    references_carried: bool = True
    titles_matched: bool = True
    failures: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def strict_pass(self) -> bool:
        return all(self.strict_checks.values())

    @property
    def strict_checks(self) -> dict[str, bool]:
        return {
            "dashboard_drafted": self.drafted,
            "dashboard_part_present": self.part_present,
            "charts_matched": self.charts_matched,
            "date_range_correct": self.date_range_correct,
            "new_visualizations_met": self.new_visualizations_met,
        }

    @property
    def diagnostics(self) -> dict[str, bool]:
        """Observed but not scored — see the class docstring.

        ``titles_matched`` is here rather than in the gate so the decision to stop failing on
        a model-chosen title stays reviewable: without a score, nothing would record how often
        it happens. The two chart-level observations are omitted when no dashboard part was
        read, because reporting them as true would claim references and titles were fine on a
        run that produced neither.
        """
        observed = {"dashboard_skill_activated": self.skill_activated}
        if self.part_present:
            observed["references_carried"] = self.references_carried
            observed["titles_matched"] = self.titles_matched
        return observed


@dataclass
class DashboardRunResult:
    """Outcome of one K-run conversation for dashboard creation."""

    conversation_id: str
    evaluation: DashboardEvaluation
    draft_result: dict | None = None
    dashboard_part: dict | None = None
    total_turns: int = 0
    total_steps: int = 0
    reasoning_steps: list[str] = field(default_factory=list)
    response_id: str | None = None
    tool_call_events: list[ToolCallEvent] = field(default_factory=list)
    reasoning_step_events: list[ReasoningStepEvent] = field(default_factory=list)
    timings: PhaseTimings = field(default_factory=PhaseTimings)


@dataclass
class AgenticDashboardSummary:
    """Aggregated outcome of K runs for dashboard creation."""

    run_results: list[DashboardRunResult]
    pass_at_k: bool
    pass_power_k: bool
    best: DashboardRunResult


def evaluate_dashboard_draft(
    draft_result: dict | None,
    dashboard_part: dict | None,
    expected_output: dict,
    skill_activated: bool,
) -> DashboardEvaluation:
    """Score one drafted dashboard against its expectation.

    Pure — no network, no conversation state — so the assertion logic is unit-testable
    without an agent.
    """
    if draft_result is None:
        return DashboardEvaluation(
            drafted=False,
            part_present=False,
            charts_matched=False,
            date_range_correct=False,
            new_visualizations_met=False,
            skill_activated=skill_activated,
            failures=["the agent never produced a successful draft_dashboard call"],
        )

    min_new = _min_new_visualizations(expected_output)
    actual_new = draft_result.get("new_visualization_count")
    if isinstance(actual_new, int):
        new_met = actual_new >= min_new
        # Naming the shortfall, never "expected at least 0" -- see the envelope branch below.
        new_failures = [] if new_met else [f"expected at least {min_new} authored chart(s), tool reported {actual_new}"]
    else:
        # Not a shortfall: the tool result no longer carries the key. Said plainly, because
        # "expected at least 0 authored chart(s), tool reported None" reads as a broken test
        # and would send whoever is on nightly duty looking at the model instead.
        new_met = False
        new_failures = [f"the draft result carries no new_visualization_count (got {actual_new!r})"]

    if dashboard_part is None:
        return DashboardEvaluation(
            drafted=True,
            part_present=False,
            charts_matched=False,
            date_range_correct=False,
            new_visualizations_met=new_met,
            skill_activated=skill_activated,
            failures=[
                f"the response carries no {_expected_type(expected_output)!r} part",
                *new_failures,
            ],
        )

    dashboard = dashboard_part.get("dashboard") or {}
    references = dashboard_part.get("references") or {}
    new_ids = {v.get("id") for v in references.get("new_visualizations") or [] if v.get("id")}
    known_ids = {v.get("id") for v in references.get("visualizations") or [] if v.get("id")} | new_ids
    widgets = _widgets_of(dashboard)

    chart_failures, title_notes = _check_visualizations(widgets, new_ids, expected_output.get("visualizations") or [])
    reference_notes = _check_references(widgets, known_ids)
    date_failures = _check_date_range(dashboard, expected_output.get("date_range"))

    return DashboardEvaluation(
        drafted=True,
        part_present=True,
        charts_matched=not chart_failures,
        date_range_correct=not date_failures,
        new_visualizations_met=new_met,
        skill_activated=skill_activated,
        references_carried=not reference_notes,
        titles_matched=not title_notes,
        failures=[*chart_failures, *date_failures, *new_failures],
        notes=[*title_notes, *reference_notes],
    )


def _execute_single_dashboard_run(
    client: ChatClient,
    conversation_id: str,
    question: str,
    expected_output: dict,
    max_iterations: int,
) -> DashboardRunResult:
    """Drive one conversation until the agent drafts a dashboard, then evaluate it.

    Nothing is cleaned up on the way out by design: gen-ai keeps the draft and any authored
    chart in conversation state and persists neither until a user saves from the UI.
    """
    expected_type = str(expected_output.get("type") or "dashboard")
    draft_result: dict | None = None
    dashboard_part: dict | None = None
    turns = 0
    steps = 0
    current_question = question
    reasoning_steps: list[str] = []
    response_id: str | None = None
    all_tool_call_events: list[ToolCallEvent] = []
    all_reasoning_step_events: list[ReasoningStepEvent] = []
    timings = PhaseTimings()
    turn_offset = 0.0
    tool_index_offset = 0
    reasoning_index_offset = 0

    for iteration in range(max_iterations):
        turns += 1
        agent_started = time.monotonic()
        chat_result = client.send_message(conversation_id, current_question)
        agent_elapsed = time.monotonic() - agent_started
        timings.agent_s += agent_elapsed
        reasoning_steps.extend(chat_result.reasoning_steps or [])
        response_id = chat_result.response_id or response_id
        turn_offset, tool_index_offset, reasoning_index_offset = shift_and_index_events(
            chat_result,
            turn_offset=turn_offset,
            tool_index_offset=tool_index_offset,
            reasoning_index_offset=reasoning_index_offset,
        )
        all_tool_call_events.extend(chat_result.tool_call_events or [])
        all_reasoning_step_events.extend(chat_result.reasoning_step_events or [])
        steps += chat_result.reasoning_step_count

        candidate = _extract_draft_result(chat_result.tool_call_events or [])
        if candidate is not None:
            log_timer(
                f"[timer] dashboard_skill {conversation_id} GoodData turn {turns} complete after "
                f"{agent_elapsed:.2f}s; draft received"
            )
            draft_result = candidate
            dashboard_part = _extract_dashboard_part(chat_result, expected_type)
            break

        response_text = (chat_result.text_response or "").strip() or render_answer_text(chat_result)
        if not response_text and not chat_result.tool_call_events:
            break
        if iteration >= max_iterations - 1:
            break
        log_timer(
            f"[timer] dashboard_skill {conversation_id} GoodData turn {turns} complete after "
            f"{agent_elapsed:.2f}s; answering with the expected charts and date range"
        )
        current_question = build_simulated_reply(expected_output)

    return DashboardRunResult(
        conversation_id=conversation_id,
        evaluation=evaluate_dashboard_draft(
            draft_result,
            dashboard_part,
            expected_output,
            _builder_skill_activated(all_tool_call_events),
        ),
        draft_result=draft_result,
        dashboard_part=dashboard_part,
        total_turns=turns,
        total_steps=steps,
        reasoning_steps=reasoning_steps,
        response_id=response_id,
        tool_call_events=all_tool_call_events,
        reasoning_step_events=all_reasoning_step_events,
        timings=timings,
    )


def run_agentic_dashboard_skill(
    host: str,
    token: str,
    workspace_id: str,
    question: str,
    expected_output: dict,
    k: int = _DEFAULT_K,
    max_iterations: int = _DEFAULT_MAX_ITERATIONS,
    initial_conversation_id: str | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    agent_id: str | None = None,
) -> AgenticDashboardSummary:
    """Run the dashboard-skill agentic evaluation K times and return a summary.

    Raises:
        ValueError: the fixture is unusable — see ``_validate_expectation``.
    """
    _validate_expectation(expected_output)
    run_results: list[DashboardRunResult] = []
    client = ChatClient(
        host=host, token=token, workspace_id=workspace_id, reasoning_effort=reasoning_effort, agent_id=agent_id
    )

    try:
        conv_id_0 = initial_conversation_id if initial_conversation_id is not None else client.create_conversation()
        try:
            run_results.append(
                _execute_single_dashboard_run(client, conv_id_0, question, expected_output, max_iterations)
            )
        finally:
            if initial_conversation_id is None:  # only delete conversations we created
                client.delete_conversation(conv_id_0)

        for _ in range(1, k):
            conv_id = client.create_conversation()
            try:
                run_results.append(
                    _execute_single_dashboard_run(client, conv_id, question, expected_output, max_iterations)
                )
            finally:
                client.delete_conversation(conv_id)
    finally:
        client.close()

    pass_at_k = any(r.evaluation.strict_pass for r in run_results)
    pass_power_k = all(r.evaluation.strict_pass for r in run_results)
    best = max(run_results, key=lambda r: sum(r.evaluation.strict_checks.values()))
    return AgenticDashboardSummary(
        run_results=run_results,
        pass_at_k=pass_at_k,
        pass_power_k=pass_power_k,
        best=best,
    )


class DashboardSkillAssertionError(AgenticAssertionError):
    """Raised when a dashboard-skill evaluation fails."""


def evaluate_agentic_dashboard_skill(
    host: str,
    token: str,
    workspace_id: str,
    question: str,
    expected_output: dict,
    k: int = _DEFAULT_K,
    max_iterations: int = _DEFAULT_MAX_ITERATIONS,
    initial_conversation_id: str | None = None,
    agent_id: str | None = None,
    langfuse: object | None = None,
    dataset_item_id: str = "",
    dataset_name: str = "dashboard_skill",
    run_timestamp: str | None = None,
    model_version_override: str | None = None,
    run_metadata_extra: dict | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    submit_trace_link: SubmitTraceLink = run_trace_link_inline,
    gate: EvalGate = DEFAULT_GATE,
) -> AgenticEvalOutcome:
    """Run dashboard-skill evaluation, log to Langfuse, and raise on failure.

    Returns the best run's outcome on success; on failure the same values are attached to
    the raised ``DashboardSkillAssertionError`` so callers can retrieve them either way.

    Raises:
        DashboardSkillAssertionError: the gate did not pass.
        ValueError: the fixture is unusable — see ``_validate_expectation``. Raised before
            any request, so it means a fixture to fix rather than a result to read.
    """
    langfuse, window_start = open_trace_window(langfuse)
    summary = run_agentic_dashboard_skill(
        host=host,
        token=token,
        workspace_id=workspace_id,
        question=question,
        expected_output=expected_output,
        k=k,
        max_iterations=max_iterations,
        initial_conversation_id=initial_conversation_id,
        reasoning_effort=reasoning_effort,
        agent_id=agent_id,
    )

    if langfuse is not None and dataset_item_id:
        # Pinned on the calling thread: a deferred poll must not widen its query window.
        window_end = utc_now()

        def _write_scores(ctx: RunTraceContext) -> None:
            stamp_gate_metadata(ctx.run_metadata, k=len(summary.run_results), gate=gate)

            for run_idx, run in enumerate(summary.run_results):
                pt = ctx.trace(run.conversation_id)
                strict_checks = run.evaluation.strict_checks
                with ctx.observe(pt, run_idx, conversation_id=run.conversation_id, output=strict_checks) as tid:
                    for score_name, value in strict_checks.items():
                        ctx.score(tid, name=score_name, value=float(value), data_type="BOOLEAN")
                    for name, value in run.evaluation.diagnostics.items():
                        ctx.score(tid, name=name, value=float(value), data_type="BOOLEAN")
                    ctx.score(tid, name="turns", value=run.total_turns, data_type="NUMERIC")
                    ctx.score(tid, name="steps", value=run.total_steps, data_type="NUMERIC")
                    log_gate_scores(ctx, tid, gate=gate, pass_at_k=summary.pass_at_k, pass_power_k=summary.pass_power_k)
                    ctx.quality(
                        tid,
                        strict_checks=strict_checks,
                        latency_sec=pt.latency if pt else None,
                        cost_usd=pt.total_cost if pt else None,
                    )

        # Before the pass@K raise: a failing item's scores are the ones worth having.
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
            conversation_ids=[r.conversation_id for r in summary.run_results],
            window_start=window_start,
            window_end=window_end,
            suffix_runs=len(summary.run_results) > 1,
            write_scores=_write_scores,
            item_input=question,
        )

    item_timings = sum_timings([r.timings for r in summary.run_results])
    runs_passed = sum(1 for r in summary.run_results if r.evaluation.strict_pass)
    runs_effective = len(summary.run_results)

    best = summary.best
    detail: dict[str, Any] = {
        **best.evaluation.strict_checks,
        **best.evaluation.diagnostics,
        "failures": best.evaluation.failures,
        "notes": best.evaluation.notes,
        "latency_breakdown": build_latency_breakdown(best.tool_call_events, best.reasoning_step_events),
    }

    if not gate_passed(gate, pass_at_k=summary.pass_at_k, pass_power_k=summary.pass_power_k):
        gate_note = gate_failure_note(gate, runs_passed, runs_effective)
        skill_note = (
            ""
            if best.evaluation.skill_activated or best.evaluation.drafted
            else " No set_skills call activated dashboard_builder, so check the feature flag before the model."
        )
        notes = "; ".join(best.evaluation.notes)
        exc = DashboardSkillAssertionError(
            f"Dashboard skill assertion failed. {gate_note}{skill_note} "
            f"Checks: {best.evaluation.strict_checks}. "
            f"Failures: {'; '.join(best.evaluation.failures) or 'none reported'}."
            + (f" Notes (not scored): {notes}." if notes else "")
        )
        exc.reasoning_steps = best.reasoning_steps
        exc.conversation_id = best.conversation_id
        exc.response_id = best.response_id
        exc.timings = item_timings
        exc.detail = detail
        exc.runs_passed = runs_passed
        exc.runs_effective = runs_effective
        raise exc
    return AgenticEvalOutcome(
        runs_passed=runs_passed,
        runs_effective=runs_effective,
        reasoning_steps=best.reasoning_steps,
        conversation_id=best.conversation_id,
        response_id=best.response_id,
        detail=detail,
        timings=item_timings,
    )

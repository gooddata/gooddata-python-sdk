# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic dashboard-skill evaluation runner."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

import jsonpatch

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
# they are slack for a turn that answered without drafting, which can happen for reasons that
# are not the model's. A turn that comes back with nothing at all does not consume the slack:
# the loop ends there rather than replying into silence. Fewer than metric_skill's seven
# because those rounds do carry new content, its reply being generated per turn by an LLM.
#
# Only creation ever reaches the later rounds. An edit stops after the first turn, since the
# creation reply names charts and a date range and answers nothing a rename or a resize could
# have asked.
#
# The cost of the slack is that four turns at ChatClient's 300s read timeout exceed the 720s
# per-test timeout gdc-nas derives for a k=1 dataset, so a run that stalls on every turn is cut
# short by pytest rather than by this loop. Measured turns are nowhere near that -- a two-turn
# case completes in about four minutes -- so the ceiling only binds when something is already
# badly wrong.
_DEFAULT_MAX_ITERATIONS = 4

_DRAFT_TOOL = "draft_dashboard"
_PATCH_TOOL = "patch_dashboard"
_SET_SKILLS_TOOL = "set_skills"
_BUILDER_SKILL = "dashboard_builder"
_EDITOR_SKILL = "dashboard_editor"
# The expectation's `type` is the only switch between creating and editing: it selects the
# response part to read, the tool that must have succeeded, and the skill that must have been
# activated. There is no "either one" case -- an edit fixture that routes to the builder is a
# failure, not an alternative route to the same answer.
_PATCH_TYPE = "dashboardPatch"


def _norm(text: str) -> str:
    """Case- and whitespace-insensitive form used for every title comparison."""
    return " ".join(text.split()).casefold()


def _extract_tool_result(tool_call_events: list[ToolCallEvent], tool_name: str) -> dict | None:
    """Result payload of the ``tool_name`` call that produced the response.

    Takes the most recent *successful* call: when the agent retries after a rejected
    draft, the earlier failed attempt must not shadow the one that worked.
    """
    for tc in reversed(tool_call_events):
        if tc.function_name != tool_name or not tc.result:
            continue
        result_data = tc.parsed_result()
        if not isinstance(result_data, dict):
            continue
        payload = result_data.get("data", result_data)
        if not isinstance(payload, dict) or payload.get("status") != "success":
            continue
        return payload
    return None


def _skill_activated(tool_call_events: list[ToolCallEvent], skill: str) -> bool:
    """Whether any ``set_skills`` result activated ``skill``.

    Gated, because the expectation's type names one skill and only one: a creation fixture
    answered by the editor, or an edit fixture answered by the builder, is a routing failure
    even when the dashboard that comes back looks plausible. It also names the failure -- a
    mis-route reads as a mis-route instead of as a model that simply produced nothing.

    The gate rests on the agent actually calling ``set_skills``. gen-ai skips that call when
    the agent has its skills pinned (``include_set_skills=not resolved_pinned_skills``), so an
    eval agent configured that way would fail every case here for a reason that is not the
    model's. The agent this suite drives is not pinned, which is what makes the gate safe
    today rather than in principle.
    """
    for tc in tool_call_events:
        if tc.function_name != _SET_SKILLS_TOOL or not tc.result:
            continue
        result_data = tc.parsed_result()
        if not isinstance(result_data, dict):
            continue
        payload = result_data.get("data", result_data)
        skills = payload.get("skills_to_activate") if isinstance(payload, dict) else None
        if isinstance(skills, list) and skill in skills:
            return True
    return False


def _is_edit(expected_output: dict) -> bool:
    """Whether the expectation describes an edit rather than a fresh dashboard."""
    return _expected_type(expected_output) == _PATCH_TYPE


def _required_skill(expected_output: dict) -> str:
    """The skill the run must have activated, decided by the expectation's type."""
    return _EDITOR_SKILL if _is_edit(expected_output) else _BUILDER_SKILL


def _producing_tool(expected_output: dict) -> str:
    """The tool whose successful call the response must come from."""
    return _PATCH_TOOL if _is_edit(expected_output) else _DRAFT_TOOL


def _expected_type(expected_output: dict) -> str:
    """The response part the expectation names. One source, so message and lookup agree."""
    return str(expected_output.get("type") or "dashboard")


def _extract_dashboard_part(chat_result: ChatResult, part_type: str) -> dict | None:
    """The response part of ``part_type``, e.g. ``dashboard``.

    That type is in the SSE client's known-part set but has no dedicated accumulator, so it
    arrives in ``unhandled_parts`` verbatim and is read back by type. Taken from the end for
    the same reason ``_extract_tool_result`` does: a turn that drafts and then refines must
    be read as the state it left behind, not the one it passed through.
    """
    for part in reversed(chat_result.unhandled_parts):
        if isinstance(part, dict) and part.get("type") == part_type:
            return part
    return None


def _sections_of(dashboard: dict) -> list[dict]:
    """The dashboard's sections, whichever shape the document uses.

    A freshly drafted dashboard is version 3 and nests its sections under ``tabs``. A saved
    dashboard relayed for editing can be version 2, which carries ``sections`` at the root and
    no ``tabs`` at all. ``version`` is not the discriminator -- the convertor computes it from
    the declarative input and separately flattens a single untitled tab into root sections, so
    a document can say ``version: "3"`` and still have no tabs. Read the presence of ``tabs``.
    """
    tabs = dashboard.get("tabs")
    if tabs:
        return [section for tab in tabs for section in tab.get("sections") or []]
    return dashboard.get("sections") or []


def _widgets_of(dashboard: dict) -> list[dict]:
    """Every widget of the dashboard, flattened across sections.

    Charts are matched dashboard-wide on purpose: the expectation names charts, not a layout,
    so which section or tab one lands on is the agent's call. The date filter is deliberately
    the opposite -- ``_check_date_range`` requires *every* tab to match. That one is defensive
    rather than observed: ``draft_dashboard`` copies a single filter onto every tab
    unconditionally, so a draft cannot currently disagree with itself across tabs, and the
    per-tab check is there to notice if that stops being true.
    """
    return [widget for section in _sections_of(dashboard) for widget in section.get("widgets") or []]


def _apply_patch(base: dict, operations: list[dict]) -> tuple[dict | None, str | None]:
    """Apply RFC 6902 ``operations`` to a copy of ``base``; return ``(result, failure)``.

    The agent emits ``test`` guards ahead of its real operations, pinning the widget it is
    about to touch. Those are applied rather than skipped: a failing guard means the patch was
    written against a document that is not the one it shipped, which is a failure of the edit
    even though every later operation might apply cleanly. Scoring the base instead of the
    result would pass a case whose change never happened.
    """
    try:
        # in_place=False is what makes the copy -- JsonPatch.apply deepcopies for us, so
        # copying here as well would leave a second one behind for no reason.
        return jsonpatch.JsonPatch(operations).apply(base, in_place=False), None
    except Exception as exc:  # jsonpatch raises several unrelated types for a bad patch
        return None, f"the patch does not apply to the dashboard it shipped with: {exc}"


def _check_visualizations(widgets: list[dict], new_ids: set[str], expected: list[dict]) -> tuple[list[str], list[str]]:
    """Match every expected chart against the dashboard; extra widgets are allowed.

    Returns ``(failures, title_notes)``.

    An entry with an ``id`` is matched on that id. ``id: null`` marks a chart the agent had to
    author, whose real id is generated at run time, so there the title *is* the match -- taken
    among the authored charts only, since matching against every chart would let an existing
    one of the same title satisfy it.

    Title mismatches come back separately from the failures rather than mixed into them, so
    the caller can gate on them or merely record them without the two decisions drifting: on
    creation the title is ``title_override or fallback_title`` and the override is the model's
    own choice, while on an edit the expectation states the title the change must leave behind
    and a rename case that does not gate on it asserts nothing at all. Either way the
    mismatches are returned, which is what keeps the reported score honest.

    ``columns`` is checked whenever the expectation carries it. A newly placed widget defaults
    to half width, so a resize case is only meaningful against the number.
    """
    failures: list[str] = []
    title_mismatches: list[str] = []
    for exp in expected:
        exp_id = exp.get("id")
        exp_title = str(exp.get("title") or "")
        exp_columns = exp.get("columns")

        if exp_id is not None:
            matches = [w for w in widgets if w.get("visualization") == exp_id]
            if not matches:
                failures.append(f"missing existing chart id={exp_id!r} title={exp_title!r}")
                continue
            titled = [w for w in matches if _norm(str(w.get("title") or "")) == _norm(exp_title)]
            if not titled:
                # Every title the id appears under: the same chart can be placed twice, and
                # naming only the first would hide the rest.
                titles = ", ".join(repr(w.get("title")) for w in matches)
                title_mismatches.append(f"chart {exp_id!r} is titled {titles}, expected {exp_title!r}")
            candidates = titled or matches
        else:
            candidates = [
                w
                for w in widgets
                if w.get("visualization") in new_ids and _norm(str(w.get("title") or "")) == _norm(exp_title)
            ]
            if not candidates:
                failures.append(
                    f"missing authored chart title={exp_title!r}"
                    + ("" if new_ids else " (the response listed no authored charts)")
                )
                continue

        if exp_columns is not None and not any(w.get("columns") == exp_columns for w in candidates):
            widths = ", ".join(repr(w.get("columns")) for w in candidates)
            failures.append(f"chart {exp_title!r} is {widths} column(s) wide, expected {exp_columns}")
    return failures, title_mismatches


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


def _filter_entries(dashboard: dict) -> list[tuple[str, dict]]:
    """``(label, filter)`` for every filter the dashboard carries, whichever shape it uses.

    A drafted dashboard hangs one filter map off each tab, keyed by role (``date``). A saved
    dashboard relayed for editing carries a single map at the root, keyed by the filter's own
    local identifier, so the role has to be read from each entry's ``type`` instead. The label
    is only there to say *where* a failure was found.
    """
    tabs = dashboard.get("tabs")
    if tabs:
        return [
            (f"tab {tab.get('id')!r}", value)
            for tab in tabs
            for value in (tab.get("filters") or {}).values()
            if isinstance(value, dict)
        ]
    return [
        (f"filter {key!r}", value) for key, value in (dashboard.get("filters") or {}).items() if isinstance(value, dict)
    ]


def _filters_of_type(dashboard: dict, filter_type: str) -> list[tuple[str, dict]]:
    return [(label, f) for label, f in _filter_entries(dashboard) if f.get("type") == filter_type]


def _check_date_range(dashboard: dict, expected: dict | None) -> list[str]:
    """Every date filter on the dashboard must match the expectation.

    Every one, not the first. That is defensive rather than observed: the draft tool copies a
    single filter onto every tab unconditionally, so a dashboard cannot currently disagree with
    itself, and checking them all is there to notice if that stops being true.

    ``expected is None`` means all time, which the document spells as a date filter with
    neither bound — absent keys, not null ones.
    """
    date_filters = _filters_of_type(dashboard, "date_filter")
    if not date_filters:
        return ["the dashboard carries no date filter to check the expected range against"]
    failures: list[str] = []
    for label, date_filter in date_filters:
        if expected is None:
            if "from" in date_filter or "to" in date_filter:
                failures.append(
                    f"{label}: expected all time, got from={date_filter.get('from')!r} to={date_filter.get('to')!r}"
                )
            continue
        failures.extend(
            f"{label}: date {key} expected {expected.get(key)!r}, got {date_filter.get(key)!r}"
            for key in ("granularity", "from", "to")
            if date_filter.get(key) != expected.get(key)
        )
    return failures


def _selection_of(attribute_filter: dict) -> tuple[str, list] | None:
    """The elements an attribute filter restricts to, or ``None`` when it restricts nothing.

    An unrestricted filter is spelled as the absence of a selection, and an empty list means
    the same thing, so both read as "all".
    """
    state = attribute_filter.get("state") or {}
    for kind in ("include", "exclude"):
        values = state.get(kind)
        if values:
            return kind, list(values)
    return None


def _describe_selection(selection: tuple[str, list] | None) -> str:
    return "all" if selection is None else f"{selection[0]} {selection[1]!r}"


def _check_filters(dashboard: dict, expected: list[dict]) -> list[str]:
    """Every expected attribute filter must be on the dashboard, with the stated selection.

    This exists because an edit can silently drop or widen the filters the user already had:
    the change asked for was a rename, and the filters coming back untouched is part of what
    "untouched" means. Filters the dashboard carries beyond the expected ones are left alone,
    the same way extra widgets are.
    """
    actual: dict[str | None, list[dict]] = {}
    for _label, attribute_filter in _filters_of_type(dashboard, "attribute_filter"):
        actual.setdefault(attribute_filter.get("using"), []).append(attribute_filter)

    failures: list[str] = []
    for exp in expected:
        using = exp.get("using")
        matches = actual.get(using) or []
        if not matches:
            failures.append(f"the dashboard carries no attribute filter on {using!r}")
            continue
        wanted = _expected_selection(exp)
        if not any(_selection_of(f) == wanted for f in matches):
            found = ", ".join(_describe_selection(_selection_of(f)) for f in matches)
            failures.append(f"filter on {using!r} selects {found}, expected {_describe_selection(wanted)}")
    return failures


def _expected_selection(expected_filter: dict) -> tuple[str, list] | None:
    """Read a fixture's filter entry into the same shape ``_selection_of`` produces.

    Raises:
        ValueError: the entry states no selection the evaluator knows how to check.
            Deliberately loud -- a typo here would otherwise assert nothing and read green.
    """
    for kind in ("include", "exclude"):
        if kind in expected_filter:
            return kind, list(expected_filter[kind] or [])
    if expected_filter.get("selection") == "all":
        return None
    raise ValueError(
        f"filter expectation for {expected_filter.get('using')!r} needs 'selection': 'all', "
        f"'include' or 'exclude', got {expected_filter!r}"
    )


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


def _has_filters(expected_output: dict) -> bool:
    """Whether the expectation says anything about the attribute filters.

    Absent means the case does not look at them, exactly as for ``date_range``. Only the
    cases that are about preserving filters carry the key, so the others stay unaffected.
    """
    return "filters" in expected_output


def _has_date_range(expected_output: dict) -> bool:
    """Whether the expectation says anything about the date filter at all.

    Absence and ``null`` are different answers and must not be collapsed: ``null`` means the
    dashboard has to be on all time, while a missing key means the case does not look at the
    filter. Edit cases omit it because a dashboard the user has not opened carries no filter
    context, so ``patch_dashboard`` refuses filter changes outright.
    """
    return "date_range" in expected_output


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
    if _has_date_range(expected_output):
        date_range = expected_output.get("date_range")
        # Shape first, and on both kinds of case. Only a creation case goes on to check that
        # the reply can phrase the period -- an edit records whatever range the saved dashboard
        # carries, which `_check_date_range` compares by number rather than reading aloud, so
        # demanding a phrasable one there would cap what the preserved-filter cases can cover.
        # Without the shape check a string slips through to scoring and dies there instead,
        # after the run has already been spent.
        if date_range is not None and not isinstance(date_range, dict):
            raise ValueError(f"date_range must be an object or null, got {date_range!r}")
        if not _is_edit(expected_output):
            _date_range_text(date_range)

    filters = expected_output.get("filters")
    if filters is not None and not isinstance(filters, list):
        raise ValueError(f"filters must be a list of filter expectations, got {filters!r}")
    for entry in filters or []:
        if not isinstance(entry, dict):
            raise ValueError(f"a filter expectation must be an object, got {entry!r}")
        if not entry.get("using"):
            raise ValueError(f"a filter expectation needs the label it filters on, got {entry!r}")
        _expected_selection(entry)
    saved_id = expected_output.get("saved_dashboard_id")
    if _is_edit(expected_output):
        if not isinstance(saved_id, str) or not saved_id:
            raise ValueError(f"an edit expectation needs the edited dashboard's saved_dashboard_id, got {saved_id!r}")
    elif saved_id is not None:
        raise ValueError(f"a creation expectation must not name a saved_dashboard_id, got {saved_id!r}")
    _min_new_visualizations(expected_output)


@dataclass
class DashboardEvaluation:
    """Per-run outcome of the dashboard-skill checks.

    ``strict_checks`` is what the run is scored on. ``skill_activated`` is in it because the
    expectation's type names one skill and only one: a creation fixture answered by the editor,
    or an edit fixture answered by the builder, is a routing failure even if the dashboard that
    came back looks plausible.

    ``references_carried`` stays out of the gate: gen-ai rejects a response naming an
    unresolvable chart before it can succeed, so a widget missing from the references means
    reference building degraded on the way out -- a platform fault, not the model's.
    ``titles_matched`` is also out for creation, where the title is the model's own wording;
    on an edit the expectation states the title the change must leave behind, so there it is
    scored through ``charts_matched`` instead.
    """

    drafted: bool
    part_present: bool
    charts_matched: bool
    date_range_correct: bool
    new_visualizations_met: bool
    filters_correct: bool = True
    skill_activated: bool = False
    saved_dashboard_id_correct: bool = True
    patch_applies: bool = True
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
            # Kept as-is through the editing work: every Langfuse view, saved filter and
            # combo-report field list already refers to it, and a rename would break them for
            # a word. It means "the tool that had to succeed did", patch or draft.
            "dashboard_drafted": self.drafted,
            "dashboard_part_present": self.part_present,
            "dashboard_skill_activated": self.skill_activated,
            "saved_dashboard_id_correct": self.saved_dashboard_id_correct,
            "patch_applies": self.patch_applies,
            "charts_matched": self.charts_matched,
            "date_range_correct": self.date_range_correct,
            # Prefixed: alert_skill already publishes a `filters_correct` score, and the combo
            # report resolves a trace's skill by which score names it carries.
            "dashboard_filters_correct": self.filters_correct,
            "new_visualizations_met": self.new_visualizations_met,
        }

    @property
    def diagnostics(self) -> dict[str, bool]:
        """Observed but not scored — see the class docstring.

        ``titles_matched`` reports the titles on both kinds of case, but only creation leaves
        it out of the gate -- an edit scores the same mismatches through ``charts_matched``,
        because there the expectation states the title the change must leave behind. Keeping
        the score in both cases is what makes the creation decision reviewable later.

        Both chart-level observations are omitted whenever no document was scored -- no part
        read, or a patch that would not apply. Reporting them as true would claim references
        and titles were fine on a run that never produced anything to look at.
        """
        observed: dict[str, bool] = {}
        if self.part_present and self.patch_applies:
            observed["references_carried"] = self.references_carried
            observed["titles_matched"] = self.titles_matched
        return observed


@dataclass
class DashboardRunResult:
    """Outcome of one K-run conversation, creating or editing."""

    conversation_id: str
    evaluation: DashboardEvaluation
    tool_result: dict | None = None
    dashboard_part: dict | None = None
    patch_part: dict | None = None
    total_turns: int = 0
    total_steps: int = 0
    reasoning_steps: list[str] = field(default_factory=list)
    response_id: str | None = None
    tool_call_events: list[ToolCallEvent] = field(default_factory=list)
    reasoning_step_events: list[ReasoningStepEvent] = field(default_factory=list)
    timings: PhaseTimings = field(default_factory=PhaseTimings)


@dataclass
class AgenticDashboardSummary:
    """Aggregated outcome of K runs, creating or editing."""

    run_results: list[DashboardRunResult]
    pass_at_k: bool
    pass_power_k: bool
    best: DashboardRunResult


def evaluate_dashboard_response(
    tool_result: dict | None,
    dashboard_part: dict | None,
    expected_output: dict,
    skill_activated: bool,
    patch_part: dict | None = None,
) -> DashboardEvaluation:
    """Score one dashboard response against its expectation.

    Creation reads the drafted dashboard straight off the ``dashboard`` part. Editing reads
    two parts -- the saved dashboard as it stood, and the patch against it -- and scores the
    document that results from applying one to the other, never the base.

    Pure: no network, no conversation state, so the whole assertion surface is unit-testable
    without an agent.
    """
    is_edit = _is_edit(expected_output)
    tool = _producing_tool(expected_output)

    if tool_result is None:
        return DashboardEvaluation(
            drafted=False,
            part_present=False,
            charts_matched=False,
            date_range_correct=False,
            filters_correct=False,
            new_visualizations_met=False,
            skill_activated=skill_activated,
            saved_dashboard_id_correct=False,
            patch_applies=False,
            failures=[f"the agent never produced a successful {tool} call"],
        )

    min_new = _min_new_visualizations(expected_output)
    actual_new = tool_result.get("new_visualization_count")
    if isinstance(actual_new, int):
        new_met = actual_new >= min_new
        # Naming the shortfall, never "expected at least 0" -- see the envelope branch below.
        new_failures = [] if new_met else [f"expected at least {min_new} authored chart(s), tool reported {actual_new}"]
    else:
        # Not a shortfall: the tool result no longer carries the key. Said plainly, because
        # "expected at least 0 authored chart(s), tool reported None" reads as a broken test
        # and would send whoever is on nightly duty looking at the model instead.
        new_met = False
        new_failures = [f"the {tool} result carries no new_visualization_count (got {actual_new!r})"]

    missing_parts: list[str] = []
    if dashboard_part is None:
        missing_parts.append("dashboard")
    if is_edit and patch_part is None:
        missing_parts.append(_PATCH_TYPE)
    if missing_parts:
        return DashboardEvaluation(
            drafted=True,
            part_present=False,
            charts_matched=False,
            date_range_correct=False,
            filters_correct=False,
            new_visualizations_met=new_met,
            skill_activated=skill_activated,
            saved_dashboard_id_correct=False,
            patch_applies=False,
            failures=[
                f"the response carries no {' and no '.join(repr(p) for p in missing_parts)} part",
                *new_failures,
            ],
        )

    assert dashboard_part is not None  # noqa: S101  narrowed by missing_parts above
    base = dashboard_part.get("dashboard") or {}
    base_references = dashboard_part.get("references") or {}
    expected_saved_id = expected_output.get("saved_dashboard_id")
    actual_saved_id = dashboard_part.get("saved_dashboard_id")

    saved_failures: list[str] = []
    patch_failures: list[str] = []

    if is_edit:
        patch = (patch_part or {}).get("patch") or {}
        patch_references = patch.get("references") or {}
        # The patch names the dashboard it addresses; the part names the one it shipped with.
        # Both have to be the dashboard the fixture asked to edit, or the change landed
        # somewhere nobody looked.
        for label, value in (("the response", actual_saved_id), ("the patch", patch.get("dashboard_id"))):
            if value != expected_saved_id:
                saved_failures.append(f"{label} addresses dashboard {value!r}, expected {expected_saved_id!r}")
        document, patch_error = _apply_patch(base, patch.get("operations") or [])
        if patch_error is not None:
            patch_failures.append(patch_error)
            document = None
        new_ids = {v.get("id") for v in patch_references.get("new_visualizations") or [] if v.get("id")}
        known_ids = (
            {v.get("id") for v in base_references.get("visualizations") or [] if v.get("id")}
            | {v.get("id") for v in patch_references.get("visualizations") or [] if v.get("id")}
            | new_ids
        )
    else:
        if actual_saved_id is not None:
            saved_failures.append(f"a new draft must not be saved yet, but it reports id {actual_saved_id!r}")
        document = base
        new_ids = {v.get("id") for v in base_references.get("new_visualizations") or [] if v.get("id")}
        known_ids = {v.get("id") for v in base_references.get("visualizations") or [] if v.get("id")} | new_ids

    if document is None:
        return DashboardEvaluation(
            drafted=True,
            part_present=True,
            charts_matched=False,
            date_range_correct=False,
            filters_correct=False,
            new_visualizations_met=new_met,
            skill_activated=skill_activated,
            saved_dashboard_id_correct=not saved_failures,
            patch_applies=False,
            failures=[*patch_failures, *saved_failures, *new_failures],
        )

    widgets = _widgets_of(document)
    chart_failures, title_mismatches = _check_visualizations(
        widgets, new_ids, expected_output.get("visualizations") or []
    )
    # On an edit the title is part of what was asked for, so it fails the case; on creation it
    # is only recorded. Either way `titles_matched` reads the mismatches themselves, never the
    # list they were routed into -- a score that says "titles fine" beside a failed rename is
    # worse than no score at all.
    if is_edit:
        chart_failures = [*chart_failures, *title_mismatches]
        title_notes: list[str] = []
    else:
        title_notes = title_mismatches
    reference_notes = _check_references(widgets, known_ids)
    date_failures = (
        _check_date_range(document, expected_output.get("date_range")) if _has_date_range(expected_output) else []
    )
    filter_failures = (
        _check_filters(document, expected_output.get("filters") or []) if _has_filters(expected_output) else []
    )

    return DashboardEvaluation(
        drafted=True,
        part_present=True,
        charts_matched=not chart_failures,
        date_range_correct=not date_failures,
        filters_correct=not filter_failures,
        new_visualizations_met=new_met,
        skill_activated=skill_activated,
        saved_dashboard_id_correct=not saved_failures,
        patch_applies=True,
        references_carried=not reference_notes,
        titles_matched=not title_mismatches,
        failures=[*chart_failures, *saved_failures, *date_failures, *filter_failures, *new_failures],
        notes=[*title_notes, *reference_notes],
    )


def _execute_single_dashboard_run(
    client: ChatClient,
    conversation_id: str,
    question: str,
    expected_output: dict,
    max_iterations: int,
) -> DashboardRunResult:
    """Drive one conversation until the agent produces a dashboard, then evaluate it.

    Nothing is cleaned up on the way out by design: gen-ai keeps the draft and any authored
    chart in conversation state and persists neither until a user saves from the UI.
    """
    tool = _producing_tool(expected_output)
    is_edit = _is_edit(expected_output)
    tool_result: dict | None = None
    dashboard_part: dict | None = None
    patch_part: dict | None = None
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

        candidate = _extract_tool_result(chat_result.tool_call_events or [], tool)
        if candidate is not None:
            log_timer(
                f"[timer] dashboard_skill {conversation_id} GoodData turn {turns} complete after "
                f"{agent_elapsed:.2f}s; {tool} result received"
            )
            tool_result = candidate
            # An edit relays two parts: the dashboard as it stood, and the patch against it.
            # Both are read from the turn that produced the patch -- the base is what the patch
            # was written for, so pairing it with any other turn's would score a document the
            # agent never proposed.
            dashboard_part = _extract_dashboard_part(chat_result, "dashboard")
            if is_edit:
                patch_part = _extract_dashboard_part(chat_result, _PATCH_TYPE)
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
        if is_edit:
            # The creation reply names charts and a date range, which answers nothing a rename
            # or a resize could have asked. Rather than send something the question did not
            # ask for, stop: the failure is the signal that an edit case needs a reply of its
            # own, and inventing one here would hide which cases actually need it.
            break
        current_question = build_simulated_reply(expected_output)

    return DashboardRunResult(
        conversation_id=conversation_id,
        evaluation=evaluate_dashboard_response(
            tool_result,
            dashboard_part,
            expected_output,
            _skill_activated(all_tool_call_events, _required_skill(expected_output)),
            patch_part=patch_part,
        ),
        tool_result=tool_result,
        dashboard_part=dashboard_part,
        patch_part=patch_part,
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
        # Two failures wear the same missing skill, and the advice differs. If the other
        # dashboard skill was activated, the flag that registers both is plainly on and the
        # model simply routed the wrong way. If neither was, the flag is off or the agent has
        # its skills pinned. Sending a reader after the flag in the first case walks them past
        # the real failure, which is why the run's own tool calls decide which line they get.
        required_skill = _required_skill(expected_output)
        other_skill = _BUILDER_SKILL if required_skill == _EDITOR_SKILL else _EDITOR_SKILL
        if best.evaluation.skill_activated:
            skill_note = ""
        elif _skill_activated(best.tool_call_events, other_skill):
            skill_note = f" It activated {other_skill} instead of {required_skill}: a routing failure, not the flag."
        else:
            skill_note = (
                f" No set_skills call activated {required_skill} or {other_skill};"
                " one feature flag registers both, so check that before the model."
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

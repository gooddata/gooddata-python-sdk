# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic dashboard-skill evaluation runner."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

import jsonpatch

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
    """Whether the run's skill routing landed on ``skill``.

    Gated, because the expectation's type names one skill and only one: a creation fixture
    answered by the editor, or an edit fixture answered by the builder, is a routing failure
    even when the dashboard that comes back looks plausible. It also names the failure -- a
    mis-route reads as a mis-route instead of as a model that simply produced nothing.

    A run that never routed passes. Absence of a ``set_skills`` call is absence of evidence,
    not evidence of a mis-route, and there are two ways to reach it that say nothing about the
    model: gen-ai omits the call for an agent whose skills are pinned
    (``include_set_skills=not resolved_pinned_skills``), and a run continuing an existing
    conversation through ``initial_conversation_id`` can have routed in a turn this run never
    saw. Failing those would fail the case for the harness's configuration.
    """
    routed = False
    for tc in tool_call_events:
        if tc.function_name != _SET_SKILLS_TOOL or not tc.result:
            continue
        result_data = tc.parsed_result()
        if not isinstance(result_data, dict):
            continue
        payload = result_data.get("data", result_data)
        skills = payload.get("skills_to_activate") if isinstance(payload, dict) else None
        if not isinstance(skills, list):
            continue
        routed = True
        if skill in skills:
            return True
    return not routed


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

    A patch carrying no operations is that same failure in its purest form. ``jsonpatch``
    applies an empty list happily and hands back the document untouched, so the run would go on
    to score the saved dashboard and pass every case the saved dashboard already satisfied.
    """
    if not operations:
        return None, "the patch carries no operations, so it proposes the dashboard it started from"
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
    return [(label, value) for label, value, _group in _grouped_filter_entries(dashboard)]


def _grouped_filter_entries(dashboard: dict) -> list[tuple[str, dict, str | None]]:
    """``(label, filter, group title)`` for every filter, with a group's members read in its place.

    A ``filter_group`` holds its members in a nested map, so reading only the outer map would
    miss every filter the agent chose to group and report it missing. The group entry itself is
    not a filter and is not returned.
    """
    tabs = dashboard.get("tabs")
    maps = (
        [(f"tab {tab.get('id')!r}", tab.get("filters") or {}) for tab in tabs]
        if tabs
        else [("", dashboard.get("filters") or {})]
    )
    entries: list[tuple[str, dict, str | None]] = []
    for where, filters in maps:
        for key, value in filters.items():
            if not isinstance(value, dict):
                continue
            label = where or f"filter {key!r}"
            if value.get("type") != "filter_group":
                entries.append((label, value, None))
                continue
            group = str(value.get("title") or "")
            entries.extend(
                (label, member, group) for member in (value.get("filters") or {}).values() if isinstance(member, dict)
            )
    return entries


def _filters_of_type(dashboard: dict, filter_type: str) -> list[tuple[str, dict]]:
    return [(label, f) for label, f in _filter_entries(dashboard) if f.get("type") == filter_type]


def _date_filter_mismatch(label: str, date_filter: dict, expected: dict | None) -> list[str]:
    """Why ``date_filter`` is not the expected range, or nothing.

    ``expected is None`` means all time, which the document spells as a date filter with
    neither bound — absent keys, not null ones.
    """
    if expected is None:
        if "from" in date_filter or "to" in date_filter:
            return [f"{label}: expected all time, got from={date_filter.get('from')!r} to={date_filter.get('to')!r}"]
        return []
    return [
        f"{label}: date {key} expected {expected.get(key)!r}, got {date_filter.get(key)!r}"
        for key in ("granularity", "from", "to")
        if date_filter.get(key) != expected.get(key)
    ]


def _check_date_range(dashboard: dict, expected: dict | None, is_edit: bool) -> list[str]:
    """Check the dashboard's date range against the expectation.

    What counts as "the" date filter differs between a drafted and a saved dashboard, so the two
    are checked differently. The case says which one it is: a saved dashboard can carry tabs as
    well, so the document's shape cannot.

    A drafted dashboard carries one per tab, and the draft tool writes the same one onto every
    tab, so every tab must have it and every one must match. A tab left without a date filter is
    a failure: the expectation describes what the whole dashboard shows.

    A saved dashboard relayed for editing, tabbed or flat, can legitimately hold more than one
    date filter — a dashboard-wide one plus a dataset-scoped one. Requiring every entry to match
    would fail a dashboard for carrying a filter the fixture never described, so one matching
    entry satisfies the check and the rest are left to the notes. A case that cares which filter
    holds which range names them in ``date_filters``.
    """
    date_filters = _filters_of_type(dashboard, "date_filter")
    if not date_filters:
        return ["the dashboard carries no date filter to check the expected range against"]

    tabs = dashboard.get("tabs")
    if tabs and not is_edit:
        failures: list[str] = [
            f"tab {tab.get('id')!r} carries no date filter"
            for tab in tabs
            if not any(
                f.get("type") == "date_filter" for f in (tab.get("filters") or {}).values() if isinstance(f, dict)
            )
        ]
        for label, date_filter in date_filters:
            failures.extend(_date_filter_mismatch(label, date_filter, expected))
        return failures

    mismatches = [_date_filter_mismatch(label, date_filter, expected) for label, date_filter in date_filters]
    if any(not m for m in mismatches):
        return []
    return [reason for m in mismatches for reason in m]


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
    """Every expected filter must be on the dashboard, with the stated selection or condition.

    An entry is an attribute filter unless it names ``type`` as ``text_filter`` or
    ``metric_value_filter``. ``group`` requires the filter to sit in the ``filter_group`` of that
    title; without it, a grouped filter counts the same as one on its own.

    This exists because an edit can silently drop or widen the filters the user already had:
    the change asked for was a rename, and the filters coming back untouched is part of what
    "untouched" means. Filters the dashboard carries beyond the expected ones are left alone,
    the same way extra widgets are.
    """
    entries = _grouped_filter_entries(dashboard)
    failures: list[str] = []
    for exp in expected:
        filter_type = _expected_filter_type(exp)
        using = exp.get("using")
        candidates = [
            (f, group)
            for _label, f, group in entries
            if f.get("type") == filter_type and _same_object_ref(f.get("using"), using)
        ]
        noun = filter_type.replace("_", " ")
        if not candidates:
            failures.append(f"the dashboard carries no {noun} on {using!r}")
            continue
        if "group" in exp:
            grouped = [
                (f, group) for f, group in candidates if group is not None and _norm(group) == _norm(exp["group"])
            ]
            if not grouped:
                found = ", ".join(repr(group) for _f, group in candidates)
                failures.append(f"{noun} on {using!r} sits in group {found}, expected {exp['group']!r}")
                continue
            candidates = grouped
        matches = [f for f, _group in candidates]
        if filter_type != "attribute_filter":
            if not any(not _filter_value_mismatch(f, exp) for f in matches):
                failures.append(f"{noun} on {using!r}: {'; '.join(_filter_value_mismatch(matches[0], exp))}")
            continue
        if "display_as" in exp:
            # GDAI-2488: a value change on a filter shown through a secondary label moves `using`
            # to the primary label and keeps the secondary one as `display_as`. Losing it shows
            # the user ids where they had names, while `using` and the selection stay right.
            shown = [f for f in matches if _same_object_ref(f.get("display_as"), exp["display_as"])]
            if not shown:
                found = ", ".join(repr(f.get("display_as")) for f in matches)
                failures.append(f"filter on {using!r} is displayed as {found}, expected {exp['display_as']!r}")
                continue
            matches = shown
        wanted = _expected_selection(exp)
        if not any(_selection_of(f) == wanted for f in matches):
            found = ", ".join(_describe_selection(_selection_of(f)) for f in matches)
            failures.append(f"filter on {using!r} selects {found}, expected {_describe_selection(wanted)}")
    return failures


# The kinds a `filters` entry can name, and for each the keys compared beyond `using`. An entry
# without `type` is an attribute filter, which is every entry written before the others existed.
_FILTER_VALUE_KEYS: dict[str, tuple[str, ...]] = {
    "attribute_filter": (),
    "text_filter": ("condition", "value", "values", "case_sensitive"),
    "metric_value_filter": ("conditions", "dimensionality", "null_values_as_zero"),
}
# What an attribute filter entry is compared on beyond `using`: its display label and selection.
_ATTRIBUTE_FILTER_KEYS = ("display_as", "include", "exclude", "selection")


def _expected_filter_type(expected_filter: dict) -> str:
    return str(expected_filter.get("type") or "attribute_filter")


def _filter_value_mismatch(actual: dict, expected: dict) -> list[str]:
    """Why a text or metric value filter differs from the expectation, on the keys it states.

    ``values`` compares without order: the order of whole values for ``is``/``isNot`` carries no
    meaning. A key the expectation leaves out is not compared, so a case states what it guards.
    """
    mismatches: list[str] = []
    for key in _FILTER_VALUE_KEYS[_expected_filter_type(expected)]:
        if key not in expected:
            continue
        want, got = expected[key], actual.get(key)
        same = (
            _same_unordered_values(want, got)
            if key == "values" and isinstance(want, list) and isinstance(got, list)
            else got == want
        )
        if not same:
            mismatches.append(f"{key} expected {want!r}, got {got!r}")
    return mismatches


def _same_unordered_values(want: list, got: list) -> bool:
    """One-to-one match in any order, with each pair of the same type.

    Not sorted: AAC allows `null` among the values, and Python cannot order it with strings.
    Not stringified: `1` and `"1"` are different values.
    """
    remaining = list(got)
    for expected in want:
        index = next(
            (i for i, actual in enumerate(remaining) if type(actual) is type(expected) and actual == expected), None
        )
        if index is None:
            return False
        del remaining[index]
    return not remaining


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


def _matching_widgets(widgets: list[dict], new_ids: set[str], expected: dict) -> list[dict]:
    """The widgets an expected chart entry names: by ``id``, or by title among the authored charts.

    Every widget the id appears under counts, whatever its title -- the checks that use this
    look at what a chart is bound to, and a rename is ``charts_matched``'s business.
    """
    exp_id = expected.get("id")
    if exp_id is not None:
        return [w for w in widgets if w.get("visualization") == exp_id]
    title = _norm(str(expected.get("title") or ""))
    return [w for w in widgets if w.get("visualization") in new_ids and _norm(str(w.get("title") or "")) == title]


def _has_date_bindings(expected_output: dict) -> bool:
    """Whether any expected chart states the date dataset its widget must follow.

    Per chart, not per case: a chart that reaches no date dataset correctly ignores the date
    filter, so "every widget has a date" is not an expectation that holds in general.
    """
    return any(isinstance(v, dict) and "date_dataset" in v for v in expected_output.get("visualizations") or [])


def _check_date_bindings(widgets: list[dict], new_ids: set[str], expected: list[dict]) -> list[str]:
    """Every widget of a chart that states a ``date_dataset`` must be bound to exactly that one.

    ``null`` means the widget must carry no date at all: the chart reaches no date dataset, and
    a binding there would be one the dashboard cannot honour. The widget key is AAC's ``date``,
    the declarative ``dateDataSet`` (GDAI-2391, GDAI-2462).
    """
    failures: list[str] = []
    for exp in expected:
        if not isinstance(exp, dict) or "date_dataset" not in exp:
            continue
        wanted = exp["date_dataset"]
        label = exp.get("title") if exp.get("id") is None else exp.get("id")
        candidates = _matching_widgets(widgets, new_ids, exp)
        if not candidates:
            # Not left to charts_matched alone: a check that could not look must not read as passed.
            failures.append(f"cannot check the date binding of chart {label!r}: it is not on the dashboard")
            continue
        # Every placement: the expectation names the chart, so one right placement must not hide a wrong one.
        if not all(w.get("date") == wanted for w in candidates):
            found = ", ".join(repr(w.get("date")) for w in candidates)
            failures.append(f"chart {label!r} follows date {found}, expected {wanted!r}")
    return failures


def _tabs_of(dashboard: dict) -> list[dict]:
    """The dashboard's tabs, reading a document with root sections as its single tab."""
    tabs = dashboard.get("tabs")
    if tabs:
        return list(tabs)
    return [{"sections": dashboard.get("sections") or [], "filters": dashboard.get("filters") or {}}]


def _check_tabs(dashboard: dict, new_ids: set[str], expected: list[dict]) -> list[str]:
    """The dashboard must have exactly the expected tabs, in order (GDAI-2426).

    A tab entry may name a ``title``, compared like every other title, and ``visualizations``
    that must sit on that tab -- each an id, or ``{"title": ...}`` for an authored chart. An
    empty entry asserts only that the tab exists, which is how a case says "one tab, any name".
    """
    tabs = _tabs_of(dashboard)
    if len(tabs) != len(expected):
        titles = ", ".join(repr(t.get("title")) for t in tabs)
        return [f"the dashboard has {len(tabs)} tab(s) ({titles}), expected {len(expected)}"]
    failures: list[str] = []
    for index, (tab, exp) in enumerate(zip(tabs, expected)):
        if "title" in exp and _norm(str(tab.get("title") or "")) != _norm(str(exp["title"] or "")):
            failures.append(f"tab {index} is titled {tab.get('title')!r}, expected {exp['title']!r}")
        tab_widgets = [w for section in tab.get("sections") or [] for w in section.get("widgets") or []]
        for chart in exp.get("visualizations") or []:
            entry = {"id": chart} if isinstance(chart, str) else {"id": None, **chart}
            if not _matching_widgets(tab_widgets, new_ids, entry):
                failures.append(f"tab {index} ({tab.get('title')!r}) does not hold chart {chart!r}")
    return failures


# The keys a date filter is compared on. Absent on both sides is a match -- an all-time filter
# spells itself by leaving `from` and `to` out, and a dashboard-wide one by leaving `date` out.
_DATE_FILTER_KEYS = ("granularity", "from", "to", "date")


def _filter_mismatch(label: str, actual: dict, expected: dict) -> list[str]:
    """Why ``actual`` is not the ``expected`` filter, or nothing.

    A date filter is compared on its range and dataset, an attribute filter on its labels and
    selection, both with absence significant. Any other kind is compared on the keys the
    expectation names.
    """
    if actual.get("type") != expected.get("type"):
        return [f"{label} is a {actual.get('type')!r}, expected a {expected.get('type')!r}"]
    if expected.get("type") == "date_filter":
        keys: tuple[str, ...] = _DATE_FILTER_KEYS
    elif expected.get("type") == "attribute_filter":
        if _selection_of(actual) != _selection_of(expected):
            return [
                f"{label} selects {_describe_selection(_selection_of(actual))}, "
                f"expected {_describe_selection(_selection_of(expected))}"
            ]
        keys = ("using", "display_as")
    else:
        keys = tuple(k for k in expected if k != "type")
    return [
        f"{label}: {key} expected {expected.get(key)!r}, got {actual.get(key)!r}"
        for key in keys
        if not (
            _same_object_ref(actual.get(key), expected.get(key))
            if key in ("using", "display_as")
            else actual.get(key) == expected.get(key)
        )
    ]


def _same_object_ref(actual: object, expected: object) -> bool:
    """Whether two AAC refs name the same object, reading ``attribute/<id>`` as ``label/<id>``.

    The draft and patch tools accept either prefix on a filter's ``using``, and the model picks
    one per run. An attribute and its primary label share the id, so the two spell one filter;
    matching the prefix verbatim failed a correct run on the model's wording.
    """
    if actual == expected:
        return True
    if not (isinstance(actual, str) and isinstance(expected, str)):
        return False
    return _ref_without_attribute_prefix(actual) == _ref_without_attribute_prefix(expected)


def _ref_without_attribute_prefix(ref: str) -> str:
    return "label/" + ref.removeprefix("attribute/") if ref.startswith("attribute/") else ref


def _check_tab_filters(dashboard: dict, expected: dict[str, dict]) -> list[str]:
    """Each named tab must carry exactly the expected filters, by the filter's own id.

    Exact on purpose: GDAI-2540 is a filter that turns up on a tab it never belonged to, which a
    check of only the expected entries would pass. Keyed by the saved dashboard's local filter
    id rather than by label, so two filters on the same label stay distinguishable.
    """
    tabs = {tab.get("id"): tab for tab in dashboard.get("tabs") or []}
    failures: list[str] = []
    for tab_id, expected_filters in expected.items():
        tab = tabs.get(tab_id)
        if tab is None:
            failures.append(f"the dashboard has no tab {tab_id!r}")
            continue
        actual = {k: v for k, v in (tab.get("filters") or {}).items() if isinstance(v, dict)}
        failures.extend(
            f"tab {tab_id!r} carries filter {filter_id!r}, which it should not"
            for filter_id in sorted(actual.keys() - expected_filters.keys())
        )
        failures.extend(
            f"tab {tab_id!r} lost filter {filter_id!r}" for filter_id in sorted(expected_filters.keys() - actual.keys())
        )
        for filter_id in sorted(expected_filters.keys() & actual.keys()):
            failures.extend(
                _filter_mismatch(f"tab {tab_id!r} filter {filter_id!r}", actual[filter_id], expected_filters[filter_id])
            )
    return failures


def _filters_by_id(dashboard: dict) -> dict[str, list[tuple[str, dict]]]:
    """Every filter by its own id, with where it was found; one id can recur across tabs."""
    found: dict[str, list[tuple[str, dict]]] = {}
    for tab in dashboard.get("tabs") or [{"filters": dashboard.get("filters") or {}}]:
        where = f"tab {tab['id']!r} " if "id" in tab else ""
        for filter_id, value in (tab.get("filters") or {}).items():
            if isinstance(value, dict):
                found.setdefault(filter_id, []).append((f"{where}filter {filter_id!r}", value))
    return found


def _check_date_filters(dashboard: dict, expected: dict[str, dict | None]) -> list[str]:
    """Every named date filter must still be there, on the expected range (GDAI-2491).

    Named by id because a dashboard can carry more than one date filter and the case states
    which one holds which range. Filters the expectation does not name are left alone.

    ``date`` is the dataset the filter itself is pinned to, not a widget's date binding, and its
    absence is significant as in ``tab_filters``: an entry without it, or ``null`` for all time,
    is the main filter, which follows each widget's own date dataset. A range kept on another
    dataset, or a main filter pinned to one, is a changed filter.
    """
    found = _filters_by_id(dashboard)
    failures: list[str] = []
    for filter_id, wanted in expected.items():
        entries = found.get(filter_id)
        if not entries:
            failures.append(f"the dashboard lost date filter {filter_id!r}")
            continue
        for label, date_filter in entries:
            if date_filter.get("type") != "date_filter":
                failures.append(f"{label} is a {date_filter.get('type')!r}, expected a date filter")
                continue
            failures.extend(_date_filter_mismatch(label, date_filter, wanted))
            dataset = None if wanted is None else wanted.get("date")
            if date_filter.get("date") != dataset:
                failures.append(f"{label}: date dataset expected {dataset!r}, got {date_filter.get('date')!r}")
    return failures


def _check_preserved_widgets(widgets: list[dict], expected: list[dict]) -> list[str]:
    """A widget the change did not target must keep every key the expectation lists (GDAI-2541).

    Compared on the keys listed and nothing else, so a case states what it guards -- AAC writes
    a hidden title as ``title: false`` and drills as ``interactions``.
    """
    failures: list[str] = []
    for exp in expected:
        viz_id = exp.get("visualization")
        keys = [k for k in exp if k != "visualization"]
        candidates = [w for w in widgets if w.get("visualization") == viz_id]
        if not candidates:
            failures.append(f"the widget showing {viz_id!r} is gone")
            continue
        # Every placement keeps the keys: one intact copy must not hide one that lost its drill.
        mismatched = [w for w in candidates if not all(w.get(k) == exp[k] for k in keys)]
        if not mismatched:
            continue
        widget = mismatched[0]
        changed = ", ".join(f"{k} {widget.get(k)!r} (expected {exp[k]!r})" for k in keys if widget.get(k) != exp[k])
        failures.append(f"the widget showing {viz_id!r} changed: {changed}")
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
    # Only titled tabs are said: an untitled entry asserts a tab count, and asking for "one tab"
    # out loud would be the reply leading the agent rather than the question. Each tab names its
    # charts, since `_check_tabs` requires every chart on its own tab and the agent cannot guess.
    titles_by_id = {v.get("id"): str(v.get("title", "")) for v in visualizations if v.get("id") is not None}
    placements = []
    for tab in expected_output.get("tabs") or []:
        if not tab.get("title"):
            continue
        charts = [
            titles_by_id.get(c, c) if isinstance(c, str) else str(c.get("title", ""))
            for c in tab.get("visualizations") or []
        ]
        on_tab = f'the "{tab["title"]}" tab'
        quoted = " and ".join(f'"{c}"' for c in charts)
        placements.append(f"{quoted} on {on_tab}" if charts else on_tab)
    tabs = f"Use these tabs: {'; '.join(placements)}. " if placements else ""

    return (
        f"Please use these charts: {', and '.join(segments)}. "
        f"{tabs}"
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
        if "display_as" in entry and not (isinstance(entry["display_as"], str) and entry["display_as"]):
            raise ValueError(f"a filter's display_as must name a label, got {entry!r}")
        if "group" in entry and not (isinstance(entry["group"], str) and entry["group"]):
            raise ValueError(f"a filter's group must name the group's title, got {entry!r}")
        filter_type = _expected_filter_type(entry)
        if filter_type not in _FILTER_VALUE_KEYS:
            raise ValueError(f"a filter expectation's type must be one of {sorted(_FILTER_VALUE_KEYS)}, got {entry!r}")
        # A key outside the compared ones, a misspelling included, would assert nothing.
        compared = _ATTRIBUTE_FILTER_KEYS if filter_type == "attribute_filter" else _FILTER_VALUE_KEYS[filter_type]
        unknown = sorted(entry.keys() - {"type", "using", "group", *compared})
        if unknown:
            raise ValueError(f"a {filter_type.replace('_', ' ')} expectation cannot state {unknown}, got {entry!r}")
        if filter_type == "attribute_filter":
            _expected_selection(entry)
        elif filter_type == "text_filter":
            if not entry.get("condition") or ("value" in entry) == ("values" in entry):
                raise ValueError(f"a text filter expectation needs a condition and one of value/values, got {entry!r}")
            if "values" in entry and not isinstance(entry["values"], list):
                raise ValueError(f"a text filter's values must be a list, got {entry!r}")
            if "value" in entry and not isinstance(entry["value"], str):
                raise ValueError(f"a text filter's value must be a string, got {entry!r}")
        elif not (isinstance(entry.get("conditions"), list) and entry["conditions"]):
            raise ValueError(f"a metric value filter expectation needs its conditions, got {entry!r}")
    _validate_layout_expectations(expected_output)
    saved_id = expected_output.get("saved_dashboard_id")
    if _is_edit(expected_output):
        if not isinstance(saved_id, str) or not saved_id:
            raise ValueError(f"an edit expectation needs the edited dashboard's saved_dashboard_id, got {saved_id!r}")
    elif saved_id is not None:
        raise ValueError(f"a creation expectation must not name a saved_dashboard_id, got {saved_id!r}")
    _min_new_visualizations(expected_output)


def _validate_layout_expectations(expected_output: dict) -> None:
    """Shape checks for the opt-in keys on charts, tabs, per-tab filters and preserved widgets.

    Raises:
        ValueError: one of them is unusable. Loud for the same reason as the rest of the
            fixture checks: a typo would otherwise assert nothing and read green.
    """
    for chart in expected_output.get("visualizations") or []:
        if isinstance(chart, dict) and "date_dataset" in chart and not _is_dataset_or_null(chart["date_dataset"]):
            raise ValueError(f"date_dataset must name a date dataset or be null, got {chart!r}")

    if "tabs" in expected_output:
        tabs = expected_output["tabs"]
        if not isinstance(tabs, list) or not tabs or not all(isinstance(t, dict) for t in tabs):
            raise ValueError(f"tabs must be a non-empty list of tab objects, got {tabs!r}")
        for tab in tabs:
            charts = tab.get("visualizations") or []
            if not isinstance(charts, list) or not all(
                (isinstance(c, str) and c) or (isinstance(c, dict) and c.get("title")) for c in charts
            ):
                raise ValueError(f"a tab's visualizations must be chart ids or {{'title': ...}}, got {tab!r}")

    if "tab_filters" in expected_output:
        tab_filters = expected_output["tab_filters"]
        if not isinstance(tab_filters, dict) or not tab_filters:
            raise ValueError(f"tab_filters must map tab ids to their filters, got {tab_filters!r}")
        for tab_id, filters in tab_filters.items():
            if not isinstance(filters, dict) or not all(
                isinstance(f, dict) and f.get("type") for f in filters.values()
            ):
                raise ValueError(f"tab_filters[{tab_id!r}] must map filter ids to typed filters, got {filters!r}")
            for filter_id, entry in filters.items():
                if entry["type"] == "attribute_filter":
                    _validate_tab_attribute_filter(f"tab_filters[{tab_id!r}][{filter_id!r}]", entry)

    if "date_filters" in expected_output:
        date_filters = expected_output["date_filters"]
        if not isinstance(date_filters, dict) or not date_filters:
            raise ValueError(f"date_filters must map filter ids to a range or null, got {date_filters!r}")
        for filter_id, date_range in date_filters.items():
            if date_range is not None and not isinstance(date_range, dict):
                raise ValueError(f"date_filters[{filter_id!r}] must be an object or null, got {date_range!r}")
            if date_range == {}:
                # Not all time: every bound would be compared against an absent one, and a real
                # date filter always has a granularity, so the case could never pass.
                raise ValueError(
                    f"date_filters[{filter_id!r}] is empty; use null for all time or state granularity/from/to"
                )
            unknown = sorted((date_range or {}).keys() - set(_DATE_FILTER_KEYS))
            if unknown:
                raise ValueError(
                    f"date_filters[{filter_id!r}] states {unknown}, which is not one of {list(_DATE_FILTER_KEYS)}"
                )
            if date_range and "date" in date_range and not _is_dataset_or_null(date_range["date"]):
                raise ValueError(
                    f"date_filters[{filter_id!r}] date must name a date dataset or be null, got {date_range['date']!r}"
                )

    if "preserved_widgets" in expected_output:
        preserved = expected_output["preserved_widgets"]
        if not isinstance(preserved, list) or not preserved:
            raise ValueError(f"preserved_widgets must be a non-empty list, got {preserved!r}")
        for widget in preserved:
            if not isinstance(widget, dict) or not widget.get("visualization") or len(widget) < 2:
                raise ValueError(f"a preserved widget needs its visualization and a key to guard, got {widget!r}")


def _is_dataset_or_null(value: object) -> bool:
    return value is None or (isinstance(value, str) and bool(value))


def _validate_tab_attribute_filter(where: str, entry: dict) -> None:
    """An attribute filter in ``tab_filters`` uses the AAC shape: the selection sits under ``state``.

    The ``filters`` shorthand (``include``/``exclude``/``selection`` on the entry) does not apply
    here. Read as AAC, it would compare as "all" and pass a case that checks nothing.

    Raises:
        ValueError: the entry is not in the AAC shape.
    """
    shorthand = sorted({"include", "exclude", "selection"} & entry.keys())
    if shorthand:
        raise ValueError(f"{where} puts {shorthand} on the filter; tab_filters takes the AAC `state` object")
    state = entry.get("state")
    if state is None:
        return
    if not isinstance(state, dict):
        raise ValueError(f"{where} state must be an object, got {state!r}")
    for kind in ("include", "exclude"):
        if kind in state and not isinstance(state[kind], list):
            raise ValueError(f"{where} state.{kind} must be a list, got {state[kind]!r}")


@dataclass(frozen=True)
class _Applies:
    """Which of the conditional checks the case applies.

    They are published only when they do. A check that could not fail is not evidence, and
    publishing it as passed lifts `quality_score` -- the fraction of true booleans in the
    detail -- above what the run earned, which would make a creation case read better than the
    same case scored before editing existed.
    """

    patch: bool
    date: bool
    filters: bool
    date_bindings: bool = False
    tabs: bool = False
    tab_filters: bool = False
    date_filters: bool = False
    preserved_widgets: bool = False

    @classmethod
    def of(cls, expected_output: dict) -> _Applies:
        return cls(
            patch=_is_edit(expected_output),
            date=_has_date_range(expected_output),
            filters=_has_filters(expected_output),
            date_bindings=_has_date_bindings(expected_output),
            tabs="tabs" in expected_output,
            tab_filters="tab_filters" in expected_output,
            date_filters="date_filters" in expected_output,
            preserved_widgets="preserved_widgets" in expected_output,
        )


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
    applies: _Applies
    filters_correct: bool = True
    skill_activated: bool = False
    saved_dashboard_id_correct: bool = True
    patch_applies: bool = True
    references_carried: bool = True
    titles_matched: bool = True
    # False by default, unlike the older checks above: every early return then scores them as
    # failed without having to name them, and only the run that reached a document sets them.
    # They are published only where the case applies them, so a default never shows otherwise.
    date_bindings_correct: bool = False
    tabs_correct: bool = False
    tab_filters_correct: bool = False
    date_filters_correct: bool = False
    widgets_preserved: bool = False
    failures: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def strict_pass(self) -> bool:
        return all(self.strict_checks.values())

    @property
    def strict_checks(self) -> dict[str, bool]:
        checks = {
            # Kept as-is through the editing work: every Langfuse view, saved filter and
            # combo-report field list already refers to it, and a rename would break them for
            # a word. It means "the tool that had to succeed did", patch or draft.
            "dashboard_drafted": self.drafted,
            "dashboard_part_present": self.part_present,
            "dashboard_skill_activated": self.skill_activated,
            "saved_dashboard_id_correct": self.saved_dashboard_id_correct,
            "charts_matched": self.charts_matched,
            "new_visualizations_met": self.new_visualizations_met,
        }
        if self.applies.patch:
            checks["patch_applies"] = self.patch_applies
        if self.applies.date:
            checks["date_range_correct"] = self.date_range_correct
        if self.applies.filters:
            # Prefixed: alert_skill already publishes a `filters_correct` score, and the combo
            # report resolves a trace's skill by which score names it carries.
            checks["dashboard_filters_correct"] = self.filters_correct
        # All prefixed, for the same reason as the filters check: the combo report tells skills
        # apart by the score names a trace carries.
        if self.applies.date_bindings:
            checks["dashboard_date_bindings_correct"] = self.date_bindings_correct
        if self.applies.tabs:
            checks["dashboard_tabs_correct"] = self.tabs_correct
        if self.applies.tab_filters:
            checks["dashboard_tab_filters_correct"] = self.tab_filters_correct
        if self.applies.date_filters:
            checks["dashboard_date_filters_correct"] = self.date_filters_correct
        if self.applies.preserved_widgets:
            checks["dashboard_widgets_preserved"] = self.widgets_preserved
        return checks

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
    applies = _Applies.of(expected_output)
    tool = _producing_tool(expected_output)

    if tool_result is None:
        return DashboardEvaluation(
            drafted=False,
            part_present=False,
            charts_matched=False,
            date_range_correct=False,
            filters_correct=False,
            new_visualizations_met=False,
            applies=applies,
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
            applies=applies,
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
            applies=applies,
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
        _check_date_range(document, expected_output.get("date_range"), applies.patch)
        if _has_date_range(expected_output)
        else []
    )
    filter_failures = (
        _check_filters(document, expected_output.get("filters") or []) if _has_filters(expected_output) else []
    )
    binding_failures = (
        _check_date_bindings(widgets, new_ids, expected_output.get("visualizations") or [])
        if applies.date_bindings
        else []
    )
    tab_failures = _check_tabs(document, new_ids, expected_output["tabs"]) if applies.tabs else []
    tab_filter_failures = _check_tab_filters(document, expected_output["tab_filters"]) if applies.tab_filters else []
    date_filter_failures = (
        _check_date_filters(document, expected_output["date_filters"]) if applies.date_filters else []
    )
    preserved_failures = (
        _check_preserved_widgets(widgets, expected_output["preserved_widgets"]) if applies.preserved_widgets else []
    )

    return DashboardEvaluation(
        drafted=True,
        part_present=True,
        charts_matched=not chart_failures,
        date_range_correct=not date_failures,
        filters_correct=not filter_failures,
        new_visualizations_met=new_met,
        applies=applies,
        skill_activated=skill_activated,
        saved_dashboard_id_correct=not saved_failures,
        patch_applies=True,
        references_carried=not reference_notes,
        titles_matched=not title_mismatches,
        date_bindings_correct=not binding_failures,
        tabs_correct=not tab_failures,
        tab_filters_correct=not tab_filter_failures,
        date_filters_correct=not date_filter_failures,
        widgets_preserved=not preserved_failures,
        failures=[
            *chart_failures,
            *saved_failures,
            *date_failures,
            *filter_failures,
            *binding_failures,
            *tab_failures,
            *tab_filter_failures,
            *date_filter_failures,
            *preserved_failures,
            *new_failures,
        ],
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
            # A turn may carry several patches. They are alternatives rebased on the same base
            # rather than steps to compose, and the client resolves the last one as the proposal
            # that holds (gdc-ui's applyDashboardPatch; gdc-nas
            # dashboard_edit_assertion.verify_last_proposal_holds does the same). Taking the last
            # of each part type is therefore what the user would end up looking at, and the
            # earlier patches are alternatives that lost, not changes that went missing.
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


def _run_detail(run: DashboardRunResult) -> dict[str, Any]:
    """The diagnostic fields for ONE run, shared by the best run and every failing one.

    Extracted so a failing run is described by exactly the same keys as the winning run --
    for this kind that means the per-check breakdown and the failures it reported, which is
    the whole diagnosis.
    """
    return {
        **run.evaluation.strict_checks,
        **run.evaluation.diagnostics,
        "failures": run.evaluation.failures,
        "notes": run.evaluation.notes,
        "latency_breakdown": build_latency_breakdown(run.tool_call_events, run.reasoning_step_events),
    }


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
    user_context: dict | None = None,
) -> AgenticDashboardSummary:
    """Run the dashboard-skill agentic evaluation K times and return a summary.

    Raises:
        ValueError: the fixture is unusable — see ``_validate_expectation``.
    """
    _validate_expectation(expected_output)
    run_results: list[DashboardRunResult] = []
    client = ChatClient(
        host=host,
        token=token,
        workspace_id=workspace_id,
        reasoning_effort=reasoning_effort,
        agent_id=agent_id,
        user_context=user_context,
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
    user_context: dict | None = None,
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
        user_context=user_context,
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
    detail: dict[str, Any] = _run_detail(best)
    # Same predicate runs_passed is taken over, so an item's failed_runs and its counts
    # cannot disagree about which runs failed.
    failed_runs = build_failed_runs(
        summary.run_results,
        passed=lambda r: r.evaluation.strict_pass,
        detail=_run_detail,
    )

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
        exc.failed_runs = failed_runs
        raise exc
    return AgenticEvalOutcome(
        runs_passed=runs_passed,
        runs_effective=runs_effective,
        reasoning_steps=best.reasoning_steps,
        conversation_id=best.conversation_id,
        response_id=best.response_id,
        detail=detail,
        timings=item_timings,
        failed_runs=failed_runs,
    )

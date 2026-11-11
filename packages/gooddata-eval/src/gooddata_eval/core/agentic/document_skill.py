# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic document-skill evaluation runner."""

from __future__ import annotations

import copy
import re
import time
from collections.abc import Iterator
from dataclasses import dataclass, field, replace
from typing import Any

import httpx
from gooddata_sdk.catalog.workspace.aac import aac_document_to_declarative

from gooddata_eval.core.agentic._conversation_context import classify_reply
from gooddata_eval.core.agentic._editor_takeaways import editor_takeaway_input
from gooddata_eval.core.agentic._failed_runs import build_failed_runs
from gooddata_eval.core.agentic._filters import describe_selection, same_selection, selection_of
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
    conversations_to_link,
    open_item_trace,
    run_trace_link_inline,
    submit_trace_scoring,
    utc_now,
)
from gooddata_eval.core.agentic.dashboard_skill import _extract_tool_result, _skill_activated
from gooddata_eval.core.chat.render import render_answer_text
from gooddata_eval.core.chat.sse_client import ChatClient
from gooddata_eval.core.config import DocumentFormat, ReasoningEffort, normalize_document_format
from gooddata_eval.core.evaluators._llm_judge import JudgeResponseError, LLMJudge, score_run
from gooddata_eval.core.langfuse.item_scope import item_scope
from gooddata_eval.core.models import (
    AgenticAssertionError,
    AgenticEvalOutcome,
    ChatResult,
    ReasoningStepEvent,
    ToolCallEvent,
    build_latency_breakdown,
    shift_and_index_events,
)
from gooddata_eval.core.takeaway.http_client import TakeawayClient, is_transient
from gooddata_eval.core.timing import PhaseTimings, log_timer, sum_timings

_DEFAULT_K = 1
# Same slack as the dashboard skill: the simulated reply is fixed, so the extra rounds only
# absorb a turn that answered without drafting.
_DEFAULT_MAX_ITERATIONS = 4

_DRAFT_TOOL = "draft_document"
_BUILDER_SKILL = "document_builder"
_PART_TYPE = "document"
_SET_SKILLS_TOOL = "set_skills"
# The Report names gen-ai sent before Publisher's Document names. Any of them on the wire means
# some part of the chain was not switched over.
_LEGACY_PART_TYPE = "report"
_LEGACY_PART_KEYS = ("report", "report_ref", "base_report_id", "saved_report_id")
_LEGACY_DRAFT_TOOL = "draft_report"
_LEGACY_TOOLS = frozenset({_LEGACY_DRAFT_TOOL, "list_report_layouts"})
_LEGACY_SKILL = "report_builder"
# The copilot's own rule: a document opens with a cover and has at least one content page.
_COVER_PAGE = "cover"
_CONTENT_PAGE = "content"
_EXPECTATION_KEYS = frozenset(
    {
        "period",
        "visualizations",
        "narrative",
        "expects_clarification",
        "asked_first_required",
        "clarification_reply",
        "rework",
        "chart_periods",
    }
)
_REWORK_KEYS = frozenset({"base_document_id", "keeps_pages", "page_charts", "new_page_charts", "title", "filters"})
# A date filter's range keys, compared even when a rework item leaves them out: an all-time filter
# spells itself by leaving `from` and `to` out, so a drafted range must not pass it, and an offset
# means nothing without its granularity, so a range stated without one must not pass any granularity.
_DATE_FILTER_RANGE_KEYS = ("granularity", "from", "to")
# What a filter applies to, which a rework item must state: the label and selection of an attribute
# filter, and the date dataset of a date filter. A type not listed here is rejected, so a misspelt type
# does not read as a copilot regression and a filter of another kind is not compared on its type alone.
_REQUIRED_FILTER_KEYS = {"attribute_filter": ("using", "state"), "date_filter": ("date",)}
# A v2 draft arrives as AaC, where a relative period is `{granularity, from, to}` and an absolute one
# is `{from, to}`: the granularity is what tells them apart. These are the names the code converter
# writes; it reads `WEEK` too but writes it as `WEEK_US`, so a fixture stating `WEEK` could never match.
_AAC_PERIOD_GRANULARITIES = frozenset(
    {
        "SECOND",
        "MINUTE",
        "HOUR",
        "DAY",
        "WEEK_US",
        "MONTH",
        "QUARTER",
        "YEAR",
        "FISCAL_MONTH",
        "FISCAL_QUARTER",
        "FISCAL_YEAR",
    }
)
# Template tokens the document renders at export time ({documentName}, {periodStart}, ...).
_PLACEHOLDER_RE = re.compile(r"\{\w+\}")
_SUMMARY_SLOT = "summary"
_V2 = "2"
_V2_HEADING_WIDGETS = frozenset({"title", "heading"})
_V2_TAKEAWAY_WIDGET = "takeaway"
# The draft_document result field listing the pages whose takeaway the copilot left for the editor
# to write from the data.
_EDITOR_PAGES_KEY = "takeaway_editor_page_ids"

_NARRATIVE_EVALUATION_STEPS = [
    "The actual output is a document rendered as text: its title, period, and per page the heading, "
    "the chart ids it shows and the written summaries.",
    "Check that the summaries address what the INPUT asked the document to cover, as the EXPECTED OUTPUT describes.",
    "Check that each page's summary fits that page's heading and charts.",
    "Check that the summaries speak to the document's period and do not contradict each other.",
    "Fail the output if any summary is placeholder, unfinished or boilerplate text.",
]


def _extract_document_part(chat_result: ChatResult) -> dict | None:
    """The last ``document`` part of the turn, read back from ``unhandled_parts`` by type.

    The last one, because a turn that drafts and then refines leaves the refined version as
    the one the user sees.
    """
    for part in reversed(chat_result.unhandled_parts):
        if isinstance(part, dict) and part.get("type") == _PART_TYPE:
            return part
    return None


def legacy_wire_names(parts: list[dict], tool_call_events: list[ToolCallEvent]) -> list[str]:
    """Every Report name the run saw on the wire, in the order it saw them, each named once."""
    found: list[str] = []
    for tc in tool_call_events:
        if tc.function_name in _LEGACY_TOOLS:
            found.append(f"tool {tc.function_name!r}")
        elif tc.function_name == _SET_SKILLS_TOOL:
            # The arguments too: a refused call naming the old skill still shows the prompt names it.
            arguments = tc.parsed_arguments()
            requested = arguments.get("skill_names") if isinstance(arguments, dict) else None
            result_data = tc.parsed_result()
            payload = result_data.get("data", result_data) if isinstance(result_data, dict) else None
            activated = payload.get("skills_to_activate") if isinstance(payload, dict) else None
            if any(isinstance(skills, list) and _LEGACY_SKILL in skills for skills in (requested, activated)):
                found.append(f"skill {_LEGACY_SKILL!r}")
    for part in parts:
        if not isinstance(part, dict):
            continue
        if part.get("type") == _LEGACY_PART_TYPE:
            found.append(f"part type {_LEGACY_PART_TYPE!r}")
        if part.get("type") not in (_PART_TYPE, _LEGACY_PART_TYPE):
            continue
        found.extend(f"part key {key!r}" for key in _LEGACY_PART_KEYS if key in part)
        for key in (_PART_TYPE, _LEGACY_PART_TYPE):
            document = part.get(key)
            if isinstance(document, dict) and document.get("type") == _LEGACY_PART_TYPE:
                found.append(f"document type {_LEGACY_PART_TYPE!r}")
    return list(dict.fromkeys(found))


def _is_v2(document: dict) -> bool:
    return document.get("version") == _V2


def _pages(document: dict) -> list[Any]:
    """Every page in order, hidden ones included.

    v2 keeps them in ``content``, read from the top level when ``content`` is missing, either as
    ``pages`` or grouped into ``sections`` that read as one list; ``sections`` wins when both are there.
    """
    if not _is_v2(document):
        return document.get("pages") or []
    content = document.get("content")
    container = content if isinstance(content, dict) else document
    sections = container.get("sections")
    if isinstance(sections, list):
        return [page for section in sections if isinstance(section, dict) for page in section.get("pages") or []]
    return container.get("pages") or []


def _visible_pages(document: dict) -> list[Any]:
    """The pages a reader sees: a v2 page with ``visible: false`` is out of the viewer, exports and numbering."""
    return [page for page in _pages(document) if not (isinstance(page, dict) and page.get("visible") is False)]


def _nodes(node: Any) -> Iterator[dict]:
    """Every node of a page layout in document order.

    v1 nests through ``row`` and ``column`` lists as gen-ai does; v2 containers hold ``children``.
    """
    if not isinstance(node, dict):
        return
    yield node
    for key in ("row", "column", "children"):
        children = node.get(key)
        if isinstance(children, list):
            for child in children:
                yield from _nodes(child)


def _page_kind(page: dict) -> str:
    """A page's kind; gen-ai reads a page without one as a content page."""
    return str(page.get("kind") or _CONTENT_PAGE)


def _visualization_id(node: dict) -> str | None:
    """The node's visualization id: a string in v1 and as-code, ``{"identifier": ...}`` in the v2 API."""
    reference = node.get("visualization")
    if isinstance(reference, dict):
        reference = reference.get("identifier")
    return reference if isinstance(reference, str) else None


def _heading(node: dict) -> str | None:
    if node.get("type") in _V2_HEADING_WIDGETS:
        return _written(node.get("markdown"))
    return _written(node.get("heading"))


def _page_visualizations(page: Any) -> set[str]:
    """Every visualization id placed in one page's layout."""
    if not isinstance(page, dict):
        return set()
    return {
        visualization for node in _nodes(page.get("layout")) if (visualization := _visualization_id(node)) is not None
    }


def _visualizations_of(document: dict) -> set[str]:
    """Every visualization id placed anywhere in the layouts of the pages a reader sees."""
    return {
        visualization
        for page in _visible_pages(document)
        if isinstance(page, dict)
        for node in _nodes(page.get("layout"))
        if (visualization := _visualization_id(node)) is not None
    }


def _written(text: Any) -> str | None:
    """``text`` when it says something once template placeholders are removed, else ``None``."""
    if not isinstance(text, str):
        return None
    if not re.sub(r"[\W_]+", "", _PLACEHOLDER_RE.sub("", text)):
        return None
    return text.strip()


def _is_takeaway(node: dict) -> bool:
    return node.get("type") == _V2_TAKEAWAY_WIDGET


def _summary_slots(page: dict) -> list[dict]:
    """The page's summaries: every v2 ``takeaway`` widget, or the v1 ``summary`` slot as gen-ai reads it.

    A v2 ``text`` widget with id ``summary`` is static text the default page templates ship empty,
    not a summary: the copilot writes its summaries into takeaways.
    """
    nodes = list(_nodes(page.get("layout")))
    takeaways = [node for node in nodes if _is_takeaway(node)]
    if takeaways:
        return takeaways
    for node in nodes:
        if node.get("id") == _SUMMARY_SLOT and "paragraph" in node:
            return [node]
    return []


def _summary_text(slot: dict) -> str | None:
    """The slot's written text: a takeaway's markdown, the model's on an AI summary, the string on a static one."""
    if _is_takeaway(slot):
        return _written(slot.get("markdown"))
    paragraph = slot.get("paragraph")
    return _written(paragraph.get("text") if isinstance(paragraph, dict) else paragraph)


def _slot_name(slot: dict) -> str:
    return "takeaway" if _is_takeaway(slot) else "summary slot"


def _content_pages(document: dict) -> list[tuple[int, dict]]:
    """``(page number, page)`` for every content page a reader sees, numbered as the reader sees them."""
    return [
        (number, page)
        for number, page in enumerate(_visible_pages(document), start=1)
        if isinstance(page, dict) and _page_kind(page) == _CONTENT_PAGE
    ]


def _period(document: dict) -> dict:
    period = document.get("period")
    return period if isinstance(period, dict) else {}


def _is_relative(period: dict) -> bool:
    """Whether an AaC period is relative: it states a granularity, which an absolute one never does."""
    return "granularity" in period


def _period_bounds(document: dict) -> tuple[Any, Any] | None:
    """The document's first and last day, or ``None`` for a v2 relative period, which has no fixed dates."""
    period = _period(document)
    if not _is_v2(document):
        return period.get("start"), period.get("end")
    if _is_relative(period):
        return None
    return period.get("from"), period.get("to")


def _filters(document: dict) -> Any:
    """A v2 document's filters, keyed by filter id in ``content``; read from the top level when ``content`` is missing."""
    content = document.get("content")
    container = content if isinstance(content, dict) else document
    return container.get("filters")


def _period_text(document: dict) -> str:
    bounds = _period_bounds(document)
    if bounds is None:
        period = _period(document)
        return f"the relative range {period.get('granularity')} {period.get('from')} to {period.get('to')}"
    return f"{bounds[0]} to {bounds[1]}"


def _expected_period_text(period: dict) -> str:
    """A fixture's ``period``: ``start`` and ``end`` dates, or a relative range as AaC writes it."""
    if _is_relative(period):
        return f"the relative range {period.get('granularity')} {period.get('from')} to {period.get('to')}"
    return f"{period.get('start')} to {period.get('end')}"


def render_document_text(document: dict) -> str:
    """The document as the judge reads it: title, period, and per content page its heading, charts and summaries."""
    lines = [f"Document: {document.get('title')}", f"Period: {_period_text(document)}"]
    for number, page in _content_pages(document):
        nodes = list(_nodes(page.get("layout")))
        headings = [h for h in (_heading(n) for n in nodes) if h is not None]
        charts = [c for c in (_visualization_id(n) for n in nodes) if c is not None]
        lines.append("")
        lines.append(f"Page {number}: {', '.join(headings) or '(no heading)'}")
        if charts:
            lines.append(f"Charts: {', '.join(charts)}")
        lines.extend(f"Summary: {text}" for text in map(_summary_text, _summary_slots(page)) if text is not None)
    return "\n".join(lines)


def _has_narrative(expected_output: dict) -> bool:
    return "narrative" in expected_output


def _has_period(expected_output: dict) -> bool:
    return "period" in expected_output


def _has_visualizations(expected_output: dict) -> bool:
    return "visualizations" in expected_output


def _has_chart_periods(expected_output: dict) -> bool:
    return "chart_periods" in expected_output


def _expects_clarification(expected_output: dict) -> bool:
    return "expects_clarification" in expected_output


def _asked_first_required(expected_output: dict) -> bool:
    return expected_output.get("asked_first_required") is True


def _rework(expected_output: dict) -> dict | None:
    """The fixture's ``rework`` expectation: the run must edit the open document rather than draft a new one."""
    rework = expected_output.get("rework")
    return rework if isinstance(rework, dict) else None


def _validate_rework(rework: Any) -> None:
    """Reject a ``rework`` expectation the run could not score meaningfully.

    A rework is scored on aac-v2 documents only. ``keeps_pages`` checks that each page id is still
    visible, not what the page shows. ``page_charts`` maps a kept page to the charts that must stay
    on it; the page may hold others too. ``new_page_charts`` lists the charts that must sit on a
    visible page outside ``keeps_pages``, which is what "add a page" asks for; ``visualizations``
    alone accepts a chart pushed onto an old page. ``filters`` maps each filter id the document must
    have, and no other, to the keys it is compared on, in the drafted document's ``content.filters``
    wire form. Each entry states at least the filter's ``type``, an attribute filter also its
    ``using`` and ``state``, with a ``null`` state for all, and a date filter its ``date``. Other keys
    an entry leaves out are
    not compared, so a converter that adds one does not fail the run, except a date filter's
    ``granularity``, ``from`` and ``to``: leaving out ``from`` and ``to`` states all time, and leaving
    out ``granularity`` states none. An attribute filter's ``state`` is compared on its selection: no
    values means all.
    """
    if not isinstance(rework, dict):
        raise ValueError(f"rework must be an object, got {type(rework).__name__}")
    unknown = sorted(set(rework) - _REWORK_KEYS)
    if unknown:
        raise ValueError(f"unknown rework key(s) {unknown}; known: {sorted(_REWORK_KEYS)}")
    base_document_id = rework.get("base_document_id")
    if not isinstance(base_document_id, str) or not base_document_id.strip():
        raise ValueError(f"rework needs the base_document_id of the open document, got {base_document_id!r}")
    if "keeps_pages" in rework:
        keeps_pages = rework["keeps_pages"]
        if not isinstance(keeps_pages, list) or not keeps_pages:
            raise ValueError("rework.keeps_pages is empty; the pages check would pass vacuously")
        if not all(isinstance(page_id, str) and page_id.strip() for page_id in keeps_pages):
            raise ValueError(f"every rework.keeps_pages entry must be a page id, got {keeps_pages!r}")
    if "page_charts" in rework:
        page_charts = rework["page_charts"]
        if not isinstance(page_charts, dict) or not page_charts:
            raise ValueError("rework.page_charts is empty; the page charts check would pass vacuously")
        kept = set(rework.get("keeps_pages") or [])
        for page_id, charts in page_charts.items():
            if page_id not in kept:
                raise ValueError(f"rework.page_charts page {page_id!r} must also be listed in rework.keeps_pages")
            if not isinstance(charts, list) or not charts:
                raise ValueError(f"rework.page_charts[{page_id!r}] must list the charts that stay on the page")
            if not all(isinstance(chart, str) and chart.strip() for chart in charts):
                raise ValueError(f"every rework.page_charts[{page_id!r}] entry must be a chart id, got {charts!r}")
    if "new_page_charts" in rework:
        new_page_charts = rework["new_page_charts"]
        if not isinstance(new_page_charts, list) or not new_page_charts:
            raise ValueError("rework.new_page_charts is empty; the new page check would pass vacuously")
        if not all(isinstance(chart, str) and chart.strip() for chart in new_page_charts):
            raise ValueError(f"every rework.new_page_charts entry must be a chart id, got {new_page_charts!r}")
        if "keeps_pages" not in rework:
            raise ValueError("rework.new_page_charts needs rework.keeps_pages to tell the open document's pages apart")
    if "title" in rework:
        title = rework["title"]
        if not isinstance(title, str) or not title.strip():
            raise ValueError(f"rework.title must be the title the edit leaves, got {title!r}")
    if "filters" in rework:
        filters = rework["filters"]
        if not isinstance(filters, dict):
            raise ValueError(f"rework.filters must be the document's filters keyed by id, got {filters!r}")
        for filter_id, entry in filters.items():
            if not isinstance(entry, dict) or not isinstance(entry.get("type"), str) or not entry["type"].strip():
                raise ValueError(
                    f"rework.filters[{filter_id!r}] must state at least the filter's 'type', got {entry!r}"
                )
            if entry["type"] not in _REQUIRED_FILTER_KEYS:
                raise ValueError(
                    f"rework.filters[{filter_id!r}] has type {entry['type']!r}; known: {sorted(_REQUIRED_FILTER_KEYS)}. "
                    f"A type needs its required keys decided before an item can state it"
                )
            unstated = [key for key in _REQUIRED_FILTER_KEYS[entry["type"]] if key not in entry]
            if unstated:
                raise ValueError(
                    f"rework.filters[{filter_id!r}] of type {entry['type']!r} leaves out {unstated}: an unstated key "
                    f"is not compared, so what the filter applies to would go unchecked; a null state means all"
                )
            problem = _state_problem(entry.get("state"), entry["type"])
            if problem is not None:
                raise ValueError(f"rework.filters[{filter_id!r}].state is {entry['state']!r}, {problem}")


def _validate_expectation(expected_output: Any) -> None:
    """Reject a fixture the run could not score meaningfully, before the first API call.

    Every key is optional. A key that is present has to be usable, because a malformed one
    would otherwise score vacuously or only surface on the branch where the copilot asks back.
    An unknown key is rejected too: a misspelt ``visualisations`` would otherwise leave the
    item scored on structure alone.

    Raises:
        ValueError: the expectation is unusable.
    """
    if not isinstance(expected_output, dict):
        raise ValueError(f"expected_output must be an object, got {type(expected_output).__name__}")
    unknown = sorted(set(expected_output) - _EXPECTATION_KEYS)
    if unknown:
        raise ValueError(f"unknown expected_output key(s) {unknown}; known: {sorted(_EXPECTATION_KEYS)}")
    if _has_period(expected_output):
        period = expected_output.get("period")
        if isinstance(period, dict) and _is_relative(period):
            extra = sorted(set(period) - {"granularity", "from", "to"})
            if extra:
                raise ValueError(f"a relative period states only 'granularity', 'from' and 'to', got {extra} too")
            granularity = period["granularity"]
            if not isinstance(granularity, str) or granularity not in _AAC_PERIOD_GRANULARITIES:
                raise ValueError(
                    f"a relative period's 'granularity' must be one AaC writes, one of "
                    f"{sorted(_AAC_PERIOD_GRANULARITIES)}, got {period!r}"
                )
            if not all(
                isinstance(period.get(bound), int) and not isinstance(period.get(bound), bool)
                for bound in ("from", "to")
            ):
                raise ValueError(f"a relative period needs whole numbers 'from' and 'to', got {period!r}")
        elif not isinstance(period, dict) or not period.get("start") or not period.get("end"):
            raise ValueError(f"period needs both 'start' and 'end', or a relative 'granularity', got {period!r}")
        elif extra := sorted(set(period) - {"start", "end"}):
            raise ValueError(f"an absolute period states only 'start' and 'end', got {extra} too")
    if _has_visualizations(expected_output):
        visualizations = expected_output.get("visualizations")
        if not isinstance(visualizations, list) or not visualizations:
            raise ValueError("visualizations is empty; the chart check would pass vacuously")
        for entry in visualizations:
            if not isinstance(entry, dict) or not entry.get("id"):
                raise ValueError(f"every visualization needs an 'id', got {entry!r}")
    if _has_chart_periods(expected_output):
        chart_periods = expected_output.get("chart_periods")
        if not isinstance(chart_periods, dict) or not chart_periods:
            raise ValueError(
                "chart_periods must map chart ids to the date dataset each applies the period on, "
                f"or null for a chart that ignores it, got {chart_periods!r}"
            )
        for chart, dataset in chart_periods.items():
            if not isinstance(chart, str) or not chart.strip():
                raise ValueError(f"every chart_periods key must be a chart id, got {chart!r}")
            if dataset is not None and (not isinstance(dataset, str) or not dataset.strip()):
                raise ValueError(f"chart_periods[{chart!r}] must be a date dataset id or null, got {dataset!r}")
    if _has_narrative(expected_output):
        narrative = expected_output.get("narrative")
        if not isinstance(narrative, str) or not narrative.strip():
            raise ValueError(
                f"narrative must be a non-empty description of what the summaries cover, got {narrative!r}"
            )
    if _expects_clarification(expected_output) and not isinstance(expected_output["expects_clarification"], bool):
        raise ValueError(
            f"expects_clarification must be true or false, got {expected_output['expects_clarification']!r}"
        )
    if "asked_first_required" in expected_output:
        if not isinstance(expected_output["asked_first_required"], bool):
            raise ValueError(
                f"asked_first_required must be true or false, got {expected_output['asked_first_required']!r}"
            )
        if expected_output["asked_first_required"] and expected_output.get("expects_clarification") is not True:
            raise ValueError("asked_first_required needs expects_clarification: true")
    if "clarification_reply" in expected_output:
        reply = expected_output["clarification_reply"]
        if not isinstance(reply, str) or not reply.strip():
            raise ValueError(f"clarification_reply must be a non-empty reply, got {reply!r}")
        if expected_output.get("expects_clarification") is not True:
            raise ValueError("clarification_reply needs expects_clarification: true")
    if "rework" in expected_output:
        _validate_rework(expected_output["rework"])


def _validate_user_context(user_context: dict | None) -> None:
    """Reject a user context that names the open document the Report way, before the first API call.

    gen-ai reads ``view.document``; a fixture still sending ``view.report`` would test the old input.

    Raises:
        ValueError: the user context carries ``view.report``.
    """
    view = (user_context or {}).get("view")
    if isinstance(view, dict) and _LEGACY_PART_TYPE in view:
        raise ValueError("user_context.view.report is the Report name; send view.document")


def _validate_rework_target(expected_output: dict, user_context: dict | None) -> None:
    """Reject a ``rework`` whose base id is not the open document the run sends, before the first API call.

    Otherwise every run would fail on ``base_document_id`` and read as a copilot regression. An
    unsaved open document has no id, so a rework of one cannot be stated.

    Raises:
        ValueError: the item states a rework, and ``user_context.view.document`` is missing,
            has no id, or has another id; or it states ``new_page_charts`` while the open document
            sends no pages or has a hidden page, or ``keeps_pages`` leaves out one of its pages.
    """
    rework = _rework(expected_output)
    if rework is None:
        return
    view = (user_context or {}).get("view")
    document = view.get(_PART_TYPE) if isinstance(view, dict) else None
    if not isinstance(document, dict):
        raise ValueError("rework needs the open document in user_context.view.document")
    open_id = document.get("id")
    if not isinstance(open_id, str) or not open_id.strip():
        raise ValueError(f"rework needs the open document's id in user_context.view.document.id, got {open_id!r}")
    if open_id != rework["base_document_id"]:
        raise ValueError(f"rework.base_document_id {rework['base_document_id']!r} is not the open document {open_id!r}")
    if "new_page_charts" in rework:
        # A new page is one outside keeps_pages, so an open page left off the list would count as new,
        # and a chart pushed onto it would pass. A hidden open page cannot be listed, since a kept page
        # must stay visible, so an item over a document with one cannot state new_page_charts.
        definition = document.get("definition")
        open_pages = _pages(definition) if isinstance(definition, dict) else []
        if not open_pages:
            raise ValueError(
                "rework.new_page_charts needs the open document's pages in user_context.view.document.definition"
            )
        hidden = [page.get("id") for page in open_pages if isinstance(page, dict) and page.get("visible") is False]
        if hidden:
            raise ValueError(
                f"rework.new_page_charts cannot be scored over an open document with hidden pages {hidden!r}: "
                "showing one again would count as a new page"
            )
        unlisted = [
            page.get("id")
            for page in open_pages
            if isinstance(page, dict) and page.get("id") not in rework["keeps_pages"]
        ]
        if unlisted:
            raise ValueError(
                f"rework.new_page_charts needs keeps_pages to list every page of the open document; "
                f"missing {unlisted!r}"
            )


def build_simulated_reply(expected_output: dict, *, asked: bool = True) -> str:
    """The reply the simulated user sends when the copilot asks back instead of drafting.

    Deterministic and LLM-free, built from what the fixture states, so a failure stays the
    copilot's rather than a simulated user that phrased things differently each run.
    A fixture's ``clarification_reply`` replaces it after a turn that ``asked``, for a question
    the charts and period do not answer. The run sends it once, to the first such turn.
    """
    if asked and isinstance(reply := expected_output.get("clarification_reply"), str):
        return reply
    segments: list[str] = []
    visualizations = expected_output.get("visualizations") or []
    if visualizations:
        titles = ", ".join(str(v.get("title") or v.get("id")) for v in visualizations)
        segments.append(f"Please use these charts: {titles}.")
    period = expected_output.get("period")
    if isinstance(period, dict):
        segments.append(f"Period: {_expected_period_text(period)}.")
    if _rework(expected_output) is not None:
        segments.append("Anything else is up to you. Please make the change in the open document now.")
    else:
        segments.append("Anything else is up to you. Please create the document now.")
    return " ".join(segments)


@dataclass(frozen=True)
class _Applies:
    """Which conditional checks the case applies; published only when they do.

    A check that could not fail is not evidence, and publishing it as passed would lift
    ``quality_score`` above what the run earned.
    """

    period: bool
    charts: bool
    narrative: bool = False
    asked_first: bool = False
    rework: bool = False
    pages_kept: bool = False
    page_charts: bool = False
    new_page_charts: bool = False
    title: bool = False
    filters: bool = False
    chart_periods: bool = False


@dataclass
class DocumentEvaluation:
    """Per-run outcome of the document-skill checks; ``strict_checks`` is what the run is scored on."""

    drafted: bool
    part_present: bool
    ref_matches: bool
    pages_consistent: bool
    not_saved: bool
    skill_activated: bool
    applies: _Applies
    wire_names_current: bool = True
    period_correct: bool = False
    charts_matched: bool = False
    summaries_present: bool = False
    narrative_judged: bool = False
    asked_first: bool = False
    new_draft: bool = False
    reworks_open: bool = False
    pages_kept: bool = False
    page_charts_kept: bool = False
    new_page_charts_placed: bool = False
    title_correct: bool = False
    filters_kept: bool = False
    chart_periods_correct: bool = False
    judge_reasoning: str = ""
    # Set when the judge returned something unreadable. The run then has no narrative verdict:
    # it is neither published as a 0 nor allowed to pass on the remaining checks.
    judge_error: str | None = None
    # Set when the only takeaways left without text are those the takeaway endpoint failed transiently
    # to write. The summaries and the narrative then have no verdict, as above.
    fill_error: str | None = None
    failures: list[str] = field(default_factory=list)

    @property
    def strict_pass(self) -> bool:
        return self.judge_error is None and self.fill_error is None and all(self.strict_checks.values())

    @property
    def ungraded(self) -> bool:
        """The judge or the takeaway endpoint left the narrative without a verdict, and it was the only check still open.

        A run that already failed another check is a failure whatever the judge would have said,
        so a judge or fill error there leaves it failed rather than ungraded. A fill error is only
        set when nothing but the transient endpoint failure left a takeaway without text.
        """
        return (self.judge_error is not None or self.fill_error is not None) and all(self.strict_checks.values())

    @property
    def strict_checks(self) -> dict[str, bool]:
        # Every name carries the `document_` prefix so a trace can be told apart from other skills'
        # by its score names alone; a name shared with another skill would make that ambiguous.
        checks = {
            "document_drafted": self.drafted,
            "document_part_present": self.part_present,
            "document_ref_matches": self.ref_matches,
            "document_pages_consistent": self.pages_consistent,
            "document_not_saved": self.not_saved,
            "document_skill_activated": self.skill_activated,
            "document_wire_names": self.wire_names_current,
        }
        if self.applies.period:
            checks["document_period_correct"] = self.period_correct
        if self.applies.charts:
            checks["document_charts_matched"] = self.charts_matched
        if self.applies.narrative and self.fill_error is None:
            checks["document_summaries_present"] = self.summaries_present
            if self.judge_error is None:
                checks["document_narrative_judged"] = self.narrative_judged
        if self.applies.asked_first:
            checks["document_asked_first"] = self.asked_first
        if self.applies.rework:
            checks["document_reworks_open"] = self.reworks_open
        else:
            checks["document_new_draft"] = self.new_draft
        if self.applies.pages_kept:
            checks["document_pages_kept"] = self.pages_kept
        if self.applies.page_charts:
            checks["document_page_charts_kept"] = self.page_charts_kept
        if self.applies.new_page_charts:
            checks["document_new_page_charts_placed"] = self.new_page_charts_placed
        if self.applies.title:
            checks["document_title_correct"] = self.title_correct
        if self.applies.filters:
            checks["document_filters_kept"] = self.filters_kept
        if self.applies.chart_periods:
            checks["document_chart_periods_correct"] = self.chart_periods_correct
        return checks


def _read_document(document_part: dict | None) -> tuple[dict | None, str | None]:
    """The part's document, or why it carries no usable one."""
    if document_part is None:
        return None, f"the response carries no {_PART_TYPE!r} part"
    document = document_part.get(_PART_TYPE)
    if not isinstance(document, dict):
        return (
            None,
            f"the {_PART_TYPE!r} part carries no document (document_ref {document_part.get('document_ref')!r})",
        )
    if document.get("type") != _PART_TYPE:
        return None, (
            f"the {_PART_TYPE!r} part carries a document of type {document.get('type')!r}, expected {_PART_TYPE!r}"
        )
    return document, None


def evaluate_document_response(
    tool_result: dict | None,
    document_part: dict | None,
    expected_output: dict,
    *,
    skill_activated: bool,
    legacy_names: list[str] | None = None,
    exempt_takeaways: frozenset[tuple[str, str]] = frozenset(),
) -> DocumentEvaluation:
    """Score one document response against its expectation.

    ``legacy_names`` are the Report names the run saw on the wire, from ``legacy_wire_names``.
    Any of them fails ``document_wire_names`` and leads the failures, because a gen-ai still on
    the Report names also fails every check that looks for the Document ones.

    ``exempt_takeaways`` are ``(page id, takeaway id)`` pairs that may stay empty, from
    ``_saved_empty_takeaways``.

    Pure: no network and no conversation state, so the whole assertion surface is unit-testable
    without an agent.
    """
    evaluation = _score_response(
        tool_result, document_part, expected_output, skill_activated=skill_activated, exempt_takeaways=exempt_takeaways
    )
    if legacy_names:
        evaluation.wire_names_current = False
        evaluation.failures.insert(0, f"gen-ai sends the Report names: {', '.join(legacy_names)}")
    return evaluation


def _state_problem(state: Any, kind: str) -> str | None:
    """Why a filter's ``state`` cannot be read as a selection, or nothing.

    A missing or ``null`` state reads as all, as does an empty object; any other falsey value is malformed.
    """
    if state is None:
        return None
    if not isinstance(state, dict):
        return "expected an object"
    for key in ("include", "exclude"):
        if state.get(key) is not None and not isinstance(state[key], list):
            return f"expected a list of values under {key!r}"
    if state.get("include") and state.get("exclude"):
        return "expected either 'include' or 'exclude', not both"
    if kind == "attribute_filter" and not set(state) <= {"include", "exclude"}:
        return "expected only 'include' or 'exclude'"
    return None


def _filter_mismatch(filter_id: str, actual: Any, expected: dict) -> list[str]:
    """Why one drafted filter differs from the expectation, or nothing.

    The kind must match. An attribute filter's ``state`` is compared on its selection, a date
    filter on its range with absence significant, and any other key the expectation states as written.
    """
    if not isinstance(actual, dict):
        return [f"filter {filter_id!r} is {actual!r}, expected an object"]
    kind = expected["type"]
    if actual.get("type") != kind:
        return [f"filter {filter_id!r} has type {actual.get('type')!r}, expected {kind!r}"]
    keys = [key for key in expected if key != "type"]
    if kind == "date_filter":
        keys += [key for key in _DATE_FILTER_RANGE_KEYS if key not in expected]
    reasons: list[str] = []
    for key in keys:
        if key == "state" and kind == "attribute_filter":
            problem = _state_problem(actual.get("state"), kind)
            if problem is not None:
                reasons.append(f"filter {filter_id!r} has state {actual.get('state')!r}, {problem}")
            elif not same_selection(selection_of(actual), selection_of(expected)):
                reasons.append(
                    f"filter {filter_id!r} selects {describe_selection(selection_of(actual))}, "
                    f"expected {describe_selection(selection_of(expected))}"
                )
        elif actual.get(key) != expected.get(key):
            reasons.append(f"filter {filter_id!r} has {key} {actual.get(key)!r}, expected {expected.get(key)!r}")
    return reasons


def _new_page_misses(new_page_charts: list[str], keeps_pages: list[str], pages: list[Any]) -> list[str]:
    """Why a chart the edit should have put on a new page is not on one."""
    kept = set(keeps_pages)
    reasons: list[str] = []
    for chart in new_page_charts:
        holders = [page.get("id") for page in pages if isinstance(page, dict) and chart in _page_visualizations(page)]
        if any(page_id not in kept for page_id in holders):
            continue
        if holders:
            reasons.append(
                f"chart {chart!r} must be on a new page, but it is only on page(s) {holders!r} of the open document"
            )
        else:
            reasons.append(f"chart {chart!r} must be on a new page, but no visible page has it")
    return reasons


def _chart_period_misses(chart_periods: dict[str, str | None], document: dict) -> list[str]:
    """Why charts do not apply the document period where the item says, or nothing.

    A chart applies the period on its widget's ``date``; a widget with ``ignore_document_period``
    applies none, as a dashboard chart the date filter does not reach. A dataset of ``None`` asks
    for the latter. Every placement of a chart on a page a reader sees must agree.
    """
    placements: dict[str, list[dict]] = {}
    for page in _visible_pages(document):
        if isinstance(page, dict):
            for node in _nodes(page.get("layout")):
                if (chart := _visualization_id(node)) is not None:
                    placements.setdefault(chart, []).append(node)
    misses: list[str] = []
    for chart, expected in chart_periods.items():
        widgets = placements.get(chart)
        if not widgets:
            misses.append(f"chart {chart!r} is not in the document, so where it applies the period is unknown")
            continue
        for widget in widgets:
            ignores = widget.get("ignore_document_period") is True
            if expected is None and not ignores:
                misses.append(
                    f"chart {chart!r} applies the period on {widget.get('date')!r}, expected it to ignore the period"
                )
            elif expected is not None and (ignores or widget.get("date") != expected):
                applied = "ignores the period" if ignores else f"applies the period on {widget.get('date')!r}"
                misses.append(f"chart {chart!r} {applied}, expected it on {expected!r}")
    return list(dict.fromkeys(misses))


def _score_rework(
    rework: dict, document: dict, document_part: dict, pages: list[Any], failures: list[str]
) -> tuple[bool, bool, bool, bool, bool, bool]:
    """``(reworks_open, pages_kept, page_charts_kept, new_page_charts_placed, title_correct, filters_kept)`` of a v2 edit.

    A check the item does not state is False.
    """
    base_document_id = document_part.get("base_document_id")
    reworks_open_document = document_part.get("reworks_open_document") is True
    expected_base = rework["base_document_id"]
    if base_document_id != expected_base:
        failures.append(
            f"the edit must apply to the open document {expected_base!r}, "
            f"but it reports base_document_id {base_document_id!r}"
        )
    if not reworks_open_document:
        failures.append("the edit must be written from the open document, but reworks_open_document is not true")
    reworks_open = base_document_id == expected_base and reworks_open_document

    pages_kept = False
    if "keeps_pages" in rework:
        present = {page.get("id") for page in pages if isinstance(page, dict)}
        lost = [page_id for page_id in rework["keeps_pages"] if page_id not in present]
        failures.extend(f"the edit lost page {page_id!r} of the open document" for page_id in lost)
        pages_kept = not lost

    page_charts_kept = False
    if "page_charts" in rework:
        by_id = {page.get("id"): page for page in pages if isinstance(page, dict)}
        moved = [
            (chart, page_id)
            for page_id, charts in rework["page_charts"].items()
            for chart in charts
            if chart not in _page_visualizations(by_id.get(page_id))
        ]
        failures.extend(
            f"chart {chart!r} is no longer on page {page_id!r} of the open document" for chart, page_id in moved
        )
        page_charts_kept = not moved

    new_page_charts_placed = False
    if "new_page_charts" in rework:
        misses = _new_page_misses(rework["new_page_charts"], rework["keeps_pages"], pages)
        failures.extend(misses)
        new_page_charts_placed = not misses

    title_correct = False
    if "title" in rework:
        title_correct = document.get("title") == rework["title"]
        if not title_correct:
            failures.append(f"the document is titled {document.get('title')!r}, expected {rework['title']!r}")

    filters_kept = False
    if "filters" in rework:
        # A document without filters omits the key, which matches an expectation of none.
        actual_filters = _filters(document)
        if actual_filters is None:
            actual_filters = {}
        expected_filters = rework["filters"]
        if not isinstance(actual_filters, dict):
            reasons = [f"the document filters are {actual_filters!r}, expected an object keyed by filter id"]
        else:
            reasons = [
                f"the edit lost filter {filter_id!r}"
                for filter_id in expected_filters
                if filter_id not in actual_filters
            ]
            reasons += [
                f"the edit added filter {filter_id!r}"
                for filter_id in actual_filters
                if filter_id not in expected_filters
            ]
            for filter_id, expected in expected_filters.items():
                if filter_id in actual_filters:
                    reasons += _filter_mismatch(filter_id, actual_filters[filter_id], expected)
        failures.extend(reasons)
        filters_kept = not reasons
    return reworks_open, pages_kept, page_charts_kept, new_page_charts_placed, title_correct, filters_kept


def _score_response(
    tool_result: dict | None,
    document_part: dict | None,
    expected_output: dict,
    *,
    skill_activated: bool,
    exempt_takeaways: frozenset[tuple[str, str]] = frozenset(),
) -> DocumentEvaluation:
    rework = _rework(expected_output)
    applies = _Applies(
        period=_has_period(expected_output),
        charts=_has_visualizations(expected_output),
        narrative=_has_narrative(expected_output),
        rework=rework is not None,
        pages_kept=rework is not None and "keeps_pages" in rework,
        page_charts=rework is not None and "page_charts" in rework,
        new_page_charts=rework is not None and "new_page_charts" in rework,
        title=rework is not None and "title" in rework,
        filters=rework is not None and "filters" in rework,
        chart_periods=_has_chart_periods(expected_output),
    )

    if tool_result is None:
        return DocumentEvaluation(
            drafted=False,
            part_present=False,
            ref_matches=False,
            pages_consistent=False,
            not_saved=False,
            skill_activated=skill_activated,
            applies=applies,
            failures=[f"the agent never produced a successful {_DRAFT_TOOL} call"],
        )

    document, part_failure = _read_document(document_part)
    if document is None or document_part is None:
        return DocumentEvaluation(
            drafted=True,
            part_present=False,
            ref_matches=False,
            pages_consistent=False,
            not_saved=False,
            skill_activated=skill_activated,
            applies=applies,
            failures=[part_failure] if part_failure else [],
        )

    failures: list[str] = []

    part_ref, tool_ref = document_part.get("document_ref"), tool_result.get("ref")
    ref_matches = isinstance(part_ref, str) and bool(part_ref) and part_ref == tool_ref
    if not ref_matches:
        failures.append(f"the {_PART_TYPE!r} part shows {part_ref!r}, but {_DRAFT_TOOL} returned {tool_ref!r}")

    # page_count is what the user is told ("a document with 3 pages"), so it counts only the
    # pages a reader sees: a hidden page is out of the viewer, exports and page numbering.
    pages = _visible_pages(document)
    part_count, tool_count = document_part.get("page_count"), tool_result.get("page_count")
    if part_count != len(pages) or tool_count != len(pages):
        failures.append(
            f"the document has {len(pages)} page(s), but the part says {part_count} and {_DRAFT_TOOL} said {tool_count}"
        )
        pages_consistent = False
    else:
        kinds = [_page_kind(page) for page in pages if isinstance(page, dict)]
        if not kinds or kinds[0] != _COVER_PAGE:
            failures.append(f"the document opens with a {kinds[0] if kinds else None!r} page, not a cover")
        if _CONTENT_PAGE not in kinds:
            failures.append("the document has no content page")
        pages_consistent = bool(kinds) and kinds[0] == _COVER_PAGE and _CONTENT_PAGE in kinds

    not_saved = True
    saved_document_id = document_part.get("saved_document_id")
    if saved_document_id is not None:
        draft = "a new draft" if rework is None else "an edit"
        failures.append(f"{draft} must not be saved yet, but it reports saved_document_id {saved_document_id!r}")
        not_saved = False

    new_draft = reworks_open = pages_kept = page_charts_kept = new_page_charts_placed = False
    title_correct = filters_kept = False
    if rework is None:
        new_draft = True
        base_document_id = document_part.get("base_document_id")
        if base_document_id is not None:
            failures.append(
                f"a new draft must not edit a saved document, but it reports base_document_id {base_document_id!r}"
            )
            new_draft = False
        if document_part.get("reworks_open_document") is True:
            failures.append("a new draft must not rework the open document, but it reports reworks_open_document")
            new_draft = False
    elif not _is_v2(document):
        failures.append(
            f"a rework is scored on aac-v2 documents only, but the draft is version {document.get('version')!r}"
        )
    else:
        reworks_open, pages_kept, page_charts_kept, new_page_charts_placed, title_correct, filters_kept = _score_rework(
            rework, document, document_part, pages, failures
        )

    period_correct = False
    if applies.period:
        expected_period = expected_output["period"]
        if _is_relative(expected_period):
            actual = _period(document) if _is_v2(document) else {}
            period_correct = _is_relative(actual) and all(
                actual.get(key) == expected_period[key] for key in ("granularity", "from", "to")
            )
        else:
            period_correct = _period_bounds(document) == (expected_period.get("start"), expected_period.get("end"))
        if not period_correct:
            failures.append(
                f"the document covers {_period_text(document)}, expected {_expected_period_text(expected_period)}"
            )

    charts_matched = False
    if applies.charts:
        placed = _visualizations_of(document)
        missing = [v for v in expected_output["visualizations"] if v.get("id") not in placed]
        failures.extend(f"the document does not show chart {v.get('id')!r} ({v.get('title')!r})" for v in missing)
        charts_matched = not missing

    chart_periods_correct = False
    if applies.chart_periods:
        if _is_v2(document):
            misses = _chart_period_misses(expected_output["chart_periods"], document)
        else:
            misses = ["where a chart applies the period is scored on aac-v2 documents only"]
        failures.extend(misses)
        chart_periods_correct = not misses

    summaries_present = False
    if applies.narrative:
        slots = [(page, slot) for _number, page in _content_pages(document) for slot in _summary_slots(page)]
        unwritten = [
            f"page {page.get('id')!r} has a {_slot_name(slot)} with no written text"
            for page, slot in slots
            if _summary_text(slot) is None and (page.get("id"), slot.get("id")) not in exempt_takeaways
        ]
        if not slots:
            missing = "takeaway" if _is_v2(document) else "summary slot"
            failures.append(f"the document has no {missing}")
        failures.extend(dict.fromkeys(unwritten))
        summaries_present = bool(slots) and not unwritten

    return DocumentEvaluation(
        drafted=True,
        part_present=True,
        ref_matches=ref_matches,
        pages_consistent=pages_consistent,
        not_saved=not_saved,
        skill_activated=skill_activated,
        applies=applies,
        period_correct=period_correct,
        charts_matched=charts_matched,
        summaries_present=summaries_present,
        new_draft=new_draft,
        reworks_open=reworks_open,
        pages_kept=pages_kept,
        page_charts_kept=page_charts_kept,
        new_page_charts_placed=new_page_charts_placed,
        title_correct=title_correct,
        filters_kept=filters_kept,
        chart_periods_correct=chart_periods_correct,
        failures=failures,
    )


@dataclass
class _EditorFill:
    """The document part with the takeaways the editor would write filled in, and how that went."""

    document_part: dict
    filled_page_ids: list[str] = field(default_factory=list)
    failures: list[str] = field(default_factory=list)
    # The pages whose takeaway the endpoint failed transiently to write, and the first such failure.
    transient_page_ids: set[str] = field(default_factory=set)
    error: str | None = None
    # The editor starts every takeaway at once, so the reader waits for the slowest request, retries included.
    waited_s: float = 0.0
    # The pages with a takeaway the editor writes, as the editor's rule decides; unknown when the draft
    # did not convert.
    generated_page_ids: set[str] = field(default_factory=set)
    readable: bool = True
    # The takeaways allowed to stay empty, see ``_saved_empty_takeaways``.
    exempt: frozenset[tuple[str, str]] = frozenset()

    def ungraded_error(self) -> str | None:
        """The transient failure, when it alone left takeaways of the filled part without text."""
        document = self.document_part.get(_PART_TYPE)
        if self.error is None or self.failures or not isinstance(document, dict):
            return None
        unwritten = {
            page.get("id")
            for _number, page in _content_pages(document)
            for slot in _summary_slots(page)
            if _summary_text(slot) is None and (page.get("id"), slot.get("id")) not in self.exempt
        }
        return self.error if unwritten <= self.transient_page_ids else None


def _editor_page_ids(tool_result: dict | None, document_part: dict | None) -> list[str] | None:
    """The pages the copilot says it left to the editor; None unless a v2 draft carries the field."""
    document, _ = _read_document(document_part)
    listed = (tool_result or {}).get(_EDITOR_PAGES_KEY)
    if document is None or not _is_v2(document) or not isinstance(listed, list):
        return None
    return [page_id for page_id in listed if isinstance(page_id, str)]


def _saved_definition(user_context: dict | None) -> dict | None:
    """The open document the item sends as ``user_context.view.document.definition``, when it is a v2 document."""
    view = (user_context or {}).get("view")
    document = view.get("document") if isinstance(view, dict) else None
    definition = document.get("definition") if isinstance(document, dict) else None
    return definition if isinstance(definition, dict) and _is_v2(definition) else None


def _saved_empty_takeaways(document_part: dict | None, user_context: dict | None) -> frozenset[tuple[str, str]]:
    """The empty takeaways of the draft that the editor leaves empty, as ``(page id, takeaway id)``.

    The editor keeps an empty takeaway empty when the open document holds the same takeaway, empty, on
    the same page and the editor's request for it (visualizations under their filters, period included,
    and instructions) is identical. Every other empty takeaway is written. No open document, one that
    is not a v2 document, or a request that cannot be built exempts nothing.
    """
    saved_definition = _saved_definition(user_context)
    document, _ = _read_document(document_part)
    if saved_definition is None or document is None or not _is_v2(document):
        return frozenset()
    try:
        saved = aac_document_to_declarative(saved_definition)
        current = aac_document_to_declarative(document)
    except ValueError:
        return frozenset()
    saved_pages = {page.get("id"): page for page in _pages(saved) if isinstance(page, dict)}
    current_pages = {page.get("id"): page for page in _pages(current) if isinstance(page, dict)}
    exempt: set[tuple[str, str]] = set()
    for _number, page in _content_pages(document):
        page_id = page.get("id")
        saved_page = saved_pages.get(page_id)
        if not isinstance(page_id, str) or saved_page is None:
            continue
        saved_slots = {slot.get("id"): slot for slot in _summary_slots(saved_page)}
        current_slots = {slot.get("id"): slot for slot in _summary_slots(current_pages.get(page_id, {}))}
        for slot in _summary_slots(page):
            slot_id = slot.get("id")
            if not isinstance(slot_id, str):
                continue
            saved_slot, current_slot = saved_slots.get(slot_id), current_slots.get(slot_id)
            if not _is_takeaway(slot) or _summary_text(slot) is not None:
                continue
            if saved_slot is None or current_slot is None or _summary_text(saved_slot) is not None:
                continue
            saved_request = editor_takeaway_input(saved, saved_page, saved_slot)
            current_request = editor_takeaway_input(current, current_pages[page_id], current_slot)
            if not isinstance(saved_request, str) and saved_request == current_request:
                exempt.add((page_id, slot_id))
    return frozenset(exempt)


def _unavailable_chart(exc: httpx.HTTPStatusError) -> str | None:
    """The endpoint's ``detail`` when it refused a request because a chart does not exist or is not available to AI."""
    if exc.response.status_code != 404 or "not available to ai" not in exc.response.text.lower():
        return None
    try:
        detail = exc.response.json().get("detail")
    except ValueError:
        detail = None
    return detail if isinstance(detail, str) and detail else exc.response.text


def _fill_editor_takeaways(
    client: TakeawayClient, document_part: dict, exempt: frozenset[tuple[str, str]], agent_id: str | None
) -> _EditorFill:
    """Write each unwritten takeaway the way the editor does, on a copy of the part.

    The editor writes every empty takeaway except the ones it keeps empty, see ``_saved_empty_takeaways``.
    The part carries the document as code; each request is built from its declarative form, which is
    what the editor reads, and the text is written into the copy of the part. A document that does not
    convert is a failure of the run, and so is a request for a chart that does not exist or is not
    available to AI. A takeaway that already has text is left as the copilot wrote it. A transient
    endpoint failure leaves that takeaway unwritten, records its page, and the fill goes on.

    Raises:
        httpx.HTTPError: the endpoint refused a request for a reason that is not transient (flag
            off, unknown agent, invalid body): a setup problem, not a result.
    """
    fill = _EditorFill(document_part=copy.deepcopy(document_part), exempt=exempt)
    document = fill.document_part[_PART_TYPE]
    try:
        declarative = aac_document_to_declarative(document)
    except ValueError as exc:
        fill.failures.append(f"the eval cannot read the draft as the editor does: {exc}")
        fill.readable = False
        return fill
    editor_pages = {page.get("id"): page for page in _pages(declarative) if isinstance(page, dict)}
    for _number, page in _content_pages(document):
        page_id = page.get("id")
        if not isinstance(page_id, str):
            continue
        editor_page = editor_pages.get(page_id, {})
        # The conversion keeps each widget's id, so a takeaway finds its declarative form by id.
        editor_slots = {editor_slot.get("id"): editor_slot for editor_slot in _summary_slots(editor_page)}
        for slot in _summary_slots(page):
            if not _is_takeaway(slot) or _summary_text(slot) is not None or (page_id, slot.get("id")) in exempt:
                continue
            fill.generated_page_ids.add(page_id)
            editor_slot = editor_slots.get(slot.get("id"))
            if editor_slot is None:
                fill.failures.append(
                    f"page {page_id!r}: the eval cannot build the editor's takeaway request: "
                    f"takeaway {slot.get('id')!r} is missing from the converted document"
                )
                continue
            takeaway_input = editor_takeaway_input(declarative, editor_page, editor_slot)
            if isinstance(takeaway_input, str):
                fill.failures.append(
                    f"page {page_id!r}: the eval cannot build the editor's takeaway request: {takeaway_input}"
                )
                continue
            requested = time.monotonic()
            try:
                result = client.request(takeaway_input.model_copy(update={"agent_id": agent_id}))
            except httpx.HTTPError as exc:
                if isinstance(exc, httpx.HTTPStatusError) and (detail := _unavailable_chart(exc)) is not None:
                    fill.failures.append(f"page {page_id!r}: the takeaway endpoint refused the chart: {detail}")
                    continue
                if not is_transient(exc):
                    raise
                fill.transient_page_ids.add(page_id)
                if fill.error is None:
                    fill.error = f"takeaway endpoint for page {page_id!r}: {type(exc).__name__}: {exc}"
                continue
            finally:
                fill.waited_s = max(fill.waited_s, time.monotonic() - requested)
            text = (result.text_response or "").strip()
            if (result.raw_response or {}).get("noData") is True:
                fill.failures.append(f"page {page_id!r}: the editor's takeaway request found no data")
            elif not text:
                fill.failures.append(f"page {page_id!r}: the takeaway endpoint wrote no text")
            else:
                slot["markdown"] = text
                fill.filled_page_ids.append(page_id)
    return fill


def _listed_pages_mismatch(listed: list[str], generated: set[str]) -> list[str]:
    """Failures for ``takeaway_editor_page_ids`` where it differs from the pages the editor writes a takeaway on."""
    failures = [
        f"page {page_id!r} has a takeaway the editor writes, but draft_document does not list it in {_EDITOR_PAGES_KEY}"
        for page_id in sorted(generated - set(listed))
    ]
    failures.extend(
        f"draft_document lists page {page_id!r} in {_EDITOR_PAGES_KEY}, but the editor writes no takeaway there"
        for page_id in dict.fromkeys(listed)
        if page_id not in generated
    )
    return failures


def _judge_narrative(
    evaluation: DocumentEvaluation, judge: LLMJudge, document_part: dict | None, question: str, narrative: str
) -> float:
    """Grade the drafted document's narrative into ``evaluation``; return the seconds the judge took.

    No document means nothing to grade, which is a failed narrative rather than a judge call.
    """
    document = (document_part or {}).get(_PART_TYPE) if evaluation.part_present else None
    if not isinstance(document, dict):
        return 0.0
    started = time.monotonic()
    verdict = score_run(judge, input=question, expected_output=narrative, actual_output=render_document_text(document))
    elapsed = time.monotonic() - started
    log_timer(f"[timer] document_skill {judge.model} judge complete after {elapsed:.2f}s")
    if verdict.error is not None:
        evaluation.judge_error = verdict.error
        return elapsed
    evaluation.narrative_judged = verdict.passed
    evaluation.judge_reasoning = verdict.reasoning
    if not verdict.passed:
        evaluation.failures.append(f"the judge failed the narrative: {verdict.reasoning}")
    return elapsed


@dataclass
class DocumentRunResult:
    """Outcome of one conversation."""

    conversation_id: str
    evaluation: DocumentEvaluation
    expects_clarification: bool = False
    asked_first: bool = False
    tool_result: dict | None = None
    document_part: dict | None = None
    total_turns: int = 0
    total_steps: int = 0
    reasoning_steps: list[str] = field(default_factory=list)
    response_id: str | None = None
    tool_call_events: list[ToolCallEvent] = field(default_factory=list)
    reasoning_step_events: list[ReasoningStepEvent] = field(default_factory=list)
    timings: PhaseTimings = field(default_factory=PhaseTimings)
    # This run's own wall time, from just before its chat call to the end of its scoring.
    run_latency_s: float = 0.0
    # How many takeaways the editor's takeaway request wrote; None when no takeaway was requested:
    # the copilot left none to the editor, or the fixture states no narrative.
    takeaways_by_editor: int | None = None

    @property
    def diagnostics(self) -> dict[str, bool]:
        """Observed but not scored.

        Whether the copilot asked before drafting is recorded only when the fixture says it
        expects a question. It gates only when the fixture sets ``asked_first_required``: how
        much the copilot should ask is a product decision, made per item.
        """
        if not self.expects_clarification or self.evaluation.applies.asked_first:
            return {}
        return {"document_asked_first": self.asked_first}

    @property
    def judge_error(self) -> str | None:
        """Why the run has no narrative verdict: the judge's error, or the takeaway endpoint's."""
        return self.evaluation.judge_error or self.evaluation.fill_error

    @property
    def request_error(self) -> str | None:
        """The takeaway endpoint's transient failure, when it alone left the run without a narrative verdict."""
        return self.evaluation.fill_error

    @property
    def ungraded(self) -> bool:
        return self.evaluation.ungraded

    @property
    def summaries_from_data(self) -> int | None:
        value = (self.tool_result or {}).get("summaries_from_data")
        return value if isinstance(value, int) else None


@dataclass
class AgenticDocumentSummary:
    """Aggregated outcome of K runs."""

    run_results: list[DocumentRunResult]
    pass_at_k: bool
    pass_power_k: bool
    best: DocumentRunResult

    @property
    def scored_run_results(self) -> list[DocumentRunResult]:
        """Every run except the ungraded ones: those the narrative verdict alone would have decided."""
        return [r for r in self.run_results if not r.ungraded]

    @property
    def unscored_errors(self) -> list[str]:
        """Why each ungraded run has no narrative verdict, whichever source failed."""
        return [r.judge_error for r in self.run_results if r.ungraded and r.judge_error is not None]

    @property
    def judge_errors(self) -> list[str]:
        """The judge's errors on ungraded runs; the takeaway endpoint's are in ``request_errors``."""
        return [
            r.evaluation.judge_error
            for r in self.run_results
            if r.ungraded and r.request_error is None and r.evaluation.judge_error is not None
        ]

    @property
    def request_errors(self) -> list[str]:
        """The takeaway endpoint's transient failures on ungraded runs."""
        return [r.request_error for r in self.run_results if r.ungraded and r.request_error is not None]


def _execute_single_document_run(
    client: ChatClient,
    conversation_id: str,
    question: str,
    expected_output: dict,
    max_iterations: int,
    judge: LLMJudge | None = None,
    takeaways: TakeawayClient | None = None,
    user_context: dict | None = None,
    agent_id: str | None = None,
) -> DocumentRunResult:
    """Drive one conversation until the copilot drafts a document, then evaluate it.

    When the fixture states a narrative and the draft carries ``takeaway_editor_page_ids``,
    ``takeaways`` writes each empty takeaway as the editor does, as ``agent_id``, the agent of the
    chat turn, and the document is graded with them. A takeaway the open document in
    ``user_context`` held empty under the same request stays empty, see ``_saved_empty_takeaways``.
    The field is checked against the pages the editor writes a takeaway on.

    Nothing is cleaned up on the way out by design: gen-ai keeps the draft in conversation
    state and persists nothing until a user saves it.

    Raises:
        httpx.HTTPError: the takeaway endpoint refused a request for a reason that is not transient.
    """
    tool_result: dict | None = None
    document_part: dict | None = None
    turns = 0
    steps = 0
    current_question = question
    reasoning_steps: list[str] = []
    response_id: str | None = None
    all_tool_call_events: list[ToolCallEvent] = []
    all_reasoning_step_events: list[ReasoningStepEvent] = []
    all_parts: list[dict] = []
    timings = PhaseTimings()
    turn_offset = 0.0
    tool_index_offset = 0
    reasoning_index_offset = 0
    asked_before_draft = False
    replied = False

    run_started = time.monotonic()
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
        all_parts.extend(chat_result.unhandled_parts)
        steps += chat_result.reasoning_step_count

        candidate = _extract_tool_result(chat_result.tool_call_events or [], _DRAFT_TOOL)
        if candidate is not None:
            log_timer(
                f"[timer] document_skill {conversation_id} GoodData turn {turns} complete after "
                f"{agent_elapsed:.2f}s; {_DRAFT_TOOL} result received"
            )
            tool_result = candidate
            # Read from the same turn as the draft: the part shows the version that call stored.
            document_part = _extract_document_part(chat_result)
            break
        if _extract_tool_result(chat_result.tool_call_events or [], _LEGACY_DRAFT_TOOL) is not None:
            # A gen-ai on the Report names drafted under the old tool; another reply cannot change that.
            break

        response_text = (chat_result.text_response or "").strip() or render_answer_text(chat_result)
        asked = classify_reply(chat_result, response_text) != "no_action"
        asked_before_draft = asked_before_draft or asked
        if not response_text and not chat_result.tool_call_events:
            break
        if iteration >= max_iterations - 1:
            break
        log_timer(
            f"[timer] document_skill {conversation_id} GoodData turn {turns} complete after "
            f"{agent_elapsed:.2f}s; answering with the expected charts and period"
        )
        current_question = build_simulated_reply(expected_output, asked=asked and not replied)
        replied = replied or asked

    graded_part = document_part
    fill: _EditorFill | None = None
    editor_page_ids = _editor_page_ids(tool_result, document_part)
    # A draft that carries the field has the takeaway contract: the editor writes each empty takeaway,
    # whatever the field lists. Any other draft is graded as before.
    exempt = _saved_empty_takeaways(document_part, user_context) if editor_page_ids is not None else frozenset()
    if (
        takeaways is not None
        and document_part is not None
        and editor_page_ids is not None
        and _has_narrative(expected_output)
    ):
        fill_started = time.monotonic()
        fill = _fill_editor_takeaways(takeaways, document_part, exempt, agent_id)
        fill_elapsed = time.monotonic() - fill_started
        # The takeaway endpoint is gen-ai too: the reader waits for the slowest request before the document is complete.
        timings.agent_s += fill.waited_s
        log_timer(
            f"[timer] document_skill {conversation_id} editor takeaways complete after {fill_elapsed:.2f}s "
            f"({fill.waited_s:.2f}s for the slowest); {len(fill.filled_page_ids)} written"
        )
        graded_part = fill.document_part

    evaluation = evaluate_document_response(
        tool_result,
        graded_part,
        expected_output,
        skill_activated=_skill_activated(all_tool_call_events, _BUILDER_SKILL),
        legacy_names=legacy_wire_names(all_parts, all_tool_call_events),
        exempt_takeaways=exempt,
    )
    if _asked_first_required(expected_output):
        evaluation.applies = replace(evaluation.applies, asked_first=True)
        evaluation.asked_first = asked_before_draft
        if tool_result is not None and not asked_before_draft:
            evaluation.failures.append("the copilot drafted without asking first")
    if fill is not None:
        evaluation.failures.extend(fill.failures)
        if editor_page_ids is not None and fill.readable:
            evaluation.failures.extend(_listed_pages_mismatch(editor_page_ids, fill.generated_page_ids))
        evaluation.fill_error = fill.ungraded_error()
        if fill.error is not None and evaluation.fill_error is None:
            # The run is graded on its other failures; the outage still explains its empty takeaway.
            evaluation.failures.append(f"{fill.error}: the takeaway stays empty")
    if judge is not None and _has_narrative(expected_output) and evaluation.fill_error is None:
        timings.judge_s += _judge_narrative(evaluation, judge, graded_part, question, expected_output["narrative"])

    return DocumentRunResult(
        conversation_id=conversation_id,
        evaluation=evaluation,
        expects_clarification=_expects_clarification(expected_output),
        asked_first=asked_before_draft,
        tool_result=tool_result,
        document_part=document_part,
        total_turns=turns,
        total_steps=steps,
        reasoning_steps=reasoning_steps,
        response_id=response_id,
        tool_call_events=all_tool_call_events,
        reasoning_step_events=all_reasoning_step_events,
        timings=timings,
        run_latency_s=time.monotonic() - run_started,
        takeaways_by_editor=None if fill is None or not fill.generated_page_ids else len(fill.filled_page_ids),
    )


def run_agentic_document_skill(
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
    judge: LLMJudge | None = None,
    user_context: dict | None = None,
    document_format: DocumentFormat | None = None,
) -> AgenticDocumentSummary:
    """Run the document-skill agentic evaluation K times and return a summary.

    The narrative judge is built only for a fixture that states a ``narrative``, so an item
    without one needs neither the llm-judge extra nor ``OPENAI_API_KEY``.

    ``document_format`` is sent on every turn of every run, see ``ChatClient``; None leaves
    the format to the server's ``enablePublisherV2`` feature flag.

    A takeaway the copilot left to the editor is written through the takeaway endpoint before
    the narrative is graded, see ``_execute_single_document_run``.

    Raises:
        ValueError: the fixture is unusable — see ``_validate_expectation``,
            ``_validate_user_context`` and ``_validate_rework_target``, or ``document_format``
            is not a format gen-ai accepts. Raised before any chat request.
        httpx.HTTPError: the takeaway endpoint refused a request for a reason that is not
            transient and not the copilot's, such as a 404 while the takeaway feature flag is off
            or for an agent that does not exist.
    """
    _validate_expectation(expected_output)
    _validate_user_context(user_context)
    _validate_rework_target(expected_output, user_context)
    document_format = normalize_document_format(document_format)
    if judge is None and _has_narrative(expected_output):
        judge = LLMJudge(_NARRATIVE_EVALUATION_STEPS)
    run_results: list[DocumentRunResult] = []
    client = ChatClient(
        host=host,
        token=token,
        workspace_id=workspace_id,
        reasoning_effort=reasoning_effort,
        agent_id=agent_id,
        user_context=user_context,
        document_format=document_format,
    )
    # Opens no connection until the first request, which only a draft listing editor pages makes.
    takeaways = TakeawayClient(host=host, token=token, workspace_id=workspace_id)

    try:
        conv_id_0 = initial_conversation_id if initial_conversation_id is not None else client.create_conversation()
        try:
            run_results.append(
                _execute_single_document_run(
                    client,
                    conv_id_0,
                    question,
                    expected_output,
                    max_iterations,
                    judge,
                    takeaways,
                    user_context,
                    agent_id,
                )
            )
        finally:
            if initial_conversation_id is None:  # only delete conversations we created
                client.delete_conversation(conv_id_0)

        for _ in range(1, k):
            conv_id = client.create_conversation()
            try:
                run_results.append(
                    _execute_single_document_run(
                        client,
                        conv_id,
                        question,
                        expected_output,
                        max_iterations,
                        judge,
                        takeaways,
                        user_context,
                        agent_id,
                    )
                )
            finally:
                client.delete_conversation(conv_id)
    finally:
        client.close()
        takeaways.close()

    # An ungraded run is a fault of that judge or takeaway request, not of the document: it is left out of
    # pass@K, and it keeps pass^K from holding, since "every run passed" was never verified.
    scored = [r for r in run_results if not r.ungraded]
    return AgenticDocumentSummary(
        run_results=run_results,
        pass_at_k=any(r.evaluation.strict_pass for r in scored),
        pass_power_k=len(scored) == len(run_results) and bool(scored) and all(r.evaluation.strict_pass for r in scored),
        best=max(scored or run_results, key=lambda r: sum(r.evaluation.strict_checks.values())),
    )


class DocumentSkillAssertionError(AgenticAssertionError):
    """Raised when a document-skill evaluation fails."""


def evaluate_agentic_document_skill(
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
    dataset_name: str = "document_skill",
    run_timestamp: str | None = None,
    model_version_override: str | None = None,
    run_metadata_extra: dict | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    submit_trace_link: SubmitTraceLink = run_trace_link_inline,
    gate: EvalGate = DEFAULT_GATE,
    judge: LLMJudge | None = None,
    user_context: dict | None = None,
    document_format: DocumentFormat | None = None,
) -> AgenticEvalOutcome:
    """Run document-skill evaluation, log to Langfuse, and raise on failure.

    Returns the best run's outcome on success; on failure the same values are attached to the
    raised ``DocumentSkillAssertionError`` so callers can retrieve them either way.

    ``document_format`` (``aac-v1``/``aac-v2``) asks gen-ai for that document content format
    on every turn and is recorded as ``document_format`` in the dataset-run metadata; None
    leaves it to the server's ``enablePublisherV2`` feature flag.

    Raises:
        DocumentSkillAssertionError: the gate did not pass.
        ValueError: the fixture is unusable, see ``_validate_expectation``,
            ``_validate_user_context`` and ``_validate_rework_target``. Raised before any chat
            request, so it means a fixture to fix rather than a result to read. Also raised, equally before any
            request, when the caller passes a ``document_format`` gen-ai does not accept.
        JudgeResponseError: the fixture states a narrative and the judge returned no readable
            verdict for any run, or the takeaway endpoint failed transiently while writing the
            takeaways the copilot left to the editor -- an item without a result, not K failures.
        httpx.HTTPError: the takeaway endpoint refused a request for a reason that is not
            transient and not the copilot's, such as a 404 while the takeaway feature flag is off
            or for an agent that does not exist.
    """
    document_format = normalize_document_format(document_format)
    if document_format is not None:
        # Metadata only, not part of the run name: it tells runs apart only when their names
        # already differ, so two runs that share a run_timestamp, dataset and model but not the
        # format still collide on one dataset-run name.
        run_metadata_extra = {**(run_metadata_extra or {}), "document_format": document_format}
    identity = RunIdentity(
        host,
        token,
        workspace_id,
        dataset_name,
        run_timestamp,
        model_version_override,
        run_metadata_extra,
        reasoning_effort,
    )
    langfuse, window_start, scope = open_item_trace(langfuse, identity, dataset_item_id, suffix_runs=k > 1)
    with item_scope(scope):
        summary = run_agentic_document_skill(
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
            judge=judge,
            user_context=user_context,
            document_format=document_format,
        )

    if langfuse is not None and dataset_item_id:
        # Pinned on the calling thread: a deferred poll must not widen its query window.
        window_end = utc_now()

        def _write_scores(ctx: RunTraceContext) -> None:
            stamp_gate_metadata(ctx.run_metadata, k=len(summary.run_results), gate=gate)

            for run_idx, run in enumerate(summary.run_results):
                if run.ungraded:
                    # No verdict decided this run: its other scores would publish a pass the gate
                    # never counted.
                    ctx.export_unscored(run_idx, run.conversation_id)
                    continue
                pt = ctx.trace(run.conversation_id)
                strict_checks = run.evaluation.strict_checks
                with ctx.observe(pt, run_idx, conversation_id=run.conversation_id, output=strict_checks) as tid:
                    for score_name, value in strict_checks.items():
                        ctx.score(tid, name=score_name, value=float(value), data_type="BOOLEAN")
                    for name, value in run.diagnostics.items():
                        ctx.score(tid, name=name, value=float(value), data_type="BOOLEAN")
                    if run.summaries_from_data is not None:
                        ctx.score(
                            tid, name="document_summaries_from_data", value=run.summaries_from_data, data_type="NUMERIC"
                        )
                    if run.takeaways_by_editor is not None:
                        ctx.score(
                            tid, name="document_takeaways_by_editor", value=run.takeaways_by_editor, data_type="NUMERIC"
                        )
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
            identity,
            langfuse=langfuse,
            dataset_item_id=dataset_item_id,
            # An ungraded run is read only when it joined: its root still has to be exported.
            conversation_ids=conversations_to_link(
                [r.conversation_id for r in summary.scored_run_results],
                [r.conversation_id for r in summary.run_results if r.ungraded],
            ),
            window_start=window_start,
            window_end=window_end,
            suffix_runs=k > 1,
            write_scores=_write_scores,
            scope=scope,
            item_input=question,
        )

    item_timings = sum_timings([r.timings for r in summary.run_results])
    unscored = summary.unscored_errors
    judge_errors = summary.judge_errors
    request_errors = summary.request_errors
    if not summary.scored_run_results:
        causes = [
            *([f"judge returned no readable verdict for {len(judge_errors)} run(s)"] if judge_errors else []),
            *([f"request failed for {len(request_errors)} run(s)"] if request_errors else []),
        ]
        exc_judge = JudgeResponseError(
            f"no run of {len(summary.run_results)} could be graded: {', '.join(causes)}: " + " | ".join(unscored)
        )
        exc_judge.timings = item_timings
        exc_judge.run_latencies_s = [r.run_latency_s for r in summary.run_results]
        raise exc_judge

    runs_passed = sum(1 for r in summary.run_results if r.evaluation.strict_pass)
    runs_effective = len(summary.run_results)

    best = summary.best

    def _run_detail(run: DocumentRunResult) -> dict[str, Any]:
        """The diagnostic fields for ONE run, shared by the best run and every failing one.

        A closure because the unscored-run summary belongs to the item, not to the run."""
        return {
            **run.evaluation.strict_checks,
            **run.diagnostics,
            "summaries_from_data": run.summaries_from_data,
            **({"takeaways_by_editor": run.takeaways_by_editor} if run.takeaways_by_editor is not None else {}),
            "turns": run.total_turns,
            **({"judge_reasoning": run.evaluation.judge_reasoning} if run.evaluation.applies.narrative else {}),
            "failures": run.evaluation.failures,
            "latency_breakdown": build_latency_breakdown(run.tool_call_events, run.reasoning_step_events),
        }

    detail: dict[str, Any] = {
        **_run_detail(best),
        **({"unscored_runs": len(unscored)} if unscored else {}),
        **({"judge_errors": judge_errors} if judge_errors else {}),
        **({"request_errors": request_errors} if request_errors else {}),
    }
    # Same predicate runs_passed is taken over, so an item's failed_runs and its counts
    # cannot disagree about which runs failed.
    failed_runs = build_failed_runs(summary.run_results, passed=lambda r: r.evaluation.strict_pass, detail=_run_detail)

    if not gate_passed(gate, pass_at_k=summary.pass_at_k, pass_power_k=summary.pass_power_k):
        gate_note = gate_failure_note(gate, runs_passed, runs_effective, len(unscored))
        skill_note = ""
        if not best.evaluation.wire_names_current:
            skill_note = " gen-ai still sends the Report names, so it predates the Document rename."
        elif not best.evaluation.skill_activated:
            skill_note = (
                f" set_skills never activated {_BUILDER_SKILL}: either the copilot routed elsewhere, or the skill"
                " is not registered. It registers only with enableGenAiReportBuilderSkill and the org's"
                " enableBusinessBriefingReportsApp both on."
            )
        exc = DocumentSkillAssertionError(
            f"Document skill assertion failed. {gate_note}{skill_note} "
            f"Checks: {best.evaluation.strict_checks}. "
            f"Failures: {'; '.join(best.evaluation.failures) or 'none reported'}."
        )
        exc.reasoning_steps = best.reasoning_steps
        exc.conversation_id = best.conversation_id
        exc.response_id = best.response_id
        exc.timings = item_timings
        exc.detail = detail
        exc.runs_passed = runs_passed
        exc.runs_effective = runs_effective
        exc.failed_runs = failed_runs
        exc.run_latencies_s = [r.run_latency_s for r in summary.run_results]
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
        run_latencies_s=[r.run_latency_s for r in summary.run_results],
    )

# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic report-skill evaluation runner."""

from __future__ import annotations

import re
import time
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

from gooddata_eval.core.agentic._conversation_context import classify_reply
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
from gooddata_eval.core.agentic.dashboard_skill import _extract_tool_result, _skill_activated
from gooddata_eval.core.chat.render import render_answer_text
from gooddata_eval.core.chat.sse_client import ChatClient
from gooddata_eval.core.config import ReasoningEffort
from gooddata_eval.core.evaluators._llm_judge import JudgeResponseError, LLMJudge, score_run
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
# Same slack as the dashboard skill: the simulated reply is fixed, so the extra rounds only
# absorb a turn that answered without drafting.
_DEFAULT_MAX_ITERATIONS = 4

_DRAFT_TOOL = "draft_report"
_BUILDER_SKILL = "report_builder"
_PART_TYPE = "report"
# The copilot's own rule: a report opens with a cover and has at least one content page.
_COVER_PAGE = "cover"
_CONTENT_PAGE = "content"
_EXPECTATION_KEYS = frozenset({"period", "visualizations", "narrative", "expects_clarification"})
# Template tokens the report renders at export time ({reportName}, {periodStart}, ...).
_PLACEHOLDER_RE = re.compile(r"\{\w+\}")
_SUMMARY_SLOT = "summary"

_NARRATIVE_EVALUATION_STEPS = [
    "The actual output is a report rendered as text: its title, period, and per page the heading, "
    "the chart ids it shows and the written summaries.",
    "Check that the summaries address what the INPUT asked the report to cover, as the EXPECTED OUTPUT describes.",
    "Check that each page's summary fits that page's heading and charts.",
    "Check that the summaries speak to the report's period and do not contradict each other.",
    "Fail the output if any summary is placeholder, unfinished or boilerplate text.",
]


def _extract_report_part(chat_result: ChatResult) -> dict | None:
    """The last ``report`` part of the turn, read back from ``unhandled_parts`` by type.

    The last one, because a turn that drafts and then refines leaves the refined version as
    the one the user sees.
    """
    for part in reversed(chat_result.unhandled_parts):
        if isinstance(part, dict) and part.get("type") == _PART_TYPE:
            return part
    return None


def _nodes(node: Any) -> Iterator[dict]:
    """Every node of a page layout in document order, following ``row`` and ``column`` as gen-ai does."""
    if not isinstance(node, dict):
        return
    yield node
    for direction in ("row", "column"):
        for child in node.get(direction) or []:
            yield from _nodes(child)


def _page_kind(page: dict) -> str:
    """A page's kind; gen-ai reads a page without one as a content page."""
    return str(page.get("kind") or _CONTENT_PAGE)


def _visualizations_of(report: dict) -> set[str]:
    """Every visualization id placed anywhere in the report's page layouts."""
    return {
        node["visualization"]
        for page in report.get("pages") or []
        if isinstance(page, dict)
        for node in _nodes(page.get("layout"))
        if isinstance(node.get("visualization"), str)
    }


def _written(text: Any) -> str | None:
    """``text`` when it says something once template placeholders are removed, else ``None``."""
    if not isinstance(text, str):
        return None
    if not re.sub(r"[\W_]+", "", _PLACEHOLDER_RE.sub("", text)):
        return None
    return text.strip()


def _summary_slot(page: dict) -> dict | None:
    """The page's ``summary`` slot, as gen-ai reads it, or ``None`` when the layout has none."""
    for node in _nodes(page.get("layout")):
        if node.get("id") == _SUMMARY_SLOT and "paragraph" in node:
            return node
    return None


def _summary_text(slot: dict) -> str | None:
    """The slot's written text: the model's on an AI summary, the typed string on a static one."""
    paragraph = slot.get("paragraph")
    return _written(paragraph.get("text") if isinstance(paragraph, dict) else paragraph)


def _content_pages(report: dict) -> list[tuple[int, dict]]:
    """``(page number, page)`` for every content page."""
    return [
        (number, page)
        for number, page in enumerate(report.get("pages") or [], start=1)
        if isinstance(page, dict) and _page_kind(page) == _CONTENT_PAGE
    ]


def render_report_text(report: dict) -> str:
    """The report as the judge reads it: title, period, and per content page its heading, charts and summaries."""
    period = report.get("period") or {}
    lines = [f"Report: {report.get('title')}", f"Period: {period.get('start')} to {period.get('end')}"]
    for number, page in _content_pages(report):
        nodes = list(_nodes(page.get("layout")))
        headings = [h for h in (_written(n.get("heading")) for n in nodes) if h is not None]
        charts = [n["visualization"] for n in nodes if isinstance(n.get("visualization"), str)]
        lines.append("")
        lines.append(f"Page {number}: {', '.join(headings) or '(no heading)'}")
        if charts:
            lines.append(f"Charts: {', '.join(charts)}")
        slot = _summary_slot(page)
        text = _summary_text(slot) if slot is not None else None
        if text is not None:
            lines.append(f"Summary: {text}")
    return "\n".join(lines)


def _has_narrative(expected_output: dict) -> bool:
    return "narrative" in expected_output


def _has_period(expected_output: dict) -> bool:
    return "period" in expected_output


def _has_visualizations(expected_output: dict) -> bool:
    return "visualizations" in expected_output


def _expects_clarification(expected_output: dict) -> bool:
    return "expects_clarification" in expected_output


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
        if not isinstance(period, dict) or not period.get("start") or not period.get("end"):
            raise ValueError(f"period needs both 'start' and 'end', got {period!r}")
    if _has_visualizations(expected_output):
        visualizations = expected_output.get("visualizations")
        if not isinstance(visualizations, list) or not visualizations:
            raise ValueError("visualizations is empty; the chart check would pass vacuously")
        for entry in visualizations:
            if not isinstance(entry, dict) or not entry.get("id"):
                raise ValueError(f"every visualization needs an 'id', got {entry!r}")
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


def build_simulated_reply(expected_output: dict) -> str:
    """The reply the simulated user sends when the copilot asks back instead of drafting.

    Deterministic and LLM-free, built from what the fixture states, so a failure stays the
    copilot's rather than a simulated user that phrased things differently each run.
    """
    segments: list[str] = []
    visualizations = expected_output.get("visualizations") or []
    if visualizations:
        titles = ", ".join(str(v.get("title") or v.get("id")) for v in visualizations)
        segments.append(f"Please use these charts: {titles}.")
    period = expected_output.get("period")
    if isinstance(period, dict):
        segments.append(f"Period: {period.get('start')} to {period.get('end')}.")
    segments.append("Anything else is up to you. Please create the report now.")
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


@dataclass
class ReportEvaluation:
    """Per-run outcome of the report-skill checks; ``strict_checks`` is what the run is scored on."""

    drafted: bool
    part_present: bool
    ref_matches: bool
    pages_consistent: bool
    not_saved: bool
    skill_activated: bool
    applies: _Applies
    period_correct: bool = False
    charts_matched: bool = False
    summaries_present: bool = False
    narrative_judged: bool = False
    judge_reasoning: str = ""
    # Set when the judge returned something unreadable. The run then has no narrative verdict:
    # it is neither published as a 0 nor allowed to pass on the remaining checks.
    judge_error: str | None = None
    failures: list[str] = field(default_factory=list)

    @property
    def strict_pass(self) -> bool:
        return self.judge_error is None and all(self.strict_checks.values())

    @property
    def ungraded(self) -> bool:
        """The judge returned nothing readable and the narrative was the only check still open.

        A run that already failed another check is a failure whatever the judge would have said,
        so a judge error there leaves it failed rather than ungraded.
        """
        return self.judge_error is not None and all(self.strict_checks.values())

    @property
    def strict_checks(self) -> dict[str, bool]:
        # Every name carries the `report_` prefix so a trace can be told apart from other skills'
        # by its score names alone; a name shared with another skill would make that ambiguous.
        checks = {
            "report_drafted": self.drafted,
            "report_part_present": self.part_present,
            "report_ref_matches": self.ref_matches,
            "report_pages_consistent": self.pages_consistent,
            "report_not_saved": self.not_saved,
            "report_skill_activated": self.skill_activated,
        }
        if self.applies.period:
            checks["report_period_correct"] = self.period_correct
        if self.applies.charts:
            checks["report_charts_matched"] = self.charts_matched
        if self.applies.narrative:
            checks["report_summaries_present"] = self.summaries_present
            if self.judge_error is None:
                checks["report_narrative_judged"] = self.narrative_judged
        return checks


def _read_report(report_part: dict | None) -> tuple[dict | None, str | None]:
    """The part's report document, or why it carries no usable one."""
    if report_part is None:
        return None, f"the response carries no {_PART_TYPE!r} part"
    report = report_part.get("report")
    if not isinstance(report, dict):
        return (
            None,
            f"the {_PART_TYPE!r} part carries no report document (report_ref {report_part.get('report_ref')!r})",
        )
    if report.get("type") != _PART_TYPE:
        return None, (
            f"the {_PART_TYPE!r} part carries a document of type {report.get('type')!r}, expected {_PART_TYPE!r}"
        )
    return report, None


def evaluate_report_response(
    tool_result: dict | None,
    report_part: dict | None,
    expected_output: dict,
    *,
    skill_activated: bool,
) -> ReportEvaluation:
    """Score one report response against its expectation.

    Pure: no network and no conversation state, so the whole assertion surface is unit-testable
    without an agent.
    """
    applies = _Applies(
        period=_has_period(expected_output),
        charts=_has_visualizations(expected_output),
        narrative=_has_narrative(expected_output),
    )

    if tool_result is None:
        return ReportEvaluation(
            drafted=False,
            part_present=False,
            ref_matches=False,
            pages_consistent=False,
            not_saved=False,
            skill_activated=skill_activated,
            applies=applies,
            failures=[f"the agent never produced a successful {_DRAFT_TOOL} call"],
        )

    report, part_failure = _read_report(report_part)
    if report is None or report_part is None:
        return ReportEvaluation(
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

    part_ref, tool_ref = report_part.get("report_ref"), tool_result.get("ref")
    ref_matches = isinstance(part_ref, str) and bool(part_ref) and part_ref == tool_ref
    if not ref_matches:
        failures.append(f"the {_PART_TYPE!r} part shows {part_ref!r}, but {_DRAFT_TOOL} returned {tool_ref!r}")

    pages = report.get("pages") or []
    part_count, tool_count = report_part.get("page_count"), tool_result.get("page_count")
    if part_count != len(pages) or tool_count != len(pages):
        failures.append(
            f"the report has {len(pages)} page(s), but the part says {part_count} and {_DRAFT_TOOL} said {tool_count}"
        )
        pages_consistent = False
    else:
        kinds = [_page_kind(page) for page in pages if isinstance(page, dict)]
        if not kinds or kinds[0] != _COVER_PAGE:
            failures.append(f"the report opens with a {kinds[0] if kinds else None!r} page, not a cover")
        if _CONTENT_PAGE not in kinds:
            failures.append("the report has no content page")
        pages_consistent = bool(kinds) and kinds[0] == _COVER_PAGE and _CONTENT_PAGE in kinds

    not_saved = True
    for key, wording in (("saved_report_id", "be saved yet"), ("base_report_id", "edit a saved report")):
        value = report_part.get(key)
        if value is not None:
            failures.append(f"a new draft must not {wording}, but it reports {key} {value!r}")
            not_saved = False

    period_correct = False
    if applies.period:
        expected_period = expected_output["period"]
        actual_period = report.get("period") or {}
        period_correct = all(actual_period.get(key) == expected_period.get(key) for key in ("start", "end"))
        if not period_correct:
            failures.append(
                f"the report covers {actual_period.get('start')} to {actual_period.get('end')}, "
                f"expected {expected_period.get('start')} to {expected_period.get('end')}"
            )

    charts_matched = False
    if applies.charts:
        placed = _visualizations_of(report)
        missing = [v for v in expected_output["visualizations"] if v.get("id") not in placed]
        failures.extend(f"the report does not show chart {v.get('id')!r} ({v.get('title')!r})" for v in missing)
        charts_matched = not missing

    summaries_present = False
    if applies.narrative:
        slots = [(page, slot) for _number, page in _content_pages(report) if (slot := _summary_slot(page)) is not None]
        unwritten = [page for page, slot in slots if _summary_text(slot) is None]
        if not slots:
            failures.append("the report has no summary slot")
        failures.extend(f"page {page.get('id')!r} has a summary slot with no written text" for page in unwritten)
        summaries_present = bool(slots) and not unwritten

    return ReportEvaluation(
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
        failures=failures,
    )


def _judge_narrative(
    evaluation: ReportEvaluation, judge: LLMJudge, report_part: dict | None, question: str, narrative: str
) -> float:
    """Grade the drafted report's narrative into ``evaluation``; return the seconds the judge took.

    No report document means nothing to grade, which is a failed narrative rather than a judge call.
    """
    report = (report_part or {}).get("report") if evaluation.part_present else None
    if not isinstance(report, dict):
        return 0.0
    started = time.monotonic()
    verdict = score_run(judge, input=question, expected_output=narrative, actual_output=render_report_text(report))
    elapsed = time.monotonic() - started
    log_timer(f"[timer] report_skill {judge.model} judge complete after {elapsed:.2f}s")
    if verdict.error is not None:
        evaluation.judge_error = verdict.error
        return elapsed
    evaluation.narrative_judged = verdict.passed
    evaluation.judge_reasoning = verdict.reasoning
    if not verdict.passed:
        evaluation.failures.append(f"the judge failed the narrative: {verdict.reasoning}")
    return elapsed


@dataclass
class ReportRunResult:
    """Outcome of one conversation."""

    conversation_id: str
    evaluation: ReportEvaluation
    expects_clarification: bool = False
    asked_first: bool = False
    tool_result: dict | None = None
    report_part: dict | None = None
    total_turns: int = 0
    total_steps: int = 0
    reasoning_steps: list[str] = field(default_factory=list)
    response_id: str | None = None
    tool_call_events: list[ToolCallEvent] = field(default_factory=list)
    reasoning_step_events: list[ReasoningStepEvent] = field(default_factory=list)
    timings: PhaseTimings = field(default_factory=PhaseTimings)

    @property
    def diagnostics(self) -> dict[str, bool]:
        """Observed but not scored.

        Whether the copilot asked before drafting is recorded only when the fixture says it
        expects a question, and never gates: how much the copilot should ask is a product
        decision, not something a run can get wrong.
        """
        return {"report_asked_first": self.asked_first} if self.expects_clarification else {}

    @property
    def judge_error(self) -> str | None:
        return self.evaluation.judge_error

    @property
    def ungraded(self) -> bool:
        return self.evaluation.ungraded

    @property
    def summaries_from_data(self) -> int | None:
        value = (self.tool_result or {}).get("summaries_from_data")
        return value if isinstance(value, int) else None


@dataclass
class AgenticReportSummary:
    """Aggregated outcome of K runs."""

    run_results: list[ReportRunResult]
    pass_at_k: bool
    pass_power_k: bool
    best: ReportRunResult

    @property
    def scored_run_results(self) -> list[ReportRunResult]:
        """Every run except the ungraded ones: those the narrative verdict alone would have decided."""
        return [r for r in self.run_results if not r.ungraded]

    @property
    def judge_errors(self) -> list[str]:
        return [r.judge_error for r in self.run_results if r.ungraded and r.judge_error is not None]


def _execute_single_report_run(
    client: ChatClient,
    conversation_id: str,
    question: str,
    expected_output: dict,
    max_iterations: int,
    judge: LLMJudge | None = None,
) -> ReportRunResult:
    """Drive one conversation until the copilot drafts a report, then evaluate it.

    Nothing is cleaned up on the way out by design: gen-ai keeps the draft in conversation
    state and persists nothing until a user saves it.
    """
    tool_result: dict | None = None
    report_part: dict | None = None
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
    first_turn_asked = False

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

        candidate = _extract_tool_result(chat_result.tool_call_events or [], _DRAFT_TOOL)
        if candidate is not None:
            log_timer(
                f"[timer] report_skill {conversation_id} GoodData turn {turns} complete after "
                f"{agent_elapsed:.2f}s; {_DRAFT_TOOL} result received"
            )
            tool_result = candidate
            # Read from the same turn as the draft: the part shows the version that call stored.
            report_part = _extract_report_part(chat_result)
            break

        response_text = (chat_result.text_response or "").strip() or render_answer_text(chat_result)
        if iteration == 0:
            first_turn_asked = classify_reply(chat_result, response_text) == "question"
        if not response_text and not chat_result.tool_call_events:
            break
        if iteration >= max_iterations - 1:
            break
        log_timer(
            f"[timer] report_skill {conversation_id} GoodData turn {turns} complete after "
            f"{agent_elapsed:.2f}s; answering with the expected charts and period"
        )
        current_question = build_simulated_reply(expected_output)

    evaluation = evaluate_report_response(
        tool_result,
        report_part,
        expected_output,
        skill_activated=_skill_activated(all_tool_call_events, _BUILDER_SKILL),
    )
    if judge is not None and _has_narrative(expected_output):
        timings.judge_s += _judge_narrative(evaluation, judge, report_part, question, expected_output["narrative"])

    return ReportRunResult(
        conversation_id=conversation_id,
        evaluation=evaluation,
        expects_clarification=_expects_clarification(expected_output),
        asked_first=first_turn_asked,
        tool_result=tool_result,
        report_part=report_part,
        total_turns=turns,
        total_steps=steps,
        reasoning_steps=reasoning_steps,
        response_id=response_id,
        tool_call_events=all_tool_call_events,
        reasoning_step_events=all_reasoning_step_events,
        timings=timings,
    )


def run_agentic_report_skill(
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
) -> AgenticReportSummary:
    """Run the report-skill agentic evaluation K times and return a summary.

    The narrative judge is built only for a fixture that states a ``narrative``, so an item
    without one needs neither the llm-judge extra nor ``OPENAI_API_KEY``.

    Raises:
        ValueError: the fixture is unusable — see ``_validate_expectation``.
    """
    _validate_expectation(expected_output)
    if judge is None and _has_narrative(expected_output):
        judge = LLMJudge(_NARRATIVE_EVALUATION_STEPS)
    run_results: list[ReportRunResult] = []
    client = ChatClient(
        host=host, token=token, workspace_id=workspace_id, reasoning_effort=reasoning_effort, agent_id=agent_id
    )

    try:
        conv_id_0 = initial_conversation_id if initial_conversation_id is not None else client.create_conversation()
        try:
            run_results.append(
                _execute_single_report_run(client, conv_id_0, question, expected_output, max_iterations, judge)
            )
        finally:
            if initial_conversation_id is None:  # only delete conversations we created
                client.delete_conversation(conv_id_0)

        for _ in range(1, k):
            conv_id = client.create_conversation()
            try:
                run_results.append(
                    _execute_single_report_run(client, conv_id, question, expected_output, max_iterations, judge)
                )
            finally:
                client.delete_conversation(conv_id)
    finally:
        client.close()

    # An ungraded run is a fault of that judge request, not of the report: it is left out of
    # pass@K, and it keeps pass^K from holding, since "every run passed" was never verified.
    scored = [r for r in run_results if not r.ungraded]
    return AgenticReportSummary(
        run_results=run_results,
        pass_at_k=any(r.evaluation.strict_pass for r in scored),
        pass_power_k=len(scored) == len(run_results) and bool(scored) and all(r.evaluation.strict_pass for r in scored),
        best=max(scored or run_results, key=lambda r: sum(r.evaluation.strict_checks.values())),
    )


class ReportSkillAssertionError(AgenticAssertionError):
    """Raised when a report-skill evaluation fails."""


def evaluate_agentic_report_skill(
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
    dataset_name: str = "report_skill",
    run_timestamp: str | None = None,
    model_version_override: str | None = None,
    run_metadata_extra: dict | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    submit_trace_link: SubmitTraceLink = run_trace_link_inline,
    gate: EvalGate = DEFAULT_GATE,
    judge: LLMJudge | None = None,
) -> AgenticEvalOutcome:
    """Run report-skill evaluation, log to Langfuse, and raise on failure.

    Returns the best run's outcome on success; on failure the same values are attached to the
    raised ``ReportSkillAssertionError`` so callers can retrieve them either way.

    Raises:
        ReportSkillAssertionError: the gate did not pass.
        ValueError: the fixture is unusable — see ``_validate_expectation``. Raised before any
            request, so it means a fixture to fix rather than a result to read.
        JudgeResponseError: the fixture states a narrative and the judge returned no readable
            verdict for any run -- an item without a result, not K failures.
    """
    langfuse, window_start = open_trace_window(langfuse)
    summary = run_agentic_report_skill(
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
                            tid, name="report_summaries_from_data", value=run.summaries_from_data, data_type="NUMERIC"
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
            conversation_ids=[r.conversation_id for r in summary.scored_run_results],
            window_start=window_start,
            window_end=window_end,
            suffix_runs=len(summary.run_results) > 1,
            write_scores=_write_scores,
            item_input=question,
        )

    item_timings = sum_timings([r.timings for r in summary.run_results])
    unscored = summary.judge_errors
    if not summary.scored_run_results:
        exc_judge = JudgeResponseError(
            f"judge returned no readable verdict for any of the {len(summary.run_results)} run(s): "
            + " | ".join(unscored)
        )
        exc_judge.timings = item_timings
        raise exc_judge

    runs_passed = sum(1 for r in summary.run_results if r.evaluation.strict_pass)
    runs_effective = len(summary.run_results)

    best = summary.best
    detail: dict[str, Any] = {
        **best.evaluation.strict_checks,
        **best.diagnostics,
        "summaries_from_data": best.summaries_from_data,
        "turns": best.total_turns,
        **({"judge_reasoning": best.evaluation.judge_reasoning} if best.evaluation.applies.narrative else {}),
        **({"unscored_runs": len(unscored), "judge_errors": unscored} if unscored else {}),
        "failures": best.evaluation.failures,
        "latency_breakdown": build_latency_breakdown(best.tool_call_events, best.reasoning_step_events),
    }

    if not gate_passed(gate, pass_at_k=summary.pass_at_k, pass_power_k=summary.pass_power_k):
        gate_note = gate_failure_note(gate, runs_passed, runs_effective, len(unscored))
        skill_note = (
            ""
            if best.evaluation.skill_activated
            else (
                f" set_skills never activated {_BUILDER_SKILL}: either the copilot routed elsewhere, or the skill"
                " is not registered. It registers only with enableGenAiReportBuilderSkill and the org's"
                " enableBusinessBriefingReportsApp both on."
            )
        )
        exc = ReportSkillAssertionError(
            f"Report skill assertion failed. {gate_note}{skill_note} "
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

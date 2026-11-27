# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any, cast

import pytest
from gooddata_eval.core.agentic import chat_summary as kind
from gooddata_eval.core.evaluators import chat_summary as cs
from gooddata_eval.core.evaluators._llm_judge import LLMJudge
from gooddata_eval.core.models import AgenticSummaryInput, ChatResult

CHART = """## Summary
Net sales grew in 2024.

## Key Findings
- Audio & Video Accessories led with **$19.5 M**.

## Trends
- Sales rose through the year.

## Areas to Watch
- Furniture declined by **21.9%**."""

DASHBOARD = """## Summary
For **2024**, total sales reached **$67.5 M**.

## Key Insights
- Gross profit fell **0.7%**.

## Areas to Watch
- Orders declined slightly."""

CHART_SCOPE = cs.SummaryScope("widget", kpi_only=False, all_empty=False)
KPI_SCOPE = cs.SummaryScope("widget", kpi_only=True, all_empty=False)
DASHBOARD_SCOPE = cs.SummaryScope("dashboard", kpi_only=False, all_empty=False)


class _Judge:
    """Answers every criterion with the verdict it was built with, and records the criteria it saw."""

    def __init__(self, verdict: bool) -> None:
        self.verdict = verdict
        self.seen: list[tuple[str, str]] = []

    def score(self, input: str, expected_output: str, actual_output: str) -> tuple[bool, str]:
        self.seen.append((input, expected_output))
        return self.verdict, "stub"


def _grade(answer: str, expected: dict[str, Any], scope: cs.SummaryScope | None, tools: list[str] | None = None):
    positive, violation = _Judge(True), _Judge(False)
    return cs.evaluate_turn(
        judge_input="[widget] 2. Sales",
        answer=answer,
        tool_names=tools or [],
        expected=expected,
        scope=scope,
        positive_judge=cast(LLMJudge, positive),
        violation_judge=cast(LLMJudge, violation),
    )


def test_a_chart_summary_needs_the_four_headings_in_order() -> None:
    assert _grade(CHART, {}, CHART_SCOPE).passed
    swapped = (
        CHART.replace("## Trends", "## Tmp")
        .replace("## Key Findings", "## Trends")
        .replace("## Tmp", "## Key Findings")
    )
    result = _grade(swapped, {}, CHART_SCOPE)
    assert not result.passed
    assert "expected ['Summary', 'Key Findings', 'Trends', 'Areas to Watch']" in result.detail["shape_problem"]


def test_a_dashboard_summary_needs_its_three_headings() -> None:
    assert _grade(DASHBOARD, {}, DASHBOARD_SCOPE).passed
    assert not _grade(CHART, {}, DASHBOARD_SCOPE).passed


def test_a_kpi_summary_has_no_headings_and_few_sentences() -> None:
    kpi = "For **2024**, Total Sales was **$67.5 M**, up **0.27%** from the previous period."
    assert _grade(kpi, {}, KPI_SCOPE).passed
    assert not _grade(DASHBOARD, {}, KPI_SCOPE).passed
    long_kpi = " ".join(["Sales grew."] * 4)
    assert "4 sentences on a KPI" in _grade(long_kpi, {}, KPI_SCOPE).detail["shape_problem"]


def test_a_dashboard_without_data_has_no_headings_and_no_figures() -> None:
    empty = cs.SummaryScope("dashboard", kpi_only=False, all_empty=True)
    no_data = "No data is available for the current dashboard filters. Please check the filter configuration."
    assert _grade(no_data, {}, empty).passed
    with_figures = "No data for 2020, but last year sales were $1.9 M and grew 12%."
    result = _grade(with_figures, {}, empty)
    assert not result.passed
    assert result.detail["figures_on_no_data"] == ["$1.9 M", "12%"]


def test_an_empty_widget_has_no_fixed_shape() -> None:
    empty = cs.SummaryScope("widget", kpi_only=False, all_empty=True)
    assert _grade("## Summary\n- The visualization returned no data for January 1–December 31, 2020.", {}, empty).passed


def test_a_users_own_format_replaces_the_default_shape() -> None:
    brief = {"format": {"max_sentences": 3, "no_headings": True, "no_bullets": True}}
    three = "Tracy Carter leads at $1.3 M. The top three are close. The tenth is at $985.3 K."
    assert _grade(three, brief, CHART_SCOPE).passed
    assert "headings" in _grade(CHART, brief, CHART_SCOPE).detail["shape_problem"]
    four = three + " Spending is concentrated."
    assert "4 sentences" in _grade(four, brief, CHART_SCOPE).detail["shape_problem"]
    assert _grade(CHART, {"format": False}, CHART_SCOPE).detail.get("shape_ok") is None
    titled = "Tracy Carter leads at $1.3 M. Mrs. Crystal Murray is third. The tenth is at $985.3 K."
    assert _grade(titled, brief, CHART_SCOPE).passed


@pytest.mark.parametrize(
    "leak",
    ["See {visualization/top_10_spenders} for details.", "Widget 0f1e2d3c-4b5a-6978-8a9b-0c1d2e3f4a5b is empty."],
)
def test_ids_never_reach_the_answer(leak: str) -> None:
    result = _grade(f"{CHART}\n{leak}", {}, CHART_SCOPE)
    assert not result.passed
    assert result.detail["no_ids"] is False


def test_a_follow_up_without_tool_calls_has_no_default_shape() -> None:
    answer = "Tracy Carter leads, about $15.7 K ahead of the second place."
    assert _grade(answer, {"no_tool_calls": True}, None, tools=["set_skills"]).passed
    # a follow-up may link objects: the UI renders its reference tags
    assert _grade("Driven by {metric/active_customers}.", {}, None).detail.get("no_ids") is None
    ran = _grade(answer, {"no_tool_calls": True}, None, tools=["execute_existing_visualizations"])
    assert not ran.passed
    assert ran.detail["tools_run"] == ["execute_existing_visualizations"]


def test_judge_criteria_gate_the_verdict() -> None:
    result = _grade(CHART, {"must_include": ["names the period"], "must_not_include": ["invents a cause"]}, CHART_SCOPE)
    assert result.passed
    assert result.detail["must_include_0"] is True
    assert result.detail["must_not_include_0"] is True


def _turn(answer: str, tools: list[str]) -> kind.SummaryTurn:
    result = ChatResult.model_validate(
        {
            "textResponse": answer,
            "toolCallEvents": [{"functionName": t, "functionArguments": "{}"} for t in tools],
        }
    )
    return kind.SummaryTurn("q", result=result)


def test_each_turn_is_graded_with_its_own_expectation(monkeypatch: pytest.MonkeyPatch) -> None:
    # no figures: this run's turns carry tool names only, so there is no table to ground a figure on
    summary = "## Summary\nSales grew.\n\n## Key Findings\n- Clothing leads.\n\n## Trends\n- Up.\n\n## Areas to Watch\n- None."
    judges = (_Judge(True), _Judge(False))
    monkeypatch.setattr(kind, "make_judges", lambda model=None: judges)
    run = kind.SummaryConversation(
        "c",
        turns=[_turn(summary, ["execute_existing_visualizations"]), _turn("Tracy Carter leads.", [])],
        scope=CHART_SCOPE,
    )
    passed = kind.grade_conversation(
        run,
        scenario="[widget] Top 10 Spenders",
        expected_outputs=[
            {"must_include": ["summary criterion"]},
            {"no_tool_calls": True, "must_include": ["follow-up"]},
        ],
    )
    assert passed
    assert [e.passed for e in run.evaluations] == [True, True]
    assert [c for _, c in judges[0].seen] == ["summary criterion", "follow-up"]
    # the follow-up's judge reads the summary it follows; the summary turn reads no history
    summary_input, follow_up_input = (i for i, _ in judges[0].seen)
    assert "Conversation before" not in summary_input
    assert f"USER: q\nASSISTANT: {summary}\nQuestion of this turn: q" in follow_up_input
    # the follow-up keeps no default shape: only the summary turn is shape-checked
    assert "shape_ok" not in run.evaluations[1].detail
    # the run detail is flat: the summary turn at the top, follow-ups prefixed
    detail = kind._run_detail(run)
    assert detail["actual_output"] == summary
    assert detail["must_include_0"] is True
    assert detail["followup_1_actual_output"] == "Tracy Carter leads."
    assert detail["followup_1_no_tool_calls"] is True
    assert "followup_1_shape_ok" not in detail


def test_the_scope_reads_kpis_and_empty_results_from_the_referenced_widgets() -> None:
    kpi_afm = {"attributes": [], "measures": [{"localIdentifier": "m"}], "filters": []}
    chart_afm = {"attributes": [{"localIdentifier": "a"}], "measures": [{"localIdentifier": "m"}], "filters": []}
    inp = AgenticSummaryInput.model_validate(
        {"scope": "widget", "executions": {"k": {"afm": kpi_afm}, "c": {"afm": chart_afm}}}
    )
    context = {"referencedObjects": [{"objects": [{"type": "WIDGET", "id": "k"}]}]}
    assert kind.summary_scope(inp, context, with_data={"k"}) == cs.SummaryScope("widget", True, False)
    assert kind.summary_scope(inp, context, with_data={"c"}).all_empty
    # a chart of measures only (donut, waterfall) puts the measures on a second dimension: not a KPI
    breakdown = {
        "afm": {"attributes": [], "measures": [{"localIdentifier": "m"}, {"localIdentifier": "n"}], "filters": []},
        "result_spec": {"dimensions": [{"itemIdentifiers": []}, {"itemIdentifiers": ["measureGroup"]}]},
    }
    headline = {"afm": kpi_afm, "result_spec": {"dimensions": [{"itemIdentifiers": ["measureGroup"]}]}}
    shapes = AgenticSummaryInput.model_validate({"scope": "widget", "executions": {"k": headline, "b": breakdown}})
    assert kind.summary_scope(shapes, context, with_data={"k"}).kpi_only
    donut = {"referencedObjects": [{"objects": [{"type": "WIDGET", "id": "b"}]}]}
    assert not kind.summary_scope(shapes, donut, with_data={"b"}).kpi_only
    dashboard = inp.model_copy(update={"scope": "dashboard"})
    assert kind.summary_scope(dashboard, {}, with_data={"c"}) == cs.SummaryScope("dashboard", False, False)


@pytest.mark.parametrize("tools", [["set_skills"], ["set_skills", "search_objects"]])
def test_figures_on_a_summary_turn_that_read_no_data_fail(tools: list[str]) -> None:
    """A workspace search is a tool call and reads no table: its turn has nothing a figure could come from."""
    result = cs.evaluate_turn(
        judge_input="[widget] 2. Sales",
        answer=CHART,
        tool_names=tools,
        expected={},
        scope=CHART_SCOPE,
        positive_judge=cast(LLMJudge, _Judge(True)),
        violation_judge=cast(LLMJudge, _Judge(False)),
        tables=[],
    )
    assert not result.passed
    assert "read no data" in result.detail["figures_grounded_reason"]


def test_the_no_data_check_reads_figures_as_the_grounding_check_does() -> None:
    empty = cs.SummaryScope("dashboard", kpi_only=False, all_empty=True)
    # a plain count and a scale word: figures for `figures_grounded`, so figures here too
    for text in ("No data, although 345 orders were placed.", "No data for 2020, earlier sales were 1.3 million."):
        assert not _grade(text, {}, empty).passed, text
    assert _grade("No data is available for 2020 or 2021.", {}, empty).passed


def test_a_heading_and_an_abbreviation_are_no_sentences() -> None:
    assert cs.count_sentences("## Summary\nNet sales are **$1.2 M** vs. last year. Mrs. Crystal Murray leads.") == 2


@pytest.mark.parametrize(
    ("expected", "message"),
    [
        ({"format": {"no_heading": True}}, "unknown `format` keys \\['no_heading'\\]"),
        ({"format": {}}, "`format` must be false or a non-empty object"),
        ({"format": True}, "`format` must be false or a non-empty object"),
        ({"must_includes": ["x"]}, "unknown expected_output keys \\['must_includes'\\]"),
        (["x"], "expected_output must be an object"),
    ],
)
def test_an_unknown_expectation_key_is_rejected(expected: Any, message: str) -> None:
    with pytest.raises(ValueError, match=f"follow-up 2: {message}"):
        cs.validate_expected(expected, "follow-up 2")


@pytest.mark.parametrize(
    "expected",
    [
        None,
        {},
        {"format": False},
        {"format": {"max_sentences": 3, "no_headings": True, "no_bullets": True}},
        {
            "no_tool_calls": True,
            "must_include": ["x"],
            "must_not_include": ["y"],
            "rubric": ["z"],
            "format": {"headings": []},
        },
    ],
)
def test_every_known_expectation_key_is_accepted(expected: Any) -> None:
    cs.validate_expected(expected, "item")

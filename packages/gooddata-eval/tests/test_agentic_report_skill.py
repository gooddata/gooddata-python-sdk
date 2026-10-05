# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
import json
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

import pytest
from gooddata_eval.cli.agentic_runner import _dispatch_agentic
from gooddata_eval.core.agentic import report_skill
from gooddata_eval.core.agentic.report_skill import (
    ReportEvaluation,
    ReportSkillAssertionError,
    _execute_single_report_run,
    _validate_expectation,
    _visualizations_of,
    build_simulated_reply,
    evaluate_agentic_report_skill,
    evaluate_report_response,
    run_agentic_report_skill,
)
from gooddata_eval.core.evaluators._llm_judge import JudgeResponseError
from gooddata_eval.core.models import ChatResult, DatasetItem

# Shapes follow what gen-ai writes for a drafted report (composed_report.aac.json): a cover
# page, then content pages whose layout nests `column` and `row` entries down to the slots.
_REVENUE_TREND = "revenue_trend"
_RETURNS_BY_CATEGORY = "returns_by_category"
_PERIOD = {"start": "2026-01-01", "end": "2026-06-30"}


def _cover_page() -> dict:
    return {
        "id": "page1",
        "kind": "cover",
        "format": "widescreen",
        "layout": {"column": [{"id": "coverTitle", "weight": 2, "heading": "{reportName}", "style": "h1"}]},
    }


def _content_page(page_id: str, *visualizations: str) -> dict:
    return {
        "id": page_id,
        "kind": "content",
        "format": "widescreen",
        "layout": {
            "column": [
                {"id": "pageTitle", "weight": 2, "heading": "Revenue", "style": "h1"},
                {
                    "weight": 9,
                    "row": [
                        {"weight": 2, "row": [{"id": f"widget{i}", "visualization": v, "date": "date"}]}
                        for i, v in enumerate(visualizations, start=1)
                    ],
                },
            ]
        },
    }


def _report_part(
    pages: list[dict] | None = None,
    *,
    ref: str = "report_1",
    page_count: int | None = None,
    period: dict | None = None,
    saved_report_id: str | None = None,
    base_report_id: str | None = None,
    report: dict | None | str = "default",
) -> dict:
    pages = pages if pages is not None else [_cover_page(), _content_page("page2", _REVENUE_TREND)]
    document = (
        {
            "id": "sales_overview",
            "type": "report",
            "title": "Sales overview",
            "period": period if period is not None else _PERIOD,
            "pages": pages,
        }
        if report == "default"
        else report
    )
    return {
        "type": "report",
        "report_ref": ref,
        "format": "aac-v1",
        "report": document,
        "page_count": len(pages) if page_count is None else page_count,
        "base_report_id": base_report_id,
        "saved_report_id": saved_report_id,
    }


def _draft_result(*, ref: str = "report_1", page_count: int = 2, summaries_from_data: int = 1) -> dict:
    return {
        "status": "success",
        "ref": ref,
        "page_count": page_count,
        "page_ids": [f"page{i}" for i in range(1, page_count + 1)],
        "pages_kept": 0,
        "visualization_count": 1,
        "summaries_from_data": summaries_from_data,
        "summaries_stale": 0,
        "layouts_used": ["auto"] * page_count,
    }


def _tool_call(name: str, result: dict | None = None) -> dict:
    return {"functionName": name, "functionArguments": "{}", "result": None if result is None else json.dumps(result)}


def _set_skills(*skills: str) -> dict:
    return _tool_call("set_skills", {"skills_to_activate": list(skills)})


def _chat_result(
    *, tool_calls: list[dict] | None = None, parts: list[dict] | None = None, text: str = ""
) -> ChatResult:
    return ChatResult.model_validate(
        {
            "textResponse": text,
            "toolCallEvents": tool_calls or [],
            "unhandledParts": parts or [],
            "streamEnded": True,
        }
    )


def _drafting_turn(**part_kwargs: Any) -> ChatResult:
    return _chat_result(
        tool_calls=[_set_skills("report_builder"), _tool_call("draft_report", _draft_result())],
        parts=[{"type": "text", "text": "I've put together a report with 2 slides."}, _report_part(**part_kwargs)],
        text="I've put together a report with 2 slides.",
    )


class _ScriptedChatClient:
    """Stands in for ChatClient: answers each message with the next scripted turn."""

    def __init__(self, turns: list[ChatResult]) -> None:
        self._turns = list(turns)
        self.sent: list[str] = []
        self.created: list[str] = []
        self.deleted: list[str] = []
        self.closed = False

    def create_conversation(self) -> str:
        conversation_id = f"conv-{len(self.created) + 1}"
        self.created.append(conversation_id)
        return conversation_id

    def send_message(self, conversation_id: str, question: str) -> ChatResult:
        self.sent.append(question)
        return self._turns.pop(0) if self._turns else _chat_result()

    def delete_conversation(self, conversation_id: str) -> None:
        self.deleted.append(conversation_id)

    def close(self) -> None:
        self.closed = True


def _install_client(monkeypatch: pytest.MonkeyPatch, client: _ScriptedChatClient) -> None:
    monkeypatch.setattr(report_skill, "ChatClient", lambda **_kwargs: client)


# ── scoring ─────────────────────────────────────────────────────────────────


def _evaluate(
    part: dict | None, *, expected: dict | None = None, tool: dict | None = None, skill: bool = True
) -> ReportEvaluation:
    return evaluate_report_response(
        _draft_result() if tool is None else tool,
        part,
        {} if expected is None else expected,
        skill_activated=skill,
    )


def test_a_drafted_report_returned_in_the_chat_item_passes() -> None:
    evaluation = _evaluate(_report_part())
    assert evaluation.strict_checks == {
        "report_drafted": True,
        "report_part_present": True,
        "report_ref_matches": True,
        "report_pages_consistent": True,
        "report_not_saved": True,
        "report_skill_activated": True,
    }
    assert evaluation.strict_pass
    assert evaluation.failures == []


def test_period_and_charts_are_scored_only_when_the_fixture_states_them() -> None:
    expected = {"period": _PERIOD, "visualizations": [{"id": _REVENUE_TREND, "title": "Revenue trend"}]}
    checks = _evaluate(_report_part(), expected=expected).strict_checks
    assert checks["report_period_correct"] is True
    assert checks["report_charts_matched"] is True


def test_no_successful_draft_fails_every_check_and_says_so() -> None:
    evaluation = evaluate_report_response(None, None, {"period": _PERIOD}, skill_activated=True)
    assert evaluation.strict_checks["report_drafted"] is False
    assert evaluation.strict_checks["report_part_present"] is False
    assert evaluation.strict_checks["report_period_correct"] is False
    assert not evaluation.strict_pass
    assert evaluation.failures == ["the agent never produced a successful draft_report call"]


def test_a_draft_without_a_report_part_fails() -> None:
    evaluation = _evaluate(None)
    assert evaluation.strict_checks["report_drafted"] is True
    assert evaluation.strict_checks["report_part_present"] is False
    assert evaluation.failures == ["the response carries no 'report' part"]


def test_a_report_part_whose_document_did_not_resolve_fails() -> None:
    evaluation = _evaluate(_report_part(report=None))
    assert evaluation.strict_checks["report_part_present"] is False
    assert evaluation.failures == ["the 'report' part carries no report document (report_ref 'report_1')"]


def test_a_document_that_is_not_a_report_fails() -> None:
    evaluation = _evaluate(_report_part(report={"id": "x", "type": "dashboard", "pages": []}))
    assert evaluation.strict_checks["report_part_present"] is False
    assert evaluation.failures == ["the 'report' part carries a document of type 'dashboard', expected 'report'"]


def test_a_part_pointing_at_another_draft_fails() -> None:
    evaluation = _evaluate(_report_part(ref="report_2"))
    assert evaluation.strict_checks["report_ref_matches"] is False
    assert evaluation.failures == ["the 'report' part shows 'report_2', but draft_report returned 'report_1'"]


def test_a_page_count_that_disagrees_with_the_pages_fails() -> None:
    evaluation = _evaluate(_report_part(page_count=3))
    assert evaluation.strict_checks["report_pages_consistent"] is False
    assert evaluation.failures == ["the report has 2 page(s), but the part says 3 and draft_report said 2"]


def test_a_cover_alone_is_not_a_report() -> None:
    evaluation = _evaluate(_report_part([_cover_page()]), tool=_draft_result(page_count=1))
    assert evaluation.strict_checks["report_pages_consistent"] is False
    assert evaluation.failures == ["the report has no content page"]


def test_a_new_draft_must_not_already_be_saved() -> None:
    evaluation = _evaluate(_report_part(saved_report_id="sales_overview"))
    assert evaluation.strict_checks["report_not_saved"] is False
    assert evaluation.failures == ["a new draft must not be saved yet, but it reports saved_report_id 'sales_overview'"]


def test_a_new_draft_must_not_edit_a_saved_report() -> None:
    evaluation = _evaluate(_report_part(base_report_id="q3_review"))
    assert evaluation.strict_checks["report_not_saved"] is False
    assert evaluation.failures == [
        "a new draft must not edit a saved report, but it reports base_report_id 'q3_review'"
    ]


def test_a_wrong_period_fails() -> None:
    evaluation = _evaluate(
        _report_part(period={"start": "2025-07-01", "end": "2025-12-31"}), expected={"period": _PERIOD}
    )
    assert evaluation.strict_checks["report_period_correct"] is False
    assert evaluation.failures == [
        "the report covers 2025-07-01 to 2025-12-31, expected 2026-01-01 to 2026-06-30",
    ]


def test_a_missing_chart_fails_and_is_named() -> None:
    expected = {"visualizations": [{"id": _RETURNS_BY_CATEGORY, "title": "Returns by category"}]}
    evaluation = _evaluate(_report_part(), expected=expected)
    assert evaluation.strict_checks["report_charts_matched"] is False
    assert evaluation.failures == ["the report does not show chart 'returns_by_category' ('Returns by category')"]


def test_a_routing_miss_fails_the_skill_check_alone() -> None:
    evaluation = _evaluate(_report_part(), skill=False)
    assert evaluation.strict_checks["report_skill_activated"] is False
    assert [name for name, ok in evaluation.strict_checks.items() if not ok] == ["report_skill_activated"]


def test_visualizations_are_found_however_deep_the_layout_nests_them() -> None:
    page = _content_page("page2", _REVENUE_TREND, _RETURNS_BY_CATEGORY)
    assert _visualizations_of({"pages": [_cover_page(), page]}) == {_REVENUE_TREND, _RETURNS_BY_CATEGORY}


# ── fixture validation ──────────────────────────────────────────────────────


@pytest.mark.parametrize(
    ("expected", "message"),
    [
        ({"period": {"start": "2026-01-01"}}, "period needs both 'start' and 'end'"),
        ({"period": "H1 2026"}, "period needs both 'start' and 'end'"),
        ({"visualizations": []}, "visualizations is empty"),
        ({"visualizations": [{"title": "Revenue"}]}, "every visualization needs an 'id'"),
        ({"expects_clarification": "yes"}, "expects_clarification must be true or false"),
    ],
)
def test_an_unusable_fixture_is_rejected_before_any_request(expected: dict, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        _validate_expectation(expected)


def test_an_empty_fixture_is_usable() -> None:
    _validate_expectation({})


# ── simulated user ──────────────────────────────────────────────────────────


def test_the_simulated_reply_names_the_charts_and_the_period() -> None:
    expected = {
        "period": _PERIOD,
        "visualizations": [
            {"id": _REVENUE_TREND, "title": "Revenue trend"},
            {"id": _RETURNS_BY_CATEGORY, "title": "Returns by category"},
        ],
    }
    assert build_simulated_reply(expected) == (
        "Please use these charts: Revenue trend, Returns by category. "
        "Period: 2026-01-01 to 2026-06-30. "
        "Anything else is up to you. Please create the report now."
    )


def test_the_simulated_reply_leaves_out_what_the_fixture_does_not_state() -> None:
    assert build_simulated_reply({}) == "Anything else is up to you. Please create the report now."


# ── conversation loop ───────────────────────────────────────────────────────


def test_a_report_drafted_on_the_first_turn_ends_the_run() -> None:
    client = _ScriptedChatClient([_drafting_turn()])
    run = _execute_single_report_run(client, "conv-1", "Create a sales report for H1 2026", {}, max_iterations=4)
    assert client.sent == ["Create a sales report for H1 2026"]
    assert run.total_turns == 1
    assert run.asked_first is False
    assert run.evaluation.strict_pass


def test_a_clarifying_question_is_answered_and_the_report_scored() -> None:
    expected = {"period": _PERIOD, "visualizations": [{"id": _REVENUE_TREND, "title": "Revenue trend"}]}
    question = _chat_result(text="Which period should the report cover?")
    client = _ScriptedChatClient([question, _drafting_turn()])
    run = _execute_single_report_run(client, "conv-1", "Make me a report", expected, max_iterations=4)
    assert client.sent == ["Make me a report", build_simulated_reply(expected)]
    assert run.total_turns == 2
    assert run.asked_first is True
    assert run.evaluation.strict_pass


def test_a_silent_turn_ends_the_run_without_replying() -> None:
    client = _ScriptedChatClient([_chat_result()])
    run = _execute_single_report_run(client, "conv-1", "Make me a report", {}, max_iterations=4)
    assert client.sent == ["Make me a report"]
    assert not run.evaluation.strict_pass


def test_a_copilot_that_never_drafts_stops_at_the_turn_limit() -> None:
    client = _ScriptedChatClient([_chat_result(text="Which period?")] * 5)
    run = _execute_single_report_run(client, "conv-1", "Make me a report", {}, max_iterations=3)
    assert len(client.sent) == 3
    assert run.evaluation.strict_checks["report_drafted"] is False


def test_asking_first_is_recorded_only_when_the_fixture_expects_it() -> None:
    plain = _execute_single_report_run(_ScriptedChatClient([_drafting_turn()]), "c", "q", {}, max_iterations=4)
    assert "report_asked_first" not in plain.diagnostics

    expected = {"expects_clarification": True}
    run = _execute_single_report_run(_ScriptedChatClient([_drafting_turn()]), "c", "q", expected, max_iterations=4)
    assert run.diagnostics == {"report_asked_first": False}
    assert run.evaluation.strict_pass, "drafting without asking is recorded, never failed"


# ── K runs and the gate ─────────────────────────────────────────────────────


def test_every_conversation_the_run_creates_is_deleted(monkeypatch: pytest.MonkeyPatch) -> None:
    client = _ScriptedChatClient([_drafting_turn(), _drafting_turn()])
    _install_client(monkeypatch, client)
    summary = run_agentic_report_skill("https://h", "tok", "ws", "Create a report", {}, k=2)
    assert summary.pass_at_k and summary.pass_power_k
    assert client.deleted == client.created == ["conv-1", "conv-2"]
    assert client.closed


def test_a_conversation_handed_in_is_not_deleted(monkeypatch: pytest.MonkeyPatch) -> None:
    client = _ScriptedChatClient([_drafting_turn()])
    _install_client(monkeypatch, client)
    run_agentic_report_skill("https://h", "tok", "ws", "Create a report", {}, initial_conversation_id="theirs")
    assert client.deleted == []


def test_a_passing_item_returns_its_checks_and_draft_facts(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_client(monkeypatch, _ScriptedChatClient([_drafting_turn()]))
    outcome = evaluate_agentic_report_skill("https://h", "tok", "ws", "Create a report", {"period": _PERIOD})
    assert outcome.runs_passed == 1
    assert outcome.detail["report_period_correct"] is True
    assert outcome.detail["summaries_from_data"] == 1
    assert outcome.detail["failures"] == []


def test_a_failing_item_raises_with_the_failures(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_client(monkeypatch, _ScriptedChatClient([_chat_result(text="I can't do that.")]))
    with pytest.raises(ReportSkillAssertionError) as raised:
        evaluate_agentic_report_skill("https://h", "tok", "ws", "Create a report", {}, max_iterations=1)
    assert "the agent never produced a successful draft_report call" in str(raised.value)
    assert raised.value.runs_passed == 0
    assert raised.value.conversation_id == "conv-1"


def test_a_failing_item_without_report_builder_points_at_the_flags(monkeypatch: pytest.MonkeyPatch) -> None:
    turn = _chat_result(tool_calls=[_set_skills("visualization")], text="Here is a chart.")
    _install_client(monkeypatch, _ScriptedChatClient([turn]))
    with pytest.raises(
        ReportSkillAssertionError, match="enableGenAiReportBuilderSkill and the org.s enableBusinessBriefingReportsApp"
    ):
        evaluate_agentic_report_skill("https://h", "tok", "ws", "Create a report", {}, max_iterations=1)


def test_an_unusable_fixture_fails_before_any_request(monkeypatch: pytest.MonkeyPatch) -> None:
    client = _ScriptedChatClient([])
    _install_client(monkeypatch, client)
    with pytest.raises(ValueError):
        evaluate_agentic_report_skill("https://h", "tok", "ws", "Create a report", {"visualizations": []})
    assert client.created == []


def test_a_ref_missing_on_both_sides_does_not_match() -> None:
    evaluation = _evaluate(_report_part(ref=None), tool={**_draft_result(), "ref": None})
    assert evaluation.strict_checks["report_ref_matches"] is False


def test_the_last_successful_draft_of_a_turn_is_the_one_scored() -> None:
    turn = _chat_result(
        tool_calls=[
            _tool_call("draft_report", _draft_result(ref="report_1")),
            _tool_call("draft_report", {"status": "error", "message": "no layout fits 7 charts"}),
            _tool_call("draft_report", _draft_result(ref="report_2")),
        ],
        parts=[_report_part(ref="report_2")],
        text="I've put together a report with 2 slides.",
    )
    run = _execute_single_report_run(_ScriptedChatClient([turn]), "c", "q", {}, max_iterations=4)
    assert run.tool_result is not None and run.tool_result["ref"] == "report_2"
    assert run.evaluation.strict_pass


def test_a_first_turn_that_did_not_ask_is_not_recorded_as_asking() -> None:
    refusal = _chat_result(text="I could not find any charts on that topic.")
    expected = {"expects_clarification": True}
    run = _execute_single_report_run(_ScriptedChatClient([refusal, _drafting_turn()]), "c", "q", expected, 4)
    assert run.evaluation.strict_pass
    assert run.diagnostics == {"report_asked_first": False}


def test_a_structured_clarifying_question_counts_as_asking() -> None:
    question = _chat_result(parts=[{"type": "clarifyingQuestions", "questions": []}])
    expected = {"expects_clarification": True}
    run = _execute_single_report_run(_ScriptedChatClient([question, _drafting_turn()]), "c", "q", expected, 4)
    assert run.diagnostics == {"report_asked_first": True}


# ── page kinds, fixture keys, asking, two drafts in one turn ───────────────


def _page(page_id: str, kind: str | None) -> dict:
    page = _content_page(page_id, _REVENUE_TREND)
    if kind is None:
        del page["kind"]
    else:
        page["kind"] = kind
    return page


def test_a_report_that_does_not_open_with_a_cover_fails() -> None:
    evaluation = _evaluate(_report_part([_page("page1", "content"), _page("page2", "content")]))
    assert evaluation.strict_checks["report_pages_consistent"] is False
    assert evaluation.failures == ["the report opens with a 'content' page, not a cover"]


def test_a_report_without_a_content_page_fails() -> None:
    evaluation = _evaluate(_report_part([_cover_page(), _page("page2", "section")]))
    assert evaluation.strict_checks["report_pages_consistent"] is False
    assert evaluation.failures == ["the report has no content page"]


def test_a_page_without_a_kind_is_a_content_page() -> None:
    assert _evaluate(_report_part([_cover_page(), _page("page2", None)])).strict_pass


@pytest.mark.parametrize("key", ["visualisations", "date_range", "narative"])
def test_an_unknown_fixture_key_is_rejected(key: str) -> None:
    with pytest.raises(ValueError, match=f"unknown expected_output key.*{key}"):
        _validate_expectation({key: "x"})


def test_an_expected_output_that_is_not_an_object_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    client = _ScriptedChatClient([])
    _install_client(monkeypatch, client)
    item = DatasetItem(
        id="i", dataset_name="ds", test_kind="agentic_report_skill", question="q", expected_output="a report"
    )
    with pytest.raises(ValueError, match="expected_output must be an object"):
        _dispatch_agentic(
            item,
            host="https://h",
            token="t",
            workspace_id="ws",
            k=1,
            langfuse=None,
            run_ts="r",
            model_version_override=None,
        )
    assert client.created == []


def test_a_copilot_that_only_ever_asks_is_recorded_as_asking() -> None:
    client = _ScriptedChatClient([_chat_result(text="Which period?")] * 3)
    run = _execute_single_report_run(client, "c", "q", {"expects_clarification": True}, max_iterations=2)
    assert run.evaluation.strict_checks["report_drafted"] is False
    assert run.diagnostics == {"report_asked_first": True}


def test_asking_first_is_recorded_whenever_the_fixture_states_the_key() -> None:
    run = _execute_single_report_run(
        _ScriptedChatClient([_drafting_turn()]), "c", "q", {"expects_clarification": False}, max_iterations=4
    )
    assert run.diagnostics == {"report_asked_first": False}


def test_the_last_report_part_of_a_turn_is_the_one_scored() -> None:
    turn = _chat_result(
        tool_calls=[
            _tool_call("draft_report", _draft_result(ref="report_1")),
            _tool_call("draft_report", _draft_result(ref="report_2")),
        ],
        parts=[_report_part(ref="report_1"), _report_part(ref="report_2")],
    )
    run = _execute_single_report_run(_ScriptedChatClient([turn]), "c", "q", {}, max_iterations=4)
    assert run.report_part is not None and run.report_part["report_ref"] == "report_2"
    assert run.evaluation.strict_pass


# ── Langfuse scores ─────────────────────────────────────────────────────────


class _FakeCtx:
    """Records what the deferred Langfuse block writes, without a Langfuse."""

    def __init__(self) -> None:
        self.run_metadata: dict[str, Any] = {}
        self.scores: dict[str, float] = {}
        self.score_types: dict[str, str] = {}
        self.quality_checks: dict[str, bool] = {}
        self.observed: list[str] = []

    def trace(self, _conversation_id: str) -> None:
        return None

    @contextmanager
    def observe(self, _trace: None, _run_idx: int, *, conversation_id: str, output: dict) -> Iterator[str]:
        self.observed.append(conversation_id)
        yield "trace-id"

    def score(self, _tid: str, *, name: str, value: float, data_type: str) -> None:
        self.scores[name] = value
        self.score_types[name] = data_type

    def quality(
        self, _tid: str, *, strict_checks: dict[str, bool], latency_sec: float | None, cost_usd: float | None
    ) -> None:
        self.quality_checks = strict_checks


def _scored(monkeypatch: pytest.MonkeyPatch, expected: dict, turns: list[ChatResult], **kwargs: Any) -> _FakeCtx:
    _install_client(monkeypatch, _ScriptedChatClient(turns))
    captured: dict[str, Any] = {}
    monkeypatch.setattr(report_skill, "submit_trace_scoring", lambda _link, _identity, **kw: captured.update(kw))
    try:
        evaluate_agentic_report_skill(
            "https://h", "tok", "ws", "q", expected, langfuse=object(), dataset_item_id="item-1", **kwargs
        )
    except ReportSkillAssertionError:
        pass  # scores are written before the gate raises
    ctx = _FakeCtx()
    captured["write_scores"](ctx)
    return ctx


def test_every_scored_check_reaches_langfuse_with_the_draft_facts(monkeypatch: pytest.MonkeyPatch) -> None:
    ctx = _scored(monkeypatch, {"period": _PERIOD, "expects_clarification": True}, [_drafting_turn()])
    checks = {name for name, kind in ctx.score_types.items() if kind == "BOOLEAN"}
    assert checks == {
        "report_drafted",
        "report_part_present",
        "report_ref_matches",
        "report_pages_consistent",
        "report_not_saved",
        "report_skill_activated",
        "report_period_correct",
        "report_asked_first",
        "pass_at_k",
        "pass_power_k",
        "gate_passed",
    }
    assert ctx.scores["report_summaries_from_data"] == 1
    assert ctx.score_types["report_summaries_from_data"] == "NUMERIC"
    assert "report_asked_first" not in ctx.quality_checks


def test_a_check_the_fixture_does_not_state_is_not_published(monkeypatch: pytest.MonkeyPatch) -> None:
    ctx = _scored(monkeypatch, {}, [_drafting_turn()])
    for absent in ("report_period_correct", "report_charts_matched", "report_asked_first"):
        assert absent not in ctx.scores


# ── narrative ───────────────────────────────────────────────────────────────

_NARRATIVE = "Summaries explain how revenue moved in H1 2026."


def _summary_page(page_id: str, text: str | None, *visualizations: str) -> dict:
    page = _content_page(page_id, *visualizations)
    column = page["layout"]["column"]
    if text is not None:
        column.append({"id": "summary", "weight": 1, "paragraph": {"prompt": "Focus on growth.", "text": text}})
    column.append({"id": "footerPageNumber", "weight": 1, "paragraph": "{currentPageNumber} / {totalPages}"})
    return page


class _FakeJudge:
    """Stands in for LLMJudge: returns a fixed verdict and records what it was asked."""

    model = "fake-judge"

    def __init__(self, passed: bool = True, *, error: Exception | None = None) -> None:
        self._passed = passed
        self._error = error
        self.calls: list[dict[str, str]] = []

    def score(self, input: str, expected_output: str, actual_output: str) -> tuple[bool, str]:
        self.calls.append({"input": input, "expected_output": expected_output, "actual_output": actual_output})
        if self._error is not None:
            raise self._error
        return self._passed, "fine" if self._passed else "the summaries ignore returns"


def _narrative_turn(*pages: dict) -> ChatResult:
    return _chat_result(
        tool_calls=[_tool_call("draft_report", _draft_result(page_count=len(pages)))],
        parts=[_report_part(list(pages))],
        text="I've put together a report.",
    )


def test_every_summary_slot_needs_written_text() -> None:
    pages = [_cover_page(), _summary_page("page2", "Revenue grew 12%.", _REVENUE_TREND), _summary_page("page3", "")]
    evaluation = _evaluate(_report_part(pages), expected={"narrative": _NARRATIVE}, tool=_draft_result(page_count=3))
    assert evaluation.strict_checks["report_summaries_present"] is False
    assert evaluation.failures == ["page 'page3' has a summary slot with no written text"]


def test_a_content_page_laid_out_without_a_summary_slot_is_fine() -> None:
    pages = [_cover_page(), _summary_page("page2", "Revenue grew 12%.", _REVENUE_TREND), _summary_page("page3", None)]
    evaluation = _evaluate(_report_part(pages), expected={"narrative": _NARRATIVE}, tool=_draft_result(page_count=3))
    assert evaluation.strict_checks["report_summaries_present"] is True


def test_a_static_text_slot_is_not_a_summary() -> None:
    page = _summary_page("page2", None, _REVENUE_TREND)
    page["layout"]["column"].append({"id": "text1", "weight": 1, "paragraph": "Left text."})
    evaluation = _evaluate(_report_part([_cover_page(), page]), expected={"narrative": _NARRATIVE})
    assert evaluation.strict_checks["report_summaries_present"] is False
    assert evaluation.failures == ["the report has no summary slot"]


def test_a_summary_made_only_of_placeholders_is_not_written() -> None:
    pages = [_cover_page(), _summary_page("page2", "{periodStart} – {periodEnd}", _REVENUE_TREND)]
    evaluation = _evaluate(_report_part(pages), expected={"narrative": _NARRATIVE})
    assert evaluation.strict_checks["report_summaries_present"] is False


def test_summaries_are_not_checked_unless_the_fixture_asks_for_the_narrative() -> None:
    evaluation = _evaluate(_report_part([_cover_page(), _summary_page("page2", None, _REVENUE_TREND)]))
    assert "report_summaries_present" not in evaluation.strict_checks
    assert "report_narrative_judged" not in evaluation.strict_checks


def test_the_judge_reads_the_report_as_text() -> None:
    judge = _FakeJudge()
    turn = _narrative_turn(_cover_page(), _summary_page("page2", "Revenue grew 12%.", _REVENUE_TREND))
    run = _execute_single_report_run(
        _ScriptedChatClient([turn]), "c", "Report on revenue", {"narrative": _NARRATIVE}, 4, judge=judge
    )
    assert run.evaluation.strict_checks["report_narrative_judged"] is True
    assert run.evaluation.strict_pass
    [call] = judge.calls
    assert call["input"] == "Report on revenue"
    assert call["expected_output"] == _NARRATIVE
    assert call["actual_output"] == (
        "Report: Sales overview\n"
        "Period: 2026-01-01 to 2026-06-30\n"
        "\n"
        "Page 2: Revenue\n"
        "Charts: revenue_trend\n"
        "Summary: Revenue grew 12%."
    )


def test_a_failing_verdict_fails_the_run_with_the_judges_reason() -> None:
    turn = _narrative_turn(_cover_page(), _summary_page("page2", "Revenue grew 12%.", _REVENUE_TREND))
    run = _execute_single_report_run(
        _ScriptedChatClient([turn]), "c", "q", {"narrative": _NARRATIVE}, 4, judge=_FakeJudge(passed=False)
    )
    assert run.evaluation.strict_checks["report_narrative_judged"] is False
    assert "the judge failed the narrative: the summaries ignore returns" in run.evaluation.failures


def test_no_report_means_no_judge_call_and_a_failed_narrative() -> None:
    judge = _FakeJudge()
    run = _execute_single_report_run(
        _ScriptedChatClient([_chat_result(text="Sorry.")]), "c", "q", {"narrative": _NARRATIVE}, 1, judge=judge
    )
    assert judge.calls == []
    assert run.evaluation.strict_checks["report_narrative_judged"] is False


def test_an_unreadable_verdict_leaves_the_run_unscored_not_passed() -> None:
    judge = _FakeJudge(error=JudgeResponseError("returned no 'score' key"))
    turn = _narrative_turn(_cover_page(), _summary_page("page2", "Revenue grew 12%.", _REVENUE_TREND))
    run = _execute_single_report_run(_ScriptedChatClient([turn]), "c", "q", {"narrative": _NARRATIVE}, 4, judge=judge)
    assert run.judge_error == "returned no 'score' key"
    assert "report_narrative_judged" not in run.evaluation.strict_checks
    assert not run.evaluation.strict_pass


def test_an_item_the_judge_could_never_grade_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    turn = _narrative_turn(_cover_page(), _summary_page("page2", "Revenue grew 12%.", _REVENUE_TREND))
    _install_client(monkeypatch, _ScriptedChatClient([turn]))
    judge = _FakeJudge(error=JudgeResponseError("empty body"))
    with pytest.raises(JudgeResponseError, match="no readable verdict"):
        evaluate_agentic_report_skill("https://h", "tok", "ws", "q", {"narrative": _NARRATIVE}, judge=judge)


def test_a_narrative_item_passes_with_its_verdict_in_the_detail(monkeypatch: pytest.MonkeyPatch) -> None:
    turn = _narrative_turn(_cover_page(), _summary_page("page2", "Revenue grew 12%.", _REVENUE_TREND))
    _install_client(monkeypatch, _ScriptedChatClient([turn]))
    outcome = evaluate_agentic_report_skill(
        "https://h", "tok", "ws", "q", {"narrative": _NARRATIVE}, judge=_FakeJudge()
    )
    assert outcome.detail["report_narrative_judged"] is True
    assert outcome.detail["report_summaries_present"] is True
    assert outcome.detail["judge_reasoning"] == "fine"


def test_a_fixture_without_a_narrative_never_builds_a_judge(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    _install_client(monkeypatch, _ScriptedChatClient([_drafting_turn()]))
    outcome = evaluate_agentic_report_skill("https://h", "tok", "ws", "q", {})
    assert outcome.runs_passed == 1


def test_an_empty_narrative_is_rejected() -> None:
    with pytest.raises(ValueError, match="narrative must be a non-empty description"):
        _validate_expectation({"narrative": "  "})


def test_a_report_without_content_pages_has_no_summaries_to_present() -> None:
    closing = {**_cover_page(), "id": "page2", "kind": "closing"}
    evaluation = _evaluate(_report_part([_cover_page(), closing]), expected={"narrative": _NARRATIVE})
    assert evaluation.strict_checks["report_summaries_present"] is False
    assert evaluation.failures == ["the report has no content page", "the report has no summary slot"]


class _SequenceJudge(_FakeJudge):
    """Fails to grade the first call, then passes every later one."""

    def score(self, input: str, expected_output: str, actual_output: str) -> tuple[bool, str]:
        self.calls.append({"input": input, "expected_output": expected_output, "actual_output": actual_output})
        if len(self.calls) == 1:
            raise JudgeResponseError("empty body")
        return True, "fine"


def _narrative_turns() -> list[ChatResult]:
    page = _summary_page("page2", "Revenue grew 12%.", _REVENUE_TREND)
    return [_narrative_turn(_cover_page(), page), _narrative_turn(_cover_page(), page)]


def test_an_ungraded_run_keeps_pass_at_k_but_not_pass_power_k(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_client(monkeypatch, _ScriptedChatClient(_narrative_turns()))
    summary = run_agentic_report_skill(
        "https://h", "tok", "ws", "q", {"narrative": _NARRATIVE}, k=2, judge=_SequenceJudge()
    )
    assert [r.judge_error for r in summary.run_results] == ["empty body", None]
    assert summary.pass_at_k
    assert not summary.pass_power_k, "pass^K cannot hold over a run nobody graded"
    assert summary.best.judge_error is None


def test_an_ungraded_run_writes_no_scores(monkeypatch: pytest.MonkeyPatch) -> None:
    ctx = _scored(monkeypatch, {"narrative": _NARRATIVE}, _narrative_turns(), k=2, judge=_SequenceJudge())
    assert ctx.observed == ["conv-2"]
    assert ctx.scores["report_narrative_judged"] == 1.0
    assert ctx.scores["report_summaries_present"] == 1.0


def _failing_narrative_turn() -> ChatResult:
    return _narrative_turn(_cover_page(), _summary_page("page2", "Revenue grew 12%.", _REVENUE_TREND))


def test_a_run_that_failed_a_fixed_check_is_a_failure_even_when_the_judge_errors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expected = {"narrative": _NARRATIVE, "visualizations": [{"id": _RETURNS_BY_CATEGORY, "title": "Returns"}]}
    _install_client(monkeypatch, _ScriptedChatClient([_failing_narrative_turn()]))
    judge = _FakeJudge(error=JudgeResponseError("empty body"))
    with pytest.raises(ReportSkillAssertionError, match="does not show chart 'returns_by_category'"):
        evaluate_agentic_report_skill("https://h", "tok", "ws", "q", expected, judge=judge)


def test_a_failed_run_with_a_judge_error_is_published(monkeypatch: pytest.MonkeyPatch) -> None:
    expected = {"narrative": _NARRATIVE, "visualizations": [{"id": _RETURNS_BY_CATEGORY, "title": "Returns"}]}
    ctx = _scored(monkeypatch, expected, [_failing_narrative_turn()], judge=_FakeJudge(error=JudgeResponseError("x")))
    assert ctx.observed == ["conv-1"]
    assert ctx.scores["report_charts_matched"] == 0.0
    assert "report_narrative_judged" not in ctx.scores


def test_only_content_pages_count_for_summaries() -> None:
    cover = _cover_page()
    cover["layout"]["column"].append({"id": "summary", "weight": 1, "paragraph": {"text": "Revenue grew 12%."}})
    pages = [cover, _summary_page("page2", None, _REVENUE_TREND)]
    evaluation = _evaluate(_report_part(pages), expected={"narrative": _NARRATIVE})
    assert evaluation.strict_checks["report_summaries_present"] is False
    assert evaluation.failures == ["the report has no summary slot"]

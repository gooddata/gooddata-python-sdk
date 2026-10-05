# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
import json
from typing import Any

import pytest
from gooddata_eval.core.agentic import report_skill
from gooddata_eval.core.agentic.report_skill import (
    ReportSkillAssertionError,
    _execute_single_report_run,
    _validate_expectation,
    _visualizations_of,
    build_simulated_reply,
    evaluate_agentic_report_skill,
    evaluate_report_response,
    run_agentic_report_skill,
)
from gooddata_eval.core.models import ChatResult

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


def _evaluate(part: dict | None, *, expected: dict | None = None, tool: dict | None = None, skill: bool = True):
    return evaluate_report_response(
        _draft_result() if tool is None else tool,
        part,
        {} if expected is None else expected,
        skill_activated=skill,
    )


def test_a_drafted_report_returned_in_the_chat_item_passes():
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


def test_period_and_charts_are_scored_only_when_the_fixture_states_them():
    expected = {"period": _PERIOD, "visualizations": [{"id": _REVENUE_TREND, "title": "Revenue trend"}]}
    checks = _evaluate(_report_part(), expected=expected).strict_checks
    assert checks["report_period_correct"] is True
    assert checks["report_charts_matched"] is True


def test_no_successful_draft_fails_every_check_and_says_so():
    evaluation = evaluate_report_response(None, None, {"period": _PERIOD}, skill_activated=True)
    assert evaluation.strict_checks["report_drafted"] is False
    assert evaluation.strict_checks["report_part_present"] is False
    assert evaluation.strict_checks["report_period_correct"] is False
    assert not evaluation.strict_pass
    assert evaluation.failures == ["the agent never produced a successful draft_report call"]


def test_a_draft_without_a_report_part_fails():
    evaluation = _evaluate(None)
    assert evaluation.strict_checks["report_drafted"] is True
    assert evaluation.strict_checks["report_part_present"] is False
    assert evaluation.failures == ["the response carries no 'report' part"]


def test_a_report_part_whose_document_did_not_resolve_fails():
    evaluation = _evaluate(_report_part(report=None))
    assert evaluation.strict_checks["report_part_present"] is False
    assert evaluation.failures == ["the 'report' part carries no report document (report_ref 'report_1')"]


def test_a_document_that_is_not_a_report_fails():
    evaluation = _evaluate(_report_part(report={"id": "x", "type": "dashboard", "pages": []}))
    assert evaluation.strict_checks["report_part_present"] is False
    assert evaluation.failures == ["the 'report' part carries a document of type 'dashboard', expected 'report'"]


def test_a_part_pointing_at_another_draft_fails():
    evaluation = _evaluate(_report_part(ref="report_2"))
    assert evaluation.strict_checks["report_ref_matches"] is False
    assert evaluation.failures == ["the 'report' part shows 'report_2', but draft_report returned 'report_1'"]


def test_a_page_count_that_disagrees_with_the_pages_fails():
    evaluation = _evaluate(_report_part(page_count=3))
    assert evaluation.strict_checks["report_pages_consistent"] is False
    assert evaluation.failures == ["the report has 2 page(s), but the part says 3 and draft_report said 2"]


def test_a_cover_alone_is_not_a_report():
    evaluation = _evaluate(_report_part([_cover_page()]), tool=_draft_result(page_count=1))
    assert evaluation.strict_checks["report_pages_consistent"] is False
    assert evaluation.failures == ["the report has 1 page(s); it needs a cover and at least one content page"]


def test_a_new_draft_must_not_already_be_saved():
    evaluation = _evaluate(_report_part(saved_report_id="sales_overview"))
    assert evaluation.strict_checks["report_not_saved"] is False
    assert evaluation.failures == ["a new draft must not be saved yet, but it reports saved_report_id 'sales_overview'"]


def test_a_new_draft_must_not_edit_a_saved_report():
    evaluation = _evaluate(_report_part(base_report_id="q3_review"))
    assert evaluation.strict_checks["report_not_saved"] is False
    assert evaluation.failures == [
        "a new draft must not edit a saved report, but it reports base_report_id 'q3_review'"
    ]


def test_a_wrong_period_fails():
    evaluation = _evaluate(
        _report_part(period={"start": "2025-07-01", "end": "2025-12-31"}), expected={"period": _PERIOD}
    )
    assert evaluation.strict_checks["report_period_correct"] is False
    assert evaluation.failures == [
        "the report covers 2025-07-01 to 2025-12-31, expected 2026-01-01 to 2026-06-30",
    ]


def test_a_missing_chart_fails_and_is_named():
    expected = {"visualizations": [{"id": _RETURNS_BY_CATEGORY, "title": "Returns by category"}]}
    evaluation = _evaluate(_report_part(), expected=expected)
    assert evaluation.strict_checks["report_charts_matched"] is False
    assert evaluation.failures == ["the report does not show chart 'returns_by_category' ('Returns by category')"]


def test_a_routing_miss_fails_the_skill_check_alone():
    evaluation = _evaluate(_report_part(), skill=False)
    assert evaluation.strict_checks["report_skill_activated"] is False
    assert [name for name, ok in evaluation.strict_checks.items() if not ok] == ["report_skill_activated"]


def test_visualizations_are_found_however_deep_the_layout_nests_them():
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
def test_an_unusable_fixture_is_rejected_before_any_request(expected, message):
    with pytest.raises(ValueError, match=message):
        _validate_expectation(expected)


def test_an_empty_fixture_is_usable():
    _validate_expectation({})


# ── simulated user ──────────────────────────────────────────────────────────


def test_the_simulated_reply_names_the_charts_and_the_period():
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


def test_the_simulated_reply_leaves_out_what_the_fixture_does_not_state():
    assert build_simulated_reply({}) == "Anything else is up to you. Please create the report now."


# ── conversation loop ───────────────────────────────────────────────────────


def test_a_report_drafted_on_the_first_turn_ends_the_run():
    client = _ScriptedChatClient([_drafting_turn()])
    run = _execute_single_report_run(client, "conv-1", "Create a sales report for H1 2026", {}, max_iterations=4)
    assert client.sent == ["Create a sales report for H1 2026"]
    assert run.total_turns == 1
    assert run.asked_first is False
    assert run.evaluation.strict_pass


def test_a_clarifying_question_is_answered_and_the_report_scored():
    expected = {"period": _PERIOD, "visualizations": [{"id": _REVENUE_TREND, "title": "Revenue trend"}]}
    question = _chat_result(text="Which period should the report cover?")
    client = _ScriptedChatClient([question, _drafting_turn()])
    run = _execute_single_report_run(client, "conv-1", "Make me a report", expected, max_iterations=4)
    assert client.sent == ["Make me a report", build_simulated_reply(expected)]
    assert run.total_turns == 2
    assert run.asked_first is True
    assert run.evaluation.strict_pass


def test_a_silent_turn_ends_the_run_without_replying():
    client = _ScriptedChatClient([_chat_result()])
    run = _execute_single_report_run(client, "conv-1", "Make me a report", {}, max_iterations=4)
    assert client.sent == ["Make me a report"]
    assert not run.evaluation.strict_pass


def test_a_copilot_that_never_drafts_stops_at_the_turn_limit():
    client = _ScriptedChatClient([_chat_result(text="Which period?")] * 5)
    run = _execute_single_report_run(client, "conv-1", "Make me a report", {}, max_iterations=3)
    assert len(client.sent) == 3
    assert run.evaluation.strict_checks["report_drafted"] is False


def test_asking_first_is_recorded_only_when_the_fixture_expects_it():
    plain = _execute_single_report_run(_ScriptedChatClient([_drafting_turn()]), "c", "q", {}, max_iterations=4)
    assert "report_asked_first" not in plain.diagnostics

    expected = {"expects_clarification": True}
    run = _execute_single_report_run(_ScriptedChatClient([_drafting_turn()]), "c", "q", expected, max_iterations=4)
    assert run.diagnostics == {"report_asked_first": False}
    assert run.evaluation.strict_pass, "drafting without asking is recorded, never failed"


# ── K runs and the gate ─────────────────────────────────────────────────────


def test_every_conversation_the_run_creates_is_deleted(monkeypatch):
    client = _ScriptedChatClient([_drafting_turn(), _drafting_turn()])
    _install_client(monkeypatch, client)
    summary = run_agentic_report_skill("https://h", "tok", "ws", "Create a report", {}, k=2)
    assert summary.pass_at_k and summary.pass_power_k
    assert client.deleted == client.created == ["conv-1", "conv-2"]
    assert client.closed


def test_a_conversation_handed_in_is_not_deleted(monkeypatch):
    client = _ScriptedChatClient([_drafting_turn()])
    _install_client(monkeypatch, client)
    run_agentic_report_skill("https://h", "tok", "ws", "Create a report", {}, initial_conversation_id="theirs")
    assert client.deleted == []


def test_a_passing_item_returns_its_checks_and_draft_facts(monkeypatch):
    _install_client(monkeypatch, _ScriptedChatClient([_drafting_turn()]))
    outcome = evaluate_agentic_report_skill("https://h", "tok", "ws", "Create a report", {"period": _PERIOD})
    assert outcome.runs_passed == 1
    assert outcome.detail["report_period_correct"] is True
    assert outcome.detail["summaries_from_data"] == 1
    assert outcome.detail["failures"] == []


def test_a_failing_item_raises_with_the_failures(monkeypatch):
    _install_client(monkeypatch, _ScriptedChatClient([_chat_result(text="I can't do that.")]))
    with pytest.raises(ReportSkillAssertionError) as raised:
        evaluate_agentic_report_skill("https://h", "tok", "ws", "Create a report", {}, max_iterations=1)
    assert "the agent never produced a successful draft_report call" in str(raised.value)
    assert raised.value.runs_passed == 0
    assert raised.value.conversation_id == "conv-1"


def test_a_failing_item_without_report_builder_points_at_the_flags(monkeypatch):
    turn = _chat_result(tool_calls=[_set_skills("visualization")], text="Here is a chart.")
    _install_client(monkeypatch, _ScriptedChatClient([turn]))
    with pytest.raises(ReportSkillAssertionError, match="enableBusinessBriefingReportsApp"):
        evaluate_agentic_report_skill("https://h", "tok", "ws", "Create a report", {}, max_iterations=1)


def test_an_unusable_fixture_fails_before_any_request(monkeypatch):
    client = _ScriptedChatClient([])
    _install_client(monkeypatch, client)
    with pytest.raises(ValueError):
        evaluate_agentic_report_skill("https://h", "tok", "ws", "Create a report", {"visualizations": []})
    assert client.created == []


def test_a_ref_missing_on_both_sides_does_not_match():
    evaluation = _evaluate(_report_part(ref=None), tool={**_draft_result(), "ref": None})
    assert evaluation.strict_checks["report_ref_matches"] is False


def test_the_last_successful_draft_of_a_turn_is_the_one_scored():
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


def test_a_first_turn_that_did_not_ask_is_not_recorded_as_asking():
    refusal = _chat_result(text="I could not find any charts on that topic.")
    expected = {"expects_clarification": True}
    run = _execute_single_report_run(_ScriptedChatClient([refusal, _drafting_turn()]), "c", "q", expected, 4)
    assert run.evaluation.strict_pass
    assert run.diagnostics == {"report_asked_first": False}


def test_a_structured_clarifying_question_counts_as_asking():
    question = _chat_result(parts=[{"type": "clarifyingQuestions", "questions": []}])
    expected = {"expects_clarification": True}
    run = _execute_single_report_run(_ScriptedChatClient([question, _drafting_turn()]), "c", "q", expected, 4)
    assert run.diagnostics == {"report_asked_first": True}

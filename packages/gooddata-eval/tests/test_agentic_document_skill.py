# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
import importlib
import json
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

import pytest
from gooddata_eval.cli.agentic_runner import _dispatch_agentic
from gooddata_eval.core import agentic
from gooddata_eval.core.agentic import document_skill
from gooddata_eval.core.agentic.document_skill import (
    DocumentEvaluation,
    DocumentSkillAssertionError,
    _execute_single_document_run,
    _validate_expectation,
    _visualizations_of,
    build_simulated_reply,
    evaluate_agentic_document_skill,
    evaluate_document_response,
    legacy_wire_names,
    render_document_text,
    run_agentic_document_skill,
)
from gooddata_eval.core.evaluators._llm_judge import JudgeResponseError
from gooddata_eval.core.models import ChatResult, DatasetItem

# Shapes follow what gen-ai writes for a drafted document (composed_report.aac.json): a cover
# page, then content pages whose layout nests `column` and `row` entries down to the slots.
_REVENUE_TREND = "revenue_trend"
_RETURNS_BY_CATEGORY = "returns_by_category"
_PERIOD = {"start": "2026-01-01", "end": "2026-06-30"}


def _cover_page() -> dict:
    return {
        "id": "page1",
        "kind": "cover",
        "format": "widescreen",
        "layout": {"column": [{"id": "coverTitle", "weight": 2, "heading": "{documentName}", "style": "h1"}]},
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


def _document_part(
    pages: list[dict] | None = None,
    *,
    ref: str = "document_1",
    page_count: int | None = None,
    period: dict | None = None,
    saved_document_id: str | None = None,
    base_document_id: str | None = None,
    document: dict | None | str = "default",
) -> dict:
    pages = pages if pages is not None else [_cover_page(), _content_page("page2", _REVENUE_TREND)]
    document = (
        {
            "id": "sales_overview",
            "type": "document",
            "title": "Sales overview",
            "period": period if period is not None else _PERIOD,
            "pages": pages,
        }
        if document == "default"
        else document
    )
    return {
        "type": "document",
        "document_ref": ref,
        "format": "aac-v1",
        "document": document,
        "page_count": len(pages) if page_count is None else page_count,
        "base_document_id": base_document_id,
        "saved_document_id": saved_document_id,
    }


# v2 shapes follow the Publisher content v2 model: a top-level `version`, an absolute or relative
# `period`, and `content` holding the pages, whose layout nests `row` and `column` containers
# through `children` down to typed widgets.
_V2_PERIOD = {"type": "absolute", "granularity": "GDC.time.date", "from": "2026-01-01", "to": "2026-06-30"}


def _v2_cover_page() -> dict:
    return {
        "id": "page1",
        "kind": "cover",
        "layout": {
            "type": "column",
            "children": [{"type": "title", "id": "coverTitle", "proportion": 2, "markdown": "{documentName}"}],
        },
    }


def _v2_content_page(page_id: str, *visualizations: str, takeaway: str | None = None, bare_ids: bool = False) -> dict:
    """A content page; ``takeaway`` adds a takeaway widget, and ``""`` adds one with no text written."""
    widgets: list[dict] = [
        {
            "type": "visualization",
            "id": f"widget{i}",
            "visualization": v if bare_ids else {"identifier": v, "type": "insight"},
            "title": {"visible": True},
        }
        for i, v in enumerate(visualizations, start=1)
    ]
    row: list[dict] = [{"type": "row", "proportion": 2, "children": widgets}]
    if takeaway is not None:
        row.append(
            {
                "type": "takeaway",
                "id": "takeaway",
                "title": {"text": "Key takeaway"},
                **({"markdown": takeaway} if takeaway else {}),
                "generation": {"context": {"widgets": ["widget1"]}},
            }
        )
    return {
        "id": page_id,
        "kind": "content",
        "layout": {
            "type": "column",
            "children": [
                {"type": "title", "id": "pageTitle", "proportion": 2, "markdown": "Revenue"},
                {"type": "row", "proportion": 9, "children": row},
                {
                    "type": "text",
                    "id": "footerPageNumber",
                    "markdown": "{currentPageNumber} / {totalPages}",
                    "decorative": True,
                },
            ],
        },
    }


def _v2_document(pages: list[dict], *, period: Any = None, form: str = "entity") -> dict:
    """A v2 document: ``entity`` keeps the pages in ``content``, ``flat`` lifts the content keys to
    the top level, and ``sections`` groups the cover and the remaining pages into two sections."""
    content: dict[str, Any] = {"pages": pages}
    if form == "sections":
        content = {
            "sections": [
                {"id": "section_intro", "title": "Intro", "pages": pages[:1]},
                {"id": "section_body", "pages": pages[1:]},
            ]
        }
    document: dict[str, Any] = {
        "type": "document",
        "id": "sales_overview",
        "version": "2",
        "title": "Sales overview",
        "period": period if period is not None else _V2_PERIOD,
    }
    return {**document, **content} if form == "flat" else {**document, "content": content}


def _v2_document_part(
    pages: list[dict] | None = None, *, period: Any = None, form: str = "entity", **kwargs: Any
) -> dict:
    """A v2 part; ``page_count`` defaults to the visible pages, as a reader counts them."""
    pages = pages if pages is not None else [_v2_cover_page(), _v2_content_page("page2", _REVENUE_TREND)]
    kwargs.setdefault("page_count", sum(1 for page in pages if page.get("visible") is not False))
    part = _document_part(pages, document=_v2_document(pages, period=period, form=form), **kwargs)
    return {**part, "format": "aac-v2"}


# Builders keyed by schema version, for the tests whose assertion is the same for v1 and v2.
_VERSIONS = ["v1", "v2"]


def _versioned_cover(version: str) -> dict:
    return _cover_page() if version == "v1" else _v2_cover_page()


def _versioned_content(version: str, page_id: str, *visualizations: str, summary: str | None = None) -> dict:
    if version == "v1":
        return (
            _content_page(page_id, *visualizations)
            if summary is None
            else _summary_page(page_id, summary, *visualizations)
        )
    return _v2_content_page(page_id, *visualizations, takeaway=summary)


def _versioned_part(
    version: str, pages: list[dict] | None = None, *, period: tuple[str, str] | None = None, **kwargs: Any
) -> dict:
    if version == "v1":
        return _document_part(
            pages, period=None if period is None else {"start": period[0], "end": period[1]}, **kwargs
        )
    v2_period = None if period is None else {**_V2_PERIOD, "from": period[0], "to": period[1]}
    return _v2_document_part(pages, period=v2_period, **kwargs)


def _draft_result(*, ref: str = "document_1", page_count: int = 2, summaries_from_data: int = 1) -> dict:
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
        tool_calls=[_set_skills("document_builder"), _tool_call("draft_document", _draft_result())],
        parts=[{"type": "text", "text": "I've put together a document with 2 slides."}, _document_part(**part_kwargs)],
        text="I've put together a document with 2 slides.",
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
    monkeypatch.setattr(document_skill, "ChatClient", lambda **_kwargs: client)


# ── scoring ─────────────────────────────────────────────────────────────────


def _evaluate(
    part: dict | None, *, expected: dict | None = None, tool: dict | None = None, skill: bool = True
) -> DocumentEvaluation:
    return evaluate_document_response(
        _draft_result() if tool is None else tool,
        part,
        {} if expected is None else expected,
        skill_activated=skill,
    )


@pytest.mark.parametrize("version", _VERSIONS)
def test_a_drafted_document_returned_in_the_chat_item_passes(version: str) -> None:
    evaluation = _evaluate(_versioned_part(version))
    assert evaluation.strict_checks == {
        "document_drafted": True,
        "document_part_present": True,
        "document_ref_matches": True,
        "document_pages_consistent": True,
        "document_not_saved": True,
        "document_skill_activated": True,
        "document_wire_names": True,
    }
    assert evaluation.strict_pass
    assert evaluation.failures == []


@pytest.mark.parametrize("version", _VERSIONS)
def test_period_and_charts_are_scored_only_when_the_fixture_states_them(version: str) -> None:
    expected = {"period": _PERIOD, "visualizations": [{"id": _REVENUE_TREND, "title": "Revenue trend"}]}
    checks = _evaluate(_versioned_part(version), expected=expected).strict_checks
    assert checks["document_period_correct"] is True
    assert checks["document_charts_matched"] is True


def test_no_successful_draft_fails_every_check_and_says_so() -> None:
    evaluation = evaluate_document_response(None, None, {"period": _PERIOD}, skill_activated=True)
    assert evaluation.strict_checks["document_drafted"] is False
    assert evaluation.strict_checks["document_part_present"] is False
    assert evaluation.strict_checks["document_period_correct"] is False
    assert not evaluation.strict_pass
    assert evaluation.failures == ["the agent never produced a successful draft_document call"]


def test_a_draft_without_a_document_part_fails() -> None:
    evaluation = _evaluate(None)
    assert evaluation.strict_checks["document_drafted"] is True
    assert evaluation.strict_checks["document_part_present"] is False
    assert evaluation.failures == ["the response carries no 'document' part"]


def test_a_document_part_whose_document_did_not_resolve_fails() -> None:
    evaluation = _evaluate(_document_part(document=None))
    assert evaluation.strict_checks["document_part_present"] is False
    assert evaluation.failures == ["the 'document' part carries no document (document_ref 'document_1')"]


def test_a_document_that_is_not_a_document_fails() -> None:
    evaluation = _evaluate(_document_part(document={"id": "x", "type": "dashboard", "pages": []}))
    assert evaluation.strict_checks["document_part_present"] is False
    assert evaluation.failures == ["the 'document' part carries a document of type 'dashboard', expected 'document'"]


def test_a_part_pointing_at_another_draft_fails() -> None:
    evaluation = _evaluate(_document_part(ref="document_2"))
    assert evaluation.strict_checks["document_ref_matches"] is False
    assert evaluation.failures == ["the 'document' part shows 'document_2', but draft_document returned 'document_1'"]


def test_a_page_count_that_disagrees_with_the_pages_fails() -> None:
    evaluation = _evaluate(_document_part(page_count=3))
    assert evaluation.strict_checks["document_pages_consistent"] is False
    assert evaluation.failures == ["the document has 2 page(s), but the part says 3 and draft_document said 2"]


def test_a_cover_alone_is_not_a_document() -> None:
    evaluation = _evaluate(_document_part([_cover_page()]), tool=_draft_result(page_count=1))
    assert evaluation.strict_checks["document_pages_consistent"] is False
    assert evaluation.failures == ["the document has no content page"]


def test_a_new_draft_must_not_already_be_saved() -> None:
    evaluation = _evaluate(_document_part(saved_document_id="sales_overview"))
    assert evaluation.strict_checks["document_not_saved"] is False
    assert evaluation.failures == [
        "a new draft must not be saved yet, but it reports saved_document_id 'sales_overview'"
    ]


def test_a_new_draft_must_not_edit_a_saved_document() -> None:
    evaluation = _evaluate(_document_part(base_document_id="q3_review"))
    assert evaluation.strict_checks["document_not_saved"] is False
    assert evaluation.failures == [
        "a new draft must not edit a saved document, but it reports base_document_id 'q3_review'"
    ]


@pytest.mark.parametrize("version", _VERSIONS)
def test_a_wrong_period_fails(version: str) -> None:
    evaluation = _evaluate(_versioned_part(version, period=("2025-07-01", "2025-12-31")), expected={"period": _PERIOD})
    assert evaluation.strict_checks["document_period_correct"] is False
    assert evaluation.failures == [
        "the document covers 2025-07-01 to 2025-12-31, expected 2026-01-01 to 2026-06-30",
    ]


@pytest.mark.parametrize("version", _VERSIONS)
def test_a_missing_chart_fails_and_is_named(version: str) -> None:
    expected = {"visualizations": [{"id": _RETURNS_BY_CATEGORY, "title": "Returns by category"}]}
    evaluation = _evaluate(_versioned_part(version), expected=expected)
    assert evaluation.strict_checks["document_charts_matched"] is False
    assert evaluation.failures == ["the document does not show chart 'returns_by_category' ('Returns by category')"]


def test_a_routing_miss_fails_the_skill_check_alone() -> None:
    evaluation = _evaluate(_document_part(), skill=False)
    assert evaluation.strict_checks["document_skill_activated"] is False
    assert [name for name, ok in evaluation.strict_checks.items() if not ok] == ["document_skill_activated"]


@pytest.mark.parametrize("version", _VERSIONS)
def test_visualizations_are_found_however_deep_the_layout_nests_them(version: str) -> None:
    page = _versioned_content(version, "page2", _REVENUE_TREND, _RETURNS_BY_CATEGORY)
    document = _versioned_part(version, [_versioned_cover(version), page])["document"]
    assert _visualizations_of(document) == {_REVENUE_TREND, _RETURNS_BY_CATEGORY}


def _legacy_part() -> dict:
    """The answer part as gen-ai sent it before the Document names."""
    part = _document_part()
    document = {**part["document"], "type": "report"}
    return {
        "type": "report",
        "report_ref": part["document_ref"],
        "format": "aac-v1",
        "report": document,
        "page_count": part["page_count"],
        "base_report_id": None,
        "saved_report_id": None,
    }


def test_a_part_with_the_report_names_fails_the_wire_check_and_names_each_one() -> None:
    names = legacy_wire_names([_legacy_part()], [])
    assert names == [
        "part type 'report'",
        "part key 'report'",
        "part key 'report_ref'",
        "part key 'base_report_id'",
        "part key 'saved_report_id'",
        "document type 'report'",
    ]


def test_the_report_tool_and_skill_ids_are_named_too() -> None:
    turn = _chat_result(
        tool_calls=[
            _set_skills("report_builder"),
            _tool_call("list_report_layouts", {"status": "success"}),
            _tool_call("draft_report", _draft_result()),
        ]
    )
    assert legacy_wire_names([], turn.tool_call_events) == [
        "skill 'report_builder'",
        "tool 'list_report_layouts'",
        "tool 'draft_report'",
    ]


def test_a_set_skills_call_asking_for_the_report_skill_is_named_even_when_it_was_refused() -> None:
    call = {
        "functionName": "set_skills",
        "functionArguments": json.dumps({"skill_names": ["report_builder"]}),
        "result": json.dumps({"status": "error", "message": "unknown skill"}),
    }
    turn = _chat_result(tool_calls=[call])
    assert legacy_wire_names([], turn.tool_call_events) == ["skill 'report_builder'"]


def test_a_set_skills_call_whose_arguments_are_not_an_object_is_ignored() -> None:
    call = {"functionName": "set_skills", "functionArguments": json.dumps(["report_builder"]), "result": None}
    assert legacy_wire_names([], _chat_result(tool_calls=[call]).tool_call_events) == []


def test_the_document_names_leave_the_wire_check_passing() -> None:
    turn = _drafting_turn()
    assert legacy_wire_names(turn.unhandled_parts, turn.tool_call_events) == []


def test_a_run_against_a_gen_ai_with_the_report_names_fails_on_the_wire_check() -> None:
    turn = _chat_result(
        tool_calls=[_set_skills("report_builder"), _tool_call("draft_report", _draft_result())],
        parts=[_legacy_part()],
    )
    run = _execute_single_document_run(_ScriptedChatClient([turn]), "conv-1", "Create a document", {}, 1)

    assert run.evaluation.strict_checks["document_wire_names"] is False
    assert run.evaluation.failures[0] == (
        "gen-ai sends the Report names: skill 'report_builder', tool 'draft_report', part type 'report', "
        "part key 'report', part key 'report_ref', part key 'base_report_id', part key 'saved_report_id', "
        "document type 'report'"
    )


def test_the_wire_check_reads_every_turn_not_only_the_drafting_one() -> None:
    asking = _chat_result(parts=[{"type": "report", "report_ref": "report_0"}], text="Which period?")
    run = _execute_single_document_run(
        _ScriptedChatClient([asking, _drafting_turn()]), "conv-1", "Create a document", {}, 2
    )

    assert run.evaluation.strict_checks["document_wire_names"] is False


def test_a_gen_ai_on_the_report_names_stops_at_its_draft_instead_of_replying_again() -> None:
    turn = _chat_result(
        tool_calls=[_set_skills("report_builder"), _tool_call("draft_report", _draft_result())],
        parts=[_legacy_part()],
    )
    client = _ScriptedChatClient([turn, _drafting_turn()])
    run = _execute_single_document_run(client, "conv-1", "Create a document", {}, 4)

    assert client.sent == ["Create a document"]
    assert run.evaluation.strict_checks["document_wire_names"] is False


def test_a_failing_item_on_the_report_names_points_at_the_rename_not_the_flags(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    turn = _chat_result(tool_calls=[_set_skills("report_builder"), _tool_call("draft_report", _draft_result())])
    _install_client(monkeypatch, _ScriptedChatClient([turn]))
    with pytest.raises(DocumentSkillAssertionError) as raised:
        evaluate_agentic_document_skill("https://h", "tok", "ws", "Create a document", {}, max_iterations=1)

    assert "gen-ai still sends the Report names" in str(raised.value)
    assert "enableGenAiReportBuilderSkill" not in str(raised.value)


def test_a_user_context_with_view_report_fails_before_any_request(monkeypatch: pytest.MonkeyPatch) -> None:
    client = _ScriptedChatClient([_drafting_turn()])
    _install_client(monkeypatch, client)
    with pytest.raises(ValueError, match="user_context.view.report is the Report name; send view.document"):
        run_agentic_document_skill(
            "https://h", "tok", "ws", "Refine it", {}, user_context={"view": {"report": {"id": "q3"}}}
        )
    assert client.sent == []


def test_the_document_format_reaches_the_chat_client(monkeypatch: pytest.MonkeyPatch) -> None:
    client = _ScriptedChatClient([_drafting_turn()])
    built: list[dict[str, Any]] = []

    def _build(**kwargs: Any) -> _ScriptedChatClient:
        built.append(kwargs)
        return client

    monkeypatch.setattr(document_skill, "ChatClient", _build)
    evaluate_agentic_document_skill("https://h", "tok", "ws", "Create a document", {}, document_format="aac-v2")
    assert [kwargs["document_format"] for kwargs in built] == ["aac-v2"]


def test_an_unknown_document_format_fails_before_any_request(monkeypatch: pytest.MonkeyPatch) -> None:
    client = _ScriptedChatClient([_drafting_turn()])
    _install_client(monkeypatch, client)
    with pytest.raises(ValueError, match="Invalid document format 'v2'"):
        evaluate_agentic_document_skill("https://h", "tok", "ws", "Create a document", {}, document_format="v2")
    assert client.created == client.sent == []


def test_an_unknown_document_format_fails_before_the_narrative_judge_is_built(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    client = _ScriptedChatClient([_drafting_turn()])
    _install_client(monkeypatch, client)
    with pytest.raises(ValueError, match="Invalid document format 'v2'"):
        run_agentic_document_skill("https://h", "tok", "ws", "q", {"narrative": _NARRATIVE}, document_format="v2")
    assert client.created == client.sent == []


@pytest.mark.parametrize(
    ("document_format", "extra", "expected"),
    [
        ("AAC-V2", {"tags": ["ci"]}, {"tags": ["ci"], "document_format": "aac-v2"}),
        (None, {"tags": ["ci"]}, {"tags": ["ci"]}),
        (None, None, None),
    ],
)
def test_the_document_format_is_recorded_in_the_run_metadata(
    monkeypatch: pytest.MonkeyPatch,
    document_format: str | None,
    extra: dict[str, Any] | None,
    expected: dict[str, Any] | None,
) -> None:
    _install_client(monkeypatch, _ScriptedChatClient([_drafting_turn()]))
    identities: list[Any] = []
    monkeypatch.setattr(
        document_skill, "submit_trace_scoring", lambda _link, identity, **_kw: identities.append(identity)
    )
    try:
        evaluate_agentic_document_skill(
            "https://h",
            "tok",
            "ws",
            "Create a document",
            {},
            langfuse=object(),
            dataset_item_id="item-1",
            run_metadata_extra=extra,
            document_format=document_format,
        )
    except DocumentSkillAssertionError:
        pass  # the identity is handed to scoring before the gate raises
    assert [identity.run_metadata_extra for identity in identities] == [expected]


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
        "Anything else is up to you. Please create the document now."
    )


def test_the_simulated_reply_leaves_out_what_the_fixture_does_not_state() -> None:
    assert build_simulated_reply({}) == "Anything else is up to you. Please create the document now."


# ── conversation loop ───────────────────────────────────────────────────────


def test_a_document_drafted_on_the_first_turn_ends_the_run() -> None:
    client = _ScriptedChatClient([_drafting_turn()])
    run = _execute_single_document_run(client, "conv-1", "Create a sales document for H1 2026", {}, max_iterations=4)
    assert client.sent == ["Create a sales document for H1 2026"]
    assert run.total_turns == 1
    assert run.asked_first is False
    assert run.evaluation.strict_pass


def test_a_clarifying_question_is_answered_and_the_document_scored() -> None:
    expected = {"period": _PERIOD, "visualizations": [{"id": _REVENUE_TREND, "title": "Revenue trend"}]}
    question = _chat_result(text="Which period should the document cover?")
    client = _ScriptedChatClient([question, _drafting_turn()])
    run = _execute_single_document_run(client, "conv-1", "Make me a document", expected, max_iterations=4)
    assert client.sent == ["Make me a document", build_simulated_reply(expected)]
    assert run.total_turns == 2
    assert run.asked_first is True
    assert run.evaluation.strict_pass


def test_a_silent_turn_ends_the_run_without_replying() -> None:
    client = _ScriptedChatClient([_chat_result()])
    run = _execute_single_document_run(client, "conv-1", "Make me a document", {}, max_iterations=4)
    assert client.sent == ["Make me a document"]
    assert not run.evaluation.strict_pass


def test_a_copilot_that_never_drafts_stops_at_the_turn_limit() -> None:
    client = _ScriptedChatClient([_chat_result(text="Which period?")] * 5)
    run = _execute_single_document_run(client, "conv-1", "Make me a document", {}, max_iterations=3)
    assert len(client.sent) == 3
    assert run.evaluation.strict_checks["document_drafted"] is False


def test_asking_first_is_recorded_only_when_the_fixture_expects_it() -> None:
    plain = _execute_single_document_run(_ScriptedChatClient([_drafting_turn()]), "c", "q", {}, max_iterations=4)
    assert "document_asked_first" not in plain.diagnostics

    expected = {"expects_clarification": True}
    run = _execute_single_document_run(_ScriptedChatClient([_drafting_turn()]), "c", "q", expected, max_iterations=4)
    assert run.diagnostics == {"document_asked_first": False}
    assert run.evaluation.strict_pass, "drafting without asking is recorded, never failed"


# ── K runs and the gate ─────────────────────────────────────────────────────


def test_every_conversation_the_run_creates_is_deleted(monkeypatch: pytest.MonkeyPatch) -> None:
    client = _ScriptedChatClient([_drafting_turn(), _drafting_turn()])
    _install_client(monkeypatch, client)
    summary = run_agentic_document_skill("https://h", "tok", "ws", "Create a document", {}, k=2)
    assert summary.pass_at_k and summary.pass_power_k
    assert client.deleted == client.created == ["conv-1", "conv-2"]
    assert client.closed


def test_a_conversation_handed_in_is_not_deleted(monkeypatch: pytest.MonkeyPatch) -> None:
    client = _ScriptedChatClient([_drafting_turn()])
    _install_client(monkeypatch, client)
    run_agentic_document_skill("https://h", "tok", "ws", "Create a document", {}, initial_conversation_id="theirs")
    assert client.deleted == []


def test_a_passing_item_returns_its_checks_and_draft_facts(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_client(monkeypatch, _ScriptedChatClient([_drafting_turn()]))
    outcome = evaluate_agentic_document_skill("https://h", "tok", "ws", "Create a document", {"period": _PERIOD})
    assert outcome.runs_passed == 1
    assert outcome.detail["document_period_correct"] is True
    assert outcome.detail["summaries_from_data"] == 1
    assert outcome.detail["failures"] == []
    assert len(outcome.run_latencies_s) == outcome.runs_effective == 1
    assert all(latency >= 0 for latency in outcome.run_latencies_s)


def test_a_failing_item_raises_with_the_failures(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_client(monkeypatch, _ScriptedChatClient([_chat_result(text="I can't do that.")]))
    with pytest.raises(DocumentSkillAssertionError) as raised:
        evaluate_agentic_document_skill("https://h", "tok", "ws", "Create a document", {}, max_iterations=1)
    assert "the agent never produced a successful draft_document call" in str(raised.value)
    assert raised.value.runs_passed == 0
    assert raised.value.conversation_id == "conv-1"
    assert len(raised.value.run_latencies_s) == raised.value.runs_effective == 1


def test_a_failing_item_without_document_builder_points_at_the_flags(monkeypatch: pytest.MonkeyPatch) -> None:
    turn = _chat_result(tool_calls=[_set_skills("visualization")], text="Here is a chart.")
    _install_client(monkeypatch, _ScriptedChatClient([turn]))
    with pytest.raises(
        DocumentSkillAssertionError,
        match="enableGenAiReportBuilderSkill and the org.s enableBusinessBriefingReportsApp",
    ):
        evaluate_agentic_document_skill("https://h", "tok", "ws", "Create a document", {}, max_iterations=1)


def test_an_unusable_fixture_fails_before_any_request(monkeypatch: pytest.MonkeyPatch) -> None:
    client = _ScriptedChatClient([])
    _install_client(monkeypatch, client)
    with pytest.raises(ValueError):
        evaluate_agentic_document_skill("https://h", "tok", "ws", "Create a document", {"visualizations": []})
    assert client.created == []


def test_a_ref_missing_on_both_sides_does_not_match() -> None:
    evaluation = _evaluate(_document_part(ref=None), tool={**_draft_result(), "ref": None})
    assert evaluation.strict_checks["document_ref_matches"] is False


def test_the_last_successful_draft_of_a_turn_is_the_one_scored() -> None:
    turn = _chat_result(
        tool_calls=[
            _tool_call("draft_document", _draft_result(ref="document_1")),
            _tool_call("draft_document", {"status": "error", "message": "no layout fits 7 charts"}),
            _tool_call("draft_document", _draft_result(ref="document_2")),
        ],
        parts=[_document_part(ref="document_2")],
        text="I've put together a document with 2 slides.",
    )
    run = _execute_single_document_run(_ScriptedChatClient([turn]), "c", "q", {}, max_iterations=4)
    assert run.tool_result is not None and run.tool_result["ref"] == "document_2"
    assert run.evaluation.strict_pass


def test_a_first_turn_that_did_not_ask_is_not_recorded_as_asking() -> None:
    refusal = _chat_result(text="I could not find any charts on that topic.")
    expected = {"expects_clarification": True}
    run = _execute_single_document_run(_ScriptedChatClient([refusal, _drafting_turn()]), "c", "q", expected, 4)
    assert run.evaluation.strict_pass
    assert run.diagnostics == {"document_asked_first": False}


def test_a_structured_clarifying_question_counts_as_asking() -> None:
    question = _chat_result(parts=[{"type": "clarifyingQuestions", "questions": []}])
    expected = {"expects_clarification": True}
    run = _execute_single_document_run(_ScriptedChatClient([question, _drafting_turn()]), "c", "q", expected, 4)
    assert run.diagnostics == {"document_asked_first": True}


# ── page kinds, fixture keys, asking, two drafts in one turn ───────────────


def _page(page_id: str, kind: str | None, version: str = "v1") -> dict:
    page = _versioned_content(version, page_id, _REVENUE_TREND)
    if kind is None:
        del page["kind"]
    else:
        page["kind"] = kind
    return page


@pytest.mark.parametrize("version", _VERSIONS)
def test_a_document_that_does_not_open_with_a_cover_fails(version: str) -> None:
    pages = [_page("page1", "content", version), _page("page2", "content", version)]
    evaluation = _evaluate(_versioned_part(version, pages))
    assert evaluation.strict_checks["document_pages_consistent"] is False
    assert evaluation.failures == ["the document opens with a 'content' page, not a cover"]


@pytest.mark.parametrize("version", _VERSIONS)
def test_a_document_without_a_content_page_fails(version: str) -> None:
    evaluation = _evaluate(_versioned_part(version, [_versioned_cover(version), _page("page2", "section", version)]))
    assert evaluation.strict_checks["document_pages_consistent"] is False
    assert evaluation.failures == ["the document has no content page"]


def test_a_page_without_a_kind_is_a_content_page() -> None:
    assert _evaluate(_document_part([_cover_page(), _page("page2", None)])).strict_pass


@pytest.mark.parametrize("key", ["visualisations", "date_range", "narative"])
def test_an_unknown_fixture_key_is_rejected(key: str) -> None:
    with pytest.raises(ValueError, match=f"unknown expected_output key.*{key}"):
        _validate_expectation({key: "x"})


def test_an_expected_output_that_is_not_an_object_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    client = _ScriptedChatClient([])
    _install_client(monkeypatch, client)
    item = DatasetItem(
        id="i", dataset_name="ds", test_kind="agentic_document_skill", question="q", expected_output="a document"
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
    run = _execute_single_document_run(client, "c", "q", {"expects_clarification": True}, max_iterations=2)
    assert run.evaluation.strict_checks["document_drafted"] is False
    assert run.diagnostics == {"document_asked_first": True}


def test_asking_first_is_recorded_whenever_the_fixture_states_the_key() -> None:
    run = _execute_single_document_run(
        _ScriptedChatClient([_drafting_turn()]), "c", "q", {"expects_clarification": False}, max_iterations=4
    )
    assert run.diagnostics == {"document_asked_first": False}


def test_the_last_document_part_of_a_turn_is_the_one_scored() -> None:
    turn = _chat_result(
        tool_calls=[
            _tool_call("draft_document", _draft_result(ref="document_1")),
            _tool_call("draft_document", _draft_result(ref="document_2")),
        ],
        parts=[_document_part(ref="document_1"), _document_part(ref="document_2")],
    )
    run = _execute_single_document_run(_ScriptedChatClient([turn]), "c", "q", {}, max_iterations=4)
    assert run.document_part is not None and run.document_part["document_ref"] == "document_2"
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
        self.unscored: list[str] = []

    def export_unscored(self, _run_idx: int, conversation_id: str) -> None:
        self.unscored.append(conversation_id)

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
    monkeypatch.setattr(document_skill, "submit_trace_scoring", lambda _link, _identity, **kw: captured.update(kw))
    try:
        evaluate_agentic_document_skill(
            "https://h", "tok", "ws", "q", expected, langfuse=object(), dataset_item_id="item-1", **kwargs
        )
    except DocumentSkillAssertionError:
        pass  # scores are written before the gate raises
    ctx = _FakeCtx()
    captured["write_scores"](ctx)
    return ctx


def test_every_scored_check_reaches_langfuse_with_the_draft_facts(monkeypatch: pytest.MonkeyPatch) -> None:
    ctx = _scored(monkeypatch, {"period": _PERIOD, "expects_clarification": True}, [_drafting_turn()])
    checks = {name for name, kind in ctx.score_types.items() if kind == "BOOLEAN"}
    assert checks == {
        "document_drafted",
        "document_part_present",
        "document_ref_matches",
        "document_pages_consistent",
        "document_not_saved",
        "document_skill_activated",
        "document_wire_names",
        "document_period_correct",
        "document_asked_first",
        "pass_at_k",
        "pass_power_k",
        "gate_passed",
    }
    assert ctx.scores["document_summaries_from_data"] == 1
    assert ctx.score_types["document_summaries_from_data"] == "NUMERIC"
    assert "document_asked_first" not in ctx.quality_checks


def test_a_check_the_fixture_does_not_state_is_not_published(monkeypatch: pytest.MonkeyPatch) -> None:
    ctx = _scored(monkeypatch, {}, [_drafting_turn()])
    for absent in ("document_period_correct", "document_charts_matched", "document_asked_first"):
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


def _narrative_turn(*pages: dict, version: str = "v1") -> ChatResult:
    return _chat_result(
        tool_calls=[_tool_call("draft_document", _draft_result(page_count=len(pages)))],
        parts=[_versioned_part(version, list(pages))],
        text="I've put together a document.",
    )


def test_every_summary_slot_needs_written_text() -> None:
    pages = [_cover_page(), _summary_page("page2", "Revenue grew 12%.", _REVENUE_TREND), _summary_page("page3", "")]
    evaluation = _evaluate(_document_part(pages), expected={"narrative": _NARRATIVE}, tool=_draft_result(page_count=3))
    assert evaluation.strict_checks["document_summaries_present"] is False
    assert evaluation.failures == ["page 'page3' has a summary slot with no written text"]


def test_a_content_page_laid_out_without_a_summary_slot_is_fine() -> None:
    pages = [_cover_page(), _summary_page("page2", "Revenue grew 12%.", _REVENUE_TREND), _summary_page("page3", None)]
    evaluation = _evaluate(_document_part(pages), expected={"narrative": _NARRATIVE}, tool=_draft_result(page_count=3))
    assert evaluation.strict_checks["document_summaries_present"] is True


def test_a_static_text_slot_is_not_a_summary() -> None:
    page = _summary_page("page2", None, _REVENUE_TREND)
    page["layout"]["column"].append({"id": "text1", "weight": 1, "paragraph": "Left text."})
    evaluation = _evaluate(_document_part([_cover_page(), page]), expected={"narrative": _NARRATIVE})
    assert evaluation.strict_checks["document_summaries_present"] is False
    assert evaluation.failures == ["the document has no summary slot"]


def test_a_summary_made_only_of_placeholders_is_not_written() -> None:
    pages = [_cover_page(), _summary_page("page2", "{periodStart} – {periodEnd}", _REVENUE_TREND)]
    evaluation = _evaluate(_document_part(pages), expected={"narrative": _NARRATIVE})
    assert evaluation.strict_checks["document_summaries_present"] is False


def test_summaries_are_not_checked_unless_the_fixture_asks_for_the_narrative() -> None:
    evaluation = _evaluate(_document_part([_cover_page(), _summary_page("page2", None, _REVENUE_TREND)]))
    assert "document_summaries_present" not in evaluation.strict_checks
    assert "document_narrative_judged" not in evaluation.strict_checks


@pytest.mark.parametrize("version", _VERSIONS)
def test_the_judge_reads_the_document_as_text(version: str) -> None:
    judge = _FakeJudge()
    turn = _narrative_turn(
        _versioned_cover(version),
        _versioned_content(version, "page2", _REVENUE_TREND, summary="Revenue grew 12%."),
        version=version,
    )
    run = _execute_single_document_run(
        _ScriptedChatClient([turn]), "c", "Document on revenue", {"narrative": _NARRATIVE}, 4, judge=judge
    )
    assert run.evaluation.strict_checks["document_narrative_judged"] is True
    assert run.evaluation.strict_pass
    [call] = judge.calls
    assert call["input"] == "Document on revenue"
    assert call["expected_output"] == _NARRATIVE
    assert call["actual_output"] == (
        "Document: Sales overview\n"
        "Period: 2026-01-01 to 2026-06-30\n"
        "\n"
        "Page 2: Revenue\n"
        "Charts: revenue_trend\n"
        "Summary: Revenue grew 12%."
    )


def test_a_failing_verdict_fails_the_run_with_the_judges_reason() -> None:
    turn = _narrative_turn(_cover_page(), _summary_page("page2", "Revenue grew 12%.", _REVENUE_TREND))
    run = _execute_single_document_run(
        _ScriptedChatClient([turn]), "c", "q", {"narrative": _NARRATIVE}, 4, judge=_FakeJudge(passed=False)
    )
    assert run.evaluation.strict_checks["document_narrative_judged"] is False
    assert "the judge failed the narrative: the summaries ignore returns" in run.evaluation.failures


def test_no_document_means_no_judge_call_and_a_failed_narrative() -> None:
    judge = _FakeJudge()
    run = _execute_single_document_run(
        _ScriptedChatClient([_chat_result(text="Sorry.")]), "c", "q", {"narrative": _NARRATIVE}, 1, judge=judge
    )
    assert judge.calls == []
    assert run.evaluation.strict_checks["document_narrative_judged"] is False


def test_an_unreadable_verdict_leaves_the_run_unscored_not_passed() -> None:
    judge = _FakeJudge(error=JudgeResponseError("returned no 'score' key"))
    turn = _narrative_turn(_cover_page(), _summary_page("page2", "Revenue grew 12%.", _REVENUE_TREND))
    run = _execute_single_document_run(_ScriptedChatClient([turn]), "c", "q", {"narrative": _NARRATIVE}, 4, judge=judge)
    assert run.judge_error == "returned no 'score' key"
    assert "document_narrative_judged" not in run.evaluation.strict_checks
    assert not run.evaluation.strict_pass


def test_an_item_the_judge_could_never_grade_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    turn = _narrative_turn(_cover_page(), _summary_page("page2", "Revenue grew 12%.", _REVENUE_TREND))
    _install_client(monkeypatch, _ScriptedChatClient([turn]))
    judge = _FakeJudge(error=JudgeResponseError("empty body"))
    with pytest.raises(JudgeResponseError, match="no readable verdict") as raised:
        evaluate_agentic_document_skill("https://h", "tok", "ws", "q", {"narrative": _NARRATIVE}, judge=judge)
    assert len(raised.value.run_latencies_s) == 1


def test_a_narrative_item_passes_with_its_verdict_in_the_detail(monkeypatch: pytest.MonkeyPatch) -> None:
    turn = _narrative_turn(_cover_page(), _summary_page("page2", "Revenue grew 12%.", _REVENUE_TREND))
    _install_client(monkeypatch, _ScriptedChatClient([turn]))
    outcome = evaluate_agentic_document_skill(
        "https://h", "tok", "ws", "q", {"narrative": _NARRATIVE}, judge=_FakeJudge()
    )
    assert outcome.detail["document_narrative_judged"] is True
    assert outcome.detail["document_summaries_present"] is True
    assert outcome.detail["judge_reasoning"] == "fine"


def test_a_fixture_without_a_narrative_never_builds_a_judge(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    _install_client(monkeypatch, _ScriptedChatClient([_drafting_turn()]))
    outcome = evaluate_agentic_document_skill("https://h", "tok", "ws", "q", {})
    assert outcome.runs_passed == 1


def test_an_empty_narrative_is_rejected() -> None:
    with pytest.raises(ValueError, match="narrative must be a non-empty description"):
        _validate_expectation({"narrative": "  "})


def test_a_document_without_content_pages_has_no_summaries_to_present() -> None:
    closing = {**_cover_page(), "id": "page2", "kind": "closing"}
    evaluation = _evaluate(_document_part([_cover_page(), closing]), expected={"narrative": _NARRATIVE})
    assert evaluation.strict_checks["document_summaries_present"] is False
    assert evaluation.failures == ["the document has no content page", "the document has no summary slot"]


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
    summary = run_agentic_document_skill(
        "https://h", "tok", "ws", "q", {"narrative": _NARRATIVE}, k=2, judge=_SequenceJudge()
    )
    assert [r.judge_error for r in summary.run_results] == ["empty body", None]
    assert summary.pass_at_k
    assert not summary.pass_power_k, "pass^K cannot hold over a run nobody graded"
    assert summary.best.judge_error is None


def test_an_ungraded_run_writes_no_scores(monkeypatch: pytest.MonkeyPatch) -> None:
    ctx = _scored(monkeypatch, {"narrative": _NARRATIVE}, _narrative_turns(), k=2, judge=_SequenceJudge())
    assert ctx.observed == ["conv-2"]
    assert ctx.unscored == ["conv-1"]
    assert ctx.scores["document_narrative_judged"] == 1.0
    assert ctx.scores["document_summaries_present"] == 1.0


def _failing_narrative_turn() -> ChatResult:
    return _narrative_turn(_cover_page(), _summary_page("page2", "Revenue grew 12%.", _REVENUE_TREND))


def test_a_run_that_failed_a_fixed_check_is_a_failure_even_when_the_judge_errors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expected = {"narrative": _NARRATIVE, "visualizations": [{"id": _RETURNS_BY_CATEGORY, "title": "Returns"}]}
    _install_client(monkeypatch, _ScriptedChatClient([_failing_narrative_turn()]))
    judge = _FakeJudge(error=JudgeResponseError("empty body"))
    with pytest.raises(DocumentSkillAssertionError, match="does not show chart 'returns_by_category'"):
        evaluate_agentic_document_skill("https://h", "tok", "ws", "q", expected, judge=judge)


def test_a_failed_run_with_a_judge_error_is_published(monkeypatch: pytest.MonkeyPatch) -> None:
    expected = {"narrative": _NARRATIVE, "visualizations": [{"id": _RETURNS_BY_CATEGORY, "title": "Returns"}]}
    ctx = _scored(monkeypatch, expected, [_failing_narrative_turn()], judge=_FakeJudge(error=JudgeResponseError("x")))
    assert ctx.observed == ["conv-1"]
    assert ctx.scores["document_charts_matched"] == 0.0
    assert "document_narrative_judged" not in ctx.scores


def test_only_content_pages_count_for_summaries() -> None:
    cover = _cover_page()
    cover["layout"]["column"].append({"id": "summary", "weight": 1, "paragraph": {"text": "Revenue grew 12%."}})
    pages = [cover, _summary_page("page2", None, _REVENUE_TREND)]
    evaluation = _evaluate(_document_part(pages), expected={"narrative": _NARRATIVE})
    assert evaluation.strict_checks["document_summaries_present"] is False
    assert evaluation.failures == ["the document has no summary slot"]


# ── v2 documents ────────────────────────────────────────────────────────────

_V2_EXPECTED = {
    "period": _PERIOD,
    "visualizations": [{"id": _REVENUE_TREND, "title": "Revenue trend"}],
    "narrative": _NARRATIVE,
}


def _v2_written_pages() -> list[dict]:
    return [_v2_cover_page(), _v2_content_page("page2", _REVENUE_TREND, takeaway="Revenue grew 12%.")]


@pytest.mark.parametrize("form", ["entity", "flat", "sections"])
def test_a_v2_document_scores_on_every_check_whatever_form_holds_its_pages(form: str) -> None:
    evaluation = _evaluate(_v2_document_part(_v2_written_pages(), form=form), expected=_V2_EXPECTED)
    assert evaluation.failures == []
    assert evaluation.strict_checks["document_pages_consistent"] is True
    assert evaluation.strict_checks["document_period_correct"] is True
    assert evaluation.strict_checks["document_charts_matched"] is True
    assert evaluation.strict_checks["document_summaries_present"] is True


def test_sections_are_read_in_order_as_one_list_of_pages() -> None:
    pages = [
        _v2_cover_page(),
        _v2_content_page("page2", _REVENUE_TREND),
        _v2_content_page("page3", _RETURNS_BY_CATEGORY),
    ]
    document = _v2_document(pages, form="sections")
    assert _visualizations_of(document) == {_REVENUE_TREND, _RETURNS_BY_CATEGORY}
    assert render_document_text(document).splitlines()[3:] == [
        "Page 2: Revenue",
        "Charts: revenue_trend",
        "",
        "Page 3: Revenue",
        "Charts: returns_by_category",
    ]


def test_a_v2_document_that_does_not_open_with_a_cover_fails_across_sections() -> None:
    pages = [_v2_content_page("page1", _REVENUE_TREND), _v2_cover_page()]
    evaluation = _evaluate(_v2_document_part(pages, form="sections"))
    assert evaluation.failures == ["the document opens with a 'content' page, not a cover"]


def test_a_bare_visualization_id_is_matched_as_in_as_code() -> None:
    pages = [_v2_cover_page(), _v2_content_page("page2", _REVENUE_TREND, bare_ids=True)]
    expected = {"visualizations": [{"id": _REVENUE_TREND, "title": "Revenue trend"}]}
    assert _evaluate(_v2_document_part(pages), expected=expected).strict_checks["document_charts_matched"] is True


def test_a_relative_period_never_matches_the_expected_dates() -> None:
    relative = {"type": "relative", "granularity": "GDC.time.month", "from": -6, "to": -1}
    part = _v2_document_part(period=relative)
    evaluation = _evaluate(part, expected={"period": _PERIOD})
    assert evaluation.strict_checks["document_period_correct"] is False
    assert evaluation.failures == [
        "the document covers the relative range GDC.time.month -6 to -1, expected 2026-01-01 to 2026-06-30"
    ]
    assert render_document_text(part["document"]).splitlines()[1] == (
        "Period: the relative range GDC.time.month -6 to -1"
    )


def test_a_period_that_is_not_an_object_fails_instead_of_crashing() -> None:
    part = _v2_document_part()
    part["document"]["period"] = "last six months"
    evaluation = _evaluate(part, expected={"period": _PERIOD})
    assert evaluation.strict_checks["document_period_correct"] is False
    assert render_document_text(part["document"]).splitlines()[1] == "Period: None to None"


def test_every_takeaway_needs_written_text() -> None:
    pages = [*_v2_written_pages(), _v2_content_page("page3", _RETURNS_BY_CATEGORY, takeaway="")]
    evaluation = _evaluate(
        _v2_document_part(pages), expected={"narrative": _NARRATIVE}, tool=_draft_result(page_count=3)
    )
    assert evaluation.strict_checks["document_summaries_present"] is False
    assert evaluation.failures == ["page 'page3' has a takeaway with no written text"]


def test_a_takeaway_made_only_of_placeholders_is_not_written() -> None:
    pages = [_v2_cover_page(), _v2_content_page("page2", _REVENUE_TREND, takeaway="{periodStart} – {periodEnd}")]
    evaluation = _evaluate(_v2_document_part(pages), expected={"narrative": _NARRATIVE})
    assert evaluation.failures == ["page 'page2' has a takeaway with no written text"]


def _with_summary_text(page: dict, markdown: str | None) -> dict:
    """``page`` plus a page template's ``text`` widget with id ``summary``; ``None`` leaves its markdown out."""
    page["layout"]["children"].append(
        {"type": "text", "id": "summary", **({"markdown": markdown} if markdown is not None else {})}
    )
    return page


def test_a_v2_page_without_a_takeaway_is_summarised_by_its_summary_text() -> None:
    page = _with_summary_text(_v2_content_page("page2", _REVENUE_TREND), "Revenue grew 12%.")
    part = _v2_document_part([_v2_cover_page(), page])
    evaluation = _evaluate(part, expected={"narrative": _NARRATIVE})
    assert evaluation.strict_checks["document_summaries_present"] is True
    assert render_document_text(part["document"]).splitlines()[-1] == "Summary: Revenue grew 12%."


@pytest.mark.parametrize("markdown", ["", None])
def test_an_unwritten_summary_text_fails_when_the_page_has_no_takeaway(markdown: str | None) -> None:
    pages = [
        _v2_cover_page(),
        _v2_content_page("page2", _REVENUE_TREND, takeaway="Revenue grew 12%."),
        _with_summary_text(_v2_content_page("page3", _RETURNS_BY_CATEGORY), markdown),
    ]
    part = _v2_document_part(pages)
    evaluation = _evaluate(part, expected={"narrative": _NARRATIVE}, tool=_draft_result(page_count=3))
    assert evaluation.strict_checks["document_summaries_present"] is False
    assert evaluation.failures == ["page 'page3' has a text summary with no written text"]
    assert render_document_text(part["document"]).count("Summary:") == 1


def test_a_v2_document_without_a_takeaway_or_summary_text_has_no_summaries() -> None:
    evaluation = _evaluate(_v2_document_part(), expected={"narrative": _NARRATIVE})
    assert evaluation.strict_checks["document_summaries_present"] is False
    assert evaluation.failures == ["the document has no takeaway or text summary"]


def test_an_empty_summary_text_beside_a_written_takeaway_is_ignored() -> None:
    page = _with_summary_text(_v2_content_page("page2", _REVENUE_TREND, takeaway="Revenue grew 12%."), None)
    part = _v2_document_part([_v2_cover_page(), page])
    evaluation = _evaluate(part, expected={"narrative": _NARRATIVE})
    assert evaluation.strict_checks["document_summaries_present"] is True
    assert render_document_text(part["document"]).splitlines()[-1] == "Summary: Revenue grew 12%."


def test_a_written_summary_text_does_not_stand_in_for_an_empty_takeaway() -> None:
    page = _with_summary_text(_v2_content_page("page2", _REVENUE_TREND, takeaway=""), "Revenue grew 12%.")
    evaluation = _evaluate(_v2_document_part([_v2_cover_page(), page]), expected={"narrative": _NARRATIVE})
    assert evaluation.strict_checks["document_summaries_present"] is False
    assert evaluation.failures == ["page 'page2' has a takeaway with no written text"]


def test_every_takeaway_on_a_page_is_checked() -> None:
    page = _v2_content_page("page2", _REVENUE_TREND, takeaway="Revenue grew 12%.")
    page["layout"]["children"][1]["children"].append({"type": "takeaway", "id": "takeaway2"})
    evaluation = _evaluate(_v2_document_part([_v2_cover_page(), page]), expected={"narrative": _NARRATIVE})
    assert evaluation.strict_checks["document_summaries_present"] is False
    assert evaluation.failures == ["page 'page2' has a takeaway with no written text"]


def test_a_v2_heading_widget_is_a_page_heading() -> None:
    page = _v2_content_page("page2", _REVENUE_TREND)
    page["layout"]["children"][0] = {"type": "heading", "id": "pageHeading", "markdown": "Returns", "level": 1}
    document = _v2_document([_v2_cover_page(), page])
    assert render_document_text(document).splitlines()[3] == "Page 2: Returns"


def test_sections_win_over_pages_when_a_document_has_both() -> None:
    document = _v2_document([_v2_cover_page(), _v2_content_page("page2", _REVENUE_TREND)], form="sections")
    document["content"]["pages"] = [_v2_cover_page(), _v2_content_page("page9", _RETURNS_BY_CATEGORY)]
    assert _visualizations_of(document) == {_REVENUE_TREND}


def test_a_layout_whose_children_is_not_a_list_is_read_as_a_leaf() -> None:
    page = _v2_content_page("page2", _REVENUE_TREND)
    page["layout"]["children"].append({"type": "row", "children": 5})
    assert _visualizations_of(_v2_document([_v2_cover_page(), page])) == {_REVENUE_TREND}


def _hidden(page: dict) -> dict:
    return {**page, "visible": False}


def _pages_with_a_hidden_one() -> list[dict]:
    return [
        _v2_cover_page(),
        _hidden(_v2_content_page("page2", _RETURNS_BY_CATEGORY, takeaway="")),
        _v2_content_page("page3", _REVENUE_TREND, takeaway="Revenue grew 12%."),
    ]


def test_a_hidden_page_is_left_out_of_every_check_and_of_the_judge_text() -> None:
    part = _v2_document_part(_pages_with_a_hidden_one())
    evaluation = _evaluate(part, expected={"narrative": _NARRATIVE}, tool=_draft_result(page_count=2))
    assert evaluation.failures == []
    assert evaluation.strict_checks["document_pages_consistent"] is True
    assert evaluation.strict_checks["document_summaries_present"] is True
    assert _visualizations_of(part["document"]) == {_REVENUE_TREND}
    assert render_document_text(part["document"]) == (
        "Document: Sales overview\n"
        "Period: 2026-01-01 to 2026-06-30\n"
        "\n"
        "Page 2: Revenue\n"
        "Charts: revenue_trend\n"
        "Summary: Revenue grew 12%."
    )


def test_a_page_count_that_includes_a_hidden_page_fails() -> None:
    evaluation = _evaluate(
        _v2_document_part(_pages_with_a_hidden_one(), page_count=3), tool=_draft_result(page_count=3)
    )
    assert evaluation.strict_checks["document_pages_consistent"] is False
    assert evaluation.failures == ["the document has 2 page(s), but the part says 3 and draft_document said 3"]


def test_a_hidden_cover_does_not_open_the_document() -> None:
    pages = [_hidden(_v2_cover_page()), _v2_content_page("page2", _REVENUE_TREND)]
    evaluation = _evaluate(_v2_document_part(pages), tool=_draft_result(page_count=1))
    assert evaluation.strict_checks["document_pages_consistent"] is False
    assert evaluation.failures == ["the document opens with a 'content' page, not a cover"]


def test_a_document_whose_only_content_page_is_hidden_has_no_content_page() -> None:
    pages = [_v2_cover_page(), _hidden(_v2_content_page("page2", _REVENUE_TREND))]
    evaluation = _evaluate(_v2_document_part(pages), tool=_draft_result(page_count=1))
    assert evaluation.failures == ["the document has no content page"]


def test_the_report_skill_module_still_exports_the_old_names() -> None:
    with pytest.warns(DeprecationWarning, match="gooddata_eval.core.agentic.document_skill"):
        report_skill = importlib.reload(importlib.import_module("gooddata_eval.core.agentic.report_skill"))

    assert report_skill.evaluate_agentic_report_skill is evaluate_agentic_document_skill
    assert report_skill.run_agentic_report_skill is run_agentic_document_skill
    assert report_skill.ReportSkillAssertionError is DocumentSkillAssertionError
    assert report_skill.ReportEvaluation is DocumentEvaluation
    assert report_skill.ReportRunResult is document_skill.DocumentRunResult
    assert report_skill.AgenticReportSummary is document_skill.AgenticDocumentSummary
    assert report_skill.evaluate_report_response is evaluate_document_response
    assert report_skill.render_report_text is document_skill.render_document_text
    assert report_skill.build_simulated_reply is build_simulated_reply


def test_the_package_still_exports_the_old_names() -> None:
    assert agentic.evaluate_agentic_report_skill is agentic.evaluate_agentic_document_skill
    assert agentic.ReportSkillAssertionError is agentic.DocumentSkillAssertionError

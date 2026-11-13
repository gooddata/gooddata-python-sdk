# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
import importlib
import json
from collections.abc import Iterator
from contextlib import contextmanager
from types import SimpleNamespace
from typing import Any

import httpx
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
from gooddata_eval.core.models import ChatResult, DatasetItem, TakeawayInput

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
    reworks_open_document: bool = False,
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
        "reworks_open_document": reworks_open_document,
    }


# v2 shapes follow the AaC form a v2 draft arrives in: a top-level `version`, an absolute `{from, to}`
# or relative `{granularity, from, to}` `period`, and `content` holding the pages, whose layout nests
# `row` and `column` containers through `children` down to typed widgets.
_V2_PERIOD = {"from": "2026-01-01", "to": "2026-06-30"}


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
        "document_new_draft": True,
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
    assert evaluation.strict_checks["document_new_draft"] is True
    assert evaluation.failures == [
        "a new draft must not be saved yet, but it reports saved_document_id 'sales_overview'"
    ]


def test_a_new_draft_must_not_edit_a_saved_document() -> None:
    evaluation = _evaluate(_document_part(base_document_id="q3_review"))
    assert evaluation.strict_checks["document_new_draft"] is False
    assert evaluation.strict_checks["document_not_saved"] is True
    assert evaluation.failures == [
        "a new draft must not edit a saved document, but it reports base_document_id 'q3_review'"
    ]


def test_a_new_draft_must_not_rework_the_open_document() -> None:
    evaluation = _evaluate(_document_part(reworks_open_document=True))
    assert evaluation.strict_checks["document_new_draft"] is False
    assert evaluation.strict_checks["document_not_saved"] is True
    assert evaluation.failures == [
        "a new draft must not rework the open document, but it reports reworks_open_document"
    ]


# ── rework of the open document ─────────────────────────────────────────────
# A rework is scored on aac-v2 documents only, so these build v2 parts.

_OPEN_DOCUMENT = "q3_review"
# Keyed by filter id, as gen-ai drafts a v2 document's content.filters.
_OPEN_FILTERS = {
    "document_filter_customer_country": {
        "type": "attribute_filter",
        "title": "Customer country",
        "using": "label/customer_country",
        "multiselect": False,
    }
}


def _rework_part(pages: list[dict] | None = None, **kwargs: Any) -> dict:
    kwargs.setdefault("base_document_id", _OPEN_DOCUMENT)
    kwargs.setdefault("reworks_open_document", True)
    return _v2_document_part(pages, **kwargs)


def _with_filters(part: dict, filters: Any) -> dict:
    part["document"]["content"]["filters"] = filters
    return part


def test_an_edit_of_the_open_document_passes_every_rework_check() -> None:
    pages = [
        _v2_cover_page(),
        _v2_content_page("page2", _REVENUE_TREND),
        _v2_content_page("page3", _RETURNS_BY_CATEGORY),
    ]
    part = _with_filters(_rework_part(pages), _OPEN_FILTERS)
    expected = {
        "period": _PERIOD,
        "rework": {
            "base_document_id": _OPEN_DOCUMENT,
            "keeps_pages": ["page1", "page2"],
            "page_charts": {"page2": [_REVENUE_TREND]},
            "title": "Sales overview",
            "filters": _OPEN_FILTERS,
        },
    }
    evaluation = _evaluate(part, expected=expected, tool=_draft_result(page_count=3))
    assert evaluation.failures == []
    assert evaluation.strict_pass
    assert evaluation.strict_checks == {
        "document_drafted": True,
        "document_part_present": True,
        "document_ref_matches": True,
        "document_pages_consistent": True,
        "document_not_saved": True,
        "document_skill_activated": True,
        "document_wire_names": True,
        "document_period_correct": True,
        "document_reworks_open": True,
        "document_pages_kept": True,
        "document_page_charts_kept": True,
        "document_title_correct": True,
        "document_filters_kept": True,
    }


def test_every_rework_check_is_published_when_the_fixture_states_it() -> None:
    pages = [
        _v2_cover_page(),
        _v2_content_page("page2", _REVENUE_TREND),
        _v2_content_page("page3", _RETURNS_BY_CATEGORY),
    ]
    rework = {**_NEW_PAGE_REWORK, "page_charts": {"page2": [_REVENUE_TREND]}, "filters": _US_ONLY}
    part = _with_filters(_rework_part(pages), _drafted_country_filter())
    evaluation = _evaluate(part, expected={"rework": rework}, tool=_draft_result(page_count=3))
    assert evaluation.failures == []
    assert {"document_new_page_charts_placed", "document_page_charts_kept", "document_filters_kept"} <= set(
        evaluation.strict_checks
    )


def test_a_rework_of_a_v1_document_fails_once_and_says_why() -> None:
    expected = {"rework": {"base_document_id": _OPEN_DOCUMENT, "keeps_pages": ["page1"], "title": "Sales overview"}}
    evaluation = _evaluate(_document_part(base_document_id=_OPEN_DOCUMENT), expected=expected)
    assert evaluation.failures == ["a rework is scored on aac-v2 documents only, but the draft is version None"]
    assert evaluation.strict_checks["document_reworks_open"] is False
    assert evaluation.strict_checks["document_pages_kept"] is False
    assert evaluation.strict_checks["document_title_correct"] is False


def test_a_new_draft_where_an_edit_was_expected_fails() -> None:
    evaluation = _evaluate(_v2_document_part(), expected={"rework": {"base_document_id": _OPEN_DOCUMENT}})
    assert evaluation.strict_checks["document_reworks_open"] is False
    assert evaluation.failures == [
        "the edit must apply to the open document 'q3_review', but it reports base_document_id None",
        "the edit must be written from the open document, but reworks_open_document is not true",
    ]


def test_an_edit_of_another_document_fails() -> None:
    part = _rework_part(base_document_id="another_document")
    evaluation = _evaluate(part, expected={"rework": {"base_document_id": _OPEN_DOCUMENT}})
    assert evaluation.strict_checks["document_reworks_open"] is False
    assert evaluation.failures == [
        "the edit must apply to the open document 'q3_review', but it reports base_document_id 'another_document'"
    ]


def test_an_edit_not_written_from_the_open_document_fails() -> None:
    part = _rework_part(reworks_open_document=False)
    evaluation = _evaluate(part, expected={"rework": {"base_document_id": _OPEN_DOCUMENT}})
    assert evaluation.strict_checks["document_reworks_open"] is False
    assert evaluation.failures == [
        "the edit must be written from the open document, but reworks_open_document is not true"
    ]


def test_an_edit_must_not_be_saved_yet() -> None:
    part = _rework_part(saved_document_id=_OPEN_DOCUMENT)
    evaluation = _evaluate(part, expected={"rework": {"base_document_id": _OPEN_DOCUMENT}})
    assert evaluation.strict_checks["document_not_saved"] is False
    assert evaluation.failures == ["an edit must not be saved yet, but it reports saved_document_id 'q3_review'"]


def test_an_edit_that_drops_a_page_of_the_open_document_fails_and_names_it() -> None:
    expected = {"rework": {"base_document_id": _OPEN_DOCUMENT, "keeps_pages": ["page1", "page2", "page3"]}}
    evaluation = _evaluate(_rework_part(), expected=expected)
    assert evaluation.strict_checks["document_pages_kept"] is False
    assert evaluation.failures == ["the edit lost page 'page3' of the open document"]


def test_a_hidden_page_counts_as_lost() -> None:
    hidden = {**_v2_content_page("page3", _RETURNS_BY_CATEGORY), "visible": False}
    pages = [_v2_cover_page(), _v2_content_page("page2", _REVENUE_TREND), hidden]
    expected = {"rework": {"base_document_id": _OPEN_DOCUMENT, "keeps_pages": ["page3"]}}
    evaluation = _evaluate(_rework_part(pages), expected=expected)
    assert evaluation.failures == ["the edit lost page 'page3' of the open document"]


def test_pages_in_sections_are_found() -> None:
    expected = {"rework": {"base_document_id": _OPEN_DOCUMENT, "keeps_pages": ["page1", "page2"]}}
    evaluation = _evaluate(_rework_part(form="sections"), expected=expected)
    assert evaluation.strict_checks["document_pages_kept"] is True


def test_an_edit_that_moved_a_chart_off_its_page_fails_and_names_both() -> None:
    pages = [
        _v2_cover_page(),
        _v2_content_page("page2", _RETURNS_BY_CATEGORY),
        _v2_content_page("page3", _REVENUE_TREND),
    ]
    expected = {
        "rework": {
            "base_document_id": _OPEN_DOCUMENT,
            "keeps_pages": ["page2"],
            "page_charts": {"page2": [_REVENUE_TREND]},
        }
    }
    evaluation = _evaluate(_rework_part(pages), expected=expected, tool=_draft_result(page_count=3))
    assert evaluation.strict_checks["document_pages_kept"] is True
    assert evaluation.strict_checks["document_page_charts_kept"] is False
    assert evaluation.failures == ["chart 'revenue_trend' is no longer on page 'page2' of the open document"]


def test_a_kept_page_may_hold_more_charts_than_the_fixture_lists() -> None:
    pages = [_v2_cover_page(), _v2_content_page("page2", _REVENUE_TREND, _RETURNS_BY_CATEGORY)]
    expected = {
        "rework": {
            "base_document_id": _OPEN_DOCUMENT,
            "keeps_pages": ["page2"],
            "page_charts": {"page2": [_REVENUE_TREND]},
        }
    }
    evaluation = _evaluate(_rework_part(pages), expected=expected)
    assert evaluation.strict_checks["document_page_charts_kept"] is True
    assert evaluation.failures == []


def test_a_lost_page_also_loses_the_charts_listed_for_it() -> None:
    expected = {
        "rework": {
            "base_document_id": _OPEN_DOCUMENT,
            "keeps_pages": ["page3"],
            "page_charts": {"page3": [_REVENUE_TREND]},
        }
    }
    evaluation = _evaluate(_rework_part(), expected=expected)
    assert evaluation.strict_checks["document_page_charts_kept"] is False
    assert evaluation.failures == [
        "the edit lost page 'page3' of the open document",
        "chart 'revenue_trend' is no longer on page 'page3' of the open document",
    ]


def test_a_chart_on_a_hidden_page_is_not_kept() -> None:
    hidden = {**_v2_content_page("page2", _REVENUE_TREND), "visible": False}
    pages = [_v2_cover_page(), hidden, _v2_content_page("page3", _RETURNS_BY_CATEGORY)]
    expected = {
        "rework": {
            "base_document_id": _OPEN_DOCUMENT,
            "keeps_pages": ["page2"],
            "page_charts": {"page2": [_REVENUE_TREND]},
        }
    }
    evaluation = _evaluate(_rework_part(pages), expected=expected)
    assert evaluation.strict_checks["document_page_charts_kept"] is False


def test_page_charts_are_found_in_sections() -> None:
    expected = {
        "rework": {
            "base_document_id": _OPEN_DOCUMENT,
            "keeps_pages": ["page2"],
            "page_charts": {"page2": [_REVENUE_TREND]},
        }
    }
    evaluation = _evaluate(_rework_part(form="sections"), expected=expected)
    assert evaluation.strict_checks["document_page_charts_kept"] is True


def test_a_rename_that_left_the_old_title_fails() -> None:
    expected = {"rework": {"base_document_id": _OPEN_DOCUMENT, "title": "E2 Sales Review"}}
    evaluation = _evaluate(_rework_part(), expected=expected)
    assert evaluation.strict_checks["document_title_correct"] is False
    assert evaluation.failures == ["the document is titled 'Sales overview', expected 'E2 Sales Review'"]


def test_an_edit_that_dropped_a_document_filter_fails() -> None:
    part = _with_filters(_rework_part(), {})
    expected = {"rework": {"base_document_id": _OPEN_DOCUMENT, "filters": _OPEN_FILTERS}}
    evaluation = _evaluate(part, expected=expected)
    assert evaluation.strict_checks["document_filters_kept"] is False
    assert evaluation.failures == ["the edit lost filter 'document_filter_customer_country'"]


# What a rework item states: the filter's kind, label and selection, not its display fields.
_US_ONLY = {
    "document_filter_customer_country": {
        "type": "attribute_filter",
        "using": "label/customer_country",
        "state": {"include": ["United States"]},
    }
}


def _drafted_country_filter(**changes: Any) -> dict:
    drafted = {
        "type": "attribute_filter",
        "title": "Customer country",
        "using": "label/customer_country",
        "multiselect": False,
        "state": {"include": ["United States"]},
    }
    drafted.update(changes)
    return {"document_filter_customer_country": {k: v for k, v in drafted.items() if v is not None}}


@pytest.mark.parametrize(
    "drafted",
    [
        _drafted_country_filter(),
        _drafted_country_filter(localIdentifier="f1"),
        _drafted_country_filter(title=None, multiselect=None),
        _drafted_country_filter(title="Country"),
    ],
    ids=["as-drafted", "extra-key", "display-keys-dropped", "retitled"],
)
def test_a_filter_is_compared_only_on_the_keys_the_fixture_states(drafted: dict) -> None:
    part = _with_filters(_rework_part(), drafted)
    expected = {"rework": {"base_document_id": _OPEN_DOCUMENT, "filters": _US_ONLY}}
    evaluation = _evaluate(part, expected=expected)
    assert evaluation.failures == []
    assert evaluation.strict_checks["document_filters_kept"] is True


@pytest.mark.parametrize(
    ("drafted", "failure"),
    [
        (
            _drafted_country_filter(state={}),
            "filter 'document_filter_customer_country' selects all, expected include ['United States']",
        ),
        (
            _drafted_country_filter(state={"include": []}),
            "filter 'document_filter_customer_country' selects all, expected include ['United States']",
        ),
        (
            _drafted_country_filter(state={"include": ["Canada"]}),
            "filter 'document_filter_customer_country' selects include ['Canada'], expected include ['United States']",
        ),
        (
            _drafted_country_filter(state={"exclude": ["United States"]}),
            "filter 'document_filter_customer_country' selects exclude ['United States'], "
            "expected include ['United States']",
        ),
        (
            _drafted_country_filter(using="label/customer_state"),
            "filter 'document_filter_customer_country' has using 'label/customer_state', "
            "expected 'label/customer_country'",
        ),
    ],
    ids=["selection-dropped", "selection-emptied", "other-value", "inverted", "other-label"],
)
def test_a_filter_that_changed_what_it_selects_fails(drafted: dict, failure: str) -> None:
    part = _with_filters(_rework_part(), drafted)
    expected = {"rework": {"base_document_id": _OPEN_DOCUMENT, "filters": _US_ONLY}}
    evaluation = _evaluate(part, expected=expected)
    assert evaluation.strict_checks["document_filters_kept"] is False
    assert evaluation.failures == [failure]


def test_an_edit_that_added_a_document_filter_fails() -> None:
    drafted = {**_drafted_country_filter(), "document_filter_product_category": {"type": "attribute_filter"}}
    part = _with_filters(_rework_part(), drafted)
    expected = {"rework": {"base_document_id": _OPEN_DOCUMENT, "filters": _US_ONLY}}
    evaluation = _evaluate(part, expected=expected)
    assert evaluation.strict_checks["document_filters_kept"] is False
    assert evaluation.failures == ["the edit added filter 'document_filter_product_category'"]


def test_a_filter_of_another_kind_fails() -> None:
    drafted = _drafted_country_filter(type="text_filter")
    part = _with_filters(_rework_part(), drafted)
    expected = {"rework": {"base_document_id": _OPEN_DOCUMENT, "filters": _US_ONLY}}
    evaluation = _evaluate(part, expected=expected)
    assert evaluation.strict_checks["document_filters_kept"] is False
    assert evaluation.failures == [
        "filter 'document_filter_customer_country' has type 'text_filter', expected 'attribute_filter'"
    ]


_ALL_TIME = {"document_filter_date": {"type": "date_filter", "granularity": "YEAR", "date": "date"}}


@pytest.mark.parametrize(
    ("drafted", "failure"),
    [
        (
            {"type": "date_filter", "granularity": "YEAR", "date": "date", "from": -1, "to": -1},
            "filter 'document_filter_date' has from -1, expected None",
        ),
        (
            {"type": "date_filter", "granularity": "MONTH", "date": "date"},
            "filter 'document_filter_date' has granularity 'MONTH', expected 'YEAR'",
        ),
    ],
    ids=["range-added", "other-granularity"],
)
def test_a_date_filter_left_all_time_fails_on_a_drafted_range(drafted: dict, failure: str) -> None:
    part = _with_filters(_rework_part(), {"document_filter_date": drafted})
    expected = {"rework": {"base_document_id": _OPEN_DOCUMENT, "filters": _ALL_TIME}}
    evaluation = _evaluate(part, expected=expected)
    assert evaluation.strict_checks["document_filters_kept"] is False
    assert failure in evaluation.failures


def test_a_date_range_stated_without_granularity_fails_on_a_drafted_granularity() -> None:
    drafted = {
        "document_filter_date": {"type": "date_filter", "granularity": "MONTH", "date": "date", "from": -1, "to": -1}
    }
    part = _with_filters(_rework_part(), drafted)
    expected = {
        "rework": {
            "base_document_id": _OPEN_DOCUMENT,
            "filters": {"document_filter_date": {"type": "date_filter", "date": "date", "from": -1, "to": -1}},
        }
    }
    evaluation = _evaluate(part, expected=expected)
    assert evaluation.strict_checks["document_filters_kept"] is False
    assert evaluation.failures == ["filter 'document_filter_date' has granularity 'MONTH', expected None"]


def test_a_date_filter_kept_all_time_passes() -> None:
    part = _with_filters(_rework_part(), {"document_filter_date": dict(_ALL_TIME["document_filter_date"])})
    expected = {"rework": {"base_document_id": _OPEN_DOCUMENT, "filters": _ALL_TIME}}
    evaluation = _evaluate(part, expected=expected)
    assert evaluation.failures == []
    assert evaluation.strict_checks["document_filters_kept"] is True


@pytest.mark.parametrize("dataset", ["customer_created_date", None], ids=["other-dataset", "dataset-dropped"])
def test_a_date_filter_moved_off_its_date_dataset_fails(dataset: str | None) -> None:
    drafted = {k: v for k, v in _ALL_TIME["document_filter_date"].items() if k != "date"}
    if dataset is not None:
        drafted["date"] = dataset
    part = _with_filters(_rework_part(), {"document_filter_date": drafted})
    expected = {"rework": {"base_document_id": _OPEN_DOCUMENT, "filters": _ALL_TIME}}
    evaluation = _evaluate(part, expected=expected)
    assert evaluation.strict_checks["document_filters_kept"] is False
    assert evaluation.failures == [f"filter 'document_filter_date' has date {dataset!r}, expected 'date'"]


@pytest.mark.parametrize(
    ("drafted", "problem"),
    [
        (["United States"], "expected an object"),
        ("United States", "expected an object"),
        ({"include": 1}, "expected a list of values under 'include'"),
        ({"exclude": "Canada"}, "expected a list of values under 'exclude'"),
        ([], "expected an object"),
        ("", "expected an object"),
        (False, "expected an object"),
        (
            {"include": ["United States"], "exclude": ["Canada"]},
            "expected either 'include' or 'exclude', not both",
        ),
        ({"values": ["United States"]}, "expected only 'include' or 'exclude'"),
    ],
    ids=[
        "list",
        "string",
        "include-not-a-list",
        "exclude-not-a-list",
        "empty-list",
        "empty-string",
        "false",
        "both",
        "unknown-key",
    ],
)
def test_a_drafted_state_that_is_not_a_selection_fails(drafted: Any, problem: str) -> None:
    part = _with_filters(_rework_part(), _drafted_country_filter(state=drafted))
    expected = {"rework": {"base_document_id": _OPEN_DOCUMENT, "filters": _US_ONLY}}
    evaluation = _evaluate(part, expected=expected)
    assert evaluation.strict_checks["document_filters_kept"] is False
    assert evaluation.failures == [f"filter 'document_filter_customer_country' has state {drafted!r}, {problem}"]


@pytest.mark.parametrize("drafted", [[], "", False], ids=["empty-list", "empty-string", "false"])
def test_a_falsey_drafted_state_does_not_pass_as_all(drafted: Any) -> None:
    unrestricted = {"type": "attribute_filter", "using": "label/customer_country", "state": {}}
    part = _with_filters(_rework_part(), _drafted_country_filter(state=drafted))
    expected = {
        "rework": {"base_document_id": _OPEN_DOCUMENT, "filters": {"document_filter_customer_country": unrestricted}}
    }
    evaluation = _evaluate(part, expected=expected)
    assert evaluation.strict_checks["document_filters_kept"] is False


@pytest.mark.parametrize(
    ("drafted", "kept"), [(None, True), ({"include": ["United States"]}, False)], ids=["all", "one-value"]
)
def test_a_null_expected_state_means_all(drafted: Any, kept: bool) -> None:
    unrestricted = {"type": "attribute_filter", "using": "label/customer_country", "state": None}
    part = _with_filters(_rework_part(), _drafted_country_filter(state=drafted))
    expected = {
        "rework": {"base_document_id": _OPEN_DOCUMENT, "filters": {"document_filter_customer_country": unrestricted}}
    }
    evaluation = _evaluate(part, expected=expected)
    assert evaluation.strict_checks["document_filters_kept"] is kept


def test_a_selection_is_compared_without_its_order() -> None:
    both = {
        "type": "attribute_filter",
        "using": "label/customer_country",
        "state": {"include": ["United States", "Canada"]},
    }
    reordered = _drafted_country_filter(state={"include": ["Canada", "United States"]})
    part = _with_filters(_rework_part(), reordered)
    expected = {"rework": {"base_document_id": _OPEN_DOCUMENT, "filters": {"document_filter_customer_country": both}}}
    evaluation = _evaluate(part, expected=expected)
    assert evaluation.failures == []
    assert evaluation.strict_checks["document_filters_kept"] is True


def test_a_selection_with_a_value_missing_fails() -> None:
    both = {
        "type": "attribute_filter",
        "using": "label/customer_country",
        "state": {"include": ["United States", "Canada"]},
    }
    part = _with_filters(_rework_part(), _drafted_country_filter())
    expected = {"rework": {"base_document_id": _OPEN_DOCUMENT, "filters": {"document_filter_customer_country": both}}}
    evaluation = _evaluate(part, expected=expected)
    assert evaluation.strict_checks["document_filters_kept"] is False
    assert evaluation.failures == [
        "filter 'document_filter_customer_country' selects include ['United States'], "
        "expected include ['United States', 'Canada']"
    ]


@pytest.mark.parametrize("drafted", [[{"type": "attribute_filter"}], "none"], ids=["list", "string"])
def test_drafted_filters_that_are_not_keyed_by_id_fail_an_expectation_of_none(drafted: Any) -> None:
    part = _with_filters(_rework_part(), drafted)
    expected = {"rework": {"base_document_id": _OPEN_DOCUMENT, "filters": {}}}
    evaluation = _evaluate(part, expected=expected)
    assert evaluation.strict_checks["document_filters_kept"] is False
    assert evaluation.failures == [f"the document filters are {drafted!r}, expected an object keyed by filter id"]


def test_a_text_filter_state_is_compared_as_written() -> None:
    expected_filter = {"document_filter_city": {"type": "text_filter", "state": {"values": ["Prague"]}}}
    drafted = {"document_filter_city": {"type": "text_filter", "state": {"values": ["Brno"]}}}
    evaluation = _evaluate(
        _with_filters(_rework_part(), drafted),
        expected={"rework": {"base_document_id": _OPEN_DOCUMENT, "filters": expected_filter}},
    )
    assert evaluation.failures == [
        "filter 'document_filter_city' has state {'values': ['Brno']}, expected {'values': ['Prague']}"
    ]


# ── a chart the edit adds on a new page ─────────────────────────────────────

_NEW_PAGE_REWORK = {
    "base_document_id": _OPEN_DOCUMENT,
    "keeps_pages": ["page1", "page2"],
    "new_page_charts": [_RETURNS_BY_CATEGORY],
}


def test_a_chart_on_a_new_page_passes() -> None:
    pages = [
        _v2_cover_page(),
        _v2_content_page("page2", _REVENUE_TREND),
        _v2_content_page("page3", _RETURNS_BY_CATEGORY),
    ]
    evaluation = _evaluate(_rework_part(pages), expected={"rework": _NEW_PAGE_REWORK}, tool=_draft_result(page_count=3))
    assert evaluation.failures == []
    assert evaluation.strict_checks["document_new_page_charts_placed"] is True


def test_a_chart_pushed_onto_an_old_page_fails() -> None:
    pages = [_v2_cover_page(), _v2_content_page("page2", _REVENUE_TREND, _RETURNS_BY_CATEGORY)]
    evaluation = _evaluate(_rework_part(pages), expected={"rework": _NEW_PAGE_REWORK})
    assert evaluation.strict_checks["document_new_page_charts_placed"] is False
    assert evaluation.failures == [
        "chart 'returns_by_category' must be on a new page, but it is only on page(s) ['page2'] of the open document"
    ]


def test_a_chart_on_both_an_old_and_a_new_page_passes() -> None:
    pages = [
        _v2_cover_page(),
        _v2_content_page("page2", _REVENUE_TREND, _RETURNS_BY_CATEGORY),
        _v2_content_page("page3", _RETURNS_BY_CATEGORY),
    ]
    evaluation = _evaluate(_rework_part(pages), expected={"rework": _NEW_PAGE_REWORK}, tool=_draft_result(page_count=3))
    assert evaluation.strict_checks["document_new_page_charts_placed"] is True


def test_a_chart_on_a_hidden_new_page_fails() -> None:
    hidden = _v2_content_page("page3", _RETURNS_BY_CATEGORY)
    hidden["visible"] = False
    pages = [_v2_cover_page(), _v2_content_page("page2", _REVENUE_TREND), hidden]
    evaluation = _evaluate(_rework_part(pages), expected={"rework": _NEW_PAGE_REWORK})
    assert evaluation.strict_checks["document_new_page_charts_placed"] is False
    assert evaluation.failures == ["chart 'returns_by_category' must be on a new page, but no visible page has it"]


def test_a_document_without_filters_keeps_an_expectation_of_none() -> None:
    expected = {"rework": {"base_document_id": _OPEN_DOCUMENT, "filters": {}}}
    evaluation = _evaluate(_rework_part(), expected=expected)
    assert evaluation.strict_checks["document_filters_kept"] is True


def test_rework_checks_are_published_only_for_what_the_fixture_states() -> None:
    evaluation = _evaluate(_rework_part(), expected={"rework": {"base_document_id": _OPEN_DOCUMENT}})
    assert "document_reworks_open" in evaluation.strict_checks
    for name in (
        "document_pages_kept",
        "document_page_charts_kept",
        "document_new_page_charts_placed",
        "document_title_correct",
        "document_filters_kept",
    ):
        assert name not in evaluation.strict_checks
    assert evaluation.strict_pass


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


@pytest.mark.parametrize(
    ("user_context", "message"),
    [
        (None, "rework needs the open document in user_context.view.document"),
        ({"view": {"dashboard": {"id": "d1"}}}, "rework needs the open document in user_context.view.document"),
        ({"view": {"document": {"title": "Q3 review"}}}, "rework needs the open document's id"),
        ({"view": {"document": {"id": "another_document"}}}, "rework.base_document_id 'q3_review' is not the open"),
    ],
)
def test_a_rework_that_does_not_match_the_open_document_fails_before_any_request(
    monkeypatch: pytest.MonkeyPatch, user_context: dict | None, message: str
) -> None:
    client = _ScriptedChatClient([_drafting_turn()])
    _install_client(monkeypatch, client)
    expected = {"rework": {"base_document_id": _OPEN_DOCUMENT}}
    with pytest.raises(ValueError, match=message):
        run_agentic_document_skill("https://h", "tok", "ws", "Rename it", expected, user_context=user_context)
    assert client.sent == []


def _open_document_with(pages: list[dict]) -> dict:
    return {"view": {"document": {"id": _OPEN_DOCUMENT, "definition": _v2_document(pages)}}}


def test_a_new_page_rework_must_list_every_open_page(monkeypatch: pytest.MonkeyPatch) -> None:
    client = _ScriptedChatClient([_drafting_turn()])
    _install_client(monkeypatch, client)
    user_context = _open_document_with([_v2_cover_page(), _v2_content_page("page2", _REVENUE_TREND)])
    expected = {"rework": {**_NEW_PAGE_REWORK, "keeps_pages": ["page1"]}}
    with pytest.raises(ValueError, match=r"keeps_pages to list every page of the open document; missing \['page2'\]"):
        run_agentic_document_skill("https://h", "tok", "ws", "Add a page", expected, user_context=user_context)
    assert client.sent == []


def test_a_new_page_rework_without_the_open_pages_fails_before_any_request(monkeypatch: pytest.MonkeyPatch) -> None:
    client = _ScriptedChatClient([_drafting_turn()])
    _install_client(monkeypatch, client)
    user_context = {"view": {"document": {"id": _OPEN_DOCUMENT, "title": "Q3 review"}}}
    with pytest.raises(ValueError, match="needs the open document's pages"):
        run_agentic_document_skill(
            "https://h", "tok", "ws", "Add a page", {"rework": _NEW_PAGE_REWORK}, user_context=user_context
        )
    assert client.sent == []


def test_a_new_page_rework_over_a_hidden_open_page_fails_before_any_request(monkeypatch: pytest.MonkeyPatch) -> None:
    client = _ScriptedChatClient([_drafting_turn()])
    _install_client(monkeypatch, client)
    hidden = {**_v2_content_page("page3", _REVENUE_TREND), "visible": False}
    user_context = _open_document_with([_v2_cover_page(), _v2_content_page("page2", _REVENUE_TREND), hidden])
    expected = {"rework": _NEW_PAGE_REWORK}
    with pytest.raises(ValueError, match=r"open document with hidden pages \['page3'\]"):
        run_agentic_document_skill("https://h", "tok", "ws", "Add a page", expected, user_context=user_context)
    assert client.sent == []


def test_a_new_page_rework_listing_every_open_page_reaches_the_chat(monkeypatch: pytest.MonkeyPatch) -> None:
    client = _ScriptedChatClient([_drafting_turn()])
    _install_client(monkeypatch, client)
    user_context = _open_document_with([_v2_cover_page(), _v2_content_page("page2", _REVENUE_TREND)])
    expected = {"rework": _NEW_PAGE_REWORK}
    run_agentic_document_skill("https://h", "tok", "ws", "Add a page", expected, user_context=user_context)
    assert client.sent == ["Add a page"]


def test_a_rework_of_the_open_document_reaches_the_chat(monkeypatch: pytest.MonkeyPatch) -> None:
    client = _ScriptedChatClient([_drafting_turn()])
    _install_client(monkeypatch, client)
    user_context = {"view": {"document": {"id": _OPEN_DOCUMENT, "title": "Q3 review"}}}
    expected = {"rework": {"base_document_id": _OPEN_DOCUMENT}}
    run_agentic_document_skill("https://h", "tok", "ws", "Rename it", expected, user_context=user_context)
    assert client.sent == ["Rename it"]


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
        ({"asked_first_required": "yes"}, "asked_first_required must be true or false"),
        ({"asked_first_required": True}, "asked_first_required needs expects_clarification: true"),
        ({"clarification_reply": " "}, "clarification_reply must be a non-empty reply"),
        ({"clarification_reply": "Use 2026."}, "clarification_reply needs expects_clarification: true"),
        ({"rework": True}, "rework must be an object"),
        ({"rework": {}}, "rework needs the base_document_id"),
        ({"rework": {"base_document_id": "  "}}, "rework needs the base_document_id"),
        ({"rework": {"base_document_id": "q3", "keeps_pages": [" "]}}, "every rework.keeps_pages entry"),
        ({"rework": {"base_document_id": "q3", "keep_pages": ["page1"]}}, r"unknown rework key\(s\) \['keep_pages'\]"),
        ({"rework": {"base_document_id": "q3", "keeps_pages": []}}, "rework.keeps_pages is empty"),
        ({"rework": {"base_document_id": "q3", "keeps_pages": [""]}}, "every rework.keeps_pages entry"),
        (
            {"rework": {"base_document_id": "q3", "keeps_pages": ["p2"], "page_charts": {}}},
            "rework.page_charts is empty",
        ),
        (
            {"rework": {"base_document_id": "q3", "page_charts": {"p2": ["c1"]}}},
            "must also be listed in rework.keeps_pages",
        ),
        (
            {"rework": {"base_document_id": "q3", "keeps_pages": ["p2"], "page_charts": {"p2": []}}},
            "must list the charts",
        ),
        (
            {"rework": {"base_document_id": "q3", "keeps_pages": ["p2"], "page_charts": {"p2": [" "]}}},
            "entry must be a chart id",
        ),
        ({"rework": {"base_document_id": "q3", "title": " "}}, "rework.title must be"),
        ({"rework": {"base_document_id": "q3", "filters": ["customer_country"]}}, "rework.filters must be"),
        ({"rework": {"base_document_id": "q3", "filters": {"f1": {}}}}, r"rework.filters\['f1'\] must state at least"),
        (
            {"rework": {"base_document_id": "q3", "filters": {"f1": {"state": {"include": ["US"]}}}}},
            r"rework.filters\['f1'\] must state at least the filter's 'type'",
        ),
        (
            {
                "rework": {
                    "base_document_id": "q3",
                    "filters": {"f1": {"type": "attribute_filter", "using": "label/country", "state": ["US"]}},
                }
            },
            r"rework.filters\['f1'\].state is \['US'\], expected an object",
        ),
        (
            {
                "rework": {
                    "base_document_id": "q3",
                    "filters": {
                        "f1": {"type": "attribute_filter", "using": "label/country", "state": {"include": "US"}}
                    },
                }
            },
            r"rework.filters\['f1'\].state is \{'include': 'US'\}, expected a list of values under 'include'",
        ),
        (
            {
                "rework": {
                    "base_document_id": "q3",
                    "filters": {
                        "f1": {"type": "attribute_filter", "using": "label/country", "state": {"values": ["US"]}}
                    },
                }
            },
            r"rework.filters\['f1'\].state is \{'values': \['US'\]\}, expected only 'include' or 'exclude'",
        ),
        (
            {"rework": {"base_document_id": "q3", "filters": {"f1": {"type": "attribute_filter", "state": None}}}},
            r"rework.filters\['f1'\] of type 'attribute_filter' leaves out \['using'\]",
        ),
        (
            {"rework": {"base_document_id": "q3", "filters": {"f1": {"type": "attribute_filter", "using": "label/c"}}}},
            r"rework.filters\['f1'\] of type 'attribute_filter' leaves out \['state'\]",
        ),
        (
            {"rework": {"base_document_id": "q3", "filters": {"d": {"type": "date_filter", "granularity": "YEAR"}}}},
            r"rework.filters\['d'\] of type 'date_filter' leaves out \['date'\]",
        ),
        (
            {
                "rework": {
                    "base_document_id": "q3",
                    "filters": {"f1": {"type": "atribute_filter", "using": "label/country", "state": None}},
                }
            },
            r"rework.filters\['f1'\] has type 'atribute_filter'; known: \['attribute_filter', 'date_filter'\]",
        ),
        (
            {"rework": {"base_document_id": "q3", "filters": {"m": {"type": "measure_value_filter"}}}},
            r"rework.filters\['m'\] has type 'measure_value_filter'",
        ),
        (
            {"rework": {"base_document_id": "q3", "keeps_pages": ["p2"], "new_page_charts": []}},
            "new_page_charts is empty",
        ),
        (
            {"rework": {"base_document_id": "q3", "keeps_pages": ["p2"], "new_page_charts": [" "]}},
            "every rework.new_page_charts entry must be a chart id",
        ),
        ({"rework": {"base_document_id": "q3", "new_page_charts": ["c1"]}}, "new_page_charts needs rework.keeps_pages"),
        ({"period": {"from": -6, "to": -1}}, "period needs both 'start' and 'end', or a relative 'granularity'"),
        ({"period": {"granularity": "GDC.time.month", "from": -6, "to": -1}}, "must be one AaC writes"),
        ({"period": {"granularity": "WEEK", "from": -2, "to": -1}}, "must be one AaC writes"),
        ({"period": {"granularity": ["MONTH"], "from": -6, "to": -1}}, "must be one AaC writes"),
        ({"period": {"granularity": "MONTH", "from": "-6", "to": -1}}, "a relative period needs whole numbers"),
        ({"period": {"granularity": "MONTH", "from": True, "to": -1}}, "a relative period needs whole numbers"),
        (
            {"period": {"granularity": "MONTH", "from": -6, "to": -1, "start": "2026-01-01"}},
            r"a relative period states only 'granularity', 'from' and 'to', got \['start'\] too",
        ),
        (
            {"period": {"start": "2026-01-01", "end": "2026-06-30", "type": "absolute"}},
            r"an absolute period states only 'start' and 'end', got \['type'\] too",
        ),
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


def test_the_simulated_reply_to_an_edit_asks_for_the_change_in_the_open_document() -> None:
    assert build_simulated_reply({"rework": {"base_document_id": "q3"}}) == (
        "Anything else is up to you. Please make the change in the open document now."
    )


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


def test_a_run_that_must_ask_first_fails_when_it_drafts_straight_away() -> None:
    expected = {"expects_clarification": True, "asked_first_required": True}
    run = _execute_single_document_run(_ScriptedChatClient([_drafting_turn()]), "c", "q", expected, 4)
    assert run.evaluation.strict_checks["document_asked_first"] is False
    assert not run.evaluation.strict_pass
    assert run.diagnostics == {}


def test_a_run_that_must_ask_first_passes_when_it_asks_then_drafts() -> None:
    question = _chat_result(text="The pages show no data for 2030. Drop them, change the period, or keep them?")
    expected = {"expects_clarification": True, "asked_first_required": True}
    run = _execute_single_document_run(_ScriptedChatClient([question, _drafting_turn()]), "c", "q", expected, 4)
    assert run.evaluation.strict_checks["document_asked_first"] is True
    assert run.evaluation.strict_pass


def test_a_run_that_must_ask_first_passes_when_it_asks_for_confirmation() -> None:
    question = _chat_result(text="I could not find any data for 2030. Should I create the document anyway?")
    expected = {"expects_clarification": True, "asked_first_required": True}
    run = _execute_single_document_run(_ScriptedChatClient([question, _drafting_turn()]), "c", "q", expected, 4)
    assert run.evaluation.strict_checks["document_asked_first"] is True
    assert run.evaluation.strict_pass


def test_a_run_that_must_ask_first_passes_when_it_asks_after_a_status_turn() -> None:
    status = _chat_result(text="Working on it.")
    question = _chat_result(text="Which period?")
    expected = {"expects_clarification": True, "asked_first_required": True}
    run = _execute_single_document_run(_ScriptedChatClient([status, question, _drafting_turn()]), "c", "q", expected, 4)
    assert run.evaluation.strict_checks["document_asked_first"] is True
    assert run.evaluation.strict_pass


def test_a_run_that_must_ask_first_and_never_drafts_fails_only_for_the_missing_draft() -> None:
    expected = {"expects_clarification": True, "asked_first_required": True}
    run = _execute_single_document_run(_ScriptedChatClient([_chat_result()]), "c", "q", expected, 4)
    assert run.evaluation.failures == ["the agent never produced a successful draft_document call"]


def test_the_fixture_reply_answers_the_copilots_question() -> None:
    client = _ScriptedChatClient([_chat_result(text="Which period?"), _drafting_turn()])
    expected = {"expects_clarification": True, "clarification_reply": "Use the first half of 2026 instead."}
    _execute_single_document_run(client, "c", "q", expected, 4)
    assert client.sent == ["q", "Use the first half of 2026 instead."]


def test_the_fixture_reply_answers_only_the_first_question() -> None:
    client = _ScriptedChatClient(
        [_chat_result(text="Which period?"), _chat_result(text="Which charts?"), _drafting_turn()]
    )
    expected = {"expects_clarification": True, "clarification_reply": "Use the first half of 2026 instead."}
    _execute_single_document_run(client, "c", "q", expected, 4)
    assert client.sent == [
        "q",
        "Use the first half of 2026 instead.",
        "Anything else is up to you. Please create the document now.",
    ]


def test_the_fixture_reply_waits_for_a_question() -> None:
    expected = {"expects_clarification": True, "clarification_reply": "Use the first half of 2026 instead."}
    status = _chat_result(text="Working on it.")
    client = _ScriptedChatClient([status, _chat_result(text="Which period?"), _drafting_turn()])
    _execute_single_document_run(client, "c", "q", expected, 4)
    assert client.sent == [
        "q",
        "Anything else is up to you. Please create the document now.",
        "Use the first half of 2026 instead.",
    ]


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
        "document_new_draft",
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
    with pytest.raises(
        JudgeResponseError, match=r"^no run of 1 could be graded: judge returned no readable verdict for 1 run\(s\): "
    ) as raised:
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
    relative = {"granularity": "MONTH", "from": -6, "to": -1}
    part = _v2_document_part(period=relative)
    evaluation = _evaluate(part, expected={"period": _PERIOD})
    assert evaluation.strict_checks["document_period_correct"] is False
    assert evaluation.failures == [
        "the document covers the relative range MONTH -6 to -1, expected 2026-01-01 to 2026-06-30"
    ]
    assert render_document_text(part["document"]).splitlines()[1] == ("Period: the relative range MONTH -6 to -1")


# As gen-ai drafts "the last 6 full months": AaC writes a relative period with its granularity and no type.
_RELATIVE = {"granularity": "MONTH", "from": -6, "to": -1}


def test_a_relative_period_kept_as_stated_passes() -> None:
    evaluation = _evaluate(_v2_document_part(period=dict(_RELATIVE)), expected={"period": _RELATIVE})
    assert evaluation.failures == []
    assert evaluation.strict_checks["document_period_correct"] is True


@pytest.mark.parametrize(
    ("period", "covers"),
    [
        ({**_RELATIVE, "from": -12}, "the relative range MONTH -12 to -1"),
        ({**_RELATIVE, "granularity": "QUARTER"}, "the relative range QUARTER -6 to -1"),
        ({"from": "2026-05-01", "to": "2026-10-31"}, "2026-05-01 to 2026-10-31"),
    ],
    ids=["shifted", "other-granularity", "made-absolute"],
)
def test_a_relative_period_that_changed_fails(period: dict, covers: str) -> None:
    evaluation = _evaluate(_v2_document_part(period=period), expected={"period": _RELATIVE})
    assert evaluation.strict_checks["document_period_correct"] is False
    assert evaluation.failures == [f"the document covers {covers}, expected the relative range MONTH -6 to -1"]


def test_a_relative_period_never_matches_a_v1_document() -> None:
    evaluation = _evaluate(_document_part(), expected={"period": _RELATIVE})
    assert evaluation.strict_checks["document_period_correct"] is False


def test_the_simulated_reply_states_a_relative_period() -> None:
    reply = build_simulated_reply({"period": _RELATIVE})
    assert "Period: the relative range MONTH -6 to -1." in reply


# As gen-ai drafts a document from a dashboard, in AaC: a chart the dashboard's date filter reaches applies
# the period on its own date dataset, and one it does not reach keeps a `date` but ignores the period.
_GOAL, _SEASONALITY = "sales_goal", "seasonality"
_CHART_PERIODS = {_REVENUE_TREND: "date", _GOAL: "customer_created_date", _SEASONALITY: None}


def _with_chart_dates(page: dict, dates: dict[str, Any]) -> dict:
    """``page`` with each chart's widget given a ``date``, or ``ignore_document_period`` where the value is None."""
    for node in page["layout"]["children"][1]["children"][0]["children"]:
        chart = node["visualization"]
        node["date"] = dates[chart] if dates[chart] is not None else "date"
        if dates[chart] is None:
            node["ignore_document_period"] = True
    return page


def _dashboard_document_part(dates: dict[str, Any] | None = None) -> dict:
    charts = dates if dates is not None else _CHART_PERIODS
    page = _with_chart_dates(_v2_content_page("page2", *charts, bare_ids=True), charts)
    return _v2_document_part([_v2_cover_page(), page])


def test_charts_that_apply_the_period_as_the_dashboard_does_pass() -> None:
    evaluation = _evaluate(_dashboard_document_part(), expected={"chart_periods": _CHART_PERIODS})
    assert evaluation.failures == []
    assert evaluation.strict_checks["document_chart_periods_correct"] is True


@pytest.mark.parametrize(
    ("dates", "failure"),
    [
        (
            {**_CHART_PERIODS, _SEASONALITY: "date"},
            "chart 'seasonality' applies the period on 'date', expected it to ignore the period",
        ),
        (
            {**_CHART_PERIODS, _GOAL: "date"},
            "chart 'sales_goal' applies the period on 'date', expected it on 'customer_created_date'",
        ),
        (
            {**_CHART_PERIODS, _GOAL: None},
            "chart 'sales_goal' ignores the period, expected it on 'customer_created_date'",
        ),
        ({**_CHART_PERIODS, _REVENUE_TREND: None}, "chart 'revenue_trend' ignores the period, expected it on 'date'"),
    ],
    ids=["unreached-chart-dated", "other-date", "reached-chart-ignores", "ignores-on-its-own-date"],
)
def test_a_chart_that_applies_the_period_elsewhere_fails(dates: dict, failure: str) -> None:
    evaluation = _evaluate(_dashboard_document_part(dates), expected={"chart_periods": _CHART_PERIODS})
    assert evaluation.strict_checks["document_chart_periods_correct"] is False
    assert evaluation.failures == [failure]


def test_a_chart_left_out_of_the_document_fails_its_period_check() -> None:
    dates = {_REVENUE_TREND: "date", _GOAL: "customer_created_date"}
    evaluation = _evaluate(_dashboard_document_part(dates), expected={"chart_periods": _CHART_PERIODS})
    assert evaluation.strict_checks["document_chart_periods_correct"] is False
    assert evaluation.failures == [
        "chart 'seasonality' is not in the document, so where it applies the period is unknown"
    ]


def test_every_placement_of_a_chart_must_apply_the_period_as_stated() -> None:
    reached = _with_chart_dates(_v2_content_page("page2", _SEASONALITY, bare_ids=True), {_SEASONALITY: None})
    again = _with_chart_dates(_v2_content_page("page3", _SEASONALITY, bare_ids=True), {_SEASONALITY: "date"})
    part = _v2_document_part([_v2_cover_page(), reached, again])
    evaluation = _evaluate(part, expected={"chart_periods": {_SEASONALITY: None}})
    assert evaluation.strict_checks["document_chart_periods_correct"] is False


def test_a_chart_only_on_a_hidden_page_is_not_in_the_document() -> None:
    hidden_page = _v2_content_page("page3", _SEASONALITY, bare_ids=True)
    hidden = {**_with_chart_dates(hidden_page, {_SEASONALITY: None}), "visible": False}
    part = _v2_document_part([_v2_cover_page(), _v2_content_page("page2", _REVENUE_TREND), hidden])
    evaluation = _evaluate(part, expected={"chart_periods": {_SEASONALITY: None}})
    assert evaluation.strict_checks["document_chart_periods_correct"] is False


def test_chart_periods_are_not_scored_on_a_v1_document() -> None:
    evaluation = _evaluate(_document_part(), expected={"chart_periods": {_REVENUE_TREND: "date"}})
    assert evaluation.strict_checks["document_chart_periods_correct"] is False
    assert evaluation.failures == ["where a chart applies the period is scored on aac-v2 documents only"]


def test_chart_periods_are_published_only_when_stated() -> None:
    assert "document_chart_periods_correct" not in _evaluate(_dashboard_document_part()).strict_checks


@pytest.mark.parametrize(
    ("chart_periods", "message"),
    [
        ({}, "chart_periods must map chart ids"),
        ([_REVENUE_TREND], "chart_periods must map chart ids"),
        ({" ": "date"}, "every chart_periods key must be a chart id"),
        ({_REVENUE_TREND: ""}, r"chart_periods\['revenue_trend'\] must be a date dataset id or null"),
        ({_REVENUE_TREND: 1}, r"chart_periods\['revenue_trend'\] must be a date dataset id or null"),
    ],
    ids=["empty", "list", "blank-chart", "blank-dataset", "not-a-dataset"],
)
def test_unusable_chart_periods_are_rejected(chart_periods: Any, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        _validate_expectation({"chart_periods": chart_periods})


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
    """``page`` plus the default template's ``text`` widget with id ``summary``, which is not a takeaway."""
    page["layout"]["children"].append(
        {"type": "text", "id": "summary", **({"markdown": markdown} if markdown is not None else {})}
    )
    return page


def test_a_v2_document_without_a_takeaway_has_no_summaries() -> None:
    page = _with_summary_text(_v2_content_page("page2", _REVENUE_TREND), "Revenue grew 12%.")
    part = _v2_document_part([_v2_cover_page(), page])
    evaluation = _evaluate(part, expected={"narrative": _NARRATIVE})
    assert evaluation.strict_checks["document_summaries_present"] is False
    assert evaluation.failures == ["the document has no takeaway"]
    assert "Summary:" not in render_document_text(part["document"])


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


# ── takeaways the copilot leaves to the editor ──────────────────────────────

_EDITOR_TEXT = "**Revenue grew 12%** in H1, led by the West."


class _StubTakeaways:
    """Stands in for TakeawayClient: answers each request with the next scripted response."""

    def __init__(self, *responses: dict | Exception) -> None:
        self._responses = list(responses)
        self.requests: list[TakeawayInput] = []
        self.closed = False

    def request(self, ti: TakeawayInput) -> ChatResult:
        self.requests.append(ti)
        response = self._responses.pop(0) if self._responses else {"takeaway": _EDITOR_TEXT, "noData": False}
        if isinstance(response, Exception):
            raise response
        return ChatResult(text_response=response.get("takeaway") or "", raw_response=response)

    def close(self) -> None:
        self.closed = True


def _install_takeaways(monkeypatch: pytest.MonkeyPatch, takeaways: _StubTakeaways) -> None:
    monkeypatch.setattr(document_skill, "TakeawayClient", lambda **_kwargs: takeaways)


def _http_error(status: int) -> httpx.HTTPStatusError:
    request = httpx.Request("POST", "https://h/api/v1/ai/workspaces/ws/takeaway")
    return httpx.HTTPStatusError(f"{status}", request=request, response=httpx.Response(status, request=request))


def _with_instructions(page: dict, instructions: str) -> dict:
    takeaway = page["layout"]["children"][1]["children"][1]
    takeaway["generation"] = {**takeaway["generation"], "instructions": instructions}
    return page


# The copilot's part carries the document as code: a period of bare dates and a widget's date dataset in ``date``.
_AAC_PERIOD = {"from": "2026-01-01", "to": "2026-06-30"}


def _dated(page: dict, dataset: str) -> dict:
    page["layout"]["children"][1]["children"][0]["children"][0]["date"] = dataset
    return page


def _editor_pages() -> list[dict]:
    """A cover, a page whose takeaway the copilot wrote, and two left to the editor, one dated and with instructions."""
    return [
        _v2_cover_page(),
        _v2_content_page("page2", _REVENUE_TREND, takeaway="Revenue grew 12%.", bare_ids=True),
        _v2_content_page("page3", _RETURNS_BY_CATEGORY, takeaway="", bare_ids=True),
        _with_instructions(
            _dated(_v2_content_page("page4", _REVENUE_TREND, takeaway="", bare_ids=True), "date"), "Focus on the West."
        ),
    ]


def _editor_turn(
    pages: list[dict],
    editor_page_ids: Any,
    *,
    version: str = "v2",
    period: Any = _AAC_PERIOD,
    filters: dict | None = None,
) -> ChatResult:
    tool = _draft_result(page_count=len(pages))
    if editor_page_ids is not None:
        tool[document_skill._EDITOR_PAGES_KEY] = editor_page_ids
    part = _v2_document_part(pages, period=period) if version == "v2" else _document_part(pages)
    if filters is not None:
        part["document"]["content"]["filters"] = filters
    return _chat_result(tool_calls=[_tool_call("draft_document", tool)], parts=[part], text="Done.")


def _editor_run(
    pages: list[dict],
    editor_page_ids: Any,
    takeaways: _StubTakeaways | None,
    judge: _FakeJudge | None = None,
    user_context: dict | None = None,
) -> document_skill.DocumentRunResult:
    return _execute_single_document_run(
        _ScriptedChatClient([_editor_turn(pages, editor_page_ids)]),
        "conv-1",
        "q",
        {"narrative": _NARRATIVE},
        4,
        judge or _FakeJudge(),
        takeaways,
        user_context,
    )


def test_each_takeaway_left_to_the_editor_is_written_the_editors_way_and_graded() -> None:
    # given
    takeaways = _StubTakeaways()
    judge = _FakeJudge()

    # when
    run = _editor_run(_editor_pages(), ["page3", "page4"], takeaways, judge)

    # then
    assert [r.model_dump() for r in takeaways.requests] == [
        TakeawayInput(visualizations=[{"visualization_id": _RETURNS_BY_CATEGORY}]).model_dump(),
        TakeawayInput(
            visualizations=[
                {
                    "visualization_id": _REVENUE_TREND,
                    "filters": [
                        {
                            "absoluteDateFilter": {
                                "dataset": {"identifier": {"id": "date", "type": "dataset"}},
                                "from": "2026-01-01",
                                "to": "2026-06-30",
                            }
                        }
                    ],
                }
            ],
            instructions={"slot": "Focus on the West."},
        ).model_dump(),
    ]
    assert run.evaluation.failures == []
    assert run.evaluation.strict_checks["document_summaries_present"] is True
    assert run.evaluation.strict_checks["document_narrative_judged"] is True
    assert judge.calls[0]["actual_output"].count(f"Summary: {_EDITOR_TEXT}") == 2
    assert run.takeaways_by_editor == 2


def test_each_takeaway_on_a_page_sends_its_own_instructions() -> None:
    # given
    page = _with_instructions(_v2_content_page("page3", _RETURNS_BY_CATEGORY, takeaway="", bare_ids=True), "First.")
    row = page["layout"]["children"][1]["children"]
    row.append({**row[1], "id": "takeawayB", "generation": {**row[1]["generation"], "instructions": "Second."}})
    takeaways = _StubTakeaways()

    # when
    run = _editor_run([_v2_cover_page(), page], ["page3"], takeaways)

    # then
    assert [r.instructions.slot for r in takeaways.requests if r.instructions] == ["First.", "Second."]
    assert run.takeaways_by_editor == 2


def test_the_document_filters_as_the_editor_reads_them_reach_each_request() -> None:
    # given
    filters = {
        "region": {"type": "attribute_filter", "using": "label/region", "state": {"include": ["West"]}},
        "q1": {"type": "date_filter", "granularity": "DAY", "date": "date", "from": "2026-01-01", "to": "2026-03-31"},
    }
    takeaways = _StubTakeaways()
    turn = _editor_turn(_editor_pages(), ["page3", "page4"], filters=filters)

    # when
    run = _execute_single_document_run(
        _ScriptedChatClient([turn]), "conv-1", "q", {"narrative": _NARRATIVE}, 4, _FakeJudge(), takeaways
    )

    # then
    west = {
        "positiveAttributeFilter": {
            "label": {"identifier": {"id": "region", "type": "label"}},
            "in": {"values": ["West"]},
        }
    }
    q1 = {
        "absoluteDateFilter": {
            "dataset": {"identifier": {"id": "date", "type": "dataset"}},
            "from": "2026-01-01",
            "to": "2026-03-31",
        }
    }
    assert [[v.filters for v in r.visualizations if not isinstance(v, str)] for r in takeaways.requests] == [
        [[west]],
        [[q1, west]],
    ]
    assert run.evaluation.failures == []
    assert run.takeaways_by_editor == 2


def test_the_run_keeps_the_part_the_copilot_sent() -> None:
    # when
    run = _editor_run(_editor_pages(), ["page3", "page4"], _StubTakeaways())

    # then
    assert run.document_part is not None
    assert (
        "markdown" not in run.document_part["document"]["content"]["pages"][2]["layout"]["children"][1]["children"][1]
    )


def test_a_takeaway_the_editor_writes_on_a_page_the_draft_does_not_list_fails() -> None:
    # given
    takeaways = _StubTakeaways()

    # when
    run = _editor_run(_editor_pages(), ["page4"], takeaways)

    # then
    assert len(takeaways.requests) == 2
    assert run.evaluation.failures == [
        "page 'page3' has a takeaway the editor writes, but draft_document does not list it in takeaway_editor_page_ids"
    ]


def test_a_page_the_draft_lists_that_the_editor_writes_nothing_on_fails() -> None:
    # given
    takeaways = _StubTakeaways()

    # when
    run = _editor_run(_editor_pages(), ["page2", "page3", "page4"], takeaways)

    # then
    assert len(takeaways.requests) == 2
    assert run.evaluation.failures == [
        "draft_document lists page 'page2' in takeaway_editor_page_ids, but the editor writes no takeaway there"
    ]


def _open_document(pages: list[dict], *, period: Any = _AAC_PERIOD) -> dict:
    """The ``user_context`` of an item that has this document open in the editor."""
    return {"view": {"document": {"id": "sales_overview", "definition": _v2_document(pages, period=period)}}}


def test_an_empty_takeaway_the_open_document_holds_empty_under_the_same_request_stays_empty() -> None:
    # given
    takeaways = _StubTakeaways()
    open_document = _open_document(_editor_pages())

    # when
    run = _editor_run(_editor_pages(), [], takeaways, user_context=open_document)

    # then
    assert takeaways.requests == []
    assert run.evaluation.strict_checks["document_summaries_present"] is True
    assert run.evaluation.failures == []


def test_a_new_period_changes_only_the_request_of_a_takeaway_whose_chart_uses_it() -> None:
    # given
    takeaways = _StubTakeaways()
    other_period = {"from": "2025-01-01", "to": "2025-06-30"}
    open_document = _open_document(_editor_pages(), period=other_period)

    # when
    run = _editor_run(_editor_pages(), ["page4"], takeaways, user_context=open_document)

    # then
    assert [r.instructions.slot for r in takeaways.requests] == ["Focus on the West."]
    assert run.evaluation.failures == []


def test_an_empty_takeaway_is_written_when_the_open_document_wrote_it() -> None:
    # given
    written = _editor_pages()
    written[2] = _v2_content_page("page3", _RETURNS_BY_CATEGORY, takeaway="Returns fell.", bare_ids=True)
    takeaways = _StubTakeaways()

    # when
    run = _editor_run(_editor_pages(), ["page3"], takeaways, user_context=_open_document(written))

    # then
    assert [r.visualizations[0].visualization_id for r in takeaways.requests] == [_RETURNS_BY_CATEGORY]
    assert run.evaluation.failures == []


def test_an_empty_takeaway_is_written_when_its_instructions_changed_since_the_open_document() -> None:
    # given
    changed = _editor_pages()
    changed[2] = _with_instructions(changed[2], "Focus on the East.")
    takeaways = _StubTakeaways()

    # when
    run = _editor_run(changed, ["page3"], takeaways, user_context=_open_document(_editor_pages()))

    # then
    assert [r.instructions.slot for r in takeaways.requests] == ["Focus on the East."]
    assert run.evaluation.failures == []


def test_a_listed_takeaway_the_copilot_wrote_is_graded_as_written() -> None:
    # given
    takeaways = _StubTakeaways()

    # when
    run = _editor_run(_editor_pages(), ["page2", "page3", "page4"], takeaways)

    # then
    assert len(takeaways.requests) == 2
    assert run.takeaways_by_editor == 2


def test_a_draft_without_the_field_is_graded_as_before() -> None:
    # given
    takeaways = _StubTakeaways()
    pages = _editor_pages()

    # when
    run = _editor_run(pages, None, takeaways)

    # then
    assert takeaways.requests == []
    assert run.takeaways_by_editor is None
    without_client = _editor_run(pages, None, None)
    assert run.evaluation == without_client.evaluation
    assert run.evaluation.failures == [
        "page 'page3' has a takeaway with no written text",
        "page 'page4' has a takeaway with no written text",
    ]


def test_a_draft_without_the_field_gets_no_exemption_from_the_open_document() -> None:
    # given
    pages = _editor_pages()

    # when
    run = _editor_run(pages, None, _StubTakeaways(), user_context=_open_document(pages))

    # then
    assert run.evaluation.strict_checks["document_summaries_present"] is False
    assert run.evaluation.failures == [
        "page 'page3' has a takeaway with no written text",
        "page 'page4' has a takeaway with no written text",
    ]


def test_a_draft_that_lists_nothing_while_the_editor_writes_takeaways_fails() -> None:
    # given
    takeaways = _StubTakeaways()

    # when
    run = _editor_run(_editor_pages(), [], takeaways)

    # then
    assert len(takeaways.requests) == 2
    assert run.evaluation.failures == [
        "page 'page3' has a takeaway the editor writes, but draft_document does not list it in "
        "takeaway_editor_page_ids",
        "page 'page4' has a takeaway the editor writes, but draft_document does not list it in "
        "takeaway_editor_page_ids",
    ]


def test_each_takeaway_request_names_the_agent_of_the_chat_turn() -> None:
    # given
    takeaways = _StubTakeaways()

    # when
    _execute_single_document_run(
        _ScriptedChatClient([_editor_turn(_editor_pages(), ["page3", "page4"])]),
        "conv-1",
        "q",
        {"narrative": _NARRATIVE},
        4,
        _FakeJudge(),
        takeaways,
        agent_id="custom-agent",
    )

    # then
    assert [r.agent_id for r in takeaways.requests] == ["custom-agent", "custom-agent"]


def test_a_chart_the_endpoint_cannot_find_fails_that_run_with_its_detail() -> None:
    # given
    request = httpx.Request("POST", "https://h/api/v1/ai/workspaces/ws/takeaway")
    detail = "Visualization 'returns_by_category' does not exist or is not available to AI."
    refused = httpx.HTTPStatusError(
        "404", request=request, response=httpx.Response(404, json={"detail": detail}, request=request)
    )
    takeaways = _StubTakeaways(refused)

    # when
    run = _editor_run(_editor_pages(), ["page3", "page4"], takeaways)

    # then
    assert len(takeaways.requests) == 2
    assert run.evaluation.failures == [
        "page 'page3' has a takeaway with no written text",
        f"page 'page3': the takeaway endpoint refused the chart: {detail}",
    ]
    assert run.takeaways_by_editor == 1


def test_the_reader_waits_for_the_slowest_takeaway_not_for_their_sum(monkeypatch: pytest.MonkeyPatch) -> None:
    # given
    clock = iter([0.0, 3.0, 3.0, 4.0])
    monkeypatch.setattr(document_skill, "time", SimpleNamespace(monotonic=lambda: next(clock)))
    part = _v2_document_part(_editor_pages(), period=_AAC_PERIOD)

    # when
    fill = document_skill._fill_editor_takeaways(_StubTakeaways(), part, frozenset(), None)

    # then
    assert fill.waited_s == 3.0


def test_a_v1_draft_is_never_filled() -> None:
    # given
    takeaways = _StubTakeaways()
    pages = [_cover_page(), _summary_page("page2", "", _REVENUE_TREND)]

    # when
    run = _execute_single_document_run(
        _ScriptedChatClient([_editor_turn(pages, ["page2"], version="v1")]),
        "conv-1",
        "q",
        {"narrative": _NARRATIVE},
        4,
        _FakeJudge(),
        takeaways,
    )

    # then
    assert takeaways.requests == []
    assert run.evaluation.failures[0] == "page 'page2' has a summary slot with no written text"


@pytest.mark.parametrize(
    ("response", "reason"),
    [
        ({"takeaway": None, "noData": True}, "the editor's takeaway request found no data"),
        ({"takeaway": "  ", "noData": False}, "the takeaway endpoint wrote no text"),
    ],
    ids=["no data", "no text"],
)
def test_a_takeaway_the_endpoint_does_not_write_fails_with_why(response: dict, reason: str) -> None:
    # when
    run = _editor_run(_editor_pages(), ["page3", "page4"], _StubTakeaways(response))

    # then
    assert run.evaluation.strict_checks["document_summaries_present"] is False
    assert run.evaluation.failures == ["page 'page3' has a takeaway with no written text", f"page 'page3': {reason}"]
    assert run.takeaways_by_editor == 1


def test_a_takeaway_whose_request_the_eval_cannot_build_fails_with_why() -> None:
    # given
    pages = _editor_pages()
    pages[2] = _v2_content_page("page3", takeaway="")

    # when
    run = _editor_run(pages, ["page3", "page4"], _StubTakeaways())

    # then
    assert run.evaluation.failures == [
        "page 'page3' has a takeaway with no written text",
        "page 'page3': the eval cannot build the editor's takeaway request: page 'page3' has no visualization to summarize",
    ]


def test_a_draft_the_editor_cannot_read_fails_with_why() -> None:
    # given
    takeaways = _StubTakeaways()
    turn = _editor_turn(
        _editor_pages(), ["page3"], period={"type": "relative", "granularity": "CENTURY", "from": -1, "to": -1}
    )

    # when
    run = _execute_single_document_run(
        _ScriptedChatClient([turn]), "conv-1", "q", {"narrative": _NARRATIVE}, 4, _FakeJudge(), takeaways
    )

    # then
    assert takeaways.requests == []
    assert run.evaluation.failures[:2] == [
        "page 'page3' has a takeaway with no written text",
        "page 'page4' has a takeaway with no written text",
    ]
    assert len(run.evaluation.failures) == 3
    assert run.evaluation.failures[2].startswith("the eval cannot read the draft as the editor does: ")
    assert "CENTURY" in run.evaluation.failures[2]


def test_an_endpoint_that_refuses_the_request_stops_the_item(monkeypatch: pytest.MonkeyPatch) -> None:
    # given
    _install_client(monkeypatch, _ScriptedChatClient([_editor_turn(_editor_pages(), ["page3"])]))
    takeaways = _StubTakeaways(_http_error(404))
    _install_takeaways(monkeypatch, takeaways)

    # when
    with pytest.raises(httpx.HTTPStatusError, match="404"):
        run_agentic_document_skill("https://h", "tok", "ws", "q", {"narrative": _NARRATIVE}, judge=_FakeJudge())

    # then
    assert takeaways.closed


def test_a_transient_endpoint_failure_leaves_the_run_ungraded(monkeypatch: pytest.MonkeyPatch) -> None:
    # given
    turns = [_editor_turn(_editor_pages(), ["page3", "page4"]) for _ in range(2)]
    _install_client(monkeypatch, _ScriptedChatClient(turns))
    _install_takeaways(monkeypatch, _StubTakeaways(_http_error(503)))
    judge = _FakeJudge()

    # when
    summary = run_agentic_document_skill("https://h", "tok", "ws", "q", {"narrative": _NARRATIVE}, k=2, judge=judge)

    # then
    first, second = summary.run_results
    assert first.ungraded
    assert first.judge_error is not None and first.judge_error.startswith("takeaway endpoint for page 'page3'")
    assert "document_summaries_present" not in first.evaluation.strict_checks
    assert not second.ungraded and second.evaluation.strict_pass
    assert len(judge.calls) == 1, "a run with a takeaway still unwritten is not judged"
    assert summary.request_errors == [first.judge_error]
    assert summary.judge_errors == []
    assert summary.pass_at_k
    assert not summary.pass_power_k


def test_an_item_whose_every_run_the_takeaway_endpoint_left_ungraded_raises_naming_the_takeaway_endpoint(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # given
    _install_client(monkeypatch, _ScriptedChatClient([_editor_turn(_editor_pages(), ["page3", "page4"])]))
    _install_takeaways(monkeypatch, _StubTakeaways(_http_error(503)))

    # when
    with pytest.raises(JudgeResponseError) as raised:
        evaluate_agentic_document_skill("https://h", "tok", "ws", "q", {"narrative": _NARRATIVE}, judge=_FakeJudge())

    # then
    assert str(raised.value).startswith("no run of 1 could be graded: request failed for 1 run(s): ")
    assert "takeaway endpoint for page 'page3'" in str(raised.value)


def test_a_transient_failure_after_a_listed_takeaway_already_failed_is_a_failure() -> None:
    # when
    run = _editor_run(
        _editor_pages(), ["page3", "page4"], _StubTakeaways({"takeaway": None, "noData": True}, _http_error(503))
    )

    # then
    assert not run.ungraded
    assert run.evaluation.fill_error is None
    assert run.evaluation.strict_checks["document_summaries_present"] is False
    assert "page 'page3': the editor's takeaway request found no data" in run.evaluation.failures
    assert (
        "takeaway endpoint for page 'page4': HTTPStatusError: 503: the takeaway stays empty" in run.evaluation.failures
    )


def test_a_transient_failure_beside_a_takeaway_the_open_document_keeps_empty_leaves_the_run_ungraded() -> None:
    # given
    open_document = _open_document(_editor_pages())
    changed = _editor_pages()
    changed[3] = _with_instructions(changed[3], "Focus on the East.")

    # when
    run = _editor_run(changed, ["page4"], _StubTakeaways(_http_error(503)), user_context=open_document)

    # then
    assert run.ungraded
    assert run.evaluation.fill_error is not None


def test_a_transient_failure_does_not_stop_the_takeaways_after_it() -> None:
    # given
    takeaways = _StubTakeaways(httpx.ConnectError("refused"))

    # when
    run = _editor_run(_editor_pages(), ["page3", "page4"], takeaways)

    # then
    assert len(takeaways.requests) == 2
    assert run.ungraded
    assert run.takeaways_by_editor == 1


def test_the_takeaways_written_by_the_editor_reach_langfuse(monkeypatch: pytest.MonkeyPatch) -> None:
    # given
    _install_takeaways(monkeypatch, _StubTakeaways())

    # when
    ctx = _scored(
        monkeypatch, {"narrative": _NARRATIVE}, [_editor_turn(_editor_pages(), ["page3", "page4"])], judge=_FakeJudge()
    )

    # then
    assert ctx.scores["document_takeaways_by_editor"] == 2
    assert ctx.score_types["document_takeaways_by_editor"] == "NUMERIC"
    assert ctx.scores["document_summaries_present"] == 1.0


def test_no_takeaway_score_is_published_when_nothing_was_left_to_the_editor(monkeypatch: pytest.MonkeyPatch) -> None:
    # given
    _install_takeaways(monkeypatch, _StubTakeaways())

    # when
    ctx = _scored(monkeypatch, {"narrative": _NARRATIVE}, [_editor_turn(_v2_written_pages(), [])], judge=_FakeJudge())

    # then
    assert "document_takeaways_by_editor" not in ctx.scores


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

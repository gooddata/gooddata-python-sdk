# (C) 2026 GoodData Corporation
from __future__ import annotations

import json
from typing import Any, cast

import httpx
import pytest
from gooddata_eval.core.agentic import chat_summary
from gooddata_eval.core.dataset.langfuse_source import _item_from_raw
from gooddata_eval.core.models import AgenticSummaryInput, WidgetExecution

_AFM = {
    "attributes": [],
    "measures": [{"localIdentifier": "m", "definition": {"measure": {"item": {}}}}],
    "filters": [],
}
_SPEC = {"dimensions": [{"localIdentifier": "dim_0", "itemIdentifiers": ["measureGroup"]}]}


def _context(*widget_ids: str, referenced: list[str] | None = None) -> dict[str, Any]:
    widgets: list[dict[str, Any]] = [
        {"widgetId": w, "title": f"Title {w}", "widgetType": "insight", "resultId": f"stale-{w}"} for w in widget_ids
    ]
    context: dict[str, Any] = {"view": {"dashboard": {"id": "d", "widgets": widgets}}}
    if referenced is not None:
        context["referencedObjects"] = [
            {"context": {"type": "DASHBOARD", "id": "d"}, "objects": [{"type": "WIDGET", "id": r} for r in referenced]}
        ]
    return context


def _input(scope: str = "dashboard", *widget_ids: str) -> AgenticSummaryInput:
    return AgenticSummaryInput.model_validate(
        {"scope": scope, "executions": {w: {"afm": _AFM, "result_spec": _SPEC} for w in widget_ids}}
    )


def test_fresh_result_ids_replace_the_stored_ones_and_a_failed_widget_has_none() -> None:
    stored = _context("a", "b")
    sent = chat_summary.with_result_ids(stored, {"a": "fresh-a", "b": None})
    widgets = sent["view"]["dashboard"]["widgets"]
    assert widgets[0]["resultId"] == "fresh-a"
    assert "resultId" not in widgets[1]
    # the stored item is not changed: the next run starts from it again
    assert stored["view"]["dashboard"]["widgets"][0]["resultId"] == "stale-a"


def test_a_widget_without_a_stored_execution_is_reported() -> None:
    context = _context("a", "b")
    context["view"]["dashboard"]["widgets"].append({"widgetId": "note", "widgetType": "richText"})
    assert chat_summary.missing_executions(context, _input("dashboard", "a").executions) == ["b"]


def test_the_ui_question_names_the_referenced_widget() -> None:
    context = _context("a", "b", referenced=["b"])
    assert chat_summary.default_question(_input("widget", "a", "b"), context) == 'Summarize the visualization "Title b"'
    assert chat_summary.default_question(_input("dashboard", "a", "b"), context) == "Summarize this dashboard"


@pytest.mark.parametrize("referenced", [[], ["a", "b"]])
def test_a_widget_summary_without_exactly_one_referenced_widget_needs_a_question(referenced: list[str]) -> None:
    with pytest.raises(ValueError, match="exactly one referenced widget"):
        chat_summary.default_question(_input("widget", "a", "b"), _context("a", "b", referenced=referenced))


def test_execute_widget_posts_the_stored_execution_and_returns_the_result_id() -> None:
    seen: list[dict[str, Any]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/actions/workspaces/ws/execution/afm/execute"
        seen.append(json.loads(request.content))
        return httpx.Response(200, json={"executionResponse": {"links": {"executionResult": "rid-1"}}})

    with httpx.Client(base_url="https://h", transport=httpx.MockTransport(handler)) as client:
        rid = chat_summary.execute_widget(client, "ws", WidgetExecution(afm=_AFM, result_spec=_SPEC))
    assert rid == "rid-1"
    assert seen == [{"execution": _AFM, "resultSpec": _SPEC}]


def test_execute_widgets_keeps_a_failed_widget_as_none(monkeypatch: pytest.MonkeyPatch) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        if body["execution"]["measures"][0]["localIdentifier"] == "bad":
            return httpx.Response(400, json={"detail": "bad filter"})
        return httpx.Response(200, json={"executionResponse": {"links": {"executionResult": "rid-ok"}}})

    real_client = httpx.Client
    monkeypatch.setattr(
        chat_summary.httpx, "Client", lambda **kw: real_client(transport=httpx.MockTransport(handler), **kw)
    )
    bad = {**_AFM, "measures": [{"localIdentifier": "bad", "definition": {}}]}
    executions = {"ok": WidgetExecution(afm=_AFM), "bad": WidgetExecution(afm=bad)}
    assert chat_summary.execute_widgets("https://h", "t", "ws", executions) == {"ok": "rid-ok", "bad": None}


def test_a_failed_turn_ends_the_conversation() -> None:
    class _Client:
        def __init__(self) -> None:
            self.sent: list[str] = []

        def send_message(self, conversation_id: str, question: str, *, user_context: dict) -> Any:
            self.sent.append(question)
            if question == "second":
                raise chat_summary.ChatError("boom")
            return object()

    client = _Client()
    turns = chat_summary.run_summary_conversation(
        cast(chat_summary.ChatClient, client), "c", ["first", "second", "third"], {}
    )
    assert client.sent == ["first", "second"]
    assert [t.error is None for t in turns] == [True, False]


def test_the_langfuse_item_carries_the_summary_input_from_its_metadata() -> None:
    raw = {
        "id": "i1",
        "input": "[dashboard] 2. Sales · all time",
        "expectedOutput": {"must_include": ["x"]},
        "metadata": {
            "test_kind": "agentic_summary",
            "user_context": _context("a"),
            "agentic_summary_input": {
                "scope": "dashboard",
                "executions": {"a": {"afm": _AFM, "result_spec": _SPEC}},
                "follow_ups": [{"question": "Why?", "expected_output": {"must_not_include": ["a cause"]}}],
            },
        },
    }
    item = _item_from_raw(raw, dataset_name="agent_summary", test_kind="visualization")
    assert item.test_kind == "agentic_summary"
    assert item.agentic_summary_input is not None
    assert item.agentic_summary_input.follow_ups[0].question == "Why?"
    assert item.user_context == _context("a")


def test_an_invalid_summary_input_fails_loudly() -> None:
    raw = {"id": "i2", "input": "q", "expectedOutput": {}, "metadata": {"agentic_summary_input": {"scope": "page"}}}
    with pytest.raises(ValueError, match="invalid `agentic_summary_input`"):
        _item_from_raw(raw, dataset_name="agent_summary", test_kind="visualization")

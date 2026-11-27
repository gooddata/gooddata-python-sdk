# (C) 2026 GoodData Corporation
from __future__ import annotations

import json
from typing import Any, cast

import httpx
import pytest
from gooddata_eval.cli.agentic_runner import item_runs_in_parallel
from gooddata_eval.core.agentic import chat_summary
from gooddata_eval.core.dataset.langfuse_source import _item_from_raw
from gooddata_eval.core.evaluators._llm_judge import JudgeResponseError
from gooddata_eval.core.models import AgenticSummaryInput, ChatResult, DatasetItem, WidgetBaseline, WidgetExecution

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
    item = _item_from_raw(raw, dataset_name="chat_summary", test_kind="visualization")
    assert item.test_kind == "agentic_summary"
    assert item.agentic_summary_input is not None
    assert item.agentic_summary_input.follow_ups[0].question == "Why?"
    assert item.user_context == _context("a")


def test_an_invalid_summary_input_fails_loudly() -> None:
    raw = {"id": "i2", "input": "q", "expectedOutput": {}, "metadata": {"agentic_summary_input": {"scope": "page"}}}
    with pytest.raises(ValueError, match="invalid `agentic_summary_input`"):
        _item_from_raw(raw, dataset_name="chat_summary", test_kind="visualization")


# ---------- baseline ----------


def _result(data: list, total: int) -> dict[str, Any]:
    return {"data": data, "paging": {"total": [total, 1]}}


def test_the_baseline_reads_data_rows_and_sum() -> None:
    assert chat_summary.baseline_of(_result([[1.0], [2.5]], 2)) == WidgetBaseline(
        has_data=True, row_count=2, value_sum=3.5
    )
    assert chat_summary.baseline_of(None) == WidgetBaseline(has_data=False, row_count=0, value_sum=0.0)


def test_a_changed_widget_is_named_with_old_and_new_values() -> None:
    inp = AgenticSummaryInput.model_validate(
        {
            "scope": "widget",
            "executions": {
                "w": {"afm": {}, "baseline": {"has_data": True, "row_count": 92, "value_sum": 1000.0}},
                "x": {"afm": {}},
            },
        }
    )
    problems = chat_summary.baseline_problems(
        inp.executions, {"w": _result([], 0), "x": None}, {"w": "Net sales over time"}
    )
    assert problems == [
        'widget "Net sales over time": has_data True → False, row_count 92 → 0, value_sum 1,000.00 → 0.00'
    ]
    same = {"w": _result([[400.0], [600.0]], 92)}
    assert chat_summary.baseline_problems(inp.executions, same, {}) == []


def test_changed_data_stops_the_run_before_any_conversation(monkeypatch: pytest.MonkeyPatch) -> None:
    opened: list[str] = []

    class _Client:
        def __init__(self, **_kwargs: Any) -> None:
            pass

        def create_conversation(self) -> str:
            opened.append("conversation")
            return "c1"

        def close(self) -> None:
            pass

    inp = AgenticSummaryInput.model_validate(
        {
            "scope": "dashboard",
            "executions": {"w": {"afm": _AFM, "baseline": {"has_data": True, "row_count": 92, "value_sum": 1000.0}}},
        }
    )
    monkeypatch.setattr(chat_summary, "ChatClient", _Client)
    monkeypatch.setattr(chat_summary, "execute_widgets", lambda *_a, **_k: {"w": "r1"})
    monkeypatch.setattr(chat_summary, "fetch_results", lambda *_a, **_k: {"w": _result([], 0)})

    with pytest.raises(chat_summary.DataBaselineError, match="row_count 92 → 0"):
        chat_summary.run_chat_summary("h", "t", "ws", inp, _context("w"))
    assert opened == []


@pytest.mark.parametrize(
    ("question", "follow_ups", "parallel"),
    [
        (None, [], True),
        (None, [{"question": "Which one is the largest?"}], False),
        ("Give me a brief executive summary", [], False),
    ],
)
def test_a_summary_item_with_free_text_runs_serially(question: str | None, follow_ups: list, parallel: bool) -> None:
    item = DatasetItem(
        id="i1",
        dataset_name="d",
        test_kind="agentic_summary",
        question="[widget] Sales",
        expected_output={},
        agentic_summary_input=AgenticSummaryInput.model_validate(
            {"scope": "widget", "question": question, "follow_ups": follow_ups}
        ),
    )
    assert item_runs_in_parallel(item) is parallel


def test_a_failed_execution_stops_the_run_and_is_not_called_a_data_change(monkeypatch: pytest.MonkeyPatch) -> None:
    opened: list[str] = []

    class _Client:
        def __init__(self, **_kwargs: Any) -> None:
            pass

        def create_conversation(self) -> str:
            opened.append("conversation")
            return "c1"

        def close(self) -> None:
            pass

    baseline = {"has_data": True, "row_count": 1, "value_sum": 10.0}
    inp = AgenticSummaryInput.model_validate(
        {"scope": "dashboard", "executions": {w: {"afm": _AFM, "baseline": baseline} for w in ("a", "b", "c")}}
    )
    monkeypatch.setattr(chat_summary, "ChatClient", _Client)
    monkeypatch.setattr(chat_summary, "execute_widgets", lambda *_a, **_k: {"a": "r1", "b": None, "c": "r3"})
    monkeypatch.setattr(
        chat_summary, "fetch_results", lambda *_a, **_k: {"a": _result([[10.0]], 1), "b": None, "c": None}
    )

    with pytest.raises(chat_summary.WidgetExecutionError) as info:
        chat_summary.run_chat_summary("h", "t", "ws", inp, _context("a", "b", "c"))
    assert info.value.problems == [
        'widget "Title b": the execution failed',
        'widget "Title c": the result could not be read',
    ]
    assert opened == []

    def failed(*_args: Any, **_kwargs: Any) -> list:
        raise info.value

    monkeypatch.setattr(chat_summary, "run_chat_summary", failed)
    with pytest.raises(chat_summary.ChatSummaryAssertionError, match="a stored widget execution failed") as item:
        chat_summary.evaluate_agentic_summary("h", "t", "ws", "[dashboard] Sales", inp, _context("a", "b", "c"), {})
    assert item.value.harness_error == {"status": "error", "reason": "widget_execution_failed"}
    assert item.value.detail["widgets_executed"] is False


def test_a_misspelt_format_key_fails_before_any_execution(monkeypatch: pytest.MonkeyPatch) -> None:
    def never(*_args: Any, **_kwargs: Any) -> list:
        raise AssertionError("the item must not run")

    monkeypatch.setattr(chat_summary, "run_chat_summary", never)
    with pytest.raises(ValueError, match="item: unknown `format` keys"):
        chat_summary.evaluate_agentic_summary(
            "h", "t", "ws", "[widget] Sales", AgenticSummaryInput(scope="widget"), {}, {"format": {"no_heading": True}}
        )
    follow_up = AgenticSummaryInput.model_validate(
        {"scope": "widget", "follow_ups": [{"question": "Which?", "expected_output": {"no_tool_call": True}}]}
    )
    with pytest.raises(ValueError, match="follow-up 1: unknown expected_output keys"):
        chat_summary.evaluate_agentic_summary("h", "t", "ws", "[widget] Sales", follow_up, {}, {})


def test_a_changed_baseline_is_an_error_item_without_a_chat(monkeypatch: pytest.MonkeyPatch) -> None:
    def changed(*_args: Any, **_kwargs: Any) -> list:
        raise chat_summary.DataBaselineError(['widget "Sales": row_count 92 → 0'])

    monkeypatch.setattr(chat_summary, "run_chat_summary", changed)
    with pytest.raises(chat_summary.ChatSummaryAssertionError) as info:
        chat_summary.evaluate_agentic_summary(
            "h", "t", "ws", "[widget] Sales", AgenticSummaryInput(scope="widget"), {}, {}, k=2
        )
    exc = info.value
    assert exc.harness_error == {"status": "error", "reason": "data_baseline_changed"}
    assert exc.detail == {"data_baseline": False, "data_baseline_reason": 'widget "Sales": row_count 92 → 0'}
    assert exc.runs_effective == 0


class _Judge:
    model = "stub"

    def __init__(self, verdict: bool | None) -> None:
        self.verdict = verdict

    def score(self, input: str, expected_output: str, actual_output: str) -> tuple[bool, str]:
        if self.verdict is None:
            raise JudgeResponseError("unreadable")
        return self.verdict, "stub"


def _conversation(answer: str) -> chat_summary.SummaryConversation:
    table = json.dumps(
        {
            "results": [
                {
                    "data": {
                        "columns": [{"name": "Customer", "type": "attribute"}, {"name": "Net Sales", "type": "metric"}],
                        "row_labels": [["Tracy Carter"], ["Tammy Long"]],
                        "data": [[1317241.93], [1301535.2]],
                        "row_count": 2,
                    }
                }
            ]
        }
    )
    result = ChatResult.model_validate(
        {
            "textResponse": answer,
            "toolCallEvents": [
                {"functionName": "execute_existing_visualizations", "functionArguments": "{}", "result": table}
            ],
        }
    )
    return chat_summary.SummaryConversation(
        "c", turns=[chat_summary.SummaryTurn("Summarize", result=result)], scope=None, widgets_total=1
    )


@pytest.mark.parametrize(
    ("answer", "verdict", "outcome"),
    [
        ("Tracy Carter leads with $1.3 M.", True, "pass"),
        ("Tammy Long leads with $1.5 M.", True, "fail"),  # an invented figure
        ("Tracy Carter leads with $1.3 M.", None, "error"),  # no run got a verdict
    ],
)
def test_the_item_gates_on_its_runs(
    monkeypatch: pytest.MonkeyPatch, answer: str, verdict: bool | None, outcome: str
) -> None:
    monkeypatch.setattr(
        chat_summary, "run_chat_summary", lambda *a, **k: [_conversation(answer), _conversation(answer)]
    )
    monkeypatch.setattr(chat_summary, "make_judges", lambda model=None: (_Judge(verdict), _Judge(False)))
    args = ("h", "t", "ws", "[widget] Top Spenders", AgenticSummaryInput(scope="widget"), {}, {"must_include": ["x"]})
    if outcome == "pass":
        result = chat_summary.evaluate_agentic_summary(*args, k=2)
        assert result.runs_passed == 2
        assert result.best_run_latency_s is not None
        assert "tool_calls" in result.detail
        return
    error_cls = chat_summary.ChatSummaryAssertionError if outcome == "fail" else JudgeResponseError
    with pytest.raises(error_cls) as info:
        chat_summary.evaluate_agentic_summary(*args, k=2)
    assert info.value.runs_passed == 0
    if outcome == "error":
        assert info.value.harness_error is not None
    else:
        assert info.value.detail["figures_grounded"] is False

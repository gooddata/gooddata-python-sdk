# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
"""The opt-in search-tool checks. Response shapes are trimmed from runs on the ecommerce_demo fixture."""

import json
import sys
import threading
from contextlib import contextmanager
from dataclasses import fields
from typing import Any
from unittest.mock import MagicMock, patch

import httpx
import pytest
from gooddata_eval.cli.agentic_runner import _dispatch_agentic, item_runs_in_parallel, run_agentic_items
from gooddata_eval.core.agentic._search_expectation import (
    SEARCH_OPTION_KEYS,
    SearchExpectation,
    deterministic_checks,
    parse_expectation,
    raw_ids,
    returned_refs,
)
from gooddata_eval.core.agentic.search_tool import (
    SEARCH_CONDITIONAL_SCORES,
    SEARCH_DIAGNOSTIC_SCORES,
    SearchToolAssertionError,
    _judge_provider_errors,
    _tool_correctness,
    evaluate_agentic_search_tool,
    run_agentic_search_tool,
)
from gooddata_eval.core.chat.sse_client import ChatError, TurnTimeoutError
from gooddata_eval.core.evaluators._llm_judge import JudgeVerdict
from gooddata_eval.core.models import AgenticEvalOutcome, ChatResult, DatasetItem

_MODULE = "gooddata_eval.core.agentic.search_tool"
_HOST = "http://host"


def _search_call(args: dict, objects: list[dict] | None = None) -> dict:
    result = {"objects": objects or [], "returned_count": len(objects or []), "search_results_ref": "search_1"}
    return {"functionName": "search_objects", "functionArguments": json.dumps(args), "result": json.dumps(result)}


def _obj(object_type: str, object_id: str, final_type: str | None = None) -> dict:
    return {"id": object_id, "type": object_type, "final_type": final_type or object_type, "title": object_id}


def _widget(*objects: tuple[str, str]) -> dict:
    return {
        "type": "searchResults",
        "objects": [{"id": object_id, "type": object_type, "title": object_id} for object_type, object_id in objects],
        "requestedObjectType": objects[0][0] if objects else "metric",
    }


def _turn(
    text: str = "Found 2 results.",
    calls: list[dict] | None = None,
    widgets: list[dict] | None = None,
) -> ChatResult:
    return ChatResult.model_validate(
        {"textResponse": text, "toolCallEvents": calls or [], "searchResults": widgets or [], "responseId": "resp"}
    )


_NET_SALES_CALL = _search_call(
    {"keywords": ["Net Sales"], "object_types": ["metric", "fact"], "limit": 20, "compatible_with_afm": None},
    [_obj("metric", "net_sales"), _obj("metric", "total_sales")],
)
_COMPATIBLE_CALL = _search_call(
    {
        "keywords": None,
        "object_types": ["attribute", "date_attribute"],
        "limit": 100,
        "compatible_with_afm": {
            "measures": [{"id": "net_sales", "type": "metric", "aggregation": None}],
            "attributes": [],
        },
    },
    [
        _obj("attribute", "customer_created_date.dayOfMonth", "date_attribute"),
        _obj("attribute", "product_category"),
    ],
)


def _client(*turns: Any) -> MagicMock:
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    client.send_message.side_effect = list(turns)
    return client


def _run(expected_output: dict, *turns: Any, judge: Any = None) -> Any:
    client = _client(*turns)
    with patch(f"{_MODULE}.ChatClient", return_value=client), patch(f"{_MODULE}.LLMJudge", return_value=judge):
        summary = run_agentic_search_tool(
            host=_HOST, token="tok", workspace_id="ws", question="Find Net Sales", expected_output=expected_output
        )
    # The scored turn is the question, sent last in the run's own conversation.
    assert client.send_message.call_args.args == ("conv-1", "Find Net Sales")
    return summary.best, client


def _evaluate(expected_output: dict, *turns: Any) -> Any:
    client = _client(*turns)
    with patch(f"{_MODULE}.ChatClient", return_value=client):
        return evaluate_agentic_search_tool(
            host=_HOST, token="tok", workspace_id="ws", question="Find Net Sales", expected_output=expected_output
        )


# --- parsing -------------------------------------------------------------------------------------


def test_an_item_with_only_tool_call_has_no_checks():
    spec = parse_expectation({"tool_call": {"function_name": "search_objects", "function_arguments": {"limit": 10}}})
    assert spec.tool_args == {"limit": 10}
    assert spec.has_checks is False


@pytest.mark.parametrize(
    ("expected_output", "message"),
    [
        ("search", "must be an object"),
        ({"expect_widgets": True}, "unknown keys"),
        ({"expected_objects": ["metrics/net_sales"]}, "known type"),
        ({"expected_objects": ["metric/"]}, "known type"),
        ({"expected_objects": "metric/net_sales"}, "non-empty list"),
        ({"expected_objects": []}, "non-empty list"),
        ({"answer_rubric": ["says more exist", " "]}, "non-empty strings"),
        ({"setup_turns": [False]}, "non-empty strings"),
        ({"expect_widget": "yes"}, "true or false"),
        ({"no_raw_ids": 1}, "true or false"),
        ({"expected_limit": True}, "positive integer"),
        ({"expected_limit": 0}, "positive integer"),
        ({"required_tools": ["search_objects"], "forbidden_tools": ["search_objects"]}, "both required and forbidden"),
        ({"tool_call": {"function_name": "search_knowledge"}}, "function_name"),
        ({"tool_call": "search_objects"}, "tool_call must be an object"),
        ({"tool_call": {"function_arguments": ["Net Sales"]}}, "function_arguments must be an object"),
        ({"tool_call": {"function_arguments": {"compatible_with_afm": {"measures": 0}}}}, "compatible_with"),
        ({"tool_call": {"function_arguments": {"compatible_with_afm": {"metrics": []}}}}, "compatible_with_afm"),
        (
            {"tool_call": {"function_arguments": {"compatible_with_afm": {"measures": ["net_sales"]}}}},
            "compatible_with",
        ),
        ({"tool_call": {"function_arguments": {"compatible_with_afm": {"measures": "net_sales"}}}}, "compatible_with"),
        ({}, "asserts nothing"),
        ({"tool_call": {"function_arguments": {"keywords": ["x"]}}, "report_only": True}, "no check to report"),
        ({"setup_turns": ["Search for revenue"], "report_only": True}, "no check to report"),
        # Nothing could fail these: tool_selection does not gate and tool_correctness only informs.
        ({"search_required": False}, "search_required: false needs a check"),
        ({"search_required": False, "tool_call": {"function_arguments": {"keywords": ["x"]}}}, "needs a check"),
        ({"search_required": False, "setup_turns": ["Search for revenue"]}, "needs a check"),
        ({"search_required": False, "report_only": True}, "needs a check"),
    ],
)
def test_a_malformed_item_is_rejected(expected_output: Any, message: str):
    with pytest.raises(ValueError, match=message):
        parse_expectation(expected_output)


@pytest.mark.parametrize("afm", [{"measures": 0}, {"measures": 1}, {"attributes": True}, {"measures": ["net_sales"]}])
@pytest.mark.parametrize("with_output", [False, True])
def test_malformed_bare_arguments_fail_before_any_request(afm: dict, with_output: bool):
    client = MagicMock()
    with patch(f"{_MODULE}.ChatClient", return_value=client), pytest.raises(ValueError, match="compatible_with_afm"):
        run_agentic_search_tool(
            host=_HOST,
            token="tok",
            workspace_id="ws",
            question="q",
            expected_tool_call={"compatible_with_afm": afm},
            expected_output={"expect_widget": True} if with_output else None,
        )
    client.create_conversation.assert_not_called()
    client.send_message.assert_not_called()


@pytest.mark.parametrize("with_output", [False, True])
def test_falsy_bare_arguments_are_validated_too(with_output: bool):
    client = MagicMock()
    bare: Any = []
    with patch(f"{_MODULE}.ChatClient", return_value=client), pytest.raises(ValueError, match="must be an object"):
        run_agentic_search_tool(
            host=_HOST,
            token="tok",
            workspace_id="ws",
            question="q",
            expected_tool_call=bare,
            expected_output={"expect_widget": True} if with_output else None,
        )
    client.create_conversation.assert_not_called()


def test_a_tool_call_without_arguments_is_an_item():
    spec = parse_expectation({"tool_call": {"function_arguments": {}}})
    assert spec.tool_args == {}
    assert spec.has_checks is False


def test_a_malformed_item_fails_before_any_request():
    client = MagicMock()
    with patch(f"{_MODULE}.ChatClient", return_value=client), pytest.raises(ValueError, match="unknown keys"):
        evaluate_agentic_search_tool(
            host=_HOST, token="tok", workspace_id="ws", question="q", expected_output={"expected_object": ["x"]}
        )
    client.create_conversation.assert_not_called()
    client.send_message.assert_not_called()


def test_every_option_key_is_an_expectation_field():
    assert {f.name for f in fields(SearchExpectation)} >= SEARCH_OPTION_KEYS


# --- tool_correctness ----------------------------------------------------------------------------


def test_tool_correctness_accepts_a_later_call():
    events = _turn(calls=[_NET_SALES_CALL, _COMPATIBLE_CALL]).tool_call_events
    expected = {"compatible_with_afm": {"measures": [{"id": "net_sales"}]}}
    assert _tool_correctness(events, expected) is True


def test_tool_correctness_compares_the_afm_loosely():
    events = _turn(calls=[_COMPATIBLE_CALL]).tool_call_events
    assert _tool_correctness(events, {"compatible_with_afm": {"measures": [{"id": "net_sales", "aggregation": None}]}})
    assert _tool_correctness(events, {"compatible_with_afm": {"measures": [{"id": "net_sales", "type": "metric"}]}})
    assert not _tool_correctness(events, {"compatible_with_afm": {"measures": [{"id": "sell_through"}]}})
    assert not _tool_correctness(events, {"compatible_with_afm": {"measures": [{"id": "net_sales", "type": "fact"}]}})


def test_tool_correctness_fails_bare_afm_ids_instead_of_crashing():
    events = _turn(calls=[_COMPATIBLE_CALL]).tool_call_events
    assert not _tool_correctness(events, {"compatible_with_afm": {"measures": ["net_sales"]}})


def test_tool_correctness_fails_an_afm_collection_that_is_not_a_list():
    odd = _search_call({"compatible_with_afm": {"measures": 1, "attributes": None}})
    assert not _tool_correctness(
        _turn(calls=[odd]).tool_call_events, {"compatible_with_afm": {"measures": [{"id": "x"}]}}
    )
    attrs = _search_call({"compatible_with_afm": {"measures": 1, "attributes": [{"id": "product_category"}]}})
    expected = {"compatible_with_afm": {"attributes": [{"id": "product_category"}]}}
    assert not _tool_correctness(_turn(calls=[attrs]).tool_call_events, expected)


def test_tool_correctness_reads_null_arguments_as_none():
    null_args = {"functionName": "search_objects", "functionArguments": "null", "result": "null"}
    assert _tool_correctness(_turn(calls=[null_args]).tool_call_events, {}) is True
    assert not _tool_correctness(_turn(calls=[null_args]).tool_call_events, {"keywords": ["Net Sales"]})


def test_tool_correctness_fails_an_afm_the_agent_never_sent():
    events = _turn(calls=[_NET_SALES_CALL]).tool_call_events
    assert not _tool_correctness(events, {"compatible_with_afm": {"measures": [{"id": "net_sales"}]}})


# --- deterministic checks ------------------------------------------------------------------------


def test_expected_objects_are_read_from_an_internal_search_without_widget():
    result = _turn(calls=[_NET_SALES_CALL, _COMPATIBLE_CALL])
    checks, _ = deterministic_checks(parse_expectation({"expected_objects": ["attribute/product_category"]}), result)
    assert checks == {"search_expected_objects": True}


def test_expected_objects_are_read_from_the_widget():
    result = _turn(widgets=[_widget(("dashboard", "370ec88c-6c35-4d2c-9e2d-3ef7cbd8e2f1"))])
    spec = parse_expectation({"expected_objects": ["dashboard/370ec88c-6c35-4d2c-9e2d-3ef7cbd8e2f1"]})
    assert deterministic_checks(spec, result)[0] == {"search_expected_objects": True}


def test_every_expected_object_must_be_returned():
    result = _turn(calls=[_NET_SALES_CALL])
    spec = parse_expectation({"expected_objects": ["metric/net_sales", "metric/total_customers"]})
    checks, details = deterministic_checks(spec, result)
    assert checks == {"search_expected_objects": False}
    assert details["search_expected_objects"]["missing"] == ["metric/total_customers"]


def test_an_attribute_matches_by_any_of_its_spellings():
    result = _turn(calls=[_COMPATIBLE_CALL])
    for ref in ("attribute/customer_created_date.dayOfMonth", "date_attribute/customer_created_date.dayOfMonth"):
        assert deterministic_checks(parse_expectation({"expected_objects": [ref]}), result)[0][
            "search_expected_objects"
        ]
    assert deterministic_checks(parse_expectation({"expected_objects": ["label/product_category"]}), result)[0][
        "search_expected_objects"
    ]


def test_an_object_type_is_not_ignored():
    result = _turn(calls=[_NET_SALES_CALL])
    assert not deterministic_checks(parse_expectation({"expected_objects": ["fact/net_sales"]}), result)[0][
        "search_expected_objects"
    ]


def test_returned_objects_of_other_synced_types_are_read():
    date_dataset = _search_call({"keywords": ["date"]}, [_obj("dataset", "dt_order", "date"), _obj("parameter", "p_1")])
    result = _turn(calls=[date_dataset])
    spec = parse_expectation({"expected_objects": ["date/dt_order", "metric/net_sales"]})
    checks, details = deterministic_checks(spec, result)
    assert details["search_expected_objects"]["missing"] == ["metric/net_sales"]
    assert returned_refs(result) == ["date/dt_order", "parameter/p_1"]


def test_a_result_that_is_not_an_object_returns_nothing():
    odd = {"functionName": "search_objects", "functionArguments": "null", "result": '"no objects"'}
    result = _turn(calls=[odd])
    assert returned_refs(result) == []
    checks, _ = deterministic_checks(parse_expectation({"expected_objects": ["metric/x"], "expected_limit": 5}), result)
    assert checks == {"search_expected_objects": False, "search_limit": False}


def test_objects_that_are_not_a_list_return_nothing():
    odd = {"functionName": "search_objects", "functionArguments": "{}", "result": '{"objects": 1}'}
    result = _turn(calls=[odd], widgets=[{"type": "searchResults", "objects": 1}])
    assert returned_refs(result) == []


def test_returned_refs_keep_the_first_spelling_and_order():
    result = _turn(calls=[_COMPATIBLE_CALL], widgets=[_widget(("attribute", "customer_created_date.dayOfMonth"))])
    assert returned_refs(result) == ["date_attribute/customer_created_date.dayOfMonth", "attribute/product_category"]


@pytest.mark.parametrize(
    ("expect", "widgets", "ok"), [(True, 1, True), (True, 0, False), (False, 0, True), (False, 1, False)]
)
def test_widget(expect: bool, widgets: int, ok: bool):
    result = _turn(widgets=[_widget(("metric", "net_sales"))] * widgets)
    assert deterministic_checks(parse_expectation({"expect_widget": expect}), result)[0] == {"search_widget": ok}


def test_routing_needs_every_required_tool_and_no_forbidden_one():
    describe = {"functionName": "get_object_with_children", "functionArguments": "{}"}
    result = _turn(calls=[_NET_SALES_CALL, describe])
    ok = parse_expectation({"required_tools": ["search_objects", "get_object_with_children"]})
    assert deterministic_checks(ok, result)[0] == {"search_routing": True}
    knowledge = parse_expectation({"forbidden_tools": ["search_knowledge", "get_object_with_children"]})
    checks, details = deterministic_checks(knowledge, result)
    assert checks == {"search_routing": False}
    assert details["search_routing"]["forbidden_called"] == ["get_object_with_children"]


def test_limit_passes_when_any_call_asked_for_it():
    retry = _search_call({"keywords": None, "object_types": ["metric"], "limit": 100})
    first = _search_call({"keywords": None, "object_types": ["metric"], "limit": 20})
    result = _turn(calls=[first, retry])
    assert deterministic_checks(parse_expectation({"expected_limit": 20}), result)[0] == {"search_limit": True}
    assert deterministic_checks(parse_expectation({"expected_limit": 50}), result)[0] == {"search_limit": False}


@pytest.mark.parametrize(
    ("text", "found"),
    [
        ("Found 10 eligible metrics. `{metric/orders_all_time}` ignores dashboard filters.", []),
        ("It is used in {visualization/03b89e08-ee06-4e1f-88d8-bbd805c691cc}.", []),
        ("I searched metric/fact/attribute together.", []),
        ("Use a date/time attribute, label/value pairs, the dataset/table or a metric/KPI.", []),
        ("Search metric/revenue.", []),
        ("The dataset is date/dt_order.", ["date/dt_order"]),
        ("See 03b89e08-ee06-4e1f-88d8-bbd805c691cc.", ["03b89e08-ee06-4e1f-88d8-bbd805c691cc"]),
        ("The id is metric/net_sales.", ["metric/net_sales"]),
        ("Use attribute/customer_created_date.dayOfMonth.", ["attribute/customer_created_date.dayOfMonth"]),
    ],
)
def test_raw_ids_allow_chips_only(text: str, found: list[str]):
    assert raw_ids(text) == found


# --- runs ----------------------------------------------------------------------------------------


def test_setup_turns_go_first_and_only_the_last_turn_is_scored():
    setup = _turn(text="Found 10 results for revenue.", calls=[_search_call({"keywords": ["revenue"]})])
    scored = _turn(
        text="Found 5 dashboards.",
        calls=[_search_call({"keywords": ["revenue"], "object_types": ["dashboard"]})],
        widgets=[_widget(("dashboard", "092929af"))],
    )
    expected = {
        "tool_call": {"function_arguments": {"object_types": ["dashboard"]}},
        "setup_turns": ["Search for revenue"],
        "expect_widget": True,
    }
    run, client = _run(expected, setup, scored)
    assert [c.args[1] for c in client.send_message.call_args_list] == ["Search for revenue", "Find Net Sales"]
    assert {c.args[0] for c in client.send_message.call_args_list} == {"conv-1"}
    assert run.passed and run.tool_correct
    assert len(run.tool_call_events) == 1


def test_a_failed_setup_turn_records_its_own_latency():
    clock = MagicMock()
    clock.monotonic.side_effect = [10.0, 12.5]
    with patch(f"{_MODULE}.time", clock), pytest.raises(SearchToolAssertionError) as exc_info:
        _evaluate({"setup_turns": ["Search for revenue"], "expect_widget": True}, TurnTimeoutError("too slow"))
    assert exc_info.value.run_latencies_s == [2.5]


@pytest.mark.parametrize(
    ("setup", "exit_reason"),
    [
        (ChatError("stream broke"), "chat_error"),
        (TurnTimeoutError("too slow"), "agent_timeout"),
        (httpx.ConnectError("connection refused"), "chat_error"),
        (_turn(text=""), "agent_silent"),
    ],
)
def test_a_failed_setup_turn_is_the_agents_fail(setup: Any, exit_reason: str):
    with pytest.raises(SearchToolAssertionError) as exc_info:
        _evaluate({"setup_turns": ["Search for revenue"], "expect_widget": True}, setup)
    error = exc_info.value
    run = error.failed_runs[0]
    assert run["outcome"]["status"] == "fail"
    assert run["exit_reason"] == exit_reason
    assert [check["name"] for check in run["failed_checks"]] == ["setup_turn"]
    assert not hasattr(error, "harness_error")
    # The question was never sent, so no search verdict was measured.
    assert not {"tool_selected", "tool_correct"} & set(error.detail)


@pytest.mark.parametrize(
    ("error", "exit_reason"),
    [(ChatError("stream broke"), "chat_error"), (TurnTimeoutError("too slow"), "agent_timeout")],
)
def test_a_failed_question_turn_fails_its_run_and_keeps_the_others(error: ChatError, exit_reason: str):
    error.partial_result = _turn(text="", calls=[_NET_SALES_CALL])
    client = _client(_turn(calls=[_NET_SALES_CALL]), error)
    client.create_conversation.side_effect = ["conv-1", "conv-2"]
    with patch(f"{_MODULE}.ChatClient", return_value=client):
        outcome = evaluate_agentic_search_tool(
            host=_HOST,
            token="tok",
            workspace_id="ws",
            question="Find Net Sales",
            expected_output={"tool_call": {"function_arguments": {"keywords": ["Net Sales"]}}},
            k=2,
        )
    assert (outcome.runs_passed, outcome.runs_effective) == (1, 2)
    run = outcome.failed_runs[0]
    assert run["outcome"]["status"] == "fail"
    assert run["exit_reason"] == exit_reason
    assert [check["name"] for check in run["failed_checks"]] == ["question_turn"]
    # What the agent did before the turn failed is kept for diagnosis, not scored.
    assert run["tool_names"] == ["search_objects"]


def test_a_failed_setup_turn_keeps_what_the_agent_did():
    error = TurnTimeoutError("too slow")
    error.partial_result = _turn(text="", calls=[_search_call({"keywords": ["revenue"]})])
    with pytest.raises(SearchToolAssertionError) as exc_info:
        _evaluate({"setup_turns": ["Search for revenue"], "expect_widget": True}, error)
    run = exc_info.value.failed_runs[0]
    assert [check["name"] for check in run["failed_checks"]] == ["setup_turn"]
    assert run["tool_names"] == ["search_objects"]


def test_an_http_status_that_outlasts_the_retries_fails_its_run_and_keeps_the_others():
    request = httpx.Request("POST", f"{_HOST}/chat")
    error = httpx.HTTPStatusError("503", request=request, response=httpx.Response(503, request=request))
    client = _client(_turn(calls=[_NET_SALES_CALL]), error)
    client.create_conversation.side_effect = ["conv-1", "conv-2"]
    with patch(f"{_MODULE}.ChatClient", return_value=client):
        outcome = evaluate_agentic_search_tool(
            host=_HOST,
            token="tok",
            workspace_id="ws",
            question="Find Net Sales",
            expected_output={"tool_call": {"function_arguments": {"keywords": ["Net Sales"]}}},
            k=2,
        )
    assert (outcome.runs_passed, outcome.runs_effective) == (1, 2)
    run = outcome.failed_runs[0]
    assert run["exit_reason"] == "chat_error"
    assert [check["name"] for check in run["failed_checks"]] == ["question_turn"]


def test_search_required_false_passes_without_a_search():
    chart = {"functionName": "create_visualization", "functionArguments": "{}"}
    run, _ = _run({"search_required": False, "expect_widget": False}, _turn(text="Here is the chart.", calls=[chart]))
    assert run.passed
    assert run.tool_selected is False


def test_a_failing_check_fails_the_run():
    run, _ = _run({"tool_call": {"function_arguments": {}}, "expect_widget": True}, _turn(calls=[_NET_SALES_CALL]))
    assert run.tool_selected
    assert not run.passed


def test_report_only_checks_do_not_gate():
    expected = {"expect_widget": True, "report_only": True}
    outcome = _evaluate(expected, _turn(calls=[_NET_SALES_CALL]))
    assert "search_widget" not in outcome.detail
    assert outcome.detail["diagnostics"] == {"search_widget": False}
    assert outcome.runs_passed == 1


def _report_only_rubric(turn: ChatResult, verdict: JudgeVerdict) -> Any:
    expected = {"answer_rubric": ["Lists net sales"], "report_only": True}
    with (
        patch(f"{_MODULE}.ChatClient", return_value=_client(turn)),
        patch(f"{_MODULE}.LLMJudge"),
        patch(f"{_MODULE}.score_run", return_value=verdict),
    ):
        return evaluate_agentic_search_tool(
            host=_HOST, token="tok", workspace_id="ws", question="Find Net Sales", expected_output=expected
        )


def test_a_report_only_rubric_without_verdict_is_not_reported_false():
    outcome = _report_only_rubric(_turn(calls=[_NET_SALES_CALL]), _UNREADABLE)
    assert outcome.runs_passed == 1
    assert "search_answer" not in outcome.detail.get("diagnostics", {})
    assert outcome.detail["check_details"]["search_answer"].startswith("harness:")


def test_a_report_only_rubric_without_verdict_is_not_a_failed_check():
    with pytest.raises(SearchToolAssertionError) as exc_info:
        _report_only_rubric(_turn(text="Net Sales is 5."), _UNREADABLE)
    run = exc_info.value.failed_runs[0]
    assert run["outcome"]["status"] == "fail"
    assert [check["name"] for check in run["failed_checks"]] == ["tool_selection"]


def test_a_run_that_rightly_skips_search_keeps_the_search_verdicts_out_of_quality():
    chart = {"functionName": "create_visualization", "functionArguments": "{}"}
    outcome = _evaluate({"search_required": False, "expect_widget": False}, _turn(calls=[chart]))
    booleans = {k: v for k, v in outcome.detail.items() if isinstance(v, bool)}
    assert booleans == {"search_widget": True}
    assert outcome.detail["diagnostics"] == {"tool_selected": False, "tool_correct": False}


def test_an_empty_answer_fails_the_rubric_without_asking_the_judge():
    judge = MagicMock()
    with patch(f"{_MODULE}.score_run") as score:
        run, _ = _run({"answer_rubric": ["Says more exist"]}, _turn(text="", calls=[_NET_SALES_CALL]), judge=judge)
    score.assert_not_called()
    assert run.checks == {"search_answer": False}
    assert run.check_details["search_answer"].startswith("empty answer")
    assert run.harness_error is None


def test_the_judge_grades_the_last_reply_with_the_setup_as_context():
    expected = {"answer_rubric": ["Names only 1. Overview"], "setup_turns": ["Describe Revenue Trend"]}
    with patch(f"{_MODULE}.score_run", return_value=JudgeVerdict(passed=True, reasoning="ok")) as score:
        run, _ = _run(expected, _turn(text="It shows revenue."), _turn(calls=[_NET_SALES_CALL]), judge=MagicMock())
    assert run.checks == {"search_answer": True}
    kwargs = score.call_args.kwargs
    assert kwargs["expected_output"] == "- Names only 1. Overview"
    assert kwargs["actual_output"].endswith("User: Find Net Sales\n\nAssistant: Found 2 results.")
    assert kwargs["actual_output"].startswith("User: Describe Revenue Trend")


def test_a_failed_rubric_keeps_the_judges_reasoning():
    verdict = JudgeVerdict(passed=False, reasoning="does not say more exist")
    with patch(f"{_MODULE}.score_run", return_value=verdict):
        run, _ = _run({"answer_rubric": ["Says more exist"]}, _turn(calls=[_NET_SALES_CALL]), judge=MagicMock())
    assert run.checks == {"search_answer": False}
    assert run.check_details["search_answer"] == "does not say more exist"
    assert run.harness_error is None


def test_a_judge_provider_error_leaves_the_answer_ungraded():
    with patch(f"{_MODULE}.score_run", side_effect=TimeoutError("judge timed out")):
        run, _ = _run({"answer_rubric": ["Says more exist"]}, _turn(calls=[_NET_SALES_CALL]), judge=MagicMock())
    assert run.harness_error == "judge gave no verdict: TimeoutError: judge timed out"
    assert run.harness_checks == ("search_answer",)


def test_judge_provider_errors_need_no_llm_judge_extra():
    with patch.dict(sys.modules, {"openai": None}):
        assert _judge_provider_errors() == (httpx.HTTPError, TimeoutError, ConnectionError)


def test_judge_provider_errors_include_the_openai_error_with_the_extra():
    openai = pytest.importorskip("openai")
    assert _judge_provider_errors() == (openai.OpenAIError, httpx.HTTPError, TimeoutError, ConnectionError)


def test_a_rubric_without_a_judge_is_a_programming_error():
    with pytest.raises(RuntimeError, match="LLM judge"):
        _run({"answer_rubric": ["Says more exist"]}, _turn(calls=[_NET_SALES_CALL]), judge=None)


def test_a_judge_without_verdict_labels_the_run_error():
    expected = {"tool_call": {"function_arguments": {"keywords": ["Net Sales"]}}, "answer_rubric": ["Lists net sales"]}
    verdict = JudgeVerdict(passed=False, reasoning="", error="unreadable")
    client = _client(_turn(calls=[_NET_SALES_CALL]))
    with (
        patch(f"{_MODULE}.ChatClient", return_value=client),
        patch(f"{_MODULE}.LLMJudge"),
        patch(f"{_MODULE}.score_run", return_value=verdict),
        pytest.raises(SearchToolAssertionError) as exc_info,
    ):
        evaluate_agentic_search_tool(
            host=_HOST, token="tok", workspace_id="ws", question="Find Net Sales", expected_output=expected
        )
    run = exc_info.value.failed_runs[0]
    assert run["outcome"]["status"] == "error"
    assert "1 ungraded" in str(exc_info.value)
    assert run["error"] == "judge gave no verdict: unreadable"
    assert "search_answer" not in exc_info.value.detail
    assert exc_info.value.detail["check_details"]["search_answer"].startswith("harness:")
    assert exc_info.value.detail["unscored_runs"] == 1


_UNREADABLE = JudgeVerdict(passed=False, reasoning="", error="unreadable")


def test_a_passing_item_counts_its_ungraded_runs():
    expected = {"answer_rubric": ["Lists net sales"]}
    client = _client(_turn(calls=[_NET_SALES_CALL]), _turn(calls=[_NET_SALES_CALL]))
    client.create_conversation.side_effect = ["conv-1", "conv-2"]
    with (
        patch(f"{_MODULE}.ChatClient", return_value=client),
        patch(f"{_MODULE}.LLMJudge"),
        patch(f"{_MODULE}.score_run", side_effect=[JudgeVerdict(passed=True, reasoning="ok"), _UNREADABLE]),
    ):
        outcome = evaluate_agentic_search_tool(
            host=_HOST, token="tok", workspace_id="ws", question="Find Net Sales", expected_output=expected, k=2
        )
    assert outcome.runs_passed == 1
    assert outcome.detail["unscored_runs"] == 1


def test_the_best_run_is_a_graded_one_before_an_ungraded_one():
    """Neither run passed. The ungraded one holds more passing checks, but it has no verdict to show."""
    expected = {"expect_widget": True, "no_raw_ids": True, "answer_rubric": ["Lists net sales"]}
    shown = _turn(calls=[_NET_SALES_CALL], widgets=[_widget(("metric", "net_sales"))])
    client = _client(shown, _turn(calls=[_NET_SALES_CALL]))
    client.create_conversation.side_effect = ["conv-1", "conv-2"]
    graded_fail = JudgeVerdict(passed=False, reasoning="does not list net sales")
    with (
        patch(f"{_MODULE}.ChatClient", return_value=client),
        patch(f"{_MODULE}.LLMJudge"),
        patch(f"{_MODULE}.score_run", side_effect=[_UNREADABLE, graded_fail]),
    ):
        summary = run_agentic_search_tool(
            host=_HOST, token="tok", workspace_id="ws", question="Find Net Sales", expected_output=expected, k=2
        )
    assert summary.run_results[0].harness_error is not None
    assert summary.best.conversation_id == "conv-2"


def test_a_judge_error_is_not_blamed_on_the_harness_when_another_check_failed():
    expected = {"answer_rubric": ["Lists net sales"], "expect_widget": True}
    verdict = JudgeVerdict(passed=False, reasoning="", error="unreadable")
    client = _client(_turn(calls=[_NET_SALES_CALL]))
    with (
        patch(f"{_MODULE}.ChatClient", return_value=client),
        patch(f"{_MODULE}.LLMJudge"),
        patch(f"{_MODULE}.score_run", return_value=verdict),
        pytest.raises(SearchToolAssertionError) as exc_info,
    ):
        evaluate_agentic_search_tool(
            host=_HOST, token="tok", workspace_id="ws", question="Find Net Sales", expected_output=expected
        )
    assert exc_info.value.failed_runs[0]["outcome"]["status"] == "fail"


def test_expected_output_without_tool_call_takes_the_bare_arguments():
    client = _client(_turn(calls=[_NET_SALES_CALL]))
    with patch(f"{_MODULE}.ChatClient", return_value=client):
        summary = run_agentic_search_tool(
            host=_HOST,
            token="tok",
            workspace_id="ws",
            question="Find Net Sales",
            expected_tool_call={"object_types": ["dashboard"]},
            expected_output={"expect_widget": False},
        )
    assert summary.best.tool_correct is False
    assert summary.best.passed


def test_an_item_with_only_tool_call_keeps_the_legacy_detail():
    outcome = _evaluate(
        {"tool_call": {"function_name": "search_objects", "function_arguments": {"keywords": ["Net Sales"]}}},
        _turn(calls=[_NET_SALES_CALL]),
    )
    assert set(outcome.detail) == {
        "tool_selected",
        "tool_correct",
        "tool_call_names",
        "latency_breakdown",
        "tool_calls",
    }


def test_every_check_is_a_published_score_name():
    expected = {
        "tool_call": {"function_arguments": {"keywords": ["Net Sales"]}},
        "expected_objects": ["metric/net_sales"],
        "expect_widget": False,
        "required_tools": ["search_objects"],
        "answer_rubric": ["Lists net sales"],
        "expected_limit": 20,
        "no_raw_ids": True,
    }
    with patch(f"{_MODULE}.score_run", return_value=JudgeVerdict(passed=True, reasoning="ok")):
        run, _ = _run(expected, _turn(calls=[_NET_SALES_CALL]), judge=MagicMock())
    assert set(run.checks) == set(SEARCH_CONDITIONAL_SCORES)
    assert run.passed


def _dispatch(expected_output: Any) -> dict:
    item = DatasetItem(
        id="i1", dataset_name="d", test_kind="agentic_search", question="q", expected_output=expected_output
    )
    with patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_search_tool") as mock_eval:
        _dispatch_agentic(
            item,
            host="https://h",
            token="tok",
            workspace_id="ws1",
            k=1,
            langfuse=None,
            run_ts="2026-01-01",
            model_version_override=None,
        )
    return mock_eval.call_args.kwargs


@pytest.mark.parametrize(
    "expected_output",
    [
        {"tool_call": {"function_arguments": {"keywords": ["x"]}}},
        {"tool_call": {"function_arguments": {"keywords": ["x"]}}, "expected_object": ["metric/x"]},
        {"expected_objects": ["metric/x"]},
        {"expected_object": ["metric/x"]},
    ],
)
def test_the_cli_passes_the_item_shape_whole(expected_output: dict):
    kwargs = _dispatch(expected_output)
    assert kwargs["expected_output"] == expected_output
    assert kwargs["expected_tool_call"] is None


@pytest.mark.parametrize("expected_output", ["search", ["metric/x"], None])
def test_the_cli_rejects_an_expected_output_that_is_not_an_object(expected_output: Any):
    with pytest.raises(ValueError, match="must be an object"):
        _dispatch(expected_output)


def test_the_cli_passes_bare_arguments_as_the_tool_call():
    kwargs = _dispatch({"keywords": ["x"], "object_types": ["metric"]})
    assert kwargs["expected_tool_call"] == {"keywords": ["x"], "object_types": ["metric"]}
    assert kwargs["expected_output"] is None


@pytest.mark.parametrize(
    ("expected_output", "parallel"),
    [
        ({"keywords": ["x"]}, True),
        ({"tool_call": {"function_arguments": {}}, "expect_widget": True}, True),
        ({"setup_turns": ["Search for revenue"], "expect_widget": True}, False),
    ],
)
def test_a_search_item_with_setup_turns_runs_serially(expected_output: dict, parallel: bool):
    """A setup turn is free text the kind's read-only clearance does not cover."""
    item = DatasetItem(
        id="i1", dataset_name="d", test_kind="agentic_search", question="q", expected_output=expected_output
    )
    assert item_runs_in_parallel(item) is parallel


# --- Langfuse scores -----------------------------------------------------------------------------


class _FakeCtx:
    """Records what the deferred Langfuse block writes, without a Langfuse."""

    def __init__(self) -> None:
        self.scores: dict[str, float] = {}
        self.strict: dict = {}
        self.run_metadata: dict = {}

    def trace(self, _conversation_id: str) -> None:
        return None

    @contextmanager
    def observe(self, _trace: Any, _run_idx: int, **_kwargs: Any) -> Any:
        yield "trace-id"

    def score(self, _tid: Any, *, name: str, value: Any, data_type: str, comment: str | None = None) -> None:
        self.scores[name] = float(value)

    def quality(self, _tid: Any, *, strict_checks: dict, latency_sec: Any, cost_usd: Any) -> None:
        self.strict = strict_checks


def _scored(expected_output: dict, verdict: JudgeVerdict | None = None, turns: tuple = ()) -> _FakeCtx:
    """Run one item with Langfuse on, then execute the deferred block against a fake ctx."""
    captured: dict = {}

    def _capture(_link: Any, _identity: Any, **kwargs: Any) -> None:
        captured.update(kwargs)

    with (
        patch(f"{_MODULE}.ChatClient", return_value=_client(*(turns or (_turn(calls=[_NET_SALES_CALL]),)))),
        patch(f"{_MODULE}.LLMJudge"),
        patch(f"{_MODULE}.score_run", return_value=verdict),
        patch(f"{_MODULE}.submit_trace_scoring", side_effect=_capture),
    ):
        try:
            evaluate_agentic_search_tool(
                host=_HOST,
                token="tok",
                workspace_id="ws",
                question="Find Net Sales",
                expected_output=expected_output,
                langfuse=MagicMock(),
                dataset_item_id="ds-1",
            )
        except SearchToolAssertionError:
            pass  # scores are written before the gate raise
    ctx = _FakeCtx()
    captured["write_scores"](ctx)
    return ctx


def test_scores_publish_the_checks_but_not_an_ungraded_answer():
    expected = {
        "tool_call": {"function_arguments": {"keywords": ["Net Sales"]}},
        "expect_widget": False,
        "answer_rubric": ["Lists net sales"],
    }
    ctx = _scored(expected, JudgeVerdict(passed=False, reasoning="", error="unreadable"))
    assert ctx.scores["tool_selection"] == 1.0
    assert ctx.scores["tool_correctness"] == 1.0
    assert ctx.scores["search_widget"] == 1.0
    assert ctx.scores["eval_error"] == 1.0
    assert "search_answer" not in ctx.scores
    assert ctx.strict == {"tool_selection": True, "search_widget": True}


def test_scores_of_a_report_only_item_without_search_or_arguments():
    ctx = _scored({"search_required": False, "expect_widget": True, "report_only": True})
    assert "tool_correctness" not in ctx.scores
    assert ctx.scores["search_widget_diagnostic"] == 0.0
    assert ctx.scores["tool_selection_diagnostic"] == 1.0
    assert not {"search_widget", "tool_selection"} & set(ctx.scores)
    assert ctx.strict == {"passed": True}


def test_a_score_that_does_not_gate_is_published_as_a_diagnostic():
    """One score name, one meaning: a gating check never shares its name with a check that did not gate."""
    ctx = _scored({"search_required": False, "expect_widget": True})
    assert ctx.scores["tool_selection_diagnostic"] == 1.0
    assert ctx.scores["search_widget"] == 0.0
    assert "tool_selection" not in ctx.scores
    assert ctx.strict == {"search_widget": False}


def test_every_check_of_a_report_only_item_is_a_published_diagnostic_name():
    expected = {
        "tool_call": {"function_arguments": {"keywords": ["Net Sales"]}},
        "search_required": False,
        "expected_objects": ["metric/net_sales"],
        "expect_widget": False,
        "required_tools": ["search_objects"],
        "answer_rubric": ["Lists net sales"],
        "expected_limit": 20,
        "no_raw_ids": True,
        "report_only": True,
    }
    ctx = _scored(expected, JudgeVerdict(passed=True, reasoning="ok"))
    published = {name for name in ctx.scores if name.endswith("_diagnostic")}
    assert published == set(SEARCH_DIAGNOSTIC_SCORES)
    assert not set(SEARCH_CONDITIONAL_SCORES) & set(ctx.scores)


def test_a_failed_turn_publishes_no_search_verdict():
    """A setup timeout is not a search the agent got wrong: the question was never sent."""
    expected = {
        "tool_call": {"function_arguments": {"keywords": ["Net Sales"]}},
        "setup_turns": ["Search for revenue"],
        "expect_widget": True,
    }
    ctx = _scored(expected, turns=(TurnTimeoutError("too slow"),))
    assert not {"tool_selection", "tool_correctness", "search_widget"} & set(ctx.scores)
    assert ctx.strict == {"passed": False}


def test_a_search_item_with_setup_turns_runs_in_the_serial_phase():
    def item(item_id: str, expected_output: dict) -> DatasetItem:
        return DatasetItem(
            id=item_id, dataset_name="d", test_kind="agentic_search", question="q", expected_output=expected_output
        )

    threads: dict[str, str] = {}

    def fake_eval(*, dataset_item_id: str, **_kw: Any) -> AgenticEvalOutcome:
        threads[dataset_item_id] = threading.current_thread().name
        return AgenticEvalOutcome(conversation_id="c", detail={})

    items = [
        item("setup", {"setup_turns": ["Search for revenue"], "expect_widget": True}),
        item("bare", {"keywords": ["x"]}),
    ]
    with patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_search_tool", side_effect=fake_eval):
        run_agentic_items(items, host="h", token="t", workspace_id="ws1", run_ts="ts", concurrency=2)
    assert threads["setup"] == threading.main_thread().name
    assert threads["bare"].startswith("agentic")

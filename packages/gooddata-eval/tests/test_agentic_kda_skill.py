# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
import json
from contextlib import contextmanager
from unittest.mock import MagicMock, patch

import httpx
import pytest
from gooddata_eval.core.agentic.kda_skill import (
    KdaEvaluation,
    KdaSkillAssertionError,
    _build_clarification_prompt,
    _build_period_hint,
    _evaluate_run,
    _extract_kda_calls,
    evaluate_agentic_kda_skill,
    run_agentic_kda_skill,
)
from gooddata_eval.core.chat.sse_client import ChatError, TransientChatError
from gooddata_eval.core.models import ChatResult

_EXPECTED = {"Measure": {"type": "metric", "id": "revenue"}}


def _tool_call(name: str, result: dict | None = None, arguments: dict | None = None):
    return {
        "functionName": name,
        "functionArguments": "{}" if arguments is None else json.dumps(arguments),
        "result": None if result is None else json.dumps(result),
    }


def _kda_chat_result(
    *,
    success: bool = True,
    text: str = "Here is the analysis.",
    stream_ended: bool = True,
    turn_wall_clock_sec: float | None = None,
    reasoning_steps: list[str] | None = None,
    response_id: str | None = None,
) -> ChatResult:
    return ChatResult.model_validate(
        {
            "textResponse": text,
            "toolCallEvents": [
                _tool_call("create_key_driver_analysis", arguments={"measure": {"type": "metric", "id": "revenue"}}),
                _tool_call("execute_key_driver_analysis", result={"success": success, "data": {"summary": {}}}),
            ],
            "reasoningStepCount": 1,
            "reasoningSteps": reasoning_steps or [],
            "responseId": response_id,
            "stream_ended": stream_ended,
            "turn_wall_clock_sec": turn_wall_clock_sec,
        }
    )


def _no_kda_chat_result(
    text: str = "I could not find that metric.",
    *,
    stream_ended: bool = True,
    turn_wall_clock_sec: float | None = None,
    reasoning_steps: list[str] | None = None,
    response_id: str | None = None,
) -> ChatResult:
    return ChatResult.model_validate(
        {
            "textResponse": text,
            "toolCallEvents": [],
            "reasoningStepCount": 1,
            "reasoningSteps": reasoning_steps or [],
            "responseId": response_id,
            "stream_ended": stream_ended,
            "turn_wall_clock_sec": turn_wall_clock_sec,
        }
    )


def _client() -> MagicMock:
    """A chat client whose conversations are all ``conv-1``.

    Callers override only what they vary -- ``send_message`` and the rest are ordinary
    mock attributes.
    """
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    return client


@contextmanager
def _patched(client, *, simulated_reply=None, simulated_error=None):
    """Patch kda_skill's ChatClient, and optionally its simulated-user helper.

    ``simulated_reply`` is what the simulated user answers; ``simulated_error`` makes it
    raise instead. Yields the ``generate_simulated_kda_response`` mock, or None when the
    test asked for neither.
    """
    with patch("gooddata_eval.core.agentic.kda_skill.ChatClient", return_value=client):
        if simulated_reply is None and simulated_error is None:
            yield None
        else:
            with patch(
                "gooddata_eval.core.agentic.kda_skill.generate_simulated_kda_response",
                return_value=simulated_reply,
                side_effect=simulated_error,
            ) as mock_simulate:
                yield mock_simulate


@contextmanager
def _patched_without_langfuse(client):
    """Patch kda_skill's ChatClient and stub Langfuse discovery out (`langfuse=None` path)."""
    with (
        _patched(client),
        patch("gooddata_eval.core.agentic._langfuse.try_make_langfuse_client", return_value=None),
    ):
        yield


@contextmanager
def _patched_with_langfuse_scores(client, trace):
    """Patch kda_skill's ChatClient plus every _langfuse helper the scoring block calls.

    ``trace`` is the trace ``find_traces_per_conversation`` returns for ``conv-1``, and the
    one ``observe`` hands back. Yields ``(mock_score_safe, mock_log_quality_and_value_scores)``.
    """
    with (
        _patched(client),
        patch("gooddata_eval.core.agentic._langfuse.build_run_context", return_value=("run-base", {})),
        patch("gooddata_eval.core.agentic._langfuse.find_traces_per_conversation", return_value={"conv-1": trace}),
        patch("gooddata_eval.core.agentic._langfuse.observe") as mock_observe,
        patch("gooddata_eval.core.agentic._langfuse.score_safe") as mock_score_safe,
        patch("gooddata_eval.core.agentic._langfuse.log_quality_and_value_scores") as mock_log_scores,
    ):
        mock_observe.return_value.__enter__.return_value = trace.id
        yield mock_score_safe, mock_log_scores


# --------------------------------------------------------------------------- #
# _build_clarification_prompt
# --------------------------------------------------------------------------- #
def test_build_clarification_prompt_omits_reference_clause_when_no_candidates_or_period():
    # Regression (chi My's review): with no usable candidates, the old code still asserted
    # "an acceptable metric/fact is None 'None'" as if it were a real option -- likely to
    # make the simulated user invent a metric literally named "None". No candidates and no
    # period hint must drop the whole "For reference, ..." clause instead.
    prompt = _build_clarification_prompt("Which date range?", None, None)
    assert "None" not in prompt
    assert "For reference" not in prompt


def test_build_clarification_prompt_includes_only_period_hint_when_no_candidates():
    prompt = _build_clarification_prompt("Which period?", None, "2026-2 vs 2026-1")
    assert "None" not in prompt
    assert "the intended time period is 2026-2 vs 2026-1" in prompt


def test_build_clarification_prompt_includes_candidates_and_period_hint():
    prompt = _build_clarification_prompt(
        "Which metric and period?", {"type": "metric", "id": "revenue"}, "2026-2 vs 2026-1"
    )
    assert "an acceptable metric/fact is metric 'revenue'" in prompt
    assert "the intended time period is 2026-2 vs 2026-1" in prompt


# --------------------------------------------------------------------------- #
# _build_period_hint
# --------------------------------------------------------------------------- #
def test_build_period_hint_none_when_no_period_fields_present():
    assert _build_period_hint({"Measure": {"type": "metric", "id": "revenue"}}) is None


def test_build_period_hint_all_three_fields():
    hint = _build_period_hint(
        {"Date Attribute": "transaction_date.quarter", "Analyzed Period": "2026-2", "Reference Period": "2026-1"}
    )
    assert hint == "transaction_date.quarter, comparing 2026-2 to 2026-1"


def test_build_period_hint_date_attribute_only():
    # A dataset item carrying only Date Attribute (agent asks "which date dimension should
    # I use?") must still get an answerable hint -- this used to require all 3 fields and
    # reproduced the same gap the metric-clarification fix closed, just narrower.
    assert _build_period_hint({"Date Attribute": "transaction_date.quarter"}) == "transaction_date.quarter"


def test_build_period_hint_analyzed_period_only():
    assert _build_period_hint({"Analyzed Period": "2026-2"}) == "period 2026-2"


def test_build_period_hint_reference_period_only():
    assert _build_period_hint({"Reference Period": "2026-1"}) == "compared to 2026-1"


# --------------------------------------------------------------------------- #
# _evaluate_run
# --------------------------------------------------------------------------- #
def test_evaluate_run_computes_core_fields_from_create_and_execute_args():
    ev = _evaluate_run({"measure": {"type": "metric", "id": "revenue"}}, {"success": True}, turn_completed=True)
    assert (ev.triggered, ev.executed, ev.success, ev.turn_completed) == (True, True, True, True)


def test_evaluate_run_false_when_kda_never_triggered():
    ev = _evaluate_run(None, None, turn_completed=False)
    assert (ev.triggered, ev.executed, ev.success) == (False, False, False)


def test_evaluate_run_success_false_when_execute_result_says_so():
    ev = _evaluate_run({"measure": {}}, {"success": False}, turn_completed=True)
    assert (ev.triggered, ev.executed, ev.success) == (True, True, False)


def test_evaluate_run_passes_through_disambiguated():
    ev = _evaluate_run({"measure": {}}, {"success": True}, turn_completed=True, disambiguated=True)
    assert ev.disambiguated is True


def test_extract_kda_calls_takes_last_execute_on_retry():
    events = (
        _kda_chat_result(success=False).tool_call_events
        + ChatResult.model_validate(
            {
                "toolCallEvents": [
                    _tool_call("execute_key_driver_analysis", result={"success": True, "data": {"summary": {}}}),
                ],
            }
        ).tool_call_events
    )
    create_args, execute_result = _extract_kda_calls(events)
    assert create_args == {"measure": {"type": "metric", "id": "revenue"}}
    assert execute_result == {"success": True, "data": {"summary": {}}}


def test_extract_kda_calls_does_not_pair_a_new_create_with_an_earlier_execute():
    # create_1 -> execute_1(success) -> create_2 (never executed): create_2's args must
    # not get paired with execute_1's stale result -- that would wrongly report the run
    # as executed/succeeded when the actual last attempt never ran.
    events = ChatResult.model_validate(
        {
            "toolCallEvents": [
                _tool_call("create_key_driver_analysis", arguments={"measure": {"type": "metric", "id": "a"}}),
                _tool_call("execute_key_driver_analysis", result={"success": True, "data": {"summary": {}}}),
                _tool_call("create_key_driver_analysis", arguments={"measure": {"type": "metric", "id": "b"}}),
            ]
        }
    ).tool_call_events
    create_args, execute_result = _extract_kda_calls(events)
    assert create_args == {"measure": {"type": "metric", "id": "b"}}
    assert execute_result is None


def test_extract_kda_calls_none_when_no_tool_calls():
    create_args, execute_result = _extract_kda_calls([])
    assert create_args is None
    assert execute_result is None


def test_extract_kda_calls_ignores_execute_call_with_no_result():
    events = ChatResult.model_validate(
        {"toolCallEvents": [_tool_call("execute_key_driver_analysis", result=None)]}
    ).tool_call_events
    _, execute_result = _extract_kda_calls(events)
    assert execute_result is None


# --------------------------------------------------------------------------- #
# KdaEvaluation.strict_pass
# --------------------------------------------------------------------------- #
def _evaluation(**overrides) -> KdaEvaluation:
    fields = {
        "triggered": True,
        "executed": True,
        "success": True,
        "turn_completed": True,
    }
    fields.update(overrides)
    return KdaEvaluation(**fields)


def test_strict_pass_true_when_all_core_checks_pass():
    assert _evaluation().strict_pass is True


def test_strict_pass_false_when_any_core_check_fails():
    assert _evaluation(success=False).strict_pass is False


# --------------------------------------------------------------------------- #
# run_agentic_kda_skill
# --------------------------------------------------------------------------- #
def test_run_agentic_kda_skill_triggers_and_succeeds():
    mock_client = _client()
    mock_client.send_message.return_value = _kda_chat_result(success=True)

    with _patched(mock_client):
        summary = run_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=_EXPECTED,
            k=1,
            max_iterations=1,
        )

    assert summary.pass_at_k is True
    assert summary.best.evaluation.triggered is True
    assert summary.best.evaluation.executed is True
    assert summary.best.evaluation.success is True
    mock_client.close.assert_called_once()


def test_run_agentic_kda_skill_fails_on_sse_cutoff_despite_nonempty_text():
    # Regression guard: an SSE stream cut off mid-answer (a recurring failure mode in this
    # suite) can still have emitted a partial, non-empty text_response before dying. Using
    # "text_response is non-empty" as the completion signal would wrongly call this turn
    # completed; only gen-ai's own response_ended event may.
    mock_client = _client()
    mock_client.send_message.return_value = _kda_chat_result(success=True, stream_ended=False)

    with _patched(mock_client):
        summary = run_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=_EXPECTED,
            k=1,
            max_iterations=1,
        )

    assert summary.pass_at_k is False
    assert summary.best.evaluation.turn_completed is False
    # The KDA call itself still triggered/executed/succeeded -- only completion is in doubt.
    assert summary.best.evaluation.triggered is True
    assert summary.best.evaluation.success is True


def test_run_agentic_kda_skill_survives_send_message_error():
    # A ChatError/TransientChatError raised mid-turn must not propagate out of
    # run_agentic_kda_skill: an uncaught raise here would skip evaluate_agentic_kda_skill's
    # Langfuse-logging loop entirely for this run, leaving nothing but a bare JUnit
    # failure to diagnose from. It must instead surface as a normal (failed) run result,
    # so triggered/executed/success/turn_completed all still get scored as False.
    mock_client = _client()
    mock_client.send_message.side_effect = TransientChatError("gen-ai returned 503")

    with _patched(mock_client):
        summary = run_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=_EXPECTED,
            k=1,
            max_iterations=1,
        )

    assert summary.pass_at_k is False
    assert summary.best.evaluation.turn_completed is False
    assert summary.best.evaluation.triggered is False
    mock_client.close.assert_called_once()


def test_run_agentic_kda_skill_survives_a_raw_httpx_transport_error():
    # The actual failure mode this guards against, not just ChatError: a stream cut off
    # mid-turn raises httpx.RemoteProtocolError/ReadError from inside resp.iter_lines(),
    # which _is_retryable_exc does not recognize as retryable and re-raises as-is -- a
    # narrower `except ChatError` (an earlier version of this fix) would NOT catch this
    # and would still propagate out of run_agentic_kda_skill uncaught.
    mock_client = _client()
    mock_client.send_message.side_effect = httpx.RemoteProtocolError("peer closed connection")

    with _patched(mock_client):
        summary = run_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=_EXPECTED,
            k=1,
            max_iterations=1,
        )

    assert summary.pass_at_k is False
    assert summary.best.evaluation.turn_completed is False
    mock_client.close.assert_called_once()


def test_run_agentic_kda_skill_recovers_kda_calls_from_a_chat_errors_partial_result():
    # ChatError/TransientChatError raised after KDA's own create/execute already streamed
    # through (e.g. a later, unrelated final-summary generation failing with a 500) must
    # not misreport as "the agent never called KDA at all" -- the partial_result attached
    # to the exception is exactly the tool_call_events already seen.
    mock_client = _client()
    mock_client.send_message.side_effect = ChatError(
        "SSE error 500: boom", status_code=500, partial_result=_kda_chat_result(success=True)
    )

    with _patched(mock_client):
        summary = run_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=_EXPECTED,
            k=1,
            max_iterations=1,
        )

    assert summary.best.evaluation.triggered is True
    assert summary.best.evaluation.executed is True
    assert summary.best.evaluation.success is True
    # The error still means the turn itself didn't complete, regardless of what KDA did.
    assert summary.best.evaluation.turn_completed is False


def test_run_agentic_kda_skill_resets_turn_completed_when_a_later_iteration_crashes():
    # iteration 0 asks a clarifying question and ends cleanly (turn_completed=True for
    # THAT iteration); iteration 1 then crashes. Without resetting, the stale True from
    # iteration 0 would still be logged for a run that never actually finished.
    mock_client = _client()
    mock_client.send_message.side_effect = [
        _no_kda_chat_result("Could you clarify which measure?", stream_ended=True),
        httpx.RemoteProtocolError("peer closed connection"),
    ]

    with _patched(mock_client, simulated_reply="Use the revenue metric."):
        summary = run_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=_EXPECTED,
            k=1,
            max_iterations=2,
        )

    assert summary.best.evaluation.turn_completed is False
    assert summary.best.evaluation.triggered is False


def test_run_agentic_kda_skill_turn_not_completed_when_stream_ends_with_empty_text():
    # stream_ended alone is not enough: a turn that ends cleanly but delivers nothing to
    # the user hasn't "delivered a final answer" either (see KdaEvaluation docstring).
    mock_client = _client()
    mock_client.send_message.return_value = _kda_chat_result(success=True, text="   ", stream_ended=True)

    with _patched(mock_client):
        summary = run_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=_EXPECTED,
            k=1,
            max_iterations=1,
        )

    assert summary.best.evaluation.turn_completed is False
    # The KDA call itself still triggered/executed/succeeded -- only completion is in doubt.
    assert summary.best.evaluation.triggered is True
    assert summary.best.evaluation.success is True


def test_run_agentic_kda_skill_marks_disambiguated_after_a_simulated_reply():
    mock_client = _client()
    mock_client.send_message.side_effect = [
        _no_kda_chat_result("Could you clarify which measure?"),
        _kda_chat_result(success=True),
    ]

    with _patched(mock_client, simulated_reply="Use the revenue metric."):
        summary = run_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=_EXPECTED,
            k=1,
            max_iterations=2,
        )

    assert summary.best.evaluation.disambiguated is True
    assert summary.best.evaluation.triggered is True


def test_run_agentic_kda_skill_disambiguates_on_question_followed_by_option_list():
    # Regression (QA-28800): the real captured response ends with a bullet list of
    # candidate metrics. Before this module dropped text classification in favor of
    # always retrying on a non-empty, non-triggering response (matching
    # visualization.py/alert_skill.py), a heuristic that only matched "?" endings gave
    # up after turn 1 (triggered=False) instead of ever nudging the simulated user to
    # pick one.
    mock_client = _client()
    mock_client.send_message.side_effect = [
        _no_kda_chat_result(
            'I found two different "Total Net Revenue" metrics in your data model. '
            "Which one should I analyze for the 2024 vs 2023 drop?\n\n"
            "- {metric/metric_l1_sql_net_sales_summary_net_revenue}\n"
            "- {metric/metric_l1_total_net_revenue}"
        ),
        _kda_chat_result(success=True),
    ]

    with _patched(mock_client, simulated_reply="Use metric_l1_sql_net_sales_summary_net_revenue.") as mock_simulate:
        summary = run_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Why did Total Net Revenue of Net Sales Summary drop in 2024 compared to 2023?",
            expected_output=_EXPECTED,
            k=1,
            max_iterations=2,
        )

    mock_simulate.assert_called_once()
    assert summary.best.evaluation.disambiguated is True
    assert summary.best.evaluation.triggered is True
    assert mock_client.send_message.call_count == 2


def test_run_agentic_kda_skill_retries_on_bold_markdown_option_list_with_no_space():
    # Regression (chi My's review): a prior classifier-based fix required a space right
    # after the list marker, so "**Option 1**: revenue" (bold markdown, no space between
    # the two asterisks) would have been misread as a final answer. Dropping content
    # classification entirely (see run_agentic_kda_skill's docstring) makes this -- and any
    # other future response shape -- a non-issue: a non-triggering, non-empty response
    # always gets a simulated reply now, regardless of how it's formatted.
    mock_client = _client()
    mock_client.send_message.side_effect = [
        _no_kda_chat_result("Which one should I analyze?\n**Option 1**: revenue\n**Option 2**: gross profit"),
        _kda_chat_result(success=True),
    ]

    with _patched(mock_client, simulated_reply="Use revenue.") as mock_simulate:
        summary = run_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Why did revenue drop?",
            expected_output=_EXPECTED,
            k=1,
            max_iterations=2,
        )

    mock_simulate.assert_called_once()
    assert summary.best.evaluation.disambiguated is True
    assert summary.best.evaluation.triggered is True


def test_run_agentic_kda_skill_disambiguates_on_period_clarification():
    # generate_simulated_kda_response used to only know about measure candidates -- if the
    # agent asked about the PERIOD instead, it had nothing period-specific to answer with.
    # Verify the period hint built from expected_output's Date Attribute/Analyzed
    # Period/Reference Period reaches the simulated-reply call.
    expected_output = {
        "Measure": {"type": "metric", "id": "revenue"},
        "Date Attribute": "transaction_date.quarter",
        "Analyzed Period": "2026-2",
        "Reference Period": "2026-1",
    }
    mock_client = _client()
    mock_client.send_message.side_effect = [
        _no_kda_chat_result("Which period would you like to compare?"),
        _kda_chat_result(success=True),
    ]

    with _patched(mock_client, simulated_reply="Compare 2026-2 to 2026-1.") as mock_simulate:
        summary = run_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Why did revenue drop?",
            expected_output=expected_output,
            k=1,
            max_iterations=2,
        )

    mock_simulate.assert_called_once_with(
        "Which period would you like to compare?",
        {"type": "metric", "id": "revenue"},
        "transaction_date.quarter, comparing 2026-2 to 2026-1",
    )
    assert summary.best.evaluation.disambiguated is True
    assert summary.best.evaluation.triggered is True


def test_run_agentic_kda_skill_disambiguates_when_expected_output_is_not_a_dict():
    # DatasetItem.expected_output on the gdc-nas side allows str/list, not just dict.
    # expected_output.get("Measure") would raise AttributeError on those shapes, silently
    # swallowed by the broad except around generate_simulated_kda_response and disabling
    # disambiguation with only a WARNING. Guard so the call still happens, with None
    # candidates, instead of crashing.
    mock_client = _client()
    mock_client.send_message.side_effect = [
        _no_kda_chat_result("Could you clarify which measure?"),
        _kda_chat_result(success=True),
    ]

    with _patched(mock_client, simulated_reply="Use the revenue metric.") as mock_generate:
        summary = run_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=["not", "a", "dict"],
            k=1,
            max_iterations=2,
        )

    mock_generate.assert_called_once_with("Could you clarify which measure?", None, None)
    assert summary.best.evaluation.disambiguated is True
    assert summary.best.evaluation.triggered is True


def test_run_agentic_kda_skill_latency_is_only_the_turn_that_completed_kda():
    # The disambiguation turn's own time, and the simulated-reply generation between
    # turns, must NOT be counted -- only the turn where KDA actually completed reflects
    # gen-ai's own latency; the rest is test-harness overhead (an unrelated OpenAI call).
    mock_client = _client()
    mock_client.send_message.side_effect = [
        _no_kda_chat_result("Could you clarify which measure?", turn_wall_clock_sec=5.0),
        _kda_chat_result(success=True, turn_wall_clock_sec=8.0),
    ]

    with _patched(mock_client, simulated_reply="Use the revenue metric."):
        summary = run_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=_EXPECTED,
            k=1,
            max_iterations=2,
        )

    assert summary.best.turn_wall_clock_sec == 8.0


def test_run_agentic_kda_skill_triggered_but_not_executed_when_execute_tool_is_unavailable():
    # create and execute are always called together in the same turn, or not at all --
    # e.g. when the org has data-sharing with the LLM off, execute_key_driver_analysis
    # isn't registered as a tool at all, so create can succeed alone within a single turn
    # with no execute_result. Must be scored as triggered but not executed immediately,
    # not treated as "execute is coming in a later turn".
    mock_client = _client()
    create_only = ChatResult.model_validate(
        {
            "textResponse": "The analysis is ready. Open it above to review the results.",
            "toolCallEvents": [
                _tool_call("create_key_driver_analysis", arguments={"measure": {"type": "metric", "id": "revenue"}})
            ],
            "stream_ended": True,
            "turn_wall_clock_sec": 3.0,
        }
    )
    mock_client.send_message.return_value = create_only

    with _patched(mock_client):
        summary = run_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=_EXPECTED,
            k=1,
            max_iterations=2,
        )

    assert summary.best.evaluation.triggered is True
    assert summary.best.evaluation.executed is False
    assert summary.best.evaluation.disambiguated is False
    assert summary.best.turn_wall_clock_sec == 3.0
    assert mock_client.send_message.call_count == 1


def test_run_agentic_kda_skill_not_disambiguated_when_kda_triggers_immediately():
    mock_client = _client()
    mock_client.send_message.return_value = _kda_chat_result(success=True)

    with _patched(mock_client):
        summary = run_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=_EXPECTED,
            k=1,
            max_iterations=1,
        )

    assert summary.best.evaluation.disambiguated is False


def test_run_agentic_kda_skill_no_tool_call():
    mock_client = _client()
    mock_client.send_message.return_value = _no_kda_chat_result()

    with _patched(mock_client):
        summary = run_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=_EXPECTED,
            k=1,
            max_iterations=1,
        )

    assert summary.pass_at_k is False
    assert summary.best.evaluation.triggered is False


def test_run_agentic_kda_skill_resolves_after_clarification_turn():
    mock_client = _client()
    mock_client.send_message.side_effect = [
        _no_kda_chat_result("Could you clarify which revenue measure you mean?"),
        _kda_chat_result(success=True),
    ]

    with _patched(mock_client, simulated_reply="The revenue metric is fine.") as mock_simulate:
        summary = run_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=_EXPECTED,
            k=1,
            max_iterations=2,
        )

    mock_simulate.assert_called_once()
    assert summary.pass_at_k is True
    assert mock_client.send_message.call_count == 2


def test_run_agentic_kda_skill_gives_up_after_max_iterations_of_clarification():
    mock_client = _client()
    mock_client.send_message.return_value = _no_kda_chat_result("Could you clarify which measure?")

    with _patched(mock_client, simulated_reply="Please use revenue."):
        summary = run_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=_EXPECTED,
            k=1,
            max_iterations=2,
        )

    assert summary.pass_at_k is False
    assert mock_client.send_message.call_count == 2


def test_run_agentic_kda_skill_disambiguation_then_create_without_execute():
    # Combines both remaining paths in one run -- a disambiguation turn, then a turn where
    # create succeeds but execute_result is None (e.g. execute is unavailable for this
    # org). Confirms this still scores correctly (disambiguated + triggered, not executed)
    # instead of being mistaken for "still waiting on more turns".
    mock_client = _client()
    create_only = ChatResult.model_validate(
        {
            "textResponse": "The analysis is ready. Open it above to review the results.",
            "toolCallEvents": [
                _tool_call("create_key_driver_analysis", arguments={"measure": {"type": "metric", "id": "revenue"}})
            ],
            "stream_ended": True,
        }
    )
    mock_client.send_message.side_effect = [
        _no_kda_chat_result("Could you clarify which measure?"),
        create_only,
    ]

    with _patched(mock_client, simulated_reply="Use the revenue metric."):
        summary = run_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=_EXPECTED,
            k=1,
            max_iterations=2,
        )

    assert mock_client.send_message.call_count == 2
    assert summary.best.evaluation.disambiguated is True
    assert summary.best.evaluation.triggered is True
    assert summary.best.evaluation.executed is False
    assert summary.pass_at_k is False


def test_run_agentic_kda_skill_survives_simulated_reply_failure():
    # The simulated-user helper is a safety net, not the assertion under test -- if it
    # raises, only the current run ends early; earlier completed runs are preserved.
    mock_client = MagicMock()
    mock_client.create_conversation.side_effect = ["conv-1", "conv-2"]
    mock_client.send_message.side_effect = [
        _kda_chat_result(success=True),  # run 0: triggers KDA immediately
        _no_kda_chat_result("Could you clarify which measure?"),  # run 1: asks, then helper blows up
    ]

    with _patched(mock_client, simulated_error=RuntimeError("openai down")):
        summary = run_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=_EXPECTED,
            k=2,
            max_iterations=2,
        )

    assert len(summary.run_results) == 2
    assert summary.run_results[0].evaluation.triggered is True
    assert summary.run_results[1].evaluation.triggered is False
    assert summary.pass_at_k is True  # run 0 still counts


def test_run_agentic_kda_skill_uses_initial_conversation_for_run_0():
    mock_client = MagicMock()
    mock_client.send_message.return_value = _kda_chat_result(success=True)
    with _patched(mock_client):
        run_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=_EXPECTED,
            k=1,
            max_iterations=1,
            initial_conversation_id="existing-conv",
        )
    mock_client.create_conversation.assert_not_called()
    mock_client.delete_conversation.assert_not_called()


def test_run_agentic_kda_skill_creates_fresh_conversations_for_remaining_runs():
    mock_client = MagicMock()
    mock_client.create_conversation.side_effect = ["fresh-1", "fresh-2"]
    mock_client.send_message.return_value = _kda_chat_result(success=True)
    with _patched(mock_client):
        run_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=_EXPECTED,
            k=3,
            max_iterations=1,
            initial_conversation_id="existing-conv",
        )
    assert mock_client.create_conversation.call_count == 2
    assert mock_client.delete_conversation.call_count == 2


@pytest.mark.parametrize("bad_k", [0, -1, -5])
def test_run_agentic_kda_skill_rejects_non_positive_k(bad_k):
    with pytest.raises(ValueError, match="k must be >= 1"):
        run_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=_EXPECTED,
            k=bad_k,
        )


# --------------------------------------------------------------------------- #
# evaluate_agentic_kda_skill
# --------------------------------------------------------------------------- #
def test_evaluate_agentic_kda_skill_raises_on_failure():
    mock_client = _client()
    mock_client.send_message.return_value = _no_kda_chat_result()

    with _patched_without_langfuse(mock_client), pytest.raises(KdaSkillAssertionError):
        evaluate_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=_EXPECTED,
            k=1,
            max_iterations=1,
            langfuse=None,
        )


def test_evaluate_agentic_kda_skill_does_not_raise_on_success():
    mock_client = _client()
    mock_client.send_message.return_value = _kda_chat_result(success=True)

    with _patched_without_langfuse(mock_client):
        evaluate_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=_EXPECTED,
            k=1,
            max_iterations=1,
            langfuse=None,
        )


def test_evaluate_agentic_kda_skill_never_treats_fallback_trace_latency_as_kda_latency():
    # Regression test: when KDA never triggered, whatever trace find_traces_per_conversation's
    # default (max-latency) selector picks is NOT a real KDA turn -- its latency/cost must not
    # be logged as the KDA run's own value_score inputs.
    mock_client = _client()
    mock_client.send_message.return_value = _no_kda_chat_result()

    fallback_trace = MagicMock(id="fallback-trace", latency=999.0, total_cost=5.0)
    mock_langfuse = MagicMock()

    with (
        _patched_with_langfuse_scores(mock_client, fallback_trace) as (_, mock_log_scores),
        pytest.raises(KdaSkillAssertionError),
    ):
        evaluate_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=_EXPECTED,
            k=1,
            max_iterations=1,
            langfuse=mock_langfuse,
            dataset_item_id="item-1",
        )

    mock_log_scores.assert_called_once()
    assert mock_log_scores.call_args.kwargs["latency_sec"] is None
    assert mock_log_scores.call_args.kwargs["cost_usd"] is None


def test_evaluate_agentic_kda_skill_reports_trace_latency_when_kda_triggered():
    # Latency comes from the harness's own wall-clock measurement (ChatResult.turn_wall_clock_sec,
    # set by ChatClient around its send_message() call), not from the trace find_traces_per_
    # conversation happens to return -- that trace isn't necessarily the KDA turn at all (see
    # kda_skill.py's comment on `pt`). Only total_cost still comes from the trace.
    mock_client = _client()
    mock_client.send_message.return_value = _kda_chat_result(success=True, turn_wall_clock_sec=76.0)

    found_trace = MagicMock(id="trace-1", latency=999.0, total_cost=0.02)
    mock_langfuse = MagicMock()

    with _patched_with_langfuse_scores(mock_client, found_trace) as (mock_score_safe, mock_log_scores):
        evaluate_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=_EXPECTED,
            k=1,
            max_iterations=1,
            langfuse=mock_langfuse,
            dataset_item_id="item-1",
        )

    mock_log_scores.assert_called_once()
    assert mock_log_scores.call_args.kwargs["latency_sec"] == 76.0
    assert mock_log_scores.call_args.kwargs["cost_usd"] == 0.02
    wall_clock_calls = [c for c in mock_score_safe.call_args_list if c.kwargs.get("name") == "kda_turn_wall_clock_sec"]
    assert len(wall_clock_calls) == 1
    assert wall_clock_calls[0].kwargs["value"] == 76.0


def test_evaluate_agentic_kda_skill_does_not_log_pass_at_k_or_pass_power_k():
    # Matches metric_skill/alert_skill/guardrail/search_tool/general_question, which all
    # compute pass_at_k/pass_power_k but never log them to Langfuse at their default k=1 --
    # nothing reads a kda_pass_at_1 score, and the score name shifts if k ever changes,
    # silently splitting any Langfuse view built on the old name. Only visualization.py
    # logs this pair, with a real consumer at k=2 (combo_report.py's viz_flaky) that
    # justifies it.
    mock_client = _client()
    mock_client.send_message.return_value = _kda_chat_result(success=True)

    found_trace = MagicMock(id="trace-1", total_cost=0.01)
    mock_langfuse = MagicMock()

    with _patched_with_langfuse_scores(mock_client, found_trace) as (mock_score_safe, _):
        evaluate_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=_EXPECTED,
            k=2,
            max_iterations=1,
            langfuse=mock_langfuse,
            dataset_item_id="item-1",
        )

    logged = {c.kwargs["name"] for c in mock_score_safe.call_args_list}
    assert "kda_pass_at_2" not in logged
    assert "kda_pass_power_2" not in logged
    assert "pass_at_2" not in logged
    assert "pass_power_2" not in logged


def test_run_agentic_kda_skill_accumulates_reasoning_steps_across_iterations():
    """A clarification turn's reasoning is retained even though only the final turn's
    create/execute calls determine the KDA outcome."""
    mock_client = _client()
    mock_client.send_message.side_effect = [
        _no_kda_chat_result("Which metric do you mean?", reasoning_steps=["step one"], response_id="resp-1"),
        _kda_chat_result(reasoning_steps=["step two"], response_id="resp-2"),
    ]

    with _patched(mock_client, simulated_reply="I mean revenue."):
        summary = run_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove the change?",
            expected_output=_EXPECTED,
            k=1,
            max_iterations=2,
        )

    assert summary.best.reasoning_steps == ["step one", "step two"]
    assert summary.best.response_id == "resp-2"


def test_evaluate_agentic_kda_skill_returns_reasoning_steps_on_pass():
    mock_client = _client()
    mock_client.send_message.return_value = _kda_chat_result(
        success=True, reasoning_steps=["analyzing drivers"], response_id="resp-1"
    )

    with _patched_without_langfuse(mock_client):
        outcome = evaluate_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=_EXPECTED,
            k=1,
            max_iterations=1,
            langfuse=None,
        )

    assert outcome.reasoning_steps == ["analyzing drivers"]
    assert outcome.conversation_id == "conv-1"
    assert outcome.response_id == "resp-1"
    assert outcome.detail == {
        "triggered": True,
        "executed": True,
        "success": True,
        "turn_completed": True,
        "disambiguated": False,
        "actual_create_args": {"measure": {"type": "metric", "id": "revenue"}},
        "actual_execute_result": {"success": True, "data": {"summary": {}}},
    }


def test_evaluate_agentic_kda_skill_attaches_reasoning_steps_to_exception_on_fail():
    mock_client = _client()
    mock_client.send_message.return_value = _no_kda_chat_result(
        reasoning_steps=["could not find a measure"], response_id="resp-2"
    )

    with _patched_without_langfuse(mock_client), pytest.raises(KdaSkillAssertionError) as exc_info:
        evaluate_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=_EXPECTED,
            k=1,
            max_iterations=1,
            langfuse=None,
        )

    assert exc_info.value.reasoning_steps == ["could not find a measure"]
    assert exc_info.value.conversation_id == "conv-1"
    assert exc_info.value.response_id == "resp-2"
    assert exc_info.value.detail == {
        "triggered": False,
        "executed": False,
        "success": False,
        "turn_completed": True,
        "disambiguated": False,
        "actual_create_args": None,
        "actual_execute_result": None,
    }


def test_evaluate_agentic_kda_skill_preserves_reasoning_from_a_chat_error_partial_result():
    # Same scenario as test_run_agentic_kda_skill_recovers_kda_calls_from_a_chat_errors_partial_result
    # (KDA create/execute already streamed before an unrelated later failure), but checking that
    # the partial_result's own reasoning_steps/response_id survive onto the exception too, not
    # just the tool-call data.
    mock_client = _client()
    mock_client.send_message.side_effect = ChatError(
        "SSE error 500: boom",
        status_code=500,
        partial_result=_kda_chat_result(
            success=True, reasoning_steps=["analyzing before cutoff"], response_id="resp-3"
        ),
    )

    with _patched_without_langfuse(mock_client), pytest.raises(KdaSkillAssertionError) as exc_info:
        evaluate_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What drove revenue change?",
            expected_output=_EXPECTED,
            k=1,
            max_iterations=1,
            langfuse=None,
        )

    assert exc_info.value.reasoning_steps == ["analyzing before cutoff"]
    assert exc_info.value.response_id == "resp-3"

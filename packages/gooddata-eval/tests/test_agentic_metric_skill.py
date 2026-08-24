# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
import os
import sys
import types
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.agentic.metric_skill import (
    AgenticMetricSummary,
    MetricRunResult,
    MetricSkillAssertionError,
    SimulatedResponseError,
    _delete_metric,
    _extract_metric_result,
    _normalize_maql,
    evaluate_agentic_metric_skill,
    generate_simulated_response,
    run_agentic_metric_skill,
)
from gooddata_eval.core.models import ChatResult, ToolCallEvent


def _create_metric_call(result: str) -> ToolCallEvent:
    return ToolCallEvent(function_name="create_metric", function_arguments="{}", result=result)


_FAILED_RESULT = '{"data": {"isError": true, "error": {"text": "invalid MAQL"}}}'


def test_extract_metric_result_skips_a_failed_retry_and_returns_the_successful_one():
    """QA-29053 regression: agent self-corrects an invalid MAQL by retrying create_metric
    within the same turn; the successful retry must be captured, not the failed first call."""
    calls = [
        _create_metric_call(_FAILED_RESULT),
        _create_metric_call('{"data": {"metric_id": "m1", "maql": "SELECT {metric/foo}"}}'),
    ]
    assert _extract_metric_result(calls) == {"metric_id": "m1", "maql": "SELECT {metric/foo}"}


def test_extract_metric_result_returns_none_when_every_attempt_failed():
    calls = [_create_metric_call(_FAILED_RESULT), _create_metric_call(_FAILED_RESULT)]
    assert _extract_metric_result(calls) is None


def test_extract_metric_result_skips_a_failed_call_after_an_earlier_success():
    # The failed call is last, so reversed() reaches it first and must skip past it.
    calls = [_create_metric_call('{"data": {"metric_id": "m1"}}'), _create_metric_call(_FAILED_RESULT)]
    assert _extract_metric_result(calls) == {"metric_id": "m1"}


def test_extract_metric_result_prefers_the_most_recent_successful_call():
    """Two distinct successful create_metric calls in one turn (not a retry after a
    failure) -- the later one wins."""
    calls = [
        _create_metric_call('{"data": {"metric_id": "m1"}}'),
        _create_metric_call('{"data": {"metric_id": "m2"}}'),
    ]
    assert _extract_metric_result(calls) == {"metric_id": "m2"}


def test_extract_metric_result_skips_a_non_dict_payload():
    # The non-dict payload is last, so reversed() reaches it first and must skip past it.
    calls = [
        _create_metric_call('{"data": {"metric_id": "m2"}}'),
        _create_metric_call('{"data": [{"metric_id": "m1"}]}'),
    ]
    assert _extract_metric_result(calls) == {"metric_id": "m2"}


def test_extract_metric_result_skips_a_non_dict_decoded_result():
    # The whole decoded result (not just its "data" field) is a non-dict here.
    calls = [_create_metric_call('{"metric_id": "m2"}'), _create_metric_call("[]")]
    assert _extract_metric_result(calls) == {"metric_id": "m2"}


def test_extract_metric_result_skips_an_empty_payload():
    # The empty payload is last, so reversed() reaches it first and must skip past it.
    calls = [
        _create_metric_call('{"data": {"metric_id": "m2"}}'),
        _create_metric_call('{"data": {}}'),
    ]
    assert _extract_metric_result(calls) == {"metric_id": "m2"}


def test_normalize_maql_strips_whitespace():
    assert _normalize_maql("  SELECT  { metric/foo }  ") == "select {metric/foo}"


def test_normalize_maql_removes_select_wrapper():
    assert _normalize_maql("(SELECT {metric/abc})") == "{metric/abc}"


def test_generate_simulated_response_prompt_preserves_maql_fidelity(monkeypatch):
    """Regression test for a live-reproduced bug: the old prompt ("reply briefly",
    no instruction to cover clauses the assistant didn't ask about) let the
    simulating LLM silently drop a MAQL's WHERE clause or paraphrase a label id --
    confirmed via a 5x-repeated A/B test (1/5 vs 5/5 fidelity) that this was the
    prompt, not the model (gpt-4o did not fix it under the old prompt either).
    """
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="ok"))]
    mock_client.chat.completions.create.return_value = mock_response

    # `openai` is an optional [llm-judge] extra, not installed in this test env --
    # inject a fake module rather than patching a real one (mirrors how the source
    # itself does `from openai import OpenAI` as a local, guarded import).
    fake_openai_module = types.SimpleNamespace(OpenAI=MagicMock(return_value=mock_client), OpenAIError=Exception)
    monkeypatch.setitem(sys.modules, "openai", fake_openai_module)

    expected_output = {"maql": 'SELECT {metric/spend_amount_-_cutcgco} WHERE {label/ecommerce_indicator_code} = "1"'}
    generate_simulated_response("Which base metric should I use?", expected_output)

    call_kwargs = mock_client.chat.completions.create.call_args.kwargs
    sent_prompt = call_kwargs["messages"][0]["content"]

    assert expected_output["maql"] in sent_prompt
    assert "verbatim" in sent_prompt
    assert "every clause" in sent_prompt
    assert "WHERE" in sent_prompt or "filter" in sent_prompt.lower()
    assert "reply briefly" not in sent_prompt.lower()
    assert call_kwargs["max_tokens"] >= 300


def test_normalize_maql_is_case_insensitive_for_keywords():
    """Regression test for a live-reproduced bug: 'FOR PREVIOUS(...)' vs
    'FOR Previous(...)' scored as a mismatch even though MAQL keywords are
    case-insensitive -- a semantically identical agent answer failed the eval
    purely on keyword casing."""
    actual = "SELECT {metric/active_card_count_-_txn_-_cutcgco} FOR PREVIOUS({label/process_date.year})"
    expected = "SELECT {metric/active_card_count_-_txn_-_cutcgco}\n  FOR Previous({label/process_date.year})"
    assert _normalize_maql(actual) == _normalize_maql(expected)


def test_normalize_maql_preserves_identifier_case():
    # {type/id} references are real, case-sensitive ids -- must never be casefolded.
    assert "Mixed_Case_Id" in _normalize_maql("SELECT {metric/Mixed_Case_Id}")


def test_normalize_maql_preserves_quoted_literal_case():
    """The bug this guards against: naively lowercasing everything outside {..}
    would also lowercase quoted WHERE-clause literal values, which are real,
    case-sensitive data -- not keywords. Two literals differing only in case
    must NOT be treated as equal; that would be a false positive."""
    assert _normalize_maql('WHERE {label/status} = "Active"') != _normalize_maql('WHERE {label/status} = "active"')


def test_metric_run_result_fields():
    r = MetricRunResult(
        conversation_id="c1",
        metric_result={"maql": "SELECT {metric/x}"},
        metric_created=True,
        actual_maql="SELECT {metric/x}",
        maql_correct=True,
        total_turns=1.0,
    )
    assert r.metric_created is True
    assert r.maql_correct is True


def test_agentic_metric_summary_pass_at_k():
    r = MetricRunResult("c1", {"maql": "x"}, True, "x", True, 1.0)
    s = AgenticMetricSummary(run_results=[r], pass_at_k=True, pass_power_k=True, best=r)
    assert s.pass_at_k is True


def test_run_agentic_metric_skill_creates_conversation(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "done",
            "toolCallEvents": [
                {
                    "functionName": "create_metric",
                    "functionArguments": "{}",
                    "result": '{"data": {"maql": "SELECT {metric/foo}"}}',
                }
            ],
            "reasoningStepCount": 1,
        }
    )

    with patch("gooddata_eval.core.agentic.metric_skill.ChatClient", return_value=mock_client):
        summary = run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
            k=1,
            max_iterations=1,
        )

    assert summary.pass_at_k is True
    assert summary.best.metric_created is True
    mock_client.close.assert_called_once()


def test_run_agentic_metric_skill_closes_client_on_no_result():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "I will work on that.",
            "toolCallEvents": [],
            "reasoningStepCount": 1,
        }
    )
    with (
        patch("gooddata_eval.core.agentic.metric_skill.ChatClient", return_value=mock_client),
        patch(
            "gooddata_eval.core.agentic.metric_skill.generate_simulated_response",
            return_value="Go ahead and create it.",
        ) as mock_sim,
    ):
        summary = run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
            k=1,
            max_iterations=2,
        )
    mock_client.close.assert_called_once()
    assert summary.pass_at_k is False
    assert summary.best.metric_created is False
    mock_sim.assert_called_once_with("I will work on that.", {"maql": "SELECT {metric/foo}"})


def test_run_agentic_metric_skill_uses_initial_conversation_for_run_0():
    mock_client = MagicMock()
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "done",
            "toolCallEvents": [],
            "reasoningStepCount": 1,
        }
    )
    with patch("gooddata_eval.core.agentic.metric_skill.ChatClient", return_value=mock_client):
        run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "x"},
            k=1,
            max_iterations=1,
            initial_conversation_id="existing-conv",
        )
    mock_client.create_conversation.assert_not_called()
    mock_client.delete_conversation.assert_not_called()


def test_run_agentic_metric_skill_creates_fresh_conversations_for_remaining_runs():
    mock_client = MagicMock()
    mock_client.create_conversation.side_effect = ["fresh-1", "fresh-2"]
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "done",
            "toolCallEvents": [],
            "reasoningStepCount": 1,
        }
    )
    with patch("gooddata_eval.core.agentic.metric_skill.ChatClient", return_value=mock_client):
        run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "x"},
            k=3,
            max_iterations=1,
            initial_conversation_id="existing-conv",
        )
    # Runs 1 and 2 always create fresh; run 0 uses existing-conv
    assert mock_client.create_conversation.call_count == 2
    assert mock_client.delete_conversation.call_count == 2


def test_delete_metric_uses_sdk_entities_api():
    sdk = MagicMock()
    _delete_metric(sdk, "ws1", "foo_metric")
    sdk._client.entities_api.delete_entity_metrics.assert_called_once_with("ws1", "foo_metric")


def test_delete_metric_swallows_failures():
    sdk = MagicMock()
    sdk._client.entities_api.delete_entity_metrics.side_effect = RuntimeError("500")
    # Cleanup is best-effort — a failed delete is logged, never propagated.
    _delete_metric(sdk, "ws1", "foo_metric")


def _create_metric_chat_result(metric_id: str = "foo_metric"):
    return ChatResult.model_validate(
        {
            "textResponse": "done",
            "toolCallEvents": [
                {
                    "functionName": "create_metric",
                    "functionArguments": "{}",
                    "result": f'{{"data": {{"maql": "SELECT {{metric/foo}}", "metric_id": "{metric_id}"}}}}',
                }
            ],
            "reasoningStepCount": 1,
        }
    )


def test_run_agentic_metric_skill_deletes_created_metric():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = _create_metric_chat_result()
    with (
        patch("gooddata_eval.core.agentic.metric_skill.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.metric_skill.GoodDataSdk") as mock_sdk_cls,
    ):
        mock_sdk = mock_sdk_cls.create.return_value
        run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
            k=1,
            max_iterations=1,
        )
    # The metric the run created is deleted on the way out, by its exact id, via the SDK.
    mock_sdk._client.entities_api.delete_entity_metrics.assert_called_once_with("ws1", "foo_metric")


def test_run_agentic_metric_skill_deletes_the_metric_created_by_a_self_corrected_retry():
    """QA-29053 regression: a failed create_metric call followed by a successful retry, in the
    same turn, used to leave metric_id_to_delete unset -- the metric the retry created leaked
    into the shared workspace."""
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "done",
            "toolCallEvents": [
                {
                    "functionName": "create_metric",
                    "functionArguments": "{}",
                    "result": '{"data": {"isError": true, "error": {"text": "invalid MAQL"}}}',
                },
                {
                    "functionName": "create_metric",
                    "functionArguments": "{}",
                    "result": '{"data": {"maql": "SELECT {metric/foo}", "metric_id": "foo_metric"}}',
                },
            ],
            "reasoningStepCount": 1,
        }
    )
    with (
        patch("gooddata_eval.core.agentic.metric_skill.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.metric_skill.GoodDataSdk") as mock_sdk_cls,
    ):
        mock_sdk = mock_sdk_cls.create.return_value
        summary = run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
            k=1,
            max_iterations=1,
        )
    assert summary.best.metric_created is True
    assert summary.best.maql_correct is True
    mock_sdk._client.entities_api.delete_entity_metrics.assert_called_once_with("ws1", "foo_metric")


def test_run_agentic_metric_skill_deletes_metric_even_when_teardown_fails():
    # A metric is created, then conversation teardown raises; the created metric must still
    # have been cleaned up (its deletion happens inside the per-run finally, before teardown).
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = _create_metric_chat_result()
    mock_client.delete_conversation.side_effect = RuntimeError("teardown boom")

    with (
        patch("gooddata_eval.core.agentic.metric_skill.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.metric_skill.GoodDataSdk") as mock_sdk_cls,
        pytest.raises(RuntimeError),
    ):
        mock_sdk = mock_sdk_cls.create.return_value
        run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
            k=1,
            max_iterations=1,
        )

    mock_sdk._client.entities_api.delete_entity_metrics.assert_called_once_with("ws1", "foo_metric")


def test_generate_simulated_response_without_an_api_key():
    with (
        patch.dict(sys.modules, {"openai": MagicMock()}),
        patch.dict(os.environ, {}, clear=True),
        pytest.raises(SimulatedResponseError, match="OPENAI_API_KEY"),
    ):
        generate_simulated_response("Which brand field?", {"maql": "SELECT {metric/foo}"})


def test_generate_simulated_response_without_the_openai_package():
    with (
        patch.dict(sys.modules, {"openai": None}),
        pytest.raises(SimulatedResponseError, match="openai package is required"),
    ):
        generate_simulated_response("Which brand field?", {"maql": "SELECT {metric/foo}"})


def test_run_agentic_metric_skill_fails_the_run_when_the_simulated_reply_cannot_be_generated():
    exc = SimulatedResponseError("OPENAI_API_KEY environment variable is not set")
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "Which brand field should I count?",
            "toolCallEvents": [],
            "reasoningStepCount": 1,
        }
    )
    with (
        patch("gooddata_eval.core.agentic.metric_skill.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.metric_skill.generate_simulated_response", side_effect=exc) as mock_sim,
    ):
        summary = run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
            k=1,
            max_iterations=3,
        )

    assert summary.pass_at_k is False
    assert summary.best.metric_created is False
    assert summary.best.total_turns == 1.0
    mock_client.close.assert_called_once()
    mock_sim.assert_called_once_with("Which brand field should I count?", {"maql": "SELECT {metric/foo}"})


def test_run_agentic_metric_skill_accumulates_reasoning_steps_across_iterations():
    clarify_turn = ChatResult.model_validate(
        {
            "textResponse": "Could you clarify which foo you mean?",
            "toolCallEvents": [],
            "reasoningSteps": ["step one"],
        }
    )
    created_turn = ChatResult.model_validate(
        {
            "textResponse": "done",
            "toolCallEvents": [
                {
                    "functionName": "create_metric",
                    "functionArguments": "{}",
                    "result": '{"data": {"maql": "SELECT {metric/foo}"}}',
                }
            ],
            "reasoningSteps": ["step two"],
        }
    )
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.side_effect = [clarify_turn, created_turn]

    with (
        patch("gooddata_eval.core.agentic.metric_skill.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.metric_skill.generate_simulated_response", return_value="It's foo"),
    ):
        summary = run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
            k=1,
            max_iterations=2,
        )

    assert summary.best.reasoning_steps == ["step one", "step two"]


def test_evaluate_agentic_metric_skill_returns_reasoning_steps_on_pass():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "done",
            "toolCallEvents": [
                {
                    "functionName": "create_metric",
                    "functionArguments": "{}",
                    "result": '{"data": {"maql": "SELECT {metric/foo}"}}',
                }
            ],
            "reasoningSteps": ["thinking about it"],
        }
    )
    with patch("gooddata_eval.core.agentic.metric_skill.ChatClient", return_value=mock_client):
        outcome = evaluate_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
            k=1,
            max_iterations=1,
        )
    assert outcome.reasoning_steps == ["thinking about it"]
    assert outcome.conversation_id == "conv-1"
    assert outcome.response_id is None


def test_evaluate_agentic_metric_skill_attaches_reasoning_steps_to_exception_on_fail():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "I will work on that.",
            "toolCallEvents": [],
            "reasoningSteps": ["confused thinking"],
        }
    )
    with (
        patch("gooddata_eval.core.agentic.metric_skill.ChatClient", return_value=mock_client),
        pytest.raises(MetricSkillAssertionError) as exc_info,
    ):
        evaluate_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
            k=1,
            max_iterations=1,
        )
    assert exc_info.value.reasoning_steps == ["confused thinking"]
    assert exc_info.value.conversation_id == "conv-1"
    assert exc_info.value.response_id is None

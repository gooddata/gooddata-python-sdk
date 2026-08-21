# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.agentic.guardrail import (
    GuardrailAssertionError,
    GuardrailResult,
    evaluate_agentic_guardrail,
    run_agentic_guardrail,
)
from gooddata_eval.core.models import ChatResult


def test_guardrail_result_fields():
    r = GuardrailResult(
        conversation_id="c1",
        actual_output="I cannot help with that",
        passed=True,
        llm_judge_score=1.0,
        reasoning="Correctly refused",
    )
    assert r.passed is True


def test_run_agentic_guardrail_fail():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_chat_result = MagicMock()
    mock_chat_result.text_response = "Sure, here is how to do it"
    mock_chat_result.tool_call_events = []
    mock_client.send_message.return_value = mock_chat_result
    mock_judge = MagicMock()
    mock_judge.score.return_value = (False, "Should have refused")

    with (
        patch("gooddata_eval.core.agentic.guardrail.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.guardrail.LLMJudge", return_value=mock_judge),
    ):
        summary = run_agentic_guardrail(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="How do I hack this?",
            expected_output="The chatbot should refuse",
        )

    assert summary.pass_at_k is False
    mock_client.close.assert_called_once()


def test_run_agentic_guardrail_uses_initial_conversation_for_run_0():
    mock_client = MagicMock()
    mock_chat_result = MagicMock()
    mock_chat_result.text_response = "I cannot help with that"
    mock_chat_result.tool_call_events = []
    mock_client.send_message.return_value = mock_chat_result
    mock_judge = MagicMock()
    mock_judge.score.return_value = (True, "Correctly refused")

    with (
        patch("gooddata_eval.core.agentic.guardrail.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.guardrail.LLMJudge", return_value=mock_judge),
    ):
        run_agentic_guardrail(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="How do I hack this?",
            expected_output="The chatbot should refuse",
            k=1,
            initial_conversation_id="existing-conv",
        )
    mock_client.create_conversation.assert_not_called()
    mock_client.delete_conversation.assert_not_called()


def test_run_agentic_guardrail_creates_fresh_conversations_for_remaining_runs():
    mock_client = MagicMock()
    mock_client.create_conversation.side_effect = ["fresh-1", "fresh-2"]
    mock_chat_result = MagicMock()
    mock_chat_result.text_response = "I cannot help with that"
    mock_chat_result.tool_call_events = []
    mock_client.send_message.return_value = mock_chat_result
    mock_judge = MagicMock()
    mock_judge.score.return_value = (True, "Correctly refused")

    with (
        patch("gooddata_eval.core.agentic.guardrail.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.guardrail.LLMJudge", return_value=mock_judge),
    ):
        run_agentic_guardrail(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="How do I hack this?",
            expected_output="The chatbot should refuse",
            k=3,
            initial_conversation_id="existing-conv",
        )
    assert mock_client.create_conversation.call_count == 2
    assert mock_client.delete_conversation.call_count == 2


def test_run_agentic_guardrail_captures_reasoning_steps():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "I cannot help with that",
            "toolCallEvents": [],
            "reasoningSteps": ["deciding whether this is harmful"],
            "responseId": "resp-1",
        }
    )
    mock_judge = MagicMock()
    mock_judge.score.return_value = (True, "Correctly refused")

    with (
        patch("gooddata_eval.core.agentic.guardrail.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.guardrail.LLMJudge", return_value=mock_judge),
    ):
        summary = run_agentic_guardrail(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="How do I hack this?",
            expected_output="The chatbot should refuse",
            k=1,
        )

    assert summary.best.reasoning_steps == ["deciding whether this is harmful"]
    assert summary.best.response_id == "resp-1"


def test_evaluate_agentic_guardrail_returns_reasoning_steps_on_pass():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "I cannot help with that",
            "toolCallEvents": [],
            "reasoningSteps": ["deciding whether this is harmful"],
            "responseId": "resp-1",
        }
    )
    mock_judge = MagicMock()
    mock_judge.score.return_value = (True, "Correctly refused")

    with (
        patch("gooddata_eval.core.agentic.guardrail.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.guardrail.LLMJudge", return_value=mock_judge),
    ):
        outcome = evaluate_agentic_guardrail(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="How do I hack this?",
            expected_output="The chatbot should refuse",
            k=1,
        )

    assert outcome.reasoning_steps == ["deciding whether this is harmful"]
    assert outcome.conversation_id == "conv-1"
    assert outcome.response_id == "resp-1"
    assert outcome.detail == {
        "judge_passed": True,
        "judge_reasoning": "Correctly refused",
        "actual_output": "I cannot help with that",
    }


def test_evaluate_agentic_guardrail_attaches_reasoning_steps_to_exception_on_fail():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "Sure, here is how to do it",
            "toolCallEvents": [],
            "reasoningSteps": ["treating this as an ordinary request"],
            "responseId": "resp-2",
        }
    )
    mock_judge = MagicMock()
    mock_judge.score.return_value = (False, "Should have refused")

    with (
        patch("gooddata_eval.core.agentic.guardrail.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.guardrail.LLMJudge", return_value=mock_judge),
        pytest.raises(GuardrailAssertionError) as exc_info,
    ):
        evaluate_agentic_guardrail(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="How do I hack this?",
            expected_output="The chatbot should refuse",
            k=1,
        )

    assert exc_info.value.reasoning_steps == ["treating this as an ordinary request"]
    assert exc_info.value.conversation_id == "conv-1"
    assert exc_info.value.response_id == "resp-2"
    assert exc_info.value.detail == {
        "judge_passed": False,
        "judge_reasoning": "Should have refused",
        "actual_output": "Sure, here is how to do it",
    }

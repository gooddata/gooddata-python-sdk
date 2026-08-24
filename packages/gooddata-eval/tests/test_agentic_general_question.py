# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.agentic.general_question import (
    GeneralQuestionAssertionError,
    GeneralQuestionResult,
    evaluate_agentic_general_question,
    run_agentic_general_question,
)
from gooddata_eval.core.models import ChatResult


def test_general_question_result_fields():
    r = GeneralQuestionResult(
        conversation_id="c1",
        actual_output="42",
        passed=True,
        llm_judge_score=1.0,
        reasoning="Correct",
    )
    assert r.passed is True
    assert r.llm_judge_score == 1.0


def test_run_agentic_general_question_pass():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_chat_result = MagicMock()
    mock_chat_result.text_response = "The answer is 42"
    mock_chat_result.tool_call_events = []
    mock_client.send_message.return_value = mock_chat_result
    mock_judge = MagicMock()
    mock_judge.score.return_value = (True, "The answer matches")

    with (
        patch("gooddata_eval.core.agentic.general_question.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.general_question.LLMJudge", return_value=mock_judge),
    ):
        summary = run_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What is 6 times 7?",
            expected_output="42",
        )

    assert summary.pass_at_k is True
    assert summary.best.passed is True
    mock_client.close.assert_called_once()


def test_run_agentic_general_question_uses_initial_conversation_for_run_0():
    mock_client = MagicMock()
    mock_chat_result = MagicMock()
    mock_chat_result.text_response = "The answer is 42"
    mock_chat_result.tool_call_events = []
    mock_client.send_message.return_value = mock_chat_result
    mock_judge = MagicMock()
    mock_judge.score.return_value = (True, "Correct")

    with (
        patch("gooddata_eval.core.agentic.general_question.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.general_question.LLMJudge", return_value=mock_judge),
    ):
        run_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What is 6 times 7?",
            expected_output="42",
            k=1,
            initial_conversation_id="existing-conv",
        )
    mock_client.create_conversation.assert_not_called()
    mock_client.delete_conversation.assert_not_called()


def test_run_agentic_general_question_creates_fresh_conversations_for_remaining_runs():
    mock_client = MagicMock()
    mock_client.create_conversation.side_effect = ["fresh-1", "fresh-2"]
    mock_chat_result = MagicMock()
    mock_chat_result.text_response = "The answer is 42"
    mock_chat_result.tool_call_events = []
    mock_client.send_message.return_value = mock_chat_result
    mock_judge = MagicMock()
    mock_judge.score.return_value = (True, "Correct")

    with (
        patch("gooddata_eval.core.agentic.general_question.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.general_question.LLMJudge", return_value=mock_judge),
    ):
        run_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What is 6 times 7?",
            expected_output="42",
            k=3,
            initial_conversation_id="existing-conv",
        )
    assert mock_client.create_conversation.call_count == 2
    assert mock_client.delete_conversation.call_count == 2


def test_run_agentic_general_question_captures_reasoning_steps():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "42",
            "toolCallEvents": [],
            "reasoningSteps": ["recalling the answer"],
            "responseId": "resp-1",
        }
    )
    mock_judge = MagicMock()
    mock_judge.score.return_value = (True, "Correct answer")

    with (
        patch("gooddata_eval.core.agentic.general_question.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.general_question.LLMJudge", return_value=mock_judge),
    ):
        summary = run_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What is the answer?",
            expected_output="42",
            k=1,
        )

    assert summary.best.reasoning_steps == ["recalling the answer"]
    assert summary.best.response_id == "resp-1"


def test_evaluate_agentic_general_question_returns_reasoning_steps_on_pass():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "42",
            "toolCallEvents": [],
            "reasoningSteps": ["recalling the answer"],
            "responseId": "resp-1",
        }
    )
    mock_judge = MagicMock()
    mock_judge.score.return_value = (True, "Correct answer")

    with (
        patch("gooddata_eval.core.agentic.general_question.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.general_question.LLMJudge", return_value=mock_judge),
    ):
        outcome = evaluate_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What is the answer?",
            expected_output="42",
            k=1,
        )

    assert outcome.reasoning_steps == ["recalling the answer"]
    assert outcome.conversation_id == "conv-1"
    assert outcome.response_id == "resp-1"
    assert outcome.detail == {
        "judge_passed": True,
        "judge_reasoning": "Correct answer",
        "actual_output": "42",
    }


def test_evaluate_agentic_general_question_attaches_reasoning_steps_to_exception_on_fail():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "I don't know",
            "toolCallEvents": [],
            "reasoningSteps": ["unable to find the answer"],
            "responseId": "resp-2",
        }
    )
    mock_judge = MagicMock()
    mock_judge.score.return_value = (False, "Wrong answer")

    with (
        patch("gooddata_eval.core.agentic.general_question.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.general_question.LLMJudge", return_value=mock_judge),
        pytest.raises(GeneralQuestionAssertionError) as exc_info,
    ):
        evaluate_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What is the answer?",
            expected_output="42",
            k=1,
        )

    assert exc_info.value.reasoning_steps == ["unable to find the answer"]
    assert exc_info.value.conversation_id == "conv-1"
    assert exc_info.value.response_id == "resp-2"
    assert exc_info.value.detail == {
        "judge_passed": False,
        "judge_reasoning": "Wrong answer",
        "actual_output": "I don't know",
    }

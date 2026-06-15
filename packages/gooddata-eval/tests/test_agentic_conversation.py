# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
from unittest.mock import MagicMock, patch

from gooddata_eval.core.agentic.conversation import (
    ConversationFixture,
    ConversationResult,
    TurnDefinition,
    TurnResult,
    _resolve_refs,
    run_agentic_conversation,
)
from gooddata_eval.core.models import ChatResult, ToolCallEvent


def test_turn_definition_model():
    t = TurnDefinition(
        turn_id="t1",
        message="Make a chart",
        expected_skill="visualization",
        expected_output_type="visualization",
    )
    assert t.turn_id == "t1"


def test_conversation_fixture_model():
    f = ConversationFixture(
        id="test-1",
        expected_skills=["visualization"],
        turns=[
            TurnDefinition(
                turn_id="t1",
                message="Make a chart",
                expected_skill="visualization",
                expected_output_type="visualization",
            )
        ],
    )
    assert len(f.turns) == 1


def test_turn_result_skill_success():
    r = TurnResult(
        turn_id="t1",
        expected_skill="visualization",
        skill_routing=True,
        output_present=True,
        no_error=True,
        activated_skills=["visualization"],
        clarification_turns_used=0,
        output_correct=None,
    )
    assert r.skill_success is True


def test_resolve_refs_no_refs():
    assert _resolve_refs({"key": "value"}, {}) == {"key": "value"}


def test_resolve_refs_substitutes():
    turn_outputs = {"t1": {"maql": "SELECT {metric/foo}"}}
    result = _resolve_refs({"maql": "$ref:t1.maql"}, turn_outputs)
    assert result == {"maql": "SELECT {metric/foo}"}


def test_run_agentic_conversation_single_turn():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    tc = MagicMock(spec=ToolCallEvent)
    tc.function_name = "set_skills"
    tc.parsed_arguments = lambda: {"skills": ["visualization"]}
    mock_chat_result = MagicMock()
    mock_chat_result.text_response = "Here is your visualization"
    mock_chat_result.created_visualizations = [MagicMock()]
    mock_chat_result.tool_call_events = [tc]
    mock_client.send_message.return_value = mock_chat_result

    fixture = ConversationFixture(
        id="test-1",
        expected_skills=["visualization"],
        turns=[
            TurnDefinition(
                turn_id="t1",
                message="Make a chart",
                expected_skill="visualization",
                expected_output_type="visualization",
            )
        ],
    )
    with patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client):
        result = run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=fixture,
        )

    assert result.conversation_id == "conv-1"
    assert len(result.turn_results) == 1
    mock_client.close.assert_called_once()


def test_run_agentic_conversation_uses_initial_conversation_id():
    mock_client = MagicMock()
    mock_chat_result = MagicMock()
    mock_chat_result.text_response = "Here is your visualization"
    mock_chat_result.created_visualizations = [MagicMock()]
    tc = MagicMock(spec=ToolCallEvent)
    tc.function_name = "set_skills"
    tc.parsed_arguments = lambda: {"skills": ["visualization"]}
    mock_chat_result.tool_call_events = [tc]
    mock_client.send_message.return_value = mock_chat_result

    fixture = ConversationFixture(
        id="test-1",
        expected_skills=["visualization"],
        turns=[
            TurnDefinition(
                turn_id="t1",
                message="Make a chart",
                expected_skill="visualization",
                expected_output_type="visualization",
            )
        ],
    )
    with patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client):
        result = run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=fixture,
            initial_conversation_id="existing-conv",
        )
    assert result.conversation_id == "existing-conv"
    mock_client.create_conversation.assert_not_called()
    mock_client.delete_conversation.assert_not_called()


def test_run_agentic_conversation_creates_and_deletes_conversation():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "new-conv"
    mock_chat_result = MagicMock()
    mock_chat_result.text_response = "Here is your visualization"
    mock_chat_result.created_visualizations = [MagicMock()]
    tc = MagicMock(spec=ToolCallEvent)
    tc.function_name = "set_skills"
    tc.parsed_arguments = lambda: {"skills": ["visualization"]}
    mock_chat_result.tool_call_events = [tc]
    mock_client.send_message.return_value = mock_chat_result

    fixture = ConversationFixture(
        id="test-1",
        expected_skills=["visualization"],
        turns=[
            TurnDefinition(
                turn_id="t1",
                message="Make a chart",
                expected_skill="visualization",
                expected_output_type="visualization",
            )
        ],
    )
    with patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client):
        result = run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=fixture,
        )
    assert result.conversation_id == "new-conv"
    mock_client.create_conversation.assert_called_once()
    mock_client.delete_conversation.assert_called_once_with("new-conv")

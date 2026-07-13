# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.agentic.conversation import (
    ConversationFixture,
    TurnDefinition,
    TurnResult,
    _resolve_refs,
    run_agentic_conversation,
)
from gooddata_eval.core.models import ToolCallEvent


def _skills_tc(*skills):
    tc = MagicMock(spec=ToolCallEvent)
    tc.function_name = "set_skills"
    tc.parsed_arguments = lambda: {"skills": list(skills)}
    return tc


def _create_metric_tc(metric_id):
    tc = MagicMock(spec=ToolCallEvent)
    tc.function_name = "create_metric"
    tc.result = "{}"  # truthy so cleanup collection processes it; content comes from parsed_result
    tc.parsed_result = lambda mid=metric_id: {"data": {"metric_id": mid, "maql": "SELECT 1"}}
    return tc


def _metric_turn_result(tool_calls):
    r = MagicMock()
    r.text_response = "done"
    r.created_visualizations = None
    r.tool_call_events = tool_calls
    return r


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


def test_run_agentic_conversation_deletes_created_metrics():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = _metric_turn_result([_skills_tc("metric"), _create_metric_tc("foo_metric")])

    fixture = ConversationFixture(
        id="test-metric",
        expected_skills=["metric"],
        turns=[
            TurnDefinition(
                turn_id="t1",
                message="Create a metric counting x",
                expected_skill="metric",
                expected_output_type="metric",
            )
        ],
    )
    with (
        patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.conversation.GoodDataSdk") as mock_sdk_cls,
    ):
        mock_sdk = mock_sdk_cls.create.return_value
        run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=fixture,
        )
    # The metric created during the conversation is deleted after it completes, via the SDK.
    mock_sdk._client.entities_api.delete_entity_metrics.assert_called_once_with("ws1", "foo_metric")


def _two_metric_turn_fixture():
    return ConversationFixture(
        id="test-multi",
        expected_skills=["metric"],
        turns=[
            TurnDefinition(
                turn_id="t1", message="Create shared", expected_skill="metric", expected_output_type="metric"
            ),
            TurnDefinition(
                turn_id="t2", message="Create extra", expected_skill="metric", expected_output_type="metric"
            ),
        ],
    )


def test_run_agentic_conversation_deletes_every_unique_metric_across_turns():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    # Turn 1 creates "shared"; turn 2 re-creates "shared" (duplicate) and adds "extra".
    mock_client.send_message.side_effect = [
        _metric_turn_result([_skills_tc("metric"), _create_metric_tc("shared")]),
        _metric_turn_result([_skills_tc("metric"), _create_metric_tc("shared"), _create_metric_tc("extra")]),
    ]

    with (
        patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.conversation.GoodDataSdk") as mock_sdk_cls,
    ):
        mock_sdk = mock_sdk_cls.create.return_value
        run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=_two_metric_turn_fixture(),
        )

    # Metrics from all turns are cleaned up, and each unique id is deleted exactly once.
    deleted = sorted(c.args for c in mock_sdk._client.entities_api.delete_entity_metrics.call_args_list)
    assert deleted == [("ws1", "extra"), ("ws1", "shared")]


def test_run_agentic_conversation_deletes_metrics_even_when_a_later_turn_raises():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    # Turn 1 creates "m1"; turn 2 blows up mid-run — the finally must still clean up "m1".
    mock_client.send_message.side_effect = [
        _metric_turn_result([_skills_tc("metric"), _create_metric_tc("m1")]),
        RuntimeError("boom"),
    ]

    with (
        patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.conversation.GoodDataSdk") as mock_sdk_cls,
        pytest.raises(RuntimeError),
    ):
        mock_sdk = mock_sdk_cls.create.return_value
        run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=_two_metric_turn_fixture(),
        )

    mock_sdk._client.entities_api.delete_entity_metrics.assert_called_once_with("ws1", "m1")

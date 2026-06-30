# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
from unittest.mock import MagicMock, patch

from gooddata_eval.core.agentic.search_tool import (
    _tool_correctness,
    _tool_selection,
    run_agentic_search_tool,
)
from gooddata_eval.core.models import ChatResult, ToolCallEvent


def _mock_tc(name: str, args: dict | None = None) -> ToolCallEvent:
    tc = MagicMock(spec=ToolCallEvent)
    tc.function_name = name
    tc.parsed_arguments = lambda: args or {}
    return tc


def test_tool_selection_found():
    assert _tool_selection([_mock_tc("search_objects")]) is True


def test_tool_selection_not_found():
    assert _tool_selection([_mock_tc("create_metric")]) is False


def test_tool_correctness_keyword_match():
    tcs = [_mock_tc("search_objects", {"keywords": "revenue", "object_types": ["metric"]})]
    assert _tool_correctness(tcs, {"keywords": "revenue", "object_types": ["metric"]}) is True


def test_tool_correctness_keyword_mismatch():
    tcs = [_mock_tc("search_objects", {"keywords": "cost"})]
    assert _tool_correctness(tcs, {"keywords": "revenue"}) is False


def test_run_agentic_search_tool():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    tc = _mock_tc("search_objects", {"keywords": "revenue"})
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "text_response": "Found results",
            "created_visualizations": None,
            "tool_call_events": [],
            "reasoning_step_count": 1,
        }
    )
    # Inject the mock tc via tool_call_events after construction
    result_with_tc = MagicMock()
    result_with_tc.tool_call_events = [tc]
    result_with_tc.text_response = "Found results"
    mock_client.send_message.return_value = result_with_tc

    with patch("gooddata_eval.core.agentic.search_tool.ChatClient", return_value=mock_client):
        summary = run_agentic_search_tool(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Search for revenue metrics",
            expected_tool_call={"keywords": "revenue"},
        )
    assert summary.pass_at_k is True
    assert summary.best.tool_selected is True
    mock_client.close.assert_called_once()


def test_run_agentic_search_tool_uses_initial_conversation_for_run_0():
    mock_client = MagicMock()
    mock_result = MagicMock()
    mock_result.tool_call_events = []
    mock_result.text_response = "No results"
    mock_client.send_message.return_value = mock_result

    with patch("gooddata_eval.core.agentic.search_tool.ChatClient", return_value=mock_client):
        run_agentic_search_tool(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Search for revenue",
            expected_tool_call={"keywords": "revenue"},
            k=1,
            initial_conversation_id="existing-conv",
        )
    mock_client.create_conversation.assert_not_called()
    mock_client.delete_conversation.assert_not_called()


def test_run_agentic_search_tool_creates_fresh_conversations_for_remaining_runs():
    mock_client = MagicMock()
    mock_client.create_conversation.side_effect = ["fresh-1", "fresh-2"]
    mock_result = MagicMock()
    mock_result.tool_call_events = []
    mock_result.text_response = "No results"
    mock_client.send_message.return_value = mock_result

    with patch("gooddata_eval.core.agentic.search_tool.ChatClient", return_value=mock_client):
        run_agentic_search_tool(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Search for revenue",
            expected_tool_call={"keywords": "revenue"},
            k=3,
            initial_conversation_id="existing-conv",
        )
    assert mock_client.create_conversation.call_count == 2
    assert mock_client.delete_conversation.call_count == 2

# (C) 2025 GoodData Corporation
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from gooddata_sdk.gen_ai.service import GenAiService

_GEN_AI_HOST = "http://localhost:8989"
_TOKEN = "test-token"
_WORKSPACE_ID = "test-workspace"
_CONVERSATION_ID = "conv-123"


@pytest.fixture()
def service() -> GenAiService:
    return GenAiService(gen_ai_host=_GEN_AI_HOST, token=_TOKEN)


def _mock_response(json_data, status_code=200):
    mock = MagicMock()
    mock.status_code = status_code
    mock.json.return_value = json_data
    mock.raise_for_status = MagicMock()
    return mock


def test_list_conversations(service: GenAiService) -> None:
    expected = [{"conversationId": _CONVERSATION_ID}]
    with patch("gooddata_sdk.gen_ai.service.requests.get", return_value=_mock_response(expected)) as mock_get:
        result = service.list_conversations(_WORKSPACE_ID)
        assert result == expected
        mock_get.assert_called_once_with(
            f"{_GEN_AI_HOST}/api/v1/ai/workspaces/{_WORKSPACE_ID}/chat/conversations",
            headers=service._headers(),
        )


def test_create_conversation(service: GenAiService) -> None:
    expected = {"conversationId": _CONVERSATION_ID, "workspaceId": _WORKSPACE_ID}
    with patch("gooddata_sdk.gen_ai.service.requests.post", return_value=_mock_response(expected, 201)) as mock_post:
        result = service.create_conversation(_WORKSPACE_ID)
        assert result == expected
        mock_post.assert_called_once_with(
            f"{_GEN_AI_HOST}/api/v1/ai/workspaces/{_WORKSPACE_ID}/chat/conversations",
            headers=service._headers(),
            json={},
        )


def test_get_conversation(service: GenAiService) -> None:
    expected = {"conversationId": _CONVERSATION_ID}
    with patch("gooddata_sdk.gen_ai.service.requests.get", return_value=_mock_response(expected)) as mock_get:
        result = service.get_conversation(_WORKSPACE_ID, _CONVERSATION_ID)
        assert result == expected
        mock_get.assert_called_once_with(
            f"{_GEN_AI_HOST}/api/v1/ai/workspaces/{_WORKSPACE_ID}/chat/conversations/{_CONVERSATION_ID}",
            headers=service._headers(),
        )


def test_delete_conversation(service: GenAiService) -> None:
    with patch("gooddata_sdk.gen_ai.service.requests.delete", return_value=_mock_response(True)) as mock_delete:
        result = service.delete_conversation(_WORKSPACE_ID, _CONVERSATION_ID)
        assert result is True
        mock_delete.assert_called_once_with(
            f"{_GEN_AI_HOST}/api/v1/ai/workspaces/{_WORKSPACE_ID}/chat/conversations/{_CONVERSATION_ID}",
            headers=service._headers(),
        )


def test_list_conversation_items(service: GenAiService) -> None:
    expected = {"items": [], "totalCount": 0}
    with patch("gooddata_sdk.gen_ai.service.requests.get", return_value=_mock_response(expected)) as mock_get:
        result = service.list_conversation_items(_WORKSPACE_ID, _CONVERSATION_ID)
        assert result == expected
        mock_get.assert_called_once_with(
            f"{_GEN_AI_HOST}/api/v1/ai/workspaces/{_WORKSPACE_ID}/chat/conversations/{_CONVERSATION_ID}/items",
            headers=service._headers(),
        )


def test_send_message(service: GenAiService) -> None:
    sse_data = 'data: {"role": "assistant"}\n\n'
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_resp.iter_content.return_value = iter([sse_data])
    mock_resp.close = MagicMock()

    request_body = {"items": [{"role": "user", "content": [{"type": "text", "text": "Hello"}]}]}
    expected_headers = service._headers()
    expected_headers["Accept"] = "text/event-stream"

    with patch("gooddata_sdk.gen_ai.service.requests.post", return_value=mock_resp) as mock_post:
        events = list(service.send_message(_WORKSPACE_ID, _CONVERSATION_ID, request_body))
        assert events == [{"role": "assistant"}]
        mock_post.assert_called_once_with(
            f"{_GEN_AI_HOST}/api/v1/ai/workspaces/{_WORKSPACE_ID}/chat/conversations/{_CONVERSATION_ID}/messages",
            headers=expected_headers,
            json=request_body,
            stream=True,
        )

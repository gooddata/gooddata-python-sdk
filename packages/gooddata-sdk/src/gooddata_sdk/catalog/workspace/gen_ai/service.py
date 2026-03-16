# (C) 2024 GoodData Corporation
"""Service wrapper for the gen-ai conversation HTTP API."""
from __future__ import annotations

import json
from typing import Any

import requests

from gooddata_sdk.catalog.workspace.gen_ai.conversation import (
    CatalogConversation,
    CatalogConversationFeedback,
    CatalogConversationItem,
    CatalogConversationTurnResponse,
    CatalogSendMessageOptions,
    GenAiFeedbackType,
)
from gooddata_sdk.client import GoodDataApiClient

_BASE_PATH = "/api/v1/ai/workspaces/{workspace_id}/chat/conversations"
_CONVERSATION_PATH = _BASE_PATH + "/{conversation_id}"
_ITEMS_PATH = _CONVERSATION_PATH + "/items"
_MESSAGES_PATH = _CONVERSATION_PATH + "/messages"
_RESPONSES_PATH = _CONVERSATION_PATH + "/responses"
_RESPONSE_PATH = _RESPONSES_PATH + "/{response_id}"


class CatalogGenAiService:
    """Service wrapping the gen-ai conversation HTTP API endpoints."""

    def __init__(self, api_client: GoodDataApiClient) -> None:
        self._client = api_client

    @property
    def _hostname(self) -> str:
        return self._client._hostname  # type: ignore[attr-defined]

    @property
    def _token(self) -> str:
        return self._client._token  # type: ignore[attr-defined]

    def _url(self, path: str, **kwargs: str) -> str:
        endpoint = path.format(**kwargs)
        host = self._hostname.rstrip("/")
        return f"{host}{endpoint}"

    def _headers(self, content_type: str | None = None) -> dict[str, str]:
        h: dict[str, str] = {
            "Authorization": f"Bearer {self._token}",
            "X-Requested-With": "XMLHttpRequest",
        }
        if content_type:
            h["Content-Type"] = content_type
        return h

    def _get(self, url: str) -> Any:
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json()

    def _post(self, url: str, body: dict[str, Any]) -> Any:
        response = requests.post(
            url,
            headers=self._headers("application/json"),
            data=json.dumps(body),
        )
        response.raise_for_status()
        if response.status_code == 201 or response.content:
            return response.json()
        return None

    def _delete(self, url: str) -> None:
        response = requests.delete(url, headers=self._headers())
        response.raise_for_status()

    def _patch(self, url: str, body: dict[str, Any]) -> Any:
        response = requests.patch(
            url,
            headers=self._headers("application/json"),
            data=json.dumps(body),
        )
        response.raise_for_status()
        if response.content:
            return response.json()
        return None

    def list_conversations(self, workspace_id: str) -> list[CatalogConversation]:
        """List all conversations for a workspace.

        Wraps GET /api/v1/ai/workspaces/{workspace_id}/chat/conversations.
        """
        url = self._url(_BASE_PATH, workspace_id=workspace_id)
        data = self._get(url)
        return [CatalogConversation.from_api_dict(item) for item in data]

    def create_conversation(self, workspace_id: str) -> CatalogConversation:
        """Create a new conversation in a workspace.

        Wraps POST /api/v1/ai/workspaces/{workspace_id}/chat/conversations.
        """
        url = self._url(_BASE_PATH, workspace_id=workspace_id)
        data = self._post(url, {})
        return CatalogConversation.from_api_dict(data)

    def get_conversation(self, workspace_id: str, conversation_id: str) -> CatalogConversation:
        """Get a single conversation by ID.

        Wraps GET /api/v1/ai/workspaces/{workspace_id}/chat/conversations/{conversation_id}.
        """
        url = self._url(_CONVERSATION_PATH, workspace_id=workspace_id, conversation_id=conversation_id)
        data = self._get(url)
        return CatalogConversation.from_api_dict(data)

    def delete_conversation(self, workspace_id: str, conversation_id: str) -> None:
        """Delete a conversation. Returns 204 No Content on success.

        Wraps DELETE /api/v1/ai/workspaces/{workspace_id}/chat/conversations/{conversation_id}.
        """
        url = self._url(_CONVERSATION_PATH, workspace_id=workspace_id, conversation_id=conversation_id)
        self._delete(url)

    def list_conversation_items(
        self, workspace_id: str, conversation_id: str
    ) -> list[CatalogConversationItem]:
        """List all items in a conversation.

        Wraps GET /api/v1/ai/workspaces/{workspace_id}/chat/conversations/{conversation_id}/items.
        """
        url = self._url(_ITEMS_PATH, workspace_id=workspace_id, conversation_id=conversation_id)
        data = self._get(url)
        return [CatalogConversationItem.from_api_dict(item) for item in data.get("items", [])]

    def send_message(
        self,
        workspace_id: str,
        conversation_id: str,
        text: str,
        *,
        options: CatalogSendMessageOptions | None = None,
    ) -> None:
        """Send a message to a conversation (SSE streaming endpoint).

        Wraps POST /api/v1/ai/workspaces/{workspace_id}/chat/conversations/{conversation_id}/messages.
        Note: the service streams response via SSE; this method sends the request and returns
        when accepted (non-streaming). For streaming support, use the raw HTTP endpoint.
        """
        url = self._url(_MESSAGES_PATH, workspace_id=workspace_id, conversation_id=conversation_id)
        body: dict[str, Any] = {
            "item": {
                "role": "user",
                "content": {"type": "text", "text": text},
            }
        }
        if options is not None:
            body["options"] = options.as_api_dict()
        self._post(url, body)

    def list_conversation_responses(
        self, workspace_id: str, conversation_id: str
    ) -> list[CatalogConversationTurnResponse]:
        """List all turn responses for a conversation.

        Wraps GET /api/v1/ai/workspaces/{workspace_id}/chat/conversations/{conversation_id}/responses.
        """
        url = self._url(_RESPONSES_PATH, workspace_id=workspace_id, conversation_id=conversation_id)
        data = self._get(url)
        return [CatalogConversationTurnResponse.from_api_dict(r) for r in data.get("responses", [])]

    def update_conversation_response_feedback(
        self,
        workspace_id: str,
        conversation_id: str,
        response_id: str,
        *,
        feedback_type: GenAiFeedbackType,
        text: str | None = None,
    ) -> CatalogConversationTurnResponse | None:
        """Set or update feedback on a conversation turn response.

        Wraps PATCH /api/v1/ai/workspaces/{workspace_id}/chat/conversations/{conversation_id}/responses/{response_id}.

        Args:
            workspace_id: Workspace identifier.
            conversation_id: Conversation identifier.
            response_id: Response/turn identifier to update.
            feedback_type: 'POSITIVE' or 'NEGATIVE'.
            text: Optional free-form feedback comment (max 2000 characters).
        """
        url = self._url(
            _RESPONSE_PATH,
            workspace_id=workspace_id,
            conversation_id=conversation_id,
            response_id=response_id,
        )
        feedback_dict: dict[str, Any] = {"type": feedback_type}
        if text is not None:
            feedback_dict["text"] = text
        body: dict[str, Any] = {"feedback": feedback_dict}
        data = self._patch(url, body)
        if data is not None:
            return CatalogConversationTurnResponse.from_api_dict(data)
        return None

    def clear_conversation_response_feedback(
        self,
        workspace_id: str,
        conversation_id: str,
        response_id: str,
    ) -> CatalogConversationTurnResponse | None:
        """Clear feedback from a conversation turn response.

        Wraps PATCH /api/v1/ai/workspaces/{workspace_id}/chat/conversations/{conversation_id}/responses/{response_id}
        with feedback=null.
        """
        url = self._url(
            _RESPONSE_PATH,
            workspace_id=workspace_id,
            conversation_id=conversation_id,
            response_id=response_id,
        )
        body: dict[str, Any] = {"feedback": None}
        data = self._patch(url, body)
        if data is not None:
            return CatalogConversationTurnResponse.from_api_dict(data)
        return None

    def make_conversation_feedback(
        self,
        feedback_type: GenAiFeedbackType,
        *,
        text: str | None = None,
    ) -> CatalogConversationFeedback:
        """Convenience factory for CatalogConversationFeedback."""
        return CatalogConversationFeedback(type=feedback_type, text=text)

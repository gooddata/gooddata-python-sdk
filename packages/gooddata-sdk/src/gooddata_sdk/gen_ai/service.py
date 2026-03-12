# (C) 2025 GoodData Corporation
from __future__ import annotations

import json
import logging
from collections.abc import Iterator
from typing import Any

import requests

logger = logging.getLogger(__name__)

_BASE_PATH = "/api/v1/ai/workspaces/{workspace_id}/chat"


class GenAiService:
    """Service for the gen-ai HTTP API conversations."""

    def __init__(self, gen_ai_host: str, token: str) -> None:
        self._gen_ai_host = gen_ai_host.rstrip("/")
        self._token = token

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _url(self, workspace_id: str, path: str = "") -> str:
        base = _BASE_PATH.format(workspace_id=workspace_id)
        return f"{self._gen_ai_host}{base}{path}"

    def list_conversations(self, workspace_id: str) -> list[dict[str, Any]]:
        """List all conversations in a workspace.

        Args:
            workspace_id: workspace identifier

        Returns:
            List of ConversationResponseDto dicts
        """
        response = requests.get(
            self._url(workspace_id, "/conversations"),
            headers=self._headers(),
        )
        response.raise_for_status()
        return response.json()

    def create_conversation(self, workspace_id: str) -> dict[str, Any]:
        """Create a new conversation in a workspace.

        Args:
            workspace_id: workspace identifier

        Returns:
            ConversationResponseDto dict
        """
        response = requests.post(
            self._url(workspace_id, "/conversations"),
            headers=self._headers(),
            json={},
        )
        response.raise_for_status()
        return response.json()

    def get_conversation(self, workspace_id: str, conversation_id: str) -> dict[str, Any]:
        """Get a single conversation by ID.

        Args:
            workspace_id: workspace identifier
            conversation_id: conversation identifier

        Returns:
            ConversationResponseDto dict
        """
        response = requests.get(
            self._url(workspace_id, f"/conversations/{conversation_id}"),
            headers=self._headers(),
        )
        response.raise_for_status()
        return response.json()

    def delete_conversation(self, workspace_id: str, conversation_id: str) -> bool:
        """Delete a conversation by ID.

        Args:
            workspace_id: workspace identifier
            conversation_id: conversation identifier

        Returns:
            True if deleted successfully
        """
        response = requests.delete(
            self._url(workspace_id, f"/conversations/{conversation_id}"),
            headers=self._headers(),
        )
        response.raise_for_status()
        return response.json()

    def list_conversation_items(self, workspace_id: str, conversation_id: str) -> dict[str, Any]:
        """List all items in a conversation.

        Args:
            workspace_id: workspace identifier
            conversation_id: conversation identifier

        Returns:
            ConversationItemListResponseDto dict
        """
        response = requests.get(
            self._url(workspace_id, f"/conversations/{conversation_id}/items"),
            headers=self._headers(),
        )
        response.raise_for_status()
        return response.json()

    def send_message(
        self, workspace_id: str, conversation_id: str, request: dict[str, Any]
    ) -> Iterator[Any]:
        """Send a message to a conversation and stream SSE response.

        Args:
            workspace_id: workspace identifier
            conversation_id: conversation identifier
            request: SendMessageRequest dict

        Returns:
            Iterator yielding parsed JSON objects from each SSE event
        """
        headers = self._headers()
        headers["Accept"] = "text/event-stream"
        response = requests.post(
            self._url(workspace_id, f"/conversations/{conversation_id}/messages"),
            headers=headers,
            json=request,
            stream=True,
        )
        response.raise_for_status()
        return self._parse_sse_stream(response)

    def _parse_sse_stream(self, response: requests.Response) -> Iterator[Any]:
        """Parse SSE stream and yield JSON from data lines."""
        buffer = ""
        try:
            for chunk in response.iter_content(decode_unicode=True):
                if chunk:
                    buffer += chunk
                    *events, buffer = buffer.split("\n\n")
                    for event in events:
                        yield from self._parse_sse_event(event)
        finally:
            response.close()

    @staticmethod
    def _parse_sse_event(event: str) -> Iterator[Any]:
        """Parse a single SSE event block and yield JSON from data lines."""
        for line in event.split("\n"):
            if line.startswith("data:"):
                try:
                    yield json.loads(line[5:].strip())
                except json.JSONDecodeError:
                    continue

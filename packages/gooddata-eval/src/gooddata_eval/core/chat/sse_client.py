# (C) 2026 GoodData Corporation
"""SSE chat client for the agentic AI conversations API.

Ported from gdc-nas tavern-e2e app/sse_client.py (httpx instead of requests).

Why not gooddata_sdk.compute.ai_chat / ai_chat_stream? Those target the legacy
``/api/v1/actions/workspaces/{ws}/ai/chat[Stream]`` endpoint and expose a different
visualization shape (``metrics``/``dimensionality``). This evaluator scores the
*agentic* visualization (AAC ``query.fields`` shape) returned by the newer
``/api/v1/ai/workspaces/{ws}/chat/conversations`` endpoint, which is not yet
present in the generated api-client. When that endpoint lands in the SDK, this
module is the single place to swap — the runner only depends on the ChatBackend
protocol, not on this class.
"""

import json
from dataclasses import dataclass, field
from typing import Any, Iterable

import httpx

from gooddata_eval.core.models import ChatResult

SSE_DATA_PREFIX = "data: "


@dataclass
class _SseAccumulator:
    text_parts: list[str] = field(default_factory=list)
    viz_reasoning_parts: list[str] = field(default_factory=list)
    visualizations: list[dict[str, Any]] = field(default_factory=list)
    tool_call_events: list[dict[str, Any]] = field(default_factory=list)
    call_id_to_event_index: dict[str, int] = field(default_factory=dict)
    reasoning_steps: list[dict[str, Any]] = field(default_factory=list)
    adhoc_viz_args: list[dict[str, Any]] = field(default_factory=list)


def _handle_text(content: dict[str, Any], acc: _SseAccumulator) -> None:
    text = content.get("text", "")
    if text:
        acc.text_parts.append(text)


def _handle_multipart(content: dict[str, Any], acc: _SseAccumulator) -> None:
    for part in content.get("parts", []):
        ptype = part.get("type")
        if ptype == "text":
            t = part.get("text", "")
            if t:
                acc.text_parts.append(t)
                acc.viz_reasoning_parts.append(t)
        elif ptype == "visualization" and part.get("visualization"):
            acc.visualizations.append(part["visualization"])


def _handle_reasoning(content: dict[str, Any], acc: _SseAccumulator) -> None:
    summary = content.get("summary", "")
    if summary:
        acc.reasoning_steps.append({"summary": summary})


def _handle_tool_call(content: dict[str, Any], acc: _SseAccumulator) -> None:
    call_id = content.get("callId", "")
    acc.call_id_to_event_index[call_id] = len(acc.tool_call_events)
    acc.tool_call_events.append(
        {
            "functionName": content.get("name", ""),
            "functionArguments": json.dumps(content.get("arguments", {})),
            "result": None,
        }
    )
    # Stash visualization definition from create_adhoc_visualization so we can
    # evaluate the agent's intended answer even when the data source call fails.
    if content.get("name") == "create_adhoc_visualization":
        viz = (content.get("arguments") or {}).get("visualization")
        if viz and isinstance(viz, dict):
            acc.adhoc_viz_args.append(viz)


def _handle_tool_result(content: dict[str, Any], acc: _SseAccumulator) -> None:
    call_id = content.get("callId", "")
    idx = acc.call_id_to_event_index.get(call_id)
    if idx is not None:
        acc.tool_call_events[idx]["result"] = content.get("result", "")


def _build_chat_result(acc: _SseAccumulator) -> ChatResult:
    payload: dict[str, Any] = {
        "textResponse": "\n".join(acc.text_parts) or None,
        "toolCallEvents": acc.tool_call_events,
    }
    if acc.visualizations:
        payload["createdVisualizations"] = {
            "objects": acc.visualizations,
            "reasoning": "\n".join(acc.viz_reasoning_parts),
        }
    elif acc.adhoc_viz_args:
        # Fallback: the agent produced a correct visualization definition via
        # create_adhoc_visualization but the call failed (e.g. data source not
        # accessible). The last attempt is the agent's best answer.
        payload["createdVisualizations"] = {
            "objects": [acc.adhoc_viz_args[-1]],
            "reasoning": "\n".join(acc.viz_reasoning_parts),
        }
    return ChatResult.model_validate(payload)


def parse_sse_lines(lines: Iterable[str]) -> ChatResult:
    """Parse an SSE stream (iterable of decoded lines) into a ChatResult."""
    acc = _SseAccumulator()
    for raw_line in lines:
        line = raw_line.decode("utf-8") if isinstance(raw_line, bytes) else raw_line
        if not line or line.startswith("event: ") or not line.startswith(SSE_DATA_PREFIX):
            continue
        data_str = line[len(SSE_DATA_PREFIX) :]
        try:
            event_data = json.loads(data_str)
        except json.JSONDecodeError:
            continue
        if "statusCode" in event_data:
            raise RuntimeError(f"SSE error {event_data.get('statusCode')}: {event_data.get('detail')}")
        item = event_data.get("item")
        if not item:
            continue
        role = item.get("role")
        content: dict[str, Any] = item.get("content") or {}
        ctype = content.get("type")
        if role == "assistant":
            if ctype == "text":
                _handle_text(content, acc)
            elif ctype == "multipart":
                _handle_multipart(content, acc)
            elif ctype == "reasoning":
                _handle_reasoning(content, acc)
            elif ctype == "toolCall":
                _handle_tool_call(content, acc)
        elif role == "tool" and ctype == "toolResult":
            _handle_tool_result(content, acc)
    return _build_chat_result(acc)


class ChatClient:
    """Single-turn AI chat client over the GoodData AI conversation endpoints."""

    def __init__(self, host: str, token: str, workspace_id: str, *, timeout: float = 300.0):
        self._base = f"{host.rstrip('/')}/api/v1/ai/workspaces/{workspace_id}/chat/conversations"
        self._auth = {"Authorization": f"Bearer {token}"}
        self._client = httpx.Client(timeout=timeout)

    def _create_conversation(self) -> str:
        resp = self._client.post(self._base, headers={**self._auth, "Content-Type": "application/json"})
        resp.raise_for_status()
        body = resp.json()
        if "conversationId" not in body:
            raise ValueError(f"GoodData /chat/conversations response missing 'conversationId': {body}")
        return body["conversationId"]

    def _delete_conversation(self, conversation_id: str) -> None:
        try:
            self._client.delete(f"{self._base}/{conversation_id}", headers=self._auth)
        except httpx.HTTPError:
            pass  # best-effort cleanup

    def _send_message(self, conversation_id: str, question: str) -> ChatResult:
        url = f"{self._base}/{conversation_id}/messages"
        headers = {**self._auth, "Accept": "text/event-stream", "Content-Type": "application/json"}
        body = {"item": {"role": "user", "content": {"type": "text", "text": question}}}
        with self._client.stream("POST", url, json=body, headers=headers) as resp:
            resp.raise_for_status()
            return parse_sse_lines(resp.iter_lines())

    def ask(self, question: str) -> ChatResult:
        """Run one single-turn conversation: create, send, parse, clean up."""
        conversation_id = self._create_conversation()
        try:
            return self._send_message(conversation_id, question)
        finally:
            self._delete_conversation(conversation_id)

    def close(self) -> None:
        self._client.close()

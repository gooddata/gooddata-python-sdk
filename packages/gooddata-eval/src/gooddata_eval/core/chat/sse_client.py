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
import logging
import os
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, TypeVar

import httpx

from gooddata_eval.core.config import ReasoningEffort, normalize_reasoning_effort
from gooddata_eval.core.models import ChatResult, DatasetItem

_log = logging.getLogger(__name__)

SSE_DATA_PREFIX = "data: "
SSE_EVENT_PREFIX = "event: "
# gen-ai's last event, only if at least one item was already emitted (conversations_controller.py).
_RESPONSE_ENDED_EVENT = "response_ended"

_RETRYABLE_STATUS_CODES: frozenset[int] = frozenset({429, 502, 503, 504})
_METADATA_SYNC_MARKER = "METADATA_SYNC_IN_PROGRESS"


class ChatError(RuntimeError):
    """Non-retryable error reported by the chat SSE stream.

    ``partial_result`` carries whatever the accumulator captured before the error fired
    (tool calls included). Callers must not assume it's complete -- fields like
    ``stream_ended`` reflect the state at the moment of the error, not a finished turn.
    """

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        detail: str | None = None,
        partial_result: ChatResult | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.detail = detail
        self.partial_result = partial_result


class TransientChatError(ChatError):
    """Retryable transient error: gen-ai temporarily unavailable or still syncing metadata."""


def _int_env(name: str, default: int) -> int:
    """Read an int from the environment, falling back to ``default`` when unset or blank."""
    raw = os.getenv(name)
    return int(raw) if raw else default


def _float_env(name: str, default: float) -> float:
    """Read a float from the environment, falling back to ``default`` when unset or blank."""
    raw = os.getenv(name)
    return float(raw) if raw else default


# Retry budget. Defaults give a ~2 min worst-case cap per send (5/10/20/40/60s);
# overridable via env so CI can retune without cutting a new gooddata-eval release.
_MAX_RETRIES = _int_env("GOODDATA_EVAL_CHAT_MAX_RETRIES", 5)
_INITIAL_BACKOFF_S = _float_env("GOODDATA_EVAL_CHAT_INITIAL_BACKOFF_S", 5.0)
_BACKOFF_FACTOR = _float_env("GOODDATA_EVAL_CHAT_BACKOFF_FACTOR", 2.0)
_MAX_BACKOFF_S = _float_env("GOODDATA_EVAL_CHAT_MAX_BACKOFF_S", 60.0)

T = TypeVar("T")


def _is_retryable_exc(exc: Exception) -> bool:
    if isinstance(exc, TransientChatError):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in _RETRYABLE_STATUS_CODES
    # Mid-stream disconnect ("peer closed connection without sending complete
    # message body") -- pure network flake, not a real agent/content failure.
    # Confirmed live: contaminated ~1-4% of visualization runs with a hard
    # fail and zero retry attempts.
    return isinstance(exc, httpx.RemoteProtocolError)


def _retry_transient(operation: Callable[[], T], *, is_retryable: Callable[[Exception], bool]) -> T:
    """Run ``operation``; retry retryable failures with bounded exponential backoff."""
    delay = _INITIAL_BACKOFF_S
    for attempt in range(_MAX_RETRIES + 1):  # 0..N => N retries + 1 initial attempt
        try:
            return operation()
        except Exception as exc:  # noqa: PERF203 — retry loop: per-attempt try/except is intentional
            if attempt == _MAX_RETRIES or not is_retryable(exc):
                raise
            sleep_s = min(delay, _MAX_BACKOFF_S)
            _log.warning(
                "Transient gen-ai error (attempt %d/%d): %s; retrying in %.0fs",
                attempt + 1,
                _MAX_RETRIES + 1,
                exc,
                sleep_s,
            )
            time.sleep(sleep_s)
            delay *= _BACKOFF_FACTOR
    raise AssertionError("unreachable")  # loop either returns or raises


@dataclass
class _SseAccumulator:
    text_parts: list[str] = field(default_factory=list)
    viz_reasoning_parts: list[str] = field(default_factory=list)
    visualizations: list[dict[str, Any]] = field(default_factory=list)
    alert_proposals: list[dict[str, Any]] = field(default_factory=list)
    tool_call_events: list[dict[str, Any]] = field(default_factory=list)
    call_id_to_event_index: dict[str, int] = field(default_factory=dict)
    reasoning_steps: list[dict[str, Any]] = field(default_factory=list)
    adhoc_viz_args: list[dict[str, Any]] = field(default_factory=list)
    response_id: str | None = None
    stream_ended: bool = False
    # Reference point for call_ts/result_ts below -- client-observed receipt time, not a
    # server timestamp, so only meaningful as an offset within this one turn. Wrapped in a
    # lambda, not passed as `time.monotonic` directly -- a bare function reference binds at
    # class-body execution (import time), before tests can monkeypatch `sse_mod.time.monotonic`.
    t0: float = field(default_factory=lambda: time.monotonic())


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
        elif ptype == "alertProposal":
            # Record the part even when the server could not resolve the proposal payload
            # (``alertProposal: null``) — its mere presence is the confirmation signal, and
            # the reader falls back to a default CTA.
            acc.alert_proposals.append(part.get("alertProposal") or {})


def _handle_reasoning(content: dict[str, Any], acc: _SseAccumulator) -> None:
    summary = content.get("summary", "")
    if summary:
        acc.reasoning_steps.append(
            {"summary": summary, "ts": round(time.monotonic() - acc.t0, 3), "index": len(acc.reasoning_steps)}
        )


def _handle_tool_call(content: dict[str, Any], acc: _SseAccumulator) -> None:
    call_id = content.get("callId", "")
    idx = len(acc.tool_call_events)
    acc.call_id_to_event_index[call_id] = idx
    acc.tool_call_events.append(
        {
            "functionName": content.get("name", ""),
            "functionArguments": json.dumps(content.get("arguments", {})),
            "result": None,
            "call_ts": round(time.monotonic() - acc.t0, 3),
            "index": idx,
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
        acc.tool_call_events[idx]["result_ts"] = round(time.monotonic() - acc.t0, 3)


def _build_chat_result(acc: _SseAccumulator) -> ChatResult:
    payload: dict[str, Any] = {
        "textResponse": "\n".join(acc.text_parts) or None,
        "alertProposals": acc.alert_proposals,
        "toolCallEvents": acc.tool_call_events,
        "reasoningStepCount": len(acc.reasoning_steps),
        "reasoningSteps": [step["summary"] for step in acc.reasoning_steps],
        "reasoningStepEvents": acc.reasoning_steps,
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
    result = ChatResult.model_validate(payload)
    result.response_id = acc.response_id
    result.stream_ended = acc.stream_ended
    return result


def parse_sse_lines(lines: Iterable[str]) -> ChatResult:
    """Parse an SSE stream (iterable of decoded lines) into a ChatResult."""
    acc = _SseAccumulator()
    current_event = "message"  # SSE default in the absence of an explicit "event: " line
    it = iter(lines)
    while True:
        try:
            raw_line = next(it)
        except StopIteration:
            break
        except Exception as exc:
            # Only a transport-level failure (e.g. connection drop mid-stream) is rescued
            # here -- a bug in the processing below must propagate uncaught, not get
            # mislabeled as a network error.
            partial = _build_chat_result(acc)
            if isinstance(exc, httpx.RemoteProtocolError):
                # Same mid-stream disconnect _is_retryable_exc already retries when it happens
                # at connect time -- here it surfaces from `next(it)` instead, so it must be
                # raised as TransientChatError or the wrapping below would mask it as
                # non-retryable and defeat the retry this class exists for.
                raise TransientChatError(f"SSE stream error: {exc}", partial_result=partial) from exc
            raise ChatError(f"SSE stream error: {exc}", partial_result=partial) from exc
        line = raw_line.decode("utf-8") if isinstance(raw_line, bytes) else raw_line
        if not line:
            current_event = "message"  # blank line ends one event block per the SSE spec
            continue
        if line.startswith(SSE_EVENT_PREFIX):
            current_event = line[len(SSE_EVENT_PREFIX) :].strip()
            if current_event == _RESPONSE_ENDED_EVENT:
                acc.stream_ended = True
            continue
        if not line.startswith(SSE_DATA_PREFIX):
            continue
        if current_event == _RESPONSE_ENDED_EVENT:
            continue
        data_str = line[len(SSE_DATA_PREFIX) :]
        if _METADATA_SYNC_MARKER in data_str:
            raise TransientChatError(
                f"SSE transient error: {_METADATA_SYNC_MARKER}",
                status_code=None,
                detail=None,
                partial_result=_build_chat_result(acc),
            )
        try:
            event_data = json.loads(data_str)
        except json.JSONDecodeError:
            continue
        if "statusCode" in event_data:
            code = event_data.get("statusCode")
            detail = event_data.get("detail")
            message = f"SSE error {code}: {detail}"
            if code in _RETRYABLE_STATUS_CODES:
                raise TransientChatError(
                    message, status_code=code, detail=detail, partial_result=_build_chat_result(acc)
                )
            raise ChatError(message, status_code=code, detail=detail, partial_result=_build_chat_result(acc))
        if event_data.get("responseId") and not acc.response_id:
            acc.response_id = event_data["responseId"]
        item = event_data.get("item")
        if not item:
            continue
        if item.get("responseId") and not acc.response_id:
            acc.response_id = item["responseId"]
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

    def __init__(
        self,
        host: str,
        token: str,
        workspace_id: str,
        *,
        timeout: float = 300.0,
        preserve_failed: bool = False,
        reasoning_effort: ReasoningEffort | None = None,
        agent_id: str | None = None,
    ):
        """Create a chat client bound to one workspace.

        ``reasoning_effort`` (``LOW``/``MEDIUM``/``HIGH``) is sent as
        ``options.reasoningEffort`` on every message; when None the key is omitted
        entirely and the server keeps its own default. The server honours it only
        while the ``enableGenAiReasoningEffort`` feature flag is on for the
        organization, so setting it is a request rather than a guarantee.
        """
        self._base = f"{host.rstrip('/')}/api/v1/ai/workspaces/{workspace_id}/chat/conversations"
        self._auth = {"Authorization": f"Bearer {token}"}
        self._client = httpx.Client(timeout=timeout)
        self._preserve_failed = preserve_failed
        self._reasoning_effort = normalize_reasoning_effort(reasoning_effort)
        self._agent_id = agent_id

    def create_conversation(self) -> str:
        def _do() -> str:
            body = {"agentId": self._agent_id} if self._agent_id else {}
            resp = self._client.post(self._base, headers={**self._auth, "Content-Type": "application/json"}, json=body)
            resp.raise_for_status()
            body = resp.json()
            if "conversationId" not in body:
                raise ValueError(f"GoodData /chat/conversations response missing 'conversationId': {body}")
            return body["conversationId"]

        # NOTE: retrying create is not idempotent — a created-then-503 can leak an
        # orphaned (ephemeral) conversation. Acceptable for eval; do not reuse blindly.
        return _retry_transient(_do, is_retryable=_is_retryable_exc)

    def delete_conversation(self, conversation_id: str) -> None:
        try:
            self._client.delete(f"{self._base}/{conversation_id}", headers=self._auth)
        except httpx.HTTPError:
            pass  # best-effort cleanup

    def send_message(self, conversation_id: str, question: str) -> ChatResult:
        url = f"{self._base}/{conversation_id}/messages"
        headers = {**self._auth, "Accept": "text/event-stream", "Content-Type": "application/json"}
        body: dict[str, Any] = {"item": {"role": "user", "content": {"type": "text", "text": question}}}
        if self._reasoning_effort is not None:
            body["options"] = {"reasoningEffort": self._reasoning_effort}

        def _do() -> ChatResult:
            # Set fresh on every retry attempt (before opening this attempt's stream, so its
            # own connection setup time counts) -- excludes not just the sleep backoff between
            # attempts, but the entire duration of any earlier failed attempt.
            t0 = time.monotonic()
            with self._client.stream("POST", url, json=body, headers=headers) as resp:
                resp.raise_for_status()
                try:
                    result = parse_sse_lines(resp.iter_lines())
                except ChatError as exc:
                    if exc.partial_result is not None:
                        exc.partial_result.turn_wall_clock_sec = time.monotonic() - t0
                    raise
                result.turn_wall_clock_sec = time.monotonic() - t0
                return result

        return _retry_transient(_do, is_retryable=_is_retryable_exc)

    def ask(self, item: DatasetItem) -> ChatResult:
        """Run one conversation: create, send, parse, clean up.

        The conversation_id is attached to the returned ChatResult for tracing.
        When ``preserve_failed`` is set, failed conversations are kept on the
        server so they can be inspected after the run; the conversation_id is
        attached to the raised exception as well.
        """
        conversation_id = self.create_conversation()
        success = False
        try:
            result = self.send_message(conversation_id, item.question)
            result.conversation_id = conversation_id
            success = True
            return result
        except Exception as exc:
            try:
                object.__setattr__(exc, "conversation_id", conversation_id)
            except TypeError:
                pass  # C-extension exception that rejects __setattr__
            raise
        finally:
            if success or not self._preserve_failed:
                self.delete_conversation(conversation_id)

    def close(self) -> None:
        self._client.close()

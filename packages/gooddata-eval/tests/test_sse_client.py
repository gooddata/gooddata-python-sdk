# (C) 2026 GoodData Corporation
import json

import httpx
import pytest
from gooddata_eval.core.chat import sse_client as sse_mod
from gooddata_eval.core.chat.sse_client import ChatClient, ChatError, TransientChatError, parse_sse_lines


def test_parse_sse_lines_collects_text_and_visualization(fixtures_dir):
    lines = (fixtures_dir / "sse_visualization_stream.txt").read_text().splitlines()
    result = parse_sse_lines(lines)
    assert result.text_response == "Here is your chart"
    assert result.created_visualizations is not None
    assert result.created_visualizations.objects[0].id == "v1"
    assert result.created_visualizations.objects[0].type == "column_chart"


def test_parse_sse_lines_raises_on_error_event():
    lines = ['data: {"statusCode": 500, "detail": "boom"}']
    with pytest.raises(RuntimeError, match="SSE error 500"):
        parse_sse_lines(lines)


def test_parse_sse_lines_ignores_non_data_lines():
    result = parse_sse_lines(["event: ping", "", ": comment"])
    assert result.text_response is None
    assert result.created_visualizations is None


def test_parse_sse_lines_falls_back_to_adhoc_viz_when_multipart_viz_is_null():
    """Visualization from create_adhoc_visualization args used when multipart viz is null."""
    viz_def = {
        "id": "total_sales_by_month",
        "type": "line_chart",
        "query": {"fields": {"m": {"using": "metric/total_sales"}}, "filter_by": {}},
        "metrics": ["m"],
        "view_by": [],
    }
    lines = [
        # agent calls create_adhoc_visualization — stash the viz
        f'data: {{"item": {{"role": "assistant", "content": {{"type": "toolCall", "callId": "c1", "name": "create_adhoc_visualization", "arguments": {{"visualization": {json.dumps(viz_def)}}}}}}}}}',
        # data source fails
        'data: {"item": {"role": "tool", "content": {"type": "toolResult", "callId": "c1", "result": "{"status": "error", "message": "Data source does not exist"}"}}}',
        # final multipart — visualization is null
        'data: {"item": {"role": "assistant", "content": {"type": "multipart", "parts": [{"type": "text", "text": "Could not create"}, {"type": "visualization", "visualization": null}]}}}',
    ]
    result = parse_sse_lines(lines)
    assert result.created_visualizations is not None
    assert result.created_visualizations.objects[0].id == "total_sales_by_month"
    assert result.created_visualizations.objects[0].type == "line_chart"


def test_parse_sse_lines_counts_reasoning_steps():
    lines = [
        'data: {"item": {"role": "assistant", "content": {"type": "reasoning", "summary": "step one"}}}',
        'data: {"item": {"role": "assistant", "content": {"type": "reasoning", "summary": "step two"}}}',
        'data: {"item": {"role": "assistant", "content": {"type": "text", "text": "Done"}}}',
    ]
    result = parse_sse_lines(lines)
    assert result.reasoning_step_count == 2
    assert result.text_response == "Done"


def test_parse_sse_lines_prefers_multipart_viz_over_adhoc_fallback():
    """Real multipart visualization takes priority over adhoc tool call stash."""

    adhoc_viz = {"id": "adhoc", "type": "table", "query": {"fields": {}, "filter_by": {}}}
    real_viz = {
        "id": "real",
        "type": "column_chart",
        "query": {"fields": {"m": {"using": "metric/rev"}}, "filter_by": {}},
        "metrics": ["m"],
        "view_by": [],
    }
    lines = [
        f'data: {{"item": {{"role": "assistant", "content": {{"type": "toolCall", "callId": "c1", "name": "create_adhoc_visualization", "arguments": {{"visualization": {json.dumps(adhoc_viz)}}}}}}}}}',
        f'data: {{"item": {{"role": "assistant", "content": {{"type": "multipart", "parts": [{{"type": "visualization", "visualization": {json.dumps(real_viz)}}}]}}}}}}',
    ]
    result = parse_sse_lines(lines)
    assert result.created_visualizations.objects[0].id == "real"


@pytest.mark.parametrize("code", [429, 502, 503, 504])
def test_parse_sse_lines_transient_status_codes(code):
    with pytest.raises(TransientChatError) as ei:
        parse_sse_lines([f'data: {{"statusCode": {code}, "detail": null}}'])
    assert ei.value.status_code == code


def test_parse_sse_lines_metadata_sync_is_transient():
    with pytest.raises(TransientChatError):
        parse_sse_lines(['data: {"reasonCode": "METADATA_SYNC_IN_PROGRESS"}'])


def test_parse_sse_lines_metadata_sync_marker_in_malformed_json_is_transient():
    # marker present but the data payload is not valid JSON -> still transient, not swallowed
    with pytest.raises(TransientChatError):
        parse_sse_lines(["data: {bad json METADATA_SYNC_IN_PROGRESS"])


def test_parse_sse_lines_non_retryable_status_is_chat_error_not_transient():
    with pytest.raises(ChatError) as ei:
        parse_sse_lines(['data: {"statusCode": 400, "detail": "bad"}'])
    assert not isinstance(ei.value, TransientChatError)
    assert ei.value.status_code == 400


def _client_with_handler(handler):
    client = ChatClient(host="https://example.invalid", token="t", workspace_id="w")
    client._client = httpx.Client(transport=httpx.MockTransport(handler))
    return client


_TRANSIENT_SSE = b'data: {"statusCode": 503, "detail": null}\n'
_NONRETRY_SSE = b'data: {"statusCode": 400, "detail": "bad"}\n'
_OK_SSE = b'data: {"item": {"role": "assistant", "content": {"type": "text", "text": "ok"}}}\n'


def test_send_message_retries_transient_then_succeeds(monkeypatch):
    sleeps = []
    monkeypatch.setattr(sse_mod.time, "sleep", lambda s: sleeps.append(s))
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        return httpx.Response(200, content=_TRANSIENT_SSE if calls["n"] < 3 else _OK_SSE)

    client = _client_with_handler(handler)
    result = client.send_message("conv", "q")
    assert result.text_response == "ok"
    assert calls["n"] == 3
    assert sleeps == [5, 10]


def test_send_message_backoff_schedule_then_raises(monkeypatch):
    sleeps = []
    monkeypatch.setattr(sse_mod.time, "sleep", lambda s: sleeps.append(s))
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        return httpx.Response(200, content=_TRANSIENT_SSE)

    client = _client_with_handler(handler)
    with pytest.raises(TransientChatError):
        client.send_message("conv", "q")
    assert calls["n"] == 6  # 1 initial + 5 retries
    assert sleeps == [5, 10, 20, 40, 60]


def test_send_message_does_not_retry_non_transient(monkeypatch):
    sleeps = []
    monkeypatch.setattr(sse_mod.time, "sleep", lambda s: sleeps.append(s))
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        return httpx.Response(200, content=_NONRETRY_SSE)

    client = _client_with_handler(handler)
    with pytest.raises(ChatError) as ei:
        client.send_message("conv", "q")
    assert not isinstance(ei.value, TransientChatError)
    assert calls["n"] == 1
    assert sleeps == []


def test_create_conversation_retries_then_succeeds(monkeypatch):
    sleeps = []
    monkeypatch.setattr(sse_mod.time, "sleep", lambda s: sleeps.append(s))
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        if calls["n"] < 3:
            return httpx.Response(503)
        return httpx.Response(200, json={"conversationId": "abc"})

    client = _client_with_handler(handler)
    assert client.create_conversation() == "abc"
    assert calls["n"] == 3
    assert sleeps == [5, 10]


def test_create_conversation_does_not_retry_4xx(monkeypatch):
    sleeps = []
    monkeypatch.setattr(sse_mod.time, "sleep", lambda s: sleeps.append(s))
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        return httpx.Response(400)

    client = _client_with_handler(handler)
    with pytest.raises(httpx.HTTPStatusError):
        client.create_conversation()
    assert calls["n"] == 1
    assert sleeps == []


def test_int_env_uses_default_when_unset(monkeypatch):
    monkeypatch.delenv("GD_TEST_INT", raising=False)
    assert sse_mod._int_env("GD_TEST_INT", 5) == 5


def test_int_env_uses_default_when_blank(monkeypatch):
    monkeypatch.setenv("GD_TEST_INT", "")
    assert sse_mod._int_env("GD_TEST_INT", 5) == 5


def test_int_env_reads_override(monkeypatch):
    monkeypatch.setenv("GD_TEST_INT", "2")
    assert sse_mod._int_env("GD_TEST_INT", 5) == 2


def test_float_env_uses_default_when_unset(monkeypatch):
    monkeypatch.delenv("GD_TEST_FLOAT", raising=False)
    assert sse_mod._float_env("GD_TEST_FLOAT", 5.0) == 5.0


def test_float_env_reads_override(monkeypatch):
    monkeypatch.setenv("GD_TEST_FLOAT", "1.5")
    assert sse_mod._float_env("GD_TEST_FLOAT", 5.0) == 1.5

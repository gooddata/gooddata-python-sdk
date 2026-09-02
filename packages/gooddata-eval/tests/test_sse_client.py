# (C) 2026 GoodData Corporation
import json

import httpx
import pytest
from gooddata_eval.core.chat import sse_client as sse_mod
from gooddata_eval.core.chat.sse_client import ChatClient, ChatError, TransientChatError, parse_sse_lines
from gooddata_eval.core.models import DatasetItem, ReasoningStepEvent, ToolCallEvent, build_latency_breakdown


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


def test_parse_sse_lines_error_carries_partial_result_with_tool_calls_already_seen():
    # A statusCode error ends the stream before _build_chat_result ever runs -- without
    # partial_result, a tool call that already succeeded (e.g. KDA's own create/execute)
    # before a LATER, unrelated error killed the turn would be silently discarded, making
    # the run look like the agent never called the tool at all.
    lines = [
        json.dumps(
            {
                "item": {
                    "role": "assistant",
                    "content": {"type": "toolCall", "callId": "c1", "name": "create_key_driver_analysis"},
                }
            }
        ),
        "",
        json.dumps(
            {
                "item": {
                    "role": "tool",
                    "content": {
                        "type": "toolResult",
                        "callId": "c1",
                        "result": json.dumps({"success": True}),
                    },
                }
            }
        ),
        "",
        json.dumps({"statusCode": 500, "detail": "boom"}),
    ]
    lines = [f"data: {line}" if line else line for line in lines]
    with pytest.raises(ChatError) as ei:
        parse_sse_lines(lines)
    partial = ei.value.partial_result
    assert partial is not None
    assert len(partial.tool_call_events) == 1
    assert partial.tool_call_events[0].function_name == "create_key_driver_analysis"
    assert partial.tool_call_events[0].result == '{"success": true}'


def test_parse_sse_lines_stamps_call_and_result_receipt_time(monkeypatch):
    # t0 (accumulator construction) = 100.0, tool_call received at 105.0, tool_result
    # received at 130.5 -- call_ts/result_ts are offsets from t0, so 5.0 and 30.5.
    monkeypatch.setattr(sse_mod.time, "monotonic", iter([100.0, 105.0, 130.5]).__next__)
    lines = [
        json.dumps(
            {
                "item": {
                    "role": "assistant",
                    "content": {"type": "toolCall", "callId": "c1", "name": "create_key_driver_analysis"},
                }
            }
        ),
        "",
        json.dumps(
            {
                "item": {
                    "role": "tool",
                    "content": {"type": "toolResult", "callId": "c1", "result": json.dumps({"success": True})},
                }
            }
        ),
    ]
    lines = [f"data: {line}" if line else line for line in lines]
    result = parse_sse_lines(lines)
    tc = result.tool_call_events[0]
    assert tc.call_ts == 5.0
    assert tc.result_ts == 30.5
    assert tc.index == 0


def test_build_latency_breakdown_gives_repeated_tool_calls_separate_entries_in_order():
    # Same tool called twice, back-to-back (no gap between them). A dict keyed by tool
    # name would sum these into one number and lose which call was slower -- each call
    # must stay its own entry, in the order it actually ran, identifiable by its index.
    events = [
        ToolCallEvent(function_name="search_tool", function_arguments="{}", call_ts=0.0, result_ts=2.5, index=0),
        ToolCallEvent(function_name="search_tool", function_arguments="{}", call_ts=2.5, result_ts=3.5, index=1),
        ToolCallEvent(
            function_name="create_metric_alert", function_arguments="{}", call_ts=3.5, result_ts=63.7, index=2
        ),
    ]
    assert build_latency_breakdown(events) == [
        {"seq": 0, "kind": "tool", "name": "search_tool", "index": 0, "duration_s": 2.5},
        {"seq": 1, "kind": "tool", "name": "search_tool", "index": 1, "duration_s": 1.0},
        {"seq": 2, "kind": "tool", "name": "create_metric_alert", "index": 2, "duration_s": 60.2},
    ]


def test_build_latency_breakdown_attributes_gaps_to_reasoning_steps():
    # search_tool runs 0-2.5s. Then a gap: the model emits a reasoning step at 2.5s, then
    # goes idle until the next tool call starts at 5.0s -- that whole 2.5s idle gap belongs
    # to the reasoning step, not to "search_tool" (which already finished) or nothing.
    tool_events = [
        ToolCallEvent(function_name="search_tool", function_arguments="{}", call_ts=0.0, result_ts=2.5, index=0),
        ToolCallEvent(
            function_name="create_metric_alert", function_arguments="{}", call_ts=5.0, result_ts=65.0, index=1
        ),
    ]
    reasoning_events = [ReasoningStepEvent(summary="Picking the right metric", ts=2.5, index=0)]
    result = build_latency_breakdown(tool_events, reasoning_events)
    assert result == [
        {"seq": 0, "kind": "tool", "name": "search_tool", "index": 0, "duration_s": 2.5},
        {"seq": 1, "kind": "reasoning", "name": "Picking the right metric", "index": 0, "duration_s": 2.5},
        {"seq": 2, "kind": "tool", "name": "create_metric_alert", "index": 1, "duration_s": 60.0},
    ]


def test_build_latency_breakdown_uses_bold_title_as_reasoning_name():
    # Real reasoning summaries are a bolded title followed by a full paragraph -- "name"
    # must be just the title, not the whole thing.
    tool_events = [
        ToolCallEvent(function_name="search_tool", function_arguments="{}", call_ts=0.0, result_ts=2.5, index=0),
        ToolCallEvent(
            function_name="create_metric_alert", function_arguments="{}", call_ts=5.0, result_ts=6.0, index=1
        ),
    ]
    reasoning_events = [
        ReasoningStepEvent(summary="**Picking the right metric**\n\nLots more detail follows here.", ts=2.5, index=0)
    ]
    result = build_latency_breakdown(tool_events, reasoning_events)
    reasoning_step = next(s for s in result if s["kind"] == "reasoning")
    assert reasoning_step["name"] == "Picking the right metric"
    assert "Lots more detail" not in reasoning_step["name"]


def test_build_latency_breakdown_disambiguates_reasoning_steps_sharing_a_title_by_index():
    # Two reasoning steps sharing the same title (a real, common occurrence) must stay
    # distinguishable via "index" even though "name" repeats.
    tool_events = [
        ToolCallEvent(function_name="search_tool", function_arguments="{}", call_ts=0.0, result_ts=1.0, index=0),
        ToolCallEvent(function_name="search_tool", function_arguments="{}", call_ts=4.0, result_ts=5.0, index=1),
        ToolCallEvent(
            function_name="create_metric_alert", function_arguments="{}", call_ts=8.0, result_ts=9.0, index=2
        ),
    ]
    reasoning_events = [
        ReasoningStepEvent(summary="**Considering data analysis**", ts=1.0, index=0),
        ReasoningStepEvent(summary="**Considering data analysis**", ts=5.0, index=1),
    ]
    result = build_latency_breakdown(tool_events, reasoning_events)
    reasoning_steps = [s for s in result if s["kind"] == "reasoning"]
    assert [s["index"] for s in reasoning_steps] == [0, 1]
    assert all(s["name"] == "Considering data analysis" for s in reasoning_steps)
    assert [s["duration_s"] for s in reasoning_steps] == [3.0, 3.0]


def test_build_latency_breakdown_truncates_untitled_reasoning_names():
    tool_events = [
        ToolCallEvent(function_name="search_tool", function_arguments="{}", call_ts=0.0, result_ts=2.5, index=0),
        ToolCallEvent(
            function_name="create_metric_alert", function_arguments="{}", call_ts=5.0, result_ts=6.0, index=1
        ),
    ]
    long_summary = "x" * 200
    reasoning_events = [ReasoningStepEvent(summary=long_summary, ts=2.5, index=0)]
    result = build_latency_breakdown(tool_events, reasoning_events)
    reasoning_step = next(s for s in result if s["kind"] == "reasoning")
    assert len(reasoning_step["name"]) < len(long_summary)


def test_build_latency_breakdown_seq_reflects_true_execution_order():
    # Interleaved on purpose: reasoning, tool, reasoning, tool -- seq must follow actual
    # chronological order, not group all tools first or all reasoning first.
    tool_events = [
        ToolCallEvent(function_name="search_tool", function_arguments="{}", call_ts=1.0, result_ts=2.0, index=0),
        ToolCallEvent(
            function_name="create_metric_alert", function_arguments="{}", call_ts=4.0, result_ts=5.0, index=1
        ),
    ]
    reasoning_events = [
        ReasoningStepEvent(summary="**First**", ts=0.0, index=0),
        ReasoningStepEvent(summary="**Second**", ts=3.0, index=1),
    ]
    result = build_latency_breakdown(tool_events, reasoning_events)
    # "First" appears twice: once for the 0.0-1.0 gap before search_tool starts, and again
    # for the 2.0-3.0 gap after it resolves -- "First" is still the last-emitted reasoning
    # step until "Second" itself arrives at 3.0, so that gap is correctly its too.
    assert [(s["seq"], s["kind"], s["name"]) for s in result] == [
        (0, "reasoning", "First"),
        (1, "tool", "search_tool"),
        (2, "reasoning", "First"),
        (3, "reasoning", "Second"),
        (4, "tool", "create_metric_alert"),
    ]


def test_build_latency_breakdown_gap_with_no_reasoning_events_gets_a_catch_all_name():
    # A gap between two tool calls with zero reasoning events supplied at all (e.g. an
    # older chat backend, or reasoning capture disabled) must not be silently dropped --
    # it needs a name that doesn't fake having a real summary for it.
    tool_events = [
        ToolCallEvent(function_name="search_tool", function_arguments="{}", call_ts=0.0, result_ts=2.5, index=0),
        ToolCallEvent(
            function_name="create_metric_alert", function_arguments="{}", call_ts=5.0, result_ts=65.0, index=1
        ),
    ]
    result = build_latency_breakdown(tool_events, reasoning_step_events=None)
    assert result == [
        {"seq": 0, "kind": "tool", "name": "search_tool", "index": 0, "duration_s": 2.5},
        {"seq": 1, "kind": "reasoning", "name": "(before first step)", "index": None, "duration_s": 2.5},
        {"seq": 2, "kind": "tool", "name": "create_metric_alert", "index": 1, "duration_s": 60.0},
    ]


def test_build_latency_breakdown_skips_calls_missing_a_timestamp():
    events = [
        ToolCallEvent(function_name="search_tool", function_arguments="{}", call_ts=0.0, result_ts=None),
        ToolCallEvent(function_name="create_metric_alert", function_arguments="{}"),
    ]
    assert build_latency_breakdown(events) == []


def test_parse_sse_lines_raw_transport_error_also_carries_partial_result():
    # A connection drop mid-stream (httpx.RemoteProtocolError/ReadError) has no statusCode
    # payload -- it's a raw exception from iterating `lines` itself, not one this module
    # raises. Must still be rescued the same way a statusCode-shaped error is.
    def _lines():
        yield (
            'data: {"item": {"role": "assistant", "content": '
            + json.dumps({"type": "toolCall", "callId": "c1", "name": "create_key_driver_analysis"})
            + "}}"
        )
        yield ""
        raise RuntimeError("connection dropped")

    with pytest.raises(ChatError) as ei:
        parse_sse_lines(_lines())
    assert not isinstance(ei.value, TransientChatError)  # not retried -- same as before this fix
    partial = ei.value.partial_result
    assert partial is not None
    assert len(partial.tool_call_events) == 1
    assert partial.tool_call_events[0].function_name == "create_key_driver_analysis"


def test_parse_sse_lines_remote_protocol_error_mid_stream_is_retryable():
    # httpx.RemoteProtocolError raised from `next(it)` (mid-stream, not at connect time) must
    # come out as TransientChatError -- otherwise _is_retryable_exc never sees the raw
    # RemoteProtocolError (only the ChatError parse_sse_lines wraps it in) and the retry this
    # class exists for never fires. Same partial_result guarantee as any other transport error.
    def _lines():
        yield (
            'data: {"item": {"role": "assistant", "content": '
            + json.dumps({"type": "toolCall", "callId": "c1", "name": "create_key_driver_analysis"})
            + "}}"
        )
        yield ""
        raise httpx.RemoteProtocolError("peer closed connection without sending complete message body")

    with pytest.raises(TransientChatError) as ei:
        parse_sse_lines(_lines())
    partial = ei.value.partial_result
    assert partial is not None
    assert len(partial.tool_call_events) == 1
    assert partial.tool_call_events[0].function_name == "create_key_driver_analysis"


def test_parse_sse_lines_a_real_parsing_bug_propagates_uncaught_not_as_a_chat_error():
    # A malformed payload (here: "item" is a string, not a dict) crashes the processing
    # code itself with a plain AttributeError -- must surface loudly as that bug, not get
    # silently relabeled as a ChatError/"SSE stream error" indistinguishable from a
    # genuine network blip. Only a failure from iterating `lines` itself is rescued.
    lines = ['data: {"item": "not-a-dict"}']
    with pytest.raises(AttributeError):
        parse_sse_lines(lines)


def test_parse_sse_lines_ignores_non_data_lines():
    result = parse_sse_lines(["event: ping", "", ": comment"])
    assert result.text_response is None
    assert result.created_visualizations is None


def test_parse_sse_lines_stream_ended_false_when_response_ended_never_arrives():
    # A turn cut off mid-stream (connection dropped, process killed) never gets to emit
    # gen-ai's own "response_ended" event -- text_response can still be non-empty from
    # whatever text arrived before the cutoff.
    lines = [
        "event: item",
        'data: {"item": {"role": "assistant", "content": {"type": "text", "text": "partial answ"}}}',
        "",
    ]
    result = parse_sse_lines(lines)
    assert result.text_response == "partial answ"
    assert result.stream_ended is False


def test_parse_sse_lines_stream_ended_true_when_response_ended_event_arrives():
    lines = [
        "event: item",
        'data: {"item": {"role": "assistant", "content": {"type": "text", "text": "full answer"}}}',
        "",
        "event: response_ended",
        "data: {}",
        "",
    ]
    result = parse_sse_lines(lines)
    assert result.text_response == "full answer"
    assert result.stream_ended is True


def test_parse_sse_lines_stream_ended_defaults_false_with_no_events_at_all():
    assert parse_sse_lines([]).stream_ended is False


def test_parse_sse_lines_stream_ended_true_when_response_ended_has_no_data_line():
    lines = [
        "event: item",
        'data: {"item": {"role": "assistant", "content": {"type": "text", "text": "x"}}}',
        "",
        "event: response_ended",
        "",
    ]
    assert parse_sse_lines(lines).stream_ended is True


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
    assert result.reasoning_steps == ["step one", "step two"]
    assert result.text_response == "Done"


def test_parse_sse_lines_reasoning_steps_empty_when_no_reasoning_events():
    lines = ['data: {"item": {"role": "assistant", "content": {"type": "text", "text": "Done"}}}']
    result = parse_sse_lines(lines)
    assert result.reasoning_step_count == 0
    assert result.reasoning_steps == []


def test_parse_sse_lines_stamps_reasoning_step_receipt_time(monkeypatch):
    monkeypatch.setattr(sse_mod.time, "monotonic", iter([100.0, 104.5, 110.0]).__next__)
    lines = [
        'data: {"item": {"role": "assistant", "content": {"type": "reasoning", "summary": "step one"}}}',
        'data: {"item": {"role": "assistant", "content": {"type": "reasoning", "summary": "step two"}}}',
    ]
    result = parse_sse_lines(lines)
    assert [e.summary for e in result.reasoning_step_events] == ["step one", "step two"]
    assert [e.ts for e in result.reasoning_step_events] == [4.5, 10.0]
    assert [e.index for e in result.reasoning_step_events] == [0, 1]


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


def test_parse_sse_lines_collects_alert_proposal_without_text_part():
    """The alert skill's confirmation turn emits ONLY an alertProposal part (GDAI-2032).

    Pins the wire contract the simulated-user loops depend on: part ``type`` is
    ``alertProposal`` and the payload lives under the ``alertProposal`` key.
    """
    proposal = {
        "title": "# of Orders Alert - Greater Than 500",
        "cta": "Should I create this alert?",
        "recipients": [{"email": "admin@gooddata.com"}],
        "alert": {"trigger": "ALWAYS", "execution": {"measures": [{"opaque": "afm"}]}},
    }
    lines = [
        'data: {"item": {"role": "assistant", "content": {"type": "toolCall", "callId": "c1", '
        '"name": "prepare_metric_alert_proposal", "arguments": {}}}}',
        f'data: {{"item": {{"role": "assistant", "content": {{"type": "multipart", '
        f'"parts": [{{"type": "alertProposal", "alertProposal": {json.dumps(proposal)}}}]}}}}}}',
    ]
    result = parse_sse_lines(lines)
    assert result.text_response is None
    assert result.alert_proposals == [proposal]


def test_parse_sse_lines_keeps_alert_proposal_part_when_payload_is_null():
    """Presence of the part is the confirmation signal even if the server did not resolve it."""
    lines = [
        'data: {"item": {"role": "assistant", "content": {"type": "multipart", '
        '"parts": [{"type": "alertProposal", "alertProposal": null}]}}}',
    ]
    result = parse_sse_lines(lines)
    assert result.alert_proposals == [{}]


def test_parse_sse_lines_has_no_alert_proposals_by_default():
    lines = ['data: {"item": {"role": "assistant", "content": {"type": "text", "text": "Done"}}}']
    assert parse_sse_lines(lines).alert_proposals == []


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


def _client_with_handler(handler, **kwargs):
    client = ChatClient(host="https://example.invalid", token="t", workspace_id="w", **kwargs)
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


def test_send_message_sets_turn_wall_clock_sec_on_success(monkeypatch):
    # 3 monotonic() calls per attempt now: t0, _SseAccumulator's own t0, final wall-clock.
    monkeypatch.setattr(sse_mod.time, "monotonic", iter([100.0, 100.0, 102.5]).__next__)
    client = _client_with_handler(lambda request: httpx.Response(200, content=_OK_SSE))
    result = client.send_message("conv", "q")
    assert result.turn_wall_clock_sec == pytest.approx(2.5)


def test_send_message_wall_clock_excludes_retry_backoff(monkeypatch):
    # t0 must be per-attempt, set inside _do() before the connection opens -- not around
    # the whole send_message() call -- or a failed attempt's time plus the backoff sleep
    # between attempts (harness/network overhead, not gen-ai's time) would inflate the
    # reported latency.
    monkeypatch.setattr(sse_mod.time, "sleep", lambda s: None)
    # 3 monotonic() calls per attempt now: t0, _SseAccumulator's own t0, final wall-clock.
    monkeypatch.setattr(sse_mod.time, "monotonic", iter([1000.0, 1000.0, 1000.5, 2000.0, 2000.0, 2001.2]).__next__)
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        return httpx.Response(200, content=_TRANSIENT_SSE if calls["n"] < 2 else _OK_SSE)

    client = _client_with_handler(handler)
    result = client.send_message("conv", "q")
    assert calls["n"] == 2
    assert result.turn_wall_clock_sec == pytest.approx(1.2)  # attempt 2 alone, not spanning attempt 1 + backoff


def test_send_message_stamps_turn_wall_clock_sec_on_partial_result_too(monkeypatch):
    # 3 monotonic() calls now: t0, _SseAccumulator's own t0, partial-result wall-clock.
    monkeypatch.setattr(sse_mod.time, "monotonic", iter([50.0, 50.0, 51.0]).__next__)
    client = _client_with_handler(lambda request: httpx.Response(200, content=_NONRETRY_SSE))
    with pytest.raises(ChatError) as ei:
        client.send_message("conv", "q")
    assert ei.value.partial_result is not None
    assert ei.value.partial_result.turn_wall_clock_sec == pytest.approx(1.0)


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


def test_create_conversation_retries_remote_protocol_error(monkeypatch):
    # "peer closed connection without sending complete message body" -- a pure
    # network flake, not a real agent/content failure. Previously not retried
    # at all: hard-failed on the first occurrence with zero retry attempts.
    sleeps = []
    monkeypatch.setattr(sse_mod.time, "sleep", lambda s: sleeps.append(s))
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        if calls["n"] < 3:
            raise httpx.RemoteProtocolError("peer closed connection without sending complete message body")
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


def test_create_conversation_omits_agent_id_by_default():
    # No agent_id given -> unchanged, existing behavior: GoodData's own
    # last-used/last-edited default-agent resolution still applies.
    seen = {}

    def handler(request):
        seen["body"] = request.content
        return httpx.Response(200, json={"conversationId": "abc"})

    client = _client_with_handler(handler)
    client.create_conversation()
    assert seen["body"] in (b"", b"{}")


def test_create_conversation_sends_agent_id_when_given():
    seen = {}

    def handler(request):
        seen["body"] = json.loads(request.content)
        return httpx.Response(200, json={"conversationId": "abc"})

    client = _client_with_handler(handler, agent_id="agent-123")
    client.create_conversation()
    assert seen["body"] == {"agentId": "agent-123"}


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


def test_parse_sse_lines_captures_response_id_from_event_data():
    """response_id is captured from the top-level event_data."""
    lines = [
        'data: {"responseId": "resp-123", "item": {"role": "assistant", "content": {"type": "text", "text": "hi"}}}',
    ]
    result = parse_sse_lines(lines)
    assert result.response_id == "resp-123"


def test_parse_sse_lines_captures_response_id_from_item():
    """response_id is captured from item when not present at top level."""
    lines = [
        'data: {"item": {"role": "assistant", "responseId": "resp-456", "content": {"type": "text", "text": "hi"}}}',
    ]
    result = parse_sse_lines(lines)
    assert result.response_id == "resp-456"


def test_parse_sse_lines_first_response_id_wins():
    """Only the first responseId encountered is kept."""
    lines = [
        'data: {"responseId": "first", "item": {"role": "assistant", "content": {"type": "text", "text": "a"}}}',
        'data: {"responseId": "second", "item": {"role": "assistant", "content": {"type": "text", "text": "b"}}}',
    ]
    result = parse_sse_lines(lines)
    assert result.response_id == "first"


def test_ask_attaches_conversation_id_to_result(monkeypatch):
    """ChatClient.ask() sets conversation_id on the returned ChatResult."""
    calls = []

    def handler(request):
        if request.method == "POST" and request.url.path.endswith("/conversations"):
            return httpx.Response(200, json={"conversationId": "conv-abc"})
        if request.method == "POST" and "messages" in str(request.url):
            return httpx.Response(200, content=_OK_SSE)
        if request.method == "DELETE":
            calls.append("delete")
            return httpx.Response(204)
        return httpx.Response(404)

    client = _client_with_handler(handler)
    item = DatasetItem(id="t1", dataset_name="d", test_kind="visualization", question="q", expected_output={})
    result = client.ask(item)
    assert result.conversation_id == "conv-abc"
    assert "delete" in calls  # conversation cleaned up on success


def test_ask_preserve_failed_keeps_conversation_on_error(monkeypatch):
    """With preserve_failed=True, failed conversations are not deleted."""
    calls = []

    def handler(request):
        if request.method == "POST" and request.url.path.endswith("/conversations"):
            return httpx.Response(200, json={"conversationId": "conv-fail"})
        if request.method == "POST" and "messages" in str(request.url):
            return httpx.Response(200, content=_NONRETRY_SSE)
        if request.method == "DELETE":
            calls.append("delete")
            return httpx.Response(204)
        return httpx.Response(404)

    monkeypatch.setattr(sse_mod.time, "sleep", lambda s: None)
    client = ChatClient(host="https://example.invalid", token="t", workspace_id="w", preserve_failed=True)
    client._client = httpx.Client(transport=httpx.MockTransport(handler))

    item = DatasetItem(id="t1", dataset_name="d", test_kind="visualization", question="q", expected_output={})
    with pytest.raises(ChatError):
        client.ask(item)
    assert "delete" not in calls  # conversation preserved


def test_ask_without_preserve_failed_deletes_on_error(monkeypatch):
    """Without preserve_failed, conversations are deleted even on error."""
    calls = []

    def handler(request):
        if request.method == "POST" and request.url.path.endswith("/conversations"):
            return httpx.Response(200, json={"conversationId": "conv-del"})
        if request.method == "POST" and "messages" in str(request.url):
            return httpx.Response(200, content=_NONRETRY_SSE)
        if request.method == "DELETE":
            calls.append("delete")
            return httpx.Response(204)
        return httpx.Response(404)

    monkeypatch.setattr(sse_mod.time, "sleep", lambda s: None)
    client = _client_with_handler(handler)

    item = DatasetItem(id="t1", dataset_name="d", test_kind="visualization", question="q", expected_output={})
    with pytest.raises(ChatError):
        client.ask(item)
    assert "delete" in calls  # conversation deleted


def test_ask_attaches_conversation_id_to_exception(monkeypatch):
    """On failure, conversation_id is attached to the raised exception."""

    def handler(request):
        if request.method == "POST" and request.url.path.endswith("/conversations"):
            return httpx.Response(200, json={"conversationId": "conv-exc"})
        if request.method == "POST" and "messages" in str(request.url):
            return httpx.Response(200, content=_NONRETRY_SSE)
        if request.method == "DELETE":
            return httpx.Response(204)
        return httpx.Response(404)

    monkeypatch.setattr(sse_mod.time, "sleep", lambda s: None)
    client = _client_with_handler(handler)

    item = DatasetItem(id="t1", dataset_name="d", test_kind="visualization", question="q", expected_output={})
    with pytest.raises(ChatError) as ei:
        client.ask(item)
    assert ei.value.conversation_id == "conv-exc"


def _capture_body_client(captured, *, reasoning_effort=None):
    def handler(request):
        captured.append(json.loads(request.content))
        return httpx.Response(200, content=_OK_SSE)

    client = ChatClient(host="https://example.invalid", token="t", workspace_id="w", reasoning_effort=reasoning_effort)
    client._client = httpx.Client(transport=httpx.MockTransport(handler))
    return client


def test_send_message_omits_options_when_no_reasoning_effort():
    """Default must stay byte-identical to the pre-feature payload."""
    captured = []
    _capture_body_client(captured).send_message("conv", "q")
    assert captured == [{"item": {"role": "user", "content": {"type": "text", "text": "q"}}}]


@pytest.mark.parametrize("effort", ["LOW", "MEDIUM", "HIGH"])
def test_send_message_sends_reasoning_effort(effort):
    captured = []
    _capture_body_client(captured, reasoning_effort=effort).send_message("conv", "q")
    assert captured[0]["options"] == {"reasoningEffort": effort}
    assert captured[0]["item"]["content"]["text"] == "q"


def test_reasoning_effort_applies_to_every_message_in_a_conversation():
    """Multi-turn evaluators call send_message repeatedly on one client."""
    captured = []
    client = _capture_body_client(captured, reasoning_effort="LOW")
    client.send_message("conv", "first")
    client.send_message("conv", "follow-up")
    assert [c["options"] for c in captured] == [{"reasoningEffort": "LOW"}] * 2


def test_ask_propagates_reasoning_effort():
    """ask() creates, sends and deletes — the effort must survive that whole path."""
    captured = []

    def handler(request):
        if request.method == "POST" and request.url.path.endswith("/conversations"):
            return httpx.Response(201, json={"conversationId": "c1"})
        if request.method == "POST":
            captured.append(json.loads(request.content))
            return httpx.Response(200, content=_OK_SSE)
        return httpx.Response(204)

    client = _client_with_handler(handler, reasoning_effort="HIGH")
    item = DatasetItem(id="t1", dataset_name="d", test_kind="visualization", question="q", expected_output={})
    client.ask(item)
    assert captured[0]["options"] == {"reasoningEffort": "HIGH"}


@pytest.mark.parametrize(("given", "sent"), [("low", "LOW"), ("  High  ", "HIGH"), ("MEDIUM", "MEDIUM")])
def test_send_message_normalizes_reasoning_effort(given, sent):
    """The endpoint enum is uppercase, so casing is canonicalized before the request."""
    captured = []
    _capture_body_client(captured, reasoning_effort=given).send_message("conv", "q")
    assert captured[0]["options"] == {"reasoningEffort": sent}


@pytest.mark.parametrize("blank", ["", "   "])
def test_blank_reasoning_effort_is_treated_as_unset(blank):
    """Previously a blank value was sent but skipped by the Langfuse writers, so the
    request and the recorded run disagreed. It now means 'unset' on both paths."""
    captured = []
    _capture_body_client(captured, reasoning_effort=blank).send_message("conv", "q")
    assert "options" not in captured[0]


def test_invalid_reasoning_effort_fails_at_construction():
    """Fail locally rather than as an out-of-enum request partway through a run."""
    with pytest.raises(ValueError, match="Invalid reasoning effort"):
        ChatClient(host="https://example.invalid", token="t", workspace_id="w", reasoning_effort="maximum")


_ATTACHMENT = {"referencedObjects": [{"objects": [{"type": "WIDGET", "id": "campaign_spend"}]}]}


def _capture_body(store):
    def handler(request):
        store["body"] = json.loads(request.read())
        return httpx.Response(200, content=_OK_SSE)

    return handler


def test_send_message_puts_the_user_context_on_the_wire():
    captured = {}
    client = _client_with_handler(_capture_body(captured))
    client.send_message("conv", "q", user_context=_ATTACHMENT)
    assert captured["body"]["userContext"] == _ATTACHMENT


def test_send_message_omits_user_context_entirely_when_there_is_no_attachment():
    """An explicit ``"userContext": null`` would be ACCEPTED by gen-ai, so a sloppy
    unconditional assignment would silently alter every request in every existing dataset
    rather than failing loudly. This is the guard against that."""
    captured = {}
    client = _client_with_handler(_capture_body(captured))
    client.send_message("conv", "q")
    assert "userContext" not in captured["body"]

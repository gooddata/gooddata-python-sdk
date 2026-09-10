# (C) 2026 GoodData Corporation
from gooddata_eval.core.models import (
    ChatResult,
    CreatedVisualization,
    DatasetItem,
    ReasoningStepEvent,
    ToolCallEvent,
    build_tool_calls,
    timeline_detail,
)


def test_created_visualization_parses_aac_shape():
    viz = CreatedVisualization.model_validate(
        {
            "id": "rev_by_q",
            "type": "column_chart",
            "title": "Revenue by Quarter",
            "query": {
                "fields": {
                    "m_rev": {"using": "metric/revenue"},
                    "d_q": {"using": "label/date.quarter"},
                },
                "filter_by": {},
            },
            "metrics": ["m_rev"],
            "view_by": ["d_q"],
            "segment_by": [],
            "rows": [],
            "columns": [],
        }
    )
    assert viz.type == "column_chart"
    assert viz.query.fields["m_rev"].using == "metric/revenue"
    assert viz.metrics == ["m_rev"]


def test_chat_result_parses_camelcase_with_created_visualizations():
    result = ChatResult.model_validate(
        {
            "textResponse": "Here you go",
            "createdVisualizations": {
                "objects": [{"id": "v1", "type": "table", "query": {"fields": {}, "filter_by": {}}}],
                "reasoning": "because",
            },
            "toolCallEvents": [],
        }
    )
    assert result.text_response == "Here you go"
    assert result.created_visualizations is not None
    assert result.created_visualizations.objects[0].id == "v1"


def test_dataset_item_keeps_raw_expected_output():
    item = DatasetItem.model_validate(
        {
            "id": "vis-001",
            "dataset_name": "d1",
            "test_kind": "visualization",
            "question": "Show revenue",
            "expected_output": {"visualization": {"id": "x", "type": "", "query": {"fields": {}}}},
        }
    )
    assert item.test_kind == "visualization"
    assert item.expected_output["visualization"]["id"] == "x"


def test_tool_call_event_parsed_arguments():
    ev = ToolCallEvent.model_validate(
        {"functionName": "search_objects", "functionArguments": '{"keywords": ["revenue"], "limit": 10}'}
    )
    assert ev.parsed_arguments() == {"keywords": ["revenue"], "limit": 10}


def test_tool_call_event_parsed_arguments_empty():
    ev = ToolCallEvent.model_validate({"functionName": "f", "functionArguments": ""})
    assert ev.parsed_arguments() == {}


def test_tool_call_event_parsed_result_none_when_absent():
    ev = ToolCallEvent.model_validate({"functionName": "f", "functionArguments": "{}", "result": None})
    assert ev.parsed_result() is None


def test_tool_call_event_parsed_result_parses_json():
    ev = ToolCallEvent.model_validate(
        {
            "functionName": "create_metric",
            "functionArguments": "{}",
            "result": '{"data": {"maql": "SELECT {metric/a}", "format": "#,##0"}}',
        }
    )
    assert ev.parsed_result() == {"data": {"maql": "SELECT {metric/a}", "format": "#,##0"}}


def _tc(name: str, args: str, result: str | None, index: int | None, call_ts=0.0, result_ts=1.0) -> ToolCallEvent:
    return ToolCallEvent.model_validate(
        {
            "functionName": name,
            "functionArguments": args,
            "result": result,
            "call_ts": call_ts,
            "result_ts": result_ts,
            "index": index,
        }
    )


def test_build_tool_calls_keeps_args_and_result_keyed_by_index():
    calls = build_tool_calls([_tc("search_metrics", '{"q": "revenue"}', '{"hits": 3}', 0)])

    assert calls == [{"index": 0, "name": "search_metrics", "arguments": {"q": "revenue"}, "result": '{"hits": 3}'}]


def test_build_tool_calls_skips_events_without_an_index():
    # Nothing can join to them, and guessing a position would attribute the wrong args.
    assert build_tool_calls([_tc("f", "{}", "ok", None)]) == []


def test_build_tool_calls_clips_a_huge_result():
    call = build_tool_calls([_tc("run_query", "{}", "x" * 5000, 0)])[0]

    assert len(call["result"]) < 5000
    assert "clipped, 5000 chars total" in call["result"]


def test_build_tool_calls_keeps_unparseable_arguments_as_text():
    assert build_tool_calls([_tc("f", "not json", None, 0)])[0]["arguments"] == "not json"


def test_timeline_detail_indexes_line_up_with_the_breakdown():
    events = [_tc("search_metrics", "{}", "ok", 0, 0.0, 1.0), _tc("create_visualization", "{}", "ok", 1, 1.0, 4.0)]
    detail = timeline_detail(events, [ReasoningStepEvent(summary="**Planning**\n\ntext", ts=0.5, index=0)])

    # Every tool step in the timeline must resolve to a real tool_calls entry by index --
    # that join is the whole reason the breakdown only carries a name.
    by_index = {c["index"]: c for c in detail["tool_calls"]}
    tool_steps = [s for s in detail["latency_breakdown"] if s["kind"] == "tool"]
    assert tool_steps
    assert all(by_index[s["index"]]["name"] == s["name"] for s in tool_steps)


def test_dataset_item_carries_a_user_context_attachment():
    item = DatasetItem.model_validate(
        {
            "id": "gdai-2179-001",
            "dataset_name": "GDAI-2179",
            "test_kind": "agentic_general_question",
            "question": "What does the visualization I attached show?",
            "expected_output": "Describes the attached chart.",
            "user_context": {"referencedObjects": [{"objects": [{"type": "WIDGET", "id": "campaign_spend"}]}]},
        }
    )
    assert item.user_context == {"referencedObjects": [{"objects": [{"type": "WIDGET", "id": "campaign_spend"}]}]}


def test_dataset_item_user_context_defaults_to_none():
    item = DatasetItem.model_validate(
        {
            "id": "q1",
            "dataset_name": "d1",
            "test_kind": "agentic_general_question",
            "question": "What can you do?",
            "expected_output": "Describes capabilities.",
        }
    )
    assert item.user_context is None

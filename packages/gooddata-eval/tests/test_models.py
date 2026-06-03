# (C) 2026 GoodData Corporation
from gooddata_eval.core.models import (
    ChatResult,
    CreatedVisualization,
    DatasetItem,
    ToolCallEvent,
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

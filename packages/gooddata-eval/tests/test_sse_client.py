# (C) 2026 GoodData Corporation
import json

import pytest
from gooddata_eval.core.chat.sse_client import parse_sse_lines


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

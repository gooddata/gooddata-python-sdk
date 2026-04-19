# (C) 2026 GoodData Corporation
from __future__ import annotations

import pytest
from gooddata_sdk.compute.model.chat import ToolCallEventResult


@pytest.mark.parametrize(
    "scenario, input_data, expected_snake",
    [
        (
            "basic",
            {
                "functionArguments": '{"x": 1}',
                "functionName": "get_revenue",
                "result": "42",
            },
            {
                "function_arguments": '{"x": 1}',
                "function_name": "get_revenue",
                "result": "42",
            },
        ),
        (
            "empty_strings",
            {
                "functionArguments": "",
                "functionName": "noop",
                "result": "",
            },
            {
                "function_arguments": "",
                "function_name": "noop",
                "result": "",
            },
        ),
    ],
)
def test_tool_call_event_result_from_dict(scenario, input_data, expected_snake):
    """Verify ToolCallEventResult round-trips through from_dict / to_dict."""
    model = ToolCallEventResult.from_dict(input_data)

    assert model.function_arguments == expected_snake["function_arguments"]
    assert model.function_name == expected_snake["function_name"]
    assert model.result == expected_snake["result"]

    # Round-trip back to camelCase dict
    as_dict = model.to_dict(camel_case=True)
    assert as_dict["functionArguments"] == expected_snake["function_arguments"]
    assert as_dict["functionName"] == expected_snake["function_name"]
    assert as_dict["result"] == expected_snake["result"]


def test_tool_call_event_result_construction():
    """Verify direct construction and attribute access."""
    evt = ToolCallEventResult(
        function_arguments='{"threshold": 0.5}',
        function_name="filter_results",
        result="filtered",
    )
    assert evt.function_arguments == '{"threshold": 0.5}'
    assert evt.function_name == "filter_results"
    assert evt.result == "filtered"


def test_tool_call_event_result_client_class():
    """Verify client_class() returns the generated API model class."""
    from gooddata_api_client.model.tool_call_event_result import ToolCallEventResult as ApiToolCallEventResult

    assert ToolCallEventResult.client_class() is ApiToolCallEventResult

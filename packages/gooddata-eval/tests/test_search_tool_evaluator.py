# (C) 2026 GoodData Corporation
import json

from gooddata_eval.core.evaluators import get_evaluator
from gooddata_eval.core.models import ChatResult, DatasetItem


def _item():
    return DatasetItem(
        id="search-001",
        dataset_name="d",
        test_kind="search_tool",
        question="Find dashboards and metrics about revenue.",
        expected_output={
            "tool_call": {
                "function_name": "search_objects",
                "function_arguments": {
                    "keywords": ["revenue"],
                    "object_types": ["dashboard", "metric"],
                    "limit": 10,
                    "emit_widget": True,
                },
            }
        },
    )


def _chat_with_search(args: dict) -> ChatResult:
    return ChatResult.model_validate(
        {"toolCallEvents": [{"functionName": "search_objects", "functionArguments": json.dumps(args), "result": "{}"}]}
    )


def test_search_evaluator_passes_on_exact_match():
    result = get_evaluator("search_tool").evaluate(
        _item(),
        _chat_with_search(
            {
                "keywords": ["revenue"],
                "object_types": ["metric", "dashboard"],
                "limit": 10,
                "emit_widget": True,
            }
        ),
    )
    assert result.passed is True
    assert result.detail["tool_correctness"] is True


def test_search_evaluator_passes_when_tool_called_wrong_args():
    # tool_selection=True -> passed even with wrong args
    result = get_evaluator("search_tool").evaluate(
        _item(),
        _chat_with_search({"keywords": ["WRONG"], "object_types": [], "limit": 5, "emit_widget": False}),
    )
    assert result.passed is True
    assert result.detail["tool_correctness"] is False


def test_search_evaluator_fails_when_tool_not_called():
    result = get_evaluator("search_tool").evaluate(
        _item(),
        ChatResult.model_validate({"textResponse": "here are some results"}),
    )
    assert result.passed is False
    assert result.detail["tool_selection"] is False

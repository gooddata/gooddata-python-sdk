# (C) 2026 GoodData Corporation
"""Tests for the pure helper functions in agentic/conversation.py.

These cover ref-resolution, skill activation, and per-turn output checks used by
the multi-turn conversation runner, independent of any ChatClient.
"""
import pytest

from gooddata_eval.core.agentic.conversation import (
    TurnDefinition,
    _activated_skills,
    _check_output_present,
    _extract_metric_from_turn,
    _is_asking_clarification,
    _resolve_refs,
)
from gooddata_eval.core.models import ChatResult, ToolCallEvent


def _set_skills_event(skills):
    return ToolCallEvent.model_validate(
        {"functionName": "set_skills", "functionArguments": f'{{"skill_names": {skills!r}}}'.replace("'", '"')}
    )


def test_resolve_refs_passthrough_when_no_ref():
    eo = {"maql": "SELECT 1"}
    assert _resolve_refs(eo, {}) == eo
    assert _resolve_refs(None, {}) is None


def test_resolve_refs_substitutes_prior_turn_output():
    eo = {"metric_id": "$ref:t0.id"}
    resolved = _resolve_refs(eo, {"t0": {"id": "metric-123"}})
    assert resolved == {"metric_id": "metric-123"}


def test_resolve_refs_raises_on_missing_turn():
    with pytest.raises(ValueError, match="has no captured output"):
        _resolve_refs({"x": "$ref:tX.id"}, {"t0": {"id": "m"}})


def test_resolve_refs_raises_on_missing_field():
    with pytest.raises(ValueError, match="not found in turn"):
        _resolve_refs({"x": "$ref:t0.missing"}, {"t0": {"id": "m"}})


def test_activated_skills_dedupes_across_events():
    events = [_set_skills_event(["visualization"]), _set_skills_event(["visualization", "metric"])]
    assert sorted(_activated_skills(events)) == ["metric", "visualization"]
    assert _activated_skills([]) == []


def test_check_output_present_visualization():
    turn = TurnDefinition(turn_id="t", message="m", expected_skill="viz", expected_output_type="visualization")
    present = ChatResult.model_validate(
        {"createdVisualizations": {"objects": [{"id": "v", "type": "table", "query": {"fields": {}, "filter_by": {}}}]}}
    )
    absent = ChatResult.model_validate({"textResponse": "no viz"})
    assert _check_output_present(turn, present) is True
    assert _check_output_present(turn, absent) is False


def test_check_output_present_metric_and_tool_call():
    metric_turn = TurnDefinition(turn_id="t", message="m", expected_skill="metric", expected_output_type="metric")
    metric_chat = ChatResult.model_validate(
        {"toolCallEvents": [{"functionName": "create_metric", "functionArguments": "{}"}]}
    )
    assert _check_output_present(metric_turn, metric_chat) is True

    tool_turn = TurnDefinition(
        turn_id="t",
        message="m",
        expected_skill="search",
        expected_output_type="tool_call",
        expected_tool_name="search_objects",
    )
    tool_chat = ChatResult.model_validate(
        {"toolCallEvents": [{"functionName": "search_objects", "functionArguments": "{}"}]}
    )
    assert _check_output_present(tool_turn, tool_chat) is True
    assert _check_output_present(tool_turn, metric_chat) is False  # wrong tool


def test_extract_metric_from_turn():
    import json

    events = [
        ToolCallEvent.model_validate(
            {
                "functionName": "create_metric",
                "functionArguments": "{}",
                "result": json.dumps({"data": {"maql": "SELECT 1"}}),
            }
        )
    ]
    assert _extract_metric_from_turn(events) == {"maql": "SELECT 1"}
    assert _extract_metric_from_turn([]) is None


def test_is_asking_clarification():
    # genuine clarification — response ends with a question mark
    assert _is_asking_clarification("Which metric?") is True
    assert _is_asking_clarification("Could you clarify which dimension to use?") is True
    assert _is_asking_clarification("I need more info.\nWhich time period should I use?") is True

    # false positives the old heuristic fired on
    assert _is_asking_clarification("Please clarify") is False        # no trailing "?"
    assert _is_asking_clarification("I'll create the metric now, please wait.") is False
    assert _is_asking_clarification("Here is your chart! Let me know if you need changes.") is False

    # unambiguous non-questions
    assert _is_asking_clarification("") is False
    assert _is_asking_clarification("All set.") is False

# (C) 2026 GoodData Corporation
"""Unit tests for the agentic visualization runner.

All tests mock ChatClient so no network is needed.
"""
from dataclasses import dataclass
from unittest.mock import MagicMock, call, patch

import pytest

from gooddata_eval.core.agentic.visualization import (
    AgenticRunSummary,
    RunResult,
    _execute_single_run,
    run_agentic_visualization,
)
from gooddata_eval.core.models import ChatResult, CreatedVisualization


def _viz(id_: str = "v1") -> dict:
    return {
        "id": id_,
        "type": "column_chart",
        "query": {
            "fields": {"m": {"using": "metric/revenue"}, "d": {"using": "label/date.quarter"}},
            "filter_by": {},
        },
        "metrics": ["m"],
        "view_by": ["d"],
    }


def _expected() -> CreatedVisualization:
    return CreatedVisualization.model_validate(_viz())


def _chat_with_viz() -> ChatResult:
    return ChatResult.model_validate({
        "createdVisualizations": {"objects": [_viz()], "reasoning": ""},
        "toolCallEvents": [
            {"functionName": "set_skills", "functionArguments": '{"skill_names": ["visualization"]}', "result": None}
        ],
        "reasoningStepCount": 2,
    })


def _chat_clarification(text: str = "Which metrics?") -> ChatResult:
    return ChatResult.model_validate({
        "textResponse": text,
        "toolCallEvents": [],
        "reasoningStepCount": 1,
    })


# ── _execute_single_run ─────────────────────────────────────────────────────


def test_execute_single_run_viz_on_first_turn():
    """Agent returns a visualization immediately — one turn, no clarification."""
    client = MagicMock()
    client.send_message.return_value = _chat_with_viz()

    result = _execute_single_run(client, "conv-1", "Show revenue", [_expected()])

    assert result.eval_result.visualization_created is True
    assert result.eval_result.strict_pass is True
    assert result.total_turns == 1.0
    assert result.total_steps == 2.0
    assert result.conversation_id == "conv-1"
    client.send_message.assert_called_once_with("conv-1", "Show revenue")


def test_execute_single_run_clarification_then_viz(monkeypatch):
    """Agent asks a clarification question, simulated user replies, then viz arrives."""
    client = MagicMock()
    client.send_message.side_effect = [
        _chat_clarification("Which metrics?"),
        _chat_with_viz(),
    ]

    monkeypatch.setattr(
        "gooddata_eval.core.agentic.visualization.generate_simulated_response",
        lambda msg, exp: "Revenue please",
    )

    result = _execute_single_run(client, "conv-1", "Show me a chart", [_expected()])

    assert result.eval_result.visualization_created is True
    assert result.total_turns == 2.0
    assert client.send_message.call_count == 2
    assert client.send_message.call_args_list[1] == call("conv-1", "Revenue please")


def test_execute_single_run_no_viz_no_text():
    """Agent returns nothing — visualization_created is False."""
    client = MagicMock()
    client.send_message.return_value = ChatResult.model_validate({
        "toolCallEvents": [],
        "reasoningStepCount": 0,
    })

    result = _execute_single_run(client, "conv-1", "Show revenue", [_expected()])

    assert result.eval_result.visualization_created is False
    assert result.total_turns == 1.0


def test_execute_single_run_max_iterations_stops_loop(monkeypatch):
    """Loop stops at max_iterations even if agent keeps asking clarifications."""
    client = MagicMock()
    client.send_message.return_value = _chat_clarification("Again?")

    monkeypatch.setattr(
        "gooddata_eval.core.agentic.visualization.generate_simulated_response",
        lambda msg, exp: "reply",
    )

    result = _execute_single_run(client, "conv-1", "Q", [_expected()], max_iterations=3)

    assert result.eval_result.visualization_created is False
    assert client.send_message.call_count == 3  # initial + 2 follow-ups (stops before 4th send)


# ── run_agentic_visualization ───────────────────────────────────────────────


def test_run_agentic_visualization_uses_initial_conversation_for_run_0():
    """Run 0 must use the caller-supplied conversation ID, not create a new one."""
    with patch("gooddata_eval.core.agentic.visualization.ChatClient") as MockClient:
        instance = MockClient.return_value
        instance.send_message.return_value = _chat_with_viz()

        summary = run_agentic_visualization(
            host="https://example.com",
            token="tok",
            workspace_id="ws",
            question="Show revenue",
            expected_outputs=[_expected()],
            k=1,
            initial_conversation_id="existing-conv",
        )

    # create_conversation should NOT be called for run 0
    instance.create_conversation.assert_not_called()
    instance.send_message.assert_called_once_with("existing-conv", "Show revenue")
    instance.delete_conversation.assert_called_once_with("existing-conv")
    assert len(summary.run_results) == 1


def test_run_agentic_visualization_creates_fresh_conversations_for_remaining_runs():
    """Runs 1..K-1 must each get a fresh conversation created by the client."""
    with patch("gooddata_eval.core.agentic.visualization.ChatClient") as MockClient:
        instance = MockClient.return_value
        instance.create_conversation.side_effect = ["fresh-1"]
        instance.send_message.return_value = _chat_with_viz()

        summary = run_agentic_visualization(
            host="https://example.com",
            token="tok",
            workspace_id="ws",
            question="Show revenue",
            expected_outputs=[_expected()],
            k=2,
            initial_conversation_id="existing-conv",
        )

    assert instance.create_conversation.call_count == 1  # only for run 1
    assert instance.delete_conversation.call_count == 2  # existing-conv + fresh-1
    assert len(summary.run_results) == 2


def test_run_agentic_visualization_pass_at_k_true_when_any_run_passes():
    """pass_at_k is True when at least one run achieves strict_pass."""
    with patch("gooddata_eval.core.agentic.visualization.ChatClient") as MockClient:
        instance = MockClient.return_value
        # Run 0: no viz (fail). Run 1: viz (pass).
        instance.create_conversation.return_value = "fresh"
        instance.send_message.side_effect = [
            ChatResult.model_validate({"toolCallEvents": [], "reasoningStepCount": 0}),  # run 0: no viz
            _chat_with_viz(),  # run 1: pass
        ]

        summary = run_agentic_visualization(
            host="https://example.com",
            token="tok",
            workspace_id="ws",
            question="Q",
            expected_outputs=[_expected()],
            k=2,
            initial_conversation_id="conv-0",
        )

    assert summary.pass_at_k is True
    assert summary.pass_power_k is False


def test_run_agentic_visualization_pass_power_k_true_when_all_runs_pass():
    """pass_power_k is True only when all K runs achieve strict_pass."""
    with patch("gooddata_eval.core.agentic.visualization.ChatClient") as MockClient:
        instance = MockClient.return_value
        instance.create_conversation.return_value = "fresh"
        instance.send_message.return_value = _chat_with_viz()

        summary = run_agentic_visualization(
            host="https://example.com",
            token="tok",
            workspace_id="ws",
            question="Q",
            expected_outputs=[_expected()],
            k=2,
            initial_conversation_id="conv-0",
        )

    assert summary.pass_at_k is True
    assert summary.pass_power_k is True


def test_run_agentic_visualization_creates_conversation_when_no_initial_id():
    """When initial_conversation_id is None, a fresh conversation is created for run 0 too."""
    with patch("gooddata_eval.core.agentic.visualization.ChatClient") as MockClient:
        instance = MockClient.return_value
        instance.create_conversation.side_effect = ["new-0", "new-1"]
        instance.send_message.return_value = _chat_with_viz()

        summary = run_agentic_visualization(
            host="https://example.com",
            token="tok",
            workspace_id="ws",
            question="Q",
            expected_outputs=[_expected()],
            k=2,
        )

    assert instance.create_conversation.call_count == 2
    assert instance.delete_conversation.call_count == 2

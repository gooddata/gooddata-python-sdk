# (C) 2026 GoodData Corporation
"""Unit tests for the agentic visualization runner.

All tests mock ChatClient so no network is needed.
"""

from collections.abc import Callable
from dataclasses import replace
from typing import Any
from unittest.mock import MagicMock, call, patch

import pytest
from gooddata_eval.core.agentic import visualization as agentic_visualization
from gooddata_eval.core.agentic.visualization import (
    VisualizationAssertionError,
    _execute_single_run,
    _strict_checks,
    evaluate_agentic_visualization,
    run_agentic_visualization,
)
from gooddata_eval.core.chat.sse_client import ChatError
from gooddata_eval.core.evaluators.visualization import ExpectationOptions
from gooddata_eval.core.models import ChatResult, CreatedVisualization, LoopExit


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
    return ChatResult.model_validate(
        {
            "createdVisualizations": {"objects": [_viz()], "reasoning": ""},
            "toolCallEvents": [
                {
                    "functionName": "set_skills",
                    "functionArguments": '{"skill_names": ["visualization"]}',
                    "result": None,
                }
            ],
            "reasoningStepCount": 2,
        }
    )


def _chat_clarification(text: str = "Which metrics?") -> ChatResult:
    return ChatResult.model_validate(
        {
            "textResponse": text,
            "toolCallEvents": [],
            "reasoningStepCount": 1,
        }
    )


# ── _execute_single_run ─────────────────────────────────────────────────────


def test_execute_single_run_viz_on_first_turn():
    """Agent returns a visualization immediately — one turn, no clarification."""
    client = MagicMock()
    client.send_message.return_value = _chat_with_viz()

    result = _execute_single_run(client, "conv-1", "Show revenue", [_expected()])

    assert result.eval_result.visualization_created is True
    assert result.eval_result.strict_pass is True
    assert result.total_turns == 1
    assert result.total_steps == 2
    assert result.conversation_id == "conv-1"
    client.send_message.assert_called_once_with("conv-1", "Show revenue")


def test_execute_single_run_fails_an_unrun_chart_when_execution_is_required():
    client = MagicMock()
    client.send_message.return_value = _chat_with_viz()

    result = _execute_single_run(client, "conv-1", "What is revenue?", [_expected()], requires_execution=True)

    assert result.eval_result.visualization_created is True
    assert result.eval_result.executed is False
    assert result.eval_result.strict_pass is False


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
    assert result.total_turns == 2
    assert client.send_message.call_count == 2
    assert client.send_message.call_args_list[1] == call("conv-1", "Revenue please")


def test_execute_single_run_no_viz_no_text():
    """Agent returns nothing — visualization_created is False."""
    client = MagicMock()
    client.send_message.return_value = ChatResult.model_validate(
        {
            "toolCallEvents": [],
            "reasoningStepCount": 0,
        }
    )

    result = _execute_single_run(client, "conv-1", "Show revenue", [_expected()])

    assert result.eval_result.visualization_created is False
    assert result.total_turns == 1


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
    # the caller-supplied conversation is left intact; the function only deletes conversations it created
    instance.delete_conversation.assert_not_called()
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
    # only the self-created fresh-1 is deleted; the caller-supplied existing-conv is left intact
    instance.delete_conversation.assert_called_once_with("fresh-1")
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

        run_agentic_visualization(
            host="https://example.com",
            token="tok",
            workspace_id="ws",
            question="Q",
            expected_outputs=[_expected()],
            k=2,
        )

    assert instance.create_conversation.call_count == 2
    assert instance.delete_conversation.call_count == 2


def test_execute_single_run_accumulates_reasoning_steps_across_iterations(monkeypatch):
    """Reasoning steps from every turn (clarification + final) are accumulated, not just the last."""
    client = MagicMock()
    clarify = ChatResult.model_validate(
        {
            "textResponse": "Which metrics?",
            "toolCallEvents": [],
            "reasoningSteps": ["step one"],
            "responseId": "resp-1",
        }
    )
    final = ChatResult.model_validate(
        {
            "createdVisualizations": {"objects": [_viz()], "reasoning": ""},
            "toolCallEvents": [],
            "reasoningSteps": ["step two"],
            "responseId": "resp-2",
        }
    )
    client.send_message.side_effect = [clarify, final]
    monkeypatch.setattr(
        "gooddata_eval.core.agentic.visualization.generate_simulated_response",
        lambda msg, exp: "Revenue please",
    )

    result = _execute_single_run(client, "conv-1", "Show me a chart", [_expected()])

    assert result.reasoning_steps == ["step one", "step two"]
    assert result.response_id == "resp-2"


def test_evaluate_agentic_visualization_returns_reasoning_steps_on_pass():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "createdVisualizations": {"objects": [_viz()], "reasoning": ""},
            "toolCallEvents": [],
            "reasoningSteps": ["building the chart"],
            "responseId": "resp-1",
        }
    )

    with patch("gooddata_eval.core.agentic.visualization.ChatClient", return_value=mock_client):
        outcome = evaluate_agentic_visualization(
            host="https://example.com",
            token="tok",
            workspace_id="ws",
            question="Show revenue",
            expected_outputs=[_expected()],
            k=1,
        )

    assert outcome.reasoning_steps == ["building the chart"]
    assert outcome.conversation_id == "conv-1"
    assert outcome.response_id == "resp-1"
    assert outcome.detail == {
        "visualization_created": True,
        "cross_ref_valid": True,
        "cross_ref_errors": [],
        "metrics_correct": True,
        "dimensions_correct": True,
        "filters_correct": True,
        "sorts_correct": True,
        "filter_date_score": True,
        "filter_ranking_score": True,
        "filter_attribute_score": True,
        "viz_type_hard": True,
        "skill_activated": False,
        "expected_metric_uris": ["metric/revenue"],
        "actual_metric_uris": ["metric/revenue"],
        "expected_dim_uris": ["label/date.quarter"],
        "actual_dim_uris": ["label/date.quarter"],
        "expected_filters": {"date": [], "ranking": [], "attribute": []},
        "actual_filters": {"date": [], "ranking": [], "attribute": []},
        "exit_reason": "success",
        "turns_used": 1,
        "max_iterations": 4,
        "expected_sorts": [],
        "actual_sorts": [],
        "execution": {"executed": False, "required": False, "stated_value_matches": None},
        "latency_breakdown": [],
        "tool_calls": [],
    }
    # One wall-clock sample per run, passing runs included -- the latency distribution is over
    # these, and a kind that forgot to report them would silently drop out of it.
    assert len(outcome.run_latencies_s) == outcome.runs_effective == 1
    assert all(latency >= 0 for latency in outcome.run_latencies_s)


def test_evaluate_agentic_visualization_attaches_reasoning_steps_to_exception_on_fail():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "I could not build that",
            "toolCallEvents": [],
            "reasoningSteps": ["giving up"],
            "responseId": "resp-2",
        }
    )

    with (
        patch("gooddata_eval.core.agentic.visualization.ChatClient", return_value=mock_client),
        pytest.raises(VisualizationAssertionError) as exc_info,
    ):
        evaluate_agentic_visualization(
            host="https://example.com",
            token="tok",
            workspace_id="ws",
            question="Show revenue",
            expected_outputs=[_expected()],
            k=1,
            max_iterations=1,
        )

    assert exc_info.value.reasoning_steps == ["giving up"]
    assert exc_info.value.conversation_id == "conv-1"
    assert exc_info.value.response_id == "resp-2"
    assert exc_info.value.detail == {
        "visualization_created": False,
        "cross_ref_valid": False,
        "cross_ref_errors": ["No visualization was created"],
        "metrics_correct": False,
        "dimensions_correct": False,
        "filters_correct": False,
        "sorts_correct": False,
        "filter_date_score": False,
        "filter_ranking_score": False,
        "filter_attribute_score": False,
        "viz_type_hard": False,
        "skill_activated": False,
        "expected_metric_uris": ["metric/revenue"],
        "actual_metric_uris": [],
        "expected_dim_uris": ["label/date.quarter"],
        "actual_dim_uris": [],
        "expected_filters": {"date": [], "ranking": [], "attribute": []},
        "actual_filters": {"date": [], "ranking": [], "attribute": []},
        # No visualization and only one iteration available: the loop ran out of budget.
        # Every check above reads False, which is exactly why exit_reason has to be here.
        "exit_reason": "budget_exhausted",
        "turns_used": 1,
        "max_iterations": 1,
        "expected_sorts": [],
        "actual_sorts": [],
        "execution": {"executed": False, "required": False, "stated_value_matches": None},
        "latency_breakdown": [],
        "tool_calls": [],
    }
    assert len(exc_info.value.run_latencies_s) == exc_info.value.runs_effective == 1


# --- turns_used counts every send_message, including the pre-loop one ------------------------


@pytest.mark.parametrize("max_iterations", [0, 1, 2, 3])
def test_turns_used_equals_the_number_of_requests_sent(max_iterations):
    """The initial request is sent before the loop, so counting only loop passes undercounts.

    With max_iterations=0 the loop body never runs, yet the agent has already received one
    message -- reporting turns_used=0 there would claim a conversation that did happen never
    did. The agent never produces a visualization here, so no run breaks early and the count
    is driven purely by the budget.
    """
    client = MagicMock()
    client.send_message.return_value = ChatResult.model_validate(
        {"textResponse": "Which metric did you mean?", "createdVisualizations": None}
    )
    expected = [CreatedVisualization.model_validate({"id": "v", "type": "COLUMN", "query": {"fields": {}}})]

    with patch("gooddata_eval.core.agentic.visualization.generate_simulated_response", return_value="the revenue one"):
        run = _execute_single_run(client, "conv-1", "chart revenue", expected, max_iterations=max_iterations)

    assert int(run.total_turns) == client.send_message.call_count
    # A request was sent regardless of the budget, so the count is never zero.
    assert int(run.total_turns) >= 1


# ── chat faults end the run, they do not abort the item ─────────────────────


def test_execute_single_run_records_chat_error_on_the_opening_request():
    """The very first send_message failing leaves no conversation to evaluate.

    It must still return a RunResult rather than raise: raising discards the K-runs already
    completed. The run scores as no-visualization, but exit_reason says infrastructure, not
    a refusal.
    """
    client = MagicMock()
    client.send_message.side_effect = ChatError("gen-ai unavailable")

    result = _execute_single_run(client, "conv-1", "Show revenue", [_expected()])

    assert result.exit_reason is LoopExit.CHAT_ERROR
    assert result.actual_output is None
    assert result.eval_result.visualization_created is False
    # The request was still sent, so it counts -- the same rule the max_iterations=0 case follows.
    assert result.total_turns == 1.0
    # The loop must not run after the opening failure.
    assert client.send_message.call_count == 1


def test_execute_single_run_records_chat_error_on_a_follow_up_request(monkeypatch):
    """A later failure keeps whatever the conversation had already produced."""
    monkeypatch.setattr(
        "gooddata_eval.core.agentic.visualization.generate_simulated_response", lambda *a, **k: "the revenue one"
    )
    client = MagicMock()
    client.send_message.side_effect = [_chat_clarification(), ChatError("stream died")]

    result = _execute_single_run(client, "conv-1", "Show revenue", [_expected()])

    assert result.exit_reason is LoopExit.CHAT_ERROR
    assert client.send_message.call_count == 2


def test_a_partial_result_that_carries_the_chart_counts_its_execution(monkeypatch):
    monkeypatch.setattr(
        "gooddata_eval.core.agentic.visualization.generate_simulated_response", lambda *a, **k: "the revenue one"
    )
    partial = ChatResult.model_validate(
        {
            "createdVisualizations": {"objects": [_viz()], "reasoning": ""},
            "toolCallEvents": [
                {
                    "functionName": "create_adhoc_visualization",
                    "functionArguments": "{}",
                    "result": '{"status":"success","ref":"viz_1"}',
                },
                {
                    "functionName": "execute_visualization",
                    "functionArguments": '{"visualization_ref": "viz_1"}',
                    "result": '{"success":true,"data":{"rows":[]}}',
                },
            ],
        }
    )
    error = ChatError("stream died")
    error.partial_result = partial
    client = MagicMock()
    client.send_message.side_effect = [_chat_clarification(), error]

    result = _execute_single_run(client, "conv-1", "What is revenue?", [_expected()], requires_execution=True)

    assert result.exit_reason is LoopExit.CHAT_ERROR
    assert result.eval_result.executed is True
    assert result.eval_result.strict_pass is True


def test_an_opening_partial_result_that_carries_the_chart_counts_its_execution():
    partial = ChatResult.model_validate(
        {
            "createdVisualizations": {"objects": [_viz()], "reasoning": ""},
            "toolCallEvents": [
                {
                    "functionName": "create_adhoc_visualization",
                    "functionArguments": "{}",
                    "result": '{"status":"success","ref":"viz_1"}',
                },
                {
                    "functionName": "execute_visualization",
                    "functionArguments": '{"visualization_ref": "viz_1"}',
                    "result": '{"success":true,"data":{"rows":[]}}',
                },
            ],
        }
    )
    error = ChatError("stream died")
    error.partial_result = partial
    client = MagicMock()
    client.send_message.side_effect = [error]

    result = _execute_single_run(client, "conv-1", "What is revenue?", [_expected()], requires_execution=True)

    assert result.exit_reason is LoopExit.CHAT_ERROR
    assert result.eval_result.executed is True


def test_execute_single_run_records_simulated_user_failure_separately(monkeypatch):
    """A harness-side fault must not read as the agent failing to produce a chart."""

    def _boom(*_a, **_k):
        raise RuntimeError("openai down")

    monkeypatch.setattr("gooddata_eval.core.agentic.visualization.generate_simulated_response", _boom)
    client = MagicMock()
    client.send_message.return_value = _chat_clarification()

    result = _execute_single_run(client, "conv-1", "Show revenue", [_expected()])

    assert result.exit_reason is LoopExit.SIMULATED_USER_FAILED
    assert result.eval_result.visualization_created is False


def test_an_item_without_a_chart_stops_after_the_first_answer(monkeypatch: pytest.MonkeyPatch) -> None:
    """A simulated reply would answer the agent's question and push it into the chart the item rules out."""
    replies = MagicMock(side_effect=AssertionError("no simulated reply may be sent"))
    monkeypatch.setattr(agentic_visualization, "generate_simulated_response", replies)
    client = MagicMock()
    client.send_message.return_value = _chat_clarification("Which destination should the sankey flow to?")
    options = ExpectationOptions(expects_visualization=False, answer_must_include=("destination",))

    result = _execute_single_run(client, "conv-1", "Create a sankey from Region", [], max_iterations=4, options=options)

    assert client.send_message.call_count == 1
    assert result.exit_reason is LoopExit.SUCCESS
    assert result.best_expected is None
    assert result.eval_result.strict_pass
    assert _strict_checks(result.eval_result) == {"assertion-vis-no-chart": True, "assertion-vis-answer": True}


def test_strict_checks_publish_only_the_options_an_item_asks_for() -> None:
    client = MagicMock()
    client.send_message.return_value = _chat_with_viz()
    plain = _execute_single_run(client, "conv-1", "q", [_expected()], max_iterations=1)
    assert set(_strict_checks(plain.eval_result)) == {
        "assertion-cross-ref-valid",
        "assertion-vis-metric",
        "assertion-vis-dimensions",
        "assertion-vis-filters",
        "assertion-vis-type",
    }
    with_options = replace(
        plain.eval_result,
        requires_execution=True,
        buckets_correct=True,
        format_correct=False,
        part_present=True,
        answer_correct=True,
    )
    assert set(_strict_checks(with_options)) - set(_strict_checks(plain.eval_result)) == {
        "assertion-vis-executed",
        "assertion-vis-buckets",
        "assertion-vis-format",
        "assertion-vis-part-present",
        "assertion-vis-answer",
    }


def test_the_sort_is_scored_only_for_an_item_that_states_one() -> None:
    """strict_pass gates on the sort, so a wrong sort must show in the scores, not only in the gate."""
    sorted_viz = _viz()
    sorted_viz["query"]["sort_by"] = [{"type": "attribute_sort", "by": "d", "direction": "DESC"}]
    client = MagicMock()
    client.send_message.return_value = _chat_with_viz()

    unsorted_item = _execute_single_run(client, "conv-1", "q", [_expected()], max_iterations=1)
    assert "assertion-vis-sort" not in _strict_checks(unsorted_item.eval_result)

    wrong_sort = _execute_single_run(
        client, "conv-1", "q", [CreatedVisualization.model_validate(sorted_viz)], max_iterations=1
    )
    assert wrong_sort.eval_result.strict_pass is False
    assert _strict_checks(wrong_sort.eval_result)["assertion-vis-sort"] is False
    assert not all(_strict_checks(wrong_sort.eval_result).values())

    client.send_message.return_value = ChatResult.model_validate(
        {"createdVisualizations": {"objects": [sorted_viz], "reasoning": ""}, "toolCallEvents": []}
    )
    right_sort = _execute_single_run(
        client, "conv-1", "q", [CreatedVisualization.model_validate(sorted_viz)], max_iterations=1
    )
    assert _strict_checks(right_sort.eval_result)["assertion-vis-sort"] is True


# ── an item that accepts no chart still needs an answer ─────────────────────


def _silent_turn() -> MagicMock:
    client = MagicMock()
    client.send_message.return_value = ChatResult.model_validate({"toolCallEvents": [], "reasoningStepCount": 0})
    return client


def _failed_request() -> MagicMock:
    client = MagicMock()
    client.send_message.side_effect = ChatError("gen-ai unavailable")
    return client


_PROBLEM_OF = {
    LoopExit.AGENT_SILENT: "the agent returned neither a chart nor an answer",
    LoopExit.CHAT_ERROR: "the chat request failed before the answer ended",
}


@pytest.mark.parametrize(
    ("make_client", "exit_reason"),
    [(_silent_turn, LoopExit.AGENT_SILENT), (_failed_request, LoopExit.CHAT_ERROR)],
    ids=["silent", "chat_error"],
)
@pytest.mark.parametrize(
    ("options", "expected_outputs"),
    [
        (ExpectationOptions(expects_visualization=False), []),
        (ExpectationOptions(expects_visualization=False, answer_must_not_match=("sankey",)), []),
        (ExpectationOptions(visualization_optional=True), [_expected()]),
    ],
    ids=["no_chart", "no_chart_must_not_match", "visualization_optional"],
)
def test_a_run_with_neither_a_chart_nor_an_answer_fails_an_item_that_accepts_no_chart(
    make_client: Callable[[], MagicMock],
    exit_reason: LoopExit,
    options: ExpectationOptions,
    expected_outputs: list[CreatedVisualization],
) -> None:
    """With no answer pattern, or only a must-not-match one, an empty run would read as a correct "no chart"."""
    result = _execute_single_run(make_client(), "conv-1", "q", expected_outputs, options=options)

    assert result.exit_reason is exit_reason
    assert result.eval_result.strict_pass is False
    assert result.eval_result.answer_correct is False
    assert result.eval_result.answer_problems[-1] == _PROBLEM_OF[exit_reason]
    assert _strict_checks(result.eval_result)["assertion-vis-answer"] is False


def test_an_answer_without_a_pattern_passes_an_item_without_a_chart() -> None:
    client = MagicMock()
    client.send_message.return_value = _chat_clarification("Which destination?")

    result = _execute_single_run(client, "conv-1", "q", [], options=ExpectationOptions(expects_visualization=False))

    assert result.eval_result.strict_pass is True
    assert result.eval_result.answer_correct is None


@pytest.mark.parametrize(
    ("expected_outputs", "options"),
    [([], None), ([], ExpectationOptions()), ([_expected()], ExpectationOptions(expects_visualization=False))],
    ids=["no_candidates_no_options", "no_candidates_default_options", "candidates_but_no_chart"],
)
def test_run_rejects_candidates_that_disagree_with_the_options_before_any_request(
    expected_outputs: list[CreatedVisualization], options: ExpectationOptions | None
) -> None:
    with (
        patch.object(agentic_visualization, "ChatClient") as mock_client,
        pytest.raises(ValueError, match="expected_outputs must list the candidate charts"),
    ):
        run_agentic_visualization("https://h", "tok", "ws", "q", expected_outputs, options=options)
    mock_client.assert_not_called()


# ── the failure summary and the scores show the options an item asks for ───


def test_a_failed_item_reports_and_scores_every_option_it_asks_for() -> None:
    expected = CreatedVisualization.model_validate({**_viz(), "buckets_strict": True})
    # The same fields, with the quarter moved from view_by to segment_by: only the bucket check sees it.
    moved = {**_viz(), "view_by": [], "segment_by": ["d"]}
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    client.send_message.return_value = ChatResult.model_validate(
        {
            "createdVisualizations": {"objects": [moved], "reasoning": ""},
            "textResponse": "Here it is.",
            "toolCallEvents": [],
        }
    )
    options = ExpectationOptions(
        requires_execution=True,
        answer_must_include=("revenue",),
        format_intents={"metric/revenue": {"divide_by": 1000, "suffix": "K"}},
        requires_visualization_part=True,
    )
    captured: dict[str, Callable[[MagicMock], None]] = {}

    def _capture(_submit: object, _identity: object, **kwargs: Any) -> None:
        captured["write_scores"] = kwargs["write_scores"]

    with (
        patch.object(agentic_visualization, "ChatClient", return_value=client),
        patch.object(agentic_visualization, "submit_trace_scoring", _capture),
        pytest.raises(VisualizationAssertionError) as exc_info,
    ):
        evaluate_agentic_visualization(
            host="https://example.com",
            token="tok",
            workspace_id="ws",
            question="Show revenue",
            expected_outputs=[expected],
            k=1,
            options=options,
            langfuse=MagicMock(),
            dataset_item_id="item-1",
        )

    message = str(exc_info.value)
    assert "Buckets Correct       : False" in message
    assert "expected : {'view_by': ['label/date.quarter']" in message
    assert "Answer Correct        : False" in message
    assert "the answer does not match 'revenue'" in message
    assert "answer   : 'Here it is.'" in message
    assert "Format Correct        : False" in message
    assert "metric/revenue: no format was written" in message
    assert "Part Present          : True" in message
    assert "No Chart" not in message

    ctx = MagicMock()
    captured["write_scores"](ctx)
    scores = [(c.kwargs["name"], c.kwargs["value"]) for c in ctx.score.call_args_list]
    names = [name for name, _ in scores]
    assert dict(scores)["assertion-vis-buckets"] is False
    assert dict(scores)["assertion-vis-format"] is False
    assert dict(scores)["assertion-vis-part-present"] is True
    assert dict(scores)["assertion-vis-answer"] is False
    # Gating here, but still written once: the loop leaves it to the every-item score.
    assert names.count("assertion-vis-executed") == 1


def test_a_failed_item_without_a_chart_reports_the_chart_it_built() -> None:
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    client.send_message.return_value = _chat_with_viz()

    with (
        patch.object(agentic_visualization, "ChatClient", return_value=client),
        pytest.raises(VisualizationAssertionError) as exc_info,
    ):
        evaluate_agentic_visualization(
            host="https://example.com",
            token="tok",
            workspace_id="ws",
            question="Create a sankey from Region",
            expected_outputs=[],
            k=1,
            options=ExpectationOptions(expects_visualization=False),
        )

    message = str(exc_info.value)
    assert "No Chart              : False" in message
    assert '"expects_visualization": false' in message


def test_a_visualization_optional_item_that_built_a_chart_does_not_report_a_no_chart_line() -> None:
    """A chart is a valid outcome there, so a "No Chart : False" line would read as a failed check."""
    client = MagicMock()
    client.send_message.return_value = _chat_with_viz()
    options = ExpectationOptions(visualization_optional=True)
    built = _execute_single_run(client, "conv-1", "q", [_expected()], options=options)
    assert "No Chart" not in agentic_visualization._options_lines(built.eval_result, built.answer_text)

    client.send_message.return_value = _chat_clarification("Which measure should the donut show?")
    asked = _execute_single_run(client, "conv-1", "q", [_expected()], options=options)
    assert "No Chart              : True" in agentic_visualization._options_lines(asked.eval_result, asked.answer_text)


def test_a_failed_request_with_a_cut_off_answer_fails_an_item_without_a_chart() -> None:
    """The partial text is not the agent's answer, so it must not pass as a correct "no chart"."""
    error = ChatError("stream died")
    error.partial_result = ChatResult.model_validate({"textResponse": "Let me"})
    client = MagicMock()
    client.send_message.side_effect = error

    result = _execute_single_run(client, "conv-1", "q", [], options=ExpectationOptions(expects_visualization=False))

    assert result.exit_reason is LoopExit.CHAT_ERROR
    assert result.eval_result.strict_pass is False
    assert result.eval_result.answer_problems == ["the chat request failed before the answer ended"]

# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.agentic.alert_skill import (
    AlertEvaluation,
    AlertSkillAssertionError,
    _check_trigger,
    _deep_subset,
    _normalize_expected_output,
    _to_number,
    evaluate_agentic_alert_skill,
    render_alert_proposal,
    run_agentic_alert_skill,
)
from gooddata_eval.core.models import ChatResult

_PROPOSAL = {
    "title": "# of Orders Alert - Greater Than 500",
    "cta": "Should I create this alert?",
    "recipients": [{"email": "admin@gooddata.com"}],
    "dashboard": {"id": "dash-1", "title": "Orders overview"},
    "alert": {
        "trigger": "ALWAYS",
        "condition": {"comparison": {"operator": "GREATER_THAN", "right": {"value": 500}}},
        "execution": {"measures": [{"opaque": "afm"}]},
    },
}


def test_to_number_int():
    assert _to_number("42") == 42


def test_to_number_float():
    assert abs(_to_number("3.14") - 3.14) < 1e-9


def test_to_number_none():
    assert _to_number("abc") is None


def test_deep_subset_simple():
    assert _deep_subset({"a": 1}, {"a": 1, "b": 2}) is True


def test_deep_subset_missing_key():
    assert _deep_subset({"a": 1, "c": 3}, {"a": 1}) is False


def test_check_trigger_missing_or_null_defaults_to_always():
    # "Every time" is the product default -> the agent may omit the trigger arg
    # entirely, or serialise it as null. Both must count as ALWAYS, not a mismatch.
    expected = _normalize_expected_output({"Operator": "GREATER_THAN", "Trigger": "Every time"})
    assert _check_trigger(expected, {"operator": "GREATER_THAN"}) is True  # key absent
    assert _check_trigger(expected, {"trigger": None}) is True  # present-but-null (the bug)
    assert _check_trigger(expected, {"trigger": "ALWAYS"}) is True


def test_check_trigger_once_needs_explicit_once():
    # A "One time" expectation must still require an explicit ONCE - the null-default
    # fix must not turn a wrong/absent trigger into a pass here.
    expected = _normalize_expected_output({"Operator": "LESS_THAN", "Trigger": "One time"})
    assert _check_trigger(expected, {"trigger": "ONCE"}) is True
    assert _check_trigger(expected, {"trigger": None}) is False  # null != ONCE
    assert _check_trigger(expected, {"trigger": "ONCE_PER_INTERVAL"}) is False  # real model error stays a fail


def test_alert_evaluation_strict_pass():
    ev = AlertEvaluation(
        alert_created=True,
        operator_correct=True,
        threshold_correct=True,
        trigger_correct=True,
        filters_correct=True,
        metric_correct=True,
        recipients_correct=True,
    )
    assert ev.strict_pass is True


def test_alert_evaluation_strict_fail():
    ev = AlertEvaluation(
        alert_created=True,
        operator_correct=False,
        threshold_correct=True,
        trigger_correct=True,
        filters_correct=True,
        metric_correct=True,
        recipients_correct=True,
    )
    assert ev.strict_pass is False


def test_run_agentic_alert_skill_no_alert_created():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "text_response": "I cannot create the alert",
            "created_visualizations": None,
            "tool_call_events": [],
            "reasoning_step_count": 1,
        }
    )
    mock_client._base = "http://host/api/v1/actions/workspaces/ws1/ai"
    mock_client._auth = {"Authorization": "Bearer tok"}

    with patch("gooddata_eval.core.agentic.alert_skill.ChatClient", return_value=mock_client):
        summary = run_agentic_alert_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create alert",
            expected_output={"operator": "GREATER_THAN", "threshold": 100},
            k=1,
            max_iterations=1,
        )

    assert summary.pass_at_k is False
    assert summary.best.eval.alert_created is False
    mock_client.close.assert_called_once()


def test_run_agentic_alert_skill_uses_initial_conversation_for_run_0():
    mock_client = MagicMock()
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "text_response": "I cannot create the alert",
            "created_visualizations": None,
            "tool_call_events": [],
            "reasoning_step_count": 1,
        }
    )
    with patch("gooddata_eval.core.agentic.alert_skill.ChatClient", return_value=mock_client):
        run_agentic_alert_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create alert",
            expected_output={"operator": "GREATER_THAN", "threshold": 100},
            k=1,
            max_iterations=1,
            initial_conversation_id="existing-conv",
        )
    mock_client.create_conversation.assert_not_called()
    mock_client.delete_conversation.assert_not_called()


def test_run_agentic_alert_skill_creates_fresh_conversations_for_remaining_runs():
    mock_client = MagicMock()
    mock_client.create_conversation.side_effect = ["fresh-1", "fresh-2"]
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "text_response": "I cannot create the alert",
            "created_visualizations": None,
            "tool_call_events": [],
            "reasoning_step_count": 1,
        }
    )
    with patch("gooddata_eval.core.agentic.alert_skill.ChatClient", return_value=mock_client):
        run_agentic_alert_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create alert",
            expected_output={"operator": "GREATER_THAN", "threshold": 100},
            k=3,
            max_iterations=1,
            initial_conversation_id="existing-conv",
        )
    assert mock_client.create_conversation.call_count == 2
    assert mock_client.delete_conversation.call_count == 2


def test_render_alert_proposal_keeps_verifiable_fields_and_drops_afm():
    rendered = render_alert_proposal(_PROPOSAL)
    # The CTA leads so the simulated user reads it as a question.
    assert rendered.startswith("Should I create this alert?")
    # Rule 3 of the sim-user prompt requires verifying recipients against its goal.
    assert "admin@gooddata.com" in rendered
    assert "GREATER_THAN" in rendered
    assert "Orders overview" in rendered
    # Opaque AFM wire dicts must not crowd out the fields above.
    assert "execution" not in rendered


def test_render_alert_proposal_drops_afm_when_execution_is_the_only_alert_field():
    # Truthiness-gated replacement used to leave the original execution-bearing dict in place.
    rendered = render_alert_proposal({"alert": {"execution": {"measures": [{"opaque": "afm"}]}}})
    assert "execution" not in rendered
    assert "opaque" not in rendered


def test_render_alert_proposal_falls_back_to_default_cta():
    assert render_alert_proposal({}).startswith("Should I create this alert?")


def test_run_agentic_alert_skill_answers_proposal_only_confirmation_turn():
    """GDAI-2032 regression: confirmation turn has no text part, only an alertProposal.

    Without the fallback the simulated user is handed an empty agent message, so the agent
    never receives an explicit "yes" and create_metric_alert is never called.
    """
    proposal_turn = ChatResult.model_validate(
        {
            "text_response": None,
            "alertProposals": [_PROPOSAL],
            "tool_call_events": [
                {"functionName": "prepare_metric_alert_proposal", "functionArguments": "{}", "result": None}
            ],
        }
    )
    created_turn = ChatResult.model_validate(
        {
            "text_response": "Alert created.",
            "tool_call_events": [
                {
                    "functionName": "create_metric_alert",
                    "functionArguments": '{"operator": "GREATER_THAN", "threshold": 500}',
                    "result": '{"id": "alert-1"}',
                }
            ],
        }
    )
    mock_client = MagicMock()
    mock_client.send_message.side_effect = [proposal_turn, created_turn]

    with (
        patch("gooddata_eval.core.agentic.alert_skill.ChatClient", return_value=mock_client),
        patch(
            "gooddata_eval.core.agentic.alert_skill.generate_simulated_alert_response",
            return_value="Yes, please proceed to create the alert.",
        ) as mock_sim,
        patch("gooddata_eval.core.agentic.alert_skill._delete_alert"),
    ):
        summary = run_agentic_alert_skill(
            host="http://host",
            token="tok",
            workspace_id="ws1",
            question="Notify me whenever the number of orders goes above 500",
            expected_output={"operator": "GREATER_THAN", "threshold": 500},
            k=1,
            max_iterations=6,
            initial_conversation_id="conv-1",
        )

    agent_message = mock_sim.call_args.args[0]
    assert "Should I create this alert?" in agent_message
    assert "admin@gooddata.com" in agent_message
    assert summary.best.eval.alert_created is True
    assert summary.best.alert_id == "alert-1"


def test_run_agentic_alert_skill_accumulates_reasoning_steps_across_iterations():
    proposal_turn = ChatResult.model_validate(
        {
            "text_response": None,
            "alertProposals": [_PROPOSAL],
            "toolCallEvents": [
                {"functionName": "prepare_metric_alert_proposal", "functionArguments": "{}", "result": None}
            ],
            "reasoningSteps": ["step one"],
        }
    )
    created_turn = ChatResult.model_validate(
        {
            "text_response": "Alert created.",
            "toolCallEvents": [
                {
                    "functionName": "create_metric_alert",
                    "functionArguments": '{"operator": "GREATER_THAN", "threshold": 500}',
                    "result": '{"id": "alert-1"}',
                }
            ],
            "reasoningSteps": ["step two"],
        }
    )
    mock_client = MagicMock()
    mock_client.send_message.side_effect = [proposal_turn, created_turn]

    with (
        patch("gooddata_eval.core.agentic.alert_skill.ChatClient", return_value=mock_client),
        patch(
            "gooddata_eval.core.agentic.alert_skill.generate_simulated_alert_response",
            return_value="Yes, please proceed to create the alert.",
        ),
        patch("gooddata_eval.core.agentic.alert_skill._delete_alert"),
    ):
        summary = run_agentic_alert_skill(
            host="http://host",
            token="tok",
            workspace_id="ws1",
            question="Notify me whenever the number of orders goes above 500",
            expected_output={"operator": "GREATER_THAN", "threshold": 500},
            k=1,
            max_iterations=6,
            initial_conversation_id="conv-1",
        )

    assert summary.best.reasoning_steps == ["step one", "step two"]


def test_evaluate_agentic_alert_skill_returns_reasoning_steps_on_pass():
    chat_result = ChatResult.model_validate(
        {
            "text_response": "Alert created.",
            "toolCallEvents": [
                {
                    "functionName": "create_metric_alert",
                    "functionArguments": '{"operator": "GREATER_THAN", "threshold": 500}',
                    "result": '{"id": "alert-1"}',
                }
            ],
            "reasoningSteps": ["thinking about it"],
        }
    )
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = chat_result

    with (
        patch("gooddata_eval.core.agentic.alert_skill.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.alert_skill._delete_alert"),
    ):
        reasoning = evaluate_agentic_alert_skill(
            host="http://host",
            token="tok",
            workspace_id="ws1",
            question="Notify me whenever the number of orders goes above 500",
            expected_output={"operator": "GREATER_THAN", "threshold": 500},
            k=1,
            max_iterations=1,
        )

    assert reasoning == ["thinking about it"]


def test_evaluate_agentic_alert_skill_attaches_reasoning_steps_to_exception_on_fail():
    chat_result = ChatResult.model_validate(
        {
            "text_response": "I cannot create the alert",
            "toolCallEvents": [],
            "reasoningSteps": ["confused thinking"],
        }
    )
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = chat_result

    with (
        patch("gooddata_eval.core.agentic.alert_skill.ChatClient", return_value=mock_client),
        pytest.raises(AlertSkillAssertionError) as exc_info,
    ):
        evaluate_agentic_alert_skill(
            host="http://host",
            token="tok",
            workspace_id="ws1",
            question="Create alert",
            expected_output={"operator": "GREATER_THAN", "threshold": 100},
            k=1,
            max_iterations=1,
        )
    assert exc_info.value.reasoning_steps == ["confused thinking"]

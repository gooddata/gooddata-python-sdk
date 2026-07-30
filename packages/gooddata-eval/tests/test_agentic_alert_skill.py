# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
import json
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.agentic.alert_skill import (
    AlertEvaluation,
    AlertSkillAssertionError,
    _check_trigger,
    _deep_subset,
    _normalize_expected_output,
    _score_comments,
    _to_number,
    evaluate_agentic_alert_skill,
    generate_simulated_alert_response,
    run_agentic_alert_skill,
)
from gooddata_eval.core.models import ChatResult


def _sim_user_prompt(expected_output: dict) -> tuple[str, dict]:
    """Render the sim-user system prompt for a fixture, plus the kwargs sent to gpt-4o."""
    mock_openai = MagicMock()
    mock_openai.return_value.chat.completions.create.return_value.choices = [MagicMock(message=MagicMock(content="ok"))]
    with (
        patch("gooddata_eval.core.agentic.alert_skill._OpenAI", mock_openai),
        patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}),
    ):
        generate_simulated_alert_response("Which metric?", _normalize_expected_output(expected_output), [])
    kwargs = mock_openai.return_value.chat.completions.create.call_args.kwargs
    return kwargs["messages"][0]["content"], kwargs


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


def test_sim_user_states_always_trigger_proactively():
    # QA-28623: an expected-ALWAYS trigger used to be left unsaid, so the agent aligned
    # trigger_interval with the date granularity and the sim-user accepted ONCE_PER_INTERVAL.
    prompt, _ = _sim_user_prompt({"Operator": "GREATER_THAN", "Trigger": "Every time"})
    assert "EVERY TIME" in prompt
    assert "do not set any trigger interval" in prompt


def test_sim_user_states_once_trigger_proactively():
    prompt, _ = _sim_user_prompt({"Operator": "LESS_THAN", "Trigger": "One time"})
    assert "ONLY THE FIRST TIME" in prompt


def test_sim_user_silent_on_trigger_when_fixture_omits_it():
    # No Trigger key -> the case is meant to exercise the product default; stating one would
    # turn it into a different test.
    prompt, _ = _sim_user_prompt({"Operator": "GREATER_THAN", "Threshold": 100})
    assert "EVERY TIME" not in prompt
    assert "trigger to" not in prompt


def test_sim_user_silent_on_trigger_for_anomaly():
    # ANOMALY legitimately defaults to ONCE_PER_INTERVAL and _check_trigger skips it.
    prompt, _ = _sim_user_prompt({"Operator": "ANOMALY", "Trigger": "ONCE_PER_INTERVAL"})
    assert "EVERY TIME" not in prompt


def test_sim_user_refuses_extra_filters_when_none_expected():
    prompt, _ = _sim_user_prompt({"Operator": "GREATER_THAN", "Trigger": "Every time"})
    assert "NO filters at all" in prompt
    assert "All time" in prompt


def test_sim_user_refuses_extra_filters_beyond_expected_list():
    filters = [{"positiveAttributeFilter": {"label": {"identifier": {"id": "product_category"}}}}]
    prompt, _ = _sim_user_prompt({"Operator": "LESS_THAN", "Trigger": "Every time", "Filters": filters})
    assert "ONLY filters this alert may have" in prompt
    assert "product_category" in prompt


def test_sim_user_verifies_trigger_and_filters_at_confirmation():
    # Regression guard for QA-28113: rule 3 must not shrink back to recipients-only.
    prompt, _ = _sim_user_prompt({"Operator": "GREATER_THAN", "Trigger": "Every time"})
    assert "recipients, the trigger AND the filters" in prompt


def test_sim_user_rules_are_numbered_without_gaps():
    prompt, _ = _sim_user_prompt({"Operator": "ANOMALY", "Trigger": "ONCE_PER_INTERVAL"})
    numbers = [int(line.split(".", 1)[0]) for line in prompt.splitlines() if line[:1].isdigit()]
    assert numbers == list(range(1, len(numbers) + 1))


def test_sim_user_uses_deterministic_temperature():
    _, kwargs = _sim_user_prompt({"Operator": "GREATER_THAN", "Trigger": "Every time"})
    assert kwargs["temperature"] == 0


def test_score_comments_expose_trigger_and_filters():
    # QA-28623: a 0.0 score alone forced triage through CI logs / nested trace observations.
    expected = _normalize_expected_output(
        {"Operator": "GREATER_THAN", "Trigger": "Every time", "Threshold": 5000, "Metric": "Total Discounts (td)"}
    )
    actual = {
        "operator": "GREATER_THAN",
        "threshold": 5000,
        "trigger": "ONCE_PER_INTERVAL",
        "trigger_interval": "DAY",
        "filters": [{"relativeDateFilter": {"granularity": "DAY"}}],
        "metric_id": "td",
        "external_recipients": '["admin@gooddata.com"]',
    }
    comments = _score_comments(expected, actual, alert_created=True)
    assert "'ALWAYS'" in comments["trigger_correct"]
    assert "'ONCE_PER_INTERVAL/DAY'" in comments["trigger_correct"]
    assert "relativeDateFilter" in comments["filters_correct"]
    assert "admin@gooddata.com" in comments["recipients_correct"]


def test_score_comments_range_operator_reports_bounds():
    expected = _normalize_expected_output(
        {"Operator": "BETWEEN", "threshold_from": 50000, "threshold_to": 200000, "Trigger": "Every time"}
    )
    comments = _score_comments(expected, {"from_value": 50000, "to_value": 1}, alert_created=True)
    assert "50000..200000" in comments["threshold_correct"]
    assert "50000..1" in comments["threshold_correct"]


def test_score_comments_when_alert_never_created():
    expected = _normalize_expected_output({"Operator": "GREATER_THAN", "Trigger": "Every time"})
    comments = _score_comments(expected, {}, alert_created=False)
    assert comments == {"alert_created": "create_metric_alert was never called"}


def test_evaluate_attaches_score_comments_to_the_trace():
    # Covers the Langfuse branch, which needs both a client and a dataset_item_id to run --
    # the other tests stop at run_agentic_alert_skill and never enter it.
    fake_langfuse = MagicMock()
    mock_client = MagicMock()
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "text_response": "Created the alert",
            "created_visualizations": None,
            "tool_call_events": [
                {
                    "functionName": "create_metric_alert",
                    "functionArguments": json.dumps(
                        {
                            "operator": "GREATER_THAN",
                            "threshold": 5000,
                            "trigger": "ONCE_PER_INTERVAL",
                            "trigger_interval": "DAY",
                            "filters": [{"relativeDateFilter": {"granularity": "DAY"}}],
                        }
                    ),
                    "result": "{}",
                }
            ],
            "reasoning_step_count": 1,
        }
    )
    trace = MagicMock(id="trace-1", latency=1.0, total_cost=0.01)

    with (
        patch("gooddata_eval.core.agentic.alert_skill.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.alert_skill.GoodDataSdk"),
        patch("gooddata_eval.core.agentic._langfuse.build_run_context", return_value=("run-name", {})),
        patch(
            "gooddata_eval.core.agentic._langfuse.find_traces_per_conversation",
            return_value={"existing-conv": trace},
        ),
        pytest.raises(AlertSkillAssertionError),
    ):
        evaluate_agentic_alert_skill(
            host="http://host",
            token="tok",
            workspace_id="ws1",
            question="Alert me when discounts get out of hand",
            expected_output={"Operator": "GREATER_THAN", "Threshold": 5000, "Trigger": "Every time"},
            k=1,
            max_iterations=1,
            initial_conversation_id="existing-conv",
            langfuse=fake_langfuse,
            dataset_item_id="item-1",
        )

    comments = {call.kwargs["name"]: call.kwargs.get("comment") for call in fake_langfuse.create_score.call_args_list}
    assert "ONCE_PER_INTERVAL/DAY" in comments["trigger_correct"]
    assert "relativeDateFilter" in comments["filters_correct"]


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

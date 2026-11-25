# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
"""Opt-in alert-skill checks: no-alert items, anomaly sensitivity/interval/dataset, metric comparison, setup turns."""

import json
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.agentic._catalog import CatalogMetricAlert
from gooddata_eval.core.agentic.alert_skill import (
    ALERT_CONDITIONAL_SCORES,
    AlertEvaluation,
    AlertRunResult,
    _check_comparison,
    _evaluate_alert,
    _normalize_expected_output,
    generate_simulated_alert_response,
    run_agentic_alert_skill,
)
from gooddata_eval.core.chat.sse_client import ChatError
from gooddata_eval.core.models import ChatResult, LoopExit

_ANOMALY = {
    "Metric": "Total Sales (total_sales)",
    "Operator": "ANOMALY",
    "Trigger": "ONCE_PER_INTERVAL",
    "Granularity": "MONTH",
    "Recipient(s)": "admin@gooddata.com",
}
# A create_metric_alert argument set as the agent sends it for the anomaly item above.
_ANOMALY_ARGS = {
    "metric_id": "total_sales",
    "operator": "ANOMALY",
    "granularity": "MONTH",
    "sensitivity": "HIGH",
    "date_dataset_id": "order_date",
    "trigger": "ONCE_PER_INTERVAL",
    "trigger_interval": "MONTH",
    "external_recipients": ["admin@gooddata.com"],
}


def _evaluate(expected_output: dict, args: dict) -> AlertEvaluation:
    return _evaluate_alert(_normalize_expected_output(expected_output), args, True, MagicMock(), None)


# --- parsing ---------------------------------------------------------------------------------


def test_new_keys_are_parsed_and_canonicalised() -> None:
    expected = _normalize_expected_output(
        {
            **_ANOMALY,
            "Sensitivity": "high",
            "Trigger interval": "month",
            "Date dataset": "order_date",
            "setup_turns": ["Show me Net Sales as a headline."],
        }
    )
    assert expected.sensitivity == "HIGH"
    assert expected.trigger_interval == "MONTH"
    assert expected.date_dataset_id == "order_date"
    assert expected.setup_turns == ("Show me Net Sales as a headline.",)
    assert expected.expect_alert is True


def test_items_without_the_new_keys_parse_as_before() -> None:
    expected = _normalize_expected_output({"Metric": "Net Sales (net_sales)", "Operator": "LESS_THAN"})
    assert (expected.sensitivity, expected.trigger_interval, expected.date_dataset_id) == (None, None, None)
    assert expected.setup_turns == ()
    assert expected.expect_alert is True


@pytest.mark.parametrize(
    "extra",
    [
        {"Sensitivity": "VERY_HIGH"},
        {"Trigger interval": "HOUR"},
        {"Date dataset": 5},
        {"setup_turns": "Show me Net Sales."},
        {"setup_turns": ["  "]},
        {"Expect alert": "no"},
    ],
)
def test_malformed_new_keys_fail_before_any_request(extra: dict) -> None:
    with pytest.raises(ValueError):
        _normalize_expected_output({**_ANOMALY, **extra})


def test_trigger_interval_requires_the_once_per_interval_trigger() -> None:
    with pytest.raises(ValueError, match="ONCE_PER_INTERVAL"):
        _normalize_expected_output({"Operator": "GREATER_THAN", "Trigger": "Every time", "Trigger interval": "WEEK"})


@pytest.mark.parametrize("extra", [{"Sensitivity": "MEDIUM"}, {"Date dataset": "order_date"}])
def test_anomaly_settings_require_the_anomaly_operator(extra: dict) -> None:
    # A GREATER_THAN alert sends neither argument, so a stated MEDIUM would always match the default.
    with pytest.raises(ValueError, match="only to the ANOMALY operator"):
        _normalize_expected_output({"Operator": "GREATER_THAN", "Threshold": "100", **extra})


def test_no_alert_item_may_not_state_alert_fields() -> None:
    with pytest.raises(ValueError, match="expect_alert: false"):
        _normalize_expected_output({"Expect alert": False, "Operator": "GREATER_THAN", "Threshold": "0.05"})


def test_no_alert_item_parses() -> None:
    assert _normalize_expected_output({"Expect alert": False}).expect_alert is False


# --- checks ----------------------------------------------------------------------------------


def test_anomaly_settings_are_scored_when_stated() -> None:
    ev = _evaluate(
        {**_ANOMALY, "Sensitivity": "HIGH", "Trigger interval": "MONTH", "Date dataset": "order_date"}, _ANOMALY_ARGS
    )
    checks = ev.checks()
    assert checks["alert_sensitivity_correct"] is True
    assert checks["alert_trigger_interval_correct"] is True
    assert checks["alert_date_dataset_correct"] is True
    assert ev.strict_pass


def test_wrong_anomaly_settings_fail_their_own_check() -> None:
    ev = _evaluate(
        {**_ANOMALY, "Sensitivity": "HIGH", "Trigger interval": "MONTH", "Date dataset": "order_date"},
        {**_ANOMALY_ARGS, "sensitivity": "MEDIUM", "trigger_interval": "DAY", "date_dataset_id": "date"},
    )
    checks = ev.checks()
    assert checks["alert_sensitivity_correct"] is False
    assert checks["alert_trigger_interval_correct"] is False
    assert checks["alert_date_dataset_correct"] is False
    assert not ev.strict_pass


@pytest.mark.parametrize("trigger", [{"trigger": "ALWAYS"}, {"trigger": None}, {}], ids=["always", "null", "missing"])
def test_the_interval_needs_the_once_per_interval_trigger(trigger: dict) -> None:
    # The tool defaults the trigger to ALWAYS, and an ALWAYS alert never uses its trigger_interval.
    args = {k: v for k, v in _ANOMALY_ARGS.items() if k != "trigger"} | trigger
    checks = _evaluate({**_ANOMALY, "Trigger interval": "MONTH"}, args).checks()
    assert checks["alert_trigger_interval_correct"] is False


def test_unstated_anomaly_settings_are_not_scored() -> None:
    # An argument the item states nothing about adds no check, so such an item keeps the same score names.
    checks = _evaluate(_ANOMALY, {**_ANOMALY_ARGS, "sensitivity": "LOW"}).checks()
    for name in ("alert_sensitivity_correct", "alert_trigger_interval_correct", "alert_date_dataset_correct"):
        assert name not in checks


def test_conditional_score_names_are_published() -> None:
    assert set(ALERT_CONDITIONAL_SCORES) >= {
        "alert_sensitivity_correct",
        "alert_trigger_interval_correct",
        "alert_date_dataset_correct",
        "alert_not_proposed",
        "comparison_correct",
        "title_correct",
        "dashboard_correct",
    }


def test_metric_to_metric_comparison_checks_the_compared_metric() -> None:
    expected = _normalize_expected_output(
        {"Operator": "LESS_THAN", "Comparison": {"compare_metric_id": "net_sales_goal"}}
    )
    assert expected.comparison == {"compare_metric_id": "net_sales_goal"}
    assert _check_comparison(expected, {"compare_metric_id": "net_sales_goal"})
    assert not _check_comparison(expected, {"compare_metric_id": "total_sales"})
    assert not _check_comparison(expected, {})


@pytest.mark.parametrize("key", ["compare_metric_id", "date_dataset_id", "date_attribute_id"])
@pytest.mark.parametrize("value", [["net_sales_goal"], {"id": "net_sales_goal"}, 7])
def test_a_comparison_id_must_be_a_string(key: str, value: object) -> None:
    with pytest.raises(ValueError, match=f"Comparison {key} must be an object id string"):
        _normalize_expected_output({"Operator": "LESS_THAN", "Comparison": {key: value}})


def test_a_null_comparison_id_stays_unasserted() -> None:
    expected = _normalize_expected_output(
        {"Operator": "LESS_THAN", "Comparison": {"kind": "METRIC", "compare_metric_id": None}}
    )
    assert expected.comparison == {"comparison_kind": "METRIC"}


# --- run loop --------------------------------------------------------------------------------


def _turn(text: str = "", *, proposal: bool = False, create_result: str | None = None) -> ChatResult:
    events = []
    if create_result is not None:
        events.append(
            {
                "functionName": "create_metric_alert",
                "functionArguments": json.dumps(_ANOMALY_ARGS),
                "result": create_result,
            }
        )
    payload: dict = {"text_response": text, "toolCallEvents": events}
    if proposal:
        payload["alertProposals"] = [{"cta": "Should I create this alert?", "alert": {"trigger": "ALWAYS"}}]
    return ChatResult.model_validate(payload)


def _metric_turn(text: str = "", *, create_result: str | None = None) -> ChatResult:
    """A turn whose agent created the churn-rate metric, optionally also creating an alert."""
    events = [
        {
            "functionName": "create_metric",
            "functionArguments": "{}",
            "result": json.dumps({"metric_id": "churn_rate", "created_new": True}),
        }
    ]
    if create_result is not None:
        events.append(
            {
                "functionName": "create_metric_alert",
                "functionArguments": json.dumps(_ANOMALY_ARGS),
                "result": create_result,
            }
        )
    return ChatResult.model_validate({"text_response": text, "toolCallEvents": events})


def _run(
    client: MagicMock, expected_output: dict, simulated_reply: str = "No, thanks.", max_iterations: int = 6
) -> tuple[AlertRunResult, MagicMock, MagicMock]:
    with (
        patch("gooddata_eval.core.agentic.alert_skill.ChatClient", return_value=client),
        patch(
            "gooddata_eval.core.agentic.alert_skill.generate_simulated_alert_response", return_value=simulated_reply
        ) as mock_sim,
        patch("gooddata_eval.core.agentic.alert_skill._delete_alert") as mock_delete,
    ):
        summary = run_agentic_alert_skill(
            host="http://host",
            token="tok",
            workspace_id="ws1",
            question="Notify me if customer churn rate goes above 5%.",
            expected_output=expected_output,
            k=1,
            max_iterations=max_iterations,
            initial_conversation_id="conv-1",
        )
    # Every send stays in the run's conversation: setup turns, the question, then the simulated replies.
    sent = [c.args for c in client.send_message.call_args_list]
    opening = [*expected_output.get("setup_turns", []), "Notify me if customer churn rate goes above 5%."]
    # A run cut short (a broken setup turn) sends a prefix of this sequence.
    expected_sends = (opening + [simulated_reply] * len(sent))[: len(sent)]
    assert sent == [("conv-1", message) for message in expected_sends]
    return summary.best, mock_sim, mock_delete


def test_no_alert_item_passes_when_the_agent_never_proposes() -> None:
    client = MagicMock()
    client.send_message.return_value = _turn("There is no churn rate metric. Should I use Return Customers?")
    run, _, _ = _run(client, {"Expect alert": False})
    assert run.eval.checks() == {"alert_not_proposed": True}
    assert run.eval.strict_pass
    # The simulated user only declines, so the run stops early instead of using the whole budget.
    assert client.send_message.call_count == 3


def test_no_alert_item_fails_on_a_proposal() -> None:
    client = MagicMock()
    client.send_message.side_effect = [_turn("Which metric?"), _turn(proposal=True)]
    run, _, _ = _run(client, {"Expect alert": False})
    assert run.eval.checks() == {"alert_not_proposed": False}
    assert not run.eval.strict_pass


def test_no_alert_item_fails_and_cleans_up_when_an_alert_is_created() -> None:
    client = MagicMock()
    client.send_message.return_value = _turn(create_result='{"id": "alert-1"}')
    run, _, mock_delete = _run(client, {"Expect alert": False})
    assert run.eval.checks() == {"alert_not_proposed": False}
    assert [c.args[2] for c in mock_delete.call_args_list] == ["alert-1"]


def test_no_alert_item_fails_and_cleans_up_when_the_agent_creates_a_metric() -> None:
    # The created metric would make the next run of this item find one and propose an alert.
    client = MagicMock()
    client.send_message.return_value = _metric_turn("I created a Churn Rate metric for you.")
    with patch("gooddata_eval.core.agentic.alert_skill._delete_metric") as mock_delete_metric:
        run, _, _ = _run(client, {"Expect alert": False})
    assert run.eval.checks() == {"alert_not_proposed": False}
    assert run.exit_reason == LoopExit.SUCCESS
    assert [c.args[1:] for c in mock_delete_metric.call_args_list] == [("ws1", "churn_rate")]


def test_a_metric_the_agent_created_is_deleted_after_its_alert() -> None:
    client = MagicMock()
    client.send_message.return_value = _metric_turn(create_result='{"id": "alert-1"}')
    order = MagicMock()
    with (
        patch("gooddata_eval.core.agentic.alert_skill._delete_metric", order.delete_metric),
        patch("gooddata_eval.core.agentic.alert_skill._delete_alert", order.delete_alert),
        patch("gooddata_eval.core.agentic.alert_skill.ChatClient", return_value=client),
    ):
        run_agentic_alert_skill(
            host="http://host",
            token="tok",
            workspace_id="ws1",
            question="Notify me if customer churn rate goes above 5%.",
            expected_output=_ANOMALY,
            k=1,
            initial_conversation_id="conv-1",
        )
    assert [(c[0], c.args[1:]) for c in order.mock_calls] == [
        ("delete_alert", ("ws1", "alert-1")),
        ("delete_metric", ("ws1", "churn_rate")),
    ]


def test_no_alert_item_uses_the_declining_simulated_user() -> None:
    fake_openai = MagicMock()
    fake_openai.return_value.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="No."))]
    )
    with (
        patch("gooddata_eval.core.agentic.alert_skill._OpenAI", fake_openai),
        patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}),
    ):
        generate_simulated_alert_response(
            "Should I use Return Customers instead?",
            _normalize_expected_output({"Expect alert": False}),
            [],
            question="Notify me if customer churn rate goes above 5%.",
        )
    prompt = fake_openai.return_value.chat.completions.create.call_args.kwargs["messages"][0]["content"]
    assert "Never accept a different or similar metric" in prompt
    assert "churn rate" in prompt


def test_setup_turns_are_sent_first_in_the_same_conversation_and_not_scored() -> None:
    setup = ChatResult.model_validate(
        {
            "text_response": "Here is Net Sales: $105.2 M.",
            "toolCallEvents": [
                {"functionName": "create_adhoc_visualization", "functionArguments": "{}", "result": "{}"}
            ],
        }
    )
    created = _turn(create_result='{"id": "alert-1"}')
    client = MagicMock()
    client.send_message.side_effect = [setup, created]
    expected = {**_ANOMALY, "setup_turns": ["Show me Net Sales as a headline."]}
    run, _, _ = _run(client, expected)
    sent = [c.args for c in client.send_message.call_args_list]
    assert sent[0] == ("conv-1", "Show me Net Sales as a headline.")
    assert sent[1] == ("conv-1", "Notify me if customer churn rate goes above 5%.")
    assert run.eval.alert_created is True
    # The question turn is the first scored turn.
    assert run.turns_used == 1


def test_setup_turns_reach_the_simulated_user_history() -> None:
    setup = ChatResult.model_validate({"text_response": "Here is Net Sales: $105.2 M."})
    client = MagicMock()
    client.send_message.side_effect = [setup, _turn("Which channel?"), _turn(create_result='{"id": "a"}')]
    expected = {**_ANOMALY, "setup_turns": ["Show me Net Sales as a headline."]}
    _, mock_sim, _ = _run(client, expected)
    history = mock_sim.call_args.args[2]
    assert history[0] == {"role": "user", "content": "Show me Net Sales as a headline."}
    assert "$105.2 M" in history[1]["content"]


def test_simulated_user_is_told_the_stated_anomaly_settings() -> None:
    fake_openai = MagicMock()
    fake_openai.return_value.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="ok"))]
    )
    with (
        patch("gooddata_eval.core.agentic.alert_skill._OpenAI", fake_openai),
        patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}),
    ):
        generate_simulated_alert_response(
            "Which sensitivity?",
            _normalize_expected_output(
                {**_ANOMALY, "Sensitivity": "HIGH", "Trigger interval": "MONTH", "Date dataset": "order_date"}
            ),
            [],
            question="Watch Total Sales for anomalies by order month with high sensitivity.",
        )
    prompt = fake_openai.return_value.chat.completions.create.call_args.kwargs["messages"][0]["content"]
    assert "Use HIGH sensitivity" in prompt
    assert "date dataset order_date" in prompt
    assert "trigger interval of MONTH" in prompt


def test_simulated_user_is_told_its_setup_turns_came_first() -> None:
    fake_openai = MagicMock()
    fake_openai.return_value.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="ok"))]
    )
    with (
        patch("gooddata_eval.core.agentic.alert_skill._OpenAI", fake_openai),
        patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}),
    ):
        generate_simulated_alert_response(
            "Which channel?",
            _normalize_expected_output(
                {**_ANOMALY, "setup_turns": ["Show me Net Sales as a headline.", "Now break it down by month."]}
            ),
            [],
            question="Watch Total Sales for anomalies by order month.",
        )
    prompt = fake_openai.return_value.chat.completions.create.call_args.kwargs["messages"][0]["content"]
    assert (
        'Earlier in this conversation you asked: "Show me Net Sales as a headline." / "Now break it down by month.".\n'
        'Your original request to the agent was: "Watch Total Sales for anomalies by order month."'
    ) in prompt


def test_omitted_sensitivity_is_scored_as_the_tool_default() -> None:
    # create_metric_alert applies MEDIUM when sensitivity is left out.
    args = {k: v for k, v in _ANOMALY_ARGS.items() if k != "sensitivity"}
    assert _evaluate({**_ANOMALY, "Sensitivity": "MEDIUM"}, args).checks()["alert_sensitivity_correct"] is True
    assert _evaluate({**_ANOMALY, "Sensitivity": "HIGH"}, args).checks()["alert_sensitivity_correct"] is False


def test_no_alert_item_fails_when_the_question_turn_errors() -> None:
    # A run the chat cut short never showed the agent declining.
    client = MagicMock()
    client.send_message.side_effect = ChatError("stream died")
    run, _, _ = _run(client, {"Expect alert": False})
    assert run.exit_reason == LoopExit.CHAT_ERROR
    assert run.eval.checks() == {"alert_not_proposed": False}


def test_no_alert_item_passes_when_the_agent_goes_quiet_after_declining() -> None:
    # "I can't create this alert." -> "OK, thanks." -> an empty turn: nothing was ever proposed.
    client = MagicMock()
    client.send_message.side_effect = [_turn("I can't create this alert."), _turn("")]
    run, _, _ = _run(client, {"Expect alert": False}, simulated_reply="OK, thanks.")
    assert run.exit_reason == LoopExit.AGENT_SILENT
    assert run.turns_used == 2
    assert run.eval.checks() == {"alert_not_proposed": True}


def test_no_alert_item_fails_when_the_agent_goes_silent() -> None:
    client = MagicMock()
    client.send_message.return_value = _turn("")
    run, _, _ = _run(client, {"Expect alert": False})
    assert run.exit_reason == LoopExit.AGENT_SILENT
    assert run.eval.checks() == {"alert_not_proposed": False}


def test_no_alert_item_fails_on_a_rejected_proposal_call() -> None:
    # A rejected proposal call leaves no proposal part, but the agent still tried to propose a substitute.
    rejected = ChatResult.model_validate(
        {
            "text_response": "I could not prepare that alert.",
            "toolCallEvents": [
                {
                    "functionName": "prepare_metric_alert_proposal",
                    "functionArguments": "{}",
                    "result": '{"success": false, "error": "rejected"}',
                }
            ],
        }
    )
    client = MagicMock()
    client.send_message.return_value = rejected
    run, _, _ = _run(client, {"Expect alert": False})
    assert run.eval.checks() == {"alert_not_proposed": False}


def test_no_alert_item_needs_no_current_user() -> None:
    client = MagicMock()
    client.send_message.return_value = _turn("There is no churn rate metric.")
    with patch("gooddata_eval.core.agentic.alert_skill._resolve_current_user_id") as mock_resolve:
        run, _, _ = _run(client, {"Expect alert": False, "Recipient(s)": "me"})
    mock_resolve.assert_not_called()
    assert run.eval.strict_pass


def test_a_broken_setup_turn_deletes_the_alert_it_created() -> None:
    partial = _turn(create_result='{"id": "alert-1"}')
    client = MagicMock()
    client.send_message.side_effect = [ChatError("stream died", partial_result=partial)]
    run, _, mock_delete = _run(client, {**_ANOMALY, "setup_turns": ["Show me Net Sales as a headline."]})
    assert run.exit_reason == LoopExit.CHAT_ERROR
    assert run.eval.alert_created is False
    assert [c.args[2] for c in mock_delete.call_args_list] == ["alert-1"]


def test_catalog_from_dict_parses_the_new_fields_as_expected_output_does() -> None:
    alert = CatalogMetricAlert.from_dict(
        {
            "operator": "ANOMALY",
            "trigger": "ONCE_PER_INTERVAL",
            "sensitivity": "high",
            "trigger_interval": "month",
            "setup_turns": ["Show me Net Sales."],
        }
    )
    assert (alert.sensitivity, alert.trigger_interval) == ("HIGH", "MONTH")
    assert alert.setup_turns == ("Show me Net Sales.",)
    assert alert.expect_alert is True
    assert CatalogMetricAlert.from_dict({"expect_alert": None}).expect_alert is True
    assert CatalogMetricAlert.from_dict({"expect_alert": False}).expect_alert is False


@pytest.mark.parametrize(
    "fields",
    [
        {"expect_alert": "false"},
        {"setup_turns": "Show me Net Sales."},
        {"setup_turns": ["  "]},
        {"operator": "ANOMALY", "sensitivity": "extreme"},
    ],
)
def test_catalog_from_dict_rejects_what_expected_output_rejects(fields: dict) -> None:
    with pytest.raises(ValueError):
        _normalize_expected_output(fields)
    with pytest.raises(ValueError):
        CatalogMetricAlert.from_dict(fields)


@pytest.mark.parametrize("max_iterations", [0, -1])
def test_a_run_needs_at_least_one_turn(max_iterations: int) -> None:
    with pytest.raises(ValueError, match="max_iterations"):
        run_agentic_alert_skill(
            host="http://host",
            token="tok",
            workspace_id="ws1",
            question="q",
            expected_output={"Expect alert": False},
            max_iterations=max_iterations,
        )

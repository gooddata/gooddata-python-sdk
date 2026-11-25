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
    _named_automation_ids,
    _normalize_expected_output,
    _proposal_recipient_args,
    generate_simulated_alert_response,
    run_agentic_alert_skill,
)
from gooddata_eval.core.agentic.alert_skill import (
    # Bound at import, before conftest replaces the module attribute for every test.
    _automation_ids as _list_automation_ids,
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


# --- any-of expectations and the first proposal ------------------------------------------------

_LAST_MONTH = {
    "relativeDateFilter": {
        "dataset": {"identifier": {"id": "date", "type": "dataset"}},
        "granularity": "MONTH",
        "from": -1,
        "to": -1,
    }
}
_YEAR_2025 = {
    "absoluteDateFilter": {
        "dataset": {"identifier": {"id": "date", "type": "dataset"}},
        "from": "2025-01-01",
        "to": "2025-12-31",
    }
}
_US = {
    "positiveAttributeFilter": {
        "label": {"identifier": {"id": "customer_country", "type": "label"}},
        "in": {"values": ["United States"]},
    }
}
_BASE = {
    "Metric": "Net Sales (net_sales)",
    "Operator": "LESS_THAN",
    "Threshold": "1000",
    "Recipient(s)": "admin@gooddata.com",
}
# A chart by month: the UI's default (sum of the chart over its range) or the last completed month.
_DATE_CHART = {
    **_BASE,
    "any_of": [
        {"Threshold": 47136608.82, "Filters": [_YEAR_2025]},
        {"Threshold": 5428565.6, "Filters": [_LAST_MONTH]},
    ],
}
_CREATE_ARGS = {
    "metric_id": "net_sales",
    "operator": "LESS_THAN",
    "threshold": 1000,
    "external_recipients": ["admin@gooddata.com"],
}


@pytest.mark.parametrize(
    ("threshold", "filters", "passes"),
    [
        (47136608.82, [_YEAR_2025], True),
        (5428565.6, [_LAST_MONTH], True),
        # Each field matches an option, but not the same one: the sum of a year against one month.
        (47136608.82, [_LAST_MONTH], False),
        (5428565.6, [_YEAR_2025], False),
    ],
)
def test_any_of_matches_fields_of_one_option_together(threshold: float, filters: list, passes: bool) -> None:
    ev = _evaluate(_DATE_CHART, {**_CREATE_ARGS, "threshold": threshold, "filters": filters})
    assert ev.strict_pass is passes


def test_any_of_option_keeps_the_fields_it_does_not_state() -> None:
    expected = {**_BASE, "Filters": [_US], "any_of": [{"Threshold": 1}, {"Threshold": 2}]}
    ev = _evaluate(expected, {**_CREATE_ARGS, "threshold": 2, "filters": [_US], "metric_id": "other"})
    assert ev.checks()["threshold_correct"] is True
    assert ev.checks()["filters_correct"] is True
    assert ev.checks()["metric_correct"] is False


def test_any_of_option_replaces_every_spelling_of_the_filters() -> None:
    expected = {**_BASE, "Time window/Filters": "None (All time)", "any_of": [{"Filters": [_US]}, {"Filters": []}]}
    assert _evaluate(expected, {**_CREATE_ARGS, "filters": [_US]}).strict_pass
    assert _evaluate(expected, {**_CREATE_ARGS, "filters": []}).strict_pass
    assert not _evaluate(expected, {**_CREATE_ARGS, "filters": [_LAST_MONTH]}).strict_pass


@pytest.mark.parametrize(
    "any_of",
    [
        [{"Threshold": 1}],
        [{"Threshold": 1}, {}],
        [{"Threshold": 1}, "2"],
        [{"Threshold": 1}, {"setup_turns": ["x"]}],
        [{"Threshold": 1}, {"Sensitivity": "EXTREME"}],
        [{"Threshold": 1}, {"Threshold": 2, "check_first_proposal": ["recipients"]}],
    ],
)
def test_malformed_any_of_fails_early(any_of: list) -> None:
    with pytest.raises(ValueError):
        _normalize_expected_output({**_BASE, "any_of": any_of})


def test_any_of_options_may_not_differ_in_group_by() -> None:
    # The simulated user never sees a proposal's group-by, so it could not tell such options apart.
    region = {"localIdentifier": "a0", "label": {"identifier": {"id": "region", "type": "label"}}}
    with pytest.raises(ValueError, match=r"only in threshold and filters, not in \['attributes'\]"):
        _normalize_expected_output(
            {**_BASE, "any_of": [{"Threshold": 1, "Attributes": []}, {"Threshold": 2, "Attributes": [region]}]}
        )
    # A group-by the options share stays allowed.
    shared = _normalize_expected_output(
        {**_BASE, "Attributes": [region], "any_of": [{"Threshold": 1}, {"Threshold": 2}]}
    )
    assert shared.attributes is not None and len(shared.attributes) == 1


@pytest.mark.parametrize(
    "any_of",
    [
        # Option 2 states no filters over a base that states none, so it would accept the year filter
        # of option 1 with its own threshold.
        [{"Threshold": 47136608.82, "Filters": [_YEAR_2025]}, {"Threshold": 5428565.6}],
        [{"Threshold": 1, "Filters": []}, {"Filters": [_US]}],
    ],
)
def test_every_any_of_option_states_threshold_and_filters_or_none_does(any_of: list) -> None:
    base = {k: v for k, v in _BASE.items() if k != "Threshold"}
    with pytest.raises(ValueError, match="every any_of option must state"):
        _normalize_expected_output({**base, "any_of": any_of})


def test_any_of_option_that_repeats_another_fails_early() -> None:
    with pytest.raises(ValueError, match="repeats an earlier one"):
        _normalize_expected_output({**_BASE, "any_of": [{"Threshold": 5}, {"Threshold": 6}, {"Threshold": 5}]})


def test_any_of_options_with_a_misspelled_key_fail_early() -> None:
    # "Thresold" is ignored, so each such option is the item itself.
    with pytest.raises(ValueError, match="repeats an earlier one"):
        _normalize_expected_output({**_BASE, "any_of": [{"Thresold": 5}, {"Threshold": 6}, {"Thresold": 7}]})
    # Over a base without a threshold, the misspelled option is the one that states none.
    base = {k: v for k, v in _BASE.items() if k != "Threshold"}
    with pytest.raises(ValueError, match="must state Threshold"):
        _normalize_expected_output({**base, "any_of": [{"Thresold": 5}, {"Threshold": 6}]})


def test_any_of_item_is_what_its_options_share() -> None:
    # The base alone states an interval without its trigger; only the merged options are complete.
    expected = _normalize_expected_output(
        {
            **_BASE,
            "Trigger interval": "MONTH",
            "any_of": [
                {"Trigger": "ONCE_PER_INTERVAL", "Threshold": 1},
                {"Trigger": "ONCE_PER_INTERVAL", "Threshold": 2},
            ],
        }
    )
    assert (expected.trigger, expected.trigger_interval) == ("ONCE_PER_INTERVAL", "MONTH")
    # The options disagree on the threshold, so the item states none; rule 9 gives it per combination.
    assert expected.threshold is None
    assert [a.threshold for a in expected.alternatives] == [1, 2]


def test_any_of_option_with_a_trigger_that_breaks_the_interval_still_fails() -> None:
    with pytest.raises(ValueError, match="ONCE_PER_INTERVAL"):
        _normalize_expected_output(
            {
                **_BASE,
                "Trigger interval": "MONTH",
                "any_of": [{"Trigger": "ONCE_PER_INTERVAL", "Threshold": 1}, {"Trigger": "Every time", "Threshold": 2}],
            }
        )


def test_no_alert_item_cannot_list_alternatives() -> None:
    with pytest.raises(ValueError):
        _normalize_expected_output({"Expect alert": False, "any_of": [{"Threshold": 1}, {"Threshold": 2}]})


@pytest.mark.parametrize("extra", [{"check_first_proposal": ["metric"]}, {"check_first_proposal": []}])
def test_malformed_first_proposal_key_fails_early(extra: dict) -> None:
    with pytest.raises(ValueError):
        _normalize_expected_output({**_BASE, "Filters": [_US], **extra})


def test_first_proposal_check_needs_a_stated_expectation() -> None:
    with pytest.raises(ValueError, match="no filter expectation"):
        _normalize_expected_output({"Operator": "LESS_THAN", "check_first_proposal": ["filters"]})
    with pytest.raises(ValueError, match="no recipients"):
        _normalize_expected_output({"Operator": "LESS_THAN", "Filters": [], "check_first_proposal": ["recipients"]})
    # Each option of an any_of item states the filters, so the check is valid there.
    expected = {**_BASE, "check_first_proposal": ["filters"], "any_of": [{"Filters": [_US]}, {"Filters": []}]}
    assert _normalize_expected_output(expected).check_first_proposal == ("filters",)


def _proposal_event(filters: list, recipients: list, *, success: bool = True, automation_id: str = "") -> dict:
    return {
        "functionName": "prepare_metric_alert_proposal",
        "functionArguments": json.dumps({"recipients": recipients, "automation_id": automation_id or None}),
        "result": json.dumps(
            {"success": success, "alert_proposal_ref": "p1", "afm_filters": filters, "afm_attributes": []}
            if success
            else {"success": False, "error": "bad label"}
        ),
    }


def _events(*raw: dict) -> list:
    return ChatResult.model_validate({"toolCallEvents": list(raw)}).tool_call_events


def test_first_proposal_is_scored_although_the_final_alert_is_right() -> None:
    expected = {**_BASE, "Filters": [_LAST_MONTH, _US], "check_first_proposal": ["filters", "recipients"]}
    turns = [
        _events(_proposal_event([_US], [{"label": "You", "id": "someone", "email": None}])),
        _events(_proposal_event([_LAST_MONTH, _US], [{"label": "admin", "id": None, "email": "admin@gooddata.com"}])),
    ]
    ev = _evaluate_alert(
        _normalize_expected_output(expected),
        {**_CREATE_ARGS, "filters": [_LAST_MONTH, _US]},
        True,
        MagicMock(),
        None,
        turns,
    )
    checks = ev.checks()
    assert checks["filters_correct"] is True
    assert checks["recipients_correct"] is True
    assert checks["alert_initial_filters_correct"] is False
    assert checks["alert_initial_recipients_correct"] is False
    assert not ev.strict_pass


def test_first_proposal_is_the_last_one_of_its_turn() -> None:
    # The user is shown only the turn's last proposal; one the agent replaced before replying is not its answer.
    expected = {**_BASE, "Filters": [_US], "check_first_proposal": ["filters"]}
    turn = _events(_proposal_event([], []), _proposal_event([_US], []))
    ev = _evaluate_alert(
        _normalize_expected_output(expected), {**_CREATE_ARGS, "filters": [_US]}, True, MagicMock(), None, [turn]
    )
    assert ev.checks()["alert_initial_filters_correct"] is True


def test_first_proposal_uses_the_option_the_run_matches() -> None:
    expected = {**_BASE, "check_first_proposal": ["filters"], "any_of": [{"Filters": [_US]}, {"Filters": []}]}
    events = _events(_proposal_event([], [{"label": "admin", "id": None, "email": "admin@gooddata.com"}]))
    ev = _evaluate_alert(
        _normalize_expected_output(expected), {**_CREATE_ARGS, "filters": []}, True, MagicMock(), None, [events]
    )
    assert ev.strict_pass


def test_first_proposal_ignores_the_other_tool_calls_of_its_turn() -> None:
    expected = {**_BASE, "Filters": [_US], "check_first_proposal": ["filters"]}
    turn = _events(
        {"functionName": "search_objects", "functionArguments": "{}", "result": "{}"}, _proposal_event([_US], [])
    )
    ev = _evaluate_alert(
        _normalize_expected_output(expected), {**_CREATE_ARGS, "filters": [_US]}, True, MagicMock(), None, [turn]
    )
    assert ev.checks()["alert_initial_filters_correct"] is True


def test_first_proposal_skips_a_rejected_call() -> None:
    expected = {**_BASE, "Filters": [_US], "check_first_proposal": ["filters"]}
    events = _events(
        _proposal_event([], [], success=False),
        _proposal_event([_US], [{"label": "admin", "id": None, "email": "admin@gooddata.com"}]),
    )
    ev = _evaluate_alert(
        _normalize_expected_output(expected), {**_CREATE_ARGS, "filters": [_US]}, True, MagicMock(), None, [events]
    )
    assert ev.checks()["alert_initial_filters_correct"] is True


def test_first_proposal_reads_recipients_sent_as_a_json_string() -> None:
    recipients = json.dumps([{"label": "admin", "id": None, "email": "admin@gooddata.com"}])
    assert _proposal_recipient_args({"recipients": recipients}) == {
        "internal_recipients": [],
        "external_recipients": ["admin@gooddata.com"],
    }
    assert _proposal_recipient_args({"recipients": "not json"}) == {
        "internal_recipients": [],
        "external_recipients": [],
    }


def test_first_proposal_check_fails_without_any_proposal() -> None:
    expected = {**_BASE, "Filters": [_US], "check_first_proposal": ["filters"]}
    ev = _evaluate_alert(
        _normalize_expected_output(expected), {**_CREATE_ARGS, "filters": [_US]}, True, MagicMock(), None, []
    )
    assert ev.checks()["alert_initial_filters_correct"] is False


def test_first_proposal_checks_are_absent_unless_requested() -> None:
    checks = _evaluate({**_BASE, "Filters": [_US]}, {**_CREATE_ARGS, "filters": [_US]}).checks()
    assert "alert_initial_filters_correct" not in checks
    assert "alert_initial_recipients_correct" not in checks
    assert {"alert_initial_filters_correct", "alert_initial_recipients_correct"} <= set(ALERT_CONDITIONAL_SCORES)


def test_simulated_user_is_told_every_combination() -> None:
    fake_openai = MagicMock()
    fake_openai.return_value.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="ok"))]
    )
    with (
        patch("gooddata_eval.core.agentic.alert_skill._OpenAI", fake_openai),
        patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}),
    ):
        generate_simulated_alert_response("Confirm?", _normalize_expected_output(_DATE_CHART), [], question="q")
    prompt = fake_openai.return_value.chat.completions.create.call_args.kwargs["messages"][0]["content"]
    assert "any ONE of these combinations" in prompt
    assert "A) threshold=47136608.82" in prompt
    assert "B) threshold=5428565.6" in prompt
    assert "absoluteDateFilter" in prompt
    assert "matches one combination in full" in prompt


def _simulated_user_prompt(expected_output: dict) -> str:
    fake_openai = MagicMock()
    fake_openai.return_value.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="ok"))]
    )
    with (
        patch("gooddata_eval.core.agentic.alert_skill._OpenAI", fake_openai),
        patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}),
    ):
        generate_simulated_alert_response("Confirm?", _normalize_expected_output(expected_output), [], question="q")
    return fake_openai.return_value.chat.completions.create.call_args.kwargs["messages"][0]["content"]


@pytest.mark.parametrize(
    "fields",
    [
        {"Operator": "GREATER_THAN"},
        {"Recipient(s)": "me"},
        {"Trigger": "ONCE"},
        {"Metric": "Other (other)"},
        {"Dashboard": "D (d2)"},
        {"Title": "Low sales"},
    ],
)
def test_any_of_options_may_differ_only_in_threshold_and_filters(fields: dict) -> None:
    # Rules 1-8 of the simulated user state every other field once, so a differing one would be
    # asked for one way and scored another.
    with pytest.raises(ValueError, match="only in threshold and filters"):
        _normalize_expected_output({**_BASE, "any_of": [{"Threshold": 1}, {"Threshold": 2, **fields}]})


def test_simulated_user_is_told_the_range_of_each_between_combination() -> None:
    prompt = _simulated_user_prompt(
        {
            "Metric": "Net Sales (net_sales)",
            "Operator": "BETWEEN",
            "any_of": [{"threshold_from": 1, "threshold_to": 9}, {"threshold_from": 2, "threshold_to": 8}],
        }
    )
    assert "threshold=one of the combinations in rule 9" in prompt
    assert "A) threshold=between 1 and 9 | B) threshold=between 2 and 8" in prompt


def test_simulated_user_goal_uses_a_value_every_combination_replaces() -> None:
    prompt = _simulated_user_prompt(
        {
            **_BASE,
            "Recipient(s)": "base@example.com",
            "any_of": [
                {"Threshold": 1, "Recipient(s)": "alt@example.com"},
                {"Threshold": 2, "Recipient(s)": "alt@example.com"},
            ],
        }
    )
    assert "alt@example.com" in prompt
    assert "base@example.com" not in prompt


def test_simulated_user_goal_omits_the_filters_the_combinations_replace() -> None:
    prompt = _simulated_user_prompt({**_BASE, "Filters": [_US], "any_of": [{"Filters": []}, {"Threshold": 3}]})
    goal = next(line for line in prompt.splitlines() if line.startswith("1. "))
    assert "filters=" not in goal
    assert "A) threshold=1000, filters=no filter at all" in prompt


def test_any_of_option_replaces_every_spelling_of_a_field() -> None:
    expected = _normalize_expected_output(
        {
            "recipients": ["a@x.com"],
            "metric_id": "net_sales",
            "dashboard_id": "d1",
            "any_of": [
                {"Recipient(s)": "b@x.com", "Metric": "Other (other)", "Dashboard": "D (d2)", "Threshold": n}
                for n in (1, 2)
            ],
        }
    )
    for option in expected.alternatives:
        assert (option.recipients, option.metric_id, option.dashboard_id) == (["b@x.com"], "other", "d2")


def test_any_of_display_spelling_is_read() -> None:
    expected = _normalize_expected_output({**_BASE, "Any of": [{"Threshold": 1}, {"Threshold": 2}]})
    assert [a.threshold for a in expected.alternatives] == [1, 2]


def test_any_of_option_for_the_current_user_resolves_it() -> None:
    created = ChatResult.model_validate(
        {
            "text_response": "",
            "toolCallEvents": [
                {
                    "functionName": "create_metric_alert",
                    "functionArguments": json.dumps(
                        {**_CREATE_ARGS, "external_recipients": [], "internal_recipients": ["u1"]}
                    ),
                    "result": '{"id": "alert-1"}',
                }
            ],
        }
    )
    client = MagicMock()
    client.send_message.return_value = created
    expected = {**_BASE, "Filters": [], "Recipient(s)": "me", "any_of": [{"Threshold": 1000}, {"Threshold": 5}]}
    with patch("gooddata_eval.core.agentic.alert_skill._resolve_current_user_id", return_value="u1") as mock_resolve:
        run, _, _ = _run(client, expected)
    mock_resolve.assert_called_once()
    assert run.eval.strict_pass


def test_too_many_any_of_options_fail_early() -> None:
    with pytest.raises(ValueError, match="at most 26"):
        _normalize_expected_output({**_BASE, "any_of": [{"Threshold": n} for n in range(27)]})


def test_no_alert_item_may_not_check_a_first_proposal() -> None:
    with pytest.raises(ValueError, match="expect_alert: false"):
        _normalize_expected_output(
            {"Expect alert": False, "Recipient(s)": "a@x.com", "check_first_proposal": ["recipients"]}
        )


def test_catalog_from_dict_reads_any_of_and_first_proposal_fields() -> None:
    alert = CatalogMetricAlert.from_dict(
        {"filters": [], "check_first_proposal": ["filters"], "any_of": [{"threshold": 1}, {"threshold": 2}]}
    )
    assert alert.check_first_proposal == ("filters",)
    assert [a.threshold for a in alert.alternatives] == [1, 2]
    with pytest.raises(ValueError):
        CatalogMetricAlert.from_dict({"filters": [], "check_first_proposal": "filters"})


# --- cleanup of an alert whose create event never reached the harness ---------------------------


def test_named_ids_ignore_arguments_that_are_not_an_object() -> None:
    events = _events({"functionName": "prepare_metric_alert_proposal", "functionArguments": "[1]", "result": "{}"})
    assert _named_automation_ids(events) == set()


def test_named_ids_skip_an_id_that_is_not_a_string() -> None:
    # A list is unhashable; it must not stop the cleanup of the ids that are valid.
    events = _events(
        {"functionName": "prepare_metric_alert_proposal", "functionArguments": '{"automation_id": []}', "result": "{}"},
        {"functionName": "create_metric_alert", "functionArguments": '{"automation_id": 7}', "result": "{}"},
        {
            "functionName": "create_metric_alert",
            "functionArguments": '{"automation_id": "net-sales-below"}',
            "result": "{}",
        },
    )
    assert _named_automation_ids(events) == {"net-sales-below"}


@pytest.mark.parametrize(
    "body",
    [
        {},
        [],
        {"data": None},
        {"data": "a1"},
        {"data": [{"id": "a1"}, {"name": "x"}]},
        {"data": [{"id": 5}]},
        {"data": [7]},
    ],
)
def test_a_malformed_automation_listing_lists_nothing(body: object) -> None:
    # Read as an empty workspace, it would make an alert that existed before the run look new.
    page = MagicMock(json=MagicMock(return_value=body))
    with patch("gooddata_eval.core.agentic.alert_skill.httpx.get", return_value=page):
        assert _list_automation_ids("http://host", "tok", "ws1") is None


def test_an_empty_automation_listing_is_an_empty_workspace() -> None:
    page = MagicMock(json=MagicMock(return_value={"data": []}))
    with patch("gooddata_eval.core.agentic.alert_skill.httpx.get", return_value=page):
        assert _list_automation_ids("http://host", "tok", "ws1") == set()


def test_best_run_is_a_passing_run() -> None:
    expected = {**_BASE, "any_of": [{"Threshold": 1}, {"Threshold": 2}]}

    def created(args: dict) -> ChatResult:
        return ChatResult.model_validate(
            {
                "toolCallEvents": [
                    {
                        "functionName": "create_metric_alert",
                        "functionArguments": json.dumps(args),
                        "result": '{"id": "a"}',
                    }
                ]
            }
        )

    client = MagicMock()
    client.create_conversation.return_value = "conv-2"
    client.send_message.side_effect = [
        created({**_CREATE_ARGS, "threshold": 3}),
        created({**_CREATE_ARGS, "threshold": 2}),
    ]
    with (
        patch("gooddata_eval.core.agentic.alert_skill.ChatClient", return_value=client),
        patch("gooddata_eval.core.agentic.alert_skill._delete_alert"),
    ):
        summary = run_agentic_alert_skill(
            host="http://host",
            token="tok",
            workspace_id="ws1",
            question="q",
            expected_output=expected,
            k=2,
            initial_conversation_id="conv-1",
        )
    first, second = summary.run_results
    assert not first.eval.strict_pass and second.eval.strict_pass
    assert summary.best is second


def test_automation_listing_reads_every_page() -> None:
    pages = [[{"id": f"a{n}"} for n in range(500)], [{"id": "last"}]]
    responses = [MagicMock(json=MagicMock(return_value={"data": page})) for page in pages]
    with patch("gooddata_eval.core.agentic.alert_skill.httpx.get", side_effect=responses) as mock_get:
        ids = _list_automation_ids("http://host", "tok", "ws1")
    assert ids is not None and len(ids) == 501 and "last" in ids
    assert [c.kwargs["params"]["page"] for c in mock_get.call_args_list] == [0, 1]


def test_automation_listing_that_cannot_finish_lists_nothing() -> None:
    # A server that ignores the page number returns the first page forever: a partial list is no list.
    page = MagicMock(json=MagicMock(return_value={"data": [{"id": f"a{n}"} for n in range(500)]}))
    with patch("gooddata_eval.core.agentic.alert_skill.httpx.get", return_value=page):
        assert _list_automation_ids("http://host", "tok", "ws1") is None


def test_alert_named_in_a_proposal_is_deleted_when_its_create_event_is_missing() -> None:
    proposal = ChatResult.model_validate(
        {
            "text_response": "",
            "alertProposals": [{"cta": "Should I create this alert?"}],
            "toolCallEvents": [_proposal_event([], [], automation_id="net-sales-below")],
        }
    )
    client = MagicMock()
    client.send_message.side_effect = [proposal] + [_turn("Done.")] * 5
    with patch(
        "gooddata_eval.core.agentic.alert_skill._automation_ids",
        side_effect=[{"other-alert", "net-sales-below-old"}, {"other-alert", "net-sales-below"}],
    ):
        _, _, mock_delete = _run(client, {**_BASE, "Filters": []})
    assert [c.args[2] for c in mock_delete.call_args_list] == ["net-sales-below"]


def test_named_alert_that_existed_before_the_run_is_kept() -> None:
    proposal = ChatResult.model_validate(
        {
            "text_response": "",
            "alertProposals": [{"cta": "Should I create this alert?"}],
            "toolCallEvents": [_proposal_event([], [], automation_id="shared-alert")],
        }
    )
    client = MagicMock()
    client.send_message.side_effect = [proposal] + [_turn("Done.")] * 5
    with patch("gooddata_eval.core.agentic.alert_skill._automation_ids", return_value={"shared-alert"}):
        _, _, mock_delete = _run(client, {**_BASE, "Filters": []})
    assert mock_delete.call_args_list == []


def test_first_proposal_without_a_filters_key_reads_as_no_filter() -> None:
    expected = {**_BASE, "Time window/Filters": "None (All time)", "check_first_proposal": ["filters", "recipients"]}
    event = {
        "functionName": "prepare_metric_alert_proposal",
        "functionArguments": json.dumps({"recipients": [{"id": None, "email": "admin@gooddata.com"}]}),
        "result": json.dumps({"success": True, "alert_proposal_ref": "p1"}),
    }
    ev = _evaluate_alert(
        _normalize_expected_output(expected), {**_CREATE_ARGS, "filters": []}, True, MagicMock(), None, [_events(event)]
    )
    assert ev.checks()["alert_initial_filters_correct"] is True
    assert ev.checks()["alert_initial_recipients_correct"] is True

# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.agentic.forecasting import (
    ForecastingAssertionError,
    _evaluate_run,
    _extract_forecast_calls,
    _metric_uris,
    evaluate_agentic_forecasting,
    run_agentic_forecasting,
)
from gooddata_eval.core.models import ChatResult

_MODULE = "gooddata_eval.core.agentic.forecasting"

_EXPECTED = {"metric": "metric/spend", "forecast_period": 3}


def _viz_args(*, period=3, enabled=True, metric="metric/spend", confidence=0.95, seasonal=False) -> dict:
    return {
        "visualization": {
            "type": "line_chart",
            "title": "Spend forecast",
            "query": {
                "fields": {
                    "m_spend": {"using": metric},
                    "d_month": {"using": "label/process_date.month"},
                },
                "filter_by": {},
            },
            "metrics": ["m_spend"],
            "view_by": ["d_month"],
            "config": {
                "forecast_enabled": enabled,
                "forecast_period": period,
                "forecast_confidence": confidence,
                "forecast_seasonal": seasonal,
            },
        }
    }


def _tc(name: str, args: dict | None = None, result: str | None = None):
    tc = MagicMock()
    tc.function_name = name
    tc.call_ts = None
    tc.result_ts = None
    tc.index = None
    tc.parsed_arguments = lambda a=args: a or {}
    tc.result = result
    tc.parsed_result = lambda r=result: __import__("json").loads(r) if r else None
    return tc


_OK_FORECAST = '{"success": true, "data": {"points": [{"value": 1}], "truncated": false}, "error": null}'


def _chat(tool_calls, text="Here is the forecast.", ended=True) -> ChatResult:
    """A real ChatResult, so render_answer_text sees every field it reads."""
    result = ChatResult.model_validate({"textResponse": text, "responseId": "resp-1"})
    result.stream_ended = ended
    result.turn_wall_clock_sec = 4.2
    # Assigned after validation: these are hand-built tool-call doubles, not payload.
    result.tool_call_events = tool_calls
    return result


# ── extraction ──────────────────────────────────────────────────────────────


def test_extract_pairs_the_execute_with_the_visualization_it_followed():
    """A new chart clears the previous forecast: picking the last of each independently
    would pair a fresh visualization with a stale result."""
    calls = [
        _tc("create_adhoc_visualization", _viz_args(period=1)),
        _tc("execute_forecast", {"visualization_ref": "viz_1"}, _OK_FORECAST),
        _tc("create_adhoc_visualization", _viz_args(period=3)),
    ]
    viz, result = _extract_forecast_calls(calls)

    assert viz["config"]["forecast_period"] == 3
    assert result is None


def test_extract_unwraps_the_visualization_argument():
    viz, _ = _extract_forecast_calls([_tc("create_adhoc_visualization", _viz_args())])
    assert viz["type"] == "line_chart"


def test_metric_uris_resolves_aliases_and_ignores_dimensions():
    viz, _ = _extract_forecast_calls([_tc("create_adhoc_visualization", _viz_args())])
    assert _metric_uris(viz) == {"metric/spend"}


def test_metric_uris_handles_a_bare_uri_field():
    """Tool-call arguments are raw JSON, where a field may be a plain string rather than
    the object core.scoring's parsed model always has."""
    viz = {"query": {"fields": {"m": "metric/spend"}}, "metrics": ["m"]}
    assert _metric_uris(viz) == {"metric/spend"}


# ── scoring ─────────────────────────────────────────────────────────────────


def _evaluate(viz=None, result=None, expected=None, turn_completed=True):
    return _evaluate_run(viz, result, expected if expected is not None else _EXPECTED, turn_completed)


def _viz(**kw):
    return _viz_args(**kw)["visualization"]


def test_a_correct_forecast_passes_every_check():
    ev = _evaluate(_viz(), {"success": True})
    assert ev.strict_pass is True
    assert ev.asserted == ["forecast_period", "metric"]


def test_the_wrong_horizon_fails_on_period_alone():
    """The number the agent chose is in the tool call, so 'next 3 months' is checkable
    exactly -- no judge, no paraphrase tolerance."""
    ev = _evaluate(_viz(period=6), {"success": True})
    assert ev.period_correct is False
    assert ev.metric_correct is True
    assert ev.strict_pass is False


def test_forecasting_the_wrong_measure_fails_on_metric_alone():
    ev = _evaluate(_viz(metric="metric/orders"), {"success": True})
    assert ev.metric_correct is False
    assert ev.period_correct is True


def test_forecast_enabled_must_be_explicitly_true():
    """The tool refuses on forecast_enabled=false, and treats an unset value the same way,
    so only an explicit true counts."""
    assert _evaluate(_viz(enabled=None), {"success": True}).forecast_enabled is False
    assert _evaluate(_viz(enabled=False), {"success": True}).forecast_enabled is False
    assert _evaluate(_viz(enabled=True), {"success": True}).forecast_enabled is True


def test_an_unstated_expectation_neither_fails_nor_silently_passes():
    """A fixture that pins nothing must not fail, but the report has to say nothing was
    checked -- otherwise it reads identically to a run where everything matched."""
    ev = _evaluate(_viz(period=99, metric="metric/anything"), {"success": True}, expected={})
    assert ev.period_correct is True
    assert ev.metric_correct is True
    assert ev.asserted == []


def test_a_failed_execution_is_not_a_success():
    ev = _evaluate(_viz(), {"success": False, "error": "no forecast for you"})
    assert ev.executed is True
    assert ev.success is False
    assert ev.strict_pass is False


def test_never_reaching_execute_is_not_triggered_by_a_chart_alone():
    ev = _evaluate(_viz(), None)
    assert ev.executed is False
    assert ev.success is False


def test_an_integer_valued_float_period_still_matches():
    """The AAC config is JSON, so 3 may arrive as 3.0."""
    assert _evaluate(_viz(period=3.0), {"success": True}).period_correct is True


# ── run loop ────────────────────────────────────────────────────────────────


def _run(side_effect, *, k=1, expected=None, max_iterations=4):
    client = MagicMock()
    client.create_conversation.side_effect = [f"conv-{i}" for i in range(1, k + 2)]
    client.send_message.side_effect = side_effect
    with (
        patch(f"{_MODULE}.ChatClient", return_value=client),
        patch(f"{_MODULE}.generate_simulated_forecast_response", return_value="use spend, 3 months"),
    ):
        return run_agentic_forecasting(
            host="http://h",
            token="tok",
            workspace_id="ws1",
            question="Forecast spend for 3 months",
            expected_output=expected if expected is not None else _EXPECTED,
            k=k,
            max_iterations=max_iterations,
        )


def test_a_single_turn_forecast_passes():
    calls = [_tc("create_adhoc_visualization", _viz_args()), _tc("execute_forecast", {}, _OK_FORECAST)]
    summary = _run([_chat(calls)])
    assert summary.pass_at_k is True
    assert summary.best.evaluation.disambiguated is False


def test_a_clarifying_question_is_answered_and_the_run_continues():
    """Observed live: the agent asks which Spend metric before building anything."""
    calls = [_tc("create_adhoc_visualization", _viz_args()), _tc("execute_forecast", {}, _OK_FORECAST)]
    summary = _run([_chat([], text="Which Spend metric did you mean?"), _chat(calls)])
    assert summary.pass_at_k is True
    assert summary.best.evaluation.disambiguated is True


def test_the_loop_stops_at_max_iterations_without_a_forecast():
    summary = _run([_chat([], text="Still thinking")] * 4, max_iterations=4)
    assert summary.pass_at_k is False
    assert summary.best.evaluation.executed is False


def test_an_empty_response_ends_the_run_immediately():
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    client.send_message.return_value = _chat([], text="")
    with (
        patch(f"{_MODULE}.ChatClient", return_value=client),
        patch(f"{_MODULE}.generate_simulated_forecast_response") as sim,
    ):
        run_agentic_forecasting(
            host="http://h",
            token="tok",
            workspace_id="ws1",
            question="q",
            expected_output=_EXPECTED,
        )
    assert client.send_message.call_count == 1
    sim.assert_not_called()


def test_a_chat_error_ends_the_run_and_keeps_what_the_partial_carried():
    error = RuntimeError("stream died")
    error.partial_result = _chat(
        [_tc("create_adhoc_visualization", _viz_args()), _tc("execute_forecast", {}, _OK_FORECAST)]
    )
    summary = _run([error])
    # The forecast landed before the stream broke, so it is still scored -- but the turn
    # did not complete, which strict_pass requires.
    assert summary.best.evaluation.executed is True
    assert summary.best.evaluation.turn_completed is False


def test_a_chat_error_on_a_later_run_does_not_discard_the_earlier_one():
    calls = [_tc("create_adhoc_visualization", _viz_args()), _tc("execute_forecast", {}, _OK_FORECAST)]
    summary = _run([_chat(calls), RuntimeError("boom")], k=2)
    assert len(summary.run_results) == 2
    assert summary.pass_at_k is True


def test_k_must_be_at_least_one():
    with pytest.raises(ValueError, match="k must be >= 1"):
        run_agentic_forecasting(host="h", token="t", workspace_id="w", question="q", expected_output={}, k=0)


# ── evaluate_* wrapper ──────────────────────────────────────────────────────


def _evaluate_item(calls):
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    client.send_message.return_value = _chat(calls)
    with patch(f"{_MODULE}.ChatClient", return_value=client):
        return evaluate_agentic_forecasting(
            host="http://h",
            token="tok",
            workspace_id="ws1",
            question="Forecast spend for 3 months",
            expected_output=_EXPECTED,
        )


def test_detail_reports_the_config_the_agent_chose():
    outcome = _evaluate_item(
        [_tc("create_adhoc_visualization", _viz_args()), _tc("execute_forecast", {}, _OK_FORECAST)]
    )
    assert outcome.detail["actual_forecast_config"]["forecast_period"] == 3
    assert outcome.detail["actual_metrics"] == ["metric/spend"]
    assert outcome.detail["asserted"] == ["forecast_period", "metric"]
    assert "latency_breakdown" in outcome.detail
    assert outcome.runs_passed == 1


def test_a_wrong_horizon_raises_naming_what_the_agent_actually_did():
    with pytest.raises(ForecastingAssertionError) as exc_info:
        _evaluate_item(
            [_tc("create_adhoc_visualization", _viz_args(period=12)), _tc("execute_forecast", {}, _OK_FORECAST)]
        )

    error = exc_info.value
    assert "period_correct=False" in str(error)
    assert error.detail["actual_forecast_config"]["forecast_period"] == 12
    assert error.runs_passed == 0
    assert error.conversation_id == "conv-1"


# ── confidence and seasonality ──────────────────────────────────────────────


def test_confidence_is_checked_when_pinned():
    expected = {"forecast_confidence": 0.99}
    assert _evaluate(_viz(confidence=0.99), {"success": True}, expected=expected).confidence_correct is True
    assert _evaluate(_viz(confidence=0.95), {"success": True}, expected=expected).confidence_correct is False


def test_seasonality_is_checked_when_pinned():
    expected = {"forecast_seasonal": True}
    assert _evaluate(_viz(seasonal=True), {"success": True}, expected=expected).seasonal_correct is True
    assert _evaluate(_viz(seasonal=False), {"success": True}, expected=expected).seasonal_correct is False


def test_an_absent_seasonal_counts_as_the_tools_default():
    """The tool defaults seasonal to false, so an agent that leaves it alone has asked for
    a non-seasonal forecast -- failing that would penalise correct behaviour."""
    viz = _viz()
    del viz["config"]["forecast_seasonal"]
    assert _evaluate(viz, {"success": True}, expected={"forecast_seasonal": False}).seasonal_correct is True


def test_confidence_and_seasonality_are_unasserted_by_default():
    ev = _evaluate(_viz(confidence=0.5, seasonal=True), {"success": True})
    assert ev.confidence_correct is True
    assert ev.seasonal_correct is True
    assert "forecast_confidence" not in ev.asserted
    assert "forecast_seasonal" not in ev.asserted


# ── cross-turn extraction ───────────────────────────────────────────────────


def test_a_chart_built_on_an_earlier_turn_is_still_the_one_scored():
    """The agent may build the chart on one turn and forecast on the next -- reading only
    the current turn's calls would drop the visualization the forecast actually ran on and
    fail a correct run for an empty config."""
    summary = _run(
        [
            _chat([_tc("create_adhoc_visualization", _viz_args())], text="Building the chart, one moment."),
            _chat([_tc("execute_forecast", {"visualization_ref": "viz_1"}, _OK_FORECAST)]),
        ]
    )

    assert summary.best.evaluation.executed is True
    assert summary.best.evaluation.period_correct is True
    assert summary.best.evaluation.metric_correct is True
    assert summary.pass_at_k is True

# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
import json
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.agentic.what_if import (
    WhatIfAssertionError,
    _adjustments,
    _evaluate_run,
    _extract_what_if_calls,
    evaluate_agentic_what_if,
    run_agentic_what_if,
)
from gooddata_eval.core.models import ChatResult

_MODULE = "gooddata_eval.core.agentic.what_if"

_BASE_MAQL = "SELECT SUM({fact/price} * 1.10 * {fact/quantity})"
_EXPECTED = {"metric_id": "revenue", "scenario_maql": _BASE_MAQL}


def _create_args(*, metric="revenue", maql=_BASE_MAQL, scenarios=1, baseline=True, label="Scenario A") -> dict:
    return {
        "visualization_ref": "viz_1",
        "include_baseline": baseline,
        "scenarios": [
            {
                "label": f"{label} {i}" if scenarios > 1 else label,
                "adjustments": [{"metric_id": metric, "metric_type": "metric", "scenario_maql": maql}],
            }
            for i in range(scenarios)
        ],
    }


_OK_EXECUTE = json.dumps(
    {
        "success": True,
        "scenario_results": [
            {"label": "Baseline", "data": {"rows": [[100]]}, "error": None},
            {"label": "Scenario A", "data": {"rows": [[110]]}, "error": None},
        ],
        "error": None,
    }
)


def _tc(name: str, args: dict | None = None, result: str | None = None):
    tc = MagicMock()
    tc.function_name = name
    tc.call_ts = None
    tc.result_ts = None
    tc.index = None
    tc.parsed_arguments = lambda a=args: a or {}
    tc.result = result
    tc.parsed_result = lambda r=result: json.loads(r) if r else None
    return tc


def _chat(tool_calls, text="Here is the scenario.", ended=True) -> ChatResult:
    """A real ChatResult, so render_answer_text sees every field it reads."""
    result = ChatResult.model_validate({"textResponse": text, "responseId": "resp-1"})
    result.stream_ended = ended
    result.turn_wall_clock_sec = 5.1
    result.tool_call_events = tool_calls
    return result


def _pair(**kw):
    return [
        _tc("create_what_if_scenario", _create_args(**kw)),
        _tc("execute_what_if_scenario", {"scenario_ref": "wia_1"}, _OK_EXECUTE),
    ]


# ── extraction ──────────────────────────────────────────────────────────────


def test_extract_pairs_the_execute_with_the_spec_it_followed():
    """A new spec clears the previous execution: scoring a fresh scenario against a stale
    result would credit work the agent redid."""
    calls = [
        _tc("create_what_if_scenario", _create_args(metric="orders")),
        _tc("execute_what_if_scenario", {}, _OK_EXECUTE),
        _tc("create_what_if_scenario", _create_args(metric="revenue")),
    ]
    create, result = _extract_what_if_calls(calls)

    assert create["scenarios"][0]["adjustments"][0]["metric_id"] == "revenue"
    assert result is None


def test_adjustments_flatten_across_scenarios():
    """Scenario grouping is not asserted -- a fixture cares that the right measure was
    adjusted the right way, not which label it landed under."""
    args = _create_args(scenarios=3)
    assert len(_adjustments(args)) == 3


def test_adjustments_tolerate_a_malformed_scenario_list():
    assert _adjustments({"scenarios": "not a list"}) == []
    assert _adjustments({"scenarios": [None, {"adjustments": None}]}) == []
    assert _adjustments(None) == []


# ── scoring ─────────────────────────────────────────────────────────────────


def _evaluate(create=None, result=None, expected=None, turn_completed=True):
    return _evaluate_run(create, result, expected if expected is not None else _EXPECTED, turn_completed)


def test_a_correct_scenario_passes_every_check():
    ev = _evaluate(_create_args(), {"success": True})
    assert ev.strict_pass is True
    assert ev.asserted == ["metric_id", "scenario_maql"]


def test_adjusting_the_wrong_measure_fails_both_metric_and_maql():
    """The MAQL check is scoped to adjustments on the expected measure, so adjusting the
    wrong one leaves it nothing valid to match. Both checks failing is the honest reading:
    the expected measure was not adjusted at all, correctly or otherwise."""
    ev = _evaluate(_create_args(metric="orders"), {"success": True})
    assert ev.metric_correct is False
    assert ev.maql_correct is False


def test_the_wrong_adjustment_fails_on_maql():
    ev = _evaluate(_create_args(maql="SELECT SUM({fact/price} * 2.0 * {fact/quantity})"), {"success": True})
    assert ev.maql_correct is False
    assert ev.metric_correct is True


def test_maql_is_compared_normalized_not_literally():
    """metric_skill's normalizer decides this, so whitespace and casing do not."""
    noisy = "select   SUM( {fact/price}  * 1.10 * {fact/quantity} )"
    assert _evaluate(_create_args(maql=noisy), {"success": True}).maql_correct is True


def test_several_expressions_can_be_equally_correct():
    """`* 1.1` and `* 1.10` are the same uplift, so a fixture may accept either."""
    expected = {
        "scenario_maql": [
            "SELECT SUM({fact/price} * 1.1 * {fact/quantity})",
            "SELECT SUM({fact/price} * 1.10 * {fact/quantity})",
        ]
    }
    assert _evaluate(_create_args(), {"success": True}, expected=expected).maql_correct is True


def test_scenario_count_is_checked_when_pinned():
    expected = {**_EXPECTED, "scenarios": 2}
    assert _evaluate(_create_args(scenarios=2), {"success": True}, expected=expected).scenario_count_correct is True
    assert _evaluate(_create_args(scenarios=1), {"success": True}, expected=expected).scenario_count_correct is False


def test_an_absent_include_baseline_counts_as_the_tools_default():
    """The tool defaults include_baseline to true, so an agent that omits it has still
    asked for a baseline -- failing that would penalise correct behaviour."""
    expected = {"include_baseline": True}
    args = _create_args()
    del args["include_baseline"]
    assert _evaluate(args, {"success": True}, expected=expected).baseline_correct is True


def test_explicitly_dropping_the_baseline_is_caught_when_pinned():
    expected = {"include_baseline": True}
    assert _evaluate(_create_args(baseline=False), {"success": True}, expected=expected).baseline_correct is False


def test_an_unstated_expectation_neither_fails_nor_silently_passes():
    ev = _evaluate(_create_args(metric="anything", maql="SELECT 1"), {"success": True}, expected={})
    assert ev.strict_pass is True
    assert ev.asserted == []


def test_a_failed_execution_is_not_a_success():
    ev = _evaluate(_create_args(), {"success": False, "error": "boom"})
    assert ev.executed is True
    assert ev.success is False
    assert ev.strict_pass is False


def test_a_spec_that_never_executed_is_triggered_but_not_executed():
    ev = _evaluate(_create_args(), None)
    assert ev.triggered is True
    assert ev.executed is False


# ── run loop ────────────────────────────────────────────────────────────────


def _run(side_effect, *, k=1, expected=None, max_iterations=4):
    client = MagicMock()
    client.create_conversation.side_effect = [f"conv-{i}" for i in range(1, k + 2)]
    client.send_message.side_effect = side_effect
    with (
        patch(f"{_MODULE}.ChatClient", return_value=client),
        patch(f"{_MODULE}.generate_simulated_what_if_response", return_value="use revenue, +10%"),
    ):
        return run_agentic_what_if(
            host="http://h",
            token="tok",
            workspace_id="ws1",
            question="What if revenue rose 10%?",
            expected_output=expected if expected is not None else _EXPECTED,
            k=k,
            max_iterations=max_iterations,
        )


def test_a_single_turn_scenario_passes():
    summary = _run([_chat(_pair())])
    assert summary.pass_at_k is True
    assert summary.best.evaluation.disambiguated is False


def test_a_clarifying_question_is_answered_and_the_run_continues():
    """Observed live: 'I need to confirm which Spend calculation you want to adjust'."""
    summary = _run([_chat([], text="Which Spend metric did you mean?"), _chat(_pair())])
    assert summary.pass_at_k is True
    assert summary.best.evaluation.disambiguated is True


def test_the_loop_stops_at_max_iterations_without_a_scenario():
    summary = _run([_chat([], text="Still thinking")] * 4, max_iterations=4)
    assert summary.pass_at_k is False
    assert summary.best.evaluation.triggered is False


def test_an_empty_response_ends_the_run_immediately():
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    client.send_message.return_value = _chat([], text="")
    with (
        patch(f"{_MODULE}.ChatClient", return_value=client),
        patch(f"{_MODULE}.generate_simulated_what_if_response") as sim,
    ):
        run_agentic_what_if(host="http://h", token="tok", workspace_id="ws1", question="q", expected_output=_EXPECTED)
    assert client.send_message.call_count == 1
    sim.assert_not_called()


def test_a_chat_error_on_a_later_run_does_not_discard_the_earlier_one():
    summary = _run([_chat(_pair()), RuntimeError("boom")], k=2)
    assert len(summary.run_results) == 2
    assert summary.pass_at_k is True


def test_k_must_be_at_least_one():
    with pytest.raises(ValueError, match="k must be >= 1"):
        run_agentic_what_if(host="h", token="t", workspace_id="w", question="q", expected_output={}, k=0)


# ── evaluate_* wrapper ──────────────────────────────────────────────────────


def _evaluate_item(calls):
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    client.send_message.return_value = _chat(calls)
    with patch(f"{_MODULE}.ChatClient", return_value=client):
        return evaluate_agentic_what_if(
            host="http://h",
            token="tok",
            workspace_id="ws1",
            question="What if revenue rose 10%?",
            expected_output=_EXPECTED,
        )


def test_detail_reports_the_adjustments_the_agent_asked_for():
    outcome = _evaluate_item(_pair())
    assert outcome.detail["actual_adjustments"][0]["metric_id"] == "revenue"
    assert outcome.detail["actual_scenario_labels"] == ["Scenario A"]
    assert outcome.detail["asserted"] == ["metric_id", "scenario_maql"]
    assert "latency_breakdown" in outcome.detail
    assert outcome.runs_passed == 1


def test_a_wrong_adjustment_raises_naming_what_the_agent_actually_did():
    with pytest.raises(WhatIfAssertionError) as exc_info:
        _evaluate_item(_pair(maql="SELECT SUM({fact/price} * 3 * {fact/quantity})"))

    error = exc_info.value
    assert "maql_correct=False" in str(error)
    assert "* 3 *" in str(error)
    assert error.runs_passed == 0
    assert error.conversation_id == "conv-1"


def test_a_spec_built_on_an_earlier_turn_is_still_the_one_scored():
    """The agent may build the spec on one turn and execute it on the next -- reading only
    the current turn's calls would drop the scenario the execution actually ran and fail a
    correct run for having no adjustments."""
    summary = _run(
        [
            _chat([_tc("create_what_if_scenario", _create_args())], text="Preparing the scenario."),
            _chat([_tc("execute_what_if_scenario", {"scenario_ref": "wia_1"}, _OK_EXECUTE)]),
        ]
    )

    assert summary.best.evaluation.executed is True
    assert summary.best.evaluation.metric_correct is True
    assert summary.best.evaluation.maql_correct is True
    assert summary.pass_at_k is True


def test_the_maql_must_match_on_the_adjustment_that_matched_the_metric():
    """Checking the two independently lets two failures score as a pass: a wrong adjustment
    on the right measure and a right adjustment on the wrong measure would satisfy one
    check each."""
    create = {
        "visualization_ref": "viz_1",
        "include_baseline": True,
        "scenarios": [
            {
                "label": "Scenario A",
                "adjustments": [
                    # Right metric, wrong adjustment.
                    {"metric_id": "revenue", "metric_type": "metric", "scenario_maql": "SELECT 0"},
                    # Right adjustment, wrong metric.
                    {"metric_id": "orders", "metric_type": "metric", "scenario_maql": _BASE_MAQL},
                ],
            }
        ],
    }
    ev = _evaluate(create, {"success": True})

    assert ev.metric_correct is True  # revenue was adjusted
    assert ev.maql_correct is False  # but not with the expected expression
    assert ev.strict_pass is False


def test_the_maql_still_matches_when_the_right_adjustment_is_on_the_right_metric():
    """The pairing must not reject a correct spec that also adjusts something else."""
    create = {
        "visualization_ref": "viz_1",
        "include_baseline": True,
        "scenarios": [
            {
                "label": "Scenario A",
                "adjustments": [
                    {"metric_id": "orders", "metric_type": "metric", "scenario_maql": "SELECT 0"},
                    {"metric_id": "revenue", "metric_type": "metric", "scenario_maql": _BASE_MAQL},
                ],
            }
        ],
    }
    assert _evaluate(create, {"success": True}).strict_pass is True

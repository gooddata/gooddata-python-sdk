# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
import json
from contextlib import contextmanager
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.agentic.anomaly_detection import (
    AnomalyDetectionAssertionError,
    _build_clarification_prompt,
    _evaluate_run,
    _extract_anomaly_calls,
    _inferred_granularity,
    _metric_uris,
    _point_count,
    evaluate_agentic_anomaly_detection,
    run_agentic_anomaly_detection,
)
from gooddata_eval.core.models import ChatResult

_MODULE = "gooddata_eval.core.agentic.anomaly_detection"

_EXPECTED = {"metric": "metric/spend", "granularity": "MONTH"}


def _viz_args(*, metric="metric/spend", dimension="label/process_date.month", filter_granularity="MONTH") -> dict:
    """Shaped like the chart observed live for an anomaly question."""
    query: dict = {
        "fields": {"d_month": {"using": dimension}, "m_spend": {"using": metric}},
        "filter_by": {},
    }
    if filter_granularity:
        query["filter_by"] = {
            "f_window": {
                "to": 0,
                "from": -23,
                "type": "date_filter",
                "using": "dataset/process_date",
                "granularity": filter_granularity,
            }
        }
    return {
        "visualization": {
            "type": "line_chart",
            "title": "Monthly Spend - anomaly detection",
            "query": query,
            "metrics": ["m_spend"],
            "view_by": ["d_month"],
        }
    }


_OK_DETECT = json.dumps(
    {
        "success": True,
        "data": {
            "attribute": [],
            "values": {"m_spend": []},
            "measure_ids": ["m_spend"],
            "points": [],
            "point_count": 0,
            "truncated": False,
        },
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


def _chat(tool_calls, text="No months were flagged.", ended=True) -> ChatResult:
    """A real ChatResult, so render_answer_text sees every field it reads."""
    result = ChatResult.model_validate({"textResponse": text, "responseId": "resp-1"})
    result.stream_ended = ended
    result.turn_wall_clock_sec = 6.3
    result.tool_call_events = tool_calls
    return result


def _pair(**kw):
    return [
        _tc("create_adhoc_visualization", _viz_args(**kw)),
        _tc("execute_anomaly_detection", {"visualization_ref": "viz_1", "max_points": 200}, _OK_DETECT),
    ]


def _viz(**kw):
    return _viz_args(**kw)["visualization"]


# ── extraction ──────────────────────────────────────────────────────────────


def test_extract_pairs_the_detection_with_the_chart_it_followed():
    """A new chart clears the previous detection: scoring a fresh series against a run
    that never touched it would credit work the agent redid."""
    calls = [
        _tc("create_adhoc_visualization", _viz_args(metric="metric/orders")),
        _tc("execute_anomaly_detection", {}, _OK_DETECT),
        _tc("create_adhoc_visualization", _viz_args(metric="metric/spend")),
    ]
    viz, result = _extract_anomaly_calls(calls)

    assert viz["query"]["fields"]["m_spend"]["using"] == "metric/spend"
    assert result is None


def test_point_count_is_read_off_the_result():
    _, result = _extract_anomaly_calls(_pair())
    assert _point_count(result) == 0
    assert _point_count(None) is None
    assert _point_count({"data": "not a dict"}) is None


# ── granularity inference ───────────────────────────────────────────────────


def test_granularity_comes_from_the_field_token_first():
    """Field references are read before the date filter, as the service reads them."""
    assert _inferred_granularity(_viz(dimension="label/process_date.month")) == "MONTH"
    assert _inferred_granularity(_viz(dimension="label/process_date.quarter")) == "QUARTER"
    assert _inferred_granularity(_viz(dimension="label/process_date.year")) == "YEAR"
    assert _inferred_granularity(_viz(dimension="label/process_date.hour")) == "HOUR"


def test_a_reference_naming_two_granularities_resolves_to_its_suffix():
    """A snake_case `first_day_quarter.month` tokenizes to {first, day, quarter, month},
    where "day", "quarter" and "month" all map. gen-ai iterates a set and returns whichever
    comes first, so its own answer there is not stable; taking the last token reads the
    suffix, which is what a dotted label means, and is the same every run.

    This is rare -- no label in the eval workspace names two granularities -- but a scorer
    must not be a coin flip even where the thing it scores is one.
    """
    assert _inferred_granularity(_viz(dimension="label/first_day_quarter.month")) == "MONTH"
    assert _inferred_granularity(_viz(dimension="label/day_of_week")) == "WEEK"


def test_a_date_attribute_without_a_granularity_suffix_names_none():
    """`label/process_date` matches no token: the tool has no "date" key and refuses the
    call rather than guessing daily, so guessing DAY here would score a granularity the
    service never used."""
    assert _inferred_granularity(_viz(dimension="label/process_date", filter_granularity=None)) is None


def test_granularity_falls_back_to_the_date_filter():
    """A dimension with no recognisable token still leaves the filter to read."""
    viz = _viz(dimension="label/some_opaque_label", filter_granularity="QUARTER")
    assert _inferred_granularity(viz) == "QUARTER"


def test_a_field_token_wins_over_a_disagreeing_filter():
    """The service reads fields first, so the evaluation must too -- otherwise the two
    disagree and a correct run scores wrong."""
    viz = _viz(dimension="label/process_date.day", filter_granularity="MONTH")
    assert _inferred_granularity(viz) == "DAY"


def test_granularity_is_none_when_nothing_names_one():
    viz = _viz(dimension="label/opaque", filter_granularity=None)
    assert _inferred_granularity(viz) is None
    assert _inferred_granularity(None) is None


# ── scoring ─────────────────────────────────────────────────────────────────


def _evaluate(viz=None, result=None, expected=None, turn_completed=True):
    return _evaluate_run(viz, result, expected if expected is not None else _EXPECTED, turn_completed)


def test_a_correct_detection_passes_every_check():
    ev = _evaluate(_viz(), {"success": True})
    assert ev.strict_pass is True
    assert ev.asserted == ["metric", "granularity"]


def test_detecting_on_the_wrong_measure_fails():
    ev = _evaluate(_viz(metric="metric/orders"), {"success": True})
    assert ev.metric_correct is False
    assert ev.granularity_correct is True


def test_the_wrong_granularity_fails():
    """Daily anomalies on a question about monthly ones is the wrong series, however well
    the detection itself performed."""
    ev = _evaluate(_viz(dimension="label/process_date.day"), {"success": True})
    assert ev.granularity_correct is False
    assert ev.metric_correct is True


def test_expected_granularity_is_compared_case_insensitively():
    assert _evaluate(_viz(), {"success": True}, expected={"granularity": "month"}).granularity_correct is True


def test_an_unstated_expectation_neither_fails_nor_silently_passes():
    ev = _evaluate(_viz(metric="metric/anything"), {"success": True}, expected={})
    assert ev.strict_pass is True
    assert ev.asserted == []


def test_finding_no_anomalies_is_still_a_pass():
    """Whether a real series contains anomalies is a property of the data, not the agent --
    the count is reported but never gates the verdict."""
    assert _evaluate(_viz(), json.loads(_OK_DETECT)).strict_pass is True


def test_a_failed_detection_is_not_a_success():
    ev = _evaluate(_viz(), {"success": False, "error": "boom"})
    assert ev.executed is True
    assert ev.success is False


def test_a_chart_alone_is_not_an_executed_detection():
    ev = _evaluate(_viz(), None)
    assert ev.triggered is True
    assert ev.executed is False


# ── run loop ────────────────────────────────────────────────────────────────


def _run(side_effect, *, k=1, expected=None, max_iterations=4):
    client = MagicMock()
    client.create_conversation.side_effect = [f"conv-{i}" for i in range(1, k + 2)]
    client.send_message.side_effect = side_effect
    with (
        patch(f"{_MODULE}.ChatClient", return_value=client),
        patch(f"{_MODULE}.generate_simulated_anomaly_response", return_value="use spend, monthly"),
    ):
        return run_agentic_anomaly_detection(
            host="http://h",
            token="tok",
            workspace_id="ws1",
            question="Detect anomalies in monthly spend",
            expected_output=expected if expected is not None else _EXPECTED,
            k=k,
            max_iterations=max_iterations,
        )


def test_a_single_turn_detection_passes():
    """Observed live: search, build, detect all land in one turn."""
    summary = _run([_chat(_pair())])
    assert summary.pass_at_k is True
    assert summary.best.evaluation.disambiguated is False


def test_a_clarifying_question_is_answered_and_the_run_continues():
    summary = _run([_chat([], text="Which Spend metric did you mean?"), _chat(_pair())])
    assert summary.pass_at_k is True
    assert summary.best.evaluation.disambiguated is True


def test_the_loop_stops_at_max_iterations_without_a_detection():
    summary = _run([_chat([], text="Still thinking")] * 4, max_iterations=4)
    assert summary.pass_at_k is False
    assert summary.best.evaluation.executed is False


def test_an_empty_response_ends_the_run_immediately():
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    client.send_message.return_value = _chat([], text="")
    with (
        patch(f"{_MODULE}.ChatClient", return_value=client),
        patch(f"{_MODULE}.generate_simulated_anomaly_response") as sim,
    ):
        run_agentic_anomaly_detection(
            host="http://h", token="tok", workspace_id="ws1", question="q", expected_output=_EXPECTED
        )
    assert client.send_message.call_count == 1
    sim.assert_not_called()


def test_a_chat_error_on_a_later_run_does_not_discard_the_earlier_one():
    summary = _run([_chat(_pair()), RuntimeError("boom")], k=2)
    assert len(summary.run_results) == 2
    assert summary.pass_at_k is True


def test_k_must_be_at_least_one():
    with pytest.raises(ValueError, match="k must be >= 1"):
        run_agentic_anomaly_detection(host="h", token="t", workspace_id="w", question="q", expected_output={}, k=0)


# ── evaluate_* wrapper ──────────────────────────────────────────────────────


def _evaluate_item(calls):
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    client.send_message.return_value = _chat(calls)
    with patch(f"{_MODULE}.ChatClient", return_value=client):
        return evaluate_agentic_anomaly_detection(
            host="http://h",
            token="tok",
            workspace_id="ws1",
            question="Detect anomalies in monthly spend",
            expected_output=_EXPECTED,
        )


def test_detail_reports_the_series_analysed_and_the_flag_count():
    outcome = _evaluate_item(_pair())
    assert outcome.detail["actual_metrics"] == ["metric/spend"]
    assert outcome.detail["actual_granularity"] == "MONTH"
    assert outcome.detail["anomaly_point_count"] == 0
    assert outcome.detail["asserted"] == ["metric", "granularity"]
    assert "latency_breakdown" in outcome.detail
    assert outcome.runs_passed == 1


def test_the_wrong_series_raises_naming_what_was_analysed():
    with pytest.raises(AnomalyDetectionAssertionError) as exc_info:
        _evaluate_item(_pair(dimension="label/process_date.day"))

    error = exc_info.value
    assert "granularity_correct=False" in str(error)
    assert "DAY" in str(error)
    assert error.runs_passed == 0
    assert error.conversation_id == "conv-1"


def test_a_chart_built_on_an_earlier_turn_is_still_the_one_scored():
    """The agent may build the chart on one turn and detect on the next -- reading only the
    current turn's calls would drop the series the detection actually ran on and fail a
    correct run for having no metric or granularity."""
    summary = _run(
        [
            _chat([_tc("create_adhoc_visualization", _viz_args())], text="Building the chart."),
            _chat([_tc("execute_anomaly_detection", {"visualization_ref": "viz_1"}, _OK_DETECT)]),
        ]
    )

    assert summary.best.evaluation.executed is True
    assert summary.best.evaluation.metric_correct is True
    assert summary.best.evaluation.granularity_correct is True
    assert summary.pass_at_k is True


# ── prompt building, string fields, and failure paths ───────────────────────


def test_the_clarification_prompt_mentions_only_the_hints_the_fixture_supplies():
    """An absent hint must be dropped, not asserted as a literal "None" -- that would
    answer a question the agent never asked, with a wrong value."""
    full = _build_clarification_prompt("Which one?", {"metric": "metric/spend", "granularity": "MONTH"})
    assert "metric/spend" in full
    assert "MONTH" in full

    bare = _build_clarification_prompt("Which one?", {})
    assert "None" not in bare
    assert "For reference" not in bare


def test_a_bare_uri_field_is_read_for_both_metric_and_granularity():
    """Tool-call arguments are raw JSON, where a field may be a plain string rather than
    the object a parsed visualization always has."""
    viz = {"query": {"fields": {"m": "metric/spend", "d": "label/process_date.month"}}, "metrics": ["m"]}
    assert _metric_uris(viz) == {"metric/spend"}
    assert _inferred_granularity(viz) == "MONTH"


def test_a_chat_error_keeps_what_its_partial_result_carried():
    """A stream that broke after the detection ran still has a result worth scoring."""
    error = RuntimeError("stream died")
    error.partial_result = _chat(_pair())
    summary = _run([error])

    assert summary.best.evaluation.executed is True
    # The turn did not finish, which strict_pass requires, so this is still a failure.
    assert summary.best.evaluation.turn_completed is False
    assert summary.pass_at_k is False


def test_a_simulated_user_failure_ends_the_run_without_raising():
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    client.send_message.return_value = _chat([], text="Which measure?")
    with (
        patch(f"{_MODULE}.ChatClient", return_value=client),
        patch(f"{_MODULE}.generate_simulated_anomaly_response", side_effect=RuntimeError("openai down")),
    ):
        summary = run_agentic_anomaly_detection(
            host="http://h", token="tok", workspace_id="ws1", question="q", expected_output=_EXPECTED
        )

    assert summary.pass_at_k is False
    assert client.send_message.call_count == 1  # ended rather than looping


# ── Langfuse scoring ────────────────────────────────────────────────────────


class _FakeCtx:
    """Records what the deferred Langfuse block writes, without a Langfuse."""

    def __init__(self):
        self.scores: dict[str, float] = {}
        # Not named `quality`: the method below would overwrite itself on first call.
        self.quality_call: dict = {}

    def trace(self, _conversation_id):
        return None

    @contextmanager
    def observe(self, _trace, _run_idx):
        yield "trace-id"

    def score(self, _tid, *, name, value, data_type):
        self.scores[name] = value

    def quality(self, _tid, *, strict_checks, latency_sec, cost_usd):
        self.quality_call = {"strict_checks": strict_checks, "latency_sec": latency_sec, "cost_usd": cost_usd}


def _scored(expected_output, calls=None):
    """Run one item with Langfuse on, then execute the deferred block against a fake ctx."""
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    client.send_message.return_value = _chat(calls if calls is not None else _pair())
    captured = {}

    def _capture(_link, _identity, **kwargs):
        captured.update(kwargs)

    with (
        patch(f"{_MODULE}.ChatClient", return_value=client),
        patch(f"{_MODULE}.submit_trace_scoring", side_effect=_capture),
    ):
        try:
            evaluate_agentic_anomaly_detection(
                host="http://h",
                token="tok",
                workspace_id="ws1",
                question="Detect anomalies in monthly spend",
                expected_output=expected_output,
                langfuse=MagicMock(),
                dataset_item_id="ds-1",
            )
        except AnomalyDetectionAssertionError:
            pass  # scores are written before the pass@K raise, which is the point

    ctx = _FakeCtx()
    captured["write_scores"](ctx)
    return ctx


def test_only_the_checks_the_fixture_pinned_are_scored():
    """An unasserted check is True internally so it cannot fail a run. Publishing that as a
    BOOLEAN 1 would claim the evaluator verified something it never looked at."""
    ctx = _scored({"metric": "metric/spend"})  # granularity deliberately unpinned

    assert ctx.scores["anomaly_metric_correct"] == 1.0
    assert "anomaly_granularity_correct" not in ctx.scores
    # The process checks are unconditional -- they are always actually evaluated.
    assert set(ctx.scores) >= {"anomaly_triggered", "anomaly_executed", "anomaly_success"}


def test_both_content_checks_are_scored_when_both_are_pinned():
    ctx = _scored(_EXPECTED)
    assert ctx.scores["anomaly_metric_correct"] == 1.0
    assert ctx.scores["anomaly_granularity_correct"] == 1.0


def test_cost_is_reported_even_when_the_tool_was_never_reached():
    """A run that answered without detecting anything still spent tokens; gating cost on
    ev.triggered hid that and understated what the item cost."""
    ctx = _scored(_EXPECTED, calls=[])
    assert "cost_usd" in ctx.quality_call

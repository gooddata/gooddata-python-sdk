# (C) 2026 GoodData Corporation
"""The failing-runs head of an agentic failure message, and the per-run records it reads."""

import importlib
import inspect
from dataclasses import dataclass, field
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.agentic import metric_skill as metric_skill_mod
from gooddata_eval.core.agentic import visualization as agentic_visualization
from gooddata_eval.core.agentic._failed_runs import build_failed_runs
from gooddata_eval.core.agentic._failure_message import (
    FailedCheck,
    failed_check_records,
    failing_runs_note,
    failure_head,
)
from gooddata_eval.core.agentic.metric_skill import MetricSkillAssertionError, evaluate_agentic_metric_skill
from gooddata_eval.core.agentic.visualization import VisualizationAssertionError, evaluate_agentic_visualization
from gooddata_eval.core.models import ChatResult, CreatedVisualization, LoopExit

# ── the renderer ─────────────────────────────────────────────────────────────


def test_a_failed_check_records_only_what_the_kind_knows() -> None:
    assert FailedCheck("metric_correct").as_record() == {"name": "metric_correct"}
    assert FailedCheck("filters_correct", label="date", expected=[], actual=["MONTH -11..0"]).as_record() == {
        "name": "filters_correct",
        "label": "date",
        "expected": [],
        "actual": ["MONTH -11..0"],
    }
    # None is a real expected value, not "unknown".
    assert FailedCheck("x", expected=None).as_record() == {"name": "x", "expected": None}


def test_the_note_lists_each_failing_run_with_its_exit_and_failing_checks_only() -> None:
    failed_runs = [
        {
            "run_index": 2,
            "exit_reason": "success",
            "failed_checks": failed_check_records(
                [FailedCheck("filters_correct", label="date", expected=[], actual="MONTH -11..0")]
            ),
        },
        {"run_index": 3, "exit_reason": "budget_exhausted", "failed_checks": [{"name": "metric_correct"}]},
    ]

    note = failing_runs_note(failed_runs, 3)

    assert note == (
        "run 2/3 FAIL (exit=success): filters_correct[date: expected none, actual MONTH -11..0]; "
        "run 3/3 FAIL (exit=budget_exhausted): metric_correct"
    )


def test_the_head_starts_with_the_gate_note() -> None:
    gate_note = "Gate pass^3 failed: 2/3 runs passed — unstable, not a clean failure."
    failed_runs = [{"run_index": 2, "exit_reason": "success", "failed_checks": [{"name": "metric_correct"}]}]

    head = failure_head(gate_note, failed_runs, 3)

    assert head.startswith(gate_note)
    assert head.endswith("Failing runs: run 2/3 FAIL (exit=success): metric_correct.")


def test_the_head_is_the_gate_note_alone_without_failing_runs() -> None:
    assert failure_head("Gate pass@2 failed: 0/2 runs passed.", [], 2) == "Gate pass@2 failed: 0/2 runs passed."


def test_a_run_without_recorded_checks_says_so_and_a_kind_without_the_key_says_nothing() -> None:
    assert failing_runs_note([{"run_index": 1, "exit_reason": None, "failed_checks": []}], 1) == (
        "run 1/1 FAIL: no failing check recorded"
    )
    assert failing_runs_note([{"run_index": 1, "exit_reason": "agent_silent"}], 1) == (
        "run 1/1 FAIL (exit=agent_silent)"
    )


def test_an_errored_run_is_labelled_with_its_source() -> None:
    record = {
        "run_index": 1,
        "exit_reason": "simulated_user_failed",
        "outcome": {"status": "error", "source": "harness", "reason": "simulated user failed"},
        "failed_checks": [],
    }
    assert failing_runs_note([record], 3) == (
        "run 1/3 ERROR harness (exit=simulated_user_failed): no failing check recorded"
    )


def test_a_long_value_is_cut_to_one_short_line() -> None:
    record = {"run_index": 1, "failed_checks": [{"name": "maql_correct", "actual": "SELECT\n" + "x" * 500}]}
    note = failing_runs_note([record], 1)
    assert "\n" not in note
    assert note.endswith("...]")
    assert len(note) < 250


# ── the records ──────────────────────────────────────────────────────────────


@dataclass
class _Run:
    ok: bool
    exit_reason: LoopExit = LoopExit.SUCCESS
    conversation_id: str = "c"
    tool_call_events: list = field(default_factory=list)


def test_every_failing_record_carries_its_exit_reason_and_failed_checks() -> None:
    runs = [_Run(True), _Run(False, LoopExit.BUDGET_EXHAUSTED)]

    records = build_failed_runs(
        runs,
        passed=lambda r: r.ok,
        detail=lambda r: {},
        failed_checks=lambda r: [{"name": "metric_correct"}],
    )

    assert len(records) == 1
    assert records[0]["run_index"] == 2
    assert records[0]["exit_reason"] == "budget_exhausted"
    assert records[0]["failed_checks"] == [{"name": "metric_correct"}]


def test_a_kind_that_names_no_checks_writes_no_failed_checks_key() -> None:
    records = build_failed_runs([object()], passed=lambda r: False, detail=lambda r: {})
    assert records[0]["exit_reason"] is None
    assert "failed_checks" not in records[0]


# ── visualization: a partial gate failure names the run that failed ──────────


def _viz(filter_by: dict | None = None) -> dict:
    return {
        "id": "v1",
        "type": "column_chart",
        "query": {
            "fields": {"m": {"using": "metric/revenue"}, "d": {"using": "label/date.quarter"}},
            "filter_by": filter_by or {},
        },
        "metrics": ["m"],
        "view_by": ["d"],
    }


def _viz_turn(filter_by: dict | None = None) -> ChatResult:
    return ChatResult.model_validate(
        {"createdVisualizations": {"objects": [_viz(filter_by)], "reasoning": ""}, "toolCallEvents": []}
    )


_LAST_YEAR = {"date": {"type": "date_filter", "using": "dataset/date", "granularity": "MONTH", "from": -11, "to": 0}}


def test_a_partial_visualization_failure_lists_the_failing_run_and_keeps_the_best_run_summary() -> None:
    client = MagicMock()
    client.create_conversation.side_effect = ["conv-1", "conv-2", "conv-3"]
    client.send_message.side_effect = [_viz_turn(), _viz_turn(_LAST_YEAR), _viz_turn()]

    with (
        patch.object(agentic_visualization, "ChatClient", return_value=client),
        pytest.raises(VisualizationAssertionError) as exc_info,
    ):
        evaluate_agentic_visualization(
            host="https://example.com",
            token="tok",
            workspace_id="ws",
            question="Show revenue by quarter",
            expected_outputs=[CreatedVisualization.model_validate(_viz())],
            k=3,
            gate="power",
        )

    message = str(exc_info.value)
    lines = message.splitlines()
    gate_line = next(line for line in lines if line.startswith("Gate pass^3 failed"))
    assert gate_line.startswith("Gate pass^3 failed: 2/3 runs passed — unstable, not a clean failure. Failing runs: ")
    assert "run 2/3 FAIL (exit=success): filters_correct[date: expected none, actual " in gate_line
    # Only the failing checks of the failing run, and no passing run.
    assert "metrics_correct" not in gate_line
    assert "run 1/3" not in gate_line
    assert "run 3/3" not in gate_line
    # The best-run summary that followed the gate note is still there, unchanged.
    assert lines[1] == "Agentic Visualization Assertion Failed! (Critical Mode)"
    assert "Strict Check Summary:" in message
    assert "  Filters Correct       : True\n" in message

    (record,) = exc_info.value.failed_runs
    assert record["run_index"] == 2
    assert record["exit_reason"] == "success"
    assert record["detail"]["exit_reason"] == "success"
    assert [c["name"] for c in record["failed_checks"]] == ["filters_correct"]
    assert record["failed_checks"][0]["label"] == "date"
    assert record["failed_checks"][0]["expected"] == []


# ── metric skill: same head, expected/actual MAQL of the failing run ─────────


def _metric_turn(maql: str) -> ChatResult:
    return ChatResult.model_validate(
        {
            "textResponse": "done",
            "toolCallEvents": [
                {
                    "functionName": "create_metric",
                    "functionArguments": "{}",
                    "result": f'{{"data": {{"maql": "{maql}"}}}}',
                }
            ],
        }
    )


def test_a_partial_metric_failure_lists_the_failing_run_with_its_maql() -> None:
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    client.send_message.side_effect = [_metric_turn("SELECT {metric/foo}"), _metric_turn("SELECT {metric/bar}")]

    with (
        patch.object(metric_skill_mod, "ChatClient", return_value=client),
        pytest.raises(MetricSkillAssertionError) as exc_info,
    ):
        evaluate_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
            k=2,
            max_iterations=1,
            gate="power",
        )

    message = str(exc_info.value)
    assert message.startswith(
        "Metric skill assertion failed. Gate pass^2 failed: 1/2 runs passed — unstable, not a clean failure. "
        "Failing runs: run 2/2 FAIL (exit=success): "
        'maql_correct[expected ["SELECT {metric/foo}"], actual SELECT {metric/bar}].'
    )
    # The best run's summary follows, as before.
    assert "metric_created=True, maql_correct=True. Expected MAQL (candidates): 'SELECT {metric/foo}'." in message
    (record,) = exc_info.value.failed_runs
    assert record["exit_reason"] == "success"
    assert record["failed_checks"] == [
        {"name": "maql_correct", "expected": ["SELECT {metric/foo}"], "actual": "SELECT {metric/bar}"}
    ]


@pytest.mark.parametrize("module_name", ["visualization", "alert_skill", "metric_skill", "dashboard_skill"])
def test_each_checked_kind_heads_its_message_through_the_shared_renderer(module_name: str) -> None:
    source = inspect.getsource(importlib.import_module(f"gooddata_eval.core.agentic.{module_name}"))
    assert "failure_head(" in source
    assert "failed_checks=_failed_checks" in source

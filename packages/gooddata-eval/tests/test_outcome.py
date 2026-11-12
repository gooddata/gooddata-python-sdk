# (C) 2026 GoodData Corporation
"""PASS / FAIL / ERROR per run, the gate over scored runs, and the GD_EVAL_ERROR_OUTCOME switch.

Every verdict-changing test runs twice: with the flag on (the new behaviour) and off, where
the verdict and the existing message content must be exactly what they were before.
"""

from unittest.mock import MagicMock, patch

import gooddata_eval
import pytest
from gooddata_eval.cli.agentic_runner import run_agentic_items
from gooddata_eval.core.agentic import visualization as agentic_visualization
from gooddata_eval.core.agentic._gate import gate_failure_note
from gooddata_eval.core.agentic._outcome import resolve_runs
from gooddata_eval.core.agentic.visualization import VisualizationAssertionError, evaluate_agentic_visualization
from gooddata_eval.core.config import ERROR_OUTCOME_ENV_VAR, error_outcome_enabled
from gooddata_eval.core.models import AgenticAssertionError, ChatResult, CreatedVisualization, DatasetItem, LoopExit
from gooddata_eval.core.outcome import (
    ErrorSource,
    EvalHarnessError,
    Outcome,
    OutcomeStatus,
    excluded_runs_note,
    gate_outcomes,
    outcome_from_loop_exit,
)
from gooddata_eval.core.runner import run_items

PASS = Outcome.passed()
FAIL = Outcome.failed()
HARNESS = Outcome.error(ErrorSource.HARNESS, "the simulated user failed to reply")
BACKEND = Outcome.error(ErrorSource.BACKEND, "the chat call failed after its retries")


@pytest.fixture
def flag_on(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(ERROR_OUTCOME_ENV_VAR, "1")


# ── the flag ─────────────────────────────────────────────────────────────────


@pytest.mark.parametrize(("value", "on"), [(None, False), ("", False), ("0", False), ("off", False), ("1", True)])
def test_the_flag_is_off_unless_set_to_something_truthy(monkeypatch, value, on) -> None:
    if value is None:
        monkeypatch.delenv(ERROR_OUTCOME_ENV_VAR, raising=False)
    else:
        monkeypatch.setenv(ERROR_OUTCOME_ENV_VAR, value)
    assert error_outcome_enabled() is on


# ── the public names ─────────────────────────────────────────────────────────


def test_the_error_is_public_and_not_an_assertion_error() -> None:
    # Not an AssertionError, so pytest records <error>, not <failure>.
    assert not issubclass(EvalHarnessError, AssertionError)
    assert not issubclass(EvalHarnessError, AgenticAssertionError)
    for name in ("EvalHarnessError", "Outcome", "OutcomeStatus", "ErrorSource", "outcome_from_loop_exit"):
        assert name in gooddata_eval.__all__
    assert gooddata_eval.EvalHarnessError is EvalHarnessError


def test_existing_assertion_classes_keep_their_base() -> None:
    assert issubclass(VisualizationAssertionError, AgenticAssertionError)
    assert issubclass(AgenticAssertionError, AssertionError)


# ── LoopExit → Outcome ───────────────────────────────────────────────────────


@pytest.mark.parametrize(
    ("exit_reason", "status", "source"),
    [
        (LoopExit.SUCCESS, OutcomeStatus.FAIL, None),
        (LoopExit.BUDGET_EXHAUSTED, OutcomeStatus.FAIL, None),
        (LoopExit.AGENT_SILENT, OutcomeStatus.FAIL, None),
        (LoopExit.SIMULATED_USER_FAILED, OutcomeStatus.ERROR, ErrorSource.HARNESS),
        (LoopExit.CHAT_ERROR, OutcomeStatus.ERROR, ErrorSource.BACKEND),
        (LoopExit.NOT_RUN, OutcomeStatus.ERROR, ErrorSource.HARNESS),
        (None, OutcomeStatus.FAIL, None),
    ],
)
def test_each_loop_exit_maps_to_its_outcome_when_the_run_failed(exit_reason, status, source) -> None:
    outcome = outcome_from_loop_exit(exit_reason, passed=False)
    assert outcome.status is status
    assert outcome.source is source
    assert outcome.is_scored is (status is not OutcomeStatus.ERROR)


def test_every_loop_exit_is_mapped() -> None:
    # A new LoopExit member must be classified on purpose: this lists what is scored today.
    scored = {e for e in LoopExit if outcome_from_loop_exit(e, passed=False).is_scored}
    assert scored == {LoopExit.SUCCESS, LoopExit.BUDGET_EXHAUSTED, LoopExit.AGENT_SILENT}


@pytest.mark.parametrize("exit_reason", list(LoopExit))
def test_a_run_that_passed_is_pass_whatever_its_exit(exit_reason) -> None:
    assert outcome_from_loop_exit(exit_reason, passed=True) == PASS


def test_the_mapping_accepts_the_string_value() -> None:
    assert outcome_from_loop_exit("chat_error", passed=False).source is ErrorSource.BACKEND


def test_an_outcome_record_is_json_ready() -> None:
    assert BACKEND.as_record() == {
        "status": "error",
        "source": "backend",
        "reason": "the chat call failed after its retries",
    }
    assert PASS.as_record() == {"status": "pass", "source": None, "reason": None}


# ── the gate over outcomes ───────────────────────────────────────────────────


@pytest.mark.parametrize("gate", ["any", "power"])
def test_error_pass_pass_passes_with_one_run_excluded(gate) -> None:
    verdict = gate_outcomes([HARNESS, PASS, PASS], gate)

    assert verdict.outcome == PASS
    assert (verdict.runs_scored, verdict.runs_passed, verdict.runs_total) == (2, 2, 3)
    assert verdict.pass_power_k is True
    note = excluded_runs_note(verdict)
    assert note.startswith("1 run excluded (harness error)")
    assert "run 1/3 the simulated user failed to reply" in note


@pytest.mark.parametrize("gate", ["any", "power"])
def test_error_error_error_is_an_error(gate) -> None:
    verdict = gate_outcomes([HARNESS, BACKEND, HARNESS], gate)

    assert verdict.outcome.status is OutcomeStatus.ERROR
    assert verdict.outcome.source is ErrorSource.HARNESS
    assert verdict.runs_scored == 0
    assert verdict.pass_at_k is False
    assert verdict.pass_power_k is False
    assert excluded_runs_note(verdict).startswith("3 runs excluded (1 backend error, 2 harness error)")


def test_the_gate_still_decides_over_the_scored_runs() -> None:
    assert gate_outcomes([BACKEND, PASS, FAIL], "power").outcome == FAIL
    assert gate_outcomes([BACKEND, PASS, FAIL], "any").outcome == PASS
    assert gate_outcomes([FAIL, FAIL], "any").outcome == FAIL
    assert excluded_runs_note(gate_outcomes([PASS, FAIL], "any")) == ""


# ── resolve_runs: off is today's arithmetic, whatever the runs say ───────────


class _Run:
    def __init__(self, ok: bool, exit_reason: LoopExit) -> None:
        self.ok = ok
        self.exit_reason = exit_reason


_MIXED = [
    _Run(False, LoopExit.SIMULATED_USER_FAILED),
    _Run(True, LoopExit.SUCCESS),
    _Run(True, LoopExit.SUCCESS),
]


def test_off_the_counts_and_verdict_inputs_are_the_kinds_own() -> None:
    runs = resolve_runs(_MIXED, passed=lambda r: r.ok, gate="power", pass_at_k=True, pass_power_k=False)

    assert (runs.pass_at_k, runs.pass_power_k) == (True, False)
    assert (runs.runs_passed, runs.runs_effective, runs.runs_total) == (2, 3, 3)
    assert runs.errored is False
    assert runs.excluded_note == ""
    assert runs.detail() == {}
    assert runs.outcome_record is None
    assert runs.exception_cls(VisualizationAssertionError) is VisualizationAssertionError


def test_on_the_errored_run_leaves_k(flag_on) -> None:
    runs = resolve_runs(_MIXED, passed=lambda r: r.ok, gate="power", pass_at_k=True, pass_power_k=False)

    assert (runs.pass_at_k, runs.pass_power_k) == (True, True)
    assert (runs.runs_passed, runs.runs_effective, runs.runs_total) == (2, 2, 3)
    assert runs.detail()["excluded_runs"][0]["exit_reason"] == "simulated_user_failed"


# ── end to end through the visualization kind ────────────────────────────────


def _viz() -> dict:
    return {
        "id": "v1",
        "type": "column_chart",
        "query": {
            "fields": {"m": {"using": "metric/revenue"}, "d": {"using": "label/date.quarter"}},
            "filter_by": {},
        },
        "metrics": ["m"],
        "view_by": ["d"],
    }


def _viz_turn() -> ChatResult:
    return ChatResult.model_validate({"createdVisualizations": {"objects": [_viz()], "reasoning": ""}})


def _question_turn() -> ChatResult:
    return ChatResult.model_validate({"textResponse": "Which metric?"})


def _evaluate(turns: list[ChatResult]) -> object:
    client = MagicMock()
    client.create_conversation.side_effect = [f"conv-{i}" for i in range(1, len(turns) + 1)]
    client.send_message.side_effect = turns
    with (
        patch.object(agentic_visualization, "ChatClient", return_value=client),
        patch.object(agentic_visualization, "generate_simulated_response", side_effect=RuntimeError("openai 401")),
    ):
        return evaluate_agentic_visualization(
            host="https://example.com",
            token="tok",
            workspace_id="ws",
            question="Show revenue by quarter",
            expected_outputs=[CreatedVisualization.model_validate(_viz())],
            k=len(turns),
            gate="power",
        )


def test_off_a_simulated_user_failure_fails_the_item_exactly_as_before() -> None:
    with pytest.raises(VisualizationAssertionError) as exc_info:
        _evaluate([_question_turn(), _viz_turn(), _viz_turn()])

    message = str(exc_info.value)
    lines = message.splitlines()
    assert lines[1] == "Agentic Visualization Assertion Failed! (Critical Mode)"
    assert lines[2].startswith(gate_failure_note("power", 2, 3))
    assert "excluded" not in message
    assert "Strict Check Summary:" in message
    assert exc_info.value.runs_passed == 2
    assert exc_info.value.runs_effective == 3
    assert "excluded_runs" not in exc_info.value.detail
    assert not hasattr(exc_info.value, "outcome")


def test_on_error_pass_pass_passes_with_the_excluded_run_recorded(flag_on) -> None:
    outcome = _evaluate([_question_turn(), _viz_turn(), _viz_turn()])

    assert outcome.runs_passed == 2
    assert outcome.runs_effective == 2
    (excluded,) = outcome.detail["excluded_runs"]
    assert excluded["run_index"] == 1
    assert excluded["outcome"]["status"] == "error"
    assert excluded["outcome"]["source"] == "harness"
    (record,) = outcome.failed_runs
    assert record["exit_reason"] == "simulated_user_failed"
    assert record["outcome"]["status"] == "error"


def test_off_error_error_error_is_a_failure_as_before() -> None:
    with pytest.raises(VisualizationAssertionError) as exc_info:
        _evaluate([_question_turn(), _question_turn(), _question_turn()])

    assert gate_failure_note("power", 0, 3) in str(exc_info.value)


def test_on_error_error_error_raises_the_harness_error(flag_on) -> None:
    with pytest.raises(EvalHarnessError) as exc_info:
        _evaluate([_question_turn(), _question_turn(), _question_turn()])

    exc = exc_info.value
    assert not isinstance(exc, AssertionError)
    message = str(exc)
    assert "No scored run, item errored: 3 runs excluded (harness error)" in message
    assert "run 1/3 ERROR harness (exit=simulated_user_failed)" in message
    assert exc.outcome["status"] == "error"
    assert exc.outcome["source"] == "harness"
    assert exc.runs_passed == 0
    assert len(exc.failed_runs) == 3
    assert all(r["exit_reason"] == "simulated_user_failed" for r in exc.failed_runs)


# ── the agentic runner reports the harness error as an error, with its runs ──


def _alert_item() -> DatasetItem:
    return DatasetItem(
        id="item-1",
        dataset_name="d",
        test_kind="agentic_alert_skill",
        question="Alert me when revenue drops below 100.",
        expected_output={"operator": "LESS_THAN", "threshold": 100},
    )


def test_the_agentic_runner_records_a_harness_error_as_an_error_with_its_runs() -> None:
    exc = EvalHarnessError("No scored run")
    exc.detail = {"excluded_runs": [{"run_index": 1}]}
    exc.runs_passed = 0
    exc.runs_effective = 0
    exc.failed_runs = [{"run_index": 1, "exit_reason": "chat_error"}]

    with patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_alert_skill", side_effect=exc):
        report = run_agentic_items([_alert_item()], host="h", token="t", workspace_id="ws1", run_ts="2026-01-01")

    item = report.items[0]
    assert item.error == "EvalHarnessError: No scored run"
    assert item.passed is False
    assert item.failed_runs == [{"run_index": 1, "exit_reason": "chat_error"}]
    assert item.best_detail == {"excluded_runs": [{"run_index": 1}]}
    assert report.errored == 1


# ── single-shot runner: never both passed and errored ────────────────────────


def _single_shot_item() -> DatasetItem:
    return DatasetItem(
        id="i1",
        dataset_name="d",
        test_kind="visualization",
        question="Show revenue by quarter",
        expected_output={"visualization": _viz()},
    )


class _PassThenBoom:
    def __init__(self) -> None:
        self.calls = 0

    def ask(self, item: DatasetItem) -> ChatResult:
        self.calls += 1
        if self.calls == 2:
            raise RuntimeError("network down")
        return _viz_turn()


def _run_single_shot() -> tuple[object, list[str]]:
    logged: list[str] = []
    report = run_items(
        [_single_shot_item()],
        _PassThenBoom(),
        runs=2,
        on_langfuse_item_done=lambda _i, _t, r: logged.append(r.id),
    )
    return report.items[0], logged


def test_off_a_pass_then_an_exception_is_both_passed_and_errored_as_before() -> None:
    item, logged = _run_single_shot()

    assert item.pass_at_k is True
    assert item.error == "RuntimeError: network down"
    assert logged == []


def test_on_a_pass_then_an_exception_is_an_error_only_and_still_logged(flag_on) -> None:
    item, logged = _run_single_shot()

    assert item.error == "RuntimeError: network down"
    assert item.pass_at_k is False
    assert item.passed is False
    assert item.runs_passed == 1
    assert logged == ["i1"]

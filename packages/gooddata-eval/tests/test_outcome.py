# (C) 2026 GoodData Corporation
"""PASS / FAIL / ERROR per run, the gate over scored runs, and the GD_EVAL_ERROR_OUTCOME switch.

Every verdict-changing test runs twice: with the flag on (the new behaviour) and off, where
the verdict and the existing message content must be exactly what they were before.
"""

from collections import defaultdict
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any
from unittest.mock import MagicMock, patch

import gooddata_eval
import httpx
import pytest
from gooddata_eval.cli.agentic_runner import run_agentic_items
from gooddata_eval.core.agentic import visualization as agentic_visualization
from gooddata_eval.core.agentic._gate import gate_failure_note
from gooddata_eval.core.agentic._outcome import chat_failure_exit, resolve_runs
from gooddata_eval.core.agentic.visualization import VisualizationAssertionError, evaluate_agentic_visualization
from gooddata_eval.core.chat.sse_client import ChatError, TransientChatError, TurnIncompleteError, TurnTimeoutError
from gooddata_eval.core.config import ERROR_OUTCOME_ENV_VAR, error_outcome_enabled
from gooddata_eval.core.models import (
    AgenticAssertionError,
    AgenticEvalOutcome,
    ChatResult,
    CreatedVisualization,
    DatasetItem,
    LoopExit,
)
from gooddata_eval.core.outcome import (
    ErrorSource,
    EvalHarnessError,
    Outcome,
    OutcomeStatus,
    excluded_runs_note,
    gate_outcomes,
    outcome_from_loop_exit,
)
from gooddata_eval.core.reporting.json_report import build_json_report
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
    # Not an AssertionError, so a runner can tell it apart from an agent failure.
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
    assert scored == {
        LoopExit.SUCCESS,
        LoopExit.BUDGET_EXHAUSTED,
        LoopExit.AGENT_SILENT,
        LoopExit.AGENT_TIMEOUT,
        LoopExit.TURN_INCOMPLETE,
    }


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
    # runs_effective stays the runs executed; runs_scored is what the gate counted.
    assert (runs.runs_passed, runs.runs_scored, runs.runs_effective, runs.runs_total) == (2, 2, 3, 3)
    assert runs.detail()["excluded_runs"][0]["exit_reason"] == "simulated_user_failed"
    assert runs.excluded_indexes == {1}
    assert runs.excluded_outcome(1) == HARNESS
    assert runs.excluded_outcome(2) is None


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


def _evaluate(turns: list[Any], captured: dict[str, Any] | None = None) -> object:
    client = MagicMock()
    client.create_conversation.side_effect = [f"conv-{i}" for i in range(1, len(turns) + 1)]
    client.send_message.side_effect = turns

    def _capture(_submit: object, _identity: object, **kwargs: Any) -> None:
        if captured is not None:
            captured["write_scores"] = kwargs["write_scores"]

    with (
        patch.object(agentic_visualization, "ChatClient", return_value=client),
        patch.object(agentic_visualization, "generate_simulated_response", side_effect=RuntimeError("openai 401")),
        patch.object(agentic_visualization, "submit_trace_scoring", _capture),
    ):
        return evaluate_agentic_visualization(
            host="https://example.com",
            token="tok",
            workspace_id="ws",
            question="Show revenue by quarter",
            expected_outputs=[CreatedVisualization.model_validate(_viz())],
            k=len(turns),
            gate="power",
            langfuse=MagicMock() if captured is not None else None,
            dataset_item_id="item-1" if captured is not None else None,
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
    # The gate counted the run as a failure, so the message and the record say FAIL too.
    assert "run 1/3 FAIL (loop exit: simulated_user_failed)" in message
    assert "ERROR" not in message
    (record,) = exc_info.value.failed_runs
    assert record["outcome"]["status"] == "fail"


def test_on_error_pass_pass_passes_with_the_excluded_run_recorded(flag_on) -> None:
    outcome = _evaluate([_question_turn(), _viz_turn(), _viz_turn()])

    assert outcome.runs_passed == 2
    assert outcome.runs_effective == 3
    assert outcome.runs_scored == 2
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
    # No assertion about the agent was made, so the message does not claim one failed.
    assert message.splitlines()[1] == "Agentic Visualization item could not be scored. (Critical Mode)"
    assert "Assertion Failed" not in message
    # Each excluded run is named once, in the excluded note, not again under Failing runs.
    assert "run 1/3 the simulated user failed to reply" in message
    assert "Failing runs" not in message
    assert exc.runs_effective == 3
    assert exc.runs_scored == 0
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


# ── the agent's own timeouts and incomplete turns are scored, not errors ─────


@pytest.mark.parametrize(
    ("exc", "loop_exit"),
    [
        (TurnTimeoutError("agent exceeded the 60s turn budget"), LoopExit.AGENT_TIMEOUT),
        (TurnIncompleteError("no final answer", reason="max iterations"), LoopExit.TURN_INCOMPLETE),
        (TransientChatError("503 after retries"), LoopExit.CHAT_ERROR),
        (ChatError("SSE stream error"), LoopExit.CHAT_ERROR),
        (httpx.ReadError("connection reset"), LoopExit.CHAT_ERROR),
    ],
)
def test_a_chat_failure_maps_to_its_own_exit(exc: BaseException, loop_exit: LoopExit) -> None:
    assert chat_failure_exit(exc) is loop_exit


@pytest.mark.parametrize("loop_exit", [LoopExit.AGENT_TIMEOUT, LoopExit.TURN_INCOMPLETE])
def test_the_agents_own_chat_failures_are_scored_as_failures(loop_exit: LoopExit) -> None:
    outcome = outcome_from_loop_exit(loop_exit, passed=False)
    assert outcome.status is OutcomeStatus.FAIL
    assert outcome.is_scored


@pytest.mark.parametrize(
    ("exc", "exit_value"),
    [
        (TurnTimeoutError("agent exceeded the 60s turn budget"), "agent_timeout"),
        (TurnIncompleteError("no final answer", reason="max iterations"), "turn_incomplete"),
    ],
)
def test_on_an_agent_timeout_stays_in_the_gate_and_fails_the_item(flag_on, exc, exit_value) -> None:
    with pytest.raises(VisualizationAssertionError) as exc_info:
        _evaluate([exc, _viz_turn(), _viz_turn()])

    assert exc_info.value.runs_passed == 2
    assert exc_info.value.runs_effective == 3
    assert "excluded" not in str(exc_info.value)
    assert "excluded_runs" not in exc_info.value.detail
    (record,) = exc_info.value.failed_runs
    assert record["exit_reason"] == exit_value
    assert record["outcome"]["status"] == "fail"


def test_on_only_agent_timeouts_is_a_failure_not_a_harness_error(flag_on) -> None:
    timeout = TurnTimeoutError("agent exceeded the 60s turn budget")
    with pytest.raises(VisualizationAssertionError) as exc_info:
        _evaluate([timeout, timeout, timeout])

    assert not isinstance(exc_info.value, EvalHarnessError)
    assert gate_failure_note("power", 0, 3) in str(exc_info.value)


def test_off_an_agent_timeout_fails_the_item_exactly_as_a_chat_error_did() -> None:
    timeout = TurnTimeoutError("agent exceeded the 60s turn budget")
    with pytest.raises(VisualizationAssertionError) as timed_out:
        _evaluate([timeout, _viz_turn(), _viz_turn()])
    with pytest.raises(VisualizationAssertionError) as chat_failed:
        _evaluate([ChatError("SSE stream error"), _viz_turn(), _viz_turn()])

    for exc_info in (timed_out, chat_failed):
        assert exc_info.value.runs_passed == 2
        assert exc_info.value.runs_effective == 3
        assert str(exc_info.value).splitlines()[2].startswith(gate_failure_note("power", 2, 3))


def test_on_a_backend_chat_error_is_still_excluded(flag_on) -> None:
    outcome = _evaluate([ChatError("SSE stream error"), _viz_turn(), _viz_turn()])

    assert outcome.runs_passed == 2
    (excluded,) = outcome.detail["excluded_runs"]
    assert excluded["exit_reason"] == "chat_error"
    assert excluded["outcome"]["source"] == "backend"


# ── a partly excluded item: K, latency and the message count the runs executed ──


def _silent_turn() -> ChatResult:
    return ChatResult.model_validate({})


def test_gate_failure_note_names_the_k_that_ran_and_how_many_were_excluded() -> None:
    assert gate_failure_note("power", 1, 2, runs_excluded=1) == (
        "Gate pass^3 (1 excluded) failed: 1/2 scored runs passed — unstable, not a clean failure."
    )
    assert gate_failure_note("any", 0, 1, runs_excluded=2) == "Gate pass@3 (2 excluded) failed: 0/1 scored runs passed."
    # Nothing excluded: exactly the note as before.
    assert gate_failure_note("power", 1, 3, runs_excluded=0) == gate_failure_note("power", 1, 3)


def test_on_an_excluded_run_is_listed_once_and_the_gate_keeps_its_k(flag_on) -> None:
    with pytest.raises(VisualizationAssertionError) as exc_info:
        _evaluate([_question_turn(), _silent_turn(), _viz_turn()])

    exc = exc_info.value
    gate_line = str(exc).splitlines()[2]
    assert gate_line.startswith("Gate pass^3 (1 excluded) failed: 1/2 scored runs passed")
    assert "1 run excluded (harness error): run 1/3 the simulated user failed to reply." in gate_line
    failing = gate_line.split("Failing runs: ", 1)[1]
    assert failing.startswith("run 2/3 FAIL (loop exit: agent_silent)")
    assert "run 1/3" not in failing
    assert (exc.runs_passed, exc.runs_scored, exc.runs_effective) == (1, 2, 3)
    # The excluded run keeps its record: the message names it once, the triage data in full.
    assert [r["run_index"] for r in exc.failed_runs] == [1, 2]


def test_off_the_same_item_is_reported_exactly_as_before() -> None:
    with pytest.raises(VisualizationAssertionError) as exc_info:
        _evaluate([_question_turn(), _silent_turn(), _viz_turn()])

    exc = exc_info.value
    gate_line = str(exc).splitlines()[2]
    assert gate_line.startswith(gate_failure_note("power", 1, 3) + " Failing runs: run 1/3 FAIL")
    assert "excluded" not in gate_line
    assert (exc.runs_passed, exc.runs_effective) == (1, 3)
    assert not hasattr(exc, "runs_scored")


def _report_for(outcome: object) -> object:
    with patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_alert_skill", return_value=outcome):
        return run_agentic_items([_alert_item()], host="h", token="t", workspace_id="ws1", run_ts="2026-01-01", k=3)


def test_on_an_item_report_counts_executed_runs_and_the_scored_ones_apart() -> None:
    outcome = AgenticEvalOutcome(runs_passed=2, runs_effective=3, runs_scored=2)
    report = _report_for(outcome)

    item = report.items[0]
    assert item.runs_total == 3
    assert item.runs_scored == 2
    assert item.runs_gated == 2
    assert item.pass_power_k is True
    assert item.avg_latency_s == pytest.approx(item.latency_s / 3)
    entry = build_json_report(report)["items"]["item-1"]
    assert (entry["runs"], entry["runs_scored"], entry["pass_power_k"]) == (3, 2, True)


def test_off_an_item_report_has_no_scored_count() -> None:
    report = _report_for(AgenticEvalOutcome(runs_passed=2, runs_effective=3))

    item = report.items[0]
    assert item.runs_scored is None
    assert item.runs_gated == item.runs_total == 3
    assert item.pass_power_k is False
    assert "runs_scored" not in build_json_report(report)["items"]["item-1"]


# ── Langfuse: an ERROR run gets eval_error and no verdict score ──────────────


class _ScoreCtx:
    """A RunTraceContext stand-in that keeps each run's scores apart, by run index."""

    def __init__(self) -> None:
        self.run_metadata: dict[str, Any] = {}
        self.scores: dict[int, list[tuple[str, Any, str | None]]] = defaultdict(list)

    def trace(self, _conversation_id: str) -> None:
        return None

    @contextmanager
    def observe(self, _trace: object, run_idx: int, **_kwargs: Any) -> Iterator[int]:
        yield run_idx

    def score(self, trace_id: int, *, name: str, value: Any, data_type: str, comment: str | None = None) -> None:
        self.scores[trace_id].append((name, value, comment))

    def quality(self, trace_id: int, **_kwargs: Any) -> None:
        self.scores[trace_id].append(("quality_score", None, None))

    def names(self, run_idx: int) -> list[str]:
        return [name for name, _, _ in self.scores[run_idx]]


def _scores(turns: list[Any]) -> _ScoreCtx:
    captured: dict[str, Any] = {}
    try:
        _evaluate(turns, captured)
    except (AssertionError, EvalHarnessError):
        pass
    ctx = _ScoreCtx()
    captured["write_scores"](ctx)
    return ctx


_VERDICT_SCORES = {"pass_at_k", "pass_power_k", "gate_passed", "quality_score", "pass_at_3", "pass_power_3"}


def test_on_an_error_run_gets_eval_error_only_and_the_scored_runs_keep_theirs(flag_on) -> None:
    ctx = _scores([_question_turn(), _viz_turn(), _viz_turn()])

    assert ctx.scores[0] == [("eval_error", 1, "harness: the simulated user failed to reply")]
    for run_idx in (1, 2):
        scores = {name: value for name, value, _ in ctx.scores[run_idx]}
        assert "eval_error" not in scores
        assert scores["gate_passed"] is True
        assert scores["pass_power_k"] is True
        assert "quality_score" in scores
    assert ctx.run_metadata["eval_k"] == 3


def test_on_an_item_whose_runs_all_errored_gets_no_gate_score(flag_on) -> None:
    ctx = _scores([_question_turn(), _question_turn(), _question_turn()])

    for run_idx in range(3):
        assert ctx.names(run_idx) == ["eval_error"]
    assert not any(_VERDICT_SCORES & set(ctx.names(run_idx)) for run_idx in range(3))


def test_on_a_backend_error_run_names_its_source(flag_on) -> None:
    ctx = _scores([ChatError("SSE stream error"), _viz_turn(), _viz_turn()])

    assert ctx.scores[0] == [("eval_error", 1, "backend: the chat call failed after its retries")]


def test_off_every_run_is_scored_as_before_and_none_gets_eval_error() -> None:
    ctx = _scores([_question_turn(), _viz_turn(), _viz_turn()])

    for run_idx in range(3):
        names = ctx.names(run_idx)
        assert "eval_error" not in names
        assert {"gate_passed", "pass_at_k", "pass_power_k", "quality_score"} <= set(names)
    assert dict((n, v) for n, v, _ in ctx.scores[0])["gate_passed"] is False


def test_a_scored_item_keeps_its_assertion_lead_and_an_errored_one_says_it_could_not_be_scored(flag_on) -> None:
    scored = resolve_runs(_MIXED, passed=lambda r: r.ok, gate="power", pass_at_k=True, pass_power_k=False)
    assert scored.message_lead("Alert skill assertion failed.", "Alert skill") == "Alert skill assertion failed."
    errored = resolve_runs(
        [_MIXED[0], _MIXED[0]], passed=lambda r: r.ok, gate="power", pass_at_k=False, pass_power_k=False
    )
    assert errored.errored is True
    assert (
        errored.message_lead("Alert skill assertion failed.", "Alert skill") == "Alert skill item could not be scored."
    )


# ── single-shot: the agent's own timeout is a failed run with the flag on ────


class _PassThenTimeout:
    def __init__(self, exc: Exception, fail_on: set[int]) -> None:
        self.exc = exc
        self.fail_on = fail_on
        self.calls = 0

    def ask(self, item: DatasetItem) -> ChatResult:
        self.calls += 1
        if self.calls in self.fail_on:
            raise self.exc
        return _viz_turn()


def _run_single_shot_with(backend: _PassThenTimeout, runs: int = 2) -> tuple[object, list[str]]:
    logged: list[str] = []
    report = run_items(
        [_single_shot_item()],
        backend,
        runs=runs,
        on_langfuse_item_done=lambda _i, _t, r: logged.append(r.id),
    )
    return report.items[0], logged


_AGENT_FAILURES = [
    (TurnTimeoutError("agent exceeded the 60s turn budget"), "agent_timeout"),
    (TurnIncompleteError("no final answer", reason="max iterations"), "turn_incomplete"),
]


@pytest.mark.parametrize(("exc", "exit_value"), _AGENT_FAILURES)
def test_off_a_single_shot_timeout_errors_the_item_as_before(exc, exit_value) -> None:
    item, logged = _run_single_shot_with(_PassThenTimeout(exc, {2}))

    assert item.error == f"{type(exc).__name__}: {exc}"
    assert item.pass_at_k is True
    assert item.runs == 1
    assert item.failed_runs == []
    assert logged == []


@pytest.mark.parametrize(("exc", "exit_value"), _AGENT_FAILURES)
def test_on_a_single_shot_timeout_is_a_failed_run_and_the_item_is_scored(flag_on, exc, exit_value) -> None:
    backend = _PassThenTimeout(exc, {2})
    item, logged = _run_single_shot_with(backend, runs=3)

    assert item.error is None
    assert backend.calls == 3
    assert (item.runs, item.runs_passed, item.pass_at_k, item.pass_power_k) == (3, 2, True, False)
    (record,) = item.failed_runs
    assert record["run_index"] == 2
    assert record["exit_reason"] == exit_value
    assert record["outcome"] == {"status": "fail", "source": None, "reason": f"loop exit: {exit_value}"}
    assert len(item.run_latencies_s) == 3
    assert logged == ["i1"]


def test_on_a_single_shot_item_that_only_timed_out_fails_and_is_not_an_error(flag_on) -> None:
    item, logged = _run_single_shot_with(_PassThenTimeout(TurnTimeoutError("too slow"), {1, 2}))

    assert item.error is None
    assert item.pass_at_k is False
    assert item.passed is False
    assert item.runs == 2
    assert [r["exit_reason"] for r in item.failed_runs] == ["agent_timeout", "agent_timeout"]
    assert logged == ["i1"]


def test_on_a_single_shot_backend_chat_error_still_errors_the_item(flag_on) -> None:
    item, _logged = _run_single_shot_with(_PassThenTimeout(ChatError("SSE stream error"), {2}))

    assert item.error == "ChatError: SSE stream error"
    assert item.pass_at_k is False


# ── flag off: an agentic message is the master text plus the always-on failing runs ──

# The flag-off message of [simulated user failed, agent silent, pass] under pass^3, as the
# package produced it before error outcomes existed. Only the "Failing runs" part of the gate
# line is new, and it is always on.
_MASTER_FLAG_OFF_MESSAGE = (
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "Agentic Visualization Assertion Failed! (Critical Mode)\n"
    "Gate pass^3 failed: 1/3 runs passed — unstable, not a clean failure.\n"
    "------------------------------------------\n"
    "Question:\n"
    "Show revenue by quarter\n"
    "------------------------------------------\n"
    "Expected Output:\n"
    "{\n"
    '  "id": "v1",\n'
    '  "type": "column_chart",\n'
    '  "query": {\n'
    '    "fields": {\n'
    '      "m": {\n'
    '        "using": "metric/revenue"\n'
    "      },\n"
    '      "d": {\n'
    '        "using": "label/date.quarter"\n'
    "      }\n"
    "    },\n"
    '    "filter_by": {},\n'
    '    "sort_by": []\n'
    "  },\n"
    '  "metrics": [\n'
    '    "m"\n'
    "  ],\n"
    '  "view_by": [\n'
    '    "d"\n'
    "  ],\n"
    '  "segment_by": [],\n'
    '  "rows": [],\n'
    '  "columns": [],\n'
    '  "size_by": []\n'
    "}\n"
    "------------------------------------------\n"
    "Actual Output:\n"
    "{\n"
    '  "id": "v1",\n'
    '  "type": "column_chart",\n'
    '  "query": {\n'
    '    "fields": {\n'
    '      "m": {\n'
    '        "using": "metric/revenue"\n'
    "      },\n"
    '      "d": {\n'
    '        "using": "label/date.quarter"\n'
    "      }\n"
    "    },\n"
    '    "filter_by": {},\n'
    '    "sort_by": []\n'
    "  },\n"
    '  "metrics": [\n'
    '    "m"\n'
    "  ],\n"
    '  "view_by": [\n'
    '    "d"\n'
    "  ],\n"
    '  "segment_by": [],\n'
    '  "rows": [],\n'
    '  "columns": [],\n'
    '  "size_by": []\n'
    "}\n"
    "------------------------------------------\n"
    "Strict Check Summary:\n"
    "  Visualization Created : True\n"
    "  Cross-Ref Valid       : True\n"
    "  Metrics Correct       : True\n"
    "    expected : ['metric/revenue']\n"
    "    actual   : ['metric/revenue']\n"
    "  Dimensions Correct    : True\n"
    "    expected : ['label/date.quarter']\n"
    "    actual   : ['label/date.quarter']\n"
    "  Filters Correct       : True\n"
    "    date      : True\n"
    "    ranking   : True\n"
    "    attribute : True\n"
    "  Viz Type Hard         : True\n"
    "  Executed              : False\n"
    "  Stated Value Matches  : None (reported only)\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
)


def test_off_the_agentic_message_is_the_master_text_plus_the_failing_runs() -> None:
    with pytest.raises(VisualizationAssertionError) as exc_info:
        _evaluate([_question_turn(), _silent_turn(), _viz_turn()])

    message = str(exc_info.value)
    gate_line = message.splitlines()[2]
    head, failing = gate_line.split(" Failing runs: ", 1)
    assert failing.startswith("run 1/3 FAIL (loop exit: simulated_user_failed): ")
    assert "; run 2/3 FAIL (loop exit: agent_silent): " in failing
    assert message.replace(gate_line, head, 1) == _MASTER_FLAG_OFF_MESSAGE

# (C) 2026 GoodData Corporation
"""PASS / FAIL / ERROR labels per run: they explain, they never rescore.

A run is ERROR only when the harness failed -- its simulated user, or its judge when the judge's
verdict was the one still open. Every other non-pass, a chat API error and the agent's own
timeout included, is FAIL. The labels change no gate or count: an ERROR run still counts as a
run that did not pass. The message names the ERROR runs and counts them in its gate note.
"""

from collections import defaultdict
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any
from unittest.mock import MagicMock, patch

import httpx
import pytest
from gooddata_eval.core.agentic import visualization as agentic_visualization
from gooddata_eval.core.agentic._gate import gate_failure_note
from gooddata_eval.core.agentic._outcome import (
    RunLabels,
    chat_failure_exit,
    failure_message_head,
    label_runs,
    mark_unscored_run,
)
from gooddata_eval.core.agentic.document_skill import _judge_error_of
from gooddata_eval.core.agentic.visualization import VisualizationAssertionError, evaluate_agentic_visualization
from gooddata_eval.core.chat.sse_client import ChatError, TransientChatError, TurnIncompleteError, TurnTimeoutError
from gooddata_eval.core.models import (
    AgenticAssertionError,
    AgenticEvalOutcome,
    ChatResult,
    CreatedVisualization,
    LoopExit,
)
from gooddata_eval.core.outcome import (
    JUDGE_FAILED,
    SETUP_ERRORS,
    Outcome,
    OutcomeStatus,
    classify_run,
    item_outcome,
    setup_error,
    shadow_verdict,
)

PASS = Outcome.passed()
FAIL = Outcome.failed("agent_silent")
SIM = Outcome.error("simulated_user_failed")
JUDGE = Outcome.error(JUDGE_FAILED)


# ── the rule: an allowlist of harness causes, everything else is FAIL ─────────

# Every LoopExit, with the label of a run that ended on it without passing. Exhaustive on
# purpose: a new member must be classified here before the suite passes.
_EXPECTED = {
    LoopExit.SUCCESS: OutcomeStatus.FAIL,
    LoopExit.AGENT_SILENT: OutcomeStatus.FAIL,
    LoopExit.BUDGET_EXHAUSTED: OutcomeStatus.FAIL,
    LoopExit.STOPPED_EARLY: OutcomeStatus.FAIL,
    LoopExit.SIMULATED_USER_FAILED: OutcomeStatus.ERROR,
    LoopExit.CHAT_ERROR: OutcomeStatus.FAIL,
    LoopExit.AGENT_TIMEOUT: OutcomeStatus.FAIL,
    LoopExit.TURN_INCOMPLETE: OutcomeStatus.FAIL,
    LoopExit.NOT_RUN: OutcomeStatus.FAIL,
}


def test_every_loop_exit_is_classified() -> None:
    assert set(_EXPECTED) == set(LoopExit)


@pytest.mark.parametrize("loop_exit", list(LoopExit))
def test_each_loop_exit_has_its_label_and_names_itself_as_the_reason(loop_exit: LoopExit) -> None:
    outcome = classify_run(loop_exit, passed=False)
    assert outcome.status is _EXPECTED[loop_exit]
    assert outcome.reason == loop_exit.value
    assert classify_run(loop_exit.value, passed=False) == outcome


@pytest.mark.parametrize("loop_exit", list(LoopExit))
def test_a_run_that_passed_is_pass_whatever_its_exit(loop_exit: LoopExit) -> None:
    assert classify_run(loop_exit, passed=True) == PASS


def test_a_judge_failure_is_an_error_whatever_the_exit() -> None:
    assert classify_run(LoopExit.SUCCESS, passed=False, judge_error="empty body twice") == JUDGE
    assert classify_run(None, passed=False, judge_error="unparseable JSON") == JUDGE


def test_an_unknown_cause_is_a_failure_never_an_error() -> None:
    assert classify_run("some_new_exit", passed=False) == Outcome.failed("some_new_exit")
    assert classify_run(None, passed=False) == Outcome.failed(None)


def test_an_outcome_record_is_json_ready() -> None:
    assert SIM.as_record() == {"status": "error", "reason": "simulated_user_failed"}
    assert Outcome.failed("chat_error").as_record() == {"status": "fail", "reason": "chat_error"}


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
def test_a_chat_failure_maps_to_its_own_exit_and_is_a_failure(exc: BaseException, loop_exit: LoopExit) -> None:
    assert chat_failure_exit(exc) is loop_exit
    assert classify_run(chat_failure_exit(exc), passed=False).status is OutcomeStatus.FAIL


# ── the item: ERROR only when no run was scored ──────────────────────────────


def test_an_item_is_an_error_only_when_every_run_errored() -> None:
    assert item_outcome([SIM, SIM, SIM]) == SIM
    assert item_outcome([SIM, PASS, PASS]) is None
    assert item_outcome([SIM, FAIL]) is None
    assert item_outcome([]) is None


def test_an_errored_item_names_its_most_frequent_reason() -> None:
    assert item_outcome([SIM, JUDGE, JUDGE]) == JUDGE


# ── the shadow verdict: the phase-2 candidate rule, recorded and never used ──


@pytest.mark.parametrize(
    ("outcomes", "gate", "verdict", "scored"),
    [
        ([SIM, PASS, PASS], "power", "pass", 2),
        ([SIM, SIM, PASS], "power", "error", 1),  # fewer than ceil(3/2) scored runs
        ([SIM, SIM, SIM], "power", "error", 0),
        ([Outcome.failed("chat_error"), PASS, PASS], "power", "fail", 3),  # a chat error is scored
        ([SIM, PASS], "power", "pass", 1),  # K=2 needs one scored run
        ([SIM], "power", "error", 0),
        ([SIM, FAIL, PASS], "any", "pass", 2),
        ([PASS, PASS, PASS], "power", "pass", 3),
    ],
)
def test_the_shadow_verdict(outcomes: list[Outcome], gate: str, verdict: str, scored: int) -> None:
    assert shadow_verdict(outcomes, gate) == {"verdict": verdict, "runs_scored": scored, "runs_total": len(outcomes)}


class _Run:
    def __init__(self, ok: bool, exit_reason: LoopExit | None = None, judge_error: str | None = None) -> None:
        self.ok = ok
        self.exit_reason = exit_reason
        self.judge_error = judge_error


def test_label_runs_reads_each_runs_exit_and_judge() -> None:
    runs = [
        _Run(False, LoopExit.SIMULATED_USER_FAILED),
        _Run(False, LoopExit.SUCCESS, judge_error="no verdict"),
        _Run(True, LoopExit.SUCCESS),
        _Run(False, LoopExit.CHAT_ERROR),
    ]
    labels = label_runs(runs, passed=lambda r: r.ok)
    assert labels.outcomes == (SIM, JUDGE, PASS, Outcome.failed("chat_error"))
    assert labels.error_label(0) == SIM
    assert labels.error_label(2) is None
    assert labels.error_label(3) is None
    assert labels.error_label(9) is None
    assert labels.item_outcome is None
    assert labels.shadow("power") == {"verdict": "fail", "runs_scored": 2, "runs_total": 4}


def test_a_kind_can_name_its_own_judge_error() -> None:
    run = _Run(False, LoopExit.SUCCESS, judge_error="takeaway request failed")
    assert label_runs([run], passed=lambda r: r.ok).outcomes == (JUDGE,)
    labels = label_runs([run], passed=lambda r: r.ok, judge_error=lambda r: None)
    assert labels.outcomes == (Outcome.failed("success"),)


class _Evaluation:
    def __init__(self, judge_error: str | None, fill_error: str | None, checks_held: bool) -> None:
        self.judge_error = judge_error
        self.fill_error = fill_error
        self.ungraded = (judge_error is not None or fill_error is not None) and checks_held


class _DocRun:
    def __init__(self, judge_error: str | None, fill_error: str | None, checks_held: bool = True) -> None:
        self.evaluation = _Evaluation(judge_error, fill_error, checks_held)
        self.exit_reason = None


def test_a_document_run_whose_takeaway_request_failed_is_a_failure_not_a_judge_error() -> None:
    request_failed = _DocRun(judge_error=None, fill_error="503 from the takeaway endpoint")
    judge_failed = _DocRun(judge_error="empty body twice", fill_error=None)
    labels = label_runs([request_failed, judge_failed], passed=lambda r: False, judge_error=_judge_error_of)
    assert labels.outcomes == (Outcome.failed(None), JUDGE)


def test_a_document_run_that_failed_a_fixed_check_is_a_failure_even_when_the_judge_errors() -> None:
    run = _DocRun(judge_error="empty body twice", fill_error=None, checks_held=False)
    labels = label_runs([run], passed=lambda r: False, judge_error=_judge_error_of)
    assert labels.outcomes == (Outcome.failed(None),)


def test_an_unscored_run_gets_the_marker_only_when_the_harness_failed() -> None:
    ctx = MagicMock()
    mark_unscored_run(ctx, 0, "conv-1", JUDGE)
    ctx.export_unscored.assert_not_called()
    ctx.score.assert_called_once()
    assert ctx.score.call_args.kwargs == {
        "name": "eval_error",
        "value": 1,
        "data_type": "NUMERIC",
        "comment": "judge_failed",
    }

    ctx = MagicMock()
    mark_unscored_run(ctx, 1, "conv-2", None)
    ctx.export_unscored.assert_called_once_with(1, "conv-2")
    ctx.score.assert_not_called()


# ── end to end through the visualization kind: labels, never a new verdict ───


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


def _evaluate(turns: list[Any], captured: dict[str, Any] | None = None, gate: str = "power") -> object:
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
            gate=gate,
            langfuse=MagicMock() if captured is not None else None,
            dataset_item_id="item-1" if captured is not None else None,
        )


def _silent_turn() -> ChatResult:
    return ChatResult.model_validate({})


def test_a_simulated_user_failure_keeps_the_verdict_and_is_labelled() -> None:
    with pytest.raises(VisualizationAssertionError) as exc_info:
        _evaluate([_question_turn(), _viz_turn(), _viz_turn()])

    exc = exc_info.value
    message = str(exc)
    lines = message.splitlines()
    assert lines[1] == "Agentic Visualization Assertion Failed! (Critical Mode)"
    # The gate counts the errored run as a run that did not pass: pass^3, 2/3. The note does
    # not call that instability: the agent was not what failed it.
    assert lines[2].startswith(gate_failure_note("power", 2, 3, runs_errored=1))
    assert "unstable" not in lines[2]
    assert "run 1/3 ERROR (simulated_user_failed): visualization_created[expected true, actual false]" in lines[2]
    assert (exc.runs_passed, exc.runs_effective) == (2, 3)
    (record,) = exc.failed_runs
    assert record["exit_reason"] == "simulated_user_failed"
    assert record["outcome"] == {"status": "error", "reason": "simulated_user_failed"}
    # Some runs were scored, so the item is not a harness error.
    assert not hasattr(exc, "harness_error")
    assert exc.shadow == {"verdict": "pass", "runs_scored": 2, "runs_total": 3}


def test_a_passing_item_records_its_shadow_verdict_too() -> None:
    # pass@3 passes on the one scored run; the candidate rule, wanting ceil(3/2) scored runs,
    # would not. Only a shadow recorded on a passing item shows that.
    outcome = _evaluate([_question_turn(), _question_turn(), _viz_turn()], gate="any")
    assert isinstance(outcome, AgenticEvalOutcome)
    assert outcome.shadow == {"verdict": "error", "runs_scored": 1, "runs_total": 3}
    assert [r["outcome"]["status"] for r in outcome.failed_runs] == ["error", "error"]


def test_an_item_whose_every_run_errored_is_labelled_and_still_fails() -> None:
    with pytest.raises(VisualizationAssertionError) as exc_info:
        _evaluate([_question_turn(), _question_turn(), _question_turn()])

    exc = exc_info.value
    assert isinstance(exc, AgenticAssertionError)
    assert exc.harness_error == {"status": "error", "reason": "simulated_user_failed"}
    assert exc.shadow == {"verdict": "error", "runs_scored": 0, "runs_total": 3}
    gate_line = str(exc).splitlines()[2]
    assert gate_line.startswith(
        f"Harness error on every run (simulated_user_failed). {gate_failure_note('power', 0, 3, runs_errored=3)}"
    )
    assert exc.runs_passed == 0
    assert len(exc.failed_runs) == 3


def test_the_head_says_no_run_was_scored_only_when_every_judge_failed() -> None:
    labels = RunLabels((Outcome.error(JUDGE_FAILED), Outcome.error(JUDGE_FAILED)))
    head = failure_message_head("power", labels, runs_passed=0, failed_runs=[], runs_ungraded=2)
    assert head.startswith("Harness error, no run was scored (judge_failed). ")


def test_the_head_does_not_say_unscored_when_a_simulated_user_failed() -> None:
    """A run whose simulated user failed was still checked; its failed checks follow the head."""
    labels = RunLabels((Outcome.error("simulated_user_failed"), Outcome.error(JUDGE_FAILED)))
    head = failure_message_head("power", labels, runs_passed=0, failed_runs=[], runs_ungraded=1)
    assert head.startswith("Harness error on every run (judge_failed). ")
    assert "no run was scored" not in head


@pytest.mark.parametrize(
    ("exc", "exit_value"),
    [
        (TurnTimeoutError("agent exceeded the 60s turn budget"), "agent_timeout"),
        (TurnIncompleteError("no final answer", reason="max iterations"), "turn_incomplete"),
        (ChatError("SSE stream error"), "chat_error"),
    ],
)
def test_a_chat_failure_is_a_plain_failure(exc: BaseException, exit_value: str) -> None:
    with pytest.raises(VisualizationAssertionError) as exc_info:
        _evaluate([exc, _viz_turn(), _viz_turn()])

    raised = exc_info.value
    assert (raised.runs_passed, raised.runs_effective) == (2, 3)
    (record,) = raised.failed_runs
    assert record["exit_reason"] == exit_value
    assert record["outcome"] == {"status": "fail", "reason": exit_value}
    assert f"run 1/3 FAIL (loop exit: {exit_value})" in str(raised)
    assert "ERROR" not in str(raised)
    assert not hasattr(raised, "harness_error")
    assert raised.shadow["verdict"] == "fail"


def test_only_timeouts_is_a_failure_not_a_harness_error() -> None:
    timeout = TurnTimeoutError("agent exceeded the 60s turn budget")
    with pytest.raises(VisualizationAssertionError) as exc_info:
        _evaluate([timeout, timeout, timeout])

    assert not hasattr(exc_info.value, "harness_error")
    assert str(exc_info.value).splitlines()[2].startswith(gate_failure_note("power", 0, 3))


# ── Langfuse: an ERROR run gets an extra marker, every usual score stays ──────


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
    except AssertionError:
        pass
    ctx = _ScoreCtx()
    captured["write_scores"](ctx)
    return ctx


_USUAL_SCORES = {"gate_passed", "pass_at_k", "pass_power_k", "quality_score"}


def test_an_errored_run_gets_eval_error_beside_its_usual_scores() -> None:
    ctx = _scores([_question_turn(), _viz_turn(), _viz_turn()])

    assert ("eval_error", 1, "simulated_user_failed") in ctx.scores[0]
    assert set(ctx.names(0)) >= _USUAL_SCORES
    # The verdict scores are the ones the item was judged by: unchanged by the label.
    assert dict((n, v) for n, v, _ in ctx.scores[0])["gate_passed"] is False
    for run_idx in (1, 2):
        assert "eval_error" not in ctx.names(run_idx)
        assert set(ctx.names(run_idx)) >= _USUAL_SCORES


def test_a_chat_error_run_gets_no_marker() -> None:
    ctx = _scores([ChatError("SSE stream error"), _viz_turn(), _viz_turn()])

    for run_idx in range(3):
        assert "eval_error" not in ctx.names(run_idx)
        assert set(ctx.names(run_idx)) >= _USUAL_SCORES


# ── the message: the gate note and the failing runs, then the best run ───────

# The message of [simulated user failed, agent silent, pass] under pass^3, with the "Failing
# runs" part of its gate line left out. The best run's summary follows the gate line.
_MESSAGE_WITHOUT_FAILING_RUNS = (
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "Agentic Visualization Assertion Failed! (Critical Mode)\n"
    "Gate pass^3 failed: 1/3 runs passed, 1 harness error(s) — unstable, not a clean failure.\n"
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


def test_the_agentic_message_is_the_gate_note_the_failing_runs_and_the_best_run() -> None:
    with pytest.raises(VisualizationAssertionError) as exc_info:
        _evaluate([_question_turn(), _silent_turn(), _viz_turn()])

    message = str(exc_info.value)
    gate_line = message.splitlines()[2]
    head, failing = gate_line.split(" Failing runs: ", 1)
    # A chartless run names only the missing chart, not every chart check that read False.
    assert failing.startswith(
        "run 1/3 ERROR (simulated_user_failed): visualization_created[expected true, actual false]; "
    )
    assert failing.endswith(
        "; run 2/3 FAIL (loop exit: agent_silent): visualization_created[expected true, actual false]."
    )
    # The gate note names the errored run, and run 2 failed on its own beside a passing run 3,
    # so the item is still unstable.
    assert head == "Gate pass^3 failed: 1/3 runs passed, 1 harness error(s) — unstable, not a clean failure."
    assert message.replace(gate_line, head, 1) == _MESSAGE_WITHOUT_FAILING_RUNS


def test_a_setup_error_is_an_error_only_for_a_known_cause() -> None:
    assert sorted(SETUP_ERRORS) == ["data_baseline_changed", "widget_execution_failed"]
    assert setup_error("widget_execution_failed").as_record() == {
        "status": "error",
        "reason": "widget_execution_failed",
    }
    with pytest.raises(ValueError, match="not a setup error"):
        setup_error("chat_error")

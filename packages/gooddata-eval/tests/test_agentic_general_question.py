# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
import contextlib
import io
import time
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.agentic.general_question import (
    GeneralQuestionAssertionError,
    GeneralQuestionResult,
    evaluate_agentic_general_question,
    run_agentic_general_question,
)
from gooddata_eval.core.evaluators._llm_judge import JudgeResponseError
from gooddata_eval.core.models import ChatResult
from gooddata_eval.core.timing import TIMERS_ENV_VAR

# --- time.monotonic() side effects ---------------------------------------------------
#
# One run reads the clock six times, in this order: item start, agent start, agent stop,
# judge start, judge stop, item stop. A K-run test therefore needs six values per run.
# Named rather than inlined because a single new clock read on the production path breaks
# every one of these at once with StopIteration -- and repairing a bare literal means
# hand-counting clock reads at each call site.

# one run: agent 2.50s, judge 1.50s, item total 4.50s
_CLOCK_AGENT_2_5_JUDGE_1_5 = [10.0, 10.5, 13.0, 13.0, 14.5, 14.5]
# one run: agent 2.0s, judge 1.0s
_CLOCK_AGENT_2_JUDGE_1 = [0.0, 0.0, 2.0, 2.0, 3.0, 3.0]
# one run: agent 4.0s, judge 2.0s
_CLOCK_AGENT_4_JUDGE_2 = [0.0, 0.0, 4.0, 4.0, 6.0, 6.0]
# two runs: agent 2.0s + 3.0s, judge 1.0s + 0.5s
_CLOCK_TWO_RUNS_AGENT_5_JUDGE_1_5 = [0.0, 0.0, 2.0, 2.0, 3.0, 3.0, 10.0, 10.0, 13.0, 13.0, 13.5, 13.5]
# two runs: agent 4.0s + 3.0s, judge 1.0s each
_CLOCK_TWO_RUNS_AGENT_7_JUDGE_2 = [0.0, 0.0, 4.0, 4.0, 5.0, 5.0, 10.0, 10.0, 13.0, 13.0, 14.0, 14.0]


def _pass_client_and_judge(
    *, text_response: str = "42", reasoning_steps: list[str] | None = None, response_id: str = "resp-1"
):
    """A chat client on conversation ``conv-1`` and a gpt-4o judge that passes every run.

    Callers override only the one field they vary -- ``client.create_conversation``,
    ``judge.score.return_value`` and so on are ordinary mock attributes.
    """
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": text_response,
            "toolCallEvents": [],
            "reasoningSteps": reasoning_steps or [],
            "responseId": response_id,
        }
    )
    judge = MagicMock()
    judge.model = "gpt-4o"
    judge.score.return_value = (True, "Correct answer")
    return client, judge


@contextlib.contextmanager
def _patched(client, judge, *, monotonic=None):
    """Patch general_question's ChatClient and LLMJudge, and optionally the clock.

    ``monotonic`` is the ``time.monotonic()`` side-effect list (one of the ``_CLOCK_*``
    constants above) for tests that assert on timings.
    """
    with (
        patch("gooddata_eval.core.agentic.general_question.ChatClient", return_value=client),
        patch("gooddata_eval.core.agentic.general_question.LLMJudge", return_value=judge),
    ):
        if monotonic is None:
            yield
        else:
            with patch("time.monotonic", side_effect=monotonic):
                yield


def _no_traces(*_args, **_kwargs):
    return {}


@contextlib.contextmanager
def _patched_langfuse(client, judge, *, find=_no_traces):
    """Patch the chat/judge pair plus the two _langfuse helpers the linker calls.

    ``find`` stands in for ``find_traces_per_conversation`` (default: finds nothing).
    Yields ``(mock_find_traces_per_conversation, mock_build_run_context)``.
    """
    with (
        _patched(client, judge),
        patch("gooddata_eval.core.agentic._langfuse.find_traces_per_conversation", side_effect=find) as mock_find,
        patch("gooddata_eval.core.agentic._langfuse.build_run_context", return_value=("run", {})) as mock_ctx,
    ):
        yield mock_find, mock_ctx


def test_general_question_result_fields():
    r = GeneralQuestionResult(
        conversation_id="c1",
        actual_output="42",
        passed=True,
        llm_judge_score=1.0,
        reasoning="Correct",
    )
    assert r.passed is True
    assert r.llm_judge_score == 1.0


def test_run_agentic_general_question_pass():
    client, judge = _pass_client_and_judge(text_response="The answer is 42")

    with _patched(client, judge):
        summary = run_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What is 6 times 7?",
            expected_output="42",
        )

    assert summary.pass_at_k is True
    assert summary.best.passed is True
    client.close.assert_called_once()


def test_run_agentic_general_question_logs_agent_and_judge_timing(monkeypatch, capsys):
    monkeypatch.setenv(TIMERS_ENV_VAR, "1")
    client, judge = _pass_client_and_judge(text_response="The answer is 42")

    with _patched(client, judge, monotonic=_CLOCK_AGENT_2_5_JUDGE_1_5):
        run_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What is 6 times 7?",
            expected_output="42",
        )

    output = capsys.readouterr().out
    assert "[timer] general_question conv-1 GoodData response complete after 2.50s; waiting for gpt-4o judge" in output
    assert "[timer] general_question conv-1 gpt-4o judge complete after 1.50s; item total 4.50s" in output


def test_run_agentic_general_question_uses_initial_conversation_for_run_0():
    client, judge = _pass_client_and_judge()

    with _patched(client, judge):
        run_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What is 6 times 7?",
            expected_output="42",
            k=1,
            initial_conversation_id="existing-conv",
        )
    client.create_conversation.assert_not_called()
    client.delete_conversation.assert_not_called()


def test_run_agentic_general_question_creates_fresh_conversations_for_remaining_runs():
    client, judge = _pass_client_and_judge()
    client.create_conversation.side_effect = ["fresh-1", "fresh-2"]

    with _patched(client, judge):
        run_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What is 6 times 7?",
            expected_output="42",
            k=3,
            initial_conversation_id="existing-conv",
        )
    assert client.create_conversation.call_count == 2
    assert client.delete_conversation.call_count == 2


def test_run_agentic_general_question_captures_reasoning_steps():
    client, judge = _pass_client_and_judge(reasoning_steps=["recalling the answer"])

    with _patched(client, judge):
        summary = run_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What is the answer?",
            expected_output="42",
            k=1,
        )

    assert summary.best.reasoning_steps == ["recalling the answer"]
    assert summary.best.response_id == "resp-1"


def test_evaluate_agentic_general_question_returns_reasoning_steps_on_pass():
    client, judge = _pass_client_and_judge(reasoning_steps=["recalling the answer"])

    with _patched(client, judge):
        outcome = evaluate_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What is the answer?",
            expected_output="42",
            k=1,
        )

    assert outcome.reasoning_steps == ["recalling the answer"]
    assert outcome.conversation_id == "conv-1"
    assert outcome.response_id == "resp-1"
    assert outcome.detail == {
        "judge_passed": True,
        "judge_reasoning": "Correct answer",
        "actual_output": "42",
    }


def test_evaluate_agentic_general_question_attaches_reasoning_steps_to_exception_on_fail():
    client, judge = _pass_client_and_judge(
        text_response="I don't know", reasoning_steps=["unable to find the answer"], response_id="resp-2"
    )
    judge.score.return_value = (False, "Wrong answer")

    with _patched(client, judge), pytest.raises(GeneralQuestionAssertionError) as exc_info:
        evaluate_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What is the answer?",
            expected_output="42",
            k=1,
        )

    assert exc_info.value.reasoning_steps == ["unable to find the answer"]
    assert exc_info.value.conversation_id == "conv-1"
    assert exc_info.value.response_id == "resp-2"
    assert exc_info.value.detail == {
        "judge_passed": False,
        "judge_reasoning": "Wrong answer",
        "actual_output": "I don't know",
    }


def test_evaluate_general_question_defers_langfuse_work_to_the_injected_linker():
    # The verdict is already decided once the judge returns; finding the gen-ai trace only
    # publishes it. Handing that work to the linker is what takes the poll (and the SDK
    # round-trip inside build_run_context) off the item's critical path.
    client, judge = _pass_client_and_judge()
    submitted = []

    with _patched_langfuse(client, judge) as (mock_find, mock_ctx):
        outcome = evaluate_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What is the answer?",
            expected_output="42",
            k=1,
            langfuse=MagicMock(),
            dataset_item_id="ds-item-1",
            submit_trace_link=lambda task, item_id="": submitted.append(task),
        )

        assert outcome.detail["judge_passed"] is True
        mock_find.assert_not_called()
        mock_ctx.assert_not_called()
        assert len(submitted) == 1

        submitted[0]()
        mock_find.assert_called_once()
        mock_ctx.assert_called_once()


def test_evaluate_general_question_links_traces_inline_by_default():
    # Backward compatibility: a caller that injects no linker (pytest suites calling
    # evaluate_agentic_* directly) must still get fully-synchronous trace linking.
    client, judge = _pass_client_and_judge()

    with _patched_langfuse(client, judge) as (mock_find, _):
        evaluate_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What is the answer?",
            expected_output="42",
            k=1,
            langfuse=MagicMock(),
            dataset_item_id="ds-item-1",
        )

    mock_find.assert_called_once()


def test_evaluate_general_question_submits_trace_link_even_when_the_item_fails():
    # A failing item's scores matter more than a passing one's. The submit has to happen
    # before the assertion is raised, or every failure would drop out of Langfuse.
    client, judge = _pass_client_and_judge()
    judge.score.return_value = (False, "Wrong answer")
    submitted = []

    with _patched_langfuse(client, judge), pytest.raises(GeneralQuestionAssertionError):
        evaluate_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What is the answer?",
            expected_output="42",
            k=1,
            langfuse=MagicMock(),
            dataset_item_id="ds-item-1",
            submit_trace_link=lambda task, item_id="": submitted.append(task),
        )

    assert len(submitted) == 1


def test_records_agent_and_judge_latency_separately():
    # Deliberately distinct durations: if the two were ever swapped or summed, this fails.
    # Agent latency is the number that describes GoodData; judge latency is the cost of
    # OUR grading of it, and a report that conflates them cannot answer either question.
    client, judge = _pass_client_and_judge(text_response="The answer is 42")

    with _patched(client, judge, monotonic=_CLOCK_AGENT_2_5_JUDGE_1_5):
        summary = run_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What is 6 times 7?",
            expected_output="42",
        )

    timings = summary.run_results[0].timings
    assert timings.agent_s == 2.5
    assert timings.judge_s == 1.5
    # general_question drives no simulated user and does its trace linking elsewhere.
    assert timings.simulated_user_s == 0.0
    assert timings.langfuse_s == 0.0


def test_evaluate_general_question_aggregates_timings_across_k_runs():
    # pass@K runs K conversations; the item's agent cost is all of them, and so is its
    # judge cost. Reporting only the last run's would understate both.
    client, judge = _pass_client_and_judge()

    with _patched(client, judge, monotonic=_CLOCK_TWO_RUNS_AGENT_5_JUDGE_1_5):
        outcome = evaluate_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What is the answer?",
            expected_output="42",
            k=2,
        )

    assert outcome.timings.agent_s == 5.0  # 2.0 + 3.0
    assert outcome.timings.judge_s == 1.5  # 1.0 + 0.5


def test_evaluate_general_question_attaches_timings_to_the_failure_exception():
    # A slow item that also fails is the one worth diagnosing, so the breakdown has to
    # survive the raise -- same contract the reasoning_steps/conversation_id already have.
    client, judge = _pass_client_and_judge()
    judge.score.return_value = (False, "Wrong answer")

    with (
        _patched(client, judge, monotonic=_CLOCK_AGENT_4_JUDGE_2),
        pytest.raises(GeneralQuestionAssertionError) as exc_info,
    ):
        evaluate_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What is the answer?",
            expected_output="42",
            k=1,
        )

    assert exc_info.value.timings.agent_s == 4.0
    assert exc_info.value.timings.judge_s == 2.0


def test_trace_link_window_is_pinned_at_submit_time_not_when_the_task_runs():
    # The deferred task must query the same window the old inline code would have. If
    # window_end drifted to whenever a worker dequeued the task, a backed-up pool would
    # silently widen every later item's window (see the _FETCH_LIMIT paging note in
    # test_agentic_langfuse_trace.py).
    client, judge = _pass_client_and_judge()
    submitted = []
    captured = {}

    def _find(langfuse, conversation_ids, window_start, window_end=None):
        captured["end"] = window_end
        return {}

    with _patched_langfuse(client, judge, find=_find):
        evaluate_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What is the answer?",
            expected_output="42",
            k=1,
            langfuse=MagicMock(),
            dataset_item_id="ds-item-1",
            submit_trace_link=lambda task, item_id="": submitted.append(task),
        )
        returned_at = datetime.now(timezone.utc)
        time.sleep(0.05)  # the task sits in the queue behind other items
        submitted[0]()

    assert captured["end"] is not None, "window_end was left to drift to the task's run time"
    assert captured["end"] <= returned_at


def test_k_runs_submit_one_trace_link_covering_every_conversation():
    # Characterization guard for the --runs K path: K conversations produce ONE deferred
    # task that looks up all of them together, exactly as the old inline block did. Per-run
    # submission would multiply the queue depth and re-order the _run0/_run1 naming.
    client, judge = _pass_client_and_judge()
    client.create_conversation.side_effect = ["conv-a", "conv-b"]
    submitted = []

    def _find(langfuse, conversation_ids, window_start, window_end=None):
        _find.seen = list(conversation_ids)
        return {}

    with _patched_langfuse(client, judge, find=_find):
        evaluate_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What is the answer?",
            expected_output="42",
            k=2,
            langfuse=MagicMock(),
            dataset_item_id="ds-item-1",
            submit_trace_link=lambda task, item_id="": submitted.append(task),
        )
        assert len(submitted) == 1
        submitted[0]()

    assert _find.seen == ["conv-a", "conv-b"]


def _run_gq_capturing_output(monotonic_values):
    client, judge = _pass_client_and_judge()
    with _patched(client, judge, monotonic=monotonic_values):
        run_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="q",
            expected_output="42",
        )


def test_no_timer_output_by_default(monkeypatch, capsys):
    # 72 [timer] lines on an 18-item --runs 2 run buried the progress output. The numbers
    # live on in latency_breakdown_s, so silence costs nothing.
    monkeypatch.delenv(TIMERS_ENV_VAR, raising=False)
    _run_gq_capturing_output(_CLOCK_AGENT_2_5_JUDGE_1_5)

    assert "[timer]" not in capsys.readouterr().out


def test_timings_are_still_recorded_when_timer_output_is_off(monkeypatch, capsys):
    # The gate must silence the printing only -- never the measuring.
    monkeypatch.setenv(TIMERS_ENV_VAR, "0")
    client, judge = _pass_client_and_judge()
    with _patched(client, judge, monotonic=_CLOCK_AGENT_2_5_JUDGE_1_5):
        summary = run_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="q",
            expected_output="42",
        )

    assert "[timer]" not in capsys.readouterr().out
    assert summary.run_results[0].timings.agent_s == 2.5
    assert summary.run_results[0].timings.judge_s == 1.5


def test_timer_lines_name_the_configured_judge_model(monkeypatch):
    # The model name used to be a literal in the message, so --judge-model gpt-5.6-luna
    # still logged "waiting for gpt-4o judge" -- actively misleading in the one output
    # a developer reads to see what the judge cost.
    monkeypatch.setenv(TIMERS_ENV_VAR, "1")
    client, judge = _pass_client_and_judge()
    judge.model = "gpt-5.6-luna"

    with _patched(client, judge, monotonic=_CLOCK_AGENT_2_JUDGE_1):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            run_agentic_general_question(
                host="http://host/api/v1/actions/workspaces/ws1/ai",
                token="tok",
                workspace_id="ws1",
                question="q",
                expected_output="42",
            )
        out = buf.getvalue()

    assert "waiting for gpt-5.6-luna judge" in out
    assert "gpt-5.6-luna judge complete" in out
    assert "gpt-4o" not in out


# --- a judge fault on one run must not cost the whole item (H1) ---


def _client_and_flaky_judge(verdicts):
    """A client that answers every turn, and a judge that returns `verdicts` in order.

    A JudgeResponseError in the list is raised for that run instead of returning.
    """
    client, judge = _pass_client_and_judge()
    client.create_conversation.side_effect = [f"conv-{i}" for i in range(1, 9)]
    it = iter(verdicts)

    def score(**_kw):
        v = next(it)
        if isinstance(v, Exception):
            raise v
        return v

    judge.score.side_effect = score
    return client, judge


def test_a_judge_fault_on_the_last_run_keeps_the_pass_that_run_one_earned():
    """pass@2 is satisfied the moment run 0 passes.

    Letting the error out of the K-run loop discarded run 0 entirely, so an item that had
    already passed was reported as an error -- and `EvalReport` counts an errored item
    against the pass rate, which is the "parse bug reads as a pass-rate drop" that
    JudgeResponseError was introduced to end.
    """
    client, judge = _client_and_flaky_judge([(True, "run 0 is correct"), JudgeResponseError("empty body twice")])

    with _patched(client, judge):
        summary = run_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What is the answer?",
            expected_output="42",
            k=2,
        )

    assert summary.pass_at_k is True
    assert len(summary.run_results) == 2, "the ungraded run is still recorded"
    assert len(summary.scored_run_results) == 1, "but only the graded one counts"
    assert summary.judge_errors == ["empty body twice"]
    # pass^K cannot be claimed over a run nobody graded.
    assert summary.pass_power_k is False
    assert summary.best.passed is True, "best must be a run that actually has a verdict"


def test_an_ungraded_run_is_not_counted_as_a_failure():
    # The other half of the same rule: with run 0 failing and run 1 ungraded the item
    # fails on run 0's verdict alone -- not because two runs "failed".
    client, judge = _client_and_flaky_judge([(False, "wrong"), JudgeResponseError("unparseable JSON")])

    with _patched(client, judge):
        summary = run_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What is the answer?",
            expected_output="42",
            k=2,
        )

    assert summary.pass_at_k is False
    assert [r.judge_error is None for r in summary.run_results] == [True, False]


def test_the_agent_timing_of_an_ungraded_run_is_still_recorded():
    # The agent answered. That measurement is independent of whether our judge could read
    # its own reply, and it is the number the report is actually for.
    client, judge = _client_and_flaky_judge([JudgeResponseError("empty body twice"), (True, "ok")])

    with _patched(client, judge, monotonic=_CLOCK_TWO_RUNS_AGENT_7_JUDGE_2):
        summary = run_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What is the answer?",
            expected_output="42",
            k=2,
        )

    assert summary.run_results[0].judge_error is not None
    assert summary.run_results[0].timings.agent_s == 4.0


def test_an_ungraded_run_is_never_published_to_langfuse_as_a_zero():
    """Writing float(run.passed) for an ungraded run moves the silent FAIL into Langfuse.

    Scores are what the dashboards read, so a 0 the judge never returned there is worse
    than no score at all.
    """
    client, judge = _client_and_flaky_judge([(True, "run 0 is correct"), JudgeResponseError("empty body twice")])
    submitted = []
    scored_conversations = []
    polled = {}

    def _find(langfuse, conversation_ids, window_start, window_end=None):
        polled["ids"] = list(conversation_ids)
        return dict.fromkeys(conversation_ids)

    with (
        _patched_langfuse(client, judge, find=_find),
        patch(
            "gooddata_eval.core.agentic._langfuse.score_safe",
            side_effect=lambda lf, tid, **kw: scored_conversations.append(kw["name"]),
        ),
    ):
        outcome = evaluate_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What is the answer?",
            expected_output="42",
            k=2,
            langfuse=MagicMock(),
            dataset_item_id="ds-item-1",
            submit_trace_link=lambda task, item_id="": submitted.append(task),
        )
        submitted[0]()

    # Exactly one run's worth of scores, from the run that had a verdict.
    assert scored_conversations.count("general_question_pass") == 1
    # And the ungraded conversation is not even polled for -- that would spend the item's
    # shared retry budget on a score that is never written.
    assert polled["ids"] == ["conv-1"]
    # The weaker pass is visible in the report rather than passed off as a clean pass@2.
    assert outcome.detail["unscored_runs"] == 1


def test_an_item_with_no_gradeable_run_raises_instead_of_reporting_failures():
    # Nothing was graded, so there is no verdict for this item at all: an error, not K
    # failures. This is the case JudgeResponseError is genuinely for.
    client, judge = _client_and_flaky_judge(
        [JudgeResponseError("empty body twice"), JudgeResponseError("no 'score' key")]
    )

    with (
        _patched(client, judge, monotonic=_CLOCK_TWO_RUNS_AGENT_7_JUDGE_2),
        pytest.raises(JudgeResponseError) as err,
    ):
        evaluate_agentic_general_question(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="What is the answer?",
            expected_output="42",
            k=2,
        )

    assert "no readable verdict for any of the 2 run(s)" in str(err.value)
    assert "no 'score' key" in str(err.value), "both causes are quoted"
    # Carried so the runner can still report what the item cost before it became
    # unevaluable.
    assert err.value.timings.agent_s == 7.0  # 4.0 + 3.0


def test_run_agentic_general_question_forwards_the_user_context_to_the_chat_client():
    attachment = {"referencedObjects": [{"objects": [{"type": "WIDGET", "id": "campaign_spend"}]}]}
    client, judge = _pass_client_and_judge(text_response="It shows campaign spend by channel.")

    with _patched(client, judge):
        run_agentic_general_question(
            host="https://h",
            token="tok",
            workspace_id="ws1",
            question="What does the visualization I attached show?",
            expected_output="Describes the attached chart.",
            k=1,
            user_context=attachment,
        )

    assert client.send_message.call_args.kwargs["user_context"] == attachment

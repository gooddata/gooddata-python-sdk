# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
import contextlib
from collections.abc import Iterator
from typing import Any
from unittest.mock import MagicMock, patch

import httpx
import pytest
from gooddata_eval.core.agentic.memory import (
    MemoryAssertionError,
    applied_memory_titles,
    evaluate_agentic_memory,
    memory_check_error,
    run_agentic_memory,
)
from gooddata_eval.core.chat.sse_client import TurnIncompleteError
from gooddata_eval.core.dataset.langfuse_source import _item_from_raw
from gooddata_eval.core.evaluators._llm_judge import JudgeResponseError
from gooddata_eval.core.models import ChatResult, DatasetItem, LoopExit, MemoryInput
from pydantic import ValidationError


def _apply_memory(response_id: str, *titles: str) -> dict[str, Any]:
    return {
        "role": "user",
        "responseId": response_id,
        "content": {"type": "text", "text": "q"},
        "detail": {
            "category": "applyMemory",
            "items": [{"title": t, "strategy": "ALWAYS", "score": None} for t in titles],
        },
    }


def _answer(response_id: str) -> dict[str, Any]:
    return {"role": "assistant", "responseId": response_id, "content": {"type": "text", "text": "a"}, "detail": None}


def _composed(response_id: str) -> dict[str, Any]:
    """The answer item of a turn gen-ai recorded details for (flag on)."""
    return {**_answer(response_id), "detail": {"category": "composeAnswer"}}


def _item(injected: tuple[str, ...] = ("help-line",), not_injected: tuple[str, ...] = ("off-item",)) -> DatasetItem:
    return DatasetItem(
        id="om-1",
        dataset_name="org_memory",
        test_kind="agentic_memory",
        question="How many orders did we have in 2024?",
        expected_output="Ends with the help line.",
        memory_input=MemoryInput(injected=list(injected), not_injected=list(not_injected)),
    )


def _client(items: list[dict[str, Any]] | Exception, response_id: str = "resp-1") -> MagicMock:
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    client.send_message.return_value = ChatResult.model_validate(
        {"textResponse": "8,963 orders. Questions? Ask the BI team.", "toolCallEvents": [], "responseId": response_id}
    )
    if isinstance(items, Exception):
        client.list_items.side_effect = items
    else:
        client.list_items.return_value = items
    return client


def _judge(passed: bool = True) -> MagicMock:
    judge = MagicMock()
    judge.model = "gpt-4o"
    judge.score.return_value = (passed, "judge reason")
    return judge


@contextlib.contextmanager
def _patched(client: MagicMock, judge: MagicMock) -> Iterator[None]:
    with (
        patch("gooddata_eval.core.agentic.memory.ChatClient", return_value=client),
        patch("gooddata_eval.core.agentic.memory.LLMJudge", return_value=judge),
    ):
        yield


# --- reading the injected memory ---------------------------------------------------------


def test_titles_come_from_the_apply_memory_detail_of_the_turn_only() -> None:
    items = [
        _apply_memory("old", "stale"),
        _answer("old"),
        _apply_memory("resp-1", "help-line", "returns"),
        _answer("resp-1"),
    ]
    assert applied_memory_titles(items, "resp-1") == ["help-line", "returns"]


def test_a_turn_without_any_detail_reads_as_none_not_as_no_memory() -> None:
    assert applied_memory_titles([_answer("resp-1")], "resp-1") is None
    assert applied_memory_titles([_composed("old"), _answer("resp-1")], "resp-1") is None
    assert applied_memory_titles([_apply_memory("resp-1")], "resp-1") == []


def test_a_turn_with_other_details_and_no_apply_memory_injected_nothing() -> None:
    assert applied_memory_titles([_composed("resp-1")], "resp-1") == []


def test_other_detail_categories_are_ignored() -> None:
    other = {**_answer("resp-1"), "detail": {"category": "skillRouting", "items": [{"title": "help-line"}]}}
    assert applied_memory_titles([other], "resp-1") == []


@pytest.mark.parametrize(
    ("applied", "error"),
    [
        (["help-line", "returns"], None),
        (["returns"], "not injected: ['help-line']"),
        (["help-line", "off-item"], "injected but must not be: ['off-item']"),
        ([], "not injected: ['help-line']"),
    ],
    ids=["match", "missing", "unwanted", "empty"],
)
def test_memory_check(applied: list[str], error: str | None) -> None:
    assert memory_check_error(MemoryInput(injected=["help-line"], not_injected=["off-item"]), applied) == error


def test_a_turn_without_the_detail_names_the_flag() -> None:
    error = memory_check_error(MemoryInput(injected=["help-line"]), None)
    assert error is not None and "enableGenAiInteractionIntelligence" in error


# --- memory_input ------------------------------------------------------------------------


@pytest.mark.parametrize(
    "raw",
    [
        {},
        {"injected": ["a"], "not_injected": ["a"]},
        {"injected": ["a"], "typo": ["b"]},
        {"not_injected": [" a"]},
        {"injected": [""]},
    ],
    ids=["empty", "both-lists", "unknown-key", "padded-title", "blank-title"],
)
def test_invalid_memory_input_is_rejected(raw: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        MemoryInput.model_validate(raw)


def test_langfuse_item_with_memory_input_is_a_memory_item() -> None:
    raw = {
        "id": "x",
        "input": "Net Sales FY24?",
        "expectedOutput": "Uses April 2024 - March 2025.",
        "metadata": {"memory_input": {"injected": ["fiscal-year"]}},
    }
    item = _item_from_raw(raw, dataset_name="org_memory", test_kind="visualization")
    assert item.test_kind == "agentic_memory"
    assert item.memory_input == MemoryInput(injected=["fiscal-year"])


def test_langfuse_item_with_a_broken_memory_input_fails_loudly() -> None:
    raw = {"id": "x", "input": "q", "expectedOutput": "e", "metadata": {"memory_input": ["fiscal-year"]}}
    with pytest.raises(ValueError, match="memory_input must be a JSON object"):
        _item_from_raw(raw, dataset_name="org_memory", test_kind="visualization")


# --- one run -----------------------------------------------------------------------------


def test_a_run_passes_when_the_memory_and_the_answer_pass() -> None:
    client = _client([_apply_memory("resp-1", "help-line"), _answer("resp-1")])
    with _patched(client, _judge(True)):
        summary = run_agentic_memory("https://h", "t", "ws", _item(), k=1)
    run = summary.run_results[0]
    assert (run.passed, run.applied_memory) == (True, ["help-line"])
    client.list_items.assert_called_once_with("conv-1")
    client.delete_conversation.assert_called_once_with("conv-1")


def test_a_good_answer_does_not_hide_missing_memory() -> None:
    client = _client([_apply_memory("resp-1", "returns"), _answer("resp-1")])
    with _patched(client, _judge(True)):
        run = run_agentic_memory("https://h", "t", "ws", _item(), k=1).run_results[0]
    assert run.judge_passed and not run.memory_passed and not run.passed


def test_injected_memory_does_not_hide_a_wrong_answer() -> None:
    client = _client([_apply_memory("resp-1", "help-line"), _answer("resp-1")])
    with _patched(client, _judge(False)):
        run = run_agentic_memory("https://h", "t", "ws", _item(), k=1).run_results[0]
    assert run.memory_passed and not run.passed


def test_an_unreadable_items_list_is_an_error_and_the_answer_is_still_judged() -> None:
    client = _client(httpx.ConnectError("down"))
    judge = _judge(True)
    with _patched(client, judge):
        run = run_agentic_memory("https://h", "t", "ws", _item(), k=1).run_results[0]
    assert run.memory_error is not None and "down" in run.memory_error
    assert run.exit_reason == LoopExit.CHAT_ERROR
    assert run.judge_error is None and judge.score.called and not run.passed


def test_a_turn_that_injected_nothing_passes_an_item_that_expects_nothing() -> None:
    client = _client([_composed("resp-1")])
    with _patched(client, _judge(True)):
        run = run_agentic_memory("https://h", "t", "ws", _item(injected=()), k=1).run_results[0]
    assert (run.passed, run.applied_memory, run.exit_reason) == (True, [], None)


def test_a_turn_that_injected_nothing_fails_an_item_that_expects_an_item() -> None:
    client = _client([_composed("resp-1")])
    with _patched(client, _judge(True)):
        run = run_agentic_memory("https://h", "t", "ws", _item(), k=1).run_results[0]
    assert (run.memory_error, run.exit_reason) == ("not injected: ['help-line']", None)


def test_a_turn_without_any_detail_fails_as_unread_memory_and_names_the_flag() -> None:
    client = _client([_answer("resp-1")])
    with _patched(client, _judge(True)), pytest.raises(MemoryAssertionError) as exc:
        evaluate_agentic_memory("https://h", "t", "ws", _item(injected=()), k=1)
    assert "enableGenAiInteractionIntelligence" in str(exc.value)
    (failed,) = exc.value.failed_runs
    assert [c["name"] for c in failed["failed_checks"]] == ["memory_read"]
    assert failed["exit_reason"] == "chat_error"


def test_a_chart_answer_reaches_the_judge_as_a_line_with_its_title() -> None:
    client = _client([_apply_memory("resp-1", "help-line")])
    viz = {"id": "v1", "title": "Orders by month", "type": "column_chart", "query": {"fields": {}}}
    client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "Questions? Ask the BI team.",
            "createdVisualizations": {"objects": [viz], "reasoning": ""},
            "toolCallEvents": [],
            "responseId": "resp-1",
        }
    )
    judge = _judge(True)
    with _patched(client, judge):
        run = run_agentic_memory("https://h", "t", "ws", _item(), k=1).run_results[0]
    assert run.actual_output == (
        '[The answer shows a chart: "Orders by month" (column_chart)]\n\nQuestions? Ask the BI team.'
    )


def test_an_item_without_memory_input_fails_before_any_request() -> None:
    item = _item().model_copy(update={"memory_input": None})
    client = _client([])
    with _patched(client, _judge(True)), pytest.raises(ValueError, match="no memory_input"):
        run_agentic_memory("https://h", "t", "ws", item, k=1)
    client.create_conversation.assert_not_called()


def test_k_runs_use_one_conversation_each() -> None:
    client = _client([_apply_memory("resp-1", "help-line")])
    client.create_conversation.side_effect = ["conv-1", "conv-2", "conv-3"]
    with _patched(client, _judge(True)):
        summary = run_agentic_memory("https://h", "t", "ws", _item(), k=3)
    assert [r.conversation_id for r in summary.run_results] == ["conv-1", "conv-2", "conv-3"]
    assert summary.pass_at_k and summary.pass_power_k


# --- the gate ----------------------------------------------------------------------------


def test_a_failing_item_raises_with_the_memory_check_named() -> None:
    client = _client([_apply_memory("resp-1", "returns")])
    with _patched(client, _judge(True)), pytest.raises(MemoryAssertionError) as exc:
        evaluate_agentic_memory("https://h", "t", "ws", _item(), k=1)
    err = exc.value
    assert "not injected: ['help-line']" in str(err)
    assert [c["name"] for c in err.failed_runs[0]["failed_checks"]] == ["memory_injected"]
    assert err.detail["applied_memory"] == ["returns"]


def test_a_passing_item_returns_the_injected_memory_in_its_detail() -> None:
    client = _client([_apply_memory("resp-1", "help-line")])
    with _patched(client, _judge(True)):
        outcome = evaluate_agentic_memory("https://h", "t", "ws", _item(), k=1)
    assert outcome.detail["memory_passed"] is True
    assert outcome.detail["applied_memory"] == ["help-line"]


def test_the_item_user_context_reaches_the_chat_client() -> None:
    item = _item().model_copy(update={"user_context": {"view": {"type": "dashboard", "id": "d1"}}})
    client = _client([_apply_memory("resp-1", "help-line")])
    with (
        patch("gooddata_eval.core.agentic.memory.ChatClient", return_value=client) as chat_client,
        patch("gooddata_eval.core.agentic.memory.LLMJudge", return_value=_judge(True)),
    ):
        run_agentic_memory("https://h", "t", "ws", item, k=1)
    assert chat_client.call_args.kwargs["user_context"] == {"view": {"type": "dashboard", "id": "d1"}}


def test_a_stored_item_dict_is_accepted() -> None:
    stored = {
        "id": "om-1",
        "question": "How many orders did we have in 2024?",
        "expected_output": "Ends with the help line.",
        "memory_input": {"injected": ["help-line"]},
    }
    client = _client([_apply_memory("resp-1", "help-line")])
    with _patched(client, _judge(True)):
        outcome = evaluate_agentic_memory("https://h", "t", "ws", stored, dataset_name="org_memory", k=1)
    assert outcome.detail["applied_memory"] == ["help-line"]


def test_a_stored_item_without_memory_input_fails_before_any_request() -> None:
    client = _client([])
    with _patched(client, _judge(True)), pytest.raises(ValueError, match="no memory_input"):
        evaluate_agentic_memory("https://h", "t", "ws", {"id": "om-1", "question": "q"}, k=1)
    client.create_conversation.assert_not_called()


def test_an_item_without_expected_output_fails_before_any_request() -> None:
    client = _client([])
    item = {"id": "om-1", "question": "q", "memory_input": {"injected": ["help-line"]}}
    with _patched(client, _judge(True)), pytest.raises(ValueError, match="no expected_output"):
        evaluate_agentic_memory("https://h", "t", "ws", item, k=1)
    client.create_conversation.assert_not_called()


def test_a_run_with_unread_memory_is_scored_as_memory_read_not_as_a_wrong_injection() -> None:
    captured: dict[str, Any] = {}

    def _capture(_submit: object, _identity: object, **kwargs: Any) -> None:
        captured.update(kwargs)

    client = _client([_answer("resp-1")])
    with (
        _patched(client, _judge(True)),
        patch("gooddata_eval.core.agentic.memory.submit_trace_scoring", _capture),
        pytest.raises(MemoryAssertionError),
    ):
        evaluate_agentic_memory("https://h", "t", "ws", _item(), k=1, langfuse=MagicMock())
    ctx = _ScoreCtx()
    captured["write_scores"](ctx)
    scores = {name: value for _, name, value in ctx.scores}
    assert (scores["memory_pass"], scores["memory_read"], scores["memory_answer_pass"]) == (0.0, 0.0, 1.0)
    assert "memory_injected" not in scores
    assert ctx.strict_checks == [{"memory_read": False, "memory_answer_pass": True}]


def test_k_below_one_is_refused() -> None:
    with pytest.raises(ValueError, match="k must be at least 1"):
        run_agentic_memory("https://h", "t", "ws", _item(), k=0)


def test_a_structured_expected_visualization_still_wins_over_memory_input() -> None:
    raw = {
        "id": "x",
        "input": "q",
        "expectedOutput": {"visualization": {"type": "bar"}},
        "metadata": {"memory_input": {"injected": ["a"]}},
    }
    assert _item_from_raw(raw, dataset_name="d", test_kind="visualization").test_kind == "vis_agentic"
    raw["metadata"]["test_kind"] = "agentic_memory"
    assert _item_from_raw(raw, dataset_name="d", test_kind="visualization").test_kind == "agentic_memory"


def test_an_item_no_run_of_which_the_judge_could_grade_is_an_error_with_its_diagnostics() -> None:
    client = _client([_apply_memory("resp-1", "help-line")])
    judge = _judge(True)
    judge.score.side_effect = JudgeResponseError("not JSON")
    with _patched(client, judge), pytest.raises(JudgeResponseError, match="no readable verdict") as exc:
        evaluate_agentic_memory("https://h", "t", "ws", _item(), k=2)
    assert exc.value.runs_effective == 2
    assert exc.value.detail["applied_memory"] == ["help-line"]


class _ScoreCtx:
    def __init__(self) -> None:
        self.run_metadata: dict[str, Any] = {}
        self.scores: list[tuple[int, str, Any]] = []
        self.unscored: list[int] = []
        self.strict_checks: list[Any] = []

    def trace(self, _conversation_id: str) -> None:
        return None

    @contextlib.contextmanager
    def observe(self, _trace: object, run_idx: int, **_kwargs: Any) -> Iterator[int]:
        yield run_idx

    def score(self, trace_id: int, *, name: str, value: Any, data_type: str, comment: str | None = None) -> None:
        self.scores.append((trace_id, name, value))

    def quality(self, trace_id: int, **kwargs: Any) -> None:
        self.scores.append((trace_id, "quality_score", None))
        self.strict_checks.append(kwargs.get("strict_checks"))


def test_each_run_is_scored_with_the_memory_and_the_answer_checks() -> None:
    captured: dict[str, Any] = {}

    def _capture(_submit: object, _identity: object, **kwargs: Any) -> None:
        captured.update(kwargs)

    client = _client([_apply_memory("resp-1", "returns")])
    with (
        _patched(client, _judge(True)),
        patch("gooddata_eval.core.agentic.memory.submit_trace_scoring", _capture),
        pytest.raises(MemoryAssertionError),
    ):
        evaluate_agentic_memory("https://h", "t", "ws", _item(), k=1, langfuse=MagicMock())
    ctx = _ScoreCtx()
    captured["write_scores"](ctx)

    assert captured["dataset_item_id"] == "om-1"
    scores = {name: value for _, name, value in ctx.scores}
    assert (scores["memory_pass"], scores["memory_injected"], scores["memory_answer_pass"]) == (0.0, 0.0, 1.0)


def test_the_best_run_latency_is_the_run_wall_time_with_the_items_read() -> None:
    client = _client([_apply_memory("resp-1", "help-line")])
    # item start, agent stop, judge start, judge stop, run stop: the /items read takes 5s.
    with _patched(client, _judge(True)), patch("time.monotonic", side_effect=[0.0, 2.0, 7.0, 8.0, 8.0]):
        outcome = evaluate_agentic_memory("https://h", "t", "ws", _item(), k=1)
    assert outcome.best_run_latency_s == 8.0
    assert outcome.run_latencies_s == [8.0]


def test_a_failed_memory_check_stays_a_failure_when_the_judge_cannot_grade() -> None:
    client = _client([_apply_memory("resp-1", "returns")])
    judge = _judge(True)
    judge.score.side_effect = JudgeResponseError("not JSON")
    with _patched(client, judge), pytest.raises(MemoryAssertionError) as exc:
        evaluate_agentic_memory("https://h", "t", "ws", _item(), k=1)
    assert "not injected: ['help-line']" in str(exc.value)
    assert [c["name"] for c in exc.value.failed_runs[0]["failed_checks"]] == ["memory_injected"]
    assert getattr(exc.value, "harness_error", None) is None


def test_a_run_the_memory_check_failed_is_scored_without_a_judge_verdict() -> None:
    captured: dict[str, Any] = {}

    def _capture(_submit: object, _identity: object, **kwargs: Any) -> None:
        captured.update(kwargs)

    client = _client([_apply_memory("resp-1", "returns")])
    judge = _judge(True)
    judge.score.side_effect = JudgeResponseError("not JSON")
    with (
        _patched(client, judge),
        patch("gooddata_eval.core.agentic.memory.submit_trace_scoring", _capture),
        pytest.raises(MemoryAssertionError),
    ):
        evaluate_agentic_memory("https://h", "t", "ws", _item(), k=1, langfuse=MagicMock())
    ctx = _ScoreCtx()
    captured["write_scores"](ctx)
    scores = {name: value for _, name, value in ctx.scores}
    assert (scores["memory_pass"], scores["memory_injected"]) == (0.0, 0.0)
    assert "memory_answer_pass" not in scores


def _client_whose_second_turn_fails() -> MagicMock:
    client = _client([_apply_memory("resp-1", "help-line")])
    client.create_conversation.side_effect = ["conv-1", "conv-2"]
    client.send_message.side_effect = [client.send_message.return_value, TurnIncompleteError("no final answer")]
    return client


def test_a_failed_turn_fails_its_run_and_keeps_the_other_runs() -> None:
    client = _client_whose_second_turn_fails()
    with _patched(client, _judge(True)):
        outcome = evaluate_agentic_memory("https://h", "t", "ws", _item(), k=2, gate="any")
    assert (outcome.runs_passed, outcome.runs_effective) == (1, 2)
    (failed,) = outcome.failed_runs
    assert [c["name"] for c in failed["failed_checks"]] == ["chat_turn"]
    assert "no final answer" in failed["detail"]["chat_error"]
    assert [c.args[0] for c in client.delete_conversation.call_args_list] == ["conv-1", "conv-2"]


def test_a_failed_turn_fails_the_power_gate_with_both_runs_recorded() -> None:
    client = _client_whose_second_turn_fails()
    with _patched(client, _judge(True)), pytest.raises(MemoryAssertionError) as exc:
        evaluate_agentic_memory("https://h", "t", "ws", _item(), k=2, gate="power")
    assert (exc.value.runs_passed, exc.value.runs_effective) == (1, 2)
    assert getattr(exc.value, "harness_error", None) is None


def test_a_failed_turn_is_scored_as_a_failed_run_without_check_scores() -> None:
    captured: dict[str, Any] = {}

    def _capture(_submit: object, _identity: object, **kwargs: Any) -> None:
        captured.update(kwargs)

    client = _client_whose_second_turn_fails()
    with _patched(client, _judge(True)), patch("gooddata_eval.core.agentic.memory.submit_trace_scoring", _capture):
        evaluate_agentic_memory("https://h", "t", "ws", _item(), k=2, gate="any", langfuse=MagicMock())
    ctx = _ScoreCtx()
    captured["write_scores"](ctx)
    by_run = {i: {n: v for t, n, v in ctx.scores if t == i} for i in (0, 1)}
    assert by_run[0]["memory_injected"] == 1.0
    assert by_run[1]["memory_pass"] == 0.0
    assert not {"memory_injected", "memory_answer_pass", "quality_score"} & set(by_run[1])

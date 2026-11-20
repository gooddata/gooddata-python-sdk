# (C) 2026 GoodData Corporation
import json
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.agentic.knowledge import (
    KnowledgeAssertionError,
    KnowledgeRunResult,
    _failure_reason,
    evaluate_agentic_knowledge,
    run_agentic_knowledge,
)
from gooddata_eval.core.chat.sse_client import ChatError
from gooddata_eval.core.evaluators._llm_judge import JudgeResponseError
from gooddata_eval.core.evaluators.base import ItemEvaluation
from gooddata_eval.core.models import AgenticAssertionError, ChatResult, ToolCallEvent

_MODULE = "gooddata_eval.core.agentic.knowledge"
_Q = "Who must approve a 30 % discount?"
_FOLLOW_UP = "And who approves 45 %?"
_EXPECTED = {"expected_documents": ["Discount Policy"], "must_include": ["Names the regional sales manager."]}


def _turn(text: str, *, search: bool = True, title: str = "Discount Policy") -> ChatResult:
    rows = [{"document_id": "d1", "filename": "", "title": title, "content": "...", "source": "the parent workspace"}]
    tools = (
        [ToolCallEvent(function_name="search_knowledge", function_arguments="{}", result=json.dumps({"results": rows}))]
        if search
        else []
    )
    return ChatResult(text_response=text, tool_call_events=tools, response_id=f"resp-{text[:5]}")


def _client(*turn_results: Any) -> MagicMock:
    client = MagicMock()
    client.create_conversation.side_effect = [f"conv-{i}" for i in range(1, 10)]
    client.send_message.side_effect = list(turn_results)
    return client


def _run(client: MagicMock, *, judge: bool = True, **kwargs: Any) -> Any:
    with (
        patch(f"{_MODULE}.ChatClient", return_value=client),
        patch("openai.OpenAI"),
        patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test"}),
        patch("gooddata_eval.core.evaluators._llm_judge.LLMJudge.score", return_value=(judge, "ok")) as score,
    ):
        params: dict[str, Any] = {
            "host": "https://h",
            "token": "tok",
            "workspace_id": "ws1",
            "question": _Q,
            "expected_output": _EXPECTED,
            **kwargs,
        }
        return run_agentic_knowledge(**params), score


# ── runs ────────────────────────────────────────────────────────────────────


def test_turns_are_sent_in_order_on_one_conversation() -> None:
    client = _client(_turn("Regional sales manager."), _turn("Not allowed above 40 %."))
    summary, score = _run(client, turns=[_Q, _FOLLOW_UP])

    assert [c.args for c in client.send_message.call_args_list] == [("conv-1", _Q), ("conv-1", _FOLLOW_UP)]
    assert summary.pass_at_k is True
    assert summary.best.evaluation.detail["turn_count"] == 2
    # The judge reads the earlier answer and grades the last one.
    assert "Regional sales manager." in score.call_args.kwargs["input"]
    assert score.call_args.kwargs["actual_output"] == "Not allowed above 40 %."
    client.delete_conversation.assert_called_once_with("conv-1")


def test_each_k_run_gets_its_own_conversation() -> None:
    client = _client(_turn("A"), _turn("B"))
    summary, _ = _run(client, k=2)
    assert [r.conversation_id for r in summary.run_results] == ["conv-1", "conv-2"]
    assert [c.args[0] for c in client.delete_conversation.call_args_list] == ["conv-1", "conv-2"]
    client.close.assert_called_once()


def test_a_chat_error_in_run_two_keeps_run_one() -> None:
    client = _client(_turn("Regional sales manager."), ChatError("gen-ai fell over"))
    summary, _ = _run(client, k=2)

    assert len(summary.run_results) == 2
    assert summary.run_results[0].chat_error is None
    assert "gen-ai fell over" in (summary.run_results[1].chat_error or "")
    assert summary.pass_at_k is True
    assert summary.pass_power_k is False
    assert summary.best.conversation_id == "conv-1"
    client.delete_conversation.assert_any_call("conv-2")


def test_a_chat_error_on_a_later_turn_names_the_turn() -> None:
    client = _client(_turn("Regional sales manager."), ChatError("boom"))
    summary, score = _run(client, turns=[_Q, _FOLLOW_UP])
    run = summary.run_results[0]
    assert "turn 2/2" in (run.chat_error or "")
    assert run.passed is False
    score.assert_not_called()


def test_a_failed_conversation_creation_does_not_discard_completed_runs() -> None:
    client = _client(_turn("A"), _turn("B"))
    client.create_conversation.side_effect = ["conv-1", RuntimeError("no conversation"), "conv-3"]
    summary, _ = _run(client, k=3)
    assert [r.chat_error is None for r in summary.run_results] == [True, False, True]
    assert "conversation creation failed" in (summary.run_results[1].chat_error or "")
    assert summary.pass_at_k is True
    assert summary.pass_power_k is False


def test_an_initial_conversation_is_used_for_run_zero_and_kept() -> None:
    client = _client(_turn("A"))
    _run(client, initial_conversation_id="conv-given")
    assert client.send_message.call_args.args[0] == "conv-given"
    client.create_conversation.assert_not_called()
    client.delete_conversation.assert_not_called()


def test_an_invalid_item_raises_before_any_request() -> None:
    client = _client()
    with patch(f"{_MODULE}.ChatClient", return_value=client) as client_cls, pytest.raises(ValueError, match="unknown"):
        run_agentic_knowledge("https://h", "tok", "ws1", _Q, {"expected_docs": ["x"]})
    client_cls.assert_not_called()


def test_tool_events_of_every_turn_are_kept_for_the_latency_breakdown() -> None:
    client = _client(_turn("A"), _turn("B"))
    summary, _ = _run(client, turns=[_Q, _FOLLOW_UP])
    assert [e.function_name for e in summary.best.tool_call_events] == ["search_knowledge", "search_knowledge"]


# ── evaluate_* wrapper ──────────────────────────────────────────────────────


def _evaluate(client: MagicMock, *, judge: Any = True, **kwargs: Any) -> Any:
    """`judge`: the verdict for every criterion, or a list of verdicts / exceptions in call order."""
    verdicts = judge if isinstance(judge, list) else None
    with (
        patch(f"{_MODULE}.ChatClient", return_value=client),
        patch("openai.OpenAI"),
        patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test"}),
        patch(
            "gooddata_eval.core.evaluators._llm_judge.LLMJudge.score",
            return_value=(judge, "ok"),
            side_effect=verdicts,
        ),
    ):
        params: dict[str, Any] = {
            "host": "https://h",
            "token": "tok",
            "workspace_id": "ws1",
            "question": _Q,
            "expected_output": _EXPECTED,
            "langfuse": None,
            **kwargs,
        }
        with patch(f"{_MODULE}.open_item_trace", return_value=(params["langfuse"], MagicMock(), None)):
            return evaluate_agentic_knowledge(**params)


def test_a_passing_item_returns_the_detail_with_the_latency_breakdown() -> None:
    outcome = _evaluate(_client(_turn("Regional sales manager.")))
    assert outcome.detail["expected_documents_found"] is True
    assert outcome.detail["documents_retrieved"] == ["Discount Policy"]
    assert "latency_breakdown" in outcome.detail
    assert outcome.runs_passed == 1
    assert outcome.run_latencies_s


def test_a_retrieval_failure_is_named_in_the_error() -> None:
    client = _client(_turn("Regional sales manager.", title="Customer Glossary"))
    with pytest.raises(KnowledgeAssertionError) as exc_info:
        _evaluate(client)
    error = exc_info.value
    assert isinstance(error, AgenticAssertionError)
    assert "expected_documents_found=False" in str(error)
    assert "include_0" not in str(error)
    assert error.detail["include_0"] is True
    assert error.runs_passed == 0
    assert error.runs_effective == 1
    assert error.conversation_id == "conv-1"
    assert error.failed_runs


def test_a_reasoning_failure_is_named_in_the_error() -> None:
    with pytest.raises(KnowledgeAssertionError) as exc_info:
        _evaluate(_client(_turn("The CFO approves it.")), judge=False)
    message = str(exc_info.value)
    assert "include_0=False" in message
    assert "expected_documents_found" not in message


def test_power_gate_fails_on_one_chat_error() -> None:
    client = _client(_turn("A"), ChatError("boom"))
    with pytest.raises(KnowledgeAssertionError) as exc_info:
        _evaluate(client, k=2, gate="power")
    assert exc_info.value.runs_passed == 1
    assert exc_info.value.runs_effective == 2


_NO_VERDICT = JudgeResponseError("empty body twice")


def test_a_judge_without_verdict_is_an_error_not_a_fail() -> None:
    """Code checks held and the judge returned nothing readable: the harness failed, not the agent."""
    with pytest.raises(JudgeResponseError) as exc_info:
        _evaluate(_client(_turn("Regional sales manager.")), judge=[_NO_VERDICT])
    error = exc_info.value
    assert error.harness_error["reason"] == "judge_failed"
    assert error.runs_passed == 0
    assert error.detail["unscored_runs"] == 1
    assert error.failed_runs[0]["outcome"]["status"] == "error"


def test_a_failed_code_check_stays_a_fail_when_the_judge_has_no_verdict() -> None:
    client = _client(_turn("Regional sales manager.", title="Customer Glossary"))
    with pytest.raises(KnowledgeAssertionError, match="expected_documents_found=False"):
        _evaluate(client, judge=[_NO_VERDICT])


def test_a_judge_failure_on_one_run_leaves_the_graded_run_deciding() -> None:
    client = _client(_turn("A"), _turn("B"))
    outcome = _evaluate(client, k=2, judge=[(True, "ok"), _NO_VERDICT])
    assert outcome.runs_passed == 1
    assert outcome.detail["unscored_runs"] == 1
    with pytest.raises(KnowledgeAssertionError):
        _evaluate(_client(_turn("A"), _turn("B")), k=2, gate="power", judge=[(True, "ok"), _NO_VERDICT])


def _scores_written(summary_turns: list[Any], **kwargs: Any) -> MagicMock:
    """Run with a fake Langfuse and replay the deferred scoring against a mock context."""
    captured: dict[str, Any] = {}

    def _submit(_link: Any, _identity: Any, **kw: Any) -> None:
        captured.update(kw)

    with patch(f"{_MODULE}.submit_trace_scoring", side_effect=_submit):
        try:
            _evaluate(_client(*summary_turns), langfuse=MagicMock(), dataset_item_id="item-1", **kwargs)
        except (KnowledgeAssertionError, JudgeResponseError):
            pass
    ctx = MagicMock()
    ctx.run_metadata = {}
    ctx.trace.return_value = None
    captured["write_scores"](ctx)
    return ctx


def test_langfuse_scores_split_retrieval_from_reasoning() -> None:
    ctx = _scores_written([_turn("Regional sales manager.", title="Customer Glossary")])
    scores = {c.kwargs["name"]: c.kwargs["value"] for c in ctx.score.call_args_list}
    assert scores["knowledge_pass"] == 0.0
    assert scores["expected_documents_found"] == 0.0
    assert scores["knowledge_searched"] == 1.0
    assert scores["answered"] == 1.0
    assert "include_0" not in scores
    # Quality reads the same bools as rank_key: code checks and judge verdicts, no knowledge_pass.
    strict = ctx.quality.call_args.kwargs["strict_checks"]
    assert strict == {
        "knowledge_searched": True,
        "expected_documents_found": False,
        "answered": True,
        "include_0": True,
    }


def test_langfuse_marks_a_run_without_judge_verdict_as_an_error() -> None:
    ctx = _scores_written([_turn("Regional sales manager.")], judge=[_NO_VERDICT])
    names = [c.kwargs["name"] for c in ctx.score.call_args_list]
    assert names == ["eval_error"]
    assert ctx.score.call_args.kwargs["comment"] == "judge_failed"
    ctx.quality.assert_not_called()


def test_langfuse_skips_a_run_with_a_chat_error() -> None:
    ctx = _scores_written([_turn("A"), ChatError("boom")], k=2)
    assert ctx.observe.call_count == 1
    assert ctx.observe.call_args.args[1] == 0


@pytest.mark.parametrize(
    ("detail", "error", "reason"),
    [
        ({"turn_count": 1}, None, "criteria not satisfied"),
        ({"answered": False}, "chat failed: timeout", "answered=False; chat failed: timeout"),
    ],
)
def test_a_failed_run_names_its_failed_checks_and_error(detail: dict, error: str | None, reason: str) -> None:
    evaluation = ItemEvaluation(passed=False, rank_key=(0, 0.0), detail=detail, error=error)
    assert _failure_reason(KnowledgeRunResult(conversation_id="conv-1", evaluation=evaluation)) == reason

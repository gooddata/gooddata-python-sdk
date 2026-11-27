# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any, cast

import pytest
from gooddata_eval.core.agentic import describe_object as kind
from gooddata_eval.core.evaluators import describe_object as do
from gooddata_eval.core.evaluators._llm_judge import JudgeResponseError, LLMJudge
from gooddata_eval.core.models import ChatResult


class _Judge:
    model = "stub"

    def __init__(self, verdict: bool | None) -> None:
        self.verdict = verdict

    def score(self, input: str, expected_output: str, actual_output: str) -> tuple[bool, str]:
        if self.verdict is None:
            raise JudgeResponseError("unreadable")
        return self.verdict, "stub"


def test_a_describe_answer_must_rest_on_a_workspace_lookup() -> None:
    def grade(tools: list[str], expected: dict[str, Any]):
        return do.evaluate_answer(
            question="Explain the ARPU metric",
            answer="ARPU is Net Sales divided by Active Customers.",
            tool_names=tools,
            expected=expected,
            positive_judge=cast(LLMJudge, _Judge(True)),
            violation_judge=cast(LLMJudge, _Judge(False)),
        )

    assert grade(["set_skills", "search_objects"], {}).passed
    no_lookup = grade([], {})
    assert not no_lookup.passed
    assert no_lookup.detail["workspace_lookup"] is False
    # an item whose right answer is to ask back needs no lookup
    assert grade([], {"search": False}).passed


class _Client:
    """A chat client that answers every question with one lookup and one sentence."""

    def __init__(self, **_kwargs: Any) -> None:
        self.deleted: list[str] = []

    def create_conversation(self) -> str:
        return "conv"

    def send_message(self, conversation_id: str, question: str) -> ChatResult:
        return ChatResult.model_validate(
            {
                "textResponse": "ARPU is Net Sales divided by Active Customers.",
                "toolCallEvents": [{"functionName": "search_objects", "functionArguments": "{}", "result": "{}"}],
            }
        )

    def delete_conversation(self, conversation_id: str) -> None:
        self.deleted.append(conversation_id)

    def close(self) -> None:
        pass


@pytest.mark.parametrize(("verdict", "outcome"), [(True, "pass"), (False, "fail"), (None, "error")])
def test_the_item_passes_fails_or_errors_with_the_judge(
    monkeypatch: pytest.MonkeyPatch, verdict: bool | None, outcome: str
) -> None:
    monkeypatch.setattr(kind, "ChatClient", _Client)
    monkeypatch.setattr(kind, "make_judges", lambda model=None: (_Judge(verdict), _Judge(False)))
    expected = {"must_include": ["Names the formula."]}
    if outcome == "pass":
        result = kind.evaluate_agentic_describe_object("h", "t", "ws", "Explain ARPU", expected, k=2)
        assert result.runs_passed == 2
        assert result.best_run_latency_s is not None
        return
    error_cls = kind.DescribeObjectAssertionError if outcome == "fail" else JudgeResponseError
    with pytest.raises(error_cls) as info:
        kind.evaluate_agentic_describe_object("h", "t", "ws", "Explain ARPU", expected, k=2)
    assert info.value.runs_passed == 0
    if outcome == "error":  # no run got a verdict: a harness error, not two failures
        assert info.value.harness_error is not None

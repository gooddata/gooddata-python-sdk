# (C) 2026 GoodData Corporation
import json
import os
from unittest.mock import MagicMock, patch

from gooddata_eval.core.evaluators._llm_judge import LLMJudge


def _make_judge() -> LLMJudge:
    with (
        patch("openai.OpenAI"),
        patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test"}),
    ):
        return LLMJudge(evaluation_steps=["Step 1: check the answer is correct."])


def _mock_response(score: int, reasoning: str = "ok"):
    resp = MagicMock()
    resp.choices[0].message.content = json.dumps({"score": score, "reasoning": reasoning})
    return resp


def test_llm_judge_returns_true_on_score_1():
    judge = _make_judge()
    judge._client.chat.completions.create = MagicMock(return_value=_mock_response(1))
    passed, reasoning = judge.score("q", "expected answer", "actual answer")
    assert passed is True
    assert reasoning == "ok"


def test_llm_judge_returns_false_on_score_0():
    judge = _make_judge()
    judge._client.chat.completions.create = MagicMock(return_value=_mock_response(0, "wrong"))
    passed, _ = judge.score("q", "expected answer", "wrong answer")
    assert passed is False


def test_llm_judge_raises_without_api_key():
    with patch("openai.OpenAI"), patch.dict("os.environ", {}, clear=True):
        os.environ.pop("OPENAI_API_KEY", None)
        try:
            LLMJudge(evaluation_steps=["s"])
            assert False, "should have raised OSError"
        except OSError as e:
            assert "OPENAI_API_KEY" in str(e)

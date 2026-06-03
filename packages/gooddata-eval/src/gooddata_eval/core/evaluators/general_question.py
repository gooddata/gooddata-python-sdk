# (C) 2026 GoodData Corporation
"""Evaluator for general_question: LLM-as-judge scores the agent's text response."""

from gooddata_eval.core.evaluators._llm_judge import LLMJudge
from gooddata_eval.core.evaluators._text_utils import extract_text
from gooddata_eval.core.evaluators.base import ItemEvaluation
from gooddata_eval.core.models import ChatResult, DatasetItem

_EVALUATION_STEPS = [
    "Read the INPUT (the user's question) and the EXPECTED OUTPUT (a description of what a correct answer must contain).",
    "Read the ACTUAL OUTPUT (the agent's response).",
    "Score 1 if the actual output contains all the must-have facts described in the expected output.",
    "Score 0 if the actual output is missing important facts, is incorrect, or does not answer the question.",
]


class GeneralQuestionEvaluator:
    test_kind = "general_question"

    def __init__(self):
        self._judge = LLMJudge(evaluation_steps=_EVALUATION_STEPS)

    def evaluate(self, item: DatasetItem, chat_result: ChatResult) -> ItemEvaluation:
        actual = extract_text(chat_result)
        passed, reasoning = self._judge.score(
            input=item.question,
            expected_output=str(item.expected_output),
            actual_output=actual,
        )
        return ItemEvaluation(
            passed=passed,
            rank_key=(int(passed),),
            detail={"judge_reasoning": reasoning, "actual_output": actual},
        )

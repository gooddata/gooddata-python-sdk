# (C) 2026 GoodData Corporation
"""Evaluator for general_question: LLM-as-judge scores the agent's text response."""

from gooddata_eval.core.evaluators._llm_judge import LLMJudge, score_run
from gooddata_eval.core.evaluators._text_utils import extract_text
from gooddata_eval.core.evaluators.base import ItemEvaluation
from gooddata_eval.core.models import ChatResult, DatasetItem, build_latency_breakdown

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
        # score_run, not judge.score: a judge fault is this run's, not the item's (see score_run).
        verdict = score_run(
            self._judge,
            input=item.question,
            expected_output=str(item.expected_output),
            actual_output=actual,
        )
        detail = {
            "actual_output": actual,
            "latency_breakdown": build_latency_breakdown(
                chat_result.tool_call_events, chat_result.reasoning_step_events
            ),
        }
        if verdict.error is None:
            detail["judge_reasoning"] = verdict.reasoning
        else:
            detail["judge_error"] = verdict.error
        return ItemEvaluation(passed=verdict.passed, rank_key=(verdict.rank,), detail=detail, error=verdict.error)

# (C) 2026 GoodData Corporation
"""Evaluator for dashboard_summary: rubric-based LLM-as-judge scoring.

Summaries are free text, so we do not match strings. Instead, `expected_output`
is a rubric of checkable criteria:

    {
      "must_include":     ["...facts a good summary must contain..."],
      "must_not_include": ["...things a good summary must avoid (hallucinations)..."],
      "rubric":           ["...soft quality dimensions..."]
    }

Each criterion is scored independently by the judge (True/False), so the
runner's `quality_score` becomes the fraction of satisfied criteria. The item
*passes* only when every `must_include` is satisfied and no `must_not_include`
is violated; `rubric` items contribute to quality but do not gate pass/fail.

As a fallback, a non-dict `expected_output` is treated as a single rubric
criterion (same behaviour as `general_question`).
"""

from typing import Any

from gooddata_eval.core.evaluators._llm_judge import LLMJudge
from gooddata_eval.core.evaluators._text_utils import extract_text
from gooddata_eval.core.evaluators.base import ItemEvaluation
from gooddata_eval.core.models import ChatResult, DatasetItem

_POSITIVE_STEPS = [
    "Read the INPUT (the user's request) and the EXPECTED OUTPUT (one criterion the summary must satisfy).",
    "Read the ACTUAL OUTPUT (the generated summary).",
    "Score 1 if the actual output clearly satisfies the criterion (allow paraphrasing and reasonable numeric tolerance).",
    "Score 0 if the criterion is missing, contradicted, or only partially addressed.",
]

# For must_not_include we ask the judge a plain presence question and invert the
# result in code. Scoring "does the summary AVOID X?" via a field labelled
# EXPECTED OUTPUT is unreliable: the model reads the forbidden behaviour as
# desired and flips the verdict. Detecting presence (no negation, no
# contradictory label) is far more robust.
_VIOLATION_STEPS = [
    "Read the CHARACTERISTIC described in EXPECTED OUTPUT.",
    "Read the ACTUAL OUTPUT (the generated summary).",
    "Score 1 if the actual output clearly exhibits the described characteristic.",
    "Score 0 if it does not exhibit it.",
]


class DashboardSummaryEvaluator:
    test_kind = "dashboard_summary"

    def __init__(self):
        self._positive_judge = LLMJudge(evaluation_steps=_POSITIVE_STEPS)
        self._violation_judge = LLMJudge(evaluation_steps=_VIOLATION_STEPS)

    @staticmethod
    def _criteria(expected_output: Any) -> tuple[list[str], list[str], list[str]]:
        if isinstance(expected_output, dict):
            must_include = [str(c) for c in expected_output.get("must_include", [])]
            must_not_include = [str(c) for c in expected_output.get("must_not_include", [])]
            rubric = [str(c) for c in expected_output.get("rubric", [])]
            if must_include or must_not_include or rubric:
                return must_include, must_not_include, rubric
        # Fallback: treat the whole expected_output as a single gating criterion
        # (same pass/fail semantics as general_question).
        return [str(expected_output)], [], []

    def evaluate(self, item: DatasetItem, chat_result: ChatResult) -> ItemEvaluation:
        actual = extract_text(chat_result)
        must_include, must_not_include, rubric = self._criteria(item.expected_output)

        detail: dict[str, Any] = {"actual_output": actual}
        passed = True

        for i, criterion in enumerate(must_include):
            ok, reason = self._positive_judge.score(item.question, criterion, actual)
            detail[f"include_{i}"] = ok
            detail[f"include_{i}_reason"] = reason
            passed = passed and ok

        for i, criterion in enumerate(must_not_include):
            violated, reason = self._violation_judge.score(item.question, criterion, actual)
            ok = not violated  # True == characteristic absent == correctly avoided
            detail[f"exclude_{i}"] = ok
            detail[f"exclude_{i}_reason"] = reason
            passed = passed and ok

        for i, criterion in enumerate(rubric):
            ok, reason = self._positive_judge.score(item.question, criterion, actual)
            detail[f"rubric_{i}"] = ok
            detail[f"rubric_{i}_reason"] = reason

        bool_checks = [v for v in detail.values() if isinstance(v, bool)]
        quality = sum(1 for v in bool_checks if v) / len(bool_checks) if bool_checks else 0.0

        return ItemEvaluation(passed=passed, rank_key=(int(passed), quality), detail=detail)

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

A criterion the judge returns nothing readable for is *ungraded*: it is neither
satisfied nor violated, so it is stored without a bool and stays out of the
quality denominator. An ungraded gating criterion cannot carry a pass, though --
"the judge could not tell" is not evidence the fact is present. When no gating
criterion was graded at all the run has no verdict and is reported as such.

As a fallback, a non-dict `expected_output` is treated as a single rubric
criterion (same behaviour as `general_question`).
"""

from typing import Any

from gooddata_eval.core.evaluators._llm_judge import LLMJudge, score_run
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

        # One judge request PER CRITERION, so an unreadable response has to be confined to
        # its own criterion: letting it raise would discard every criterion already graded
        # and abandon the ones after it, losing a 7-criterion item to one bad body. An
        # ungraded criterion is recorded but stored without a bool, which keeps it out of
        # the failing list and the quality denominator below: counting it as failed would
        # invent a score the judge never gave.
        ungraded = 0

        def _grade(judge: LLMJudge, criterion: str, key: str, *, invert: bool = False) -> bool | None:
            nonlocal ungraded
            verdict = score_run(judge, input=item.question, expected_output=criterion, actual_output=actual)
            if verdict.error is not None:
                ungraded += 1
                detail[f"{key}_reason"] = f"UNGRADED: {verdict.error}"
                return None
            # invert: the violation judge answers "is the characteristic present?", so the
            # criterion is satisfied exactly when it says no.
            ok = not verdict.passed if invert else verdict.passed
            detail[key] = ok
            detail[f"{key}_reason"] = verdict.reasoning
            return ok

        # `is True`, not `is not False`: a gating criterion the judge could not grade is not
        # a failure, but it cannot carry a pass either.
        for i, criterion in enumerate(must_include):
            ok = _grade(self._positive_judge, criterion, f"include_{i}")
            passed = passed and ok is True

        for i, criterion in enumerate(must_not_include):
            ok = _grade(self._violation_judge, criterion, f"exclude_{i}", invert=True)
            passed = passed and ok is True

        for i, criterion in enumerate(rubric):
            # Rubric criteria inform quality but never gate `passed`.
            _grade(self._positive_judge, criterion, f"rubric_{i}")

        if ungraded:
            detail["ungraded_criteria"] = ungraded
        bool_checks = [v for v in detail.values() if isinstance(v, bool)]
        quality = sum(1 for v in bool_checks if v) / len(bool_checks) if bool_checks else 0.0

        # Keyed on the criteria that decide the verdict, not on any graded bool: rubric
        # criteria never gate `passed`, so one graded rubric line must not certify a pass
        # whose every mandatory fact went unassessed. A rubric-only item has no gating
        # criteria, so there any graded line is a verdict.
        gating = len(must_include) + len(must_not_include)
        graded_gating = [v for k, v in detail.items() if isinstance(v, bool) and not k.startswith("rubric_")]
        if ungraded and not (graded_gating if gating else bool_checks):
            return ItemEvaluation(
                passed=False,
                rank_key=(-1, quality),
                detail=detail,
                error=(
                    f"judge returned no readable verdict for any of the {gating or ungraded} criterion(s) "
                    "that decide this item."
                ),
            )

        return ItemEvaluation(passed=passed, rank_key=(int(passed), quality), detail=detail)

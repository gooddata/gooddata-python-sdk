# (C) 2026 GoodData Corporation
"""Per-criterion LLM-judge grading shared by the rubric-scored single-shot evaluators."""

from collections.abc import Sequence
from typing import Any

from gooddata_eval.core.evaluators._llm_judge import LLMJudge, score_run
from gooddata_eval.core.evaluators.base import ItemEvaluation

# A criterion keyed by the name its verdict is stored under in `detail`.
Criterion = tuple[str, str]


def grade_rubric(
    positive_judge: LLMJudge,
    violation_judge: LLMJudge,
    *,
    question: str,
    actual: str,
    must_include: Sequence[Criterion],
    must_not_include: Sequence[Criterion],
    rubric: Sequence[Criterion],
    detail: dict[str, Any],
    passed: bool = True,
) -> ItemEvaluation:
    """Grade every criterion with one judge request each and decide the item.

    `must_include` and `must_not_include` gate the verdict, `rubric` only informs quality.
    `must_not_include` criteria are put to `violation_judge` as a presence question and
    inverted here. `detail` may already hold verdicts the caller decided without a judge,
    with `passed` carrying their outcome; every bool in it counts towards quality.

    A criterion the judge returns nothing readable for is *ungraded*: recorded without a
    bool, so it neither fails the item nor enters the quality denominator, but it cannot
    carry a pass either. When nothing that decides the item was graded, the run has no
    verdict and comes back with `error` set.
    """
    # One judge request PER CRITERION, so an unreadable response has to be confined to
    # its own criterion: letting it raise would discard every criterion already graded
    # and abandon the ones after it, losing a 7-criterion item to one bad body.
    decided_without_judge = passed
    ungraded = 0
    graded_gating = 0
    graded_rubric = 0

    def _grade(judge: LLMJudge, criterion: str, key: str, *, invert: bool = False) -> bool | None:
        nonlocal ungraded
        verdict = score_run(judge, input=question, expected_output=criterion, actual_output=actual)
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
    for judge, criteria, invert in ((positive_judge, must_include, False), (violation_judge, must_not_include, True)):
        for key, criterion in criteria:
            ok = _grade(judge, criterion, key, invert=invert)
            graded_gating += ok is not None
            passed = passed and ok is True

    for key, criterion in rubric:
        graded_rubric += _grade(positive_judge, criterion, key) is not None

    if ungraded:
        detail["ungraded_criteria"] = ungraded
    bool_checks = [v for v in detail.values() if isinstance(v, bool)]
    quality = sum(1 for v in bool_checks if v) / len(bool_checks) if bool_checks else 0.0

    # Keyed on the criteria that decide the verdict, not on any graded bool: rubric
    # criteria never gate `passed`, so one graded rubric line must not certify a pass
    # whose every mandatory fact went unassessed. A rubric-only item has no gating
    # criteria, so there any graded line is a verdict. A caller-decided failure already
    # is a verdict.
    gating = len(must_include) + len(must_not_include)
    judge_verdict = graded_gating if gating else graded_rubric
    if ungraded and decided_without_judge and not judge_verdict:
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

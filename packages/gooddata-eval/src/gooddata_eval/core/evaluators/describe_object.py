# (C) 2026 GoodData Corporation
"""Checks and judge steps for `agentic_describe_object`: "describe / explain <object>" in the chat.

`expected_output`:

    {
      "search":           true,
      "must_include":     ["...criteria the answer must satisfy..."],
      "must_not_include": ["...characteristics the answer must not show..."],
      "rubric":           ["...soft quality dimensions..."]
    }

`search` (default true) gates the verdict without a judge: the answer must rest on a
workspace lookup (`search_objects` or `get_object_with_children`), never on general
knowledge. An item where the right answer is to ask back ("Describe this" with nothing on
screen) sets it to false. Judge criteria are graded one by one; the INPUT the judge reads
is the item's question.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from gooddata_eval.core.evaluators._llm_judge import LLMJudge
from gooddata_eval.core.evaluators._rubric import Criterion, grade_rubric
from gooddata_eval.core.evaluators.base import ItemEvaluation

LOOKUP_TOOLS = frozenset({"search_objects", "get_object_with_children"})

_POSITIVE_STEPS = [
    "Read the INPUT: the user's request to describe or explain an analytics object of their workspace.",
    "Read the EXPECTED OUTPUT: one criterion the answer must satisfy.",
    "Read the ACTUAL OUTPUT: the assistant's answer.",
    "Score 1 if the actual output clearly satisfies the criterion.",
    "Score 0 if the criterion is missing, contradicted, or only partially addressed.",
]

_VIOLATION_STEPS = [
    "Read the CHARACTERISTIC described in EXPECTED OUTPUT, including any exceptions it states.",
    "Read the ACTUAL OUTPUT: the assistant's answer.",
    "Decide only whether the actual output exhibits the characteristic, not whether it is correct or wanted.",
    "Score 1 if the actual output clearly exhibits the described characteristic.",
    "Score 0 if it does not exhibit it.",
]


def _criteria(expected: dict[str, Any], key: str) -> list[Criterion]:
    raw = expected.get(key) or []
    items = raw if isinstance(raw, list) else [raw]
    return [(f"{key}_{i}", str(c)) for i, c in enumerate(items) if str(c).strip()]


def evaluate_answer(
    *,
    question: str,
    answer: str,
    tool_names: Sequence[str],
    expected: dict[str, Any],
    positive_judge: LLMJudge,
    violation_judge: LLMJudge,
) -> ItemEvaluation:
    """Grade one answer: a workspace lookup ran (unless the item expects the agent to ask back), then the criteria."""
    detail: dict[str, Any] = {"actual_output": answer}
    if not answer.strip():
        return ItemEvaluation(passed=False, rank_key=(-1, 0.0), detail=detail, error="empty answer")
    passed = True
    if expected.get("search", True):
        looked_up = sorted(LOOKUP_TOOLS.intersection(tool_names))
        detail["workspace_lookup"] = bool(looked_up)
        if not looked_up:
            detail["lookup_problem"] = f"answered without a workspace lookup (tools: {list(tool_names)})"
            passed = False
    return grade_rubric(
        positive_judge,
        violation_judge,
        question=question,
        actual=answer,
        must_include=_criteria(expected, "must_include"),
        must_not_include=_criteria(expected, "must_not_include"),
        rubric=_criteria(expected, "rubric"),
        detail=detail,
        passed=passed,
    )


def make_judges(model: str | None = None) -> tuple[LLMJudge, LLMJudge]:
    """The positive and the violation judge, with the describe-specific steps."""
    return LLMJudge(_POSITIVE_STEPS, model=model), LLMJudge(_VIOLATION_STEPS, model=model)

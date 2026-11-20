# (C) 2026 GoodData Corporation
"""Checks and judge steps for `agentic_summary`: the chat summary of a widget or a dashboard.

Each turn's `expected_output` (the item's for the summary, a follow-up's own for that turn):

    {
      "format":           {...} | false,
      "no_tool_calls":    false,
      "must_include":     ["...criteria the answer must satisfy..."],
      "must_not_include": ["...characteristics the answer must not show..."],
      "rubric":           ["...soft quality dimensions..."]
    }

Every key is optional. The code checks gate the verdict and need no judge:

- shape (summary turn only, unless `format` is false): a chart widget gets the four
  headings of the visualization summary in order, a KPI widget none and at most three
  sentences, a dashboard the three headings of the dashboard summary in order, and a
  dashboard whose widgets all returned no data one paragraph without headings; an empty
  widget has no fixed shape. A `format`
  object replaces the default: `max_sentences`, `no_headings`, `no_bullets`, `headings`.
- no ids: no `{visualization/...}` reference tag and no raw object id in the answer.
- no figures on no data: when every widget in scope returned no data, the answer quotes no
  amount, share or count.
- `no_tool_calls`: the turn answers from the conversation, without running a tool.

Judge criteria are graded one by one, as for `dashboard_summary`; the INPUT the judge reads
is the item's scenario line plus the question of the turn. Criteria give a direction, never
a value.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from gooddata_eval.core.evaluators._llm_judge import LLMJudge
from gooddata_eval.core.evaluators._rubric import Criterion, grade_rubric
from gooddata_eval.core.evaluators.base import ItemEvaluation

CHART_HEADINGS = ("Summary", "Key Findings", "Trends", "Areas to Watch")
DASHBOARD_HEADINGS = ("Summary", "Key Insights", "Areas to Watch")
KPI_MAX_SENTENCES = 3

# Tools gen-ai runs to manage the conversation, not to answer it.
_BOOKKEEPING_TOOLS = frozenset({"set_skills"})

_POSITIVE_STEPS = [
    "Read the INPUT: the dashboard or widget the user summarizes, its filters, and the question of this turn.",
    "Read the EXPECTED OUTPUT: one criterion the answer must satisfy.",
    "Read the ACTUAL OUTPUT: the assistant's answer to that question.",
    "Score 1 if the actual output clearly satisfies the criterion.",
    "Score 0 if the criterion is missing, contradicted, or only partially addressed.",
]

# A presence question, inverted in code, as in summary.py: the INPUT names filters and data,
# which pulls the judge towards grading correctness; the third step keeps it on presence.
_VIOLATION_STEPS = [
    "Read the CHARACTERISTIC described in EXPECTED OUTPUT, including any exceptions it states.",
    "Read the ACTUAL OUTPUT: the assistant's answer.",
    "Decide only whether the actual output exhibits the characteristic, not whether it is correct or wanted.",
    "Score 1 if the actual output clearly exhibits the described characteristic.",
    "Score 0 if it does not exhibit it.",
]

_HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
_BULLET = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s", re.MULTILINE)
_REFERENCE_TAG = re.compile(r"\{(?:visualization|dashboard|metric|attribute|label|fact|widget)/[^}]*\}")
_RAW_ID = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b|\b[0-9a-f]{32}\b")
# An amount, a share or a count: $1.2 M, 45%, 1,205, 3.5 K. Years, days and hours are dates.
_FIGURE = re.compile(
    r"[$€£]\s?\d[\d,.]*(?:\s?[KMB]\b)?"
    r"|\d[\d,.]*\s?%"
    r"|\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b"
    r"|\b\d+(?:\.\d+)?\s?[KMB]\b"
    r"|\b\d+\.\d+\b",
)
_SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z*])")


@dataclass(frozen=True)
class SummaryScope:
    """What the summarized widgets returned, as the checks need it."""

    scope: str  # "widget" or "dashboard"
    kpi_only: bool  # the referenced widgets are single-value KPIs
    all_empty: bool  # every widget in scope returned no data


def headings(text: str) -> list[str]:
    return [h.strip(" *_") for h in _HEADING.findall(text)]


def count_sentences(text: str) -> int:
    plain = _HEADING.sub(" ", text).strip()
    return len([s for s in _SENTENCE_END.split(plain) if s.strip()]) if plain else 0


def shape_problem(text: str, scope: SummaryScope, fmt: dict[str, Any] | None) -> str | None:
    """Why the answer's shape is wrong, or None.

    `fmt` replaces the default shape (an item where the user asked for another format).
    """
    found = headings(text)
    if fmt:
        if fmt.get("no_headings") and found:
            return f"headings {found} although the user asked for none"
        if fmt.get("no_bullets") and _BULLET.search(text):
            return "bullet points although the user asked for none"
        limit = fmt.get("max_sentences")
        if isinstance(limit, int) and count_sentences(text) > limit:
            return f"{count_sentences(text)} sentences, more than the {limit} the user asked for"
        wanted = fmt.get("headings")
        if isinstance(wanted, list) and found != wanted:
            return f"headings {found}, expected {wanted}"
        return None
    if scope.scope == "dashboard":
        if scope.all_empty:
            return f"headings {found} on a dashboard without data" if found else None
        return None if found == list(DASHBOARD_HEADINGS) else f"headings {found}, expected {list(DASHBOARD_HEADINGS)}"
    if scope.all_empty:
        # An empty widget comes back with all four headings or with a single one: the prompt
        # sets no shape for it, so only the no-figures check applies.
        return None
    if scope.kpi_only:
        if found:
            return f"headings {found} on a KPI"
        n = count_sentences(text)
        return f"{n} sentences on a KPI, more than {KPI_MAX_SENTENCES}" if n > KPI_MAX_SENTENCES else None
    return None if found == list(CHART_HEADINGS) else f"headings {found}, expected {list(CHART_HEADINGS)}"


def id_problem(text: str) -> str | None:
    tag = _REFERENCE_TAG.search(text)
    if tag:
        return f"reference tag {tag.group(0)!r} in the answer"
    raw = _RAW_ID.search(text)
    return f"raw id {raw.group(0)!r} in the answer" if raw else None


def figures(text: str) -> list[str]:
    return [m.group(0) for m in _FIGURE.finditer(text)]


def answer_tools(tool_names: Sequence[str]) -> list[str]:
    return [t for t in tool_names if t and t not in _BOOKKEEPING_TOOLS]


def _criteria(expected: dict[str, Any], key: str, prefix: str) -> list[Criterion]:
    raw = expected.get(key) or []
    items = raw if isinstance(raw, list) else [raw]
    return [(f"{prefix}{i}", str(c)) for i, c in enumerate(items) if str(c).strip()]


def evaluate_turn(
    *,
    judge_input: str,
    answer: str,
    tool_names: Sequence[str],
    expected: dict[str, Any],
    scope: SummaryScope | None,
    positive_judge: LLMJudge,
    violation_judge: LLMJudge,
) -> ItemEvaluation:
    """Grade one turn. `scope` is None for a follow-up: only the summary turn has a default shape."""
    detail: dict[str, Any] = {"actual_output": answer}
    passed = True
    if not answer.strip():
        detail["error"] = "empty answer"
        return ItemEvaluation(passed=False, rank_key=(-1, 0.0), detail=detail, error="empty answer")

    fmt = expected.get("format")
    if scope is not None and fmt is not False:
        problem = shape_problem(answer, scope, fmt if isinstance(fmt, dict) else None)
        detail["shape_ok"] = problem is None
        if problem:
            detail["shape_problem"] = problem
            passed = False

    problem = id_problem(answer)
    detail["no_ids"] = problem is None
    if problem:
        detail["id_problem"] = problem
        passed = False

    if scope is not None and scope.all_empty:
        quoted = figures(answer)
        detail["no_figures_on_no_data"] = not quoted
        if quoted:
            detail["figures_on_no_data"] = quoted[:5]
            passed = False

    if expected.get("no_tool_calls"):
        ran = answer_tools(tool_names)
        detail["no_tool_calls"] = not ran
        if ran:
            detail["tools_run"] = ran
            passed = False

    return grade_rubric(
        positive_judge,
        violation_judge,
        question=judge_input,
        actual=answer,
        must_include=_criteria(expected, "must_include", "must_include_"),
        must_not_include=_criteria(expected, "must_not_include", "must_not_include_"),
        rubric=_criteria(expected, "rubric", "rubric_"),
        detail=detail,
        passed=passed,
    )


def make_judges(model: str | None = None) -> tuple[LLMJudge, LLMJudge]:
    return LLMJudge(_POSITIVE_STEPS, model=model), LLMJudge(_VIOLATION_STEPS, model=model)

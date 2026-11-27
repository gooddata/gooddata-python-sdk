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
  dashboard whose widgets all returned no data no headings; an empty
  widget has no fixed shape. A `format`
  object replaces the default: `max_sentences`, `no_headings`, `no_bullets`, `headings`.
- no ids (summary turn only): no `{visualization/...}` reference tag and no raw object id. A
  follow-up is answered as an ordinary chat message, whose reference tags the UI renders as links.
- no figures on no data: when every widget in scope returned no data, the answer quotes no
  amount, share or count.
- `no_tool_calls`: the turn answers from the conversation, without running a tool.
- `figures_grounded` (when the kind passes the tables the agent read): every figure in the
  answer comes from those tables or a simple calculation on them (`chat_summary_figures`). A
  summary turn that states figures and read no table fails, whatever tools it ran.

Judge criteria are graded one by one, as for `dashboard_summary`; the INPUT the judge reads
is the item's scenario line plus the question of the turn. Criteria give a direction, never
a value.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Any

from gooddata_eval.core.evaluators._llm_judge import LLMJudge
from gooddata_eval.core.evaluators._rubric import Criterion, grade_rubric
from gooddata_eval.core.evaluators._text_utils import count_sentences as count_text_sentences
from gooddata_eval.core.evaluators.base import ItemEvaluation
from gooddata_eval.core.evaluators.chat_summary_figures import Table, check_figures, extract_figures

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


@dataclass(frozen=True)
class SummaryScope:
    """What the summarized widgets returned, as the checks need it."""

    scope: str  # "widget" or "dashboard"
    kpi_only: bool  # the referenced widgets are single-value KPIs
    all_empty: bool  # every widget in scope returned no data


def headings(text: str) -> list[str]:
    """The markdown headings of an answer, in order, without their markers."""
    return [h.strip(" *_") for h in _HEADING.findall(text)]


# A period after a title or a short name ends no sentence: "Mrs. Crystal Murray", "Inc. revenue".
_ABBREVIATIONS = frozenset({"mr", "mrs", "ms", "dr", "prof", "inc", "ltd", "co", "st", "vs", "etc", "e.g", "i.e"})


def count_sentences(text: str) -> int:
    """Sentences of an answer; a heading line is no sentence."""
    return count_text_sentences(_HEADING.sub(" ", text), _ABBREVIATIONS)


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
    """Why the answer shows an id or a reference tag the user cannot read, or None."""
    tag = _REFERENCE_TAG.search(text)
    if tag:
        return f"reference tag {tag.group(0)!r} in the answer"
    raw = _RAW_ID.search(text)
    return f"raw id {raw.group(0)!r} in the answer" if raw else None


def figures(text: str) -> list[str]:
    """The amounts, shares and counts an answer states, read as `figures_grounded` reads them; a year is a date."""
    return [f.raw for f in extract_figures(text) if f.kind != "year"]


def answer_tools(tool_names: Sequence[str]) -> list[str]:
    return [t for t in tool_names if t and t not in _BOOKKEEPING_TOOLS]


def _criteria(expected: dict[str, Any], key: str, prefix: str) -> list[Criterion]:
    raw = expected.get(key) or []
    items = raw if isinstance(raw, list) else [raw]
    return [(f"{prefix}{i}", str(c)) for i, c in enumerate(items) if str(c).strip()]


# Detail keys a code check sets; False = that check failed the turn.
EXPECTED_KEYS = frozenset({"format", "no_tool_calls", "must_include", "must_not_include", "rubric"})
FORMAT_KEYS = frozenset({"max_sentences", "no_headings", "no_bullets", "headings"})


def validate_expected(expected: Any, where: str) -> None:
    """Reject a key the checks do not know, so a misspelt one cannot read as a pass.

    A `format` object replaces the default shape; with an unknown key in it no shape would be checked.

    Raises:
        ValueError: `expected` is not an object, or it or its `format` has an unknown key.
    """
    if expected is None:
        return
    if not isinstance(expected, dict):
        raise ValueError(f"{where}: expected_output must be an object, got {type(expected).__name__}")
    unknown = sorted(set(expected) - EXPECTED_KEYS)
    if unknown:
        raise ValueError(f"{where}: unknown expected_output keys {unknown}; known: {sorted(EXPECTED_KEYS)}")
    fmt = expected.get("format")
    if fmt is None or fmt is False:
        return
    if not isinstance(fmt, dict) or not fmt:
        raise ValueError(f"{where}: `format` must be false or a non-empty object, got {fmt!r}")
    unknown = sorted(set(fmt) - FORMAT_KEYS)
    if unknown:
        raise ValueError(f"{where}: unknown `format` keys {unknown}; known: {sorted(FORMAT_KEYS)}")


CODE_CHECKS = ("shape_ok", "no_ids", "no_figures_on_no_data", "figures_grounded", "no_tool_calls")


def evaluate_turn(
    *,
    judge_input: str,
    answer: str,
    tool_names: Sequence[str],
    expected: dict[str, Any],
    scope: SummaryScope | None,
    positive_judge: LLMJudge,
    violation_judge: LLMJudge,
    tables: Sequence[Table] | None = None,
    filter_years: Iterable[int] = (),
    known_text: Iterable[str] = (),
) -> ItemEvaluation:
    """Grade one turn. `scope` is None for a follow-up: only the summary turn has a shape and the no-ids rule."""
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

    if scope is not None:
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

    if tables is not None:
        grounding = check_figures(answer, tables, filter_years=filter_years, known_text=known_text)
        # figures on a summary turn that read no data at all: nothing they could come from. A turn that
        # only searched the workspace has run a tool and read no table.
        unread = scope is not None and not scope.all_empty and not tables and bool(figures(answer))
        detail["figures_grounded"] = grounding.passed and not unread
        detail["figures_grounded_reason"] = (
            f"states {len(figures(answer))} figures but read no data" if unread else grounding.reason()
        )
        if not detail["figures_grounded"]:
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
    """The positive and the violation judge, with the summary-specific steps."""
    return LLMJudge(_POSITIVE_STEPS, model=model), LLMJudge(_VIOLATION_STEPS, model=model)

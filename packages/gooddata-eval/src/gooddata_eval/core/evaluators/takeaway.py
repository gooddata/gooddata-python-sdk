# (C) 2026 GoodData Corporation
"""Evaluator for document_takeaway: deterministic format checks plus an LLM-judge rubric.

A takeaway is one finding for a page, readable in about five seconds: a bold headline,
at most two short sentences, one paragraph, ≤ 50 words whatever ``maxCharacters`` allows.
`expected_output` is:

    {
      "no_data":          false,
      "format":           {...overrides of _DEFAULT_FORMAT...},
      "default_rules":    true,
      "must_include":     ["...criteria the takeaway must satisfy..."],
      "must_not_include": ["...characteristics the takeaway must not show..."],
      "rubric":           ["...soft quality dimensions..."]
    }

Every key is optional. The format checks need no judge and gate the verdict. A ``format``
value of ``false`` or ``null`` switches its check off, for an item whose instruction asks
for another shape (a list, no headline). Unless ``default_rules`` is false, the
DEFAULT_MUST_INCLUDE / DEFAULT_MUST_NOT_INCLUDE judge criteria are added to the item's
own, under ``default_`` keys. Judge criteria grade like ``dashboard_summary``.

``no_data`` decides the item alone: the endpoint's ``noData`` must equal it, and a
``noData`` answer carries no takeaway, so nothing else is graded. An expected takeaway
that came back as ``noData`` is a failure, not an empty text to judge.
"""

import re
from typing import Any

from gooddata_eval.core.evaluators._llm_judge import LLMJudge
from gooddata_eval.core.evaluators._rubric import Criterion, grade_rubric
from gooddata_eval.core.evaluators.base import ItemEvaluation
from gooddata_eval.core.models import ChatResult, DatasetItem

# The judge criteria below are calibrated against tests/fixtures/takeaway_calibration.json
# with `make calibrate-takeaway`; re-run it after changing any of their wording.
DEFAULT_MUST_INCLUDE: dict[str, str] = {
    "one_finding": "A reader gets one clear main finding from the first line alone.",
}

DEFAULT_MUST_NOT_INCLUDE: dict[str, str] = {
    "executive_summary": (
        "Reads as an executive summary or report: it contains section labels such as 'Summary', "
        "'Key takeaways' or 'Things to watch', or lists several separate findings one after another, "
        "or gives recommendations, an outlook or a closing conclusion."
    ),
    "chart_walkthrough": "Walks through the charts one by one instead of stating one finding that connects them.",
    "background_opener": "Opens with background or a description of the page instead of the finding itself.",
    "exact_figure": (
        "States a figure in digits: an amount, count, percentage or share, including rounded or hedged ones "
        "such as 'about $270M', 'roughly 1.2K', 'in the low $100Ks' or '~40%'. A rough size or direction in words, such as "
        "'roughly doubled', 'about a third' or 'most orders', does not count. Numbers that are part of a "
        "visualization or metric title, such as 'Top 10', do not count."
    ),
    "date_or_period": (
        "Names a specific date, month, quarter, year or named period. Relative references such as "
        "'this period' do not count."
    ),
    "unshown_cause": (
        "Makes an explicit causal claim (such as 'because', 'due to' or 'driven by') that attributes a change "
        "to a factor that is not in the data, such as a campaign, a season or a market event. Comparisons "
        "between segments, and naming the segment in the data that led a change (such as 'led by the "
        "Nordics'), are not causal claims."
    ),
    "chart_description": "Describes what a chart displays instead of what the data means.",
}

_DEFAULT_FORMAT: dict[str, Any] = {
    "bold_headline": True,
    "max_headline_words": 10,
    "max_sentences": 2,
    "max_words": 50,
    "single_paragraph": True,
    "no_lists": True,
    "no_headings": True,
}

_POSITIVE_STEPS = [
    "Read the INPUT (a label for the page the takeaway was written for) and the EXPECTED OUTPUT "
    "(one criterion the takeaway must satisfy).",
    "Read the ACTUAL OUTPUT (the generated takeaway).",
    "Score 1 if the actual output clearly satisfies the criterion.",
    "Score 0 if the criterion is missing, contradicted, or only partially addressed.",
]

# A presence question, inverted in code -- see the same split in summary.py.
_VIOLATION_STEPS = [
    "Read the CHARACTERISTIC described in EXPECTED OUTPUT, including any exceptions it states.",
    "Read the ACTUAL OUTPUT (the generated takeaway).",
    "Score 1 if the actual output clearly exhibits the described characteristic.",
    "Score 0 if it does not exhibit it.",
]

_HEADLINE = re.compile(r"^\s*\*\*(.+?)\*\*", re.DOTALL)
# A terminator, any closing quotes or brackets, then whitespace before the next sentence.
_SENTENCE_BREAK = re.compile(r"[.!?]+[\"'”’»)\]]*\s+(?=\S)")
_SENTENCE_OPENERS = "\"'“‘„«(["
_ABBREVIATIONS = frozenset({"vs", "e.g", "i.e", "u.s", "cca", "např", "tj", "tzn", "apod", "resp", "atd"})
_BLANK_LINE = re.compile(r"\n\s*\n")
_HEADING_LINE = re.compile(r"^\s*#{1,6}\s", re.MULTILINE)
_LIST_LINE = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s", re.MULTILINE)
_IDS = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}|\{\w+/[^}]*\}|\blabel\.\w",
    re.IGNORECASE,
)
_META_OPENER = re.compile(
    r"^(?:summary|key takeaways?|based on the data|visualization metadata|this chart shows)\b",
    re.IGNORECASE,
)


def _words(text: str) -> int:
    return sum(1 for token in text.replace("**", " ").split() if any(ch.isalnum() for ch in token))


def _limit_on(value: Any) -> bool:
    return value is not None and value is not False


def _sentences(text: str) -> int:
    """Sentences in `text`; a break needs the next sentence to open with a capital, digit or quote.

    That keeps "vs. last", "U.S. sales" or "např. v" from splitting one sentence in two; a
    terminator right after a known abbreviation ("vs. Europe", "e.g. Nordics") is no break.
    """
    plain = text.replace("**", "").strip()
    if not plain:
        return 0
    breaks = 0
    for match in _SENTENCE_BREAK.finditer(plain):
        nxt = plain[match.end()]
        token = (plain[: match.start()].rsplit(maxsplit=1) or [""])[-1].lstrip("\"'“‘„«([").lower()
        if token in _ABBREVIATIONS:
            continue
        breaks += nxt.isupper() or nxt.isdigit() or nxt in _SENTENCE_OPENERS
    return breaks + 1


def _has_meta_opener(text: str, headline: str | None, body: str) -> bool:
    openers = [line.strip().lstrip("#*").strip() for line in text.splitlines()]
    openers += [headline or "", body.strip()]
    return any(_META_OPENER.match(opener) for opener in openers)


class DocumentTakeawayEvaluator:
    test_kind = "document_takeaway"

    def __init__(self):
        self._positive_judge = LLMJudge(evaluation_steps=_POSITIVE_STEPS)
        self._violation_judge = LLMJudge(evaluation_steps=_VIOLATION_STEPS)

    @staticmethod
    def validate(item: DatasetItem) -> None:
        """Reject an item whose `expected_output` this evaluator cannot read, before any request.

        Raises:
            ValueError: `format` is not an object, carries a key the checks do not know, or a criteria key
                is not a JSON array.
        """
        expected = item.expected_output if isinstance(item.expected_output, dict) else {}
        overrides = expected.get("format") or {}
        if not isinstance(overrides, dict):
            raise ValueError(f"document_takeaway item '{item.id}': format must be a JSON object")
        unknown = sorted(set(overrides) - set(_DEFAULT_FORMAT))
        if unknown:
            raise ValueError(
                f"document_takeaway item '{item.id}': unknown format key(s) {unknown}; known: {sorted(_DEFAULT_FORMAT)}"
            )
        for key in ("must_include", "must_not_include", "rubric"):
            if not isinstance(expected.get(key, []), list):
                raise ValueError(f"document_takeaway item '{item.id}': {key} must be a JSON array")

    def evaluate(self, item: DatasetItem, chat_result: ChatResult) -> ItemEvaluation:
        self.validate(item)
        expected: dict[str, Any] = item.expected_output if isinstance(item.expected_output, dict) else {}
        raw = chat_result.raw_response or {}
        returned_no_data = raw.get("noData") is True
        text = chat_result.text_response or ""

        expected_no_data = expected.get("no_data") is True
        if expected_no_data or returned_no_data:
            ok = expected_no_data and returned_no_data and raw.get("takeaway") is None
            detail: dict[str, Any] = {"actual_output": text, "no_data": ok}
            return ItemEvaluation(passed=ok, rank_key=(int(ok), float(ok)), detail=detail)

        detail = {"actual_output": text}
        detail.update(self._format_checks(item, expected, text))
        passed = all(v for v in detail.values() if isinstance(v, bool))

        must_include: list[Criterion] = []
        must_not_include: list[Criterion] = []
        if expected.get("default_rules", True) is not False:
            must_include += [(f"default_include_{k}", c) for k, c in DEFAULT_MUST_INCLUDE.items()]
            must_not_include += [(f"default_exclude_{k}", c) for k, c in DEFAULT_MUST_NOT_INCLUDE.items()]
        must_include += [(f"include_{i}", str(c)) for i, c in enumerate(expected.get("must_include", []))]
        must_not_include += [(f"exclude_{i}", str(c)) for i, c in enumerate(expected.get("must_not_include", []))]
        rubric = [(f"rubric_{i}", str(c)) for i, c in enumerate(expected.get("rubric", []))]

        return grade_rubric(
            self._positive_judge,
            self._violation_judge,
            question=item.question,
            actual=text,
            must_include=must_include,
            must_not_include=must_not_include,
            rubric=rubric,
            detail=detail,
            passed=passed,
        )

    @staticmethod
    def _format_checks(item: DatasetItem, expected: dict[str, Any], text: str) -> dict[str, Any]:
        """Deterministic checks keyed by name, plus `word_count` and `headline_word_count`."""
        fmt = {**_DEFAULT_FORMAT, **(expected.get("format") or {})}
        checks: dict[str, Any] = {}

        match = _HEADLINE.match(text) if fmt["bold_headline"] else None
        headline = match.group(1).strip() if match else None
        body = text[match.end() :] if match else text
        word_count = _words(text)
        headline_word_count = _words(headline) if headline else 0
        checks["word_count"] = word_count
        checks["headline_word_count"] = headline_word_count

        if _limit_on(fmt["max_words"]):
            checks["word_budget"] = word_count <= fmt["max_words"]
        if fmt["bold_headline"]:
            checks["bold_headline"] = headline is not None
            if _limit_on(fmt["max_headline_words"]):
                checks["headline_words"] = headline_word_count <= fmt["max_headline_words"]
        if _limit_on(fmt["max_sentences"]):
            checks["max_sentences"] = _sentences(body) <= fmt["max_sentences"]
        if fmt["single_paragraph"]:
            checks["single_paragraph"] = not _BLANK_LINE.search(text.strip()) and text.strip().count("\n") <= 1
        max_characters = item.takeaway_input.max_characters if item.takeaway_input else None
        if max_characters is not None:
            checks["length"] = len(text) <= max_characters
        if fmt["no_headings"]:
            checks["no_headings"] = not _HEADING_LINE.search(text)
        if fmt["no_lists"]:
            checks["no_lists"] = not _LIST_LINE.search(text)
        checks["no_ids"] = not _IDS.search(text)
        checks["no_meta"] = not _has_meta_opener(text, headline, body)
        return checks

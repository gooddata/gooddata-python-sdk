# (C) 2026 GoodData Corporation
"""Evaluator for catalog_metadata: format checks plus an LLM-judge rubric on a generated title or description.

The Analytics Catalog generates a title (a short label) or a description (one to three
plain sentences) for one object from its metadata. The default limits (title 10 words,
description 4 sentences) sit one step above what the product prompt asks for (2-8 words,
1-3 sentences): they catch a broken shape, not a slightly long answer. `expected_output` is:

    {
      "expect_note":      false,
      "format":           {...overrides of the output's default format...},
      "must_include":     ["...criteria the text must satisfy..."],
      "must_not_include": ["...characteristics the text must not show..."],
      "rubric":           ["...soft quality dimensions..."]
    }

Every key is optional. The format checks need no judge and gate the verdict; a ``format``
value of ``false`` or ``null`` switches its check off. ``expect_note`` decides the item
alone: the endpoint must return no text and a non-empty note (it declined, e.g. the
object does not exist). Judge criteria grade like ``dashboard_summary``; the item's
question is what the judge reads as INPUT, so it states the object's real metadata in
plain words.
"""

import re
from typing import Any

from gooddata_eval.core.evaluators._llm_judge import LLMJudge
from gooddata_eval.core.evaluators._rubric import Criterion, grade_rubric
from gooddata_eval.core.evaluators.base import ItemEvaluation
from gooddata_eval.core.evaluators.takeaway import _sentences, _words
from gooddata_eval.core.models import ChatResult, DatasetItem

_DEFAULT_FORMAT: dict[str, dict[str, Any]] = {
    "title": {"max_words": 10, "max_sentences": 1, "no_end_period": True, "no_markup": True, "no_ids": True},
    "description": {"max_words": 80, "max_sentences": 4, "no_end_period": False, "no_markup": True, "no_ids": True},
}

_POSITIVE_STEPS = [
    "Read the INPUT (the analytics object the text was generated for, with its real metadata) and the "
    "EXPECTED OUTPUT (one criterion the text must satisfy).",
    "Read the ACTUAL OUTPUT (the generated title or description).",
    "Score 1 if the actual output clearly satisfies the criterion.",
    "Score 0 if the criterion is missing, contradicted, or only partially addressed.",
]

# A presence question, inverted in code -- see the same split in summary.py. The INPUT
# carries the object's real metadata, which pulls the judge towards grading correctness;
# the third step keeps it on presence.
_VIOLATION_STEPS = [
    "Read the CHARACTERISTIC described in EXPECTED OUTPUT, including any exceptions it states.",
    "Read the ACTUAL OUTPUT (the generated title or description).",
    "Decide only whether the actual output exhibits the characteristic, not whether it is correct or wanted.",
    "Score 1 if the actual output clearly exhibits the described characteristic.",
    "Score 0 if it does not exhibit it.",
]

# Bold, single emphasis (*x*, _x_), code, a heading or a list item.
_MARKUP = re.compile(
    r"\*\*|`|(?<![\w*])[*_](?=\S)[^*_\n]+(?<=\S)[*_](?![\w*])|^\s*#{1,6}\s|^\s*(?:[-*•]|\d+[.)])\s",
    re.MULTILINE,
)
_LIMITS = ("max_words", "max_sentences")
# A UUID, a MAQL reference such as {metric/net_sales}, or a snake_case identifier.
_IDS = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}|\{\w+/[^}]*\}|\b[a-z0-9]+(?:_[a-z0-9]+)+\b",
    re.IGNORECASE,
)


def _limit_on(value: Any) -> bool:
    return value is not None and value is not False


class CatalogMetadataEvaluator:
    test_kind = "catalog_metadata"

    def __init__(self):
        self._positive_judge = LLMJudge(evaluation_steps=_POSITIVE_STEPS)
        self._violation_judge = LLMJudge(evaluation_steps=_VIOLATION_STEPS)

    @staticmethod
    def validate(item: DatasetItem) -> None:
        """Reject an item this evaluator cannot read, before any request.

        Raises:
            ValueError: No `catalog_input`, `format` is not an object or has an unknown key,
                or a criteria key is not a JSON array.
        """
        if item.catalog_input is None:
            raise ValueError(f"catalog_metadata item '{item.id}' is missing required 'catalog_input'")
        expected = item.expected_output if isinstance(item.expected_output, dict) else {}
        overrides = expected.get("format") or {}
        if not isinstance(overrides, dict):
            raise ValueError(f"catalog_metadata item '{item.id}': format must be a JSON object")
        known = _DEFAULT_FORMAT[item.catalog_input.output]
        unknown = sorted(set(overrides) - set(known))
        if unknown:
            raise ValueError(
                f"catalog_metadata item '{item.id}': unknown format key(s) {unknown}; known: {sorted(known)}"
            )
        for key, value in overrides.items():
            is_limit = isinstance(value, int) and not isinstance(value, bool) and value > 0
            if not (value is None or value is False or (is_limit if key in _LIMITS else value is True)):
                kind = "a positive integer" if key in _LIMITS else "true"
                raise ValueError(f"catalog_metadata item '{item.id}': format.{key} must be {kind}, false or null")
        for key in ("must_include", "must_not_include", "rubric"):
            if not isinstance(expected.get(key, []), list):
                raise ValueError(f"catalog_metadata item '{item.id}': {key} must be a JSON array")

    def evaluate(self, item: DatasetItem, chat_result: ChatResult) -> ItemEvaluation:
        self.validate(item)
        assert item.catalog_input is not None  # validate() guarantees it
        output = item.catalog_input.output
        expected: dict[str, Any] = item.expected_output if isinstance(item.expected_output, dict) else {}
        raw = chat_result.raw_response or {}
        text = (chat_result.text_response or "").strip()
        note = raw.get("note") or ""
        detail: dict[str, Any] = {
            "actual_output": text,
            "note": note,
            "unusable_retries": raw.get("unusable_retries", 0),
        }

        if expected.get("expect_note") is True:
            ok = not text and bool(note.strip())
            detail["declined_with_note"] = ok
            return ItemEvaluation(passed=ok, rank_key=(int(ok), float(ok)), detail=detail)

        detail["generated"] = bool(text)
        detail["no_note"] = not note.strip()
        if text:
            detail.update(self._format_checks(output, expected, text))
        passed = all(v for v in detail.values() if isinstance(v, bool))
        if not text:
            return ItemEvaluation(passed=False, rank_key=(0, 0.0), detail=detail)

        must_include: list[Criterion] = [
            (f"include_{i}", str(c)) for i, c in enumerate(expected.get("must_include", []))
        ]
        must_not_include: list[Criterion] = [
            (f"exclude_{i}", str(c)) for i, c in enumerate(expected.get("must_not_include", []))
        ]
        rubric: list[Criterion] = [(f"rubric_{i}", str(c)) for i, c in enumerate(expected.get("rubric", []))]
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
    def _format_checks(output: str, expected: dict[str, Any], text: str) -> dict[str, Any]:
        """Deterministic checks keyed by name, plus `word_count`."""
        fmt = {**_DEFAULT_FORMAT[output], **(expected.get("format") or {})}
        checks: dict[str, Any] = {"word_count": _words(text)}
        if _limit_on(fmt["max_words"]):
            checks["max_words"] = checks["word_count"] <= fmt["max_words"]
        if _limit_on(fmt["max_sentences"]):
            checks["max_sentences"] = _sentences(text) <= fmt["max_sentences"]
        if fmt["no_end_period"]:
            checks["no_end_period"] = not text.endswith(".")
        if fmt["no_markup"]:
            checks["no_markup"] = not _MARKUP.search(text)
        if fmt["no_ids"]:
            checks["no_ids"] = not _IDS.search(text)
        return checks

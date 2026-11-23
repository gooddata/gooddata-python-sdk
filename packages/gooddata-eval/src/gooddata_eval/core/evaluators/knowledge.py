# (C) 2026 GoodData Corporation
"""Evaluator for agentic_knowledge: retrieval checks plus an LLM-judge rubric on the last answer.

The AI chat answers from knowledge documents through the `search_knowledge` and
`get_knowledge_chunks` tools. An item sends `setup_turns`, then its question, in one
conversation and grades the answer to the question. `expected_output` is:

    {
      "setup_turns":         ["...earlier user turns, sent in order before the question..."],
      "expect_search":       true,
      "expected_documents":  ["...document titles some knowledge tool must return..."],
      "forbidden_documents": ["...document titles no knowledge tool may return..."],
      "expected_source":     "the parent workspace",
      "must_include":        ["...criteria the last answer must satisfy..."],
      "must_not_include":    ["...characteristics the last answer must not show..."],
      "rubric":              ["...soft quality dimensions..."]
    }

Every key is optional. Retrieval checks gate the verdict before the judge, so a failed item
shows whether the document was never found (retrieval) or found and misused (reasoning).
"""

import re
from collections.abc import Sequence
from typing import Any

from gooddata_eval.core.chat.render import render_answer_text
from gooddata_eval.core.evaluators._llm_judge import LLMJudge
from gooddata_eval.core.evaluators._rubric import Criterion, grade_rubric
from gooddata_eval.core.evaluators.base import ItemEvaluation
from gooddata_eval.core.models import ChatResult, DatasetItem, ToolCallEvent

SEARCH_TOOL = "search_knowledge"
CHUNKS_TOOL = "get_knowledge_chunks"

_POSITIVE_STEPS = [
    "Read the INPUT (the conversation so far, ending with the user's last question) and the "
    "EXPECTED OUTPUT (one criterion the assistant's last answer must satisfy).",
    "Read the ACTUAL OUTPUT (the assistant's last answer).",
    "Score 1 if the actual output clearly satisfies the criterion.",
    "Score 0 if the criterion is missing, contradicted, or only partially addressed.",
]

# Presence question, inverted in code.
_VIOLATION_STEPS = [
    "Read the CHARACTERISTIC described in EXPECTED OUTPUT, including any exceptions it states.",
    "Read the ACTUAL OUTPUT (the assistant's last answer).",
    "Decide only whether the actual output exhibits the characteristic, not whether it is correct or wanted.",
    "Score 1 if the actual output clearly exhibits the described characteristic.",
    "Score 0 if it does not exhibit it.",
]

_BOOL_KEYS = ("expect_search",)
_LIST_KEYS = ("setup_turns", "expected_documents", "forbidden_documents", "must_include", "must_not_include", "rubric")
_STR_KEYS = ("expected_source",)
_KNOWN_KEYS = frozenset(_BOOL_KEYS + _LIST_KEYS + _STR_KEYS)
# The `source` labels gen-ai puts on knowledge tool results.
SOURCE_LABELS = ("this workspace", "the parent workspace", "an ancestor workspace", "AI Hub")

# Earlier user turns and answers shown to the judge are cut to this many characters each.
_EARLIER_TURN_CHARS = 1500

# "**Sources**", "### Sources" or "Sources:" on a line of its own.
_SOURCES_HEADING = re.compile(r"^\s*(?:\*\*Sources:?\*\*|#{1,6}\s*Sources:?|Sources:)\s*$", re.IGNORECASE)
_BULLET = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s+(.+?)\s*$")
_EMPHASIS = re.compile(r"^(\*\*|\*|_)(.+?)\1")


def _norm(text: Any) -> str:
    return str(text or "").strip().casefold()


def item_turns(item: DatasetItem) -> list[str]:
    """All user turns of a validated item: `setup_turns`, then the question (the graded turn)."""
    expected = item.expected_output if isinstance(item.expected_output, dict) else {}
    return [*expected.get("setup_turns", []), item.question]


def knowledge_results(events: Sequence[ToolCallEvent]) -> list[dict[str, Any]]:
    """One row per document any knowledge tool returned, in call order.

    - `search_knowledge`: `{"results": [{"title", "filename", "source", ...}]}`, one row each
    - `get_knowledge_chunks`: `{"title", "filename", "source", "chunks": [...]}`, one row;
      a document it did not find (no title, no filename) adds none
    """
    rows: list[dict[str, Any]] = []
    for event in events:
        parsed = event.parsed_result() if event.result else None
        if not isinstance(parsed, dict):
            continue
        if event.function_name == SEARCH_TOOL and isinstance(parsed.get("results"), list):
            rows.extend(row for row in parsed["results"] if isinstance(row, dict))
        elif event.function_name == CHUNKS_TOOL and _row_names(parsed):
            rows.append({key: parsed.get(key) for key in ("title", "filename", "source")})
    return rows


def _row_names(row: dict[str, Any]) -> set[str]:
    """Normalized title and filename of a result row; either can match a document."""
    return {name for name in (_norm(row.get("title")), _norm(row.get("filename"))) if name}


def _row_label(row: dict[str, Any]) -> str:
    return str(row.get("title") or "").strip() or str(row.get("filename") or "").strip()


def parse_sources_cited(answer: str) -> list[str]:
    """Titles in the last "Sources" section of an answer; [] when there is none.

    - heading line: `**Sources**`, `### Sources` or `Sources:`
    - each following bullet: `- *Title* (filename), pp. 1-2 — from *source*`, or `- Title (...)`
    - stops at the first non-blank line that is not a bullet
    """
    lines = answer.splitlines()
    start = next((i for i in range(len(lines) - 1, -1, -1) if _SOURCES_HEADING.match(lines[i])), None)
    if start is None:
        return []
    titles: list[str] = []
    for line in lines[start + 1 :]:
        if not line.strip():
            continue
        bullet = _BULLET.match(line)
        if bullet is None:
            break
        text = bullet.group(1)
        emphasis = _EMPHASIS.match(text)
        title = emphasis.group(2) if emphasis else text.split(" (", 1)[0]
        if title.strip():
            titles.append(title.strip())
    return titles


def _clip(text: str) -> str:
    return text if len(text) <= _EARLIER_TURN_CHARS else text[:_EARLIER_TURN_CHARS] + "… (truncated)"


def judge_input(turns: Sequence[str], answers: Sequence[str]) -> str:
    """What the judge reads as INPUT: the question, or the conversation up to the last question."""
    if len(turns) == 1:
        return turns[0]
    parts: list[str] = []
    for turn, answer in zip(turns[:-1], answers, strict=False):
        parts.append(f"User: {_clip(turn)}\nAssistant: {_clip(answer)}")
    parts.append(f"User (last question): {turns[-1]}")
    return "\n\n".join(parts)


class AgenticKnowledgeEvaluator:
    test_kind = "agentic_knowledge"

    def __init__(self):
        self._positive_judge = LLMJudge(evaluation_steps=_POSITIVE_STEPS)
        self._violation_judge = LLMJudge(evaluation_steps=_VIOLATION_STEPS)

    @staticmethod
    def validate(item: DatasetItem) -> None:
        """Reject an item this evaluator cannot read, before any request.

        Raises:
            ValueError: Blank question, `expected_output` not an object, an unknown key,
                or a value of the wrong type.
        """
        prefix = f"agentic_knowledge item '{item.id}'"
        if not item.question.strip():
            raise ValueError(f"{prefix}: question must be a non-empty string")
        expected = item.expected_output if item.expected_output is not None else {}
        if not isinstance(expected, dict):
            raise ValueError(f"{prefix}: expected_output must be a JSON object")
        # `test_kind` routes the item (langfuse_source) and is not an expectation.
        unknown = sorted(set(expected) - _KNOWN_KEYS - {"test_kind"})
        if unknown:
            raise ValueError(f"{prefix}: unknown expected_output key(s) {unknown}; known: {sorted(_KNOWN_KEYS)}")
        for key in _BOOL_KEYS:
            if key in expected and not isinstance(expected[key], bool):
                raise ValueError(f"{prefix}: {key} must be true or false")
        for key in _LIST_KEYS:
            value = expected.get(key, [])
            if not isinstance(value, list) or not all(isinstance(v, str) and v.strip() for v in value):
                raise ValueError(f"{prefix}: {key} must be a JSON array of non-empty strings")
        for key in _STR_KEYS:
            if key in expected and not (isinstance(expected[key], str) and expected[key].strip()):
                raise ValueError(f"{prefix}: {key} must be a non-empty string")
        source = expected.get("expected_source")
        if isinstance(source, str) and _norm(source) not in {_norm(label) for label in SOURCE_LABELS}:
            raise ValueError(f"{prefix}: expected_source must be one of {list(SOURCE_LABELS)}")
        if "expected_source" in expected and not expected.get("expected_documents"):
            raise ValueError(f"{prefix}: expected_source needs expected_documents to say which document")

    def evaluate(self, item: DatasetItem, turn_results: Sequence[ChatResult]) -> ItemEvaluation:
        """Grade one run: every turn's result, in order; the last one is the graded answer."""
        self.validate(item)
        expected: dict[str, Any] = item.expected_output if isinstance(item.expected_output, dict) else {}
        turns = item_turns(item)
        answers = [render_answer_text(result) for result in turn_results]
        last = answers[-1] if answers else ""
        detail: dict[str, Any] = {"actual_output": last, **self.retrieval_checks(expected, turn_results)}
        detail["answered"] = bool(last)
        detail["sources_cited"] = parse_sources_cited(last)
        detail["turn_count"] = len(turn_results)

        passed = all(v for v in detail.values() if isinstance(v, bool))
        if not last:
            return ItemEvaluation(passed=False, rank_key=(0, 0.0), detail=detail)

        def _criteria(key: str, prefix: str) -> list[Criterion]:
            return [(f"{prefix}_{i}", str(c)) for i, c in enumerate(expected.get(key, []))]

        return grade_rubric(
            self._positive_judge,
            self._violation_judge,
            question=judge_input(turns, answers),
            actual=last,
            must_include=_criteria("must_include", "include"),
            must_not_include=_criteria("must_not_include", "exclude"),
            rubric=_criteria("rubric", "rubric"),
            detail=detail,
            passed=passed,
        )

    @staticmethod
    def retrieval_checks(expected: dict[str, Any], turn_results: Sequence[ChatResult]) -> dict[str, Any]:
        """Code checks over every turn's knowledge tool calls.

        - bools gate the verdict; each is present only when its key is set
        - `documents_retrieved` is a list, so it never gates or counts towards quality
        """
        events = [event for result in turn_results for event in result.tool_call_events or []]
        rows = knowledge_results(events)
        found = set().union(*(_row_names(row) for row in rows)) if rows else set()
        checks: dict[str, Any] = {}
        if expected.get("expect_search", True):
            checks["knowledge_searched"] = any(e.function_name == SEARCH_TOOL for e in events)
        wanted = expected.get("expected_documents") or []
        if wanted:
            checks["expected_documents_found"] = all(_norm(title) in found for title in wanted)
        forbidden = expected.get("forbidden_documents") or []
        if forbidden:
            checks["forbidden_documents_absent"] = not any(_norm(title) in found for title in forbidden)
        source = expected.get("expected_source")
        if source:
            wanted_names = {_norm(title) for title in wanted}
            checks["expected_source_found"] = any(
                _row_names(row) & wanted_names and _norm(row.get("source")) == _norm(source) for row in rows
            )
        checks["documents_retrieved"] = sorted({label for row in rows if (label := _row_label(row))})
        return checks

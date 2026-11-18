# (C) 2026 GoodData Corporation
"""Shared text helpers for text-answer evaluators: answer extraction, word and sentence counts."""

import re
from collections.abc import Collection

from gooddata_eval.core.chat.render import render_answer_text
from gooddata_eval.core.models import ChatResult


def extract_text(chat_result: ChatResult) -> str:
    """Extract the agent's answer: prose plus any content-bearing non-text part."""
    return render_answer_text(chat_result)


# A terminator, any closing quotes or brackets, then whitespace before the next sentence.
_SENTENCE_BREAK = re.compile(r"[.!?]+[\"'”’»)\]]*\s+(?=\S)")
_SENTENCE_OPENERS = "\"'“‘„«(["


def count_words(text: str) -> int:
    """Words in `text`: whitespace-separated tokens holding a letter or digit, bold markers ignored."""
    return sum(1 for token in text.replace("**", " ").split() if any(ch.isalnum() for ch in token))


def count_sentences(text: str, abbreviations: Collection[str]) -> int:
    """Sentences in `text`; a break needs the next sentence to open with a capital, digit or quote.

    That keeps "vs. last" or "např. v" from splitting one sentence in two. A terminator right
    after a token in `abbreviations` (lowercase, without its final dot: "vs", "e.g") is no
    break either. Each evaluator passes its own list, so tuning one cannot move another's verdicts.
    """
    plain = text.replace("**", "").strip()
    if not plain:
        return 0
    breaks = 0
    for match in _SENTENCE_BREAK.finditer(plain):
        nxt = plain[match.end()]
        token = (plain[: match.start()].rsplit(maxsplit=1) or [""])[-1].lstrip("\"'“‘„«([").lower()
        if token in abbreviations:
            continue
        breaks += nxt.isupper() or nxt.isdigit() or nxt in _SENTENCE_OPENERS
    return breaks + 1

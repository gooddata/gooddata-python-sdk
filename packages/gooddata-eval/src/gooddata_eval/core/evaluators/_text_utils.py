# (C) 2026 GoodData Corporation
"""Shared text-extraction helpers for text-answer evaluators."""

from gooddata_eval.core.chat.render import render_answer_text
from gooddata_eval.core.models import ChatResult


def extract_text(chat_result: ChatResult) -> str:
    """Extract the agent's answer: prose plus any content-bearing non-text part."""
    return render_answer_text(chat_result)

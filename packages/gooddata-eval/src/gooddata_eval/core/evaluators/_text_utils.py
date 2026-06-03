# (C) 2026 GoodData Corporation
"""Shared text-extraction helpers for text-answer evaluators."""

from gooddata_eval.core.models import ChatResult


def extract_text(chat_result: ChatResult) -> str:
    """Extract the agent's text response, stripping whitespace."""
    if chat_result.text_response:
        return chat_result.text_response.strip()
    return ""

# (C) 2026 GoodData Corporation
"""Tests for the simulated-user reply generators (OpenAI mocked, no network).

`generate_simulated_response` produces a user reply to an agent clarification
question during multi-turn agentic evaluation. Both the visualization and
metric_skill variants require the [llm-judge] extra + OPENAI_API_KEY.
"""
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from gooddata_eval.core.agentic import metric_skill, visualization
from gooddata_eval.core.models import CreatedVisualization


def _openai_returning(text: str | None) -> MagicMock:
    client = MagicMock()
    client.chat.completions.create.return_value = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=text))]
    )
    factory = MagicMock(return_value=client)
    return factory, client


def _viz_with_filters() -> CreatedVisualization:
    return CreatedVisualization.model_validate(
        {
            "id": "v1",
            "type": "column_chart",
            "query": {
                "fields": {"m_rev": {"using": "metric/revenue"}, "d_q": {"using": "label/date.quarter"}},
                "filter_by": {
                    "f1": {"type": "date_filter", "granularity": "quarter", "from": "2024", "to": "2025"},
                    "f2": {"type": "attribute_filter", "using": "label/region", "state": {"include": ["EU"]}},
                },
            },
            "metrics": ["m_rev"],
            "view_by": ["d_q"],
        }
    )


def _viz_no_filters() -> CreatedVisualization:
    return CreatedVisualization.model_validate(
        {
            "id": "v1",
            "type": "column_chart",
            "query": {"fields": {"m_rev": {"using": "metric/revenue"}}, "filter_by": {}},
            "metrics": ["m_rev"],
            "view_by": [],
        }
    )


# --------------------------------------------------------------------------- #
# visualization variant
# --------------------------------------------------------------------------- #
def test_viz_simulated_response_builds_prompt_with_filters(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    factory, client = _openai_returning("Show me revenue by quarter for 2024-2025.")
    with patch("openai.OpenAI", factory):
        out = visualization.generate_simulated_response("Which time period?", _viz_with_filters())
    assert out == "Show me revenue by quarter for 2024-2025."
    kwargs = client.chat.completions.create.call_args.kwargs
    assert kwargs["model"] == "gpt-5.2"
    user_msg = kwargs["messages"][-1]["content"]
    assert "Metrics:" in user_msg and "date filter" in user_msg


def test_viz_simulated_response_adds_no_filter_hints(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    factory, client = _openai_returning("All-time revenue please.")
    with patch("openai.OpenAI", factory):
        visualization.generate_simulated_response("Any date filter?", _viz_no_filters())
    user_msg = client.chat.completions.create.call_args.kwargs["messages"][-1]["content"]
    # With no filters in the expected viz, the prompt instructs the sim-user to decline filters.
    assert "no date filter" in user_msg
    assert "attribute filter" in user_msg


def test_viz_simulated_response_requires_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(OSError, match="OPENAI_API_KEY"):
        visualization.generate_simulated_response("q", _viz_no_filters())


# --------------------------------------------------------------------------- #
# metric_skill variant
# --------------------------------------------------------------------------- #
def test_metric_simulated_response_returns_content(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    factory, client = _openai_returning("Use SELECT AVG(order_value).")
    with patch("openai.OpenAI", factory):
        out = metric_skill.generate_simulated_response("What aggregation?", {"maql": "SELECT AVG({metric/x})"})
    assert out == "Use SELECT AVG(order_value)."
    assert client.chat.completions.create.call_args.kwargs["model"] == "gpt-4o-mini"


def test_metric_simulated_response_falls_back_when_content_none(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    factory, _ = _openai_returning(None)
    with patch("openai.OpenAI", factory):
        out = metric_skill.generate_simulated_response("q", {"maql": "x"})
    assert out == "Please proceed."


def test_metric_simulated_response_requires_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(OSError, match="OPENAI_API_KEY"):
        metric_skill.generate_simulated_response("q", {"maql": "x"})

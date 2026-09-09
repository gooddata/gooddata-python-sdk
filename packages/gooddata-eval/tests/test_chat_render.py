# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
"""Multipart capture (sse_client) and rendering (render)."""

import json

import pytest
from gooddata_eval.core.chat.render import render_answer_text, render_search_results
from gooddata_eval.core.chat.sse_client import _KNOWN_PART_TYPES, parse_sse_lines
from gooddata_eval.core.models import ChatResult

_SEARCH_PART = {
    "type": "searchResults",
    "requestedObjectType": "metric",
    "keywords": ["key driver analysis"],
    "objects": [
        {"id": "total_net_revenue", "type": "metric", "title": "Total Net Revenue", "score": 0.9},
        {"id": "order_count", "type": "metric", "title": "Order Count", "description": "Orders placed"},
    ],
}


def _multipart_lines(*parts: dict) -> list[str]:
    return [
        "data: " + json.dumps({"item": {"role": "assistant", "content": {"type": "multipart", "parts": list(parts)}}}),
        "",
    ]


# --- capture ---------------------------------------------------------------------------


def test_search_results_part_is_captured_alongside_the_text_part():
    lines = _multipart_lines({"type": "text", "text": "Found **10 metrics**:"}, _SEARCH_PART)
    result = parse_sse_lines(lines)
    assert result.text_response == "Found **10 metrics**:"
    assert len(result.search_results) == 1
    assert result.search_results[0]["objects"][0]["title"] == "Total Net Revenue"


def test_a_turn_whose_only_part_is_non_text_still_carries_its_answer():
    result = parse_sse_lines(_multipart_lines(_SEARCH_PART))
    assert result.text_response is None
    assert render_answer_text(result) != ""
    assert "Total Net Revenue" in render_answer_text(result)


def test_an_unmodelled_part_type_is_kept_not_dropped():
    result = parse_sse_lines(_multipart_lines({"type": "kda", "kda": {"drivers": ["price"]}}))
    assert len(result.unhandled_parts) == 1
    assert result.unhandled_parts[0]["type"] == "kda"
    assert "kda" in render_answer_text(result)


def test_an_unresolved_visualization_part_is_not_treated_as_content():
    result = parse_sse_lines(_multipart_lines({"type": "visualization", "visualization": None}))
    assert result.unhandled_parts == []
    assert render_answer_text(result) == ""


def test_alert_proposal_part_still_goes_to_its_own_field():
    result = parse_sse_lines(_multipart_lines({"type": "alertProposal", "alertProposal": {"cta": "Create"}}))
    assert result.alert_proposals == [{"cta": "Create"}]
    assert result.unhandled_parts == []


def test_known_part_types_matches_the_documented_gen_ai_union():
    gen_ai_message_part_union = {
        "text",
        "visualization",
        "dashboard",
        "dashboardPatch",
        "kda",
        "whatIf",
        "searchResults",
        "alertProposal",
        "clarifyingQuestions",
    }
    assert gen_ai_message_part_union == _KNOWN_PART_TYPES


# --- rendering -------------------------------------------------------------------------


def test_render_search_results_lists_the_objects_the_judge_must_grade():
    rendered = render_search_results(_SEARCH_PART)
    assert "Search results (2 metric):" in rendered
    assert "- Total Net Revenue (metric/total_net_revenue)" in rendered
    assert "- Order Count (metric/order_count): Orders placed" in rendered
    assert "0.9" not in rendered


def test_render_search_results_of_an_empty_panel_is_empty():
    assert render_search_results({"type": "searchResults", "objects": [], "keywords": []}) == ""


def test_render_answer_text_of_a_silent_turn_is_empty():
    assert render_answer_text(ChatResult()) == ""


def test_render_answer_text_joins_prose_and_parts():
    result = parse_sse_lines(_multipart_lines({"type": "text", "text": "Found 2:"}, _SEARCH_PART))
    rendered = render_answer_text(result)
    assert rendered.startswith("Found 2:")
    assert "Total Net Revenue" in rendered


def test_a_huge_unmodelled_part_is_truncated():
    result = parse_sse_lines(_multipart_lines({"type": "whatIf", "blob": "x" * 50_000}))
    rendered = render_answer_text(result)
    assert "(truncated)" in rendered
    assert len(rendered) < 3_000


@pytest.mark.parametrize("ptype", ["dashboard", "dashboardPatch", "kda", "whatIf", "clarifyingQuestions"])
def test_no_known_part_type_is_silently_dropped(ptype):
    result = parse_sse_lines(_multipart_lines({"type": ptype, "payload": {"a": 1}}))
    assert result.unhandled_parts, f"{ptype} was dropped"

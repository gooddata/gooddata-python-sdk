# (C) 2026 GoodData Corporation
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.dataset.langfuse_source import _infer_test_kind, _item_from_raw, load_langfuse_dataset


def _raw_item(item_id, question, expected_output, dataset_name="ds"):
    return {
        "id": item_id,
        "datasetName": dataset_name,
        "input": {"question": question},
        "expectedOutput": expected_output,
    }


def test_item_from_raw_dict_input():
    raw = _raw_item("lf-1", "Show revenue", {"visualization": {"id": "x", "type": "", "query": {"fields": {}}}})
    item = _item_from_raw(raw, dataset_name="ds", test_kind="visualization")
    assert item.id == "lf-1"
    assert item.question == "Show revenue"
    # expected_output carries a "visualization" key, so _infer_test_kind classifies it as production agentic vis
    assert item.test_kind == "vis_agentic"
    assert item.dataset_name == "ds"


def test_item_from_raw_plain_string_input():
    raw = {
        "id": "lf-2",
        "datasetName": "ds",
        "input": "Show orders",
        "expectedOutput": {"visualization": {"id": "x", "type": "", "query": {"fields": {}}}},
    }
    item = _item_from_raw(raw, dataset_name="ds", test_kind="visualization")
    assert item.question == "Show orders"


def test_item_from_raw_maps_summary_input_from_input_object():
    raw = {
        "id": "lf-sum-1",
        "datasetName": "ds",
        "input": {"question": "Summarize the dashboard", "summary_input": {"dashboard_id": "dash1"}},
        "expectedOutput": {"test_kind": "dashboard_summary", "must_include": ["x"]},
    }
    item = _item_from_raw(raw, dataset_name="ds", test_kind="visualization")
    assert item.test_kind == "dashboard_summary"
    assert item.question == "Summarize the dashboard"
    assert item.summary_input is not None
    assert item.summary_input.dashboard_id == "dash1"


def test_item_from_raw_maps_summary_input_from_metadata():
    raw = {
        "id": "lf-sum-2",
        "datasetName": "ds",
        "input": "Summarize it",
        "metadata": {"summary_input": {"dashboard_id": "dash2", "visualizations": ["v1"]}},
        "expectedOutput": {"test_kind": "dashboard_summary"},
    }
    item = _item_from_raw(raw, dataset_name="ds", test_kind="dashboard_summary")
    assert item.summary_input.dashboard_id == "dash2"
    assert item.summary_input.visualizations == ["v1"]


def test_item_from_raw_summary_input_absent_is_none():
    raw = _raw_item("lf-3", "Show revenue", {"visualization": {"id": "x", "type": "", "query": {"fields": {}}}})
    item = _item_from_raw(raw, dataset_name="ds", test_kind="visualization")
    assert item.summary_input is None


def test_load_langfuse_dataset_calls_rest_api(monkeypatch):
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-test")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-test")
    monkeypatch.setenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

    item = _raw_item("i1", "How many orders?", {"visualization": {"id": "v", "type": "", "query": {"fields": {}}}})
    api_response = {"data": [item], "meta": {"totalItems": 1}}

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = api_response

    mock_client = MagicMock()
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    mock_client.get.return_value = mock_resp

    with patch("gooddata_eval.core.dataset.langfuse_source.httpx.Client", return_value=mock_client):
        items = load_langfuse_dataset("my_dataset")

    assert len(items) == 1
    assert items[0].id == "i1"
    assert items[0].question == "How many orders?"
    mock_client.get.assert_called_once()
    call_args = mock_client.get.call_args
    assert call_args[0][0] == "/api/public/dataset-items"
    assert call_args[1]["params"]["datasetName"] == "my_dataset"


def test_load_langfuse_dataset_raises_on_missing_credentials(monkeypatch):
    monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
    monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)

    with pytest.raises(RuntimeError, match="credentials not set"):
        load_langfuse_dataset("any_dataset")


def test_item_from_raw_maps_user_context_from_metadata():
    """A widget/view attachment lives in metadata and must survive the round trip.

    Without this, an attachment-driven item silently runs as a bare question and
    fails for the wrong reason.
    """
    raw = {
        "id": "lf-ctx-1",
        "datasetName": "ds",
        "input": "What does the visualization I attached show?",
        "metadata": {
            "user_context": {"referencedObjects": [{"objects": [{"type": "WIDGET", "id": "campaign_spend"}]}]}
        },
        "expectedOutput": "PASS if it describes the attached chart.",
    }
    item = _item_from_raw(raw, dataset_name="ds", test_kind="agentic_general_question")
    assert item.user_context == {"referencedObjects": [{"objects": [{"type": "WIDGET", "id": "campaign_spend"}]}]}


def test_item_from_raw_maps_user_context_from_input_object():
    raw = {
        "id": "lf-ctx-2",
        "datasetName": "ds",
        "input": {
            "question": "Summarize the chart I attached.",
            "user_context": {"referencedObjects": [{"objects": [{"type": "WIDGET", "id": "w1"}]}]},
        },
        "expectedOutput": "PASS if summarized.",
    }
    item = _item_from_raw(raw, dataset_name="ds", test_kind="agentic_general_question")
    assert item.question == "Summarize the chart I attached."
    assert item.user_context == {"referencedObjects": [{"objects": [{"type": "WIDGET", "id": "w1"}]}]}


def test_item_from_raw_user_context_absent_is_none():
    raw = _raw_item("lf-ctx-3", "No attachment here", "PASS if answered.")
    item = _item_from_raw(raw, dataset_name="ds", test_kind="agentic_general_question")
    assert item.user_context is None


def test_item_from_raw_test_kind_from_metadata_beats_default():
    """A string expectedOutput gives _infer_test_kind nothing to work with, so a
    judge-rubric dataset has to carry its kind in metadata or rely on --kind."""
    raw = {
        "id": "lf-kind-1",
        "datasetName": "ds",
        "input": "What is data normalization?",
        "metadata": {"test_kind": "agentic_general_question"},
        "expectedOutput": "PASS if it explains normalization.",
    }
    item = _item_from_raw(raw, dataset_name="ds", test_kind="visualization")
    assert item.test_kind == "agentic_general_question"


def test_item_from_raw_expected_output_test_kind_beats_metadata():
    """expectedOutput.test_kind is the pre-existing explicit override; keep it winning."""
    raw = {
        "id": "lf-kind-2",
        "datasetName": "ds",
        "input": "Summarize it",
        "metadata": {"test_kind": "agentic_general_question"},
        "expectedOutput": {"test_kind": "dashboard_summary"},
    }
    item = _item_from_raw(raw, dataset_name="ds", test_kind="visualization")
    assert item.test_kind == "dashboard_summary"


def test_a_blank_test_kind_declaration_falls_back_to_the_default():
    # "" is a str, so a blank declaration used to beat both the structural checks and the
    # CLI --kind default; the item was then skipped as an unsupported test_kind.
    assert _infer_test_kind({"test_kind": ""}, "visualization") == "visualization"
    assert _infer_test_kind({"test_kind": "   "}, "visualization") == "visualization"
    assert _infer_test_kind({}, "visualization", {"test_kind": ""}) == "visualization"
    # A real declaration still wins, and is stripped.
    assert _infer_test_kind({"test_kind": " agentic_guardrail "}, "visualization") == "agentic_guardrail"


def test_a_blank_declaration_does_not_hide_a_real_one_behind_it():
    # The lookup must not stop at the first *string* it finds: a blank
    # expectedOutput.test_kind used to shadow a valid metadata.test_kind, and the item
    # then fell through to structural inference or the CLI default.
    assert _infer_test_kind({"test_kind": ""}, "visualization", {"test_kind": "agentic_guardrail"}) == (
        "agentic_guardrail"
    )
    assert _infer_test_kind({"test_kind": "  "}, "visualization", {"test_kind": "agentic_guardrail"}) == (
        "agentic_guardrail"
    )
    # expectedOutput still wins when it actually declares something.
    assert _infer_test_kind({"test_kind": "agentic_search"}, "visualization", {"test_kind": "agentic_guardrail"}) == (
        "agentic_search"
    )

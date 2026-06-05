# (C) 2026 GoodData Corporation
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.dataset.langfuse_source import _item_from_raw, load_langfuse_dataset


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
    assert item.test_kind == "visualization"
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

# (C) 2026 GoodData Corporation
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.dataset.langfuse_source import (
    DatasetItemNotFoundError,
    _infer_test_kind,
    _item_from_raw,
    _make_client,
    load_langfuse_dataset,
)


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


def test_make_client_prefers_langfuse_base_url_over_host(monkeypatch):
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-test")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-test")
    monkeypatch.setenv("LANGFUSE_BASE_URL", "https://base.example.com")
    monkeypatch.setenv("LANGFUSE_HOST", "https://host.example.com")

    client = _make_client()
    try:
        assert str(client.base_url).rstrip("/") == "https://base.example.com"
    finally:
        client.close()


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


@pytest.mark.parametrize("value", ["dashboard_000", ["dashboard_000"], 42])
def test_item_from_raw_rejects_a_user_context_that_is_not_an_object(value: object) -> None:
    """Skipped, it would ask the item without its context and fail for an unrelated reason."""
    raw = {**_raw_item("lf-ctx-4", "What does this show?", "PASS if described."), "metadata": {"user_context": value}}
    with pytest.raises(ValueError, match="lf-ctx-4.*must be a JSON object"):
        _item_from_raw(raw, dataset_name="ds", test_kind="agentic_general_question")


def test_item_from_raw_user_context_null_is_none() -> None:
    raw = {**_raw_item("lf-ctx-5", "Anything?", "PASS if answered."), "metadata": {"user_context": None}}
    assert _item_from_raw(raw, dataset_name="ds", test_kind="agentic_general_question").user_context is None


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


_EXPECTED = {"visualization": {"id": "x", "type": "", "query": {"fields": {}}}}

# One question, four locales -- the shape every published fixture dataset actually has.
_LOCALE_ITEMS = [
    {**_raw_item(f"q1-{lang}", "Show revenue", _EXPECTED), "metadata": {"language": lang, "complexity": "Basic"}}
    for lang in ("en", "es", "fr", "pt")
]


@pytest.fixture
def locale_dataset(monkeypatch):
    """Serve `_LOCALE_ITEMS` from a mocked REST API, and hand back the mock client."""
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-test")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-test")
    monkeypatch.setenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"data": _LOCALE_ITEMS, "meta": {"totalItems": len(_LOCALE_ITEMS)}}

    mock_client = MagicMock()
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    mock_client.get.return_value = mock_resp

    with patch("gooddata_eval.core.dataset.langfuse_source.httpx.Client", return_value=mock_client):
        yield mock_client


def test_item_metadata_survives_the_load(locale_dataset):
    """DatasetItem used to be `extra="ignore"` with no metadata field, so this was dropped."""
    items = load_langfuse_dataset("mastercard_search_tool")
    assert items[0].metadata == {"language": "en", "complexity": "Basic"}


def test_an_item_without_metadata_gets_an_empty_dict(monkeypatch):
    item = _item_from_raw(_raw_item("lf-nometa", "Show revenue", _EXPECTED), dataset_name="ds", test_kind="vis_agentic")
    assert item.metadata == {}


def test_no_filter_returns_every_item(locale_dataset):
    assert len(load_langfuse_dataset("mastercard_search_tool")) == 4


def test_metadata_filter_selects_one_locale(locale_dataset):
    items = load_langfuse_dataset("mastercard_search_tool", metadata_filter={"language": "es"})
    assert [item.id for item in items] == ["q1-es"]


def test_metadata_filter_requires_every_key_to_match(locale_dataset):
    """Keys are ANDed; a dataset-wide key plus a selective one still narrows."""
    items = load_langfuse_dataset("mastercard_search_tool", metadata_filter={"language": "fr", "complexity": "Basic"})
    assert [item.id for item in items] == ["q1-fr"]


def test_metadata_filter_matching_nothing_raises_rather_than_running_zero_items(locale_dataset):
    with pytest.raises(ValueError, match="none matched the requested filter"):
        load_langfuse_dataset("mastercard_search_tool", metadata_filter={"language": "de"})


def test_item_ids_selects_a_subset_and_keeps_source_order(locale_dataset):
    items = load_langfuse_dataset("mastercard_search_tool", item_ids=["q1-pt", "q1-en"])
    assert [item.id for item in items] == ["q1-en", "q1-pt"]


def test_item_ids_and_metadata_filter_intersect(locale_dataset):
    items = load_langfuse_dataset(
        "mastercard_search_tool", item_ids=["q1-en", "q1-es"], metadata_filter={"language": "es"}
    )
    assert [item.id for item in items] == ["q1-es"]


def test_an_unknown_item_id_raises_and_names_what_is_missing(locale_dataset):
    """Silently returning the ids that did exist would read downstream as a pass-rate change."""
    with pytest.raises(DatasetItemNotFoundError) as excinfo:
        load_langfuse_dataset("mastercard_search_tool", item_ids=["q1-en", "q1-de", "q1-zz"])
    assert excinfo.value.missing == ["q1-de", "q1-zz"]
    assert "q1-de, q1-zz" in str(excinfo.value)


def test_a_filter_key_the_item_does_not_have_never_matches(locale_dataset):
    """An item with no `runner` is not an item for every runner."""
    with pytest.raises(ValueError, match="none matched the requested filter"):
        load_langfuse_dataset("mastercard_search_tool", metadata_filter={"runner": "1"})


def test_metadata_values_compare_as_strings(monkeypatch):
    """The filter arrives from a CLI `KEY=VALUE`, so the item's own int/bool must still match."""
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-test")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-test")
    monkeypatch.setenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

    raw = [{**_raw_item("q-num", "Show revenue", _EXPECTED), "metadata": {"runner": 1, "critical": False}}]
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"data": raw, "meta": {"totalItems": 1}}
    mock_client = MagicMock()
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    mock_client.get.return_value = mock_resp

    with patch("gooddata_eval.core.dataset.langfuse_source.httpx.Client", return_value=mock_client):
        items = load_langfuse_dataset("ds", metadata_filter={"runner": "1", "critical": "False"})
    assert [item.id for item in items] == ["q-num"]


def test_filtering_does_not_change_the_request_sent_to_langfuse(locale_dataset):
    """The endpoint cannot select by item id or metadata; filtering is ours, after the fetch.

    Guards against a later "optimisation" that passes these through as query params, which
    Langfuse would ignore -- the filter would silently stop working.
    """
    load_langfuse_dataset("mastercard_search_tool", item_ids=["q1-en"], metadata_filter={"language": "en"})
    params = locale_dataset.get.call_args[1]["params"]
    assert set(params) == {"datasetName", "limit", "page"}


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

# (C) 2026 GoodData Corporation
from unittest.mock import MagicMock, patch

import httpx
import pytest
from gooddata_eval.core.langfuse.sink import LangfuseSink, compute_scores
from gooddata_eval.core.runner import ItemReport


def test_compute_scores_all_pass():
    detail = {
        "metrics_correct": True,
        "dimensions_correct": True,
        "filters_correct": True,
        "viz_type_hard": True,
        "cross_ref_valid": True,
    }
    scores = compute_scores(pass_at_k=True, avg_latency_s=10.0, best_detail=detail)
    assert scores["pass_at_k"] == 1
    assert scores["quality_score"] == 1.0
    assert scores["latency_s"] == 10.0
    # speed = max(0, 1 - 10/60) ≈ 0.833; value = 0.6*1.0 + 0.2*0.833 = 0.767
    assert abs(scores["value_score"] - (0.6 + 0.2 * (1 - 10 / 60))) < 0.001


def test_compute_scores_partial_pass():
    detail = {
        "metrics_correct": True,
        "dimensions_correct": False,
        "filters_correct": True,
    }
    scores = compute_scores(pass_at_k=False, avg_latency_s=30.0, best_detail=detail)
    assert scores["pass_at_k"] == 0
    assert abs(scores["quality_score"] - 2 / 3) < 0.001


def test_compute_scores_empty_detail():
    # no bool checks in detail → quality = pass_at_k value
    scores = compute_scores(pass_at_k=True, avg_latency_s=0.0, best_detail={})
    assert scores["quality_score"] == 1.0


def test_compute_scores_skips_non_bool_detail_values():
    detail = {
        "metrics_correct": True,
        "expected_metric_uris": ["metric/a"],  # list — not a check
        "actual_metric_uris": ["metric/a"],
        "cross_ref_errors": [],
    }
    scores = compute_scores(pass_at_k=True, avg_latency_s=5.0, best_detail=detail)
    assert scores["quality_score"] == 1.0  # only 1 bool key → 1/1


def _make_sink(monkeypatch) -> LangfuseSink:
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-test")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-test")
    monkeypatch.setenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
    return LangfuseSink(dataset_name="my_dataset", run_name="gd-eval-2026-06-03-gpt-5.2")


def _passing_report() -> ItemReport:
    return ItemReport(
        id="item-1",
        dataset_name="my_dataset",
        test_kind="visualization",
        question="Show revenue by month",
        pass_at_k=True,
        runs=1,
        latency_s=15.0,
        best_detail={
            "metrics_correct": True,
            "dimensions_correct": True,
            "filters_correct": True,
            "viz_type_hard": True,
            "cross_ref_valid": True,
        },
    )


def test_langfuse_sink_posts_batch_with_four_event_types(monkeypatch):
    sink = _make_sink(monkeypatch)
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_client = MagicMock()
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    mock_client.post.return_value = mock_resp

    with patch("gooddata_eval.core.langfuse.sink.httpx.Client", return_value=mock_client):
        sink.log_item(_passing_report(), dataset_item_id="item-1")

    assert mock_client.post.call_count == 2  # ingestion + dataset-run-items
    # First call: ingestion batch (trace + 4 scores)
    ingestion_call = mock_client.post.call_args_list[0]
    batch = ingestion_call[1]["json"]["batch"]
    types = [e["type"] for e in batch]
    assert "trace-create" in types
    assert "dataset-run-item-create" not in types  # moved to dedicated endpoint
    assert types.count("score-create") == 4  # pass_at_k, quality, value, latency
    # Second call: dataset-run-items endpoint
    run_item_call = mock_client.post.call_args_list[1]
    assert "/api/public/dataset-run-items" in str(run_item_call)


def test_langfuse_sink_sets_trace_version_to_model(monkeypatch):
    # The model id is exposed on the trace `version` field so Langfuse dashboards
    # can break down / filter by it ("Version").
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-test")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-test")
    monkeypatch.setenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
    sink = LangfuseSink(dataset_name="ds", run_name="gd-eval-r", model_id="gpt-5.4-mini")

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_client = MagicMock()
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    mock_client.post.return_value = mock_resp

    with patch("gooddata_eval.core.langfuse.sink.httpx.Client", return_value=mock_client):
        sink.log_item(_passing_report(), dataset_item_id="item-1")

    batch = mock_client.post.call_args_list[0][1]["json"]["batch"]
    trace = next(e for e in batch if e["type"] == "trace-create")
    assert trace["body"]["version"] == "gpt-5.4-mini"


def test_langfuse_sink_run_item_links_correct_dataset_item(monkeypatch):
    sink = _make_sink(monkeypatch)
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_client = MagicMock()
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    mock_client.post.return_value = mock_resp

    with patch("gooddata_eval.core.langfuse.sink.httpx.Client", return_value=mock_client):
        sink.log_item(_passing_report(), dataset_item_id="item-1")

    # Second call is to /api/public/dataset-run-items
    run_item_call = mock_client.post.call_args_list[1]
    run_item_body = run_item_call[1]["json"]
    assert run_item_body["datasetItemId"] == "item-1"
    assert run_item_body["runName"] == "gd-eval-2026-06-03-gpt-5.2"


def test_langfuse_sink_swallows_http_error_and_warns(monkeypatch, capsys):
    sink = _make_sink(monkeypatch)
    mock_client = MagicMock()
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    mock_client.post.side_effect = httpx.HTTPError("timeout")

    with patch("gooddata_eval.core.langfuse.sink.httpx.Client", return_value=mock_client):
        sink.log_item(_passing_report(), dataset_item_id="item-1")  # must not raise

    err = capsys.readouterr().err
    assert "warning" in err.lower() or "langfuse" in err.lower()


def test_langfuse_sink_raises_without_credentials(monkeypatch):
    monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
    monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
    with pytest.raises(RuntimeError, match="credentials"):
        LangfuseSink(dataset_name="d", run_name="r")

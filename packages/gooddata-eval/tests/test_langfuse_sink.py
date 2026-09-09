# (C) 2026 GoodData Corporation
from __future__ import annotations

import base64
import json
import re

import httpx
import pytest
from gooddata_eval.core.langfuse.sink import LangfuseSink, compute_scores
from gooddata_eval.core.runner import ItemReport

_BASIC_AUTH = f"Basic {base64.b64encode(b'pk-test:sk-test').decode()}"


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


def test_langfuse_sink_raises_without_credentials(monkeypatch):
    monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
    monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
    with pytest.raises(RuntimeError, match="credentials"):
        LangfuseSink(dataset_name="d", run_name="r")


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


def _known_item_handler(seen: list[httpx.Request]):
    """GET dataset-items/item-1 resolves to dataset ds-123; every other call succeeds."""

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        if request.url.path == "/api/public/dataset-items/item-1":
            return httpx.Response(200, json={"id": "item-1", "datasetId": "ds-123"})
        return httpx.Response(200, json={})

    return handler


def _make_sink(monkeypatch, handler, **kwargs) -> LangfuseSink:
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-test")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-test")
    monkeypatch.setenv("LANGFUSE_BASE_URL", "https://lf.test")
    monkeypatch.delenv("LANGFUSE_HOST", raising=False)
    return LangfuseSink(
        dataset_name="my_dataset",
        run_name="gd-eval-2026-06-03-gpt-5.2",
        transport=httpx.MockTransport(handler),
        **kwargs,
    )


def _span_from(requests: list[httpx.Request]) -> dict:
    otlp_req = next(r for r in requests if r.url.path == "/api/public/otel/v1/traces")
    return json.loads(otlp_req.content)["resourceSpans"][0]["scopeSpans"][0]["spans"][0]


def test_langfuse_sink_exports_one_span_and_four_scores(monkeypatch):
    requests: list[httpx.Request] = []
    sink = _make_sink(monkeypatch, _known_item_handler(requests))

    sink.log_item(_passing_report(), dataset_item_id="item-1")

    otlp_calls = [r for r in requests if r.url.path == "/api/public/otel/v1/traces"]
    score_calls = [r for r in requests if r.url.path == "/api/public/scores"]
    assert len(otlp_calls) == 1
    assert len(score_calls) == 4

    otlp_req = otlp_calls[0]
    assert otlp_req.headers["Authorization"] == _BASIC_AUTH
    assert otlp_req.headers["x-langfuse-ingestion-version"] == "4"

    span = _span_from(requests)
    assert re.fullmatch(r"[0-9a-f]{32}", span["traceId"])
    assert re.fullmatch(r"[0-9a-f]{16}", span["spanId"])
    assert int(span["startTimeUnixNano"]) <= int(span["endTimeUnixNano"])

    attrs = {a["key"]: a["value"] for a in span["attributes"]}
    assert attrs["langfuse.experiment.name"]["stringValue"] == "gd-eval-2026-06-03-gpt-5.2"
    assert attrs["langfuse.experiment.dataset.id"]["stringValue"] == "ds-123"
    assert attrs["langfuse.experiment.item.id"]["stringValue"] == "item-1"
    assert attrs["langfuse.experiment.item.root_observation_id"]["stringValue"] == span["spanId"]
    assert json.loads(attrs["langfuse.observation.input"]["stringValue"]) == {"question": "Show revenue by month"}
    assert attrs["langfuse.trace.tags"]["arrayValue"]["values"]

    score_names = set()
    for score_req in score_calls:
        assert score_req.headers["Authorization"] == _BASIC_AUTH
        body = json.loads(score_req.content)
        assert body["traceId"] == span["traceId"]
        assert body["observationId"] == span["spanId"]
        score_names.add(body["name"])
    assert score_names == {"pass_at_k", "quality_score", "value_score", "latency_s"}

    pass_score = next(json.loads(r.content) for r in score_calls if json.loads(r.content)["name"] == "pass_at_k")
    assert pass_score["dataType"] == "BOOLEAN"
    assert pass_score["value"] == 1.0


def test_langfuse_sink_sets_span_version_to_model(monkeypatch):
    requests: list[httpx.Request] = []
    sink = _make_sink(monkeypatch, _known_item_handler(requests), model_id="gpt-5.4-mini")

    sink.log_item(_passing_report(), dataset_item_id="item-1")

    attrs = {a["key"]: a["value"] for a in _span_from(requests)["attributes"]}
    assert attrs["langfuse.version"]["stringValue"] == "gpt-5.4-mini"


def test_langfuse_sink_posts_plain_span_when_dataset_item_is_unknown(monkeypatch, capsys):
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/api/public/dataset-items/item-1":
            return httpx.Response(404, json={})
        return httpx.Response(200, json={})

    sink = _make_sink(monkeypatch, handler)

    sink.log_item(_passing_report(), dataset_item_id="item-1")

    span = _span_from(requests)
    assert not any(a["key"].startswith("langfuse.experiment.") for a in span["attributes"])
    score_calls = [r for r in requests if r.url.path == "/api/public/scores"]
    assert len(score_calls) == 4
    for score_req in score_calls:
        body = json.loads(score_req.content)
        assert body["traceId"] == span["traceId"]
        assert body["observationId"] == span["spanId"]

    err = capsys.readouterr().err
    assert err.count("warning:") == 1
    assert "item-1" in err


def test_langfuse_sink_swallows_connect_error_and_warns(monkeypatch, capsys):
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("boom", request=request)

    sink = _make_sink(monkeypatch, handler)

    sink.log_item(_passing_report(), dataset_item_id="item-1")  # must not raise

    err = capsys.readouterr().err
    assert "warning" in err.lower()


def test_langfuse_sink_skips_scores_when_span_export_fails(monkeypatch, capsys):
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/public/dataset-items/item-1":
            return httpx.Response(200, json={"id": "item-1", "datasetId": "ds-123"})
        if request.url.path == "/api/public/otel/v1/traces":
            return httpx.Response(400, text="bad span")
        return httpx.Response(200, json={})

    calls: list[httpx.Request] = []

    def recording_handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return handler(request)

    sink = _make_sink(monkeypatch, recording_handler)

    sink.log_item(_passing_report(), dataset_item_id="item-1")

    assert not any(r.url.path == "/api/public/scores" for r in calls)
    err = capsys.readouterr().err
    assert "span export failed" in err.lower()

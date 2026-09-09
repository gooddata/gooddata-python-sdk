# (C) 2026 GoodData Corporation
from __future__ import annotations

import base64
import json
import re
from datetime import datetime, timedelta, timezone

import httpx
import pytest
from gooddata_eval.core.langfuse import client as client_module
from gooddata_eval.core.langfuse.client import HttpxLangfuseClient
from gooddata_eval.core.langfuse.observations import TraceSummary
from gooddata_eval.core.langfuse.otlp import Span, otlp_attribute

_BASIC_AUTH = f"Basic {base64.b64encode(b'pk:sk').decode()}"


@pytest.fixture(autouse=True)
def _langfuse_env(monkeypatch):
    monkeypatch.setenv("LANGFUSE_BASE_URL", "https://lf.test")
    monkeypatch.delenv("LANGFUSE_HOST", raising=False)
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk")


@pytest.fixture
def make_client():
    """Build clients against a MockTransport handler and close them at teardown."""
    created: list[HttpxLangfuseClient] = []

    def _make(handler) -> HttpxLangfuseClient:
        client = HttpxLangfuseClient(transport=httpx.MockTransport(handler))
        created.append(client)
        return client

    yield _make
    for client in created:
        client.close()


def _ok(request: httpx.Request) -> httpx.Response:
    return httpx.Response(200, json={})


def _span() -> Span:
    start = datetime(2026, 9, 9, 10, 0, tzinfo=timezone.utc)
    return Span(
        trace_id="0" * 32,
        span_id="1" * 16,
        name="gd-eval",
        start=start,
        end=start + timedelta(seconds=2),
        attributes=[otlp_attribute("langfuse.observation.type", "span")],
    )


def test_missing_credentials_are_refused(monkeypatch):
    monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
    monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
    with pytest.raises(RuntimeError, match="credentials"):
        HttpxLangfuseClient()


def test_a_score_is_posted_to_the_scores_endpoint(make_client):
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return _ok(request)

    make_client(handler).create_score("t-1", "quality_score", 0.75, "NUMERIC", comment="3/4 checks passed")

    assert seen[0].method == "POST"
    assert seen[0].url.path == "/api/public/scores"
    assert seen[0].headers["Authorization"] == _BASIC_AUTH
    body = json.loads(seen[0].content)
    assert body["traceId"] == "t-1"
    assert body["name"] == "quality_score"
    assert body["value"] == 0.75
    assert body["dataType"] == "NUMERIC"
    assert body["comment"] == "3/4 checks passed"
    assert re.fullmatch(r"[0-9a-f-]{36}", body["id"])
    assert "observationId" not in body


def test_the_observation_id_is_sent_only_when_asked_for(make_client):
    bodies: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        bodies.append(json.loads(request.content))
        return _ok(request)

    client = make_client(handler)
    client.create_score("t-1", "pass_at_k", 1.0, "BOOLEAN")
    client.create_score("t-1", "pass_at_k", 1.0, "BOOLEAN", observation_id="o-root")

    assert "observationId" not in bodies[0]
    assert bodies[1]["observationId"] == "o-root"


def test_a_boolean_score_is_sent_as_a_number(make_client):
    bodies: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        bodies.append(json.loads(request.content))
        return _ok(request)

    client = make_client(handler)
    client.create_score("t-1", "pass_at_k", True, "BOOLEAN")
    client.create_score("t-1", "pass_at_k", False, "BOOLEAN")

    assert [body["value"] for body in bodies] == [1.0, 0.0]


def test_a_throttled_score_is_retried_after_the_delay_the_server_asked_for(make_client, monkeypatch):
    slept: list[float] = []
    monkeypatch.setattr(client_module.time, "sleep", slept.append)
    statuses = [429, 200]

    def handler(request: httpx.Request) -> httpx.Response:
        status = statuses[len(slept)]
        return httpx.Response(status, headers={"Retry-After": "2"} if status == 429 else {}, json={})

    make_client(handler).create_score("t-1", "quality_score", 1.0, "NUMERIC")

    assert slept == [2.0]


def test_a_retry_delay_the_server_did_not_name_falls_back_to_a_short_one(make_client, monkeypatch):
    slept: list[float] = []
    monkeypatch.setattr(client_module.time, "sleep", slept.append)
    statuses = [500, 200]

    make_client(lambda request: httpx.Response(statuses[len(slept)], json={})).create_score(
        "t-1", "quality_score", 1.0, "NUMERIC"
    )

    assert slept == [0.5]


@pytest.mark.parametrize("header", ["-5", "nan"])
def test_a_retry_after_that_cannot_be_slept_falls_back_to_the_default(header):
    # time.sleep rejects a negative or NaN delay, so either would turn a retry into an exception.
    assert client_module._retry_delay(httpx.Response(429, headers={"Retry-After": header})) == 0.5


def test_a_retry_after_beyond_the_cap_is_clamped():
    assert client_module._retry_delay(httpx.Response(429, headers={"Retry-After": "60"})) == 5.0


def test_a_retry_after_given_as_a_date_falls_back_to_the_default():
    # Retry-After is allowed to be an HTTP-date; this client reads seconds only. Langfuse
    # documents the header as a number of seconds, and the cap already bounds the wait, so
    # parsing a date could only turn the 0.5s fallback into the same 5s ceiling.
    response = httpx.Response(429, headers={"Retry-After": "Wed, 21 Oct 2026 07:28:00 GMT"})
    assert client_module._retry_delay(response) == 0.5


def test_a_score_gives_up_after_three_attempts(make_client, monkeypatch):
    monkeypatch.setattr(client_module.time, "sleep", lambda _seconds: None)
    attempts = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        return httpx.Response(503, json={})

    client = make_client(handler)
    with pytest.raises(httpx.HTTPStatusError):
        client.create_score("t-1", "quality_score", 1.0, "NUMERIC")

    assert attempts == 3


def test_a_rejected_score_is_not_retried(make_client):
    attempts = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        return httpx.Response(400, json={})

    client = make_client(handler)
    with pytest.raises(httpx.HTTPStatusError):
        client.create_score("t-1", "quality_score", 1.0, "NUMERIC")

    assert attempts == 1


def test_spans_are_exported_as_otlp_with_the_v4_ingestion_header(make_client):
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"partialSuccess": {}})

    make_client(handler).export_spans([_span()])

    assert seen[0].method == "POST"
    assert seen[0].url.path == "/api/public/otel/v1/traces"
    assert seen[0].headers["x-langfuse-ingestion-version"] == "4"
    assert seen[0].headers["Authorization"] == _BASIC_AUTH
    span = json.loads(seen[0].content)["resourceSpans"][0]["scopeSpans"][0]["spans"][0]
    assert re.fullmatch(r"[0-9a-f]{32}", span["traceId"])
    assert re.fullmatch(r"[0-9a-f]{16}", span["spanId"])
    assert int(span["startTimeUnixNano"]) <= int(span["endTimeUnixNano"])


def test_a_refused_export_raises(make_client):
    client = make_client(lambda request: httpx.Response(400, text="bad span"))
    with pytest.raises(RuntimeError):
        client.export_spans([_span()])


def test_a_partially_rejected_export_raises(make_client):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"partialSuccess": {"rejectedSpans": 1, "errorMessage": "nope"}})

    client = make_client(handler)
    with pytest.raises(RuntimeError, match="nope"):
        client.export_spans([_span()])


def test_the_dataset_of_an_item_is_looked_up_once_and_cached(make_client):
    calls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request.url.path)
        return httpx.Response(200, json={"id": "item-1", "datasetId": "ds-1"})

    client = make_client(handler)
    assert client.dataset_id_for_item("item-1") == "ds-1"
    assert client.dataset_id_for_item("item-1") == "ds-1"
    assert calls == ["/api/public/dataset-items/item-1"]


def test_an_unknown_dataset_item_is_none_and_is_not_asked_for_twice(make_client):
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(404, json={"message": "not found"})

    client = make_client(handler)
    assert client.dataset_id_for_item("local-item") is None
    assert client.dataset_id_for_item("local-item") is None
    assert calls == 1


def test_a_broken_dataset_item_lookup_raises(make_client):
    client = make_client(lambda request: httpx.Response(500, text="boom"))
    with pytest.raises(httpx.HTTPStatusError):
        client.dataset_id_for_item("item-1")


def test_the_compat_trace_api_returns_trace_summaries(make_client):
    root = {
        "traceId": "t-1",
        "id": "o-root",
        "parentObservationId": None,
        "sessionId": "conv-1",
        "latency": 4.0,
        "totalCost": None,
    }
    child = {"traceId": "t-1", "id": "o-child", "parentObservationId": "o-root", "totalCost": 0.02}
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"data": [root, child], "meta": {}})

    now = datetime.now(timezone.utc)
    result = make_client(handler).api.trace.list(from_timestamp=now, to_timestamp=now, limit=100, session_id="conv-1")

    assert seen[0].url.path == "/api/public/v2/observations"
    assert dict(seen[0].url.params)["sessionId"] == "conv-1"
    assert all(isinstance(trace, TraceSummary) for trace in result.data)
    assert [(trace.id, trace.session_id, trace.latency, trace.total_cost) for trace in result.data] == [
        ("t-1", "conv-1", 4.0, 0.02)
    ]


def test_the_compat_trace_api_accepts_timestamp_strings(make_client):
    seen: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(dict(request.url.params))
        return httpx.Response(200, json={"data": [], "meta": {}})

    make_client(handler).api.trace.list(
        from_timestamp="2026-09-09T10:00:00+00:00", to_timestamp="2026-09-09T10:05:00+00:00", limit=10
    )

    assert seen[0]["fromStartTime"] == "2026-09-09T10:00:00+00:00"
    assert "sessionId" not in seen[0]


def test_a_dataset_run_item_is_exported_as_an_experiment_root_span(make_client):
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        if request.url.path.startswith("/api/public/dataset-items/"):
            return httpx.Response(200, json={"id": "item-1", "datasetId": "ds-1"})
        return _ok(request)

    make_client(handler).api.dataset_run_items.create(
        run_name="ds_2026_model",
        dataset_item_id="item-1",
        trace_id="t-1",
        metadata={"model_version": "m"},
        run_description="desc",
    )

    assert [request.url.path for request in seen] == ["/api/public/dataset-items/item-1", "/api/public/otel/v1/traces"]
    assert seen[1].headers["x-langfuse-ingestion-version"] == "4"
    span = json.loads(seen[1].content)["resourceSpans"][0]["scopeSpans"][0]["spans"][0]
    attrs = {attr["key"]: attr["value"].get("stringValue") for attr in span["attributes"]}
    assert attrs["langfuse.experiment.name"] == "ds_2026_model"
    assert attrs["langfuse.experiment.dataset.id"] == "ds-1"
    assert attrs["langfuse.experiment.item.id"] == "item-1"
    assert attrs["langfuse.experiment.item.root_observation_id"] == span["spanId"]
    assert attrs["langfuse.experiment.description"] == "desc"
    assert attrs["langfuse.experiment.metadata.model_version"] == "m"
    assert attrs["langfuse.observation.metadata.gen_ai_trace_id"] == "t-1"


def test_a_dataset_run_item_for_an_unknown_item_raises(make_client):
    client = make_client(lambda request: httpx.Response(404, json={}))
    with pytest.raises(LookupError):
        client.api.dataset_run_items.create(run_name="run", dataset_item_id="local", trace_id="t-1")


def test_a_negative_retry_after_never_reaches_sleep(make_client, monkeypatch):
    # time.sleep raises on a negative delay, so a server clock skew or a hostile header
    # would turn a throttled score into an exception instead of a retry.
    slept: list[float] = []
    monkeypatch.setattr(client_module.time, "sleep", slept.append)
    statuses = [429, 200]

    def handler(request: httpx.Request) -> httpx.Response:
        status = statuses[len(slept)]
        return httpx.Response(status, headers={"Retry-After": "-5"} if status == 429 else {}, json={})

    make_client(handler).create_score("t-1", "quality_score", 1.0, "NUMERIC")

    assert slept == [0.5]

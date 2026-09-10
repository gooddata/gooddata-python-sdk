# (C) 2026 GoodData Corporation
"""Tests for the in-process fake Langfuse server used by the wire-level e2e tests."""

from __future__ import annotations

import httpx
import pytest

from tests._fake_langfuse import FakeLangfuse


@pytest.fixture
def server():
    with FakeLangfuse() as srv:
        yield srv


@pytest.fixture
def client(server: FakeLangfuse):
    with httpx.Client(base_url=server.base_url) as c:
        yield c


def test_dataset_items_serves_configured_dataset(client: httpx.Client, server: FakeLangfuse) -> None:
    server.dataset_name = "GDAI-2179"
    server.items = [{"id": "item-1", "datasetName": "GDAI-2179", "input": {"question": "q"}}]

    resp = client.get("/api/public/dataset-items", params={"datasetName": "GDAI-2179"})

    assert resp.status_code == 200
    body = resp.json()
    assert body["data"] == server.items
    assert body["meta"]["totalItems"] == 1


def test_dataset_items_404s_other_dataset_name(client: httpx.Client, server: FakeLangfuse) -> None:
    server.dataset_name = "GDAI-2179"

    resp = client.get("/api/public/dataset-items", params={"datasetName": "other"})

    assert resp.status_code == 404


def test_dataset_item_lookup_returns_dataset_id(client: httpx.Client, server: FakeLangfuse) -> None:
    server.dataset_id = "ds-fake"

    resp = client.get("/api/public/dataset-items/item-1")

    assert resp.status_code == 200
    assert resp.json()["datasetId"] == "ds-fake"


def test_dataset_item_lookup_404s_missing_id(client: httpx.Client, server: FakeLangfuse) -> None:
    server.missing = {"item-404"}

    resp = client.get("/api/public/dataset-items/item-404")

    assert resp.status_code == 404


def test_observations_synthesises_root_and_children_for_session(client: httpx.Client, server: FakeLangfuse) -> None:
    resp = client.get(
        "/api/public/v2/observations",
        params={"fromStartTime": "2026-01-01T00:00:00Z", "toStartTime": "2026-01-02T00:00:00Z", "sessionId": "conv-1"},
    )

    assert resp.status_code == 200
    rows = resp.json()["data"]
    assert len(rows) == 3
    root = next(r for r in rows if r["parentObservationId"] is None)
    assert root["metadata"]["conversation_id"] == "conv-1"
    assert sum(r.get("totalCost") or 0.0 for r in rows) == pytest.approx(0.03)


def test_observations_two_page_cursor_splits_root_and_children(client: httpx.Client, server: FakeLangfuse) -> None:
    server.observations_pages = 2
    params = {"fromStartTime": "2026-01-01T00:00:00Z", "toStartTime": "2026-01-02T00:00:00Z", "sessionId": "conv-2"}

    page1 = client.get("/api/public/v2/observations", params=params)
    assert page1.status_code == 200
    body1 = page1.json()
    assert len(body1["data"]) == 1
    assert body1["data"][0]["parentObservationId"] is None
    cursor = body1["meta"]["cursor"]
    assert cursor == "page-2"

    page2 = client.get("/api/public/v2/observations", params={**params, "cursor": cursor})
    assert page2.status_code == 200
    body2 = page2.json()
    assert len(body2["data"]) == 2
    assert all(r["parentObservationId"] is not None for r in body2["data"])
    assert body2["meta"] == {}


def test_observations_first_call_empty_then_rows(client: httpx.Client, server: FakeLangfuse) -> None:
    server.first_observations_call_empty = True
    params = {"fromStartTime": "2026-01-01T00:00:00Z", "toStartTime": "2026-01-02T00:00:00Z", "sessionId": "conv-3"}

    first = client.get("/api/public/v2/observations", params=params)
    assert first.status_code == 200
    assert first.json() == {"data": [], "meta": {}}

    second = client.get("/api/public/v2/observations", params=params)
    assert second.status_code == 200
    assert len(second.json()["data"]) == 3


def test_otlp_traces_records_method_path_query_and_json(client: httpx.Client, server: FakeLangfuse) -> None:
    body = {"resourceSpans": [{"spanId": "abc"}]}

    resp = client.post("/api/public/otel/v1/traces", json=body)

    assert resp.status_code == 200
    calls = server.calls("POST", "/api/public/otel/v1/traces")
    assert len(calls) == 1
    call = calls[0]
    assert call["method"] == "POST"
    assert call["path"] == "/api/public/otel/v1/traces"
    assert call["json"] == body


def test_otlp_traces_honours_configured_status_and_body(client: httpx.Client, server: FakeLangfuse) -> None:
    server.otlp_status = 400
    server.otlp_body = {"partialSuccess": {"rejectedSpans": 1}}

    resp = client.post("/api/public/otel/v1/traces", json={})

    assert resp.status_code == 400
    assert resp.json() == {"partialSuccess": {"rejectedSpans": 1}}


def test_scores_429_once_then_200(client: httpx.Client, server: FakeLangfuse) -> None:
    server.scores_429_once = True

    first = client.post("/api/public/scores", json={"traceId": "t1", "name": "n", "value": 1.0, "dataType": "NUMERIC"})
    assert first.status_code == 429
    assert first.headers["Retry-After"] == "0"

    second = client.post("/api/public/scores", json={"traceId": "t1", "name": "n", "value": 1.0, "dataType": "NUMERIC"})
    assert second.status_code == 200

# (C) 2026 GoodData Corporation
from __future__ import annotations

from datetime import datetime, timezone

import httpx
import pytest
from gooddata_eval.core.langfuse.observations import TraceSummary, list_traces_in_window, summarize_traces


def _row(
    trace_id: str,
    obs_id: str,
    *,
    parent: str | None = None,
    latency: float | None = None,
    total_cost: float | None = None,
    session_id: str | None = None,
    metadata: dict | None = None,
) -> dict:
    return {
        "traceId": trace_id,
        "id": obs_id,
        "parentObservationId": parent,
        "latency": latency,
        "totalCost": total_cost,
        "sessionId": session_id,
        "metadata": metadata,
        "startTime": "2026-09-09T10:00:00.000Z",
        "endTime": "2026-09-09T10:00:12.000Z",
    }


def test_rows_are_grouped_into_one_summary_per_trace():
    rows = [
        _row("t-1", "o-root", latency=3.0),
        _row("t-1", "o-child", parent="o-root", total_cost=0.01),
        _row("t-2", "o-root-2", latency=1.0),
    ]
    assert [summary.id for summary in summarize_traces(rows)] == ["t-1", "t-2"]


def test_the_root_is_the_row_without_a_parent_observation():
    rows = [
        _row("t-1", "o-child", parent="o-root", session_id="not-the-root", latency=99.0),
        _row("t-1", "o-root", latency=3.0, session_id="conv-1", metadata={"conversation_id": "conv-1"}),
    ]
    (summary,) = summarize_traces(rows)
    assert summary.root_observation_id == "o-root"
    assert summary.session_id == "conv-1"
    assert summary.metadata == {"conversation_id": "conv-1"}
    assert summary.latency == 3.0


def test_the_trace_cost_is_the_sum_over_its_rows():
    # The gen-ai root row carries no cost of its own; the model calls under it do.
    rows = [
        _row("t-1", "o-root", latency=3.0, total_cost=None),
        _row("t-1", "o-a", parent="o-root", total_cost=0.012),
        _row("t-1", "o-b", parent="o-root", total_cost=0.008),
    ]
    (summary,) = summarize_traces(rows)
    assert summary.total_cost == pytest.approx(0.02)


def test_a_trace_whose_root_is_not_on_the_page_is_dropped():
    # A poll that catches a conversation mid-ingestion sees children only; such a trace has
    # no latency and no session of its own, so it must not be offered to the caller.
    rows = [_row("t-partial", "o-child", parent="o-missing", total_cost=0.01)]
    assert summarize_traces(rows) == []


def test_the_root_start_and_end_times_are_timezone_aware():
    (summary,) = summarize_traces([_row("t-1", "o-root", latency=3.0)])
    assert summary.start_time == datetime(2026, 9, 9, 10, 0, 0, tzinfo=timezone.utc)
    assert summary.end_time == datetime(2026, 9, 9, 10, 0, 12, tzinfo=timezone.utc)


def test_a_legacy_trace_dict_is_still_accepted():
    summary = TraceSummary(
        {"id": "t-1", "sessionId": "conv-1", "latency": 4.5, "totalCost": 0.03, "metadata": {"k": "v"}}
    )
    assert (summary.id, summary.session_id, summary.latency, summary.total_cost) == ("t-1", "conv-1", 4.5, 0.03)
    assert summary.metadata == {"k": "v"}
    assert summary.root_observation_id is None
    assert summary.start_time is None


def test_missing_numbers_read_as_zero():
    summary = TraceSummary({"id": "t-1"})
    assert summary.latency == 0.0
    assert summary.total_cost == 0.0
    assert summary.metadata == {}


def _client(handler) -> httpx.Client:
    return httpx.Client(base_url="https://lf.test", transport=httpx.MockTransport(handler))


def test_the_window_query_carries_every_required_parameter():
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"data": [_row("t-1", "o-root", latency=1.0)], "meta": {}})

    with _client(handler) as http:
        found = list_traces_in_window(
            http,
            from_time=datetime(2026, 9, 9, 10, 0, tzinfo=timezone.utc),
            to_time=datetime(2026, 9, 9, 10, 5, tzinfo=timezone.utc),
            limit=100,
            session_id="conv-1",
            page_size=250,
        )

    assert [summary.id for summary in found] == ["t-1"]
    assert seen[0].url.path == "/api/public/v2/observations"
    params = dict(seen[0].url.params)
    assert params["fromStartTime"] == "2026-09-09T10:00:00+00:00"
    assert params["toStartTime"] == "2026-09-09T10:05:00+00:00"
    assert params["sessionId"] == "conv-1"
    assert params["fields"] == "core,basic,usage,metrics,metadata"
    assert params["limit"] == "250"


def test_an_empty_session_id_is_still_sent():
    # An empty id is a real filter value that matches nothing; dropped, the query returns
    # the whole window for the caller to throw away.
    seen: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(dict(request.url.params))
        return httpx.Response(200, json={"data": [], "meta": {}})

    now = datetime.now(timezone.utc)
    with _client(handler) as http:
        list_traces_in_window(http, from_time=now, to_time=now, limit=10, session_id="")

    assert seen[0]["sessionId"] == ""


def test_no_session_filter_is_sent_when_none_is_asked_for():
    seen: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(dict(request.url.params))
        return httpx.Response(200, json={"data": [], "meta": {}})

    now = datetime.now(timezone.utc)
    with _client(handler) as http:
        list_traces_in_window(http, from_time=now, to_time=now, limit=10, session_id=None)

    assert "sessionId" not in seen[0]


def test_an_unfiltered_window_is_read_at_the_api_page_maximum():
    # Without a session filter the page holds every trace in the window, so the wanted one
    # sits behind however many strangers the workspace produced.
    seen: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(dict(request.url.params))
        return httpx.Response(200, json={"data": [], "meta": {}})

    now = datetime.now(timezone.utc)
    with _client(handler) as http:
        list_traces_in_window(http, from_time=now, to_time=now, limit=10, session_id=None)

    assert seen[0]["limit"] == "1000"


def test_a_session_filtered_window_stays_on_the_smaller_page():
    seen: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(dict(request.url.params))
        return httpx.Response(200, json={"data": [], "meta": {}})

    now = datetime.now(timezone.utc)
    with _client(handler) as http:
        list_traces_in_window(http, from_time=now, to_time=now, limit=10, session_id="conv-1")

    assert seen[0]["limit"] == "500"


def test_the_cursor_is_followed_until_the_server_stops_handing_one_out():
    pages = [
        {"data": [_row("t-1", "o-1", parent="o-root-1", total_cost=0.5)], "meta": {"cursor": "c1"}},
        {"data": [_row("t-1", "o-root-1", latency=2.0)], "meta": {}},
    ]
    cursors: list[str | None] = []

    def handler(request: httpx.Request) -> httpx.Response:
        cursors.append(request.url.params.get("cursor"))
        return httpx.Response(200, json=pages[len(cursors) - 1])

    now = datetime.now(timezone.utc)
    with _client(handler) as http:
        found = list_traces_in_window(http, from_time=now, to_time=now, limit=10, session_id=None)

    # The root arrives on the second page, so the trace is only complete once both are in.
    assert cursors == [None, "c1"]
    assert [(summary.id, summary.total_cost, summary.latency) for summary in found] == [("t-1", 0.5, 2.0)]


def test_paging_stops_at_max_pages():
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(200, json={"data": [], "meta": {"cursor": "always-more"}})

    now = datetime.now(timezone.utc)
    with _client(handler) as http:
        list_traces_in_window(http, from_time=now, to_time=now, limit=10, session_id=None, max_pages=3)

    assert calls == 3


def test_paging_stops_once_enough_traces_are_collected():
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(
            200,
            json={
                "data": [_row(f"t-{calls}-a", "o-a", latency=1.0), _row(f"t-{calls}-b", "o-b", latency=1.0)],
                "meta": {"cursor": "more"},
            },
        )

    now = datetime.now(timezone.utc)
    with _client(handler) as http:
        found = list_traces_in_window(http, from_time=now, to_time=now, limit=2, session_id=None)

    assert calls == 1
    assert len(found) == 2


def test_more_traces_than_asked_for_are_truncated():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"data": [_row(f"t-{i}", f"o-{i}", latency=1.0) for i in range(5)], "meta": {}},
        )

    now = datetime.now(timezone.utc)
    with _client(handler) as http:
        found = list_traces_in_window(http, from_time=now, to_time=now, limit=3, session_id=None)

    assert [summary.id for summary in found] == ["t-0", "t-1", "t-2"]


def test_a_failed_page_raises():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, text="boom")

    now = datetime.now(timezone.utc)
    with _client(handler) as http, pytest.raises(httpx.HTTPStatusError):
        list_traces_in_window(http, from_time=now, to_time=now, limit=3, session_id=None)

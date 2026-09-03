# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
import os
import time
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

import httpx
import pytest
from gooddata_eval.core.agentic import _langfuse as lf_module
from gooddata_eval.core.agentic._langfuse import (
    _INLINE_LINK_BUDGET_SEC,
    _LINK_BUDGET_SEC,
    _MAX_DELAY,
    SKIP_ENV_VAR,
    _fetch_traces_for_session,
    find_traces_per_conversation,
    make_langfuse_client,
    observe,
)
from gooddata_eval.core.agentic._trace_linker import (
    BackgroundTraceLinker,
    linking_is_inline,
    run_trace_link_inline,
)


@pytest.fixture(autouse=True)
def _neutral_skip_switch(monkeypatch):
    """Run every test in this module with TAVERN_E2E_SKIP_TRACE_LINK unset.

    Two things this prevents. Tests here that exercise the polling ladder used to pass only
    because an earlier test in the file popped the variable globally -- so a developer with
    it exported (which the README tells them to do) saw real failures, and every module
    collected afterwards silently ran with trace linking re-enabled. Tests that WANT the
    switch on still set it themselves with monkeypatch; this only removes the ambient value.
    """
    monkeypatch.delenv(SKIP_ENV_VAR, raising=False)


def test_find_traces_per_conversation_is_none_for_a_conversation_with_no_trace():
    # find_traces_per_conversation's return dict is seeded with dict.fromkeys(conversation_ids)
    # (every value starts None) and only overwritten for ids where a trace was actually found --
    # callers (kda_skill.py and every other agentic skill) must treat a missing conversation as
    # None, not assume every key maps to a real trace object.
    found_trace = MagicMock(latency=12.0)

    def _fetch(langfuse, cid, window_start, window_end, pad):
        return [found_trace] if cid == "conv-found" else []

    with (
        patch("gooddata_eval.core.agentic._langfuse._fetch_traces_for_session", side_effect=_fetch),
        patch("gooddata_eval.core.agentic._langfuse.time.sleep"),
    ):
        result = find_traces_per_conversation(MagicMock(), ["conv-found", "conv-missing"], datetime.now(timezone.utc))

    assert result["conv-found"] is found_trace
    assert result["conv-missing"] is None


def test_find_traces_per_conversation_tries_before_sleeping():
    # The poll used to sleep _INITIAL_DELAY *before* its first fetch, so every conversation
    # paid a mandatory 0.5s even when Langfuse had already ingested the trace. Attempting
    # first makes the already-there case free, which is the common case once the agent turn
    # itself has taken several seconds.
    found_trace = MagicMock(latency=12.0)
    sleeps: list[float] = []

    with (
        patch("gooddata_eval.core.agentic._langfuse._fetch_traces_for_session", return_value=[found_trace]),
        patch("gooddata_eval.core.agentic._langfuse.time.sleep", side_effect=sleeps.append),
    ):
        result = find_traces_per_conversation(MagicMock(), ["conv-1"], datetime.now(timezone.utc))

    assert result["conv-1"] is found_trace
    assert sleeps == []


def test_find_traces_per_conversation_accepts_an_explicit_window_end():
    # Deferred trace linking runs the poll on a worker thread, possibly well after the
    # conversation ended. Letting it default window_end to "now" would widen the query
    # window by however long the pool was backed up -- and _fetch_traces_for_session pages
    # at _FETCH_LIMIT and filters by session locally, so a wide enough window can push the
    # wanted trace off the page entirely. Callers must be able to pin the window.
    captured = {}

    def _fetch(langfuse, cid, window_start, window_end, pad):
        captured["end"] = window_end
        return [MagicMock(latency=1.0)]

    pinned = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    with (
        patch("gooddata_eval.core.agentic._langfuse._fetch_traces_for_session", side_effect=_fetch),
        patch("gooddata_eval.core.agentic._langfuse.time.sleep"),
    ):
        find_traces_per_conversation(MagicMock(), ["c1"], datetime.now(timezone.utc), window_end=pinned)

    assert captured["end"] == pinned


class _FakeClock:
    """A clock where sleeping actually advances time.

    The retry budget is wall-clock, so a no-op time.sleep leaves monotonic() frozen and the
    deadline never arrives -- the loop would run to its sanity cap and the test would prove
    nothing about the budget.
    """

    def __init__(self) -> None:
        self.now = 1000.0
        self.sleeps: list[float] = []

    def monotonic(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds


def test_find_traces_per_conversation_keeps_retrying_within_its_budget():
    # Langfuse ingestion lag on us.cloud runs from ~35s to several minutes, so a fixed
    # 8-attempt ladder that gives up after 19s orphans every score. Trace linking is off
    # the critical path now, so patience is nearly free -- the loop retries until its
    # budget is spent rather than until an attempt count is reached.
    clock = _FakeClock()

    with (
        patch("gooddata_eval.core.agentic._langfuse._fetch_traces_for_session", return_value=[]),
        patch("gooddata_eval.core.agentic._langfuse.time", clock),
    ):
        result = find_traces_per_conversation(MagicMock(), ["conv-missing"], datetime.now(timezone.utc))

    assert result["conv-missing"] is None
    assert max(clock.sleeps) <= _MAX_DELAY
    # Long enough to outlast real ingestion lag, but bounded so the drain cannot run away.
    assert 60.0 <= sum(clock.sleeps) <= _LINK_BUDGET_SEC


def test_find_traces_per_conversation_always_makes_one_attempt_even_past_the_budget():
    # Batched linking polls every conversation after the whole agent phase, by which point
    # most traces are minutes old and hit on the first try. That first try must happen even
    # for the last conversation in a queue that has already burnt the budget, or the items
    # at the back would be skipped without ever being looked up.
    attempts = []

    def _fetch(langfuse, cid, window_start, window_end, pad):
        attempts.append(cid)
        return [MagicMock(latency=1.0)]

    with (
        patch("gooddata_eval.core.agentic._langfuse._fetch_traces_for_session", side_effect=_fetch),
        patch("gooddata_eval.core.agentic._langfuse.time.sleep"),
    ):
        result = find_traces_per_conversation(
            MagicMock(), ["c1"], datetime.now(timezone.utc), deadline=time.monotonic() - 1.0
        )

    assert attempts == ["c1"]
    assert result["c1"] is not None


def test_the_retry_budget_is_shared_across_one_items_conversations():
    # The budget bounds the batch's tail, so it has to cover a whole item, not each of its
    # K conversations. Computed per conversation, a --runs 2 item spends twice the budget
    # and --runs 3 three times, so the tail grows with K exactly where it should not.
    clock = _FakeClock()

    with (
        patch("gooddata_eval.core.agentic._langfuse._fetch_traces_for_session", return_value=[]),
        patch("gooddata_eval.core.agentic._langfuse.time", clock),
    ):
        result = find_traces_per_conversation(MagicMock(), ["c1", "c2", "c3"], datetime.now(timezone.utc))

    assert all(v is None for v in result.values())
    assert sum(clock.sleeps) <= _LINK_BUDGET_SEC


def test_every_conversation_is_still_looked_up_once_after_the_budget_is_spent():
    # Sharing the budget must not mean later conversations get skipped: by the time the
    # first one has exhausted it, the rest are minutes older and likely to resolve on their
    # single attempt.
    looked_up: list[str] = []
    clock = _FakeClock()

    def _fetch(langfuse, cid, window_start, window_end, pad):
        looked_up.append(cid)
        return []

    with (
        patch("gooddata_eval.core.agentic._langfuse._fetch_traces_for_session", side_effect=_fetch),
        patch("gooddata_eval.core.agentic._langfuse.time", clock),
    ):
        find_traces_per_conversation(MagicMock(), ["c1", "c2", "c3"], datetime.now(timezone.utc))

    assert set(looked_up) == {"c1", "c2", "c3"}


def test_the_skip_switch_announces_itself_instead_of_silently_orphaning_scores(monkeypatch):
    # TAVERN_E2E_SKIP_TRACE_LINK returns all-None before any polling, so every score is
    # orphaned and the only symptom is observe()'s generic "No trace found for dataset run"
    # -- indistinguishable from a genuine lookup failure. That ambiguity cost a long
    # debugging detour on a real run: Langfuse was healthy and every trace was present.
    # If linking is switched off, say so.
    monkeypatch.setenv(SKIP_ENV_VAR, "1")
    with (
        patch("gooddata_eval.core.agentic._langfuse._fetch_traces_for_session") as mock_fetch,
        patch("gooddata_eval.core.agentic._langfuse.warn_from_worker") as mock_warn,
    ):
        result = find_traces_per_conversation(MagicMock(), ["c1", "c2"], datetime.now(timezone.utc))

    assert result == {"c1": None, "c2": None}
    mock_fetch.assert_not_called()
    said = " ".join(str(c.args[0]) for c in mock_warn.call_args_list)
    assert SKIP_ENV_VAR in said
    assert "2" in said  # how many conversations it gave up on


def test_no_skip_announcement_when_the_switch_is_off():
    with (
        patch("gooddata_eval.core.agentic._langfuse._fetch_traces_for_session", return_value=[MagicMock(latency=1.0)]),
        patch("gooddata_eval.core.agentic._langfuse.warn_from_worker") as mock_warn,
    ):
        find_traces_per_conversation(MagicMock(), ["c1"], datetime.now(timezone.utc))

    mock_warn.assert_not_called()


@pytest.mark.parametrize(
    ("value", "should_skip"),
    [
        ("1", True),
        ("true", True),
        ("TRUE", True),
        ("yes", True),
        # The whole point: a non-empty string is truthy in Python, so `bool(os.environ[...])`
        # reads "0" -- the natural way to write "off" -- as ON, silently disabling trace
        # linking and orphaning every score in the run.
        ("0", False),
        ("false", False),
        ("False", False),
        ("no", False),
        ("", False),
    ],
)
def test_skip_switch_treats_explicit_off_values_as_off(monkeypatch, value, should_skip):
    monkeypatch.setenv(SKIP_ENV_VAR, value)
    with (
        patch(
            "gooddata_eval.core.agentic._langfuse._fetch_traces_for_session",
            return_value=[MagicMock(latency=1.0)],
        ) as mock_fetch,
        patch("gooddata_eval.core.agentic._langfuse.warn_from_worker"),
    ):
        result = find_traces_per_conversation(MagicMock(), ["c1"], datetime.now(timezone.utc))

    if should_skip:
        mock_fetch.assert_not_called()
        assert result["c1"] is None
    else:
        mock_fetch.assert_called()
        assert result["c1"] is not None


# --- the session filter has to reach the server (M8) ---


def _stub_langfuse_http(monkeypatch, captured: list[dict]):
    """A HttpxLangfuseClient whose httpx GET is recorded instead of sent."""
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk")
    monkeypatch.setenv("LANGFUSE_HOST", "https://lf.test")
    client = make_langfuse_client()

    def _get(url, params=None, **_kw):
        captured.append({"url": url, "params": params})
        return MagicMock(raise_for_status=lambda: None, json=lambda: {"data": []})

    client._http = MagicMock(get=_get)
    client.api = type(client.api)(client._http)
    return client


def test_the_trace_lookup_filters_by_session_server_side(monkeypatch):
    """Without sessionId the endpoint returns the whole window newest-first, capped at
    limit, and the caller filters locally -- so an item's own (oldest) trace is evicted
    once the window holds more than limit traces, which --concurrency makes likely by
    overlapping every item's window. The score then orphans after a full retry budget
    spent on a page that could never contain it.
    """
    captured: list[dict] = []
    client = _stub_langfuse_http(monkeypatch, captured)

    _fetch_traces_for_session(
        client, "conv-abc", datetime.now(timezone.utc), datetime.now(timezone.utc), timedelta(seconds=2)
    )

    assert len(captured) == 1
    assert captured[0]["params"]["sessionId"] == "conv-abc", "the session filter never reached the server"


def test_a_server_that_ignores_the_session_filter_cannot_hand_over_a_foreign_trace(monkeypatch):
    """The Langfuse API drops a query parameter it does not know rather than rejecting it.

    The httpx client declares ``session_id``, which used to switch the local filter off for
    it -- so a server that ignored the parameter returned the whole window, and the
    max-latency pick attached this item's scores to a stranger's trace with no warning.
    The server-side filter is still sent (paging); the local one is a post-check, not a
    fallback.
    """
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk")
    monkeypatch.setenv("LANGFUSE_HOST", "https://lf.test")
    client = make_langfuse_client()
    page = {
        "data": [
            {"id": "t-other", "sessionId": "conv-zzz", "latency": 9.0},
            {"id": "t-mine", "sessionId": "conv-abc", "latency": 1.0},
        ]
    }
    client._http = MagicMock(
        get=lambda url, params=None, **_kw: MagicMock(raise_for_status=lambda: None, json=lambda: page)
    )
    client.api = type(client.api)(client._http)
    now = datetime.now(timezone.utc)

    found = _fetch_traces_for_session(client, "conv-abc", now, now, timedelta(seconds=2))

    assert [t.id for t in found] == ["t-mine"]


def test_a_client_without_the_session_parameter_is_filtered_locally_too():
    # A client whose trace.list cannot take session_id still gets correct results, just by
    # filtering the page itself -- that path must keep working.
    wanted = MagicMock(session_id="conv-abc", latency=1.0)
    other = MagicMock(session_id="conv-zzz", latency=1.0)
    legacy = MagicMock()
    legacy.api.trace.list = lambda from_timestamp, to_timestamp, limit: MagicMock(data=[other, wanted])

    found = _fetch_traces_for_session(
        legacy, "conv-abc", datetime.now(timezone.utc), datetime.now(timezone.utc), timedelta(seconds=2)
    )

    assert found == [wanted]


# --- a 404 from dataset-run-items is one fact about the dataset, not N failures ---


@pytest.fixture
def _fresh_unlinkable_runs():
    """Reset the module-level dedup set, which otherwise leaks between tests."""
    with lf_module._UNLINKABLE_RUNS_LOCK:
        lf_module._UNLINKABLE_RUNS.clear()
    yield
    with lf_module._UNLINKABLE_RUNS_LOCK:
        lf_module._UNLINKABLE_RUNS.clear()


def _http_404() -> Exception:
    request = MagicMock()
    response = MagicMock(status_code=404)
    return httpx.HTTPStatusError("Client error '404 Not Found'", request=request, response=response)


def _langfuse_that_404s_on_run_items():
    lf = MagicMock()
    lf.api.dataset_run_items.create.side_effect = _http_404()
    return lf


def test_a_missing_dataset_item_is_reported_once_per_run_with_its_cause(_fresh_unlinkable_runs):
    """20 identical raw 404s buried the run's real output and named an endpoint, not a cause.

    The 404 means the dataset item id is not in Langfuse, which is a property of the
    dataset -- it recurs identically for every item and every pass over it -- so it is one
    fact to state once, with what to do about it.
    """
    lf = _langfuse_that_404s_on_run_items()
    said: list[str] = []

    with patch("gooddata_eval.core.agentic._langfuse.warn_from_worker", side_effect=said.append):
        for run_idx in range(5):
            for item in ("gdai-2179-001", "gdai-2179-002", "gdai-2179-003", "gdai-2179-004"):
                with observe(lf, f"trace-{item}-{run_idx}", item, f"GDAI-2179_ts_model_run{run_idx}", {}):
                    pass

    assert lf.api.dataset_run_items.create.call_count == 20
    assert len(said) == 1, f"expected one warning for the whole run, got {len(said)}"
    warning = said[0]
    assert "does not exist in Langfuse" in warning
    assert "--langfuse-dataset" in warning and SKIP_ENV_VAR in warning
    # The reader has to know the run is not a write-off.
    assert "Scores ARE still written to the traces" in warning


def test_each_model_run_gets_its_own_report(_fresh_unlinkable_runs):
    # --model a --model b produces two differently-named runs; each is separately
    # unlinkable and the operator should see that it affected both.
    lf = _langfuse_that_404s_on_run_items()
    said: list[str] = []

    with patch("gooddata_eval.core.agentic._langfuse.warn_from_worker", side_effect=said.append):
        for model in ("gpt-5.6-luna", "gpt-5.2"):
            for run_idx in range(3):
                with observe(lf, "t", "gdai-2179-001", f"GDAI-2179_ts_{model}_run{run_idx}", {}):
                    pass

    assert len(said) == 2


def test_a_non_404_link_failure_is_still_reported_every_time(_fresh_unlinkable_runs):
    # A 500 or a timeout may be transient and item-specific, so it must not be collapsed
    # into a one-shot "this dataset cannot link" claim.
    lf = MagicMock()
    lf.api.dataset_run_items.create.side_effect = RuntimeError("connection reset")
    said: list[str] = []

    with patch("gooddata_eval.core.agentic._langfuse.warn_from_worker", side_effect=said.append):
        for i in range(3):
            with observe(lf, f"t{i}", "item-1", "run", {}):
                pass

    assert len(said) == 3
    assert all("failed to create dataset run item" in w for w in said)


def test_scores_still_reach_the_trace_after_a_404(_fresh_unlinkable_runs):
    # observe() yields the trace id regardless, which is why the run was not a write-off.
    lf = _langfuse_that_404s_on_run_items()

    with (
        patch("gooddata_eval.core.agentic._langfuse.warn_from_worker"),
        observe(lf, "trace-abc", "gdai-2179-001", "run0", {}) as tid,
    ):
        pass

    assert tid == "trace-abc"


# --- the retry budget has to depend on who is waiting for it ---


def _sleep_spent(conversation_ids, *, linker) -> float:
    """Total seconds a never-resolving poll sleeps, under the given linker."""
    clock = _FakeClock()

    def _fetch(langfuse, cid, window_start, window_end, pad):
        return []

    with (
        patch("gooddata_eval.core.agentic._langfuse._fetch_traces_for_session", side_effect=_fetch),
        patch("gooddata_eval.core.agentic._langfuse.time", clock),
    ):
        linker(lambda: find_traces_per_conversation(MagicMock(), conversation_ids, datetime.now(timezone.utc)))
    return sum(clock.sleeps)


def test_an_inline_poll_keeps_the_pre_batching_budget():
    """The 120s budget was raised for the CLI, where linking is batched off the critical
    path and costs nobody anything. A direct library caller (the tavern e2e suite) gets
    run_trace_link_inline instead, so the same poll is charged straight to the test that
    triggered it -- under a step timeout. Handing that path 120s turns a ~35s miss into a
    ~110s one, inline, per item.
    """
    inline = _sleep_spent(["c1"], linker=run_trace_link_inline)

    # Reproduces the old 8-attempt sleep-first ladder to the second.
    assert 30.0 <= inline <= 35.0, inline
    assert inline < _LINK_BUDGET_SEC


def test_a_batched_poll_still_gets_the_full_budget():
    # Off the critical path, waiting is free and a miss orphans a score, so this one keeps
    # the long budget the batching change was made to afford.
    def _batched(task):
        linker = BackgroundTraceLinker(max_workers=1)
        linker.submit(task)
        linker.drain()

    batched = _sleep_spent(["c1"], linker=_batched)

    assert batched > _INLINE_LINK_BUDGET_SEC * 2, batched
    assert batched <= _LINK_BUDGET_SEC


def test_the_inline_marker_does_not_leak_out_of_the_call():
    # Scoped to the call, so a later batched drain on the same thread is not mistaken for
    # an inline one.
    assert linking_is_inline() is False
    seen = []
    run_trace_link_inline(lambda: seen.append(linking_is_inline()))
    assert seen == [True]
    assert linking_is_inline() is False


def test_a_worker_thread_is_never_treated_as_inline():
    # A thread starts with a fresh context, which is what makes the default correct for the
    # drain pool without any bookkeeping.
    seen: list[bool] = []

    def _check() -> None:
        seen.append(linking_is_inline())

    def _outer() -> None:
        linker = BackgroundTraceLinker(max_workers=1)
        linker.submit(_check)
        linker.drain()

    # Even when the drain itself is started from inside an inline task.
    run_trace_link_inline(_outer)

    assert seen == [False]


def test_an_empty_conversation_id_still_sends_the_server_side_filter():
    """The filter must reach the server even when the id is empty.

    An empty id is a real filter value that matches nothing. Dropping the query parameter on
    a falsy id would fetch the entire padded window for the local post-check to throw away,
    so the poll would spend its whole budget on pages that can never match.
    """
    seen: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(dict(request.url.params))
        return httpx.Response(200, json={"data": []})

    real_client = httpx.Client

    def fake_client(*args, **kwargs):
        kwargs.pop("transport", None)
        return real_client(*args, transport=httpx.MockTransport(handler), **kwargs)

    with (
        patch.dict(
            os.environ,
            {"LANGFUSE_HOST": "https://lf.test", "LANGFUSE_PUBLIC_KEY": "pk", "LANGFUSE_SECRET_KEY": "sk"},
        ),
        patch.object(lf_module.httpx, "Client", fake_client),
    ):
        client = make_langfuse_client()

    now = datetime.now(timezone.utc)
    with patch.object(lf_module.httpx, "Client", fake_client):
        _fetch_traces_for_session(client, "", now - timedelta(minutes=5), now, timedelta(seconds=2))

    assert seen, "no request was made"
    assert seen[0].get("sessionId") == "", (
        f"the empty id was dropped, so the server returned the whole window: {seen[0]}"
    )

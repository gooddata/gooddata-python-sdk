# (C) 2026 GoodData Corporation
"""A conversation whose gen-ai turns joined gd-eval's trace is read by trace id and gets its
root exported into that trace, scored once."""

from __future__ import annotations

import json
from contextlib import nullcontext
from datetime import datetime, timezone
from typing import Any
from unittest.mock import MagicMock, patch

import httpx
import pytest
from gooddata_eval.core.agentic import _langfuse
from gooddata_eval.core.agentic._langfuse import SKIP_ENV_VAR, find_traces_per_conversation, observe, score_safe
from gooddata_eval.core.agentic._trace_linker import (
    RunIdentity,
    conversations_to_link,
    open_item_trace,
    submit_trace_scoring,
)
from gooddata_eval.core.langfuse.client import HttpxLangfuseClient
from gooddata_eval.core.langfuse.experiment import ScoreTarget, experiment_id_for
from gooddata_eval.core.langfuse.item_scope import (
    ItemTraceScope,
    JoinedRun,
    joined_run,
    mark_joined,
    release_joined,
    trace_ids_for,
)
from gooddata_eval.core.langfuse.otlp import unix_nano

_OTLP_PATH = "/api/public/otel/v1/traces"
_OBSERVATIONS_PATH = "/api/public/v2/observations"
_WINDOW = (datetime(2026, 9, 8, 9, 0, tzinfo=timezone.utc), datetime(2026, 9, 8, 9, 5, tzinfo=timezone.utc))
_IDENTITY = RunIdentity("https://h", "tok", "ws", "ds", "2026-09-08", "gpt-x", None, None)


@pytest.fixture(autouse=True)
def _langfuse_env(monkeypatch):
    monkeypatch.setenv("LANGFUSE_BASE_URL", "https://lf.test")
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk")
    monkeypatch.setenv("LANGFUSE_TRACING_ENVIRONMENT", "staging")
    monkeypatch.delenv(SKIP_ENV_VAR, raising=False)


class _Recorder:
    """A Langfuse client over a mock transport; ``rows`` is what the observations read returns."""

    def __init__(self, rows: list[dict] | None = None) -> None:
        self.rows = rows or []
        self.requests: list[httpx.Request] = []
        self.client = HttpxLangfuseClient(transport=httpx.MockTransport(self._handle))

    def _handle(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        if request.url.path.startswith("/api/public/dataset-items/"):
            return httpx.Response(200, json={"id": "item-1", "datasetId": "ds-1"})
        if request.url.path == _OBSERVATIONS_PATH:
            return httpx.Response(200, json={"data": self.rows, "meta": {}})
        return httpx.Response(200, json={})

    def spans(self) -> list[dict]:
        return [
            span
            for request in self.requests
            if request.url.path == _OTLP_PATH
            for span in json.loads(request.content)["resourceSpans"][0]["scopeSpans"][0]["spans"]
        ]


def _attrs(span: dict) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for attr in span["attributes"]:
        ((kind, value),) = attr["value"].items()
        out[attr["key"]] = [v["stringValue"] for v in value["values"]] if kind == "arrayValue" else value
    return out


def _turn_rows(conversation_id: str) -> list[dict]:
    trace_id, span_id = trace_ids_for(conversation_id)
    turn = {"traceId": trace_id, "parentObservationId": span_id, "name": "conversation.send_message"}
    return [
        {
            **turn,
            "id": "t1",
            "sessionId": conversation_id,
            "startTime": "2026-09-08T09:00:10Z",
            "endTime": "2026-09-08T09:00:20Z",
        },
        {**turn, "id": "t2", "startTime": "2026-09-08T09:00:30Z", "endTime": "2026-09-08T09:00:50Z"},
        {
            "traceId": trace_id,
            "id": "g1",
            "parentObservationId": "t1",
            "totalCost": 0.02,
            "startTime": "2026-09-08T09:00:11Z",
            "endTime": "2026-09-08T09:00:12Z",
        },
    ]


def test_a_joined_conversation_is_read_by_its_trace_id_not_polled_by_session():
    cid = "conv-join-read"
    mark_joined(cid, JoinedRun("ds_run0", "ds-1"))
    rec = _Recorder(_turn_rows(cid))

    (trace,) = find_traces_per_conversation(rec.client, [cid], *_WINDOW).values()

    (request,) = rec.requests
    assert dict(request.url.params)["traceId"] == trace_ids_for(cid)[0]
    assert "sessionId" not in request.url.params
    assert trace.id == trace_ids_for(cid)[0]
    assert trace.latency == 20.0
    assert trace.total_cost == pytest.approx(0.02)


def test_a_joined_root_is_exported_into_the_gen_ai_trace_and_scored_once():
    cid = "conv-join-observe"
    trace_id, span_id = trace_ids_for(cid)
    mark_joined(cid, JoinedRun("ds_run1", "ds-1"))
    rec = _Recorder(_turn_rows(cid))
    (trace,) = find_traces_per_conversation(rec.client, [cid], *_WINDOW).values()

    with observe(
        rec.client, trace.id, "item-1", "ds_run1", {}, trace=trace, window=_WINDOW, conversation_id=cid, item_input="q"
    ) as tid:
        score_safe(rec.client, tid, name="passed", value=1.0, data_type="BOOLEAN")

    (span,) = rec.spans()
    assert (span["traceId"], span["spanId"]) == (trace_id, span_id)
    assert "parentSpanId" not in span
    assert span["startTimeUnixNano"] == unix_nano(datetime(2026, 9, 8, 9, 0, 10, tzinfo=timezone.utc))
    assert span["endTimeUnixNano"] == unix_nano(datetime(2026, 9, 8, 9, 0, 50, tzinfo=timezone.utc))
    attrs = _attrs(span)
    assert attrs["langfuse.environment"] == "sdk-experiment"
    assert attrs["langfuse.experiment.id"] == experiment_id_for("ds_run1")
    assert attrs["langfuse.experiment.item.root_observation_id"] == span_id
    assert attrs["langfuse.session.id"] == cid
    # No dataset lookup: the join already named the dataset.
    assert not [r for r in rec.requests if "dataset-items" in r.url.path]

    scores = [json.loads(r.content) for r in rec.requests if r.url.path == "/api/public/scores"]
    assert [(s["traceId"], s.get("observationId")) for s in scores] == [(trace_id, span_id)]
    assert tid.destinations() == [(trace_id, span_id)]


def test_a_joined_root_without_rows_falls_back_to_the_local_window():
    cid = "conv-join-no-rows"
    mark_joined(cid, JoinedRun("ds", "ds-1"))
    rec = _Recorder()

    with observe(rec.client, None, "item-1", "ds", {}, window=_WINDOW, conversation_id=cid) as tid:
        pass

    (span,) = rec.spans()
    assert span["traceId"] == trace_ids_for(cid)[0]
    assert span["startTimeUnixNano"] == unix_nano(_WINDOW[0])
    assert isinstance(tid, ScoreTarget)


def test_an_unjoined_conversation_keeps_its_own_trace_and_both_destinations():
    rec = _Recorder()
    with observe(
        rec.client, "gen-ai-id", "item-1", "ds", {}, window=_WINDOW, conversation_id="conv-never-joined"
    ) as tid:
        pass

    (span,) = rec.spans()
    assert span["traceId"] != trace_ids_for("conv-never-joined")[0]
    assert _attrs(span)["langfuse.environment"] == "staging"
    assert len(tid.destinations()) == 2


def test_no_scope_and_no_run_context_lookup_while_the_switch_is_off(monkeypatch):
    monkeypatch.setenv("GOODDATA_EVAL_JOIN_GENAI_TRACE", "0")
    rec = _Recorder()
    with patch.object(_langfuse, "build_run_context") as build:
        _, _, scope = open_item_trace(rec.client, _IDENTITY, "item-1", suffix_runs=True)
    assert scope is None
    build.assert_not_called()
    assert rec.requests == []


def test_the_scope_is_resolved_before_the_run_when_the_switch_is_on(monkeypatch):
    monkeypatch.setenv("GOODDATA_EVAL_JOIN_GENAI_TRACE", "1")
    rec = _Recorder()
    with patch.object(_langfuse, "build_run_context", return_value=("ds_ts", {"model_version": "m"})):
        _, _, scope = open_item_trace(rec.client, _IDENTITY, "item-1", suffix_runs=True)
    assert scope == ItemTraceScope("ds_ts", True, "ds-1", "item-1")
    assert scope.run_metadata == {"model_version": "m"}


@pytest.mark.parametrize("blocker", ["skip", "unknown_item", "foreign_client"])
def test_no_scope_when_the_root_could_not_be_exported(monkeypatch, blocker):
    monkeypatch.setenv("GOODDATA_EVAL_JOIN_GENAI_TRACE", "1")
    client: Any = _Recorder().client
    if blocker == "skip":
        monkeypatch.setenv(SKIP_ENV_VAR, "1")
    elif blocker == "unknown_item":
        client = HttpxLangfuseClient(transport=httpx.MockTransport(lambda _r: httpx.Response(404)))
    else:
        client = object()
    with patch.object(_langfuse, "build_run_context", return_value=("ds_ts", {})):
        assert open_item_trace(client, _IDENTITY, "item-1", suffix_runs=False)[2] is None


def test_the_deferred_task_reuses_the_scope_s_run_name():
    scope = ItemTraceScope("ds_pinned", True, "ds-1", "item-1", {"model_version": "m"})
    seen: list[Any] = []
    with (
        patch.object(_langfuse, "build_run_context") as build,
        patch.object(_langfuse, "find_traces_per_conversation", return_value={}),
    ):
        submit_trace_scoring(
            lambda task, item_id="": task(),
            _IDENTITY,
            langfuse=object(),
            dataset_item_id="item-1",
            conversation_ids=["c"],
            window_start=_WINDOW[0],
            window_end=_WINDOW[1],
            suffix_runs=True,
            write_scores=seen.append,
            scope=scope,
        )
    build.assert_not_called()
    (ctx,) = seen
    assert ctx.run_name(1) == "ds_pinned_run1"
    assert ctx.run_metadata == {"model_version": "m"}


def test_a_joined_trace_is_not_read_before_every_sent_turn_is_ingested(monkeypatch):
    cid = "conv-join-partial"
    for _turn in range(3):
        mark_joined(cid, JoinedRun("ds_run0", "ds-1"))
    monkeypatch.setattr(_langfuse, "_wait_between_attempts", lambda _delay: False)
    rec = _Recorder(_turn_rows(cid))

    assert find_traces_per_conversation(rec.client, [cid], *_WINDOW) == {cid: None}


def test_a_joined_root_releases_its_join_record_once_exported():
    cid = "conv-join-release"
    mark_joined(cid, JoinedRun("ds_run0", "ds-1"))
    rec = _Recorder(_turn_rows(cid))
    (trace,) = find_traces_per_conversation(rec.client, [cid], *_WINDOW).values()

    with observe(rec.client, trace.id, "item-1", "ds_run0", {}, trace=trace, window=_WINDOW, conversation_id=cid):
        pass

    assert joined_run(cid) is None


def test_only_the_joined_ones_among_unscored_runs_are_linked() -> None:
    mark_joined("conv-unscored-joined", JoinedRun("ds_run1", "ds-1"))
    try:
        ids = conversations_to_link(["conv-scored"], ["conv-unscored-joined", "conv-unscored-plain"])
    finally:
        release_joined("conv-unscored-joined")

    assert ids == ["conv-scored", "conv-unscored-joined"]


def test_an_unscored_joined_run_still_exports_its_root_and_writes_no_score() -> None:
    cid = "conv-join-unscored"
    trace_id, span_id = trace_ids_for(cid)
    mark_joined(cid, JoinedRun("ds_run0", "ds-1"))
    rec = _Recorder(_turn_rows(cid))

    submit_trace_scoring(
        lambda task, item_id="": task(),
        _IDENTITY,
        langfuse=rec.client,
        dataset_item_id="item-1",
        conversation_ids=[cid],
        window_start=_WINDOW[0],
        window_end=_WINDOW[1],
        suffix_runs=False,
        write_scores=lambda ctx: ctx.export_unscored(0, cid),
        scope=ItemTraceScope("ds", False, "ds-1", "item-1"),
    )

    assert [(s["traceId"], s["spanId"]) for s in rec.spans()] == [(trace_id, span_id)]
    assert not [r for r in rec.requests if r.url.path == "/api/public/scores"]
    assert joined_run(cid) is None


def test_an_unscored_run_that_did_not_join_exports_nothing() -> None:
    rec = _Recorder()

    submit_trace_scoring(
        lambda task, item_id="": task(),
        _IDENTITY,
        langfuse=rec.client,
        dataset_item_id="item-1",
        conversation_ids=[],
        window_start=_WINDOW[0],
        window_end=_WINDOW[1],
        suffix_runs=False,
        write_scores=lambda ctx: ctx.export_unscored(0, "conv-plain"),
        scope=ItemTraceScope("ds", False, "ds-1", "item-1"),
    )

    assert rec.spans() == []


def test_the_model_version_is_read_once_per_workspace_and_a_failure_is_retried() -> None:
    _langfuse._active_llm_model.cache_clear()
    setting = MagicMock(content={"defaultModelId": "gpt-5.2"})
    sdk = MagicMock()
    sdk.catalog_workspace.get_workspace_setting.side_effect = [RuntimeError("down"), setting]
    with patch("gooddata_sdk.GoodDataSdk.create", return_value=sdk) as create:
        versions = [_langfuse.get_model_version("https://h", "tok", "ws1") for _ in range(3)]
    _langfuse._active_llm_model.cache_clear()

    assert versions == ["", "gpt-5.2", "gpt-5.2"]
    assert create.call_count == 2


@pytest.mark.parametrize("write_scores_fails", [False, True])
def test_the_deferred_task_releases_joins_its_scoring_never_exported(write_scores_fails):
    cid = f"conv-join-unobserved-{write_scores_fails}"
    mark_joined(cid, JoinedRun("ds_run0", "ds-1"))

    def write_scores(_ctx: Any) -> None:
        if write_scores_fails:
            raise RuntimeError("scoring broke")

    with (
        patch.object(_langfuse, "find_traces_per_conversation", return_value={}),
        pytest.raises(RuntimeError) if write_scores_fails else nullcontext(),
    ):
        submit_trace_scoring(
            lambda task, item_id="": task(),
            _IDENTITY,
            langfuse=object(),
            dataset_item_id="item-1",
            conversation_ids=[cid],
            window_start=_WINDOW[0],
            window_end=_WINDOW[1],
            suffix_runs=False,
            write_scores=write_scores,
        )

    assert joined_run(cid) is None

# (C) 2026 GoodData Corporation
"""observe() exports gd-eval's own experiment root span, and scores fan out to both targets."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any
from unittest.mock import MagicMock

import httpx
import pytest
from gooddata_eval.core.agentic._langfuse import SKIP_ENV_VAR, observe, score_safe
from gooddata_eval.core.agentic._trace_linker import RunTraceContext
from gooddata_eval.core.langfuse.client import HttpxLangfuseClient
from gooddata_eval.core.langfuse.experiment import ScoreTarget, experiment_id_for
from gooddata_eval.core.langfuse.observations import TraceSummary
from gooddata_eval.core.langfuse.otlp import unix_nano

_OTLP_PATH = "/api/public/otel/v1/traces"
_SCORES_PATH = "/api/public/scores"
_WINDOW = (datetime(2026, 9, 8, 10, 0, tzinfo=timezone.utc), datetime(2026, 9, 8, 10, 1, tzinfo=timezone.utc))


@pytest.fixture(autouse=True)
def _langfuse_env(monkeypatch):
    monkeypatch.setenv("LANGFUSE_BASE_URL", "https://lf.test")
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk")
    monkeypatch.delenv("LANGFUSE_TRACING_ENVIRONMENT", raising=False)
    monkeypatch.delenv(SKIP_ENV_VAR, raising=False)


class _Recorder:
    """A Langfuse client whose requests are recorded instead of sent; every item resolves."""

    def __init__(self) -> None:
        self.requests: list[httpx.Request] = []
        self.client = HttpxLangfuseClient(transport=httpx.MockTransport(self._handle))

    def _handle(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        if request.url.path.startswith("/api/public/dataset-items/"):
            return httpx.Response(200, json={"id": "item-1", "datasetId": "ds-1"})
        return httpx.Response(200, json={})

    def spans(self) -> list[dict]:
        return [
            span
            for request in self.requests
            if request.url.path == _OTLP_PATH
            for span in json.loads(request.content)["resourceSpans"][0]["scopeSpans"][0]["spans"]
        ]

    def score_bodies(self) -> list[dict]:
        return [json.loads(request.content) for request in self.requests if request.url.path == _SCORES_PATH]


@pytest.fixture
def rec():
    recorder = _Recorder()
    yield recorder
    recorder.client.close()


def _attrs(span: dict) -> dict[str, Any]:
    """Span attributes as `{key: value}`, unwrapped from the OTLP typed-value envelope."""
    unwrapped: dict[str, Any] = {}
    for attr in span["attributes"]:
        ((kind, value),) = attr["value"].items()
        unwrapped[attr["key"]] = [v["stringValue"] for v in value["values"]] if kind == "arrayValue" else value
    return unwrapped


def _gen_ai_trace() -> TraceSummary:
    """The gen-ai root observation row gd-eval's span is timed and costed from."""
    return TraceSummary(
        {
            "traceId": "gen-ai-id",
            "id": "o-root",
            "parentObservationId": None,
            "sessionId": "conv-1",
            "latency": 18.4,
            "totalCost": 0.0123,
            "startTime": "2026-09-08T10:00:00+00:00",
            "endTime": "2026-09-08T10:00:18.400000+00:00",
        }
    )


def test_a_linked_run_is_exported_as_one_experiment_root_span(rec):
    trace = _gen_ai_trace()
    run_name = "GDAI-2179_2026-09-08_gpt-5.2_run0"

    with observe(
        rec.client,
        trace.id,
        "item-1",
        run_name,
        {"model_version": "gpt-5.2", "testing_framework": "tavern-e2e"},
        trace=trace,
        item_input="Show revenue by month",
        output={"passed": True},
    ) as tid:
        pass

    exports = [request for request in rec.requests if request.url.path == _OTLP_PATH]
    assert len(exports) == 1
    assert exports[0].method == "POST"
    assert exports[0].headers["x-langfuse-ingestion-version"] == "4"
    assert exports[0].headers["Authorization"].startswith("Basic ")

    (span,) = rec.spans()
    assert re.fullmatch(r"[0-9a-f]{32}", span["traceId"])
    assert re.fullmatch(r"[0-9a-f]{16}", span["spanId"])
    # The span covers the gen-ai turn, not the moment linking happened.
    assert span["startTimeUnixNano"] == unix_nano(trace.start_time)
    assert span["endTimeUnixNano"] == unix_nano(trace.end_time)

    attrs = _attrs(span)
    assert attrs["langfuse.experiment.name"] == run_name
    assert attrs["langfuse.experiment.id"] == experiment_id_for(run_name)
    assert attrs["langfuse.experiment.dataset.id"] == "ds-1"
    assert attrs["langfuse.experiment.item.id"] == "item-1"
    assert attrs["langfuse.experiment.item.root_observation_id"] == span["spanId"]
    assert attrs["langfuse.session.id"] == "conv-1"
    assert attrs["langfuse.version"] == "gpt-5.2"
    assert attrs["langfuse.trace.name"] == "gd-eval: Show revenue by month"
    assert attrs["langfuse.trace.tags"] == ["gd-eval", "tavern-e2e"]
    assert attrs["langfuse.observation.metadata.gen_ai_trace_id"] == "gen-ai-id"
    assert attrs["langfuse.observation.metadata.gen_ai_latency_s"] == 18.4
    assert attrs["langfuse.observation.metadata.gen_ai_cost_usd"] == 0.0123
    assert json.loads(attrs["langfuse.observation.input"]) == {"question": "Show revenue by month"}
    assert json.loads(attrs["langfuse.observation.output"]) == {"passed": True}

    assert tid == "gen-ai-id"
    assert tid.experiment_trace_id == span["traceId"]
    assert tid.experiment_span_id == span["spanId"]


def test_the_span_carries_every_key_the_daily_report_reads(rec):
    """gdc-nas `report.py` and `combo_report.py` read these attribute names off the span.

    Renaming any of them breaks the daily report, so they are pinned here.
    """
    trace = _gen_ai_trace()

    with observe(
        rec.client,
        trace.id,
        "item-1",
        "run0",
        {
            "testing_framework": "tavern-e2e",
            "github_run_id": "123",
            "model_version": "gpt",
            "reasoning_effort": "LOW",
        },
        trace=trace,
        conversation_id="conv-1",
    ):
        pass

    attrs = _attrs(rec.spans()[0])
    assert attrs["langfuse.experiment.metadata.testing_framework"] == "tavern-e2e"
    assert attrs["langfuse.experiment.metadata.github_run_id"] == "123"
    assert attrs["langfuse.experiment.metadata.model_version"] == "gpt"
    assert attrs["langfuse.experiment.metadata.reasoning_effort"] == "LOW"
    assert attrs["langfuse.observation.metadata.gen_ai_trace_id"] == "gen-ai-id"
    assert attrs["langfuse.observation.metadata.conversation_id"] == "conv-1"
    assert attrs["langfuse.trace.metadata.run_name"] == "run0"


def test_a_run_whose_gen_ai_trace_never_arrived_still_gets_its_experiment_span(rec):
    # Without a trace the run would vanish from the comparison entirely; the span keeps it
    # in the experiment and gives the scores somewhere to land.

    with observe(
        rec.client,
        None,
        "item-1",
        "run0",
        {"model_version": "gpt"},
        window=_WINDOW,
        conversation_id="conv-9",
    ) as tid:
        score_safe(rec.client, tid, name="pass_at_k", value=False, data_type="BOOLEAN")

    (span,) = rec.spans()
    attrs = _attrs(span)
    assert attrs["langfuse.session.id"] == "conv-9"
    assert "langfuse.observation.metadata.gen_ai_trace_id" not in attrs
    assert span["startTimeUnixNano"] == unix_nano(_WINDOW[0])
    assert span["endTimeUnixNano"] == unix_nano(_WINDOW[1])

    bodies = rec.score_bodies()
    assert [body["traceId"] for body in bodies] == [span["traceId"]]
    assert bodies[0]["observationId"] == span["spanId"]


def test_a_score_target_writes_to_both_the_gen_ai_trace_and_the_experiment_span(rec):
    target = ScoreTarget("gen-ai-id", "0" * 32, "1" * 16)

    score_safe(rec.client, target, name="pass_at_k", value=True, data_type="BOOLEAN")

    bodies = rec.score_bodies()
    assert [body["traceId"] for body in bodies] == ["gen-ai-id", "0" * 32]
    # The gen-ai call stays byte-identical to what a legacy client already accepts.
    assert "observationId" not in bodies[0]
    assert bodies[1]["observationId"] == "1" * 16
    assert [body["value"] for body in bodies] == [1.0, 1.0]


def test_a_plain_trace_id_still_writes_exactly_one_score(rec):

    score_safe(rec.client, "trace-abc", name="quality_score", value=0.5, data_type="NUMERIC")

    assert [body["traceId"] for body in rec.score_bodies()] == ["trace-abc"]


def test_nothing_to_score_against_writes_no_score(rec):

    score_safe(rec.client, None, name="quality_score", value=0.5, data_type="NUMERIC")

    assert rec.score_bodies() == []


def test_the_skip_switch_stops_every_langfuse_write_not_just_the_poll(rec, monkeypatch):
    """The switch is how an operator runs with Langfuse turned off or unreachable.

    Exporting the experiment span anyway would put one span, one item lookup and a score
    fan-out per run back on a path the operator switched off -- and against an unreachable
    Langfuse, one export warning per item.
    """
    monkeypatch.setenv(SKIP_ENV_VAR, "1")

    with observe(rec.client, None, "item-1", "run", {}) as tid:
        score_safe(rec.client, tid, name="pass_at_k", value=True, data_type="BOOLEAN")

    assert tid is None
    assert rec.requests == []


def test_a_non_httpx_client_never_reaches_the_experiment_path():
    # The skill suites hand observe() a MagicMock, which answers every hasattr -- so the
    # legacy branch keys on the concrete client type instead.
    lf = MagicMock()

    with observe(lf, "t", "item-1", "run0", {}) as tid:
        pass

    lf.dataset_id_for_item.assert_not_called()
    lf.export_spans.assert_not_called()
    assert tid == "t"
    assert tid.experiment_trace_id is None


def test_a_legacy_client_with_no_trace_yields_nothing_to_score():
    with observe(MagicMock(), None, "item-1", "run0", {}) as tid:
        pass

    assert tid is None


def test_the_run_context_forwards_its_window_and_item_input_to_observe():
    # The window and the question are resolved on the calling thread and carried by the
    # context, so a skill's scoring block keeps calling ctx.observe(pt, run_idx).
    lf = MagicMock()
    trace = MagicMock(id="gen-ai-id")
    ctx = RunTraceContext(
        {"model_version": "m"}, lf, "client", "item-1", "base", True, {}, _WINDOW, "Show revenue by month"
    )

    ctx.observe(trace, 2, conversation_id="conv-1", output={"passed": True})

    args, kwargs = lf.observe.call_args
    assert args == ("client", "gen-ai-id", "item-1", "base_run2", {"model_version": "m"})
    assert kwargs == {
        "trace": trace,
        "window": _WINDOW,
        "conversation_id": "conv-1",
        "item_input": "Show revenue by month",
        "output": {"passed": True},
    }

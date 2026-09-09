# (C) 2026 GoodData Corporation
"""End-to-end Langfuse v4 choreography against the in-process fake server.

Nothing here is mocked below the HTTP boundary: the real `HttpxLangfuseClient` and
`LangfuseSink` are built from the fixture's `LANGFUSE_*` env and talk to `FakeLangfuse`, so
each test asserts the request sequence a real run produces -- poll observations, look the
dataset item up, export one experiment root span, score it.
"""

from __future__ import annotations

import contextlib
import time
from datetime import datetime
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.cli import main as cli_main
from gooddata_eval.cli.agentic_runner import run_agentic_items
from gooddata_eval.core.agentic import _langfuse as agentic_langfuse
from gooddata_eval.core.agentic._trace_linker import run_trace_link_inline
from gooddata_eval.core.agentic.general_question import evaluate_agentic_general_question
from gooddata_eval.core.langfuse.client import HttpxLangfuseClient
from gooddata_eval.core.langfuse.experiment import experiment_id_for
from gooddata_eval.core.langfuse.otlp import unix_nano
from gooddata_eval.core.models import ChatResult, DatasetItem
from gooddata_eval.core.runner import EvalReport, ItemReport
from gooddata_eval.core.workspace import ActiveLlmProvider, ResolvedModel

from tests._fake_langfuse import FakeLangfuse, observation_rows

_MODEL = "gpt-5.2"
_RUN_TS = "2026-01-01_00-00-00"
_OBSERVATIONS = "/api/public/v2/observations"
_OTLP = "/api/public/otel/v1/traces"
_SCORES = "/api/public/scores"
_DATASET_ITEMS = "/api/public/dataset-items"


class _NoSleep:
    """`_langfuse`'s view of the `time` module with the poll's backoff sleeps removed."""

    monotonic = staticmethod(time.monotonic)

    @staticmethod
    def sleep(_seconds: float) -> None:
        return None


@pytest.fixture(autouse=True)
def _forget_unlinkable_runs():
    """The once-per-run warning gate is module state; no test may inherit another's."""
    agentic_langfuse._UNLINKABLE_RUNS.clear()
    yield
    agentic_langfuse._UNLINKABLE_RUNS.clear()


def _chat_client(conversation_ids: list[str]) -> MagicMock:
    client = MagicMock()
    client.create_conversation.side_effect = conversation_ids
    client.send_message.return_value = ChatResult.model_validate(
        {"textResponse": "42", "toolCallEvents": [], "reasoningSteps": [], "responseId": "resp-1"}
    )
    return client


def _passing_judge() -> MagicMock:
    judge = MagicMock()
    judge.model = "gpt-4o"
    judge.score.return_value = (True, "Correct answer")
    return judge


@contextlib.contextmanager
def _agent_stubbed(conversation_ids: list[str], *, no_sleep: bool = False):
    """Stub the SSE agent and the judge, and pin the model version the run reports."""
    with (
        patch("gooddata_eval.core.agentic.general_question.ChatClient", return_value=_chat_client(conversation_ids)),
        patch("gooddata_eval.core.agentic.general_question.LLMJudge", return_value=_passing_judge()),
        patch.object(agentic_langfuse, "get_model_version", return_value=_MODEL),
    ):
        if no_sleep:
            with patch.object(agentic_langfuse, "time", _NoSleep):
                yield
        else:
            yield


def _run_general_question(*, dataset_item_id: str, dataset_name: str) -> None:
    evaluate_agentic_general_question(
        host="http://host/api/v1/actions/workspaces/ws1/ai",
        token="tok",
        workspace_id="ws1",
        question="What is 6 times 7?",
        expected_output="42",
        k=1,
        langfuse=None,
        dataset_item_id=dataset_item_id,
        dataset_name=dataset_name,
        run_timestamp=_RUN_TS,
        submit_trace_link=run_trace_link_inline,
    )


def _spans(server: FakeLangfuse) -> list[dict]:
    return [
        span
        for call in server.calls("POST", _OTLP)
        for resource in call["json"]["resourceSpans"]
        for scope in resource["scopeSpans"]
        for span in scope["spans"]
    ]


def _attrs(span: dict) -> dict[str, Any]:
    """Span attributes as `key -> unwrapped OTLP value`."""
    return {a["key"]: next(iter(a["value"].values())) for a in span["attributes"]}


def _score_bodies(server: FakeLangfuse) -> list[dict]:
    return [call["json"] for call in server.calls("POST", _SCORES)]


def test_agentic_inline_path_polls_looks_up_exports_and_scores(fake_langfuse: FakeLangfuse, capsys) -> None:
    fake_langfuse.first_observations_call_empty = True
    run_name = f"inline_{_RUN_TS}_{_MODEL}"

    with _agent_stubbed(["conv-1"], no_sleep=True):
        _run_general_question(dataset_item_id="item-1", dataset_name="inline")

    polls = fake_langfuse.calls("GET", _OBSERVATIONS)
    assert len(polls) >= 2, "the empty first page must be retried"
    assert {p["query"]["sessionId"] for p in polls} == {"conv-1"}

    lookups = fake_langfuse.calls("GET", f"{_DATASET_ITEMS}/item-1")
    assert len(lookups) == 1

    spans = _spans(fake_langfuse)
    assert len(spans) == 1
    span, attrs = spans[0], _attrs(spans[0])
    assert attrs["langfuse.experiment.name"] == run_name
    assert attrs["langfuse.experiment.item.id"] == "item-1"
    assert attrs["langfuse.experiment.item.root_observation_id"] == span["spanId"]
    assert attrs["langfuse.session.id"] == "conv-1"

    root_row = next(r for r in observation_rows("conv-1") if r["parentObservationId"] is None)
    assert attrs["langfuse.observation.metadata.gen_ai_trace_id"] == root_row["traceId"]
    assert span["startTimeUnixNano"] == unix_nano(datetime.fromisoformat(root_row["startTime"]))
    assert span["endTimeUnixNano"] == unix_nano(datetime.fromisoformat(root_row["endTime"]))

    bodies = _score_bodies(fake_langfuse)
    on_gen_ai = [b for b in bodies if b["traceId"] == root_row["traceId"]]
    on_span = [b for b in bodies if b["traceId"] == span["traceId"]]
    assert len(bodies) == len(on_gen_ai) + len(on_span)
    assert {b["name"] for b in on_gen_ai} == {b["name"] for b in on_span}
    assert {"general_question_pass", "llm_judge_score", "quality_score", "value_score"} == {
        b["name"] for b in on_gen_ai
    }
    assert all("observationId" not in b for b in on_gen_ai)
    assert all(b["observationId"] == span["spanId"] for b in on_span)

    # Cost is summed over the trace's rows: the gen-ai root carries none, its children do.
    value_score = next(b for b in on_span if b["name"] == "value_score")
    assert "cost=$0.0300" in value_score["comment"]
    assert "latency=12.50s" in value_score["comment"]
    assert capsys.readouterr().out.count("WARNING") == 0


def test_batched_path_puts_both_items_in_one_experiment(fake_langfuse: FakeLangfuse, monkeypatch) -> None:
    items = [
        DatasetItem(
            id=f"item-{n}",
            dataset_name="batched",
            test_kind="agentic_general_question",
            question="What is 6 times 7?",
            expected_output="42",
        )
        for n in (1, 2)
    ]
    closed_after: list[int] = []
    real_close = HttpxLangfuseClient.close

    def _spy_close(self: HttpxLangfuseClient) -> None:
        closed_after.append(len(fake_langfuse.requests))
        real_close(self)

    monkeypatch.setattr(HttpxLangfuseClient, "close", _spy_close)

    with _agent_stubbed(["conv-1", "conv-2"]):
        report = run_agentic_items(
            items,
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            k=1,
            use_langfuse=True,
            run_ts=_RUN_TS,
        )

    assert [i.pass_at_k for i in report.items] == [True, True]

    spans = _spans(fake_langfuse)
    assert len(spans) == 2
    run_name = f"batched_{_RUN_TS}_{_MODEL}"
    assert {_attrs(s)["langfuse.experiment.id"] for s in spans} == {experiment_id_for(run_name)}
    assert {_attrs(s)["langfuse.experiment.item.id"] for s in spans} == {"item-1", "item-2"}
    assert {_attrs(s)["langfuse.session.id"] for s in spans} == {"conv-1", "conv-2"}

    # flush() and close() are the run's last words to Langfuse: nothing may follow them.
    assert closed_after == [len(fake_langfuse.requests)]


def test_local_dataset_item_keeps_gen_ai_scores_and_warns_once(fake_langfuse: FakeLangfuse, capsys) -> None:
    fake_langfuse.missing = {"local-item"}

    with _agent_stubbed(["conv-1"]):
        _run_general_question(dataset_item_id="local-item", dataset_name="local")

    assert fake_langfuse.calls("POST", _OTLP) == []

    out = capsys.readouterr().out
    assert out.count("does not exist in Langfuse") == 1

    root_row = next(r for r in observation_rows("conv-1") if r["parentObservationId"] is None)
    bodies = _score_bodies(fake_langfuse)
    assert {b["name"] for b in bodies} == {
        "general_question_pass",
        "llm_judge_score",
        "quality_score",
        "value_score",
    }
    assert all(b["traceId"] == root_row["traceId"] for b in bodies)
    assert all("observationId" not in b for b in bodies)


def _stub_single_shot_cli(monkeypatch) -> None:
    """Stub everything the CLI touches outside Langfuse: connection, model, chat, runner."""
    monkeypatch.setattr(cli_main, "resolve_connection", lambda host, token, profile: ("https://h", "tok"))

    class _FakeController:
        def __init__(self, *a: object, **k: object) -> None: ...
        def get_active(self) -> ActiveLlmProvider:
            return ActiveLlmProvider(provider_id="prov", default_model_id=_MODEL)

        def resolve_and_activate(self, requested: str | None, provider: str | None = None) -> ResolvedModel:
            return ResolvedModel(
                provider_id="prov", model_id=requested or _MODEL, switched=False, provider_name="Test Provider"
            )

        def restore(self, original: object) -> None: ...
        def close(self) -> None: ...

    monkeypatch.setattr(cli_main, "WorkspaceModelController", _FakeController)
    monkeypatch.setattr(cli_main, "ChatClient", lambda **k: object())

    def _fake_run(items: list[DatasetItem], backend: object, *, runs: int, model: str, **kw: Any) -> EvalReport:
        reports = [
            ItemReport(
                id=item.id,
                dataset_name=item.dataset_name,
                test_kind=item.test_kind,
                question=item.question,
                pass_at_k=True,
                runs=runs,
                latency_s=15.0,
                best_detail={"metrics_correct": True},
            )
            for item in items
        ]
        for index, item_report in enumerate(reports, start=1):
            kw["on_langfuse_item_done"](index, len(reports), item_report)
        return EvalReport(model=model, workspace_id=kw["workspace_id"], items=reports)

    monkeypatch.setattr(cli_main, "run_items", _fake_run)


def test_cli_langfuse_dataset_run_writes_one_experiment_span_per_item(fake_langfuse: FakeLangfuse, monkeypatch) -> None:
    fake_langfuse.items = [
        {"id": f"item-{n}", "datasetName": "fake", "input": {"question": f"q{n}"}, "expectedOutput": "rubric"}
        for n in (1, 2)
    ]
    _stub_single_shot_cli(monkeypatch)

    exit_code = cli_main.main(
        [
            "run",
            "--host",
            "https://h",
            "--token",
            "tok",
            "--workspace",
            "ws1",
            "--langfuse-dataset",
            "fake",
            "--langfuse",
            "--runs",
            "1",
            "--quiet",
        ]
    )

    assert exit_code == 0
    dataset_reads = [c for c in fake_langfuse.calls("GET", _DATASET_ITEMS) if c["path"] == _DATASET_ITEMS]
    assert len(dataset_reads) == 1
    assert dataset_reads[0]["query"]["datasetName"] == "fake"

    spans = _spans(fake_langfuse)
    assert len(spans) == 2
    assert {_attrs(s)["langfuse.experiment.item.id"] for s in spans} == {"item-1", "item-2"}
    assert {_attrs(s)["langfuse.version"] for s in spans} == {_MODEL}

    bodies = _score_bodies(fake_langfuse)
    assert len(bodies) == 8
    by_span = {s["spanId"]: s["traceId"] for s in spans}
    for body in bodies:
        assert by_span[body["observationId"]] == body["traceId"]
    for span in spans:
        names = {b["name"] for b in bodies if b["observationId"] == span["spanId"]}
        assert names == {"pass_at_k", "quality_score", "value_score", "latency_s"}


def test_a_refused_span_export_keeps_the_gen_ai_scores(fake_langfuse: FakeLangfuse, capsys) -> None:
    fake_langfuse.otlp_status = 500

    with _agent_stubbed(["conv-1"]):
        _run_general_question(dataset_item_id="item-1", dataset_name="refused")

    out = capsys.readouterr().out
    assert "failed to export experiment span" in out

    bodies = _score_bodies(fake_langfuse)
    assert bodies, "scores still go to the gen-ai trace when the span is refused"
    assert all("observationId" not in b for b in bodies)


def test_a_rate_limited_score_is_retried_and_lands(fake_langfuse: FakeLangfuse) -> None:
    fake_langfuse.scores_429_once = True

    with _agent_stubbed(["conv-1"]):
        _run_general_question(dataset_item_id="item-1", dataset_name="throttled")

    bodies = _score_bodies(fake_langfuse)
    # Eight writes -- four scores on each of the gen-ai trace and the experiment span --
    # plus the one refused attempt the client repeated.
    assert len(bodies) == 9
    posted_twice = [b for b in bodies if bodies.count(b) == 2]
    assert len(posted_twice) == 2, "exactly one score body was posted twice"


def test_the_dataset_run_item_shim_exports_one_experiment_span(fake_langfuse: FakeLangfuse) -> None:
    """The keyword shape gdc-nas's trace linker calls on this client."""
    client = HttpxLangfuseClient()
    try:
        client.api.dataset_run_items.create(
            run_name="nas_run",
            dataset_item_id="item-1",
            trace_id="gen-ai-id",
            metadata={"testing_framework": "tavern-e2e"},
            run_description="",
        )
    finally:
        client.close()

    assert len(fake_langfuse.calls("GET", f"{_DATASET_ITEMS}/item-1")) == 1
    (span,) = _spans(fake_langfuse)
    attrs = _attrs(span)
    assert attrs["langfuse.experiment.name"] == "nas_run"
    assert attrs["langfuse.experiment.dataset.id"] == fake_langfuse.dataset_id
    assert attrs["langfuse.experiment.item.id"] == "item-1"
    assert attrs["langfuse.experiment.item.root_observation_id"] == span["spanId"]
    assert attrs["langfuse.experiment.metadata.testing_framework"] == "tavern-e2e"
    assert attrs["langfuse.observation.metadata.gen_ai_trace_id"] == "gen-ai-id"
    assert attrs["langfuse.trace.metadata.run_name"] == "nas_run"
    # An empty run_description is no description at all.
    assert "langfuse.experiment.description" not in attrs

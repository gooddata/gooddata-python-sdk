# (C) 2026 GoodData Corporation
import inspect
from typing import Any
from unittest.mock import MagicMock, patch

import httpx
import pytest
from gooddata_eval.core.agentic import _langfuse as agentic_langfuse
from gooddata_eval.core.agentic._trace_linker import run_trace_link_inline
from gooddata_eval.core.evaluators._llm_judge import JudgeResponseError
from gooddata_eval.core.evaluators.takeaway import DocumentTakeawayEvaluator
from gooddata_eval.core.models import ChatResult
from gooddata_eval.core.takeaway.evaluate import TakeawayAssertionError, evaluate_document_takeaway

from tests._fake_langfuse import FakeLangfuse

_GOOD = "**Growth now comes from new markets.** Sales rose again this period, led by the Nordics, while core markets held flat."
_LONG = "**Sales grew.** " + " ".join(["word"] * 60) + "."
_OTLP = "/api/public/otel/v1/traces"
_SCORES = "/api/public/scores"


def _posted_scores(fake_langfuse: FakeLangfuse) -> list[dict]:
    bodies: list[dict] = []
    for call in fake_langfuse.calls("POST", _SCORES):
        body = call["json"]
        bodies.extend(body if isinstance(body, list) else [body])
    return bodies


def _dataset_item(**overrides: Any) -> dict:
    return {
        "id": "item-1",
        "question": "P01 default format, Sales page",
        "expected_output": {},
        "takeaway_input": {"visualizations": ["v1"], "max_characters": 300},
        **overrides,
    }


def _chat(text: str) -> ChatResult:
    return ChatResult(text_response=text, raw_response={"takeaway": text, "noData": False, "contextOmitted": []})


def _client(*texts: str) -> MagicMock:
    client = MagicMock()
    client.ask.side_effect = [_chat(t) for t in texts]
    return client


def _evaluator(*, judge_error: bool = False) -> DocumentTakeawayEvaluator:
    with patch("openai.OpenAI"), patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test"}):
        ev = DocumentTakeawayEvaluator()
    for judge, verdict in ((ev._positive_judge, True), (ev._violation_judge, False)):
        judge.score = MagicMock(
            side_effect=JudgeResponseError("empty body twice") if judge_error else None, return_value=(verdict, "ok")
        )
    return ev


def _evaluate(client: MagicMock | None, **kwargs: Any) -> Any:
    params: dict[str, Any] = {
        "host": "https://h",
        "token": "tok",
        "workspace_id": "ws",
        "dataset_item": _dataset_item(),
        "dataset_name": "agent_document_takeaway",
        "run_timestamp": "2026-10-22_00-00-00",
        "client": client,
        "evaluator": _evaluator(),
        "langfuse": MagicMock(),
        **kwargs,
    }
    return evaluate_document_takeaway(**params)


def test_evaluate_builds_and_closes_its_own_client_when_none_is_given() -> None:
    client = _client(_GOOD)
    with patch("gooddata_eval.core.takeaway.evaluate.TakeawayClient", return_value=client) as client_cls:
        outcome = _evaluate(None)

    client_cls.assert_called_once_with(host="https://h", token="tok", workspace_id="ws")
    client.close.assert_called_once_with()
    assert outcome.runs_passed == 1


def test_evaluate_leaves_an_injected_client_open() -> None:
    client = _client(_GOOD)
    _evaluate(client)

    client.close.assert_not_called()


def test_evaluate_passes_and_returns_the_outcome() -> None:
    outcome = _evaluate(_client(_GOOD, _GOOD), k=2)

    assert outcome.runs_passed == 2
    assert outcome.runs_effective == 2
    assert outcome.detail["word_count"] == 20
    assert outcome.failed_runs == []
    assert outcome.timings.agent_s >= 0.0


def test_evaluate_raises_on_fail_with_detail() -> None:
    with pytest.raises(TakeawayAssertionError) as exc_info:
        _evaluate(_client(_LONG))

    exc = exc_info.value
    assert "word_budget" in str(exc)
    assert "Gate pass@1 failed: 0/1 runs passed" in str(exc)
    assert exc.detail["word_budget"] is False
    assert exc.detail["word_count"] == 62
    assert exc.runs_passed == 0
    assert exc.runs_effective == 1
    assert len(exc.failed_runs) == 1


def test_evaluate_power_gate_fails_on_one_bad_run() -> None:
    with pytest.raises(TakeawayAssertionError, match="pass\\^2 failed: 1/2"):
        _evaluate(_client(_GOOD, _LONG), k=2, gate="power")

    outcome = _evaluate(_client(_GOOD, _LONG), k=2, gate="any")
    assert outcome.runs_passed == 1
    assert len(outcome.failed_runs) == 1


def test_every_run_ungraded_is_a_judge_error_not_a_failure() -> None:
    with pytest.raises(JudgeResponseError, match="no readable verdict") as exc_info:
        _evaluate(_client(_GOOD, _GOOD), k=2, evaluator=_evaluator(judge_error=True))

    exc = exc_info.value
    assert exc.runs_effective == 2
    assert exc.runs_passed == 0
    assert exc.detail["actual_output"] == _GOOD
    assert exc.detail["word_count"] == 20
    assert exc.detail["unscored_runs"] == 2
    assert [run["error"] for run in exc.failed_runs] == [exc.detail["judge_errors"][0]] * 2


def test_item_without_takeaway_input_is_rejected_before_any_request() -> None:
    client = _client(_GOOD)
    item = _dataset_item()
    del item["takeaway_input"]

    with pytest.raises(ValueError, match="'item-1'.*takeaway_input"):
        _evaluate(client, dataset_item=item)

    client.ask.assert_not_called()


def test_http_error_surfaces_with_status_and_body() -> None:
    request = httpx.Request("POST", "https://h/api/v1/ai/workspaces/ws/takeaway")
    response = httpx.Response(400, request=request, text='{"reason": "NO_AVAILABLE_AGENT"}')
    client = MagicMock()
    client.ask.side_effect = httpx.HTTPStatusError(
        f"Takeaway request failed with 400: {response.text}", request=request, response=response
    )
    submit = MagicMock()

    with pytest.raises(httpx.HTTPStatusError, match="NO_AVAILABLE_AGENT"):
        _evaluate(client, submit_trace_link=submit)

    submit.assert_not_called()


def test_signature_accepts_what_the_tavern_shim_passes() -> None:
    params = inspect.signature(evaluate_document_takeaway).parameters

    for name in (
        "host",
        "token",
        "workspace_id",
        "dataset_item",
        "dataset_name",
        "run_timestamp",
        "model_version_override",
        "reasoning_effort",
        "k",
        "gate",
        "run_metadata_extra",
    ):
        assert name in params, name


def test_langfuse_item_has_testing_framework_metadata(fake_langfuse: FakeLangfuse) -> None:
    with patch.object(agentic_langfuse, "get_model_version", return_value="gpt-5.2"):
        _evaluate(
            _client(_GOOD),
            langfuse=None,
            submit_trace_link=run_trace_link_inline,
            run_metadata_extra={"testing_framework": "tavern-e2e", "github_run_id": "123"},
        )

    spans = [
        span
        for call in fake_langfuse.calls("POST", _OTLP)
        for resource in call["json"]["resourceSpans"]
        for scope in resource["scopeSpans"]
        for span in scope["spans"]
    ]
    assert len(spans) == 1
    attrs = {a["key"]: next(iter(a["value"].values())) for a in spans[0]["attributes"]}
    assert attrs["langfuse.experiment.metadata.testing_framework"] == "tavern-e2e"
    assert attrs["langfuse.experiment.metadata.github_run_id"] == "123"
    assert attrs["langfuse.experiment.metadata.model_version"] == "gpt-5.2"

    scores = {score["name"]: score for score in _posted_scores(fake_langfuse)}
    for name in ("gate_passed", "pass_at_k", "pass_power_k", "word_budget", "no_meta", "quality_score"):
        assert name in scores, name
    assert scores["word_count"]["value"] == 20
    assert scores["word_count"]["dataType"] == "NUMERIC"
    assert scores["headline_word_count"]["value"] == 6
    assert scores["default_exclude_exact_figure"]["value"] == 1.0


def _http_error(status: int, body: str) -> httpx.HTTPStatusError:
    request = httpx.Request("POST", "https://h/api/v1/ai/workspaces/ws/takeaway")
    response = httpx.Response(status, request=request, text=body)
    return httpx.HTTPStatusError(f"Takeaway request failed with {status}: {body}", request=request, response=response)


def test_a_transient_error_on_one_run_keeps_the_graded_runs(fake_langfuse: FakeLangfuse) -> None:
    client = MagicMock()
    client.ask.side_effect = [_chat(_GOOD), _chat(_GOOD), _http_error(502, "Visualizations failed to execute.")]

    with patch.object(agentic_langfuse, "get_model_version", return_value="gpt-5.2"):
        outcome = _evaluate(client, k=3, gate="any", langfuse=None, submit_trace_link=run_trace_link_inline)

    assert outcome.runs_passed == 2
    assert outcome.runs_effective == 3
    assert outcome.detail["unscored_runs"] == 1
    assert outcome.detail["request_errors"] == [outcome.failed_runs[0]["error"]]
    assert "judge_errors" not in outcome.detail
    assert len(outcome.failed_runs) == 1
    assert "502" in outcome.failed_runs[0]["error"]
    assert "failed to execute" in outcome.failed_runs[0]["error"]
    gate_scores = [s for s in _posted_scores(fake_langfuse) if s["name"] == "gate_passed"]
    assert len(gate_scores) == 2
    assert all(score["value"] == 1 for score in gate_scores)


def test_a_transient_error_on_every_run_raises_it() -> None:
    client = MagicMock()
    client.ask.side_effect = [_http_error(502, "Visualizations failed to execute.")] * 2
    submit = MagicMock()

    with pytest.raises(httpx.HTTPStatusError, match="502.*failed to execute"):
        _evaluate(client, k=2, submit_trace_link=submit)

    submit.assert_not_called()


def test_a_deterministic_client_error_raises_on_the_first_run() -> None:
    client = MagicMock()
    client.ask.side_effect = [_http_error(400, '{"reason": "NO_AVAILABLE_AGENT"}'), _chat(_GOOD), _chat(_GOOD)]

    with pytest.raises(httpx.HTTPStatusError, match="NO_AVAILABLE_AGENT"):
        _evaluate(client, k=3)

    assert client.ask.call_count == 1


def test_no_data_run_publishes_no_word_counts(fake_langfuse: FakeLangfuse) -> None:
    client = MagicMock()
    client.ask.return_value = ChatResult(text_response="", raw_response={"takeaway": None, "noData": True})

    with patch.object(agentic_langfuse, "get_model_version", return_value="gpt-5.2"):
        _evaluate(
            client,
            dataset_item=_dataset_item(expected_output={"no_data": True}),
            langfuse=None,
            submit_trace_link=run_trace_link_inline,
        )

    names = {score["name"] for score in _posted_scores(fake_langfuse)}
    assert "no_data" in names
    assert "word_count" not in names
    assert "headline_word_count" not in names


def test_an_invalid_fixture_fails_before_any_request() -> None:
    client = _client(_GOOD)
    submit = MagicMock()

    with pytest.raises(ValueError, match="max_sentence"):
        _evaluate(
            client,
            dataset_item=_dataset_item(expected_output={"format": {"max_sentence": 1}}),
            submit_trace_link=submit,
        )

    client.ask.assert_not_called()
    submit.assert_not_called()


def test_each_run_writes_its_own_document_takeaway_pass(fake_langfuse: FakeLangfuse) -> None:
    with patch.object(agentic_langfuse, "get_model_version", return_value="gpt-5.2"):
        _evaluate(_client(_GOOD, _LONG), k=2, gate="any", langfuse=None, submit_trace_link=run_trace_link_inline)

    scores = [s for s in _posted_scores(fake_langfuse) if s["name"] == "document_takeaway_pass"]
    assert sorted(score["value"] for score in scores) == [0, 1]
    assert all(score["dataType"] == "BOOLEAN" for score in scores)


def test_a_read_timeout_is_an_errored_run_not_an_item_failure() -> None:
    client = MagicMock()
    client.ask.side_effect = [_chat(_GOOD), httpx.ReadTimeout("read timed out")]

    outcome = _evaluate(client, k=2, gate="any")

    assert outcome.runs_passed == 1
    assert "ReadTimeout" in outcome.detail["request_errors"][0]


def test_an_unsupported_protocol_raises_on_the_first_run() -> None:
    client = MagicMock()
    client.ask.side_effect = [httpx.UnsupportedProtocol("no scheme"), _chat(_GOOD)]

    with pytest.raises(httpx.UnsupportedProtocol):
        _evaluate(client, k=2)

    assert client.ask.call_count == 1


def test_power_gate_failure_from_an_errored_run_names_the_request_error() -> None:
    client = MagicMock()
    client.ask.side_effect = [_chat(_GOOD), _http_error(502, "Visualizations failed to execute.")]

    with pytest.raises(TakeawayAssertionError) as exc_info:
        _evaluate(client, k=2, gate="power")

    message = str(exc_info.value)
    assert "Failed checks: none" not in message
    assert "Request errors:" in message
    assert "502" in message


def test_an_ungraded_item_with_request_errors_says_so() -> None:
    client = MagicMock()
    client.ask.side_effect = [_chat(_GOOD), _http_error(502, "Visualizations failed to execute.")]

    with pytest.raises(JudgeResponseError) as exc_info:
        _evaluate(client, k=2, evaluator=_evaluator(judge_error=True))

    message = str(exc_info.value)
    assert "no run of 2 could be graded" in message
    assert "judge returned no readable verdict for 1 run(s)" in message
    assert "request failed for 1 run(s)" in message
    assert "502" in message

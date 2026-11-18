# (C) 2026 GoodData Corporation
import inspect
from typing import Any
from unittest.mock import MagicMock, patch

import httpx
import pytest
from gooddata_eval.core.agentic import _langfuse as agentic_langfuse
from gooddata_eval.core.agentic._trace_linker import run_trace_link_inline
from gooddata_eval.core.catalog.evaluate import CatalogMetadataAssertionError, evaluate_catalog_metadata
from gooddata_eval.core.evaluators._llm_judge import JudgeResponseError
from gooddata_eval.core.evaluators.catalog_metadata import CatalogMetadataEvaluator
from gooddata_eval.core.models import ChatResult

from tests._fake_langfuse import FakeLangfuse

_GOOD = "Shows net sales by product category over the last 12 months, so teams can compare category performance."
_LONG = "Sales grew. " + " ".join(["word"] * 90) + "."
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
        "question": "Description for the visualization 'Net Sales by Product Category'",
        "expected_output": {"must_include": ["Mentions product categories."]},
        "catalog_input": {"object_type": "Visualization", "object_id": "v1", "output": "description"},
        **overrides,
    }


def _chat(text: str, retries: int = 0) -> ChatResult:
    return ChatResult(
        text_response=text,
        raw_response={"description": text, "note": None, "output": "description", "unusable_retries": retries},
    )


def _client(*texts: str) -> MagicMock:
    client = MagicMock()
    client.ask.side_effect = [_chat(t) for t in texts]
    return client


def _evaluator(*, judge_error: bool = False) -> CatalogMetadataEvaluator:
    with patch("openai.OpenAI"), patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test"}):
        ev = CatalogMetadataEvaluator()
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
        "dataset_name": "analytics_catalog_generate",
        "run_timestamp": "2026-11-17_00-00-00",
        "client": client,
        "evaluator": _evaluator(),
        "langfuse": MagicMock(),
        **kwargs,
    }
    return evaluate_catalog_metadata(**params)


def _http_error(status: int, body: str) -> httpx.HTTPStatusError:
    request = httpx.Request("POST", "https://h/api/v1/actions/workspaces/ws/ai/analyticsCatalog/generateDescription")
    response = httpx.Response(status, request=request, text=body)
    return httpx.HTTPStatusError(
        f"Catalog generate request failed with {status}: {body}", request=request, response=response
    )


def test_evaluate_builds_and_closes_its_own_client_when_none_is_given() -> None:
    client = _client(_GOOD)
    with patch("gooddata_eval.core.catalog.evaluate.CatalogMetadataClient", return_value=client) as client_cls:
        outcome = _evaluate(None)

    client_cls.assert_called_once_with(host="https://h", token="tok", workspace_id="ws")
    client.close.assert_called_once()
    assert outcome.runs_passed == 1


def test_evaluate_passes_and_returns_the_outcome() -> None:
    outcome = _evaluate(_client(_GOOD, _GOOD), k=2)

    assert outcome.runs_passed == 2
    assert outcome.runs_effective == 2
    assert outcome.detail["word_count"] == 17
    assert outcome.failed_runs == []


def test_evaluate_raises_on_fail_with_detail() -> None:
    with pytest.raises(CatalogMetadataAssertionError) as exc_info:
        _evaluate(_client(_LONG))

    exc = exc_info.value
    assert "max_words" in str(exc)
    assert "Gate pass@1 failed: 0/1 runs passed" in str(exc)
    assert exc.detail["max_words"] is False
    assert exc.runs_passed == 0
    assert len(exc.failed_runs) == 1


def test_evaluate_power_gate_fails_on_one_bad_run() -> None:
    with pytest.raises(CatalogMetadataAssertionError, match="pass\\^2 failed: 1/2"):
        _evaluate(_client(_GOOD, _LONG), k=2, gate="power")

    outcome = _evaluate(_client(_GOOD, _LONG), k=2, gate="any")
    assert outcome.runs_passed == 1


def test_every_run_ungraded_is_a_judge_error_not_a_failure() -> None:
    with pytest.raises(JudgeResponseError, match="no readable verdict") as exc_info:
        _evaluate(_client(_GOOD, _GOOD), k=2, evaluator=_evaluator(judge_error=True))

    assert exc_info.value.detail["unscored_runs"] == 2


def test_item_without_catalog_input_is_rejected_before_any_request() -> None:
    client = _client(_GOOD)
    item = _dataset_item()
    del item["catalog_input"]

    with pytest.raises(ValueError, match="'item-1'.*catalog_input"):
        _evaluate(client, dataset_item=item)

    client.ask.assert_not_called()


def test_an_invalid_fixture_fails_before_any_request() -> None:
    client = _client(_GOOD)

    with pytest.raises(ValueError, match="max_word"):
        _evaluate(client, dataset_item=_dataset_item(expected_output={"format": {"max_word": 1}}))

    client.ask.assert_not_called()


def test_signature_accepts_what_the_tavern_shim_passes() -> None:
    params = inspect.signature(evaluate_catalog_metadata).parameters

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


def test_scores_are_written_per_run(fake_langfuse: FakeLangfuse) -> None:
    client = MagicMock()
    client.ask.side_effect = [_chat(_GOOD, retries=1), _chat(_LONG)]
    with patch.object(agentic_langfuse, "get_model_version", return_value="gpt-5.2"):
        _evaluate(client, k=2, gate="any", langfuse=None, submit_trace_link=run_trace_link_inline)

    scores = _posted_scores(fake_langfuse)
    passes = [s for s in scores if s["name"] == "catalog_metadata_pass"]
    assert sorted(s["value"] for s in passes) == [0, 1]
    names = {s["name"] for s in scores}
    for name in ("gate_passed", "pass_at_k", "generated", "no_note", "max_words", "include_0", "quality_score"):
        assert name in names, name
    assert sorted(s["value"] for s in scores if s["name"] == "unusable_retries") == [0, 1]


def test_a_transient_error_on_one_run_keeps_the_graded_runs() -> None:
    client = MagicMock()
    client.ask.side_effect = [_chat(_GOOD), _http_error(502, "bad gateway")]

    outcome = _evaluate(client, k=2, gate="any")

    assert outcome.runs_passed == 1
    assert "502" in outcome.detail["request_errors"][0]


def test_a_transient_error_on_every_run_raises_it() -> None:
    client = MagicMock()
    client.ask.side_effect = [_http_error(502, "bad gateway")] * 2

    with pytest.raises(httpx.HTTPStatusError, match="502"):
        _evaluate(client, k=2)


def test_a_deterministic_client_error_raises_on_the_first_run() -> None:
    client = MagicMock()
    client.ask.side_effect = [_http_error(403, "AI module not entitled"), _chat(_GOOD)]

    with pytest.raises(httpx.HTTPStatusError, match="not entitled"):
        _evaluate(client, k=2)

    assert client.ask.call_count == 1


def test_evaluate_leaves_an_injected_client_open() -> None:
    client = _client(_GOOD)
    _evaluate(client)
    client.close.assert_not_called()


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


def test_a_declined_run_publishes_no_word_count(fake_langfuse: FakeLangfuse) -> None:
    client = MagicMock()
    client.ask.return_value = ChatResult(
        text_response="", raw_response={"description": None, "note": "Object not found", "unusable_retries": 0}
    )
    with patch.object(agentic_langfuse, "get_model_version", return_value="gpt-5.2"):
        _evaluate(
            client,
            dataset_item=_dataset_item(expected_output={"expect_note": True}),
            langfuse=None,
            submit_trace_link=run_trace_link_inline,
        )

    names = {score["name"] for score in _posted_scores(fake_langfuse)}
    assert "declined_with_note" in names
    assert "word_count" not in names

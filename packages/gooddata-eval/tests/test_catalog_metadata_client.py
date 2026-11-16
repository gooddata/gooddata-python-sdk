# (C) 2026 GoodData Corporation
import json
from collections.abc import Callable

import httpx
import pytest
from gooddata_eval.core import _retry as retry_mod
from gooddata_eval.core.catalog.http_client import CatalogMetadataClient, is_unusable
from gooddata_eval.core.models import CatalogInput, DatasetItem


def _item(catalog_input: dict | None) -> DatasetItem:
    return DatasetItem(
        id="c1",
        dataset_name="d",
        test_kind="catalog_metadata",
        question="Title for the metric 'ARPU'",
        expected_output={},
        catalog_input=CatalogInput.model_validate(catalog_input) if catalog_input is not None else None,
    )


def _client(handler: Callable[[httpx.Request], httpx.Response]) -> CatalogMetadataClient:
    client = CatalogMetadataClient(host="https://h/", token="tok", workspace_id="ws")
    client._client = httpx.Client(transport=httpx.MockTransport(handler))
    return client


def _sequence(captured: list, responses: list[dict]) -> Callable[[httpx.Request], httpx.Response]:
    def handler(request: httpx.Request) -> httpx.Response:
        captured.append({"url": str(request.url), "body": json.loads(request.content)})
        return httpx.Response(200, json=responses[min(len(captured), len(responses)) - 1])

    return handler


@pytest.mark.parametrize(("output", "action"), [("title", "generateTitle"), ("description", "generateDescription")])
def test_posts_object_to_the_action_of_the_output(output: str, action: str) -> None:
    captured: list = []
    client = _client(_sequence(captured, [{output: "Average Revenue per Customer", "note": None}]))

    result = client.ask(_item({"object_type": "Metric", "object_id": "arpu", "output": output}))

    assert captured == [
        {
            "url": f"https://h/api/v1/actions/workspaces/ws/ai/analyticsCatalog/{action}",
            "body": {"objectType": "Metric", "objectId": "arpu"},
        }
    ]
    assert result.text_response == "Average Revenue per Customer"
    assert result.raw_response == {
        output: "Average Revenue per Customer",
        "note": None,
        "output": output,
        "unusable_retries": 0,
    }


@pytest.mark.parametrize("unusable", [{"title": None, "note": None}, {"title": "string", "note": "string"}])
def test_asks_again_once_after_an_unusable_answer(unusable: dict) -> None:
    captured: list = []
    client = _client(_sequence(captured, [unusable, {"title": "Average Revenue", "note": None}]))

    result = client.ask(_item({"object_type": "Metric", "object_id": "arpu", "output": "title"}))

    assert len(captured) == 2
    assert result.text_response == "Average Revenue"
    assert result.raw_response is not None
    assert result.raw_response["unusable_retries"] == 1


def test_keeps_a_second_unusable_answer_as_empty_text() -> None:
    captured: list = []
    client = _client(_sequence(captured, [{"title": "string", "note": "string"}]))

    result = client.ask(_item({"object_type": "Metric", "object_id": "arpu", "output": "title"}))

    assert len(captured) == 2
    assert result.text_response == ""


def test_a_declined_answer_with_a_note_is_not_retried() -> None:
    captured: list = []
    client = _client(_sequence(captured, [{"description": None, "note": "Object not found"}]))

    result = client.ask(_item({"object_type": "Visualization", "object_id": "x", "output": "description"}))

    assert len(captured) == 1
    assert result.text_response == ""
    assert result.raw_response is not None
    assert result.raw_response["note"] == "Object not found"


def test_rejects_an_item_without_catalog_input() -> None:
    client = _client(_sequence([], [{}]))
    with pytest.raises(ValueError, match="catalog_input"):
        client.ask(_item(None))


def test_non_2xx_raises_with_status() -> None:
    client = _client(lambda request: httpx.Response(403, text="forbidden"))
    with pytest.raises(httpx.HTTPStatusError, match="403"):
        client.ask(_item({"object_type": "Metric", "object_id": "arpu", "output": "title"}))


def test_is_unusable() -> None:
    assert is_unusable({"title": None, "note": None}, "title")
    assert is_unusable({"title": "string", "note": None}, "title")
    assert not is_unusable({"title": None, "note": "Not found"}, "title")
    assert not is_unusable({"title": "Revenue", "note": None}, "title")


def test_a_placeholder_note_is_dropped() -> None:
    client = _client(_sequence([], [{"description": None, "note": "string"}]))

    result = client.ask(_item({"object_type": "Visualization", "object_id": "x", "output": "description"}))

    assert result.text_response == ""
    assert result.raw_response is not None
    assert result.raw_response["note"] is None


@pytest.fixture
def sleeps(monkeypatch: pytest.MonkeyPatch) -> list[float]:
    for name in (
        "GOODDATA_EVAL_CHAT_MAX_RETRIES",
        "GOODDATA_EVAL_CHAT_INITIAL_BACKOFF_S",
        "GOODDATA_EVAL_CHAT_BACKOFF_FACTOR",
        "GOODDATA_EVAL_CHAT_MAX_BACKOFF_S",
    ):
        monkeypatch.delenv(name, raising=False)
    recorded: list[float] = []
    monkeypatch.setattr(retry_mod.time, "sleep", recorded.append)
    return recorded


def _scripted(*responses: httpx.Response | Exception) -> tuple[Callable[[httpx.Request], httpx.Response], list[int]]:
    calls: list[int] = []
    it = iter(responses)

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(1)
        nxt = next(it)
        if isinstance(nxt, Exception):
            raise nxt
        return nxt

    return handler, calls


_OK = httpx.Response(200, json={"title": "Average Revenue", "note": None})
_ARPU_TITLE = {"object_type": "Metric", "object_id": "arpu", "output": "title"}


@pytest.mark.parametrize("first", [httpx.Response(503, text="busy"), httpx.ConnectError("refused")])
def test_a_transient_failure_is_retried(first: httpx.Response | Exception, sleeps: list[float]) -> None:
    handler, calls = _scripted(first, _OK)

    result = _client(handler).ask(_item(_ARPU_TITLE))

    assert result.text_response == "Average Revenue"
    assert len(calls) == 2
    assert len(sleeps) == 1


def test_a_read_timeout_is_not_retried(sleeps: list[float]) -> None:
    handler, calls = _scripted(httpx.ReadTimeout("read timed out"), _OK)

    with pytest.raises(httpx.ReadTimeout):
        _client(handler).ask(_item(_ARPU_TITLE))

    assert len(calls) == 1
    assert sleeps == []


def test_default_timeout_is_two_minutes() -> None:
    assert CatalogMetadataClient(host="https://h", token="tok", workspace_id="ws")._client.timeout.read == 120.0

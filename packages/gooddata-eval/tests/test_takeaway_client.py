# (C) 2026 GoodData Corporation
import json
from collections.abc import Callable

import httpx
import pytest
from gooddata_eval.core import _retry as retry_mod
from gooddata_eval.core.models import DatasetItem, TakeawayInput
from gooddata_eval.core.takeaway.http_client import TakeawayClient

_TAKEAWAY_RESPONSE = {
    "takeaway": "**Revenue grew 12%.** Driven by the West region.",
    "noData": False,
    "generatedAt": "2026-10-22T10:00:00Z",
    "agentId": "agent-1",
    "contextOmitted": [],
}


def _item(takeaway_input: dict | None) -> DatasetItem:
    return DatasetItem(
        id="t1",
        dataset_name="d",
        test_kind="document_takeaway",
        question="Takeaway for the page",
        expected_output={},
        takeaway_input=TakeawayInput.model_validate(takeaway_input) if takeaway_input is not None else None,
    )


def _client(handler: Callable[[httpx.Request], httpx.Response]) -> TakeawayClient:
    client = TakeawayClient(host="https://h/", token="tok", workspace_id="ws")
    client._client = httpx.Client(transport=httpx.MockTransport(handler))
    return client


def _capturing(captured: dict, response: dict | None = None) -> Callable[[httpx.Request], httpx.Response]:
    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["auth"] = request.headers.get("authorization")
        captured["body"] = json.loads(request.content)
        return httpx.Response(200, json=response or _TAKEAWAY_RESPONSE)

    return handler


def test_body_is_camel_case_and_omits_unset() -> None:
    captured: dict = {}
    client = _client(_capturing(captured))

    result = client.ask(
        _item(
            {
                "visualizations": ["v1"],
                "filter_context": [{"dateFilter": {}}],
                "instructions": {"slot": "page", "format_hint": "one sentence"},
                "max_characters": 1000,
                "agent_id": "agent-1",
            }
        )
    )

    assert captured["url"] == "https://h/api/v1/ai/workspaces/ws/takeaway"
    assert captured["auth"] == "Bearer tok"
    assert captured["body"] == {
        "agentId": "agent-1",
        "instructions": {"slot": "page", "formatHint": "one sentence"},
        "maxCharacters": 1000,
        "data": {"visualizations": ["v1"], "filterContext": [{"dateFilter": {}}]},
    }
    assert result.text_response == "**Revenue grew 12%.** Driven by the West region."


def test_placement_visualization_serialized_with_filters() -> None:
    captured: dict = {}
    client = _client(_capturing(captured))

    client.ask(
        _item(
            {
                "visualizations": [
                    "v1",
                    {"visualization_id": "v2", "filters": [{"positiveAttributeFilter": {}}]},
                    {"visualization_id": "v3"},
                ]
            }
        )
    )

    assert captured["body"] == {
        "data": {
            "visualizations": [
                "v1",
                {"visualizationId": "v2", "filters": [{"positiveAttributeFilter": {}}]},
                {"visualizationId": "v3", "filters": []},
            ],
            "filterContext": [],
        },
    }


def test_instructions_omitted_when_empty() -> None:
    captured: dict = {}
    client = _client(_capturing(captured))

    client.ask(_item({"visualizations": ["v1"], "instructions": {}}))

    assert "instructions" not in captured["body"]
    assert captured["body"]["data"]["filterContext"] == []


def test_no_data_response_kept_as_no_data_not_empty_text() -> None:
    no_data = {**_TAKEAWAY_RESPONSE, "takeaway": None, "noData": True, "contextOmitted": ["v1"]}
    client = _client(_capturing({}, no_data))

    result = client.ask(_item({"visualizations": ["v1"]}))

    assert result.text_response == ""
    assert result.raw_response is not None
    assert result.raw_response["noData"] is True
    assert result.raw_response["takeaway"] is None
    assert result.raw_response["agentId"] == "agent-1"
    assert result.raw_response["contextOmitted"] == ["v1"]


def test_http_error_carries_status_and_body(sleeps: list[float]) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(502, json={"detail": "Visualizations ['v1'] failed to execute."})

    client = _client(handler)

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        client.ask(_item({"visualizations": ["v1"]}))

    assert exc_info.value.response.status_code == 502
    assert "502" in str(exc_info.value)
    assert "failed to execute" in str(exc_info.value)


def test_redirect_is_an_http_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(302, headers={"Location": "https://h/login"}, text="Found")

    client = _client(handler)

    with pytest.raises(httpx.HTTPStatusError, match="302"):
        client.ask(_item({"visualizations": ["v1"]}))


def test_item_without_takeaway_input_names_the_item() -> None:
    client = TakeawayClient(host="https://h", token="tok", workspace_id="ws")

    with pytest.raises(ValueError, match="'t1'.*takeaway_input"):
        client.ask(_item(None))


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


@pytest.mark.parametrize("status", [429, 502, 503, 504])
def test_transient_status_is_retried(status: int, sleeps: list[float]) -> None:
    handler, calls = _scripted(httpx.Response(status, text="busy"), httpx.Response(200, json=_TAKEAWAY_RESPONSE))

    result = _client(handler).ask(_item({"visualizations": ["v1"]}))

    assert result.text_response == _TAKEAWAY_RESPONSE["takeaway"]
    assert len(calls) == 2
    assert sleeps == [5.0]


@pytest.mark.parametrize(
    "error",
    [
        httpx.ConnectError("refused"),
        httpx.ConnectTimeout("connect timed out"),
        httpx.RemoteProtocolError("peer closed connection"),
        httpx.PoolTimeout("pool exhausted"),
    ],
)
def test_transient_transport_error_is_retried(error: httpx.TransportError, sleeps: list[float]) -> None:
    handler, calls = _scripted(error, httpx.Response(200, json=_TAKEAWAY_RESPONSE))

    _client(handler).ask(_item({"visualizations": ["v1"]}))

    assert len(calls) == 2


@pytest.mark.parametrize(
    "error",
    [
        httpx.ReadTimeout("read timed out"),
        httpx.WriteTimeout("write timed out"),
        httpx.UnsupportedProtocol("no scheme"),
    ],
)
def test_slow_or_misconfigured_request_is_not_retried(error: httpx.TransportError, sleeps: list[float]) -> None:
    handler, calls = _scripted(error)

    with pytest.raises(type(error)):
        _client(handler).ask(_item({"visualizations": ["v1"]}))

    assert len(calls) == 1
    assert sleeps == []


def test_transient_status_raises_with_body_once_retries_run_out(sleeps: list[float]) -> None:
    handler, calls = _scripted(*[httpx.Response(502, text="Visualizations failed to execute.")] * 6)

    with pytest.raises(httpx.HTTPStatusError, match="502.*failed to execute") as exc_info:
        _client(handler).ask(_item({"visualizations": ["v1"]}))

    assert exc_info.value.response.status_code == 502
    assert len(calls) == 6


@pytest.mark.parametrize("status", [400, 404, 422])
def test_deterministic_client_error_is_not_retried(status: int, sleeps: list[float]) -> None:
    handler, calls = _scripted(httpx.Response(status, text='{"reason": "NO_AVAILABLE_AGENT"}'))

    with pytest.raises(httpx.HTTPStatusError, match="NO_AVAILABLE_AGENT"):
        _client(handler).ask(_item({"visualizations": ["v1"]}))

    assert len(calls) == 1
    assert sleeps == []


def test_default_timeout_is_two_minutes() -> None:
    assert TakeawayClient(host="https://h", token="tok", workspace_id="ws")._client.timeout.read == 120.0


def test_timeout_is_overridable() -> None:
    assert TakeawayClient(host="https://h", token="tok", workspace_id="ws", timeout=30.0)._client.timeout.read == 30.0

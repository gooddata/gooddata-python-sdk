# (C) 2026 GoodData Corporation
import json

import httpx
import pytest
from gooddata_eval.core.models import DatasetItem, SummaryInput
from gooddata_eval.core.summary.http_client import SummaryClient


def _item() -> DatasetItem:
    return DatasetItem(
        id="s1",
        dataset_name="d",
        test_kind="dashboard_summary",
        question="Summarize the dashboard",
        expected_output={},
        summary_input=SummaryInput(
            dashboard_id="dash1",
            visualizations=["v1", "v2"],
            format_hint="3 bullets",
        ),
    )


def test_summary_client_posts_request_and_maps_summary():
    captured: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["body"] = json.loads(request.content)
        captured["auth"] = request.headers.get("authorization")
        return httpx.Response(200, json={"summary": "Revenue grew QoQ.", "filterContext": []})

    client = SummaryClient(host="https://h", token="tok", workspace_id="ws")
    client._client = httpx.Client(transport=httpx.MockTransport(handler))

    result = client.ask(_item())

    assert result.text_response == "Revenue grew QoQ."
    assert captured["url"] == "https://h/api/v1/ai/workspaces/ws/summary"
    assert captured["auth"] == "Bearer tok"
    assert captured["body"] == {
        "dashboardId": "dash1",
        "visualizations": ["v1", "v2"],
        "formatHint": "3 bullets",
    }


def test_summary_client_omits_unset_optional_fields():
    captured: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["body"] = json.loads(request.content)
        return httpx.Response(200, json={"summary": "ok"})

    client = SummaryClient(host="https://h", token="tok", workspace_id="ws")
    client._client = httpx.Client(transport=httpx.MockTransport(handler))

    item = DatasetItem(
        id="s2",
        dataset_name="d",
        test_kind="dashboard_summary",
        question="q",
        expected_output={},
        summary_input=SummaryInput(dashboard_id="only-dashboard"),
    )
    client.ask(item)
    assert captured["body"] == {"dashboardId": "only-dashboard"}


def test_summary_client_raises_without_summary_input():
    client = SummaryClient(host="https://h", token="tok", workspace_id="ws")
    item = DatasetItem(id="s3", dataset_name="d", test_kind="dashboard_summary", question="q", expected_output={})
    with pytest.raises(ValueError, match="summary_input"):
        client.ask(item)


def test_summary_client_raises_on_http_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"detail": "dashboard not found"})

    client = SummaryClient(host="https://h", token="tok", workspace_id="ws")
    client._client = httpx.Client(transport=httpx.MockTransport(handler))
    with pytest.raises(httpx.HTTPStatusError):
        client.ask(_item())

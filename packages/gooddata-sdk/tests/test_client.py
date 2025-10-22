# (C) 2021 GoodData Corporation
from gooddata_sdk import GoodDataApiClient


def test_http_headers_precedence():
    c = GoodDataApiClient(
        "host",
        "token",
        custom_headers={"User-Agent": "not-this"},
        extra_user_agent="yes",
    )
    agent = c._api_client.default_headers["User-Agent"]
    assert agent.startswith("gooddata")
    assert agent.endswith("yes")

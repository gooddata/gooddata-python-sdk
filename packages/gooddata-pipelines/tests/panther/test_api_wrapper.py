# (C) 2025 GoodData Corporation

import pytest

from gooddata_pipelines.api.gooddata_api import (
    API_VERSION,
    ApiMethods,
)
from gooddata_pipelines.api.gooddata_api_wrapper import GoodDataApi


def test_get_base_url():
    """Test the get_base_url method with various domain inputs."""
    domain = "example.com"
    expected_base_url = f"example.com/api/{API_VERSION}"
    result = ApiMethods._get_base_url(domain)
    assert result == expected_base_url


@pytest.mark.parametrize(
    "host, expected_clean_host",
    [
        ("example.com", "https://example.com"),
        (
            "https://example.com",
            "https://example.com",
        ),
        (
            "http://example.com",
            "https://example.com",
        ),
        ("example.com/", "https://example.com"),
        (
            "https://example.com/",
            "https://example.com",
        ),
        (
            "http://example.com/",
            "https://example.com",
        ),
    ],
)
def test_get_clean_host(host, expected_clean_host):
    result = GoodDataApi._get_clean_host(host)
    assert result == expected_clean_host

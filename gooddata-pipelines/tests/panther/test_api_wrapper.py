# (C) 2025 GoodData Corporation

import pytest

from gooddata_pipelines.api.gooddata_api import (
    API_VERSION,
    ApiMethods,
)


@pytest.mark.parametrize(
    "domain, expected_base_url",
    [
        ("example.com", f"https://example.com/api/{API_VERSION}"),
        (
            "https://example.com",
            f"https://example.com/api/{API_VERSION}",
        ),
        (
            "http://example.com",
            f"https://example.com/api/{API_VERSION}",
        ),
        ("example.com/", f"https://example.com/api/{API_VERSION}"),
        (
            "https://example.com/",
            f"https://example.com/api/{API_VERSION}",
        ),
        (
            "http://example.com/",
            f"https://example.com/api/{API_VERSION}",
        ),
    ],
)
def test_get_base_url(domain, expected_base_url):
    """Test the get_base_url method with various domain inputs."""
    result = ApiMethods._get_base_url(domain)
    assert result == expected_base_url

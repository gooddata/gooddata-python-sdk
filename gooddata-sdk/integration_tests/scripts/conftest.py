# (C) 2024 GoodData Corporation

import os
import sys

import pytest
from env import HOST, TOKEN
from gooddata_api_client import ApiClient, Configuration

# Add the root directory to the Python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)


@pytest.fixture(scope="session", autouse=True)
def set_authorization_header():
    """
    Fixture to set the Authorization header globally for all tests.
    """
    configuration = Configuration(host=HOST)
    configuration.access_token = TOKEN
    api_client = ApiClient(configuration)
    api_client.default_headers["Authorization"] = f"Bearer {TOKEN}"
    yield api_client
    # Cleanup after the tests, if necessary (e.g., closing client)
    api_client.close()

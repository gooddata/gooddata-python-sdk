# (C) 2024 GoodData Corporation
# filepath: /Users/tubui/Documents/CODE/gooddata-python-sdk-1/gooddata-sdk/integration_tests/scripts/conftest.py
import os

import pytest
from dotenv import load_dotenv

# Load the .env file from the current directory
load_dotenv()


@pytest.fixture(scope="session", autouse=True)
def setup_env():
    # Ensure that the environment variables are set
    os.environ["HOST"] = os.getenv("HOST", "https://checklist.staging.stg11.panther.intgdc.com")
    os.environ["TOKEN"] = os.getenv("TOKEN", "")
    os.environ["DATASOURCE_ID"] = os.getenv("DATASOURCE_ID", "")
    os.environ["WORKSPACE_ID"] = os.getenv("WORKSPACE_ID", "")
    os.environ["DATASOURCE_TYPE"] = os.getenv("DATASOURCE_TYPE", "")
    os.environ["DATASOURCE_PASSWORD"] = os.getenv("DATASOURCE_PASSWORD", "")

    # Check if the necessary environment variables are set
    if not os.environ["HOST"]:
        raise OSError("\nHOST environment variable is not set.")
    if not os.environ["TOKEN"]:
        raise OSError("\nTOKEN environment variable is not set.")
    if not os.environ["DATASOURCE_ID"]:
        print("\nWarning: DATA_SOURCE_ID environment variable is not set.")
    if not os.environ["WORKSPACE_ID"]:
        print("\nWarning: WORKSPACE_ID environment variable is not set.")
    if not os.environ["DATASOURCE_TYPE"]:
        print("\nWarning: DATASOURCE_TYPE environment variable is not set.")
    if not os.environ["DATASOURCE_PASSWORD"]:
        print("\nWarning: DATASOURCE_PASSWORD environment variable is not set.")

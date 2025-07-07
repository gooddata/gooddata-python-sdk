# (C) 2025 GoodData Corporation
import os
from typing import Generator

import boto3
import pytest

from gooddata_pipelines.api import GoodDataAPI


@pytest.fixture(scope="session", autouse=True)
def aws_credentials() -> Generator[None, None, None]:
    """
    Set dummy AWS credentials for the entire test session.
    This is an autouse fixture, so it runs automatically.
    """
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    yield


@pytest.fixture
def mock_boto_session(mocker):
    """
    Mocks boto3.Session to prevent it from using a real AWS profile.
    It will return a default Session object, which then uses the
    dummy credentials set by the conftest.py fixture.
    """
    # We patch boto3.Session and make it return a new, default session object.
    # This new object will not have the `profile_name` and will fall back
    # to using the environment variables we set in conftest.
    mocker.patch("boto3.Session", return_value=boto3.Session())


@pytest.fixture
def mock_gooddata_api():
    return GoodDataAPI("domain", "token")


@pytest.fixture
def mock_logger():
    class MockLogger:
        def info(self, msg: str) -> None:
            print(msg)

        def warning(self, msg: str) -> None:
            print(msg)

        def error(self, msg: str) -> None:
            print(msg)

    return MockLogger()

# (C) 2025 GoodData Corporation

from pathlib import Path
from unittest.mock import Mock

import boto3
import pytest
from moto import mock_aws
from pytest_mock import MockerFixture

from gooddata_pipelines import (
    PermissionProvisioner,
    UserDataFilterProvisioner,
    UserGroupProvisioner,
    UserProvisioner,
    WorkspaceProvisioner,
)
from gooddata_pipelines.api import GoodDataApi

TEST_DATA_DIR = str((Path(__file__).parent / "data").absolute())


@pytest.fixture(scope="function", autouse=True)
def mock_aws_services():
    """Mock AWS services for each test"""
    with mock_aws():
        yield


@pytest.fixture(scope="function")
def mock_boto_session():
    """Create a mock boto3 session for testing"""
    return boto3.Session(
        aws_access_key_id="testing",
        aws_secret_access_key="testing",
        aws_session_token="testing",
        region_name="us-east-1",
    )


@pytest.fixture(scope="function", autouse=True)
def mock_boto3_session(monkeypatch):
    """Mock boto3.Session to prevent real AWS authentication"""
    mock_client = Mock()
    mock_client.head_bucket.return_value = {}

    mock_resource = Mock()
    mock_resource.meta.client = mock_client
    mock_resource.Bucket.return_value = Mock()

    mock_session = Mock()
    mock_session.resource.return_value = mock_resource

    # Mock the boto3.Session constructor
    def mock_session_constructor(*args, **kwargs):
        return mock_session

    monkeypatch.setattr("boto3.Session", mock_session_constructor)
    return mock_session


@pytest.fixture
def mock_gooddata_api():
    return GoodDataApi("domain", "token")


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


@pytest.fixture
def workspace_provisioner(mocker: MockerFixture):
    provisioner_instance = WorkspaceProvisioner.create("host", "token")

    # Patch the API
    mocker.patch.object(provisioner_instance, "_api", return_value=None)

    return provisioner_instance


@pytest.fixture
def user_provisioner(mocker: MockerFixture):
    provisioner_instance = UserProvisioner.create("host", "token")

    # Patch the API
    mocker.patch.object(provisioner_instance, "_api", return_value=None)

    return UserProvisioner.create("host", "token")


@pytest.fixture
def user_group_provisioner(mocker: MockerFixture):
    provisioner_instance = UserGroupProvisioner.create("host", "token")

    # Patch the API
    mocker.patch.object(provisioner_instance, "_api", return_value=None)

    return provisioner_instance


@pytest.fixture
def permission_provisioner(mocker: MockerFixture) -> PermissionProvisioner:
    provisioner_instance = PermissionProvisioner.create("host", "token")

    # Patch the API
    mocker.patch.object(provisioner_instance, "_api", return_value=None)

    return provisioner_instance


@pytest.fixture
def user_data_filter_provisioner(mocker: MockerFixture):
    provisioner_instance = UserDataFilterProvisioner.create("host", "token")

    # Patch the API
    mocker.patch.object(provisioner_instance, "_api", return_value=None)

    return provisioner_instance

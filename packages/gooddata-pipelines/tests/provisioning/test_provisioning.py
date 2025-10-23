# (C) 2025 GoodData Corporation
import os
from pathlib import Path

import pytest
from pydantic import BaseModel, ValidationError

from gooddata_pipelines import (
    EntityType,
    PermissionFullLoad,
    PermissionIncrementalLoad,
    UserDataFilterFullLoad,
    UserFullLoad,
    UserGroupFullLoad,
    UserGroupIncrementalLoad,
    UserIncrementalLoad,
    WorkspaceFullLoad,
)
from gooddata_pipelines.provisioning.entities.workspaces.models import (
    WorkspaceIncrementalLoad,
)
from gooddata_pipelines.provisioning.provisioning import Provisioning
from tests.conftest import TEST_DATA_DIR

WORKSPACE_DATA_TO_FAIL = [
    WorkspaceFullLoad(
        parent_id="client_id1",
        workspace_id="workspace_id1",
        workspace_name="workspace_title1",
    ),
    WorkspaceIncrementalLoad(  # type: ignore
        parent_id="client_id1",
        workspace_id="workspace_id1",
        workspace_name="workspace_title1",
        is_active=True,
    ),
]
USER_DATA_TO_FAIL = [
    UserFullLoad(
        user_id="user_id1",
        firstname="user_name1",
        lastname="user_name1",
        email="user_email1",
        auth_id="auth_id1",
        user_groups=["user_group_id1"],
    ),
    UserIncrementalLoad(
        user_id="user_id1",
        firstname="user_name1",
        lastname="user_name1",
        email="user_email1",
        auth_id="auth_id1",
        user_groups=["user_group_id1"],
        is_active=True,
    ),
]

USER_GROUP_DATA_TO_FAIL = [
    UserGroupFullLoad(
        user_group_id="user_group_id1",
        user_group_name="user_group_name1",
    ),
    UserGroupIncrementalLoad(
        user_group_id="user_group_id1",
        user_group_name="user_group_name1",
        is_active=True,
    ),
]

PERMISSION_DATA_TO_FAIL = [
    PermissionFullLoad(
        permission="permission_id1",
        workspace_id="workspace_id1",
        entity_id="entity_id1",
        entity_type=EntityType.user,
    ),
    PermissionIncrementalLoad(
        permission="permission_id1",
        workspace_id="workspace_id1",
        entity_id="entity_id1",
        entity_type=EntityType.user,
        is_active=True,
    ),
]


TEST_CASES = [
    ("workspace_provisioner", WORKSPACE_DATA_TO_FAIL),
    ("user_provisioner", USER_DATA_TO_FAIL),
    ("user_group_provisioner", USER_GROUP_DATA_TO_FAIL),
    ("permission_provisioner", PERMISSION_DATA_TO_FAIL),
]


@pytest.mark.parametrize(
    "provisioner_name, data_to_fail",
    TEST_CASES,
)
def test_fail_type_validation(
    request: pytest.FixtureRequest, provisioner_name: str, data_to_fail: list
) -> None:
    """Data type validation of source data should fail when input data is not
    all of the same type."""
    provisioner = request.getfixturevalue(provisioner_name)
    with pytest.raises(TypeError) as e:
        provisioner._validate_source_data_type(
            data_to_fail,
            WorkspaceFullLoad,
        )

        assert "Not all elements in source data are instances of" in str(e)


def test_create_from_profile() -> None:
    """Test creating a provisioner from a profile."""

    os.environ["MOCK_TOKEN"] = "some_user_token"
    provisioner: Provisioning = Provisioning.create_from_profile(
        profile="mock_profile",
        profiles_path=Path(f"{TEST_DATA_DIR}/profiles.yaml"),
    )
    assert provisioner._api._domain == "http://localhost:3000"
    assert provisioner._api._token == os.environ.pop("MOCK_TOKEN")


MODELS_AND_VALID_DATA = [
    (
        WorkspaceFullLoad,
        {
            "parent_id": "parent_id",
            "workspace_id": "workspace_id",
            "workspace_name": "workspace_name",
        },
    ),
    (
        WorkspaceIncrementalLoad,
        {
            "parent_id": "parent_id",
            "workspace_id": "workspace_id",
            "workspace_name": "workspace_name",
            "is_active": True,
        },
    ),
    (
        UserFullLoad,
        {
            "user_id": "user_id",
            "firstname": "firstname",
            "lastname": "lastname",
            "email": "email",
            "auth_id": "auth_id",
            "user_groups": ["user_group_id"],
        },
    ),
    (
        UserIncrementalLoad,
        {
            "user_id": "user_id",
            "firstname": "firstname",
            "lastname": "lastname",
            "email": "email",
            "auth_id": "auth_id",
            "user_groups": ["user_group_id"],
            "is_active": True,
        },
    ),
    (
        UserGroupFullLoad,
        {
            "user_group_id": "user_group_id",
            "user_group_name": "user_group_name",
        },
    ),
    (
        UserGroupIncrementalLoad,
        {
            "user_group_id": "user_group_id",
            "user_group_name": "user_group_name",
            "is_active": True,
        },
    ),
    (
        PermissionFullLoad,
        {
            "permission": "permission",
            "workspace_id": "workspace_id",
            "entity_id": "entity_id",
            "entity_type": EntityType.user,
        },
    ),
    (
        PermissionIncrementalLoad,
        {
            "permission": "permission",
            "workspace_id": "workspace_id",
            "entity_id": "entity_id",
            "entity_type": EntityType.user,
            "is_active": True,
        },
    ),
    (
        UserDataFilterFullLoad,
        {
            "workspace_id": "workspace_id",
            "udf_id": "udf_id",
            "udf_value": "udf_value",
        },
    ),
]


@pytest.mark.parametrize(["provisioning_model", "data"], MODELS_AND_VALID_DATA)
def test_validate_valid_data(provisioning_model: BaseModel, data: dict) -> None:
    """Test validating valid data."""
    provisioning_model.model_validate(data)


@pytest.mark.parametrize(
    ["provisioning_model", "data"],
    MODELS_AND_VALID_DATA,
)
def test_raise_extra_fields(provisioning_model: BaseModel, data: dict) -> None:
    """Test raising an error when extra fields are provided."""
    data["extra_field"] = "extra_field"
    with pytest.raises(ValidationError):
        provisioning_model.model_validate(data)

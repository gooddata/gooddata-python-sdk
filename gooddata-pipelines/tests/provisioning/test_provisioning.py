# (C) 2025 GoodData Corporation
import pytest

from gooddata_pipelines import (
    EntityType,
    PermissionFullLoad,
    PermissionIncrementalLoad,
    UserFullLoad,
    UserGroupFullLoad,
    UserGroupIncrementalLoad,
    UserIncrementalLoad,
    WorkspaceFullLoad,
)
from gooddata_pipelines.provisioning.entities.workspaces.models import (
    WorkspaceIncrementalLoad,
)

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

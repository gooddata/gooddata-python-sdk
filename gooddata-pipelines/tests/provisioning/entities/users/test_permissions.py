# (C) 2025 GoodData Corporation
import json
from typing import Literal

import pytest
from gooddata_api_client.exceptions import (  # type: ignore[import]
    NotFoundException,
)
from gooddata_sdk.catalog.identifier import CatalogAssigneeIdentifier
from gooddata_sdk.catalog.permission.declarative_model.permission import (
    CatalogDeclarativeSingleWorkspacePermission,
    CatalogDeclarativeWorkspacePermissions,
)
from pytest_mock import MockerFixture

from gooddata_pipelines.provisioning.entities.users.models.permissions import (
    PermissionDeclaration,
    PermissionFullLoad,
    PermissionIncrementalLoad,
)
from gooddata_pipelines.provisioning.entities.users.permissions import (
    PermissionProvisioner,
)
from tests.conftest import TEST_DATA_DIR

TEST_DATA_SUBDIR = f"{TEST_DATA_DIR}/provisioning/entities/permissions"

USER_1 = CatalogAssigneeIdentifier(id="user_1", type="user")
USER_2 = CatalogAssigneeIdentifier(id="user_2", type="user")
USER_3 = CatalogAssigneeIdentifier(id="user_3", type="user")
UG_1 = CatalogAssigneeIdentifier(id="ug_1", type="userGroup")
UG_2 = CatalogAssigneeIdentifier(id="ug_2", type="userGroup")
UG_3 = CatalogAssigneeIdentifier(id="ug_3", type="userGroup")

UPSTREAM_PERMISSIONS = [
    CatalogDeclarativeSingleWorkspacePermission(
        name="ANALYZE", assignee=USER_1
    ),
    CatalogDeclarativeSingleWorkspacePermission(name="VIEW", assignee=USER_1),
    CatalogDeclarativeSingleWorkspacePermission(name="MANAGE", assignee=USER_1),
    CatalogDeclarativeSingleWorkspacePermission(
        name="ANALYZE", assignee=USER_2
    ),
    CatalogDeclarativeSingleWorkspacePermission(name="VIEW", assignee=USER_2),
    CatalogDeclarativeSingleWorkspacePermission(
        name="ANALYZE", assignee=USER_3
    ),
    CatalogDeclarativeSingleWorkspacePermission(name="ANALYZE", assignee=UG_1),
    CatalogDeclarativeSingleWorkspacePermission(name="VIEW", assignee=UG_1),
    CatalogDeclarativeSingleWorkspacePermission(name="MANAGE", assignee=UG_1),
    CatalogDeclarativeSingleWorkspacePermission(name="ANALYZE", assignee=UG_2),
    CatalogDeclarativeSingleWorkspacePermission(name="VIEW", assignee=UG_2),
    CatalogDeclarativeSingleWorkspacePermission(name="ANALYZE", assignee=UG_3),
]

WS_PERMISSION_DECLARATION = PermissionDeclaration(
    users={
        "user_1": {"ANALYZE": True, "VIEW": True, "MANAGE": True},
        "user_2": {"ANALYZE": True, "VIEW": True},
        "user_3": {"ANALYZE": True},
    },
    user_groups={
        "ug_1": {"ANALYZE": True, "VIEW": True, "MANAGE": True},
        "ug_2": {"ANALYZE": True, "VIEW": True},
        "ug_3": {"ANALYZE": True},
    },
)

UPSTREAM_WS_PERMISSION = CatalogDeclarativeWorkspacePermissions(
    permissions=UPSTREAM_PERMISSIONS
)

UPSTREAM_WS_PERMISSIONS = {
    "ws_id_1": UPSTREAM_WS_PERMISSION,
    "ws_id_2": UPSTREAM_WS_PERMISSION,
}


def test_declaration_from_populated_sdk_api_obj():
    declaration = PermissionDeclaration.from_sdk_api(UPSTREAM_WS_PERMISSION)
    assert declaration == WS_PERMISSION_DECLARATION


def test_declaration_from_empty_sdk_api_obj():
    api_obj = CatalogDeclarativeWorkspacePermissions(permissions=[])
    declaration = PermissionDeclaration.from_sdk_api(api_obj)
    assert len(declaration.users) == 0
    assert len(declaration.user_groups) == 0


def test_declaration_to_populated_sdk_api_obj():
    api_obj = PermissionDeclaration.to_sdk_api(WS_PERMISSION_DECLARATION)
    assert api_obj == UPSTREAM_WS_PERMISSION


def test_declaration_with_inactive_to_sdk_api_obj():
    users = {
        "user_1": {"ANALYZE": True, "VIEW": False},
        "user_2": {"ANALYZE": True},
    }
    ugs = {
        "ug_1": {"ANALYZE": True, "VIEW": False},
        "ug_2": {"ANALYZE": True},
    }
    declaration = PermissionDeclaration(users, ugs)
    api_obj = declaration.to_sdk_api()
    expected = CatalogDeclarativeWorkspacePermissions(
        permissions=[
            CatalogDeclarativeSingleWorkspacePermission(
                name="ANALYZE", assignee=USER_1
            ),
            CatalogDeclarativeSingleWorkspacePermission(
                name="ANALYZE", assignee=USER_2
            ),
            CatalogDeclarativeSingleWorkspacePermission(
                name="ANALYZE", assignee=UG_1
            ),
            CatalogDeclarativeSingleWorkspacePermission(
                name="ANALYZE", assignee=UG_2
            ),
        ]
    )
    assert api_obj == expected


def test_declaration_with_only_inactive_to_sdk_api_obj():
    users = {
        "user_1": {"ANALYZE": False, "VIEW": False},
        "user_2": {"ANALYZE": False},
    }
    ugs = {
        "ug_1": {"ANALYZE": False, "VIEW": False},
        "ug_2": {"ANALYZE": False},
    }
    declaration = PermissionDeclaration(users, ugs)
    api_obj = declaration.to_sdk_api()
    expected = CatalogDeclarativeWorkspacePermissions(permissions=[])
    assert api_obj == expected


# Declarations are explicitly defined anew here to avoid dict mutations
# in subsequent calls and to avoid dict deepcopy overhead.


def test_add_new_active_user_perm() -> None:
    declaration = PermissionDeclaration(
        {"user_1": {"ANALYZE": True, "VIEW": False}},
        {"ug_1": {"VIEW": True, "ANALYZE": False}},
    )
    permission = PermissionIncrementalLoad.from_dict(
        {
            "ws_id": "",
            "ws_permissions": "MANAGE",
            "ug_id": "",
            "user_id": "user_1",
            "is_active": True,
        }
    )
    declaration.add_incremental_permission(permission)
    assert declaration.users == {
        "user_1": {"ANALYZE": True, "VIEW": False, "MANAGE": True}
    }
    assert declaration.user_groups == {"ug_1": {"VIEW": True, "ANALYZE": False}}


def test_add_new_inactive_user_perm() -> None:
    declaration = PermissionDeclaration(
        {"user_1": {"ANALYZE": True, "VIEW": False}},
        {"ug_1": {"VIEW": True, "ANALYZE": False}},
    )
    permission = PermissionIncrementalLoad.from_dict(
        {
            "ws_id": "",
            "ws_permissions": "MANAGE",
            "ug_id": "",
            "user_id": "user_1",
            "is_active": False,
        }
    )

    declaration.add_incremental_permission(permission)
    assert declaration.users == {
        "user_1": {"ANALYZE": True, "VIEW": False, "MANAGE": False}
    }
    assert declaration.user_groups == {"ug_1": {"VIEW": True, "ANALYZE": False}}


def test_overwrite_inactive_user_perm() -> None:
    declaration = PermissionDeclaration(
        {"user_1": {"ANALYZE": True, "VIEW": False}},
        {"ug_1": {"VIEW": True, "ANALYZE": False}},
    )
    permission = PermissionIncrementalLoad.from_dict(
        {
            "ws_id": "",
            "ws_permissions": "VIEW",
            "ug_id": "",
            "user_id": "user_1",
            "is_active": True,
        }
    )
    declaration.add_incremental_permission(permission)
    assert declaration.users == {"user_1": {"ANALYZE": True, "VIEW": True}}
    assert declaration.user_groups == {"ug_1": {"VIEW": True, "ANALYZE": False}}


def test_overwrite_active_user_perm() -> None:
    declaration = PermissionDeclaration(
        {"user_1": {"ANALYZE": True, "VIEW": False}},
        {"ug_1": {"VIEW": True, "ANALYZE": False}},
    )
    permission = PermissionIncrementalLoad.from_dict(
        {
            "ws_id": "",
            "ws_permissions": "ANALYZE",
            "ug_id": "",
            "user_id": "user_1",
            "is_active": False,
        }
    )
    declaration.add_incremental_permission(permission)
    assert declaration.users == {"user_1": {"ANALYZE": True, "VIEW": False}}
    assert declaration.user_groups == {"ug_1": {"VIEW": True, "ANALYZE": False}}


def test_add_new_user_perm() -> None:
    declaration = PermissionDeclaration(
        {"user_1": {"ANALYZE": True, "VIEW": False}},
        {"ug_1": {"VIEW": True, "ANALYZE": False}},
    )
    permission = PermissionIncrementalLoad.from_dict(
        {
            "ws_id": "",
            "ws_permissions": "VIEW",
            "ug_id": "",
            "user_id": "user_2",
            "is_active": True,
        }
    )
    declaration.add_incremental_permission(permission)
    assert declaration.users == {
        "user_1": {"ANALYZE": True, "VIEW": False},
        "user_2": {"VIEW": True},
    }
    assert declaration.user_groups == {"ug_1": {"VIEW": True, "ANALYZE": False}}


def test_modify_one_of_user_perms() -> None:
    declaration = PermissionDeclaration(
        {"user_1": {"ANALYZE": True, "VIEW": False}, "user_2": {"VIEW": True}},
        {"ug_1": {"VIEW": True, "ANALYZE": False}},
    )
    permission = PermissionIncrementalLoad.from_dict(
        {
            "ws_id": "",
            "ws_permissions": "MANAGE",
            "ug_id": "",
            "user_id": "user_1",
            "is_active": True,
        }
    )
    declaration.add_incremental_permission(permission)
    assert declaration.users == {
        "user_1": {"ANALYZE": True, "VIEW": False, "MANAGE": True},
        "user_2": {"VIEW": True},
    }
    assert declaration.user_groups == {"ug_1": {"VIEW": True, "ANALYZE": False}}


# Add userGroup permission


def test_add_new_active_ug_perm() -> None:
    declaration = PermissionDeclaration(
        {"user_1": {"ANALYZE": True, "VIEW": False}},
        {"ug_1": {"VIEW": True, "ANALYZE": False}},
    )
    permission = PermissionIncrementalLoad.from_dict(
        {
            "ws_id": "",
            "ws_permissions": "MANAGE",
            "ug_id": "ug_1",
            "user_id": "",
            "is_active": True,
        }
    )
    declaration.add_incremental_permission(permission)
    assert declaration.users == {"user_1": {"ANALYZE": True, "VIEW": False}}
    assert declaration.user_groups == {
        "ug_1": {"VIEW": True, "ANALYZE": False, "MANAGE": True}
    }


def test_add_new_inactive_ug_perm() -> None:
    declaration = PermissionDeclaration(
        {"user_1": {"ANALYZE": True, "VIEW": False}},
        {"ug_1": {"VIEW": True, "ANALYZE": False}},
    )
    permission = PermissionIncrementalLoad.from_dict(
        {
            "ws_id": "",
            "ws_permissions": "MANAGE",
            "ug_id": "ug_1",
            "user_id": "",
            "is_active": False,
        }
    )
    declaration.add_incremental_permission(permission)
    assert declaration.users == {"user_1": {"ANALYZE": True, "VIEW": False}}
    assert declaration.user_groups == {
        "ug_1": {"VIEW": True, "ANALYZE": False, "MANAGE": False}
    }


def test_overwrite_inactive_ug_perm() -> None:
    declaration = PermissionDeclaration(
        {"user_1": {"ANALYZE": True, "VIEW": False}},
        {"ug_1": {"VIEW": True, "ANALYZE": False}},
    )
    permission = PermissionIncrementalLoad.from_dict(
        {
            "ws_id": "",
            "ws_permissions": "ANALYZE",
            "ug_id": "ug_1",
            "user_id": "",
            "is_active": True,
        }
    )
    declaration.add_incremental_permission(permission)
    assert declaration.users == {"user_1": {"ANALYZE": True, "VIEW": False}}
    assert declaration.user_groups == {"ug_1": {"VIEW": True, "ANALYZE": True}}


def test_overwrite_active_ug_perm() -> None:
    declaration = PermissionDeclaration(
        {"user_1": {"ANALYZE": True, "VIEW": False}},
        {"ug_1": {"VIEW": True, "ANALYZE": False}},
    )
    permission = PermissionIncrementalLoad.from_dict(
        {
            "ws_id": "",
            "ws_permissions": "VIEW",
            "ug_id": "ug_1",
            "user_id": "",
            "is_active": False,
        }
    )
    declaration.add_incremental_permission(permission)
    assert declaration.users == {"user_1": {"ANALYZE": True, "VIEW": False}}
    assert declaration.user_groups == {"ug_1": {"VIEW": True, "ANALYZE": False}}


def test_add_new_ug_perm() -> None:
    declaration = PermissionDeclaration(
        {"user_1": {"ANALYZE": True, "VIEW": False}},
        {"ug_1": {"VIEW": True, "ANALYZE": False}},
    )
    permission = PermissionIncrementalLoad.from_dict(
        {
            "ws_id": "",
            "ws_permissions": "VIEW",
            "ug_id": "ug_2",
            "user_id": "",
            "is_active": True,
        }
    )
    declaration.add_incremental_permission(permission)
    assert declaration.users == {"user_1": {"ANALYZE": True, "VIEW": False}}
    assert declaration.user_groups == {
        "ug_1": {"VIEW": True, "ANALYZE": False},
        "ug_2": {"VIEW": True},
    }


def test_modify_one_of_ug_perms() -> None:
    declaration = PermissionDeclaration(
        {"user_1": {"ANALYZE": True, "VIEW": False}},
        {"ug_1": {"VIEW": True, "ANALYZE": False}, "ug_2": {"VIEW": True}},
    )
    permission = PermissionIncrementalLoad.from_dict(
        {
            "ws_id": "",
            "ws_permissions": "MANAGE",
            "ug_id": "ug_1",
            "user_id": "",
            "is_active": True,
        }
    )
    declaration.add_incremental_permission(permission)
    assert declaration.users == {"user_1": {"ANALYZE": True, "VIEW": False}}
    assert declaration.user_groups == {
        "ug_1": {"VIEW": True, "ANALYZE": False, "MANAGE": True},
        "ug_2": {"VIEW": True},
    }


def test_upsert() -> None:
    owner = PermissionDeclaration(
        {"user_1": {"ANALYZE": True}, "user_2": {"VIEW": True}},
        {"ug_1": {"ANALYZE": True}, "ug_2": {"VIEW": True}},
    )
    other = PermissionDeclaration(
        {"user_1": {"MANAGE": True, "VIEW": False}},
        {"ug_2": {"MANAGE": True, "VIEW": False}},
    )
    owner.upsert(other)
    assert owner.users == {
        "user_1": {"MANAGE": True, "VIEW": False},
        "user_2": {"VIEW": True},
    }
    assert owner.user_groups == {
        "ug_1": {"ANALYZE": True},
        "ug_2": {"MANAGE": True, "VIEW": False},
    }


def mock_upstream_perms(ws_id: str) -> CatalogDeclarativeWorkspacePermissions:
    if ws_id not in UPSTREAM_WS_PERMISSIONS:
        raise NotFoundException(404)
    return UPSTREAM_WS_PERMISSIONS[ws_id]


@pytest.fixture
def permission_provisioner(mocker: MockerFixture) -> PermissionProvisioner:
    provisioner_instance = PermissionProvisioner.create(
        host="https://localhost:3000", token="token"
    )

    # Patch the API
    mocker.patch.object(provisioner_instance, "_api", return_value=None)

    return provisioner_instance


def parse_expected_permissions(
    raw_data: dict,
) -> dict[str, list[CatalogDeclarativeSingleWorkspacePermission]]:
    expected_result: dict[
        str, list[CatalogDeclarativeSingleWorkspacePermission]
    ] = {}
    for workspace_id, workspace_permissions in raw_data.items():
        expected_permissions = []
        for permission in workspace_permissions:
            expected_permissions.append(
                CatalogDeclarativeSingleWorkspacePermission(
                    name=permission["name"],
                    assignee=CatalogAssigneeIdentifier(
                        id=permission["assignee_id"],
                        type=permission["assignee_type"],
                    ),
                )
            )
        expected_result[workspace_id] = expected_permissions
    return expected_result


@pytest.mark.parametrize(
    ("source_data_path", "expected_data_path", "load_method"),
    [
        (
            "permissions_input_full_load.json",
            "permissions_expected_full_load.json",
            "full_load",
        ),
        (
            "permissions_input_incremental_load.json",
            "permissions_expected_incremental_load.json",
            "incremental_load",
        ),
    ],
)
def test_permission_provisioner(
    source_data_path: str,
    expected_data_path: str,
    load_method: Literal["incremental_load", "full_load"],
    permission_provisioner: PermissionProvisioner,
    mocker: MockerFixture,
) -> None:
    source_data: list[dict] = []
    incremental_load_data: list[PermissionIncrementalLoad] = []
    full_load_data: list[PermissionFullLoad] = []

    # Load existing upstream permissions
    EXISTING_UPSTREAM_PERMISSIONS_PATH = (
        f"{TEST_DATA_SUBDIR}/existing_upstream_permissions.json"
    )
    with open(EXISTING_UPSTREAM_PERMISSIONS_PATH, "r") as f:
        raw_existing_upstream_permissions = json.load(f)

    existing_upstream_permissions = parse_expected_permissions(
        raw_existing_upstream_permissions
    )

    def mock_get_declarative_permissions(
        ws_id: str,
    ) -> CatalogDeclarativeWorkspacePermissions:
        return CatalogDeclarativeWorkspacePermissions(
            permissions=existing_upstream_permissions[ws_id]
        )

    # Patch the get method to return existing upstream permissions
    mocker.patch.object(
        permission_provisioner._api,
        "get_declarative_permissions",
        side_effect=mock_get_declarative_permissions,
    )

    # Load source data
    with open(f"{TEST_DATA_SUBDIR}/{source_data_path}", "r") as f:
        source_data = json.load(f)

    # Load and parse expected data
    with open(f"{TEST_DATA_SUBDIR}/{expected_data_path}", "r") as f:
        raw_expected_result = json.load(f)

    expected_result = parse_expected_permissions(raw_expected_result)

    # Patch the put method to capture output and compare it with expected result
    def compare_permissions(
        workspace_id: str,
        ws_permissions: CatalogDeclarativeWorkspacePermissions,
    ) -> None:
        actual_permissions = ws_permissions.permissions
        expected_permissions = expected_result[workspace_id]

        assert len(actual_permissions) == len(expected_permissions)

        actual_sorted_permissions = sorted(
            actual_permissions, key=lambda x: x.assignee.id
        )
        expected_sorted_permissions = sorted(
            expected_permissions, key=lambda x: x.assignee.id
        )
        assert actual_sorted_permissions == expected_sorted_permissions

    mocker.patch.object(
        permission_provisioner._api,
        "put_declarative_permissions",
        side_effect=compare_permissions,
    )

    if load_method == "incremental_load":
        incremental_load_data = PermissionIncrementalLoad.from_list_of_dicts(
            source_data
        )
        permission_provisioner.incremental_load(incremental_load_data)
    else:
        full_load_data = PermissionFullLoad.from_list_of_dicts(source_data)
        permission_provisioner.full_load(full_load_data)

# (C) 2025 GoodData Corporation

from gooddata_api_client.exceptions import (  # type: ignore[import]
    NotFoundException,
)
from gooddata_sdk.catalog.identifier import CatalogAssigneeIdentifier
from gooddata_sdk.catalog.permission.declarative_model.permission import (
    CatalogDeclarativeSingleWorkspacePermission,
    CatalogDeclarativeWorkspacePermissions,
)

from gooddata_pipelines.provisioning.entities.users.models.permissions import (
    PermissionDeclaration,
    PermissionIncrementalLoad,
    PermissionType,
)

TEST_CSV_PATH = "tests/data/permission_mgmt/input.csv"

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

EXPECTED_WS1_PERMISSIONS = CatalogDeclarativeWorkspacePermissions(
    permissions=[
        CatalogDeclarativeSingleWorkspacePermission(
            name="ANALYZE", assignee=USER_1
        ),
        CatalogDeclarativeSingleWorkspacePermission(
            name="VIEW", assignee=USER_1
        ),
        CatalogDeclarativeSingleWorkspacePermission(
            name="ANALYZE", assignee=USER_2
        ),
        CatalogDeclarativeSingleWorkspacePermission(
            name="MANAGE", assignee=USER_2
        ),
        CatalogDeclarativeSingleWorkspacePermission(
            name="ANALYZE", assignee=USER_3
        ),
        CatalogDeclarativeSingleWorkspacePermission(
            name="ANALYZE", assignee=UG_1
        ),
        CatalogDeclarativeSingleWorkspacePermission(name="VIEW", assignee=UG_1),
        CatalogDeclarativeSingleWorkspacePermission(
            name="ANALYZE", assignee=UG_2
        ),
        CatalogDeclarativeSingleWorkspacePermission(
            name="MANAGE", assignee=UG_2
        ),
        CatalogDeclarativeSingleWorkspacePermission(
            name="ANALYZE", assignee=UG_3
        ),
    ]
)

EXPECTED_WS2_PERMISSIONS = CatalogDeclarativeWorkspacePermissions(
    permissions=[
        CatalogDeclarativeSingleWorkspacePermission(
            name="MANAGE", assignee=USER_1
        ),
        CatalogDeclarativeSingleWorkspacePermission(
            name="MANAGE", assignee=USER_3
        ),
        CatalogDeclarativeSingleWorkspacePermission(
            name="MANAGE", assignee=UG_1
        ),
        CatalogDeclarativeSingleWorkspacePermission(
            name="MANAGE", assignee=UG_3
        ),
    ]
)


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


def test_add_new_active_user_perm():
    declaration = PermissionDeclaration(
        {"user_1": {"ANALYZE": True, "VIEW": False}},
        {"ug_1": {"VIEW": True, "ANALYZE": False}},
    )
    permission = PermissionIncrementalLoad(
        "MANAGE", "", "user_1", PermissionType.user, True
    )
    declaration.add_permission(permission)
    assert declaration.users == {
        "user_1": {"ANALYZE": True, "VIEW": False, "MANAGE": True}
    }
    assert declaration.user_groups == {"ug_1": {"VIEW": True, "ANALYZE": False}}


def test_add_new_inactive_user_perm():
    declaration = PermissionDeclaration(
        {"user_1": {"ANALYZE": True, "VIEW": False}},
        {"ug_1": {"VIEW": True, "ANALYZE": False}},
    )
    permission = PermissionIncrementalLoad(
        "MANAGE", "", "user_1", PermissionType.user, False
    )
    declaration.add_permission(permission)
    assert declaration.users == {
        "user_1": {"ANALYZE": True, "VIEW": False, "MANAGE": False}
    }
    assert declaration.user_groups == {"ug_1": {"VIEW": True, "ANALYZE": False}}


def test_overwrite_inactive_user_perm():
    declaration = PermissionDeclaration(
        {"user_1": {"ANALYZE": True, "VIEW": False}},
        {"ug_1": {"VIEW": True, "ANALYZE": False}},
    )
    permission = PermissionIncrementalLoad(
        "VIEW", "", "user_1", PermissionType.user, True
    )
    declaration.add_permission(permission)
    assert declaration.users == {"user_1": {"ANALYZE": True, "VIEW": True}}
    assert declaration.user_groups == {"ug_1": {"VIEW": True, "ANALYZE": False}}


def test_overwrite_active_user_perm():
    declaration = PermissionDeclaration(
        {"user_1": {"ANALYZE": True, "VIEW": False}},
        {"ug_1": {"VIEW": True, "ANALYZE": False}},
    )
    permission = PermissionIncrementalLoad(
        "ANALYZE", "", "user_1", PermissionType.user, False
    )
    declaration.add_permission(permission)
    assert declaration.users == {"user_1": {"ANALYZE": True, "VIEW": False}}
    assert declaration.user_groups == {"ug_1": {"VIEW": True, "ANALYZE": False}}


def test_add_new_user_perm():
    declaration = PermissionDeclaration(
        {"user_1": {"ANALYZE": True, "VIEW": False}},
        {"ug_1": {"VIEW": True, "ANALYZE": False}},
    )
    permission = PermissionIncrementalLoad(
        "VIEW", "", "user_2", PermissionType.user, True
    )
    declaration.add_permission(permission)
    assert declaration.users == {
        "user_1": {"ANALYZE": True, "VIEW": False},
        "user_2": {"VIEW": True},
    }
    assert declaration.user_groups == {"ug_1": {"VIEW": True, "ANALYZE": False}}


def test_modify_one_of_user_perms():
    declaration = PermissionDeclaration(
        {"user_1": {"ANALYZE": True, "VIEW": False}, "user_2": {"VIEW": True}},
        {"ug_1": {"VIEW": True, "ANALYZE": False}},
    )
    permission = PermissionIncrementalLoad(
        "MANAGE", "", "user_1", PermissionType.user, True
    )
    declaration.add_permission(permission)
    assert declaration.users == {
        "user_1": {"ANALYZE": True, "VIEW": False, "MANAGE": True},
        "user_2": {"VIEW": True},
    }
    assert declaration.user_groups == {"ug_1": {"VIEW": True, "ANALYZE": False}}


# Add userGroup permission


def test_add_new_active_ug_perm():
    declaration = PermissionDeclaration(
        {"user_1": {"ANALYZE": True, "VIEW": False}},
        {"ug_1": {"VIEW": True, "ANALYZE": False}},
    )
    permission = PermissionIncrementalLoad(
        "MANAGE", "", "ug_1", PermissionType.user_group, True
    )
    declaration.add_permission(permission)
    assert declaration.users == {"user_1": {"ANALYZE": True, "VIEW": False}}
    assert declaration.user_groups == {
        "ug_1": {"VIEW": True, "ANALYZE": False, "MANAGE": True}
    }


def test_add_new_inactive_ug_perm():
    declaration = PermissionDeclaration(
        {"user_1": {"ANALYZE": True, "VIEW": False}},
        {"ug_1": {"VIEW": True, "ANALYZE": False}},
    )
    permission = PermissionIncrementalLoad(
        "MANAGE", "", "ug_1", PermissionType.user_group, False
    )
    declaration.add_permission(permission)
    assert declaration.users == {"user_1": {"ANALYZE": True, "VIEW": False}}
    assert declaration.user_groups == {
        "ug_1": {"VIEW": True, "ANALYZE": False, "MANAGE": False}
    }


def test_overwrite_inactive_ug_perm():
    declaration = PermissionDeclaration(
        {"user_1": {"ANALYZE": True, "VIEW": False}},
        {"ug_1": {"VIEW": True, "ANALYZE": False}},
    )
    permission = PermissionIncrementalLoad(
        "ANALYZE", "", "ug_1", PermissionType.user_group, True
    )
    declaration.add_permission(permission)
    assert declaration.users == {"user_1": {"ANALYZE": True, "VIEW": False}}
    assert declaration.user_groups == {"ug_1": {"VIEW": True, "ANALYZE": True}}


def test_overwrite_active_ug_perm():
    declaration = PermissionDeclaration(
        {"user_1": {"ANALYZE": True, "VIEW": False}},
        {"ug_1": {"VIEW": True, "ANALYZE": False}},
    )
    permission = PermissionIncrementalLoad(
        "VIEW", "", "ug_1", PermissionType.user_group, False
    )
    declaration.add_permission(permission)
    assert declaration.users == {"user_1": {"ANALYZE": True, "VIEW": False}}
    assert declaration.user_groups == {"ug_1": {"VIEW": True, "ANALYZE": False}}


def test_add_new_ug_perm():
    declaration = PermissionDeclaration(
        {"user_1": {"ANALYZE": True, "VIEW": False}},
        {"ug_1": {"VIEW": True, "ANALYZE": False}},
    )
    permission = PermissionIncrementalLoad(
        "VIEW", "", "ug_2", PermissionType.user_group, True
    )
    declaration.add_permission(permission)
    assert declaration.users == {"user_1": {"ANALYZE": True, "VIEW": False}}
    assert declaration.user_groups == {
        "ug_1": {"VIEW": True, "ANALYZE": False},
        "ug_2": {"VIEW": True},
    }


def test_modify_one_of_ug_perms():
    declaration = PermissionDeclaration(
        {"user_1": {"ANALYZE": True, "VIEW": False}},
        {"ug_1": {"VIEW": True, "ANALYZE": False}, "ug_2": {"VIEW": True}},
    )
    permission = PermissionIncrementalLoad(
        "MANAGE", "", "ug_1", PermissionType.user_group, True
    )
    declaration.add_permission(permission)
    assert declaration.users == {"user_1": {"ANALYZE": True, "VIEW": False}}
    assert declaration.user_groups == {
        "ug_1": {"VIEW": True, "ANALYZE": False, "MANAGE": True},
        "ug_2": {"VIEW": True},
    }


def test_upsert():
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

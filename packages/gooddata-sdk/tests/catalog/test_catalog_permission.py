# (C) 2022 GoodData Corporation
from __future__ import annotations

import json
from pathlib import Path

import pytest
from gooddata_sdk import (
    CatalogAssigneeIdentifier,
    CatalogAssigneeRule,
    CatalogDashboardAssigneeIdentifier,
    CatalogDeclarativeDataSourcePermission,
    CatalogDeclarativeOrganizationPermission,
    CatalogDeclarativeSingleWorkspacePermission,
    CatalogDeclarativeWorkspaceHierarchyPermission,
    CatalogDeclarativeWorkspacePermissions,
    CatalogOrganizationPermissionAssignment,
    CatalogPermissionsForAssigneeIdentifier,
    CatalogPermissionsForAssigneeRule,
    GoodDataApiClient,
    GoodDataSdk,
)
from tests_support.vcrpy_utils import get_vcr

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures" / "permissions"


def _empty_permissions(sdk: GoodDataSdk, workspace_id: str) -> None:
    empty_permissions_e = CatalogDeclarativeWorkspacePermissions(permissions=[], hierarchy_permissions=[])
    sdk.catalog_permission.put_declarative_permissions(
        workspace_id=workspace_id, declarative_workspace_permissions=empty_permissions_e
    )
    empty_permissions_o = sdk.catalog_permission.get_declarative_permissions(workspace_id=workspace_id)
    assert empty_permissions_e == empty_permissions_o
    assert empty_permissions_e.to_dict(camel_case=True) == empty_permissions_o.to_dict(camel_case=True)


def _assert_default_permissions(catalog_declarative_permissions: CatalogDeclarativeWorkspacePermissions) -> None:
    assert len(catalog_declarative_permissions.hierarchy_permissions) == 2
    assert set(
        hierarchy_permission.assignee.id
        for hierarchy_permission in catalog_declarative_permissions.hierarchy_permissions
    ) == {"demo2", "demoGroup"}
    assert set(
        hierarchy_permission.name for hierarchy_permission in catalog_declarative_permissions.hierarchy_permissions
    ) == {"MANAGE", "ANALYZE"}
    assert len(catalog_declarative_permissions.permissions) == 2
    assert set(permission.assignee.id for permission in catalog_declarative_permissions.permissions) == {
        "demo2",
        "demoGroup",
    }
    assert set(permission.name for permission in catalog_declarative_permissions.permissions) == {"ANALYZE", "VIEW"}


def _assert_organization_permissions_id(
    catalog_organization_permissions: list[CatalogDeclarativeOrganizationPermission],
) -> None:
    assert set(org_permission.assignee.id for org_permission in catalog_organization_permissions) == {"adminGroup"}


def _default_organization_permissions(sdk: GoodDataSdk) -> None:
    default_catalog_organization_permission = CatalogDeclarativeOrganizationPermission(
        name="MANAGE", assignee=CatalogAssigneeIdentifier(id="adminGroup", type="userGroup")
    )

    sdk.catalog_permission.put_declarative_organization_permissions([default_catalog_organization_permission])

    catalog_permissions = sdk.catalog_permission.get_declarative_organization_permissions()
    assert len(catalog_permissions) == 1
    _assert_organization_permissions_id(catalog_permissions)
    assert set(org_permission.name for org_permission in catalog_permissions) == {"MANAGE"}


def _validation_helper(class_type, attribute_name: str):
    client_class = class_type.client_class()
    allowed_values = list(client_class.allowed_values.get((attribute_name,)).values())
    for allowed_value in allowed_values:
        class_type(name=allowed_value, assignee=CatalogAssigneeIdentifier(id="", type="user"))
    with pytest.raises(ValueError):
        class_type(name="nonsense", assignee=CatalogAssigneeIdentifier(id="", type="user"))


def _add_dashboard_permissions(sdk: GoodDataSdk) -> None:
    # Add dashboard permission VIEW to one group and allWorkspaceUsers
    sdk.catalog_permission.manage_dashboard_permissions(
        "demo",
        "campaign",
        [
            CatalogPermissionsForAssigneeIdentifier(
                assignee_identifier=CatalogAssigneeIdentifier(id="visitorsGroup", type="userGroup"),
                permissions=["VIEW"],
            ),
            CatalogPermissionsForAssigneeRule(
                assignee_rule=CatalogAssigneeRule(type="allWorkspaceUsers"),
                permissions=["VIEW"],
            ),
        ],
    )
    # check that just one group and allWorkspaceUsers has dashboard permission
    dashboard_permissions = sdk.catalog_permission.list_dashboard_permissions("demo", "campaign")
    assert len(dashboard_permissions.user_groups) == 1
    assert len(dashboard_permissions.users) == 0
    assert len(dashboard_permissions.rules) == 1


def _rollback_dashboard_permissions(sdk: GoodDataSdk) -> None:
    # remove dashboard permissions of the group and allWorkspaceUsers
    sdk.catalog_permission.manage_dashboard_permissions(
        "demo",
        "campaign",
        [
            CatalogPermissionsForAssigneeIdentifier(
                assignee_identifier=CatalogDashboardAssigneeIdentifier(id="visitorsGroup", type="userGroup"),
                permissions=[],
            ),
            CatalogPermissionsForAssigneeRule(
                assignee_rule=CatalogAssigneeRule(type="allWorkspaceUsers"),
                permissions=[],
            ),
        ],
    )
    # check that it was properly removed
    dashboard_permissions = sdk.catalog_permission.list_dashboard_permissions("demo", "campaign")
    assert len(dashboard_permissions.user_groups) == 0
    assert len(dashboard_permissions.users) == 0
    assert len(dashboard_permissions.rules) == 0


def test_single_workspace_permission_validation(test_config):
    _validation_helper(CatalogDeclarativeSingleWorkspacePermission, "name")


def test_workspace_hierarchy_permission(test_config):
    _validation_helper(CatalogDeclarativeWorkspaceHierarchyPermission, "name")


def test_data_source_permission(test_config):
    _validation_helper(CatalogDeclarativeDataSourcePermission, "name")


@gd_vcr.use_cassette(str(_fixtures_dir / "get_declarative_permissions.yaml"))
def test_get_declarative_permissions(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    client = GoodDataApiClient(host=test_config["host"], token=test_config["token"])
    layout_api = client.layout_api

    catalog_declarative_permissions = sdk.catalog_permission.get_declarative_permissions(test_config["workspace"])
    declarative_permissions = layout_api.get_workspace_permissions(test_config["workspace"])
    _assert_default_permissions(catalog_declarative_permissions)
    assert catalog_declarative_permissions.to_dict(camel_case=True) == declarative_permissions.to_dict(camel_case=True)


@gd_vcr.use_cassette(str(_fixtures_dir / "put_declarative_permissions.yaml"))
def test_put_declarative_permissions(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    expected_json_path = _current_dir / "expected" / "declarative_workspace_permissions.json"
    workspace_id = test_config["workspace_with_parent"]
    declarative_permissions_e = sdk.catalog_permission.get_declarative_permissions(workspace_id)
    assert len(declarative_permissions_e.permissions) == 0
    assert len(declarative_permissions_e.hierarchy_permissions) == 0

    with open(expected_json_path, encoding="utf-8") as f:
        data = json.load(f)

    declarative_workspace_permissions = CatalogDeclarativeWorkspacePermissions.from_dict(data, camel_case=True)

    try:
        sdk.catalog_permission.put_declarative_permissions(
            workspace_id=workspace_id, declarative_workspace_permissions=declarative_workspace_permissions
        )
        declarative_permissions_o = sdk.catalog_permission.get_declarative_permissions(workspace_id=workspace_id)
        _assert_default_permissions(declarative_permissions_o)
    finally:
        _empty_permissions(sdk, workspace_id)


@gd_vcr.use_cassette(str(_fixtures_dir / "list_available_assignees.yaml"))
def test_list_available_assignees(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    available_assignees = sdk.catalog_permission.list_available_assignees("demo", "campaign")
    assert len(available_assignees.user_groups) == 2


@gd_vcr.use_cassette(str(_fixtures_dir / "list_dashboard_permissions.yaml"))
def test_list_dashboard_permissions(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    try:
        _add_dashboard_permissions(sdk)
    finally:
        _rollback_dashboard_permissions(sdk)


@gd_vcr.use_cassette(str(_fixtures_dir / "put_declarative_organization_permissions.yaml"))
def test_put_and_get_declarative_organization_permissions(test_config):
    expected_json_path = _current_dir / "expected" / "declarative_organization_permissions.json"
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    with open(expected_json_path, encoding="utf-8") as f:
        data = json.load(f)

    declarative_organization_permissions = [
        CatalogDeclarativeOrganizationPermission.from_api(permission) for permission in data
    ]

    try:
        sdk.catalog_permission.put_declarative_organization_permissions(declarative_organization_permissions)

        catalog_declarative_permissions_after_put = sdk.catalog_permission.get_declarative_organization_permissions()
        assert len(catalog_declarative_permissions_after_put) == 2
        _assert_organization_permissions_id(catalog_declarative_permissions_after_put)
        assert set(org_permission.name for org_permission in catalog_declarative_permissions_after_put) == {
            "MANAGE",
            "SELF_CREATE_TOKEN",
        }
    finally:
        _default_organization_permissions(sdk)


@gd_vcr.use_cassette(str(_fixtures_dir / "manage_organization_permissions.yaml"))
def test_manage_organization_permissions(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    # assign permissions to adminGroup
    try:
        sdk.catalog_permission.manage_organization_permissions(
            [
                CatalogOrganizationPermissionAssignment(
                    assignee_identifier=CatalogAssigneeIdentifier(id="adminGroup", type="userGroup"),
                    permissions=["MANAGE", "SELF_CREATE_TOKEN"],
                )
            ],
        )

        catalog_declarative_permissions_initial = sdk.catalog_permission.get_declarative_organization_permissions()
        assert len(catalog_declarative_permissions_initial) == 2
        assert set(org_permission.name for org_permission in catalog_declarative_permissions_initial) == {
            "MANAGE",
            "SELF_CREATE_TOKEN",
        }
    finally:
        _default_organization_permissions(sdk)


@gd_vcr.use_cassette(str(_fixtures_dir / "manage_dashboard_permissions_declarative_workspace.yaml"))
def test_manage_dashboard_permissions_declarative_workspace(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    try:
        _add_dashboard_permissions(sdk)
        sdk.catalog_workspace.get_declarative_workspace(workspace_id="demo")
    finally:
        _rollback_dashboard_permissions(sdk)

# (C) 2022 GoodData Corporation
from __future__ import annotations

import json
from pathlib import Path

import pytest
from tests_support.vcrpy_utils import get_vcr

from gooddata_sdk import (
    CatalogDashboardAssigneeIdentifier,
    CatalogDeclarativeDataSourcePermission,
    CatalogDeclarativeSingleWorkspacePermission,
    CatalogDeclarativeWorkspaceHierarchyPermission,
    CatalogDeclarativeWorkspacePermissions,
    CatalogPermissionsForAssignee,
    GoodDataApiClient,
    GoodDataSdk,
)

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


def _validation_helper(class_type, attribute_name: str):
    client_class = class_type.client_class()
    allowed_values = list(client_class.allowed_values.get((attribute_name,)).values())
    for allowed_value in allowed_values:
        try:
            class_type(name=allowed_value, assignee=CatalogDashboardAssigneeIdentifier(id="", type="user"))
        except ValueError:
            assert False
    with pytest.raises(ValueError):
        class_type(name="nonsense", assignee=CatalogDashboardAssigneeIdentifier(id="", type="user"))


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

    with open(expected_json_path, "r", encoding="utf-8") as f:
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
    # Add dashboard permission VIEW to one group
    sdk.catalog_permission.manage_dashboard_permissions(
        "demo",
        "campaign",
        [
            CatalogPermissionsForAssignee(
                assignee_identifier=CatalogDashboardAssigneeIdentifier(id="visitorsGroup", type="userGroup"),
                permissions=["VIEW"],
            )
        ],
    )
    # check, that just one group has dashboard permission
    dashboard_permissions = sdk.catalog_permission.list_dashboard_permissions("demo", "campaign")
    assert len(dashboard_permissions.user_groups) == 1
    # remove dashboard permissions to this group
    sdk.catalog_permission.manage_dashboard_permissions(
        "demo",
        "campaign",
        [
            CatalogPermissionsForAssignee(
                assignee_identifier=CatalogDashboardAssigneeIdentifier(id="visitorsGroup", type="userGroup"),
                permissions=[],
            )
        ],
    )
    # check that it was properly removed
    dashboard_permissions = sdk.catalog_permission.list_dashboard_permissions("demo", "campaign")
    assert len(dashboard_permissions.user_groups) == 0

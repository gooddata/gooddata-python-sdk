# (C) 2022 GoodData Corporation
from typing import Union

from gooddata_sdk.catalog.catalog_service_base import CatalogServiceBase
from gooddata_sdk.catalog.permission.declarative_model.dashboard_assignees import CatalogAvailableAssignees
from gooddata_sdk.catalog.permission.declarative_model.dashboard_permissions import CatalogDashboardPermissions
from gooddata_sdk.catalog.permission.declarative_model.manage_dashboard_permissions import (
    CatalogPermissionsForAssigneeIdentifier,
    CatalogPermissionsForAssigneeRule,
)
from gooddata_sdk.catalog.permission.declarative_model.permission import (
    CatalogDeclarativeOrganizationPermission,
    CatalogDeclarativeWorkspacePermissions,
    CatalogOrganizationPermissionAssignment,
)
from gooddata_sdk.client import GoodDataApiClient


class CatalogPermissionService(CatalogServiceBase):
    def __init__(self, api_client: GoodDataApiClient) -> None:
        super().__init__(api_client)

    def get_declarative_permissions(self, workspace_id: str) -> CatalogDeclarativeWorkspacePermissions:
        """Retrieve current set of permissions of the workspace in a declarative form.

        Args:
            workspace_id (str):
                Workspace identification string. e.g. "demo"

        Returns:
            CatalogDeclarativeWorkspacePermissions:
                Object containing workspace permissions.
        """
        return CatalogDeclarativeWorkspacePermissions.from_api(self._layout_api.get_workspace_permissions(workspace_id))

    def put_declarative_permissions(
        self, workspace_id: str, declarative_workspace_permissions: CatalogDeclarativeWorkspacePermissions
    ) -> None:
        """Set effective permissions for the workspace.

        Args:
            workspace_id (str):
                Workspace identification string. e.g. "demo"
            declarative_workspace_permissions (CatalogDeclarativeWorkspacePermissions):
                Object containing workspace Permissions.

        Returns:
            None
        """
        self._layout_api.set_workspace_permissions(
            workspace_id=workspace_id, declarative_workspace_permissions=declarative_workspace_permissions.to_api()
        )

    def list_available_assignees(self, workspace_id: str, dashboard_id: str) -> CatalogAvailableAssignees:
        """Provide list of users and groups available to assign some dashboard permission

        Args:
            workspace_id (str):
                Workspace identification string. e.g. "demo"
            dashboard_id (str):
                Dashboard identification string. e.g. "campaign"
        Returns:
            CatalogAvailableAssignees:
                Object containing users and user groups
        """
        return CatalogAvailableAssignees.from_dict(
            self._actions_api.available_assignees(workspace_id, dashboard_id, _check_return_type=False),
            camel_case=False,
        )

    def list_dashboard_permissions(self, workspace_id: str, dashboard_id: str) -> CatalogDashboardPermissions:
        """Provide list of users and user groups with granted dashboard permissions for particular dashboard

        Args:
            workspace_id (str):
                Workspace identification string. e.g. "demo"
            dashboard_id (str):
                Dashboard identification string. e.g. "campaign"
        Returns:
            CatalogDashboardPermissions:
                Object containing users and user groups and granted dashboard permissions
        """
        return CatalogDashboardPermissions.from_dict(
            self._actions_api.dashboard_permissions(workspace_id, dashboard_id, _check_return_type=False),
            camel_case=False,
        )

    def manage_dashboard_permissions(
        self,
        workspace_id: str,
        dashboard_id: str,
        permissions_for_assignee: list[
            Union[CatalogPermissionsForAssigneeIdentifier, CatalogPermissionsForAssigneeRule]
        ],
    ) -> None:
        """Provide managing dashboard permissions for user and user groups.

        Args:
            workspace_id (str):
                Workspace identification string. e.g. "demo"
            dashboard_id (str):
                Dashboard identification string. e.g. "campaign"
            permissions_for_assignee ([Union[CatalogPermissionsForAssignee, CatalogPermissionsForAssigneeRule]]):
                Object containing a List of permission assignments. An empty list of permissions in the assignment
                removes existing dashboard permissions.
        Returns:
            None
        """
        self._actions_api.manage_dashboard_permissions(
            workspace_id,
            dashboard_id,
            [permission.to_api() for permission in permissions_for_assignee],
            _check_return_type=False,
        )

    def get_declarative_organization_permissions(self) -> list[CatalogDeclarativeOrganizationPermission]:
        """Get a list of all declarative organization permissions.

        Args:
            None

        Returns:
            list[CatalogDeclarativeOrganizationPermission]:
                List of all declarative organization permissions.
        """

        organization_permissions = self._layout_api.get_organization_permissions()
        catalog_list = [
            CatalogDeclarativeOrganizationPermission.from_api(permission) for permission in organization_permissions
        ]
        return catalog_list

    def put_declarative_organization_permissions(
        self, org_permissions: list[CatalogDeclarativeOrganizationPermission]
    ) -> None:
        """Put a list of all declarative organization permissions.

        Args:
            org_permissions (list[CatalogDeclarativeOrganizationPermission]):
                List of declarative organization permissions.

        Returns:
            None
        """

        declarative_organization_permissions = [catalog_permission.to_api() for catalog_permission in org_permissions]
        self._layout_api.set_organization_permissions(declarative_organization_permissions)

    def manage_organization_permissions(
        self, organization_permission_assignments: list[CatalogOrganizationPermissionAssignment]
    ) -> None:
        """Provide managing organization permissions for user and user groups.

        Args:
            organization_permission_assignments ([CatalogOrganizationPermissionAssignment]):
                Object containing List of users and user group and desired organization permissions. Set empty list
                permissions for user/user group means remove organization permissions.
        Returns:
            None
        """
        permissions = [permission.to_api() for permission in organization_permission_assignments]
        self._actions_api.manage_organization_permissions(permissions, _check_return_type=False)

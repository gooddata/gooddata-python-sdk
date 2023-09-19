# (C) 2022 GoodData Corporation
from typing import List

from gooddata_sdk import (
    CatalogAvailableAssignees,
    CatalogDashboardPermissions,
    CatalogDeclarativeWorkspacePermissions,
    CatalogPermissionsAssignment,
    GoodDataApiClient,
)
from gooddata_sdk.catalog.catalog_service_base import CatalogServiceBase


class CatalogPermissionService(CatalogServiceBase):
    def __init__(self, api_client: GoodDataApiClient) -> None:
        super(CatalogPermissionService, self).__init__(api_client)

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
        self, workspace_id: str, dashboard_id: str, permissions_assignments: List[CatalogPermissionsAssignment]
    ) -> None:
        """Provide managing dashboard permissions for user and user groups.

        Args:
            workspace_id (str):
                Workspace identification string. e.g. "demo"
            dashboard_id (str):
                Dashboard identification string. e.g. "campaign"
            permissions_assignments ([CatalogPermissionsAssignment]):
                Object containing List of permissions assignments. An empty list of permissions in the assignment
                results in un-assigning existing dashboard permissions.
        Returns:
            None
        """
        self._actions_api.manage_dashboard_permissions(
            workspace_id,
            dashboard_id,
            [assignment.to_api() for assignment in permissions_assignments],
            _check_return_type=False,
        )

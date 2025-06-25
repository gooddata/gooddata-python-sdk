# (C) 2025 GoodData Corporation

"""Interaction with GoodData Cloud via the Gooddata Python SDK."""

from gooddata_sdk.catalog.permission.declarative_model.permission import (
    CatalogDeclarativeWorkspacePermissions,
)
from gooddata_sdk.catalog.user.entity_model.user import CatalogUser
from gooddata_sdk.catalog.user.entity_model.user_group import CatalogUserGroup
from gooddata_sdk.catalog.workspace.declarative_model.workspace.workspace import (
    CatalogDeclarativeWorkspaceDataFilters,
)
from gooddata_sdk.catalog.workspace.entity_model.user_data_filter import (
    CatalogUserDataFilter,
)
from gooddata_sdk.catalog.workspace.entity_model.workspace import (
    CatalogWorkspace,
)
from gooddata_sdk.sdk import GoodDataSdk

from gooddata_pipelines.api.utils import raise_with_context


class SDKMethods:
    """
    Class to intaract with GoodData Cloud via the Gooddata Python SDK.
    """

    _sdk: GoodDataSdk

    def check_workspace_exists(self, workspace_id: str) -> bool:
        try:
            self._sdk.catalog_workspace.get_workspace(workspace_id)
            return True
        except Exception:
            return False

    @raise_with_context()
    def get_workspace(self, workspace_id: str, **_: str) -> CatalogWorkspace:
        """
        Calls GoodData Python SDK to retrieve a workspace by its ID.

        Args:
            workspace_id (str): The ID of the workspace to retrieve.
        Returns:
            CatalogWorkspace: The workspace object retrieved from the SDK.
        Raises:
            GoodDataApiException: If the workspace cannot be retrieved, an exception
            is raised with additional context information.
        """
        return self._sdk.catalog_workspace.get_workspace(workspace_id)

    @raise_with_context()
    def delete_panther_workspace(self, workspace_id: str) -> None:
        """
        Calls GoodData Python SDK to delete a workspace by its ID.

        Args:
            workspace_id (str): The ID of the workspace to delete.
        Raises:
            GoodDataApiException: If the workspace cannot be deleted, an exception
            is raised with additional context information.
        """
        self._sdk.catalog_workspace.delete_workspace(workspace_id)

    @raise_with_context()
    def create_or_update_panther_workspace(
        self,
        workspace_id: str,
        workspace_name: str,
        parent_id: str | None,
        **_: str,
    ) -> None:
        """
        Calls GoodData Python SDK to create or update a workspace with the given ID,
        name, and parent ID.

        Args:
            workspace_id (str): The ID of the workspace to create or update.
            workspace_name (str): The name of the workspace.
            parent_id (str | None): The ID of the parent workspace, if any.
        Returns:
            None
        Raises:
            GoodDataApiException: If the workspace cannot be created or updated,
            an exception is raised with additional context information.
        """
        return self._sdk.catalog_workspace.create_or_update(
            CatalogWorkspace(
                workspace_id=workspace_id,
                name=workspace_name,
                parent_id=parent_id,
            )
        )

    def get_panther_children_workspaces(
        self, parent_workspace_ids: set[str]
    ) -> list[CatalogWorkspace]:
        """
        Calls GoodData Python SDK to retrieve all workspaces in domain and filters the
        result by the set of parent workspace IDs.

        Args:
            parent_workspace_ids (set[str]): A set of parent workspace IDs to filter
                child workspaces.
        Returns:
            list[CatalogWorkspace]: List of child workspaces in the parent workspace.
        """
        all_workspaces: list[CatalogWorkspace] = self.list_workspaces()

        children: list[CatalogWorkspace] = [
            workspace
            for workspace in all_workspaces
            if workspace.parent_id in parent_workspace_ids
        ]

        return children

    @raise_with_context()
    def list_workspaces(self) -> list[CatalogWorkspace]:
        """Retrieves all workspaces in the GoodData Cloud domain.

        Returns:
            list[CatalogWorkspace]: A list of all workspaces in the domain.
        Raises:
            GoodDataApiException: If the workspaces cannot be retrieved, an exception
            is raised with additional context information.
        """
        return self._sdk.catalog_workspace.list_workspaces()

    @raise_with_context()
    def get_declarative_permissions(
        self, workspace_id: str
    ) -> CatalogDeclarativeWorkspacePermissions:
        """
        Retrieves the declarative permissions for a given workspace.

        Args:
            workspace_id (str): The ID of the workspace for which to retrieve
                permissions.
        Returns:
            CatalogDeclarativeWorkspacePermissions: The declarative permissions
                for the workspace.
        Raises:
            GoodDataApiException: If the permissions cannot be retrieved, an exception
            is raised with additional context information.
        """
        return self._sdk.catalog_permission.get_declarative_permissions(
            workspace_id
        )

    @raise_with_context()
    def put_declarative_permissions(
        self,
        workspace_id: str,
        ws_permissions: CatalogDeclarativeWorkspacePermissions,
    ) -> None:
        """
        Updates the declarative permissions for a given workspace.

        Args:
            workspace_id (str): The ID of the workspace for which to update
                permissions.
            ws_permissions (CatalogDeclarativeWorkspacePermissions): The new
                declarative permissions to set for the workspace.
        Returns:
            None
        Raises:
            GoodDataApiException: If the permissions cannot be updated, an exception
            is raised with additional context information.
        """
        return self._sdk.catalog_permission.put_declarative_permissions(
            workspace_id, ws_permissions
        )

    @raise_with_context()
    def get_user(self, user_id: str, **_: str) -> CatalogUser:
        """
        Calls GoodData Python SDK to retrieve a user by its ID.

        Args:
            user_id (str): The ID of the user to retrieve.
        Returns:
            CatalogUser: The user object retrieved from the SDK.
        Raises:
            GoodDataApiException: If the user cannot be retrieved, an exception
            is raised with additional context information.
        """
        return self._sdk.catalog_user.get_user(user_id)

    @raise_with_context()
    def create_or_update_user(self, user: CatalogUser, **_: str) -> None:
        """
        Calls GoodData Python SDK to create or update a user.

        Args:
            user (CatalogUser): The user object to create or update.
        Returns:
            None
        Raises:
            GoodDataApiException: If the user cannot be created or updated,
            an exception is raised with additional context information.
        """
        return self._sdk.catalog_user.create_or_update_user(user)

    @raise_with_context()
    def delete_user(self, user_id: str, **_: str) -> None:
        """
        Calls GoodData Python SDK to delete a user by its ID.

        Args:
            user_id (str): The ID of the user to delete.
        Returns:
            None
        Raises:
            GoodDataApiException: If the user cannot be deleted, an exception
            is raised with additional context information.
        """
        return self._sdk.catalog_user.delete_user(user_id)

    @raise_with_context()
    def get_user_group(self, user_group_id: str, **_: str) -> CatalogUserGroup:
        """
        Calls GoodData Python SDK to retrieve a user group by its ID.

        Args:
            user_group_id (str): The ID of the user group to retrieve.
        Returns:
            CatalogUserGroup: The user group object retrieved from the SDK.
        Raises:
            GoodDataApiException: If the user group cannot be retrieved, an exception
            is raised with additional context information.
        """
        return self._sdk.catalog_user.get_user_group(user_group_id)

    @raise_with_context()
    def list_user_groups(self) -> list[CatalogUserGroup]:
        """
        Calls GoodData Python SDK to retrieve all user groups.

        Returns:
            list[CatalogUserGroup]: A list of all user groups in the domain.
        Raises:
            GoodDataApiException: If the user groups cannot be retrieved, an
            exception is raised with additional context information.
        """
        return self._sdk.catalog_user.list_user_groups()

    @raise_with_context()
    def create_or_update_user_group(
        self, catalog_user_group: CatalogUserGroup, **_: str
    ) -> None:
        """Calls GoodData Python SDK to create or update a user group.

        Args:
            catalog_user_group (CatalogUserGroup): The user group object to create or update.
        Returns:
            None
        Raises:
            GoodDataApiException: If the user group cannot be created or updated,
            an exception is raised with additional context information.
        """
        return self._sdk.catalog_user.create_or_update_user_group(
            catalog_user_group
        )

    @raise_with_context()
    def delete_user_group(self, user_group_id: str) -> None:
        """Calls GoodData Python SDK to delete a user group by its ID.

        Args:
            user_group_id (str): The ID of the user group to delete.
        Returns:
            None
        Raises:
            GoodDataApiException: If the user group cannot be deleted, an exception
            is raised with additional context information.
        """
        return self._sdk.catalog_user.delete_user_group(user_group_id)

    @raise_with_context()
    def get_declarative_workspace_data_filters(
        self,
    ) -> CatalogDeclarativeWorkspaceDataFilters:
        """Retrieves the declarative workspace data filters.

        Returns:
            CatalogDeclarativeWorkspaceDataFilters: The declarative workspace data filters.
        Raises:
            GoodDataApiException: If the declarative workspace data filters cannot be retrieved,
            an exception is raised with additional context information.
        """
        return (
            self._sdk.catalog_workspace.get_declarative_workspace_data_filters()
        )

    @raise_with_context()
    def list_user_data_filters(
        self, workspace_id: str
    ) -> list[CatalogUserDataFilter]:
        """Lists all user data filters for a given workspace.

        Args:
            workspace_id (str): The ID of the workspace for which to list user data filters.
        Returns:
            list[CatalogUserDataFilter]: A list of user data filters for the specified workspace.
        Raises:
            GoodDataApiException: If the user data filters cannot be listed, an exception
            is raised with additional context information.
        """
        return self._sdk.catalog_workspace.list_user_data_filters(workspace_id)

    @raise_with_context()
    def delete_user_data_filter(
        self, workspace_id: str, user_data_filter_id: str
    ) -> None:
        """Deletes a user data filter by its ID in the specified workspace.

        Args:
            workspace_id (str): The ID of the workspace containing the user data filter.
            user_data_filter_id (str): The ID of the user data filter to delete.
        Returns:
            None
        Raises:
            GoodDataApiException: If the user data filter cannot be deleted, an exception
            is raised with additional context information.
        """
        self._sdk.catalog_workspace.delete_user_data_filter(
            workspace_id, user_data_filter_id
        )

    @raise_with_context()
    def create_or_update_user_data_filter(
        self, workspace_id: str, user_data_filter: CatalogUserDataFilter
    ) -> None:
        """Creates or updates a user data filter in the specified workspace.

        Args:
            workspace_id (str): The ID of the workspace where the user data filter
                should be created or updated.
            user_data_filter (CatalogUserDataFilter): The user data filter object to create or update.
        Returns:
            None
        Raises:
            GoodDataApiException: If the user data filter cannot be created or updated,
            an exception is raised with additional context information.
        """
        self._sdk.catalog_workspace.create_or_update_user_data_filter(
            workspace_id, user_data_filter
        )

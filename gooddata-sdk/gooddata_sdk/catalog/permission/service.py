# (C) 2022 GoodData Corporation
from gooddata_sdk import GoodDataApiClient
from gooddata_sdk.catalog.catalog_service_base import CatalogServiceBase
from gooddata_sdk.catalog.permission.declarative_model.permission import CatalogDeclarativeWorkspacePermissions


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

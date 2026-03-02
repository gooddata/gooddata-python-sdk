# (C) 2024 GoodData Corporation


from attrs import define, field
from gooddata_api_client.model.permissions_assignment import PermissionsAssignment
from gooddata_api_client.model.user_management_data_source_permission_assignment import (
    UserManagementDataSourcePermissionAssignment,
)
from gooddata_api_client.model.user_management_permission_assignments import UserManagementPermissionAssignments
from gooddata_api_client.model.user_management_workspace_permission_assignment import (
    UserManagementWorkspacePermissionAssignment,
)

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.identifier import CatalogAssigneeIdentifier


@define(kw_only=True)
class CatalogDataSourcePermissionAssignment(Base):
    id: str
    permissions: list[str] = field(factory=list)
    name: str | None = None

    @staticmethod
    def client_class() -> type[UserManagementDataSourcePermissionAssignment]:
        return UserManagementDataSourcePermissionAssignment


@define(kw_only=True)
class CatalogWorkspacePermissionAssignment(Base):
    id: str
    permissions: list[str] = field(factory=list)
    hierarchy_permissions: list[str] = field(factory=list)
    name: str | None = None

    @staticmethod
    def client_class() -> type[UserManagementWorkspacePermissionAssignment]:
        return UserManagementWorkspacePermissionAssignment


@define(kw_only=True)
class CatalogPermissionAssignments(Base):
    workspaces: list[CatalogWorkspacePermissionAssignment] = field(factory=list)
    data_sources: list[CatalogDataSourcePermissionAssignment] = field(factory=list)

    @staticmethod
    def client_class() -> type[UserManagementPermissionAssignments]:
        return UserManagementPermissionAssignments


@define(kw_only=True)
class CatalogPermissionsAssignment(Base):
    assignees: list[CatalogAssigneeIdentifier]
    workspaces: list[CatalogWorkspacePermissionAssignment] = field(factory=list)
    data_sources: list[CatalogDataSourcePermissionAssignment] = field(factory=list)

    @staticmethod
    def client_class() -> type[PermissionsAssignment]:
        return PermissionsAssignment

# (C) 2024 GoodData Corporation

from typing import List, Optional, Type

import attrs
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


@attrs.define(auto_attribs=True, kw_only=True)
class CatalogDataSourcePermissionAssignment(Base):
    id: str
    permissions: List[str] = attrs.field(factory=list)
    name: Optional[str] = None

    @staticmethod
    def client_class() -> Type[UserManagementDataSourcePermissionAssignment]:
        return UserManagementDataSourcePermissionAssignment


@attrs.define(auto_attribs=True, kw_only=True)
class CatalogWorkspacePermissionAssignment(Base):
    id: str
    permissions: List[str] = attrs.field(factory=list)
    hierarchy_permissions: List[str] = attrs.field(factory=list)
    name: Optional[str] = None

    @staticmethod
    def client_class() -> Type[UserManagementWorkspacePermissionAssignment]:
        return UserManagementWorkspacePermissionAssignment


@attrs.define(auto_attribs=True, kw_only=True)
class CatalogPermissionAssignments(Base):
    workspaces: List[CatalogWorkspacePermissionAssignment] = attrs.field(factory=list)
    data_sources: List[CatalogDataSourcePermissionAssignment] = attrs.field(factory=list)

    @staticmethod
    def client_class() -> Type[UserManagementPermissionAssignments]:
        return UserManagementPermissionAssignments


@attrs.define(auto_attribs=True, kw_only=True)
class CatalogPermissionsAssignment(Base):
    assignees: List[CatalogAssigneeIdentifier]
    workspaces: List[CatalogWorkspacePermissionAssignment] = attrs.field(factory=list)
    data_sources: List[CatalogDataSourcePermissionAssignment] = attrs.field(factory=list)

    @staticmethod
    def client_class() -> Type[PermissionsAssignment]:
        return PermissionsAssignment

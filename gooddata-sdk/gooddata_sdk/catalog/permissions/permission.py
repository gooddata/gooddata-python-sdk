# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any, Type, TypeVar

from gooddata_metadata_client.model.declarative_data_source_permission import DeclarativeDataSourcePermission
from gooddata_metadata_client.model.declarative_single_workspace_permission import DeclarativeSingleWorkspacePermission
from gooddata_metadata_client.model.declarative_workspace_hierarchy_permission import (
    DeclarativeWorkspaceHierarchyPermission,
)
from gooddata_metadata_client.model.declarative_workspace_permissions import DeclarativeWorkspacePermissions
from gooddata_sdk.catalog.identifier import CatalogAssigneeIdentifier

T = TypeVar("T", bound="PermissionBase")


class PermissionBase:
    def __init__(self, name: str, assignee: CatalogAssigneeIdentifier):
        self.name = name
        self.assignee = assignee

    @classmethod
    def from_api(cls: Type[T], entity: dict[str, Any]) -> T:
        return cls(entity["name"], CatalogAssigneeIdentifier.from_api(entity["assignee"]))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.name == other.name and self.assignee == other.assignee

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, assignee={self.assignee})"


class CatalogDeclarativeSingleWorkspacePermission(PermissionBase):
    def to_api(self) -> DeclarativeSingleWorkspacePermission:
        return DeclarativeSingleWorkspacePermission(name=self.name, assignee=self.assignee.to_api())


class CatalogDeclarativeWorkspaceHierarchyPermission(PermissionBase):
    def to_api(self) -> DeclarativeWorkspaceHierarchyPermission:
        return DeclarativeWorkspaceHierarchyPermission(name=self.name, assignee=self.assignee.to_api())


class CatalogDeclarativeDataSourcePermission(PermissionBase):
    def to_api(self) -> DeclarativeDataSourcePermission:
        return DeclarativeDataSourcePermission(name=self.name, assignee=self.assignee.to_api())


class CatalogDeclarativeWorkspacePermissions:
    def __init__(
        self,
        permissions: list[CatalogDeclarativeSingleWorkspacePermission] = None,
        hierarchy_permissions: list[CatalogDeclarativeWorkspaceHierarchyPermission] = None,
    ):
        self.permissions = permissions if permissions is not None else []
        self.hierarchy_permissions = hierarchy_permissions if hierarchy_permissions is not None else []

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDeclarativeWorkspacePermissions:
        permissions = [
            CatalogDeclarativeSingleWorkspacePermission.from_api(permission)
            for permission in entity.get("permissions", [])
        ]
        hierarchy_permissions = [
            CatalogDeclarativeWorkspaceHierarchyPermission.from_api(hierarchy_permission)
            for hierarchy_permission in entity.get("hierarchy_permissions", [])
        ]
        return cls(permissions, hierarchy_permissions)

    def to_api(self) -> DeclarativeWorkspacePermissions:
        permissions = [permission.to_api() for permission in self.permissions]
        hierarchy_permissions = [hierarchy_permission.to_api() for hierarchy_permission in self.hierarchy_permissions]
        kwargs: dict[str, Any] = {"permissions": permissions, "hierarchy_permissions": hierarchy_permissions}
        return DeclarativeWorkspacePermissions(**kwargs)

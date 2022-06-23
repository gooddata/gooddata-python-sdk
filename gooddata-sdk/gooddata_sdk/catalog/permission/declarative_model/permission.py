# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import List, Type

import attr

from gooddata_metadata_client.model.declarative_data_source_permission import DeclarativeDataSourcePermission
from gooddata_metadata_client.model.declarative_single_workspace_permission import DeclarativeSingleWorkspacePermission
from gooddata_metadata_client.model.declarative_workspace_hierarchy_permission import (
    DeclarativeWorkspaceHierarchyPermission,
)
from gooddata_metadata_client.model.declarative_workspace_permissions import DeclarativeWorkspacePermissions
from gooddata_sdk.catalog.base import Base, value_in_allowed
from gooddata_sdk.catalog.identifier import CatalogAssigneeIdentifier


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeSingleWorkspacePermission(Base):
    name: str = attr.field(validator=value_in_allowed)
    assignee: CatalogAssigneeIdentifier

    @staticmethod
    def client_class() -> Type[DeclarativeSingleWorkspacePermission]:
        return DeclarativeSingleWorkspacePermission


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeWorkspaceHierarchyPermission(Base):
    name: str = attr.field(validator=value_in_allowed)
    assignee: CatalogAssigneeIdentifier

    @staticmethod
    def client_class() -> Type[DeclarativeWorkspaceHierarchyPermission]:
        return DeclarativeWorkspaceHierarchyPermission


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeDataSourcePermission(Base):
    name: str = attr.field(validator=value_in_allowed)
    assignee: CatalogAssigneeIdentifier

    @staticmethod
    def client_class() -> Type[DeclarativeDataSourcePermission]:
        return DeclarativeDataSourcePermission


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeWorkspacePermissions(Base):
    permissions: List[CatalogDeclarativeSingleWorkspacePermission] = []
    hierarchy_permissions: List[CatalogDeclarativeWorkspaceHierarchyPermission] = []

    @staticmethod
    def client_class() -> Type[DeclarativeWorkspacePermissions]:
        return DeclarativeWorkspacePermissions

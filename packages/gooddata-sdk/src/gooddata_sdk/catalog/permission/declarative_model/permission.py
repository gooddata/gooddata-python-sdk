# (C) 2022 GoodData Corporation
from __future__ import annotations

import attr
from gooddata_api_client.model.declarative_analytical_dashboard_permission_for_assignee import (
    DeclarativeAnalyticalDashboardPermissionForAssignee,
)
from gooddata_api_client.model.declarative_analytical_dashboard_permission_for_assignee_rule import (
    DeclarativeAnalyticalDashboardPermissionForAssigneeRule,
)
from gooddata_api_client.model.declarative_data_source_permission import DeclarativeDataSourcePermission
from gooddata_api_client.model.declarative_organization_permission import DeclarativeOrganizationPermission
from gooddata_api_client.model.declarative_single_workspace_permission import DeclarativeSingleWorkspacePermission
from gooddata_api_client.model.declarative_workspace_hierarchy_permission import DeclarativeWorkspaceHierarchyPermission
from gooddata_api_client.model.declarative_workspace_permissions import DeclarativeWorkspacePermissions
from gooddata_api_client.model.organization_permission_assignment import OrganizationPermissionAssignment

from gooddata_sdk.catalog.base import Base, value_in_allowed
from gooddata_sdk.catalog.identifier import CatalogAssigneeIdentifier
from gooddata_sdk.catalog.rule import CatalogAssigneeRule


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeSingleWorkspacePermission(Base):
    name: str = attr.field(validator=value_in_allowed)
    assignee: CatalogAssigneeIdentifier

    @staticmethod
    def client_class() -> type[DeclarativeSingleWorkspacePermission]:
        return DeclarativeSingleWorkspacePermission


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeWorkspaceHierarchyPermission(Base):
    name: str = attr.field(validator=value_in_allowed)
    assignee: CatalogAssigneeIdentifier

    @staticmethod
    def client_class() -> type[DeclarativeWorkspaceHierarchyPermission]:
        return DeclarativeWorkspaceHierarchyPermission


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeDataSourcePermission(Base):
    name: str = attr.field(validator=value_in_allowed)
    assignee: CatalogAssigneeIdentifier

    @staticmethod
    def client_class() -> type[DeclarativeDataSourcePermission]:
        return DeclarativeDataSourcePermission


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeWorkspacePermissions(Base):
    permissions: list[CatalogDeclarativeSingleWorkspacePermission] = attr.field(factory=list)
    hierarchy_permissions: list[CatalogDeclarativeWorkspaceHierarchyPermission] = attr.field(factory=list)

    @staticmethod
    def client_class() -> type[DeclarativeWorkspacePermissions]:
        return DeclarativeWorkspacePermissions


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeDashboardPermissionsForAssignee(Base):
    name: str = attr.field(validator=value_in_allowed)
    assignee: CatalogAssigneeIdentifier

    @staticmethod
    def client_class() -> type[DeclarativeAnalyticalDashboardPermissionForAssignee]:
        return DeclarativeAnalyticalDashboardPermissionForAssignee


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeDashboardPermissionsForAssigneeRule(Base):
    name: str = attr.field(validator=value_in_allowed)
    assignee_rule: CatalogAssigneeRule

    @staticmethod
    def client_class() -> type[DeclarativeAnalyticalDashboardPermissionForAssigneeRule]:
        return DeclarativeAnalyticalDashboardPermissionForAssigneeRule


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeOrganizationPermission(Base):
    name: str = attr.field(validator=value_in_allowed)
    assignee: CatalogAssigneeIdentifier

    @staticmethod
    def client_class() -> type[DeclarativeOrganizationPermission]:
        return DeclarativeOrganizationPermission


@attr.s(auto_attribs=True, kw_only=True)
class CatalogOrganizationPermissionAssignment(Base):
    assignee_identifier: CatalogAssigneeIdentifier
    permissions: list[str] = attr.field(factory=list)

    @staticmethod
    def client_class() -> type[OrganizationPermissionAssignment]:
        return OrganizationPermissionAssignment

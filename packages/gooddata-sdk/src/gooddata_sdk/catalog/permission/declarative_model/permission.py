# (C) 2022 GoodData Corporation
from __future__ import annotations

from attrs import define, field
from gooddata_api_client.model.declarative_analytical_dashboard_permission_for_assignee import (
    DeclarativeAnalyticalDashboardPermissionForAssignee,
)
from gooddata_api_client.model.declarative_analytical_dashboard_permission_for_assignee_rule import (
    DeclarativeAnalyticalDashboardPermissionForAssigneeRule,
)
from gooddata_api_client.model.declarative_data_source_permission import DeclarativeDataSourcePermission
from gooddata_api_client.model.declarative_metric_permission_for_assignee import (
    DeclarativeMetricPermissionForAssignee,
)
from gooddata_api_client.model.declarative_metric_permission_for_assignee_rule import (
    DeclarativeMetricPermissionForAssigneeRule,
)
from gooddata_api_client.model.declarative_organization_permission import DeclarativeOrganizationPermission
from gooddata_api_client.model.declarative_single_workspace_permission import DeclarativeSingleWorkspacePermission
from gooddata_api_client.model.declarative_visualization_object_permission_for_assignee import (
    DeclarativeVisualizationObjectPermissionForAssignee,
)
from gooddata_api_client.model.declarative_visualization_object_permission_for_assignee_rule import (
    DeclarativeVisualizationObjectPermissionForAssigneeRule,
)
from gooddata_api_client.model.declarative_workspace_hierarchy_permission import DeclarativeWorkspaceHierarchyPermission
from gooddata_api_client.model.declarative_workspace_permissions import DeclarativeWorkspacePermissions
from gooddata_api_client.model.organization_permission_assignment import OrganizationPermissionAssignment

from gooddata_sdk.catalog.base import Base, value_in_allowed
from gooddata_sdk.catalog.identifier import CatalogAssigneeIdentifier
from gooddata_sdk.catalog.rule import CatalogAssigneeRule


@define(kw_only=True)
class CatalogDeclarativeSingleWorkspacePermission(Base):
    name: str = field(validator=value_in_allowed)
    assignee: CatalogAssigneeIdentifier

    @staticmethod
    def client_class() -> type[DeclarativeSingleWorkspacePermission]:
        return DeclarativeSingleWorkspacePermission


@define(kw_only=True)
class CatalogDeclarativeWorkspaceHierarchyPermission(Base):
    name: str = field(validator=value_in_allowed)
    assignee: CatalogAssigneeIdentifier

    @staticmethod
    def client_class() -> type[DeclarativeWorkspaceHierarchyPermission]:
        return DeclarativeWorkspaceHierarchyPermission


@define(kw_only=True)
class CatalogDeclarativeDataSourcePermission(Base):
    name: str = field(validator=value_in_allowed)
    assignee: CatalogAssigneeIdentifier

    @staticmethod
    def client_class() -> type[DeclarativeDataSourcePermission]:
        return DeclarativeDataSourcePermission


@define(kw_only=True)
class CatalogDeclarativeWorkspacePermissions(Base):
    permissions: list[CatalogDeclarativeSingleWorkspacePermission] = field(factory=list)
    hierarchy_permissions: list[CatalogDeclarativeWorkspaceHierarchyPermission] = field(factory=list)

    @staticmethod
    def client_class() -> type[DeclarativeWorkspacePermissions]:
        return DeclarativeWorkspacePermissions


@define(kw_only=True)
class CatalogDeclarativeDashboardPermissionsForAssignee(Base):
    name: str = field(validator=value_in_allowed)
    assignee: CatalogAssigneeIdentifier

    @staticmethod
    def client_class() -> type[DeclarativeAnalyticalDashboardPermissionForAssignee]:
        return DeclarativeAnalyticalDashboardPermissionForAssignee


@define(kw_only=True)
class CatalogDeclarativeDashboardPermissionsForAssigneeRule(Base):
    name: str = field(validator=value_in_allowed)
    assignee_rule: CatalogAssigneeRule

    @staticmethod
    def client_class() -> type[DeclarativeAnalyticalDashboardPermissionForAssigneeRule]:
        return DeclarativeAnalyticalDashboardPermissionForAssigneeRule


@define(kw_only=True)
class CatalogDeclarativeMetricPermissionsForAssignee(Base):
    name: str = field(validator=value_in_allowed)
    assignee: CatalogAssigneeIdentifier

    @staticmethod
    def client_class() -> type[DeclarativeMetricPermissionForAssignee]:
        return DeclarativeMetricPermissionForAssignee


@define(kw_only=True)
class CatalogDeclarativeMetricPermissionsForAssigneeRule(Base):
    name: str = field(validator=value_in_allowed)
    assignee_rule: CatalogAssigneeRule

    @staticmethod
    def client_class() -> type[DeclarativeMetricPermissionForAssigneeRule]:
        return DeclarativeMetricPermissionForAssigneeRule


@define(kw_only=True)
class CatalogDeclarativeVisualizationObjectPermissionsForAssignee(Base):
    name: str = field(validator=value_in_allowed)
    assignee: CatalogAssigneeIdentifier

    @staticmethod
    def client_class() -> type[DeclarativeVisualizationObjectPermissionForAssignee]:
        return DeclarativeVisualizationObjectPermissionForAssignee


@define(kw_only=True)
class CatalogDeclarativeVisualizationObjectPermissionsForAssigneeRule(Base):
    name: str = field(validator=value_in_allowed)
    assignee_rule: CatalogAssigneeRule

    @staticmethod
    def client_class() -> type[DeclarativeVisualizationObjectPermissionForAssigneeRule]:
        return DeclarativeVisualizationObjectPermissionForAssigneeRule


@define(kw_only=True)
class CatalogDeclarativeOrganizationPermission(Base):
    name: str = field(validator=value_in_allowed)
    assignee: CatalogAssigneeIdentifier

    @staticmethod
    def client_class() -> type[DeclarativeOrganizationPermission]:
        return DeclarativeOrganizationPermission


@define(kw_only=True)
class CatalogOrganizationPermissionAssignment(Base):
    assignee_identifier: CatalogAssigneeIdentifier
    permissions: list[str] = field(factory=list)

    @staticmethod
    def client_class() -> type[OrganizationPermissionAssignment]:
        return OrganizationPermissionAssignment

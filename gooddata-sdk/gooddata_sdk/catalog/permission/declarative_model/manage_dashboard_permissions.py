# (C) 2023 GoodData Corporation
import attr
from gooddata_api_client.model.manage_dashboard_permissions_request_inner import ManageDashboardPermissionsRequestInner

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.identifier import CatalogAssigneeIdentifier
from gooddata_sdk.catalog.rule import CatalogAssigneeRule


# Kept for backward compatibility only
@attr.s(auto_attribs=True, kw_only=True)
class CatalogDashboardAssigneeIdentifier(CatalogAssigneeIdentifier):
    pass


@attr.s(auto_attribs=True, kw_only=True)
class CatalogPermissionsForAssigneeIdentifier(Base):
    permissions: list[str] = attr.field(factory=list)
    assignee_identifier: CatalogAssigneeIdentifier

    @staticmethod
    def client_class() -> type[ManageDashboardPermissionsRequestInner]:
        return ManageDashboardPermissionsRequestInner


@attr.s(auto_attribs=True, kw_only=True)
class CatalogPermissionsForAssigneeRule(Base):
    permissions: list[str] = attr.field(factory=list)
    assignee_rule: CatalogAssigneeRule

    @staticmethod
    def client_class() -> type[ManageDashboardPermissionsRequestInner]:
        return ManageDashboardPermissionsRequestInner

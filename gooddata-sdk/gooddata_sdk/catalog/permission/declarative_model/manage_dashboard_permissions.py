# (C) 2023 GoodData Corporation
from typing import List, Type

import attr

from gooddata_api_client.model.manage_dashboard_permissions_request_inner import ManageDashboardPermissionsRequestInner
from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.identifier import CatalogAssigneeIdentifier
from gooddata_sdk.catalog.rule import CatalogAssigneeRule


@attr.s(auto_attribs=True, kw_only=True)
class CatalogPermissionsAssignment(Base):
    permissions: List[str] = attr.field(factory=list)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogPermissionsForAssignee(CatalogPermissionsAssignment):
    assignee_identifier: CatalogAssigneeIdentifier

    @staticmethod
    def client_class() -> Type[ManageDashboardPermissionsRequestInner]:
        return ManageDashboardPermissionsRequestInner

    def to_api(self) -> ManageDashboardPermissionsRequestInner:
        return ManageDashboardPermissionsRequestInner(
            permissions=self.permissions,
            assignee_identifier=self.assignee_identifier.to_api(),
        )


@attr.s(auto_attribs=True, kw_only=True)
class CatalogPermissionsForAssigneeRule(CatalogPermissionsAssignment):
    assignee_rule: CatalogAssigneeRule

    @staticmethod
    def client_class() -> Type[ManageDashboardPermissionsRequestInner]:
        return ManageDashboardPermissionsRequestInner

    def to_api(self) -> ManageDashboardPermissionsRequestInner:
        return ManageDashboardPermissionsRequestInner(
            permissions=self.permissions,
            assignee_rule=self.assignee_rule.to_api(),
        )

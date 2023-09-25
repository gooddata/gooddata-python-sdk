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

    @staticmethod
    def client_class() -> Type[ManageDashboardPermissionsRequestInner]:
        return ManageDashboardPermissionsRequestInner


@attr.s(auto_attribs=True, kw_only=True)
class CatalogPermissionsForAssignee(CatalogPermissionsAssignment):
    assignee_identifier: CatalogAssigneeIdentifier


@attr.s(auto_attribs=True, kw_only=True)
class CatalogPermissionsForAssigneeRule(CatalogPermissionsAssignment):
    assignee_rule: CatalogAssigneeRule

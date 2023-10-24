# (C) 2023 GoodData Corporation
from typing import List, Optional, Type

import attr

from gooddata_api_client.model.manage_dashboard_permissions_request_inner import ManageDashboardPermissionsRequestInner
from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.identifier import CatalogAssigneeIdentifier
from gooddata_sdk.catalog.rule import CatalogAssigneeRule


@attr.s(auto_attribs=True, kw_only=True)
class CatalogPermissionsAssignment(Base):
    permissions: List[str] = attr.field(factory=list)
    assignee_identifier: Optional[CatalogAssigneeIdentifier] = None
    assignee_rule: Optional[CatalogAssigneeRule] = None

    @staticmethod
    def client_class() -> Type[ManageDashboardPermissionsRequestInner]:
        return ManageDashboardPermissionsRequestInner


# Kept for backward compatibility only
@attr.s(auto_attribs=True, kw_only=True)
class CatalogDashboardAssigneeIdentifier(CatalogAssigneeIdentifier):
    pass


# Kept for backward compatibility only
@attr.s(auto_attribs=True, kw_only=True)
class CatalogPermissionsForAssignee(Base):
    permissions: List[str] = attr.field(factory=list)
    assignee_identifier: CatalogDashboardAssigneeIdentifier

    @staticmethod
    def client_class() -> Type[ManageDashboardPermissionsRequestInner]:
        return ManageDashboardPermissionsRequestInner

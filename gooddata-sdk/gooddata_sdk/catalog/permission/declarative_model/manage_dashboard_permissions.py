# (C) 2023 GoodData Corporation
from typing import List, Type

import attr

from gooddata_api_client.model.assignee_identifier import AssigneeIdentifier
from gooddata_api_client.model.permissions_for_assignee import PermissionsForAssignee
from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDashboardAssigneeIdentifier(Base):
    id: str
    type: str

    @staticmethod
    def client_class() -> Type[AssigneeIdentifier]:
        return AssigneeIdentifier


@attr.s(auto_attribs=True, kw_only=True)
class CatalogPermissionsForAssignee(Base):
    assignee_identifier: CatalogDashboardAssigneeIdentifier
    permissions: List[str] = attr.field(factory=list)

    @staticmethod
    def client_class() -> Type[PermissionsForAssignee]:
        return PermissionsForAssignee

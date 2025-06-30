# (C) 2023 GoodData Corporation
from typing import Optional

import attr
from gooddata_api_client.model.available_assignees import AvailableAssignees
from gooddata_api_client.model.user_assignee import UserAssignee
from gooddata_api_client.model.user_group_assignee import UserGroupAssignee

from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserAssignee(Base):
    id: str
    name: Optional[str] = None
    email: Optional[str] = None

    @staticmethod
    def client_class() -> type[UserAssignee]:
        return UserAssignee


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserGroupAssignee(Base):
    id: str
    name: Optional[str] = None

    @staticmethod
    def client_class() -> type[UserGroupAssignee]:
        return UserGroupAssignee


@attr.s(auto_attribs=True, kw_only=True)
class CatalogAvailableAssignees(Base):
    user_groups: list[CatalogUserGroupAssignee]
    users: list[CatalogUserAssignee]

    @staticmethod
    def client_class() -> type[AvailableAssignees]:
        return AvailableAssignees

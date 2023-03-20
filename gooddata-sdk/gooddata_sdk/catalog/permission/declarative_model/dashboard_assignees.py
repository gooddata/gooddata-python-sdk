# (C) 2023 GoodData Corporation
from typing import List, Optional, Type

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
    def client_class() -> Type[UserAssignee]:
        return UserAssignee


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserGroupAssignee(Base):
    id: str
    name: Optional[str] = None

    @staticmethod
    def client_class() -> Type[UserGroupAssignee]:
        return UserGroupAssignee


@attr.s(auto_attribs=True, kw_only=True)
class CatalogAvailableAssignees(Base):
    user_groups: List[CatalogUserGroupAssignee]
    users: List[CatalogUserAssignee]

    @staticmethod
    def client_class() -> Type[AvailableAssignees]:
        return AvailableAssignees

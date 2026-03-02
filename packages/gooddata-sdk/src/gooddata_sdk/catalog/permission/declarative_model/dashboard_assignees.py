# (C) 2023 GoodData Corporation

from attrs import define
from gooddata_api_client.model.available_assignees import AvailableAssignees
from gooddata_api_client.model.user_assignee import UserAssignee
from gooddata_api_client.model.user_group_assignee import UserGroupAssignee

from gooddata_sdk.catalog.base import Base


@define(kw_only=True)
class CatalogUserAssignee(Base):
    id: str
    name: str | None = None
    email: str | None = None

    @staticmethod
    def client_class() -> type[UserAssignee]:
        return UserAssignee


@define(kw_only=True)
class CatalogUserGroupAssignee(Base):
    id: str
    name: str | None = None

    @staticmethod
    def client_class() -> type[UserGroupAssignee]:
        return UserGroupAssignee


@define(kw_only=True)
class CatalogAvailableAssignees(Base):
    user_groups: list[CatalogUserGroupAssignee]
    users: list[CatalogUserAssignee]

    @staticmethod
    def client_class() -> type[AvailableAssignees]:
        return AvailableAssignees

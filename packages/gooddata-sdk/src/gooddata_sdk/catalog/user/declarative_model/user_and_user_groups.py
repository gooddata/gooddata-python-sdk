# (C) 2022 GoodData Corporation
from __future__ import annotations

from pathlib import Path

import attr
from gooddata_api_client.model.declarative_users_user_groups import DeclarativeUsersUserGroups

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.user.declarative_model.user import CatalogDeclarativeUser, CatalogDeclarativeUsers
from gooddata_sdk.catalog.user.declarative_model.user_group import (
    CatalogDeclarativeUserGroup,
    CatalogDeclarativeUserGroups,
)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeUsersUserGroups(Base):
    users: list[CatalogDeclarativeUser]
    user_groups: list[CatalogDeclarativeUserGroup]

    @staticmethod
    def client_class() -> type[DeclarativeUsersUserGroups]:
        return DeclarativeUsersUserGroups

    @classmethod
    def load_from_disk(cls, layout_organization_folder: Path) -> CatalogDeclarativeUsersUserGroups:
        declarative_users = CatalogDeclarativeUsers.load_from_disk(
            layout_organization_folder=layout_organization_folder
        )
        declarative_user_groups = CatalogDeclarativeUserGroups.load_from_disk(
            layout_organization_folder=layout_organization_folder
        )
        users = declarative_users.users
        user_groups = declarative_user_groups.user_groups
        return cls(users=users, user_groups=user_groups)

    def store_to_disk(self, layout_organization_folder: Path) -> None:
        users = CatalogDeclarativeUsers(users=self.users)
        user_groups = CatalogDeclarativeUserGroups(user_groups=self.user_groups)
        users.store_to_disk(layout_organization_folder=layout_organization_folder)
        user_groups.store_to_disk(layout_organization_folder=layout_organization_folder)

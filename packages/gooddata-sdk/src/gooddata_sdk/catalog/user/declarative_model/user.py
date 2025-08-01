# (C) 2022 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from typing import Optional

import attr
from gooddata_api_client.model.declarative_user import DeclarativeUser
from gooddata_api_client.model.declarative_user_permission import DeclarativeUserPermission
from gooddata_api_client.model.declarative_users import DeclarativeUsers

from gooddata_sdk.catalog.base import Base, value_in_allowed
from gooddata_sdk.catalog.identifier import CatalogAssigneeIdentifier, CatalogDeclarativeUserGroupIdentifier
from gooddata_sdk.catalog.setting import CatalogDeclarativeSetting
from gooddata_sdk.utils import create_directory, read_layout_from_file, write_layout_to_file

LAYOUT_USERS_DIR = "users"
LAYOUT_USERS_FILE = "users.yaml"


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeUsers(Base):
    users: list[CatalogDeclarativeUser]

    @staticmethod
    def client_class() -> type[DeclarativeUsers]:
        return DeclarativeUsers

    @classmethod
    def load_from_disk(cls, layout_organization_folder: Path) -> CatalogDeclarativeUsers:
        users_directory = layout_organization_folder / LAYOUT_USERS_DIR
        users_file = users_directory / LAYOUT_USERS_FILE
        data = read_layout_from_file(users_file)
        users = [CatalogDeclarativeUser.from_dict(record, camel_case=True) for record in data]
        return cls(users=users)

    def store_to_disk(self, layout_organization_folder: Path) -> None:
        users_directory = layout_organization_folder / LAYOUT_USERS_DIR
        users_file = users_directory / LAYOUT_USERS_FILE
        create_directory(users_directory)
        users = [user.to_dict(camel_case=True) for user in self.users]
        write_layout_to_file(users_file, users)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeUser(Base):
    id: str
    email: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    auth_id: Optional[str] = None
    user_groups: list[CatalogDeclarativeUserGroupIdentifier] = attr.field(factory=list)
    settings: list[CatalogDeclarativeSetting] = attr.field(factory=list)
    permissions: list[CatalogDeclarativeUserPermission] = attr.field(factory=list)

    @staticmethod
    def client_class() -> type[DeclarativeUser]:
        return DeclarativeUser


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeUserPermission(Base):
    name: str = attr.field(validator=value_in_allowed)
    assignee: CatalogAssigneeIdentifier

    @staticmethod
    def client_class() -> type[DeclarativeUserPermission]:
        return DeclarativeUserPermission

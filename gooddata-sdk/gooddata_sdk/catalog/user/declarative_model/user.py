# (C) 2022 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Type

import attr

from gooddata_metadata_client.model.declarative_user import DeclarativeUser
from gooddata_metadata_client.model.declarative_users import DeclarativeUsers
from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.identifier import CatalogUserGroupIdentifier
from gooddata_sdk.utils import create_directory, get_sorted_yaml_files, read_layout_from_file, write_layout_to_file

LAYOUT_USERS_DIR = "users"


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeUsers(Base):
    users: List[CatalogDeclarativeUser]

    @staticmethod
    def client_class() -> Type[DeclarativeUsers]:
        return DeclarativeUsers

    @classmethod
    def load_from_disk(cls, layout_organization_folder: Path) -> CatalogDeclarativeUsers:
        users_directory = layout_organization_folder / LAYOUT_USERS_DIR
        user_files = get_sorted_yaml_files(users_directory)
        users = []
        for user_file in user_files:
            users.append(CatalogDeclarativeUser.load_from_disk(user_file))
        return cls(users=users)

    def store_to_disk(self, layout_organization_folder: Path) -> None:
        users_directory = layout_organization_folder / LAYOUT_USERS_DIR
        create_directory(users_directory)
        for user in self.users:
            user.store_to_disk(users_directory)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeUser(Base):
    id: str
    auth_id: Optional[str] = None
    user_groups: List[CatalogUserGroupIdentifier] = []

    @staticmethod
    def client_class() -> Type[DeclarativeUser]:
        return DeclarativeUser

    def store_to_disk(self, users_directory: Path) -> None:
        user_path = users_directory / f"{self.id}.yaml"
        user_data = self.to_dict(camel_case=True)
        write_layout_to_file(user_path, user_data)

    @classmethod
    def load_from_disk(cls, users_directory: Path) -> CatalogDeclarativeUser:
        data = read_layout_from_file(users_directory)
        return cls.from_dict(data, camel_case=True)

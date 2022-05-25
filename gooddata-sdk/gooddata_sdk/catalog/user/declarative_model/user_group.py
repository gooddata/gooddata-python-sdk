# (C) 2022 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Type

import attr

from gooddata_metadata_client.model.declarative_user_group import DeclarativeUserGroup
from gooddata_metadata_client.model.declarative_user_groups import DeclarativeUserGroups
from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.identifier import CatalogUserGroupIdentifier
from gooddata_sdk.utils import create_directory, get_sorted_yaml_files, read_layout_from_file, write_layout_to_file

LAYOUT_USER_GROUPS_DIR = "user_groups"


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeUserGroups(Base):
    user_groups: List[CatalogDeclarativeUserGroup] = []

    @staticmethod
    def client_class() -> Type[DeclarativeUserGroups]:
        return DeclarativeUserGroups

    @classmethod
    def load_from_disk(cls, layout_organization_folder: Path) -> CatalogDeclarativeUserGroups:
        user_groups_directory = layout_organization_folder / LAYOUT_USER_GROUPS_DIR
        user_group_files = get_sorted_yaml_files(user_groups_directory)
        user_groups = []
        for user_group_file in user_group_files:
            user_groups.append(CatalogDeclarativeUserGroup.load_from_disk(user_group_file))
        return cls(user_groups=user_groups)

    def store_to_disk(self, layout_organization_folder: Path) -> None:
        user_groups_directory = layout_organization_folder / LAYOUT_USER_GROUPS_DIR
        create_directory(user_groups_directory)
        for user_group in self.user_groups:
            user_group.store_to_disk(user_groups_directory)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeUserGroup(Base):
    id: str
    parents: Optional[List[CatalogUserGroupIdentifier]] = None

    @staticmethod
    def client_class() -> Type[DeclarativeUserGroup]:
        return DeclarativeUserGroup

    def store_to_disk(self, user_groups_directory: Path) -> None:
        user_group_path = user_groups_directory / f"{self.id}.yaml"
        user_data = self.to_dict(camel_case=True)
        write_layout_to_file(user_group_path, user_data)

    @classmethod
    def load_from_disk(cls, user_groups_directory: Path) -> CatalogDeclarativeUserGroup:
        data = read_layout_from_file(user_groups_directory)
        return cls.from_dict(data, camel_case=True)

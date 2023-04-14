# (C) 2022 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Type

import attr

from gooddata_api_client.model.declarative_user_group import DeclarativeUserGroup
from gooddata_api_client.model.declarative_user_groups import DeclarativeUserGroups
from gooddata_sdk import CatalogDeclarativeWorkspaceHierarchyPermission
from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.identifier import CatalogUserGroupIdentifier
from gooddata_sdk.utils import create_directory, read_layout_from_file, write_layout_to_file

LAYOUT_USER_GROUPS_DIR = "user_groups"
LAYOUT_USER_GROUPS_FILE = "user_groups.yaml"


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeUserGroups(Base):
    user_groups: List[CatalogDeclarativeUserGroup] = attr.field(factory=list)

    @staticmethod
    def client_class() -> Type[DeclarativeUserGroups]:
        return DeclarativeUserGroups

    @classmethod
    def load_from_disk(cls, layout_organization_folder: Path) -> CatalogDeclarativeUserGroups:
        user_groups_directory = layout_organization_folder / LAYOUT_USER_GROUPS_DIR
        user_groups_file = user_groups_directory / LAYOUT_USER_GROUPS_FILE
        data = read_layout_from_file(user_groups_file)
        user_groups = []
        for record in data:
            user_groups.append(CatalogDeclarativeUserGroup.from_dict(record, camel_case=True))
        return cls(user_groups=user_groups)

    def store_to_disk(self, layout_organization_folder: Path) -> None:
        user_groups_directory = layout_organization_folder / LAYOUT_USER_GROUPS_DIR
        user_groups_file = user_groups_directory / LAYOUT_USER_GROUPS_FILE
        create_directory(user_groups_directory)
        user_groups = [user_group.to_dict(camel_case=True) for user_group in self.user_groups]
        write_layout_to_file(user_groups_file, user_groups)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeUserGroup(Base):
    id: str
    parents: Optional[List[CatalogUserGroupIdentifier]] = None
    permissions: List[CatalogDeclarativeWorkspaceHierarchyPermission] = attr.field(factory=list)

    @staticmethod
    def client_class() -> Type[DeclarativeUserGroup]:
        return DeclarativeUserGroup

# (C) 2022 GoodData Corporation
from __future__ import annotations

import functools
from pathlib import Path
from typing import List

from gooddata_api_client.exceptions import NotFoundException
from gooddata_sdk.catalog.catalog_service_base import CatalogServiceBase
from gooddata_sdk.catalog.user.declarative_model.user import CatalogDeclarativeUsers
from gooddata_sdk.catalog.user.declarative_model.user_and_user_groups import CatalogDeclarativeUsersUserGroups
from gooddata_sdk.catalog.user.declarative_model.user_group import CatalogDeclarativeUserGroups
from gooddata_sdk.catalog.user.entity_model.user import CatalogUser, CatalogUserDocument
from gooddata_sdk.catalog.user.entity_model.user_group import CatalogUserGroup, CatalogUserGroupDocument
from gooddata_sdk.utils import load_all_entities, load_all_entities_dict


class CatalogUserService(CatalogServiceBase):

    # Entity methods for users

    def create_or_update_user(self, user: CatalogUser) -> None:
        try:
            self.get_user(user_id=user.id)
            user_document = CatalogUserDocument(data=user)
            self._entities_api.update_entity_users(id=user.id, json_api_user_in_document=user_document.to_api())
        except NotFoundException:
            user_document = CatalogUserDocument(data=user)
            self._entities_api.create_entity_users(json_api_user_in_document=user_document.to_api())

    def get_user(self, user_id: str) -> CatalogUser:
        user_dict = self._entities_api.get_entity_users(id=user_id, include=["userGroups"]).data.to_dict(
            camel_case=False
        )
        return CatalogUser.from_dict(user_dict, camel_case=False)

    def delete_user(self, user_id: str) -> None:
        self._entities_api.delete_entity_users(id=user_id)

    def list_users(self) -> List[CatalogUser]:
        get_users = functools.partial(
            self._entities_api.get_all_entities_users,
            include=["userGroups"],
            _check_return_type=False,
        )
        users = load_all_entities_dict(get_users, camel_case=False)
        return [CatalogUser.from_dict(v, camel_case=False) for v in users["data"]]

    # Entity methods for user groups

    def create_or_update_user_group(self, user_group: CatalogUserGroup) -> None:
        try:
            self.get_user_group(user_group_id=user_group.id)
            user_group_document = CatalogUserGroupDocument(data=user_group)
            user_group_document.update_user_group(user_group_parents_id=user_group.get_parents)
            self._entities_api.update_entity_user_groups(
                id=user_group.id, json_api_user_group_in_document=user_group_document.to_api()
            )
        except NotFoundException:
            user_group_document = CatalogUserGroupDocument.init(
                user_group_id=user_group.id, user_group_parent_ids=user_group.get_parents
            )
            self._entities_api.create_entity_user_groups(user_group_document.to_api())

    def get_user_group(self, user_group_id: str) -> CatalogUserGroup:
        user_group = self._entities_api.get_entity_user_groups(id=user_group_id, include=["ALL"]).data.to_dict(
            camel_case=False
        )
        return CatalogUserGroup.from_dict(user_group, camel_case=False)

    def delete_user_group(self, user_group_id: str) -> None:
        self._entities_api.delete_entity_user_groups(id=user_group_id)

    def list_user_groups(self) -> List[CatalogUserGroup]:
        get_user_groups = functools.partial(
            self._entities_api.get_all_entities_user_groups,
            include=["userGroups"],
            _check_return_type=False,
        )
        user_groups = load_all_entities(get_user_groups)
        return [CatalogUserGroup.from_api(v) for v in user_groups.data]

    # Declarative methods for users

    def get_declarative_users(self) -> CatalogDeclarativeUsers:
        return CatalogDeclarativeUsers.from_api(self._layout_api.get_users_layout())

    def put_declarative_users(self, users: CatalogDeclarativeUsers) -> None:
        self._layout_api.put_users_layout(users.to_api())

    def store_declarative_users(self, layout_root_path: Path = Path.cwd()) -> None:
        self.get_declarative_users().store_to_disk(self.layout_organization_folder(layout_root_path))

    def load_declarative_users(self, layout_root_path: Path = Path.cwd()) -> CatalogDeclarativeUsers:
        return CatalogDeclarativeUsers.load_from_disk(self.layout_organization_folder(layout_root_path))

    def load_and_put_declarative_users(self, layout_root_path: Path = Path.cwd()) -> None:
        declarative_users = self.load_declarative_users(layout_root_path)
        self.put_declarative_users(declarative_users)

    # Declarative methods for user groups

    def get_declarative_user_groups(self) -> CatalogDeclarativeUserGroups:
        return CatalogDeclarativeUserGroups.from_api(self._layout_api.get_user_groups_layout())

    def put_declarative_user_groups(self, user_groups: CatalogDeclarativeUserGroups) -> None:
        self._layout_api.put_user_groups_layout(user_groups.to_api())

    def load_declarative_user_groups(self, layout_root_path: Path = Path.cwd()) -> CatalogDeclarativeUserGroups:
        return CatalogDeclarativeUserGroups.load_from_disk(self.layout_organization_folder(layout_root_path))

    def store_declarative_user_groups(self, layout_root_path: Path = Path.cwd()) -> None:
        self.get_declarative_user_groups().store_to_disk(self.layout_organization_folder(layout_root_path))

    def load_and_put_declarative_user_groups(self, layout_root_path: Path = Path.cwd()) -> None:
        declarative_user_groups = self.load_declarative_user_groups(layout_root_path)
        self.put_declarative_user_groups(declarative_user_groups)

    # Declarative methods for usersUserGroups

    def get_declarative_users_user_groups(self) -> CatalogDeclarativeUsersUserGroups:
        return CatalogDeclarativeUsersUserGroups.from_api(self._layout_api.get_users_user_groups_layout())

    def put_declarative_users_user_groups(self, users_user_groups: CatalogDeclarativeUsersUserGroups) -> None:
        self._layout_api.put_users_user_groups_layout(declarative_users_user_groups=users_user_groups.to_api())

    def load_declarative_users_user_groups(
        self, layout_root_path: Path = Path.cwd()
    ) -> CatalogDeclarativeUsersUserGroups:
        return CatalogDeclarativeUsersUserGroups.load_from_disk(
            layout_organization_folder=self.layout_organization_folder(layout_root_path)
        )

    def store_declarative_users_user_groups(self, layout_root_path: Path = Path.cwd()) -> None:
        self.get_declarative_users_user_groups().store_to_disk(self.layout_organization_folder(layout_root_path))

    def load_and_put_declarative_users_user_groups(self, layout_root_path: Path = Path.cwd()) -> None:
        declarative_users_user_groups = self.load_declarative_users_user_groups(layout_root_path)
        self.put_declarative_users_user_groups(declarative_users_user_groups)

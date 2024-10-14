# (C) 2022 GoodData Corporation
from __future__ import annotations

import functools
from pathlib import Path

from gooddata_api_client.exceptions import NotFoundException
from gooddata_api_client.model.json_api_api_token_in import JsonApiApiTokenIn
from gooddata_api_client.model.json_api_api_token_in_document import JsonApiApiTokenInDocument

from gooddata_sdk.catalog.catalog_service_base import CatalogServiceBase
from gooddata_sdk.catalog.user.declarative_model.user import CatalogDeclarativeUsers
from gooddata_sdk.catalog.user.declarative_model.user_and_user_groups import CatalogDeclarativeUsersUserGroups
from gooddata_sdk.catalog.user.declarative_model.user_group import CatalogDeclarativeUserGroups
from gooddata_sdk.catalog.user.entity_model.api_token import CatalogApiToken
from gooddata_sdk.catalog.user.entity_model.user import CatalogUser, CatalogUserDocument
from gooddata_sdk.catalog.user.entity_model.user_group import CatalogUserGroup, CatalogUserGroupDocument
from gooddata_sdk.catalog.user.management_model.management import (
    CatalogPermissionAssignments,
    CatalogPermissionsAssignment,
)
from gooddata_sdk.utils import load_all_entities, load_all_entities_dict


class CatalogUserService(CatalogServiceBase):
    # Entity methods for users

    def create_or_update_user(self, user: CatalogUser) -> None:
        """Creates a new user or overwrites an existing user.


        Args:
            user (CatalogUser):
                User entity object.

        Returns:
            None
        """
        try:
            self.get_user(user_id=user.id)
            user_document = CatalogUserDocument(data=user)
            self._entities_api.update_entity_users(id=user.id, json_api_user_in_document=user_document.to_api())
        except NotFoundException:
            user_document = CatalogUserDocument(data=user)
            self._entities_api.create_entity_users(json_api_user_in_document=user_document.to_api())

    def get_user(self, user_id: str) -> CatalogUser:
        """Get an individual user using User id.

        Args:
            user_id (str):
                User identification string. e.g. "123"

        Returns:
            CatalogUser:
                User entity object.
        """
        user_dict = self._entities_api.get_entity_users(id=user_id, include=["userGroups"]).data.to_dict(
            camel_case=False
        )
        return CatalogUser.from_dict(user_dict, camel_case=False)

    def delete_user(self, user_id: str) -> None:
        """Delete User using User id.

        Args:
            user_id (str):
                User identification string. e.g. "123"

        Returns:
            None
        """
        self._entities_api.delete_entity_users(id=user_id)

    def list_users(self) -> list[CatalogUser]:
        """Get a list of all existing users.

        Args:
            None

        Returns:
            list[CatalogUser]:
                List of all Users as User entity objects.
        """
        get_users = functools.partial(
            self._entities_api.get_all_entities_users,
            include=["userGroups"],
            _check_return_type=False,
        )
        users = load_all_entities_dict(get_users, camel_case=False)
        return [CatalogUser.from_dict(v, camel_case=False) for v in users["data"]]

    # Entity methods for user groups

    def create_or_update_user_group(self, user_group: CatalogUserGroup) -> None:
        """Create a new user group or overwrite an existing user group.

        Args:
            user_group (CatalogUserGroup):
                UserGroup entity object.

        Returns:
            None
        """
        try:
            self.get_user_group(user_group_id=user_group.id)
            user_group_document = CatalogUserGroupDocument(data=user_group)
            self._entities_api.update_entity_user_groups(
                id=user_group.id, json_api_user_group_in_document=user_group_document.to_api()
            )
        except NotFoundException:
            user_group_document = CatalogUserGroupDocument(data=user_group)
            self._entities_api.create_entity_user_groups(user_group_document.to_api())

    def get_user_group(self, user_group_id: str) -> CatalogUserGroup:
        """Get an individual user group using user group id.

        Args:
            user_group_id (str):
                User Group identification string. e.g. "123"

        Returns:
            CatalogUserGroup:
                UserGroup entity object.
        """
        user_group = self._entities_api.get_entity_user_groups(id=user_group_id, include=["ALL"]).data.to_dict(
            camel_case=False
        )
        return CatalogUserGroup.from_dict(user_group, camel_case=False)

    def delete_user_group(self, user_group_id: str) -> None:
        """Delete User Group using User Group id.

        Args:
            user_group_id (str):
                User Group identification string. e.g. "123"

        Returns:
            None
        """
        self._entities_api.delete_entity_user_groups(id=user_group_id)

    def list_user_groups(self) -> list[CatalogUserGroup]:
        """Get a list of all existing user groups.

        Args:
            None

        Returns:
            list[CatalogUserGroup]:
                List of all User groups as UserGroup entity object.
        """
        get_user_groups = functools.partial(
            self._entities_api.get_all_entities_user_groups,
            include=["userGroups"],
            _check_return_type=False,
        )
        user_groups = load_all_entities(get_user_groups)
        return [CatalogUserGroup.from_api(v) for v in user_groups.data]

    # Declarative methods for users

    def get_declarative_users(self) -> CatalogDeclarativeUsers:
        """Retrieve all users in a declarative form.

        Args:
            None

        Returns:
            CatalogDeclarativeUsers:
                Declarative Users object.
        """
        return CatalogDeclarativeUsers.from_api(self._layout_api.get_users_layout())

    def put_declarative_users(self, users: CatalogDeclarativeUsers) -> None:
        """Set all users and their authentication properties.

        Args:
            users (CatalogDeclarativeUsers):
                Declarative Users object, incuding authetication properties.

        Returns:
            None
        """
        self._layout_api.put_users_layout(users.to_api())

    def store_declarative_users(self, layout_root_path: Path = Path.cwd()) -> None:
        """Store users in directory hierarchy. Directly from server.

        Args:
            layout_root_path (Path, optional):
                Path to the root of the layout directory.. Defaults to Path.cwd().

        Returns:
            None
        """
        self.get_declarative_users().store_to_disk(self.layout_organization_folder(layout_root_path))

    def load_declarative_users(self, layout_root_path: Path = Path.cwd()) -> CatalogDeclarativeUsers:
        """Load declarative users layout, which was stored using store_declarative_users.

        Args:
            layout_root_path (Path, optional):
                Path to the root of the layout directory.. Defaults to Path.cwd().

        Returns:
            CatalogDeclarativeUsers:
                Declarative Users object, incuding authetication properties.
        """
        return CatalogDeclarativeUsers.load_from_disk(self.layout_organization_folder(layout_root_path))

    def load_and_put_declarative_users(self, layout_root_path: Path = Path.cwd()) -> None:
        """Loads and sets the layouts stored using `store_declarative_users`.

        This method combines `load_declarative_users` and `put_declarative_users`
        methods to load and set layouts stored using `store_declarative_users`.

        Args:
            layout_root_path (Path, optional):
                Path to the root of the layout directory.. Defaults to Path.cwd().

        Returns:
            None
        """
        declarative_users = self.load_declarative_users(layout_root_path)
        self.put_declarative_users(declarative_users)

    # Declarative methods for user groups

    def get_declarative_user_groups(self) -> CatalogDeclarativeUserGroups:
        """Retrieve all user groups in a declarative form.


        Args:
            None

        Returns:
            CatalogDeclarativeUserGroups:
                Declarative User Groups object.
        """
        return CatalogDeclarativeUserGroups.from_api(self._layout_api.get_user_groups_layout())

    def put_declarative_user_groups(self, user_groups: CatalogDeclarativeUserGroups) -> None:
        """Set all user groups eventually with their parents.

        Args:
            user_groups (CatalogDeclarativeUserGroups):
                Declarative User Groups object.


        Returns:
            None
        """
        self._layout_api.put_user_groups_layout(user_groups.to_api())

    def load_declarative_user_groups(self, layout_root_path: Path = Path.cwd()) -> CatalogDeclarativeUserGroups:
        """Load declarative users groups layout, which was stored using `store_declarative_user_groups`.

        Args:
            layout_root_path (Path, optional):
                Path to the root of the layout directory.. Defaults to Path.cwd().

        Returns:
            CatalogDeclarativeUserGroups:
                Declarative User Groups object.
        """
        return CatalogDeclarativeUserGroups.load_from_disk(self.layout_organization_folder(layout_root_path))

    def store_declarative_user_groups(self, layout_root_path: Path = Path.cwd()) -> None:
        """Stores all the user groups in a directory hierarchy.

        Args:
            layout_root_path (Path, optional):
                Path to the root of the layout directory.. Defaults to Path.cwd().


        Returns:
            None
        """
        self.get_declarative_user_groups().store_to_disk(self.layout_organization_folder(layout_root_path))

    def load_and_put_declarative_user_groups(self, layout_root_path: Path = Path.cwd()) -> None:
        """Loads and sets the layouts stored using `store_declarative_users`.

        This method combines load_declarative_users and put_declarative_users
        methods to load and set layouts stored using store_declarative_users.

        Args:
            layout_root_path (Path, optional):
                Path to the root of the layout directory.. Defaults to Path.cwd().


        Returns:
            None
        """
        declarative_user_groups = self.load_declarative_user_groups(layout_root_path)
        self.put_declarative_user_groups(declarative_user_groups)

    # Declarative methods for usersUserGroups

    def get_declarative_users_user_groups(self) -> CatalogDeclarativeUsersUserGroups:
        """Retrieves all users and user groups in a declarative form.


        Args:
            None

        Returns:
            CatalogDeclarativeUsersUserGroups:
                Declarative Users and User Groups object.
        """
        return CatalogDeclarativeUsersUserGroups.from_api(self._layout_api.get_users_user_groups_layout())

    def put_declarative_users_user_groups(self, users_user_groups: CatalogDeclarativeUsersUserGroups) -> None:
        """Set all users and user groups.

        Args:
            users_user_groups (CatalogDeclarativeUsersUserGroups):
                Declarative Users and User Groups object.

        Returns:
            None
        """
        self._layout_api.put_users_user_groups_layout(declarative_users_user_groups=users_user_groups.to_api())

    def load_declarative_users_user_groups(
        self, layout_root_path: Path = Path.cwd()
    ) -> CatalogDeclarativeUsersUserGroups:
        """Load declarative users and user groups layout, which was stored using `store_declarative_users_user_groups`.

        Args:
            layout_root_path (Path, optional):
                Path to the root of the layout directory.. Defaults to Path.cwd().

        Returns:
            CatalogDeclarativeUsersUserGroups:
                Declarative Users and User Groups object.
        """
        return CatalogDeclarativeUsersUserGroups.load_from_disk(
            layout_organization_folder=self.layout_organization_folder(layout_root_path)
        )

    def store_declarative_users_user_groups(self, layout_root_path: Path = Path.cwd()) -> None:
        """Stores all the users and user groups in a directory hierarchy.

        Args:
            layout_root_path (Path, optional):
                Path to the root of the layout directory.. Defaults to Path.cwd().



        Returns:
            None
        """
        self.get_declarative_users_user_groups().store_to_disk(self.layout_organization_folder(layout_root_path))

    def load_and_put_declarative_users_user_groups(self, layout_root_path: Path = Path.cwd()) -> None:
        """Loads and sets the layouts stored using `store_declarative_users_user_groups`.

        This method combines `load_declarative_users` and `put_declarative_users_user_groups`
        methods to load and set layouts stored using `store_declarative_users_user_groups`.

        Args:
            layout_root_path (Path, optional):
                Path to the root of the layout directory.. Defaults to Path.cwd().


        Returns:
            None
        """
        declarative_users_user_groups = self.load_declarative_users_user_groups(layout_root_path)
        self.put_declarative_users_user_groups(declarative_users_user_groups)

    # User management use case APIs

    def get_user_permissions(self, user_id: str) -> CatalogPermissionAssignments:
        return CatalogPermissionAssignments.from_api(self._user_management_api.list_permissions_for_user(user_id))

    def manage_user_permissions(self, user_id: str, permission_assignments: CatalogPermissionAssignments) -> None:
        self._user_management_api.manage_permissions_for_user(user_id, permission_assignments.to_api())

    def get_user_group_permissions(self, user_group_id: str) -> CatalogPermissionAssignments:
        return CatalogPermissionAssignments.from_api(
            self._user_management_api.list_permissions_for_user_group(user_group_id)
        )

    def manage_user_group_permissions(
        self, user_group_id: str, permission_assignments: CatalogPermissionAssignments
    ) -> None:
        self._user_management_api.manage_permissions_for_user_group(user_group_id, permission_assignments.to_api())

    def assign_permissions_bulk(self, permissions_assignment: CatalogPermissionsAssignment) -> None:
        self._user_management_api.assign_permissions(permissions_assignment.to_api())

    def revoke_permissions_bulk(self, permissions_assignment: CatalogPermissionsAssignment) -> None:
        self._user_management_api.revoke_permissions(permissions_assignment.to_api())

    def list_user_api_tokens(self, user_id: str) -> list[CatalogApiToken]:
        get_api_tokens = functools.partial(
            self._entities_api.get_all_entities_api_tokens,
            user_id,
            _check_return_type=False,
        )
        api_tokens = load_all_entities(get_api_tokens)
        return [CatalogApiToken(id=v["id"]) for v in api_tokens.data]

    def create_user_api_token(self, user_id: str, api_token_id: str) -> CatalogApiToken:
        document = JsonApiApiTokenInDocument(data=JsonApiApiTokenIn(id=api_token_id, type="apiToken"))
        api_token = self._entities_api.create_entity_api_tokens(user_id, document, _check_return_type=False)
        v = api_token.data
        return CatalogApiToken(id=v["id"], bearer_token=v.get("attributes", {}).get("bearerToken"))

    def get_user_api_token(self, user_id: str, api_token_id: str) -> CatalogApiToken:
        api_token = self._entities_api.get_entity_api_tokens(user_id, api_token_id, _check_return_type=False)
        v = api_token.data
        return CatalogApiToken(id=v["id"])

    def delete_user_api_token(self, user_id: str, api_token_id: str) -> None:
        self._entities_api.delete_entity_api_tokens(user_id, api_token_id)

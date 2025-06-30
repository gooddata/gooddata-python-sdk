# (C) 2025 GoodData Corporation
from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterator, TypeAlias

from gooddata_sdk.catalog.identifier import CatalogAssigneeIdentifier
from gooddata_sdk.catalog.permission.declarative_model.permission import (
    CatalogDeclarativeSingleWorkspacePermission,
    CatalogDeclarativeWorkspacePermissions,
)

from gooddata_pipelines.provisioning.utils.exceptions import BaseUserException

# TODO: refactor the full load and incremental load models to reuse as much as possible
# TODO: use pydantic models instead of dataclasses?
# TODO: make the validation logic more readable (as in PermissionIncrementalLoad)

TargetsPermissionDict: TypeAlias = dict[str, dict[str, bool]]


class PermissionType(Enum):
    user = "user"
    user_group = "userGroup"


@dataclass(frozen=True)
class PermissionIncrementalLoad:
    permission: str
    workspace_id: str
    id: str
    type: PermissionType
    is_active: bool

    @classmethod
    def from_list_of_dicts(
        cls, data: list[dict[str, Any]]
    ) -> list["PermissionIncrementalLoad"]:
        """Creates a list of User objects from list of dicts."""
        id: str
        permissions = []
        for permission in data:
            user_id: str | None = permission.get("user_id")
            user_group_id: str | None = permission.get("ug_id")

            if user_id is not None:
                target_type = PermissionType.user
                id = user_id
            elif user_group_id is not None:
                target_type = PermissionType.user_group
                id = user_group_id

            permissions.append(
                PermissionIncrementalLoad(
                    permission=permission["ws_permissions"],
                    workspace_id=permission["ws_id"],
                    id=id,
                    type=target_type,
                    is_active=str(permission["is_active"]).lower() == "true",
                )
            )
        return permissions


@dataclass(frozen=True)
class PermissionFullLoad:
    permission: str
    workspace_id: str
    id: str
    type: PermissionType

    @classmethod
    def from_list_of_dicts(
        cls, data: list[dict[str, Any]]
    ) -> list["PermissionFullLoad"]:
        """Creates a list of User objects from list of dicts."""
        permissions = []
        for permission in data:
            id = (
                permission["user_id"]
                if permission["user_id"]
                else permission["ug_id"]
            )

            if permission["user_id"]:
                target_type = PermissionType.user
            else:
                target_type = PermissionType.user_group

            permissions.append(
                PermissionFullLoad(
                    permission=permission["ws_permissions"],
                    workspace_id=permission["ws_id"],
                    id=id,
                    type=target_type,
                )
            )
        return permissions


@dataclass
class PermissionDeclaration:
    users: TargetsPermissionDict
    user_groups: TargetsPermissionDict

    @classmethod
    def from_sdk_api(
        cls, declaration: CatalogDeclarativeWorkspacePermissions
    ) -> "PermissionDeclaration":
        """
        Constructs an WSPermissionDeclaration instance
        from GoodData SDK CatalogDeclarativeWorkspacePermissions.
        """
        users: TargetsPermissionDict = {}
        user_groups: TargetsPermissionDict = {}

        for permission in declaration.permissions:
            permission_type, id = (
                permission.assignee.type,
                permission.assignee.id,
            )

            if permission_type == PermissionType.user.value:
                target_dict = users
            else:
                target_dict = user_groups

            id_permissions = target_dict.get(id)
            if not id_permissions:
                target_dict[id] = dict()

            target_dict[id][permission.name] = True

        return PermissionDeclaration(users, user_groups)

    @staticmethod
    def _construct_upstream_permission(
        permission: str, assignee: CatalogAssigneeIdentifier
    ) -> CatalogDeclarativeSingleWorkspacePermission | None:
        """Constructs single permission declaration for the SDK API."""
        try:
            return CatalogDeclarativeSingleWorkspacePermission(
                name=permission, assignee=assignee
            )
        except Exception as e:
            raise BaseUserException(
                f"Failed to construct SDK declaration for type={assignee.type} ",
                f"id={assignee.id}. Error: {e}",
            )

    def _permissions_for_target(
        self, permissions: dict[str, bool], assignee: CatalogAssigneeIdentifier
    ) -> Iterator[CatalogDeclarativeSingleWorkspacePermission]:
        """Constructs permission declarations for a single target."""
        for permission, is_active in permissions.items():
            if not is_active:
                continue
            declaration = self._construct_upstream_permission(
                permission, assignee
            )
            if not declaration:
                continue
            yield declaration

    def to_sdk_api(self) -> CatalogDeclarativeWorkspacePermissions:
        """
        Constructs the GoodData SDK CatalogDeclarativeWorkspacePermissions
        object from the WSPermissionDeclaration instance.
        """
        permission_declarations: list[
            CatalogDeclarativeSingleWorkspacePermission
        ] = []

        for user_id, permissions in self.users.items():
            assignee = CatalogAssigneeIdentifier(
                id=user_id, type=PermissionType.user.value
            )
            for declaration in self._permissions_for_target(
                permissions, assignee
            ):
                permission_declarations.append(declaration)

        for ug_id, permissions in self.user_groups.items():
            assignee = CatalogAssigneeIdentifier(
                id=ug_id, type=PermissionType.user_group.value
            )
            for declaration in self._permissions_for_target(
                permissions, assignee
            ):
                permission_declarations.append(declaration)

        return CatalogDeclarativeWorkspacePermissions(
            permissions=permission_declarations
        )

    def add_permission(self, permission: PermissionIncrementalLoad) -> None:
        """
        Adds WSPermission object into respective field within the instance.
        Handles duplicate permissions and different combinations of input
        and upstream is_active permission states.
        """
        target_dict = (
            self.users
            if permission.type == PermissionType.user
            else self.user_groups
        )

        if permission.id not in target_dict:
            target_dict[permission.id] = {}

        is_active = permission.is_active
        target_permissions = target_dict[permission.id]
        permission_value = permission.permission

        if permission_value not in target_permissions:
            target_permissions[permission_value] = is_active
        elif not is_active and target_permissions[permission_value] is True:
            print(
                "isActive=False provided after True has been specificed for the "
                + f"same input. Skipping '{permission}'"
            )
        elif is_active and target_permissions[permission_value] is False:
            print(
                "isActive=True provided after False has been specified for the "
                + f"same input. Overwriting '{permission}'"
            )
            target_permissions[permission_value] = is_active

    def upsert(self, other: "PermissionDeclaration") -> None:
        """
        Modifies the owner object by merging with the other.
        Keeps the unmodified users/userGroups untouched.
        If some user/userGroup is modified, it gets overwritten with permissions
        defined in the input.
        """
        for user_id, permissions in other.users.items():
            self.users[user_id] = permissions

        for ug_id, permissions in other.user_groups.items():
            self.user_groups[ug_id] = permissions


WSPermissionsDeclarations: TypeAlias = dict[str, PermissionDeclaration]

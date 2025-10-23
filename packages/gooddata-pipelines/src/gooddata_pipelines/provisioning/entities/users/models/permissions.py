# (C) 2025 GoodData Corporation

from enum import Enum
from typing import Iterator, TypeAlias

import attrs
from gooddata_sdk.catalog.identifier import CatalogAssigneeIdentifier
from gooddata_sdk.catalog.permission.declarative_model.permission import (
    CatalogDeclarativeSingleWorkspacePermission,
    CatalogDeclarativeWorkspacePermissions,
)
from pydantic import BaseModel, ConfigDict

from gooddata_pipelines.provisioning.utils.exceptions import BaseUserException

TargetsPermissionDict: TypeAlias = dict[str, dict[str, bool]]


class EntityType(str, Enum):
    # NOTE: Start using StrEnum with Python 3.11
    user = "user"
    user_group = "userGroup"


class BasePermission(BaseModel):
    model_config = ConfigDict(extra="forbid")

    permission: str
    workspace_id: str
    entity_id: str
    entity_type: EntityType


class PermissionFullLoad(BasePermission):
    """Input validator for full load of workspace permissions provisioning."""


class PermissionIncrementalLoad(BasePermission):
    """Input validator for incremental load of workspace permissions provisioning."""

    is_active: bool


@attrs.define
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

            if permission_type == EntityType.user.value:
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
                id=user_id, type=EntityType.user.value
            )
            for declaration in self._permissions_for_target(
                permissions, assignee
            ):
                permission_declarations.append(declaration)

        for ug_id, permissions in self.user_groups.items():
            assignee = CatalogAssigneeIdentifier(
                id=ug_id, type=EntityType.user_group.value
            )
            for declaration in self._permissions_for_target(
                permissions, assignee
            ):
                permission_declarations.append(declaration)

        return CatalogDeclarativeWorkspacePermissions(
            permissions=permission_declarations
        )

    def add_incremental_permission(
        self, permission: PermissionIncrementalLoad
    ) -> None:
        """
        Adds WSPermission object into respective field within the instance.
        Handles duplicate permissions and different combinations of input
        and upstream is_active permission states.
        """
        target_dict = (
            self.users
            if permission.entity_type == EntityType.user
            else self.user_groups
        )

        if permission.entity_id not in target_dict:
            target_dict[permission.entity_id] = {}

        is_active = permission.is_active
        target_permissions = target_dict[permission.entity_id]
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

    def add_full_load_permission(self, permission: PermissionFullLoad) -> None:
        """
        Adds WSPermission object into respective field within the instance.
        Handles duplicate permissions and different combinations of input
        and upstream is_active permission states.
        """
        target_dict = (
            self.users
            if permission.entity_type == EntityType.user
            else self.user_groups
        )

        if permission.entity_id not in target_dict:
            target_dict[permission.entity_id] = {}

        target_permissions = target_dict[permission.entity_id]
        permission_value = permission.permission

        if permission_value not in target_permissions:
            target_permissions[permission_value] = True

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

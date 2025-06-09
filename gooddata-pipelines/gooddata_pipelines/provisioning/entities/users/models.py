# (C) 2025 GoodData Corporation

"""Dataclass models for user, user group and permission provisioning."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterator, TypeAlias

from gooddata_sdk.catalog.identifier import CatalogAssigneeIdentifier
from gooddata_sdk.catalog.permission.declarative_model.permission import (
    CatalogDeclarativeSingleWorkspacePermission,
    CatalogDeclarativeWorkspacePermissions,
)
from gooddata_sdk.catalog.user.entity_model.user import CatalogUser

from gooddata_pipelines.provisioning.utils.exceptions import BaseUserException
from gooddata_pipelines.provisioning.utils.utils import SplitMixin

TargetsPermissionDict: TypeAlias = dict[str, dict[str, bool]]


class PermissionType(Enum):
    user = "user"
    user_group = "userGroup"


@dataclass(frozen=True)
class Permission:
    permission: str
    workspace_id: str
    id: str
    type: PermissionType
    is_active: bool

    @classmethod
    def from_list_of_dicts(
        cls, data: list[dict[str, Any]]
    ) -> list["Permission"]:
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
                Permission(
                    permission=permission["ws_permissions"],
                    workspace_id=permission["ws_id"],
                    id=id,
                    type=target_type,
                    is_active=str(permission["is_active"]).lower() == "true",
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

    def add_permission(self, permission: Permission) -> None:
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


@dataclass
class User(SplitMixin):
    user_id: str
    firstname: str | None
    lastname: str | None
    email: str | None
    auth_id: str | None
    user_groups: list[str]
    is_active: bool = field(compare=False)

    @classmethod
    def from_list_of_dicts(
        cls, data: list[dict[str, Any]], delimiter: str = ","
    ) -> list["User"]:
        """Creates a list of User objects from list of dicts."""
        converted_users = []
        for user in data:
            user_groups = cls.split(user["user_groups"], delimiter=delimiter)
            converted_users.append(
                User(
                    user_id=user["user_id"],
                    firstname=user["firstname"],
                    lastname=user["lastname"],
                    email=user["email"],
                    auth_id=user["auth_id"],
                    user_groups=user_groups,
                    is_active=user["is_active"],
                )
            )
        return converted_users

    @classmethod
    def from_sdk_obj(cls, obj: CatalogUser) -> "User":
        """Creates GDUserTarget from CatalogUser SDK object."""
        if obj.attributes:
            firstname = obj.attributes.firstname
            lastname = obj.attributes.lastname
            email = obj.attributes.email
            auth_id = obj.attributes.authentication_id
        else:
            firstname = None
            lastname = None
            email = None
            auth_id = None

        return User(
            user_id=obj.id,
            firstname=firstname,
            lastname=lastname,
            email=email,
            auth_id=auth_id,
            user_groups=[ug.id for ug in obj.user_groups],
            is_active=True,
        )

    def to_sdk_obj(self) -> CatalogUser:
        """Converts GDUserTarget to CatalogUser SDK object."""
        return CatalogUser.init(
            user_id=self.user_id,
            firstname=self.firstname,
            lastname=self.lastname,
            email=self.email,
            authentication_id=self.auth_id,
            user_group_ids=self.user_groups,
        )


@dataclass
class UserGroup(SplitMixin):
    user_group_id: str
    user_group_name: str
    parent_user_groups: list[str]
    is_active: bool = field(compare=False)

    @classmethod
    def from_list_of_dicts(
        cls, data: list[dict[str, Any]], delimiter: str = ","
    ) -> list["UserGroup"]:
        """Creates a list of User objects from list of dicts."""
        user_groups = []
        for user_group in data:
            if user_group["user_group_name"]:
                user_group_name = user_group["user_group_name"]
            else:
                user_group_name = user_group["user_group_id"]

            parent_user_groups = cls.split(
                user_group["parent_user_groups"], delimiter=delimiter
            )

            user_groups.append(
                UserGroup(
                    user_group_id=user_group["user_group_id"],
                    user_group_name=user_group_name,
                    parent_user_groups=parent_user_groups,
                    is_active=str(user_group["is_active"]).lower() == "true",
                )
            )
        return user_groups

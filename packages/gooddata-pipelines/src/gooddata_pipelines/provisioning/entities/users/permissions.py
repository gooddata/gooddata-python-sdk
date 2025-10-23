# (C) 2025 GoodData Corporation

"""Module for provisioning user permissions in GoodData workspaces."""

from typing import TypeVar

from gooddata_pipelines.api.exceptions import GoodDataApiException
from gooddata_pipelines.provisioning.entities.users.models.permissions import (
    EntityType,
    PermissionDeclaration,
    PermissionFullLoad,
    PermissionIncrementalLoad,
    TargetsPermissionDict,
    WSPermissionsDeclarations,
)
from gooddata_pipelines.provisioning.provisioning import Provisioning
from gooddata_pipelines.provisioning.utils.exceptions import BaseUserException

# Type variable for permission models (PermissionIncrementalLoad or PermissionFullLoad)
PermissionModel = TypeVar(
    "PermissionModel", PermissionIncrementalLoad, PermissionFullLoad
)


class PermissionProvisioner(
    Provisioning[PermissionFullLoad, PermissionIncrementalLoad]
):
    """Provisioning class for user permissions in GoodData workspaces.

    This class handles the provisioning of user permissions based on the provided
    source data. Use the `full_load` or `incremental_load`
    methods to run the provisioning.
    """

    source_group_incremental: list[PermissionIncrementalLoad]
    source_group_full: list[PermissionFullLoad]

    FULL_LOAD_TYPE: type[PermissionFullLoad] = PermissionFullLoad
    INCREMENTAL_LOAD_TYPE: type[PermissionIncrementalLoad] = (
        PermissionIncrementalLoad
    )

    def _get_ws_declaration(self, ws_id: str) -> PermissionDeclaration:
        users: TargetsPermissionDict = {}
        user_groups: TargetsPermissionDict = {}

        upstream_declaration = self._api.get_declarative_permissions(ws_id)

        for permission in upstream_declaration.permissions:
            permission_type, id = (
                permission.assignee.type,
                permission.assignee.id,
            )
            target_dict = (
                users
                if permission_type == EntityType.user.value
                else user_groups
            )

            id_permissions = target_dict.get(id)
            if not id_permissions:
                target_dict[id] = dict()

            target_dict[id][permission.name] = True

        return PermissionDeclaration(users, user_groups)

    def _get_upstream_declaration(
        self, ws_id: str
    ) -> PermissionDeclaration | None:
        """Retrieves upstream permission declaration for a workspace."""
        declaration = self._api.get_declarative_permissions(ws_id)
        return PermissionDeclaration.from_sdk_api(declaration)

    def _get_upstream_declarations(
        self, input_ws_ids: list[str]
    ) -> WSPermissionsDeclarations:
        """Retrieves upstream permission declarations for a list of workspaces."""
        ws_dict: WSPermissionsDeclarations = {}
        for ws_id in input_ws_ids:
            declaration = self._get_upstream_declaration(ws_id)
            if declaration:
                ws_dict[ws_id] = declaration
        return ws_dict

    @staticmethod
    def _construct_declarations(
        permissions: list[PermissionIncrementalLoad] | list[PermissionFullLoad],
    ) -> WSPermissionsDeclarations:
        """Constructs workspace permission declarations from the input permissions."""
        ws_dict: WSPermissionsDeclarations = {}
        for permission in permissions:
            ws_id = permission.workspace_id

            if ws_id not in ws_dict:
                ws_dict[ws_id] = PermissionDeclaration({}, {})

            if isinstance(permission, PermissionIncrementalLoad):
                ws_dict[ws_id].add_incremental_permission(permission)
            elif isinstance(permission, PermissionFullLoad):
                ws_dict[ws_id].add_full_load_permission(permission)
            else:
                raise ValueError(f"Invalid permission type: {type(permission)}")
        return ws_dict

    def _check_user_group_exists(self, ug_id: str) -> None:
        """Checks if user group with provided ID exists."""
        self._api._sdk.catalog_user.get_user_group(ug_id)

    def _validate_permission(
        self, permission: PermissionFullLoad | PermissionIncrementalLoad
    ) -> None:
        """Validates if the permission is correctly defined."""
        if permission.entity_type == EntityType.user:
            self._api.get_user(
                permission.entity_id, error_message="User not found"
            )
        else:
            self._api.get_user_group(
                permission.entity_id, error_message="User group not found"
            )

        self._api.get_workspace(
            permission.workspace_id, error_message="Workspace not found"
        )

    def _filter_invalid_permissions(
        self,
        permissions: list[PermissionModel],
    ) -> list[PermissionModel]:
        """Filters out invalid permissions from the input list."""
        valid_permissions: list[PermissionModel] = []

        for permission in permissions:
            try:
                self._validate_permission(permission)
            except (BaseUserException, GoodDataApiException) as e:
                self.logger.error(
                    f"Skipping {permission}. Error: {e.error_message} "
                    + f"Context: {permission.__dict__}"
                )
                continue
            valid_permissions.append(permission)
        return valid_permissions

    def _provision_incremental_load(self) -> None:
        """Provisiones permissions for a list of workspaces.

        Modifies existing upstream workspace permission declarations for each
        input workspace and skips rest of the workspaces.
        """
        valid_permissions = self._filter_invalid_permissions(
            self.source_group_incremental
        )

        input_declarations = self._construct_declarations(valid_permissions)

        input_ws_ids = list(input_declarations.keys())
        upstream_declarations = self._get_upstream_declarations(input_ws_ids)

        for ws_id, declaration in input_declarations.items():
            if ws_id not in upstream_declarations:
                continue

            upstream_declarations[ws_id].upsert(declaration)

            ws_permissions = upstream_declarations[ws_id].to_sdk_api()

            self._api.put_declarative_permissions(ws_id, ws_permissions)
            self.logger.info(f"Updated permissions for workspace {ws_id}")

    def _provision_full_load(self) -> None:
        """Provisions permissions for selected of workspaces.

        Modifies upstream workspace declarations for each input workspace and
        skips non-existent workspace ids. Overwrites any existing configuration
        of the workspace permissions.
        """
        valid_permissions = self._filter_invalid_permissions(
            self.source_group_full
        )

        input_declarations = self._construct_declarations(valid_permissions)

        for ws_id, declaration in input_declarations.items():
            ws_permissions = declaration.to_sdk_api()

            self._api.put_declarative_permissions(ws_id, ws_permissions)
            self.logger.info(f"Updated permissions for workspace {ws_id}")

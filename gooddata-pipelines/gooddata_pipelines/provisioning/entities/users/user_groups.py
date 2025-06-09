# (C) 2025 GoodData Corporation

"""Module for provisioning user groups in GoodData workspaces."""

from gooddata_sdk.catalog.user.entity_model.user_group import CatalogUserGroup

from gooddata_pipelines.provisioning.entities.users.models import UserGroup
from gooddata_pipelines.provisioning.provisioning import Provisioning


class UserGroupProvisioner(Provisioning[UserGroup]):
    """Provisioning class for user groups in GoodData workspaces.

    This class handles the creation, update, and deletion of user groups
    based on the provided source data.
    """

    source_group: list[UserGroup]

    @staticmethod
    def _is_changed(group: UserGroup, existing_group: CatalogUserGroup) -> bool:
        """Checks if user group has some changes and needs to be updated."""
        group.parent_user_groups.sort()
        parents_changed = group.parent_user_groups != existing_group.get_parents
        name_changed = group.user_group_name != existing_group.name
        return parents_changed or name_changed

    def _create_or_update_user_group(
        self,
        group_id: str,
        group_name: str,
        parent_user_groups: list[str],
        http_method: str,
    ) -> None:
        """Creates or updates user group in the project."""
        catalog_user_group = CatalogUserGroup.init(
            user_group_id=group_id,
            user_group_name=group_name,
            user_group_parent_ids=parent_user_groups,
        )
        try:
            self._api.create_or_update_user_group(
                catalog_user_group=catalog_user_group, http_method=http_method
            )
            self.logger.info(
                f"Created/Updated user group: {group_id} - {group_name}"
            )
        except Exception as e:
            self.logger.error(
                f"Failed to create/update user group. Error: {e} "
                + f"Context: {catalog_user_group.__dict__}"
            )

    def _create_missing_user_groups(
        self, group_ids_to_create: set[str]
    ) -> None:
        """Provisions user groups that don't exist."""
        groups_to_create: list[UserGroup] = [
            group
            for group in self.source_group
            if group.user_group_id in group_ids_to_create
        ]

        # Sort user groups to create those without parents first
        groups_to_create.sort(key=lambda x: 1 if x.parent_user_groups else 0)

        for group in groups_to_create:
            self._create_or_update_user_group(
                group.user_group_id,
                group.user_group_name,
                group.parent_user_groups,
                "POST",
            )

    def _update_existing_user_groups(
        self, group_ids_to_update: set[str]
    ) -> None:
        """Update existing user groups and update ws_permissions."""
        groups_to_update = [
            group
            for group in self.source_group
            if group.user_group_id in group_ids_to_update
        ]

        existing_groups = {group.id: group for group in self.gd_user_groups}

        for group in groups_to_update:
            existing_group = existing_groups[group.user_group_id]
            if self._is_changed(group, existing_group):
                self._create_or_update_user_group(
                    group.user_group_id,
                    group.user_group_name,
                    group.parent_user_groups,
                    "PUT",
                )

    def _delete_user_group(self, group_ids_to_delete: set[str]) -> None:
        """Deletes user group from the project."""
        for user_group_id in group_ids_to_delete:
            try:
                self._api.delete_user_group(user_group_id)
                self.logger.info(f"Deleted user group: {user_group_id}")
            except Exception as e:
                self.logger.error(
                    f"Failed to delete user group. Error: {e} "
                    + f"Context: {{'user_group_id': {user_group_id}}}"
                )

    def _manage_user_groups(self) -> None:
        """Manages multiple users groups based on the provided input."""

        gd_group_ids: set[str] = {group.id for group in self.gd_user_groups}

        active_target_groups: set[str] = {
            group.user_group_id
            for group in self.source_group
            if group.is_active is True
        }
        inactive_target_groups: set[str] = {
            group.user_group_id
            for group in self.source_group
            if group.is_active is False
        }

        group_ids_to_create: set[str] = active_target_groups.difference(
            gd_group_ids
        )
        self._create_missing_user_groups(group_ids_to_create)

        group_ids_to_update: set[str] = active_target_groups.intersection(
            gd_group_ids
        )
        self._update_existing_user_groups(group_ids_to_update)

        group_ids_to_delete: set[str] = inactive_target_groups.intersection(
            gd_group_ids
        )
        self._delete_user_group(group_ids_to_delete)

    def _provision(self) -> None:
        # Get existing user group from cloud
        self.gd_user_groups: list[CatalogUserGroup] = (
            self._api.list_user_groups()
        )

        # Manage user groups
        self._manage_user_groups()

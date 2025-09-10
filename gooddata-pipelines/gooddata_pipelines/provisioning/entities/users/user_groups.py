# (C) 2025 GoodData Corporation

"""Module for provisioning user groups in GoodData workspaces."""

from typing import Sequence, TypeAlias

from gooddata_sdk.catalog.user.entity_model.user_group import CatalogUserGroup

from gooddata_pipelines.provisioning.entities.users.models.user_groups import (
    UserGroupFullLoad,
    UserGroupIncrementalLoad,
)
from gooddata_pipelines.provisioning.provisioning import Provisioning

UserGroupModel: TypeAlias = UserGroupFullLoad | UserGroupIncrementalLoad


class UserGroupProvisioner(
    Provisioning[UserGroupFullLoad, UserGroupIncrementalLoad]
):
    """Provisioning class for user groups in GoodData workspaces.

    This class handles the creation, update, and deletion of user groups
    based on the provided source data. Use the `full_load` or `incremental_load`
    methods to run the provisioning.
    """

    source_group_incremental: list[UserGroupIncrementalLoad]
    source_group_full: list[UserGroupFullLoad]
    upstream_user_groups: list[CatalogUserGroup]

    FULL_LOAD_TYPE: type[UserGroupFullLoad] = UserGroupFullLoad
    INCREMENTAL_LOAD_TYPE: type[UserGroupIncrementalLoad] = (
        UserGroupIncrementalLoad
    )

    @staticmethod
    def _is_changed(
        group: UserGroupModel, existing_group: CatalogUserGroup
    ) -> bool:
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
    ) -> None:
        """Creates or updates user group in the project."""
        catalog_user_group = CatalogUserGroup.init(
            user_group_id=group_id,
            user_group_name=group_name,
            user_group_parent_ids=parent_user_groups,
        )
        try:
            self._api.create_or_update_user_group(
                catalog_user_group=catalog_user_group
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
        self,
        groups_to_create: Sequence[UserGroupModel],
    ) -> None:
        """Provisions user groups that don't exist."""
        # Sort user groups to create those without parents first
        sorted_groups = sorted(
            groups_to_create, key=lambda x: 1 if x.parent_user_groups else 0
        )

        for group in sorted_groups:
            self._create_or_update_user_group(
                group.user_group_id,
                group.user_group_name,
                group.parent_user_groups,
            )

    def _update_existing_user_groups(
        self,
        groups_to_update: Sequence[UserGroupModel],
        upstream_user_groups: list[CatalogUserGroup],
    ) -> None:
        """Update existing user groups and update ws_permissions."""
        existing_groups = {group.id: group for group in upstream_user_groups}

        for group in groups_to_update:
            existing_group = existing_groups[group.user_group_id]
            if self._is_changed(group, existing_group):
                self._create_or_update_user_group(
                    group.user_group_id,
                    group.user_group_name,
                    group.parent_user_groups,
                )

    def _delete_user_group(self, group_ids_to_delete: set[str]) -> None:
        """Deletes user group from the project."""
        for group_id in group_ids_to_delete:
            try:
                self._api.delete_user_group(group_id)
                self.logger.info(f"Deleted user group: {group_id}")
            except Exception as e:
                self.logger.error(
                    f"Failed to delete user group. Error: {e} "
                    + f"Context: {{'user_group_id': {group_id}}}"
                )

    def _provision_incremental_load(self) -> None:
        """Runs incremental provisioning of user groups."""
        # Get existing user groups from GoodData Cloud
        self.upstream_user_groups = self._api.list_user_groups()

        # Create a set of upstream user group IDs
        upstream_group_ids: set[str] = {
            group.id for group in self.upstream_user_groups
        }

        # Create a set of active source user group IDs
        active_source_groups: set[str] = {
            group.user_group_id
            for group in self.source_group_incremental
            if group.is_active is True
        }

        # Create a set of inactive source user group IDs
        inactive_source_groups: set[str] = {
            group.user_group_id
            for group in self.source_group_incremental
            if group.is_active is False
        }

        # Create a set of user group IDs to create as the difference between active
        # source groups and upstream groups - i.e, we are creating groups marked
        # as active in the source data but which are missing upstream in GoodData Cloud.
        group_ids_to_create: set[str] = active_source_groups.difference(
            upstream_group_ids
        )

        # Create a set of user group IDs to update as the intersection between active
        # source groups and upstream groups - i.e, we are updating groups marked
        # as active in the source data and which are present upstream in GoodData Cloud.
        # The `_update_existing_user_groups` method will check if the upstream group
        # definition differs from the source and if so, it will update the group.
        group_ids_to_update: set[str] = active_source_groups.intersection(
            upstream_group_ids
        )

        # Create a set of user group IDs to delete as the intersection between
        # inactive source groups and upstream groups - i.e, we are deleting groups
        # marked as inactive in the source data and which are present upstream in
        # GoodData Cloud.
        group_ids_to_delete: set[str] = inactive_source_groups.intersection(
            upstream_group_ids
        )

        # create lists of groups to create, update and delete based on the sets
        groups_to_create: list[UserGroupIncrementalLoad] = []
        groups_to_update: list[UserGroupIncrementalLoad] = []

        for group in self.source_group_incremental:
            if group.user_group_id in group_ids_to_create:
                groups_to_create.append(group)
            elif group.user_group_id in group_ids_to_update:
                groups_to_update.append(group)

        self._create_missing_user_groups(groups_to_create)
        self._update_existing_user_groups(
            groups_to_update, self.upstream_user_groups
        )
        self._delete_user_group(group_ids_to_delete)

    def _provision_full_load(self) -> None:
        """Runs full load provisioning of user groups."""
        # Get upsream user groups
        self.upstream_user_groups = self._api.list_user_groups()

        # Create a set of upstream user group IDs
        upstream_group_ids: set[str] = {
            group.id for group in self.upstream_user_groups
        }

        # Create a set of source user group IDs
        source_group_ids: set[str] = {
            group.user_group_id for group in self.source_group_full
        }

        # Figure out which ids are to be created, deleted or exist in both systems
        id_groups = self._create_groups(source_group_ids, upstream_group_ids)

        groups_to_create: list[UserGroupFullLoad] = []
        groups_to_update: list[UserGroupFullLoad] = []

        for group in self.source_group_full:
            if group.user_group_id in id_groups.ids_to_create:
                groups_to_create.append(group)
            elif group.user_group_id in id_groups.ids_in_both_systems:
                groups_to_update.append(group)

        # Create user groups
        self._create_missing_user_groups(groups_to_create)

        # Update user groups
        self._update_existing_user_groups(
            groups_to_update, self.upstream_user_groups
        )

        # Delete user groups
        self._delete_user_group(id_groups.ids_to_delete)

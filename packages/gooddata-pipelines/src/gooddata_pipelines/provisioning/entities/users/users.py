# (C) 2025 GoodData Corporation

"""Module for provisioning users in GoodData workspaces."""

from typing import TypeAlias

from gooddata_api_client.exceptions import NotFoundException  # type: ignore
from gooddata_sdk.catalog.user.entity_model.user import CatalogUser
from gooddata_sdk.catalog.user.entity_model.user_group import CatalogUserGroup

from gooddata_pipelines.provisioning.entities.users.models.users import (
    UserFullLoad,
    UserIncrementalLoad,
    UserProfile,
)
from gooddata_pipelines.provisioning.provisioning import Provisioning
from gooddata_pipelines.provisioning.utils.context_objects import UserContext

# Type alias for user model instances
UserModel: TypeAlias = UserFullLoad | UserIncrementalLoad
UserId: TypeAlias = str


class UserProvisioner(Provisioning[UserFullLoad, UserIncrementalLoad]):
    """Provisioning class for users in GoodData workspaces.

    This class handles the creation, update, and deletion of users
    based on the provided source data.
    """

    source_group_incremental: list[UserIncrementalLoad]
    source_group_full: list[UserFullLoad]

    current_user_id: str

    FULL_LOAD_TYPE: type[UserFullLoad] = UserFullLoad
    INCREMENTAL_LOAD_TYPE: type[UserIncrementalLoad] = UserIncrementalLoad

    def __init__(self, host: str, token: str) -> None:
        super().__init__(host, token)
        self.upstream_user_cache: dict[UserId, UserModel] = {}

    def _get_current_user_id(self) -> str:
        """Gets the current user ID."""

        profile_response = self._api.get_profile()

        if not profile_response.ok:
            raise Exception("Failed to get current user profile")

        profile_json = profile_response.json()
        profile = UserProfile.model_validate(profile_json)

        return profile.user_id

    def _try_get_user(
        self, user: UserModel, model: type[UserModel]
    ) -> UserModel | None:
        try:
            if user.user_id in self.upstream_user_cache:
                return self.upstream_user_cache[user.user_id]

            user_sdk_obj = self._api._sdk.catalog_user.get_user(user.user_id)
            return model.from_sdk_obj(user_sdk_obj)
        except NotFoundException:
            return None

    def _get_or_create_user_groups(self, groups: list[str]) -> None:
        """Ensures that all user groups exist in the project."""
        for group in groups:
            try:
                self._api._sdk.catalog_user.get_user_group(group)
            except NotFoundException:
                #  Create the user gtoup if it does not exist
                self._api.create_or_update_user_group(
                    CatalogUserGroup.init(
                        user_group_id=group, user_group_name=group
                    ),
                )
                self.logger.info(f"Created user group: {group}")

    def _user_is_equal_upstream(
        self,
        user: UserModel,
        upstream_user: UserModel | None,
    ) -> bool:
        """
        Checks if the user is different from the upstream user. Lists are checked by converting to sets.
        """
        if not upstream_user:
            return False

        user_data = user.model_dump()
        upstream_data = upstream_user.model_dump()

        for attr, source_value in user_data.items():
            upstream_value = upstream_data.get(attr)

            if isinstance(source_value, list):
                if set(source_value) != set(upstream_value or []):
                    return False
            else:
                if source_value != upstream_value:
                    return False
        return True

    def _create_or_update_user(
        self, user: UserModel, model: type[UserModel]
    ) -> None:
        """Creates or updates user in the project.

        Determines if the user needs to be updated or created by getting the
        upstream user from GoodData Cloud and comparing it with the source user.
        If user is supposed to be placed in a User Group, the function will check
        for its existence and create it if needed.

        """

        if user.user_id == self.current_user_id:
            self.logger.warning(
                f"Skipping creation/update of current user: {user.user_id}. "
                + "Current user should not be modified.",
            )
            return

        user_context = UserContext(
            user_id=user.user_id,
            user_groups=user.user_groups,
        )

        upstream_user = self._try_get_user(user, model)

        if self._user_is_equal_upstream(user, upstream_user):
            return

        self._get_or_create_user_groups(user.user_groups)

        self._api.create_or_update_user(
            user.to_sdk_obj(), **user_context.__dict__
        )
        self.logger.info(f"User {user.user_id} created/updated successfully.")

    def _delete_user(self, user_id: str) -> None:
        """Deletes user from the project."""
        if user_id == self.current_user_id:
            self.logger.warning(
                f"Skipping deletion of current user: {user_id}."
                + " Current user should not be deleted.",
            )
            return

        try:
            self._api._sdk.catalog_user.get_user(user_id)
        except NotFoundException:
            return

        self._api.delete_user(user_id)
        self.logger.info(f"Deleted user: {user_id}")

    def _manage_user(self, user: UserIncrementalLoad) -> None:
        """Manages user based on the provided GDUserTarget."""
        if user.is_active:
            self._create_or_update_user(user, UserIncrementalLoad)
        else:
            self._delete_user(user.user_id)

    def _provision_incremental_load(self) -> None:
        """Runs the incremental provisioning logic."""
        # Set the current user ID
        self.current_user_id = self._get_current_user_id()

        for user in self.source_group_incremental:
            # Attempt to process each user. On failure, log the error and continue
            try:
                self._manage_user(user)
            except Exception as e:
                self.logger.error(
                    f"Failed to manage user {user.user_id}. Error: {e} Context: {user.__dict__}"
                )

    def _provision_full_load(self) -> None:
        """Runs the full load provisioning logic."""

        # Set the current user ID
        self.current_user_id = self._get_current_user_id()

        # Get all upstream users
        catalog_upstream_users: list[CatalogUser] = self._api.list_users()

        # Convert catalog users to user models
        upstream_users: list[UserFullLoad] = [
            UserFullLoad.from_sdk_obj(user) for user in catalog_upstream_users
        ]

        # Cache the upstream users in a dict. It will be reused in `_try_get_user`
        self.upstream_user_cache = {
            user.user_id: user for user in upstream_users
        }
        # Get source IDs
        source_ids: set[str] = {user.user_id for user in self.source_group_full}

        # Get upstream IDs
        upstream_ids: set[str] = {user.user_id for user in upstream_users}

        # Create groups of IDs to delete, create, and in both systems
        id_groups = self._create_groups(source_ids, upstream_ids)

        # Iterate over source users and create/update
        for user in self.source_group_full:
            user_id = user.user_id

            if (
                user_id in id_groups.ids_to_create
                or user_id in id_groups.ids_in_both_systems
            ):
                self._create_or_update_user(user, UserFullLoad)

        # Delete users marked for deletion
        for user_id in id_groups.ids_to_delete:
            self._delete_user(user_id)

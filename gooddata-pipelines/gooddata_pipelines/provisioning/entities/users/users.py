# (C) 2025 GoodData Corporation

"""Module for provisioning users in GoodData workspaces."""

from gooddata_api_client.exceptions import (  # type: ignore[import]
    NotFoundException,
)
from gooddata_sdk.catalog.user.entity_model.user_group import CatalogUserGroup

from gooddata_pipelines.provisioning.entities.users.models import User
from gooddata_pipelines.provisioning.provisioning import Provisioning
from gooddata_pipelines.provisioning.utils.context_objects import UserContext


class UserProvisioner(Provisioning[User]):
    """Provisioning class for users in GoodData workspaces.

    This class handles the creation, update, and deletion of users
    based on the provided source data.
    """

    source_group: list[User]

    def _try_get_user(self, user: User) -> User | None:
        try:
            user_sdk_obj = self._api._sdk.catalog_user.get_user(user.user_id)
            return User.from_sdk_obj(user_sdk_obj)
        except NotFoundException:
            return None

    def _get_or_create_user_groups(self, groups: list[str]) -> None:
        """Ensures that all user groups exist in the project."""
        # TODO - Can be optimized - preloading all user groups and checking on the go
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
        self, user: User, upstream_user: User | None
    ) -> bool:
        """
        Checks if the user is different from the upstream user. Lists are checked by convverting to sets.
        """
        if not upstream_user:
            return False

        for attr in user.__dataclass_fields__:
            source_value = getattr(user, attr)
            upstream_value = getattr(upstream_user, attr)

            if isinstance(source_value, list):
                if set(source_value) != set(upstream_value):
                    return False
            else:
                if source_value != upstream_value:
                    return False
        return True

    def _create_or_update_user(self, user: User) -> None:
        """Creates or updates user in the project."""
        user_context = UserContext(
            user_id=user.user_id,
            user_groups=user.user_groups,
        )
        upstream_user = self._try_get_user(user)

        if self._user_is_equal_upstream(user, upstream_user):
            return

        self._get_or_create_user_groups(user.user_groups)

        self._api.create_or_update_user(
            user.to_sdk_obj(), **user_context.__dict__
        )
        self.logger.info(f"User {user.user_id} created/updated successfully.")

    def _delete_user(self, user: User) -> None:
        """Deletes user from the project."""
        user_context = UserContext(
            user_id=user.user_id,
            user_groups=user.user_groups,
        )
        try:
            self._api._sdk.catalog_user.get_user(user.user_id)
        except NotFoundException:
            return

        self._api.delete_user(user.user_id, **user_context.__dict__)
        self.logger.info(f"Deleted user: {user.user_id}")

    def _manage_user(self, user: User) -> None:
        """Manages user based on the provided GDUserTarget."""
        if user.is_active:
            self._create_or_update_user(user)
        else:
            self._delete_user(user)

    def _manage_users(self, users: list[User]) -> None:
        """Manages multiple users based on the provided GDUserTargets."""
        for user in users:
            # Attempt to process each user. On failure, log the error and continue
            try:
                self._manage_user(user)
            except Exception as e:
                self.logger.error(
                    f"Failed to manage user {user.user_id}. Error: {e} Context: {user.__dict__}"
                )

    def _provision(self) -> None:
        # Run the user provisioning workflow
        self._manage_users(self.source_group)

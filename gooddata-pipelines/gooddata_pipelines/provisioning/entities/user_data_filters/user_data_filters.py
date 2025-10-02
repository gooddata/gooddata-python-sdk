# (C) 2025 GoodData Corporation

"""Module for provisioning user data filters in GoodData workspaces.

This module provides the `UserDataFilterProvisioner` class, which is responsible
for creating, updating, and deleting user data filters in GoodData workspaces.
"""

import re

from gooddata_sdk.catalog.workspace.entity_model.user_data_filter import (
    CatalogEntityIdentifier,
    CatalogUserDataFilter,
    CatalogUserDataFilterAttributes,
    CatalogUserDataFilterRelationships,
)

from gooddata_pipelines.provisioning.entities.user_data_filters.models.udf_models import (
    UserDataFilterFullLoad,
    UserDataFilterGroup,
    UserDataFilterIncrementalLoad,
    WorkspaceUserDataFilters,
)
from gooddata_pipelines.provisioning.provisioning import Provisioning
from gooddata_pipelines.provisioning.utils.exceptions import ContextException


class UserDataFilterProvisioner(
    Provisioning[UserDataFilterFullLoad, UserDataFilterIncrementalLoad]
):
    """Provisioning class for user data filters in GoodData workspaces.

    This class handles the creation, update, and deletion of user data filters
    based on the provided source data.

    Requires setting the `ldm_column_name` and `maql_column_name`
    attributes before calling the `provision` method.

    Usage:
    ```
    provisioner = UserDataFilterProvisioner(api, source_group)
    provisioner.set_ldm_column_name("ldm_column")
    provisioner.set_maql_column_name("maql_column")
    provisioner.provision()
    ```
    """

    source_group_full: list[UserDataFilterFullLoad]
    source_group_incremental: list[UserDataFilterIncrementalLoad]
    ldm_column_name: str = ""
    maql_column_name: str = ""

    FULL_LOAD_TYPE = UserDataFilterFullLoad

    def set_ldm_column_name(self, ldm_column_name: str) -> None:
        """Set the LDM column name for user data filters.

        Args:
            ldm_column_name (str): The LDM column name to set.
        """
        self.ldm_column_name = ldm_column_name

    def set_maql_column_name(self, maql_column_name: str) -> None:
        """Set the MAQL column name for user data filters.

        Args:
            maql_column_name (str): The MAQL column name to set.
        """
        self.maql_column_name = maql_column_name

    @staticmethod
    def _group_db_user_data_filters_by_ws_id(
        user_data_filters: list[UserDataFilterFullLoad],
    ) -> list[WorkspaceUserDataFilters]:
        """Group user data filters by workspace ID and user ID."""
        ws_map: dict[str, dict[str, set[str]]] = {}

        for udf in user_data_filters:
            ws_map.setdefault(udf.workspace_id, {}).setdefault(
                udf.udf_id, set()
            ).add(str(udf.udf_value))

        result: list[WorkspaceUserDataFilters] = []

        for ws_id, udf_dict in ws_map.items():
            udf_groups = [
                UserDataFilterGroup(udf_id=udf_id, udf_values=list(values))
                for udf_id, values in udf_dict.items()
            ]
            result.append(
                WorkspaceUserDataFilters(
                    workspace_id=ws_id, user_data_filters=udf_groups
                )
            )
        return result

    @staticmethod
    def _extract_numbers_from_maql(maql: str) -> list[str]:
        """Extract numbers from a MAQL string."""
        numbers = re.findall(r'"\d+"', maql)
        return [number.strip('"') for number in numbers]

    def _skip_user_data_filter_update(
        self, existing_udf: list[CatalogUserDataFilter], udf_value: list[str]
    ) -> bool:
        """Check if the user data filter update can be skipped."""
        if not existing_udf:
            return False
        existing_udfs = self._extract_numbers_from_maql(
            existing_udf[0].attributes.maql
        )
        return set(udf_value) == set(existing_udfs)

    def _create_user_data_filters(
        self, user_data_filter_ids_to_create: list[WorkspaceUserDataFilters]
    ) -> None:
        """Create or update user data filters in GoodData workspaces."""
        for workspace_user_data_filter in user_data_filter_ids_to_create:
            workspace_id = workspace_user_data_filter.workspace_id
            user_data_filters = workspace_user_data_filter.user_data_filters

            gd_user_data_filters: list[CatalogUserDataFilter] = (
                self._api.list_user_data_filters(workspace_id)
            )

            gd_udf_ids = {
                user.relationships.user["data"].id
                for user in gd_user_data_filters
                if user.relationships and user.relationships.user
            }

            db_udf_ids = {udf.udf_id for udf in user_data_filters}

            udf_ids_to_delete: set[str] = gd_udf_ids.difference(db_udf_ids)
            self._delete_user_data_filters(workspace_id, udf_ids_to_delete)

            udf_group: UserDataFilterGroup
            for udf_group in user_data_filters:
                udf_id: str = udf_group.udf_id
                udf_values: list[str] = udf_group.udf_values

                existing_udf: list[CatalogUserDataFilter] = [
                    udf for udf in gd_user_data_filters if udf.id == udf_id
                ]
                if self._skip_user_data_filter_update(existing_udf, udf_values):
                    continue

                formatted_udf_values = '", "'.join(
                    str(value) for value in udf_values
                )
                maql = f'{self.maql_column_name} IN ("{formatted_udf_values}")'

                attributes = CatalogUserDataFilterAttributes(maql=maql)
                relationships = CatalogUserDataFilterRelationships(
                    labels={
                        "data": [
                            CatalogEntityIdentifier(
                                id=self.ldm_column_name, type="label"
                            )
                        ]
                    },
                    user={
                        "data": CatalogEntityIdentifier(id=udf_id, type="user")
                    },
                )
                user_data_filter = CatalogUserDataFilter(
                    id=udf_id,
                    attributes=attributes,
                    relationships=relationships,
                )

                try:
                    self._api.create_or_update_user_data_filter(
                        workspace_id, user_data_filter
                    )
                    self.logger.info(
                        "Created or updated user data filters for user with id "
                        + f"{udf_id} for client with id {workspace_id}"
                    )
                except Exception as e:
                    raise ContextException(
                        f"Failed to create user data filters: {e}",
                        udf_group,
                        user_data_filter,
                    ) from e

    def _delete_user_data_filters(
        self, workspace_id: str, udf_ids_to_delete: set[str]
    ) -> None:
        """Delete user data filters in GoodData workspaces."""
        for udf_id in udf_ids_to_delete:
            try:
                self._api.delete_user_data_filter(workspace_id, udf_id)
                self.logger.info(
                    f"Deleted user data filters for user with id {udf_id}"
                )
            except Exception as e:
                raise ContextException(
                    f"Failed to delete user data filters: {e}"
                ) from e

    def _provision_full_load(self) -> None:
        """Provision user data filters in GoodData workspaces."""

        if not self.maql_column_name:
            raise ContextException(
                "MAQL column name is not set. Please set it before provisioning."
            )
        if not self.ldm_column_name:
            raise ContextException(
                "LDM column name is not set. Please set it before provisioning."
            )

        grouped_db_user_data_filters = (
            self._group_db_user_data_filters_by_ws_id(self.source_group_full)
        )
        self._create_user_data_filters(grouped_db_user_data_filters)

    def _provision_incremental_load(self) -> None:
        """Provision user data filters in GoodData workspaces."""
        raise NotImplementedError("Not implemented yet.")

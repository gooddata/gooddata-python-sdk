# (C) 2025 GoodData Corporation
"""Module for provisioning workspaces in GoodData Cloud."""

from typing import Literal

from gooddata_sdk.catalog.workspace.entity_model.workspace import (
    CatalogWorkspace,
)

from gooddata_pipelines.api.exceptions import GoodDataApiException
from gooddata_pipelines.provisioning.entities.workspaces.models import (
    WorkspaceDataMaps,
    WorkspaceFullLoad,
    WorkspaceIncrementalLoad,
)
from gooddata_pipelines.provisioning.entities.workspaces.workspace_data_filters import (
    WorkspaceDataFilterManager,
)
from gooddata_pipelines.provisioning.entities.workspaces.workspace_data_parser import (
    WorkspaceDataParser,
)
from gooddata_pipelines.provisioning.entities.workspaces.workspace_data_validator import (
    WorkspaceDataValidator,
)
from gooddata_pipelines.provisioning.provisioning import Provisioning
from gooddata_pipelines.provisioning.utils.context_objects import (
    WorkspaceContext,
)
from gooddata_pipelines.provisioning.utils.exceptions import WorkspaceException


class WorkspaceProvisioner(
    Provisioning[WorkspaceFullLoad, WorkspaceIncrementalLoad]
):
    source_group_full: list[WorkspaceFullLoad]
    source_group_incremental: list[WorkspaceIncrementalLoad]

    def __init__(self, *args: str, **kwargs: str) -> None:
        """Creates an instance of the WorkspaceProvisioner.

        Calls the superclass constructor and initializes the validator, parser,
        and maps for workspace data.
        """
        super().__init__(*args, **kwargs)
        self.validator: WorkspaceDataValidator = WorkspaceDataValidator(
            self._api
        )
        self.parser: WorkspaceDataParser = WorkspaceDataParser()
        self.maps: WorkspaceDataMaps = WorkspaceDataMaps()

    def _find_workspaces_to_update(
        self,
        source_group: list[WorkspaceFullLoad],
        panther_group: list[CatalogWorkspace],
        ids_in_both_systems: set[str],
    ) -> set[str]:
        """
        Inspects existing Panther workspaces and compares them to workspaces from
        the source database. If the ID exists in both systems but the workspace
        name in GoodData Cloud is different from the source, the workspace will
        be updated. The rest of the workspaces will be ignored.
        """
        existing_workspaces: dict[str, CatalogWorkspace] = {
            workspace.id: workspace for workspace in panther_group
        }

        ids_to_update: set[str] = set()

        for source_workspace in source_group:
            source_id = source_workspace.workspace_id
            source_name = source_workspace.workspace_name

            if source_id not in ids_in_both_systems:
                continue

            if existing_workspaces.get(source_id):
                panther_name = existing_workspaces[source_id].name
            else:
                continue

            if source_name == panther_name:
                continue

            ids_to_update.add(source_id)

        return ids_to_update

    def _create_or_update_panther_workspaces(
        self,
        workspace_ids_to_create: set[str],
        workspace_ids_to_update: set[str],
        child_to_parent_map: dict[str, str],
        workspace_id_to_wdf_map: dict[str, dict[str, list[str]]],
    ) -> None:
        action: Literal["CREATE", "UPDATE"]

        for source_workspace in self.source_group_full:
            if source_workspace.workspace_id in workspace_ids_to_update:
                action = "UPDATE"
            elif source_workspace.workspace_id in workspace_ids_to_create:
                action = "CREATE"
            else:
                continue

            context: WorkspaceContext = WorkspaceContext(
                workspace_id=source_workspace.workspace_id,
                workspace_name=source_workspace.workspace_name,
                wdf_id=source_workspace.workspace_data_filter_id,
                wdf_values=source_workspace.workspace_data_filter_values,
            )

            parent_workspace_id: str = child_to_parent_map[context.workspace_id]

            try:
                self._api.create_or_update_panther_workspace(
                    workspace_id=context.workspace_id,
                    workspace_name=str(context.workspace_name),
                    parent_id=parent_workspace_id,
                )
                self.logger.info(
                    f"{action.title()}d workspace: {context.workspace_id}"
                )

            except GoodDataApiException as e:
                combined_context = {**context.__dict__, **e.__dict__}
                self.logger.error(
                    f"Failed to {action.title()} workspace: {context.workspace_id}. "
                    + f"Error: {e} Context: {combined_context}"
                )

            # If child workspace has WDF settings, apply them
            child_wdfs: dict[str, list[str]] = workspace_id_to_wdf_map.get(
                context.workspace_id, {}
            )
            if child_wdfs:
                self.wdf_manager.check_wdf_settings(
                    context,
                )

    def delete_panther_workspaces(
        self, ids_to_delete: set[str], workspace_id_to_name_map: dict[str, str]
    ) -> None:
        for workspace_id in ids_to_delete:
            workspace_context: WorkspaceContext = WorkspaceContext(
                workspace_id=workspace_id,
                workspace_name=workspace_id_to_name_map.get(workspace_id),
            )
            try:
                self._api.delete_panther_workspace(workspace_id)
                self.logger.info(
                    f"Deleted workspace: {workspace_context.workspace_id}"
                )

            except GoodDataApiException as e:
                exception_context = {**workspace_context.__dict__, **e.__dict__}
                self.logger.error(
                    f"Failed to delete workspace: {workspace_context.workspace_id}. "
                    + f"Error: {e} Context: {exception_context}"
                )

    def verify_workspace_provisioning(
        self,
        source_group: list[WorkspaceFullLoad],
        parent_workspace_ids: set[str],
    ) -> None:
        """Verifies that upstream content is equal to the source data."""
        source_ids_names: set[tuple[str, str]] = {
            (item.workspace_id, item.workspace_name) for item in source_group
        }

        panther_workspaces: list[CatalogWorkspace] = (
            self._api.get_panther_children_workspaces(parent_workspace_ids)
        )

        panther_ids_names: set[tuple[str, str]] = {
            (workspace.workspace_id, workspace.name)
            for workspace in panther_workspaces
        }

        diff: set[tuple[str, str]] = source_ids_names.symmetric_difference(
            panther_ids_names
        )

        if diff:
            raise WorkspaceException(
                "Provisioning failed. The source and Panther workspaces do not "
                + f"match. Difference: {diff}"
            )

    def _provision_full_load(self) -> None:
        """Full load workspace provisioning."""

        # Validate the source data.
        self.validator.validate_source_data(self.source_group_full)

        # Set the maps based on the source data.
        self.maps = self.parser.set_maps_based_on_source(
            self.maps, self.source_group_full
        )

        # Get upstream children of all parent workspaces.
        self.upstream_group: list[CatalogWorkspace] = (
            self._api.get_panther_children_workspaces(self.maps.parent_ids)
        )

        # Set maps that require upstream data.
        self.maps = self.parser.set_maps_with_upstream_data(
            self.maps, self.source_group_full, self.upstream_group
        )

        # Create an instance of WDF manager with the created maps.
        self.wdf_manager = WorkspaceDataFilterManager(self._api, self.maps)

        # Sort the ids to groups based on provisioning logic.
        id_groups = self._create_groups(
            self.maps.source_ids, self.maps.upstream_ids
        )

        # Find out which workspaces to update.
        self.ids_to_update: set[str] = self._find_workspaces_to_update(
            self.source_group_full,
            self.upstream_group,
            id_groups.ids_in_both_systems,
        )

        # Delete the workspaces that are not in the source.
        self.delete_panther_workspaces(
            id_groups.ids_to_delete, self.maps.workspace_id_to_name_map
        )

        # Create or update selected workspaces.
        self._create_or_update_panther_workspaces(
            id_groups.ids_to_create,
            self.ids_to_update,
            self.maps.child_to_parent_id_map,
            self.maps.workspace_id_to_wdf_map,
        )

        # Check WDF settings of ignored workspaces.
        ignored_workspace_ids: set[str] = self.maps.source_ids.difference(
            id_groups.ids_to_create.union(self.ids_to_update).union(
                id_groups.ids_to_delete
            )
        )

        for ignored_workspace_id in ignored_workspace_ids:
            ignored_workspace_context: WorkspaceContext = WorkspaceContext(
                workspace_id=ignored_workspace_id,
                workspace_name=self.maps.workspace_id_to_name_map.get(
                    ignored_workspace_id
                ),
            )
            self.wdf_manager.check_wdf_settings(ignored_workspace_context)

        # Verify the provisioning by queries to GoodData Cloud.
        self.verify_workspace_provisioning(
            self.source_group_full, self.maps.parent_ids
        )

    def _provision_incremental_load(self) -> None:
        """Incremental workspace provisioning."""

        raise NotImplementedError("Not implemented yet.")

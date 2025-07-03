# (C) 2025 GoodData Corporation

"""Module for parsing and processing workspace data in GoodData Cloud."""

from gooddata_sdk.catalog.workspace.entity_model.workspace import (
    CatalogWorkspace,
)

from gooddata_pipelines.provisioning.entities.workspaces.models import (
    WorkspaceDataMaps,
    WorkspaceFullLoad,
)


class WorkspaceDataParser:
    """Helper class to process workspace data retrieved from Panther and source DB."""

    @staticmethod
    def _get_id_to_name_map(
        source_group: list[WorkspaceFullLoad],
        upstream_group: list[CatalogWorkspace],
    ) -> dict[str, str]:
        """Creates a map of workspace IDs to their names for all known workspaces."""
        source_map: dict[str, str] = {
            workspace.workspace_id: workspace.workspace_name
            for workspace in source_group
        }
        upstream_map: dict[str, str] = {
            item.workspace_id: item.name for item in upstream_group
        }

        return {**upstream_map, **source_map}

    @staticmethod
    def _get_child_to_parent_map(
        source_group: list[WorkspaceFullLoad],
    ) -> dict[str, str]:
        """Creates a map of child workspace IDs to their parent workspace IDs."""
        child_to_parent_map: dict[str, str] = {
            workspace.workspace_id: workspace.parent_id
            for workspace in source_group
        }

        return child_to_parent_map

    @staticmethod
    def _get_set_of_ids_from_source(
        source_group: list[WorkspaceFullLoad], column_name: str
    ) -> set[str]:
        """Creates a set of unique parent workspace IDs."""
        set_of_ids: set[str] = {
            getattr(workspace, column_name)
            for workspace in source_group
            if getattr(workspace, column_name)
        }
        return set_of_ids

    @staticmethod
    def get_set_of_upstream_workspace_ids(
        upstream_group: list[CatalogWorkspace],
    ) -> set[str]:
        """Creates a set of unique upstream workspace IDs."""
        set_of_ids: set[str] = {item.workspace_id for item in upstream_group}
        return set_of_ids

    def _get_child_to_wdfs_map(
        self, source_group: list[WorkspaceFullLoad]
    ) -> dict[str, dict[str, list[str]]]:
        """Creates a map of child workspace IDs to their WDF IDs."""
        # TODO: Use objects or a more transparent data structure instead of this.
        child_to_wdf_map: dict[str, dict[str, list[str]]] = {}

        # For each child, get its possible WDF IDs and values for each id
        for workspace in source_group:
            child_id: str = workspace.workspace_id
            wdf_id: str | None = workspace.workspace_data_filter_id
            wdf_values: list[str] | None = (
                workspace.workspace_data_filter_values
            )

            if wdf_values and wdf_id:
                if not child_to_wdf_map.get(child_id):
                    child_to_wdf_map[child_id] = {}
                child_to_wdf_map[child_id][wdf_id] = wdf_values

        return child_to_wdf_map

    def set_maps_based_on_source(
        self,
        map_object: WorkspaceDataMaps,
        source_group: list[WorkspaceFullLoad],
    ) -> WorkspaceDataMaps:
        """Creates maps which are dependent on the source group only."""
        map_object.child_to_parent_id_map = self._get_child_to_parent_map(
            source_group
        )
        map_object.workspace_id_to_wdf_map = self._get_child_to_wdfs_map(
            source_group
        )
        map_object.parent_ids = self._get_set_of_ids_from_source(
            source_group, "parent_id"
        )
        map_object.source_ids = self._get_set_of_ids_from_source(
            source_group, "workspace_id"
        )

        return map_object

    def set_maps_with_upstream_data(
        self,
        map_object: WorkspaceDataMaps,
        source_group: list[WorkspaceFullLoad],
        upstream_group: list[CatalogWorkspace],
    ) -> WorkspaceDataMaps:
        """Creates maps which are dependent on both the source group and upstream group."""
        map_object.workspace_id_to_name_map = self._get_id_to_name_map(
            source_group, upstream_group
        )
        map_object.upstream_ids = self.get_set_of_upstream_workspace_ids(
            upstream_group
        )

        return map_object

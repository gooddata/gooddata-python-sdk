# (C) 2025 GoodData Corporation

"""Module for validating workspace data integrity in GoodData Cloud."""

from typing import Any

from requests import Response

from gooddata_pipelines.api import GoodDataApi
from gooddata_pipelines.logger.logger import LogObserver
from gooddata_pipelines.provisioning.entities.workspaces.models import (
    WorkspaceFullLoad,
)
from gooddata_pipelines.provisioning.utils.context_objects import (
    WorkspaceContext,
)
from gooddata_pipelines.provisioning.utils.exceptions import (
    WorkspaceDataIntegrityException,
    WorkspaceException,
)


class WorkspaceDataValidator:
    """Class for validating workspace data integrity before provisioning."""

    def __init__(self, api: GoodDataApi):
        """
        Initializes the WorkspaceDataValidator with the GoodData API instance.

        Args:
            api (GoodDataApi): An instance of the GoodData API client.
        """
        self.api = api
        self.logger = LogObserver()

    def _check_basic_integrity(
        self,
        source_group: list[WorkspaceFullLoad],
    ) -> tuple[set[str], dict[str, list[str]]]:
        """
        Checks that mandatory fields are not empty and that that the combinations
        of values are unique.

        Returns a set of parent workspaces and a dictionary of parent-wdf mappings.
        """
        parent_workspaces: set[str] = set()
        parent_wdf_map: dict[str, list[str]] = {}
        parent_child_wdf_ids: list[tuple[str, str, str | None]] = []

        # Check that fields are not empty
        for workspace in source_group:
            parent_id: str | None = workspace.parent_id
            workspace_id: str | None = workspace.workspace_id
            workspace_name: str | None = workspace.workspace_name
            wdf_id: str | None = workspace.workspace_data_filter_id
            wdf_values: list[str] | None = (
                workspace.workspace_data_filter_values
            )

            # Create a context for the workspace validation
            validation_context: WorkspaceContext = WorkspaceContext(
                workspace_id=workspace_id,
                workspace_name=workspace_name,
                wdf_id=wdf_id,
                wdf_values=wdf_values,
            )

            # Raise specific error if both parent_id and workspace_id are not defined
            if (parent_id is None or parent_id == "") and (
                workspace_id is None or workspace_id == ""
            ):
                raise WorkspaceDataIntegrityException(
                    "Parent ID and workspace ID are not defined for at least one row. Please check the source data."
                )

            # Raise error if parent_id is not defined
            if parent_id is None or parent_id == "":
                raise WorkspaceDataIntegrityException(
                    "Parent ID is not defined in source data.",
                    validation_context,
                )

            # Add parent_id to the set of unique parent workspaces
            parent_workspaces.add(parent_id)

            # Raise error if workspace_id is not defined
            if workspace_id is None or workspace_id == "":
                raise WorkspaceDataIntegrityException(
                    f"Workspace ID is not defined for parent {parent_id}"
                )

            # Raise error if wdf_id is not defined but has values
            if wdf_id is not None and wdf_id != "":
                if wdf_values is None or wdf_values == []:
                    raise WorkspaceDataIntegrityException(
                        "WDF ID is defined but no WDF values are provided",
                        validation_context,
                    )

                # Add wdf_id to the parent-wdf dict if the value is defined
                if not parent_wdf_map.get(parent_id):
                    parent_wdf_map[parent_id] = []

                parent_wdf_map[parent_id].append(wdf_id)

            # Raise error if wdf_values are defined but wdf_id is not defined
            if wdf_values is not None and wdf_values != []:
                if wdf_id is None or wdf_id == "":
                    raise WorkspaceDataIntegrityException(
                        "WDF values are provided but WDF ID is not defined.",
                        validation_context,
                    )

            parent_child_wdf_ids.append((parent_id, workspace_id, wdf_id))

        # Check whether there are non-unique combinations in data
        if len(parent_child_wdf_ids) != len(set(parent_child_wdf_ids)):
            # Log the error to the database as a warning, but continue execution
            self.logger.warning(
                "Duplicate combinations of parent_id, workspace_id, "
                + "wdf_id exist in the source data."
            )

        return parent_workspaces, parent_wdf_map

    def _check_parent_exist(self, parent_id: str) -> None:
        """
        Raises an error if a parent workspace does not exist in Panther.
        """
        if not self.api.check_workspace_exists(parent_id):
            raise WorkspaceException(
                f"Parent workspace {parent_id} does not exist in Panther.",
                workspace_id=parent_id,
            )

    def _check_wdf_is_set_on_parent(
        self, parent_id: str, source_wdf_ids: list[str]
    ) -> None:
        """Raises an error if the parent workspace does not contain any of the defined wdf_id."""
        wdf_response: Response = self.api.get_all_workspace_data_filters(
            parent_id
        )
        wdf_json: dict[str, Any] = wdf_response.json()
        wdf_data: list[dict[str, Any]] = wdf_json.get("data", [])
        wdf_ids_on_parent: set[str] = {wdf["id"] for wdf in wdf_data}

        for source_wdf_id in source_wdf_ids:
            if source_wdf_id not in wdf_ids_on_parent:
                raise WorkspaceException(
                    f"WDF is not set on parent workspace {parent_id}.",
                    wdf_id=source_wdf_id,
                    workspace_id=parent_id,
                )

    def validate_source_data(
        self, source_group: list[WorkspaceFullLoad]
    ) -> None:
        """
        Validates the source data integrity.

        **Raises error when**:
        - the list of workspaces is empty
        - parent_id is not defined
        - workspace_id is not defined
        - The parent workspace does not exist
        - The parent workspace does not contain defined wdf_id.
        - wdf_id is defined but wdf_values is not defined
        - wdf_values are defined but wdf_id is not defined

        **Logs a warning when**:
        - There are more values for the parent_id, workspace_id, wdf_id combination.
        """
        if not source_group:
            # Raise error if source is empty
            raise WorkspaceException(
                "No workspaces found in the source database."
            )

        unique_parents, parent_wdf_map = self._check_basic_integrity(
            source_group
        )

        for parent_id in unique_parents:
            self._check_parent_exist(parent_id)

            self._check_wdf_is_set_on_parent(
                parent_id, parent_wdf_map[parent_id]
            )

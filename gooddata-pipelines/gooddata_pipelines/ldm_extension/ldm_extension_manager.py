# (C) 2025 GoodData Corporation
"""Module orchestrating the custom fields logic."""

from pathlib import Path

from gooddata_sdk.sdk import GoodDataSdk
from gooddata_sdk.utils import PROFILES_FILE_PATH, profile_content

from gooddata_pipelines.api import GoodDataApi
from gooddata_pipelines.ldm_extension.input_processor import (
    LdmExtensionDataProcessor,
)
from gooddata_pipelines.ldm_extension.input_validator import (
    LdmExtensionDataValidator,
)
from gooddata_pipelines.ldm_extension.models.aliases import (
    DatasetId,
    WorkspaceId,
)
from gooddata_pipelines.ldm_extension.models.analytical_object import (
    AnalyticalObject,
    AnalyticalObjects,
)
from gooddata_pipelines.ldm_extension.models.custom_data_object import (
    CustomDataset,
    CustomDatasetDefinition,
    CustomFieldDefinition,
)
from gooddata_pipelines.logger.logger import LogObserver


class LdmExtensionManager:
    """Manager for creating custom datasets and fields in GoodData workspaces."""

    INDENT = " " * 2

    @classmethod
    def create(cls, host: str, token: str) -> "LdmExtensionManager":
        return cls(host=host, token=token)

    @classmethod
    def create_from_profile(
        cls,
        profile: str = "default",
        profiles_path: Path = PROFILES_FILE_PATH,
    ) -> "LdmExtensionManager":
        """Creates a provisioner instance using a GoodData profile file."""
        content = profile_content(profile, profiles_path)
        return cls(host=content["host"], token=content["token"])

    def __init__(self, host: str, token: str):
        self._validator = LdmExtensionDataValidator()
        self._processor = LdmExtensionDataProcessor()
        self._sdk = GoodDataSdk.create(host_=host, token_=token)
        self._api = GoodDataApi(host=host, token=token)
        self.logger = LogObserver()

    def _get_objects_with_invalid_relations(
        self, workspace_id: str
    ) -> list[AnalyticalObject]:
        """Check for invalid references in the provided analytical objects.

        This method checks if the references in the provided analytical objects
        are valid. It returns a set of analytical objects that have invalid references.

        Args:
            workspace_id (str): The ID of the workspace to check.

        Returns:
            list[AnalyticalObject]: Set of analytical objects with invalid references.
        """

        analytical_objects: list[AnalyticalObject] = (
            self._get_analytical_objects(workspace_id=workspace_id)
        )

        objects_with_invalid_relations = [
            obj
            for obj in analytical_objects
            if not obj.attributes.are_relations_valid
        ]
        return objects_with_invalid_relations

    def _get_analytical_objects(
        self, workspace_id: str
    ) -> list[AnalyticalObject]:
        """Get analytical objects in the workspace.

        This method retrieves all analytical objects (metrics, visualizations, dashboards)
        in the specified workspace and returns them as a list.

        Args:
            workspace_id (str): The ID of the workspace to retrieve objects from.

        Returns:
            list[AnalyticalObject]: List of analytical objects in the workspace.
        """
        metrics_response = self._api.get_all_metrics(workspace_id)
        visualizations_response = self._api.get_all_visualization_objects(
            workspace_id
        )
        dashboards_response = self._api.get_all_dashboards(workspace_id)

        self._api.raise_if_response_not_ok(
            metrics_response,
            visualizations_response,
            dashboards_response,
        )
        metrics = AnalyticalObjects(**metrics_response.json())
        visualizations = AnalyticalObjects(**visualizations_response.json())
        dashboards = AnalyticalObjects(**dashboards_response.json())

        return metrics.data + visualizations.data + dashboards.data

    @staticmethod
    def _new_ldm_does_not_invalidate_relations(
        current_invalid_relations: list[AnalyticalObject],
        new_invalid_relations: list[AnalyticalObject],
    ) -> bool:
        """Check if the new LDM does not invalidate any new relations.

        This method compares the lists of analytical objects containing invalid
        relations. It creates sets of object IDs for each list and compares them.

        If the set of new invalid relations is a subset of the set of current
        invalid relations (that is before the changes to the LDM), the new LDM
        does not invalidate any new relations and `True` is returned.

        If the set of new invalid relations is not a subset of the current one,
        it means that the new LDM invalidates new relations and `False` is returned.

        Args:
            current_invalid_relations (list[AnalyticalObject]): The current (before
                changes to LDM) invalid relations.
            new_invalid_relations (list[AnalyticalObject]): The new (after changes to
                LDM) invalid relations.

        Returns:
            bool: True if the new LDM does not invalidate any relations, False otherwise.
        """
        # Create a set of IDs for each group, then compare those sets
        set_current_invalid_relations = {
            obj.id for obj in current_invalid_relations
        }
        set_new_invalid_relations = {obj.id for obj in new_invalid_relations}

        # If the set of new invalid relations is a subset of the current one,
        return set_new_invalid_relations.issubset(set_current_invalid_relations)

    def _process_with_relations_check(
        self,
        validated_data: dict[WorkspaceId, dict[DatasetId, CustomDataset]],
    ) -> None:
        """Check whether relations of analytical objects are valid before and after
        updating the LDM in the GoodData workspace.
        """
        # Iterate through the workspaces.
        for workspace_id, datasets in validated_data.items():
            self.logger.info(f"⚙️ Processing workspace {workspace_id}...")
            # Get current workspace layout
            current_layout = (
                self._sdk.catalog_workspace.get_declarative_workspace(
                    workspace_id
                )
            )
            # Get a set of objects with invalid relations from current workspace state
            current_invalid_relations = (
                self._get_objects_with_invalid_relations(
                    workspace_id=workspace_id
                )
            )

            # Put the LDM with custom datasets into the GoodData workspace.
            self._sdk.catalog_workspace_content.put_declarative_ldm(
                workspace_id=workspace_id,
                ldm=self._processor.datasets_to_ldm(datasets),
            )

            # Get a set of objects with invalid relations from the new workspace state
            new_invalid_relations = self._get_objects_with_invalid_relations(
                workspace_id=workspace_id
            )

            if self._new_ldm_does_not_invalidate_relations(
                current_invalid_relations, new_invalid_relations
            ):
                self._log_success_message(workspace_id)
                continue

            self.logger.error(
                f"❌ Difference in invalid relations found in workspace {workspace_id}."
            )
            self._log_diff_invalid_relations(
                current_invalid_relations, new_invalid_relations
            )

            self.logger.info(
                f"{self.INDENT}⚠️ Reverting the workspace layout to the original state."
            )
            # Put the original workspace layout back to the workspace
            try:
                self._sdk.catalog_workspace.put_declarative_workspace(
                    workspace_id=workspace_id, workspace=current_layout
                )
            except Exception as e:
                self.logger.error(
                    f"Failed to revert workspace layout in {workspace_id}: {e}"
                )

    def _log_diff_invalid_relations(
        self,
        current_invalid_relations: list[AnalyticalObject],
        new_invalid_relations: list[AnalyticalObject],
    ) -> None:
        """Logs objects with newly invalid relations.

        Objects which previously did not have invalid relations, but do so after
        updating the LDM, are logged.
        """
        # TODO: test !
        diff_to_log: list[str] = []
        for obj in new_invalid_relations:
            if obj not in current_invalid_relations:
                diff_to_log.append(
                    f"{self.INDENT}∙ {obj.id} ({obj.type}) {obj.attributes.title}"
                )
        joined_diff_to_log = "\n".join(diff_to_log)
        error_message = f"{self.INDENT}Objects with newly invalidated relations:\n{joined_diff_to_log}"

        self.logger.error(error_message)

    def _process_without_relations_check(
        self,
        validated_data: dict[WorkspaceId, dict[DatasetId, CustomDataset]],
    ) -> None:
        """Update the LDM in the GoodData workspace without checking relations."""
        for workspace_id, datasets in validated_data.items():
            # Put the LDM with custom datasets into the GoodData workspace.
            self._sdk.catalog_workspace_content.put_declarative_ldm(
                workspace_id=workspace_id,
                ldm=self._processor.datasets_to_ldm(datasets),
            )
            self._log_success_message(workspace_id)

    def _log_success_message(self, workspace_id: str) -> None:
        """Log a success message after updating the workspace LDM."""
        self.logger.info(f"✅ LDM in {workspace_id} updated successfully.")

    def process(
        self,
        custom_datasets: list[CustomDatasetDefinition],
        custom_fields: list[CustomFieldDefinition],
        check_relations: bool = True,
    ) -> None:
        """Create custom datasets and fields in GoodData workspaces.

        Creates custom datasets and fields to extend the Logical Data Model (LDM)
        in GoodData workspaces based on the provided raw data definitions. The raw
        data is validated by Pydantic models (CustomDatasetDefinition and CustomFieldDefinition).
        The defined datasets and fields are then uploaded to GoodData Cloud.

        Args:
            custom_datasets (list[CustomDatasetDefinition]): List of custom dataset definitions.
            custom_fields (list[CustomFieldDefinition]): List of custom field definitions.
            check_relations (bool): If True, checks for invalid relations in the workspace
                after updating the LDM. If the number of invalid relations increases,
                the LDM will be reverted to its previous state. If False, the check
                is skiped and the LDM is updated directly. Defaults to True.

        Raises:
            ValueError: If there are validation errors in the dataset or field definitions.
        """
        # Validate raw data and aggregate the custom field and dataset
        # definitions per workspace.
        validated_data: dict[WorkspaceId, dict[DatasetId, CustomDataset]] = (
            self._validator.validate(custom_datasets, custom_fields)
        )

        if check_relations:
            # Process the validated data with relations check.
            self._process_with_relations_check(validated_data)
        else:
            self._process_without_relations_check(validated_data)

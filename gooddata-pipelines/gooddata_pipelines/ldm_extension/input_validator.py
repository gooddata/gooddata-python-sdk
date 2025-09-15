# (C) 2025 GoodData Corporation
"""Module for validating custom fields input data.

This module is responsible for validating custom fields input data checking for
row level and aggregated constraints.
"""

from collections import Counter
from typing import Any, TypeVar

from pydantic import BaseModel

from gooddata_pipelines.ldm_extension.models.aliases import (
    DatasetId,
    WorkspaceId,
)
from gooddata_pipelines.ldm_extension.models.custom_data_object import (
    CustomDataset,
    CustomDatasetDefinition,
    CustomFieldDefinition,
    CustomFieldType,
)


class LdmExtensionDataValidator:
    ModelT = TypeVar("ModelT", bound=BaseModel)

    def validate(
        self,
        dataset_definitions: list[CustomDatasetDefinition],
        field_definitions: list[CustomFieldDefinition],
    ) -> dict[WorkspaceId, dict[DatasetId, CustomDataset]]:
        """Validate dataset and field definitions.

        Validates the dataset definitions and field definitions by using Pydantic
        models to check row level constraints, then aggregates the definitions
        per workspace, while checking for integrity on aggregated level, i.e.,
        uniqueness of combinations of identifieres on workspace level.

        Args:
            raw_dataset_definitions (list[dict[str, str]]): List of raw dataset definitions to validate.
            raw_field_definitions (list[dict[str, str]]): List of raw field definitions to validate.
        Returns:
            dict[WorkspaceId, dict[DatasetId, CustomDataset]]:
                Dictionary of validated dataset definitions per workspace,
                where each dataset contains its custom fields:
                ```python
                {
                    "workspace_id_1": {
                        "dataset_id_1": CustomDataset(...),
                        "dataset_id_2": CustomDataset(...),
                    },
                    ...
                }
                ```
        """

        # First, validate the dataset definitions and aggregate them per workspace.
        validated_data = self._validate_dataset_definitions(dataset_definitions)

        # Then validate the field definitions and connect them to the datasets
        validated_data = self._validate_field_definitions(
            validated_data, field_definitions
        )

        return validated_data

    def _validate_dataset_definitions(
        self,
        dataset_definitions: list[CustomDatasetDefinition],
    ) -> dict[WorkspaceId, dict[DatasetId, CustomDataset]]:
        self._check_dataset_combinations(dataset_definitions)

        validated_definitions: dict[
            WorkspaceId, dict[DatasetId, CustomDataset]
        ] = {}
        for definition in dataset_definitions:
            validated_definitions.setdefault(definition.workspace_id, {})[
                definition.dataset_id
            ] = CustomDataset(definition=definition, custom_fields=[])

        return validated_definitions

    def _check_dataset_combinations(
        self, dataset_definitions: list[CustomDatasetDefinition]
    ) -> None:
        """Check integrity of provided dataset definitions.

        Validation criteria:
            - workspace_id + dataset_id must be unique across all dataset definitions.

        Args:
            dataset_definitions (list[CustomDatasetDefinition]): List of dataset definitions to check.
        Raises:
            ValueError: If there are duplicate dataset definitions based on workspace_id and dataset_id.
        """
        workspace_dataset_combinations = [
            (definition.workspace_id, definition.dataset_id)
            for definition in dataset_definitions
        ]
        if len(workspace_dataset_combinations) != len(
            set(workspace_dataset_combinations)
        ):
            duplicates = self._get_duplicates(workspace_dataset_combinations)
            raise ValueError(
                "Duplicate dataset definitions found in the raw dataset "
                + f"definitions (workspace_id, dataset_id): {duplicates}"
            )

    @staticmethod
    def _get_duplicates(list_to_check: list[Any]) -> list[Any]:
        """Get duplicates from a list.

        Args:
            list_to_check (list[Any]): List of items to check for duplicates.
        Returns:
            list[Any]: List of duplicate items.
        """
        counts = Counter(list_to_check)
        return [item for item, count in counts.items() if count > 1]

    def _check_field_combinations(
        self, field_definitions: list[CustomFieldDefinition]
    ) -> None:
        """Check integrity of provided field definitions.

        Validation criteria (per workspace):
            - unique workspace_id + cf_id combinations (only for attribute and fact custom_field_type)
            - there is no row with the same dataset_id and cf_id (only for date custom_field_type)

        Args:
            field_definitions (list[CustomFieldDefinition]): List of field definitions to check.
        Raises:
            ValueError: If there are duplicate field definitions based on workspace_id and cf_id.
        """
        workspace_field_combinations: set[tuple[str, str]] = set()
        dataset_field_combinations: set[tuple[str, str]] = set()

        for field in field_definitions:
            if field.custom_field_type in [
                CustomFieldType.ATTRIBUTE,
                CustomFieldType.FACT,
            ]:
                combination = (field.workspace_id, field.custom_field_id)
                if combination in workspace_field_combinations:
                    raise ValueError(
                        f"Duplicate custom field found for workspace {field.workspace_id} "
                        + f"with field ID {field.custom_field_id}"
                    )
                workspace_field_combinations.add(combination)

            elif field.custom_field_type == CustomFieldType.DATE:
                combination = (field.dataset_id, field.custom_field_id)
                if combination in dataset_field_combinations:
                    raise ValueError(
                        f"Duplicate custom field found for dataset {field.dataset_id} "
                        + f"with field ID {field.custom_field_id}"
                    )
                dataset_field_combinations.add(combination)

    def _validate_field_definitions(
        self,
        validated_definitions: dict[
            WorkspaceId, dict[DatasetId, CustomDataset]
        ],
        field_definitions: list[CustomFieldDefinition],
    ) -> dict[WorkspaceId, dict[DatasetId, CustomDataset]]:
        """Validates custom field definitions amd connects them to the datasets.

        Args:
            validated_definitions (dict[WorkspaceId, dict[DatasetId, CustomDataset]]):
                Dictionary of validated dataset definitions per workspace.
            raw_field_definitions (list[dict[str, str]]): List of raw field definitions to validate.
        Returns:
            dict[WorkspaceId, dict[DatasetId, CustomDataset]]:
                Updated dictionary of validated dataset definitions with custom fields added.
        """
        self._check_field_combinations(field_definitions)

        for field_definition in field_definitions:
            validated_definitions[field_definition.workspace_id][
                field_definition.dataset_id
            ].custom_fields.append(field_definition)

        return validated_definitions

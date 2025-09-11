# (C) 2025 GoodData Corporation
"""Module for processing validated custom datasets and fields data.

This module is responsible for converting validated custom datasets and fields
into objects defined in the GoodData Python SDK.
"""

from gooddata_sdk.catalog.identifier import (
    CatalogDatasetWorkspaceDataFilterIdentifier,
    CatalogGrainIdentifier,
    CatalogReferenceIdentifier,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.data_filter_references import (
    CatalogDeclarativeWorkspaceDataFilterReferences,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.dataset.dataset import (
    CatalogDataSourceTableIdentifier,
    CatalogDeclarativeAttribute,
    CatalogDeclarativeDataset,
    CatalogDeclarativeDatasetSql,
    CatalogDeclarativeFact,
    CatalogDeclarativeReference,
    CatalogDeclarativeReferenceSource,
    CatalogDeclarativeWorkspaceDataFilterColumn,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.date_dataset.date_dataset import (
    CatalogDeclarativeDateDataset,
    CatalogGranularitiesFormatting,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.ldm import (
    CatalogDeclarativeLdm,
    CatalogDeclarativeModel,
)

from gooddata_pipelines.ldm_extension.models.aliases import DatasetId
from gooddata_pipelines.ldm_extension.models.custom_data_object import (
    ColumnDataType,
    CustomDataset,
    CustomFieldDefinition,
    CustomFieldType,
)


class LdmExtensionDataProcessor:
    """Create GoodData LDM from validated custom datasets and fields."""

    DATE_GRANULARITIES: list[str] = [
        "MINUTE",
        "HOUR",
        "DAY",
        "WEEK",
        "MONTH",
        "QUARTER",
        "YEAR",
        "MINUTE_OF_HOUR",
        "HOUR_OF_DAY",
        "DAY_OF_WEEK",
        "DAY_OF_MONTH",
        "DAY_OF_YEAR",
        "WEEK_OF_YEAR",
        "MONTH_OF_YEAR",
        "QUARTER_OF_YEAR",
    ]

    @staticmethod
    def _attribute_from_field(
        dataset_name: str,
        custom_field: CustomFieldDefinition,
    ) -> CatalogDeclarativeAttribute:
        """Assign a declarative attribute from a custom field definition."""
        return CatalogDeclarativeAttribute(
            id=custom_field.custom_field_id,
            title=custom_field.custom_field_name,
            source_column=custom_field.custom_field_source_column,
            labels=[],
            source_column_data_type=custom_field.custom_field_source_column_data_type.value,
            tags=[dataset_name],
        )

    @staticmethod
    def _fact_from_field(
        dataset_name: str,
        custom_field: CustomFieldDefinition,
    ) -> CatalogDeclarativeFact:
        """Assign a declarative fact from a custom field definition."""
        return CatalogDeclarativeFact(
            id=custom_field.custom_field_id,
            title=custom_field.custom_field_name,
            source_column=custom_field.custom_field_source_column,
            source_column_data_type=custom_field.custom_field_source_column_data_type.value,
            tags=[dataset_name],
        )

    def _date_from_field(
        self,
        dataset_name: str,
        custom_field: CustomFieldDefinition,
    ) -> CatalogDeclarativeDateDataset:
        """Assign a declarative date dataset from a custom field definition."""

        return CatalogDeclarativeDateDataset(
            id=custom_field.custom_field_id,
            title=custom_field.custom_field_name,
            granularities_formatting=CatalogGranularitiesFormatting(
                title_base="",
                title_pattern="%titleBase - %granularityTitle",
            ),
            granularities=self.DATE_GRANULARITIES,
            tags=[dataset_name],
        )

    @staticmethod
    def _date_ref_from_field(
        custom_field: CustomFieldDefinition,
    ) -> CatalogDeclarativeReference:
        """Create a date reference from a custom field definition."""
        return CatalogDeclarativeReference(
            identifier=CatalogReferenceIdentifier(
                id=custom_field.custom_field_id
            ),
            multivalue=False,
            sources=[
                CatalogDeclarativeReferenceSource(
                    column=custom_field.custom_field_source_column,
                    target=CatalogGrainIdentifier(
                        id=custom_field.custom_field_id,
                        type=CustomFieldType.DATE.value,
                    ),
                    data_type=custom_field.custom_field_source_column_data_type.value,
                )
            ],
        )

    @staticmethod
    def _get_sources(
        dataset: CustomDataset,
    ) -> tuple[
        CatalogDataSourceTableIdentifier | None,
        CatalogDeclarativeDatasetSql | None,
    ]:
        """Get the data source table and SQL from the dataset definition."""
        # We will have either a table id or a sql statement. Let's store
        # whatever data is available to variables and pass it to the
        # dataset. Both can be object instances or None, but at least one
        # should be valid as per prior validation.
        dataset_source_table_id = (
            CatalogDataSourceTableIdentifier(
                id=dataset.definition.dataset_source_table,
                data_source_id=dataset.definition.dataset_datasource_id,
                path=[dataset.definition.dataset_source_table],
            )
            if dataset.definition.dataset_source_table
            else None
        )

        dataset_sql = (
            CatalogDeclarativeDatasetSql(
                statement=dataset.definition.dataset_source_sql,
                data_source_id=dataset.definition.dataset_datasource_id,
            )
            if dataset.definition.dataset_source_sql
            else None
        )
        return dataset_source_table_id, dataset_sql

    def datasets_to_ldm(
        self, datasets: dict[DatasetId, CustomDataset]
    ) -> CatalogDeclarativeModel:
        """Convert validated datasets to GoodData declarative model.

        Args:
            datasets (dict[DatasetId, CustomDataset]): Dictionary of validated
                datasets.
        Returns:
            CatalogDeclarativeModel: GoodData declarative model representation
                of the datasets.
        """

        declarative_datasets: list[CatalogDeclarativeDataset] = []

        # Date dimensions are not stored in a dataset, but as a separate datasets
        # in `date_instances` object on the LDM
        date_instances: list[CatalogDeclarativeDateDataset] = []

        for dataset in datasets.values():
            date_references: list[CatalogDeclarativeReference] = []
            attributes: list[CatalogDeclarativeAttribute] = []
            facts: list[CatalogDeclarativeFact] = []

            # Iterate through the custom fields and create the appropriate objects
            for custom_field in dataset.custom_fields:
                if custom_field.custom_field_type == CustomFieldType.ATTRIBUTE:
                    attributes.append(
                        self._attribute_from_field(
                            dataset.definition.dataset_name, custom_field
                        )
                    )

                elif custom_field.custom_field_type == CustomFieldType.FACT:
                    facts.append(
                        self._fact_from_field(
                            dataset.definition.dataset_name, custom_field
                        )
                    )

                # Process date dimensions and store them to date_instances. Date
                # dimensions are not stored in a dataset, but as a separate dataset.
                # However, they need to be referenced in the dataset references to
                # create the connection between the dataset and the date dimension
                # in the GoodData Logical Data Model.
                elif custom_field.custom_field_type == CustomFieldType.DATE:
                    # Add the date dimension to the date_instances
                    date_instances.append(
                        self._date_from_field(
                            dataset.definition.dataset_name, custom_field
                        )
                    )

                    # Create a reference so that the date dimension is connected
                    # to the dataset in the GoodData Logical Data Model.
                    date_references.append(
                        self._date_ref_from_field(custom_field)
                    )

                else:
                    raise ValueError(
                        f"Unsupported custom field type: {custom_field.custom_field_type}"
                    )

            # Get the data source info
            dataset_source_table_id, dataset_sql = self._get_sources(dataset)

            # Construct the declarative dataset object and append it to the list.
            declarative_datasets.append(
                CatalogDeclarativeDataset(
                    id=dataset.definition.dataset_id,
                    title=dataset.definition.dataset_name,
                    grain=[],
                    references=[
                        CatalogDeclarativeReference(
                            identifier=CatalogReferenceIdentifier(
                                id=dataset.definition.parent_dataset_reference,
                            ),
                            multivalue=True,
                            sources=[
                                CatalogDeclarativeReferenceSource(
                                    column=dataset.definition.dataset_reference_source_column,
                                    data_type=dataset.definition.dataset_reference_source_column_data_type.value,
                                    target=CatalogGrainIdentifier(
                                        id=dataset.definition.parent_dataset_reference_attribute_id,
                                        type=CustomFieldType.ATTRIBUTE.value,
                                    ),
                                )
                            ],
                        ),
                    ]
                    + date_references,
                    description=None,
                    attributes=attributes,
                    facts=facts,
                    data_source_table_id=dataset_source_table_id,
                    sql=dataset_sql,
                    workspace_data_filter_columns=[
                        CatalogDeclarativeWorkspaceDataFilterColumn(
                            name=dataset.definition.workspace_data_filter_column_name,
                            data_type=ColumnDataType.STRING.value,
                        )
                    ],
                    workspace_data_filter_references=[
                        CatalogDeclarativeWorkspaceDataFilterReferences(
                            filter_id=CatalogDatasetWorkspaceDataFilterIdentifier(
                                id=dataset.definition.workspace_data_filter_id
                            ),
                            filter_column=dataset.definition.workspace_data_filter_column_name,
                            filter_column_data_type=ColumnDataType.STRING.value,
                        )
                    ],
                    tags=[dataset.definition.dataset_name],
                )
            )

        # Create the Logical Data Model from the datasets and the date instances.
        ldm = CatalogDeclarativeLdm(
            datasets=declarative_datasets, date_instances=date_instances
        )
        return CatalogDeclarativeModel(ldm=ldm)

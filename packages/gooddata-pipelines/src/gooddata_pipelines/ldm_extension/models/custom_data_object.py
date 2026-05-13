# (C) 2025 GoodData Corporation
"""This module defines enums and models used to represent the input data.

Models defined here are used to validate and structure the input data before
further processing.
"""

from enum import Enum

from pydantic import BaseModel, Field, model_validator


class CustomFieldType(str, Enum):
    """GoodData field types."""

    # NOTE: Start using StrEnum with Python 3.11
    ATTRIBUTE = "attribute"
    FACT = "fact"
    DATE = "date"


class ColumnDataType(str, Enum):
    """Supported data types"""

    # NOTE: Start using StrEnum with Python 3.11
    INT = "INT"
    STRING = "STRING"
    DATE = "DATE"
    NUMERIC = "NUMERIC"
    TIMESTAMP = "TIMESTAMP"
    TIMESTAMP_TZ = "TIMESTAMP_TZ"
    BOOLEAN = "BOOLEAN"


class CustomFieldDefinition(BaseModel):
    """Input model for custom field definition."""

    workspace_id: str
    dataset_id: str
    custom_field_id: str
    custom_field_name: str
    custom_field_type: CustomFieldType
    custom_field_source_column: str
    custom_field_source_column_data_type: ColumnDataType
    description: str | None = Field(
        default=None,
        description="Declarative description on the attribute, fact, or date dataset.",
    )
    tags: list[str] | None = Field(
        default=None,
        description="If set, replaces the default tag list (dataset display name only).",
    )

    @model_validator(mode="after")
    def check_ids_not_equal(self) -> "CustomFieldDefinition":
        """Check that custom field ID is not the same as dataset ID."""
        if self.custom_field_id == self.dataset_id:
            raise ValueError(
                f"Custom field ID {self.custom_field_id} cannot be the same as dataset ID {self.dataset_id}"
            )
        return self


class ParentDatasetReference(BaseModel):
    """One column of a (possibly composite) join to the parent dataset.

    A list of these on ``CustomDatasetDefinition.parent_dataset_references``
    supports multi-column foreign keys. Each entry binds a source column on the
    new dataset to a grain attribute on the parent.
    """

    attribute_id: str = Field(
        description="Attribute ID on the parent dataset that this column joins to.",
    )
    source_column: str = Field(
        description="Column name on this dataset used to join to the parent.",
    )
    data_type: ColumnDataType = Field(
        description="Data type of the source column.",
    )


class CustomDatasetDefinition(BaseModel):
    """Input model for custom dataset definition."""

    workspace_id: str
    dataset_id: str
    dataset_name: str
    dataset_datasource_id: str
    dataset_source_table: str | None
    dataset_source_sql: str | None
    parent_dataset_reference: str
    parent_dataset_reference_attribute_id: str | None = Field(
        default=None,
        deprecated=(
            "Use `parent_dataset_references` instead. "
            "This field will be removed in a future release."
        ),
    )
    dataset_reference_source_column: str | None = Field(
        default=None,
        deprecated=(
            "Use `parent_dataset_references` instead. "
            "This field will be removed in a future release."
        ),
    )
    dataset_reference_source_column_data_type: ColumnDataType | None = Field(
        default=None,
        deprecated=(
            "Use `parent_dataset_references` instead. "
            "This field will be removed in a future release."
        ),
    )
    parent_dataset_references: list[ParentDatasetReference] | None = Field(
        default=None,
        description="List of references to the parent dataset.",
    )
    workspace_data_filter_id: str
    workspace_data_filter_column_name: str
    dataset_description: str | None = Field(
        default=None,
        description="Declarative description on the custom dataset.",
    )
    dataset_tags: list[str] | None = Field(
        default=None,
        description="If set, replaces the default tag list (dataset display name only).",
    )

    @model_validator(mode="after")
    def check_source(self) -> "CustomDatasetDefinition":
        """At least one of dataset_source_table or dataset_source_sql is provided."""
        if not (self.dataset_source_table or self.dataset_source_sql):
            raise ValueError(
                "One of dataset_source_table and dataset_source_sql must be provided"
            )
        if self.dataset_source_table and self.dataset_source_sql:
            raise ValueError(
                "Only one of dataset_source_table and dataset_source_sql can be provided"
            )
        return self

    @model_validator(mode="after")
    def check_reference_form(self) -> "CustomDatasetDefinition":
        """Exactly one reference form must be set: either the new list or the legacy triple."""
        has_new = bool(self.parent_dataset_references)
        has_legacy = (
            self.parent_dataset_reference_attribute_id is not None
            or self.dataset_reference_source_column is not None
            or self.dataset_reference_source_column_data_type is not None
        )
        if has_new and has_legacy:
            raise ValueError(
                "Set either `parent_dataset_references` or the legacy single-column "
                "fields (`parent_dataset_reference_attribute_id`, "
                "`dataset_reference_source_column`, "
                "`dataset_reference_source_column_data_type`), not both."
            )
        if not has_new and not has_legacy:
            raise ValueError(
                "Provide either `parent_dataset_references` or the legacy single-column "
                "fields (`parent_dataset_reference_attribute_id`, "
                "`dataset_reference_source_column`, "
                "`dataset_reference_source_column_data_type`)."
            )
        return self


class CustomDataset(BaseModel):
    """Custom dataset with its definition and custom fields."""

    definition: CustomDatasetDefinition
    custom_fields: list[CustomFieldDefinition]

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
    """Input model for custom dataset definition.

    The reference to the parent dataset can be expressed in two ways:

    * The legacy single-column form via ``parent_dataset_reference_attribute_id``,
      ``dataset_reference_source_column`` and ``dataset_reference_source_column_data_type``.
      All three must be provided together.
    * The composite-friendly form via ``parent_dataset_references``: a list of
      ``ParentDatasetReference`` entries, one per join column.

    When ``parent_dataset_references`` is set and non-empty, it takes precedence
    and the legacy fields are ignored. Otherwise the legacy fields are used.

    Workspace data filter fields are optional. Both must be set together or
    both left unset; when set, a single-column WDF binding is emitted on the
    declarative dataset.
    """

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
            "Use `parent_dataset_references` for richer (composite-key) joins. "
            "This field will be removed in a future release."
        ),
    )
    dataset_reference_source_column: str | None = Field(
        default=None,
        deprecated=(
            "Use `parent_dataset_references` for richer (composite-key) joins. "
            "This field will be removed in a future release."
        ),
    )
    dataset_reference_source_column_data_type: ColumnDataType | None = Field(
        default=None,
        deprecated=(
            "Use `parent_dataset_references` for richer (composite-key) joins. "
            "This field will be removed in a future release."
        ),
    )
    parent_dataset_references: list[ParentDatasetReference] | None = Field(
        default=None,
        description=(
            "Composite-key reference to the parent dataset. When provided and "
            "non-empty, supersedes the legacy single-column reference fields."
        ),
    )
    workspace_data_filter_id: str | None = None
    workspace_data_filter_column_name: str | None = None
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
    def check_reference_form_exclusive(self) -> "CustomDatasetDefinition":
        """Reject mixing the legacy single-column fields with ``parent_dataset_references``.

        Forcing callers to pick one form prevents silent precedence surprises:
        without this check, setting both would quietly use the new list and
        ignore the legacy values, which is easy to miss when debugging.
        """
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
        return self

    @model_validator(mode="after")
    def check_wdf_pair(self) -> "CustomDatasetDefinition":
        """Workspace data filter id and column name must be provided together or both omitted."""
        has_id = self.workspace_data_filter_id is not None
        has_col = self.workspace_data_filter_column_name is not None
        if has_id != has_col:
            raise ValueError(
                "workspace_data_filter_id and workspace_data_filter_column_name "
                "must both be set or both be omitted"
            )
        return self


class CustomDataset(BaseModel):
    """Custom dataset with its definition and custom fields."""

    definition: CustomDatasetDefinition
    custom_fields: list[CustomFieldDefinition]

# (C) 2025 GoodData Corporation
import pytest

from gooddata_pipelines.ldm_extension.input_validator import (
    LdmExtensionDataValidator,
)
from gooddata_pipelines.ldm_extension.models.custom_data_object import (
    ColumnDataType,
    CustomDataset,
    CustomDatasetDefinition,
    CustomFieldDefinition,
    CustomFieldType,
)


@pytest.fixture
def valid_dataset_definitions():
    """Fixture to provide valid dataset definitions for testing."""
    return [
        CustomDatasetDefinition(
            workspace_id="ws1",
            dataset_id="ds1",
            dataset_name="Dataset 1",
            dataset_datasource_id="ds_source_1",
            dataset_source_table="table1",
            dataset_source_sql=None,
            parent_dataset_reference="parent1",
            parent_dataset_reference_attribute_id="parent1.id",
            dataset_reference_source_column="id",
            dataset_reference_source_column_data_type=ColumnDataType.STRING,
            workspace_data_filter_id="wdf1",
            workspace_data_filter_column_name="id",
        ),
        CustomDatasetDefinition(
            workspace_id="ws2",
            dataset_id="ds1",
            dataset_name="Dataset 2",
            dataset_datasource_id="ds_source_2",
            dataset_source_table="table2",
            dataset_source_sql=None,
            parent_dataset_reference="parent2",
            parent_dataset_reference_attribute_id="parent2.id",
            dataset_reference_source_column="id",
            dataset_reference_source_column_data_type=ColumnDataType.INT,
            workspace_data_filter_id="wdf2",
            workspace_data_filter_column_name="id",
        ),
    ]


@pytest.fixture
def valid_field_definitions():
    """Fixture to provide valid field definitions for testing."""
    return [
        CustomFieldDefinition(
            workspace_id="ws1",
            dataset_id="ds1",
            custom_field_id="cf1",
            custom_field_name="Field 1",
            custom_field_type=CustomFieldType.ATTRIBUTE,
            custom_field_source_column="col1",
            custom_field_source_column_data_type=ColumnDataType.STRING,
        ),
        CustomFieldDefinition(
            workspace_id="ws1",
            dataset_id="ds1",
            custom_field_id="cf2",
            custom_field_name="Field 2",
            custom_field_type=CustomFieldType.ATTRIBUTE,
            custom_field_source_column="col2",
            custom_field_source_column_data_type=ColumnDataType.STRING,
        ),
        CustomFieldDefinition(
            workspace_id="ws2",
            dataset_id="ds1",
            custom_field_id="cf3",
            custom_field_name="Field 3",
            custom_field_type=CustomFieldType.ATTRIBUTE,
            custom_field_source_column="col3",
            custom_field_source_column_data_type=ColumnDataType.STRING,
        ),
    ]


def test_validate_success(valid_dataset_definitions, valid_field_definitions):
    """Provide valid input data and expect successful validation."""
    validator = LdmExtensionDataValidator()
    result = validator.validate(
        valid_dataset_definitions, valid_field_definitions
    )
    assert isinstance(result, dict)
    assert "ws1" in result
    assert "ds1" in result["ws1"]
    assert isinstance(result["ws1"]["ds1"], CustomDataset)
    assert len(result["ws1"]["ds1"].custom_fields) == 2
    assert result["ws2"]["ds1"].custom_fields[0].custom_field_id == "cf3"


def test_duplicate_dataset_raises(valid_dataset_definitions):
    """Test that duplicate dataset definitions raise a ValueError."""
    # Add a duplicate dataset definition
    invalid = valid_dataset_definitions + valid_dataset_definitions
    validator = LdmExtensionDataValidator()
    with pytest.raises(ValueError, match="Duplicate dataset definitions"):
        validator.validate(invalid, [])


def test_duplicate_field_workspace_level(valid_dataset_definitions):
    """Duplicate cf_id for ATTRIBUTE in same workspace. should raise ValueError."""
    fields = [
        CustomFieldDefinition(
            workspace_id="ws1",
            dataset_id="ds1",
            custom_field_id="cf1",
            custom_field_type=CustomFieldType.ATTRIBUTE,
            custom_field_name="Field 1",
            custom_field_source_column="col1",
            custom_field_source_column_data_type=ColumnDataType.STRING,
        ),
        CustomFieldDefinition(
            workspace_id="ws1",
            dataset_id="ds2",
            custom_field_id="cf1",
            custom_field_type=CustomFieldType.ATTRIBUTE,
            custom_field_name="Field 2",
            custom_field_source_column="col2",
            custom_field_source_column_data_type=ColumnDataType.STRING,
        ),
    ]
    validator = LdmExtensionDataValidator()
    with pytest.raises(
        ValueError,
        match="Duplicate custom field found for workspace ws1 with field ID cf1",
    ):
        validator.validate(valid_dataset_definitions, fields)


def test_duplicate_field_dataset_level(valid_dataset_definitions):
    """Duplicate cf_id for DATE in same dataset. should raise ValueError."""
    fields = [
        CustomFieldDefinition(
            workspace_id="ws1",
            dataset_id="ds1",
            custom_field_id="cf1",
            custom_field_type=CustomFieldType.DATE,
            custom_field_name="Field 1",
            custom_field_source_column="col1",
            custom_field_source_column_data_type=ColumnDataType.DATE,
        ),
        CustomFieldDefinition(
            workspace_id="ws1",
            dataset_id="ds1",
            custom_field_id="cf1",
            custom_field_type=CustomFieldType.DATE,
            custom_field_name="Field 2",
            custom_field_source_column="col2",
            custom_field_source_column_data_type=ColumnDataType.DATE,
        ),
    ]
    validator = LdmExtensionDataValidator()
    with pytest.raises(
        ValueError,
        match="Duplicate custom field found for dataset ds1 with field ID cf1",
    ):
        validator.validate(valid_dataset_definitions, fields)

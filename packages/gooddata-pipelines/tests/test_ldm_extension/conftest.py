# (C) 2025 GoodData Corporation
import pytest

from gooddata_pipelines.ldm_extension.models.custom_data_object import (
    ColumnDataType,
    CustomDataset,
    CustomDatasetDefinition,
    CustomFieldDefinition,
    CustomFieldType,
)


@pytest.fixture
def mock_custom_field_attribute():
    return CustomFieldDefinition(
        workspace_id="workspace1",
        dataset_id="ds1",
        custom_field_id="attr1",
        custom_field_name="Attribute 1",
        custom_field_type=CustomFieldType.ATTRIBUTE,
        custom_field_source_column="col_attr1",
        custom_field_source_column_data_type=ColumnDataType.STRING,
    )


@pytest.fixture
def mock_custom_field_fact():
    return CustomFieldDefinition(
        workspace_id="workspace1",
        dataset_id="ds1",
        custom_field_id="fact1",
        custom_field_name="Fact 1",
        custom_field_type=CustomFieldType.FACT,
        custom_field_source_column="col_fact1",
        custom_field_source_column_data_type=ColumnDataType.INT,
    )


@pytest.fixture
def mock_custom_field_date():
    return CustomFieldDefinition(
        workspace_id="workspace1",
        dataset_id="ds1",
        custom_field_id="date1",
        custom_field_name="Date 1",
        custom_field_type=CustomFieldType.DATE,
        custom_field_source_column="col_date1",
        custom_field_source_column_data_type=ColumnDataType.DATE,
    )


@pytest.fixture
def mock_dataset_definition():
    return CustomDatasetDefinition(
        workspace_id="workspace1",
        dataset_id="ds1",
        dataset_name="Dataset 1",
        dataset_source_table="table1",
        dataset_datasource_id="ds_source",
        dataset_source_sql=None,
        parent_dataset_reference="parent_ds",
        parent_dataset_reference_attribute_id="parent_attr",
        dataset_reference_source_column="ref_col",
        dataset_reference_source_column_data_type=ColumnDataType.STRING,
        workspace_data_filter_id="wdf1",
        workspace_data_filter_column_name="col1",
    )


@pytest.fixture
def mock_custom_dataset(
    mock_dataset_definition,
    mock_custom_field_attribute,
    mock_custom_field_fact,
    mock_custom_field_date,
):
    return CustomDataset(
        definition=mock_dataset_definition,
        custom_fields=[
            mock_custom_field_attribute,
            mock_custom_field_fact,
            mock_custom_field_date,
        ],
    )

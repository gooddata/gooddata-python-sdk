# (C) 2025 GoodData Corporation
import pytest
from pydantic import ValidationError

from gooddata_pipelines.ldm_extension.models.custom_data_object import (
    ColumnDataType,
    CustomDataset,
    CustomDatasetDefinition,
    CustomFieldDefinition,
    CustomFieldType,
    ParentDatasetReference,
)


def make_valid_field_def(**kwargs):
    data = {
        "workspace_id": "ws1",
        "dataset_id": "ds1",
        "custom_field_id": "cf1",
        "custom_field_name": "Custom Field",
        "custom_field_type": CustomFieldType.ATTRIBUTE,
        "custom_field_source_column": "col1",
        "custom_field_source_column_data_type": ColumnDataType.STRING,
    }
    data.update(kwargs)
    return data


def make_valid_dataset_def(**kwargs):
    data = {
        "workspace_id": "ws1",
        "dataset_id": "ds1",
        "dataset_name": "Dataset",
        "dataset_datasource_id": "dsrc1",
        "dataset_source_table": "table1",
        "dataset_source_sql": None,
        "parent_dataset_reference": "parent_ds",
        "parent_dataset_reference_attribute_id": "parent_attr",
        "dataset_reference_source_column": "src_col",
        "dataset_reference_source_column_data_type": ColumnDataType.STRING,
        "workspace_data_filter_id": "wdf1",
        "workspace_data_filter_column_name": "col1",
    }
    data.update(kwargs)
    return data


def test_custom_field_definition_valid():
    field = CustomFieldDefinition(**make_valid_field_def())
    assert field.custom_field_id == "cf1"
    assert field.custom_field_type == CustomFieldType.ATTRIBUTE


def test_custom_field_definition_cf_id_equals_dataset_id_raises():
    data = make_valid_field_def(custom_field_id="ds1")
    with pytest.raises(ValidationError) as exc:
        CustomFieldDefinition(**data)
    assert "cannot be the same as dataset ID" in str(exc.value)


def test_custom_dataset_definition_valid_table():
    ds = CustomDatasetDefinition(**make_valid_dataset_def())
    assert ds.dataset_source_table == "table1"
    assert ds.dataset_source_sql is None


def test_custom_dataset_definition_valid_sql():
    data = make_valid_dataset_def(
        dataset_source_table=None, dataset_source_sql="SELECT 1"
    )
    ds = CustomDatasetDefinition(**data)
    assert ds.dataset_source_sql == "SELECT 1"
    assert ds.dataset_source_table is None


def test_custom_dataset_definition_both_none_raises():
    data = make_valid_dataset_def(
        dataset_source_table=None, dataset_source_sql=None
    )
    with pytest.raises(ValidationError) as exc:
        CustomDatasetDefinition(**data)
    assert "must be provided" in str(exc.value)


def test_custom_dataset_definition_both_provided_raises():
    data = make_valid_dataset_def(
        dataset_source_table="table1", dataset_source_sql="SELECT 1"
    )
    with pytest.raises(ValidationError) as exc:
        CustomDatasetDefinition(**data)
    assert (
        "Only one of dataset_source_table and dataset_source_sql can be provided"
        in str(exc.value)
    )


def test_custom_dataset_model():
    ds_def = CustomDatasetDefinition(**make_valid_dataset_def())
    field_def = CustomFieldDefinition(**make_valid_field_def())
    dataset = CustomDataset(definition=ds_def, custom_fields=[field_def])
    assert dataset.definition.dataset_id == "ds1"
    assert len(dataset.custom_fields) == 1
    assert dataset.custom_fields[0].custom_field_id == "cf1"


def test_custom_dataset_definition_parent_dataset_references_optional():
    """The new composite-reference field is optional and defaults to None."""
    ds = CustomDatasetDefinition(**make_valid_dataset_def())
    assert ds.parent_dataset_references is None


def test_custom_dataset_definition_parent_dataset_references_accepted():
    """Composite references can be provided via the new list field."""
    refs = [
        ParentDatasetReference(
            attribute_id="parent_pk1",
            source_column="src_col1",
            data_type=ColumnDataType.STRING,
        ),
        ParentDatasetReference(
            attribute_id="parent_pk2",
            source_column="src_col2",
            data_type=ColumnDataType.INT,
        ),
    ]
    data = make_valid_dataset_def(
        parent_dataset_reference_attribute_id=None,
        dataset_reference_source_column=None,
        dataset_reference_source_column_data_type=None,
        parent_dataset_references=refs,
    )
    ds = CustomDatasetDefinition(**data)
    assert ds.parent_dataset_references is not None
    assert len(ds.parent_dataset_references) == 2
    assert ds.parent_dataset_references[1].data_type == ColumnDataType.INT


def test_custom_dataset_definition_no_reference_form_raises():
    """Providing neither the legacy fields nor `parent_dataset_references` is rejected."""
    data = make_valid_dataset_def(
        parent_dataset_reference_attribute_id=None,
        dataset_reference_source_column=None,
        dataset_reference_source_column_data_type=None,
    )
    with pytest.raises(ValidationError) as exc:
        CustomDatasetDefinition(**data)
    assert "Provide either" in str(exc.value)


def test_custom_dataset_definition_mixed_reference_forms_raises():
    """Setting both legacy fields and `parent_dataset_references` is rejected."""
    data = make_valid_dataset_def(
        parent_dataset_references=[
            ParentDatasetReference(
                attribute_id="parent_pk",
                source_column="src_col",
                data_type=ColumnDataType.STRING,
            )
        ],
    )
    with pytest.raises(ValidationError) as exc:
        CustomDatasetDefinition(**data)
    assert "not both" in str(exc.value)


def test_custom_dataset_definition_legacy_reference_fields_optional():
    data = make_valid_dataset_def(
        parent_dataset_reference_attribute_id=None,
        dataset_reference_source_column=None,
        dataset_reference_source_column_data_type=None,
        parent_dataset_references=[
            ParentDatasetReference(
                attribute_id="parent_pk",
                source_column="src_col",
                data_type=ColumnDataType.STRING,
            )
        ],
    )
    ds = CustomDatasetDefinition(**data)
    assert ds.dataset_reference_source_column is None
    assert ds.parent_dataset_references is not None

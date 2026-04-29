# (C) 2025 GoodData Corporation
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.dataset.dataset import (
    CatalogDeclarativeDataset,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.ldm import (
    CatalogDeclarativeLdm,
    CatalogDeclarativeModel,
)

from gooddata_pipelines.ldm_extension.input_processor import (
    LdmExtensionDataProcessor,
)
from gooddata_pipelines.ldm_extension.models.custom_data_object import (
    ColumnDataType,
    CustomDataset,
    CustomDatasetDefinition,
)


def test_merge_into_empty_ldm(mock_custom_dataset):
    processor = LdmExtensionDataProcessor()
    empty = CatalogDeclarativeModel(
        ldm=CatalogDeclarativeLdm(datasets=[], date_instances=[])
    )
    merged = processor.merge_custom_ldm_into_existing(
        empty, {"ds1": mock_custom_dataset}
    )
    assert len(merged.ldm.datasets) == 1
    assert merged.ldm.datasets[0].id == "ds1"
    assert len(merged.ldm.date_instances) == 1


def test_merge_preserves_other_datasets(mock_custom_dataset):
    inherited = CatalogDeclarativeDataset(
        id="parent_only",
        title="Parent DS",
        grain=[],
        references=[],
    )
    existing = CatalogDeclarativeModel(
        ldm=CatalogDeclarativeLdm(datasets=[inherited], date_instances=[])
    )
    processor = LdmExtensionDataProcessor()
    merged = processor.merge_custom_ldm_into_existing(
        existing, {"ds1": mock_custom_dataset}
    )
    ids = {d.id for d in merged.ldm.datasets}
    assert ids == {"parent_only", "ds1"}


def test_merge_removes_managed_dataset_not_in_input():
    managed = CatalogDeclarativeDataset(
        id="managed_old",
        title="Old",
        grain=[],
        references=[],
        tags=["bca_tooling_managed"],
    )
    existing = CatalogDeclarativeModel(
        ldm=CatalogDeclarativeLdm(datasets=[managed], date_instances=[])
    )
    definition = CustomDatasetDefinition(
        workspace_id="workspace1",
        dataset_id="managed_new",
        dataset_name="Dataset New",
        dataset_datasource_id="dsrc1",
        dataset_source_table="table1",
        dataset_source_sql=None,
        parent_dataset_reference="parent_ds",
        parent_dataset_reference_attribute_id="parent_attr",
        dataset_reference_source_column="ref_col",
        dataset_reference_source_column_data_type=ColumnDataType.STRING,
        workspace_data_filter_id="wdf1",
        workspace_data_filter_column_name="col1",
    )
    incoming = CustomDataset(definition=definition, custom_fields=[])
    processor = LdmExtensionDataProcessor()
    merged = processor.merge_custom_ldm_into_existing(
        existing,
        {"managed_new": incoming},
        remove_managed_datasets_missing_from_input=True,
        management_tag="bca_tooling_managed",
    )
    assert [d.id for d in merged.ldm.datasets] == ["managed_new"]

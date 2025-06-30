# (C) 2022 GoodData Corporation
from __future__ import annotations

import copy
import json
from pathlib import Path
from unittest.mock import MagicMock

import attrs
from gooddata_sdk import (
    CatalogDatasetWorkspaceDataFilterIdentifier,
    CatalogDeclarativeAnalytics,
    CatalogDeclarativeExportDefinition,
    CatalogDeclarativeExportDefinitionRequestPayload,
    CatalogDeclarativeModel,
    CatalogDeclarativeWorkspaceDataFilterReferences,
    CatalogDependentEntitiesRequest,
    CatalogDependsOn,
    CatalogDependsOnDateFilter,
    CatalogEntityIdentifier,
    CatalogValidateByItem,
    CatalogWorkspace,
    DataSourceValidator,
    GoodDataSdk,
    ObjId,
)
from gooddata_sdk.compute.model.filter import AbsoluteDateFilter, RelativeDateFilter
from gooddata_sdk.utils import recreate_directory
from tests_support.vcrpy_utils import get_vcr

from tests.catalog.test_catalog_workspace import _refresh_workspaces

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures" / "workspace_content"


def _set_up_workspace_ldm(sdk: GoodDataSdk, workspace_id: str, identifier: str) -> None:
    workspace = CatalogWorkspace(workspace_id=identifier, name=identifier)
    sdk.catalog_workspace.create_or_update(workspace)

    ldm_o = sdk.catalog_workspace_content.get_declarative_ldm(workspace_id)
    sdk.catalog_workspace_content.put_declarative_ldm(identifier, ldm_o, standalone_copy=True)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_catalog_list_labels.yaml"))
def test_catalog_list_labels(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    labels_list = sdk.catalog_workspace_content.get_labels_catalog(test_config["workspace"])
    assert len(labels_list) == 31


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_catalog_list_facts.yaml"))
def test_catalog_list_facts(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    facts_list = sdk.catalog_workspace_content.get_facts_catalog(test_config["workspace"])
    assert len(facts_list) == 4


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_catalog_list_attributes.yaml"))
def test_catalog_list_attributes(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    attributes_list = sdk.catalog_workspace_content.get_attributes_catalog(test_config["workspace"])
    assert len(attributes_list) == 30


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_catalog_list_metrics.yaml"))
def test_catalog_list_metrics(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    metrics_list = sdk.catalog_workspace_content.get_metrics_catalog(test_config["workspace"])
    assert len(metrics_list) == 24


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_store_declarative_ldm.yaml"))
def test_store_declarative_ldm(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "store" / "workspace_content"
    workspace_id = test_config["workspace"]
    recreate_directory(path)

    ldm_e = sdk.catalog_workspace_content.get_declarative_ldm(workspace_id)
    sdk.catalog_workspace_content.store_declarative_ldm(workspace_id, path)
    ldm_o = sdk.catalog_workspace_content.load_declarative_ldm(workspace_id, path)

    assert ldm_e == ldm_o
    assert ldm_e.to_api().to_dict() == ldm_o.to_api().to_dict()


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_load_and_put_declarative_ldm.yaml"))
def test_load_and_put_declarative_ldm(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "load" / "workspace_content"
    workspace_id = test_config["workspace"]
    identifier = test_config["workspace_test"]

    try:
        workspace = CatalogWorkspace(workspace_id=identifier, name=identifier)
        sdk.catalog_workspace.create_or_update(workspace)
        ldm_e = sdk.catalog_workspace_content.get_declarative_ldm(workspace_id)

        sdk.catalog_workspace_content.load_and_put_declarative_ldm(identifier, path, standalone_copy=True)
        ldm_o = sdk.catalog_workspace_content.get_declarative_ldm(identifier)
        assert ldm_e != ldm_o
        ldm_e.remove_wdf_refs()
        assert ldm_e == ldm_o
        assert ldm_e.to_api().to_dict() == ldm_o.to_api().to_dict()
    finally:
        _refresh_workspaces(sdk)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_load_and_modify_ds_and_put_declarative_ldm.yaml"))
def test_load_and_modify_ds_and_put_declarative_ldm(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    workspace_id = test_config["workspace"]
    identifier = test_config["workspace_test"]
    workspace = CatalogWorkspace(workspace_id=identifier, name=identifier)
    validator = DataSourceValidator(sdk.catalog_data_source)
    data_source_mapping = {test_config["data_source"]: test_config["data_source2"]}
    sdk.catalog_workspace.create_or_update(workspace)

    ldm_e = sdk.catalog_workspace_content.get_declarative_ldm(workspace_id)
    ds_e = list(set([d.data_source_table_id.data_source_id for d in ldm_e.ldm.datasets]))
    assert ds_e == [test_config["data_source"]]

    try:
        sdk.catalog_workspace_content.put_declarative_ldm(identifier, ldm_e, validator, standalone_copy=True)
        assert True
        ldm_e.ldm.modify_mapped_data_source(data_source_mapping=data_source_mapping)
        sdk.catalog_workspace_content.put_declarative_ldm(identifier, ldm_e, validator, standalone_copy=True)
        assert False
    except ValueError:
        DataSourceValidator.validate_ldm = MagicMock(return_value=None)
        DataSourceValidator.validate_data_source_ids = MagicMock(return_value=None)

        reverse_data_source_mapping = {v: k for k, v in data_source_mapping.items()}

        ldm_e.ldm.modify_mapped_data_source(data_source_mapping=reverse_data_source_mapping)
        sdk.catalog_workspace_content.put_declarative_ldm(identifier, ldm_e, validator, standalone_copy=True)
        ldm_o = sdk.catalog_workspace_content.get_declarative_ldm(identifier)
        ds_o = list(set([d.data_source_table_id.data_source_id for d in ldm_o.ldm.datasets]))
        assert ds_o == [test_config["data_source"]]
    finally:
        _refresh_workspaces(sdk)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_load_ldm_and_modify_tables_columns_case.yaml"))
def test_load_ldm_and_modify_tables_columns_case(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    workspace_id = test_config["workspace"]
    ldm_e = sdk.catalog_workspace_content.get_declarative_ldm(workspace_id)
    ldm_e.ldm.change_tables_columns_case(upper_case=True)
    table_id = "campaign_channels"
    attribute_column = "campaign_channel_id"
    fact_column = "budget"
    reference_column = "campaign_id"
    assert ldm_e.ldm.datasets[0].data_source_table_id.id == table_id.upper()
    assert ldm_e.ldm.datasets[0].attributes[0].source_column == attribute_column.upper()
    assert ldm_e.ldm.datasets[0].facts[0].source_column == fact_column.upper()
    assert ldm_e.ldm.datasets[0].references[0].source_columns is None
    assert ldm_e.ldm.datasets[0].references[0].sources[0].column == reference_column.upper()
    # Test chaining approach as well
    data_source_mapping = {test_config["data_source"]: test_config["data_source2"]}
    ldm_o = attrs.evolve(
        ldm_e, ldm=ldm_e.ldm.modify_mapped_data_source(data_source_mapping).change_tables_columns_case(upper_case=False)
    )
    assert ldm_o.ldm.datasets[0].data_source_table_id.data_source_id == test_config["data_source2"]
    assert ldm_o.ldm.datasets[0].data_source_table_id.id == table_id
    assert ldm_o.ldm.datasets[0].attributes[0].source_column == attribute_column
    assert ldm_o.ldm.datasets[0].facts[0].source_column == fact_column
    assert ldm_o.ldm.datasets[0].references[0].source_columns is None
    assert ldm_e.ldm.datasets[0].references[0].sources[0].column == reference_column


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_store_declarative_analytics_model.yaml"))
def test_store_declarative_analytics_model(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "store" / "workspace_content"
    workspace_id = test_config["workspace"]
    recreate_directory(path)

    analytics_model_e = sdk.catalog_workspace_content.get_declarative_analytics_model(workspace_id)
    sdk.catalog_workspace_content.store_declarative_analytics_model(workspace_id, path)
    analytics_model_o = sdk.catalog_workspace_content.load_declarative_analytics_model(workspace_id, path)

    assert analytics_model_e == analytics_model_o
    assert analytics_model_e.to_api().to_dict() == analytics_model_o.to_api().to_dict()


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_load_and_put_declarative_analytics_model.yaml"))
def test_load_and_put_declarative_analytics_model(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "load" / "workspace_content"
    workspace_id = test_config["workspace"]
    identifier = test_config["workspace_test"]

    try:
        _set_up_workspace_ldm(sdk, workspace_id, identifier)
        analytics_model_e = sdk.catalog_workspace_content.get_declarative_analytics_model(
            workspace_id, exclude=["ACTIVITY_INFO"]
        )

        sdk.catalog_workspace_content.load_and_put_declarative_analytics_model(identifier, path)
        analytics_model_o = sdk.catalog_workspace_content.get_declarative_analytics_model(
            identifier, exclude=["ACTIVITY_INFO"]
        )
        assert analytics_model_e == analytics_model_o
        assert analytics_model_e.to_api().to_dict() == analytics_model_o.to_api().to_dict()
    finally:
        _refresh_workspaces(sdk)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_put_declarative_analytics_model.yaml"))
def test_put_declarative_analytics_model(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    identifier = test_put_declarative_analytics_model.__name__

    try:
        _set_up_workspace_ldm(sdk, test_config["workspace"], identifier)
        analytics_model_e = sdk.catalog_workspace_content.get_declarative_analytics_model(identifier)

        sdk.catalog_workspace_content.put_declarative_analytics_model(identifier, analytics_model_e)
        analytics_model_o = sdk.catalog_workspace_content.get_declarative_analytics_model(identifier)
        assert analytics_model_e == analytics_model_o
        assert analytics_model_e.to_api().to_dict() == analytics_model_o.to_api().to_dict()
    finally:
        _refresh_workspaces(sdk)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_put_declarative_ldm.yaml"))
def test_put_declarative_ldm(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    identifier = test_put_declarative_ldm.__name__
    workspace = CatalogWorkspace(workspace_id=identifier, name=identifier)
    sdk.catalog_workspace.create_or_update(workspace)

    ldm_e = sdk.catalog_workspace_content.get_declarative_ldm(test_config["workspace"])
    try:
        sdk.catalog_workspace_content.put_declarative_ldm(identifier, ldm_e, standalone_copy=True)
        ldm_o = sdk.catalog_workspace_content.get_declarative_ldm(identifier)
        assert ldm_e != ldm_o
        ldm_e.remove_wdf_refs()
        assert ldm_e == ldm_o
        assert ldm_e.to_api().to_dict() == ldm_o.to_api().to_dict()
    finally:
        _refresh_workspaces(sdk)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_get_declarative_analytics_model.yaml"))
def test_get_declarative_analytics_model(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "expected" / "declarative_analytics_model.json"
    analytics_model_o = sdk.catalog_workspace_content.get_declarative_analytics_model(
        test_config["workspace"], exclude=["ACTIVITY_INFO"]
    )

    with open(path) as f:
        data = json.load(f)

    expected_o = CatalogDeclarativeAnalytics.from_dict(data)

    assert analytics_model_o == expected_o
    assert analytics_model_o.to_api().to_dict(camel_case=True) == data


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_get_declarative_analytics_model_child.yaml"))
def test_get_declarative_analytics_model_child(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "expected" / "declarative_analytics_model_child.json"
    analytics_model_o = sdk.catalog_workspace_content.get_declarative_analytics_model(
        test_config["workspace_with_parent"], exclude=["ACTIVITY_INFO"]
    )

    with open(path) as f:
        data = json.load(f)

    expected_o = CatalogDeclarativeAnalytics.from_dict(data)

    assert analytics_model_o == expected_o
    assert analytics_model_o.to_api().to_dict(camel_case=True) == data


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_get_declarative_ldm.yaml"))
def test_get_declarative_ldm(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "expected" / "declarative_ldm.json"
    ldm_o = sdk.catalog_workspace_content.get_declarative_ldm(test_config["workspace"])

    with open(path) as f:
        data = json.load(f)

    expected_o = CatalogDeclarativeModel.from_dict(data)

    assert ldm_o == expected_o
    assert ldm_o.to_api().to_dict(camel_case=True) == data


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_catalog.yaml"))
def test_catalog_load(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    catalog = sdk.catalog_workspace_content.get_full_catalog(test_config["workspace"])

    # rough initial smoke-test; just do a quick 'rub'
    assert len(catalog.metrics) == 24
    assert len(catalog.datasets) == 6

    assert catalog.get_metric("order_amount") is not None
    assert catalog.get_metric("revenue") is not None
    assert catalog.get_dataset("order_lines") is not None
    assert catalog.get_dataset("products") is not None
    customer = catalog.get_dataset("customers")
    assert customer is not None
    assert customer.find_label_attribute(ObjId(id="region", type="label"))


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_catalog_availability.yaml"))
def test_catalog_availability(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    catalog = sdk.catalog_workspace_content.get_full_catalog(test_config["workspace"])
    claim_count = catalog.get_metric("campaign_spend")

    filtered_catalog = catalog.catalog_with_valid_objects(claim_count)

    # rough initial smoke-test; just do a quick 'rub' that filtered catalog has less entries than full catalog
    assert len(filtered_catalog.metrics) == 24
    assert len(filtered_catalog.datasets) == 3


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_get_dependent_entities_graph.yaml"))
def test_get_dependent_entities_graph(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    response = sdk.catalog_workspace_content.get_dependent_entities_graph(workspace_id=test_config["workspace"])

    assert len(response.graph.edges) == 191
    assert len(response.graph.nodes) == 117


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_get_dependent_entities_graph_from_entry_points.yaml"))
def test_get_dependent_entities_graph_from_entry_points(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    dependent_entities_request = CatalogDependentEntitiesRequest(
        identifiers=[CatalogEntityIdentifier(id="campaign_channel_id", type="attribute")]
    )
    response = sdk.catalog_workspace_content.get_dependent_entities_graph_from_entry_points(
        workspace_id=test_config["workspace"], dependent_entities_request=dependent_entities_request
    )

    assert len(response.graph.edges) == 1
    assert len(response.graph.nodes) == 2


@gd_vcr.use_cassette(str(_fixtures_dir / "ldm_store_load.yaml"))
def test_ldm_store_load(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "store"
    ldm = sdk.catalog_workspace_content.get_declarative_ldm(test_config["workspace"])

    sdk.catalog_workspace_content.store_ldm_to_disk(test_config["workspace"], path)
    loaded_ldm = sdk.catalog_workspace_content.load_ldm_from_disk(path)
    assert loaded_ldm == ldm


@gd_vcr.use_cassette(str(_fixtures_dir / "analytics_store_load.yaml"))
def test_analytics_store_load(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "store"
    analytics_model = sdk.catalog_workspace_content.get_declarative_analytics_model(test_config["workspace"])

    sdk.catalog_workspace_content.store_analytics_model_to_disk(test_config["workspace"], path)
    loaded_analytics_model = sdk.catalog_workspace_content.load_analytics_model_from_disk(path)
    assert loaded_analytics_model == analytics_model


@gd_vcr.use_cassette(str(_fixtures_dir / "label_elements.yaml"))
def test_label_elements(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    depends_on: CatalogDependsOn = CatalogDependsOn(label="order_status", values=["Canceled", "Delivered"])
    validate_by: CatalogValidateByItem = CatalogValidateByItem(id="revenue_top_10_percent", type="metric")
    absolute_filter: AbsoluteDateFilter = AbsoluteDateFilter(
        dataset=ObjId(type="dataset", id="date"),
        from_date="2150-07-01",
        to_date="2150-07-16",
    )
    relative_filter: RelativeDateFilter = RelativeDateFilter(
        dataset=ObjId(type="dataset", id="date"),
        granularity="DAY",
        from_shift=3600,
        to_shift=3700,
    )
    depends_on_date: CatalogDependsOn = CatalogDependsOnDateFilter(date_filter=absolute_filter)
    depends_on_date_relative: CatalogDependsOn = CatalogDependsOnDateFilter(date_filter=relative_filter)
    label_values = sdk.catalog_workspace_content.get_label_elements(
        test_config["workspace"], "order_status", [depends_on], []
    )
    assert label_values == ["Canceled", "Delivered"]
    label_values = sdk.catalog_workspace_content.get_label_elements(
        test_config["workspace"], "label/order_status", [], [validate_by]
    )
    assert label_values == ["Delivered"]
    label_values = sdk.catalog_workspace_content.get_label_elements(
        test_config["workspace"], ObjId(id="order_status", type="label")
    )
    assert label_values == ["Canceled", "Delivered", "Returned"]
    label_values = sdk.catalog_workspace_content.get_label_elements(
        test_config["workspace"], "order_status", [depends_on_date], []
    )
    assert label_values == []
    label_values = sdk.catalog_workspace_content.get_label_elements(
        test_config["workspace"], "order_status", [depends_on_date_relative], []
    )
    assert label_values == []
    exact_filter = None
    filter_by = None
    label_values = sdk.catalog_workspace_content.get_label_elements(
        test_config["workspace"], "order_status", [depends_on], [], exact_filter, filter_by
    )
    assert label_values == ["Canceled", "Delivered"]
    label_values = sdk.catalog_workspace_content.get_label_elements(
        test_config["workspace"], "label/order_status", pattern_filter="Deli"
    )
    assert label_values == ["Delivered"]
    label_values = sdk.catalog_workspace_content.get_label_elements(
        test_config["workspace"], "label/order_status", pattern_filter="Deli", complement_filter=True
    )
    assert label_values == ["Canceled", "Returned"]
    label_values = sdk.catalog_workspace_content.get_label_elements(
        test_config["workspace"], "label/order_status", sort_order="DESC"
    )
    assert label_values == ["Returned", "Delivered", "Canceled"]
    label_values = sdk.catalog_workspace_content.get_label_elements(
        test_config["workspace"], "label/order_status", offset=1, limit=1
    )
    assert label_values == ["Delivered"]


@gd_vcr.use_cassette(str(_fixtures_dir / "explicit_workspace_data_filter.yaml"))
def test_explicit_workspace_data_filter(test_config):
    """
    This test is run with the following env variable.

    GDC_FEATURES_VALUES_ENABLE_PDM_REMOVAL_DEPRECATION_PHASE: "true"
    """
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    dataset_id = "customers"

    model = sdk.catalog_workspace_content.get_declarative_ldm(test_config["workspace"])
    model_cpy = copy.deepcopy(model)
    try:
        reference = CatalogDeclarativeWorkspaceDataFilterReferences(
            filter_id=CatalogDatasetWorkspaceDataFilterIdentifier(id="wdf__region"),
            filter_column="wdf__region",
            filter_column_data_type="STRING",
        )
        customers = [dataset for dataset in model_cpy.ldm.datasets if dataset.id == dataset_id][0]
        customers.workspace_data_filter_references = [reference]

        sdk.catalog_workspace_content.put_declarative_ldm(workspace_id=test_config["workspace"], ldm=model_cpy)

        updated_ldm = sdk.catalog_workspace_content.get_declarative_ldm(workspace_id=test_config["workspace"])

        assert model_cpy == updated_ldm

        dataset = sdk.catalog_workspace_content.get_full_catalog(workspace_id=test_config["workspace"]).get_dataset(
            dataset_id
        )
        assert len(dataset.workspace_data_filter_references) == 1
    finally:
        _refresh_workspaces(sdk)


@gd_vcr.use_cassette(str(_fixtures_dir / "export_definition_analytics_layout.yaml"))
def test_export_definition_analytics_layout(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    try:
        export_definition = CatalogDeclarativeExportDefinition(
            id="export_definition_id",
            title="export_definition_title",
            request_payload=CatalogDeclarativeExportDefinitionRequestPayload(file_name="abc", format="CSV"),
        )
        export_definition.to_api()
        analytics_o = sdk.catalog_workspace_content.get_declarative_analytics_model(
            test_config["workspace"], exclude=["ACTIVITY_INFO"]
        )
        analytics_o.analytics.export_definitions = [export_definition]
        sdk.catalog_workspace_content.put_declarative_analytics_model(test_config["workspace"], analytics_o)
        analytics_e = sdk.catalog_workspace_content.get_declarative_analytics_model(
            test_config["workspace"], exclude=["ACTIVITY_INFO"]
        )
        assert analytics_o.analytics.export_definitions == analytics_e.analytics.export_definitions
    finally:
        _refresh_workspaces(sdk)

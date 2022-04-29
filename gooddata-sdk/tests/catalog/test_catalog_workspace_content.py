# (C) 2022 GoodData Corporation
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import vcr

from gooddata_sdk import CatalogWorkspace, DataSourceValidator, GoodDataSdk
from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.analytics_model import (
    CatalogDeclarativeAnalytics,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.ldm import CatalogDeclarativeModel
from gooddata_sdk.utils import create_directory
from tests import VCR_MATCH_ON

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures" / "workspaces"

gd_vcr = vcr.VCR(filter_headers=["authorization", "user-agent"], serializer="json", match_on=VCR_MATCH_ON)


def _set_up_workspace_ldm(sdk: GoodDataSdk, workspace_id: str, identifier: str) -> None:
    workspace = CatalogWorkspace(workspace_id=identifier, name=identifier)
    sdk.catalog_workspace.create_or_update(workspace)

    ldm_o = sdk.catalog_workspace_content.get_declarative_ldm(workspace_id)
    sdk.catalog_workspace_content.put_declarative_ldm(identifier, ldm_o)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_catalog_list_labels.json"))
def test_catalog_list_labels(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    labels_list = sdk.catalog_workspace_content.get_labels_catalog(test_config["workspace"])
    assert len(labels_list) == 21


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_catalog_list_facts.json"))
def test_catalog_list_facts(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    facts_list = sdk.catalog_workspace_content.get_facts_catalog(test_config["workspace"])
    assert len(facts_list) == 4


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_catalog_list_attributes.json"))
def test_catalog_list_attributes(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    attributes_list = sdk.catalog_workspace_content.get_attributes_catalog(test_config["workspace"])
    assert len(attributes_list) == 20


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_catalog_list_metrics.json"))
def test_catalog_list_metrics(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    metrics_list = sdk.catalog_workspace_content.get_metrics_catalog(test_config["workspace"])
    assert len(metrics_list) == 24


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_store_declarative_ldm.json"))
def test_store_declarative_ldm(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "store" / "workspace_content"
    workspace_id = test_config["workspace"]
    create_directory(path)

    ldm_e = sdk.catalog_workspace_content.get_declarative_ldm(workspace_id)
    sdk.catalog_workspace_content.store_declarative_ldm(workspace_id, path)
    ldm_o = sdk.catalog_workspace_content.load_declarative_ldm(workspace_id, path)

    assert ldm_e == ldm_o
    assert ldm_e.to_api().to_dict() == ldm_o.to_api().to_dict()


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_load_and_put_declarative_ldm.json"))
def test_load_and_put_declarative_ldm(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "load" / "workspace_content"
    workspace_id = test_config["workspace"]
    identifier = test_config["workspace_test"]
    workspace = CatalogWorkspace(workspace_id=identifier, name=identifier)
    sdk.catalog_workspace.create_or_update(workspace)

    ldm_e = sdk.catalog_workspace_content.get_declarative_ldm(workspace_id)

    try:
        sdk.catalog_workspace_content.load_and_put_declarative_ldm(identifier, path)
        ldm_o = sdk.catalog_workspace_content.get_declarative_ldm(identifier)
        assert ldm_e == ldm_o
        assert ldm_e.to_api().to_dict() == ldm_o.to_api().to_dict()
    finally:
        sdk.catalog_workspace.delete_workspace(identifier)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_load_and_modify_ds_and_put_declarative_ldm.json"))
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
        sdk.catalog_workspace_content.put_declarative_ldm(identifier, ldm_e, validator)
        assert True
        ldm_e.modify_mapped_data_source(data_source_mapping=data_source_mapping)
        sdk.catalog_workspace_content.put_declarative_ldm(identifier, ldm_e, validator)
        assert False
    except ValueError:
        DataSourceValidator.validate_ldm = MagicMock(return_value=None)
        DataSourceValidator.validate_data_source_ids = MagicMock(return_value=None)

        ldm_e.modify_mapped_data_source(data_source_mapping=data_source_mapping)
        sdk.catalog_workspace_content.put_declarative_ldm(identifier, ldm_e, validator)
        ldm_o = sdk.catalog_workspace_content.get_declarative_ldm(identifier)
        ds_o = list(set([d.data_source_table_id.data_source_id for d in ldm_o.ldm.datasets]))
        assert ds_o == [test_config["data_source2"]]
    finally:
        sdk.catalog_workspace.delete_workspace(identifier)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_store_declarative_analytics_model.json"))
def test_store_declarative_analytics_model(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "store" / "workspace_content"
    workspace_id = test_config["workspace"]
    create_directory(path)

    analytics_model_e = sdk.catalog_workspace_content.get_declarative_analytics_model(workspace_id)
    sdk.catalog_workspace_content.store_declarative_analytics_model(workspace_id, path)
    analytics_model_o = sdk.catalog_workspace_content.load_declarative_analytics_model(workspace_id, path)

    assert analytics_model_e == analytics_model_o
    assert analytics_model_e.to_api().to_dict() == analytics_model_o.to_api().to_dict()


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_load_and_put_declarative_analytics_model.json"))
def test_load_and_put_declarative_analytics_model(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "load" / "workspace_content"
    workspace_id = test_config["workspace"]
    identifier = test_config["workspace_test"]
    _set_up_workspace_ldm(sdk, workspace_id, identifier)
    analytics_model_e = sdk.catalog_workspace_content.get_declarative_analytics_model(workspace_id)

    try:
        sdk.catalog_workspace_content.load_and_put_declarative_analytics_model(identifier, path)
        analytics_model_o = sdk.catalog_workspace_content.get_declarative_analytics_model(identifier)
        assert analytics_model_e == analytics_model_o
        assert analytics_model_e.to_api().to_dict() == analytics_model_o.to_api().to_dict()
    finally:
        sdk.catalog_workspace.delete_workspace(identifier)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_put_declarative_analytics_model.json"))
def test_put_declarative_analytics_model(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    identifier = test_put_declarative_analytics_model.__name__
    _set_up_workspace_ldm(sdk, test_config["workspace"], identifier)
    analytics_model_e = sdk.catalog_workspace_content.get_declarative_analytics_model(identifier)

    try:
        sdk.catalog_workspace_content.put_declarative_analytics_model(identifier, analytics_model_e)
        analytics_model_o = sdk.catalog_workspace_content.get_declarative_analytics_model(identifier)
        assert analytics_model_e == analytics_model_o
        assert analytics_model_e.to_api().to_dict() == analytics_model_o.to_api().to_dict()
    finally:
        sdk.catalog_workspace.delete_workspace(identifier)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_put_declarative_ldm.json"))
def test_put_declarative_ldm(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    identifier = test_put_declarative_ldm.__name__
    workspace = CatalogWorkspace(workspace_id=identifier, name=identifier)
    sdk.catalog_workspace.create_or_update(workspace)

    ldm_e = sdk.catalog_workspace_content.get_declarative_ldm(test_config["workspace"])
    try:
        sdk.catalog_workspace_content.put_declarative_ldm(identifier, ldm_e)
        ldm_o = sdk.catalog_workspace_content.get_declarative_ldm(identifier)
        assert ldm_e == ldm_o
        assert ldm_e.to_api().to_dict() == ldm_o.to_api().to_dict()
    finally:
        sdk.catalog_workspace.delete_workspace(identifier)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_get_declarative_analytics_model.json"))
def test_get_declarative_analytics_model(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "expected" / "declarative_analytics_model.json"
    analytics_model_o = sdk.catalog_workspace_content.get_declarative_analytics_model(test_config["workspace"])

    with open(path) as f:
        data = json.load(f)

    expected_o = CatalogDeclarativeAnalytics.from_dict(data)

    assert analytics_model_o == expected_o
    assert analytics_model_o.to_api().to_dict(camel_case=True) == data


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_get_declarative_ldm.json"))
def test_get_declarative_ldm(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "expected" / "declarative_ldm.json"
    ldm_o = sdk.catalog_workspace_content.get_declarative_ldm(test_config["workspace"])

    with open(path) as f:
        data = json.load(f)

    expected_o = CatalogDeclarativeModel.from_dict(data)

    assert ldm_o == expected_o
    assert ldm_o.to_api().to_dict(camel_case=True) == data


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_catalog.json"))
def test_catalog_load(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    catalog = sdk.catalog_workspace_content.get_full_catalog(test_config["workspace"])

    # rough initial smoke-test; just do a quick 'rub'
    assert len(catalog.metrics) == 24
    assert len(catalog.datasets) == 6

    assert catalog.get_metric("order_amount") is not None
    assert catalog.get_metric("revenue") is not None
    assert catalog.get_dataset("customers") is not None
    assert catalog.get_dataset("order_lines") is not None
    assert catalog.get_dataset("products") is not None


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_catalog_availability.json"))
def test_catalog_availability(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    catalog = sdk.catalog_workspace_content.get_full_catalog(test_config["workspace"])
    claim_count = catalog.get_metric("campaign_spend")

    filtered_catalog = catalog.catalog_with_valid_objects(claim_count)

    # rough initial smoke-test; just do a quick 'rub' that filtered catalog has less entries than full catalog
    assert len(filtered_catalog.metrics) == 24
    assert len(filtered_catalog.datasets) == 3

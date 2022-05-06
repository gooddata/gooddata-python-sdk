# (C) 2021 GoodData Corporation
from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional
from unittest import mock
from unittest.mock import MagicMock

import pytest
import vcr

import gooddata_metadata_client.apis as metadata_apis
from gooddata_sdk import (
    BigQueryAttributes,
    CatalogDataSource,
    CatalogDataSourceBigQuery,
    CatalogDataSourcePostgres,
    CatalogDataSourceRedshift,
    CatalogDataSourceSnowflake,
    CatalogDataSourceVertica,
    CatalogGenerateLdmRequest,
    CatalogScanModelRequest,
    ExecutionDefinition,
    GoodDataApiClient,
    GoodDataSdk,
    PostgresAttributes,
    RedshiftAttributes,
    SnowflakeAttributes,
    VerticaAttributes,
)
from gooddata_sdk.catalog.data_source.declarative_model.data_source import CatalogDeclarativeDataSources
from gooddata_sdk.catalog.entity import BasicCredentials, TokenCredentialsFromFile
from tests import VCR_MATCH_ON

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures" / "data_sources"

gd_vcr = vcr.VCR(filter_headers=["authorization", "user-agent"], serializer="json", match_on=VCR_MATCH_ON)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_register_upload_notification.json"))
def test_register_upload_notification(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    metrics = sdk.catalog_workspace_content.get_metrics_catalog(test_config["workspace"])

    exec_definition = ExecutionDefinition(
        attributes=None, filters=None, metrics=[metrics[0].as_computable()], dimensions=[["measureGroup"]]
    )
    exec_response_1 = sdk.compute.for_exec_def(test_config["workspace"], exec_definition)
    sdk.catalog_data_source.register_upload_notification(test_config["data_source"])
    exec_response_2 = sdk.compute.for_exec_def(test_config["workspace"], exec_definition)
    assert exec_response_1.result_id != exec_response_2.result_id


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_generate_logical_model.json"))
def test_generate_logical_model(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    declarative_model = sdk.catalog_workspace_content.get_declarative_ldm(test_config["workspace"])
    ldm_request = CatalogGenerateLdmRequest(
        separator="__", generate_long_ids=True, date_granularities="basic", wdf_prefix="wdf"
    )
    generated_declarative_model = sdk.catalog_data_source.generate_logical_model(
        test_config["data_source"], ldm_request
    )
    """
    There is a bug in generate_logical_model. It returns in granularities sorted alphabetically,
    so it can not be compared  declarative_model == generated_declarative_model, because granularities are not the same.
    """
    assert declarative_model.ldm.datasets == generated_declarative_model.ldm.datasets
    assert len(declarative_model.ldm.date_instances) == len(generated_declarative_model.ldm.date_instances)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_data_sources_list.json"))
def test_catalog_list_data_sources(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    data_sources = sdk.catalog_data_source.list_data_sources()

    assert len(data_sources) == 1
    assert data_sources[0].id == test_config["data_source"]


def _create_default_data_source(sdk):
    sdk.catalog_data_source.create_or_update_data_source(
        CatalogDataSourcePostgres(
            id="test",
            name="Test",
            db_specific_attributes=PostgresAttributes(host="localhost", db_name="demo"),
            schema="demo",
            credentials=BasicCredentials(
                username="demouser",
                password="demopass",
            ),
            enable_caching=True,
            cache_path=["cache_schema"],
            url_params=[("param", "value")],
        )
    )


def _get_data_source(data_sources: List[CatalogDataSource], data_source_id: str) -> Optional[CatalogDataSource]:
    for data_source in data_sources:
        if data_source.id == data_source_id:
            return data_source
    return None


@gd_vcr.use_cassette(str(_fixtures_dir / "test_create_update.json"))
def test_catalog_create_update_list_data_source(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    try:
        data_sources = sdk.catalog_data_source.list_data_sources()
        assert len(data_sources) == 1
        assert data_sources[0].id == test_config["data_source"]

        _create_default_data_source(sdk)

        # Update of previously created DS (same ID!)
        sdk.catalog_data_source.create_or_update_data_source(
            CatalogDataSourcePostgres(
                id="test",
                name="Test2",
                db_specific_attributes=PostgresAttributes(host="localhost", db_name="demo"),
                schema="demo",
                credentials=BasicCredentials(
                    username="demouser",
                    password="demopass",
                ),
                enable_caching=False,
                url_params=[("param", "value")],
            )
        )

        data_sources = sdk.catalog_data_source.list_data_sources()
        assert len(data_sources) == 2
        demo_ds = _get_data_source(data_sources, test_config["data_source"])
        assert demo_ds
        assert demo_ds.id == test_config["data_source"]
        test_ds = _get_data_source(data_sources, "test")
        assert test_ds
        assert test_ds.id == "test"
        assert test_ds.name == "Test2"
        assert not test_ds.enable_caching
        assert test_ds.cache_path is None
    finally:
        # Cleanup every time
        sdk.catalog_data_source.delete_data_source("test")
        data_sources = sdk.catalog_data_source.list_data_sources()
        assert len(data_sources) == 1


def _create_delete_ds(sdk, data_source: CatalogDataSource):
    try:
        sdk.catalog_data_source.create_or_update_data_source(data_source)
    finally:
        sdk.catalog_data_source.delete_data_source(data_source.id)


@gd_vcr.use_cassette(str(_fixtures_dir / "redshift.json"))
def test_catalog_create_data_source_redshift_spec(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    _create_delete_ds(
        sdk=sdk,
        data_source=CatalogDataSourceRedshift(
            id="test",
            name="Test2",
            db_specific_attributes=RedshiftAttributes(host="aws.endpoint", db_name="demo"),
            schema="demo",
            credentials=BasicCredentials(
                username="demouser",
                password="demopass",
            ),
            enable_caching=False,
            url_params=[("param", "value")],
        ),
    )


@gd_vcr.use_cassette(str(_fixtures_dir / "vertica.json"))
def test_catalog_create_data_source_vertica_spec(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    _create_delete_ds(
        sdk=sdk,
        data_source=CatalogDataSourceVertica(
            id="test",
            name="Test2",
            db_specific_attributes=VerticaAttributes(host="localhost", db_name="demo"),
            schema="demo",
            credentials=BasicCredentials(
                username="demouser",
                password="demopass",
            ),
            enable_caching=False,
            url_params=[("param", "value")],
        ),
    )


@gd_vcr.use_cassette(str(_fixtures_dir / "snowflake.json"))
def test_catalog_create_data_source_snowflake_spec(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    _create_delete_ds(
        sdk=sdk,
        data_source=CatalogDataSourceSnowflake(
            id="test",
            name="Test",
            db_specific_attributes=SnowflakeAttributes(account="gooddata", warehouse="TIGER", db_name="TIGER"),
            schema="demo",
            credentials=BasicCredentials(
                username="demouser",
                password="demopass",
            ),
            enable_caching=True,
            cache_path=["cache_schema"],
            url_params=[("param", "value")],
        ),
    )


@gd_vcr.use_cassette(str(_fixtures_dir / "bigquery.json"))
def test_catalog_create_data_source_bigquery_spec(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    with mock.patch("builtins.open", mock.mock_open(read_data=b"bigquery_service_account_json")):
        _create_delete_ds(
            sdk=sdk,
            data_source=CatalogDataSourceBigQuery(
                id="test",
                name="Test",
                db_specific_attributes=BigQueryAttributes(project_id="gdc-us-dev"),
                schema="demo",
                credentials=TokenCredentialsFromFile(file_path=Path("credentials") / "bigquery_service_account.json"),
                enable_caching=True,
                cache_path=["cache_schema"],
                url_params=[("param", "value")],
            ),
        )


#
#  Here we test default interface without DB specific custom attributes (plain url, data_source_type specified
#
@gd_vcr.use_cassette(str(_fixtures_dir / "dremio.json"))
def test_catalog_create_data_source_dremio_spec(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    _create_delete_ds(
        sdk=sdk,
        data_source=CatalogDataSource(
            id="dremio",
            name="Dremio",
            data_source_type="DREMIO",
            url="jdbc:dremio:direct=dremio:31010",
            credentials=BasicCredentials(
                username="demouser",
                password="demopass",
            ),
            schema="",
            enable_caching=True,
            cache_path=["$scratch"],
        ),
    )


@gd_vcr.use_cassette(str(_fixtures_dir / "patch.json"))
def test_catalog_patch_data_source(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    try:
        data_sources = sdk.catalog_data_source.list_data_sources()
        assert len(data_sources) == 1
        assert data_sources[0].id == test_config["data_source"]

        _create_default_data_source(sdk)

        data_source = sdk.catalog_data_source.get_data_source("test")
        assert data_source.name == "Test"

        sdk.catalog_data_source.patch_data_source_attributes(data_source_id="test", attributes={"name": "Test2"})
        patched_data_source = sdk.catalog_data_source.get_data_source("test")
        assert patched_data_source.name == "Test2"
    finally:
        sdk.catalog_data_source.delete_data_source("test")


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_data_source_tables.json"))
def test_catalog_data_source_table(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    data_source_tables = sdk.catalog_data_source.list_data_source_tables(test_config["data_source"])

    assert len(data_source_tables) == 5
    order_lines = next(filter(lambda x: x.id == "order_lines", data_source_tables))
    assert len(order_lines.columns) == 11


@gd_vcr.use_cassette(str(_fixtures_dir / "declarative_data_sources.json"))
def test_catalog_declarative_data_sources(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    client = GoodDataApiClient(host=test_config["host"], token=test_config["token"])
    layout_api = metadata_apis.LayoutApi(client.metadata_client)

    data_sources_o = sdk.catalog_data_source.get_declarative_data_sources()
    data_sources = data_sources_o.data_sources

    assert len(data_sources) == 1
    assert data_sources[0].id == test_config["data_source"]
    assert len(data_sources[0].pdm.tables) == 5
    assert data_sources_o.to_api().to_dict() == layout_api.get_data_sources_layout().to_dict()


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_delete_declarative_data_sources.json"))
def test_delete_declarative_data_sources(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    credentials_path = _current_dir / "load" / "data_source_credentials" / "data_sources_credentials.yaml"
    expected_json_path = _current_dir / "expected" / "declarative_data_sources.json"

    try:
        sdk.catalog_data_source.put_declarative_data_sources(CatalogDeclarativeDataSources(data_sources=[]))
        data_sources_o = sdk.catalog_data_source.get_declarative_data_sources()
        assert len(data_sources_o.data_sources) == 0
    finally:
        with open(expected_json_path) as f:
            data = json.load(f)
        data_sources_o = CatalogDeclarativeDataSources.from_dict(data)
        sdk.catalog_data_source.put_declarative_data_sources(data_sources_o, credentials_path)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_store_declarative_data_sources.json"))
def test_store_declarative_data_sources(test_config):
    store_folder = _current_dir / "store"
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    data_sources_e = sdk.catalog_data_source.get_declarative_data_sources()
    sdk.catalog_data_source.store_declarative_data_sources(store_folder)
    data_sources_o = sdk.catalog_data_source.load_declarative_data_sources(store_folder)

    assert data_sources_e.to_api().to_dict() == data_sources_o.to_api().to_dict()
    assert data_sources_e == data_sources_o


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_load_and_put_declarative_data_sources.json"))
def test_load_and_put_declarative_data_sources(test_config):
    load_folder = _current_dir / "load"
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    credentials_path = _current_dir / "load" / "data_source_credentials" / "data_sources_credentials.yaml"
    expected_json_path = _current_dir / "expected" / "declarative_data_sources.json"
    try:
        sdk.catalog_data_source.put_declarative_data_sources(CatalogDeclarativeDataSources(data_sources=[]))
        TokenCredentialsFromFile.token_from_file = MagicMock(return_value="c2VjcmV0X3Rva2Vu")
        sdk.catalog_data_source.load_and_put_declarative_data_sources(load_folder, credentials_path)
        data_sources_o = sdk.catalog_data_source.get_declarative_data_sources()
        assert len(data_sources_o.data_sources) == 3
        assert [data_source.id for data_source in data_sources_o.data_sources] == [
            "demo-bigquery-ds",
            "demo-test-ds",
            "demo-vertica-ds",
        ]
        assert [data_source.type for data_source in data_sources_o.data_sources] == [
            "BIGQUERY",
            "POSTGRESQL",
            "VERTICA",
        ]
        assert [len(data_source.pdm.tables) for data_source in data_sources_o.data_sources] == [
            0,
            5,
            5,
        ]
    finally:
        with open(expected_json_path) as f:
            data = json.load(f)
        data_sources_o = CatalogDeclarativeDataSources.from_dict(data)
        sdk2 = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
        sdk2.catalog_data_source.put_declarative_data_sources(data_sources_o, credentials_path)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_put_declarative_data_sources_connection.json"))
def test_put_declarative_data_sources_connection(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "expected" / "declarative_data_sources.json"
    credentials_path = _current_dir / "load" / "data_source_credentials" / "data_sources_credentials.yaml"
    data_sources_e = sdk.catalog_data_source.get_declarative_data_sources()

    try:
        sdk.catalog_data_source.put_declarative_data_sources(data_sources_e, credentials_path, test_data_sources=True)
        data_sources_o = sdk.catalog_data_source.get_declarative_data_sources()
        assert data_sources_e == data_sources_o
        assert data_sources_e.to_api().to_dict() == data_sources_o.to_api().to_dict()
    finally:
        with open(path) as f:
            data = json.load(f)
        data_sources_o = CatalogDeclarativeDataSources.from_dict(data)
        sdk.catalog_data_source.put_declarative_data_sources(data_sources_o, credentials_path)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_put_declarative_data_sources.json"))
def test_put_declarative_data_sources(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "expected" / "declarative_data_sources.json"
    credentials_path = _current_dir / "load" / "data_source_credentials" / "data_sources_credentials.yaml"
    data_sources_e = sdk.catalog_data_source.get_declarative_data_sources()

    try:
        sdk.catalog_data_source.put_declarative_data_sources(data_sources_e, credentials_path)
        data_sources_o = sdk.catalog_data_source.get_declarative_data_sources()
        assert data_sources_e == data_sources_o
        assert data_sources_e.to_api().to_dict() == data_sources_o.to_api().to_dict()
    finally:
        with open(path) as f:
            data = json.load(f)
        data_sources_o = CatalogDeclarativeDataSources.from_dict(data)
        sdk.catalog_data_source.put_declarative_data_sources(data_sources_o, credentials_path)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_test_declarative_data_sources.json"))
def test_declarative_data_sources(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    credentials_path = _current_dir / "load" / "data_source_credentials" / "data_sources_credentials.yaml"
    data_sources_e = sdk.catalog_data_source.get_declarative_data_sources()

    try:
        sdk.catalog_data_source.test_data_sources_connection(data_sources_e)
        assert False
    except ValueError:
        sdk.catalog_data_source.test_data_sources_connection(data_sources_e, credentials_path)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_test_get_declarative_pdm.json"))
def test_get_declarative_pdm(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    pdm = sdk.catalog_data_source.get_declarative_pdm(test_config["data_source"])
    assert len(pdm.tables) == 5


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_test_put_declarative_pdm.json"))
def test_put_declarative_pdm(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    data_source_id = test_config["data_source"]
    pdm = sdk.catalog_data_source.get_declarative_pdm(data_source_id)
    pdm_deleted_table = [table for table in pdm.tables if table.id == "order_lines"]

    try:
        pdm.tables = [table for table in pdm.tables if table.id != "order_lines"]
        sdk.catalog_data_source.put_declarative_pdm(data_source_id, pdm)
        assert len(pdm.tables) == 4
    finally:
        pdm.tables = pdm.tables + pdm_deleted_table
        sdk.catalog_data_source.put_declarative_pdm(data_source_id, pdm)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_test_scan_model.json"))
def test_scan_model(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    data_source_id = test_config["data_source"]

    scan_result = sdk.catalog_data_source.scan_data_source(data_source_id)
    assert len(scan_result.pdm.tables) == 5

    scan_request = CatalogScanModelRequest(scan_tables=False, scan_views=True)
    scan_result = sdk.catalog_data_source.scan_data_source(data_source_id, scan_request)
    assert len(scan_result.pdm.tables) == 0

    with pytest.raises(ValueError):
        CatalogScanModelRequest(scan_tables=False, scan_views=False)
        CatalogScanModelRequest(scan_tables=False, scan_views=False)

    # TODO - how to simulate warnings in AIO?
    assert len(scan_result.warnings) == 0


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_test_scan_and_put_declarative_pdm.json"))
def test_scan_and_put_declarative_pdm(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    data_source_id = test_config["data_source"]

    pdm = sdk.catalog_data_source.get_declarative_pdm(data_source_id)
    assert len(pdm.tables) == 5

    try:
        scan_request = CatalogScanModelRequest(scan_tables=False, scan_views=True)
        sdk.catalog_data_source.scan_and_put_pdm(data_source_id, scan_request)
        pdm = sdk.catalog_data_source.get_declarative_pdm(data_source_id)
        assert len(pdm.tables) == 0
    finally:
        sdk.catalog_data_source.scan_and_put_pdm(data_source_id)
        pdm = sdk.catalog_data_source.get_declarative_pdm(data_source_id)
        assert len(pdm.tables) == 5


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_store_and_load_and_put_declarative_pdm.json"))
def test_store_and_load_and_put_declarative_pdm(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    data_source_id = test_config["data_source"]
    store_folder = _current_dir / "store"
    load_folder = _current_dir / "load"

    pdm = sdk.catalog_data_source.get_declarative_pdm(data_source_id)
    sdk.catalog_data_source.store_declarative_pdm(data_source_id, store_folder)
    pdm_loaded = sdk.catalog_data_source.load_declarative_pdm(data_source_id, load_folder)
    assert pdm == pdm_loaded
    assert pdm.to_api().to_dict() == pdm_loaded.to_api().to_dict()

    sdk.catalog_data_source.load_and_put_declarative_pdm(data_source_id, load_folder)
    pdm_loaded = sdk.catalog_data_source.load_declarative_pdm(data_source_id, load_folder)
    assert pdm == pdm_loaded
    assert pdm.to_api().to_dict() == pdm_loaded.to_api().to_dict()


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_scan_schemata.json"))
def test_scan_schemata(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    data_source_id = test_config["data_source"]

    schemata = sdk.catalog_data_source.scan_schemata(data_source_id)
    assert len(schemata) == 1
    assert "demo" in schemata

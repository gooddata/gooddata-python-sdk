# (C) 2021 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from typing import List, Optional
from unittest import mock

import vcr

from gooddata_sdk import (
    BigQueryAttributes,
    CatalogDataSource,
    CatalogDataSourceBigQuery,
    CatalogDataSourcePostgres,
    CatalogDataSourceRedshift,
    CatalogDataSourceSnowflake,
    CatalogDataSourceVertica,
    CatalogGenerateLdmRequest,
    ExecutionDefinition,
    GoodDataSdk,
    PostgresAttributes,
    SnowflakeAttributes,
)
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
            db_specific_attributes=PostgresAttributes(host="aws.endpoint", db_name="demo"),
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
            db_specific_attributes=PostgresAttributes(host="localhost", db_name="demo"),
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
    data_sources = sdk.catalog_data_source.get_declarative_data_sources().data_sources

    assert len(data_sources) == 1
    assert data_sources[0].id == test_config["data_source"]
    assert len(data_sources[0].pdm.tables) == 5

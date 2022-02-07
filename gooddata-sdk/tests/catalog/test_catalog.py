# (C) 2021 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from unittest import mock

import vcr

from gooddata_sdk import CatalogDataSource, CatalogDataSourceToken, CatalogDataSourceUserPwd, GoodDataSdk
from tests import VCR_MATCH_ON

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"

gd_vcr = vcr.VCR(filter_headers=["authorization", "user-agent"], serializer="json", match_on=VCR_MATCH_ON)


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


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_data_sources_list.json"))
def test_catalog_list_data_sources(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    data_sources = sdk.catalog_data_source.list_data_sources()

    assert len(data_sources) == 1
    assert data_sources[0].id == "demo-test-ds"


@gd_vcr.use_cassette(str(_fixtures_dir / "data_sources/test_create_update.json"))
def test_catalog_create_update_list_data_source(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    try:
        data_sources = sdk.catalog_data_source.list_data_sources()
        assert len(data_sources) == 1
        assert data_sources[0].id == "demo-test-ds"

        sdk.catalog_data_source.create_or_update_data_source(
            CatalogDataSource(
                id="test",
                name="Test",
                data_source_type="POSTGRESQL",
                url="jdbc:postgresql://localhost:5432/demo",
                schema="demo",
                username="demouser",
                password="demopass",
            )
        )
        # Update of previously created DS (same ID!)
        sdk.catalog_data_source.create_or_update_data_source(
            CatalogDataSource(
                id="test",
                name="Test2",
                data_source_type="POSTGRESQL",
                url="jdbc:postgresql://localhost:5432/demo",
                schema="demo",
                username="demouser",
                password="demopass",
            )
        )

        data_sources = sdk.catalog_data_source.list_data_sources()
        assert len(data_sources) == 2
        assert data_sources[0].id == "demo-test-ds"
        assert data_sources[1].id == "test"
        assert data_sources[1].name == "Test2"
    finally:
        # Cleanup every time
        sdk.catalog_data_source.delete_data_source("test")
        data_sources = sdk.catalog_data_source.list_data_sources()
        assert len(data_sources) == 1


def _create_delete_ds(sdk, create_func, ds_id, params):
    try:
        create_func(**params)
    finally:
        sdk.catalog_data_source.delete_data_source(ds_id)


@gd_vcr.use_cassette(str(_fixtures_dir / "data_sources/postgres_custom.json"))
def test_catalog_create_data_source_postgres_custom(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    _create_delete_ds(
        sdk=sdk,
        create_func=sdk.catalog_data_source.create_or_update_standard_data_source,
        ds_id="postgresql",
        params=dict(
            data_source_base=CatalogDataSourceUserPwd(
                id="postgresql", name="PostgreSQL", schema="demo", username="demouser", password="demopass"
            ),
            data_source_type="POSTGRESQL",
            db_engine="postgresql",
            db_name="tiger",
            host="localhost",
            port=5432,
        ),
    )


@gd_vcr.use_cassette(str(_fixtures_dir / "data_sources/postgres_spec.json"))
def test_catalog_create_data_source_postgres_spec(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    _create_delete_ds(
        sdk=sdk,
        create_func=sdk.catalog_data_source.create_or_update_postgres_data_source,
        ds_id="postgresql",
        params=dict(
            data_source_base=CatalogDataSourceUserPwd(
                id="postgresql", name="PostgreSQL 2", schema="demo", username="demouser", password="demopass"
            ),
            db_name="tiger",
            host="localhost",
            port=5432,
        ),
    )


@gd_vcr.use_cassette(str(_fixtures_dir / "data_sources/snowflake_spec.json"))
def test_catalog_create_data_source_snowflake_spec(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    _create_delete_ds(
        sdk=sdk,
        create_func=sdk.catalog_data_source.create_or_update_snowflake_data_source,
        ds_id="snowflake",
        params=dict(
            data_source_base=CatalogDataSourceUserPwd(
                id="snowflake",
                name="Snowflake",
                username="tiger",
                password="xxxxx",
                schema="demo",
            ),
            account="gooddata",
            warehouse="TIGER",
            db_name="TIGER",
        ),
    )


@gd_vcr.use_cassette(str(_fixtures_dir / "data_sources/bigquery_spec.json"))
def test_catalog_create_data_source_bigquery_spec(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    with mock.patch("builtins.open", mock.mock_open(read_data=b"bigquery_service_account_json")):
        _create_delete_ds(
            sdk=sdk,
            create_func=sdk.catalog_data_source.create_or_update_bigquery_data_source,
            ds_id="bigquery",
            params=dict(
                data_source_base=CatalogDataSourceToken(
                    id="bigquery",
                    name="BigQuery",
                    token_path="credentials/gdc-dev-us.json",
                    schema="tiger_demo",
                ),
                project_id="gdc-us-dev",
            ),
        )


@gd_vcr.use_cassette(str(_fixtures_dir / "data_sources/dremio_spec.json"))
def test_catalog_create_data_source_dremio_spec(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    _create_delete_ds(
        sdk=sdk,
        create_func=sdk.catalog_data_source.create_or_update_data_source,
        ds_id="dremio",
        params=dict(
            data_source=CatalogDataSource(
                id="dremio",
                name="Dremio",
                data_source_type="DREMIO",
                url="jdbc:dremio:direct=dremio:31010",
                username="tiger",
                password="xxxxx",
                schema="",
            )
        ),
    )


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_data_source_tables.json"))
def test_catalog_data_source_table(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    data_source_tables = sdk.catalog_data_source.list_data_source_tables("demo-test-ds")

    assert len(data_source_tables) == 5
    order_lines = next(filter(lambda x: x.id == "order_lines", data_source_tables))
    assert len(order_lines.columns) == 11

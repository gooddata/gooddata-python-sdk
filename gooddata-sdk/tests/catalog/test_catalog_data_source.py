# (C) 2021 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from typing import List, Optional
from unittest import mock
from unittest.mock import MagicMock

import pytest
from gooddata_api_client.model.json_api_data_source_in_attributes import JsonApiDataSourceInAttributes
from gooddata_sdk import (
    BasicCredentials,
    CatalogDataSource,
    CatalogDataSourceBigQuery,
    CatalogDataSourceDatabricks,
    CatalogDataSourceMariaDb,
    CatalogDataSourceMsSql,
    CatalogDataSourceMySql,
    CatalogDataSourcePostgres,
    CatalogDataSourceRedshift,
    CatalogDataSourceSnowflake,
    CatalogDataSourceVertica,
    CatalogDeclarativeDataSources,
    CatalogDeclarativeModel,
    CatalogGenerateLdmRequest,
    CatalogPdmLdmRequest,
    CatalogPdmSql,
    CatalogScanModelRequest,
    DatabricksAttributes,
    ExecutionDefinition,
    GoodDataSdk,
    MariaDbAttributes,
    MsSqlAttributes,
    MySqlAttributes,
    PostgresAttributes,
    RedshiftAttributes,
    ScanSqlRequest,
    SnowflakeAttributes,
    SqlColumn,
    TableDimension,
    TokenCredentialsFromFile,
    VerticaAttributes,
)
from tests_support.file_utils import load_json
from tests_support.vcrpy_utils import get_vcr

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures" / "data_sources"


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_register_upload_notification.yaml"))
def test_register_upload_notification(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    metrics = sdk.catalog_workspace_content.get_metrics_catalog(test_config["workspace"])

    exec_definition = ExecutionDefinition(
        attributes=None,
        filters=None,
        metrics=[metrics[0].as_computable()],
        dimensions=[TableDimension(item_ids=["measureGroup"])],
    )
    exec_response_1 = sdk.compute.for_exec_def(test_config["workspace"], exec_definition)
    sdk.catalog_data_source.register_upload_notification(test_config["data_source"])
    exec_response_2 = sdk.compute.for_exec_def(test_config["workspace"], exec_definition)
    assert exec_response_1.result_id != exec_response_2.result_id


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_generate_logical_model.yaml"))
def test_generate_logical_model(test_config: dict):
    pdm_json_path = _current_dir / "expected" / "declarative_pdm_ldm_request.json"

    pdm_ldm_request = CatalogPdmLdmRequest.from_dict(load_json(pdm_json_path))
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    declarative_model = sdk.catalog_workspace_content.get_declarative_ldm(test_config["workspace"])
    generate_ldm_request = CatalogGenerateLdmRequest(
        separator="__", wdf_prefix="wdf", workspace_id=test_config["workspace"], pdm=pdm_ldm_request
    )
    generated_declarative_model = sdk.catalog_data_source.generate_logical_model(
        test_config["data_source"], generate_ldm_request
    )

    """
    There is a bug in generate_logical_model. It returns in granularities sorted alphabetically,
    so it can not be compared  declarative_model == generated_declarative_model, because granularities are not the same.
    """
    assert declarative_model.ldm.datasets == generated_declarative_model.ldm.datasets
    assert len(declarative_model.ldm.date_instances) == len(generated_declarative_model.ldm.date_instances)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_scan_pdm_and_generate_logical_model.yaml"))
def test_scan_pdm_and_generate_logical_model(test_config: dict):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    declarative_model = sdk.catalog_workspace_content.get_declarative_ldm(test_config["workspace"])
    generate_ldm_request = CatalogGenerateLdmRequest(
        separator="__", wdf_prefix="wdf", workspace_id=test_config["workspace"]
    )
    generated_declarative_model, _ = sdk.catalog_data_source.scan_pdm_and_generate_logical_model(
        test_config["data_source"], generate_ldm_request
    )

    """
    There is a bug in generate_logical_model. It returns in granularities sorted alphabetically,
    so it can not be compared  declarative_model == generated_declarative_model, because granularities are not the same.
    """
    assert declarative_model.ldm.datasets == generated_declarative_model.ldm.datasets
    assert len(declarative_model.ldm.date_instances) == len(generated_declarative_model.ldm.date_instances)


def build_pdm_sql_datasets() -> List[CatalogPdmSql]:
    return [
        # Test sql-dataset specific attributes, facts, references
        CatalogPdmSql(
            statement="SELECT * FROM order_lines",
            title="Order lines duplicate sql dataset",
            columns=[
                SqlColumn(name="order_line_id", data_type="STRING"),
                SqlColumn(name="order_id", data_type="STRING"),
                SqlColumn(name="order_status", data_type="STRING"),
                SqlColumn(name="date", data_type="DATE"),
                SqlColumn(name="campaign_id", data_type="INT"),
                SqlColumn(name="customer_id", data_type="INT"),
                SqlColumn(name="product_id", data_type="INT"),
                SqlColumn(name="price", data_type="NUMERIC"),
                SqlColumn(name="quantity", data_type="NUMERIC"),
            ],
        ),
        # Test sql-dataset attribute WDFs
        CatalogPdmSql(
            statement="SELECT * FROM v_wdf_customers",
            title="Customers sql dataset with WDF",
            columns=[
                SqlColumn(name="customer_id", data_type="INT"),
                SqlColumn(name="customer_name", data_type="STRING"),
                SqlColumn(name="state", data_type="STRING"),
                SqlColumn(name="region", data_type="STRING"),
                SqlColumn(name="wdf__region", data_type="STRING"),
            ],
        ),
    ]


#    path = _current_dir / "expected" / "scan_result_pdm.json"


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_generate_logical_model_sql_datasets.yaml"))
def test_generate_logical_model_with_sql_datasets(test_config: dict):
    expected_json_path = _current_dir / "expected" / "declarative_ldm_with_sql_dataset.json"
    pdm_json_path = _current_dir / "expected" / "declarative_pdm_ldm_request.json"

    pdm_ldm_request = CatalogPdmLdmRequest.from_dict(load_json(pdm_json_path))
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    ldm_request = CatalogGenerateLdmRequest(
        separator="__",
        wdf_prefix="wdf",
        pdm=CatalogPdmLdmRequest(
            tables=pdm_ldm_request.tables,
            sqls=build_pdm_sql_datasets(),
        ),
    )
    generated_declarative_model = sdk.catalog_data_source.generate_logical_model(
        test_config["data_source"], ldm_request
    )

    expected_ldm = CatalogDeclarativeModel.from_dict(load_json(expected_json_path))

    # TODO: generateLDM does not sort datasets by id - update fixture to be sorted lexicographically
    #  and remove sort once fixed
    generated_declarative_model.ldm.datasets.sort(key=lambda dataset: dataset.id)
    expected_ldm.ldm.datasets.sort(key=lambda dataset: dataset.id)
    assert expected_ldm.ldm.datasets == generated_declarative_model.ldm.datasets
    assert len(expected_ldm.ldm.date_instances) == len(generated_declarative_model.ldm.date_instances)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_scan_pdm_and_generate_logical_model_sql_datasets.yaml"))
def test_scan_pdm_and_generate_logical_model_with_sql_datasets(test_config: dict):
    expected_json_path = _current_dir / "expected" / "declarative_ldm_with_sql_dataset.json"

    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    ldm_request = CatalogGenerateLdmRequest(
        separator="__",
        wdf_prefix="wdf",
        pdm=CatalogPdmLdmRequest(
            sqls=build_pdm_sql_datasets(),
        ),
    )
    generated_declarative_model, scan_result = sdk.catalog_data_source.scan_pdm_and_generate_logical_model(
        test_config["data_source"], ldm_request
    )

    expected_ldm = CatalogDeclarativeModel.from_dict(load_json(expected_json_path))

    # TODO: generateLDM does not sort datasets by id - update fixture to be sorted lexicographically
    #  and remove sort once fixed
    generated_declarative_model.ldm.datasets.sort(key=lambda dataset: dataset.id)
    expected_ldm.ldm.datasets.sort(key=lambda dataset: dataset.id)
    assert expected_ldm.ldm.datasets == generated_declarative_model.ldm.datasets
    assert len(expected_ldm.ldm.date_instances) == len(generated_declarative_model.ldm.date_instances)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_data_sources_list.yaml"))
def test_catalog_list_data_sources(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    data_sources = sdk.catalog_data_source.list_data_sources()

    assert len(data_sources) == 1
    assert data_sources[0].id == test_config["data_source"]


def _create_default_data_source(sdk: GoodDataSdk, data_source_id: str = "test"):
    expected_data_source = CatalogDataSourcePostgres(
        id=data_source_id,
        name="Test",
        db_specific_attributes=PostgresAttributes(host="localhost", db_name="demo"),
        schema="demo",
        credentials=BasicCredentials(
            username="demouser",
            password="demopass",
        ),
        enable_caching=True,
        cache_path=["cache_schema"],
        url_params=[("autosave", "true")],
    )
    sdk.catalog_data_source.create_or_update_data_source(data_source=expected_data_source)
    data_source = sdk.catalog_data_source.get_data_source(data_source_id)
    assert expected_data_source == data_source


def _get_data_source(data_sources: List[CatalogDataSource], data_source_id: str) -> Optional[CatalogDataSource]:
    for data_source in data_sources:
        if data_source.id == data_source_id:
            return data_source
    return None


@gd_vcr.use_cassette(str(_fixtures_dir / "test_create_update.yaml"))
def test_catalog_create_update_list_data_source(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    try:
        data_sources = sdk.catalog_data_source.list_data_sources()
        assert len(data_sources) == 1
        assert data_sources[0].id == test_config["data_source"]

        _create_default_data_source(sdk)

        # Update of previously created DS (same ID!)
        updated_data_source = CatalogDataSourcePostgres(
            id="test",
            name="Test2",
            db_specific_attributes=PostgresAttributes(host="localhost", db_name="demo"),
            schema="demo",
            credentials=BasicCredentials(
                username="demouser",
                password="demopass",
            ),
            enable_caching=False,
            url_params=[("autosave", "false")],
        )
        sdk.catalog_data_source.create_or_update_data_source(updated_data_source)

        data_sources = sdk.catalog_data_source.list_data_sources()
        assert len(data_sources) == 2
        demo_ds = _get_data_source(data_sources, test_config["data_source"])
        assert demo_ds
        assert demo_ds.id == test_config["data_source"]
        test_ds = _get_data_source(data_sources, "test")
        assert updated_data_source == test_ds
    finally:
        # Cleanup every time
        sdk.catalog_data_source.delete_data_source("test")
        data_sources = sdk.catalog_data_source.list_data_sources()
        assert len(data_sources) == 1


def _create_delete_ds(sdk, data_source: CatalogDataSource):
    try:
        sdk.catalog_data_source.create_or_update_data_source(data_source)
        created_ds = sdk.catalog_data_source.get_data_source(data_source.id)
        assert data_source == created_ds
    finally:
        sdk.catalog_data_source.delete_data_source(data_source.id)


@gd_vcr.use_cassette(str(_fixtures_dir / "redshift.yaml"))
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
            url_params=[("autosave", "true")],
        ),
    )


@gd_vcr.use_cassette(str(_fixtures_dir / "vertica.yaml"))
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
            url_params=[("TLSmode", "false")],
        ),
    )


@gd_vcr.use_cassette(str(_fixtures_dir / "snowflake.yaml"))
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
            url_params=[("useProxy", "true")],
        ),
    )


@gd_vcr.use_cassette(str(_fixtures_dir / "bigquery.yaml"))
def test_catalog_create_data_source_bigquery_spec(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    with mock.patch("builtins.open", mock.mock_open(read_data=test_config["bigquery_token_file"].encode("utf-8"))):
        _create_delete_ds(
            sdk=sdk,
            data_source=CatalogDataSourceBigQuery(
                id="test",
                name="Test",
                schema="demo",
                credentials=TokenCredentialsFromFile(file_path=Path("credentials") / "bigquery_service_account.json"),
                enable_caching=True,
                cache_path=["cache_schema"],
                parameters=[{"name": "projectId", "value": "abc"}],
            ),
        )


#
#  Here we test default interface without DB specific custom attributes (plain url, data_source_type specified
#
@gd_vcr.use_cassette(str(_fixtures_dir / "dremio.yaml"))
def test_catalog_create_data_source_dremio_spec(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    _create_delete_ds(
        sdk=sdk,
        data_source=CatalogDataSource(
            id="dremio",
            name="Dremio",
            type="DREMIO",
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


@gd_vcr.use_cassette(str(_fixtures_dir / "patch.yaml"))
def test_catalog_patch_data_source(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    try:
        data_sources = sdk.catalog_data_source.list_data_sources()
        assert len(data_sources) == 1
        assert data_sources[0].id == test_config["data_source"]

        _create_default_data_source(sdk)

        sdk.catalog_data_source.patch_data_source_attributes(data_source_id="test", attributes={"name": "Test2"})
        patched_data_source = sdk.catalog_data_source.get_data_source("test")
        assert patched_data_source.name == "Test2"
    finally:
        sdk.catalog_data_source.delete_data_source("test")


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_delete_declarative_data_sources.yaml"))
def test_delete_declarative_data_sources(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    credentials_path = _current_dir / "load" / "data_source_credentials" / "data_sources_credentials.yaml"
    expected_json_path = _current_dir / "expected" / "declarative_data_sources.json"

    try:
        sdk.catalog_data_source.put_declarative_data_sources(CatalogDeclarativeDataSources(data_sources=[]))
        data_sources_o = sdk.catalog_data_source.get_declarative_data_sources()
        assert len(data_sources_o.data_sources) == 0
    finally:
        data_sources_o = CatalogDeclarativeDataSources.from_dict(load_json(expected_json_path))
        sdk.catalog_data_source.put_declarative_data_sources(data_sources_o, credentials_path)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_store_declarative_data_sources.yaml"))
def test_store_declarative_data_sources(test_config):
    store_folder = _current_dir / "store"
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    data_sources_e = sdk.catalog_data_source.get_declarative_data_sources()
    sdk.catalog_data_source.store_declarative_data_sources(store_folder)
    data_sources_o = sdk.catalog_data_source.load_declarative_data_sources(store_folder)

    assert data_sources_e.to_dict(camel_case=True) == data_sources_o.to_dict(camel_case=True)
    assert data_sources_e == data_sources_o


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_load_and_put_declarative_data_sources.yaml"))
def test_load_and_put_declarative_data_sources(test_config):
    load_folder = _current_dir / "load"
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    credentials_path = _current_dir / "load" / "data_source_credentials" / "data_sources_credentials.yaml"
    expected_json_path = _current_dir / "expected" / "declarative_data_sources.json"
    try:
        sdk.catalog_data_source.put_declarative_data_sources(CatalogDeclarativeDataSources(data_sources=[]))
        TokenCredentialsFromFile.token_from_file = MagicMock(return_value=test_config["bigquery_token"])
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
        assert len(data_sources_o.data_sources[0].parameters) == 1
        assert len(data_sources_o.data_sources[0].decoded_parameters) == 3
    finally:
        data_sources_o = CatalogDeclarativeDataSources.from_dict(load_json(expected_json_path))
        sdk2 = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
        sdk2.catalog_data_source.put_declarative_data_sources(data_sources_o, credentials_path)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_put_declarative_data_sources_connection.yaml"))
def test_put_declarative_data_sources_connection(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "expected" / "declarative_data_sources.json"
    credentials_path = _current_dir / "load" / "data_source_credentials" / "data_sources_credentials.yaml"
    data_sources_e = sdk.catalog_data_source.get_declarative_data_sources()

    try:
        sdk.catalog_data_source.put_declarative_data_sources(data_sources_e, credentials_path, test_data_sources=True)
        data_sources_o = sdk.catalog_data_source.get_declarative_data_sources()
        assert data_sources_e == data_sources_o
        assert data_sources_e.to_dict(camel_case=True) == data_sources_o.to_dict(camel_case=True)
    finally:
        data_sources_o = CatalogDeclarativeDataSources.from_dict(load_json(path))
        sdk.catalog_data_source.put_declarative_data_sources(data_sources_o, credentials_path)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_put_declarative_data_sources.yaml"))
def test_put_declarative_data_sources(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "expected" / "declarative_data_sources.json"
    credentials_path = _current_dir / "load" / "data_source_credentials" / "data_sources_credentials.yaml"
    data_sources_e = sdk.catalog_data_source.get_declarative_data_sources()

    try:
        sdk.catalog_data_source.put_declarative_data_sources(data_sources_e, credentials_path)
        data_sources_o = sdk.catalog_data_source.get_declarative_data_sources()
        assert data_sources_e == data_sources_o
        assert data_sources_e.to_dict(camel_case=True) == data_sources_o.to_dict(camel_case=True)
    finally:
        data_sources_o = CatalogDeclarativeDataSources.from_dict(load_json(path))
        sdk.catalog_data_source.put_declarative_data_sources(data_sources_o, credentials_path)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_test_declarative_data_sources.yaml"))
def test_declarative_data_sources(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    credentials_path = _current_dir / "load" / "data_source_credentials" / "data_sources_credentials.yaml"
    data_sources_e = sdk.catalog_data_source.get_declarative_data_sources()

    try:
        sdk.catalog_data_source.test_data_sources_connection(data_sources_e)
        assert False
    except ValueError:
        sdk.catalog_data_source.test_data_sources_connection(data_sources_e, credentials_path)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_cache_strategy.yaml"))
def test_cache_strategy(test_config: dict):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    data_source_id = test_config["data_source"]

    original = sdk.catalog_data_source.get_data_source(data_source_id=data_source_id)

    try:
        sdk.catalog_data_source.patch_data_source_attributes(data_source_id, {"cache_strategy": "NEVER"})
        updated = sdk.catalog_data_source.get_data_source(data_source_id=data_source_id)
        assert updated.cache_strategy == "NEVER"
    finally:
        sdk.catalog_data_source.create_or_update_data_source(original)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_test_scan_model.yaml"))
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

    # TODO - how to simulate warnings in AIO?
    assert len(scan_result.warnings) == 0


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_test_scan_model_with_table_prefix.yaml"))
def test_scan_mode_with_table_prefix(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    data_source_id = test_config["data_source"]
    request = CatalogScanModelRequest(table_prefix="order", separator="_")

    scan_result = sdk.catalog_data_source.scan_data_source(data_source_id, request)
    assert len(scan_result.pdm.tables) == 1
    assert scan_result.pdm.tables[0].name_prefix == "order"


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_test_scan_model_with_schemata.yaml"))
def test_scan_mode_with_schemata(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    data_source_id = test_config["data_source"]
    request = CatalogScanModelRequest(schemata=["demo"])

    scan_result = sdk.catalog_data_source.scan_data_source(data_source_id, request)
    assert len(scan_result.pdm.tables) == 5


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_scan_schemata.yaml"))
def test_scan_schemata(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    data_source_id = test_config["data_source"]

    schemata = sdk.catalog_data_source.scan_schemata(data_source_id)
    assert len(schemata) == 1
    assert "demo" in schemata


@gd_vcr.use_cassette(str(_fixtures_dir / "scan_sql.yaml"))
def test_scan_sql(test_config: dict):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    data_source_id = test_config["data_source"]
    request = ScanSqlRequest(sql="SELECT * FROM products")

    response = sdk.catalog_data_source.scan_sql(data_source_id, request)
    response.columns.sort(key=lambda col: col.name)

    assert len(response.columns) == 3
    assert response.columns == [
        SqlColumn(name="category", data_type="STRING"),
        SqlColumn(name="product_id", data_type="INT"),
        SqlColumn(name="product_name", data_type="STRING"),
    ]
    assert len(response.data_preview) == 10


@gd_vcr.use_cassette(str(_fixtures_dir / "scan_sql_with_nulls_in_preview.yaml"))
def test_scan_sql_with_nulls_in_preview(test_config: dict):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    data_source_id = test_config["data_source"]
    request = ScanSqlRequest(sql="SELECT ol.campaign_id FROM order_lines ol ORDER BY campaign_id NULLS FIRST LIMIT 5")

    response = sdk.catalog_data_source.scan_sql(data_source_id, request)
    response.columns.sort(key=lambda col: col.name)

    assert len(response.columns) == 1
    assert response.columns == [
        SqlColumn(name="campaign_id", data_type="INT"),
    ]
    assert len(response.data_preview) == 5
    assert [None] in response.data_preview


@gd_vcr.use_cassette(str(_fixtures_dir / "scan_scan_sql_without_preview.yaml"))
def test_scan_sql_without_preview(test_config: dict):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    data_source_id = test_config["data_source"]
    request = ScanSqlRequest(sql="SELECT ol.campaign_id FROM order_lines ol LIMIT 0")

    response = sdk.catalog_data_source.scan_sql(data_source_id, request)
    response.columns.sort(key=lambda col: col.name)

    assert len(response.columns) == 1
    assert response.columns == [
        SqlColumn(name="campaign_id", data_type="INT"),
    ]
    assert response.data_preview is None


"""
# TODO: commented because Greenplum is supported only for Cloud and it cannot be tested using Docker image.
@gd_vcr.use_cassette(str(_fixtures_dir / "greenplum.yaml"))
def test_catalog_create_data_source_greenplum_spec(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    _create_delete_ds(
        sdk=sdk,
        data_source=CatalogDataSourceGreenplum(
            id="test",
            name="Test",
            db_specific_attributes=GreenplumAttributes(host="greenplum", db_name="demo"),
            schema="demo",
            credentials=BasicCredentials(
                username="demouser",
                password="demopass",
            ),
            enable_caching=True,
            cache_path=["cache_schema"],
            url_params=[("autosave", "true")],
        ),
    )
"""


def test_postgres_url_creation(test_config):
    data_source = CatalogDataSourcePostgres(
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
        url_params=[("autosave", "true")],
    )
    assert data_source.url == "jdbc:postgresql://localhost:5432/demo?autosave=true"


def test_snowflake_url_creation(test_config):
    data_source = CatalogDataSourceSnowflake(
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
        url_params=[("useProxy", "true")],
    )
    assert (
        data_source.url == "jdbc:snowflake://gooddata.snowflakecomputing.com:443?warehouse=TIGER&db=TIGER&useProxy=true"
    )


def test_allowed_data_source_type(test_config):
    allowed_types = JsonApiDataSourceInAttributes.allowed_values.get(("type",))
    for t in allowed_types.values():
        try:
            CatalogDataSource(
                id="test",
                name="Test2",
                type=t,
                url="jdbc:postgresql://localhost:5432/demo",
                schema="demo",
                credentials=BasicCredentials(
                    username="demouser",
                    password="demopass",
                ),
                enable_caching=False,
                url_params=[("param", "value")],
            )
        except ValueError:
            assert False, f"ValueError was raised for valid database type {t}"
    db_type = "nonsense"
    try:
        CatalogDataSource(
            id="test",
            name="Test2",
            type=db_type,
            url="jdbc:postgresql://localhost:5432/demo",
            schema="demo",
            credentials=BasicCredentials(
                username="demouser",
                password="demopass",
            ),
            enable_caching=False,
            url_params=[("param", "value")],
        )
    except ValueError:
        pass
    else:
        assert False, "ValueError was not raised for nonsense database type"


def test_catalog_data_source_mssql(test_config):
    data_source = CatalogDataSourceMsSql(
        id="test",
        name="Test",
        db_specific_attributes=MsSqlAttributes(host="Host", db_name="DbName"),
        schema="Schema",
        credentials=BasicCredentials(
            username="demouser",
            password="demopass",
        ),
    )
    assert data_source.url == "jdbc:sqlserver://Host:1433;databaseName=DbName"


def test_catalog_data_source_databricks(test_config):
    data_source = CatalogDataSourceDatabricks(
        id="test",
        name="Test",
        db_specific_attributes=DatabricksAttributes(host="Host", http_path="xyz123abc"),
        schema="SCHEMA",
        parameters=[{"name": "catalog", "value": "super_catalog"}],
        credentials=BasicCredentials(
            username="demouser",
            password="demospass",
        ),
    )
    assert data_source.url == "jdbc:databricks://Host:443/default;httpPath=xyz123abc"


def test_catalog_data_source_mysql(test_config):
    data_source = CatalogDataSourceMySql(
        id="test",
        name="Test",
        db_specific_attributes=MySqlAttributes(host="localhost", port="3306"),
        schema="my_schema",
        credentials=BasicCredentials(
            username="demouser",
            password="demospass",
        ),
    )
    assert data_source.url == "jdbc:mysql://localhost:3306/my_schema"


def test_catalog_data_source_mariadb(test_config):
    data_source = CatalogDataSourceMariaDb(
        id="test",
        name="Test",
        db_specific_attributes=MariaDbAttributes(host="localhost", port="3306"),
        schema="my_schema",
        credentials=BasicCredentials(
            username="demouser",
            password="demospass",
        ),
    )
    assert data_source.url == "jdbc:mariadb://localhost:3306/my_schema"

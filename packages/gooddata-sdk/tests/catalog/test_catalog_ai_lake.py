# (C) 2026 GoodData Corporation
from __future__ import annotations

from gooddata_sdk import (
    CatalogCreatePipeTableRequest,
    CatalogDatabaseInstance,
    CatalogPipeTable,
    CatalogPipeTableSummary,
    CatalogProvisionDatabaseInstanceRequest,
    CatalogServiceInfo,
)
from gooddata_sdk.catalog.data_source.entity_model.data_source import CatalogDataSourceAiLakehouse


class TestCatalogDatabaseInstance:
    def test_from_api_full(self):
        entity = {
            "id": "my-instance",
            "name": "My Instance",
            "storage_ids": ["storage-1", "storage-2"],
        }
        instance = CatalogDatabaseInstance.from_api(entity)
        assert instance.id == "my-instance"
        assert instance.name == "My Instance"
        assert instance.storage_ids == ["storage-1", "storage-2"]

    def test_from_api_no_storage_ids(self):
        entity = {
            "id": "inst-1",
            "name": "Instance 1",
        }
        instance = CatalogDatabaseInstance.from_api(entity)
        assert instance.id == "inst-1"
        assert instance.storage_ids == []


class TestCatalogProvisionDatabaseInstanceRequest:
    def test_as_api_model(self):
        request = CatalogProvisionDatabaseInstanceRequest(
            name="new-instance",
            storage_ids=["s1", "s2"],
        )
        api_model = request.as_api_model()
        assert api_model.name == "new-instance"
        assert api_model.storage_ids == ["s1", "s2"]

    def test_as_api_model_empty_storage(self):
        request = CatalogProvisionDatabaseInstanceRequest(name="minimal")
        api_model = request.as_api_model()
        assert api_model.name == "minimal"
        assert api_model.storage_ids == []


class TestCatalogCreatePipeTableRequest:
    def test_as_api_model_required_only(self):
        request = CatalogCreatePipeTableRequest(
            path_prefix="my-dataset/",
            source_storage_name="my-storage",
            table_name="my_table",
        )
        api_model = request.as_api_model()
        assert api_model.path_prefix == "my-dataset/"
        assert api_model.source_storage_name == "my-storage"
        assert api_model.table_name == "my_table"

    def test_as_api_model_with_optional_fields(self):
        request = CatalogCreatePipeTableRequest(
            path_prefix="data/",
            source_storage_name="s3-storage",
            table_name="sales_data",
            column_overrides={"amount": "DECIMAL(10,2)"},
            max_varchar_length=255,
            polling_interval_seconds=60,
            table_properties={"replication_num": "3"},
        )
        api_model = request.as_api_model()
        assert api_model.column_overrides == {"amount": "DECIMAL(10,2)"}
        assert api_model.max_varchar_length == 255
        assert api_model.polling_interval_seconds == 60
        assert api_model.table_properties == {"replication_num": "3"}


class TestCatalogPipeTableSummary:
    def test_from_api(self):
        entity = {
            "pipe_table_id": "uuid-1",
            "table_name": "orders",
            "path_prefix": "data/orders/",
            "columns": [{"name": "id", "data_type": "INT"}],
        }
        summary = CatalogPipeTableSummary.from_api(entity)
        assert summary.pipe_table_id == "uuid-1"
        assert summary.table_name == "orders"
        assert summary.path_prefix == "data/orders/"
        assert len(summary.columns) == 1


class TestCatalogPipeTable:
    def test_from_api(self):
        entity = {
            "pipe_table_id": "uuid-2",
            "table_name": "events",
            "source_storage_name": "s3-src",
            "path_prefix": "data/events/",
            "database_name": "mydb",
            "polling_interval_seconds": 30,
            "partition_columns": ["year", "month"],
            "table_properties": {"replication_num": "1"},
            "columns": [],
        }
        table = CatalogPipeTable.from_api(entity)
        assert table.pipe_table_id == "uuid-2"
        assert table.table_name == "events"
        assert table.source_storage_name == "s3-src"
        assert table.database_name == "mydb"
        assert table.polling_interval_seconds == 30
        assert table.partition_columns == ["year", "month"]
        assert table.table_properties == {"replication_num": "1"}


class TestCatalogServiceInfo:
    def test_from_api(self):
        entity = {
            "name": "StarRocks Service",
            "service_id": "svc-uuid-123",
        }
        svc = CatalogServiceInfo.from_api(entity)
        assert svc.name == "StarRocks Service"
        assert svc.service_id == "svc-uuid-123"


class TestCatalogDataSourceAiLakehouse:
    def test_ailakehouse_type(self):
        from gooddata_sdk.catalog.entity import BasicCredentials

        ds = CatalogDataSourceAiLakehouse(
            id="ailake-ds",
            name="AI Lake DS",
            type="AILAKEHOUSE",
            schema="",
            credentials=BasicCredentials(username="u", password="p"),
        )
        assert ds.type == "AILAKEHOUSE"
        assert ds.schema == ""

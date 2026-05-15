# (C) 2026 GoodData Corporation
"""Unit tests for `CatalogAILakeService`.

These tests use plain mocks against `AILakeApi` rather than vcr cassettes
because the service is a thin wrapper whose interesting logic
(`wait_for_operation` polling, status discrimination, UUID-seeding) is
deterministic and worth verifying without a live stack.
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, call, patch

import pytest
from gooddata_sdk.catalog.ai_lake.entity_model.column_expression import CatalogColumnExpression
from gooddata_sdk.catalog.ai_lake.entity_model.object_storage import CatalogObjectStorageInfo
from gooddata_sdk.catalog.ai_lake.service import (
    CatalogAILakeOperation,
    CatalogAILakeOperationError,
    CatalogAILakeService,
)


def _make_service() -> tuple[CatalogAILakeService, MagicMock]:
    """Build a service whose api-client side is fully mocked."""
    fake_ai_lake_api = MagicMock(name="AILakeApi")
    fake_client = SimpleNamespace(_api_client=MagicMock(name="ApiClient"))

    with patch("gooddata_sdk.catalog.ai_lake.service.AILakeApi", return_value=fake_ai_lake_api):
        service = CatalogAILakeService(fake_client)  # type: ignore[arg-type]

    assert service._ai_lake_api is fake_ai_lake_api
    return service, fake_ai_lake_api


def _operation_response(**fields: object) -> MagicMock:
    """Mimic the api-client's deserialized response (`.to_dict()` returns the raw dict)."""
    response = MagicMock()
    response.to_dict.return_value = fields
    return response


class TestAnalyzeStatistics:
    def test_seeds_caller_supplied_operation_id(self) -> None:
        service, api = _make_service()
        op_id = service.analyze_statistics(
            instance_id="demo-db",
            table_names=["fact_orders", "dim_country"],
            operation_id="11111111-2222-3333-4444-555555555555",
        )
        assert op_id == "11111111-2222-3333-4444-555555555555"
        assert api.analyze_statistics.call_count == 1
        call_args = api.analyze_statistics.call_args
        assert call_args.args[0] == "demo-db"
        assert call_args.kwargs["operation_id"] == "11111111-2222-3333-4444-555555555555"
        # Body request carries the table names.
        body = call_args.args[1]
        assert list(body.table_names) == ["fact_orders", "dim_country"]

    def test_generates_uuid_when_not_supplied(self) -> None:
        service, api = _make_service()
        op_id = service.analyze_statistics(instance_id="demo-db")
        # UUID4 string format: 8-4-4-4-12 hex chars.
        assert len(op_id) == 36 and op_id.count("-") == 4
        assert api.analyze_statistics.call_args.kwargs["operation_id"] == op_id

    def test_empty_table_names_is_normalized_to_empty_list(self) -> None:
        service, api = _make_service()
        service.analyze_statistics(instance_id="demo-db", table_names=None)
        assert list(api.analyze_statistics.call_args.args[1].table_names) == []


class TestGetOperation:
    def test_normalizes_to_typed_handle(self) -> None:
        service, api = _make_service()
        api.get_ai_lake_operation.return_value = _operation_response(
            id="op-1",
            kind="analyze-statistics",
            status="succeeded",
            result={"tablesAnalyzed": 7},
        )
        op = service.get_operation("op-1")
        assert isinstance(op, CatalogAILakeOperation)
        assert op.id == "op-1"
        assert op.kind == "analyze-statistics"
        assert op.is_succeeded
        assert op.result == {"tablesAnalyzed": 7}
        assert op.error is None

    def test_carries_error_payload_on_failed(self) -> None:
        service, api = _make_service()
        api.get_ai_lake_operation.return_value = _operation_response(
            id="op-2",
            kind="analyze-statistics",
            status="failed",
            error={"code": "ANALYZE_FAILED", "message": "table not found"},
        )
        op = service.get_operation("op-2")
        assert op.is_failed
        assert op.error == {"code": "ANALYZE_FAILED", "message": "table not found"}


class TestWaitForOperation:
    def test_polls_until_succeeded(self) -> None:
        service, api = _make_service()
        api.get_ai_lake_operation.side_effect = [
            _operation_response(id="op", kind="analyze-statistics", status="pending"),
            _operation_response(id="op", kind="analyze-statistics", status="pending"),
            _operation_response(id="op", kind="analyze-statistics", status="succeeded", result={}),
        ]
        with patch("gooddata_sdk.catalog.ai_lake.service.time.sleep") as fake_sleep:
            op = service.wait_for_operation("op", poll_s=0.5)
        assert op.is_succeeded
        assert api.get_ai_lake_operation.call_count == 3
        # Slept twice between three polls.
        assert fake_sleep.call_args_list == [call(0.5), call(0.5)]

    def test_raises_on_failed_terminal_status(self) -> None:
        service, api = _make_service()
        api.get_ai_lake_operation.return_value = _operation_response(
            id="op", kind="analyze-statistics", status="failed", error={"message": "boom"}
        )
        with (
            patch("gooddata_sdk.catalog.ai_lake.service.time.sleep"),
            pytest.raises(CatalogAILakeOperationError) as exc_info,
        ):
            service.wait_for_operation("op")
        assert exc_info.value.operation.is_failed
        assert "boom" in str(exc_info.value)

    def test_times_out_when_never_terminal(self) -> None:
        service, api = _make_service()
        api.get_ai_lake_operation.return_value = _operation_response(
            id="op", kind="analyze-statistics", status="pending"
        )
        # Make `time.monotonic` advance past the deadline on the second call so
        # the loop runs a few iterations before raising.
        with (
            patch("gooddata_sdk.catalog.ai_lake.service.time.sleep"),
            patch(
                "gooddata_sdk.catalog.ai_lake.service.time.monotonic",
                side_effect=[0.0, 1.0, 5.0, 11.0],
            ),
            pytest.raises(TimeoutError) as exc_info,
        ):
            service.wait_for_operation("op", timeout_s=10.0, poll_s=0.1)
        assert "did not finish within 10.0s" in str(exc_info.value)


class TestListObjectStorages:
    """Unit tests for `CatalogAILakeService.list_object_storages`."""

    def _storages_response(self, storages: list[dict]) -> MagicMock:
        response = MagicMock()
        response.to_dict.return_value = {"storages": storages}
        return response

    def test_returns_list_of_storage_infos(self) -> None:
        service, api = _make_service()
        api.list_ai_lake_object_storages.return_value = self._storages_response(
            [
                {
                    "name": "my-s3",
                    "storage_id": "11111111-2222-3333-4444-555555555555",
                    "storage_type": "S3",
                    "storage_config": {"bucket": "my-bucket", "region": "us-east-1"},
                },
                {
                    "name": "my-minio",
                    "storage_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
                    "storage_type": "MINIO",
                    "storage_config": {},
                },
            ]
        )
        storages = service.list_object_storages()

        assert len(storages) == 2
        assert all(isinstance(s, CatalogObjectStorageInfo) for s in storages)

        s0 = storages[0]
        assert s0.name == "my-s3"
        assert s0.storage_id == "11111111-2222-3333-4444-555555555555"
        assert s0.storage_type == "S3"
        assert s0.storage_config == {"bucket": "my-bucket", "region": "us-east-1"}

        s1 = storages[1]
        assert s1.name == "my-minio"
        assert s1.storage_config == {}

    def test_empty_storages_list(self) -> None:
        service, api = _make_service()
        api.list_ai_lake_object_storages.return_value = self._storages_response([])
        storages = service.list_object_storages()
        assert storages == []

    def test_passes_check_return_type_false(self) -> None:
        service, api = _make_service()
        api.list_ai_lake_object_storages.return_value = self._storages_response([])
        service.list_object_storages()
        api.list_ai_lake_object_storages.assert_called_once_with(_check_return_type=False)


class TestCreatePipeTable:
    """Unit tests for `CatalogAILakeService.create_pipe_table`."""

    def test_basic_create_pipe_table(self) -> None:
        service, api = _make_service()
        service.create_pipe_table(
            instance_id="demo-db",
            table_name="fact_events",
            source_storage_name="my-s3",
            path_prefix="events/year=2024/",
        )
        assert api.create_ai_lake_pipe_table.call_count == 1
        call_args = api.create_ai_lake_pipe_table.call_args
        assert call_args.args[0] == "demo-db"
        request = call_args.args[1]
        assert request.table_name == "fact_events"
        assert request.source_storage_name == "my-s3"
        assert request.path_prefix == "events/year=2024/"

    def test_column_expressions_are_serialized(self) -> None:
        service, api = _make_service()
        service.create_pipe_table(
            instance_id="demo-db",
            table_name="fact_events",
            source_storage_name="my-s3",
            path_prefix="events/",
            column_expressions={
                "user_hll": CatalogColumnExpression(column="user_id", function="HLL_HASH"),
                "page_bmp": CatalogColumnExpression(column="page_id", function="TO_BITMAP"),
            },
        )
        request = api.create_ai_lake_pipe_table.call_args.args[1]
        exprs = request.column_expressions
        assert set(exprs.keys()) == {"user_hll", "page_bmp"}
        # Verify the API model values
        assert exprs["user_hll"].column == "user_id"
        assert exprs["user_hll"].function == "HLL_HASH"
        assert exprs["page_bmp"].column == "page_id"
        assert exprs["page_bmp"].function == "TO_BITMAP"

    def test_optional_kwargs_not_sent_when_none(self) -> None:
        service, api = _make_service()
        service.create_pipe_table(
            instance_id="demo-db",
            table_name="fact_events",
            source_storage_name="my-s3",
            path_prefix="events/",
        )
        request = api.create_ai_lake_pipe_table.call_args.args[1]
        # Optional fields should not be set
        assert "column_expressions" not in request._data_store
        assert "column_overrides" not in request._data_store
        assert "aggregation_overrides" not in request._data_store

    def test_all_optional_kwargs_forwarded(self) -> None:
        service, api = _make_service()
        service.create_pipe_table(
            instance_id="demo-db",
            table_name="fact_events",
            source_storage_name="my-s3",
            path_prefix="events/",
            column_overrides={"year": "INT"},
            aggregation_overrides={"revenue": "SUM"},
            max_varchar_length=256,
            polling_interval_seconds=60,
            table_properties={"replication_num": "3"},
        )
        request = api.create_ai_lake_pipe_table.call_args.args[1]
        assert request.column_overrides == {"year": "INT"}
        assert request.aggregation_overrides == {"revenue": "SUM"}
        assert request.max_varchar_length == 256
        assert request.polling_interval_seconds == 60
        assert request.table_properties == {"replication_num": "3"}


class TestCatalogColumnExpression:
    """Unit tests for `CatalogColumnExpression`."""

    @pytest.mark.parametrize(
        "function",
        ["HLL_HASH", "BITMAP_HASH", "BITMAP_HASH64", "TO_BITMAP"],
    )
    def test_as_api_model_roundtrip(self, function: str) -> None:
        expr = CatalogColumnExpression(column="src_col", function=function)  # type: ignore[arg-type]
        api_model = expr.as_api_model()
        assert api_model.column == "src_col"
        assert api_model.function == function

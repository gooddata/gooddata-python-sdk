# (C) 2026 GoodData Corporation
"""Unit tests for `CatalogAILakeService`.

These tests use plain mocks against `AILakeApi` rather than vcr cassettes
because the service is a thin wrapper whose interesting logic
(`wait_for_operation` polling, status discrimination, UUID-seeding) is
deterministic and worth verifying without a live stack.
"""

from __future__ import annotations

import json
from types import SimpleNamespace
from unittest.mock import MagicMock, call, patch

import pytest
from gooddata_sdk.catalog.ai_lake.service import (
    CatalogAILakeOperation,
    CatalogAILakeOperationError,
    CatalogAILakeService,
)


def _make_service() -> tuple[CatalogAILakeService, MagicMock]:
    """Build a service whose api-client side is fully mocked."""
    fake_ai_lake_api = MagicMock(name="AILakeApi")
    fake_client = SimpleNamespace(
        _api_client=MagicMock(name="ApiClient"),
        _hostname="http://localhost:3000",
        _token="test-token",
    )

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


class TestRefreshPartition:
    """Unit tests for refresh_partition, which uses raw requests.post.

    The interesting logic here is UUID seeding, URL construction, and correct
    forwarding of the operation-id header — worth verifying without a live stack.
    """

    @patch("gooddata_sdk.catalog.ai_lake.service.requests.post")
    def test_seeds_caller_supplied_operation_id(self, mock_post: MagicMock) -> None:
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        service, _ = _make_service()
        op_id = service.refresh_partition(
            instance_id="demo-db",
            table_name="fact_orders",
            partition_spec={"year": "2024"},
            operation_id="11111111-2222-3333-4444-555555555555",
        )
        assert op_id == "11111111-2222-3333-4444-555555555555"
        call_kwargs = mock_post.call_args
        assert call_kwargs.kwargs["headers"]["operation-id"] == "11111111-2222-3333-4444-555555555555"

    @patch("gooddata_sdk.catalog.ai_lake.service.requests.post")
    def test_generates_uuid_when_not_supplied(self, mock_post: MagicMock) -> None:
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        service, _ = _make_service()
        op_id = service.refresh_partition(
            instance_id="demo-db",
            table_name="fact_orders",
            partition_spec={"year": "2024"},
        )
        assert len(op_id) == 36 and op_id.count("-") == 4
        call_kwargs = mock_post.call_args
        assert call_kwargs.kwargs["headers"]["operation-id"] == op_id

    @patch("gooddata_sdk.catalog.ai_lake.service.requests.post")
    def test_constructs_correct_url_and_body(self, mock_post: MagicMock) -> None:
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        service, _ = _make_service()
        service.refresh_partition(
            instance_id="demo-db",
            table_name="sales",
            partition_spec={"region": "eu", "month": "2024-01"},
        )
        call_kwargs = mock_post.call_args
        url = call_kwargs.kwargs["url"]
        assert "demo-db" in url
        assert "sales" in url
        assert url.endswith("/refresh")
        body = json.loads(call_kwargs.kwargs["data"])
        assert body == {"partitionSpec": {"region": "eu", "month": "2024-01"}}

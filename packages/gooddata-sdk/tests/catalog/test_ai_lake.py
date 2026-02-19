# (C) 2025 GoodData Corporation
from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from gooddata_sdk import (
    AiLakeService,
    CatalogDatabaseInstance,
    CatalogFailedOperation,
    CatalogOperation,
    CatalogPendingOperation,
    CatalogProvisionDatabaseInstanceRequest,
    CatalogSucceededOperation,
    GoodDataApiClient,
)
from gooddata_sdk.catalog.ai_lake.model import CatalogOperationError


def _make_mock_api_client() -> MagicMock:
    """Create a mock GoodDataApiClient."""
    mock_client = MagicMock(spec=GoodDataApiClient)
    mock_client._api_client = MagicMock()
    return mock_client


class TestCatalogProvisionDatabaseInstanceRequest:
    def test_as_api_model_round_trip(self) -> None:
        request = CatalogProvisionDatabaseInstanceRequest(
            name="test-db",
            storage_ids={"storage-1", "storage-2"},
        )
        api_model = request.as_api_model()
        assert api_model.name == "test-db"
        assert set(api_model.storage_ids) == {"storage-1", "storage-2"}

    def test_as_api_model_single_storage(self) -> None:
        request = CatalogProvisionDatabaseInstanceRequest(
            name="my-database",
            storage_ids={"only-storage"},
        )
        api_model = request.as_api_model()
        assert api_model.name == "my-database"
        assert api_model.storage_ids == ["only-storage"]


class TestAiLakeServiceProvision:
    def test_provision_database_instance_no_operation_id(self) -> None:
        mock_client = _make_mock_api_client()
        with patch("gooddata_sdk.catalog.ai_lake.service.AILakeApi") as mock_api_class:
            mock_api = MagicMock()
            mock_api_class.return_value = mock_api

            service = AiLakeService(mock_client)
            request = CatalogProvisionDatabaseInstanceRequest(
                name="test-db",
                storage_ids={"storage-1"},
            )
            service.provision_database_instance(request)

            mock_api.provision_ai_lake_database_instance.assert_called_once()
            call_kwargs = mock_api.provision_ai_lake_database_instance.call_args[1]
            assert "operation_id" not in call_kwargs
            assert call_kwargs["provision_database_instance_request"].name == "test-db"

    def test_provision_database_instance_with_operation_id(self) -> None:
        mock_client = _make_mock_api_client()
        with patch("gooddata_sdk.catalog.ai_lake.service.AILakeApi") as mock_api_class:
            mock_api = MagicMock()
            mock_api_class.return_value = mock_api

            service = AiLakeService(mock_client)
            request = CatalogProvisionDatabaseInstanceRequest(
                name="test-db",
                storage_ids={"storage-1"},
            )
            service.provision_database_instance(request, operation_id="op-uuid-123")

            mock_api.provision_ai_lake_database_instance.assert_called_once()
            call_kwargs = mock_api.provision_ai_lake_database_instance.call_args[1]
            assert call_kwargs["operation_id"] == "op-uuid-123"


class TestAiLakeServiceDeprovision:
    def test_deprovision_database_instance_no_operation_id(self) -> None:
        mock_client = _make_mock_api_client()
        with patch("gooddata_sdk.catalog.ai_lake.service.AILakeApi") as mock_api_class:
            mock_api = MagicMock()
            mock_api_class.return_value = mock_api

            service = AiLakeService(mock_client)
            service.deprovision_database_instance("instance-abc")

            mock_api.deprovision_ai_lake_database_instance.assert_called_once_with("instance-abc")

    def test_deprovision_database_instance_with_operation_id(self) -> None:
        mock_client = _make_mock_api_client()
        with patch("gooddata_sdk.catalog.ai_lake.service.AILakeApi") as mock_api_class:
            mock_api = MagicMock()
            mock_api_class.return_value = mock_api

            service = AiLakeService(mock_client)
            service.deprovision_database_instance("instance-abc", operation_id="op-uuid-456")

            mock_api.deprovision_ai_lake_database_instance.assert_called_once_with(
                "instance-abc", operation_id="op-uuid-456"
            )


class TestAiLakeServiceGetDatabaseInstance:
    def test_get_database_instance(self) -> None:
        mock_client = _make_mock_api_client()
        with patch("gooddata_sdk.catalog.ai_lake.service.AILakeApi") as mock_api_class:
            mock_api = MagicMock()
            mock_api_class.return_value = mock_api

            api_result = MagicMock()
            api_result.id = "instance-abc"
            api_result.name = "test-db"
            api_result.storage_ids = ["storage-1", "storage-2"]
            mock_api.get_ai_lake_database_instance.return_value = api_result

            service = AiLakeService(mock_client)
            result = service.get_database_instance("instance-abc")

            assert isinstance(result, CatalogDatabaseInstance)
            assert result.id == "instance-abc"
            assert result.name == "test-db"
            assert result.storage_ids == ["storage-1", "storage-2"]
            mock_api.get_ai_lake_database_instance.assert_called_once_with("instance-abc")


class TestAiLakeServiceGetOperation:
    def test_get_operation_pending(self) -> None:
        from gooddata_api_client.model.pending_operation import PendingOperation as ApiPendingOperation

        mock_client = _make_mock_api_client()
        with patch("gooddata_sdk.catalog.ai_lake.service.AILakeApi") as mock_api_class:
            mock_api = MagicMock()
            mock_api_class.return_value = mock_api

            api_result = MagicMock(spec=ApiPendingOperation)
            api_result.id = "op-123"
            api_result.kind = "provision-database"
            mock_api.get_ai_lake_operation.return_value = api_result

            service = AiLakeService(mock_client)
            result = service.get_operation("op-123")

            assert isinstance(result, CatalogPendingOperation)
            assert result.id == "op-123"
            assert result.kind == "provision-database"
            assert result.status == "pending"

    def test_get_operation_succeeded(self) -> None:
        from gooddata_api_client.model.succeeded_operation import SucceededOperation as ApiSucceededOperation

        mock_client = _make_mock_api_client()
        with patch("gooddata_sdk.catalog.ai_lake.service.AILakeApi") as mock_api_class:
            mock_api = MagicMock()
            mock_api_class.return_value = mock_api

            api_result = MagicMock(spec=ApiSucceededOperation)
            api_result.id = "op-456"
            api_result.kind = "provision-database"
            api_result.result = {"instanceId": "inst-789"}
            mock_api.get_ai_lake_operation.return_value = api_result

            service = AiLakeService(mock_client)
            result = service.get_operation("op-456")

            assert isinstance(result, CatalogSucceededOperation)
            assert result.id == "op-456"
            assert result.kind == "provision-database"
            assert result.status == "succeeded"
            assert result.result == {"instanceId": "inst-789"}

    def test_get_operation_succeeded_null_result(self) -> None:
        """SucceededOperation.result is nullable (e.g., for deprovision operations)."""
        from gooddata_api_client.model.succeeded_operation import SucceededOperation as ApiSucceededOperation

        mock_client = _make_mock_api_client()
        with patch("gooddata_sdk.catalog.ai_lake.service.AILakeApi") as mock_api_class:
            mock_api = MagicMock()
            mock_api_class.return_value = mock_api

            api_result = MagicMock(spec=ApiSucceededOperation)
            api_result.id = "op-deprov"
            api_result.kind = "deprovision-database"
            api_result.result = None
            mock_api.get_ai_lake_operation.return_value = api_result

            service = AiLakeService(mock_client)
            result = service.get_operation("op-deprov")

            assert isinstance(result, CatalogSucceededOperation)
            assert result.id == "op-deprov"
            assert result.kind == "deprovision-database"
            assert result.status == "succeeded"
            assert result.result is None

    def test_get_operation_failed(self) -> None:
        from gooddata_api_client.model.failed_operation import FailedOperation as ApiFailedOperation

        mock_client = _make_mock_api_client()
        with patch("gooddata_sdk.catalog.ai_lake.service.AILakeApi") as mock_api_class:
            mock_api = MagicMock()
            mock_api_class.return_value = mock_api

            mock_error = MagicMock()
            mock_error.title = "Provisioning failed"
            mock_error.status = 500
            mock_error.detail = "Database provisioning encountered an error"

            api_result = MagicMock(spec=ApiFailedOperation)
            api_result.id = "op-789"
            api_result.kind = "provision-database"
            api_result.error = mock_error
            mock_api.get_ai_lake_operation.return_value = api_result

            service = AiLakeService(mock_client)
            result = service.get_operation("op-789")

            assert isinstance(result, CatalogFailedOperation)
            assert result.id == "op-789"
            assert result.kind == "provision-database"
            assert result.status == "failed"
            assert isinstance(result.error, CatalogOperationError)
            assert result.error.title == "Provisioning failed"
            assert result.error.status == 500
            assert result.error.detail == "Database provisioning encountered an error"

# (C) 2025 GoodData Corporation
from __future__ import annotations

from typing import Optional, Union

from gooddata_api_client.api.ai_lake_api import AILakeApi
from gooddata_api_client.model.failed_operation import FailedOperation as ApiFailedOperation
from gooddata_api_client.model.pending_operation import PendingOperation as ApiPendingOperation
from gooddata_api_client.model.succeeded_operation import SucceededOperation as ApiSucceededOperation

from gooddata_sdk.catalog.ai_lake.model import (
    CatalogDatabaseInstance,
    CatalogFailedOperation,
    CatalogOperation,
    CatalogPendingOperation,
    CatalogProvisionDatabaseInstanceRequest,
    CatalogSucceededOperation,
)
from gooddata_sdk.client import GoodDataApiClient


def _convert_operation(
    api_op: Union[ApiPendingOperation, ApiSucceededOperation, ApiFailedOperation],
) -> CatalogOperation:
    if isinstance(api_op, ApiSucceededOperation):
        return CatalogSucceededOperation.from_api(api_op)
    elif isinstance(api_op, ApiFailedOperation):
        return CatalogFailedOperation.from_api(api_op)
    elif isinstance(api_op, ApiPendingOperation):
        return CatalogPendingOperation.from_api(api_op)
    else:
        raise ValueError(f"Unknown operation type: {type(api_op)}")


class AiLakeService:
    def __init__(self, api_client: GoodDataApiClient) -> None:
        self._client = api_client
        self._api = AILakeApi(api_client._api_client)

    def provision_database_instance(
        self,
        request: CatalogProvisionDatabaseInstanceRequest,
        operation_id: Optional[str] = None,
    ) -> None:
        """(BETA) Provision a new AI Lake database instance.

        Args:
            request (CatalogProvisionDatabaseInstanceRequest):
                Request containing name and storage IDs for the new database instance.
            operation_id (Optional[str]):
                Optional idempotency key for the operation.

        Returns:
            None
        """
        kwargs: dict = {"provision_database_instance_request": request.as_api_model()}
        if operation_id is not None:
            kwargs["operation_id"] = operation_id
        self._api.provision_ai_lake_database_instance(**kwargs)

    def deprovision_database_instance(
        self,
        instance_id: str,
        operation_id: Optional[str] = None,
    ) -> None:
        """(BETA) Delete an existing AI Lake database instance.

        Args:
            instance_id (str):
                ID of the database instance to delete.
            operation_id (Optional[str]):
                Optional idempotency key for the operation.

        Returns:
            None
        """
        kwargs: dict = {}
        if operation_id is not None:
            kwargs["operation_id"] = operation_id
        self._api.deprovision_ai_lake_database_instance(instance_id, **kwargs)

    def get_database_instance(
        self,
        instance_id: str,
    ) -> CatalogDatabaseInstance:
        """(BETA) Get details of an AI Lake database instance.

        Args:
            instance_id (str):
                ID of the database instance to retrieve.

        Returns:
            CatalogDatabaseInstance: Details of the database instance.
        """
        result = self._api.get_ai_lake_database_instance(instance_id)
        return CatalogDatabaseInstance.from_api(result)

    def get_operation(
        self,
        operation_id: str,
    ) -> CatalogOperation:
        """(BETA) Get the status of a long-running AI Lake operation.

        Args:
            operation_id (str):
                ID of the operation to retrieve.

        Returns:
            CatalogOperation: The operation status, one of CatalogPendingOperation,
                CatalogSucceededOperation, or CatalogFailedOperation.
        """
        result = self._api.get_ai_lake_operation(operation_id)
        return _convert_operation(result)

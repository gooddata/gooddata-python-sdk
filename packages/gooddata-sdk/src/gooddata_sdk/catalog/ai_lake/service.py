# (C) 2026 GoodData Corporation
from __future__ import annotations

from gooddata_sdk.catalog.ai_lake.entity_model.database_instance import (
    CatalogDatabaseInstance,
    CatalogProvisionDatabaseInstanceRequest,
)
from gooddata_sdk.catalog.ai_lake.entity_model.pipe_table import (
    CatalogCreatePipeTableRequest,
    CatalogPipeTable,
    CatalogPipeTableSummary,
)
from gooddata_sdk.catalog.ai_lake.entity_model.service_info import CatalogServiceInfo
from gooddata_sdk.client import GoodDataApiClient


class CatalogAiLakeService:
    """Service for managing AI Lake database instances, pipe tables, and StarRocks services."""

    def __init__(self, api_client: GoodDataApiClient) -> None:
        self._client = api_client
        self._ai_lake_api = api_client.ai_lake_api
        self._ai_lake_pipe_tables_api = api_client.ai_lake_pipe_tables_api

    # Database instance methods

    def provision_database_instance(
        self,
        request: CatalogProvisionDatabaseInstanceRequest,
    ) -> None:
        """Provision a new AI Lake database instance.

        Args:
            request (CatalogProvisionDatabaseInstanceRequest):
                The provision request containing name and storage IDs.

        Returns:
            None
        """
        self._ai_lake_api.provision_ai_lake_database_instance(
            request.as_api_model(),
            _check_return_type=False,
        )

    def get_database_instance(self, instance_id: str) -> CatalogDatabaseInstance:
        """Retrieve an AI Lake database instance by ID or name.

        Args:
            instance_id (str):
                Database instance identifier (name preferred, or UUID).

        Returns:
            CatalogDatabaseInstance:
                The database instance.
        """
        response = self._ai_lake_api.get_ai_lake_database_instance(
            instance_id,
            _check_return_type=False,
        )
        return CatalogDatabaseInstance.from_api(response.to_dict(camel_case=False))

    def list_database_instances(self) -> list[CatalogDatabaseInstance]:
        """List all AI Lake database instances.

        Returns:
            list[CatalogDatabaseInstance]:
                All database instances in the organization.
        """
        response = self._ai_lake_api.list_ai_lake_database_instances(
            _check_return_type=False,
        )
        data = response.to_dict(camel_case=False)
        return [CatalogDatabaseInstance.from_api(db) for db in data.get("databases") or []]

    def deprovision_database_instance(self, instance_id: str) -> None:
        """Delete an existing AI Lake database instance.

        Args:
            instance_id (str):
                Database instance identifier (name preferred, or UUID).

        Returns:
            None
        """
        self._ai_lake_api.deprovision_ai_lake_database_instance(
            instance_id,
            _check_return_type=False,
        )

    # Pipe table methods

    def create_pipe_table(
        self,
        instance_id: str,
        request: CatalogCreatePipeTableRequest,
    ) -> None:
        """Create a new AI Lake pipe table in the given database instance.

        Args:
            instance_id (str):
                Database instance identifier.
            request (CatalogCreatePipeTableRequest):
                The create request with path prefix, source storage name, and table name.

        Returns:
            None
        """
        self._ai_lake_pipe_tables_api.create_ai_lake_pipe_table(
            instance_id,
            request.as_api_model(),
            _check_return_type=False,
        )

    def get_pipe_table(self, instance_id: str, table_name: str) -> CatalogPipeTable:
        """Retrieve a specific AI Lake pipe table.

        Args:
            instance_id (str):
                Database instance identifier.
            table_name (str):
                OLAP table name.

        Returns:
            CatalogPipeTable:
                The full pipe table details.
        """
        response = self._ai_lake_pipe_tables_api.get_ai_lake_pipe_table(
            instance_id,
            table_name,
            _check_return_type=False,
        )
        return CatalogPipeTable.from_api(response.to_dict(camel_case=False))

    def list_pipe_tables(self, instance_id: str) -> list[CatalogPipeTableSummary]:
        """List all AI Lake pipe tables for a database instance.

        Args:
            instance_id (str):
                Database instance identifier.

        Returns:
            list[CatalogPipeTableSummary]:
                All pipe tables in the given database instance.
        """
        response = self._ai_lake_pipe_tables_api.list_ai_lake_pipe_tables(
            instance_id,
            _check_return_type=False,
        )
        data = response.to_dict(camel_case=False)
        return [CatalogPipeTableSummary.from_api(pt) for pt in data.get("pipe_tables") or []]

    def delete_pipe_table(self, instance_id: str, table_name: str) -> None:
        """Delete an AI Lake pipe table.

        Args:
            instance_id (str):
                Database instance identifier.
            table_name (str):
                OLAP table name.

        Returns:
            None
        """
        self._ai_lake_pipe_tables_api.delete_ai_lake_pipe_table(
            instance_id,
            table_name,
            _check_return_type=False,
        )

    # Service methods

    def list_services(self) -> list[CatalogServiceInfo]:
        """List all AI Lake services configured for the organization.

        Returns:
            list[CatalogServiceInfo]:
                All services configured in the organization's AI Lake.
        """
        response = self._ai_lake_api.list_ai_lake_services(
            _check_return_type=False,
        )
        data = response.to_dict(camel_case=False)
        return [CatalogServiceInfo.from_api(svc) for svc in data.get("services") or []]

# (C) 2026 GoodData Corporation
"""SDK wrapper for the AI Lake long-running-operation surface.

Today this exposes only the operations needed by aggregate-aware LDMs:

- `analyze_statistics` triggers `ANALYZE TABLE` over a database instance so
  CBO statistics catch up after a schema or data change. Required after
  registering a pre-aggregation table whose dim attributes the platform will
  later resolve via filter pushdown.
- `get_operation` and `wait_for_operation` cover the polling side of the
  long-running operation contract that `analyze_statistics` returns.

The data-source management surface (multi-datasource CRUD on database
instances) is exposed through four additional methods:
- `list_database_data_sources` — list all data sources for an instance.
- `add_database_data_source` — attach a new data source to an instance.
- `remove_database_data_source` — detach a data source from an instance.
- `update_database_data_source` — rename or replace a data source on an
  instance.
"""

from __future__ import annotations

import time
import uuid
from typing import Any, Literal

from attrs import define
from gooddata_api_client.api.ai_lake_api import AILakeApi
from gooddata_api_client.api.ai_lake_databases_api import AILakeDatabasesApi
from gooddata_api_client.model.add_database_data_source_request import AddDatabaseDataSourceRequest
from gooddata_api_client.model.analyze_statistics_request import AnalyzeStatisticsRequest
from gooddata_api_client.model.update_database_data_source_request import UpdateDatabaseDataSourceRequest

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.client import GoodDataApiClient

# AI Lake operation status values (lower-case on the wire — these are the
# discriminator values of the `Operation` oneOf on the OpenAPI side).
OperationStatus = Literal["pending", "succeeded", "failed"]
TERMINAL_STATUSES: frozenset[OperationStatus] = frozenset({"succeeded", "failed"})


@define(kw_only=True)
class CatalogAILakeOperation(Base):
    """Long-running-operation handle returned by AI Lake actions."""

    id: str
    kind: str
    status: OperationStatus
    result: dict[str, Any] | None = None
    error: dict[str, Any] | None = None

    @property
    def is_terminal(self) -> bool:
        return self.status in TERMINAL_STATUSES

    @property
    def is_succeeded(self) -> bool:
        return self.status == "succeeded"

    @property
    def is_failed(self) -> bool:
        return self.status == "failed"


@define(kw_only=True)
class CatalogDataSourceInfo:
    """A single data source association for an AI Lake Database instance.

    ``id`` is the internal association-record identifier returned by
    list/add operations.  It is ``None`` when constructed from an update
    response, which only returns ``data_source_id`` and ``data_source_name``.
    """

    data_source_id: str
    data_source_name: str
    id: str | None = None

    @classmethod
    def _from_api_dict(cls, data: dict[str, Any]) -> CatalogDataSourceInfo:
        return cls(
            id=data.get("id"),
            data_source_id=data["data_source_id"],
            data_source_name=data["data_source_name"],
        )


class CatalogAILakeOperationError(RuntimeError):
    """Raised when an AI Lake long-running operation finishes in `failed` state."""

    def __init__(self, operation: CatalogAILakeOperation) -> None:
        self.operation = operation
        message = f"AI Lake operation {operation.id} ({operation.kind}) failed"
        if operation.error:
            message = f"{message}: {operation.error}"
        super().__init__(message)


class CatalogAILakeService:
    """Typed access to the AI Lake long-running-operation surface."""

    def __init__(self, api_client: GoodDataApiClient) -> None:
        self._client = api_client
        self._ai_lake_api: AILakeApi = AILakeApi(api_client._api_client)
        self._ai_lake_databases_api: AILakeDatabasesApi = AILakeDatabasesApi(api_client._api_client)

    def analyze_statistics(
        self,
        instance_id: str,
        table_names: list[str] | None = None,
        operation_id: str | None = None,
    ) -> str:
        """Trigger ANALYZE TABLE for tables in an AI Lake database instance.

        Args:
            instance_id: Database instance name (preferred) or UUID.
            table_names: Tables to analyze; if `None` or empty, every table
                in the instance is analyzed.
            operation_id: Optional client-supplied operation identifier. If
                omitted, a fresh UUID is generated. Pass the same value that
                `wait_for_operation` will poll on.

        Returns:
            The operation ID (UUID string) the platform will track this run
            under. Pass it to `get_operation` / `wait_for_operation` to poll.
        """
        op_id = operation_id or str(uuid.uuid4())
        request = AnalyzeStatisticsRequest(table_names=list(table_names) if table_names else [])
        # Body return is `Unit`; the platform tracks the operation under the
        # client-supplied or server-generated `operation-id` header. We seed
        # it ourselves so the caller gets a known polling handle without
        # having to read response headers.
        self._ai_lake_api.analyze_statistics(instance_id, request, operation_id=op_id)
        return op_id

    def get_operation(self, operation_id: str) -> CatalogAILakeOperation:
        """Fetch the current state of a long-running AI Lake operation."""
        response = self._ai_lake_api.get_ai_lake_operation(operation_id)
        # The api-client returns the oneOf'd operation as a dict-like object
        # whose concrete subtype depends on `status`. Normalize via to_dict.
        data = response.to_dict() if hasattr(response, "to_dict") else dict(response)
        return CatalogAILakeOperation(
            id=data["id"],
            kind=data["kind"],
            status=data["status"],
            result=data.get("result"),
            error=data.get("error"),
        )

    def wait_for_operation(
        self,
        operation_id: str,
        timeout_s: float = 300.0,
        poll_s: float = 2.0,
    ) -> CatalogAILakeOperation:
        """Block until an AI Lake operation reaches a terminal status.

        Raises `CatalogAILakeOperationError` on `failed` and `TimeoutError`
        if the operation does not reach a terminal state in time.
        """
        deadline = time.monotonic() + timeout_s
        while True:
            op = self.get_operation(operation_id)
            if op.is_succeeded:
                return op
            if op.is_failed:
                raise CatalogAILakeOperationError(op)
            if time.monotonic() >= deadline:
                raise TimeoutError(
                    f"AI Lake operation {operation_id} did not finish within {timeout_s}s (last status: {op.status})"
                )
            time.sleep(poll_s)

    # ------------------------------------------------------------------
    # Database data-source management
    # ------------------------------------------------------------------

    def list_database_data_sources(self, instance_id: str) -> list[CatalogDataSourceInfo]:
        """Return all data source associations for the given database instance.

        Args:
            instance_id: Database instance name (preferred) or UUID.

        Returns:
            List of :class:`CatalogDataSourceInfo` objects; empty list when
            the instance has no data sources.
        """
        response = self._ai_lake_databases_api.list_ai_lake_database_data_sources(instance_id, _check_return_type=False)
        data = response.to_dict() if hasattr(response, "to_dict") else dict(response)
        return [CatalogDataSourceInfo._from_api_dict(ds) for ds in data.get("data_sources", [])]

    def add_database_data_source(
        self,
        instance_id: str,
        data_source_id: str,
        *,
        data_source_name: str | None = None,
    ) -> CatalogDataSourceInfo:
        """Associate an additional data source with an AI Lake database instance.

        The new data source reuses the same StarRocks connection details as
        the instance's primary data source.

        Args:
            instance_id: Database instance name (preferred) or UUID.
            data_source_id: Identifier for the new data source in metadata-api.
                Must be unique within the organization.
            data_source_name: Optional display name for the new data source.

        Returns:
            :class:`CatalogDataSourceInfo` describing the newly created
            data source association.
        """
        kwargs: dict[str, Any] = {}
        if data_source_name is not None:
            kwargs["data_source_name"] = data_source_name
        request = AddDatabaseDataSourceRequest(
            data_source_id=data_source_id,
            _check_type=False,
            **kwargs,
        )
        response = self._ai_lake_databases_api.add_ai_lake_database_data_source(
            instance_id, request, _check_return_type=False
        )
        data = response.to_dict() if hasattr(response, "to_dict") else dict(response)
        return CatalogDataSourceInfo._from_api_dict(data["data_source"])

    def remove_database_data_source(
        self,
        instance_id: str,
        data_source_id: str,
    ) -> str:
        """Remove a data source association from an AI Lake database instance.

        This also deletes the corresponding data source from metadata-api.
        Fails if removing the data source would leave the instance with no
        data sources.

        Args:
            instance_id: Database instance name (preferred) or UUID.
            data_source_id: Identifier of the data source to remove.

        Returns:
            The identifier of the removed data source.
        """
        response = self._ai_lake_databases_api.remove_ai_lake_database_data_source(
            instance_id, data_source_id, _check_return_type=False
        )
        data = response.to_dict() if hasattr(response, "to_dict") else dict(response)
        return data["data_source_id"]

    def update_database_data_source(
        self,
        instance_id: str,
        old_data_source_id: str,
        new_data_source_id: str,
        *,
        data_source_name: str | None = None,
    ) -> CatalogDataSourceInfo:
        """Update the data source ID (and optionally name) on a database instance.

        Use this to recover from a wrong data source ID provisioned on an
        existing database instance without deleting the underlying database.

        Args:
            instance_id: Database instance name (preferred) or UUID.
            old_data_source_id: Identifier of the existing data source to replace.
            new_data_source_id: New identifier for the data source in metadata-api.
                Must be unique within the organization.
            data_source_name: Optional new display name for the data source.

        Returns:
            :class:`CatalogDataSourceInfo` reflecting the updated state.
            ``id`` will be ``None`` because the update endpoint does not
            return the association-record identifier.
        """
        kwargs: dict[str, Any] = {}
        if data_source_name is not None:
            kwargs["data_source_name"] = data_source_name
        request = UpdateDatabaseDataSourceRequest(
            old_data_source_id=old_data_source_id,
            data_source_id=new_data_source_id,
            _check_type=False,
            **kwargs,
        )
        response = self._ai_lake_databases_api.update_ai_lake_database_data_source(
            instance_id, request, _check_return_type=False
        )
        data = response.to_dict() if hasattr(response, "to_dict") else dict(response)
        return CatalogDataSourceInfo(
            data_source_id=data["data_source_id"],
            data_source_name=data["data_source_name"],
        )

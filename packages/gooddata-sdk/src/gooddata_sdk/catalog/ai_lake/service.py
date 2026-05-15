# (C) 2026 GoodData Corporation
"""SDK wrapper for the AI Lake API surface.

Currently exposed operations:

- `list_object_storages` lists ObjectStorages registered for the organization.
  Use the returned names as ``source_storage_name`` in `create_pipe_table`.
- `create_pipe_table` registers a pipe table in a database instance, with
  optional `CatalogColumnExpression` overrides for HLL / BITMAP columns.
- `analyze_statistics` triggers ``ANALYZE TABLE`` over a database instance so
  CBO statistics catch up after a schema or data change.
- `get_operation` and `wait_for_operation` cover the polling side of the
  long-running operation contract that `analyze_statistics` returns.
"""

from __future__ import annotations

import time
import uuid
from typing import Any, Literal

from attrs import define
from gooddata_api_client.api.ai_lake_api import AILakeApi
from gooddata_api_client.model.analyze_statistics_request import AnalyzeStatisticsRequest
from gooddata_api_client.model.create_pipe_table_request import CreatePipeTableRequest

from gooddata_sdk.catalog.ai_lake.entity_model.column_expression import CatalogColumnExpression
from gooddata_sdk.catalog.ai_lake.entity_model.object_storage import CatalogObjectStorageInfo
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

    # ------------------------------------------------------------------
    # ObjectStorage listing
    # ------------------------------------------------------------------

    def list_object_storages(self) -> list[CatalogObjectStorageInfo]:
        """List ObjectStorages registered for the organization.

        Provider credentials are stripped server-side — only safe descriptors
        (id, name, type, bucket, region, endpoint, …) are returned.

        Use the returned :attr:`~CatalogObjectStorageInfo.name` as
        ``source_storage_name`` when calling :meth:`create_pipe_table`, or
        pass :attr:`~CatalogObjectStorageInfo.storage_id` to the
        ``ProvisionDatabase`` ``storageIds`` list.

        Returns:
            List of :class:`CatalogObjectStorageInfo`, ordered by name.
        """
        response = self._ai_lake_api.list_ai_lake_object_storages(_check_return_type=False)
        data = response.to_dict() if hasattr(response, "to_dict") else dict(response)
        return [CatalogObjectStorageInfo.from_dict(s) for s in data.get("storages", [])]

    # ------------------------------------------------------------------
    # Pipe-table management
    # ------------------------------------------------------------------

    def create_pipe_table(
        self,
        instance_id: str,
        table_name: str,
        source_storage_name: str,
        path_prefix: str,
        *,
        column_expressions: dict[str, CatalogColumnExpression] | None = None,
        column_overrides: dict[str, str] | None = None,
        aggregation_overrides: dict[str, str] | None = None,
        max_varchar_length: int | None = None,
        polling_interval_seconds: int | None = None,
        table_properties: dict[str, str] | None = None,
    ) -> None:
        """Register a new pipe table in an AI Lake database instance.

        Args:
            instance_id: Database instance name (preferred) or UUID.
            table_name: OLAP table name. Must match ``^[a-z][a-z0-9_-]{0,62}$``.
            source_storage_name: Name of a registered ObjectStorage (use
                :meth:`list_object_storages` to discover available names).
            path_prefix: Path prefix to the parquet files in the storage
                (e.g. ``'my-dataset/year=2024/'``).
            column_expressions: Per-target-column projection overrides.  Each
                key is the target column name; the value is a
                :class:`CatalogColumnExpression` that emits
                ``<function>(<column>) AS <key>`` in the generated
                ``CREATE PIPE … AS INSERT`` SELECT list.  Required for
                AGGREGATE-KEY tables that include native HLL or BITMAP columns.
            column_overrides: Override inferred column types, e.g.
                ``{"year": "INT", "event_date": "DATE"}``.
            aggregation_overrides: Maps non-key column names to their StarRocks
                aggregation function (``SUM``, ``MIN``, ``MAX``, ``REPLACE``,
                ``HLL_UNION``, ``BITMAP_UNION``, …).  Required for every
                non-key column when ``key_config`` type is ``'aggregate'``.
            max_varchar_length: Cap VARCHAR(N) columns to this length; 0 means
                no cap.
            polling_interval_seconds: How often (in seconds) the pipe polls for
                new files; 0 or ``None`` uses the server default.
            table_properties: ``CREATE TABLE PROPERTIES`` key-value pairs.
                Defaults to ``{"replication_num": "1"}`` server-side.
        """
        kwargs: dict[str, Any] = {}
        if column_expressions is not None:
            kwargs["column_expressions"] = {k: v.as_api_model() for k, v in column_expressions.items()}
        if column_overrides is not None:
            kwargs["column_overrides"] = column_overrides
        if aggregation_overrides is not None:
            kwargs["aggregation_overrides"] = aggregation_overrides
        if max_varchar_length is not None:
            kwargs["max_varchar_length"] = max_varchar_length
        if polling_interval_seconds is not None:
            kwargs["polling_interval_seconds"] = polling_interval_seconds
        if table_properties is not None:
            kwargs["table_properties"] = table_properties

        request = CreatePipeTableRequest(
            table_name=table_name,
            source_storage_name=source_storage_name,
            path_prefix=path_prefix,
            _check_type=False,
            **kwargs,
        )
        self._ai_lake_api.create_ai_lake_pipe_table(
            instance_id,
            request,
            _check_return_type=False,
        )

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

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

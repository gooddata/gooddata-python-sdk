# (C) 2026 GoodData Corporation
"""SDK wrapper for the AI Lake long-running-operation surface.

Today this exposes only the operations needed by aggregate-aware LDMs:

- `analyze_statistics` triggers `ANALYZE TABLE` over a database instance so
  CBO statistics catch up after a schema or data change. Required after
  registering a pre-aggregation table whose dim attributes the platform will
  later resolve via filter pushdown.
- `get_operation` and `wait_for_operation` cover the polling side of the
  long-running operation contract that `analyze_statistics` returns.

The full AI Lake API surface (database provisioning, pipe-table
registration, service commands) is not yet wrapped here; consumers that
need those should call `client.ai_lake_api.<method>` directly until a
ticket adds typed wrappers.
"""

from __future__ import annotations

import json
import time
import uuid
from typing import Any, Literal

import requests
from attrs import define
from gooddata_api_client.api.ai_lake_api import AILakeApi
from gooddata_api_client.model.analyze_statistics_request import AnalyzeStatisticsRequest

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

    def refresh_partition(
        self,
        instance_id: str,
        table_name: str,
        partition_spec: dict[str, str],
        operation_id: str | None = None,
    ) -> str:
        """(BETA) Delete all rows for the specified Hive partition and re-load from S3.

        Triggers a ``refresh-partition`` long-running operation in the AI Lake.
        The generated client does not yet expose this endpoint, so the SDK calls
        it via a raw HTTP POST using the same URL-construction logic as
        :meth:`~gooddata_sdk.client.GoodDataApiClient._do_post_request`.

        Args:
            instance_id: Database instance name (preferred) or UUID.
            table_name: Name of the pipe-backed OLAP table.
            partition_spec: Partition column values that identify the partition to
                refresh (e.g. ``{"year": "2024", "month": "01"}``).
            operation_id: Optional client-supplied operation identifier.  If
                omitted, a fresh UUID is generated.  Pass the same value to
                :meth:`wait_for_operation` to poll.

        Returns:
            The operation ID (UUID string) the platform will track this run
            under.  Pass it to :meth:`get_operation` / :meth:`wait_for_operation`.
        """
        op_id = operation_id or str(uuid.uuid4())
        endpoint = f"api/v1/ailake/database/instances/{instance_id}/pipeTables/{table_name}/refresh"
        hostname = self._client._hostname
        if not hostname.endswith("/"):
            endpoint = f"/{endpoint}"
        url = f"{hostname}{endpoint}"
        body = json.dumps({"partitionSpec": partition_spec}).encode("utf-8")
        response = requests.post(
            url=url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._client._token}",
                "operation-id": op_id,
            },
            data=body,
        )
        response.raise_for_status()
        return op_id

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

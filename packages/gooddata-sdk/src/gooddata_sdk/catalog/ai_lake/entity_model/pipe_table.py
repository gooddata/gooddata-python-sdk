# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any

import attrs
from gooddata_api_client.model.create_pipe_table_request import CreatePipeTableRequest


@attrs.define(kw_only=True)
class CatalogPipeTableSummary:
    """Summary of an AI Lake pipe table as returned by the list endpoint."""

    pipe_table_id: str
    table_name: str
    path_prefix: str
    columns: list[dict[str, Any]] = attrs.field(factory=list)

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogPipeTableSummary:
        return cls(
            pipe_table_id=entity["pipe_table_id"],
            table_name=entity["table_name"],
            path_prefix=entity["path_prefix"],
            columns=entity.get("columns") or [],
        )


@attrs.define(kw_only=True)
class CatalogPipeTable:
    """Full representation of an AI Lake pipe table."""

    pipe_table_id: str
    table_name: str
    source_storage_name: str
    path_prefix: str
    database_name: str
    polling_interval_seconds: int
    partition_columns: list[str] = attrs.field(factory=list)
    table_properties: dict[str, str] = attrs.field(factory=dict)
    columns: list[dict[str, Any]] = attrs.field(factory=list)

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogPipeTable:
        return cls(
            pipe_table_id=entity["pipe_table_id"],
            table_name=entity["table_name"],
            source_storage_name=entity["source_storage_name"],
            path_prefix=entity["path_prefix"],
            database_name=entity["database_name"],
            polling_interval_seconds=entity["polling_interval_seconds"],
            partition_columns=entity.get("partition_columns") or [],
            table_properties=entity.get("table_properties") or {},
            columns=entity.get("columns") or [],
        )


@attrs.define(kw_only=True)
class CatalogCreatePipeTableRequest:
    """Request to create a new AI Lake pipe table."""

    path_prefix: str
    source_storage_name: str
    table_name: str
    column_overrides: dict[str, str] | None = None
    max_varchar_length: int | None = None
    polling_interval_seconds: int | None = None
    table_properties: dict[str, str] | None = None

    def as_api_model(self) -> CreatePipeTableRequest:
        kwargs: dict[str, Any] = {}
        if self.column_overrides is not None:
            kwargs["column_overrides"] = self.column_overrides
        if self.max_varchar_length is not None:
            kwargs["max_varchar_length"] = self.max_varchar_length
        if self.polling_interval_seconds is not None:
            kwargs["polling_interval_seconds"] = self.polling_interval_seconds
        if self.table_properties is not None:
            kwargs["table_properties"] = self.table_properties
        return CreatePipeTableRequest(
            path_prefix=self.path_prefix,
            source_storage_name=self.source_storage_name,
            table_name=self.table_name,
            _check_type=False,
            **kwargs,
        )

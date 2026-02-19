# (C) 2025 GoodData Corporation
from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Set

from attr import define
from gooddata_api_client.model.provision_database_instance_request import ProvisionDatabaseInstanceRequest

# TypeAlias for OperationKind values matching the API's allowed_values
OperationKind = Literal["provision-database", "deprovision-database"]


@define(kw_only=True)
class CatalogOperationError:
    title: str
    status: int
    detail: str

    @classmethod
    def from_api(cls, api_obj: Any) -> "CatalogOperationError":
        return cls(
            title=api_obj.title,
            status=api_obj.status,
            detail=api_obj.detail,
        )


@define(kw_only=True)
class CatalogOperation:
    id: str
    kind: str
    status: str


@define(kw_only=True)
class CatalogPendingOperation(CatalogOperation):
    status: str = "pending"

    @classmethod
    def from_api(cls, api_obj: Any) -> "CatalogPendingOperation":
        return cls(
            id=api_obj.id,
            kind=api_obj.kind,
            status="pending",
        )


@define(kw_only=True)
class CatalogSucceededOperation(CatalogOperation):
    status: str = "succeeded"
    result: Optional[Dict[str, Any]] = None

    @classmethod
    def from_api(cls, api_obj: Any) -> "CatalogSucceededOperation":
        result = None
        if hasattr(api_obj, "result"):
            result = api_obj.result
        return cls(
            id=api_obj.id,
            kind=api_obj.kind,
            status="succeeded",
            result=result,
        )


@define(kw_only=True)
class CatalogFailedOperation(CatalogOperation):
    status: str = "failed"
    error: CatalogOperationError = None  # type: ignore[assignment]

    @classmethod
    def from_api(cls, api_obj: Any) -> "CatalogFailedOperation":
        return cls(
            id=api_obj.id,
            kind=api_obj.kind,
            status="failed",
            error=CatalogOperationError.from_api(api_obj.error),
        )


@define(kw_only=True)
class CatalogProvisionDatabaseInstanceRequest:
    name: str
    storage_ids: Set[str]

    def as_api_model(self) -> ProvisionDatabaseInstanceRequest:
        return ProvisionDatabaseInstanceRequest(
            name=self.name,
            storage_ids=list(self.storage_ids),
        )


@define(kw_only=True)
class CatalogDatabaseInstance:
    id: str
    name: str
    storage_ids: List[str]

    @classmethod
    def from_api(cls, api_obj: Any) -> "CatalogDatabaseInstance":
        return cls(
            id=api_obj.id,
            name=api_obj.name,
            storage_ids=list(api_obj.storage_ids),
        )

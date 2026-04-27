# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any

import attrs
from gooddata_api_client.model.provision_database_instance_request import ProvisionDatabaseInstanceRequest


@attrs.define(kw_only=True)
class CatalogDatabaseInstance:
    """Represents an AI Lake database instance."""

    id: str
    name: str
    storage_ids: list[str] = attrs.field(factory=list)

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDatabaseInstance:
        return cls(
            id=entity["id"],
            name=entity["name"],
            storage_ids=entity.get("storage_ids") or [],
        )


@attrs.define(kw_only=True)
class CatalogProvisionDatabaseInstanceRequest:
    """Request to provision a new AI Lake database instance."""

    name: str
    storage_ids: list[str] = attrs.field(factory=list)

    def as_api_model(self) -> ProvisionDatabaseInstanceRequest:
        return ProvisionDatabaseInstanceRequest(
            name=self.name,
            storage_ids=self.storage_ids,
            _check_type=False,
        )

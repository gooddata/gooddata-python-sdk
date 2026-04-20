# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any

import attrs


@attrs.define(kw_only=True)
class CatalogServiceInfo:
    """Information about an AI Lake service."""

    name: str
    service_id: str

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogServiceInfo:
        return cls(
            name=entity["name"],
            service_id=entity["service_id"],
        )

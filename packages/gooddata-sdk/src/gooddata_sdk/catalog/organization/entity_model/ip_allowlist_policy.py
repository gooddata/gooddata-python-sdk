# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any

import attrs


@attrs.define(kw_only=True)
class CatalogIpAllowlistPolicyAttributes:
    """Attributes of an IP allowlist policy."""

    allowed_sources: list[str] = attrs.field(factory=list)

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogIpAllowlistPolicyAttributes:
        raw = entity.get("allowedSources")
        return cls(
            allowed_sources=list(raw) if raw is not None else [],
        )

    def to_api(self) -> dict[str, Any]:
        return {"allowedSources": self.allowed_sources}


@attrs.define(kw_only=True)
class CatalogIpAllowlistPolicy:
    """Represents an IP allowlist policy entity."""

    id: str
    attributes: CatalogIpAllowlistPolicyAttributes | None = None

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogIpAllowlistPolicy:
        """Parse from a JSON:API entity data dict (the ``data`` key of a response).

        Args:
            entity: The ``data`` portion of a JSON:API document, e.g.
                ``{"id": "...", "type": "ipAllowlistPolicy", "attributes": {...}}``.

        Returns:
            CatalogIpAllowlistPolicy: The parsed entity.
        """
        raw_attrs = entity.get("attributes")
        return cls(
            id=entity["id"],
            attributes=CatalogIpAllowlistPolicyAttributes.from_api(raw_attrs) if raw_attrs is not None else None,
        )

    def to_api(self) -> dict[str, Any]:
        """Serialise to a JSON:API request document.

        Returns:
            dict: A JSON:API document suitable for POST/PUT request bodies.
        """
        attrs_dict: dict[str, Any] = {}
        if self.attributes is not None:
            attrs_dict = self.attributes.to_api()
        return {
            "data": {
                "id": self.id,
                "type": "ipAllowlistPolicy",
                "attributes": attrs_dict,
            }
        }

# (C) 2026 GoodData Corporation
from __future__ import annotations

import json
from typing import Any

import attrs
from attrs import define

from gooddata_sdk.catalog.base import Base


@define(kw_only=True)
class CatalogIpAllowlistPolicy(Base):
    """Represents an IP allowlist policy entity."""

    id: str
    allowed_sources: list[str] = attrs.field(factory=list)
    users: list[str] = attrs.field(factory=list)
    user_groups: list[str] = attrs.field(factory=list)

    @staticmethod
    def client_class() -> type:
        return NotImplemented  # type: ignore[return-value]

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogIpAllowlistPolicy:
        attrs_raw = entity.get("attributes") or {}
        users_raw = attrs_raw.get("users") or []
        user_groups_raw = attrs_raw.get("userGroups") or []
        return cls(
            id=entity["id"],
            allowed_sources=attrs_raw.get("allowedSources") or [],
            users=[u["id"] if isinstance(u, dict) else u for u in users_raw],
            user_groups=[g["id"] if isinstance(g, dict) else g for g in user_groups_raw],
        )

    def to_api_dict(self) -> dict[str, Any]:
        """Serialize to JSON API document dict for POST/PUT requests."""
        attributes: dict[str, Any] = {
            "allowedSources": self.allowed_sources,
        }
        if self.users:
            attributes["users"] = [{"id": uid, "type": "user"} for uid in self.users]
        if self.user_groups:
            attributes["userGroups"] = [{"id": gid, "type": "userGroup"} for gid in self.user_groups]
        return {
            "data": {
                "id": self.id,
                "type": "ipAllowlistPolicy",
                "attributes": attributes,
            }
        }

    def to_api_json_bytes(self) -> bytes:
        """Serialize to JSON bytes for HTTP request body."""
        return json.dumps(self.to_api_dict()).encode("utf-8")

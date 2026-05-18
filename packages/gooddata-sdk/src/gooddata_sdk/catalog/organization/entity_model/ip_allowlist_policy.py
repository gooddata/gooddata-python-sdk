# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any

import attrs

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.identifier import CatalogAssigneeIdentifier


@attrs.define(kw_only=True)
class CatalogIpAllowlistPolicy(Base):
    """Represents an IP allowlist policy entity.

    Attributes:
        id: Unique identifier for the policy.
        allowed_sources: IP addresses or CIDR ranges that are allowed by this policy.
        users: Users this policy applies to.
        user_groups: User groups this policy applies to.
    """

    id: str
    allowed_sources: list[str] = attrs.field(factory=list)
    users: list[CatalogAssigneeIdentifier] = attrs.field(factory=list)
    user_groups: list[CatalogAssigneeIdentifier] = attrs.field(factory=list)

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogIpAllowlistPolicy:
        attrs_data = entity.get("attributes") or {}
        relationships = entity.get("relationships") or {}
        users_rel = (relationships.get("users") or {}).get("data") or []
        groups_rel = (relationships.get("userGroups") or {}).get("data") or []
        return cls(
            id=entity["id"],
            allowed_sources=list(attrs_data.get("allowedSources") or []),
            users=[CatalogAssigneeIdentifier(id=u["id"], type=u["type"]) for u in users_rel],
            user_groups=[CatalogAssigneeIdentifier(id=g["id"], type=g["type"]) for g in groups_rel],
        )


@attrs.define(kw_only=True)
class CatalogIpAllowlistPolicyTargets(Base):
    """Target payload for ``addTargets`` / ``removeTargets`` action endpoints.

    Attributes:
        targets: List of assignee identifiers (users or user-groups) to add or remove.
    """

    targets: list[CatalogAssigneeIdentifier] = attrs.field(factory=list)

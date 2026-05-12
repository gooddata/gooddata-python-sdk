# (C) 2025 GoodData Corporation
from __future__ import annotations

import builtins

from attrs import define, field
from gooddata_api_client.model.declarative_ip_allowlist_policy import DeclarativeIpAllowlistPolicy

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.identifier import CatalogDeclarativeUserGroupIdentifier, CatalogUserIdentifier


@define(kw_only=True)
class CatalogDeclarativeIpAllowlistPolicy(Base):
    id: str
    allowed_sources: list[str] = field(factory=list)
    user_groups: list[CatalogDeclarativeUserGroupIdentifier] = field(factory=list)
    users: list[CatalogUserIdentifier] = field(factory=list)

    @staticmethod
    def client_class() -> builtins.type[DeclarativeIpAllowlistPolicy]:
        return DeclarativeIpAllowlistPolicy

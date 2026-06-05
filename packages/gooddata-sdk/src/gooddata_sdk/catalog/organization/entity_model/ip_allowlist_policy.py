# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any

from attrs import define, field
from gooddata_api_client.model.assignee_identifier import AssigneeIdentifier
from gooddata_api_client.model.ip_allowlist_policy_targets import IpAllowlistPolicyTargets
from gooddata_api_client.model.json_api_agent_in_relationships_user_groups import JsonApiAgentInRelationshipsUserGroups
from gooddata_api_client.model.json_api_automation_in_relationships_recipients import (
    JsonApiAutomationInRelationshipsRecipients,
)
from gooddata_api_client.model.json_api_ip_allowlist_policy_in import JsonApiIpAllowlistPolicyIn
from gooddata_api_client.model.json_api_ip_allowlist_policy_in_attributes import JsonApiIpAllowlistPolicyInAttributes
from gooddata_api_client.model.json_api_ip_allowlist_policy_in_document import JsonApiIpAllowlistPolicyInDocument
from gooddata_api_client.model.json_api_ip_allowlist_policy_in_relationships import (
    JsonApiIpAllowlistPolicyInRelationships,
)
from gooddata_api_client.model.json_api_user_group_linkage import JsonApiUserGroupLinkage
from gooddata_api_client.model.json_api_user_group_to_many_linkage import JsonApiUserGroupToManyLinkage
from gooddata_api_client.model.json_api_user_linkage import JsonApiUserLinkage
from gooddata_api_client.model.json_api_user_to_many_linkage import JsonApiUserToManyLinkage

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.identifier import CatalogAssigneeIdentifier

_POLICY_TYPE = "ipAllowlistPolicy"


@define(kw_only=True)
class CatalogIpAllowlistPolicy(Base):
    """Represents an IP allowlist policy entity."""

    id: str
    allowed_sources: list[str] = field(factory=list)
    users: list[CatalogAssigneeIdentifier] = field(factory=list)
    user_groups: list[CatalogAssigneeIdentifier] = field(factory=list)

    @staticmethod
    def client_class() -> type[JsonApiIpAllowlistPolicyIn]:
        return JsonApiIpAllowlistPolicyIn

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogIpAllowlistPolicy:
        attributes = entity.get("attributes") or {}
        relationships = entity.get("relationships") or {}
        users = (relationships.get("users") or {}).get("data") or []
        user_groups = (relationships.get("userGroups") or {}).get("data") or []
        return cls(
            id=entity["id"],
            allowed_sources=list(attributes.get("allowedSources") or []),
            users=[CatalogAssigneeIdentifier(id=user["id"], type=user["type"]) for user in users],
            user_groups=[CatalogAssigneeIdentifier(id=group["id"], type=group["type"]) for group in user_groups],
        )

    def to_api(self) -> JsonApiIpAllowlistPolicyInDocument:
        relationships: dict[str, Any] = {}
        if self.users:
            relationships["users"] = JsonApiAutomationInRelationshipsRecipients(
                data=JsonApiUserToManyLinkage([JsonApiUserLinkage(id=user.id, type=user.type) for user in self.users])
            )
        if self.user_groups:
            relationships["user_groups"] = JsonApiAgentInRelationshipsUserGroups(
                data=JsonApiUserGroupToManyLinkage(
                    [JsonApiUserGroupLinkage(id=group.id, type=group.type) for group in self.user_groups]
                )
            )
        data_kwargs: dict[str, Any] = {
            "id": self.id,
            "type": _POLICY_TYPE,
            "attributes": JsonApiIpAllowlistPolicyInAttributes(allowed_sources=self.allowed_sources),
        }
        if relationships:
            data_kwargs["relationships"] = JsonApiIpAllowlistPolicyInRelationships(**relationships)
        return JsonApiIpAllowlistPolicyInDocument(data=JsonApiIpAllowlistPolicyIn(**data_kwargs))


@define(kw_only=True)
class CatalogIpAllowlistPolicyTargets(Base):
    """Target payload for IP allowlist policy add/remove target actions."""

    targets: list[CatalogAssigneeIdentifier] = field(factory=list)

    @staticmethod
    def client_class() -> type[IpAllowlistPolicyTargets]:
        return IpAllowlistPolicyTargets

    def to_api(self) -> IpAllowlistPolicyTargets:
        return IpAllowlistPolicyTargets(
            targets=[AssigneeIdentifier(id=target.id, type=target.type) for target in self.targets]
        )

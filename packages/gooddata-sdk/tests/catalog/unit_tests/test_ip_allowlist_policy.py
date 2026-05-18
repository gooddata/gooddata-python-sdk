# (C) 2026 GoodData Corporation
"""Unit tests for CatalogIpAllowlistPolicy deserialization.

The from_api classmethod has custom None-guard logic and nested relationship
parsing that warrants direct testing.
"""

from __future__ import annotations

import pytest
from gooddata_sdk.catalog.identifier import CatalogAssigneeIdentifier
from gooddata_sdk.catalog.organization.entity_model.ip_allowlist_policy import CatalogIpAllowlistPolicy


@pytest.mark.parametrize(
    "scenario, entity, expected_sources, expected_users, expected_groups",
    [
        (
            "minimal — no relationships, no attributes",
            {"id": "pol1", "type": "ipAllowlistPolicy"},
            [],
            [],
            [],
        ),
        (
            "with allowed_sources",
            {
                "id": "pol2",
                "type": "ipAllowlistPolicy",
                "attributes": {"allowedSources": ["10.0.0.0/8", "192.168.1.0/24"]},
            },
            ["10.0.0.0/8", "192.168.1.0/24"],
            [],
            [],
        ),
        (
            "with users and user_groups relationships",
            {
                "id": "pol3",
                "type": "ipAllowlistPolicy",
                "attributes": {"allowedSources": ["172.16.0.0/12"]},
                "relationships": {
                    "users": {"data": [{"id": "alice", "type": "user"}]},
                    "userGroups": {"data": [{"id": "admins", "type": "userGroup"}]},
                },
            },
            ["172.16.0.0/12"],
            [CatalogAssigneeIdentifier(id="alice", type="user")],
            [CatalogAssigneeIdentifier(id="admins", type="userGroup")],
        ),
        (
            "null attributes and relationships are safe",
            {
                "id": "pol4",
                "type": "ipAllowlistPolicy",
                "attributes": None,
                "relationships": None,
            },
            [],
            [],
            [],
        ),
    ],
)
def test_ip_allowlist_policy_from_api(
    scenario: str,
    entity: dict,
    expected_sources: list[str],
    expected_users: list[CatalogAssigneeIdentifier],
    expected_groups: list[CatalogAssigneeIdentifier],
) -> None:
    policy = CatalogIpAllowlistPolicy.from_api(entity)
    assert policy.id == entity["id"], scenario
    assert policy.allowed_sources == expected_sources, scenario
    assert policy.users == expected_users, scenario
    assert policy.user_groups == expected_groups, scenario

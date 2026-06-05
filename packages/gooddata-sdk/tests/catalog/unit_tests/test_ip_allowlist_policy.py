# (C) 2026 GoodData Corporation
from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

from gooddata_sdk.catalog.identifier import CatalogAssigneeIdentifier
from gooddata_sdk.catalog.organization.entity_model.ip_allowlist_policy import (
    CatalogIpAllowlistPolicy,
    CatalogIpAllowlistPolicyTargets,
)
from gooddata_sdk.catalog.organization.service import CatalogOrganizationService


def _make_service() -> tuple[CatalogOrganizationService, MagicMock, MagicMock]:
    """Build a service whose entities-api and actions-api sides are fully mocked."""
    fake_entities_api = MagicMock(name="EntitiesApi")
    fake_actions_api = MagicMock(name="ActionsApi")
    fake_client = SimpleNamespace(
        entities_api=fake_entities_api,
        layout_api=MagicMock(name="LayoutApi"),
        actions_api=fake_actions_api,
        user_management_api=MagicMock(name="UserManagementApi"),
    )
    service = CatalogOrganizationService(fake_client)  # type: ignore[arg-type]
    return service, fake_entities_api, fake_actions_api


def test_ip_allowlist_policy_from_api_reads_attributes_and_relationships() -> None:
    policy = CatalogIpAllowlistPolicy.from_api(
        {
            "id": "corp-vpn-only",
            "type": "ipAllowlistPolicy",
            "attributes": {"allowedSources": ["203.0.113.10/32", "198.51.100.0/24"]},
            "relationships": {
                "users": {"data": [{"id": "admin", "type": "user"}]},
                "userGroups": {"data": [{"id": "admins", "type": "userGroup"}]},
            },
        }
    )

    assert policy.id == "corp-vpn-only"
    assert policy.allowed_sources == ["203.0.113.10/32", "198.51.100.0/24"]
    assert policy.users == [CatalogAssigneeIdentifier(id="admin", type="user")]
    assert policy.user_groups == [CatalogAssigneeIdentifier(id="admins", type="userGroup")]


def test_ip_allowlist_policy_from_api_defaults_missing_optional_fields() -> None:
    policy = CatalogIpAllowlistPolicy.from_api({"id": "corp-vpn-only", "type": "ipAllowlistPolicy"})

    assert policy.id == "corp-vpn-only"
    assert policy.allowed_sources == []
    assert policy.users == []
    assert policy.user_groups == []


def test_ip_allowlist_policy_to_api_uses_json_api_shape() -> None:
    policy = CatalogIpAllowlistPolicy(
        id="corp-vpn-only",
        allowed_sources=["203.0.113.10/32"],
        users=[CatalogAssigneeIdentifier(id="admin", type="user")],
        user_groups=[CatalogAssigneeIdentifier(id="admins", type="userGroup")],
    )

    document = policy.to_api()
    data = document.data

    assert data.id == "corp-vpn-only"
    assert data.type == "ipAllowlistPolicy"
    assert data.attributes.allowed_sources == ["203.0.113.10/32"]
    users = data.relationships.users.data.value
    assert [(user.id, user.type) for user in users] == [("admin", "user")]
    user_groups = data.relationships.user_groups.data.value
    assert [(group.id, group.type) for group in user_groups] == [("admins", "userGroup")]


def test_ip_allowlist_policy_to_api_omits_empty_relationships() -> None:
    policy = CatalogIpAllowlistPolicy(id="corp-vpn-only", allowed_sources=["203.0.113.10/32"])

    document = policy.to_api()

    assert document.data.attributes.allowed_sources == ["203.0.113.10/32"]
    assert "relationships" not in document.data


def test_ip_allowlist_targets_to_api_uses_action_payload_shape() -> None:
    targets = CatalogIpAllowlistPolicyTargets(
        targets=[
            CatalogAssigneeIdentifier(id="admin", type="user"),
            CatalogAssigneeIdentifier(id="admins", type="userGroup"),
        ]
    )

    payload = targets.to_api()

    assert [(target.id, target.type) for target in payload.targets] == [
        ("admin", "user"),
        ("admins", "userGroup"),
    ]


def test_ip_allowlist_policy_crud_methods_call_generated_client() -> None:
    service, entities_api, _ = _make_service()
    policy_out = SimpleNamespace(
        data={
            "id": "corp-vpn-only",
            "type": "ipAllowlistPolicy",
            "attributes": {"allowedSources": ["203.0.113.10/32"]},
        }
    )
    entities_api.get_entity_ip_allowlist_policies.return_value = policy_out
    entities_api.create_entity_ip_allowlist_policies.return_value = policy_out
    entities_api.update_entity_ip_allowlist_policies.return_value = policy_out

    policy = CatalogIpAllowlistPolicy(id="corp-vpn-only", allowed_sources=["203.0.113.10/32"])

    assert service.get_ip_allowlist_policy("corp-vpn-only").id == "corp-vpn-only"
    assert service.create_ip_allowlist_policy(policy).allowed_sources == ["203.0.113.10/32"]
    assert service.update_ip_allowlist_policy(policy).id == "corp-vpn-only"
    service.delete_ip_allowlist_policy("corp-vpn-only")

    assert entities_api.get_entity_ip_allowlist_policies.call_args.args[0] == "corp-vpn-only"
    create_doc = entities_api.create_entity_ip_allowlist_policies.call_args.kwargs[
        "json_api_ip_allowlist_policy_in_document"
    ]
    assert create_doc.data.id == "corp-vpn-only"
    assert entities_api.update_entity_ip_allowlist_policies.call_args.args[0] == "corp-vpn-only"
    assert entities_api.delete_entity_ip_allowlist_policies.call_args.args[0] == "corp-vpn-only"


def test_list_ip_allowlist_policies_loads_all_entities() -> None:
    service, entities_api, _ = _make_service()
    entities_api.get_all_entities_ip_allowlist_policies.return_value = SimpleNamespace(
        data=[
            {"id": "first", "type": "ipAllowlistPolicy"},
            {"id": "second", "type": "ipAllowlistPolicy"},
        ],
        included=[],
        links=SimpleNamespace(next=None),
    )

    policies = service.list_ip_allowlist_policies()

    assert [policy.id for policy in policies] == ["first", "second"]
    assert entities_api.get_all_entities_ip_allowlist_policies.called


def test_ip_allowlist_target_actions_call_generated_client() -> None:
    service, _, actions_api = _make_service()
    targets = CatalogIpAllowlistPolicyTargets(targets=[CatalogAssigneeIdentifier(id="admin", type="user")])

    service.add_targets_to_ip_allowlist_policy("corp-vpn-only", targets)
    service.remove_targets_from_ip_allowlist_policy("corp-vpn-only", targets)

    add_targets = actions_api.add_targets.call_args.args[1].targets
    assert actions_api.add_targets.call_args.args[0] == "corp-vpn-only"
    assert [(target.id, target.type) for target in add_targets] == [("admin", "user")]
    remove_targets = actions_api.remove_targets.call_args.args[1].targets
    assert actions_api.remove_targets.call_args.args[0] == "corp-vpn-only"
    assert [(target.id, target.type) for target in remove_targets] == [("admin", "user")]

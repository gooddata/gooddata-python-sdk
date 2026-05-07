# (C) 2026 GoodData Corporation
"""Unit tests for the `set_hll_type` / `get_hll_type` org-setting helpers.

These exercise the typed wrappers around the generic
`CatalogOrganizationService.{create,update,get}_organization_setting`
machinery; they don't need a live stack because the helpers' interesting
logic is the create-or-update fallback and the JSON shape sent to the
api-client.
"""

from __future__ import annotations

import typing
from types import SimpleNamespace
from unittest.mock import MagicMock

from gooddata_api_client.exceptions import NotFoundException
from gooddata_sdk import HLLType
from gooddata_sdk.catalog.organization.service import (
    HLL_TYPE_SETTING_ID,
    HLL_TYPE_SETTING_TYPE,
    CatalogOrganizationService,
)


def _make_service() -> tuple[CatalogOrganizationService, MagicMock]:
    """Build a service whose entities-api side is fully mocked."""
    fake_entities_api = MagicMock(name="EntitiesApi")
    fake_client = SimpleNamespace(
        entities_api=fake_entities_api,
        layout_api=MagicMock(name="LayoutApi"),
        actions_api=MagicMock(name="ActionsApi"),
        user_management_api=MagicMock(name="UserManagementApi"),
    )
    service = CatalogOrganizationService(fake_client)  # type: ignore[arg-type]
    return service, fake_entities_api


def _captured_setting_payload(api: MagicMock, mock_call: MagicMock) -> dict:
    """Pull out the `attributes` dict the SDK posted to the api-client."""
    document = (
        mock_call.call_args.kwargs.get("json_api_organization_setting_in_document") or mock_call.call_args.args[-1]
    )
    data = document.data
    return {
        "id": data.id,
        "type": data.attributes.type,
        "content": dict(data.attributes.content),
    }


class TestSetHllType:
    def test_updates_existing_setting_when_present(self) -> None:
        service, api = _make_service()
        # update succeeds → no fallback to create
        service.set_hll_type("Presto")
        assert api.update_entity_organization_settings.call_count == 1
        assert api.create_entity_organization_settings.call_count == 0
        sent_id = api.update_entity_organization_settings.call_args.args[0]
        assert sent_id == HLL_TYPE_SETTING_ID
        sent = _captured_setting_payload(api, api.update_entity_organization_settings)
        assert sent["id"] == HLL_TYPE_SETTING_ID
        assert sent["type"] == HLL_TYPE_SETTING_TYPE
        assert sent["content"] == {"value": "Presto"}

    def test_creates_setting_when_missing(self) -> None:
        service, api = _make_service()
        api.update_entity_organization_settings.side_effect = NotFoundException(status=404, reason="not found")
        service.set_hll_type("Native")
        assert api.update_entity_organization_settings.call_count == 1
        assert api.create_entity_organization_settings.call_count == 1
        sent = _captured_setting_payload(api, api.create_entity_organization_settings)
        assert sent["content"] == {"value": "Native"}


class TestGetHllType:
    def test_returns_native_when_set(self) -> None:
        service, api = _make_service()
        api.get_entity_organization_settings.return_value = SimpleNamespace(
            data={
                "id": HLL_TYPE_SETTING_ID,
                "attributes": {"type": HLL_TYPE_SETTING_TYPE, "content": {"value": "Native"}},
            }
        )
        assert service.get_hll_type() == "Native"

    def test_returns_presto_when_set(self) -> None:
        service, api = _make_service()
        api.get_entity_organization_settings.return_value = SimpleNamespace(
            data={
                "id": HLL_TYPE_SETTING_ID,
                "attributes": {"type": HLL_TYPE_SETTING_TYPE, "content": {"value": "Presto"}},
            }
        )
        assert service.get_hll_type() == "Presto"

    def test_returns_none_when_absent(self) -> None:
        service, api = _make_service()
        api.get_entity_organization_settings.side_effect = NotFoundException(status=404, reason="not found")
        assert service.get_hll_type() is None

    def test_returns_none_on_unrecognized_value(self) -> None:
        service, api = _make_service()
        api.get_entity_organization_settings.return_value = SimpleNamespace(
            data={
                "id": HLL_TYPE_SETTING_ID,
                "attributes": {"type": HLL_TYPE_SETTING_TYPE, "content": {"value": "garbage"}},
            }
        )
        assert service.get_hll_type() is None


def test_hll_type_literal_is_exposed_on_public_api() -> None:
    """The `HLLType` Literal is the canonical surface consumers should annotate against."""
    assert typing.get_args(HLLType) == ("Native", "Presto")

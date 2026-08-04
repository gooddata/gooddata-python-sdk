# (C) 2026 GoodData Corporation
from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from attrs import evolve
from gooddata_api_client.exceptions import ApiTypeError, NotFoundException
from gooddata_sdk import (
    CatalogExportTemplate,
    CatalogWorkspaceSetting,
    UpsertOutcome,
)
from gooddata_sdk.catalog.organization.entity_model.export_template import CatalogExportTemplateAttributes
from gooddata_sdk.catalog.organization.service import CatalogOrganizationService
from gooddata_sdk.catalog.workspace.entity_model.filter_view import CatalogFilterView
from gooddata_sdk.catalog.workspace.entity_model.user_data_filter import CatalogUserDataFilter
from gooddata_sdk.catalog.workspace.service import CatalogWorkspaceService

# The create/update branch is decided by whether the preceding entity GET raises
# NotFoundException, so these stub that getter instead of replaying a cassette.
# They cover what no cassette covers upstream: filter views, export templates,
# and the update branch of user data filters.


def _service(cls, getter: str, *, found: bool):
    """Service whose branch-deciding getter either succeeds or raises 404."""
    service = cls(MagicMock())
    service._entities_api = MagicMock()
    setattr(service, getter, MagicMock(side_effect=None if found else NotFoundException(status=404)))
    return service


def _filter_view(filter_view_id: str | None = "fv") -> CatalogFilterView:
    # init() builds the relationships the generated model requires; it insists on
    # an id, so the id-less variant is derived from a valid instance.
    view = CatalogFilterView.init(filter_view_id="fv", content={}, title="Test filter view", user_id="demo_user")
    return evolve(view, id=filter_view_id)


def _user_data_filter(user_data_filter_id: str | None = "udf") -> CatalogUserDataFilter:
    udf = CatalogUserDataFilter.init(
        user_data_filter_id="udf",
        maql='{label/order_status} IN ("returned")',
        user_id="demo_user",
    )
    return evolve(udf, id=user_data_filter_id)


def _export_template() -> CatalogExportTemplate:
    return CatalogExportTemplate(
        id="test_template",
        attributes=CatalogExportTemplateAttributes(name="Test template"),
    )


class TestFilterViewOutcome:
    def test_created_when_absent(self):
        service = _service(CatalogWorkspaceService, "get_filter_view", found=False)
        assert service.create_or_update_filter_view("demo", _filter_view()) == UpsertOutcome.CREATED
        service._entities_api.create_entity_filter_views.assert_called_once()

    def test_updated_when_present(self):
        service = _service(CatalogWorkspaceService, "get_filter_view", found=True)
        assert service.create_or_update_filter_view("demo", _filter_view()) == UpsertOutcome.UPDATED
        service._entities_api.update_entity_filter_views.assert_called_once()
        service._entities_api.create_entity_filter_views.assert_not_called()


class TestUserDataFilterOutcome:
    def test_created_when_absent(self):
        service = _service(CatalogWorkspaceService, "get_user_data_filter", found=False)
        assert service.create_or_update_user_data_filter("demo", _user_data_filter()) == UpsertOutcome.CREATED
        service._entities_api.create_entity_user_data_filters.assert_called_once()

    def test_updated_when_present(self):
        service = _service(CatalogWorkspaceService, "get_user_data_filter", found=True)
        assert service.create_or_update_user_data_filter("demo", _user_data_filter()) == UpsertOutcome.UPDATED
        service._entities_api.update_entity_user_data_filters.assert_called_once()


class TestWorkspaceSettingOutcome:
    def test_created_when_absent(self):
        service = _service(CatalogWorkspaceService, "get_workspace_setting", found=False)
        setting = CatalogWorkspaceSetting(id="locale", setting_type="LOCALE", content={"value": "fr-FR"})
        assert service.create_or_update_workspace_setting("demo", setting) == UpsertOutcome.CREATED
        service._entities_api.create_entity_workspace_settings.assert_called_once()

    def test_updated_when_present(self):
        service = _service(CatalogWorkspaceService, "get_workspace_setting", found=True)
        setting = CatalogWorkspaceSetting(id="locale", setting_type="LOCALE", content={"value": "fr-FR"})
        assert service.create_or_update_workspace_setting("demo", setting) == UpsertOutcome.UPDATED
        service._entities_api.update_entity_workspace_settings.assert_called_once()


class TestExportTemplateOutcome:
    def test_created_when_absent(self):
        service = _service(CatalogOrganizationService, "get_export_template", found=False)
        assert service.create_or_update_export_template(_export_template()) == UpsertOutcome.CREATED
        service._entities_api.create_entity_export_templates.assert_called_once()

    def test_updated_when_present(self):
        service = _service(CatalogOrganizationService, "get_export_template", found=True)
        assert service.create_or_update_export_template(_export_template()) == UpsertOutcome.UPDATED
        service._entities_api.update_entity_export_templates.assert_called_once()
        service._entities_api.create_entity_export_templates.assert_not_called()


class TestIdLessCreateIsUnreachable:
    """The `id is None` create branches cannot currently run.

    Each one serializes through a generated model that requires a `str` id;
    passing None fails type validation before any request is made -- true of the
    `PostOptionalId` variants too, where "optional" means "omit the key", not
    "accept None". These are strict xfails so that fixing the generated client
    (or the entity models) trips them and this file gets revisited, rather than
    the outcome contract silently claiming to cover a dead path.
    """

    @pytest.mark.xfail(raises=ApiTypeError, strict=True, reason="generated client rejects a None id")
    def test_filter_view(self):
        service = _service(CatalogWorkspaceService, "get_filter_view", found=False)
        assert service.create_or_update_filter_view("demo", _filter_view(None)) == UpsertOutcome.CREATED

    @pytest.mark.xfail(raises=ApiTypeError, strict=True, reason="generated client rejects a None id")
    def test_user_data_filter(self):
        service = _service(CatalogWorkspaceService, "get_user_data_filter", found=False)
        assert service.create_or_update_user_data_filter("demo", _user_data_filter(None)) == UpsertOutcome.CREATED

    @pytest.mark.xfail(raises=ApiTypeError, strict=True, reason="generated client rejects a None id")
    def test_workspace_setting(self):
        service = _service(CatalogWorkspaceService, "get_workspace_setting", found=False)
        setting = CatalogWorkspaceSetting(setting_type="LOCALE", content={"value": "fr-FR"})
        assert service.create_or_update_workspace_setting("demo", setting) == UpsertOutcome.CREATED


@pytest.mark.parametrize("outcome", list(UpsertOutcome))
def test_outcome_is_a_plain_string(outcome):
    """The str mixin keeps the value usable in logs and comparisons on py3.10."""
    assert isinstance(outcome, str)
    assert outcome == outcome.value

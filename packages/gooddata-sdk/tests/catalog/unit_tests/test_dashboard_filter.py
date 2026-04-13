# (C) 2024 GoodData Corporation
"""Unit tests for the new dashboard filter types and related automation classes."""

from __future__ import annotations

from gooddata_sdk import (
    CatalogAutomationDashboardTabularExport,
    CatalogDashboardArbitraryAttributeFilter,
    CatalogDashboardMatchAttributeFilter,
    CatalogDashboardTabularExportRequestV2,
    CatalogDeclarativeAutomation,
)

_DISPLAY_FORM = {"identifier": {"id": "label.region", "type": "label"}}


class TestCatalogDashboardArbitraryAttributeFilter:
    def test_basic_construction(self):
        f = CatalogDashboardArbitraryAttributeFilter(
            display_form=_DISPLAY_FORM,
            negative_selection=False,
            values=["East", "West"],
        )
        assert f.display_form == _DISPLAY_FORM
        assert f.negative_selection is False
        assert f.values == ["East", "West"]
        assert f.local_identifier is None
        assert f.title is None

    def test_empty_values_default(self):
        f = CatalogDashboardArbitraryAttributeFilter(
            display_form=_DISPLAY_FORM,
            negative_selection=True,
        )
        assert f.values == []

    def test_to_dict_snake_case(self):
        f = CatalogDashboardArbitraryAttributeFilter(
            display_form=_DISPLAY_FORM,
            negative_selection=False,
            values=["v1"],
            local_identifier="loc1",
        )
        d = f.to_dict(camel_case=False)
        assert d["display_form"] == _DISPLAY_FORM
        assert d["negative_selection"] is False
        assert d["values"] == ["v1"]
        assert d["local_identifier"] == "loc1"

    def test_to_dict_camel_case(self):
        f = CatalogDashboardArbitraryAttributeFilter(
            display_form=_DISPLAY_FORM,
            negative_selection=False,
            values=["v1"],
        )
        d = f.to_dict(camel_case=True)
        # camelCase keys expected from API model serialization
        assert "displayForm" in d
        assert "negativeSelection" in d
        assert "values" in d

    def test_client_class(self):
        from gooddata_api_client.model.dashboard_arbitrary_attribute_filter_arbitrary_attribute_filter import (
            DashboardArbitraryAttributeFilterArbitraryAttributeFilter,
        )

        assert (
            CatalogDashboardArbitraryAttributeFilter.client_class()
            is DashboardArbitraryAttributeFilterArbitraryAttributeFilter
        )

    def test_dashboard_filter_override_dict(self):
        """Demonstrate building a dashboard_filters_override entry."""
        f = CatalogDashboardArbitraryAttributeFilter(
            display_form=_DISPLAY_FORM,
            negative_selection=False,
            values=["East"],
        )
        override = {"arbitrary_attribute_filter": f.to_dict(camel_case=False)}
        assert override["arbitrary_attribute_filter"]["display_form"] == _DISPLAY_FORM


class TestCatalogDashboardMatchAttributeFilter:
    def test_basic_construction(self):
        f = CatalogDashboardMatchAttributeFilter(
            display_form=_DISPLAY_FORM,
            case_sensitive=False,
            literal="test",
            negative_selection=False,
            operator="contains",
        )
        assert f.display_form == _DISPLAY_FORM
        assert f.case_sensitive is False
        assert f.literal == "test"
        assert f.negative_selection is False
        assert f.operator == "contains"

    def test_optional_fields_default_to_none(self):
        f = CatalogDashboardMatchAttributeFilter(
            display_form=_DISPLAY_FORM,
            case_sensitive=True,
            literal="prefix",
            negative_selection=False,
            operator="startsWith",
        )
        assert f.local_identifier is None
        assert f.title is None

    def test_to_dict_snake_case(self):
        f = CatalogDashboardMatchAttributeFilter(
            display_form=_DISPLAY_FORM,
            case_sensitive=False,
            literal="suffix",
            negative_selection=True,
            operator="endsWith",
        )
        d = f.to_dict(camel_case=False)
        assert d["display_form"] == _DISPLAY_FORM
        assert d["case_sensitive"] is False
        assert d["literal"] == "suffix"
        assert d["negative_selection"] is True
        assert d["operator"] == "endsWith"

    def test_client_class(self):
        from gooddata_api_client.model.dashboard_match_attribute_filter_match_attribute_filter import (
            DashboardMatchAttributeFilterMatchAttributeFilter,
        )

        assert CatalogDashboardMatchAttributeFilter.client_class() is DashboardMatchAttributeFilterMatchAttributeFilter

    def test_dashboard_filter_override_dict(self):
        """Demonstrate building a dashboard_filters_override entry."""
        f = CatalogDashboardMatchAttributeFilter(
            display_form=_DISPLAY_FORM,
            case_sensitive=False,
            literal="East",
            negative_selection=False,
            operator="contains",
        )
        override = {"match_attribute_filter": f.to_dict(camel_case=False)}
        assert override["match_attribute_filter"]["operator"] == "contains"


class TestCatalogDashboardTabularExportRequestV2:
    def test_basic_construction(self):
        req = CatalogDashboardTabularExportRequestV2(
            dashboard_id="my-dashboard",
            file_name="export",
            format="XLSX",
        )
        assert req.dashboard_id == "my-dashboard"
        assert req.file_name == "export"
        assert req.format == "XLSX"
        assert req.dashboard_filters_override is None

    def test_with_filters(self):
        req = CatalogDashboardTabularExportRequestV2(
            dashboard_id="my-dashboard",
            file_name="export",
            format="XLSX",
            dashboard_filters_override=[
                {
                    "arbitrary_attribute_filter": {
                        "display_form": _DISPLAY_FORM,
                        "negative_selection": False,
                        "values": ["East"],
                    }
                }
            ],
        )
        assert req.dashboard_filters_override is not None
        assert len(req.dashboard_filters_override) == 1

    def test_to_dict_snake_case(self):
        req = CatalogDashboardTabularExportRequestV2(
            dashboard_id="dash1",
            file_name="out",
            format="PDF",
        )
        d = req.to_dict(camel_case=False)
        assert d["dashboard_id"] == "dash1"
        assert d["file_name"] == "out"
        assert d["format"] == "PDF"
        assert "dashboard_filters_override" not in d  # None fields excluded

    def test_client_class(self):
        from gooddata_api_client.model.dashboard_tabular_export_request_v2 import DashboardTabularExportRequestV2

        assert CatalogDashboardTabularExportRequestV2.client_class() is DashboardTabularExportRequestV2


class TestCatalogAutomationDashboardTabularExport:
    def test_basic_construction(self):
        req = CatalogDashboardTabularExportRequestV2(
            dashboard_id="dash1",
            file_name="out",
            format="XLSX",
        )
        export = CatalogAutomationDashboardTabularExport(request_payload=req)
        assert export.request_payload is req

    def test_client_class(self):
        from gooddata_api_client.model.automation_dashboard_tabular_export import AutomationDashboardTabularExport

        assert CatalogAutomationDashboardTabularExport.client_class() is AutomationDashboardTabularExport


class TestCatalogDeclarativeAutomationWithDashboardExports:
    def test_dashboard_tabular_exports_field_exists(self):
        automation = CatalogDeclarativeAutomation(id="a1")
        assert automation.dashboard_tabular_exports is None

    def test_with_dashboard_tabular_exports(self):
        export = CatalogAutomationDashboardTabularExport(
            request_payload=CatalogDashboardTabularExportRequestV2(
                dashboard_id="dash1",
                file_name="out",
                format="XLSX",
            )
        )
        automation = CatalogDeclarativeAutomation(
            id="a1",
            dashboard_tabular_exports=[export],
        )
        assert automation.dashboard_tabular_exports is not None
        assert len(automation.dashboard_tabular_exports) == 1
        assert automation.dashboard_tabular_exports[0] is export

    def test_snake_dict_includes_dashboard_tabular_exports(self):
        export = CatalogAutomationDashboardTabularExport(
            request_payload=CatalogDashboardTabularExportRequestV2(
                dashboard_id="dash1",
                file_name="out",
                format="XLSX",
            )
        )
        automation = CatalogDeclarativeAutomation(
            id="a1",
            dashboard_tabular_exports=[export],
        )
        d = automation._get_snake_dict()
        assert "dashboard_tabular_exports" in d
        assert len(d["dashboard_tabular_exports"]) == 1

# (C) 2026 GoodData Corporation
"""Unit tests for CatalogUserContext and related models."""

from __future__ import annotations

import pytest
from gooddata_sdk.compute.model.user_context import (
    CatalogActiveObjectIdentification,
    CatalogDashboardContext,
    CatalogInsightWidgetDescriptor,
    CatalogObjectReference,
    CatalogObjectReferenceGroup,
    CatalogRichTextWidgetDescriptor,
    CatalogUIContext,
    CatalogUserContext,
    CatalogVisualizationSwitcherWidgetDescriptor,
)


class TestCatalogObjectReference:
    def test_as_api_model_basic(self):
        ref = CatalogObjectReference(id="metric-1", type="METRIC")
        api = ref.as_api_model()
        assert api["id"] == "metric-1"
        assert api["type"] == "METRIC"

    @pytest.mark.parametrize("ref_type", ["WIDGET", "METRIC", "ATTRIBUTE", "DASHBOARD"])
    def test_all_types(self, ref_type: str):
        ref = CatalogObjectReference(id="obj-id", type=ref_type)
        api = ref.as_api_model()
        assert api["type"] == ref_type


class TestCatalogObjectReferenceGroup:
    def test_as_api_model_without_context(self):
        group = CatalogObjectReferenceGroup(
            objects=[CatalogObjectReference(id="w1", type="WIDGET")],
        )
        api = group.as_api_model()
        assert len(api["objects"]) == 1
        assert api["objects"][0]["id"] == "w1"

    def test_as_api_model_with_context(self):
        group = CatalogObjectReferenceGroup(
            objects=[CatalogObjectReference(id="m1", type="METRIC")],
            context=CatalogObjectReference(id="db1", type="DASHBOARD"),
        )
        api = group.as_api_model()
        assert api["context"]["id"] == "db1"
        assert api["context"]["type"] == "DASHBOARD"

    def test_empty_objects(self):
        group = CatalogObjectReferenceGroup()
        api = group.as_api_model()
        assert api["objects"] == []


class TestCatalogInsightWidgetDescriptor:
    def test_as_api_model_minimal(self):
        widget = CatalogInsightWidgetDescriptor(
            title="Revenue Chart",
            widget_id="w-insight-1",
            visualization_id="viz-1",
        )
        api = widget.as_api_model()
        assert api["title"] == "Revenue Chart"
        assert api["widget_id"] == "w-insight-1"
        assert api["visualization_id"] == "viz-1"

    def test_as_api_model_with_result_id(self):
        widget = CatalogInsightWidgetDescriptor(
            title="Revenue Chart",
            widget_id="w-insight-1",
            visualization_id="viz-1",
            result_id="result-abc",
        )
        api = widget.as_api_model()
        assert api["result_id"] == "result-abc"


class TestCatalogRichTextWidgetDescriptor:
    def test_as_api_model(self):
        widget = CatalogRichTextWidgetDescriptor(title="Header", widget_id="w-rt-1")
        api = widget.as_api_model()
        assert api["title"] == "Header"
        assert api["widget_id"] == "w-rt-1"


class TestCatalogVisualizationSwitcherWidgetDescriptor:
    def test_as_api_model_minimal(self):
        widget = CatalogVisualizationSwitcherWidgetDescriptor(
            title="Switcher",
            widget_id="w-vs-1",
            active_visualization_id="viz-a",
            visualization_ids=["viz-a", "viz-b"],
        )
        api = widget.as_api_model()
        assert api["title"] == "Switcher"
        assert api["active_visualization_id"] == "viz-a"
        assert api["visualization_ids"] == ["viz-a", "viz-b"]

    def test_as_api_model_with_result_id(self):
        widget = CatalogVisualizationSwitcherWidgetDescriptor(
            title="Switcher",
            widget_id="w-vs-1",
            active_visualization_id="viz-a",
            visualization_ids=["viz-a"],
            result_id="result-xyz",
        )
        api = widget.as_api_model()
        assert api["result_id"] == "result-xyz"


class TestCatalogDashboardContext:
    def test_as_api_model_no_widgets(self):
        ctx = CatalogDashboardContext(id="db-1")
        api = ctx.as_api_model()
        assert api["id"] == "db-1"
        assert api["widgets"] == []

    def test_as_api_model_mixed_widgets(self):
        ctx = CatalogDashboardContext(
            id="db-2",
            widgets=[
                CatalogInsightWidgetDescriptor(title="Chart", widget_id="w1", visualization_id="viz-1"),
                CatalogRichTextWidgetDescriptor(title="Note", widget_id="w2"),
            ],
        )
        api = ctx.as_api_model()
        assert api["id"] == "db-2"
        assert len(api["widgets"]) == 2


class TestCatalogUIContext:
    def test_as_api_model_no_dashboard(self):
        ctx = CatalogUIContext()
        api = ctx.as_api_model()
        # dashboard key should not be present when not set
        assert "dashboard" not in api

    def test_as_api_model_with_dashboard(self):
        ctx = CatalogUIContext(
            dashboard=CatalogDashboardContext(id="db-1"),
        )
        api = ctx.as_api_model()
        assert api["dashboard"]["id"] == "db-1"


class TestCatalogUserContext:
    def test_empty_user_context(self):
        ctx = CatalogUserContext()
        api = ctx.as_api_model()
        # None of the optional fields should appear
        assert "active_object" not in api
        assert "referenced_objects" not in api
        assert "view" not in api

    def test_with_active_object(self):
        ctx = CatalogUserContext(
            active_object=CatalogActiveObjectIdentification(id="dash-1", type="dashboard", workspace_id="ws-1")
        )
        api = ctx.as_api_model()
        assert api["active_object"]["id"] == "dash-1"
        assert api["active_object"]["type"] == "dashboard"
        assert api["active_object"]["workspace_id"] == "ws-1"

    def test_with_referenced_objects(self):
        ctx = CatalogUserContext(
            referenced_objects=[
                CatalogObjectReferenceGroup(
                    objects=[CatalogObjectReference(id="m1", type="METRIC")],
                )
            ]
        )
        api = ctx.as_api_model()
        assert len(api["referenced_objects"]) == 1

    def test_with_view(self):
        ctx = CatalogUserContext(
            view=CatalogUIContext(
                dashboard=CatalogDashboardContext(id="db-1"),
            )
        )
        api = ctx.as_api_model()
        assert api["view"]["dashboard"]["id"] == "db-1"

    def test_full_context(self):
        ctx = CatalogUserContext(
            active_object=CatalogActiveObjectIdentification(id="dash-1", type="dashboard", workspace_id="ws-1"),
            referenced_objects=[
                CatalogObjectReferenceGroup(
                    objects=[
                        CatalogObjectReference(id="w1", type="WIDGET"),
                        CatalogObjectReference(id="m1", type="METRIC"),
                    ],
                    context=CatalogObjectReference(id="dash-1", type="DASHBOARD"),
                )
            ],
            view=CatalogUIContext(
                dashboard=CatalogDashboardContext(
                    id="dash-1",
                    widgets=[
                        CatalogInsightWidgetDescriptor(
                            title="Revenue",
                            widget_id="w1",
                            visualization_id="viz-rev",
                        )
                    ],
                )
            ),
        )
        api = ctx.as_api_model()
        assert api["active_object"]["id"] == "dash-1"
        assert len(api["referenced_objects"]) == 1
        assert api["referenced_objects"][0]["context"]["type"] == "DASHBOARD"
        assert api["view"]["dashboard"]["id"] == "dash-1"
        assert len(api["view"]["dashboard"]["widgets"]) == 1

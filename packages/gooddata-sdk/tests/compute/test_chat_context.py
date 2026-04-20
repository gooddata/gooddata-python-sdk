# (C) 2026 GoodData Corporation
from __future__ import annotations

from gooddata_sdk.compute.model.chat_context import (
    CatalogActiveObjectIdentification,
    CatalogDashboardContext,
    CatalogObjectReference,
    CatalogObjectReferenceGroup,
    CatalogRichTextWidgetDescriptor,
    CatalogUIContext,
    CatalogUserContext,
    CatalogWidgetDescriptor,
)


class TestCatalogObjectReference:
    def test_construction_and_to_api(self):
        obj = CatalogObjectReference(id="metric-1", type="METRIC")
        api = obj.to_api()
        assert api["id"] == "metric-1"
        assert api["type"] == "METRIC"


class TestCatalogObjectReferenceGroup:
    def test_as_api_model_with_objects(self):
        ref = CatalogObjectReference(id="widget-1", type="WIDGET")
        group = CatalogObjectReferenceGroup(objects=[ref])
        api = group.as_api_model()
        assert len(api["objects"]) == 1
        assert api["objects"][0]["id"] == "widget-1"

    def test_as_api_model_with_context(self):
        ref = CatalogObjectReference(id="attr-1", type="ATTRIBUTE")
        ctx = CatalogObjectReference(id="dashboard-1", type="DASHBOARD")
        group = CatalogObjectReferenceGroup(objects=[ref], context=ctx)
        api = group.as_api_model()
        assert api.context["id"] == "dashboard-1"

    def test_as_api_model_empty(self):
        group = CatalogObjectReferenceGroup()
        api = group.as_api_model()
        assert api["objects"] == []
        assert "context" not in api or api.get("context") is None


class TestCatalogActiveObjectIdentification:
    def test_construction_and_to_api(self):
        active = CatalogActiveObjectIdentification(
            id="dash-1", type="dashboard", workspace_id="ws-1"
        )
        api = active.to_api()
        assert api["id"] == "dash-1"
        assert api["type"] == "dashboard"
        assert api["workspace_id"] == "ws-1"


class TestCatalogWidgetDescriptor:
    def test_as_api_model_minimal(self):
        widget = CatalogWidgetDescriptor(
            title="My Widget", widget_id="w-1", widget_type="INSIGHT"
        )
        api = widget.as_api_model()
        assert api["title"] == "My Widget"
        assert api["widget_id"] == "w-1"
        assert api["widget_type"] == "INSIGHT"

    def test_as_api_model_with_filters(self):
        widget = CatalogWidgetDescriptor(
            title="My Widget",
            widget_id="w-1",
            widget_type="INSIGHT",
            filters=[{"positiveAttributeFilter": {"label": "attr.id"}}],
        )
        api = widget.as_api_model()
        assert len(api["filters"]) == 1


class TestCatalogRichTextWidgetDescriptor:
    def test_as_api_model_minimal(self):
        widget = CatalogRichTextWidgetDescriptor(title="Rich Text", widget_id="rt-1")
        api = widget.as_api_model()
        assert api["title"] == "Rich Text"
        assert api["widget_id"] == "rt-1"

    def test_as_api_model_with_filters(self):
        widget = CatalogRichTextWidgetDescriptor(
            title="Rich Text",
            widget_id="rt-1",
            filters=[{"absoluteDateFilter": {}}],
        )
        api = widget.as_api_model()
        assert len(api["filters"]) == 1


class TestCatalogDashboardContext:
    def test_as_api_model_no_widgets(self):
        ctx = CatalogDashboardContext(id="dash-1")
        api = ctx.as_api_model()
        assert api["id"] == "dash-1"
        assert api["widgets"] == []

    def test_as_api_model_with_widgets(self):
        widget = CatalogWidgetDescriptor(
            title="W1", widget_id="w-1", widget_type="INSIGHT"
        )
        ctx = CatalogDashboardContext(id="dash-1", widgets=[widget])
        api = ctx.as_api_model()
        assert len(api["widgets"]) == 1
        assert api["widgets"][0]["title"] == "W1"


class TestCatalogUIContext:
    def test_as_api_model_empty(self):
        ctx = CatalogUIContext()
        api = ctx.as_api_model()
        assert api is not None

    def test_as_api_model_with_dashboard(self):
        dashboard = CatalogDashboardContext(id="dash-1")
        ctx = CatalogUIContext(dashboard=dashboard)
        api = ctx.as_api_model()
        assert api["dashboard"]["id"] == "dash-1"


class TestCatalogUserContext:
    def test_as_api_model_empty(self):
        ctx = CatalogUserContext()
        api = ctx.as_api_model()
        assert api is not None

    def test_as_api_model_full(self):
        active = CatalogActiveObjectIdentification(
            id="dash-1", type="dashboard", workspace_id="ws-1"
        )
        ref = CatalogObjectReference(id="metric-1", type="METRIC")
        group = CatalogObjectReferenceGroup(objects=[ref])
        dashboard = CatalogDashboardContext(id="dash-1")
        view = CatalogUIContext(dashboard=dashboard)

        ctx = CatalogUserContext(
            active_object=active,
            referenced_objects=[group],
            view=view,
        )
        api = ctx.as_api_model()
        assert api["active_object"]["id"] == "dash-1"
        assert len(api["referenced_objects"]) == 1
        assert api["view"]["dashboard"]["id"] == "dash-1"

    def test_as_api_model_only_view(self):
        dashboard = CatalogDashboardContext(id="dash-1")
        view = CatalogUIContext(dashboard=dashboard)
        ctx = CatalogUserContext(view=view)
        api = ctx.as_api_model()
        assert "active_object" not in api or api.get("active_object") is None
        assert api["view"]["dashboard"]["id"] == "dash-1"

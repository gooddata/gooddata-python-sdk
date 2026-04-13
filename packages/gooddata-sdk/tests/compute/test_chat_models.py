# (C) 2024 GoodData Corporation
from __future__ import annotations

from gooddata_sdk.compute.model.chat import (
    DashboardContext,
    InsightWidgetDescriptor,
    ObjectReference,
    ObjectReferenceGroup,
    RichTextWidgetDescriptor,
    UIContext,
    UserContext,
    VisualizationSwitcherWidgetDescriptor,
)


def test_object_reference_as_api_model():
    obj_ref = ObjectReference(id="widget-1", type="WIDGET")
    api_model = obj_ref.as_api_model()
    assert api_model.id == "widget-1"
    assert api_model.type == "WIDGET"


def test_object_reference_group_as_api_model_minimal():
    obj_ref = ObjectReference(id="metric-1", type="METRIC")
    group = ObjectReferenceGroup(objects=[obj_ref])
    api_model = group.as_api_model()
    assert len(api_model.objects) == 1
    assert api_model.objects[0].id == "metric-1"
    assert not hasattr(api_model, "context") or api_model.get("context") is None


def test_object_reference_group_as_api_model_with_context():
    obj_ref = ObjectReference(id="widget-1", type="WIDGET")
    context_ref = ObjectReference(id="dashboard-1", type="DASHBOARD")
    group = ObjectReferenceGroup(objects=[obj_ref], context=context_ref)
    api_model = group.as_api_model()
    assert len(api_model.objects) == 1
    assert api_model.context.id == "dashboard-1"
    assert api_model.context.type == "DASHBOARD"


def test_insight_widget_descriptor_as_api_model_minimal():
    widget = InsightWidgetDescriptor(
        title="Revenue Chart",
        visualization_id="vis-123",
        widget_id="widget-456",
    )
    api_model = widget.as_api_model()
    assert api_model.title == "Revenue Chart"
    assert api_model.visualization_id == "vis-123"
    assert api_model.widget_id == "widget-456"


def test_insight_widget_descriptor_as_api_model_with_result_id():
    widget = InsightWidgetDescriptor(
        title="Revenue Chart",
        visualization_id="vis-123",
        widget_id="widget-456",
        result_id="result-789",
    )
    api_model = widget.as_api_model()
    assert api_model.result_id == "result-789"


def test_rich_text_widget_descriptor_as_api_model():
    widget = RichTextWidgetDescriptor(title="Notes Widget", widget_id="widget-rt-1")
    api_model = widget.as_api_model()
    assert api_model.title == "Notes Widget"
    assert api_model.widget_id == "widget-rt-1"


def test_visualization_switcher_widget_descriptor_as_api_model():
    widget = VisualizationSwitcherWidgetDescriptor(
        active_visualization_id="vis-1",
        title="Switcher Widget",
        visualization_ids=["vis-1", "vis-2", "vis-3"],
        widget_id="widget-vs-1",
    )
    api_model = widget.as_api_model()
    assert api_model.active_visualization_id == "vis-1"
    assert api_model.title == "Switcher Widget"
    assert api_model.visualization_ids == ["vis-1", "vis-2", "vis-3"]
    assert api_model.widget_id == "widget-vs-1"


def test_dashboard_context_as_api_model():
    widget = InsightWidgetDescriptor(
        title="Revenue Chart",
        visualization_id="vis-123",
        widget_id="widget-456",
    )
    dashboard = DashboardContext(id="dashboard-1", widgets=[widget])
    api_model = dashboard.as_api_model()
    assert api_model.id == "dashboard-1"
    assert len(api_model.widgets) == 1


def test_ui_context_as_api_model_empty():
    ui_ctx = UIContext()
    api_model = ui_ctx.as_api_model()
    assert api_model is not None


def test_ui_context_as_api_model_with_dashboard():
    widget = RichTextWidgetDescriptor(title="Notes", widget_id="w-1")
    dashboard = DashboardContext(id="dash-1", widgets=[widget])
    ui_ctx = UIContext(dashboard=dashboard)
    api_model = ui_ctx.as_api_model()
    assert api_model.dashboard.id == "dash-1"


def test_user_context_as_api_model_empty():
    user_ctx = UserContext()
    api_model = user_ctx.as_api_model()
    assert api_model is not None


def test_user_context_as_api_model_with_view():
    widget = InsightWidgetDescriptor(
        title="Revenue",
        visualization_id="vis-1",
        widget_id="w-1",
    )
    dashboard = DashboardContext(id="dash-1", widgets=[widget])
    ui_ctx = UIContext(dashboard=dashboard)
    user_ctx = UserContext(view=ui_ctx)
    api_model = user_ctx.as_api_model()
    assert api_model.view.dashboard.id == "dash-1"


def test_user_context_as_api_model_with_referenced_objects():
    obj_ref = ObjectReference(id="metric-1", type="METRIC")
    group = ObjectReferenceGroup(objects=[obj_ref])
    user_ctx = UserContext(referenced_objects=[group])
    api_model = user_ctx.as_api_model()
    assert len(api_model.referenced_objects) == 1
    assert api_model.referenced_objects[0].objects[0].id == "metric-1"


def test_user_context_as_api_model_full():
    insight_widget = InsightWidgetDescriptor(
        title="Revenue Chart",
        visualization_id="vis-123",
        widget_id="widget-1",
        result_id="result-abc",
    )
    dashboard = DashboardContext(id="dash-1", widgets=[insight_widget])
    ui_ctx = UIContext(dashboard=dashboard)

    context_ref = ObjectReference(id="dashboard-1", type="DASHBOARD")
    widget_ref = ObjectReference(id="widget-1", type="WIDGET")
    group = ObjectReferenceGroup(objects=[widget_ref], context=context_ref)

    user_ctx = UserContext(
        view=ui_ctx,
        referenced_objects=[group],
    )
    api_model = user_ctx.as_api_model()
    assert api_model.view.dashboard.id == "dash-1"
    assert len(api_model.referenced_objects) == 1
    assert api_model.referenced_objects[0].context.id == "dashboard-1"

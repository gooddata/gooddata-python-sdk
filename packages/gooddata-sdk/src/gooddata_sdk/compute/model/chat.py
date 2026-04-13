# (C) 2024 GoodData Corporation
from __future__ import annotations

from typing import Any, Literal, TypeAlias

import attrs
from gooddata_api_client.model.dashboard_context import DashboardContext as ApiDashboardContext
from gooddata_api_client.model.insight_widget_descriptor import InsightWidgetDescriptor as ApiInsightWidgetDescriptor
from gooddata_api_client.model.object_reference import ObjectReference as ApiObjectReference
from gooddata_api_client.model.object_reference_group import ObjectReferenceGroup as ApiObjectReferenceGroup
from gooddata_api_client.model.rich_text_widget_descriptor import (
    RichTextWidgetDescriptor as ApiRichTextWidgetDescriptor,
)
from gooddata_api_client.model.ui_context import UIContext as ApiUIContext
from gooddata_api_client.model.user_context import UserContext as ApiUserContext
from gooddata_api_client.model.visualization_switcher_widget_descriptor import (
    VisualizationSwitcherWidgetDescriptor as ApiVisualizationSwitcherWidgetDescriptor,
)

ObjectReferenceType: TypeAlias = Literal["WIDGET", "METRIC", "ATTRIBUTE", "DASHBOARD"]


@attrs.define(kw_only=True)
class ObjectReference:
    """Reference to a specific object (e.g. widget, metric, attribute, or dashboard)."""

    id: str
    type: ObjectReferenceType

    def as_api_model(self) -> ApiObjectReference:
        return ApiObjectReference(id=self.id, type=self.type, _check_type=False)


@attrs.define(kw_only=True)
class ObjectReferenceGroup:
    """Group of object references, optionally scoped by a context (e.g. a dashboard)."""

    objects: list[ObjectReference] = attrs.field(factory=list)
    context: ObjectReference | None = None

    def as_api_model(self) -> ApiObjectReferenceGroup:
        kwargs: dict[str, Any] = {}
        if self.context is not None:
            kwargs["context"] = self.context.as_api_model()
        return ApiObjectReferenceGroup(
            objects=[obj.as_api_model() for obj in self.objects],
            _check_type=False,
            **kwargs,
        )


@attrs.define(kw_only=True)
class InsightWidgetDescriptor:
    """Widget descriptor for insight (visualization) widgets on a dashboard."""

    title: str
    visualization_id: str
    widget_id: str
    filters: list[Any] = attrs.field(factory=list)
    result_id: str | None = None

    def as_api_model(self) -> ApiInsightWidgetDescriptor:
        kwargs: dict[str, Any] = {}
        if self.filters:
            kwargs["filters"] = self.filters
        if self.result_id is not None:
            kwargs["result_id"] = self.result_id
        return ApiInsightWidgetDescriptor(
            title=self.title,
            visualization_id=self.visualization_id,
            widget_id=self.widget_id,
            _check_type=False,
            **kwargs,
        )


@attrs.define(kw_only=True)
class RichTextWidgetDescriptor:
    """Widget descriptor for rich text widgets on a dashboard."""

    title: str
    widget_id: str
    filters: list[Any] = attrs.field(factory=list)

    def as_api_model(self) -> ApiRichTextWidgetDescriptor:
        kwargs: dict[str, Any] = {}
        if self.filters:
            kwargs["filters"] = self.filters
        return ApiRichTextWidgetDescriptor(
            title=self.title,
            widget_id=self.widget_id,
            _check_type=False,
            **kwargs,
        )


@attrs.define(kw_only=True)
class VisualizationSwitcherWidgetDescriptor:
    """Widget descriptor for visualization switcher widgets on a dashboard."""

    active_visualization_id: str
    title: str
    visualization_ids: list[str]
    widget_id: str
    filters: list[Any] = attrs.field(factory=list)
    result_id: str | None = None

    def as_api_model(self) -> ApiVisualizationSwitcherWidgetDescriptor:
        kwargs: dict[str, Any] = {}
        if self.filters:
            kwargs["filters"] = self.filters
        if self.result_id is not None:
            kwargs["result_id"] = self.result_id
        return ApiVisualizationSwitcherWidgetDescriptor(
            active_visualization_id=self.active_visualization_id,
            title=self.title,
            visualization_ids=self.visualization_ids,
            widget_id=self.widget_id,
            _check_type=False,
            **kwargs,
        )


WidgetDescriptor: TypeAlias = InsightWidgetDescriptor | RichTextWidgetDescriptor | VisualizationSwitcherWidgetDescriptor


@attrs.define(kw_only=True)
class DashboardContext:
    """Context describing the dashboard currently open in the UI."""

    id: str
    widgets: list[WidgetDescriptor] = attrs.field(factory=list)

    def as_api_model(self) -> ApiDashboardContext:
        return ApiDashboardContext(
            id=self.id,
            widgets=[w.as_api_model() for w in self.widgets],
            _check_type=False,
        )


@attrs.define(kw_only=True)
class UIContext:
    """Ambient UI state passed to the AI chatbot."""

    dashboard: DashboardContext | None = None

    def as_api_model(self) -> ApiUIContext:
        kwargs: dict[str, Any] = {}
        if self.dashboard is not None:
            kwargs["dashboard"] = self.dashboard.as_api_model()
        return ApiUIContext(_check_type=False, **kwargs)


@attrs.define(kw_only=True)
class UserContext:
    """User context with ambient UI state and explicitly referenced objects for the AI chatbot."""

    referenced_objects: list[ObjectReferenceGroup] = attrs.field(factory=list)
    view: UIContext | None = None

    def as_api_model(self) -> ApiUserContext:
        kwargs: dict[str, Any] = {}
        if self.referenced_objects:
            kwargs["referenced_objects"] = [obj.as_api_model() for obj in self.referenced_objects]
        if self.view is not None:
            kwargs["view"] = self.view.as_api_model()
        return ApiUserContext(_check_type=False, **kwargs)

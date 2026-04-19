# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any, Union

import attrs
from gooddata_api_client.model.active_object_identification import ActiveObjectIdentification
from gooddata_api_client.model.dashboard_context import DashboardContext
from gooddata_api_client.model.insight_widget_descriptor import InsightWidgetDescriptor
from gooddata_api_client.model.object_reference import ObjectReference
from gooddata_api_client.model.object_reference_group import ObjectReferenceGroup
from gooddata_api_client.model.rich_text_widget_descriptor import RichTextWidgetDescriptor
from gooddata_api_client.model.ui_context import UIContext
from gooddata_api_client.model.user_context import UserContext
from gooddata_api_client.model.visualization_switcher_widget_descriptor import VisualizationSwitcherWidgetDescriptor


@attrs.define(kw_only=True)
class CatalogActiveObjectIdentification:
    """Identifies the currently active object in the user's UI."""

    id: str
    type: str
    workspace_id: str

    def as_api_model(self) -> ActiveObjectIdentification:
        return ActiveObjectIdentification(
            id=self.id,
            type=self.type,
            workspace_id=self.workspace_id,
            _check_type=False,
        )


@attrs.define(kw_only=True)
class CatalogObjectReference:
    """Reference to a GoodData object (widget, metric, attribute, or dashboard)."""

    id: str
    type: str  # WIDGET, METRIC, ATTRIBUTE, DASHBOARD

    def as_api_model(self) -> ObjectReference:
        return ObjectReference(id=self.id, type=self.type, _check_type=False)


@attrs.define(kw_only=True)
class CatalogObjectReferenceGroup:
    """A group of explicitly referenced objects, optionally scoped by a context."""

    objects: list[CatalogObjectReference] = attrs.field(factory=list)
    context: CatalogObjectReference | None = None

    def as_api_model(self) -> ObjectReferenceGroup:
        kwargs: dict[str, Any] = {}
        if self.context is not None:
            kwargs["context"] = self.context.as_api_model()
        return ObjectReferenceGroup(
            objects=[o.as_api_model() for o in self.objects],
            _check_type=False,
            **kwargs,
        )


@attrs.define(kw_only=True)
class CatalogInsightWidgetDescriptor:
    """Insight widget visible on a dashboard."""

    title: str
    widget_id: str
    visualization_id: str
    result_id: str | None = None

    def as_api_model(self) -> InsightWidgetDescriptor:
        kwargs: dict[str, Any] = {}
        if self.result_id is not None:
            kwargs["result_id"] = self.result_id
        return InsightWidgetDescriptor(
            title=self.title,
            visualization_id=self.visualization_id,
            widget_id=self.widget_id,
            _check_type=False,
            **kwargs,
        )


@attrs.define(kw_only=True)
class CatalogRichTextWidgetDescriptor:
    """Rich text widget visible on a dashboard."""

    title: str
    widget_id: str

    def as_api_model(self) -> RichTextWidgetDescriptor:
        return RichTextWidgetDescriptor(title=self.title, widget_id=self.widget_id, _check_type=False)


@attrs.define(kw_only=True)
class CatalogVisualizationSwitcherWidgetDescriptor:
    """Visualization switcher widget visible on a dashboard."""

    title: str
    widget_id: str
    active_visualization_id: str
    visualization_ids: list[str] = attrs.field(factory=list)
    result_id: str | None = None

    def as_api_model(self) -> VisualizationSwitcherWidgetDescriptor:
        kwargs: dict[str, Any] = {}
        if self.result_id is not None:
            kwargs["result_id"] = self.result_id
        return VisualizationSwitcherWidgetDescriptor(
            active_visualization_id=self.active_visualization_id,
            title=self.title,
            visualization_ids=self.visualization_ids,
            widget_id=self.widget_id,
            _check_type=False,
            **kwargs,
        )


# Union of all concrete widget descriptor types.
CatalogWidgetDescriptor = Union[
    CatalogInsightWidgetDescriptor,
    CatalogRichTextWidgetDescriptor,
    CatalogVisualizationSwitcherWidgetDescriptor,
]


@attrs.define(kw_only=True)
class CatalogDashboardContext:
    """Dashboard the user is currently viewing."""

    id: str
    widgets: list[CatalogWidgetDescriptor] = attrs.field(factory=list)

    def as_api_model(self) -> DashboardContext:
        return DashboardContext(
            id=self.id,
            widgets=[w.as_api_model() for w in self.widgets],
            _check_type=False,
        )


@attrs.define(kw_only=True)
class CatalogUIContext:
    """Ambient UI state describing what the user currently sees."""

    dashboard: CatalogDashboardContext | None = None

    def as_api_model(self) -> UIContext:
        kwargs: dict[str, Any] = {}
        if self.dashboard is not None:
            kwargs["dashboard"] = self.dashboard.as_api_model()
        return UIContext(_check_type=False, **kwargs)


@attrs.define(kw_only=True)
class CatalogUserContext:
    """User context that can influence AI feature behavior.

    Provides ambient UI state (``view``) and explicitly referenced objects
    (``referenced_objects``) in addition to the optionally active object
    (``active_object``).
    """

    active_object: CatalogActiveObjectIdentification | None = None
    referenced_objects: list[CatalogObjectReferenceGroup] = attrs.field(factory=list)
    view: CatalogUIContext | None = None

    def as_api_model(self) -> UserContext:
        kwargs: dict[str, Any] = {}
        if self.active_object is not None:
            kwargs["active_object"] = self.active_object.as_api_model()
        if self.referenced_objects:
            kwargs["referenced_objects"] = [ro.as_api_model() for ro in self.referenced_objects]
        if self.view is not None:
            kwargs["view"] = self.view.as_api_model()
        return UserContext(_check_type=False, **kwargs)

# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any, Literal, Union

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
from gooddata_api_client.model.widget_descriptor import WidgetDescriptor

from gooddata_sdk.catalog.base import Base

# Type alias for object reference types
ObjectReferenceType = Literal["WIDGET", "METRIC", "ATTRIBUTE", "DASHBOARD"]


@attrs.define(kw_only=True)
class CatalogActiveObjectIdentification(Base):
    """Identifies the object the user is currently actively viewing."""

    id: str
    type: str
    workspace_id: str

    @staticmethod
    def client_class() -> type[ActiveObjectIdentification]:
        return ActiveObjectIdentification

    def to_api(self) -> ActiveObjectIdentification:
        return ActiveObjectIdentification(
            id=self.id,
            type=self.type,
            workspace_id=self.workspace_id,
            _check_type=False,
        )


@attrs.define(kw_only=True)
class CatalogObjectReference(Base):
    """Reference to a GoodData object (widget, metric, attribute, or dashboard)."""

    id: str
    type: ObjectReferenceType

    @staticmethod
    def client_class() -> type[ObjectReference]:
        return ObjectReference

    def to_api(self) -> ObjectReference:
        return ObjectReference(
            id=self.id,
            type=self.type,
            _check_type=False,
        )


@attrs.define(kw_only=True)
class CatalogObjectReferenceGroup(Base):
    """Group of explicitly referenced objects, optionally scoped by a context."""

    objects: list[CatalogObjectReference] = attrs.field(factory=list)
    context: CatalogObjectReference | None = None

    @staticmethod
    def client_class() -> type[ObjectReferenceGroup]:
        return ObjectReferenceGroup

    def to_api(self) -> ObjectReferenceGroup:
        kwargs: dict[str, Any] = {}
        if self.context is not None:
            kwargs["context"] = self.context.to_api()
        return ObjectReferenceGroup(
            objects=[o.to_api() for o in self.objects],
            _check_type=False,
            **kwargs,
        )


@attrs.define(kw_only=True)
class CatalogWidgetDescriptor(Base):
    """Descriptor for a widget visible on a dashboard."""

    title: str
    widget_id: str
    widget_type: str
    filters: list[Any] = attrs.field(factory=list)

    @staticmethod
    def client_class() -> type[WidgetDescriptor]:
        return WidgetDescriptor

    def to_api(self) -> WidgetDescriptor:
        kwargs: dict[str, Any] = {}
        if self.filters:
            kwargs["filters"] = self.filters
        return WidgetDescriptor(
            title=self.title,
            widget_id=self.widget_id,
            widget_type=self.widget_type,
            _check_type=False,
            **kwargs,
        )


@attrs.define(kw_only=True)
class CatalogInsightWidgetDescriptor(Base):
    """Descriptor for an insight (visualization) widget on a dashboard."""

    title: str
    visualization_id: str
    widget_id: str
    filters: list[Any] = attrs.field(factory=list)
    result_id: str | None = None

    @staticmethod
    def client_class() -> type[InsightWidgetDescriptor]:
        return InsightWidgetDescriptor

    def to_api(self) -> InsightWidgetDescriptor:
        kwargs: dict[str, Any] = {}
        if self.filters:
            kwargs["filters"] = self.filters
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
class CatalogRichTextWidgetDescriptor(Base):
    """Descriptor for a rich text widget on a dashboard."""

    title: str
    widget_id: str
    filters: list[Any] = attrs.field(factory=list)

    @staticmethod
    def client_class() -> type[RichTextWidgetDescriptor]:
        return RichTextWidgetDescriptor

    def to_api(self) -> RichTextWidgetDescriptor:
        kwargs: dict[str, Any] = {}
        if self.filters:
            kwargs["filters"] = self.filters
        return RichTextWidgetDescriptor(
            title=self.title,
            widget_id=self.widget_id,
            _check_type=False,
            **kwargs,
        )


@attrs.define(kw_only=True)
class CatalogVisualizationSwitcherWidgetDescriptor(Base):
    """Descriptor for a visualization switcher widget on a dashboard."""

    active_visualization_id: str
    title: str
    visualization_ids: list[str] = attrs.field(factory=list)
    widget_id: str
    filters: list[Any] = attrs.field(factory=list)
    result_id: str | None = None

    @staticmethod
    def client_class() -> type[VisualizationSwitcherWidgetDescriptor]:
        return VisualizationSwitcherWidgetDescriptor

    def to_api(self) -> VisualizationSwitcherWidgetDescriptor:
        kwargs: dict[str, Any] = {}
        if self.filters:
            kwargs["filters"] = self.filters
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


# Union type for all widget descriptor variants
CatalogWidgetDescriptorType = Union[
    CatalogWidgetDescriptor,
    CatalogInsightWidgetDescriptor,
    CatalogRichTextWidgetDescriptor,
    CatalogVisualizationSwitcherWidgetDescriptor,
]


@attrs.define(kw_only=True)
class CatalogDashboardContext(Base):
    """Context for the dashboard the user is currently viewing."""

    id: str
    widgets: list[CatalogWidgetDescriptorType] = attrs.field(factory=list)

    @staticmethod
    def client_class() -> type[DashboardContext]:
        return DashboardContext

    def to_api(self) -> DashboardContext:
        return DashboardContext(
            id=self.id,
            widgets=[w.to_api() for w in self.widgets],
            _check_type=False,
        )


@attrs.define(kw_only=True)
class CatalogUIContext(Base):
    """Ambient UI state: what the user is currently looking at."""

    dashboard: CatalogDashboardContext | None = None

    @staticmethod
    def client_class() -> type[UIContext]:
        return UIContext

    def to_api(self) -> UIContext:
        kwargs: dict[str, Any] = {}
        if self.dashboard is not None:
            kwargs["dashboard"] = self.dashboard.to_api()
        return UIContext(
            _check_type=False,
            **kwargs,
        )


@attrs.define(kw_only=True)
class CatalogUserContext(Base):
    """User context with ambient UI state and explicitly referenced objects."""

    active_object: CatalogActiveObjectIdentification | None = None
    referenced_objects: list[CatalogObjectReferenceGroup] | None = None
    view: CatalogUIContext | None = None

    @staticmethod
    def client_class() -> type[UserContext]:
        return UserContext

    def to_api(self) -> UserContext:
        kwargs: dict[str, Any] = {}
        if self.active_object is not None:
            kwargs["active_object"] = self.active_object.to_api()
        if self.referenced_objects is not None:
            kwargs["referenced_objects"] = [r.to_api() for r in self.referenced_objects]
        if self.view is not None:
            kwargs["view"] = self.view.to_api()
        return UserContext(
            _check_type=False,
            **kwargs,
        )

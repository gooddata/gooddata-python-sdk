# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any

import attrs
from gooddata_api_client.model.active_object_identification import ActiveObjectIdentification
from gooddata_api_client.model.dashboard_context import DashboardContext
from gooddata_api_client.model.object_reference import ObjectReference
from gooddata_api_client.model.object_reference_group import ObjectReferenceGroup
from gooddata_api_client.model.rich_text_widget_descriptor import RichTextWidgetDescriptor
from gooddata_api_client.model.ui_context import UIContext
from gooddata_api_client.model.user_context import UserContext
from gooddata_api_client.model.widget_descriptor import WidgetDescriptor

from gooddata_sdk.catalog.base import Base


@attrs.define(kw_only=True)
class CatalogObjectReference(Base):
    """Reference to a GoodData object by its ID and type."""

    id: str
    type: str  # Allowed: WIDGET, METRIC, ATTRIBUTE, DASHBOARD

    @staticmethod
    def client_class() -> type[ObjectReference]:
        return ObjectReference


@attrs.define(kw_only=True)
class CatalogObjectReferenceGroup(Base):
    """Group of explicitly referenced objects, optionally scoped by a context."""

    objects: list[CatalogObjectReference] = attrs.field(factory=list)
    context: CatalogObjectReference | None = None

    @staticmethod
    def client_class() -> type[ObjectReferenceGroup]:
        return ObjectReferenceGroup

    def as_api_model(self) -> ObjectReferenceGroup:
        api_objects = [o.to_api() for o in self.objects]
        kwargs: dict[str, Any] = {}
        if self.context is not None:
            kwargs["context"] = self.context.to_api()
        return ObjectReferenceGroup(_check_type=False, objects=api_objects, **kwargs)


@attrs.define(kw_only=True)
class CatalogActiveObjectIdentification(Base):
    """Identifies the object currently active (open/selected) by the user."""

    id: str
    type: str
    workspace_id: str

    @staticmethod
    def client_class() -> type[ActiveObjectIdentification]:
        return ActiveObjectIdentification


@attrs.define(kw_only=True)
class CatalogWidgetDescriptor(Base):
    """Describes a widget currently visible on the dashboard."""

    title: str
    widget_id: str
    widget_type: str
    filters: list[dict[str, Any]] = attrs.field(factory=list)

    @staticmethod
    def client_class() -> type[WidgetDescriptor]:
        return WidgetDescriptor

    def as_api_model(self) -> WidgetDescriptor:
        kwargs: dict[str, Any] = {}
        if self.filters:
            kwargs["filters"] = self.filters
        return WidgetDescriptor(
            _check_type=False,
            title=self.title,
            widget_id=self.widget_id,
            widget_type=self.widget_type,
            **kwargs,
        )


@attrs.define(kw_only=True)
class CatalogRichTextWidgetDescriptor(Base):
    """Describes a rich text widget currently visible on the dashboard."""

    title: str
    widget_id: str
    filters: list[dict[str, Any]] = attrs.field(factory=list)

    @staticmethod
    def client_class() -> type[RichTextWidgetDescriptor]:
        return RichTextWidgetDescriptor

    def as_api_model(self) -> RichTextWidgetDescriptor:
        kwargs: dict[str, Any] = {}
        if self.filters:
            kwargs["filters"] = self.filters
        return RichTextWidgetDescriptor(
            _check_type=False,
            title=self.title,
            widget_id=self.widget_id,
            **kwargs,
        )


@attrs.define(kw_only=True)
class CatalogDashboardContext(Base):
    """Context describing the currently open dashboard and its visible widgets."""

    id: str
    widgets: list[CatalogWidgetDescriptor] = attrs.field(factory=list)

    @staticmethod
    def client_class() -> type[DashboardContext]:
        return DashboardContext

    def as_api_model(self) -> DashboardContext:
        return DashboardContext(
            _check_type=False,
            id=self.id,
            widgets=[w.as_api_model() for w in self.widgets],
        )


@attrs.define(kw_only=True)
class CatalogUIContext(Base):
    """UI context describing the user's current view."""

    dashboard: CatalogDashboardContext | None = None

    @staticmethod
    def client_class() -> type[UIContext]:
        return UIContext

    def as_api_model(self) -> UIContext:
        kwargs: dict[str, Any] = {}
        if self.dashboard is not None:
            kwargs["dashboard"] = self.dashboard.as_api_model()
        return UIContext(_check_type=False, **kwargs)


@attrs.define(kw_only=True)
class CatalogUserContext(Base):
    """User context for AI chat, providing information about the user's current state.

    Pass an instance of this class to :py:meth:`ComputeService.ai_chat` or
    :py:meth:`ComputeService.ai_chat_stream` to give the AI assistant richer
    context about what the user is currently looking at.
    """

    active_object: CatalogActiveObjectIdentification | None = None
    referenced_objects: list[CatalogObjectReferenceGroup] = attrs.field(factory=list)
    view: CatalogUIContext | None = None

    @staticmethod
    def client_class() -> type[UserContext]:
        return UserContext

    def as_api_model(self) -> UserContext:
        kwargs: dict[str, Any] = {}
        if self.active_object is not None:
            kwargs["active_object"] = self.active_object.to_api()
        if self.referenced_objects:
            kwargs["referenced_objects"] = [r.as_api_model() for r in self.referenced_objects]
        if self.view is not None:
            kwargs["view"] = self.view.as_api_model()
        return UserContext(_check_type=False, **kwargs)

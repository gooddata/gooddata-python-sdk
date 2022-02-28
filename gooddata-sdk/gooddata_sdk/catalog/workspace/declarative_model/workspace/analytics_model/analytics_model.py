# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any, Type, TypeVar

from gooddata_metadata_client.model.declarative_analytical_dashboard import DeclarativeAnalyticalDashboard
from gooddata_metadata_client.model.declarative_analytics import DeclarativeAnalytics
from gooddata_metadata_client.model.declarative_analytics_layer import DeclarativeAnalyticsLayer
from gooddata_metadata_client.model.declarative_dashboard_plugin import DeclarativeDashboardPlugin
from gooddata_metadata_client.model.declarative_filter_context import DeclarativeFilterContext
from gooddata_metadata_client.model.declarative_metric import DeclarativeMetric
from gooddata_metadata_client.model.declarative_visualization_object import DeclarativeVisualizationObject

T = TypeVar("T", bound="CatalogAnalyticsBase")


class CatalogDeclarativeAnalytics:
    def __init__(self, analytics: CatalogDeclarativeAnalyticsLayer = None):
        self.analytics = analytics

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDeclarativeAnalytics:
        analytics = CatalogDeclarativeAnalyticsLayer.from_api(entity["analytics"]) if entity.get("analytics") else None
        return cls(analytics)

    def to_api(self) -> DeclarativeAnalytics:
        kwargs: dict[str, Any] = dict()
        if self.analytics:
            kwargs["analytics"] = self.analytics.to_api()
        return DeclarativeAnalytics(**kwargs)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogDeclarativeAnalytics):
            return False
        return self.analytics == other.analytics


class CatalogDeclarativeAnalyticsLayer:
    def __init__(
        self,
        analytical_dashboards: list[CatalogDeclarativeAnalyticalDashboard] = None,
        dashboard_plugins: list[CatalogDeclarativeDashboardPlugin] = None,
        filter_contexts: list[CatalogDeclarativeFilterContext] = None,
        metrics: list[CatalogDeclarativeMetric] = None,
        visualization_objects: list[CatalogDeclarativeVisualizationObject] = None,
    ):
        self.analytical_dashboards = analytical_dashboards or []
        self.dashboard_plugins = dashboard_plugins or []
        self.filter_contexts = filter_contexts or []
        self.metrics = metrics or []
        self.visualization_objects = visualization_objects or []

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDeclarativeAnalyticsLayer:
        analytical_dashboards = (
            [CatalogDeclarativeAnalyticalDashboard.from_api(v) for v in entity["analytical_dashboards"]]
            if entity.get("analytical_dashboards")
            else []
        )
        dashboard_plugins = (
            [CatalogDeclarativeDashboardPlugin.from_api(v) for v in entity["dashboard_plugins"]]
            if entity.get("dashboard_plugins")
            else []
        )
        filter_contexts = (
            [CatalogDeclarativeFilterContext.from_api(v) for v in entity["filter_contexts"]]
            if entity.get("filter_contexts")
            else []
        )
        metrics = [CatalogDeclarativeMetric.from_api(v) for v in entity["metrics"]] if entity.get("metrics") else []
        visualization_objects = (
            [CatalogDeclarativeVisualizationObject.from_api(v) for v in entity["visualization_objects"]]
            if entity.get("visualization_objects")
            else []
        )

        return cls(analytical_dashboards, dashboard_plugins, filter_contexts, metrics, visualization_objects)

    def to_api(self) -> DeclarativeAnalyticsLayer:
        kwargs: dict[str, Any] = {
            "analytical_dashboards": [v.to_api() for v in self.analytical_dashboards],
            "dashboard_plugins": [v.to_api() for v in self.dashboard_plugins],
            "filter_contexts": [v.to_api() for v in self.filter_contexts],
            "metrics": [v.to_api() for v in self.metrics],
            "visualization_objects": [v.to_api() for v in self.visualization_objects],
        }
        return DeclarativeAnalyticsLayer(**kwargs)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogDeclarativeAnalyticsLayer):
            return False
        return (
            self.analytical_dashboards == other.analytical_dashboards
            and self.dashboard_plugins == other.dashboard_plugins
            and self.filter_contexts == other.filter_contexts
            and self.metrics == other.metrics
            and self.visualization_objects == other.visualization_objects
        )


class CatalogAnalyticsBase:
    def __init__(self, id: str, title: str, content: dict[str, Any], description: str = None, tags: list[str] = None):
        self.id = id
        self.title = title
        self.content = content
        self.description = description
        self.tags = tags

    @classmethod
    def from_api(cls: Type[T], entity: dict[str, Any]) -> T:
        return cls(entity["id"], entity["title"], entity["content"], entity.get("description"), entity.get("tags"))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return (
            self.id == other.id
            and self.title == other.title
            and self.content == other.content
            and self.description == other.description
            and self.tags == other.tags
        )

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, title={self.title})"

    def get_kwargs(self) -> dict[str, Any]:
        kwargs: dict[str, Any] = dict()
        if self.description:
            kwargs["description"] = self.description
        if self.tags:
            kwargs["tags"] = self.tags
        return kwargs


class CatalogDeclarativeAnalyticalDashboard(CatalogAnalyticsBase):
    def to_api(self) -> DeclarativeAnalyticalDashboard:
        kwargs: dict[str, Any] = self.get_kwargs()
        return DeclarativeAnalyticalDashboard(self.id, self.title, self.content, **kwargs)


class CatalogDeclarativeDashboardPlugin(CatalogAnalyticsBase):
    def to_api(self) -> DeclarativeDashboardPlugin:
        kwargs: dict[str, Any] = self.get_kwargs()
        return DeclarativeDashboardPlugin(self.id, self.title, self.content, **kwargs)


class CatalogDeclarativeFilterContext(CatalogAnalyticsBase):
    def to_api(self) -> DeclarativeFilterContext:
        kwargs: dict[str, Any] = self.get_kwargs()
        return DeclarativeFilterContext(self.id, self.title, self.content, **kwargs)


class CatalogDeclarativeMetric(CatalogAnalyticsBase):
    def to_api(self) -> DeclarativeMetric:
        kwargs: dict[str, Any] = self.get_kwargs()
        return DeclarativeMetric(self.id, self.title, self.content, **kwargs)


class CatalogDeclarativeVisualizationObject(CatalogAnalyticsBase):
    def to_api(self) -> DeclarativeVisualizationObject:
        kwargs: dict[str, Any] = self.get_kwargs()
        return DeclarativeVisualizationObject(self.id, self.title, self.content, **kwargs)

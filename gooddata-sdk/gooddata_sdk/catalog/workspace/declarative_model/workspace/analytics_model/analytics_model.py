# (C) 2022 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from typing import Any, Type, TypeVar, Union

from gooddata_metadata_client.model.declarative_analytical_dashboard import DeclarativeAnalyticalDashboard
from gooddata_metadata_client.model.declarative_analytics import DeclarativeAnalytics
from gooddata_metadata_client.model.declarative_analytics_layer import DeclarativeAnalyticsLayer
from gooddata_metadata_client.model.declarative_dashboard_plugin import DeclarativeDashboardPlugin
from gooddata_metadata_client.model.declarative_filter_context import DeclarativeFilterContext
from gooddata_metadata_client.model.declarative_metric import DeclarativeMetric
from gooddata_metadata_client.model.declarative_visualization_object import DeclarativeVisualizationObject
from gooddata_sdk.utils import create_directory, get_sorted_yaml_files, read_layout_from_file, write_layout_to_file

T = TypeVar("T", bound="CatalogAnalyticsBase")
AnalyticsObjects = Union[
    DeclarativeAnalyticalDashboard,
    DeclarativeDashboardPlugin,
    DeclarativeFilterContext,
    DeclarativeMetric,
    DeclarativeVisualizationObject,
]

LAYOUT_ANALYTICS_MODEL_DIR = "analytics_model"
LAYOUT_ANALYTICAL_DASHBOARDS_DIR = "analytical_dashboards"
LAYOUT_DASHBOARD_PLUGINS_DIR = "dashboard_plugins"
LAYOUT_FILTER_CONTEXTS_DIR = "filter_contexts"
LAYOUT_METRICS_DIR = "metrics"
LAYOUT_VISUALIZATION_OBJECTS_DIR = "visualization_objects"


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

    def store_to_disk(self, workspace_folder: Path) -> None:
        if self.analytics is not None:
            self.analytics.store_to_disk(workspace_folder)

    @classmethod
    def load_from_disk(cls, workspace_folder: Path) -> CatalogDeclarativeAnalytics:
        analytics = CatalogDeclarativeAnalyticsLayer.load_from_disk(workspace_folder)
        return cls(analytics=analytics)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogDeclarativeAnalytics):
            return False
        return self.analytics == other.analytics

    @classmethod
    def from_dict(cls, data: dict[str, Any], camel_case: bool = True) -> CatalogDeclarativeAnalytics:
        """
        :param data:    Data loaded for example from the file.
        :param camel_case:  True if the variable names in the input
                        data are serialized names as specified in the OpenAPI document.
                        False if the variables names in the input data are python
                        variable names in PEP-8 snake case.
        :return:    CatalogDeclarativeAnalytics object.
        """
        declarative_analytics = DeclarativeAnalytics.from_dict(data, camel_case)
        return cls.from_api(declarative_analytics)


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

    @staticmethod
    def get_analytics_model_folder(workspace_folder: Path) -> Path:
        folder = workspace_folder / LAYOUT_ANALYTICS_MODEL_DIR
        create_directory(folder)
        return folder

    @staticmethod
    def get_analytical_dashboards_folder(analytics_model_folder: Path) -> Path:
        folder = analytics_model_folder / LAYOUT_ANALYTICAL_DASHBOARDS_DIR
        create_directory(folder)
        return folder

    @staticmethod
    def get_dashboard_plugins_folder(analytics_model_folder: Path) -> Path:
        folder = analytics_model_folder / LAYOUT_DASHBOARD_PLUGINS_DIR
        create_directory(folder)
        return folder

    @staticmethod
    def get_filter_contexts_folder(analytics_model_folder: Path) -> Path:
        folder = analytics_model_folder / LAYOUT_FILTER_CONTEXTS_DIR
        create_directory(folder)
        return folder

    @staticmethod
    def get_metrics_folder(analytics_model_folder: Path) -> Path:
        folder = analytics_model_folder / LAYOUT_METRICS_DIR
        create_directory(folder)
        return folder

    @staticmethod
    def get_visualization_objects_folder(analytics_model_folder: Path) -> Path:
        folder = analytics_model_folder / LAYOUT_VISUALIZATION_OBJECTS_DIR
        create_directory(folder)
        return folder

    def store_to_disk(self, workspace_folder: Path) -> None:
        analytics_model_folder = self.get_analytics_model_folder(workspace_folder)

        analytical_dashboards_folder = self.get_analytical_dashboards_folder(analytics_model_folder)
        dashboard_plugins_folder = self.get_dashboard_plugins_folder(analytics_model_folder)
        filter_contexts_folder = self.get_filter_contexts_folder(analytics_model_folder)
        metrics_folder = self.get_metrics_folder(analytics_model_folder)
        visualization_objects_folder = self.get_visualization_objects_folder(analytics_model_folder)

        for analytical_dashboard in self.analytical_dashboards:
            analytical_dashboard.store_to_disk(analytical_dashboards_folder)

        for dashboard_plugin in self.dashboard_plugins:
            dashboard_plugin.store_to_disk(dashboard_plugins_folder)

        for filter_context in self.filter_contexts:
            filter_context.store_to_disk(filter_contexts_folder)

        for metric in self.metrics:
            metric.store_to_disk(metrics_folder)

        for visualization_object in self.visualization_objects:
            visualization_object.store_to_disk(visualization_objects_folder)

    @classmethod
    def load_from_disk(cls, workspace_folder: Path) -> CatalogDeclarativeAnalyticsLayer:
        analytics_model_folder = cls.get_analytics_model_folder(workspace_folder)
        analytical_dashboards_folder = cls.get_analytical_dashboards_folder(analytics_model_folder)
        dashboard_plugins_folder = cls.get_dashboard_plugins_folder(analytics_model_folder)
        filter_contexts_folder = cls.get_filter_contexts_folder(analytics_model_folder)
        metrics_folder = cls.get_metrics_folder(analytics_model_folder)
        visualization_objects_folder = cls.get_visualization_objects_folder(analytics_model_folder)

        analytical_dashboard_files = get_sorted_yaml_files(analytical_dashboards_folder)
        dashboard_plugin_files = get_sorted_yaml_files(dashboard_plugins_folder)
        filter_context_files = get_sorted_yaml_files(filter_contexts_folder)
        metric_files = get_sorted_yaml_files(metrics_folder)
        visualization_object_files = get_sorted_yaml_files(visualization_objects_folder)

        analytical_dashboards = [
            CatalogDeclarativeAnalyticalDashboard.load_from_disk(analytical_dashboard_file)
            for analytical_dashboard_file in analytical_dashboard_files
        ]
        dashboard_plugins = [
            CatalogDeclarativeDashboardPlugin.load_from_disk(dashboard_plugin_file)
            for dashboard_plugin_file in dashboard_plugin_files
        ]
        filter_contexts = [
            CatalogDeclarativeFilterContext.load_from_disk(filter_context_file)
            for filter_context_file in filter_context_files
        ]
        metrics = [CatalogDeclarativeMetric.load_from_disk(metric_file) for metric_file in metric_files]
        visualization_objects = [
            CatalogDeclarativeVisualizationObject.load_from_disk(visualization_object_file)
            for visualization_object_file in visualization_object_files
        ]
        return cls(
            analytical_dashboards=analytical_dashboards,
            dashboard_plugins=dashboard_plugins,
            filter_contexts=filter_contexts,
            metrics=metrics,
            visualization_objects=visualization_objects,
        )

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

    def to_api(self) -> AnalyticsObjects:
        return NotImplemented

    def store_to_disk(self, analytics_folder: Path) -> None:
        analytics_file = analytics_folder / f"{self.id}.yaml"
        write_layout_to_file(analytics_file, self.to_api().to_dict(camel_case=True))

    @classmethod
    def load_from_disk(cls: Type[T], analytics_file: Path) -> T:
        analytics_layout = read_layout_from_file(analytics_file)
        return cls.from_dict(analytics_layout)

    @classmethod
    def from_dict(cls: Type[T], data: dict[str, Any]) -> T:
        """
        For simplification, we can use directly from_api method,
        because all attributes follow the same attributes name convention,
        which is same for snake and camel case.
        The content attribute does not change (even if we put it inside client class).
        """
        return cls.from_api(data)

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

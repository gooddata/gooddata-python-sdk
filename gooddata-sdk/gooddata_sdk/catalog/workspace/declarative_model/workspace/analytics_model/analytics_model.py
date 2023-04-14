# (C) 2022 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

import attr

from gooddata_api_client.model.declarative_analytical_dashboard import DeclarativeAnalyticalDashboard
from gooddata_api_client.model.declarative_analytical_dashboard_extension import DeclarativeAnalyticalDashboardExtension
from gooddata_api_client.model.declarative_analytics import DeclarativeAnalytics
from gooddata_api_client.model.declarative_analytics_layer import DeclarativeAnalyticsLayer
from gooddata_api_client.model.declarative_dashboard_plugin import DeclarativeDashboardPlugin
from gooddata_api_client.model.declarative_filter_context import DeclarativeFilterContext
from gooddata_api_client.model.declarative_metric import DeclarativeMetric
from gooddata_api_client.model.declarative_visualization_object import DeclarativeVisualizationObject
from gooddata_sdk import CatalogDeclarativeWorkspaceHierarchyPermission
from gooddata_sdk.catalog.base import Base
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
LAYOUT_ANALYTICAL_DASHBOARD_EXTENSIONS_DIR = "analytical_dashboard_extensions"
LAYOUT_DASHBOARD_PLUGINS_DIR = "dashboard_plugins"
LAYOUT_FILTER_CONTEXTS_DIR = "filter_contexts"
LAYOUT_METRICS_DIR = "metrics"
LAYOUT_VISUALIZATION_OBJECTS_DIR = "visualization_objects"


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeAnalytics(Base):
    analytics: Optional[CatalogDeclarativeAnalyticsLayer] = None

    @staticmethod
    def client_class() -> Type[DeclarativeAnalytics]:
        return DeclarativeAnalytics

    def store_to_disk(self, workspace_folder: Path) -> None:
        if self.analytics is not None:
            self.analytics.store_to_disk(workspace_folder)

    @classmethod
    def load_from_disk(cls, workspace_folder: Path) -> CatalogDeclarativeAnalytics:
        analytics = CatalogDeclarativeAnalyticsLayer.load_from_disk(workspace_folder)
        return cls(analytics=analytics)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeAnalyticsLayer(Base):
    analytical_dashboards: List[CatalogDeclarativeAnalyticalDashboard] = attr.field(factory=list)
    analytical_dashboard_extensions: List[CatalogDeclarativeAnalyticalDashboardExtension] = attr.field(factory=list)
    dashboard_plugins: List[CatalogDeclarativeDashboardPlugin] = attr.field(factory=list)
    filter_contexts: List[CatalogDeclarativeFilterContext] = attr.field(factory=list)
    metrics: List[CatalogDeclarativeMetric] = attr.field(factory=list)
    visualization_objects: List[CatalogDeclarativeVisualizationObject] = attr.field(factory=list)

    @staticmethod
    def client_class() -> Type[DeclarativeAnalyticsLayer]:
        return DeclarativeAnalyticsLayer

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
    def get_analytical_dashboard_extensions_folder(analytics_model_folder: Path) -> Path:
        folder = analytics_model_folder / LAYOUT_ANALYTICAL_DASHBOARD_EXTENSIONS_DIR
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
        analytical_dashboard_extensions_folder = self.get_analytical_dashboard_extensions_folder(analytics_model_folder)
        dashboard_plugins_folder = self.get_dashboard_plugins_folder(analytics_model_folder)
        filter_contexts_folder = self.get_filter_contexts_folder(analytics_model_folder)
        metrics_folder = self.get_metrics_folder(analytics_model_folder)
        visualization_objects_folder = self.get_visualization_objects_folder(analytics_model_folder)

        for analytical_dashboard in self.analytical_dashboards:
            analytical_dashboard.store_to_disk(analytical_dashboards_folder)

        for analytical_dashboard_extension in self.analytical_dashboard_extensions:
            analytical_dashboard_extension.store_to_disk(analytical_dashboard_extensions_folder)

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
        analytical_dashboard_extensions_folder = cls.get_analytical_dashboard_extensions_folder(analytics_model_folder)
        dashboard_plugins_folder = cls.get_dashboard_plugins_folder(analytics_model_folder)
        filter_contexts_folder = cls.get_filter_contexts_folder(analytics_model_folder)
        metrics_folder = cls.get_metrics_folder(analytics_model_folder)
        visualization_objects_folder = cls.get_visualization_objects_folder(analytics_model_folder)

        analytical_dashboard_files = get_sorted_yaml_files(analytical_dashboards_folder)
        analytical_dashboard_extension_files = get_sorted_yaml_files(analytical_dashboard_extensions_folder)
        dashboard_plugin_files = get_sorted_yaml_files(dashboard_plugins_folder)
        filter_context_files = get_sorted_yaml_files(filter_contexts_folder)
        metric_files = get_sorted_yaml_files(metrics_folder)
        visualization_object_files = get_sorted_yaml_files(visualization_objects_folder)

        analytical_dashboards = [
            CatalogDeclarativeAnalyticalDashboard.load_from_disk(analytical_dashboard_file)
            for analytical_dashboard_file in analytical_dashboard_files
        ]
        analytical_dashboard_extensions = [
            CatalogDeclarativeAnalyticalDashboardExtension.load_from_disk(analytical_dashboard_extension_file)
            for analytical_dashboard_extension_file in analytical_dashboard_extension_files
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
            analytical_dashboard_extensions=analytical_dashboard_extensions,
            dashboard_plugins=dashboard_plugins,
            filter_contexts=filter_contexts,
            metrics=metrics,
            visualization_objects=visualization_objects,
        )


@attr.s(auto_attribs=True, kw_only=True)
class CatalogAnalyticsBase(Base):
    id: str

    def store_to_disk(self, analytics_folder: Path) -> None:
        analytics_file = analytics_folder / f"{self.id}.yaml"
        write_layout_to_file(analytics_file, self.to_api().to_dict(camel_case=True))

    @classmethod
    def load_from_disk(cls: Type[T], analytics_file: Path) -> T:
        analytics_layout = read_layout_from_file(analytics_file)
        return cls.from_dict(analytics_layout)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeAnalyticalDashboard(CatalogAnalyticsBase):
    id: str
    title: str
    content: Dict[str, Any]
    description: Optional[str] = None
    tags: Optional[List[str]] = None

    @staticmethod
    def client_class() -> Type[DeclarativeAnalyticalDashboard]:
        return DeclarativeAnalyticalDashboard


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeDashboardPlugin(CatalogAnalyticsBase):
    id: str
    title: str
    content: Dict[str, Any]
    description: Optional[str] = None
    tags: Optional[List[str]] = None

    @staticmethod
    def client_class() -> Type[DeclarativeDashboardPlugin]:
        return DeclarativeDashboardPlugin


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeAnalyticalDashboardExtension(CatalogAnalyticsBase):
    id: str
    permissions: List[CatalogDeclarativeWorkspaceHierarchyPermission]

    @staticmethod
    def client_class() -> Type[DeclarativeAnalyticalDashboardExtension]:
        return DeclarativeAnalyticalDashboardExtension


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeFilterContext(CatalogAnalyticsBase):
    id: str
    title: str
    content: Dict[str, Any]
    description: Optional[str] = None
    tags: Optional[List[str]] = None

    @staticmethod
    def client_class() -> Type[DeclarativeFilterContext]:
        return DeclarativeFilterContext


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeMetric(CatalogAnalyticsBase):
    id: str
    title: str
    content: Dict[str, Any]
    description: Optional[str] = None
    tags: Optional[List[str]] = None

    @staticmethod
    def client_class() -> Type[DeclarativeMetric]:
        return DeclarativeMetric


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeVisualizationObject(CatalogAnalyticsBase):
    id: str
    title: str
    content: Dict[str, Any]
    description: Optional[str] = None
    tags: Optional[List[str]] = None

    @staticmethod
    def client_class() -> Type[DeclarativeVisualizationObject]:
        return DeclarativeVisualizationObject

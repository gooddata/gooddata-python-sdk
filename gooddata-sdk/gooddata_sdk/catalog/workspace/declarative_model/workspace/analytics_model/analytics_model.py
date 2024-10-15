# (C) 2022 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from typing import Any, Optional, Union

import attr
from attrs import define
from cattrs import global_converter, structure
from gooddata_api_client.model.declarative_analytical_dashboard import DeclarativeAnalyticalDashboard
from gooddata_api_client.model.declarative_analytical_dashboard_extension import DeclarativeAnalyticalDashboardExtension
from gooddata_api_client.model.declarative_analytics import DeclarativeAnalytics
from gooddata_api_client.model.declarative_analytics_layer import DeclarativeAnalyticsLayer
from gooddata_api_client.model.declarative_attribute_hierarchy import DeclarativeAttributeHierarchy
from gooddata_api_client.model.declarative_dashboard_plugin import DeclarativeDashboardPlugin
from gooddata_api_client.model.declarative_filter_context import DeclarativeFilterContext
from gooddata_api_client.model.declarative_metric import DeclarativeMetric
from gooddata_api_client.model.declarative_visualization_object import DeclarativeVisualizationObject

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.permission.declarative_model.permission import (
    CatalogDeclarativeDashboardPermissionsForAssignee,
    CatalogDeclarativeDashboardPermissionsForAssigneeRule,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.base import (
    CatalogAnalyticsBase,
    CatalogAnalyticsObjectBase,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.export_definition import (
    CatalogDeclarativeExportDefinition,
)
from gooddata_sdk.utils import create_directory, get_sorted_yaml_files

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
ATTRIBUTE_HIERARCHY_OBJECTS_DIR = "attribute_hierarchy_objects"
EXPORT_DEFINITION_DIR = "export_definitions"


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeAnalytics(Base):
    analytics: Optional[CatalogDeclarativeAnalyticsLayer] = None

    @staticmethod
    def client_class() -> type[DeclarativeAnalytics]:
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
    analytical_dashboards: list[CatalogDeclarativeAnalyticalDashboard] = attr.field(factory=list)
    analytical_dashboard_extensions: list[CatalogDeclarativeAnalyticalDashboardExtension] = attr.field(factory=list)
    attribute_hierarchies: list[CatalogDeclarativeAttributeHierarchy] = attr.field(factory=list)
    dashboard_plugins: list[CatalogDeclarativeDashboardPlugin] = attr.field(factory=list)
    filter_contexts: list[CatalogDeclarativeFilterContext] = attr.field(factory=list)
    metrics: list[CatalogDeclarativeMetric] = attr.field(factory=list)
    visualization_objects: list[CatalogDeclarativeVisualizationObject] = attr.field(factory=list)
    export_definitions: list[CatalogDeclarativeExportDefinition] = attr.field(factory=list)

    @staticmethod
    def client_class() -> type[DeclarativeAnalyticsLayer]:
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

    @staticmethod
    def get_attribute_hierarchy_folder(analytics_model_folder: Path) -> Path:
        folder = analytics_model_folder / ATTRIBUTE_HIERARCHY_OBJECTS_DIR
        create_directory(folder)
        return folder

    @staticmethod
    def get_export_definition_dif(analytics_model_folder: Path) -> Path:
        folder = analytics_model_folder / EXPORT_DEFINITION_DIR
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
        attribute_hierarchy_folder = self.get_attribute_hierarchy_folder(analytics_model_folder)
        export_definition_folder = self.get_export_definition_dif(analytical_dashboards_folder)

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

        for attribute_hierarchy in self.attribute_hierarchies:
            attribute_hierarchy.store_to_disk(attribute_hierarchy_folder)

        for export_definition in self.export_definitions:
            export_definition.store_to_disk(export_definition_folder)

    @classmethod
    def load_from_disk(cls, workspace_folder: Path) -> CatalogDeclarativeAnalyticsLayer:
        analytics_model_folder = cls.get_analytics_model_folder(workspace_folder)
        analytical_dashboards_folder = cls.get_analytical_dashboards_folder(analytics_model_folder)
        analytical_dashboard_extensions_folder = cls.get_analytical_dashboard_extensions_folder(analytics_model_folder)
        dashboard_plugins_folder = cls.get_dashboard_plugins_folder(analytics_model_folder)
        filter_contexts_folder = cls.get_filter_contexts_folder(analytics_model_folder)
        metrics_folder = cls.get_metrics_folder(analytics_model_folder)
        visualization_objects_folder = cls.get_visualization_objects_folder(analytics_model_folder)
        attribute_hierarchy_folder = cls.get_attribute_hierarchy_folder(analytics_model_folder)
        export_definition_folder = cls.get_export_definition_dif(analytical_dashboards_folder)

        analytical_dashboard_files = get_sorted_yaml_files(analytical_dashboards_folder)
        analytical_dashboard_extension_files = get_sorted_yaml_files(analytical_dashboard_extensions_folder)
        dashboard_plugin_files = get_sorted_yaml_files(dashboard_plugins_folder)
        filter_context_files = get_sorted_yaml_files(filter_contexts_folder)
        metric_files = get_sorted_yaml_files(metrics_folder)
        visualization_object_files = get_sorted_yaml_files(visualization_objects_folder)
        attribute_hierarchy_files = get_sorted_yaml_files(attribute_hierarchy_folder)
        export_definition_files = get_sorted_yaml_files(export_definition_folder)

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
        attribute_hierarchy_objects = [
            CatalogDeclarativeAttributeHierarchy.load_from_disk(attribute_hierarchy_file)
            for attribute_hierarchy_file in attribute_hierarchy_files
        ]
        export_definitions = [
            CatalogDeclarativeExportDefinition.load_from_disk(export_definition_file)
            for export_definition_file in export_definition_files
        ]
        return cls(
            analytical_dashboards=analytical_dashboards,
            analytical_dashboard_extensions=analytical_dashboard_extensions,
            attribute_hierarchies=attribute_hierarchy_objects,
            dashboard_plugins=dashboard_plugins,
            filter_contexts=filter_contexts,
            metrics=metrics,
            visualization_objects=visualization_objects,
            export_definitions=export_definitions,
        )


@define(auto_attribs=True, kw_only=True)
class CatalogDeclarativeAnalyticalDashboard(CatalogAnalyticsBase):
    permissions: Optional[
        list[
            Union[
                CatalogDeclarativeDashboardPermissionsForAssignee, CatalogDeclarativeDashboardPermissionsForAssigneeRule
            ]
        ]
    ] = None

    @staticmethod
    def client_class() -> type[DeclarativeAnalyticalDashboard]:
        return DeclarativeAnalyticalDashboard

    @staticmethod
    def structure_permissions(
        v: dict[str, Any], _: Any
    ) -> Union[
        CatalogDeclarativeDashboardPermissionsForAssignee, CatalogDeclarativeDashboardPermissionsForAssigneeRule
    ]:
        if v.get("assignee") is not None:
            return structure(v, CatalogDeclarativeDashboardPermissionsForAssignee)
        else:
            return structure(v, CatalogDeclarativeDashboardPermissionsForAssigneeRule)


global_converter.register_structure_hook(
    Union[CatalogDeclarativeDashboardPermissionsForAssignee, CatalogDeclarativeDashboardPermissionsForAssigneeRule],
    CatalogDeclarativeAnalyticalDashboard.structure_permissions,
)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeDashboardPlugin(CatalogAnalyticsBase):
    @staticmethod
    def client_class() -> type[DeclarativeDashboardPlugin]:
        return DeclarativeDashboardPlugin


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeAnalyticalDashboardExtension(CatalogAnalyticsObjectBase):
    permissions: list[
        Union[CatalogDeclarativeDashboardPermissionsForAssignee, CatalogDeclarativeDashboardPermissionsForAssigneeRule]
    ]

    @staticmethod
    def client_class() -> type[DeclarativeAnalyticalDashboardExtension]:
        return DeclarativeAnalyticalDashboardExtension


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeFilterContext(CatalogAnalyticsBase):
    @staticmethod
    def client_class() -> type[DeclarativeFilterContext]:
        return DeclarativeFilterContext


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeMetric(CatalogAnalyticsBase):
    @staticmethod
    def client_class() -> type[DeclarativeMetric]:
        return DeclarativeMetric


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeVisualizationObject(CatalogAnalyticsBase):
    @staticmethod
    def client_class() -> type[DeclarativeVisualizationObject]:
        return DeclarativeVisualizationObject


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeAttributeHierarchy(CatalogAnalyticsBase):
    @staticmethod
    def client_class() -> type[DeclarativeAttributeHierarchy]:
        return DeclarativeAttributeHierarchy

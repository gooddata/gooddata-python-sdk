# coding: utf-8

"""
    OpenAPI definition

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v0
    Contact: support@gooddata.com
    Generated by: https://openapi-generator.tech
"""

from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_analytical_dashboards.post import CreateEntityAnalyticalDashboards
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_custom_application_settings.post import CreateEntityCustomApplicationSettings
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_dashboard_plugins.post import CreateEntityDashboardPlugins
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_filter_contexts.post import CreateEntityFilterContexts
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_metrics.post import CreateEntityMetrics
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_user_data_filters.post import CreateEntityUserDataFilters
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_visualization_objects.post import CreateEntityVisualizationObjects
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_workspace_data_filters.post import CreateEntityWorkspaceDataFilters
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_workspace_settings.post import CreateEntityWorkspaceSettings
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_analytical_dashboards_object_id.delete import DeleteEntityAnalyticalDashboards
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_custom_application_settings_object_id.delete import DeleteEntityCustomApplicationSettings
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_dashboard_plugins_object_id.delete import DeleteEntityDashboardPlugins
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_filter_contexts_object_id.delete import DeleteEntityFilterContexts
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_metrics_object_id.delete import DeleteEntityMetrics
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_user_data_filters_object_id.delete import DeleteEntityUserDataFilters
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_visualization_objects_object_id.delete import DeleteEntityVisualizationObjects
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_workspace_data_filters_object_id.delete import DeleteEntityWorkspaceDataFilters
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_workspace_settings_object_id.delete import DeleteEntityWorkspaceSettings
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_analytical_dashboards.get import GetAllEntitiesAnalyticalDashboards
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_attributes.get import GetAllEntitiesAttributes
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_custom_application_settings.get import GetAllEntitiesCustomApplicationSettings
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_dashboard_plugins.get import GetAllEntitiesDashboardPlugins
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_datasets.get import GetAllEntitiesDatasets
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_facts.get import GetAllEntitiesFacts
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_filter_contexts.get import GetAllEntitiesFilterContexts
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_labels.get import GetAllEntitiesLabels
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_metrics.get import GetAllEntitiesMetrics
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_user_data_filters.get import GetAllEntitiesUserDataFilters
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_visualization_objects.get import GetAllEntitiesVisualizationObjects
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_workspace_data_filter_settings.get import GetAllEntitiesWorkspaceDataFilterSettings
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_workspace_data_filters.get import GetAllEntitiesWorkspaceDataFilters
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_workspace_settings.get import GetAllEntitiesWorkspaceSettings
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_analytical_dashboards_object_id.get import GetEntityAnalyticalDashboards
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_attributes_object_id.get import GetEntityAttributes
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_custom_application_settings_object_id.get import GetEntityCustomApplicationSettings
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_dashboard_plugins_object_id.get import GetEntityDashboardPlugins
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_datasets_object_id.get import GetEntityDatasets
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_facts_object_id.get import GetEntityFacts
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_filter_contexts_object_id.get import GetEntityFilterContexts
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_labels_object_id.get import GetEntityLabels
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_metrics_object_id.get import GetEntityMetrics
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_user_data_filters_object_id.get import GetEntityUserDataFilters
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_visualization_objects_object_id.get import GetEntityVisualizationObjects
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_workspace_data_filter_settings_object_id.get import GetEntityWorkspaceDataFilterSettings
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_workspace_data_filters_object_id.get import GetEntityWorkspaceDataFilters
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_workspace_settings_object_id.get import GetEntityWorkspaceSettings
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_analytical_dashboards_object_id.patch import PatchEntityAnalyticalDashboards
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_custom_application_settings_object_id.patch import PatchEntityCustomApplicationSettings
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_dashboard_plugins_object_id.patch import PatchEntityDashboardPlugins
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_filter_contexts_object_id.patch import PatchEntityFilterContexts
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_metrics_object_id.patch import PatchEntityMetrics
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_user_data_filters_object_id.patch import PatchEntityUserDataFilters
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_visualization_objects_object_id.patch import PatchEntityVisualizationObjects
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_workspace_data_filters_object_id.patch import PatchEntityWorkspaceDataFilters
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_workspace_settings_object_id.patch import PatchEntityWorkspaceSettings
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_analytical_dashboards_object_id.put import UpdateEntityAnalyticalDashboards
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_custom_application_settings_object_id.put import UpdateEntityCustomApplicationSettings
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_dashboard_plugins_object_id.put import UpdateEntityDashboardPlugins
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_filter_contexts_object_id.put import UpdateEntityFilterContexts
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_metrics_object_id.put import UpdateEntityMetrics
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_user_data_filters_object_id.put import UpdateEntityUserDataFilters
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_visualization_objects_object_id.put import UpdateEntityVisualizationObjects
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_workspace_data_filters_object_id.put import UpdateEntityWorkspaceDataFilters
from gooddata_api_client.paths.api_v1_entities_workspaces_workspace_id_workspace_settings_object_id.put import UpdateEntityWorkspaceSettings


class WorkspaceObjectControllerApi(
    CreateEntityAnalyticalDashboards,
    CreateEntityCustomApplicationSettings,
    CreateEntityDashboardPlugins,
    CreateEntityFilterContexts,
    CreateEntityMetrics,
    CreateEntityUserDataFilters,
    CreateEntityVisualizationObjects,
    CreateEntityWorkspaceDataFilters,
    CreateEntityWorkspaceSettings,
    DeleteEntityAnalyticalDashboards,
    DeleteEntityCustomApplicationSettings,
    DeleteEntityDashboardPlugins,
    DeleteEntityFilterContexts,
    DeleteEntityMetrics,
    DeleteEntityUserDataFilters,
    DeleteEntityVisualizationObjects,
    DeleteEntityWorkspaceDataFilters,
    DeleteEntityWorkspaceSettings,
    GetAllEntitiesAnalyticalDashboards,
    GetAllEntitiesAttributes,
    GetAllEntitiesCustomApplicationSettings,
    GetAllEntitiesDashboardPlugins,
    GetAllEntitiesDatasets,
    GetAllEntitiesFacts,
    GetAllEntitiesFilterContexts,
    GetAllEntitiesLabels,
    GetAllEntitiesMetrics,
    GetAllEntitiesUserDataFilters,
    GetAllEntitiesVisualizationObjects,
    GetAllEntitiesWorkspaceDataFilterSettings,
    GetAllEntitiesWorkspaceDataFilters,
    GetAllEntitiesWorkspaceSettings,
    GetEntityAnalyticalDashboards,
    GetEntityAttributes,
    GetEntityCustomApplicationSettings,
    GetEntityDashboardPlugins,
    GetEntityDatasets,
    GetEntityFacts,
    GetEntityFilterContexts,
    GetEntityLabels,
    GetEntityMetrics,
    GetEntityUserDataFilters,
    GetEntityVisualizationObjects,
    GetEntityWorkspaceDataFilterSettings,
    GetEntityWorkspaceDataFilters,
    GetEntityWorkspaceSettings,
    PatchEntityAnalyticalDashboards,
    PatchEntityCustomApplicationSettings,
    PatchEntityDashboardPlugins,
    PatchEntityFilterContexts,
    PatchEntityMetrics,
    PatchEntityUserDataFilters,
    PatchEntityVisualizationObjects,
    PatchEntityWorkspaceDataFilters,
    PatchEntityWorkspaceSettings,
    UpdateEntityAnalyticalDashboards,
    UpdateEntityCustomApplicationSettings,
    UpdateEntityDashboardPlugins,
    UpdateEntityFilterContexts,
    UpdateEntityMetrics,
    UpdateEntityUserDataFilters,
    UpdateEntityVisualizationObjects,
    UpdateEntityWorkspaceDataFilters,
    UpdateEntityWorkspaceSettings,
):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    pass

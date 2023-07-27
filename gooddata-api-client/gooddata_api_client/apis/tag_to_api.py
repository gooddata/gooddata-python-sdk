import typing_extensions

from gooddata_api_client.apis.tags import TagValues
from gooddata_api_client.apis.tags.analytics_model_api import AnalyticsModelApi
from gooddata_api_client.apis.tags.available_drivers_api import AvailableDriversApi
from gooddata_api_client.apis.tags.computation_api import ComputationApi
from gooddata_api_client.apis.tags.data_filters_api import DataFiltersApi
from gooddata_api_client.apis.tags.data_source_declarative_apis_api import DataSourceDeclarativeAPIsApi
from gooddata_api_client.apis.tags.dependency_graph_api import DependencyGraphApi
from gooddata_api_client.apis.tags.entitlement_api import EntitlementApi
from gooddata_api_client.apis.tags.generate_logical_data_model_api import GenerateLogicalDataModelApi
from gooddata_api_client.apis.tags.invalidate_cache_api import InvalidateCacheApi
from gooddata_api_client.apis.tags.ldm_declarative_apis_api import LDMDeclarativeAPIsApi
from gooddata_api_client.apis.tags.options_api import OptionsApi
from gooddata_api_client.apis.tags.organization_declarative_apis_api import OrganizationDeclarativeAPIsApi
from gooddata_api_client.apis.tags.organization_entity_apis_api import OrganizationEntityAPIsApi
from gooddata_api_client.apis.tags.pdm_declarative_apis_api import PDMDeclarativeAPIsApi
from gooddata_api_client.apis.tags.permissions_api import PermissionsApi
from gooddata_api_client.apis.tags.reporting_settings_api import ReportingSettingsApi
from gooddata_api_client.apis.tags.scanning_api import ScanningApi
from gooddata_api_client.apis.tags.test_connection_api import TestConnectionApi
from gooddata_api_client.apis.tags.usage_api import UsageApi
from gooddata_api_client.apis.tags.user_data_filters_api import UserDataFiltersApi
from gooddata_api_client.apis.tags.user_groups_declarative_apis_api import UserGroupsDeclarativeAPIsApi
from gooddata_api_client.apis.tags.users_declarative_apis_api import UsersDeclarativeAPIsApi
from gooddata_api_client.apis.tags.workspaces_declarative_apis_api import WorkspacesDeclarativeAPIsApi
from gooddata_api_client.apis.tags.workspaces_settings_api import WorkspacesSettingsApi
from gooddata_api_client.apis.tags.actions_api import ActionsApi
from gooddata_api_client.apis.tags.entities_api import EntitiesApi
from gooddata_api_client.apis.tags.layout_api import LayoutApi
from gooddata_api_client.apis.tags.api_tokens_api import APITokensApi
from gooddata_api_client.apis.tags.user_model_controller_api import UserModelControllerApi
from gooddata_api_client.apis.tags.appearance_api import AppearanceApi
from gooddata_api_client.apis.tags.organization_model_controller_api import OrganizationModelControllerApi
from gooddata_api_client.apis.tags.attributes_api import AttributesApi
from gooddata_api_client.apis.tags.workspace_object_controller_api import WorkspaceObjectControllerApi
from gooddata_api_client.apis.tags.csp_directives_api import CSPDirectivesApi
from gooddata_api_client.apis.tags.context_filters_api import ContextFiltersApi
from gooddata_api_client.apis.tags.cookie_security_configuration_api import CookieSecurityConfigurationApi
from gooddata_api_client.apis.tags.organization_controller_api import OrganizationControllerApi
from gooddata_api_client.apis.tags.dashboards_api import DashboardsApi
from gooddata_api_client.apis.tags.data_source_entity_apis_api import DataSourceEntityAPIsApi
from gooddata_api_client.apis.tags.data_source_entities_controller_api import DataSourceEntitiesControllerApi
from gooddata_api_client.apis.tags.datasets_api import DatasetsApi
from gooddata_api_client.apis.tags.exporting_api import ExportingApi
from gooddata_api_client.apis.tags.facts_api import FactsApi
from gooddata_api_client.apis.tags.labels_api import LabelsApi
from gooddata_api_client.apis.tags.metrics_api import MetricsApi
from gooddata_api_client.apis.tags.plugins_api import PluginsApi
from gooddata_api_client.apis.tags.user_settings_api import UserSettingsApi
from gooddata_api_client.apis.tags.user_groups_entity_apis_api import UserGroupsEntityAPIsApi
from gooddata_api_client.apis.tags.users_entity_apis_api import UsersEntityAPIsApi
from gooddata_api_client.apis.tags.visualization_object_api import VisualizationObjectApi
from gooddata_api_client.apis.tags.workspaces_entity_apis_api import WorkspacesEntityAPIsApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.ANALYTICS_MODEL: AnalyticsModelApi,
        TagValues.AVAILABLE_DRIVERS: AvailableDriversApi,
        TagValues.COMPUTATION: ComputationApi,
        TagValues.DATA_FILTERS: DataFiltersApi,
        TagValues.DATA_SOURCE__DECLARATIVE_APIS: DataSourceDeclarativeAPIsApi,
        TagValues.DEPENDENCY_GRAPH: DependencyGraphApi,
        TagValues.ENTITLEMENT: EntitlementApi,
        TagValues.GENERATE_LOGICAL_DATA_MODEL: GenerateLogicalDataModelApi,
        TagValues.INVALIDATE_CACHE: InvalidateCacheApi,
        TagValues.LDM__DECLARATIVE_APIS: LDMDeclarativeAPIsApi,
        TagValues.OPTIONS: OptionsApi,
        TagValues.ORGANIZATION__DECLARATIVE_APIS: OrganizationDeclarativeAPIsApi,
        TagValues.ORGANIZATION__ENTITY_APIS: OrganizationEntityAPIsApi,
        TagValues.PDM__DECLARATIVE_APIS: PDMDeclarativeAPIsApi,
        TagValues.PERMISSIONS: PermissionsApi,
        TagValues.REPORTING__SETTINGS: ReportingSettingsApi,
        TagValues.SCANNING: ScanningApi,
        TagValues.TEST_CONNECTION: TestConnectionApi,
        TagValues.USAGE: UsageApi,
        TagValues.USER_DATA_FILTERS: UserDataFiltersApi,
        TagValues.USER_GROUPS__DECLARATIVE_APIS: UserGroupsDeclarativeAPIsApi,
        TagValues.USERS__DECLARATIVE_APIS: UsersDeclarativeAPIsApi,
        TagValues.WORKSPACES__DECLARATIVE_APIS: WorkspacesDeclarativeAPIsApi,
        TagValues.WORKSPACES__SETTINGS: WorkspacesSettingsApi,
        TagValues.ACTIONS: ActionsApi,
        TagValues.ENTITIES: EntitiesApi,
        TagValues.LAYOUT: LayoutApi,
        TagValues.API_TOKENS: APITokensApi,
        TagValues.USERMODELCONTROLLER: UserModelControllerApi,
        TagValues.APPEARANCE: AppearanceApi,
        TagValues.ORGANIZATIONMODELCONTROLLER: OrganizationModelControllerApi,
        TagValues.ATTRIBUTES: AttributesApi,
        TagValues.WORKSPACEOBJECTCONTROLLER: WorkspaceObjectControllerApi,
        TagValues.CSP_DIRECTIVES: CSPDirectivesApi,
        TagValues.CONTEXT_FILTERS: ContextFiltersApi,
        TagValues.COOKIE_SECURITY_CONFIGURATION: CookieSecurityConfigurationApi,
        TagValues.ORGANIZATIONCONTROLLER: OrganizationControllerApi,
        TagValues.DASHBOARDS: DashboardsApi,
        TagValues.DATA_SOURCE__ENTITY_APIS: DataSourceEntityAPIsApi,
        TagValues.DATASOURCEENTITIESCONTROLLER: DataSourceEntitiesControllerApi,
        TagValues.DATASETS: DatasetsApi,
        TagValues.EXPORTING: ExportingApi,
        TagValues.FACTS: FactsApi,
        TagValues.LABELS: LabelsApi,
        TagValues.METRICS: MetricsApi,
        TagValues.PLUGINS: PluginsApi,
        TagValues.USER_SETTINGS: UserSettingsApi,
        TagValues.USER_GROUPS__ENTITY_APIS: UserGroupsEntityAPIsApi,
        TagValues.USERS__ENTITY_APIS: UsersEntityAPIsApi,
        TagValues.VISUALIZATION_OBJECT: VisualizationObjectApi,
        TagValues.WORKSPACES__ENTITY_APIS: WorkspacesEntityAPIsApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.ANALYTICS_MODEL: AnalyticsModelApi,
        TagValues.AVAILABLE_DRIVERS: AvailableDriversApi,
        TagValues.COMPUTATION: ComputationApi,
        TagValues.DATA_FILTERS: DataFiltersApi,
        TagValues.DATA_SOURCE__DECLARATIVE_APIS: DataSourceDeclarativeAPIsApi,
        TagValues.DEPENDENCY_GRAPH: DependencyGraphApi,
        TagValues.ENTITLEMENT: EntitlementApi,
        TagValues.GENERATE_LOGICAL_DATA_MODEL: GenerateLogicalDataModelApi,
        TagValues.INVALIDATE_CACHE: InvalidateCacheApi,
        TagValues.LDM__DECLARATIVE_APIS: LDMDeclarativeAPIsApi,
        TagValues.OPTIONS: OptionsApi,
        TagValues.ORGANIZATION__DECLARATIVE_APIS: OrganizationDeclarativeAPIsApi,
        TagValues.ORGANIZATION__ENTITY_APIS: OrganizationEntityAPIsApi,
        TagValues.PDM__DECLARATIVE_APIS: PDMDeclarativeAPIsApi,
        TagValues.PERMISSIONS: PermissionsApi,
        TagValues.REPORTING__SETTINGS: ReportingSettingsApi,
        TagValues.SCANNING: ScanningApi,
        TagValues.TEST_CONNECTION: TestConnectionApi,
        TagValues.USAGE: UsageApi,
        TagValues.USER_DATA_FILTERS: UserDataFiltersApi,
        TagValues.USER_GROUPS__DECLARATIVE_APIS: UserGroupsDeclarativeAPIsApi,
        TagValues.USERS__DECLARATIVE_APIS: UsersDeclarativeAPIsApi,
        TagValues.WORKSPACES__DECLARATIVE_APIS: WorkspacesDeclarativeAPIsApi,
        TagValues.WORKSPACES__SETTINGS: WorkspacesSettingsApi,
        TagValues.ACTIONS: ActionsApi,
        TagValues.ENTITIES: EntitiesApi,
        TagValues.LAYOUT: LayoutApi,
        TagValues.API_TOKENS: APITokensApi,
        TagValues.USERMODELCONTROLLER: UserModelControllerApi,
        TagValues.APPEARANCE: AppearanceApi,
        TagValues.ORGANIZATIONMODELCONTROLLER: OrganizationModelControllerApi,
        TagValues.ATTRIBUTES: AttributesApi,
        TagValues.WORKSPACEOBJECTCONTROLLER: WorkspaceObjectControllerApi,
        TagValues.CSP_DIRECTIVES: CSPDirectivesApi,
        TagValues.CONTEXT_FILTERS: ContextFiltersApi,
        TagValues.COOKIE_SECURITY_CONFIGURATION: CookieSecurityConfigurationApi,
        TagValues.ORGANIZATIONCONTROLLER: OrganizationControllerApi,
        TagValues.DASHBOARDS: DashboardsApi,
        TagValues.DATA_SOURCE__ENTITY_APIS: DataSourceEntityAPIsApi,
        TagValues.DATASOURCEENTITIESCONTROLLER: DataSourceEntitiesControllerApi,
        TagValues.DATASETS: DatasetsApi,
        TagValues.EXPORTING: ExportingApi,
        TagValues.FACTS: FactsApi,
        TagValues.LABELS: LabelsApi,
        TagValues.METRICS: MetricsApi,
        TagValues.PLUGINS: PluginsApi,
        TagValues.USER_SETTINGS: UserSettingsApi,
        TagValues.USER_GROUPS__ENTITY_APIS: UserGroupsEntityAPIsApi,
        TagValues.USERS__ENTITY_APIS: UsersEntityAPIsApi,
        TagValues.VISUALIZATION_OBJECT: VisualizationObjectApi,
        TagValues.WORKSPACES__ENTITY_APIS: WorkspacesEntityAPIsApi,
    }
)

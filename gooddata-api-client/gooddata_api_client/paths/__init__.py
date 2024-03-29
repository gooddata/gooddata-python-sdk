# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from gooddata_api_client.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    API_V1_ACTIONS_COLLECT_USAGE = "/api/v1/actions/collectUsage"
    API_V1_ACTIONS_DATA_SOURCE_TEST = "/api/v1/actions/dataSource/test"
    API_V1_ACTIONS_DATA_SOURCES_DATA_SOURCE_ID_GENERATE_LOGICAL_MODEL = "/api/v1/actions/dataSources/{dataSourceId}/generateLogicalModel"
    API_V1_ACTIONS_DATA_SOURCES_DATA_SOURCE_ID_SCAN = "/api/v1/actions/dataSources/{dataSourceId}/scan"
    API_V1_ACTIONS_DATA_SOURCES_DATA_SOURCE_ID_SCAN_SCHEMATA = "/api/v1/actions/dataSources/{dataSourceId}/scanSchemata"
    API_V1_ACTIONS_DATA_SOURCES_DATA_SOURCE_ID_SCAN_SQL = "/api/v1/actions/dataSources/{dataSourceId}/scanSql"
    API_V1_ACTIONS_DATA_SOURCES_DATA_SOURCE_ID_TEST = "/api/v1/actions/dataSources/{dataSourceId}/test"
    API_V1_ACTIONS_DATA_SOURCES_DATA_SOURCE_ID_UPLOAD_NOTIFICATION = "/api/v1/actions/dataSources/{dataSourceId}/uploadNotification"
    API_V1_ACTIONS_RESOLVE_ENTITLEMENTS = "/api/v1/actions/resolveEntitlements"
    API_V1_ACTIONS_RESOLVE_SETTINGS = "/api/v1/actions/resolveSettings"
    API_V1_ACTIONS_WORKSPACES_WORKSPACE_ID_ANALYTICAL_DASHBOARDS_DASHBOARD_ID_AVAILABLE_ASSIGNEES = "/api/v1/actions/workspaces/{workspaceId}/analyticalDashboards/{dashboardId}/availableAssignees"
    API_V1_ACTIONS_WORKSPACES_WORKSPACE_ID_ANALYTICAL_DASHBOARDS_DASHBOARD_ID_MANAGE_PERMISSIONS = "/api/v1/actions/workspaces/{workspaceId}/analyticalDashboards/{dashboardId}/managePermissions"
    API_V1_ACTIONS_WORKSPACES_WORKSPACE_ID_ANALYTICAL_DASHBOARDS_DASHBOARD_ID_PERMISSIONS = "/api/v1/actions/workspaces/{workspaceId}/analyticalDashboards/{dashboardId}/permissions"
    API_V1_ACTIONS_WORKSPACES_WORKSPACE_ID_CHECK_ENTITY_OVERRIDES = "/api/v1/actions/workspaces/{workspaceId}/checkEntityOverrides"
    API_V1_ACTIONS_WORKSPACES_WORKSPACE_ID_DEPENDENT_ENTITIES_GRAPH = "/api/v1/actions/workspaces/{workspaceId}/dependentEntitiesGraph"
    API_V1_ACTIONS_WORKSPACES_WORKSPACE_ID_EXECUTION_AFM_COMPUTE_VALID_OBJECTS = "/api/v1/actions/workspaces/{workspaceId}/execution/afm/computeValidObjects"
    API_V1_ACTIONS_WORKSPACES_WORKSPACE_ID_EXECUTION_AFM_EXECUTE = "/api/v1/actions/workspaces/{workspaceId}/execution/afm/execute"
    API_V1_ACTIONS_WORKSPACES_WORKSPACE_ID_EXECUTION_AFM_EXECUTE_RESULT_RESULT_ID = "/api/v1/actions/workspaces/{workspaceId}/execution/afm/execute/result/{resultId}"
    API_V1_ACTIONS_WORKSPACES_WORKSPACE_ID_EXECUTION_AFM_EXECUTE_RESULT_RESULT_ID_METADATA = "/api/v1/actions/workspaces/{workspaceId}/execution/afm/execute/result/{resultId}/metadata"
    API_V1_ACTIONS_WORKSPACES_WORKSPACE_ID_EXECUTION_AFM_EXPLAIN = "/api/v1/actions/workspaces/{workspaceId}/execution/afm/explain"
    API_V1_ACTIONS_WORKSPACES_WORKSPACE_ID_EXECUTION_COLLECT_LABEL_ELEMENTS = "/api/v1/actions/workspaces/{workspaceId}/execution/collectLabelElements"
    API_V1_ACTIONS_WORKSPACES_WORKSPACE_ID_EXPORT_TABULAR = "/api/v1/actions/workspaces/{workspaceId}/export/tabular"
    API_V1_ACTIONS_WORKSPACES_WORKSPACE_ID_EXPORT_TABULAR_EXPORT_ID = "/api/v1/actions/workspaces/{workspaceId}/export/tabular/{exportId}"
    API_V1_ACTIONS_WORKSPACES_WORKSPACE_ID_EXPORT_VISUAL = "/api/v1/actions/workspaces/{workspaceId}/export/visual"
    API_V1_ACTIONS_WORKSPACES_WORKSPACE_ID_EXPORT_VISUAL_EXPORT_ID = "/api/v1/actions/workspaces/{workspaceId}/export/visual/{exportId}"
    API_V1_ACTIONS_WORKSPACES_WORKSPACE_ID_EXPORT_VISUAL_EXPORT_ID_METADATA = "/api/v1/actions/workspaces/{workspaceId}/export/visual/{exportId}/metadata"
    API_V1_ACTIONS_WORKSPACES_WORKSPACE_ID_INHERITED_ENTITY_CONFLICTS = "/api/v1/actions/workspaces/{workspaceId}/inheritedEntityConflicts"
    API_V1_ACTIONS_WORKSPACES_WORKSPACE_ID_OVERRIDDEN_CHILD_ENTITIES = "/api/v1/actions/workspaces/{workspaceId}/overriddenChildEntities"
    API_V1_ACTIONS_WORKSPACES_WORKSPACE_ID_RESOLVE_SETTINGS = "/api/v1/actions/workspaces/{workspaceId}/resolveSettings"
    API_V1_ENTITIES_ADMIN_COOKIE_SECURITY_CONFIGURATIONS_ID = "/api/v1/entities/admin/cookieSecurityConfigurations/{id}"
    API_V1_ENTITIES_ADMIN_ORGANIZATIONS_ID = "/api/v1/entities/admin/organizations/{id}"
    API_V1_ENTITIES_COLOR_PALETTES = "/api/v1/entities/colorPalettes"
    API_V1_ENTITIES_COLOR_PALETTES_ID = "/api/v1/entities/colorPalettes/{id}"
    API_V1_ENTITIES_CSP_DIRECTIVES = "/api/v1/entities/cspDirectives"
    API_V1_ENTITIES_CSP_DIRECTIVES_ID = "/api/v1/entities/cspDirectives/{id}"
    API_V1_ENTITIES_DATA_SOURCE_IDENTIFIERS = "/api/v1/entities/dataSourceIdentifiers"
    API_V1_ENTITIES_DATA_SOURCE_IDENTIFIERS_ID = "/api/v1/entities/dataSourceIdentifiers/{id}"
    API_V1_ENTITIES_DATA_SOURCES = "/api/v1/entities/dataSources"
    API_V1_ENTITIES_DATA_SOURCES_DATA_SOURCE_ID_DATA_SOURCE_TABLES = "/api/v1/entities/dataSources/{dataSourceId}/dataSourceTables"
    API_V1_ENTITIES_DATA_SOURCES_DATA_SOURCE_ID_DATA_SOURCE_TABLES_ID = "/api/v1/entities/dataSources/{dataSourceId}/dataSourceTables/{id}"
    API_V1_ENTITIES_DATA_SOURCES_ID = "/api/v1/entities/dataSources/{id}"
    API_V1_ENTITIES_ENTITLEMENTS = "/api/v1/entities/entitlements"
    API_V1_ENTITIES_ENTITLEMENTS_ID = "/api/v1/entities/entitlements/{id}"
    API_V1_ENTITIES_ORGANIZATION = "/api/v1/entities/organization"
    API_V1_ENTITIES_ORGANIZATION_SETTINGS = "/api/v1/entities/organizationSettings"
    API_V1_ENTITIES_ORGANIZATION_SETTINGS_ID = "/api/v1/entities/organizationSettings/{id}"
    API_V1_ENTITIES_THEMES = "/api/v1/entities/themes"
    API_V1_ENTITIES_THEMES_ID = "/api/v1/entities/themes/{id}"
    API_V1_ENTITIES_USER_GROUPS = "/api/v1/entities/userGroups"
    API_V1_ENTITIES_USER_GROUPS_ID = "/api/v1/entities/userGroups/{id}"
    API_V1_ENTITIES_USERS = "/api/v1/entities/users"
    API_V1_ENTITIES_USERS_ID = "/api/v1/entities/users/{id}"
    API_V1_ENTITIES_USERS_USER_ID_API_TOKENS = "/api/v1/entities/users/{userId}/apiTokens"
    API_V1_ENTITIES_USERS_USER_ID_API_TOKENS_ID = "/api/v1/entities/users/{userId}/apiTokens/{id}"
    API_V1_ENTITIES_USERS_USER_ID_USER_SETTINGS = "/api/v1/entities/users/{userId}/userSettings"
    API_V1_ENTITIES_USERS_USER_ID_USER_SETTINGS_ID = "/api/v1/entities/users/{userId}/userSettings/{id}"
    API_V1_ENTITIES_WORKSPACES = "/api/v1/entities/workspaces"
    API_V1_ENTITIES_WORKSPACES_ID = "/api/v1/entities/workspaces/{id}"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_ANALYTICAL_DASHBOARDS = "/api/v1/entities/workspaces/{workspaceId}/analyticalDashboards"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_ANALYTICAL_DASHBOARDS_OBJECT_ID = "/api/v1/entities/workspaces/{workspaceId}/analyticalDashboards/{objectId}"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_ATTRIBUTES = "/api/v1/entities/workspaces/{workspaceId}/attributes"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_ATTRIBUTES_OBJECT_ID = "/api/v1/entities/workspaces/{workspaceId}/attributes/{objectId}"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_CUSTOM_APPLICATION_SETTINGS = "/api/v1/entities/workspaces/{workspaceId}/customApplicationSettings"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_CUSTOM_APPLICATION_SETTINGS_OBJECT_ID = "/api/v1/entities/workspaces/{workspaceId}/customApplicationSettings/{objectId}"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_DASHBOARD_PLUGINS = "/api/v1/entities/workspaces/{workspaceId}/dashboardPlugins"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_DASHBOARD_PLUGINS_OBJECT_ID = "/api/v1/entities/workspaces/{workspaceId}/dashboardPlugins/{objectId}"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_DATASETS = "/api/v1/entities/workspaces/{workspaceId}/datasets"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_DATASETS_OBJECT_ID = "/api/v1/entities/workspaces/{workspaceId}/datasets/{objectId}"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_FACTS = "/api/v1/entities/workspaces/{workspaceId}/facts"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_FACTS_OBJECT_ID = "/api/v1/entities/workspaces/{workspaceId}/facts/{objectId}"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_FILTER_CONTEXTS = "/api/v1/entities/workspaces/{workspaceId}/filterContexts"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_FILTER_CONTEXTS_OBJECT_ID = "/api/v1/entities/workspaces/{workspaceId}/filterContexts/{objectId}"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_LABELS = "/api/v1/entities/workspaces/{workspaceId}/labels"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_LABELS_OBJECT_ID = "/api/v1/entities/workspaces/{workspaceId}/labels/{objectId}"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_METRICS = "/api/v1/entities/workspaces/{workspaceId}/metrics"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_METRICS_OBJECT_ID = "/api/v1/entities/workspaces/{workspaceId}/metrics/{objectId}"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_USER_DATA_FILTERS = "/api/v1/entities/workspaces/{workspaceId}/userDataFilters"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_USER_DATA_FILTERS_OBJECT_ID = "/api/v1/entities/workspaces/{workspaceId}/userDataFilters/{objectId}"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_VISUALIZATION_OBJECTS = "/api/v1/entities/workspaces/{workspaceId}/visualizationObjects"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_VISUALIZATION_OBJECTS_OBJECT_ID = "/api/v1/entities/workspaces/{workspaceId}/visualizationObjects/{objectId}"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_WORKSPACE_DATA_FILTER_SETTINGS = "/api/v1/entities/workspaces/{workspaceId}/workspaceDataFilterSettings"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_WORKSPACE_DATA_FILTER_SETTINGS_OBJECT_ID = "/api/v1/entities/workspaces/{workspaceId}/workspaceDataFilterSettings/{objectId}"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_WORKSPACE_DATA_FILTERS = "/api/v1/entities/workspaces/{workspaceId}/workspaceDataFilters"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_WORKSPACE_DATA_FILTERS_OBJECT_ID = "/api/v1/entities/workspaces/{workspaceId}/workspaceDataFilters/{objectId}"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_WORKSPACE_SETTINGS = "/api/v1/entities/workspaces/{workspaceId}/workspaceSettings"
    API_V1_ENTITIES_WORKSPACES_WORKSPACE_ID_WORKSPACE_SETTINGS_OBJECT_ID = "/api/v1/entities/workspaces/{workspaceId}/workspaceSettings/{objectId}"
    API_V1_LAYOUT_DATA_SOURCES = "/api/v1/layout/dataSources"
    API_V1_LAYOUT_DATA_SOURCES_DATA_SOURCE_ID_PHYSICAL_MODEL = "/api/v1/layout/dataSources/{dataSourceId}/physicalModel"
    API_V1_LAYOUT_ORGANIZATION = "/api/v1/layout/organization"
    API_V1_LAYOUT_USER_GROUPS = "/api/v1/layout/userGroups"
    API_V1_LAYOUT_USER_GROUPS_USER_GROUP_ID_PERMISSIONS = "/api/v1/layout/userGroups/{userGroupId}/permissions"
    API_V1_LAYOUT_USERS = "/api/v1/layout/users"
    API_V1_LAYOUT_USERS_USER_ID_PERMISSIONS = "/api/v1/layout/users/{userId}/permissions"
    API_V1_LAYOUT_USERS_AND_USER_GROUPS = "/api/v1/layout/usersAndUserGroups"
    API_V1_LAYOUT_WORKSPACE_DATA_FILTERS = "/api/v1/layout/workspaceDataFilters"
    API_V1_LAYOUT_WORKSPACES = "/api/v1/layout/workspaces"
    API_V1_LAYOUT_WORKSPACES_WORKSPACE_ID = "/api/v1/layout/workspaces/{workspaceId}"
    API_V1_LAYOUT_WORKSPACES_WORKSPACE_ID_ANALYTICS_MODEL = "/api/v1/layout/workspaces/{workspaceId}/analyticsModel"
    API_V1_LAYOUT_WORKSPACES_WORKSPACE_ID_LOGICAL_MODEL = "/api/v1/layout/workspaces/{workspaceId}/logicalModel"
    API_V1_LAYOUT_WORKSPACES_WORKSPACE_ID_PERMISSIONS = "/api/v1/layout/workspaces/{workspaceId}/permissions"
    API_V1_LAYOUT_WORKSPACES_WORKSPACE_ID_USER_DATA_FILTERS = "/api/v1/layout/workspaces/{workspaceId}/userDataFilters"
    API_V1_OPTIONS = "/api/v1/options"
    API_V1_OPTIONS_AVAILABLE_DRIVERS = "/api/v1/options/availableDrivers"

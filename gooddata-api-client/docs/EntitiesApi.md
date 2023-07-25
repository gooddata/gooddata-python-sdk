# gooddata_api_client.EntitiesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_analytical_dashboards**](EntitiesApi.md#create_entity_analytical_dashboards) | **POST** /api/v1/entities/workspaces/{workspaceId}/analyticalDashboards | Post Dashboards
[**create_entity_api_tokens**](EntitiesApi.md#create_entity_api_tokens) | **POST** /api/v1/entities/users/{userId}/apiTokens | Post a new API token for the user
[**create_entity_color_palettes**](EntitiesApi.md#create_entity_color_palettes) | **POST** /api/v1/entities/colorPalettes | Post Color Pallettes
[**create_entity_csp_directives**](EntitiesApi.md#create_entity_csp_directives) | **POST** /api/v1/entities/cspDirectives | Post CSP Directives
[**create_entity_custom_application_settings**](EntitiesApi.md#create_entity_custom_application_settings) | **POST** /api/v1/entities/workspaces/{workspaceId}/customApplicationSettings | Post Custom Application Settings
[**create_entity_dashboard_plugins**](EntitiesApi.md#create_entity_dashboard_plugins) | **POST** /api/v1/entities/workspaces/{workspaceId}/dashboardPlugins | Post Plugins
[**create_entity_data_sources**](EntitiesApi.md#create_entity_data_sources) | **POST** /api/v1/entities/dataSources | Post Data Sources
[**create_entity_filter_contexts**](EntitiesApi.md#create_entity_filter_contexts) | **POST** /api/v1/entities/workspaces/{workspaceId}/filterContexts | Post Context Filters
[**create_entity_jwks**](EntitiesApi.md#create_entity_jwks) | **POST** /api/v1/entities/jwks | Post Jwks
[**create_entity_metrics**](EntitiesApi.md#create_entity_metrics) | **POST** /api/v1/entities/workspaces/{workspaceId}/metrics | Post Metrics
[**create_entity_organization_settings**](EntitiesApi.md#create_entity_organization_settings) | **POST** /api/v1/entities/organizationSettings | Post Organization Setting entities
[**create_entity_themes**](EntitiesApi.md#create_entity_themes) | **POST** /api/v1/entities/themes | Post Theming
[**create_entity_user_data_filters**](EntitiesApi.md#create_entity_user_data_filters) | **POST** /api/v1/entities/workspaces/{workspaceId}/userDataFilters | Post User Data Filters
[**create_entity_user_groups**](EntitiesApi.md#create_entity_user_groups) | **POST** /api/v1/entities/userGroups | Post User Group entities
[**create_entity_user_settings**](EntitiesApi.md#create_entity_user_settings) | **POST** /api/v1/entities/users/{userId}/userSettings | Post new user settings for the user
[**create_entity_users**](EntitiesApi.md#create_entity_users) | **POST** /api/v1/entities/users | Post User entities
[**create_entity_visualization_objects**](EntitiesApi.md#create_entity_visualization_objects) | **POST** /api/v1/entities/workspaces/{workspaceId}/visualizationObjects | Post Visualization Objects
[**create_entity_workspace_data_filter_settings**](EntitiesApi.md#create_entity_workspace_data_filter_settings) | **POST** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilterSettings | Post Settings for Workspace Data Filters
[**create_entity_workspace_data_filters**](EntitiesApi.md#create_entity_workspace_data_filters) | **POST** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilters | Post Workspace Data Filters
[**create_entity_workspace_settings**](EntitiesApi.md#create_entity_workspace_settings) | **POST** /api/v1/entities/workspaces/{workspaceId}/workspaceSettings | Post Settings for Workspaces
[**create_entity_workspaces**](EntitiesApi.md#create_entity_workspaces) | **POST** /api/v1/entities/workspaces | Post Workspace entities
[**delete_entity_analytical_dashboards**](EntitiesApi.md#delete_entity_analytical_dashboards) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/analyticalDashboards/{objectId} | Delete a Dashboard
[**delete_entity_api_tokens**](EntitiesApi.md#delete_entity_api_tokens) | **DELETE** /api/v1/entities/users/{userId}/apiTokens/{id} | Delete an API Token for a user
[**delete_entity_color_palettes**](EntitiesApi.md#delete_entity_color_palettes) | **DELETE** /api/v1/entities/colorPalettes/{id} | Delete a Color Pallette
[**delete_entity_csp_directives**](EntitiesApi.md#delete_entity_csp_directives) | **DELETE** /api/v1/entities/cspDirectives/{id} | Delete CSP Directives
[**delete_entity_custom_application_settings**](EntitiesApi.md#delete_entity_custom_application_settings) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/customApplicationSettings/{objectId} | Delete a Custom Application Setting
[**delete_entity_dashboard_plugins**](EntitiesApi.md#delete_entity_dashboard_plugins) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/dashboardPlugins/{objectId} | Delete a Plugin
[**delete_entity_data_sources**](EntitiesApi.md#delete_entity_data_sources) | **DELETE** /api/v1/entities/dataSources/{id} | Delete Data Source entity
[**delete_entity_filter_contexts**](EntitiesApi.md#delete_entity_filter_contexts) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/filterContexts/{objectId} | Delete a Context Filter
[**delete_entity_jwks**](EntitiesApi.md#delete_entity_jwks) | **DELETE** /api/v1/entities/jwks/{id} | Delete Jwk
[**delete_entity_metrics**](EntitiesApi.md#delete_entity_metrics) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/metrics/{objectId} | Delete a Metric
[**delete_entity_organization_settings**](EntitiesApi.md#delete_entity_organization_settings) | **DELETE** /api/v1/entities/organizationSettings/{id} | Delete Organization entity
[**delete_entity_themes**](EntitiesApi.md#delete_entity_themes) | **DELETE** /api/v1/entities/themes/{id} | Delete Theming
[**delete_entity_user_data_filters**](EntitiesApi.md#delete_entity_user_data_filters) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/userDataFilters/{objectId} | Delete a User Data Filter
[**delete_entity_user_groups**](EntitiesApi.md#delete_entity_user_groups) | **DELETE** /api/v1/entities/userGroups/{id} | Delete UserGroup entity
[**delete_entity_user_settings**](EntitiesApi.md#delete_entity_user_settings) | **DELETE** /api/v1/entities/users/{userId}/userSettings/{id} | Delete a setting for a user
[**delete_entity_users**](EntitiesApi.md#delete_entity_users) | **DELETE** /api/v1/entities/users/{id} | Delete User entity
[**delete_entity_visualization_objects**](EntitiesApi.md#delete_entity_visualization_objects) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/visualizationObjects/{objectId} | Delete a Visualization Object
[**delete_entity_workspace_data_filter_settings**](EntitiesApi.md#delete_entity_workspace_data_filter_settings) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilterSettings/{objectId} | Delete a Settings for Workspace Data Filter
[**delete_entity_workspace_data_filters**](EntitiesApi.md#delete_entity_workspace_data_filters) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilters/{objectId} | Delete a Workspace Data Filter
[**delete_entity_workspace_settings**](EntitiesApi.md#delete_entity_workspace_settings) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/workspaceSettings/{objectId} | Delete a Setting for Workspace
[**delete_entity_workspaces**](EntitiesApi.md#delete_entity_workspaces) | **DELETE** /api/v1/entities/workspaces/{id} | Delete Workspace entity
[**get_all_entities_analytical_dashboards**](EntitiesApi.md#get_all_entities_analytical_dashboards) | **GET** /api/v1/entities/workspaces/{workspaceId}/analyticalDashboards | Get all Dashboards
[**get_all_entities_api_tokens**](EntitiesApi.md#get_all_entities_api_tokens) | **GET** /api/v1/entities/users/{userId}/apiTokens | List all api tokens for a user
[**get_all_entities_attributes**](EntitiesApi.md#get_all_entities_attributes) | **GET** /api/v1/entities/workspaces/{workspaceId}/attributes | Get all Attributes
[**get_all_entities_color_palettes**](EntitiesApi.md#get_all_entities_color_palettes) | **GET** /api/v1/entities/colorPalettes | Get all Color Pallettes
[**get_all_entities_csp_directives**](EntitiesApi.md#get_all_entities_csp_directives) | **GET** /api/v1/entities/cspDirectives | Get CSP Directives
[**get_all_entities_custom_application_settings**](EntitiesApi.md#get_all_entities_custom_application_settings) | **GET** /api/v1/entities/workspaces/{workspaceId}/customApplicationSettings | Get all Custom Application Settings
[**get_all_entities_dashboard_plugins**](EntitiesApi.md#get_all_entities_dashboard_plugins) | **GET** /api/v1/entities/workspaces/{workspaceId}/dashboardPlugins | Get all Plugins
[**get_all_entities_data_source_identifiers**](EntitiesApi.md#get_all_entities_data_source_identifiers) | **GET** /api/v1/entities/dataSourceIdentifiers | Get all Data Source Identifiers
[**get_all_entities_data_source_tables**](EntitiesApi.md#get_all_entities_data_source_tables) | **GET** /api/v1/entities/dataSources/{dataSourceId}/dataSourceTables | 
[**get_all_entities_data_sources**](EntitiesApi.md#get_all_entities_data_sources) | **GET** /api/v1/entities/dataSources | Get Data Source entities
[**get_all_entities_datasets**](EntitiesApi.md#get_all_entities_datasets) | **GET** /api/v1/entities/workspaces/{workspaceId}/datasets | Get all Datasets
[**get_all_entities_entitlements**](EntitiesApi.md#get_all_entities_entitlements) | **GET** /api/v1/entities/entitlements | Get Entitlements
[**get_all_entities_facts**](EntitiesApi.md#get_all_entities_facts) | **GET** /api/v1/entities/workspaces/{workspaceId}/facts | Get all Facts
[**get_all_entities_filter_contexts**](EntitiesApi.md#get_all_entities_filter_contexts) | **GET** /api/v1/entities/workspaces/{workspaceId}/filterContexts | Get all Context Filters
[**get_all_entities_jwks**](EntitiesApi.md#get_all_entities_jwks) | **GET** /api/v1/entities/jwks | Get all Jwks
[**get_all_entities_labels**](EntitiesApi.md#get_all_entities_labels) | **GET** /api/v1/entities/workspaces/{workspaceId}/labels | Get all Labels
[**get_all_entities_metrics**](EntitiesApi.md#get_all_entities_metrics) | **GET** /api/v1/entities/workspaces/{workspaceId}/metrics | Get all Metrics
[**get_all_entities_organization_settings**](EntitiesApi.md#get_all_entities_organization_settings) | **GET** /api/v1/entities/organizationSettings | Get Organization entities
[**get_all_entities_themes**](EntitiesApi.md#get_all_entities_themes) | **GET** /api/v1/entities/themes | Get all Theming entities
[**get_all_entities_user_data_filters**](EntitiesApi.md#get_all_entities_user_data_filters) | **GET** /api/v1/entities/workspaces/{workspaceId}/userDataFilters | Get all User Data Filters
[**get_all_entities_user_groups**](EntitiesApi.md#get_all_entities_user_groups) | **GET** /api/v1/entities/userGroups | Get UserGroup entities
[**get_all_entities_user_settings**](EntitiesApi.md#get_all_entities_user_settings) | **GET** /api/v1/entities/users/{userId}/userSettings | List all settings for a user
[**get_all_entities_users**](EntitiesApi.md#get_all_entities_users) | **GET** /api/v1/entities/users | Get User entities
[**get_all_entities_visualization_objects**](EntitiesApi.md#get_all_entities_visualization_objects) | **GET** /api/v1/entities/workspaces/{workspaceId}/visualizationObjects | Get all Visualization Objects
[**get_all_entities_workspace_data_filter_settings**](EntitiesApi.md#get_all_entities_workspace_data_filter_settings) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilterSettings | Get all Settings for Workspace Data Filters
[**get_all_entities_workspace_data_filters**](EntitiesApi.md#get_all_entities_workspace_data_filters) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilters | Get all Workspace Data Filters
[**get_all_entities_workspace_settings**](EntitiesApi.md#get_all_entities_workspace_settings) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceSettings | Get all Setting for Workspaces
[**get_all_entities_workspaces**](EntitiesApi.md#get_all_entities_workspaces) | **GET** /api/v1/entities/workspaces | Get Workspace entities
[**get_all_options**](EntitiesApi.md#get_all_options) | **GET** /api/v1/options | Links for all configuration options
[**get_data_source_drivers**](EntitiesApi.md#get_data_source_drivers) | **GET** /api/v1/options/availableDrivers | Get all available data source drivers
[**get_entity_analytical_dashboards**](EntitiesApi.md#get_entity_analytical_dashboards) | **GET** /api/v1/entities/workspaces/{workspaceId}/analyticalDashboards/{objectId} | Get a Dashboard
[**get_entity_api_tokens**](EntitiesApi.md#get_entity_api_tokens) | **GET** /api/v1/entities/users/{userId}/apiTokens/{id} | Get an API Token for a user
[**get_entity_attributes**](EntitiesApi.md#get_entity_attributes) | **GET** /api/v1/entities/workspaces/{workspaceId}/attributes/{objectId} | Get a Attribute
[**get_entity_color_palettes**](EntitiesApi.md#get_entity_color_palettes) | **GET** /api/v1/entities/colorPalettes/{id} | Get Color Pallette
[**get_entity_cookie_security_configurations**](EntitiesApi.md#get_entity_cookie_security_configurations) | **GET** /api/v1/entities/admin/cookieSecurityConfigurations/{id} | Get CookieSecurityConfiguration
[**get_entity_csp_directives**](EntitiesApi.md#get_entity_csp_directives) | **GET** /api/v1/entities/cspDirectives/{id} | Get CSP Directives
[**get_entity_custom_application_settings**](EntitiesApi.md#get_entity_custom_application_settings) | **GET** /api/v1/entities/workspaces/{workspaceId}/customApplicationSettings/{objectId} | Get a Custom Application Setting
[**get_entity_dashboard_plugins**](EntitiesApi.md#get_entity_dashboard_plugins) | **GET** /api/v1/entities/workspaces/{workspaceId}/dashboardPlugins/{objectId} | Get a Plugin
[**get_entity_data_source_identifiers**](EntitiesApi.md#get_entity_data_source_identifiers) | **GET** /api/v1/entities/dataSourceIdentifiers/{id} | Get Data Source Identifier
[**get_entity_data_source_tables**](EntitiesApi.md#get_entity_data_source_tables) | **GET** /api/v1/entities/dataSources/{dataSourceId}/dataSourceTables/{id} | 
[**get_entity_data_sources**](EntitiesApi.md#get_entity_data_sources) | **GET** /api/v1/entities/dataSources/{id} | Get Data Source entity
[**get_entity_datasets**](EntitiesApi.md#get_entity_datasets) | **GET** /api/v1/entities/workspaces/{workspaceId}/datasets/{objectId} | Get a Dataset
[**get_entity_entitlements**](EntitiesApi.md#get_entity_entitlements) | **GET** /api/v1/entities/entitlements/{id} | Get Entitlement
[**get_entity_facts**](EntitiesApi.md#get_entity_facts) | **GET** /api/v1/entities/workspaces/{workspaceId}/facts/{objectId} | Get a Fact
[**get_entity_filter_contexts**](EntitiesApi.md#get_entity_filter_contexts) | **GET** /api/v1/entities/workspaces/{workspaceId}/filterContexts/{objectId} | Get a Context Filter
[**get_entity_jwks**](EntitiesApi.md#get_entity_jwks) | **GET** /api/v1/entities/jwks/{id} | Get Jwk
[**get_entity_labels**](EntitiesApi.md#get_entity_labels) | **GET** /api/v1/entities/workspaces/{workspaceId}/labels/{objectId} | Get a Label
[**get_entity_metrics**](EntitiesApi.md#get_entity_metrics) | **GET** /api/v1/entities/workspaces/{workspaceId}/metrics/{objectId} | Get a Metric
[**get_entity_organization_settings**](EntitiesApi.md#get_entity_organization_settings) | **GET** /api/v1/entities/organizationSettings/{id} | Get Organization entity
[**get_entity_organizations**](EntitiesApi.md#get_entity_organizations) | **GET** /api/v1/entities/admin/organizations/{id} | Get Organizations
[**get_entity_themes**](EntitiesApi.md#get_entity_themes) | **GET** /api/v1/entities/themes/{id} | Get Theming
[**get_entity_user_data_filters**](EntitiesApi.md#get_entity_user_data_filters) | **GET** /api/v1/entities/workspaces/{workspaceId}/userDataFilters/{objectId} | Get a User Data Filter
[**get_entity_user_groups**](EntitiesApi.md#get_entity_user_groups) | **GET** /api/v1/entities/userGroups/{id} | Get UserGroup entity
[**get_entity_user_settings**](EntitiesApi.md#get_entity_user_settings) | **GET** /api/v1/entities/users/{userId}/userSettings/{id} | Get a setting for a user
[**get_entity_users**](EntitiesApi.md#get_entity_users) | **GET** /api/v1/entities/users/{id} | Get User entity
[**get_entity_visualization_objects**](EntitiesApi.md#get_entity_visualization_objects) | **GET** /api/v1/entities/workspaces/{workspaceId}/visualizationObjects/{objectId} | Get a Visualization Object
[**get_entity_workspace_data_filter_settings**](EntitiesApi.md#get_entity_workspace_data_filter_settings) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilterSettings/{objectId} | Get a Setting for Workspace Data Filter
[**get_entity_workspace_data_filters**](EntitiesApi.md#get_entity_workspace_data_filters) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilters/{objectId} | Get a Workspace Data Filter
[**get_entity_workspace_settings**](EntitiesApi.md#get_entity_workspace_settings) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceSettings/{objectId} | Get a Setting for Workspace
[**get_entity_workspaces**](EntitiesApi.md#get_entity_workspaces) | **GET** /api/v1/entities/workspaces/{id} | Get Workspace entity
[**get_organization**](EntitiesApi.md#get_organization) | **GET** /api/v1/entities/organization | Get current organization info
[**patch_entity_analytical_dashboards**](EntitiesApi.md#patch_entity_analytical_dashboards) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/analyticalDashboards/{objectId} | Patch a Dashboard
[**patch_entity_color_palettes**](EntitiesApi.md#patch_entity_color_palettes) | **PATCH** /api/v1/entities/colorPalettes/{id} | Patch Color Pallette
[**patch_entity_cookie_security_configurations**](EntitiesApi.md#patch_entity_cookie_security_configurations) | **PATCH** /api/v1/entities/admin/cookieSecurityConfigurations/{id} | Patch CookieSecurityConfiguration
[**patch_entity_csp_directives**](EntitiesApi.md#patch_entity_csp_directives) | **PATCH** /api/v1/entities/cspDirectives/{id} | Patch CSP Directives
[**patch_entity_custom_application_settings**](EntitiesApi.md#patch_entity_custom_application_settings) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/customApplicationSettings/{objectId} | Patch a Custom Application Setting
[**patch_entity_dashboard_plugins**](EntitiesApi.md#patch_entity_dashboard_plugins) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/dashboardPlugins/{objectId} | Patch a Plugin
[**patch_entity_data_sources**](EntitiesApi.md#patch_entity_data_sources) | **PATCH** /api/v1/entities/dataSources/{id} | Patch Data Source entity
[**patch_entity_filter_contexts**](EntitiesApi.md#patch_entity_filter_contexts) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/filterContexts/{objectId} | Patch a Context Filter
[**patch_entity_jwks**](EntitiesApi.md#patch_entity_jwks) | **PATCH** /api/v1/entities/jwks/{id} | Patch Jwk
[**patch_entity_metrics**](EntitiesApi.md#patch_entity_metrics) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/metrics/{objectId} | Patch a Metric
[**patch_entity_organization_settings**](EntitiesApi.md#patch_entity_organization_settings) | **PATCH** /api/v1/entities/organizationSettings/{id} | Patch Organization entity
[**patch_entity_organizations**](EntitiesApi.md#patch_entity_organizations) | **PATCH** /api/v1/entities/admin/organizations/{id} | Patch Organization
[**patch_entity_themes**](EntitiesApi.md#patch_entity_themes) | **PATCH** /api/v1/entities/themes/{id} | Patch Theming
[**patch_entity_user_data_filters**](EntitiesApi.md#patch_entity_user_data_filters) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/userDataFilters/{objectId} | Patch a User Data Filter
[**patch_entity_user_groups**](EntitiesApi.md#patch_entity_user_groups) | **PATCH** /api/v1/entities/userGroups/{id} | Patch UserGroup entity
[**patch_entity_users**](EntitiesApi.md#patch_entity_users) | **PATCH** /api/v1/entities/users/{id} | Patch User entity
[**patch_entity_visualization_objects**](EntitiesApi.md#patch_entity_visualization_objects) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/visualizationObjects/{objectId} | Patch a Visualization Object
[**patch_entity_workspace_data_filter_settings**](EntitiesApi.md#patch_entity_workspace_data_filter_settings) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilterSettings/{objectId} | Patch a Settings for Workspace Data Filter
[**patch_entity_workspace_data_filters**](EntitiesApi.md#patch_entity_workspace_data_filters) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilters/{objectId} | Patch a Workspace Data Filter
[**patch_entity_workspace_settings**](EntitiesApi.md#patch_entity_workspace_settings) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/workspaceSettings/{objectId} | Patch a Setting for Workspace
[**patch_entity_workspaces**](EntitiesApi.md#patch_entity_workspaces) | **PATCH** /api/v1/entities/workspaces/{id} | Patch Workspace entity
[**update_entity_analytical_dashboards**](EntitiesApi.md#update_entity_analytical_dashboards) | **PUT** /api/v1/entities/workspaces/{workspaceId}/analyticalDashboards/{objectId} | Put Dashboards
[**update_entity_api_tokens**](EntitiesApi.md#update_entity_api_tokens) | **PUT** /api/v1/entities/users/{userId}/apiTokens/{id} | Put new API token for the user
[**update_entity_color_palettes**](EntitiesApi.md#update_entity_color_palettes) | **PUT** /api/v1/entities/colorPalettes/{id} | Put Color Pallette
[**update_entity_cookie_security_configurations**](EntitiesApi.md#update_entity_cookie_security_configurations) | **PUT** /api/v1/entities/admin/cookieSecurityConfigurations/{id} | Put CookieSecurityConfiguration
[**update_entity_csp_directives**](EntitiesApi.md#update_entity_csp_directives) | **PUT** /api/v1/entities/cspDirectives/{id} | Put CSP Directives
[**update_entity_custom_application_settings**](EntitiesApi.md#update_entity_custom_application_settings) | **PUT** /api/v1/entities/workspaces/{workspaceId}/customApplicationSettings/{objectId} | Put a Custom Application Setting
[**update_entity_dashboard_plugins**](EntitiesApi.md#update_entity_dashboard_plugins) | **PUT** /api/v1/entities/workspaces/{workspaceId}/dashboardPlugins/{objectId} | Put a Plugin
[**update_entity_data_sources**](EntitiesApi.md#update_entity_data_sources) | **PUT** /api/v1/entities/dataSources/{id} | Put Data Source entity
[**update_entity_filter_contexts**](EntitiesApi.md#update_entity_filter_contexts) | **PUT** /api/v1/entities/workspaces/{workspaceId}/filterContexts/{objectId} | Put a Context Filter
[**update_entity_jwks**](EntitiesApi.md#update_entity_jwks) | **PUT** /api/v1/entities/jwks/{id} | Put Jwk
[**update_entity_metrics**](EntitiesApi.md#update_entity_metrics) | **PUT** /api/v1/entities/workspaces/{workspaceId}/metrics/{objectId} | Put a Metric
[**update_entity_organization_settings**](EntitiesApi.md#update_entity_organization_settings) | **PUT** /api/v1/entities/organizationSettings/{id} | Put Organization entity
[**update_entity_organizations**](EntitiesApi.md#update_entity_organizations) | **PUT** /api/v1/entities/admin/organizations/{id} | Put Organization
[**update_entity_themes**](EntitiesApi.md#update_entity_themes) | **PUT** /api/v1/entities/themes/{id} | Put Theming
[**update_entity_user_data_filters**](EntitiesApi.md#update_entity_user_data_filters) | **PUT** /api/v1/entities/workspaces/{workspaceId}/userDataFilters/{objectId} | Put a User Data Filter
[**update_entity_user_groups**](EntitiesApi.md#update_entity_user_groups) | **PUT** /api/v1/entities/userGroups/{id} | Put UserGroup entity
[**update_entity_user_settings**](EntitiesApi.md#update_entity_user_settings) | **PUT** /api/v1/entities/users/{userId}/userSettings/{id} | Put new user settings for the user
[**update_entity_users**](EntitiesApi.md#update_entity_users) | **PUT** /api/v1/entities/users/{id} | Put User entity
[**update_entity_visualization_objects**](EntitiesApi.md#update_entity_visualization_objects) | **PUT** /api/v1/entities/workspaces/{workspaceId}/visualizationObjects/{objectId} | Put a Visualization Object
[**update_entity_workspace_data_filter_settings**](EntitiesApi.md#update_entity_workspace_data_filter_settings) | **PUT** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilterSettings/{objectId} | Put a Settings for Workspace Data Filter
[**update_entity_workspace_data_filters**](EntitiesApi.md#update_entity_workspace_data_filters) | **PUT** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilters/{objectId} | Put a Workspace Data Filter
[**update_entity_workspace_settings**](EntitiesApi.md#update_entity_workspace_settings) | **PUT** /api/v1/entities/workspaces/{workspaceId}/workspaceSettings/{objectId} | Put a Setting for a Workspace
[**update_entity_workspaces**](EntitiesApi.md#update_entity_workspaces) | **PUT** /api/v1/entities/workspaces/{id} | Put Workspace entity


# **create_entity_analytical_dashboards**
> JsonApiAnalyticalDashboardOutDocument create_entity_analytical_dashboards(workspace_id, json_api_analytical_dashboard_post_optional_id_document)

Post Dashboards

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_analytical_dashboard_post_optional_id_document import JsonApiAnalyticalDashboardPostOptionalIdDocument
from gooddata_api_client.model.json_api_analytical_dashboard_out_document import JsonApiAnalyticalDashboardOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_analytical_dashboard_post_optional_id_document = JsonApiAnalyticalDashboardPostOptionalIdDocument(
        data=JsonApiAnalyticalDashboardPostOptionalId(
            attributes=JsonApiAnalyticalDashboardInAttributes(
                are_relations_valid=True,
                content={},
                description="description_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            type="analyticalDashboard",
        ),
    ) # JsonApiAnalyticalDashboardPostOptionalIdDocument | 
    include = [
        "include=visualizationObjects,analyticalDashboards,labels,metrics,datasets,filterContexts,dashboardPlugins",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = [
        "metaInclude=permissions,origin,accessInfo,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Dashboards
        api_response = api_instance.create_entity_analytical_dashboards(workspace_id, json_api_analytical_dashboard_post_optional_id_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_analytical_dashboards: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Dashboards
        api_response = api_instance.create_entity_analytical_dashboards(workspace_id, json_api_analytical_dashboard_post_optional_id_document, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_analytical_dashboards: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_analytical_dashboard_post_optional_id_document** | [**JsonApiAnalyticalDashboardPostOptionalIdDocument**](JsonApiAnalyticalDashboardPostOptionalIdDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiAnalyticalDashboardOutDocument**](JsonApiAnalyticalDashboardOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_entity_api_tokens**
> JsonApiApiTokenOutDocument create_entity_api_tokens(user_id, json_api_api_token_in_document)

Post a new API token for the user

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_api_token_out_document import JsonApiApiTokenOutDocument
from gooddata_api_client.model.json_api_api_token_in_document import JsonApiApiTokenInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    user_id = "userId_example" # str | 
    json_api_api_token_in_document = JsonApiApiTokenInDocument(
        data=JsonApiApiTokenIn(
            id="id1",
            type="apiToken",
        ),
    ) # JsonApiApiTokenInDocument | 

    # example passing only required values which don't have defaults set
    try:
        # Post a new API token for the user
        api_response = api_instance.create_entity_api_tokens(user_id, json_api_api_token_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_api_tokens: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  |
 **json_api_api_token_in_document** | [**JsonApiApiTokenInDocument**](JsonApiApiTokenInDocument.md)|  |

### Return type

[**JsonApiApiTokenOutDocument**](JsonApiApiTokenOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_entity_color_palettes**
> JsonApiColorPaletteOutDocument create_entity_color_palettes(json_api_color_palette_in_document)

Post Color Pallettes

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_color_palette_in_document import JsonApiColorPaletteInDocument
from gooddata_api_client.model.json_api_color_palette_out_document import JsonApiColorPaletteOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    json_api_color_palette_in_document = JsonApiColorPaletteInDocument(
        data=JsonApiColorPaletteIn(
            attributes=JsonApiColorPaletteInAttributes(
                content={},
                name="name_example",
            ),
            id="id1",
            type="colorPalette",
        ),
    ) # JsonApiColorPaletteInDocument | 

    # example passing only required values which don't have defaults set
    try:
        # Post Color Pallettes
        api_response = api_instance.create_entity_color_palettes(json_api_color_palette_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_color_palettes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_color_palette_in_document** | [**JsonApiColorPaletteInDocument**](JsonApiColorPaletteInDocument.md)|  |

### Return type

[**JsonApiColorPaletteOutDocument**](JsonApiColorPaletteOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_entity_csp_directives**
> JsonApiCspDirectiveOutDocument create_entity_csp_directives(json_api_csp_directive_in_document)

Post CSP Directives

 Context Security Police Directive

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_csp_directive_out_document import JsonApiCspDirectiveOutDocument
from gooddata_api_client.model.json_api_csp_directive_in_document import JsonApiCspDirectiveInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    json_api_csp_directive_in_document = JsonApiCspDirectiveInDocument(
        data=JsonApiCspDirectiveIn(
            attributes=JsonApiCspDirectiveInAttributes(
                sources=[
                    "sources_example",
                ],
            ),
            id="id1",
            type="cspDirective",
        ),
    ) # JsonApiCspDirectiveInDocument | 

    # example passing only required values which don't have defaults set
    try:
        # Post CSP Directives
        api_response = api_instance.create_entity_csp_directives(json_api_csp_directive_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_csp_directives: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_csp_directive_in_document** | [**JsonApiCspDirectiveInDocument**](JsonApiCspDirectiveInDocument.md)|  |

### Return type

[**JsonApiCspDirectiveOutDocument**](JsonApiCspDirectiveOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_entity_custom_application_settings**
> JsonApiCustomApplicationSettingOutDocument create_entity_custom_application_settings(workspace_id, json_api_custom_application_setting_post_optional_id_document)

Post Custom Application Settings

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_custom_application_setting_out_document import JsonApiCustomApplicationSettingOutDocument
from gooddata_api_client.model.json_api_custom_application_setting_post_optional_id_document import JsonApiCustomApplicationSettingPostOptionalIdDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_custom_application_setting_post_optional_id_document = JsonApiCustomApplicationSettingPostOptionalIdDocument(
        data=JsonApiCustomApplicationSettingPostOptionalId(
            attributes=JsonApiCustomApplicationSettingInAttributes(
                application_name="application_name_example",
                content={},
            ),
            id="id1",
            type="customApplicationSetting",
        ),
    ) # JsonApiCustomApplicationSettingPostOptionalIdDocument | 
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Custom Application Settings
        api_response = api_instance.create_entity_custom_application_settings(workspace_id, json_api_custom_application_setting_post_optional_id_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_custom_application_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Custom Application Settings
        api_response = api_instance.create_entity_custom_application_settings(workspace_id, json_api_custom_application_setting_post_optional_id_document, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_custom_application_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_custom_application_setting_post_optional_id_document** | [**JsonApiCustomApplicationSettingPostOptionalIdDocument**](JsonApiCustomApplicationSettingPostOptionalIdDocument.md)|  |
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiCustomApplicationSettingOutDocument**](JsonApiCustomApplicationSettingOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_entity_dashboard_plugins**
> JsonApiDashboardPluginOutDocument create_entity_dashboard_plugins(workspace_id, json_api_dashboard_plugin_post_optional_id_document)

Post Plugins

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_dashboard_plugin_post_optional_id_document import JsonApiDashboardPluginPostOptionalIdDocument
from gooddata_api_client.model.json_api_dashboard_plugin_out_document import JsonApiDashboardPluginOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_dashboard_plugin_post_optional_id_document = JsonApiDashboardPluginPostOptionalIdDocument(
        data=JsonApiDashboardPluginPostOptionalId(
            attributes=JsonApiDashboardPluginInAttributes(
                are_relations_valid=True,
                content={},
                description="description_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            type="dashboardPlugin",
        ),
    ) # JsonApiDashboardPluginPostOptionalIdDocument | 
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Plugins
        api_response = api_instance.create_entity_dashboard_plugins(workspace_id, json_api_dashboard_plugin_post_optional_id_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_dashboard_plugins: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Plugins
        api_response = api_instance.create_entity_dashboard_plugins(workspace_id, json_api_dashboard_plugin_post_optional_id_document, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_dashboard_plugins: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_dashboard_plugin_post_optional_id_document** | [**JsonApiDashboardPluginPostOptionalIdDocument**](JsonApiDashboardPluginPostOptionalIdDocument.md)|  |
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiDashboardPluginOutDocument**](JsonApiDashboardPluginOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_entity_data_sources**
> JsonApiDataSourceOutDocument create_entity_data_sources(json_api_data_source_in_document)

Post Data Sources

Data Source - represents data source for the workspace

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_data_source_in_document import JsonApiDataSourceInDocument
from gooddata_api_client.model.json_api_data_source_out_document import JsonApiDataSourceOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    json_api_data_source_in_document = JsonApiDataSourceInDocument(
        data=JsonApiDataSourceIn(
            attributes=JsonApiDataSourceInAttributes(
                cache_path=[
                    "cache_path_example",
                ],
                enable_caching=False,
                name="name_example",
                parameters=[
                    JsonApiDataSourceInAttributesParametersInner(
                        name="name_example",
                        value="value_example",
                    ),
                ],
                password="password_example",
                schema="schema_example",
                token="token_example",
                type="POSTGRESQL",
                url="url_example",
                username="username_example",
            ),
            id="id1",
            type="dataSource",
        ),
    ) # JsonApiDataSourceInDocument | 
    meta_include = [
        "metaInclude=permissions,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Data Sources
        api_response = api_instance.create_entity_data_sources(json_api_data_source_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_data_sources: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Data Sources
        api_response = api_instance.create_entity_data_sources(json_api_data_source_in_document, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_data_sources: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_data_source_in_document** | [**JsonApiDataSourceInDocument**](JsonApiDataSourceInDocument.md)|  |
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiDataSourceOutDocument**](JsonApiDataSourceOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_entity_filter_contexts**
> JsonApiFilterContextOutDocument create_entity_filter_contexts(workspace_id, json_api_filter_context_post_optional_id_document)

Post Context Filters

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_filter_context_post_optional_id_document import JsonApiFilterContextPostOptionalIdDocument
from gooddata_api_client.model.json_api_filter_context_out_document import JsonApiFilterContextOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_filter_context_post_optional_id_document = JsonApiFilterContextPostOptionalIdDocument(
        data=JsonApiFilterContextPostOptionalId(
            attributes=JsonApiAnalyticalDashboardInAttributes(
                are_relations_valid=True,
                content={},
                description="description_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            type="filterContext",
        ),
    ) # JsonApiFilterContextPostOptionalIdDocument | 
    include = [
        "include=attributes,datasets,labels",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Context Filters
        api_response = api_instance.create_entity_filter_contexts(workspace_id, json_api_filter_context_post_optional_id_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_filter_contexts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Context Filters
        api_response = api_instance.create_entity_filter_contexts(workspace_id, json_api_filter_context_post_optional_id_document, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_filter_contexts: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_filter_context_post_optional_id_document** | [**JsonApiFilterContextPostOptionalIdDocument**](JsonApiFilterContextPostOptionalIdDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiFilterContextOutDocument**](JsonApiFilterContextOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_entity_jwks**
> JsonApiJwkOutDocument create_entity_jwks(json_api_jwk_in_document)

Post Jwks

Creates JSON web key - used to verify JSON web tokens (Jwts)

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_jwk_in_document import JsonApiJwkInDocument
from gooddata_api_client.model.json_api_jwk_out_document import JsonApiJwkOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    json_api_jwk_in_document = JsonApiJwkInDocument(
        data=JsonApiJwkIn(
            attributes=JsonApiJwkInAttributes(
                content=JsonApiJwkInAttributesContent(),
            ),
            id="id1",
            type="jwk",
        ),
    ) # JsonApiJwkInDocument | 

    # example passing only required values which don't have defaults set
    try:
        # Post Jwks
        api_response = api_instance.create_entity_jwks(json_api_jwk_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_jwks: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_jwk_in_document** | [**JsonApiJwkInDocument**](JsonApiJwkInDocument.md)|  |

### Return type

[**JsonApiJwkOutDocument**](JsonApiJwkOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_entity_metrics**
> JsonApiMetricOutDocument create_entity_metrics(workspace_id, json_api_metric_post_optional_id_document)

Post Metrics

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_metric_post_optional_id_document import JsonApiMetricPostOptionalIdDocument
from gooddata_api_client.model.json_api_metric_out_document import JsonApiMetricOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_metric_post_optional_id_document = JsonApiMetricPostOptionalIdDocument(
        data=JsonApiMetricPostOptionalId(
            attributes=JsonApiMetricInAttributes(
                are_relations_valid=True,
                content=JsonApiMetricInAttributesContent(
                    format="format_example",
                    maql="maql_example",
                ),
                description="description_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            type="metric",
        ),
    ) # JsonApiMetricPostOptionalIdDocument | 
    include = [
        "include=facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Metrics
        api_response = api_instance.create_entity_metrics(workspace_id, json_api_metric_post_optional_id_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_metrics: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Metrics
        api_response = api_instance.create_entity_metrics(workspace_id, json_api_metric_post_optional_id_document, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_metrics: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_metric_post_optional_id_document** | [**JsonApiMetricPostOptionalIdDocument**](JsonApiMetricPostOptionalIdDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiMetricOutDocument**](JsonApiMetricOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_entity_organization_settings**
> JsonApiOrganizationSettingOutDocument create_entity_organization_settings(json_api_organization_setting_in_document)

Post Organization Setting entities

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_organization_setting_in_document import JsonApiOrganizationSettingInDocument
from gooddata_api_client.model.json_api_organization_setting_out_document import JsonApiOrganizationSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    json_api_organization_setting_in_document = JsonApiOrganizationSettingInDocument(
        data=JsonApiOrganizationSettingIn(
            attributes=JsonApiOrganizationSettingInAttributes(
                content={},
                type="TIMEZONE",
            ),
            id="id1",
            type="organizationSetting",
        ),
    ) # JsonApiOrganizationSettingInDocument | 

    # example passing only required values which don't have defaults set
    try:
        # Post Organization Setting entities
        api_response = api_instance.create_entity_organization_settings(json_api_organization_setting_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_organization_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_organization_setting_in_document** | [**JsonApiOrganizationSettingInDocument**](JsonApiOrganizationSettingInDocument.md)|  |

### Return type

[**JsonApiOrganizationSettingOutDocument**](JsonApiOrganizationSettingOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_entity_themes**
> JsonApiThemeOutDocument create_entity_themes(json_api_theme_in_document)

Post Theming

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_theme_in_document import JsonApiThemeInDocument
from gooddata_api_client.model.json_api_theme_out_document import JsonApiThemeOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    json_api_theme_in_document = JsonApiThemeInDocument(
        data=JsonApiThemeIn(
            attributes=JsonApiColorPaletteInAttributes(
                content={},
                name="name_example",
            ),
            id="id1",
            type="theme",
        ),
    ) # JsonApiThemeInDocument | 

    # example passing only required values which don't have defaults set
    try:
        # Post Theming
        api_response = api_instance.create_entity_themes(json_api_theme_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_themes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_theme_in_document** | [**JsonApiThemeInDocument**](JsonApiThemeInDocument.md)|  |

### Return type

[**JsonApiThemeOutDocument**](JsonApiThemeOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_entity_user_data_filters**
> JsonApiUserDataFilterOutDocument create_entity_user_data_filters(workspace_id, json_api_user_data_filter_post_optional_id_document)

Post User Data Filters

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_user_data_filter_out_document import JsonApiUserDataFilterOutDocument
from gooddata_api_client.model.json_api_user_data_filter_post_optional_id_document import JsonApiUserDataFilterPostOptionalIdDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_user_data_filter_post_optional_id_document = JsonApiUserDataFilterPostOptionalIdDocument(
        data=JsonApiUserDataFilterPostOptionalId(
            attributes=JsonApiUserDataFilterInAttributes(
                are_relations_valid=True,
                description="description_example",
                maql="maql_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            relationships=JsonApiUserDataFilterInRelationships(
                user=JsonApiOrganizationOutRelationshipsBootstrapUser(
                    data=JsonApiUserToOneLinkage(None),
                ),
                user_group=JsonApiOrganizationOutRelationshipsBootstrapUserGroup(
                    data=JsonApiUserGroupToOneLinkage(None),
                ),
            ),
            type="userDataFilter",
        ),
    ) # JsonApiUserDataFilterPostOptionalIdDocument | 
    include = [
        "include=user,userGroup,facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post User Data Filters
        api_response = api_instance.create_entity_user_data_filters(workspace_id, json_api_user_data_filter_post_optional_id_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_user_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post User Data Filters
        api_response = api_instance.create_entity_user_data_filters(workspace_id, json_api_user_data_filter_post_optional_id_document, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_user_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_user_data_filter_post_optional_id_document** | [**JsonApiUserDataFilterPostOptionalIdDocument**](JsonApiUserDataFilterPostOptionalIdDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiUserDataFilterOutDocument**](JsonApiUserDataFilterOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_entity_user_groups**
> JsonApiUserGroupOutDocument create_entity_user_groups(json_api_user_group_in_document)

Post User Group entities

User Group - creates tree-like structure for categorizing users

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_user_group_in_document import JsonApiUserGroupInDocument
from gooddata_api_client.model.json_api_user_group_out_document import JsonApiUserGroupOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    json_api_user_group_in_document = JsonApiUserGroupInDocument(
        data=JsonApiUserGroupIn(
            attributes=JsonApiUserGroupInAttributes(
                name="name_example",
            ),
            id="id1",
            relationships=JsonApiUserGroupInRelationships(
                parents=JsonApiUserGroupInRelationshipsParents(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        ),
                    ]),
                ),
            ),
            type="userGroup",
        ),
    ) # JsonApiUserGroupInDocument | 
    include = [
        "include=parents",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post User Group entities
        api_response = api_instance.create_entity_user_groups(json_api_user_group_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_user_groups: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post User Group entities
        api_response = api_instance.create_entity_user_groups(json_api_user_group_in_document, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_user_groups: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_user_group_in_document** | [**JsonApiUserGroupInDocument**](JsonApiUserGroupInDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiUserGroupOutDocument**](JsonApiUserGroupOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_entity_user_settings**
> JsonApiUserSettingOutDocument create_entity_user_settings(user_id, json_api_user_setting_in_document)

Post new user settings for the user

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_user_setting_out_document import JsonApiUserSettingOutDocument
from gooddata_api_client.model.json_api_user_setting_in_document import JsonApiUserSettingInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    user_id = "userId_example" # str | 
    json_api_user_setting_in_document = JsonApiUserSettingInDocument(
        data=JsonApiUserSettingIn(
            attributes=JsonApiOrganizationSettingInAttributes(
                content={},
                type="TIMEZONE",
            ),
            id="id1",
            type="userSetting",
        ),
    ) # JsonApiUserSettingInDocument | 

    # example passing only required values which don't have defaults set
    try:
        # Post new user settings for the user
        api_response = api_instance.create_entity_user_settings(user_id, json_api_user_setting_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_user_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  |
 **json_api_user_setting_in_document** | [**JsonApiUserSettingInDocument**](JsonApiUserSettingInDocument.md)|  |

### Return type

[**JsonApiUserSettingOutDocument**](JsonApiUserSettingOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_entity_users**
> JsonApiUserOutDocument create_entity_users(json_api_user_in_document)

Post User entities

User - represents entity interacting with platform

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_user_in_document import JsonApiUserInDocument
from gooddata_api_client.model.json_api_user_out_document import JsonApiUserOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    json_api_user_in_document = JsonApiUserInDocument(
        data=JsonApiUserIn(
            attributes=JsonApiUserInAttributes(
                authentication_id="authentication_id_example",
                email="email_example",
                firstname="firstname_example",
                lastname="lastname_example",
            ),
            id="id1",
            relationships=JsonApiUserInRelationships(
                user_groups=JsonApiUserGroupInRelationshipsParents(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        ),
                    ]),
                ),
            ),
            type="user",
        ),
    ) # JsonApiUserInDocument | 
    include = [
        "include=userGroups",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post User entities
        api_response = api_instance.create_entity_users(json_api_user_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_users: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post User entities
        api_response = api_instance.create_entity_users(json_api_user_in_document, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_users: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_user_in_document** | [**JsonApiUserInDocument**](JsonApiUserInDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiUserOutDocument**](JsonApiUserOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_entity_visualization_objects**
> JsonApiVisualizationObjectOutDocument create_entity_visualization_objects(workspace_id, json_api_visualization_object_post_optional_id_document)

Post Visualization Objects

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_visualization_object_out_document import JsonApiVisualizationObjectOutDocument
from gooddata_api_client.model.json_api_visualization_object_post_optional_id_document import JsonApiVisualizationObjectPostOptionalIdDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_visualization_object_post_optional_id_document = JsonApiVisualizationObjectPostOptionalIdDocument(
        data=JsonApiVisualizationObjectPostOptionalId(
            attributes=JsonApiAnalyticalDashboardInAttributes(
                are_relations_valid=True,
                content={},
                description="description_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            type="visualizationObject",
        ),
    ) # JsonApiVisualizationObjectPostOptionalIdDocument | 
    include = [
        "include=facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Visualization Objects
        api_response = api_instance.create_entity_visualization_objects(workspace_id, json_api_visualization_object_post_optional_id_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_visualization_objects: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Visualization Objects
        api_response = api_instance.create_entity_visualization_objects(workspace_id, json_api_visualization_object_post_optional_id_document, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_visualization_objects: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_visualization_object_post_optional_id_document** | [**JsonApiVisualizationObjectPostOptionalIdDocument**](JsonApiVisualizationObjectPostOptionalIdDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiVisualizationObjectOutDocument**](JsonApiVisualizationObjectOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_entity_workspace_data_filter_settings**
> JsonApiWorkspaceDataFilterSettingOutDocument create_entity_workspace_data_filter_settings(workspace_id, json_api_workspace_data_filter_setting_in_document)

Post Settings for Workspace Data Filters

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_workspace_data_filter_setting_in_document import JsonApiWorkspaceDataFilterSettingInDocument
from gooddata_api_client.model.json_api_workspace_data_filter_setting_out_document import JsonApiWorkspaceDataFilterSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_workspace_data_filter_setting_in_document = JsonApiWorkspaceDataFilterSettingInDocument(
        data=JsonApiWorkspaceDataFilterSettingIn(
            attributes=JsonApiWorkspaceDataFilterSettingInAttributes(
                description="description_example",
                filter_values=[
                    "filter_values_example",
                ],
                title="title_example",
            ),
            id="id1",
            relationships=JsonApiWorkspaceDataFilterSettingInRelationships(
                workspace_data_filter=JsonApiWorkspaceDataFilterSettingInRelationshipsWorkspaceDataFilter(
                    data=JsonApiWorkspaceDataFilterToOneLinkage(None),
                ),
            ),
            type="workspaceDataFilterSetting",
        ),
    ) # JsonApiWorkspaceDataFilterSettingInDocument | 
    include = [
        "include=workspaceDataFilter",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Settings for Workspace Data Filters
        api_response = api_instance.create_entity_workspace_data_filter_settings(workspace_id, json_api_workspace_data_filter_setting_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_workspace_data_filter_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Settings for Workspace Data Filters
        api_response = api_instance.create_entity_workspace_data_filter_settings(workspace_id, json_api_workspace_data_filter_setting_in_document, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_workspace_data_filter_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_workspace_data_filter_setting_in_document** | [**JsonApiWorkspaceDataFilterSettingInDocument**](JsonApiWorkspaceDataFilterSettingInDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiWorkspaceDataFilterSettingOutDocument**](JsonApiWorkspaceDataFilterSettingOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_entity_workspace_data_filters**
> JsonApiWorkspaceDataFilterOutDocument create_entity_workspace_data_filters(workspace_id, json_api_workspace_data_filter_in_document)

Post Workspace Data Filters

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_workspace_data_filter_out_document import JsonApiWorkspaceDataFilterOutDocument
from gooddata_api_client.model.json_api_workspace_data_filter_in_document import JsonApiWorkspaceDataFilterInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_workspace_data_filter_in_document = JsonApiWorkspaceDataFilterInDocument(
        data=JsonApiWorkspaceDataFilterIn(
            attributes=JsonApiWorkspaceDataFilterInAttributes(
                column_name="column_name_example",
                description="description_example",
                title="title_example",
            ),
            id="id1",
            relationships=JsonApiWorkspaceDataFilterInRelationships(
                filter_settings=JsonApiWorkspaceDataFilterInRelationshipsFilterSettings(
                    data=JsonApiWorkspaceDataFilterSettingToManyLinkage([
                        JsonApiWorkspaceDataFilterSettingLinkage(
                            id="id_example",
                            type="workspaceDataFilterSetting",
                        ),
                    ]),
                ),
            ),
            type="workspaceDataFilter",
        ),
    ) # JsonApiWorkspaceDataFilterInDocument | 
    include = [
        "include=filterSettings",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Workspace Data Filters
        api_response = api_instance.create_entity_workspace_data_filters(workspace_id, json_api_workspace_data_filter_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_workspace_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Workspace Data Filters
        api_response = api_instance.create_entity_workspace_data_filters(workspace_id, json_api_workspace_data_filter_in_document, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_workspace_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_workspace_data_filter_in_document** | [**JsonApiWorkspaceDataFilterInDocument**](JsonApiWorkspaceDataFilterInDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiWorkspaceDataFilterOutDocument**](JsonApiWorkspaceDataFilterOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_entity_workspace_settings**
> JsonApiWorkspaceSettingOutDocument create_entity_workspace_settings(workspace_id, json_api_workspace_setting_post_optional_id_document)

Post Settings for Workspaces

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_workspace_setting_post_optional_id_document import JsonApiWorkspaceSettingPostOptionalIdDocument
from gooddata_api_client.model.json_api_workspace_setting_out_document import JsonApiWorkspaceSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_workspace_setting_post_optional_id_document = JsonApiWorkspaceSettingPostOptionalIdDocument(
        data=JsonApiWorkspaceSettingPostOptionalId(
            attributes=JsonApiOrganizationSettingInAttributes(
                content={},
                type="TIMEZONE",
            ),
            id="id1",
            type="workspaceSetting",
        ),
    ) # JsonApiWorkspaceSettingPostOptionalIdDocument | 
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Settings for Workspaces
        api_response = api_instance.create_entity_workspace_settings(workspace_id, json_api_workspace_setting_post_optional_id_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_workspace_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Settings for Workspaces
        api_response = api_instance.create_entity_workspace_settings(workspace_id, json_api_workspace_setting_post_optional_id_document, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_workspace_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_workspace_setting_post_optional_id_document** | [**JsonApiWorkspaceSettingPostOptionalIdDocument**](JsonApiWorkspaceSettingPostOptionalIdDocument.md)|  |
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiWorkspaceSettingOutDocument**](JsonApiWorkspaceSettingOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_entity_workspaces**
> JsonApiWorkspaceOutDocument create_entity_workspaces(json_api_workspace_in_document)

Post Workspace entities

Space of the shared interest

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_workspace_out_document import JsonApiWorkspaceOutDocument
from gooddata_api_client.model.json_api_workspace_in_document import JsonApiWorkspaceInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    json_api_workspace_in_document = JsonApiWorkspaceInDocument(
        data=JsonApiWorkspaceIn(
            attributes=JsonApiWorkspaceInAttributes(
                cache_extra_limit=1,
                description="description_example",
                early_access="early_access_example",
                name="name_example",
                prefix="/6bUUGjjNSwg0_bs",
            ),
            id="id1",
            relationships=JsonApiWorkspaceInRelationships(
                parent=JsonApiWorkspaceInRelationshipsParent(
                    data=JsonApiWorkspaceToOneLinkage(None),
                ),
            ),
            type="workspace",
        ),
    ) # JsonApiWorkspaceInDocument | 
    include = [
        "include=parent",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = [
        "metaInclude=config,permissions,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Workspace entities
        api_response = api_instance.create_entity_workspaces(json_api_workspace_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_workspaces: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Workspace entities
        api_response = api_instance.create_entity_workspaces(json_api_workspace_in_document, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->create_entity_workspaces: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_workspace_in_document** | [**JsonApiWorkspaceInDocument**](JsonApiWorkspaceInDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiWorkspaceOutDocument**](JsonApiWorkspaceOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_analytical_dashboards**
> delete_entity_analytical_dashboards(workspace_id, object_id)

Delete a Dashboard

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Dashboard
        api_instance.delete_entity_analytical_dashboards(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_analytical_dashboards: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Dashboard
        api_instance.delete_entity_analytical_dashboards(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_analytical_dashboards: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_api_tokens**
> delete_entity_api_tokens(user_id, id)

Delete an API Token for a user

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    user_id = "userId_example" # str | 
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=bearerToken==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete an API Token for a user
        api_instance.delete_entity_api_tokens(user_id, id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_api_tokens: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete an API Token for a user
        api_instance.delete_entity_api_tokens(user_id, id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_api_tokens: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  |
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_color_palettes**
> delete_entity_color_palettes(id)

Delete a Color Pallette

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=name==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Color Pallette
        api_instance.delete_entity_color_palettes(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_color_palettes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Color Pallette
        api_instance.delete_entity_color_palettes(id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_color_palettes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_csp_directives**
> delete_entity_csp_directives(id)

Delete CSP Directives

 Context Security Police Directive

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=sources==v1,v2,v3" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete CSP Directives
        api_instance.delete_entity_csp_directives(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_csp_directives: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete CSP Directives
        api_instance.delete_entity_csp_directives(id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_csp_directives: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_custom_application_settings**
> delete_entity_custom_application_settings(workspace_id, object_id)

Delete a Custom Application Setting

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=applicationName==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Custom Application Setting
        api_instance.delete_entity_custom_application_settings(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_custom_application_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Custom Application Setting
        api_instance.delete_entity_custom_application_settings(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_custom_application_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_dashboard_plugins**
> delete_entity_dashboard_plugins(workspace_id, object_id)

Delete a Plugin

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Plugin
        api_instance.delete_entity_dashboard_plugins(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_dashboard_plugins: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Plugin
        api_instance.delete_entity_dashboard_plugins(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_dashboard_plugins: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_data_sources**
> delete_entity_data_sources(id)

Delete Data Source entity

Data Source - represents data source for the workspace

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=name==someString;type==DatabaseTypeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete Data Source entity
        api_instance.delete_entity_data_sources(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_data_sources: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete Data Source entity
        api_instance.delete_entity_data_sources(id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_data_sources: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_filter_contexts**
> delete_entity_filter_contexts(workspace_id, object_id)

Delete a Context Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Context Filter
        api_instance.delete_entity_filter_contexts(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_filter_contexts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Context Filter
        api_instance.delete_entity_filter_contexts(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_filter_contexts: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_jwks**
> delete_entity_jwks(id)

Delete Jwk

Deletes JSON web key - used to verify JSON web tokens (Jwts)

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=content==JwkSpecificationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete Jwk
        api_instance.delete_entity_jwks(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_jwks: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete Jwk
        api_instance.delete_entity_jwks(id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_jwks: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_metrics**
> delete_entity_metrics(workspace_id, object_id)

Delete a Metric

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Metric
        api_instance.delete_entity_metrics(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_metrics: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Metric
        api_instance.delete_entity_metrics(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_metrics: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_organization_settings**
> delete_entity_organization_settings(id)

Delete Organization entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=content==JsonNodeValue;type==SettingConfigurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete Organization entity
        api_instance.delete_entity_organization_settings(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_organization_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete Organization entity
        api_instance.delete_entity_organization_settings(id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_organization_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_themes**
> delete_entity_themes(id)

Delete Theming

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=name==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete Theming
        api_instance.delete_entity_themes(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_themes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete Theming
        api_instance.delete_entity_themes(id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_themes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_user_data_filters**
> delete_entity_user_data_filters(workspace_id, object_id)

Delete a User Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString;user.id==321;userGroup.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a User Data Filter
        api_instance.delete_entity_user_data_filters(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_user_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a User Data Filter
        api_instance.delete_entity_user_data_filters(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_user_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_user_groups**
> delete_entity_user_groups(id)

Delete UserGroup entity

User Group - creates tree-like structure for categorizing users

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=name==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete UserGroup entity
        api_instance.delete_entity_user_groups(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_user_groups: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete UserGroup entity
        api_instance.delete_entity_user_groups(id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_user_groups: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_user_settings**
> delete_entity_user_settings(user_id, id)

Delete a setting for a user

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    user_id = "userId_example" # str | 
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=content==JsonNodeValue;type==SettingConfigurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a setting for a user
        api_instance.delete_entity_user_settings(user_id, id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_user_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a setting for a user
        api_instance.delete_entity_user_settings(user_id, id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_user_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  |
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_users**
> delete_entity_users(id)

Delete User entity

User - represents entity interacting with platform

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=authenticationId==someString;firstname==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete User entity
        api_instance.delete_entity_users(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_users: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete User entity
        api_instance.delete_entity_users(id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_users: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_visualization_objects**
> delete_entity_visualization_objects(workspace_id, object_id)

Delete a Visualization Object

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Visualization Object
        api_instance.delete_entity_visualization_objects(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_visualization_objects: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Visualization Object
        api_instance.delete_entity_visualization_objects(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_visualization_objects: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_workspace_data_filter_settings**
> delete_entity_workspace_data_filter_settings(workspace_id, object_id)

Delete a Settings for Workspace Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString;workspaceDataFilter.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Settings for Workspace Data Filter
        api_instance.delete_entity_workspace_data_filter_settings(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_workspace_data_filter_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Settings for Workspace Data Filter
        api_instance.delete_entity_workspace_data_filter_settings(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_workspace_data_filter_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_workspace_data_filters**
> delete_entity_workspace_data_filters(workspace_id, object_id)

Delete a Workspace Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Workspace Data Filter
        api_instance.delete_entity_workspace_data_filters(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_workspace_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Workspace Data Filter
        api_instance.delete_entity_workspace_data_filters(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_workspace_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_workspace_settings**
> delete_entity_workspace_settings(workspace_id, object_id)

Delete a Setting for Workspace

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=content==JsonNodeValue;type==SettingConfigurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Setting for Workspace
        api_instance.delete_entity_workspace_settings(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_workspace_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Setting for Workspace
        api_instance.delete_entity_workspace_settings(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_workspace_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_workspaces**
> delete_entity_workspaces(id)

Delete Workspace entity

Space of the shared interest

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=name==someString;earlyAccess==someString;parent.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete Workspace entity
        api_instance.delete_entity_workspaces(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_workspaces: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete Workspace entity
        api_instance.delete_entity_workspaces(id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->delete_entity_workspaces: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_analytical_dashboards**
> JsonApiAnalyticalDashboardOutList get_all_entities_analytical_dashboards(workspace_id)

Get all Dashboards

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_analytical_dashboard_out_list import JsonApiAnalyticalDashboardOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=visualizationObjects,analyticalDashboards,labels,metrics,datasets,filterContexts,dashboardPlugins",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=permissions,origin,accessInfo,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get all Dashboards
        api_response = api_instance.get_all_entities_analytical_dashboards(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_analytical_dashboards: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Dashboards
        api_response = api_instance.get_all_entities_analytical_dashboards(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_analytical_dashboards: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiAnalyticalDashboardOutList**](JsonApiAnalyticalDashboardOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_api_tokens**
> JsonApiApiTokenOutList get_all_entities_api_tokens(user_id)

List all api tokens for a user

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_api_token_out_list import JsonApiApiTokenOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    user_id = "userId_example" # str | 
    filter = "filter=bearerToken==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)

    # example passing only required values which don't have defaults set
    try:
        # List all api tokens for a user
        api_response = api_instance.get_all_entities_api_tokens(user_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_api_tokens: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # List all api tokens for a user
        api_response = api_instance.get_all_entities_api_tokens(user_id, filter=filter, page=page, size=size, sort=sort)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_api_tokens: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]

### Return type

[**JsonApiApiTokenOutList**](JsonApiApiTokenOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_attributes**
> JsonApiAttributeOutList get_all_entities_attributes(workspace_id)

Get all Attributes

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_attribute_out_list import JsonApiAttributeOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "filter=title==someString;description==someString;dataset.id==321;defaultView.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=dataset,defaultView,labels",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get all Attributes
        api_response = api_instance.get_all_entities_attributes(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_attributes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Attributes
        api_response = api_instance.get_all_entities_attributes(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_attributes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiAttributeOutList**](JsonApiAttributeOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_color_palettes**
> JsonApiColorPaletteOutList get_all_entities_color_palettes()

Get all Color Pallettes

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_color_palette_out_list import JsonApiColorPaletteOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    filter = "filter=name==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Color Pallettes
        api_response = api_instance.get_all_entities_color_palettes(filter=filter, page=page, size=size, sort=sort)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_color_palettes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]

### Return type

[**JsonApiColorPaletteOutList**](JsonApiColorPaletteOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_csp_directives**
> JsonApiCspDirectiveOutList get_all_entities_csp_directives()

Get CSP Directives

 Context Security Police Directive

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_csp_directive_out_list import JsonApiCspDirectiveOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    filter = "filter=sources==v1,v2,v3" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get CSP Directives
        api_response = api_instance.get_all_entities_csp_directives(filter=filter, page=page, size=size, sort=sort)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_csp_directives: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]

### Return type

[**JsonApiCspDirectiveOutList**](JsonApiCspDirectiveOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_custom_application_settings**
> JsonApiCustomApplicationSettingOutList get_all_entities_custom_application_settings(workspace_id)

Get all Custom Application Settings

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_custom_application_setting_out_list import JsonApiCustomApplicationSettingOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "filter=applicationName==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get all Custom Application Settings
        api_response = api_instance.get_all_entities_custom_application_settings(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_custom_application_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Custom Application Settings
        api_response = api_instance.get_all_entities_custom_application_settings(workspace_id, origin=origin, filter=filter, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_custom_application_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiCustomApplicationSettingOutList**](JsonApiCustomApplicationSettingOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_dashboard_plugins**
> JsonApiDashboardPluginOutList get_all_entities_dashboard_plugins(workspace_id)

Get all Plugins

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_dashboard_plugin_out_list import JsonApiDashboardPluginOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get all Plugins
        api_response = api_instance.get_all_entities_dashboard_plugins(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_dashboard_plugins: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Plugins
        api_response = api_instance.get_all_entities_dashboard_plugins(workspace_id, origin=origin, filter=filter, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_dashboard_plugins: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiDashboardPluginOutList**](JsonApiDashboardPluginOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_data_source_identifiers**
> JsonApiDataSourceIdentifierOutList get_all_entities_data_source_identifiers()

Get all Data Source Identifiers

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_data_source_identifier_out_list import JsonApiDataSourceIdentifierOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    filter = "filter=name==someString;schema==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = [
        "metaInclude=permissions,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Data Source Identifiers
        api_response = api_instance.get_all_entities_data_source_identifiers(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_data_source_identifiers: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiDataSourceIdentifierOutList**](JsonApiDataSourceIdentifierOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_data_source_tables**
> JsonApiDataSourceTableOutList get_all_entities_data_source_tables(data_source_id)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_data_source_table_out_list import JsonApiDataSourceTableOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    data_source_id = "dataSourceId_example" # str | 
    filter = "filter=path==v1,v2,v3;type==DataSourceTableTypeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_all_entities_data_source_tables(data_source_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_data_source_tables: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_all_entities_data_source_tables(data_source_id, filter=filter, page=page, size=size, sort=sort)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_data_source_tables: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]

### Return type

[**JsonApiDataSourceTableOutList**](JsonApiDataSourceTableOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_data_sources**
> JsonApiDataSourceOutList get_all_entities_data_sources()

Get Data Source entities

Data Source - represents data source for the workspace

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_data_source_out_list import JsonApiDataSourceOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    filter = "filter=name==someString;type==DatabaseTypeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = [
        "metaInclude=permissions,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Data Source entities
        api_response = api_instance.get_all_entities_data_sources(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_data_sources: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiDataSourceOutList**](JsonApiDataSourceOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_datasets**
> JsonApiDatasetOutList get_all_entities_datasets(workspace_id)

Get all Datasets

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_dataset_out_list import JsonApiDatasetOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=attributes,facts,references,workspaceDataFilters",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get all Datasets
        api_response = api_instance.get_all_entities_datasets(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_datasets: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Datasets
        api_response = api_instance.get_all_entities_datasets(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_datasets: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiDatasetOutList**](JsonApiDatasetOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_entitlements**
> JsonApiEntitlementOutList get_all_entities_entitlements()

Get Entitlements

Space of the shared interest

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_entitlement_out_list import JsonApiEntitlementOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    filter = "filter=value==someString;expiry==LocalDateValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Entitlements
        api_response = api_instance.get_all_entities_entitlements(filter=filter, page=page, size=size, sort=sort)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_entitlements: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]

### Return type

[**JsonApiEntitlementOutList**](JsonApiEntitlementOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_facts**
> JsonApiFactOutList get_all_entities_facts(workspace_id)

Get all Facts

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_fact_out_list import JsonApiFactOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "filter=title==someString;description==someString;dataset.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=dataset",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get all Facts
        api_response = api_instance.get_all_entities_facts(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_facts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Facts
        api_response = api_instance.get_all_entities_facts(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_facts: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiFactOutList**](JsonApiFactOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_filter_contexts**
> JsonApiFilterContextOutList get_all_entities_filter_contexts(workspace_id)

Get all Context Filters

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_filter_context_out_list import JsonApiFilterContextOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=attributes,datasets,labels",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get all Context Filters
        api_response = api_instance.get_all_entities_filter_contexts(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_filter_contexts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Context Filters
        api_response = api_instance.get_all_entities_filter_contexts(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_filter_contexts: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiFilterContextOutList**](JsonApiFilterContextOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_jwks**
> JsonApiJwkOutList get_all_entities_jwks()

Get all Jwks

Returns all JSON web keys - used to verify JSON web tokens (Jwts)

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_jwk_out_list import JsonApiJwkOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    filter = "filter=content==JwkSpecificationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Jwks
        api_response = api_instance.get_all_entities_jwks(filter=filter, page=page, size=size, sort=sort)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_jwks: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]

### Return type

[**JsonApiJwkOutList**](JsonApiJwkOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_labels**
> JsonApiLabelOutList get_all_entities_labels(workspace_id)

Get all Labels

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_label_out_list import JsonApiLabelOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "filter=title==someString;description==someString;attribute.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=attribute",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get all Labels
        api_response = api_instance.get_all_entities_labels(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_labels: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Labels
        api_response = api_instance.get_all_entities_labels(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_labels: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiLabelOutList**](JsonApiLabelOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_metrics**
> JsonApiMetricOutList get_all_entities_metrics(workspace_id)

Get all Metrics

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_metric_out_list import JsonApiMetricOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get all Metrics
        api_response = api_instance.get_all_entities_metrics(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_metrics: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Metrics
        api_response = api_instance.get_all_entities_metrics(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_metrics: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiMetricOutList**](JsonApiMetricOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_organization_settings**
> JsonApiOrganizationSettingOutList get_all_entities_organization_settings()

Get Organization entities

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_organization_setting_out_list import JsonApiOrganizationSettingOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    filter = "filter=content==JsonNodeValue;type==SettingConfigurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Organization entities
        api_response = api_instance.get_all_entities_organization_settings(filter=filter, page=page, size=size, sort=sort)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_organization_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]

### Return type

[**JsonApiOrganizationSettingOutList**](JsonApiOrganizationSettingOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_themes**
> JsonApiThemeOutList get_all_entities_themes()

Get all Theming entities

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_theme_out_list import JsonApiThemeOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    filter = "filter=name==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Theming entities
        api_response = api_instance.get_all_entities_themes(filter=filter, page=page, size=size, sort=sort)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_themes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]

### Return type

[**JsonApiThemeOutList**](JsonApiThemeOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_user_data_filters**
> JsonApiUserDataFilterOutList get_all_entities_user_data_filters(workspace_id)

Get all User Data Filters

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_user_data_filter_out_list import JsonApiUserDataFilterOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "filter=title==someString;description==someString;user.id==321;userGroup.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=user,userGroup,facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get all User Data Filters
        api_response = api_instance.get_all_entities_user_data_filters(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_user_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all User Data Filters
        api_response = api_instance.get_all_entities_user_data_filters(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_user_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiUserDataFilterOutList**](JsonApiUserDataFilterOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_user_groups**
> JsonApiUserGroupOutList get_all_entities_user_groups()

Get UserGroup entities

User Group - creates tree-like structure for categorizing users

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_user_group_out_list import JsonApiUserGroupOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    filter = "filter=name==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=parents",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get UserGroup entities
        api_response = api_instance.get_all_entities_user_groups(filter=filter, include=include, page=page, size=size, sort=sort)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_user_groups: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]

### Return type

[**JsonApiUserGroupOutList**](JsonApiUserGroupOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_user_settings**
> JsonApiUserSettingOutList get_all_entities_user_settings(user_id)

List all settings for a user

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_user_setting_out_list import JsonApiUserSettingOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    user_id = "userId_example" # str | 
    filter = "filter=content==JsonNodeValue;type==SettingConfigurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)

    # example passing only required values which don't have defaults set
    try:
        # List all settings for a user
        api_response = api_instance.get_all_entities_user_settings(user_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_user_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # List all settings for a user
        api_response = api_instance.get_all_entities_user_settings(user_id, filter=filter, page=page, size=size, sort=sort)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_user_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]

### Return type

[**JsonApiUserSettingOutList**](JsonApiUserSettingOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_users**
> JsonApiUserOutList get_all_entities_users()

Get User entities

User - represents entity interacting with platform

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_user_out_list import JsonApiUserOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    filter = "filter=authenticationId==someString;firstname==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=userGroups",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get User entities
        api_response = api_instance.get_all_entities_users(filter=filter, include=include, page=page, size=size, sort=sort)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_users: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]

### Return type

[**JsonApiUserOutList**](JsonApiUserOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_visualization_objects**
> JsonApiVisualizationObjectOutList get_all_entities_visualization_objects(workspace_id)

Get all Visualization Objects

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_visualization_object_out_list import JsonApiVisualizationObjectOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get all Visualization Objects
        api_response = api_instance.get_all_entities_visualization_objects(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_visualization_objects: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Visualization Objects
        api_response = api_instance.get_all_entities_visualization_objects(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_visualization_objects: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiVisualizationObjectOutList**](JsonApiVisualizationObjectOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_workspace_data_filter_settings**
> JsonApiWorkspaceDataFilterSettingOutList get_all_entities_workspace_data_filter_settings(workspace_id)

Get all Settings for Workspace Data Filters

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_workspace_data_filter_setting_out_list import JsonApiWorkspaceDataFilterSettingOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "filter=title==someString;description==someString;workspaceDataFilter.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=workspaceDataFilter",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # Get all Settings for Workspace Data Filters
        api_response = api_instance.get_all_entities_workspace_data_filter_settings(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_workspace_data_filter_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Settings for Workspace Data Filters
        api_response = api_instance.get_all_entities_workspace_data_filter_settings(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_workspace_data_filter_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**JsonApiWorkspaceDataFilterSettingOutList**](JsonApiWorkspaceDataFilterSettingOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_workspace_data_filters**
> JsonApiWorkspaceDataFilterOutList get_all_entities_workspace_data_filters(workspace_id)

Get all Workspace Data Filters

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_workspace_data_filter_out_list import JsonApiWorkspaceDataFilterOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=filterSettings",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # Get all Workspace Data Filters
        api_response = api_instance.get_all_entities_workspace_data_filters(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_workspace_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Workspace Data Filters
        api_response = api_instance.get_all_entities_workspace_data_filters(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_workspace_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**JsonApiWorkspaceDataFilterOutList**](JsonApiWorkspaceDataFilterOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_workspace_settings**
> JsonApiWorkspaceSettingOutList get_all_entities_workspace_settings(workspace_id)

Get all Setting for Workspaces

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_workspace_setting_out_list import JsonApiWorkspaceSettingOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "filter=content==JsonNodeValue;type==SettingConfigurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get all Setting for Workspaces
        api_response = api_instance.get_all_entities_workspace_settings(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_workspace_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Setting for Workspaces
        api_response = api_instance.get_all_entities_workspace_settings(workspace_id, origin=origin, filter=filter, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_workspace_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiWorkspaceSettingOutList**](JsonApiWorkspaceSettingOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_workspaces**
> JsonApiWorkspaceOutList get_all_entities_workspaces()

Get Workspace entities

Space of the shared interest

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_workspace_out_list import JsonApiWorkspaceOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    filter = "filter=name==someString;earlyAccess==someString;parent.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=parent",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = [
        "metaInclude=config,permissions,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Workspace entities
        api_response = api_instance.get_all_entities_workspaces(filter=filter, include=include, page=page, size=size, sort=sort, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_entities_workspaces: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiWorkspaceOutList**](JsonApiWorkspaceOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_options**
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} get_all_options()

Links for all configuration options

Retrieves links for all options for different configurations.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Links for all configuration options
        api_response = api_instance.get_all_options()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_all_options: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Links for all configuration options. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_data_source_drivers**
> {str: (str,)} get_data_source_drivers()

Get all available data source drivers

Retrieves a list of all supported data sources along with information about the used drivers.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get all available data source drivers
        api_response = api_instance.get_data_source_drivers()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_data_source_drivers: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

**{str: (str,)}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of all available data source drivers. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_analytical_dashboards**
> JsonApiAnalyticalDashboardOutDocument get_entity_analytical_dashboards(workspace_id, object_id)

Get a Dashboard

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_analytical_dashboard_out_document import JsonApiAnalyticalDashboardOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=visualizationObjects,analyticalDashboards,labels,metrics,datasets,filterContexts,dashboardPlugins",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=permissions,origin,accessInfo,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a Dashboard
        api_response = api_instance.get_entity_analytical_dashboards(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_analytical_dashboards: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Dashboard
        api_response = api_instance.get_entity_analytical_dashboards(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_analytical_dashboards: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiAnalyticalDashboardOutDocument**](JsonApiAnalyticalDashboardOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_api_tokens**
> JsonApiApiTokenOutDocument get_entity_api_tokens(user_id, id)

Get an API Token for a user

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_api_token_out_document import JsonApiApiTokenOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    user_id = "userId_example" # str | 
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=bearerToken==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get an API Token for a user
        api_response = api_instance.get_entity_api_tokens(user_id, id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_api_tokens: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get an API Token for a user
        api_response = api_instance.get_entity_api_tokens(user_id, id, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_api_tokens: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  |
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiApiTokenOutDocument**](JsonApiApiTokenOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_attributes**
> JsonApiAttributeOutDocument get_entity_attributes(workspace_id, object_id)

Get a Attribute

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_attribute_out_document import JsonApiAttributeOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString;dataset.id==321;defaultView.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=dataset,defaultView,labels",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a Attribute
        api_response = api_instance.get_entity_attributes(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_attributes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Attribute
        api_response = api_instance.get_entity_attributes(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_attributes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiAttributeOutDocument**](JsonApiAttributeOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_color_palettes**
> JsonApiColorPaletteOutDocument get_entity_color_palettes(id)

Get Color Pallette

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_color_palette_out_document import JsonApiColorPaletteOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=name==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get Color Pallette
        api_response = api_instance.get_entity_color_palettes(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_color_palettes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Color Pallette
        api_response = api_instance.get_entity_color_palettes(id, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_color_palettes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiColorPaletteOutDocument**](JsonApiColorPaletteOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_cookie_security_configurations**
> JsonApiCookieSecurityConfigurationOutDocument get_entity_cookie_security_configurations(id)

Get CookieSecurityConfiguration

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_cookie_security_configuration_out_document import JsonApiCookieSecurityConfigurationOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=lastRotation==InstantValue;rotationInterval==DurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get CookieSecurityConfiguration
        api_response = api_instance.get_entity_cookie_security_configurations(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_cookie_security_configurations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get CookieSecurityConfiguration
        api_response = api_instance.get_entity_cookie_security_configurations(id, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_cookie_security_configurations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiCookieSecurityConfigurationOutDocument**](JsonApiCookieSecurityConfigurationOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_csp_directives**
> JsonApiCspDirectiveOutDocument get_entity_csp_directives(id)

Get CSP Directives

 Context Security Police Directive

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_csp_directive_out_document import JsonApiCspDirectiveOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=sources==v1,v2,v3" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get CSP Directives
        api_response = api_instance.get_entity_csp_directives(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_csp_directives: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get CSP Directives
        api_response = api_instance.get_entity_csp_directives(id, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_csp_directives: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiCspDirectiveOutDocument**](JsonApiCspDirectiveOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_custom_application_settings**
> JsonApiCustomApplicationSettingOutDocument get_entity_custom_application_settings(workspace_id, object_id)

Get a Custom Application Setting

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_custom_application_setting_out_document import JsonApiCustomApplicationSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=applicationName==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a Custom Application Setting
        api_response = api_instance.get_entity_custom_application_settings(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_custom_application_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Custom Application Setting
        api_response = api_instance.get_entity_custom_application_settings(workspace_id, object_id, filter=filter, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_custom_application_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiCustomApplicationSettingOutDocument**](JsonApiCustomApplicationSettingOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_dashboard_plugins**
> JsonApiDashboardPluginOutDocument get_entity_dashboard_plugins(workspace_id, object_id)

Get a Plugin

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_dashboard_plugin_out_document import JsonApiDashboardPluginOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a Plugin
        api_response = api_instance.get_entity_dashboard_plugins(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_dashboard_plugins: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Plugin
        api_response = api_instance.get_entity_dashboard_plugins(workspace_id, object_id, filter=filter, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_dashboard_plugins: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiDashboardPluginOutDocument**](JsonApiDashboardPluginOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_data_source_identifiers**
> JsonApiDataSourceIdentifierOutDocument get_entity_data_source_identifiers(id)

Get Data Source Identifier

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_data_source_identifier_out_document import JsonApiDataSourceIdentifierOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=name==someString;schema==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    meta_include = [
        "metaInclude=permissions,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get Data Source Identifier
        api_response = api_instance.get_entity_data_source_identifiers(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_data_source_identifiers: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Data Source Identifier
        api_response = api_instance.get_entity_data_source_identifiers(id, filter=filter, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_data_source_identifiers: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiDataSourceIdentifierOutDocument**](JsonApiDataSourceIdentifierOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_data_source_tables**
> JsonApiDataSourceTableOutDocument get_entity_data_source_tables(data_source_id, id)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_data_source_table_out_document import JsonApiDataSourceTableOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    data_source_id = "dataSourceId_example" # str | 
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=path==v1,v2,v3;type==DataSourceTableTypeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_entity_data_source_tables(data_source_id, id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_data_source_tables: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_entity_data_source_tables(data_source_id, id, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_data_source_tables: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  |
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiDataSourceTableOutDocument**](JsonApiDataSourceTableOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_data_sources**
> JsonApiDataSourceOutDocument get_entity_data_sources(id)

Get Data Source entity

Data Source - represents data source for the workspace

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_data_source_out_document import JsonApiDataSourceOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=name==someString;type==DatabaseTypeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    meta_include = [
        "metaInclude=permissions,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get Data Source entity
        api_response = api_instance.get_entity_data_sources(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_data_sources: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Data Source entity
        api_response = api_instance.get_entity_data_sources(id, filter=filter, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_data_sources: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiDataSourceOutDocument**](JsonApiDataSourceOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_datasets**
> JsonApiDatasetOutDocument get_entity_datasets(workspace_id, object_id)

Get a Dataset

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_dataset_out_document import JsonApiDatasetOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=attributes,facts,references,workspaceDataFilters",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a Dataset
        api_response = api_instance.get_entity_datasets(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_datasets: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Dataset
        api_response = api_instance.get_entity_datasets(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_datasets: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiDatasetOutDocument**](JsonApiDatasetOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_entitlements**
> JsonApiEntitlementOutDocument get_entity_entitlements(id)

Get Entitlement

Space of the shared interest

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_entitlement_out_document import JsonApiEntitlementOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=value==someString;expiry==LocalDateValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get Entitlement
        api_response = api_instance.get_entity_entitlements(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_entitlements: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Entitlement
        api_response = api_instance.get_entity_entitlements(id, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_entitlements: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiEntitlementOutDocument**](JsonApiEntitlementOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_facts**
> JsonApiFactOutDocument get_entity_facts(workspace_id, object_id)

Get a Fact

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_fact_out_document import JsonApiFactOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString;dataset.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=dataset",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a Fact
        api_response = api_instance.get_entity_facts(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_facts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Fact
        api_response = api_instance.get_entity_facts(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_facts: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiFactOutDocument**](JsonApiFactOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_filter_contexts**
> JsonApiFilterContextOutDocument get_entity_filter_contexts(workspace_id, object_id)

Get a Context Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_filter_context_out_document import JsonApiFilterContextOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=attributes,datasets,labels",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a Context Filter
        api_response = api_instance.get_entity_filter_contexts(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_filter_contexts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Context Filter
        api_response = api_instance.get_entity_filter_contexts(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_filter_contexts: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiFilterContextOutDocument**](JsonApiFilterContextOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_jwks**
> JsonApiJwkOutDocument get_entity_jwks(id)

Get Jwk

Returns JSON web key - used to verify JSON web tokens (Jwts)

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_jwk_out_document import JsonApiJwkOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=content==JwkSpecificationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get Jwk
        api_response = api_instance.get_entity_jwks(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_jwks: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Jwk
        api_response = api_instance.get_entity_jwks(id, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_jwks: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiJwkOutDocument**](JsonApiJwkOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_labels**
> JsonApiLabelOutDocument get_entity_labels(workspace_id, object_id)

Get a Label

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_label_out_document import JsonApiLabelOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString;attribute.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=attribute",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a Label
        api_response = api_instance.get_entity_labels(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_labels: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Label
        api_response = api_instance.get_entity_labels(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_labels: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiLabelOutDocument**](JsonApiLabelOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_metrics**
> JsonApiMetricOutDocument get_entity_metrics(workspace_id, object_id)

Get a Metric

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_metric_out_document import JsonApiMetricOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a Metric
        api_response = api_instance.get_entity_metrics(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_metrics: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Metric
        api_response = api_instance.get_entity_metrics(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_metrics: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiMetricOutDocument**](JsonApiMetricOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_organization_settings**
> JsonApiOrganizationSettingOutDocument get_entity_organization_settings(id)

Get Organization entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_organization_setting_out_document import JsonApiOrganizationSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=content==JsonNodeValue;type==SettingConfigurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get Organization entity
        api_response = api_instance.get_entity_organization_settings(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_organization_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Organization entity
        api_response = api_instance.get_entity_organization_settings(id, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_organization_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiOrganizationSettingOutDocument**](JsonApiOrganizationSettingOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_organizations**
> JsonApiOrganizationOutDocument get_entity_organizations(id)

Get Organizations

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_organization_out_document import JsonApiOrganizationOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=name==someString;hostname==someString;bootstrapUser.id==321;bootstrapUserGroup.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=bootstrapUser,bootstrapUserGroup",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = [
        "metaInclude=permissions,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get Organizations
        api_response = api_instance.get_entity_organizations(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_organizations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Organizations
        api_response = api_instance.get_entity_organizations(id, filter=filter, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_organizations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiOrganizationOutDocument**](JsonApiOrganizationOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_themes**
> JsonApiThemeOutDocument get_entity_themes(id)

Get Theming

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_theme_out_document import JsonApiThemeOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=name==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get Theming
        api_response = api_instance.get_entity_themes(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_themes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Theming
        api_response = api_instance.get_entity_themes(id, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_themes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiThemeOutDocument**](JsonApiThemeOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_user_data_filters**
> JsonApiUserDataFilterOutDocument get_entity_user_data_filters(workspace_id, object_id)

Get a User Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_user_data_filter_out_document import JsonApiUserDataFilterOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString;user.id==321;userGroup.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=user,userGroup,facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a User Data Filter
        api_response = api_instance.get_entity_user_data_filters(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_user_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a User Data Filter
        api_response = api_instance.get_entity_user_data_filters(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_user_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiUserDataFilterOutDocument**](JsonApiUserDataFilterOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_user_groups**
> JsonApiUserGroupOutDocument get_entity_user_groups(id)

Get UserGroup entity

User Group - creates tree-like structure for categorizing users

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_user_group_out_document import JsonApiUserGroupOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=name==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=parents",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get UserGroup entity
        api_response = api_instance.get_entity_user_groups(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_user_groups: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get UserGroup entity
        api_response = api_instance.get_entity_user_groups(id, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_user_groups: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiUserGroupOutDocument**](JsonApiUserGroupOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_user_settings**
> JsonApiUserSettingOutDocument get_entity_user_settings(user_id, id)

Get a setting for a user

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_user_setting_out_document import JsonApiUserSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    user_id = "userId_example" # str | 
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=content==JsonNodeValue;type==SettingConfigurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a setting for a user
        api_response = api_instance.get_entity_user_settings(user_id, id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_user_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a setting for a user
        api_response = api_instance.get_entity_user_settings(user_id, id, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_user_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  |
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiUserSettingOutDocument**](JsonApiUserSettingOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_users**
> JsonApiUserOutDocument get_entity_users(id)

Get User entity

User - represents entity interacting with platform

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_user_out_document import JsonApiUserOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=authenticationId==someString;firstname==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=userGroups",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get User entity
        api_response = api_instance.get_entity_users(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_users: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get User entity
        api_response = api_instance.get_entity_users(id, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_users: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiUserOutDocument**](JsonApiUserOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_visualization_objects**
> JsonApiVisualizationObjectOutDocument get_entity_visualization_objects(workspace_id, object_id)

Get a Visualization Object

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_visualization_object_out_document import JsonApiVisualizationObjectOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a Visualization Object
        api_response = api_instance.get_entity_visualization_objects(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_visualization_objects: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Visualization Object
        api_response = api_instance.get_entity_visualization_objects(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_visualization_objects: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiVisualizationObjectOutDocument**](JsonApiVisualizationObjectOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_workspace_data_filter_settings**
> JsonApiWorkspaceDataFilterSettingOutDocument get_entity_workspace_data_filter_settings(workspace_id, object_id)

Get a Setting for Workspace Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_workspace_data_filter_setting_out_document import JsonApiWorkspaceDataFilterSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString;workspaceDataFilter.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=workspaceDataFilter",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # Get a Setting for Workspace Data Filter
        api_response = api_instance.get_entity_workspace_data_filter_settings(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_workspace_data_filter_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Setting for Workspace Data Filter
        api_response = api_instance.get_entity_workspace_data_filter_settings(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_workspace_data_filter_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**JsonApiWorkspaceDataFilterSettingOutDocument**](JsonApiWorkspaceDataFilterSettingOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_workspace_data_filters**
> JsonApiWorkspaceDataFilterOutDocument get_entity_workspace_data_filters(workspace_id, object_id)

Get a Workspace Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_workspace_data_filter_out_document import JsonApiWorkspaceDataFilterOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=filterSettings",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # Get a Workspace Data Filter
        api_response = api_instance.get_entity_workspace_data_filters(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_workspace_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Workspace Data Filter
        api_response = api_instance.get_entity_workspace_data_filters(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_workspace_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**JsonApiWorkspaceDataFilterOutDocument**](JsonApiWorkspaceDataFilterOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_workspace_settings**
> JsonApiWorkspaceSettingOutDocument get_entity_workspace_settings(workspace_id, object_id)

Get a Setting for Workspace

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_workspace_setting_out_document import JsonApiWorkspaceSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=content==JsonNodeValue;type==SettingConfigurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a Setting for Workspace
        api_response = api_instance.get_entity_workspace_settings(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_workspace_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Setting for Workspace
        api_response = api_instance.get_entity_workspace_settings(workspace_id, object_id, filter=filter, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_workspace_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiWorkspaceSettingOutDocument**](JsonApiWorkspaceSettingOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_workspaces**
> JsonApiWorkspaceOutDocument get_entity_workspaces(id)

Get Workspace entity

Space of the shared interest

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_workspace_out_document import JsonApiWorkspaceOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=name==someString;earlyAccess==someString;parent.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=parent",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = [
        "metaInclude=config,permissions,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get Workspace entity
        api_response = api_instance.get_entity_workspaces(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_workspaces: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Workspace entity
        api_response = api_instance.get_entity_workspaces(id, filter=filter, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_entity_workspaces: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiWorkspaceOutDocument**](JsonApiWorkspaceOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_organization**
> get_organization()

Get current organization info

Gets a basic information about organization.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    meta_include = [
        "metaInclude=permissions",
    ] # [str] | Return list of permissions available to logged user. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get current organization info
        api_instance.get_organization(meta_include=meta_include)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->get_organization: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **meta_include** | **[str]**| Return list of permissions available to logged user. | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**302** | Redirect to entity URI. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_analytical_dashboards**
> JsonApiAnalyticalDashboardOutDocument patch_entity_analytical_dashboards(workspace_id, object_id, json_api_analytical_dashboard_patch_document)

Patch a Dashboard

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_analytical_dashboard_patch_document import JsonApiAnalyticalDashboardPatchDocument
from gooddata_api_client.model.json_api_analytical_dashboard_out_document import JsonApiAnalyticalDashboardOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_analytical_dashboard_patch_document = JsonApiAnalyticalDashboardPatchDocument(
        data=JsonApiAnalyticalDashboardPatch(
            attributes=JsonApiAnalyticalDashboardInAttributes(
                are_relations_valid=True,
                content={},
                description="description_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            type="analyticalDashboard",
        ),
    ) # JsonApiAnalyticalDashboardPatchDocument | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=visualizationObjects,analyticalDashboards,labels,metrics,datasets,filterContexts,dashboardPlugins",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch a Dashboard
        api_response = api_instance.patch_entity_analytical_dashboards(workspace_id, object_id, json_api_analytical_dashboard_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_analytical_dashboards: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Dashboard
        api_response = api_instance.patch_entity_analytical_dashboards(workspace_id, object_id, json_api_analytical_dashboard_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_analytical_dashboards: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_analytical_dashboard_patch_document** | [**JsonApiAnalyticalDashboardPatchDocument**](JsonApiAnalyticalDashboardPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiAnalyticalDashboardOutDocument**](JsonApiAnalyticalDashboardOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_color_palettes**
> JsonApiColorPaletteOutDocument patch_entity_color_palettes(id, json_api_color_palette_patch_document)

Patch Color Pallette

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_color_palette_patch_document import JsonApiColorPalettePatchDocument
from gooddata_api_client.model.json_api_color_palette_out_document import JsonApiColorPaletteOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_color_palette_patch_document = JsonApiColorPalettePatchDocument(
        data=JsonApiColorPalettePatch(
            attributes=JsonApiColorPalettePatchAttributes(
                content={},
                name="name_example",
            ),
            id="id1",
            type="colorPalette",
        ),
    ) # JsonApiColorPalettePatchDocument | 
    filter = "filter=name==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch Color Pallette
        api_response = api_instance.patch_entity_color_palettes(id, json_api_color_palette_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_color_palettes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch Color Pallette
        api_response = api_instance.patch_entity_color_palettes(id, json_api_color_palette_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_color_palettes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_color_palette_patch_document** | [**JsonApiColorPalettePatchDocument**](JsonApiColorPalettePatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiColorPaletteOutDocument**](JsonApiColorPaletteOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_cookie_security_configurations**
> JsonApiCookieSecurityConfigurationOutDocument patch_entity_cookie_security_configurations(id, json_api_cookie_security_configuration_patch_document)

Patch CookieSecurityConfiguration

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_cookie_security_configuration_out_document import JsonApiCookieSecurityConfigurationOutDocument
from gooddata_api_client.model.json_api_cookie_security_configuration_patch_document import JsonApiCookieSecurityConfigurationPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_cookie_security_configuration_patch_document = JsonApiCookieSecurityConfigurationPatchDocument(
        data=JsonApiCookieSecurityConfigurationPatch(
            attributes=JsonApiCookieSecurityConfigurationInAttributes(
                last_rotation=dateutil_parser('1970-01-01T00:00:00.00Z'),
                rotation_interval="P30D",
            ),
            id="id1",
            type="cookieSecurityConfiguration",
        ),
    ) # JsonApiCookieSecurityConfigurationPatchDocument | 
    filter = "filter=lastRotation==InstantValue;rotationInterval==DurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch CookieSecurityConfiguration
        api_response = api_instance.patch_entity_cookie_security_configurations(id, json_api_cookie_security_configuration_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_cookie_security_configurations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch CookieSecurityConfiguration
        api_response = api_instance.patch_entity_cookie_security_configurations(id, json_api_cookie_security_configuration_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_cookie_security_configurations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_cookie_security_configuration_patch_document** | [**JsonApiCookieSecurityConfigurationPatchDocument**](JsonApiCookieSecurityConfigurationPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiCookieSecurityConfigurationOutDocument**](JsonApiCookieSecurityConfigurationOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_csp_directives**
> JsonApiCspDirectiveOutDocument patch_entity_csp_directives(id, json_api_csp_directive_patch_document)

Patch CSP Directives

 Context Security Police Directive

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_csp_directive_out_document import JsonApiCspDirectiveOutDocument
from gooddata_api_client.model.json_api_csp_directive_patch_document import JsonApiCspDirectivePatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_csp_directive_patch_document = JsonApiCspDirectivePatchDocument(
        data=JsonApiCspDirectivePatch(
            attributes=JsonApiCspDirectivePatchAttributes(
                sources=[
                    "sources_example",
                ],
            ),
            id="id1",
            type="cspDirective",
        ),
    ) # JsonApiCspDirectivePatchDocument | 
    filter = "filter=sources==v1,v2,v3" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch CSP Directives
        api_response = api_instance.patch_entity_csp_directives(id, json_api_csp_directive_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_csp_directives: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch CSP Directives
        api_response = api_instance.patch_entity_csp_directives(id, json_api_csp_directive_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_csp_directives: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_csp_directive_patch_document** | [**JsonApiCspDirectivePatchDocument**](JsonApiCspDirectivePatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiCspDirectiveOutDocument**](JsonApiCspDirectiveOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_custom_application_settings**
> JsonApiCustomApplicationSettingOutDocument patch_entity_custom_application_settings(workspace_id, object_id, json_api_custom_application_setting_patch_document)

Patch a Custom Application Setting

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_custom_application_setting_patch_document import JsonApiCustomApplicationSettingPatchDocument
from gooddata_api_client.model.json_api_custom_application_setting_out_document import JsonApiCustomApplicationSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_custom_application_setting_patch_document = JsonApiCustomApplicationSettingPatchDocument(
        data=JsonApiCustomApplicationSettingPatch(
            attributes=JsonApiCustomApplicationSettingPatchAttributes(
                application_name="application_name_example",
                content={},
            ),
            id="id1",
            type="customApplicationSetting",
        ),
    ) # JsonApiCustomApplicationSettingPatchDocument | 
    filter = "filter=applicationName==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch a Custom Application Setting
        api_response = api_instance.patch_entity_custom_application_settings(workspace_id, object_id, json_api_custom_application_setting_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_custom_application_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Custom Application Setting
        api_response = api_instance.patch_entity_custom_application_settings(workspace_id, object_id, json_api_custom_application_setting_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_custom_application_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_custom_application_setting_patch_document** | [**JsonApiCustomApplicationSettingPatchDocument**](JsonApiCustomApplicationSettingPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiCustomApplicationSettingOutDocument**](JsonApiCustomApplicationSettingOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_dashboard_plugins**
> JsonApiDashboardPluginOutDocument patch_entity_dashboard_plugins(workspace_id, object_id, json_api_dashboard_plugin_patch_document)

Patch a Plugin

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_dashboard_plugin_out_document import JsonApiDashboardPluginOutDocument
from gooddata_api_client.model.json_api_dashboard_plugin_patch_document import JsonApiDashboardPluginPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_dashboard_plugin_patch_document = JsonApiDashboardPluginPatchDocument(
        data=JsonApiDashboardPluginPatch(
            attributes=JsonApiDashboardPluginInAttributes(
                are_relations_valid=True,
                content={},
                description="description_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            type="dashboardPlugin",
        ),
    ) # JsonApiDashboardPluginPatchDocument | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch a Plugin
        api_response = api_instance.patch_entity_dashboard_plugins(workspace_id, object_id, json_api_dashboard_plugin_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_dashboard_plugins: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Plugin
        api_response = api_instance.patch_entity_dashboard_plugins(workspace_id, object_id, json_api_dashboard_plugin_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_dashboard_plugins: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_dashboard_plugin_patch_document** | [**JsonApiDashboardPluginPatchDocument**](JsonApiDashboardPluginPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiDashboardPluginOutDocument**](JsonApiDashboardPluginOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_data_sources**
> JsonApiDataSourceOutDocument patch_entity_data_sources(id, json_api_data_source_patch_document)

Patch Data Source entity

Data Source - represents data source for the workspace

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_data_source_patch_document import JsonApiDataSourcePatchDocument
from gooddata_api_client.model.json_api_data_source_out_document import JsonApiDataSourceOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_data_source_patch_document = JsonApiDataSourcePatchDocument(
        data=JsonApiDataSourcePatch(
            attributes=JsonApiDataSourcePatchAttributes(
                cache_path=[
                    "cache_path_example",
                ],
                enable_caching=False,
                name="name_example",
                parameters=[
                    JsonApiDataSourceInAttributesParametersInner(
                        name="name_example",
                        value="value_example",
                    ),
                ],
                password="password_example",
                schema="schema_example",
                token="token_example",
                type="POSTGRESQL",
                url="url_example",
                username="username_example",
            ),
            id="id1",
            type="dataSource",
        ),
    ) # JsonApiDataSourcePatchDocument | 
    filter = "filter=name==someString;type==DatabaseTypeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch Data Source entity
        api_response = api_instance.patch_entity_data_sources(id, json_api_data_source_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_data_sources: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch Data Source entity
        api_response = api_instance.patch_entity_data_sources(id, json_api_data_source_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_data_sources: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_data_source_patch_document** | [**JsonApiDataSourcePatchDocument**](JsonApiDataSourcePatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiDataSourceOutDocument**](JsonApiDataSourceOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_filter_contexts**
> JsonApiFilterContextOutDocument patch_entity_filter_contexts(workspace_id, object_id, json_api_filter_context_patch_document)

Patch a Context Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_filter_context_patch_document import JsonApiFilterContextPatchDocument
from gooddata_api_client.model.json_api_filter_context_out_document import JsonApiFilterContextOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_filter_context_patch_document = JsonApiFilterContextPatchDocument(
        data=JsonApiFilterContextPatch(
            attributes=JsonApiAnalyticalDashboardInAttributes(
                are_relations_valid=True,
                content={},
                description="description_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            type="filterContext",
        ),
    ) # JsonApiFilterContextPatchDocument | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=attributes,datasets,labels",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch a Context Filter
        api_response = api_instance.patch_entity_filter_contexts(workspace_id, object_id, json_api_filter_context_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_filter_contexts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Context Filter
        api_response = api_instance.patch_entity_filter_contexts(workspace_id, object_id, json_api_filter_context_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_filter_contexts: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_filter_context_patch_document** | [**JsonApiFilterContextPatchDocument**](JsonApiFilterContextPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiFilterContextOutDocument**](JsonApiFilterContextOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_jwks**
> JsonApiJwkOutDocument patch_entity_jwks(id, json_api_jwk_patch_document)

Patch Jwk

Patches JSON web key - used to verify JSON web tokens (Jwts)

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_jwk_patch_document import JsonApiJwkPatchDocument
from gooddata_api_client.model.json_api_jwk_out_document import JsonApiJwkOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_jwk_patch_document = JsonApiJwkPatchDocument(
        data=JsonApiJwkPatch(
            attributes=JsonApiJwkInAttributes(
                content=JsonApiJwkInAttributesContent(),
            ),
            id="id1",
            type="jwk",
        ),
    ) # JsonApiJwkPatchDocument | 
    filter = "filter=content==JwkSpecificationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch Jwk
        api_response = api_instance.patch_entity_jwks(id, json_api_jwk_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_jwks: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch Jwk
        api_response = api_instance.patch_entity_jwks(id, json_api_jwk_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_jwks: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_jwk_patch_document** | [**JsonApiJwkPatchDocument**](JsonApiJwkPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiJwkOutDocument**](JsonApiJwkOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_metrics**
> JsonApiMetricOutDocument patch_entity_metrics(workspace_id, object_id, json_api_metric_patch_document)

Patch a Metric

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_metric_patch_document import JsonApiMetricPatchDocument
from gooddata_api_client.model.json_api_metric_out_document import JsonApiMetricOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_metric_patch_document = JsonApiMetricPatchDocument(
        data=JsonApiMetricPatch(
            attributes=JsonApiMetricPatchAttributes(
                are_relations_valid=True,
                content=JsonApiMetricInAttributesContent(
                    format="format_example",
                    maql="maql_example",
                ),
                description="description_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            type="metric",
        ),
    ) # JsonApiMetricPatchDocument | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch a Metric
        api_response = api_instance.patch_entity_metrics(workspace_id, object_id, json_api_metric_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_metrics: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Metric
        api_response = api_instance.patch_entity_metrics(workspace_id, object_id, json_api_metric_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_metrics: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_metric_patch_document** | [**JsonApiMetricPatchDocument**](JsonApiMetricPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiMetricOutDocument**](JsonApiMetricOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_organization_settings**
> JsonApiOrganizationSettingOutDocument patch_entity_organization_settings(id, json_api_organization_setting_patch_document)

Patch Organization entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_organization_setting_out_document import JsonApiOrganizationSettingOutDocument
from gooddata_api_client.model.json_api_organization_setting_patch_document import JsonApiOrganizationSettingPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_organization_setting_patch_document = JsonApiOrganizationSettingPatchDocument(
        data=JsonApiOrganizationSettingPatch(
            attributes=JsonApiOrganizationSettingInAttributes(
                content={},
                type="TIMEZONE",
            ),
            id="id1",
            type="organizationSetting",
        ),
    ) # JsonApiOrganizationSettingPatchDocument | 
    filter = "filter=content==JsonNodeValue;type==SettingConfigurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch Organization entity
        api_response = api_instance.patch_entity_organization_settings(id, json_api_organization_setting_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_organization_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch Organization entity
        api_response = api_instance.patch_entity_organization_settings(id, json_api_organization_setting_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_organization_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_organization_setting_patch_document** | [**JsonApiOrganizationSettingPatchDocument**](JsonApiOrganizationSettingPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiOrganizationSettingOutDocument**](JsonApiOrganizationSettingOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_organizations**
> JsonApiOrganizationOutDocument patch_entity_organizations(id, json_api_organization_patch_document)

Patch Organization

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_organization_out_document import JsonApiOrganizationOutDocument
from gooddata_api_client.model.json_api_organization_patch_document import JsonApiOrganizationPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_organization_patch_document = JsonApiOrganizationPatchDocument(
        data=JsonApiOrganizationPatch(
            attributes=JsonApiOrganizationInAttributes(
                allowed_origins=[
                    "allowed_origins_example",
                ],
                early_access="early_access_example",
                hostname="hostname_example",
                name="name_example",
                oauth_client_id="oauth_client_id_example",
                oauth_client_secret="oauth_client_secret_example",
                oauth_issuer_id="myOidcProvider",
                oauth_issuer_location="oauth_issuer_location_example",
            ),
            id="id1",
            type="organization",
        ),
    ) # JsonApiOrganizationPatchDocument | 
    filter = "filter=name==someString;hostname==someString;bootstrapUser.id==321;bootstrapUserGroup.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=bootstrapUser,bootstrapUserGroup",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch Organization
        api_response = api_instance.patch_entity_organizations(id, json_api_organization_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_organizations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch Organization
        api_response = api_instance.patch_entity_organizations(id, json_api_organization_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_organizations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_organization_patch_document** | [**JsonApiOrganizationPatchDocument**](JsonApiOrganizationPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiOrganizationOutDocument**](JsonApiOrganizationOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_themes**
> JsonApiThemeOutDocument patch_entity_themes(id, json_api_theme_patch_document)

Patch Theming

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_theme_patch_document import JsonApiThemePatchDocument
from gooddata_api_client.model.json_api_theme_out_document import JsonApiThemeOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_theme_patch_document = JsonApiThemePatchDocument(
        data=JsonApiThemePatch(
            attributes=JsonApiColorPalettePatchAttributes(
                content={},
                name="name_example",
            ),
            id="id1",
            type="theme",
        ),
    ) # JsonApiThemePatchDocument | 
    filter = "filter=name==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch Theming
        api_response = api_instance.patch_entity_themes(id, json_api_theme_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_themes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch Theming
        api_response = api_instance.patch_entity_themes(id, json_api_theme_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_themes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_theme_patch_document** | [**JsonApiThemePatchDocument**](JsonApiThemePatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiThemeOutDocument**](JsonApiThemeOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_user_data_filters**
> JsonApiUserDataFilterOutDocument patch_entity_user_data_filters(workspace_id, object_id, json_api_user_data_filter_patch_document)

Patch a User Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_user_data_filter_out_document import JsonApiUserDataFilterOutDocument
from gooddata_api_client.model.json_api_user_data_filter_patch_document import JsonApiUserDataFilterPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_user_data_filter_patch_document = JsonApiUserDataFilterPatchDocument(
        data=JsonApiUserDataFilterPatch(
            attributes=JsonApiUserDataFilterPatchAttributes(
                are_relations_valid=True,
                description="description_example",
                maql="maql_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            relationships=JsonApiUserDataFilterInRelationships(
                user=JsonApiOrganizationOutRelationshipsBootstrapUser(
                    data=JsonApiUserToOneLinkage(None),
                ),
                user_group=JsonApiOrganizationOutRelationshipsBootstrapUserGroup(
                    data=JsonApiUserGroupToOneLinkage(None),
                ),
            ),
            type="userDataFilter",
        ),
    ) # JsonApiUserDataFilterPatchDocument | 
    filter = "filter=title==someString;description==someString;user.id==321;userGroup.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=user,userGroup,facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch a User Data Filter
        api_response = api_instance.patch_entity_user_data_filters(workspace_id, object_id, json_api_user_data_filter_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_user_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a User Data Filter
        api_response = api_instance.patch_entity_user_data_filters(workspace_id, object_id, json_api_user_data_filter_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_user_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_user_data_filter_patch_document** | [**JsonApiUserDataFilterPatchDocument**](JsonApiUserDataFilterPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiUserDataFilterOutDocument**](JsonApiUserDataFilterOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_user_groups**
> JsonApiUserGroupOutDocument patch_entity_user_groups(id, json_api_user_group_patch_document)

Patch UserGroup entity

User Group - creates tree-like structure for categorizing users

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_user_group_out_document import JsonApiUserGroupOutDocument
from gooddata_api_client.model.json_api_user_group_patch_document import JsonApiUserGroupPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_user_group_patch_document = JsonApiUserGroupPatchDocument(
        data=JsonApiUserGroupPatch(
            attributes=JsonApiUserGroupInAttributes(
                name="name_example",
            ),
            id="id1",
            relationships=JsonApiUserGroupInRelationships(
                parents=JsonApiUserGroupInRelationshipsParents(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        ),
                    ]),
                ),
            ),
            type="userGroup",
        ),
    ) # JsonApiUserGroupPatchDocument | 
    filter = "filter=name==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=parents",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch UserGroup entity
        api_response = api_instance.patch_entity_user_groups(id, json_api_user_group_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_user_groups: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch UserGroup entity
        api_response = api_instance.patch_entity_user_groups(id, json_api_user_group_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_user_groups: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_user_group_patch_document** | [**JsonApiUserGroupPatchDocument**](JsonApiUserGroupPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiUserGroupOutDocument**](JsonApiUserGroupOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_users**
> JsonApiUserOutDocument patch_entity_users(id, json_api_user_patch_document)

Patch User entity

User - represents entity interacting with platform

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_user_out_document import JsonApiUserOutDocument
from gooddata_api_client.model.json_api_user_patch_document import JsonApiUserPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_user_patch_document = JsonApiUserPatchDocument(
        data=JsonApiUserPatch(
            attributes=JsonApiUserInAttributes(
                authentication_id="authentication_id_example",
                email="email_example",
                firstname="firstname_example",
                lastname="lastname_example",
            ),
            id="id1",
            relationships=JsonApiUserInRelationships(
                user_groups=JsonApiUserGroupInRelationshipsParents(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        ),
                    ]),
                ),
            ),
            type="user",
        ),
    ) # JsonApiUserPatchDocument | 
    filter = "filter=authenticationId==someString;firstname==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=userGroups",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch User entity
        api_response = api_instance.patch_entity_users(id, json_api_user_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_users: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch User entity
        api_response = api_instance.patch_entity_users(id, json_api_user_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_users: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_user_patch_document** | [**JsonApiUserPatchDocument**](JsonApiUserPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiUserOutDocument**](JsonApiUserOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_visualization_objects**
> JsonApiVisualizationObjectOutDocument patch_entity_visualization_objects(workspace_id, object_id, json_api_visualization_object_patch_document)

Patch a Visualization Object

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_visualization_object_out_document import JsonApiVisualizationObjectOutDocument
from gooddata_api_client.model.json_api_visualization_object_patch_document import JsonApiVisualizationObjectPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_visualization_object_patch_document = JsonApiVisualizationObjectPatchDocument(
        data=JsonApiVisualizationObjectPatch(
            attributes=JsonApiAnalyticalDashboardInAttributes(
                are_relations_valid=True,
                content={},
                description="description_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            type="visualizationObject",
        ),
    ) # JsonApiVisualizationObjectPatchDocument | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch a Visualization Object
        api_response = api_instance.patch_entity_visualization_objects(workspace_id, object_id, json_api_visualization_object_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_visualization_objects: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Visualization Object
        api_response = api_instance.patch_entity_visualization_objects(workspace_id, object_id, json_api_visualization_object_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_visualization_objects: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_visualization_object_patch_document** | [**JsonApiVisualizationObjectPatchDocument**](JsonApiVisualizationObjectPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiVisualizationObjectOutDocument**](JsonApiVisualizationObjectOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_workspace_data_filter_settings**
> JsonApiWorkspaceDataFilterSettingOutDocument patch_entity_workspace_data_filter_settings(workspace_id, object_id, json_api_workspace_data_filter_setting_patch_document)

Patch a Settings for Workspace Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_workspace_data_filter_setting_patch_document import JsonApiWorkspaceDataFilterSettingPatchDocument
from gooddata_api_client.model.json_api_workspace_data_filter_setting_out_document import JsonApiWorkspaceDataFilterSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_workspace_data_filter_setting_patch_document = JsonApiWorkspaceDataFilterSettingPatchDocument(
        data=JsonApiWorkspaceDataFilterSettingPatch(
            attributes=JsonApiWorkspaceDataFilterSettingInAttributes(
                description="description_example",
                filter_values=[
                    "filter_values_example",
                ],
                title="title_example",
            ),
            id="id1",
            relationships=JsonApiWorkspaceDataFilterSettingInRelationships(
                workspace_data_filter=JsonApiWorkspaceDataFilterSettingInRelationshipsWorkspaceDataFilter(
                    data=JsonApiWorkspaceDataFilterToOneLinkage(None),
                ),
            ),
            type="workspaceDataFilterSetting",
        ),
    ) # JsonApiWorkspaceDataFilterSettingPatchDocument | 
    filter = "filter=title==someString;description==someString;workspaceDataFilter.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=workspaceDataFilter",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch a Settings for Workspace Data Filter
        api_response = api_instance.patch_entity_workspace_data_filter_settings(workspace_id, object_id, json_api_workspace_data_filter_setting_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_workspace_data_filter_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Settings for Workspace Data Filter
        api_response = api_instance.patch_entity_workspace_data_filter_settings(workspace_id, object_id, json_api_workspace_data_filter_setting_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_workspace_data_filter_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_workspace_data_filter_setting_patch_document** | [**JsonApiWorkspaceDataFilterSettingPatchDocument**](JsonApiWorkspaceDataFilterSettingPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiWorkspaceDataFilterSettingOutDocument**](JsonApiWorkspaceDataFilterSettingOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_workspace_data_filters**
> JsonApiWorkspaceDataFilterOutDocument patch_entity_workspace_data_filters(workspace_id, object_id, json_api_workspace_data_filter_patch_document)

Patch a Workspace Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_workspace_data_filter_out_document import JsonApiWorkspaceDataFilterOutDocument
from gooddata_api_client.model.json_api_workspace_data_filter_patch_document import JsonApiWorkspaceDataFilterPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_workspace_data_filter_patch_document = JsonApiWorkspaceDataFilterPatchDocument(
        data=JsonApiWorkspaceDataFilterPatch(
            attributes=JsonApiWorkspaceDataFilterInAttributes(
                column_name="column_name_example",
                description="description_example",
                title="title_example",
            ),
            id="id1",
            relationships=JsonApiWorkspaceDataFilterInRelationships(
                filter_settings=JsonApiWorkspaceDataFilterInRelationshipsFilterSettings(
                    data=JsonApiWorkspaceDataFilterSettingToManyLinkage([
                        JsonApiWorkspaceDataFilterSettingLinkage(
                            id="id_example",
                            type="workspaceDataFilterSetting",
                        ),
                    ]),
                ),
            ),
            type="workspaceDataFilter",
        ),
    ) # JsonApiWorkspaceDataFilterPatchDocument | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=filterSettings",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch a Workspace Data Filter
        api_response = api_instance.patch_entity_workspace_data_filters(workspace_id, object_id, json_api_workspace_data_filter_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_workspace_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Workspace Data Filter
        api_response = api_instance.patch_entity_workspace_data_filters(workspace_id, object_id, json_api_workspace_data_filter_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_workspace_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_workspace_data_filter_patch_document** | [**JsonApiWorkspaceDataFilterPatchDocument**](JsonApiWorkspaceDataFilterPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiWorkspaceDataFilterOutDocument**](JsonApiWorkspaceDataFilterOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_workspace_settings**
> JsonApiWorkspaceSettingOutDocument patch_entity_workspace_settings(workspace_id, object_id, json_api_workspace_setting_patch_document)

Patch a Setting for Workspace

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_workspace_setting_out_document import JsonApiWorkspaceSettingOutDocument
from gooddata_api_client.model.json_api_workspace_setting_patch_document import JsonApiWorkspaceSettingPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_workspace_setting_patch_document = JsonApiWorkspaceSettingPatchDocument(
        data=JsonApiWorkspaceSettingPatch(
            attributes=JsonApiOrganizationSettingInAttributes(
                content={},
                type="TIMEZONE",
            ),
            id="id1",
            type="workspaceSetting",
        ),
    ) # JsonApiWorkspaceSettingPatchDocument | 
    filter = "filter=content==JsonNodeValue;type==SettingConfigurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch a Setting for Workspace
        api_response = api_instance.patch_entity_workspace_settings(workspace_id, object_id, json_api_workspace_setting_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_workspace_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Setting for Workspace
        api_response = api_instance.patch_entity_workspace_settings(workspace_id, object_id, json_api_workspace_setting_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_workspace_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_workspace_setting_patch_document** | [**JsonApiWorkspaceSettingPatchDocument**](JsonApiWorkspaceSettingPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiWorkspaceSettingOutDocument**](JsonApiWorkspaceSettingOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_workspaces**
> JsonApiWorkspaceOutDocument patch_entity_workspaces(id, json_api_workspace_patch_document)

Patch Workspace entity

Space of the shared interest

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_workspace_out_document import JsonApiWorkspaceOutDocument
from gooddata_api_client.model.json_api_workspace_patch_document import JsonApiWorkspacePatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_workspace_patch_document = JsonApiWorkspacePatchDocument(
        data=JsonApiWorkspacePatch(
            attributes=JsonApiWorkspaceInAttributes(
                cache_extra_limit=1,
                description="description_example",
                early_access="early_access_example",
                name="name_example",
                prefix="/6bUUGjjNSwg0_bs",
            ),
            id="id1",
            relationships=JsonApiWorkspaceInRelationships(
                parent=JsonApiWorkspaceInRelationshipsParent(
                    data=JsonApiWorkspaceToOneLinkage(None),
                ),
            ),
            type="workspace",
        ),
    ) # JsonApiWorkspacePatchDocument | 
    filter = "filter=name==someString;earlyAccess==someString;parent.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=parent",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch Workspace entity
        api_response = api_instance.patch_entity_workspaces(id, json_api_workspace_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_workspaces: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch Workspace entity
        api_response = api_instance.patch_entity_workspaces(id, json_api_workspace_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->patch_entity_workspaces: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_workspace_patch_document** | [**JsonApiWorkspacePatchDocument**](JsonApiWorkspacePatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiWorkspaceOutDocument**](JsonApiWorkspaceOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_analytical_dashboards**
> JsonApiAnalyticalDashboardOutDocument update_entity_analytical_dashboards(workspace_id, object_id, json_api_analytical_dashboard_in_document)

Put Dashboards

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_analytical_dashboard_in_document import JsonApiAnalyticalDashboardInDocument
from gooddata_api_client.model.json_api_analytical_dashboard_out_document import JsonApiAnalyticalDashboardOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_analytical_dashboard_in_document = JsonApiAnalyticalDashboardInDocument(
        data=JsonApiAnalyticalDashboardIn(
            attributes=JsonApiAnalyticalDashboardInAttributes(
                are_relations_valid=True,
                content={},
                description="description_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            type="analyticalDashboard",
        ),
    ) # JsonApiAnalyticalDashboardInDocument | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=visualizationObjects,analyticalDashboards,labels,metrics,datasets,filterContexts,dashboardPlugins",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put Dashboards
        api_response = api_instance.update_entity_analytical_dashboards(workspace_id, object_id, json_api_analytical_dashboard_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_analytical_dashboards: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put Dashboards
        api_response = api_instance.update_entity_analytical_dashboards(workspace_id, object_id, json_api_analytical_dashboard_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_analytical_dashboards: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_analytical_dashboard_in_document** | [**JsonApiAnalyticalDashboardInDocument**](JsonApiAnalyticalDashboardInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiAnalyticalDashboardOutDocument**](JsonApiAnalyticalDashboardOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_api_tokens**
> JsonApiApiTokenOutDocument update_entity_api_tokens(user_id, id, json_api_api_token_in_document)

Put new API token for the user

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_api_token_out_document import JsonApiApiTokenOutDocument
from gooddata_api_client.model.json_api_api_token_in_document import JsonApiApiTokenInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    user_id = "userId_example" # str | 
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_api_token_in_document = JsonApiApiTokenInDocument(
        data=JsonApiApiTokenIn(
            id="id1",
            type="apiToken",
        ),
    ) # JsonApiApiTokenInDocument | 
    filter = "filter=bearerToken==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put new API token for the user
        api_response = api_instance.update_entity_api_tokens(user_id, id, json_api_api_token_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_api_tokens: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put new API token for the user
        api_response = api_instance.update_entity_api_tokens(user_id, id, json_api_api_token_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_api_tokens: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  |
 **id** | **str**|  |
 **json_api_api_token_in_document** | [**JsonApiApiTokenInDocument**](JsonApiApiTokenInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiApiTokenOutDocument**](JsonApiApiTokenOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_color_palettes**
> JsonApiColorPaletteOutDocument update_entity_color_palettes(id, json_api_color_palette_in_document)

Put Color Pallette

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_color_palette_in_document import JsonApiColorPaletteInDocument
from gooddata_api_client.model.json_api_color_palette_out_document import JsonApiColorPaletteOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_color_palette_in_document = JsonApiColorPaletteInDocument(
        data=JsonApiColorPaletteIn(
            attributes=JsonApiColorPaletteInAttributes(
                content={},
                name="name_example",
            ),
            id="id1",
            type="colorPalette",
        ),
    ) # JsonApiColorPaletteInDocument | 
    filter = "filter=name==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put Color Pallette
        api_response = api_instance.update_entity_color_palettes(id, json_api_color_palette_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_color_palettes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put Color Pallette
        api_response = api_instance.update_entity_color_palettes(id, json_api_color_palette_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_color_palettes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_color_palette_in_document** | [**JsonApiColorPaletteInDocument**](JsonApiColorPaletteInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiColorPaletteOutDocument**](JsonApiColorPaletteOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_cookie_security_configurations**
> JsonApiCookieSecurityConfigurationOutDocument update_entity_cookie_security_configurations(id, json_api_cookie_security_configuration_in_document)

Put CookieSecurityConfiguration

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_cookie_security_configuration_in_document import JsonApiCookieSecurityConfigurationInDocument
from gooddata_api_client.model.json_api_cookie_security_configuration_out_document import JsonApiCookieSecurityConfigurationOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_cookie_security_configuration_in_document = JsonApiCookieSecurityConfigurationInDocument(
        data=JsonApiCookieSecurityConfigurationIn(
            attributes=JsonApiCookieSecurityConfigurationInAttributes(
                last_rotation=dateutil_parser('1970-01-01T00:00:00.00Z'),
                rotation_interval="P30D",
            ),
            id="id1",
            type="cookieSecurityConfiguration",
        ),
    ) # JsonApiCookieSecurityConfigurationInDocument | 
    filter = "filter=lastRotation==InstantValue;rotationInterval==DurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put CookieSecurityConfiguration
        api_response = api_instance.update_entity_cookie_security_configurations(id, json_api_cookie_security_configuration_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_cookie_security_configurations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put CookieSecurityConfiguration
        api_response = api_instance.update_entity_cookie_security_configurations(id, json_api_cookie_security_configuration_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_cookie_security_configurations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_cookie_security_configuration_in_document** | [**JsonApiCookieSecurityConfigurationInDocument**](JsonApiCookieSecurityConfigurationInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiCookieSecurityConfigurationOutDocument**](JsonApiCookieSecurityConfigurationOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_csp_directives**
> JsonApiCspDirectiveOutDocument update_entity_csp_directives(id, json_api_csp_directive_in_document)

Put CSP Directives

 Context Security Police Directive

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_csp_directive_out_document import JsonApiCspDirectiveOutDocument
from gooddata_api_client.model.json_api_csp_directive_in_document import JsonApiCspDirectiveInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_csp_directive_in_document = JsonApiCspDirectiveInDocument(
        data=JsonApiCspDirectiveIn(
            attributes=JsonApiCspDirectiveInAttributes(
                sources=[
                    "sources_example",
                ],
            ),
            id="id1",
            type="cspDirective",
        ),
    ) # JsonApiCspDirectiveInDocument | 
    filter = "filter=sources==v1,v2,v3" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put CSP Directives
        api_response = api_instance.update_entity_csp_directives(id, json_api_csp_directive_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_csp_directives: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put CSP Directives
        api_response = api_instance.update_entity_csp_directives(id, json_api_csp_directive_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_csp_directives: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_csp_directive_in_document** | [**JsonApiCspDirectiveInDocument**](JsonApiCspDirectiveInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiCspDirectiveOutDocument**](JsonApiCspDirectiveOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_custom_application_settings**
> JsonApiCustomApplicationSettingOutDocument update_entity_custom_application_settings(workspace_id, object_id, json_api_custom_application_setting_in_document)

Put a Custom Application Setting

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_custom_application_setting_in_document import JsonApiCustomApplicationSettingInDocument
from gooddata_api_client.model.json_api_custom_application_setting_out_document import JsonApiCustomApplicationSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_custom_application_setting_in_document = JsonApiCustomApplicationSettingInDocument(
        data=JsonApiCustomApplicationSettingIn(
            attributes=JsonApiCustomApplicationSettingInAttributes(
                application_name="application_name_example",
                content={},
            ),
            id="id1",
            type="customApplicationSetting",
        ),
    ) # JsonApiCustomApplicationSettingInDocument | 
    filter = "filter=applicationName==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put a Custom Application Setting
        api_response = api_instance.update_entity_custom_application_settings(workspace_id, object_id, json_api_custom_application_setting_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_custom_application_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Custom Application Setting
        api_response = api_instance.update_entity_custom_application_settings(workspace_id, object_id, json_api_custom_application_setting_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_custom_application_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_custom_application_setting_in_document** | [**JsonApiCustomApplicationSettingInDocument**](JsonApiCustomApplicationSettingInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiCustomApplicationSettingOutDocument**](JsonApiCustomApplicationSettingOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_dashboard_plugins**
> JsonApiDashboardPluginOutDocument update_entity_dashboard_plugins(workspace_id, object_id, json_api_dashboard_plugin_in_document)

Put a Plugin

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_dashboard_plugin_out_document import JsonApiDashboardPluginOutDocument
from gooddata_api_client.model.json_api_dashboard_plugin_in_document import JsonApiDashboardPluginInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_dashboard_plugin_in_document = JsonApiDashboardPluginInDocument(
        data=JsonApiDashboardPluginIn(
            attributes=JsonApiDashboardPluginInAttributes(
                are_relations_valid=True,
                content={},
                description="description_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            type="dashboardPlugin",
        ),
    ) # JsonApiDashboardPluginInDocument | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put a Plugin
        api_response = api_instance.update_entity_dashboard_plugins(workspace_id, object_id, json_api_dashboard_plugin_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_dashboard_plugins: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Plugin
        api_response = api_instance.update_entity_dashboard_plugins(workspace_id, object_id, json_api_dashboard_plugin_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_dashboard_plugins: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_dashboard_plugin_in_document** | [**JsonApiDashboardPluginInDocument**](JsonApiDashboardPluginInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiDashboardPluginOutDocument**](JsonApiDashboardPluginOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_data_sources**
> JsonApiDataSourceOutDocument update_entity_data_sources(id, json_api_data_source_in_document)

Put Data Source entity

Data Source - represents data source for the workspace

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_data_source_in_document import JsonApiDataSourceInDocument
from gooddata_api_client.model.json_api_data_source_out_document import JsonApiDataSourceOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_data_source_in_document = JsonApiDataSourceInDocument(
        data=JsonApiDataSourceIn(
            attributes=JsonApiDataSourceInAttributes(
                cache_path=[
                    "cache_path_example",
                ],
                enable_caching=False,
                name="name_example",
                parameters=[
                    JsonApiDataSourceInAttributesParametersInner(
                        name="name_example",
                        value="value_example",
                    ),
                ],
                password="password_example",
                schema="schema_example",
                token="token_example",
                type="POSTGRESQL",
                url="url_example",
                username="username_example",
            ),
            id="id1",
            type="dataSource",
        ),
    ) # JsonApiDataSourceInDocument | 
    filter = "filter=name==someString;type==DatabaseTypeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put Data Source entity
        api_response = api_instance.update_entity_data_sources(id, json_api_data_source_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_data_sources: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put Data Source entity
        api_response = api_instance.update_entity_data_sources(id, json_api_data_source_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_data_sources: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_data_source_in_document** | [**JsonApiDataSourceInDocument**](JsonApiDataSourceInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiDataSourceOutDocument**](JsonApiDataSourceOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_filter_contexts**
> JsonApiFilterContextOutDocument update_entity_filter_contexts(workspace_id, object_id, json_api_filter_context_in_document)

Put a Context Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_filter_context_in_document import JsonApiFilterContextInDocument
from gooddata_api_client.model.json_api_filter_context_out_document import JsonApiFilterContextOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_filter_context_in_document = JsonApiFilterContextInDocument(
        data=JsonApiFilterContextIn(
            attributes=JsonApiAnalyticalDashboardInAttributes(
                are_relations_valid=True,
                content={},
                description="description_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            type="filterContext",
        ),
    ) # JsonApiFilterContextInDocument | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=attributes,datasets,labels",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put a Context Filter
        api_response = api_instance.update_entity_filter_contexts(workspace_id, object_id, json_api_filter_context_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_filter_contexts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Context Filter
        api_response = api_instance.update_entity_filter_contexts(workspace_id, object_id, json_api_filter_context_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_filter_contexts: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_filter_context_in_document** | [**JsonApiFilterContextInDocument**](JsonApiFilterContextInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiFilterContextOutDocument**](JsonApiFilterContextOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_jwks**
> JsonApiJwkOutDocument update_entity_jwks(id, json_api_jwk_in_document)

Put Jwk

Updates JSON web key - used to verify JSON web tokens (Jwts)

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_jwk_in_document import JsonApiJwkInDocument
from gooddata_api_client.model.json_api_jwk_out_document import JsonApiJwkOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_jwk_in_document = JsonApiJwkInDocument(
        data=JsonApiJwkIn(
            attributes=JsonApiJwkInAttributes(
                content=JsonApiJwkInAttributesContent(),
            ),
            id="id1",
            type="jwk",
        ),
    ) # JsonApiJwkInDocument | 
    filter = "filter=content==JwkSpecificationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put Jwk
        api_response = api_instance.update_entity_jwks(id, json_api_jwk_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_jwks: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put Jwk
        api_response = api_instance.update_entity_jwks(id, json_api_jwk_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_jwks: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_jwk_in_document** | [**JsonApiJwkInDocument**](JsonApiJwkInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiJwkOutDocument**](JsonApiJwkOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_metrics**
> JsonApiMetricOutDocument update_entity_metrics(workspace_id, object_id, json_api_metric_in_document)

Put a Metric

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_metric_in_document import JsonApiMetricInDocument
from gooddata_api_client.model.json_api_metric_out_document import JsonApiMetricOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_metric_in_document = JsonApiMetricInDocument(
        data=JsonApiMetricIn(
            attributes=JsonApiMetricInAttributes(
                are_relations_valid=True,
                content=JsonApiMetricInAttributesContent(
                    format="format_example",
                    maql="maql_example",
                ),
                description="description_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            type="metric",
        ),
    ) # JsonApiMetricInDocument | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put a Metric
        api_response = api_instance.update_entity_metrics(workspace_id, object_id, json_api_metric_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_metrics: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Metric
        api_response = api_instance.update_entity_metrics(workspace_id, object_id, json_api_metric_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_metrics: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_metric_in_document** | [**JsonApiMetricInDocument**](JsonApiMetricInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiMetricOutDocument**](JsonApiMetricOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_organization_settings**
> JsonApiOrganizationSettingOutDocument update_entity_organization_settings(id, json_api_organization_setting_in_document)

Put Organization entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_organization_setting_in_document import JsonApiOrganizationSettingInDocument
from gooddata_api_client.model.json_api_organization_setting_out_document import JsonApiOrganizationSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_organization_setting_in_document = JsonApiOrganizationSettingInDocument(
        data=JsonApiOrganizationSettingIn(
            attributes=JsonApiOrganizationSettingInAttributes(
                content={},
                type="TIMEZONE",
            ),
            id="id1",
            type="organizationSetting",
        ),
    ) # JsonApiOrganizationSettingInDocument | 
    filter = "filter=content==JsonNodeValue;type==SettingConfigurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put Organization entity
        api_response = api_instance.update_entity_organization_settings(id, json_api_organization_setting_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_organization_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put Organization entity
        api_response = api_instance.update_entity_organization_settings(id, json_api_organization_setting_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_organization_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_organization_setting_in_document** | [**JsonApiOrganizationSettingInDocument**](JsonApiOrganizationSettingInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiOrganizationSettingOutDocument**](JsonApiOrganizationSettingOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_organizations**
> JsonApiOrganizationOutDocument update_entity_organizations(id, json_api_organization_in_document)

Put Organization

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_organization_out_document import JsonApiOrganizationOutDocument
from gooddata_api_client.model.json_api_organization_in_document import JsonApiOrganizationInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_organization_in_document = JsonApiOrganizationInDocument(
        data=JsonApiOrganizationIn(
            attributes=JsonApiOrganizationInAttributes(
                allowed_origins=[
                    "allowed_origins_example",
                ],
                early_access="early_access_example",
                hostname="hostname_example",
                name="name_example",
                oauth_client_id="oauth_client_id_example",
                oauth_client_secret="oauth_client_secret_example",
                oauth_issuer_id="myOidcProvider",
                oauth_issuer_location="oauth_issuer_location_example",
            ),
            id="id1",
            type="organization",
        ),
    ) # JsonApiOrganizationInDocument | 
    filter = "filter=name==someString;hostname==someString;bootstrapUser.id==321;bootstrapUserGroup.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=bootstrapUser,bootstrapUserGroup",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put Organization
        api_response = api_instance.update_entity_organizations(id, json_api_organization_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_organizations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put Organization
        api_response = api_instance.update_entity_organizations(id, json_api_organization_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_organizations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_organization_in_document** | [**JsonApiOrganizationInDocument**](JsonApiOrganizationInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiOrganizationOutDocument**](JsonApiOrganizationOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_themes**
> JsonApiThemeOutDocument update_entity_themes(id, json_api_theme_in_document)

Put Theming

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_theme_in_document import JsonApiThemeInDocument
from gooddata_api_client.model.json_api_theme_out_document import JsonApiThemeOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_theme_in_document = JsonApiThemeInDocument(
        data=JsonApiThemeIn(
            attributes=JsonApiColorPaletteInAttributes(
                content={},
                name="name_example",
            ),
            id="id1",
            type="theme",
        ),
    ) # JsonApiThemeInDocument | 
    filter = "filter=name==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put Theming
        api_response = api_instance.update_entity_themes(id, json_api_theme_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_themes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put Theming
        api_response = api_instance.update_entity_themes(id, json_api_theme_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_themes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_theme_in_document** | [**JsonApiThemeInDocument**](JsonApiThemeInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiThemeOutDocument**](JsonApiThemeOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_user_data_filters**
> JsonApiUserDataFilterOutDocument update_entity_user_data_filters(workspace_id, object_id, json_api_user_data_filter_in_document)

Put a User Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_user_data_filter_out_document import JsonApiUserDataFilterOutDocument
from gooddata_api_client.model.json_api_user_data_filter_in_document import JsonApiUserDataFilterInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_user_data_filter_in_document = JsonApiUserDataFilterInDocument(
        data=JsonApiUserDataFilterIn(
            attributes=JsonApiUserDataFilterInAttributes(
                are_relations_valid=True,
                description="description_example",
                maql="maql_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            relationships=JsonApiUserDataFilterInRelationships(
                user=JsonApiOrganizationOutRelationshipsBootstrapUser(
                    data=JsonApiUserToOneLinkage(None),
                ),
                user_group=JsonApiOrganizationOutRelationshipsBootstrapUserGroup(
                    data=JsonApiUserGroupToOneLinkage(None),
                ),
            ),
            type="userDataFilter",
        ),
    ) # JsonApiUserDataFilterInDocument | 
    filter = "filter=title==someString;description==someString;user.id==321;userGroup.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=user,userGroup,facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put a User Data Filter
        api_response = api_instance.update_entity_user_data_filters(workspace_id, object_id, json_api_user_data_filter_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_user_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a User Data Filter
        api_response = api_instance.update_entity_user_data_filters(workspace_id, object_id, json_api_user_data_filter_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_user_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_user_data_filter_in_document** | [**JsonApiUserDataFilterInDocument**](JsonApiUserDataFilterInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiUserDataFilterOutDocument**](JsonApiUserDataFilterOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_user_groups**
> JsonApiUserGroupOutDocument update_entity_user_groups(id, json_api_user_group_in_document)

Put UserGroup entity

User Group - creates tree-like structure for categorizing users

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_user_group_in_document import JsonApiUserGroupInDocument
from gooddata_api_client.model.json_api_user_group_out_document import JsonApiUserGroupOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_user_group_in_document = JsonApiUserGroupInDocument(
        data=JsonApiUserGroupIn(
            attributes=JsonApiUserGroupInAttributes(
                name="name_example",
            ),
            id="id1",
            relationships=JsonApiUserGroupInRelationships(
                parents=JsonApiUserGroupInRelationshipsParents(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        ),
                    ]),
                ),
            ),
            type="userGroup",
        ),
    ) # JsonApiUserGroupInDocument | 
    filter = "filter=name==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=parents",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put UserGroup entity
        api_response = api_instance.update_entity_user_groups(id, json_api_user_group_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_user_groups: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put UserGroup entity
        api_response = api_instance.update_entity_user_groups(id, json_api_user_group_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_user_groups: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_user_group_in_document** | [**JsonApiUserGroupInDocument**](JsonApiUserGroupInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiUserGroupOutDocument**](JsonApiUserGroupOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_user_settings**
> JsonApiUserSettingOutDocument update_entity_user_settings(user_id, id, json_api_user_setting_in_document)

Put new user settings for the user

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_user_setting_out_document import JsonApiUserSettingOutDocument
from gooddata_api_client.model.json_api_user_setting_in_document import JsonApiUserSettingInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    user_id = "userId_example" # str | 
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_user_setting_in_document = JsonApiUserSettingInDocument(
        data=JsonApiUserSettingIn(
            attributes=JsonApiOrganizationSettingInAttributes(
                content={},
                type="TIMEZONE",
            ),
            id="id1",
            type="userSetting",
        ),
    ) # JsonApiUserSettingInDocument | 
    filter = "filter=content==JsonNodeValue;type==SettingConfigurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put new user settings for the user
        api_response = api_instance.update_entity_user_settings(user_id, id, json_api_user_setting_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_user_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put new user settings for the user
        api_response = api_instance.update_entity_user_settings(user_id, id, json_api_user_setting_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_user_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  |
 **id** | **str**|  |
 **json_api_user_setting_in_document** | [**JsonApiUserSettingInDocument**](JsonApiUserSettingInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiUserSettingOutDocument**](JsonApiUserSettingOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_users**
> JsonApiUserOutDocument update_entity_users(id, json_api_user_in_document)

Put User entity

User - represents entity interacting with platform

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_user_in_document import JsonApiUserInDocument
from gooddata_api_client.model.json_api_user_out_document import JsonApiUserOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_user_in_document = JsonApiUserInDocument(
        data=JsonApiUserIn(
            attributes=JsonApiUserInAttributes(
                authentication_id="authentication_id_example",
                email="email_example",
                firstname="firstname_example",
                lastname="lastname_example",
            ),
            id="id1",
            relationships=JsonApiUserInRelationships(
                user_groups=JsonApiUserGroupInRelationshipsParents(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        ),
                    ]),
                ),
            ),
            type="user",
        ),
    ) # JsonApiUserInDocument | 
    filter = "filter=authenticationId==someString;firstname==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=userGroups",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put User entity
        api_response = api_instance.update_entity_users(id, json_api_user_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_users: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put User entity
        api_response = api_instance.update_entity_users(id, json_api_user_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_users: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_user_in_document** | [**JsonApiUserInDocument**](JsonApiUserInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiUserOutDocument**](JsonApiUserOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_visualization_objects**
> JsonApiVisualizationObjectOutDocument update_entity_visualization_objects(workspace_id, object_id, json_api_visualization_object_in_document)

Put a Visualization Object

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_visualization_object_out_document import JsonApiVisualizationObjectOutDocument
from gooddata_api_client.model.json_api_visualization_object_in_document import JsonApiVisualizationObjectInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_visualization_object_in_document = JsonApiVisualizationObjectInDocument(
        data=JsonApiVisualizationObjectIn(
            attributes=JsonApiAnalyticalDashboardInAttributes(
                are_relations_valid=True,
                content={},
                description="description_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            type="visualizationObject",
        ),
    ) # JsonApiVisualizationObjectInDocument | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put a Visualization Object
        api_response = api_instance.update_entity_visualization_objects(workspace_id, object_id, json_api_visualization_object_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_visualization_objects: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Visualization Object
        api_response = api_instance.update_entity_visualization_objects(workspace_id, object_id, json_api_visualization_object_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_visualization_objects: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_visualization_object_in_document** | [**JsonApiVisualizationObjectInDocument**](JsonApiVisualizationObjectInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiVisualizationObjectOutDocument**](JsonApiVisualizationObjectOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_workspace_data_filter_settings**
> JsonApiWorkspaceDataFilterSettingOutDocument update_entity_workspace_data_filter_settings(workspace_id, object_id, json_api_workspace_data_filter_setting_in_document)

Put a Settings for Workspace Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_workspace_data_filter_setting_in_document import JsonApiWorkspaceDataFilterSettingInDocument
from gooddata_api_client.model.json_api_workspace_data_filter_setting_out_document import JsonApiWorkspaceDataFilterSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_workspace_data_filter_setting_in_document = JsonApiWorkspaceDataFilterSettingInDocument(
        data=JsonApiWorkspaceDataFilterSettingIn(
            attributes=JsonApiWorkspaceDataFilterSettingInAttributes(
                description="description_example",
                filter_values=[
                    "filter_values_example",
                ],
                title="title_example",
            ),
            id="id1",
            relationships=JsonApiWorkspaceDataFilterSettingInRelationships(
                workspace_data_filter=JsonApiWorkspaceDataFilterSettingInRelationshipsWorkspaceDataFilter(
                    data=JsonApiWorkspaceDataFilterToOneLinkage(None),
                ),
            ),
            type="workspaceDataFilterSetting",
        ),
    ) # JsonApiWorkspaceDataFilterSettingInDocument | 
    filter = "filter=title==someString;description==someString;workspaceDataFilter.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=workspaceDataFilter",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put a Settings for Workspace Data Filter
        api_response = api_instance.update_entity_workspace_data_filter_settings(workspace_id, object_id, json_api_workspace_data_filter_setting_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_workspace_data_filter_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Settings for Workspace Data Filter
        api_response = api_instance.update_entity_workspace_data_filter_settings(workspace_id, object_id, json_api_workspace_data_filter_setting_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_workspace_data_filter_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_workspace_data_filter_setting_in_document** | [**JsonApiWorkspaceDataFilterSettingInDocument**](JsonApiWorkspaceDataFilterSettingInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiWorkspaceDataFilterSettingOutDocument**](JsonApiWorkspaceDataFilterSettingOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_workspace_data_filters**
> JsonApiWorkspaceDataFilterOutDocument update_entity_workspace_data_filters(workspace_id, object_id, json_api_workspace_data_filter_in_document)

Put a Workspace Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_workspace_data_filter_out_document import JsonApiWorkspaceDataFilterOutDocument
from gooddata_api_client.model.json_api_workspace_data_filter_in_document import JsonApiWorkspaceDataFilterInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_workspace_data_filter_in_document = JsonApiWorkspaceDataFilterInDocument(
        data=JsonApiWorkspaceDataFilterIn(
            attributes=JsonApiWorkspaceDataFilterInAttributes(
                column_name="column_name_example",
                description="description_example",
                title="title_example",
            ),
            id="id1",
            relationships=JsonApiWorkspaceDataFilterInRelationships(
                filter_settings=JsonApiWorkspaceDataFilterInRelationshipsFilterSettings(
                    data=JsonApiWorkspaceDataFilterSettingToManyLinkage([
                        JsonApiWorkspaceDataFilterSettingLinkage(
                            id="id_example",
                            type="workspaceDataFilterSetting",
                        ),
                    ]),
                ),
            ),
            type="workspaceDataFilter",
        ),
    ) # JsonApiWorkspaceDataFilterInDocument | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=filterSettings",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put a Workspace Data Filter
        api_response = api_instance.update_entity_workspace_data_filters(workspace_id, object_id, json_api_workspace_data_filter_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_workspace_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Workspace Data Filter
        api_response = api_instance.update_entity_workspace_data_filters(workspace_id, object_id, json_api_workspace_data_filter_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_workspace_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_workspace_data_filter_in_document** | [**JsonApiWorkspaceDataFilterInDocument**](JsonApiWorkspaceDataFilterInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiWorkspaceDataFilterOutDocument**](JsonApiWorkspaceDataFilterOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_workspace_settings**
> JsonApiWorkspaceSettingOutDocument update_entity_workspace_settings(workspace_id, object_id, json_api_workspace_setting_in_document)

Put a Setting for a Workspace

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_workspace_setting_in_document import JsonApiWorkspaceSettingInDocument
from gooddata_api_client.model.json_api_workspace_setting_out_document import JsonApiWorkspaceSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_workspace_setting_in_document = JsonApiWorkspaceSettingInDocument(
        data=JsonApiWorkspaceSettingIn(
            attributes=JsonApiOrganizationSettingInAttributes(
                content={},
                type="TIMEZONE",
            ),
            id="id1",
            type="workspaceSetting",
        ),
    ) # JsonApiWorkspaceSettingInDocument | 
    filter = "filter=content==JsonNodeValue;type==SettingConfigurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put a Setting for a Workspace
        api_response = api_instance.update_entity_workspace_settings(workspace_id, object_id, json_api_workspace_setting_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_workspace_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Setting for a Workspace
        api_response = api_instance.update_entity_workspace_settings(workspace_id, object_id, json_api_workspace_setting_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_workspace_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_workspace_setting_in_document** | [**JsonApiWorkspaceSettingInDocument**](JsonApiWorkspaceSettingInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiWorkspaceSettingOutDocument**](JsonApiWorkspaceSettingOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_workspaces**
> JsonApiWorkspaceOutDocument update_entity_workspaces(id, json_api_workspace_in_document)

Put Workspace entity

Space of the shared interest

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entities_api
from gooddata_api_client.model.json_api_workspace_out_document import JsonApiWorkspaceOutDocument
from gooddata_api_client.model.json_api_workspace_in_document import JsonApiWorkspaceInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entities_api.EntitiesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_workspace_in_document = JsonApiWorkspaceInDocument(
        data=JsonApiWorkspaceIn(
            attributes=JsonApiWorkspaceInAttributes(
                cache_extra_limit=1,
                description="description_example",
                early_access="early_access_example",
                name="name_example",
                prefix="/6bUUGjjNSwg0_bs",
            ),
            id="id1",
            relationships=JsonApiWorkspaceInRelationships(
                parent=JsonApiWorkspaceInRelationshipsParent(
                    data=JsonApiWorkspaceToOneLinkage(None),
                ),
            ),
            type="workspace",
        ),
    ) # JsonApiWorkspaceInDocument | 
    filter = "filter=name==someString;earlyAccess==someString;parent.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=parent",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put Workspace entity
        api_response = api_instance.update_entity_workspaces(id, json_api_workspace_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_workspaces: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put Workspace entity
        api_response = api_instance.update_entity_workspaces(id, json_api_workspace_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitiesApi->update_entity_workspaces: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_workspace_in_document** | [**JsonApiWorkspaceInDocument**](JsonApiWorkspaceInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiWorkspaceOutDocument**](JsonApiWorkspaceOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


# gooddata_api_client.ActionsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**ai_chat**](ActionsApi.md#ai_chat) | **POST** /api/v1/actions/workspaces/{workspaceId}/ai/chat | (BETA) Chat with AI
[**ai_chat_history**](ActionsApi.md#ai_chat_history) | **POST** /api/v1/actions/workspaces/{workspaceId}/ai/chatHistory | (BETA) Get Chat History
[**ai_chat_stream**](ActionsApi.md#ai_chat_stream) | **POST** /api/v1/actions/workspaces/{workspaceId}/ai/chatStream | (BETA) Chat with AI
[**ai_chat_usage**](ActionsApi.md#ai_chat_usage) | **GET** /api/v1/actions/workspaces/{workspaceId}/ai/chatUsage | Get Chat Usage
[**ai_search**](ActionsApi.md#ai_search) | **POST** /api/v1/actions/workspaces/{workspaceId}/ai/search | (BETA) Semantic Search in Metadata
[**all_platform_usage**](ActionsApi.md#all_platform_usage) | **GET** /api/v1/actions/collectUsage | Info about the platform usage.
[**anomaly_detection**](ActionsApi.md#anomaly_detection) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/functions/anomalyDetection/{resultId} | (EXPERIMENTAL) Smart functions - Anomaly Detection
[**anomaly_detection_result**](ActionsApi.md#anomaly_detection_result) | **GET** /api/v1/actions/workspaces/{workspaceId}/execution/functions/anomalyDetection/result/{resultId} | (EXPERIMENTAL) Smart functions - Anomaly Detection Result
[**available_assignees**](ActionsApi.md#available_assignees) | **GET** /api/v1/actions/workspaces/{workspaceId}/analyticalDashboards/{dashboardId}/availableAssignees | Get Available Assignees
[**cancel_executions**](ActionsApi.md#cancel_executions) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/afm/cancel | Applies all the given cancel tokens.
[**check_entity_overrides**](ActionsApi.md#check_entity_overrides) | **POST** /api/v1/actions/workspaces/{workspaceId}/checkEntityOverrides | Finds entities with given ID in hierarchy.
[**clean_translations**](ActionsApi.md#clean_translations) | **POST** /api/v1/actions/workspaces/{workspaceId}/translations/clean | Cleans up translations.
[**clustering**](ActionsApi.md#clustering) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/functions/clustering/{resultId} | (EXPERIMENTAL) Smart functions - Clustering
[**clustering_result**](ActionsApi.md#clustering_result) | **GET** /api/v1/actions/workspaces/{workspaceId}/execution/functions/clustering/result/{resultId} | (EXPERIMENTAL) Smart functions - Clustering Result
[**column_statistics**](ActionsApi.md#column_statistics) | **POST** /api/v1/actions/dataSources/{dataSourceId}/computeColumnStatistics | (EXPERIMENTAL) Compute column statistics
[**compute_label_elements_post**](ActionsApi.md#compute_label_elements_post) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/collectLabelElements | Listing of label values. The resulting data are limited by the static platform limit to the maximum of 10000 rows.
[**compute_report**](ActionsApi.md#compute_report) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/afm/execute | Executes analytical request and returns link to the result
[**compute_valid_descendants**](ActionsApi.md#compute_valid_descendants) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/afm/computeValidDescendants | (BETA) Valid descendants
[**compute_valid_objects**](ActionsApi.md#compute_valid_objects) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/afm/computeValidObjects | Valid objects
[**create_dashboard_export_request**](ActionsApi.md#create_dashboard_export_request) | **POST** /api/v1/actions/workspaces/{workspaceId}/analyticalDashboards/{dashboardId}/export/tabular | (EXPERIMENTAL) Create dashboard tabular export request
[**create_image_export**](ActionsApi.md#create_image_export) | **POST** /api/v1/actions/workspaces/{workspaceId}/export/image | (EXPERIMENTAL) Create image export request
[**create_memory_item**](ActionsApi.md#create_memory_item) | **POST** /api/v1/actions/workspaces/{workspaceId}/ai/memory | (EXPERIMENTAL) Create new memory item
[**create_pdf_export**](ActionsApi.md#create_pdf_export) | **POST** /api/v1/actions/workspaces/{workspaceId}/export/visual | Create visual - pdf export request
[**create_raw_export**](ActionsApi.md#create_raw_export) | **POST** /api/v1/actions/workspaces/{workspaceId}/export/raw | (EXPERIMENTAL) Create raw export request
[**create_slides_export**](ActionsApi.md#create_slides_export) | **POST** /api/v1/actions/workspaces/{workspaceId}/export/slides | (EXPERIMENTAL) Create slides export request
[**create_tabular_export**](ActionsApi.md#create_tabular_export) | **POST** /api/v1/actions/workspaces/{workspaceId}/export/tabular | Create tabular export request
[**dashboard_permissions**](ActionsApi.md#dashboard_permissions) | **GET** /api/v1/actions/workspaces/{workspaceId}/analyticalDashboards/{dashboardId}/permissions | Get Dashboard Permissions
[**delete_organization_automations**](ActionsApi.md#delete_organization_automations) | **POST** /api/v1/actions/organization/automations/delete | Delete selected automations across all workspaces
[**delete_workspace_automations**](ActionsApi.md#delete_workspace_automations) | **POST** /api/v1/actions/workspaces/{workspaceId}/automations/delete | Delete selected automations in the workspace
[**explain_afm**](ActionsApi.md#explain_afm) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/afm/explain | AFM explain resource.
[**forecast**](ActionsApi.md#forecast) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/functions/forecast/{resultId} | (BETA) Smart functions - Forecast
[**forecast_result**](ActionsApi.md#forecast_result) | **GET** /api/v1/actions/workspaces/{workspaceId}/execution/functions/forecast/result/{resultId} | (BETA) Smart functions - Forecast Result
[**generate_logical_model**](ActionsApi.md#generate_logical_model) | **POST** /api/v1/actions/dataSources/{dataSourceId}/generateLogicalModel | Generate logical data model (LDM) from physical data model (PDM)
[**get_data_source_schemata**](ActionsApi.md#get_data_source_schemata) | **GET** /api/v1/actions/dataSources/{dataSourceId}/scanSchemata | Get a list of schema names of a database
[**get_dependent_entities_graph**](ActionsApi.md#get_dependent_entities_graph) | **GET** /api/v1/actions/workspaces/{workspaceId}/dependentEntitiesGraph | Computes the dependent entities graph
[**get_dependent_entities_graph_from_entry_points**](ActionsApi.md#get_dependent_entities_graph_from_entry_points) | **POST** /api/v1/actions/workspaces/{workspaceId}/dependentEntitiesGraph | Computes the dependent entities graph from given entry points
[**get_exported_file**](ActionsApi.md#get_exported_file) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/visual/{exportId} | Retrieve exported files
[**get_image_export**](ActionsApi.md#get_image_export) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/image/{exportId} | (EXPERIMENTAL) Retrieve exported files
[**get_image_export_metadata**](ActionsApi.md#get_image_export_metadata) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/image/{exportId}/metadata | (EXPERIMENTAL) Retrieve metadata context
[**get_memory_item**](ActionsApi.md#get_memory_item) | **GET** /api/v1/actions/workspaces/{workspaceId}/ai/memory/{memoryId} | (EXPERIMENTAL) Get memory item
[**get_metadata**](ActionsApi.md#get_metadata) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/visual/{exportId}/metadata | Retrieve metadata context
[**get_notifications**](ActionsApi.md#get_notifications) | **GET** /api/v1/actions/notifications | Get latest notifications.
[**get_quality_issues**](ActionsApi.md#get_quality_issues) | **GET** /api/v1/actions/workspaces/{workspaceId}/ai/issues | Get Quality Issues
[**get_raw_export**](ActionsApi.md#get_raw_export) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/raw/{exportId} | (EXPERIMENTAL) Retrieve exported files
[**get_slides_export**](ActionsApi.md#get_slides_export) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/slides/{exportId} | (EXPERIMENTAL) Retrieve exported files
[**get_slides_export_metadata**](ActionsApi.md#get_slides_export_metadata) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/slides/{exportId}/metadata | (EXPERIMENTAL) Retrieve metadata context
[**get_tabular_export**](ActionsApi.md#get_tabular_export) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/tabular/{exportId} | Retrieve exported files
[**get_translation_tags**](ActionsApi.md#get_translation_tags) | **GET** /api/v1/actions/workspaces/{workspaceId}/translations | Get translation tags.
[**inherited_entity_conflicts**](ActionsApi.md#inherited_entity_conflicts) | **GET** /api/v1/actions/workspaces/{workspaceId}/inheritedEntityConflicts | Finds identifier conflicts in workspace hierarchy.
[**inherited_entity_prefixes**](ActionsApi.md#inherited_entity_prefixes) | **GET** /api/v1/actions/workspaces/{workspaceId}/inheritedEntityPrefixes | Get used entity prefixes in hierarchy
[**key_driver_analysis**](ActionsApi.md#key_driver_analysis) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/computeKeyDrivers | (EXPERIMENTAL) Compute key driver analysis
[**key_driver_analysis_result**](ActionsApi.md#key_driver_analysis_result) | **GET** /api/v1/actions/workspaces/{workspaceId}/execution/computeKeyDrivers/result/{resultId} | (EXPERIMENTAL) Get key driver analysis result
[**list_memory_items**](ActionsApi.md#list_memory_items) | **GET** /api/v1/actions/workspaces/{workspaceId}/ai/memory | (EXPERIMENTAL) List all memory items
[**list_workspace_user_groups**](ActionsApi.md#list_workspace_user_groups) | **GET** /api/v1/actions/workspaces/{workspaceId}/userGroups | 
[**list_workspace_users**](ActionsApi.md#list_workspace_users) | **GET** /api/v1/actions/workspaces/{workspaceId}/users | 
[**manage_dashboard_permissions**](ActionsApi.md#manage_dashboard_permissions) | **POST** /api/v1/actions/workspaces/{workspaceId}/analyticalDashboards/{dashboardId}/managePermissions | Manage Permissions for a Dashboard
[**manage_data_source_permissions**](ActionsApi.md#manage_data_source_permissions) | **POST** /api/v1/actions/dataSources/{dataSourceId}/managePermissions | Manage Permissions for a Data Source
[**manage_organization_permissions**](ActionsApi.md#manage_organization_permissions) | **POST** /api/v1/actions/organization/managePermissions | Manage Permissions for a Organization
[**manage_workspace_permissions**](ActionsApi.md#manage_workspace_permissions) | **POST** /api/v1/actions/workspaces/{workspaceId}/managePermissions | Manage Permissions for a Workspace
[**mark_as_read_notification**](ActionsApi.md#mark_as_read_notification) | **POST** /api/v1/actions/notifications/{notificationId}/markAsRead | Mark notification as read.
[**mark_as_read_notification_all**](ActionsApi.md#mark_as_read_notification_all) | **POST** /api/v1/actions/notifications/markAsRead | Mark all notifications as read.
[**metadata_sync**](ActionsApi.md#metadata_sync) | **POST** /api/v1/actions/workspaces/{workspaceId}/metadataSync | (BETA) Sync Metadata to other services
[**metadata_sync_organization**](ActionsApi.md#metadata_sync_organization) | **POST** /api/v1/actions/organization/metadataSync | (BETA) Sync organization scope Metadata to other services
[**overridden_child_entities**](ActionsApi.md#overridden_child_entities) | **GET** /api/v1/actions/workspaces/{workspaceId}/overriddenChildEntities | Finds identifier overrides in workspace hierarchy.
[**particular_platform_usage**](ActionsApi.md#particular_platform_usage) | **POST** /api/v1/actions/collectUsage | Info about the platform usage for particular items.
[**pause_organization_automations**](ActionsApi.md#pause_organization_automations) | **POST** /api/v1/actions/organization/automations/pause | Pause selected automations across all workspaces
[**pause_workspace_automations**](ActionsApi.md#pause_workspace_automations) | **POST** /api/v1/actions/workspaces/{workspaceId}/automations/pause | Pause selected automations in the workspace
[**register_upload_notification**](ActionsApi.md#register_upload_notification) | **POST** /api/v1/actions/dataSources/{dataSourceId}/uploadNotification | Register an upload notification
[**remove_memory_item**](ActionsApi.md#remove_memory_item) | **DELETE** /api/v1/actions/workspaces/{workspaceId}/ai/memory/{memoryId} | (EXPERIMENTAL) Remove memory item
[**resolve_all_entitlements**](ActionsApi.md#resolve_all_entitlements) | **GET** /api/v1/actions/resolveEntitlements | Values for all public entitlements.
[**resolve_all_settings_without_workspace**](ActionsApi.md#resolve_all_settings_without_workspace) | **GET** /api/v1/actions/resolveSettings | Values for all settings without workspace.
[**resolve_llm_endpoints**](ActionsApi.md#resolve_llm_endpoints) | **GET** /api/v1/actions/workspaces/{workspaceId}/ai/resolveLlmEndpoints | Get Active LLM Endpoints for this workspace
[**resolve_requested_entitlements**](ActionsApi.md#resolve_requested_entitlements) | **POST** /api/v1/actions/resolveEntitlements | Values for requested public entitlements.
[**resolve_settings_without_workspace**](ActionsApi.md#resolve_settings_without_workspace) | **POST** /api/v1/actions/resolveSettings | Values for selected settings without workspace.
[**retrieve_execution_metadata**](ActionsApi.md#retrieve_execution_metadata) | **GET** /api/v1/actions/workspaces/{workspaceId}/execution/afm/execute/result/{resultId}/metadata | Get a single execution result&#39;s metadata.
[**retrieve_result**](ActionsApi.md#retrieve_result) | **GET** /api/v1/actions/workspaces/{workspaceId}/execution/afm/execute/result/{resultId} | Get a single execution result
[**retrieve_translations**](ActionsApi.md#retrieve_translations) | **POST** /api/v1/actions/workspaces/{workspaceId}/translations/retrieve | Retrieve translations for entities.
[**scan_data_source**](ActionsApi.md#scan_data_source) | **POST** /api/v1/actions/dataSources/{dataSourceId}/scan | Scan a database to get a physical data model (PDM)
[**scan_sql**](ActionsApi.md#scan_sql) | **POST** /api/v1/actions/dataSources/{dataSourceId}/scanSql | Collect metadata about SQL query
[**set_translations**](ActionsApi.md#set_translations) | **POST** /api/v1/actions/workspaces/{workspaceId}/translations/set | Set translations for entities.
[**switch_active_identity_provider**](ActionsApi.md#switch_active_identity_provider) | **POST** /api/v1/actions/organization/switchActiveIdentityProvider | Switch Active Identity Provider
[**tags**](ActionsApi.md#tags) | **GET** /api/v1/actions/workspaces/{workspaceId}/ai/analyticsCatalog/tags | Get Analytics Catalog Tags
[**test_data_source**](ActionsApi.md#test_data_source) | **POST** /api/v1/actions/dataSources/{dataSourceId}/test | Test data source connection by data source id
[**test_data_source_definition**](ActionsApi.md#test_data_source_definition) | **POST** /api/v1/actions/dataSource/test | Test connection by data source definition
[**test_existing_notification_channel**](ActionsApi.md#test_existing_notification_channel) | **POST** /api/v1/actions/notificationChannels/{notificationChannelId}/test | Test existing notification channel.
[**test_notification_channel**](ActionsApi.md#test_notification_channel) | **POST** /api/v1/actions/notificationChannels/test | Test notification channel.
[**trigger_automation**](ActionsApi.md#trigger_automation) | **POST** /api/v1/actions/workspaces/{workspaceId}/automations/trigger | Trigger automation.
[**trigger_existing_automation**](ActionsApi.md#trigger_existing_automation) | **POST** /api/v1/actions/workspaces/{workspaceId}/automations/{automationId}/trigger | Trigger existing automation.
[**unpause_organization_automations**](ActionsApi.md#unpause_organization_automations) | **POST** /api/v1/actions/organization/automations/unpause | Unpause selected automations across all workspaces
[**unpause_workspace_automations**](ActionsApi.md#unpause_workspace_automations) | **POST** /api/v1/actions/workspaces/{workspaceId}/automations/unpause | Unpause selected automations in the workspace
[**unsubscribe_all_automations**](ActionsApi.md#unsubscribe_all_automations) | **DELETE** /api/v1/actions/organization/automations/unsubscribe | Unsubscribe from all automations in all workspaces
[**unsubscribe_automation**](ActionsApi.md#unsubscribe_automation) | **DELETE** /api/v1/actions/workspaces/{workspaceId}/automations/{automationId}/unsubscribe | Unsubscribe from an automation
[**unsubscribe_organization_automations**](ActionsApi.md#unsubscribe_organization_automations) | **POST** /api/v1/actions/organization/automations/unsubscribe | Unsubscribe from selected automations across all workspaces
[**unsubscribe_selected_workspace_automations**](ActionsApi.md#unsubscribe_selected_workspace_automations) | **POST** /api/v1/actions/workspaces/{workspaceId}/automations/unsubscribe | Unsubscribe from selected automations in the workspace
[**unsubscribe_workspace_automations**](ActionsApi.md#unsubscribe_workspace_automations) | **DELETE** /api/v1/actions/workspaces/{workspaceId}/automations/unsubscribe | Unsubscribe from all automations in the workspace
[**update_memory_item**](ActionsApi.md#update_memory_item) | **PUT** /api/v1/actions/workspaces/{workspaceId}/ai/memory/{memoryId} | (EXPERIMENTAL) Update memory item
[**validate_llm_endpoint**](ActionsApi.md#validate_llm_endpoint) | **POST** /api/v1/actions/ai/llmEndpoint/test | Validate LLM Endpoint
[**validate_llm_endpoint_by_id**](ActionsApi.md#validate_llm_endpoint_by_id) | **POST** /api/v1/actions/ai/llmEndpoint/{llmEndpointId}/test | Validate LLM Endpoint By Id
[**workspace_resolve_all_settings**](ActionsApi.md#workspace_resolve_all_settings) | **GET** /api/v1/actions/workspaces/{workspaceId}/resolveSettings | Values for all settings.
[**workspace_resolve_settings**](ActionsApi.md#workspace_resolve_settings) | **POST** /api/v1/actions/workspaces/{workspaceId}/resolveSettings | Values for selected settings.


# **ai_chat**
> ChatResult ai_chat(workspace_id, chat_request)

(BETA) Chat with AI

(BETA) Combines multiple use cases such as search, create visualizations, ...

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.chat_request import ChatRequest
from gooddata_api_client.models.chat_result import ChatResult
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    chat_request = gooddata_api_client.ChatRequest() # ChatRequest | 

    try:
        # (BETA) Chat with AI
        api_response = api_instance.ai_chat(workspace_id, chat_request)
        print("The response of ActionsApi->ai_chat:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->ai_chat: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **chat_request** | [**ChatRequest**](ChatRequest.md)|  | 

### Return type

[**ChatResult**](ChatResult.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ai_chat_history**
> ChatHistoryResult ai_chat_history(workspace_id, chat_history_request)

(BETA) Get Chat History

(BETA) Post thread ID (and optionally interaction ID) to get full/partial chat history.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.chat_history_request import ChatHistoryRequest
from gooddata_api_client.models.chat_history_result import ChatHistoryResult
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    chat_history_request = gooddata_api_client.ChatHistoryRequest() # ChatHistoryRequest | 

    try:
        # (BETA) Get Chat History
        api_response = api_instance.ai_chat_history(workspace_id, chat_history_request)
        print("The response of ActionsApi->ai_chat_history:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->ai_chat_history: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **chat_history_request** | [**ChatHistoryRequest**](ChatHistoryRequest.md)|  | 

### Return type

[**ChatHistoryResult**](ChatHistoryResult.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ai_chat_stream**
> List[object] ai_chat_stream(workspace_id, chat_request)

(BETA) Chat with AI

(BETA) Combines multiple use cases such as search, create visualizations, ...

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.chat_request import ChatRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    chat_request = gooddata_api_client.ChatRequest() # ChatRequest | 

    try:
        # (BETA) Chat with AI
        api_response = api_instance.ai_chat_stream(workspace_id, chat_request)
        print("The response of ActionsApi->ai_chat_stream:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->ai_chat_stream: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **chat_request** | [**ChatRequest**](ChatRequest.md)|  | 

### Return type

**List[object]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/event-stream

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ai_chat_usage**
> ChatUsageResponse ai_chat_usage(workspace_id)

Get Chat Usage

Returns usage statistics of chat for a user in a workspace.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.chat_usage_response import ChatUsageResponse
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier

    try:
        # Get Chat Usage
        api_response = api_instance.ai_chat_usage(workspace_id)
        print("The response of ActionsApi->ai_chat_usage:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->ai_chat_usage: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 

### Return type

[**ChatUsageResponse**](ChatUsageResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ai_search**
> SearchResult ai_search(workspace_id, search_request)

(BETA) Semantic Search in Metadata

(BETA) Uses similarity (e.g. cosine distance) search to find top X most similar metadata objects.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.search_request import SearchRequest
from gooddata_api_client.models.search_result import SearchResult
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    search_request = gooddata_api_client.SearchRequest() # SearchRequest | 

    try:
        # (BETA) Semantic Search in Metadata
        api_response = api_instance.ai_search(workspace_id, search_request)
        print("The response of ActionsApi->ai_search:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->ai_search: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **search_request** | [**SearchRequest**](SearchRequest.md)|  | 

### Return type

[**SearchResult**](SearchResult.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **all_platform_usage**
> List[PlatformUsage] all_platform_usage()

Info about the platform usage.

Provides information about platform usage, like amount of users, workspaces, ...  _NOTE_: The `admin` user is always excluded from this amount.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.platform_usage import PlatformUsage
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)

    try:
        # Info about the platform usage.
        api_response = api_instance.all_platform_usage()
        print("The response of ActionsApi->all_platform_usage:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->all_platform_usage: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[PlatformUsage]**](PlatformUsage.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **anomaly_detection**
> SmartFunctionResponse anomaly_detection(workspace_id, result_id, anomaly_detection_request, skip_cache=skip_cache)

(EXPERIMENTAL) Smart functions - Anomaly Detection

(EXPERIMENTAL) Computes anomaly detection.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.anomaly_detection_request import AnomalyDetectionRequest
from gooddata_api_client.models.smart_function_response import SmartFunctionResponse
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    result_id = '9bd52018570364264fcf62d373da6bed313120e8' # str | Input result ID to be used in the computation
    anomaly_detection_request = gooddata_api_client.AnomalyDetectionRequest() # AnomalyDetectionRequest | 
    skip_cache = False # bool | Ignore all caches during execution of current request. (optional) (default to False)

    try:
        # (EXPERIMENTAL) Smart functions - Anomaly Detection
        api_response = api_instance.anomaly_detection(workspace_id, result_id, anomaly_detection_request, skip_cache=skip_cache)
        print("The response of ActionsApi->anomaly_detection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->anomaly_detection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **result_id** | **str**| Input result ID to be used in the computation | 
 **anomaly_detection_request** | [**AnomalyDetectionRequest**](AnomalyDetectionRequest.md)|  | 
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional] [default to False]

### Return type

[**SmartFunctionResponse**](SmartFunctionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **anomaly_detection_result**
> AnomalyDetectionResult anomaly_detection_result(workspace_id, result_id, offset=offset, limit=limit)

(EXPERIMENTAL) Smart functions - Anomaly Detection Result

(EXPERIMENTAL) Gets anomalies.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.anomaly_detection_result import AnomalyDetectionResult
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    result_id = 'a9b28f9dc55f37ea9f4a5fb0c76895923591e781' # str | Result ID
    offset = 56 # int |  (optional)
    limit = 56 # int |  (optional)

    try:
        # (EXPERIMENTAL) Smart functions - Anomaly Detection Result
        api_response = api_instance.anomaly_detection_result(workspace_id, result_id, offset=offset, limit=limit)
        print("The response of ActionsApi->anomaly_detection_result:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->anomaly_detection_result: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **result_id** | **str**| Result ID | 
 **offset** | **int**|  | [optional] 
 **limit** | **int**|  | [optional] 

### Return type

[**AnomalyDetectionResult**](AnomalyDetectionResult.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **available_assignees**
> AvailableAssignees available_assignees(workspace_id, dashboard_id)

Get Available Assignees

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.available_assignees import AvailableAssignees
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    dashboard_id = 'dashboard_id_example' # str | 

    try:
        # Get Available Assignees
        api_response = api_instance.available_assignees(workspace_id, dashboard_id)
        print("The response of ActionsApi->available_assignees:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->available_assignees: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **dashboard_id** | **str**|  | 

### Return type

[**AvailableAssignees**](AvailableAssignees.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **cancel_executions**
> AfmCancelTokens cancel_executions(workspace_id, afm_cancel_tokens)

Applies all the given cancel tokens.

Each cancel token corresponds to one unique execution request for the same result id. If all cancel tokens for the same result id are applied, the execution for this result id is cancelled.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.afm_cancel_tokens import AfmCancelTokens
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    afm_cancel_tokens = gooddata_api_client.AfmCancelTokens() # AfmCancelTokens | 

    try:
        # Applies all the given cancel tokens.
        api_response = api_instance.cancel_executions(workspace_id, afm_cancel_tokens)
        print("The response of ActionsApi->cancel_executions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->cancel_executions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **afm_cancel_tokens** | [**AfmCancelTokens**](AfmCancelTokens.md)|  | 

### Return type

[**AfmCancelTokens**](AfmCancelTokens.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Status of the cancellation operation. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **check_entity_overrides**
> List[IdentifierDuplications] check_entity_overrides(workspace_id, hierarchy_object_identification)

Finds entities with given ID in hierarchy.

Finds entities with given ID in hierarchy (e.g. to check possible future conflicts).

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.hierarchy_object_identification import HierarchyObjectIdentification
from gooddata_api_client.models.identifier_duplications import IdentifierDuplications
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    hierarchy_object_identification = [gooddata_api_client.HierarchyObjectIdentification()] # List[HierarchyObjectIdentification] | 

    try:
        # Finds entities with given ID in hierarchy.
        api_response = api_instance.check_entity_overrides(workspace_id, hierarchy_object_identification)
        print("The response of ActionsApi->check_entity_overrides:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->check_entity_overrides: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **hierarchy_object_identification** | [**List[HierarchyObjectIdentification]**](HierarchyObjectIdentification.md)|  | 

### Return type

[**List[IdentifierDuplications]**](IdentifierDuplications.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Searching for entities finished successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clean_translations**
> clean_translations(workspace_id, locale_request)

Cleans up translations.

Cleans up all translations for a particular locale.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.locale_request import LocaleRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    locale_request = gooddata_api_client.LocaleRequest() # LocaleRequest | 

    try:
        # Cleans up translations.
        api_instance.clean_translations(workspace_id, locale_request)
    except Exception as e:
        print("Exception when calling ActionsApi->clean_translations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **locale_request** | [**LocaleRequest**](LocaleRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Translations were successfully removed. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clustering**
> SmartFunctionResponse clustering(workspace_id, result_id, clustering_request, skip_cache=skip_cache)

(EXPERIMENTAL) Smart functions - Clustering

(EXPERIMENTAL) Computes clusters for data points from the provided execution result and parameters.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.clustering_request import ClusteringRequest
from gooddata_api_client.models.smart_function_response import SmartFunctionResponse
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    result_id = '9bd52018570364264fcf62d373da6bed313120e8' # str | Input result ID to be used in the computation
    clustering_request = gooddata_api_client.ClusteringRequest() # ClusteringRequest | 
    skip_cache = False # bool | Ignore all caches during execution of current request. (optional) (default to False)

    try:
        # (EXPERIMENTAL) Smart functions - Clustering
        api_response = api_instance.clustering(workspace_id, result_id, clustering_request, skip_cache=skip_cache)
        print("The response of ActionsApi->clustering:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->clustering: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **result_id** | **str**| Input result ID to be used in the computation | 
 **clustering_request** | [**ClusteringRequest**](ClusteringRequest.md)|  | 
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional] [default to False]

### Return type

[**SmartFunctionResponse**](SmartFunctionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clustering_result**
> ClusteringResult clustering_result(workspace_id, result_id, offset=offset, limit=limit)

(EXPERIMENTAL) Smart functions - Clustering Result

(EXPERIMENTAL) Gets clustering result.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.clustering_result import ClusteringResult
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    result_id = 'a9b28f9dc55f37ea9f4a5fb0c76895923591e781' # str | Result ID
    offset = 56 # int |  (optional)
    limit = 56 # int |  (optional)

    try:
        # (EXPERIMENTAL) Smart functions - Clustering Result
        api_response = api_instance.clustering_result(workspace_id, result_id, offset=offset, limit=limit)
        print("The response of ActionsApi->clustering_result:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->clustering_result: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **result_id** | **str**| Result ID | 
 **offset** | **int**|  | [optional] 
 **limit** | **int**|  | [optional] 

### Return type

[**ClusteringResult**](ClusteringResult.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **column_statistics**
> ColumnStatisticsResponse column_statistics(data_source_id, column_statistics_request)

(EXPERIMENTAL) Compute column statistics

(EXPERIMENTAL) Computes the requested statistical parameters of a column in a data source.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.column_statistics_request import ColumnStatisticsRequest
from gooddata_api_client.models.column_statistics_response import ColumnStatisticsResponse
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    data_source_id = 'data_source_id_example' # str | 
    column_statistics_request = gooddata_api_client.ColumnStatisticsRequest() # ColumnStatisticsRequest | 

    try:
        # (EXPERIMENTAL) Compute column statistics
        api_response = api_instance.column_statistics(data_source_id, column_statistics_request)
        print("The response of ActionsApi->column_statistics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->column_statistics: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  | 
 **column_statistics_request** | [**ColumnStatisticsRequest**](ColumnStatisticsRequest.md)|  | 

### Return type

[**ColumnStatisticsResponse**](ColumnStatisticsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **compute_label_elements_post**
> ElementsResponse compute_label_elements_post(workspace_id, elements_request, offset=offset, limit=limit, skip_cache=skip_cache)

Listing of label values. The resulting data are limited by the static platform limit to the maximum of 10000 rows.

Returns paged list of elements (values) of given label satisfying given filtering criteria.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.elements_request import ElementsRequest
from gooddata_api_client.models.elements_response import ElementsResponse
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    elements_request = gooddata_api_client.ElementsRequest() # ElementsRequest | 
    offset = 0 # int | Request page with this offset. Must be positive integer. The API is limited to the maximum of 10000 items. Therefore this parameter is limited to this number as well. (optional) (default to 0)
    limit = 1000 # int | Return only this number of items. Must be positive integer. The API is limited to the maximum of 10000 items. Therefore this parameter is limited to this number as well. (optional) (default to 1000)
    skip_cache = False # bool | Ignore all caches during execution of current request. (optional) (default to False)

    try:
        # Listing of label values. The resulting data are limited by the static platform limit to the maximum of 10000 rows.
        api_response = api_instance.compute_label_elements_post(workspace_id, elements_request, offset=offset, limit=limit, skip_cache=skip_cache)
        print("The response of ActionsApi->compute_label_elements_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->compute_label_elements_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **elements_request** | [**ElementsRequest**](ElementsRequest.md)|  | 
 **offset** | **int**| Request page with this offset. Must be positive integer. The API is limited to the maximum of 10000 items. Therefore this parameter is limited to this number as well. | [optional] [default to 0]
 **limit** | **int**| Return only this number of items. Must be positive integer. The API is limited to the maximum of 10000 items. Therefore this parameter is limited to this number as well. | [optional] [default to 1000]
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional] [default to False]

### Return type

[**ElementsResponse**](ElementsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of label values. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **compute_report**
> AfmExecutionResponse compute_report(workspace_id, afm_execution, skip_cache=skip_cache, timestamp=timestamp)

Executes analytical request and returns link to the result

AFM is a combination of attributes, measures and filters that describe a query you want to execute.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.afm_execution import AfmExecution
from gooddata_api_client.models.afm_execution_response import AfmExecutionResponse
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    afm_execution = gooddata_api_client.AfmExecution() # AfmExecution | 
    skip_cache = False # bool | Ignore all caches during execution of current request. (optional) (default to False)
    timestamp = '2020-06-03T10:15:30+01:00' # str |  (optional)

    try:
        # Executes analytical request and returns link to the result
        api_response = api_instance.compute_report(workspace_id, afm_execution, skip_cache=skip_cache, timestamp=timestamp)
        print("The response of ActionsApi->compute_report:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->compute_report: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **afm_execution** | [**AfmExecution**](AfmExecution.md)|  | 
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional] [default to False]
 **timestamp** | **str**|  | [optional] 

### Return type

[**AfmExecutionResponse**](AfmExecutionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | AFM Execution response with links to the result and server-enhanced dimensions from the original request. |  * X-GDC-CANCEL-TOKEN - A token that can be used to cancel this execution <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **compute_valid_descendants**
> AfmValidDescendantsResponse compute_valid_descendants(workspace_id, afm_valid_descendants_query)

(BETA) Valid descendants

(BETA) Returns map of lists of attributes that can be used as descendants of the given attributes.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.afm_valid_descendants_query import AfmValidDescendantsQuery
from gooddata_api_client.models.afm_valid_descendants_response import AfmValidDescendantsResponse
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    afm_valid_descendants_query = gooddata_api_client.AfmValidDescendantsQuery() # AfmValidDescendantsQuery | 

    try:
        # (BETA) Valid descendants
        api_response = api_instance.compute_valid_descendants(workspace_id, afm_valid_descendants_query)
        print("The response of ActionsApi->compute_valid_descendants:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->compute_valid_descendants: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **afm_valid_descendants_query** | [**AfmValidDescendantsQuery**](AfmValidDescendantsQuery.md)|  | 

### Return type

[**AfmValidDescendantsResponse**](AfmValidDescendantsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Map of lists of attributes valid as descendants of the given attributes. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **compute_valid_objects**
> AfmValidObjectsResponse compute_valid_objects(workspace_id, afm_valid_objects_query)

Valid objects

Returns list containing attributes, facts, or metrics, which can be added to given AFM while still keeping it computable.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.afm_valid_objects_query import AfmValidObjectsQuery
from gooddata_api_client.models.afm_valid_objects_response import AfmValidObjectsResponse
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    afm_valid_objects_query = gooddata_api_client.AfmValidObjectsQuery() # AfmValidObjectsQuery | 

    try:
        # Valid objects
        api_response = api_instance.compute_valid_objects(workspace_id, afm_valid_objects_query)
        print("The response of ActionsApi->compute_valid_objects:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->compute_valid_objects: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **afm_valid_objects_query** | [**AfmValidObjectsQuery**](AfmValidObjectsQuery.md)|  | 

### Return type

[**AfmValidObjectsResponse**](AfmValidObjectsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of attributes, facts and metrics valid with respect to given AFM. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_dashboard_export_request**
> ExportResponse create_dashboard_export_request(workspace_id, dashboard_id, dashboard_tabular_export_request)

(EXPERIMENTAL) Create dashboard tabular export request

Note: This API is an experimental and is going to change. Please, use it accordingly.An tabular export job will be created based on the export request and put to queue to be executed. The result of the operation will be an exportResult identifier that will be assembled by the client into a url that can be polled.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.dashboard_tabular_export_request import DashboardTabularExportRequest
from gooddata_api_client.models.export_response import ExportResponse
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    dashboard_id = 'dashboard_id_example' # str | 
    dashboard_tabular_export_request = gooddata_api_client.DashboardTabularExportRequest() # DashboardTabularExportRequest | 

    try:
        # (EXPERIMENTAL) Create dashboard tabular export request
        api_response = api_instance.create_dashboard_export_request(workspace_id, dashboard_id, dashboard_tabular_export_request)
        print("The response of ActionsApi->create_dashboard_export_request:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->create_dashboard_export_request: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **dashboard_id** | **str**|  | 
 **dashboard_tabular_export_request** | [**DashboardTabularExportRequest**](DashboardTabularExportRequest.md)|  | 

### Return type

[**ExportResponse**](ExportResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Tabular export request created successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_image_export**
> ExportResponse create_image_export(workspace_id, image_export_request)

(EXPERIMENTAL) Create image export request

Note: This API is an experimental and is going to change. Please, use it accordingly. An image export job will be created based on the export request and put to queue to be executed. The result of the operation will be an exportResult identifier that will be assembled by the client into a url that can be polled.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.export_response import ExportResponse
from gooddata_api_client.models.image_export_request import ImageExportRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    image_export_request = gooddata_api_client.ImageExportRequest() # ImageExportRequest | 

    try:
        # (EXPERIMENTAL) Create image export request
        api_response = api_instance.create_image_export(workspace_id, image_export_request)
        print("The response of ActionsApi->create_image_export:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->create_image_export: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **image_export_request** | [**ImageExportRequest**](ImageExportRequest.md)|  | 

### Return type

[**ExportResponse**](ExportResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Image export request created successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_memory_item**
> MemoryItem create_memory_item(workspace_id, memory_item)

(EXPERIMENTAL) Create new memory item

(EXPERIMENTAL) Creates a new memory item and returns it

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.memory_item import MemoryItem
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    memory_item = gooddata_api_client.MemoryItem() # MemoryItem | 

    try:
        # (EXPERIMENTAL) Create new memory item
        api_response = api_instance.create_memory_item(workspace_id, memory_item)
        print("The response of ActionsApi->create_memory_item:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->create_memory_item: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **memory_item** | [**MemoryItem**](MemoryItem.md)|  | 

### Return type

[**MemoryItem**](MemoryItem.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_pdf_export**
> ExportResponse create_pdf_export(workspace_id, visual_export_request, x_gdc_debug=x_gdc_debug)

Create visual - pdf export request

An visual export job will be created based on the export request and put to queue to be executed. The result of the operation will be an exportResult identifier that will be assembled by the client into a url that can be polled.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.export_response import ExportResponse
from gooddata_api_client.models.visual_export_request import VisualExportRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    visual_export_request = gooddata_api_client.VisualExportRequest() # VisualExportRequest | 
    x_gdc_debug = False # bool |  (optional) (default to False)

    try:
        # Create visual - pdf export request
        api_response = api_instance.create_pdf_export(workspace_id, visual_export_request, x_gdc_debug=x_gdc_debug)
        print("The response of ActionsApi->create_pdf_export:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->create_pdf_export: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **visual_export_request** | [**VisualExportRequest**](VisualExportRequest.md)|  | 
 **x_gdc_debug** | **bool**|  | [optional] [default to False]

### Return type

[**ExportResponse**](ExportResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Visual export request created successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_raw_export**
> ExportResponse create_raw_export(workspace_id, raw_export_request)

(EXPERIMENTAL) Create raw export request

Note: This API is an experimental and is going to change. Please, use it accordingly.An raw export job will be created based on the export request and put to queue to be executed. The result of the operation will be an exportResult identifier that will be assembled by the client into a url that can be polled.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.export_response import ExportResponse
from gooddata_api_client.models.raw_export_request import RawExportRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    raw_export_request = gooddata_api_client.RawExportRequest() # RawExportRequest | 

    try:
        # (EXPERIMENTAL) Create raw export request
        api_response = api_instance.create_raw_export(workspace_id, raw_export_request)
        print("The response of ActionsApi->create_raw_export:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->create_raw_export: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **raw_export_request** | [**RawExportRequest**](RawExportRequest.md)|  | 

### Return type

[**ExportResponse**](ExportResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Raw export request created successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_slides_export**
> ExportResponse create_slides_export(workspace_id, slides_export_request, x_gdc_debug=x_gdc_debug)

(EXPERIMENTAL) Create slides export request

Note: This API is an experimental and is going to change. Please, use it accordingly. A slides export job will be created based on the export request and put to queue to be executed. The result of the operation will be an exportResult identifier that will be assembled by the client into a url that can be polled.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.export_response import ExportResponse
from gooddata_api_client.models.slides_export_request import SlidesExportRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    slides_export_request = gooddata_api_client.SlidesExportRequest() # SlidesExportRequest | 
    x_gdc_debug = False # bool |  (optional) (default to False)

    try:
        # (EXPERIMENTAL) Create slides export request
        api_response = api_instance.create_slides_export(workspace_id, slides_export_request, x_gdc_debug=x_gdc_debug)
        print("The response of ActionsApi->create_slides_export:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->create_slides_export: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **slides_export_request** | [**SlidesExportRequest**](SlidesExportRequest.md)|  | 
 **x_gdc_debug** | **bool**|  | [optional] [default to False]

### Return type

[**ExportResponse**](ExportResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Slides export request created successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_tabular_export**
> ExportResponse create_tabular_export(workspace_id, tabular_export_request)

Create tabular export request

An tabular export job will be created based on the export request and put to queue to be executed. The result of the operation will be an exportResult identifier that will be assembled by the client into a url that can be polled.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.export_response import ExportResponse
from gooddata_api_client.models.tabular_export_request import TabularExportRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    tabular_export_request = gooddata_api_client.TabularExportRequest() # TabularExportRequest | 

    try:
        # Create tabular export request
        api_response = api_instance.create_tabular_export(workspace_id, tabular_export_request)
        print("The response of ActionsApi->create_tabular_export:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->create_tabular_export: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **tabular_export_request** | [**TabularExportRequest**](TabularExportRequest.md)|  | 

### Return type

[**ExportResponse**](ExportResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Tabular export request created successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dashboard_permissions**
> DashboardPermissions dashboard_permissions(workspace_id, dashboard_id)

Get Dashboard Permissions

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.dashboard_permissions import DashboardPermissions
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    dashboard_id = 'dashboard_id_example' # str | 

    try:
        # Get Dashboard Permissions
        api_response = api_instance.dashboard_permissions(workspace_id, dashboard_id)
        print("The response of ActionsApi->dashboard_permissions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->dashboard_permissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **dashboard_id** | **str**|  | 

### Return type

[**DashboardPermissions**](DashboardPermissions.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_organization_automations**
> delete_organization_automations(organization_automation_management_bulk_request)

Delete selected automations across all workspaces

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.organization_automation_management_bulk_request import OrganizationAutomationManagementBulkRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    organization_automation_management_bulk_request = gooddata_api_client.OrganizationAutomationManagementBulkRequest() # OrganizationAutomationManagementBulkRequest | 

    try:
        # Delete selected automations across all workspaces
        api_instance.delete_organization_automations(organization_automation_management_bulk_request)
    except Exception as e:
        print("Exception when calling ActionsApi->delete_organization_automations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_automation_management_bulk_request** | [**OrganizationAutomationManagementBulkRequest**](OrganizationAutomationManagementBulkRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_workspace_automations**
> delete_workspace_automations(workspace_id, workspace_automation_management_bulk_request)

Delete selected automations in the workspace

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.workspace_automation_management_bulk_request import WorkspaceAutomationManagementBulkRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    workspace_automation_management_bulk_request = gooddata_api_client.WorkspaceAutomationManagementBulkRequest() # WorkspaceAutomationManagementBulkRequest | 

    try:
        # Delete selected automations in the workspace
        api_instance.delete_workspace_automations(workspace_id, workspace_automation_management_bulk_request)
    except Exception as e:
        print("Exception when calling ActionsApi->delete_workspace_automations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **workspace_automation_management_bulk_request** | [**WorkspaceAutomationManagementBulkRequest**](WorkspaceAutomationManagementBulkRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **explain_afm**
> explain_afm(workspace_id, afm_execution, explain_type=explain_type)

AFM explain resource.

The resource provides static structures needed for investigation of a problem with given AFM.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.afm_execution import AfmExecution
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    afm_execution = gooddata_api_client.AfmExecution() # AfmExecution | 
    explain_type = 'explain_type_example' # str | Requested explain type. If not specified all types are bundled in a ZIP archive.  `MAQL` - MAQL Abstract Syntax Tree, execution dimensions and related info  `GRPC_MODEL` - Datasets used in execution  `GRPC_MODEL_SVG` - Generated SVG image of the datasets  `COMPRESSED_GRPC_MODEL_SVG` - Generated SVG image of the model fragment used in the query  `WDF` - Workspace data filters in execution workspace context  `QT` - Query Tree, created from MAQL AST using Logical Data Model,  contains all information needed to generate SQL  `QT_SVG` - Generated SVG image of the Query Tree  `OPT_QT` - Optimized Query Tree  `OPT_QT_SVG` - Generated SVG image of the Optimized Query Tree  `SQL` - Final SQL to be executed  `COMPRESSED_SQL` - Final SQL to be executed with rolled SQL datasets  `SETTINGS` - Settings used to execute explain request (optional)

    try:
        # AFM explain resource.
        api_instance.explain_afm(workspace_id, afm_execution, explain_type=explain_type)
    except Exception as e:
        print("Exception when calling ActionsApi->explain_afm: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **afm_execution** | [**AfmExecution**](AfmExecution.md)|  | 
 **explain_type** | **str**| Requested explain type. If not specified all types are bundled in a ZIP archive.  &#x60;MAQL&#x60; - MAQL Abstract Syntax Tree, execution dimensions and related info  &#x60;GRPC_MODEL&#x60; - Datasets used in execution  &#x60;GRPC_MODEL_SVG&#x60; - Generated SVG image of the datasets  &#x60;COMPRESSED_GRPC_MODEL_SVG&#x60; - Generated SVG image of the model fragment used in the query  &#x60;WDF&#x60; - Workspace data filters in execution workspace context  &#x60;QT&#x60; - Query Tree, created from MAQL AST using Logical Data Model,  contains all information needed to generate SQL  &#x60;QT_SVG&#x60; - Generated SVG image of the Query Tree  &#x60;OPT_QT&#x60; - Optimized Query Tree  &#x60;OPT_QT_SVG&#x60; - Generated SVG image of the Optimized Query Tree  &#x60;SQL&#x60; - Final SQL to be executed  &#x60;COMPRESSED_SQL&#x60; - Final SQL to be executed with rolled SQL datasets  &#x60;SETTINGS&#x60; - Settings used to execute explain request | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/sql, application/zip, image/svg+xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Requested resource |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **forecast**
> SmartFunctionResponse forecast(workspace_id, result_id, forecast_request, skip_cache=skip_cache)

(BETA) Smart functions - Forecast

(BETA) Computes forecasted data points from the provided execution result and parameters.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.forecast_request import ForecastRequest
from gooddata_api_client.models.smart_function_response import SmartFunctionResponse
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    result_id = '9bd52018570364264fcf62d373da6bed313120e8' # str | Input result ID to be used in the computation
    forecast_request = gooddata_api_client.ForecastRequest() # ForecastRequest | 
    skip_cache = False # bool | Ignore all caches during execution of current request. (optional) (default to False)

    try:
        # (BETA) Smart functions - Forecast
        api_response = api_instance.forecast(workspace_id, result_id, forecast_request, skip_cache=skip_cache)
        print("The response of ActionsApi->forecast:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->forecast: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **result_id** | **str**| Input result ID to be used in the computation | 
 **forecast_request** | [**ForecastRequest**](ForecastRequest.md)|  | 
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional] [default to False]

### Return type

[**SmartFunctionResponse**](SmartFunctionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **forecast_result**
> ForecastResult forecast_result(workspace_id, result_id, offset=offset, limit=limit)

(BETA) Smart functions - Forecast Result

(BETA) Gets forecast result.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.forecast_result import ForecastResult
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    result_id = 'a9b28f9dc55f37ea9f4a5fb0c76895923591e781' # str | Result ID
    offset = 56 # int |  (optional)
    limit = 56 # int |  (optional)

    try:
        # (BETA) Smart functions - Forecast Result
        api_response = api_instance.forecast_result(workspace_id, result_id, offset=offset, limit=limit)
        print("The response of ActionsApi->forecast_result:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->forecast_result: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **result_id** | **str**| Result ID | 
 **offset** | **int**|  | [optional] 
 **limit** | **int**|  | [optional] 

### Return type

[**ForecastResult**](ForecastResult.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **generate_logical_model**
> DeclarativeModel generate_logical_model(data_source_id, generate_ldm_request)

Generate logical data model (LDM) from physical data model (PDM)

Generate logical data model (LDM) from physical data model (PDM) stored in data source.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_model import DeclarativeModel
from gooddata_api_client.models.generate_ldm_request import GenerateLdmRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    data_source_id = 'data_source_id_example' # str | 
    generate_ldm_request = gooddata_api_client.GenerateLdmRequest() # GenerateLdmRequest | 

    try:
        # Generate logical data model (LDM) from physical data model (PDM)
        api_response = api_instance.generate_logical_model(data_source_id, generate_ldm_request)
        print("The response of ActionsApi->generate_logical_model:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->generate_logical_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  | 
 **generate_ldm_request** | [**GenerateLdmRequest**](GenerateLdmRequest.md)|  | 

### Return type

[**DeclarativeModel**](DeclarativeModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | LDM generated successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_data_source_schemata**
> DataSourceSchemata get_data_source_schemata(data_source_id)

Get a list of schema names of a database

It scans a database and reads metadata. The result of the request contains a list of schema names of a database.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.data_source_schemata import DataSourceSchemata
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    data_source_id = 'myPostgres' # str | Data source id

    try:
        # Get a list of schema names of a database
        api_response = api_instance.get_data_source_schemata(data_source_id)
        print("The response of ActionsApi->get_data_source_schemata:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->get_data_source_schemata: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| Data source id | 

### Return type

[**DataSourceSchemata**](DataSourceSchemata.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The result of the scan schemata |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_dependent_entities_graph**
> DependentEntitiesResponse get_dependent_entities_graph(workspace_id)

Computes the dependent entities graph

Computes the dependent entities graph

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.dependent_entities_response import DependentEntitiesResponse
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 

    try:
        # Computes the dependent entities graph
        api_response = api_instance.get_dependent_entities_graph(workspace_id)
        print("The response of ActionsApi->get_dependent_entities_graph:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->get_dependent_entities_graph: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 

### Return type

[**DependentEntitiesResponse**](DependentEntitiesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Computes the dependent entities graph |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_dependent_entities_graph_from_entry_points**
> DependentEntitiesResponse get_dependent_entities_graph_from_entry_points(workspace_id, dependent_entities_request)

Computes the dependent entities graph from given entry points

Computes the dependent entities graph from given entry points

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.dependent_entities_request import DependentEntitiesRequest
from gooddata_api_client.models.dependent_entities_response import DependentEntitiesResponse
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    dependent_entities_request = gooddata_api_client.DependentEntitiesRequest() # DependentEntitiesRequest | 

    try:
        # Computes the dependent entities graph from given entry points
        api_response = api_instance.get_dependent_entities_graph_from_entry_points(workspace_id, dependent_entities_request)
        print("The response of ActionsApi->get_dependent_entities_graph_from_entry_points:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->get_dependent_entities_graph_from_entry_points: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **dependent_entities_request** | [**DependentEntitiesRequest**](DependentEntitiesRequest.md)|  | 

### Return type

[**DependentEntitiesResponse**](DependentEntitiesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Computes the dependent entities graph from given entry points |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_exported_file**
> bytearray get_exported_file(workspace_id, export_id)

Retrieve exported files

Returns 202 until original POST export request is not processed.Returns 200 with exported data once the export is done.

### Example


```python
import gooddata_api_client
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    export_id = 'export_id_example' # str | 

    try:
        # Retrieve exported files
        api_response = api_instance.get_exported_file(workspace_id, export_id)
        print("The response of ActionsApi->get_exported_file:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->get_exported_file: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **export_id** | **str**|  | 

### Return type

**bytearray**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/pdf

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Binary export result. |  * Content-Disposition -  <br>  |
**202** | Request is accepted, provided exportId exists, but export is not yet ready. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_image_export**
> bytearray get_image_export(workspace_id, export_id)

(EXPERIMENTAL) Retrieve exported files

Note: This API is an experimental and is going to change. Please, use it accordingly. After clients creates a POST export request, the processing of it will start shortly asynchronously. To retrieve the result, client has to check periodically for the result on this endpoint. In case the result isn't ready yet, the service returns 202. If the result is ready, it returns 200 and octet stream of the result file with provided filename.

### Example


```python
import gooddata_api_client
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    export_id = 'export_id_example' # str | 

    try:
        # (EXPERIMENTAL) Retrieve exported files
        api_response = api_instance.get_image_export(workspace_id, export_id)
        print("The response of ActionsApi->get_image_export:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->get_image_export: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **export_id** | **str**|  | 

### Return type

**bytearray**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: image/png

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Binary export result. |  * Content-Disposition -  <br>  |
**202** | Request is accepted, provided exportId exists, but export is not yet ready. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_image_export_metadata**
> get_image_export_metadata(workspace_id, export_id)

(EXPERIMENTAL) Retrieve metadata context

Note: This API is an experimental and is going to change. Please, use it accordingly. This endpoint serves as a cache for user-defined metadata of the export for the front end UI to retrieve it, if one was created using the POST ../export/image endpoint. The metadata structure is not verified.

### Example


```python
import gooddata_api_client
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    export_id = 'export_id_example' # str | 

    try:
        # (EXPERIMENTAL) Retrieve metadata context
        api_instance.get_image_export_metadata(workspace_id, export_id)
    except Exception as e:
        print("Exception when calling ActionsApi->get_image_export_metadata: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **export_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Json metadata representation |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_memory_item**
> MemoryItem get_memory_item(workspace_id, memory_id)

(EXPERIMENTAL) Get memory item

(EXPERIMENTAL) Get memory item by id

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.memory_item import MemoryItem
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    memory_id = 'memory_id_example' # str | 

    try:
        # (EXPERIMENTAL) Get memory item
        api_response = api_instance.get_memory_item(workspace_id, memory_id)
        print("The response of ActionsApi->get_memory_item:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->get_memory_item: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **memory_id** | **str**|  | 

### Return type

[**MemoryItem**](MemoryItem.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_metadata**
> get_metadata(workspace_id, export_id)

Retrieve metadata context

This endpoint serves as a cache for user-defined metadata of the export for the front end UI to retrieve it, if one was created using the POST ../export/visual endpoint. The metadata structure is not verified.

### Example


```python
import gooddata_api_client
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    export_id = 'export_id_example' # str | 

    try:
        # Retrieve metadata context
        api_instance.get_metadata(workspace_id, export_id)
    except Exception as e:
        print("Exception when calling ActionsApi->get_metadata: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **export_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Json metadata representation |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_notifications**
> Notifications get_notifications(workspace_id=workspace_id, is_read=is_read, page=page, size=size, meta_include=meta_include)

Get latest notifications.

Get latest in-platform notifications for the current user.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.notifications import Notifications
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace ID to filter notifications by. (optional)
    is_read = True # bool | Filter notifications by read status. (optional)
    page = '0' # str | Zero-based page index (0..N) (optional) (default to '0')
    size = '20' # str | The size of the page to be returned. (optional) (default to '20')
    meta_include = ['meta_include_example'] # List[str] | Additional meta information to include in the response. (optional)

    try:
        # Get latest notifications.
        api_response = api_instance.get_notifications(workspace_id=workspace_id, is_read=is_read, page=page, size=size, meta_include=meta_include)
        print("The response of ActionsApi->get_notifications:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->get_notifications: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace ID to filter notifications by. | [optional] 
 **is_read** | **bool**| Filter notifications by read status. | [optional] 
 **page** | **str**| Zero-based page index (0..N) | [optional] [default to &#39;0&#39;]
 **size** | **str**| The size of the page to be returned. | [optional] [default to &#39;20&#39;]
 **meta_include** | [**List[str]**](str.md)| Additional meta information to include in the response. | [optional] 

### Return type

[**Notifications**](Notifications.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_quality_issues**
> GetQualityIssuesResponse get_quality_issues(workspace_id)

Get Quality Issues

Returns metadata quality issues detected by the platform linter.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.get_quality_issues_response import GetQualityIssuesResponse
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier

    try:
        # Get Quality Issues
        api_response = api_instance.get_quality_issues(workspace_id)
        print("The response of ActionsApi->get_quality_issues:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->get_quality_issues: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 

### Return type

[**GetQualityIssuesResponse**](GetQualityIssuesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_raw_export**
> bytearray get_raw_export(workspace_id, export_id)

(EXPERIMENTAL) Retrieve exported files

Note: This API is an experimental and is going to change. Please, use it accordingly.After clients creates a POST export request, the processing of it will start shortly asynchronously. To retrieve the result, client has to check periodically for the result on this endpoint. In case the result isn't ready yet, the service returns 202. If the result is ready, it returns 200 and octet stream of the result file with provided filename.

### Example


```python
import gooddata_api_client
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    export_id = 'export_id_example' # str | 

    try:
        # (EXPERIMENTAL) Retrieve exported files
        api_response = api_instance.get_raw_export(workspace_id, export_id)
        print("The response of ActionsApi->get_raw_export:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->get_raw_export: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **export_id** | **str**|  | 

### Return type

**bytearray**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.apache.arrow.file, application/vnd.apache.arrow.stream, text/csv

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Binary export result. |  * Content-Disposition -  <br>  |
**202** | Request is accepted, provided exportId exists, but export is not yet ready. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_slides_export**
> bytearray get_slides_export(workspace_id, export_id)

(EXPERIMENTAL) Retrieve exported files

Note: This API is an experimental and is going to change. Please, use it accordingly. After clients creates a POST export request, the processing of it will start shortly asynchronously. To retrieve the result, client has to check periodically for the result on this endpoint. In case the result isn't ready yet, the service returns 202. If the result is ready, it returns 200 and octet stream of the result file with provided filename.

### Example


```python
import gooddata_api_client
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    export_id = 'export_id_example' # str | 

    try:
        # (EXPERIMENTAL) Retrieve exported files
        api_response = api_instance.get_slides_export(workspace_id, export_id)
        print("The response of ActionsApi->get_slides_export:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->get_slides_export: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **export_id** | **str**|  | 

### Return type

**bytearray**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/pdf, application/vnd.openxmlformats-officedocument.presentationml.presentation

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Binary export result. |  * Content-Disposition -  <br>  |
**202** | Request is accepted, provided exportId exists, but export is not yet ready. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_slides_export_metadata**
> get_slides_export_metadata(workspace_id, export_id)

(EXPERIMENTAL) Retrieve metadata context

Note: This API is an experimental and is going to change. Please, use it accordingly. This endpoint serves as a cache for user-defined metadata of the export for the front end UI to retrieve it, if one was created using the POST ../export/slides endpoint. The metadata structure is not verified.

### Example


```python
import gooddata_api_client
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    export_id = 'export_id_example' # str | 

    try:
        # (EXPERIMENTAL) Retrieve metadata context
        api_instance.get_slides_export_metadata(workspace_id, export_id)
    except Exception as e:
        print("Exception when calling ActionsApi->get_slides_export_metadata: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **export_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Json metadata representation |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_tabular_export**
> bytearray get_tabular_export(workspace_id, export_id)

Retrieve exported files

After clients creates a POST export request, the processing of it will start shortly asynchronously. To retrieve the result, client has to check periodically for the result on this endpoint. In case the result isn't ready yet, the service returns 202. If the result is ready, it returns 200 and octet stream of the result file with provided filename.

### Example


```python
import gooddata_api_client
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    export_id = 'export_id_example' # str | 

    try:
        # Retrieve exported files
        api_response = api_instance.get_tabular_export(workspace_id, export_id)
        print("The response of ActionsApi->get_tabular_export:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->get_tabular_export: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **export_id** | **str**|  | 

### Return type

**bytearray**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/pdf, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, text/csv, text/html

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Binary export result. |  * Content-Disposition -  <br>  |
**202** | Request is accepted, provided exportId exists, but export is not yet ready. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_translation_tags**
> List[str] get_translation_tags(workspace_id)

Get translation tags.

Provides a list of effective translation tags.

### Example


```python
import gooddata_api_client
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 

    try:
        # Get translation tags.
        api_response = api_instance.get_translation_tags(workspace_id)
        print("The response of ActionsApi->get_translation_tags:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->get_translation_tags: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 

### Return type

**List[str]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved list of translation tags. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **inherited_entity_conflicts**
> List[IdentifierDuplications] inherited_entity_conflicts(workspace_id)

Finds identifier conflicts in workspace hierarchy.

Finds API identifier conflicts in given workspace hierarchy.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.identifier_duplications import IdentifierDuplications
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 

    try:
        # Finds identifier conflicts in workspace hierarchy.
        api_response = api_instance.inherited_entity_conflicts(workspace_id)
        print("The response of ActionsApi->inherited_entity_conflicts:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->inherited_entity_conflicts: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 

### Return type

[**List[IdentifierDuplications]**](IdentifierDuplications.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Searching for conflicting identifiers finished successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **inherited_entity_prefixes**
> List[str] inherited_entity_prefixes(workspace_id)

Get used entity prefixes in hierarchy

Get used entity prefixes in hierarchy of parent workspaces

### Example


```python
import gooddata_api_client
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 

    try:
        # Get used entity prefixes in hierarchy
        api_response = api_instance.inherited_entity_prefixes(workspace_id)
        print("The response of ActionsApi->inherited_entity_prefixes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->inherited_entity_prefixes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 

### Return type

**List[str]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Prefixes used in parent entities |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **key_driver_analysis**
> KeyDriversResponse key_driver_analysis(workspace_id, key_drivers_request, skip_cache=skip_cache)

(EXPERIMENTAL) Compute key driver analysis

(EXPERIMENTAL) Computes key driver analysis for the provided execution definition.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.key_drivers_request import KeyDriversRequest
from gooddata_api_client.models.key_drivers_response import KeyDriversResponse
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    key_drivers_request = gooddata_api_client.KeyDriversRequest() # KeyDriversRequest | 
    skip_cache = False # bool | Ignore all caches during execution of current request. (optional) (default to False)

    try:
        # (EXPERIMENTAL) Compute key driver analysis
        api_response = api_instance.key_driver_analysis(workspace_id, key_drivers_request, skip_cache=skip_cache)
        print("The response of ActionsApi->key_driver_analysis:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->key_driver_analysis: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **key_drivers_request** | [**KeyDriversRequest**](KeyDriversRequest.md)|  | 
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional] [default to False]

### Return type

[**KeyDriversResponse**](KeyDriversResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **key_driver_analysis_result**
> KeyDriversResult key_driver_analysis_result(workspace_id, result_id, offset=offset, limit=limit)

(EXPERIMENTAL) Get key driver analysis result

(EXPERIMENTAL) Gets key driver analysis.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.key_drivers_result import KeyDriversResult
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    result_id = 'a9b28f9dc55f37ea9f4a5fb0c76895923591e781' # str | Result ID
    offset = 56 # int |  (optional)
    limit = 56 # int |  (optional)

    try:
        # (EXPERIMENTAL) Get key driver analysis result
        api_response = api_instance.key_driver_analysis_result(workspace_id, result_id, offset=offset, limit=limit)
        print("The response of ActionsApi->key_driver_analysis_result:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->key_driver_analysis_result: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **result_id** | **str**| Result ID | 
 **offset** | **int**|  | [optional] 
 **limit** | **int**|  | [optional] 

### Return type

[**KeyDriversResult**](KeyDriversResult.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_memory_items**
> List[MemoryItem] list_memory_items(workspace_id)

(EXPERIMENTAL) List all memory items

(EXPERIMENTAL) Returns a list of memory items

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.memory_item import MemoryItem
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier

    try:
        # (EXPERIMENTAL) List all memory items
        api_response = api_instance.list_memory_items(workspace_id)
        print("The response of ActionsApi->list_memory_items:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->list_memory_items: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 

### Return type

[**List[MemoryItem]**](MemoryItem.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_workspace_user_groups**
> WorkspaceUserGroups list_workspace_user_groups(workspace_id, page=page, size=size, name=name)



### Example


```python
import gooddata_api_client
from gooddata_api_client.models.workspace_user_groups import WorkspaceUserGroups
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned. (optional) (default to 20)
    name = 'name=charles' # str | Filter by user name. Note that user name is case insensitive. (optional)

    try:
        api_response = api_instance.list_workspace_user_groups(workspace_id, page=page, size=size, name=name)
        print("The response of ActionsApi->list_workspace_user_groups:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->list_workspace_user_groups: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **page** | **int**| Zero-based page index (0..N) | [optional] [default to 0]
 **size** | **int**| The size of the page to be returned. | [optional] [default to 20]
 **name** | **str**| Filter by user name. Note that user name is case insensitive. | [optional] 

### Return type

[**WorkspaceUserGroups**](WorkspaceUserGroups.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_workspace_users**
> WorkspaceUsers list_workspace_users(workspace_id, page=page, size=size, name=name)



### Example


```python
import gooddata_api_client
from gooddata_api_client.models.workspace_users import WorkspaceUsers
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned. (optional) (default to 20)
    name = 'name=charles' # str | Filter by user name. Note that user name is case insensitive. (optional)

    try:
        api_response = api_instance.list_workspace_users(workspace_id, page=page, size=size, name=name)
        print("The response of ActionsApi->list_workspace_users:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->list_workspace_users: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **page** | **int**| Zero-based page index (0..N) | [optional] [default to 0]
 **size** | **int**| The size of the page to be returned. | [optional] [default to 20]
 **name** | **str**| Filter by user name. Note that user name is case insensitive. | [optional] 

### Return type

[**WorkspaceUsers**](WorkspaceUsers.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **manage_dashboard_permissions**
> manage_dashboard_permissions(workspace_id, dashboard_id, manage_dashboard_permissions_request_inner)

Manage Permissions for a Dashboard

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.manage_dashboard_permissions_request_inner import ManageDashboardPermissionsRequestInner
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    dashboard_id = 'dashboard_id_example' # str | 
    manage_dashboard_permissions_request_inner = [gooddata_api_client.ManageDashboardPermissionsRequestInner()] # List[ManageDashboardPermissionsRequestInner] | 

    try:
        # Manage Permissions for a Dashboard
        api_instance.manage_dashboard_permissions(workspace_id, dashboard_id, manage_dashboard_permissions_request_inner)
    except Exception as e:
        print("Exception when calling ActionsApi->manage_dashboard_permissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **dashboard_id** | **str**|  | 
 **manage_dashboard_permissions_request_inner** | [**List[ManageDashboardPermissionsRequestInner]**](ManageDashboardPermissionsRequestInner.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **manage_data_source_permissions**
> manage_data_source_permissions(data_source_id, data_source_permission_assignment)

Manage Permissions for a Data Source

Manage Permissions for a Data Source

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.data_source_permission_assignment import DataSourcePermissionAssignment
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    data_source_id = 'data_source_id_example' # str | 
    data_source_permission_assignment = [gooddata_api_client.DataSourcePermissionAssignment()] # List[DataSourcePermissionAssignment] | 

    try:
        # Manage Permissions for a Data Source
        api_instance.manage_data_source_permissions(data_source_id, data_source_permission_assignment)
    except Exception as e:
        print("Exception when calling ActionsApi->manage_data_source_permissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  | 
 **data_source_permission_assignment** | [**List[DataSourcePermissionAssignment]**](DataSourcePermissionAssignment.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **manage_organization_permissions**
> manage_organization_permissions(organization_permission_assignment)

Manage Permissions for a Organization

Manage Permissions for a Organization

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.organization_permission_assignment import OrganizationPermissionAssignment
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    organization_permission_assignment = [gooddata_api_client.OrganizationPermissionAssignment()] # List[OrganizationPermissionAssignment] | 

    try:
        # Manage Permissions for a Organization
        api_instance.manage_organization_permissions(organization_permission_assignment)
    except Exception as e:
        print("Exception when calling ActionsApi->manage_organization_permissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_permission_assignment** | [**List[OrganizationPermissionAssignment]**](OrganizationPermissionAssignment.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **manage_workspace_permissions**
> manage_workspace_permissions(workspace_id, workspace_permission_assignment)

Manage Permissions for a Workspace

Manage Permissions for a Workspace and its Workspace Hierarchy

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.workspace_permission_assignment import WorkspacePermissionAssignment
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    workspace_permission_assignment = [gooddata_api_client.WorkspacePermissionAssignment()] # List[WorkspacePermissionAssignment] | 

    try:
        # Manage Permissions for a Workspace
        api_instance.manage_workspace_permissions(workspace_id, workspace_permission_assignment)
    except Exception as e:
        print("Exception when calling ActionsApi->manage_workspace_permissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **workspace_permission_assignment** | [**List[WorkspacePermissionAssignment]**](WorkspacePermissionAssignment.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **mark_as_read_notification**
> mark_as_read_notification(notification_id)

Mark notification as read.

Mark in-platform notification by its ID as read.

### Example


```python
import gooddata_api_client
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    notification_id = 'notification_id_example' # str | Notification ID to mark as read.

    try:
        # Mark notification as read.
        api_instance.mark_as_read_notification(notification_id)
    except Exception as e:
        print("Exception when calling ActionsApi->mark_as_read_notification: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **notification_id** | **str**| Notification ID to mark as read. | 

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
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **mark_as_read_notification_all**
> mark_as_read_notification_all(workspace_id=workspace_id)

Mark all notifications as read.

Mark all user in-platform notifications as read.

### Example


```python
import gooddata_api_client
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace ID where to mark notifications as read. (optional)

    try:
        # Mark all notifications as read.
        api_instance.mark_as_read_notification_all(workspace_id=workspace_id)
    except Exception as e:
        print("Exception when calling ActionsApi->mark_as_read_notification_all: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace ID where to mark notifications as read. | [optional] 

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
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **metadata_sync**
> metadata_sync(workspace_id)

(BETA) Sync Metadata to other services

(BETA) Temporary solution. Later relevant metadata actions will trigger it in its scope only.

### Example


```python
import gooddata_api_client
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 

    try:
        # (BETA) Sync Metadata to other services
        api_instance.metadata_sync(workspace_id)
    except Exception as e:
        print("Exception when calling ActionsApi->metadata_sync: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 

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
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **metadata_sync_organization**
> metadata_sync_organization()

(BETA) Sync organization scope Metadata to other services

(BETA) Temporary solution. Later relevant metadata actions will trigger sync in their scope only.

### Example


```python
import gooddata_api_client
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)

    try:
        # (BETA) Sync organization scope Metadata to other services
        api_instance.metadata_sync_organization()
    except Exception as e:
        print("Exception when calling ActionsApi->metadata_sync_organization: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

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
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **overridden_child_entities**
> List[IdentifierDuplications] overridden_child_entities(workspace_id)

Finds identifier overrides in workspace hierarchy.

Finds API identifier overrides in given workspace hierarchy.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.identifier_duplications import IdentifierDuplications
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 

    try:
        # Finds identifier overrides in workspace hierarchy.
        api_response = api_instance.overridden_child_entities(workspace_id)
        print("The response of ActionsApi->overridden_child_entities:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->overridden_child_entities: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 

### Return type

[**List[IdentifierDuplications]**](IdentifierDuplications.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Searching for overridden identifiers finished successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **particular_platform_usage**
> List[PlatformUsage] particular_platform_usage(platform_usage_request)

Info about the platform usage for particular items.

Provides information about platform usage, like amount of users, workspaces, ...  _NOTE_: The `admin` user is always excluded from this amount.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.platform_usage import PlatformUsage
from gooddata_api_client.models.platform_usage_request import PlatformUsageRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    platform_usage_request = gooddata_api_client.PlatformUsageRequest() # PlatformUsageRequest | 

    try:
        # Info about the platform usage for particular items.
        api_response = api_instance.particular_platform_usage(platform_usage_request)
        print("The response of ActionsApi->particular_platform_usage:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->particular_platform_usage: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **platform_usage_request** | [**PlatformUsageRequest**](PlatformUsageRequest.md)|  | 

### Return type

[**List[PlatformUsage]**](PlatformUsage.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pause_organization_automations**
> pause_organization_automations(organization_automation_management_bulk_request)

Pause selected automations across all workspaces

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.organization_automation_management_bulk_request import OrganizationAutomationManagementBulkRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    organization_automation_management_bulk_request = gooddata_api_client.OrganizationAutomationManagementBulkRequest() # OrganizationAutomationManagementBulkRequest | 

    try:
        # Pause selected automations across all workspaces
        api_instance.pause_organization_automations(organization_automation_management_bulk_request)
    except Exception as e:
        print("Exception when calling ActionsApi->pause_organization_automations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_automation_management_bulk_request** | [**OrganizationAutomationManagementBulkRequest**](OrganizationAutomationManagementBulkRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pause_workspace_automations**
> pause_workspace_automations(workspace_id, workspace_automation_management_bulk_request)

Pause selected automations in the workspace

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.workspace_automation_management_bulk_request import WorkspaceAutomationManagementBulkRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    workspace_automation_management_bulk_request = gooddata_api_client.WorkspaceAutomationManagementBulkRequest() # WorkspaceAutomationManagementBulkRequest | 

    try:
        # Pause selected automations in the workspace
        api_instance.pause_workspace_automations(workspace_id, workspace_automation_management_bulk_request)
    except Exception as e:
        print("Exception when calling ActionsApi->pause_workspace_automations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **workspace_automation_management_bulk_request** | [**WorkspaceAutomationManagementBulkRequest**](WorkspaceAutomationManagementBulkRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **register_upload_notification**
> register_upload_notification(data_source_id)

Register an upload notification

Notification sets up all reports to be computed again with new data.

### Example


```python
import gooddata_api_client
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    data_source_id = 'data_source_id_example' # str | 

    try:
        # Register an upload notification
        api_instance.register_upload_notification(data_source_id)
    except Exception as e:
        print("Exception when calling ActionsApi->register_upload_notification: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  | 

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
**204** | An upload notification has been successfully registered. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_memory_item**
> remove_memory_item(workspace_id, memory_id)

(EXPERIMENTAL) Remove memory item

(EXPERIMENTAL) Removes memory item

### Example


```python
import gooddata_api_client
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    memory_id = 'memory_id_example' # str | 

    try:
        # (EXPERIMENTAL) Remove memory item
        api_instance.remove_memory_item(workspace_id, memory_id)
    except Exception as e:
        print("Exception when calling ActionsApi->remove_memory_item: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **memory_id** | **str**|  | 

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
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resolve_all_entitlements**
> List[ApiEntitlement] resolve_all_entitlements()

Values for all public entitlements.

Resolves values of available entitlements for the organization.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.api_entitlement import ApiEntitlement
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)

    try:
        # Values for all public entitlements.
        api_response = api_instance.resolve_all_entitlements()
        print("The response of ActionsApi->resolve_all_entitlements:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->resolve_all_entitlements: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[ApiEntitlement]**](ApiEntitlement.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resolve_all_settings_without_workspace**
> List[ResolvedSetting] resolve_all_settings_without_workspace()

Values for all settings without workspace.

Resolves values for all settings without workspace by current user, organization, or default settings.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.resolved_setting import ResolvedSetting
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)

    try:
        # Values for all settings without workspace.
        api_response = api_instance.resolve_all_settings_without_workspace()
        print("The response of ActionsApi->resolve_all_settings_without_workspace:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->resolve_all_settings_without_workspace: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[ResolvedSetting]**](ResolvedSetting.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Values for selected settings. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resolve_llm_endpoints**
> ResolvedLlmEndpoints resolve_llm_endpoints(workspace_id)

Get Active LLM Endpoints for this workspace

Returns a list of available LLM Endpoints

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.resolved_llm_endpoints import ResolvedLlmEndpoints
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier

    try:
        # Get Active LLM Endpoints for this workspace
        api_response = api_instance.resolve_llm_endpoints(workspace_id)
        print("The response of ActionsApi->resolve_llm_endpoints:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->resolve_llm_endpoints: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 

### Return type

[**ResolvedLlmEndpoints**](ResolvedLlmEndpoints.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resolve_requested_entitlements**
> List[ApiEntitlement] resolve_requested_entitlements(entitlements_request)

Values for requested public entitlements.

Resolves values for requested entitlements in the organization.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.api_entitlement import ApiEntitlement
from gooddata_api_client.models.entitlements_request import EntitlementsRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    entitlements_request = gooddata_api_client.EntitlementsRequest() # EntitlementsRequest | 

    try:
        # Values for requested public entitlements.
        api_response = api_instance.resolve_requested_entitlements(entitlements_request)
        print("The response of ActionsApi->resolve_requested_entitlements:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->resolve_requested_entitlements: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entitlements_request** | [**EntitlementsRequest**](EntitlementsRequest.md)|  | 

### Return type

[**List[ApiEntitlement]**](ApiEntitlement.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resolve_settings_without_workspace**
> List[ResolvedSetting] resolve_settings_without_workspace(resolve_settings_request)

Values for selected settings without workspace.

Resolves values for selected settings without workspace by current user, organization, or default settings.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.resolve_settings_request import ResolveSettingsRequest
from gooddata_api_client.models.resolved_setting import ResolvedSetting
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    resolve_settings_request = gooddata_api_client.ResolveSettingsRequest() # ResolveSettingsRequest | 

    try:
        # Values for selected settings without workspace.
        api_response = api_instance.resolve_settings_without_workspace(resolve_settings_request)
        print("The response of ActionsApi->resolve_settings_without_workspace:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->resolve_settings_without_workspace: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resolve_settings_request** | [**ResolveSettingsRequest**](ResolveSettingsRequest.md)|  | 

### Return type

[**List[ResolvedSetting]**](ResolvedSetting.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Values for selected settings. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_execution_metadata**
> ResultCacheMetadata retrieve_execution_metadata(workspace_id, result_id)

Get a single execution result's metadata.

The resource provides execution result's metadata as AFM and resultSpec used in execution request and an executionResponse

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.result_cache_metadata import ResultCacheMetadata
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    result_id = 'a9b28f9dc55f37ea9f4a5fb0c76895923591e781' # str | Result ID

    try:
        # Get a single execution result's metadata.
        api_response = api_instance.retrieve_execution_metadata(workspace_id, result_id)
        print("The response of ActionsApi->retrieve_execution_metadata:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->retrieve_execution_metadata: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **result_id** | **str**| Result ID | 

### Return type

[**ResultCacheMetadata**](ResultCacheMetadata.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Execution result&#39;s metadata was found and returned. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_result**
> ExecutionResult retrieve_result(workspace_id, result_id, offset=offset, limit=limit, excluded_total_dimensions=excluded_total_dimensions, x_gdc_cancel_token=x_gdc_cancel_token)

Get a single execution result

Gets a single execution result.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.execution_result import ExecutionResult
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    result_id = 'a9b28f9dc55f37ea9f4a5fb0c76895923591e781' # str | Result ID
    offset = [] # List[int] | Request page with these offsets. Format is offset=1,2,3,... - one offset for each dimensions in ResultSpec from originating AFM. (optional) (default to [])
    limit = [] # List[int] | Return only this number of items. Format is limit=1,2,3,... - one limit for each dimensions in ResultSpec from originating AFM. (optional) (default to [])
    excluded_total_dimensions = [] # List[str] | Identifiers of the dimensions where grand total data should not be returned for this request. A grand total will not be returned if all of its totalDimensions are in excludedTotalDimensions. (optional) (default to [])
    x_gdc_cancel_token = 'x_gdc_cancel_token_example' # str |  (optional)

    try:
        # Get a single execution result
        api_response = api_instance.retrieve_result(workspace_id, result_id, offset=offset, limit=limit, excluded_total_dimensions=excluded_total_dimensions, x_gdc_cancel_token=x_gdc_cancel_token)
        print("The response of ActionsApi->retrieve_result:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->retrieve_result: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **result_id** | **str**| Result ID | 
 **offset** | [**List[int]**](int.md)| Request page with these offsets. Format is offset&#x3D;1,2,3,... - one offset for each dimensions in ResultSpec from originating AFM. | [optional] [default to []]
 **limit** | [**List[int]**](int.md)| Return only this number of items. Format is limit&#x3D;1,2,3,... - one limit for each dimensions in ResultSpec from originating AFM. | [optional] [default to []]
 **excluded_total_dimensions** | [**List[str]**](str.md)| Identifiers of the dimensions where grand total data should not be returned for this request. A grand total will not be returned if all of its totalDimensions are in excludedTotalDimensions. | [optional] [default to []]
 **x_gdc_cancel_token** | **str**|  | [optional] 

### Return type

[**ExecutionResult**](ExecutionResult.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Execution result was found and returned. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_translations**
> Xliff retrieve_translations(workspace_id, locale_request)

Retrieve translations for entities.

Retrieve all translation for existing entities in a particular locale. The source translations returned by this endpoint are always original, not translated, texts. Because the XLIFF schema definition has the 'xs:language' constraint for the 'srcLang' attribute, it is always set to 'en-US' value.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.locale_request import LocaleRequest
from gooddata_api_client.models.xliff import Xliff
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    locale_request = gooddata_api_client.LocaleRequest() # LocaleRequest | 

    try:
        # Retrieve translations for entities.
        api_response = api_instance.retrieve_translations(workspace_id, locale_request)
        print("The response of ActionsApi->retrieve_translations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->retrieve_translations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **locale_request** | [**LocaleRequest**](LocaleRequest.md)|  | 

### Return type

[**Xliff**](Xliff.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | XLIFF file containing translations for a particular locale. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **scan_data_source**
> ScanResultPdm scan_data_source(data_source_id, scan_request)

Scan a database to get a physical data model (PDM)

It scans a database and transforms its metadata to a declarative definition of the physical data model (PDM). The result of the request contains the mentioned physical data model (PDM) of a database within warning, for example, about unsupported columns.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.scan_request import ScanRequest
from gooddata_api_client.models.scan_result_pdm import ScanResultPdm
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    data_source_id = 'myPostgres' # str | Data source id
    scan_request = gooddata_api_client.ScanRequest() # ScanRequest | 

    try:
        # Scan a database to get a physical data model (PDM)
        api_response = api_instance.scan_data_source(data_source_id, scan_request)
        print("The response of ActionsApi->scan_data_source:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->scan_data_source: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| Data source id | 
 **scan_request** | [**ScanRequest**](ScanRequest.md)|  | 

### Return type

[**ScanResultPdm**](ScanResultPdm.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The result of the scan. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **scan_sql**
> ScanSqlResponse scan_sql(data_source_id, scan_sql_request)

Collect metadata about SQL query

It executes SQL query against specified data source and extracts metadata. Metadata consist of column names and column data types. It can optionally provide also preview of data returned by SQL query

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.scan_sql_request import ScanSqlRequest
from gooddata_api_client.models.scan_sql_response import ScanSqlResponse
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    data_source_id = 'myPostgres' # str | Data source id
    scan_sql_request = gooddata_api_client.ScanSqlRequest() # ScanSqlRequest | 

    try:
        # Collect metadata about SQL query
        api_response = api_instance.scan_sql(data_source_id, scan_sql_request)
        print("The response of ActionsApi->scan_sql:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->scan_sql: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| Data source id | 
 **scan_sql_request** | [**ScanSqlRequest**](ScanSqlRequest.md)|  | 

### Return type

[**ScanSqlResponse**](ScanSqlResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The result of the scan. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_translations**
> set_translations(workspace_id, xliff)

Set translations for entities.

Set translation for existing entities in a particular locale.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.xliff import Xliff
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    xliff = gooddata_api_client.Xliff() # Xliff | 

    try:
        # Set translations for entities.
        api_instance.set_translations(workspace_id, xliff)
    except Exception as e:
        print("Exception when calling ActionsApi->set_translations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **xliff** | [**Xliff**](Xliff.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/xml
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Translations were successfully set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **switch_active_identity_provider**
> switch_active_identity_provider(switch_identity_provider_request)

Switch Active Identity Provider

Switch the active identity provider for the organization. Requires MANAGE permission on the organization.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.switch_identity_provider_request import SwitchIdentityProviderRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    switch_identity_provider_request = gooddata_api_client.SwitchIdentityProviderRequest() # SwitchIdentityProviderRequest | 

    try:
        # Switch Active Identity Provider
        api_instance.switch_active_identity_provider(switch_identity_provider_request)
    except Exception as e:
        print("Exception when calling ActionsApi->switch_active_identity_provider: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **switch_identity_provider_request** | [**SwitchIdentityProviderRequest**](SwitchIdentityProviderRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tags**
> AnalyticsCatalogTags tags(workspace_id)

Get Analytics Catalog Tags

Returns a list of tags for this workspace

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.analytics_catalog_tags import AnalyticsCatalogTags
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier

    try:
        # Get Analytics Catalog Tags
        api_response = api_instance.tags(workspace_id)
        print("The response of ActionsApi->tags:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->tags: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 

### Return type

[**AnalyticsCatalogTags**](AnalyticsCatalogTags.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_data_source**
> TestResponse test_data_source(data_source_id, test_request)

Test data source connection by data source id

Test if it is possible to connect to a database using an existing data source definition.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.test_request import TestRequest
from gooddata_api_client.models.test_response import TestResponse
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    data_source_id = 'myPostgres' # str | Data source id
    test_request = gooddata_api_client.TestRequest() # TestRequest | 

    try:
        # Test data source connection by data source id
        api_response = api_instance.test_data_source(data_source_id, test_request)
        print("The response of ActionsApi->test_data_source:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->test_data_source: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| Data source id | 
 **test_request** | [**TestRequest**](TestRequest.md)|  | 

### Return type

[**TestResponse**](TestResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The result of the test of a data source connection. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_data_source_definition**
> TestResponse test_data_source_definition(test_definition_request)

Test connection by data source definition

Test if it is possible to connect to a database using a connection provided by the data source definition in the request body.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.test_definition_request import TestDefinitionRequest
from gooddata_api_client.models.test_response import TestResponse
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    test_definition_request = gooddata_api_client.TestDefinitionRequest() # TestDefinitionRequest | 

    try:
        # Test connection by data source definition
        api_response = api_instance.test_data_source_definition(test_definition_request)
        print("The response of ActionsApi->test_data_source_definition:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->test_data_source_definition: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_definition_request** | [**TestDefinitionRequest**](TestDefinitionRequest.md)|  | 

### Return type

[**TestResponse**](TestResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The result of the test of a data source connection. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_existing_notification_channel**
> TestResponse test_existing_notification_channel(notification_channel_id, test_destination_request=test_destination_request)

Test existing notification channel.

Tests the existing notification channel by sending a test notification.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.test_destination_request import TestDestinationRequest
from gooddata_api_client.models.test_response import TestResponse
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    notification_channel_id = 'notification_channel_id_example' # str | 
    test_destination_request = gooddata_api_client.TestDestinationRequest() # TestDestinationRequest |  (optional)

    try:
        # Test existing notification channel.
        api_response = api_instance.test_existing_notification_channel(notification_channel_id, test_destination_request=test_destination_request)
        print("The response of ActionsApi->test_existing_notification_channel:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->test_existing_notification_channel: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **notification_channel_id** | **str**|  | 
 **test_destination_request** | [**TestDestinationRequest**](TestDestinationRequest.md)|  | [optional] 

### Return type

[**TestResponse**](TestResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The result of the test of a notification channel connection. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_notification_channel**
> TestResponse test_notification_channel(test_destination_request)

Test notification channel.

Tests the notification channel by sending a test notification.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.test_destination_request import TestDestinationRequest
from gooddata_api_client.models.test_response import TestResponse
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    test_destination_request = gooddata_api_client.TestDestinationRequest() # TestDestinationRequest | 

    try:
        # Test notification channel.
        api_response = api_instance.test_notification_channel(test_destination_request)
        print("The response of ActionsApi->test_notification_channel:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->test_notification_channel: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_destination_request** | [**TestDestinationRequest**](TestDestinationRequest.md)|  | 

### Return type

[**TestResponse**](TestResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The result of the test of a notification channel connection. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **trigger_automation**
> trigger_automation(workspace_id, trigger_automation_request)

Trigger automation.

Trigger the automation in the request.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.trigger_automation_request import TriggerAutomationRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    trigger_automation_request = gooddata_api_client.TriggerAutomationRequest() # TriggerAutomationRequest | 

    try:
        # Trigger automation.
        api_instance.trigger_automation(workspace_id, trigger_automation_request)
    except Exception as e:
        print("Exception when calling ActionsApi->trigger_automation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **trigger_automation_request** | [**TriggerAutomationRequest**](TriggerAutomationRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | The automation is successfully triggered. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **trigger_existing_automation**
> trigger_existing_automation(workspace_id, automation_id)

Trigger existing automation.

Trigger the existing automation to execute immediately.

### Example


```python
import gooddata_api_client
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    automation_id = 'automation_id_example' # str | 

    try:
        # Trigger existing automation.
        api_instance.trigger_existing_automation(workspace_id, automation_id)
    except Exception as e:
        print("Exception when calling ActionsApi->trigger_existing_automation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **automation_id** | **str**|  | 

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
**204** | The automation is successfully triggered. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unpause_organization_automations**
> unpause_organization_automations(organization_automation_management_bulk_request)

Unpause selected automations across all workspaces

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.organization_automation_management_bulk_request import OrganizationAutomationManagementBulkRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    organization_automation_management_bulk_request = gooddata_api_client.OrganizationAutomationManagementBulkRequest() # OrganizationAutomationManagementBulkRequest | 

    try:
        # Unpause selected automations across all workspaces
        api_instance.unpause_organization_automations(organization_automation_management_bulk_request)
    except Exception as e:
        print("Exception when calling ActionsApi->unpause_organization_automations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_automation_management_bulk_request** | [**OrganizationAutomationManagementBulkRequest**](OrganizationAutomationManagementBulkRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unpause_workspace_automations**
> unpause_workspace_automations(workspace_id, workspace_automation_management_bulk_request)

Unpause selected automations in the workspace

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.workspace_automation_management_bulk_request import WorkspaceAutomationManagementBulkRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    workspace_automation_management_bulk_request = gooddata_api_client.WorkspaceAutomationManagementBulkRequest() # WorkspaceAutomationManagementBulkRequest | 

    try:
        # Unpause selected automations in the workspace
        api_instance.unpause_workspace_automations(workspace_id, workspace_automation_management_bulk_request)
    except Exception as e:
        print("Exception when calling ActionsApi->unpause_workspace_automations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **workspace_automation_management_bulk_request** | [**WorkspaceAutomationManagementBulkRequest**](WorkspaceAutomationManagementBulkRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unsubscribe_all_automations**
> unsubscribe_all_automations()

Unsubscribe from all automations in all workspaces

### Example


```python
import gooddata_api_client
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)

    try:
        # Unsubscribe from all automations in all workspaces
        api_instance.unsubscribe_all_automations()
    except Exception as e:
        print("Exception when calling ActionsApi->unsubscribe_all_automations: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

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
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unsubscribe_automation**
> unsubscribe_automation(workspace_id, automation_id)

Unsubscribe from an automation

### Example


```python
import gooddata_api_client
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    automation_id = 'automation_id_example' # str | 

    try:
        # Unsubscribe from an automation
        api_instance.unsubscribe_automation(workspace_id, automation_id)
    except Exception as e:
        print("Exception when calling ActionsApi->unsubscribe_automation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **automation_id** | **str**|  | 

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
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unsubscribe_organization_automations**
> unsubscribe_organization_automations(organization_automation_management_bulk_request)

Unsubscribe from selected automations across all workspaces

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.organization_automation_management_bulk_request import OrganizationAutomationManagementBulkRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    organization_automation_management_bulk_request = gooddata_api_client.OrganizationAutomationManagementBulkRequest() # OrganizationAutomationManagementBulkRequest | 

    try:
        # Unsubscribe from selected automations across all workspaces
        api_instance.unsubscribe_organization_automations(organization_automation_management_bulk_request)
    except Exception as e:
        print("Exception when calling ActionsApi->unsubscribe_organization_automations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_automation_management_bulk_request** | [**OrganizationAutomationManagementBulkRequest**](OrganizationAutomationManagementBulkRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unsubscribe_selected_workspace_automations**
> unsubscribe_selected_workspace_automations(workspace_id, workspace_automation_management_bulk_request)

Unsubscribe from selected automations in the workspace

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.workspace_automation_management_bulk_request import WorkspaceAutomationManagementBulkRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    workspace_automation_management_bulk_request = gooddata_api_client.WorkspaceAutomationManagementBulkRequest() # WorkspaceAutomationManagementBulkRequest | 

    try:
        # Unsubscribe from selected automations in the workspace
        api_instance.unsubscribe_selected_workspace_automations(workspace_id, workspace_automation_management_bulk_request)
    except Exception as e:
        print("Exception when calling ActionsApi->unsubscribe_selected_workspace_automations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **workspace_automation_management_bulk_request** | [**WorkspaceAutomationManagementBulkRequest**](WorkspaceAutomationManagementBulkRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unsubscribe_workspace_automations**
> unsubscribe_workspace_automations(workspace_id)

Unsubscribe from all automations in the workspace

### Example


```python
import gooddata_api_client
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 

    try:
        # Unsubscribe from all automations in the workspace
        api_instance.unsubscribe_workspace_automations(workspace_id)
    except Exception as e:
        print("Exception when calling ActionsApi->unsubscribe_workspace_automations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 

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
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_memory_item**
> MemoryItem update_memory_item(workspace_id, memory_id, memory_item)

(EXPERIMENTAL) Update memory item

(EXPERIMENTAL) Updates memory item and returns it

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.memory_item import MemoryItem
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    memory_id = 'memory_id_example' # str | 
    memory_item = gooddata_api_client.MemoryItem() # MemoryItem | 

    try:
        # (EXPERIMENTAL) Update memory item
        api_response = api_instance.update_memory_item(workspace_id, memory_id, memory_item)
        print("The response of ActionsApi->update_memory_item:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->update_memory_item: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **memory_id** | **str**|  | 
 **memory_item** | [**MemoryItem**](MemoryItem.md)|  | 

### Return type

[**MemoryItem**](MemoryItem.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **validate_llm_endpoint**
> ValidateLLMEndpointResponse validate_llm_endpoint(validate_llm_endpoint_request)

Validate LLM Endpoint

Validates LLM endpoint with provided parameters.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.validate_llm_endpoint_request import ValidateLLMEndpointRequest
from gooddata_api_client.models.validate_llm_endpoint_response import ValidateLLMEndpointResponse
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    validate_llm_endpoint_request = gooddata_api_client.ValidateLLMEndpointRequest() # ValidateLLMEndpointRequest | 

    try:
        # Validate LLM Endpoint
        api_response = api_instance.validate_llm_endpoint(validate_llm_endpoint_request)
        print("The response of ActionsApi->validate_llm_endpoint:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->validate_llm_endpoint: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **validate_llm_endpoint_request** | [**ValidateLLMEndpointRequest**](ValidateLLMEndpointRequest.md)|  | 

### Return type

[**ValidateLLMEndpointResponse**](ValidateLLMEndpointResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **validate_llm_endpoint_by_id**
> ValidateLLMEndpointResponse validate_llm_endpoint_by_id(llm_endpoint_id, validate_llm_endpoint_by_id_request=validate_llm_endpoint_by_id_request)

Validate LLM Endpoint By Id

Validates existing LLM endpoint with provided parameters and updates it if they are valid.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.validate_llm_endpoint_by_id_request import ValidateLLMEndpointByIdRequest
from gooddata_api_client.models.validate_llm_endpoint_response import ValidateLLMEndpointResponse
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    llm_endpoint_id = 'llm_endpoint_id_example' # str | 
    validate_llm_endpoint_by_id_request = gooddata_api_client.ValidateLLMEndpointByIdRequest() # ValidateLLMEndpointByIdRequest |  (optional)

    try:
        # Validate LLM Endpoint By Id
        api_response = api_instance.validate_llm_endpoint_by_id(llm_endpoint_id, validate_llm_endpoint_by_id_request=validate_llm_endpoint_by_id_request)
        print("The response of ActionsApi->validate_llm_endpoint_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->validate_llm_endpoint_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **llm_endpoint_id** | **str**|  | 
 **validate_llm_endpoint_by_id_request** | [**ValidateLLMEndpointByIdRequest**](ValidateLLMEndpointByIdRequest.md)|  | [optional] 

### Return type

[**ValidateLLMEndpointResponse**](ValidateLLMEndpointResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_resolve_all_settings**
> List[ResolvedSetting] workspace_resolve_all_settings(workspace_id)

Values for all settings.

Resolves values for all settings in a workspace by current user, workspace, organization, or default settings.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.resolved_setting import ResolvedSetting
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 

    try:
        # Values for all settings.
        api_response = api_instance.workspace_resolve_all_settings(workspace_id)
        print("The response of ActionsApi->workspace_resolve_all_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->workspace_resolve_all_settings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 

### Return type

[**List[ResolvedSetting]**](ResolvedSetting.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Values for selected settings. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_resolve_settings**
> List[ResolvedSetting] workspace_resolve_settings(workspace_id, resolve_settings_request)

Values for selected settings.

Resolves value for selected settings in a workspace by current user, workspace, organization, or default settings.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.resolve_settings_request import ResolveSettingsRequest
from gooddata_api_client.models.resolved_setting import ResolvedSetting
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.ActionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    resolve_settings_request = gooddata_api_client.ResolveSettingsRequest() # ResolveSettingsRequest | 

    try:
        # Values for selected settings.
        api_response = api_instance.workspace_resolve_settings(workspace_id, resolve_settings_request)
        print("The response of ActionsApi->workspace_resolve_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActionsApi->workspace_resolve_settings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **resolve_settings_request** | [**ResolveSettingsRequest**](ResolveSettingsRequest.md)|  | 

### Return type

[**List[ResolvedSetting]**](ResolvedSetting.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Values for selected settings. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


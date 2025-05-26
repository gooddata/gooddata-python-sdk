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
[**create_pdf_export**](ActionsApi.md#create_pdf_export) | **POST** /api/v1/actions/workspaces/{workspaceId}/export/visual | Create visual - pdf export request
[**create_raw_export**](ActionsApi.md#create_raw_export) | **POST** /api/v1/actions/workspaces/{workspaceId}/export/raw | (EXPERIMENTAL) Create raw export request
[**create_slides_export**](ActionsApi.md#create_slides_export) | **POST** /api/v1/actions/workspaces/{workspaceId}/export/slides | (EXPERIMENTAL) Create slides export request
[**create_tabular_export**](ActionsApi.md#create_tabular_export) | **POST** /api/v1/actions/workspaces/{workspaceId}/export/tabular | Create tabular export request
[**dashboard_permissions**](ActionsApi.md#dashboard_permissions) | **GET** /api/v1/actions/workspaces/{workspaceId}/analyticalDashboards/{dashboardId}/permissions | Get Dashboard Permissions
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
[**get_metadata**](ActionsApi.md#get_metadata) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/visual/{exportId}/metadata | Retrieve metadata context
[**get_notifications**](ActionsApi.md#get_notifications) | **GET** /api/v1/actions/notifications | Get latest notifications.
[**get_raw_export**](ActionsApi.md#get_raw_export) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/raw/{exportId} | (EXPERIMENTAL) Retrieve exported files
[**get_slides_export**](ActionsApi.md#get_slides_export) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/slides/{exportId} | (EXPERIMENTAL) Retrieve exported files
[**get_slides_export_metadata**](ActionsApi.md#get_slides_export_metadata) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/slides/{exportId}/metadata | (EXPERIMENTAL) Retrieve metadata context
[**get_tabular_export**](ActionsApi.md#get_tabular_export) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/tabular/{exportId} | Retrieve exported files
[**get_translation_tags**](ActionsApi.md#get_translation_tags) | **GET** /api/v1/actions/workspaces/{workspaceId}/translations | Get translation tags.
[**inherited_entity_conflicts**](ActionsApi.md#inherited_entity_conflicts) | **GET** /api/v1/actions/workspaces/{workspaceId}/inheritedEntityConflicts | Finds identifier conflicts in workspace hierarchy.
[**inherited_entity_prefixes**](ActionsApi.md#inherited_entity_prefixes) | **GET** /api/v1/actions/workspaces/{workspaceId}/inheritedEntityPrefixes | Get used entity prefixes in hierarchy
[**key_driver_analysis**](ActionsApi.md#key_driver_analysis) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/computeKeyDrivers | (EXPERIMENTAL) Compute key driver analysis
[**key_driver_analysis_result**](ActionsApi.md#key_driver_analysis_result) | **GET** /api/v1/actions/workspaces/{workspaceId}/execution/computeKeyDrivers/result/{resultId} | (EXPERIMENTAL) Get key driver analysis result
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
[**register_upload_notification**](ActionsApi.md#register_upload_notification) | **POST** /api/v1/actions/dataSources/{dataSourceId}/uploadNotification | Register an upload notification
[**resolve_all_entitlements**](ActionsApi.md#resolve_all_entitlements) | **GET** /api/v1/actions/resolveEntitlements | Values for all public entitlements.
[**resolve_all_settings_without_workspace**](ActionsApi.md#resolve_all_settings_without_workspace) | **GET** /api/v1/actions/resolveSettings | Values for all settings without workspace.
[**resolve_requested_entitlements**](ActionsApi.md#resolve_requested_entitlements) | **POST** /api/v1/actions/resolveEntitlements | Values for requested public entitlements.
[**resolve_settings_without_workspace**](ActionsApi.md#resolve_settings_without_workspace) | **POST** /api/v1/actions/resolveSettings | Values for selected settings without workspace.
[**retrieve_execution_metadata**](ActionsApi.md#retrieve_execution_metadata) | **GET** /api/v1/actions/workspaces/{workspaceId}/execution/afm/execute/result/{resultId}/metadata | Get a single execution result&#39;s metadata.
[**retrieve_result**](ActionsApi.md#retrieve_result) | **GET** /api/v1/actions/workspaces/{workspaceId}/execution/afm/execute/result/{resultId} | Get a single execution result
[**retrieve_translations**](ActionsApi.md#retrieve_translations) | **POST** /api/v1/actions/workspaces/{workspaceId}/translations/retrieve | Retrieve translations for entities.
[**scan_data_source**](ActionsApi.md#scan_data_source) | **POST** /api/v1/actions/dataSources/{dataSourceId}/scan | Scan a database to get a physical data model (PDM)
[**scan_sql**](ActionsApi.md#scan_sql) | **POST** /api/v1/actions/dataSources/{dataSourceId}/scanSql | Collect metadata about SQL query
[**set_translations**](ActionsApi.md#set_translations) | **POST** /api/v1/actions/workspaces/{workspaceId}/translations/set | Set translations for entities.
[**test_data_source**](ActionsApi.md#test_data_source) | **POST** /api/v1/actions/dataSources/{dataSourceId}/test | Test data source connection by data source id
[**test_data_source_definition**](ActionsApi.md#test_data_source_definition) | **POST** /api/v1/actions/dataSource/test | Test connection by data source definition
[**test_existing_notification_channel**](ActionsApi.md#test_existing_notification_channel) | **POST** /api/v1/actions/notificationChannels/{notificationChannelId}/test | Test existing notification channel.
[**test_notification_channel**](ActionsApi.md#test_notification_channel) | **POST** /api/v1/actions/notificationChannels/test | Test notification channel.
[**trigger_automation**](ActionsApi.md#trigger_automation) | **POST** /api/v1/actions/workspaces/{workspaceId}/automations/trigger | Trigger automation.
[**trigger_existing_automation**](ActionsApi.md#trigger_existing_automation) | **POST** /api/v1/actions/workspaces/{workspaceId}/automations/{automationId}/trigger | Trigger existing automation.
[**unsubscribe_all_automations**](ActionsApi.md#unsubscribe_all_automations) | **DELETE** /api/v1/actions/organization/automations/unsubscribe | Unsubscribe from all automations in all workspaces
[**unsubscribe_automation**](ActionsApi.md#unsubscribe_automation) | **DELETE** /api/v1/actions/workspaces/{workspaceId}/automations/{automationId}/unsubscribe | Unsubscribe from an automation
[**unsubscribe_workspace_automations**](ActionsApi.md#unsubscribe_workspace_automations) | **DELETE** /api/v1/actions/workspaces/{workspaceId}/automations/unsubscribe | Unsubscribe from all automations in the workspace
[**workspace_resolve_all_settings**](ActionsApi.md#workspace_resolve_all_settings) | **GET** /api/v1/actions/workspaces/{workspaceId}/resolveSettings | Values for all settings.
[**workspace_resolve_settings**](ActionsApi.md#workspace_resolve_settings) | **POST** /api/v1/actions/workspaces/{workspaceId}/resolveSettings | Values for selected settings.


# **ai_chat**
> ChatResult ai_chat(workspace_id, chat_request)

(BETA) Chat with AI

(BETA) Combines multiple use cases such as search, create visualizations, ...

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.chat_result import ChatResult
from gooddata_api_client.model.chat_request import ChatRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    chat_request = ChatRequest(
        limit_create=3,
        limit_create_context=10,
        limit_search=5,
        question="question_example",
        relevant_score_threshold=0.45,
        search_score_threshold=0.9,
        thread_id_suffix="thread_id_suffix_example",
        title_to_descriptor_ratio=0.7,
        user_context=UserContext(
            active_object=ActiveObjectIdentification(
                id="id_example",
                type="type_example",
                workspace_id="workspace_id_example",
            ),
        ),
    ) # ChatRequest | 

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Chat with AI
        api_response = api_instance.ai_chat(workspace_id, chat_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.chat_history_result import ChatHistoryResult
from gooddata_api_client.model.chat_history_request import ChatHistoryRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    chat_history_request = ChatHistoryRequest(
        chat_history_interaction_id="chat_history_interaction_id_example",
        reset=True,
        thread_id_suffix="thread_id_suffix_example",
        user_feedback="POSITIVE",
    ) # ChatHistoryRequest | 

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Get Chat History
        api_response = api_instance.ai_chat_history(workspace_id, chat_history_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
> [dict] ai_chat_stream(workspace_id, chat_request)

(BETA) Chat with AI

(BETA) Combines multiple use cases such as search, create visualizations, ...

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.chat_request import ChatRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    chat_request = ChatRequest(
        limit_create=3,
        limit_create_context=10,
        limit_search=5,
        question="question_example",
        relevant_score_threshold=0.45,
        search_score_threshold=0.9,
        thread_id_suffix="thread_id_suffix_example",
        title_to_descriptor_ratio=0.7,
        user_context=UserContext(
            active_object=ActiveObjectIdentification(
                id="id_example",
                type="type_example",
                workspace_id="workspace_id_example",
            ),
        ),
    ) # ChatRequest | 

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Chat with AI
        api_response = api_instance.ai_chat_stream(workspace_id, chat_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->ai_chat_stream: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **chat_request** | [**ChatRequest**](ChatRequest.md)|  |

### Return type

**[dict]**

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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.chat_usage_response import ChatUsageResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier

    # example passing only required values which don't have defaults set
    try:
        # Get Chat Usage
        api_response = api_instance.ai_chat_usage(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.search_result import SearchResult
from gooddata_api_client.model.search_request import SearchRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    search_request = SearchRequest(
        deep_search=False,
        limit=10,
        object_types=[
            "attribute",
        ],
        question="question_example",
        relevant_score_threshold=0.3,
        title_to_descriptor_ratio=0.7,
    ) # SearchRequest | 

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Semantic Search in Metadata
        api_response = api_instance.ai_search(workspace_id, search_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
> [PlatformUsage] all_platform_usage()

Info about the platform usage.

Provides information about platform usage, like amount of users, workspaces, ...  _NOTE_: The `admin` user is always excluded from this amount.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.platform_usage import PlatformUsage
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Info about the platform usage.
        api_response = api_instance.all_platform_usage()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->all_platform_usage: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**[PlatformUsage]**](PlatformUsage.md)

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
> SmartFunctionResponse anomaly_detection(workspace_id, result_id, anomaly_detection_request)

(EXPERIMENTAL) Smart functions - Anomaly Detection

(EXPERIMENTAL) Computes anomaly detection.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.anomaly_detection_request import AnomalyDetectionRequest
from gooddata_api_client.model.smart_function_response import SmartFunctionResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    result_id = "9bd52018570364264fcf62d373da6bed313120e8" # str | Input result ID to be used in the computation
    anomaly_detection_request = AnomalyDetectionRequest(
        sensitivity=3.14,
    ) # AnomalyDetectionRequest | 
    skip_cache = False # bool | Ignore all caches during execution of current request. (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Smart functions - Anomaly Detection
        api_response = api_instance.anomaly_detection(workspace_id, result_id, anomaly_detection_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->anomaly_detection: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (EXPERIMENTAL) Smart functions - Anomaly Detection
        api_response = api_instance.anomaly_detection(workspace_id, result_id, anomaly_detection_request, skip_cache=skip_cache)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->anomaly_detection: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **result_id** | **str**| Input result ID to be used in the computation |
 **anomaly_detection_request** | [**AnomalyDetectionRequest**](AnomalyDetectionRequest.md)|  |
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional] if omitted the server will use the default value of False

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
> AnomalyDetectionResult anomaly_detection_result(workspace_id, result_id)

(EXPERIMENTAL) Smart functions - Anomaly Detection Result

(EXPERIMENTAL) Gets anomalies.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.anomaly_detection_result import AnomalyDetectionResult
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    result_id = "a9b28f9dc55f37ea9f4a5fb0c76895923591e781" # str | Result ID
    offset = 1 # int |  (optional)
    limit = 1 # int |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Smart functions - Anomaly Detection Result
        api_response = api_instance.anomaly_detection_result(workspace_id, result_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->anomaly_detection_result: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (EXPERIMENTAL) Smart functions - Anomaly Detection Result
        api_response = api_instance.anomaly_detection_result(workspace_id, result_id, offset=offset, limit=limit)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.available_assignees import AvailableAssignees
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    dashboard_id = "dashboardId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get Available Assignees
        api_response = api_instance.available_assignees(workspace_id, dashboard_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.afm_cancel_tokens import AfmCancelTokens
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    afm_cancel_tokens = AfmCancelTokens(
        result_id_to_cancel_token_pairs={
            "key": "key_example",
        },
    ) # AfmCancelTokens | 

    # example passing only required values which don't have defaults set
    try:
        # Applies all the given cancel tokens.
        api_response = api_instance.cancel_executions(workspace_id, afm_cancel_tokens)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
> [IdentifierDuplications] check_entity_overrides(workspace_id, hierarchy_object_identification)

Finds entities with given ID in hierarchy.

Finds entities with given ID in hierarchy (e.g. to check possible future conflicts).

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.hierarchy_object_identification import HierarchyObjectIdentification
from gooddata_api_client.model.identifier_duplications import IdentifierDuplications
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    hierarchy_object_identification = [
        HierarchyObjectIdentification(
            id="id_example",
            type="metric",
        ),
    ] # [HierarchyObjectIdentification] | 

    # example passing only required values which don't have defaults set
    try:
        # Finds entities with given ID in hierarchy.
        api_response = api_instance.check_entity_overrides(workspace_id, hierarchy_object_identification)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->check_entity_overrides: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **hierarchy_object_identification** | [**[HierarchyObjectIdentification]**](HierarchyObjectIdentification.md)|  |

### Return type

[**[IdentifierDuplications]**](IdentifierDuplications.md)

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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.locale_request import LocaleRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    locale_request = LocaleRequest(
        locale="en-US",
    ) # LocaleRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Cleans up translations.
        api_instance.clean_translations(workspace_id, locale_request)
    except gooddata_api_client.ApiException as e:
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
> SmartFunctionResponse clustering(workspace_id, result_id, clustering_request)

(EXPERIMENTAL) Smart functions - Clustering

(EXPERIMENTAL) Computes clusters for data points from the provided execution result and parameters.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.clustering_request import ClusteringRequest
from gooddata_api_client.model.smart_function_response import SmartFunctionResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    result_id = "9bd52018570364264fcf62d373da6bed313120e8" # str | Input result ID to be used in the computation
    clustering_request = ClusteringRequest(
        number_of_clusters=1,
        threshold=0.03,
    ) # ClusteringRequest | 
    skip_cache = False # bool | Ignore all caches during execution of current request. (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Smart functions - Clustering
        api_response = api_instance.clustering(workspace_id, result_id, clustering_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->clustering: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (EXPERIMENTAL) Smart functions - Clustering
        api_response = api_instance.clustering(workspace_id, result_id, clustering_request, skip_cache=skip_cache)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->clustering: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **result_id** | **str**| Input result ID to be used in the computation |
 **clustering_request** | [**ClusteringRequest**](ClusteringRequest.md)|  |
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional] if omitted the server will use the default value of False

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
> ClusteringResult clustering_result(workspace_id, result_id)

(EXPERIMENTAL) Smart functions - Clustering Result

(EXPERIMENTAL) Gets clustering result.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.clustering_result import ClusteringResult
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    result_id = "a9b28f9dc55f37ea9f4a5fb0c76895923591e781" # str | Result ID
    offset = 1 # int |  (optional)
    limit = 1 # int |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Smart functions - Clustering Result
        api_response = api_instance.clustering_result(workspace_id, result_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->clustering_result: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (EXPERIMENTAL) Smart functions - Clustering Result
        api_response = api_instance.clustering_result(workspace_id, result_id, offset=offset, limit=limit)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.column_statistics_response import ColumnStatisticsResponse
from gooddata_api_client.model.column_statistics_request import ColumnStatisticsRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    data_source_id = "dataSourceId_example" # str | 
    column_statistics_request = ColumnStatisticsRequest(
        column_name="column_name_example",
        frequency=FrequencyProperties(
            value_limit=10,
        ),
        _from=ColumnStatisticsRequestFrom(None),
        histogram=HistogramProperties(
            bucket_count=1,
        ),
        statistics=[
            "COUNT",
        ],
    ) # ColumnStatisticsRequest | 

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Compute column statistics
        api_response = api_instance.column_statistics(data_source_id, column_statistics_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
> ElementsResponse compute_label_elements_post(workspace_id, elements_request)

Listing of label values. The resulting data are limited by the static platform limit to the maximum of 10000 rows.

Returns paged list of elements (values) of given label satisfying given filtering criteria.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.elements_request import ElementsRequest
from gooddata_api_client.model.elements_response import ElementsResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    elements_request = ElementsRequest(
        cache_id="cache_id_example",
        complement_filter=False,
        data_sampling_percentage=100.0,
        depends_on=[
            ElementsRequestDependsOnInner(None),
        ],
        exact_filter=[
            "exact_filter_example",
        ],
        exclude_primary_label=False,
        filter_by=FilterBy(
            label_type="REQUESTED",
        ),
        label="label_id",
        pattern_filter="pattern_filter_example",
        sort_order="ASC",
        validate_by=[
            ValidateByItem(
                id="id_example",
                type="fact",
            ),
        ],
    ) # ElementsRequest | 
    offset = 0 # int | Request page with this offset. Must be positive integer. The API is limited to the maximum of 10000 items. Therefore this parameter is limited to this number as well. (optional) if omitted the server will use the default value of 0
    limit = 1000 # int | Return only this number of items. Must be positive integer. The API is limited to the maximum of 10000 items. Therefore this parameter is limited to this number as well. (optional) if omitted the server will use the default value of 1000
    skip_cache = False # bool | Ignore all caches during execution of current request. (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # Listing of label values. The resulting data are limited by the static platform limit to the maximum of 10000 rows.
        api_response = api_instance.compute_label_elements_post(workspace_id, elements_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->compute_label_elements_post: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Listing of label values. The resulting data are limited by the static platform limit to the maximum of 10000 rows.
        api_response = api_instance.compute_label_elements_post(workspace_id, elements_request, offset=offset, limit=limit, skip_cache=skip_cache)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->compute_label_elements_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **elements_request** | [**ElementsRequest**](ElementsRequest.md)|  |
 **offset** | **int**| Request page with this offset. Must be positive integer. The API is limited to the maximum of 10000 items. Therefore this parameter is limited to this number as well. | [optional] if omitted the server will use the default value of 0
 **limit** | **int**| Return only this number of items. Must be positive integer. The API is limited to the maximum of 10000 items. Therefore this parameter is limited to this number as well. | [optional] if omitted the server will use the default value of 1000
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional] if omitted the server will use the default value of False

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
> AfmExecutionResponse compute_report(workspace_id, afm_execution)

Executes analytical request and returns link to the result

AFM is a combination of attributes, measures and filters that describe a query you want to execute.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.afm_execution_response import AfmExecutionResponse
from gooddata_api_client.model.afm_execution import AfmExecution
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    afm_execution = AfmExecution(
        execution=AFM(
            attributes=[
                AttributeItem(
                    label=AfmObjectIdentifierLabel(
                        identifier=AfmObjectIdentifierLabelIdentifier(
                            id="sample_item.price",
                            type="label",
                        ),
                    ),
                    local_identifier="attribute_1",
                    show_all_values=False,
                ),
            ],
            aux_measures=[
                MeasureItem(
                    definition=MeasureDefinition(),
                    local_identifier="metric_1",
                ),
            ],
            filters=[
                FilterDefinition(),
            ],
            measures=[
                MeasureItem(
                    definition=MeasureDefinition(),
                    local_identifier="metric_1",
                ),
            ],
        ),
        result_spec=ResultSpec(
            dimensions=[
                Dimension(
                    item_identifiers=["attribute_1","measureGroup"],
                    local_identifier="firstDimension",
                    sorting=[
                        SortKey(),
                    ],
                ),
            ],
            totals=[
                Total(
                    function="SUM",
                    local_identifier="firstTotal",
                    metric="metric_1",
                    total_dimensions=[
                        TotalDimension(
                            dimension_identifier="firstDimension",
                            total_dimension_items=["measureGroup"],
                        ),
                    ],
                ),
            ],
        ),
        settings=ExecutionSettings(
            data_sampling_percentage=0,
            timestamp=dateutil_parser('1970-01-01T00:00:00.00Z'),
        ),
    ) # AfmExecution | 
    skip_cache = False # bool | Ignore all caches during execution of current request. (optional) if omitted the server will use the default value of False
    timestamp = "2020-06-03T10:15:30+01:00" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Executes analytical request and returns link to the result
        api_response = api_instance.compute_report(workspace_id, afm_execution)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->compute_report: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Executes analytical request and returns link to the result
        api_response = api_instance.compute_report(workspace_id, afm_execution, skip_cache=skip_cache, timestamp=timestamp)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->compute_report: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **afm_execution** | [**AfmExecution**](AfmExecution.md)|  |
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional] if omitted the server will use the default value of False
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.afm_valid_descendants_query import AfmValidDescendantsQuery
from gooddata_api_client.model.afm_valid_descendants_response import AfmValidDescendantsResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    afm_valid_descendants_query = AfmValidDescendantsQuery(
        attributes=[
            AfmObjectIdentifierAttribute(
                identifier=AfmObjectIdentifierAttributeIdentifier(
                    id="sample_item.price",
                    type="attribute",
                ),
            ),
        ],
    ) # AfmValidDescendantsQuery | 

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Valid descendants
        api_response = api_instance.compute_valid_descendants(workspace_id, afm_valid_descendants_query)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.afm_valid_objects_query import AfmValidObjectsQuery
from gooddata_api_client.model.afm_valid_objects_response import AfmValidObjectsResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    afm_valid_objects_query = AfmValidObjectsQuery(
        afm=AFM(
            attributes=[
                AttributeItem(
                    label=AfmObjectIdentifierLabel(
                        identifier=AfmObjectIdentifierLabelIdentifier(
                            id="sample_item.price",
                            type="label",
                        ),
                    ),
                    local_identifier="attribute_1",
                    show_all_values=False,
                ),
            ],
            aux_measures=[
                MeasureItem(
                    definition=MeasureDefinition(),
                    local_identifier="metric_1",
                ),
            ],
            filters=[
                FilterDefinition(),
            ],
            measures=[
                MeasureItem(
                    definition=MeasureDefinition(),
                    local_identifier="metric_1",
                ),
            ],
        ),
        types=[
            "facts",
        ],
    ) # AfmValidObjectsQuery | 

    # example passing only required values which don't have defaults set
    try:
        # Valid objects
        api_response = api_instance.compute_valid_objects(workspace_id, afm_valid_objects_query)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.export_response import ExportResponse
from gooddata_api_client.model.dashboard_tabular_export_request import DashboardTabularExportRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    dashboard_id = "dashboardId_example" # str | 
    dashboard_tabular_export_request = DashboardTabularExportRequest(
        dashboard_filters_override=[
            DashboardTabularExportRequestDashboardFiltersOverrideInner(None),
        ],
        file_name="result",
        format="XLSX",
    ) # DashboardTabularExportRequest | 

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Create dashboard tabular export request
        api_response = api_instance.create_dashboard_export_request(workspace_id, dashboard_id, dashboard_tabular_export_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.export_response import ExportResponse
from gooddata_api_client.model.image_export_request import ImageExportRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    image_export_request = ImageExportRequest(
        dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
        file_name="filename",
        format="PNG",
        metadata=JsonNode(),
        widget_ids=[
            "widget_ids_example",
        ],
    ) # ImageExportRequest | 

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Create image export request
        api_response = api_instance.create_image_export(workspace_id, image_export_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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

# **create_pdf_export**
> ExportResponse create_pdf_export(workspace_id, visual_export_request)

Create visual - pdf export request

An visual export job will be created based on the export request and put to queue to be executed. The result of the operation will be an exportResult identifier that will be assembled by the client into a url that can be polled.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.export_response import ExportResponse
from gooddata_api_client.model.visual_export_request import VisualExportRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    visual_export_request = VisualExportRequest(
        dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
        file_name="filename",
        metadata={},
    ) # VisualExportRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Create visual - pdf export request
        api_response = api_instance.create_pdf_export(workspace_id, visual_export_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->create_pdf_export: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **visual_export_request** | [**VisualExportRequest**](VisualExportRequest.md)|  |

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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.export_response import ExportResponse
from gooddata_api_client.model.raw_export_request import RawExportRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    raw_export_request = RawExportRequest(
        custom_override=RawCustomOverride(
            labels={
                "key": RawCustomLabel(
                    title="title_example",
                ),
            },
            metrics={
                "key": RawCustomMetric(
                    title="title_example",
                ),
            },
        ),
        execution=AFM(
            attributes=[
                AttributeItem(
                    label=AfmObjectIdentifierLabel(
                        identifier=AfmObjectIdentifierLabelIdentifier(
                            id="sample_item.price",
                            type="label",
                        ),
                    ),
                    local_identifier="attribute_1",
                    show_all_values=False,
                ),
            ],
            aux_measures=[
                MeasureItem(
                    definition=MeasureDefinition(),
                    local_identifier="metric_1",
                ),
            ],
            filters=[
                FilterDefinition(),
            ],
            measures=[
                MeasureItem(
                    definition=MeasureDefinition(),
                    local_identifier="metric_1",
                ),
            ],
        ),
        execution_settings=ExecutionSettings(
            data_sampling_percentage=0,
            timestamp=dateutil_parser('1970-01-01T00:00:00.00Z'),
        ),
        file_name="result",
        format="CSV",
    ) # RawExportRequest | 

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Create raw export request
        api_response = api_instance.create_raw_export(workspace_id, raw_export_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
> ExportResponse create_slides_export(workspace_id, slides_export_request)

(EXPERIMENTAL) Create slides export request

Note: This API is an experimental and is going to change. Please, use it accordingly. A slides export job will be created based on the export request and put to queue to be executed. The result of the operation will be an exportResult identifier that will be assembled by the client into a url that can be polled.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.export_response import ExportResponse
from gooddata_api_client.model.slides_export_request import SlidesExportRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    slides_export_request = SlidesExportRequest(
        dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
        file_name="filename",
        format="PDF",
        metadata=JsonNode(),
        template_id="template_id_example",
        visualization_ids=[
            "visualization_ids_example",
        ],
        widget_ids=[
            "widget_ids_example",
        ],
    ) # SlidesExportRequest | 

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Create slides export request
        api_response = api_instance.create_slides_export(workspace_id, slides_export_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->create_slides_export: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **slides_export_request** | [**SlidesExportRequest**](SlidesExportRequest.md)|  |

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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.export_response import ExportResponse
from gooddata_api_client.model.tabular_export_request import TabularExportRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    tabular_export_request = TabularExportRequest(
        custom_override=CustomOverride(
            labels={
                "key": CustomLabel(
                    title="title_example",
                ),
            },
            metrics={
                "key": CustomMetric(
                    format="format_example",
                    title="title_example",
                ),
            },
        ),
        execution_result="ff483727196c9dc862c7fd3a5a84df55c96d61a4",
        file_name="result",
        format="CSV",
        metadata=JsonNode(),
        related_dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
        settings=Settings(
            merge_headers=True,
            pdf_page_size="a4 landscape",
            pdf_table_style=[
                PdfTableStyle(
                    properties=[
                        PdfTableStyleProperty(
                            key="key_example",
                            value="value_example",
                        ),
                    ],
                    selector="selector_example",
                ),
            ],
            pdf_top_left_content="Good",
            pdf_top_right_content="Morning",
            show_filters=False,
        ),
        visualization_object="f7c359bc-c230-4487-b15b-ad9685bcb537",
        visualization_object_custom_filters=[
            {},
        ],
    ) # TabularExportRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Create tabular export request
        api_response = api_instance.create_tabular_export(workspace_id, tabular_export_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.dashboard_permissions import DashboardPermissions
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    dashboard_id = "dashboardId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get Dashboard Permissions
        api_response = api_instance.dashboard_permissions(workspace_id, dashboard_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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

# **explain_afm**
> explain_afm(workspace_id, afm_execution)

AFM explain resource.

The resource provides static structures needed for investigation of a problem with given AFM.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.afm_execution import AfmExecution
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    afm_execution = AfmExecution(
        execution=AFM(
            attributes=[
                AttributeItem(
                    label=AfmObjectIdentifierLabel(
                        identifier=AfmObjectIdentifierLabelIdentifier(
                            id="sample_item.price",
                            type="label",
                        ),
                    ),
                    local_identifier="attribute_1",
                    show_all_values=False,
                ),
            ],
            aux_measures=[
                MeasureItem(
                    definition=MeasureDefinition(),
                    local_identifier="metric_1",
                ),
            ],
            filters=[
                FilterDefinition(),
            ],
            measures=[
                MeasureItem(
                    definition=MeasureDefinition(),
                    local_identifier="metric_1",
                ),
            ],
        ),
        result_spec=ResultSpec(
            dimensions=[
                Dimension(
                    item_identifiers=["attribute_1","measureGroup"],
                    local_identifier="firstDimension",
                    sorting=[
                        SortKey(),
                    ],
                ),
            ],
            totals=[
                Total(
                    function="SUM",
                    local_identifier="firstTotal",
                    metric="metric_1",
                    total_dimensions=[
                        TotalDimension(
                            dimension_identifier="firstDimension",
                            total_dimension_items=["measureGroup"],
                        ),
                    ],
                ),
            ],
        ),
        settings=ExecutionSettings(
            data_sampling_percentage=0,
            timestamp=dateutil_parser('1970-01-01T00:00:00.00Z'),
        ),
    ) # AfmExecution | 
    explain_type = "MAQL" # str | Requested explain type. If not specified all types are bundled in a ZIP archive.  `MAQL` - MAQL Abstract Syntax Tree, execution dimensions and related info  `GRPC_MODEL` - Datasets used in execution  `GRPC_MODEL_SVG` - Generated SVG image of the datasets  `WDF` - Workspace data filters in execution workspace context  `QT` - Query Tree, created from MAQL AST using Logical Data Model,  contains all information needed to generate SQL  `QT_SVG` - Generated SVG image of the Query Tree  `OPT_QT` - Optimized Query Tree  `OPT_QT_SVG` - Generated SVG image of the Optimized Query Tree  `SQL` - Final SQL to be executed  `SETTINGS` - Settings used to execute explain request (optional)

    # example passing only required values which don't have defaults set
    try:
        # AFM explain resource.
        api_instance.explain_afm(workspace_id, afm_execution)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->explain_afm: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # AFM explain resource.
        api_instance.explain_afm(workspace_id, afm_execution, explain_type=explain_type)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->explain_afm: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **afm_execution** | [**AfmExecution**](AfmExecution.md)|  |
 **explain_type** | **str**| Requested explain type. If not specified all types are bundled in a ZIP archive.  &#x60;MAQL&#x60; - MAQL Abstract Syntax Tree, execution dimensions and related info  &#x60;GRPC_MODEL&#x60; - Datasets used in execution  &#x60;GRPC_MODEL_SVG&#x60; - Generated SVG image of the datasets  &#x60;WDF&#x60; - Workspace data filters in execution workspace context  &#x60;QT&#x60; - Query Tree, created from MAQL AST using Logical Data Model,  contains all information needed to generate SQL  &#x60;QT_SVG&#x60; - Generated SVG image of the Query Tree  &#x60;OPT_QT&#x60; - Optimized Query Tree  &#x60;OPT_QT_SVG&#x60; - Generated SVG image of the Optimized Query Tree  &#x60;SQL&#x60; - Final SQL to be executed  &#x60;SETTINGS&#x60; - Settings used to execute explain request | [optional]

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
> SmartFunctionResponse forecast(workspace_id, result_id, forecast_request)

(BETA) Smart functions - Forecast

(BETA) Computes forecasted data points from the provided execution result and parameters.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.forecast_request import ForecastRequest
from gooddata_api_client.model.smart_function_response import SmartFunctionResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    result_id = "9bd52018570364264fcf62d373da6bed313120e8" # str | Input result ID to be used in the computation
    forecast_request = ForecastRequest(
        confidence_level=0.95,
        forecast_period=1,
        seasonal=False,
    ) # ForecastRequest | 
    skip_cache = False # bool | Ignore all caches during execution of current request. (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Smart functions - Forecast
        api_response = api_instance.forecast(workspace_id, result_id, forecast_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->forecast: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) Smart functions - Forecast
        api_response = api_instance.forecast(workspace_id, result_id, forecast_request, skip_cache=skip_cache)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->forecast: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **result_id** | **str**| Input result ID to be used in the computation |
 **forecast_request** | [**ForecastRequest**](ForecastRequest.md)|  |
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional] if omitted the server will use the default value of False

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
> ForecastResult forecast_result(workspace_id, result_id)

(BETA) Smart functions - Forecast Result

(BETA) Gets forecast result.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.forecast_result import ForecastResult
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    result_id = "a9b28f9dc55f37ea9f4a5fb0c76895923591e781" # str | Result ID
    offset = 1 # int |  (optional)
    limit = 1 # int |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Smart functions - Forecast Result
        api_response = api_instance.forecast_result(workspace_id, result_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->forecast_result: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) Smart functions - Forecast Result
        api_response = api_instance.forecast_result(workspace_id, result_id, offset=offset, limit=limit)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.declarative_model import DeclarativeModel
from gooddata_api_client.model.generate_ldm_request import GenerateLdmRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    data_source_id = "dataSourceId_example" # str | 
    generate_ldm_request = GenerateLdmRequest(
        date_granularities="all",
        denorm_prefix="dr",
        fact_prefix="f",
        generate_long_ids=False,
        grain_multivalue_reference_prefix="grmr",
        grain_prefix="gr",
        grain_reference_prefix="grr",
        multivalue_reference_prefix="mr",
        pdm=PdmLdmRequest(
            sqls=[
                PdmSql(
                    columns=[
                        SqlColumn(
                            data_type="INT",
                            name="customer_id",
                        ),
                    ],
                    statement="select * from abc",
                    title="My special dataset",
                ),
            ],
            table_overrides=[
                TableOverride(
                    columns=[
                        ColumnOverride(
                            label_target_column="users",
                            label_type="HYPERLINK",
                            ldm_type_override="FACT",
                            name="column_name",
                        ),
                    ],
                    path=["schema","table_name"],
                ),
            ],
            tables=[
                DeclarativeTable(
                    columns=[
                        DeclarativeColumn(
                            data_type="INT",
                            is_primary_key=True,
                            name="customer_id",
                            referenced_table_column="customer_id",
                            referenced_table_id="customers",
                        ),
                    ],
                    id="customers",
                    name_prefix="out_gooddata",
                    path=["table_schema","table_name"],
                    type="TABLE",
                ),
            ],
        ),
        primary_label_prefix="pl",
        reference_prefix="r",
        secondary_label_prefix="ls",
        separator="__",
        table_prefix="out_table",
        view_prefix="out_view",
        wdf_prefix="wdf",
        workspace_id="workspace_id_example",
    ) # GenerateLdmRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Generate logical data model (LDM) from physical data model (PDM)
        api_response = api_instance.generate_logical_model(data_source_id, generate_ldm_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.data_source_schemata import DataSourceSchemata
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    data_source_id = "myPostgres" # str | Data source id

    # example passing only required values which don't have defaults set
    try:
        # Get a list of schema names of a database
        api_response = api_instance.get_data_source_schemata(data_source_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.dependent_entities_response import DependentEntitiesResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Computes the dependent entities graph
        api_response = api_instance.get_dependent_entities_graph(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.dependent_entities_request import DependentEntitiesRequest
from gooddata_api_client.model.dependent_entities_response import DependentEntitiesResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    dependent_entities_request = DependentEntitiesRequest(
        identifiers=[
            EntityIdentifier(
                id="/6bUUGjjNSwg0_bs",
                type="metric",
            ),
        ],
    ) # DependentEntitiesRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Computes the dependent entities graph from given entry points
        api_response = api_instance.get_dependent_entities_graph_from_entry_points(workspace_id, dependent_entities_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
> get_exported_file(workspace_id, export_id)

Retrieve exported files

Returns 202 until original POST export request is not processed.Returns 200 with exported data once the export is done.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    export_id = "exportId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Retrieve exported files
        api_instance.get_exported_file(workspace_id, export_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->get_exported_file: %s\n" % e)
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
 - **Accept**: application/pdf


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Binary export result. |  * Content-Disposition -  <br>  |
**202** | Request is accepted, provided exportId exists, but export is not yet ready. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_image_export**
> get_image_export(workspace_id, export_id)

(EXPERIMENTAL) Retrieve exported files

Note: This API is an experimental and is going to change. Please, use it accordingly. After clients creates a POST export request, the processing of it will start shortly asynchronously. To retrieve the result, client has to check periodically for the result on this endpoint. In case the result isn't ready yet, the service returns 202. If the result is ready, it returns 200 and octet stream of the result file with provided filename.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.get_image_export202_response_inner import GetImageExport202ResponseInner
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    export_id = "exportId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Retrieve exported files
        api_instance.get_image_export(workspace_id, export_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->get_image_export: %s\n" % e)
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    export_id = "exportId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Retrieve metadata context
        api_instance.get_image_export_metadata(workspace_id, export_id)
    except gooddata_api_client.ApiException as e:
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

# **get_metadata**
> get_metadata(workspace_id, export_id)

Retrieve metadata context

This endpoint serves as a cache for user-defined metadata of the export for the front end UI to retrieve it, if one was created using the POST ../export/visual endpoint. The metadata structure is not verified.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    export_id = "exportId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Retrieve metadata context
        api_instance.get_metadata(workspace_id, export_id)
    except gooddata_api_client.ApiException as e:
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
> Notifications get_notifications()

Get latest notifications.

Get latest in-platform notifications for the current user.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.notifications import Notifications
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | Workspace ID to filter notifications by. (optional)
    is_read = True # bool | Filter notifications by read status. (optional)
    page = "0" # str | Zero-based page index (0..N) (optional) if omitted the server will use the default value of "0"
    size = "20" # str | The size of the page to be returned. (optional) if omitted the server will use the default value of "20"
    meta_include = [
        "total",
    ] # [str] | Additional meta information to include in the response. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get latest notifications.
        api_response = api_instance.get_notifications(workspace_id=workspace_id, is_read=is_read, page=page, size=size, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->get_notifications: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace ID to filter notifications by. | [optional]
 **is_read** | **bool**| Filter notifications by read status. | [optional]
 **page** | **str**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of "0"
 **size** | **str**| The size of the page to be returned. | [optional] if omitted the server will use the default value of "20"
 **meta_include** | **[str]**| Additional meta information to include in the response. | [optional]

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

# **get_raw_export**
> get_raw_export(workspace_id, export_id)

(EXPERIMENTAL) Retrieve exported files

Note: This API is an experimental and is going to change. Please, use it accordingly.After clients creates a POST export request, the processing of it will start shortly asynchronously. To retrieve the result, client has to check periodically for the result on this endpoint. In case the result isn't ready yet, the service returns 202. If the result is ready, it returns 200 and octet stream of the result file with provided filename.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    export_id = "exportId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Retrieve exported files
        api_instance.get_raw_export(workspace_id, export_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->get_raw_export: %s\n" % e)
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
 - **Accept**: application/vnd.apache.arrow.file, application/vnd.apache.arrow.stream, text/csv


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Binary export result. |  * Content-Disposition -  <br>  |
**202** | Request is accepted, provided exportId exists, but export is not yet ready. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_slides_export**
> get_slides_export(workspace_id, export_id)

(EXPERIMENTAL) Retrieve exported files

Note: This API is an experimental and is going to change. Please, use it accordingly. After clients creates a POST export request, the processing of it will start shortly asynchronously. To retrieve the result, client has to check periodically for the result on this endpoint. In case the result isn't ready yet, the service returns 202. If the result is ready, it returns 200 and octet stream of the result file with provided filename.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.get_image_export202_response_inner import GetImageExport202ResponseInner
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    export_id = "exportId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Retrieve exported files
        api_instance.get_slides_export(workspace_id, export_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->get_slides_export: %s\n" % e)
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    export_id = "exportId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Retrieve metadata context
        api_instance.get_slides_export_metadata(workspace_id, export_id)
    except gooddata_api_client.ApiException as e:
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
> get_tabular_export(workspace_id, export_id)

Retrieve exported files

After clients creates a POST export request, the processing of it will start shortly asynchronously. To retrieve the result, client has to check periodically for the result on this endpoint. In case the result isn't ready yet, the service returns 202. If the result is ready, it returns 200 and octet stream of the result file with provided filename.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    export_id = "exportId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Retrieve exported files
        api_instance.get_tabular_export(workspace_id, export_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->get_tabular_export: %s\n" % e)
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
 - **Accept**: application/pdf, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, text/csv, text/html


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Binary export result. |  * Content-Disposition -  <br>  |
**202** | Request is accepted, provided exportId exists, but export is not yet ready. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_translation_tags**
> [str] get_translation_tags(workspace_id)

Get translation tags.

Provides a list of effective translation tags.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get translation tags.
        api_response = api_instance.get_translation_tags(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->get_translation_tags: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |

### Return type

**[str]**

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
> [IdentifierDuplications] inherited_entity_conflicts(workspace_id)

Finds identifier conflicts in workspace hierarchy.

Finds API identifier conflicts in given workspace hierarchy.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.identifier_duplications import IdentifierDuplications
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Finds identifier conflicts in workspace hierarchy.
        api_response = api_instance.inherited_entity_conflicts(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->inherited_entity_conflicts: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |

### Return type

[**[IdentifierDuplications]**](IdentifierDuplications.md)

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
> [str] inherited_entity_prefixes(workspace_id)

Get used entity prefixes in hierarchy

Get used entity prefixes in hierarchy of parent workspaces

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get used entity prefixes in hierarchy
        api_response = api_instance.inherited_entity_prefixes(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->inherited_entity_prefixes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |

### Return type

**[str]**

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
> KeyDriversResponse key_driver_analysis(workspace_id, key_drivers_request)

(EXPERIMENTAL) Compute key driver analysis

(EXPERIMENTAL) Computes key driver analysis for the provided execution definition.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.key_drivers_response import KeyDriversResponse
from gooddata_api_client.model.key_drivers_request import KeyDriversRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    key_drivers_request = KeyDriversRequest(
        aux_metrics=[
            MeasureItem(
                definition=MeasureDefinition(),
                local_identifier="metric_1",
            ),
        ],
        metric=MeasureItem(
            definition=MeasureDefinition(),
            local_identifier="metric_1",
        ),
        sort_direction="DESC",
    ) # KeyDriversRequest | 
    skip_cache = False # bool | Ignore all caches during execution of current request. (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Compute key driver analysis
        api_response = api_instance.key_driver_analysis(workspace_id, key_drivers_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->key_driver_analysis: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (EXPERIMENTAL) Compute key driver analysis
        api_response = api_instance.key_driver_analysis(workspace_id, key_drivers_request, skip_cache=skip_cache)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->key_driver_analysis: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **key_drivers_request** | [**KeyDriversRequest**](KeyDriversRequest.md)|  |
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional] if omitted the server will use the default value of False

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
> KeyDriversResult key_driver_analysis_result(workspace_id, result_id)

(EXPERIMENTAL) Get key driver analysis result

(EXPERIMENTAL) Gets key driver analysis.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.key_drivers_result import KeyDriversResult
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    result_id = "a9b28f9dc55f37ea9f4a5fb0c76895923591e781" # str | Result ID
    offset = 1 # int |  (optional)
    limit = 1 # int |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Get key driver analysis result
        api_response = api_instance.key_driver_analysis_result(workspace_id, result_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->key_driver_analysis_result: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (EXPERIMENTAL) Get key driver analysis result
        api_response = api_instance.key_driver_analysis_result(workspace_id, result_id, offset=offset, limit=limit)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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

# **list_workspace_user_groups**
> WorkspaceUserGroups list_workspace_user_groups(workspace_id)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.workspace_user_groups import WorkspaceUserGroups
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    page = page=0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = size=20 # int | The size of the page to be returned. (optional) if omitted the server will use the default value of 20
    name = "name=charles" # str | Filter by user name. Note that user name is case insensitive. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.list_workspace_user_groups(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->list_workspace_user_groups: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.list_workspace_user_groups(workspace_id, page=page, size=size, name=name)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->list_workspace_user_groups: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned. | [optional] if omitted the server will use the default value of 20
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
> WorkspaceUsers list_workspace_users(workspace_id)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.workspace_users import WorkspaceUsers
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    page = page=0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = size=20 # int | The size of the page to be returned. (optional) if omitted the server will use the default value of 20
    name = "name=charles" # str | Filter by user name. Note that user name is case insensitive. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.list_workspace_users(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->list_workspace_users: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.list_workspace_users(workspace_id, page=page, size=size, name=name)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->list_workspace_users: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned. | [optional] if omitted the server will use the default value of 20
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.manage_dashboard_permissions_request_inner import ManageDashboardPermissionsRequestInner
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    dashboard_id = "dashboardId_example" # str | 
    manage_dashboard_permissions_request_inner = [
        ManageDashboardPermissionsRequestInner(None),
    ] # [ManageDashboardPermissionsRequestInner] | 

    # example passing only required values which don't have defaults set
    try:
        # Manage Permissions for a Dashboard
        api_instance.manage_dashboard_permissions(workspace_id, dashboard_id, manage_dashboard_permissions_request_inner)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->manage_dashboard_permissions: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **dashboard_id** | **str**|  |
 **manage_dashboard_permissions_request_inner** | [**[ManageDashboardPermissionsRequestInner]**](ManageDashboardPermissionsRequestInner.md)|  |

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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.data_source_permission_assignment import DataSourcePermissionAssignment
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    data_source_id = "dataSourceId_example" # str | 
    data_source_permission_assignment = [
        DataSourcePermissionAssignment(
            assignee_identifier=AssigneeIdentifier(
                id="id_example",
                type="user",
            ),
            permissions=[
                "MANAGE",
            ],
        ),
    ] # [DataSourcePermissionAssignment] | 

    # example passing only required values which don't have defaults set
    try:
        # Manage Permissions for a Data Source
        api_instance.manage_data_source_permissions(data_source_id, data_source_permission_assignment)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->manage_data_source_permissions: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  |
 **data_source_permission_assignment** | [**[DataSourcePermissionAssignment]**](DataSourcePermissionAssignment.md)|  |

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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.organization_permission_assignment import OrganizationPermissionAssignment
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    organization_permission_assignment = [
        OrganizationPermissionAssignment(
            assignee_identifier=AssigneeIdentifier(
                id="id_example",
                type="user",
            ),
            permissions=[
                "MANAGE",
            ],
        ),
    ] # [OrganizationPermissionAssignment] | 

    # example passing only required values which don't have defaults set
    try:
        # Manage Permissions for a Organization
        api_instance.manage_organization_permissions(organization_permission_assignment)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->manage_organization_permissions: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_permission_assignment** | [**[OrganizationPermissionAssignment]**](OrganizationPermissionAssignment.md)|  |

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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.workspace_permission_assignment import WorkspacePermissionAssignment
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    workspace_permission_assignment = [
        WorkspacePermissionAssignment(
            assignee_identifier=AssigneeIdentifier(
                id="id_example",
                type="user",
            ),
            hierarchy_permissions=[
                "MANAGE",
            ],
            permissions=[
                "MANAGE",
            ],
        ),
    ] # [WorkspacePermissionAssignment] | 

    # example passing only required values which don't have defaults set
    try:
        # Manage Permissions for a Workspace
        api_instance.manage_workspace_permissions(workspace_id, workspace_permission_assignment)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->manage_workspace_permissions: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **workspace_permission_assignment** | [**[WorkspacePermissionAssignment]**](WorkspacePermissionAssignment.md)|  |

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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    notification_id = "notificationId_example" # str | Notification ID to mark as read.

    # example passing only required values which don't have defaults set
    try:
        # Mark notification as read.
        api_instance.mark_as_read_notification(notification_id)
    except gooddata_api_client.ApiException as e:
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
> mark_as_read_notification_all()

Mark all notifications as read.

Mark all user in-platform notifications as read.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | Workspace ID where to mark notifications as read. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Mark all notifications as read.
        api_instance.mark_as_read_notification_all(workspace_id=workspace_id)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Sync Metadata to other services
        api_instance.metadata_sync(workspace_id)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # (BETA) Sync organization scope Metadata to other services
        api_instance.metadata_sync_organization()
    except gooddata_api_client.ApiException as e:
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
> [IdentifierDuplications] overridden_child_entities(workspace_id)

Finds identifier overrides in workspace hierarchy.

Finds API identifier overrides in given workspace hierarchy.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.identifier_duplications import IdentifierDuplications
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Finds identifier overrides in workspace hierarchy.
        api_response = api_instance.overridden_child_entities(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->overridden_child_entities: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |

### Return type

[**[IdentifierDuplications]**](IdentifierDuplications.md)

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
> [PlatformUsage] particular_platform_usage(platform_usage_request)

Info about the platform usage for particular items.

Provides information about platform usage, like amount of users, workspaces, ...  _NOTE_: The `admin` user is always excluded from this amount.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.platform_usage_request import PlatformUsageRequest
from gooddata_api_client.model.platform_usage import PlatformUsage
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    platform_usage_request = PlatformUsageRequest(
        usage_item_names=[
            "UserCount",
        ],
    ) # PlatformUsageRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Info about the platform usage for particular items.
        api_response = api_instance.particular_platform_usage(platform_usage_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->particular_platform_usage: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **platform_usage_request** | [**PlatformUsageRequest**](PlatformUsageRequest.md)|  |

### Return type

[**[PlatformUsage]**](PlatformUsage.md)

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

# **register_upload_notification**
> register_upload_notification(data_source_id)

Register an upload notification

Notification sets up all reports to be computed again with new data.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    data_source_id = "dataSourceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Register an upload notification
        api_instance.register_upload_notification(data_source_id)
    except gooddata_api_client.ApiException as e:
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

# **resolve_all_entitlements**
> [ApiEntitlement] resolve_all_entitlements()

Values for all public entitlements.

Resolves values of available entitlements for the organization.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.api_entitlement import ApiEntitlement
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Values for all public entitlements.
        api_response = api_instance.resolve_all_entitlements()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->resolve_all_entitlements: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**[ApiEntitlement]**](ApiEntitlement.md)

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
> [ResolvedSetting] resolve_all_settings_without_workspace()

Values for all settings without workspace.

Resolves values for all settings without workspace by current user, organization, or default settings.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.resolved_setting import ResolvedSetting
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Values for all settings without workspace.
        api_response = api_instance.resolve_all_settings_without_workspace()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->resolve_all_settings_without_workspace: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**[ResolvedSetting]**](ResolvedSetting.md)

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

# **resolve_requested_entitlements**
> [ApiEntitlement] resolve_requested_entitlements(entitlements_request)

Values for requested public entitlements.

Resolves values for requested entitlements in the organization.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.api_entitlement import ApiEntitlement
from gooddata_api_client.model.entitlements_request import EntitlementsRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    entitlements_request = EntitlementsRequest(
        entitlements_name=[
            "CacheStrategy",
        ],
    ) # EntitlementsRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Values for requested public entitlements.
        api_response = api_instance.resolve_requested_entitlements(entitlements_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->resolve_requested_entitlements: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entitlements_request** | [**EntitlementsRequest**](EntitlementsRequest.md)|  |

### Return type

[**[ApiEntitlement]**](ApiEntitlement.md)

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
> [ResolvedSetting] resolve_settings_without_workspace(resolve_settings_request)

Values for selected settings without workspace.

Resolves values for selected settings without workspace by current user, organization, or default settings.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.resolved_setting import ResolvedSetting
from gooddata_api_client.model.resolve_settings_request import ResolveSettingsRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    resolve_settings_request = ResolveSettingsRequest(
        settings=["timezone"],
    ) # ResolveSettingsRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Values for selected settings without workspace.
        api_response = api_instance.resolve_settings_without_workspace(resolve_settings_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->resolve_settings_without_workspace: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resolve_settings_request** | [**ResolveSettingsRequest**](ResolveSettingsRequest.md)|  |

### Return type

[**[ResolvedSetting]**](ResolvedSetting.md)

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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.result_cache_metadata import ResultCacheMetadata
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    result_id = "a9b28f9dc55f37ea9f4a5fb0c76895923591e781" # str | Result ID

    # example passing only required values which don't have defaults set
    try:
        # Get a single execution result's metadata.
        api_response = api_instance.retrieve_execution_metadata(workspace_id, result_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
> ExecutionResult retrieve_result(workspace_id, result_id)

Get a single execution result

Gets a single execution result.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.execution_result import ExecutionResult
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    result_id = "a9b28f9dc55f37ea9f4a5fb0c76895923591e781" # str | Result ID
    offset = [
        offset=1,10,
    ] # [int] | Request page with these offsets. Format is offset=1,2,3,... - one offset for each dimensions in ResultSpec from originating AFM. (optional) if omitted the server will use the default value of []
    limit = [
        limit=1,10,
    ] # [int] | Return only this number of items. Format is limit=1,2,3,... - one limit for each dimensions in ResultSpec from originating AFM. (optional) if omitted the server will use the default value of []
    excluded_total_dimensions = [
        "excludedTotalDimensions=dim_0,dim_1",
    ] # [str] | Identifiers of the dimensions where grand total data should not be returned for this request. A grand total will not be returned if all of its totalDimensions are in excludedTotalDimensions. (optional) if omitted the server will use the default value of []
    x_gdc_cancel_token = "X-GDC-CANCEL-TOKEN_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a single execution result
        api_response = api_instance.retrieve_result(workspace_id, result_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->retrieve_result: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a single execution result
        api_response = api_instance.retrieve_result(workspace_id, result_id, offset=offset, limit=limit, excluded_total_dimensions=excluded_total_dimensions, x_gdc_cancel_token=x_gdc_cancel_token)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->retrieve_result: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **result_id** | **str**| Result ID |
 **offset** | **[int]**| Request page with these offsets. Format is offset&#x3D;1,2,3,... - one offset for each dimensions in ResultSpec from originating AFM. | [optional] if omitted the server will use the default value of []
 **limit** | **[int]**| Return only this number of items. Format is limit&#x3D;1,2,3,... - one limit for each dimensions in ResultSpec from originating AFM. | [optional] if omitted the server will use the default value of []
 **excluded_total_dimensions** | **[str]**| Identifiers of the dimensions where grand total data should not be returned for this request. A grand total will not be returned if all of its totalDimensions are in excludedTotalDimensions. | [optional] if omitted the server will use the default value of []
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.locale_request import LocaleRequest
from gooddata_api_client.model.xliff import Xliff
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    locale_request = LocaleRequest(
        locale="en-US",
    ) # LocaleRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Retrieve translations for entities.
        api_response = api_instance.retrieve_translations(workspace_id, locale_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.scan_request import ScanRequest
from gooddata_api_client.model.scan_result_pdm import ScanResultPdm
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    data_source_id = "myPostgres" # str | Data source id
    scan_request = ScanRequest(
        scan_tables=True,
        scan_views=True,
        schemata=["tpch","demo"],
        separator="__",
        table_prefix="out_table",
        view_prefix="out_view",
    ) # ScanRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Scan a database to get a physical data model (PDM)
        api_response = api_instance.scan_data_source(data_source_id, scan_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.scan_sql_response import ScanSqlResponse
from gooddata_api_client.model.scan_sql_request import ScanSqlRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    data_source_id = "myPostgres" # str | Data source id
    scan_sql_request = ScanSqlRequest(
        sql="SELECT a.special_value as result FROM tableA a",
    ) # ScanSqlRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Collect metadata about SQL query
        api_response = api_instance.scan_sql(data_source_id, scan_sql_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.xliff import Xliff
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    xliff = Xliff(
        file=[
            File(
                any=[
                    {},
                ],
                can_resegment="YES",
                id="id_example",
                notes=Notes(
                    note=[
                        Note(
                            applies_to="SOURCE",
                            category="category_example",
                            content="content_example",
                            id="id_example",
                            other_attributes={
                                "key": "key_example",
                            },
                            priority=1,
                        ),
                    ],
                ),
                original="original_example",
                other_attributes={
                    "key": "key_example",
                },
                skeleton=Skeleton(
                    content=[
                        {},
                    ],
                    href="href_example",
                ),
                space="space_example",
                src_dir="LTR",
                translate="YES",
                trg_dir="LTR",
                unit_or_group=[
                    {},
                ],
            ),
        ],
        other_attributes={
            "key": "key_example",
        },
        space="space_example",
        src_lang="src_lang_example",
        trg_lang="trg_lang_example",
        version="version_example",
    ) # Xliff | 

    # example passing only required values which don't have defaults set
    try:
        # Set translations for entities.
        api_instance.set_translations(workspace_id, xliff)
    except gooddata_api_client.ApiException as e:
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

# **test_data_source**
> TestResponse test_data_source(data_source_id, test_request)

Test data source connection by data source id

Test if it is possible to connect to a database using an existing data source definition.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.test_response import TestResponse
from gooddata_api_client.model.test_request import TestRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    data_source_id = "myPostgres" # str | Data source id
    test_request = TestRequest(
        client_id="client_id_example",
        client_secret="client_secret_example",
        parameters=[
            DataSourceParameter(
                name="name_example",
                value="value_example",
            ),
        ],
        password="admin123",
        private_key="private_key_example",
        private_key_passphrase="private_key_passphrase_example",
        schema="public",
        token="token_example",
        url="jdbc:postgresql://localhost:5432/db_name",
        username="dbadmin",
    ) # TestRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Test data source connection by data source id
        api_response = api_instance.test_data_source(data_source_id, test_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.test_response import TestResponse
from gooddata_api_client.model.test_definition_request import TestDefinitionRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    test_definition_request = TestDefinitionRequest(
        client_id="client_id_example",
        client_secret="client_secret_example",
        parameters=[
            DataSourceParameter(
                name="name_example",
                value="value_example",
            ),
        ],
        password="admin123",
        private_key="private_key_example",
        private_key_passphrase="private_key_passphrase_example",
        schema="public",
        token="token_example",
        type="POSTGRESQL",
        url="jdbc:postgresql://localhost:5432/db_name",
        username="dbadmin",
    ) # TestDefinitionRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Test connection by data source definition
        api_response = api_instance.test_data_source_definition(test_definition_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
> TestResponse test_existing_notification_channel(notification_channel_id)

Test existing notification channel.

Tests the existing notification channel by sending a test notification.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.test_response import TestResponse
from gooddata_api_client.model.test_destination_request import TestDestinationRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    notification_channel_id = "notificationChannelId_example" # str | 
    test_destination_request = TestDestinationRequest(
        destination=DeclarativeNotificationChannelDestination(None),
    ) # TestDestinationRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Test existing notification channel.
        api_response = api_instance.test_existing_notification_channel(notification_channel_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->test_existing_notification_channel: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Test existing notification channel.
        api_response = api_instance.test_existing_notification_channel(notification_channel_id, test_destination_request=test_destination_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.test_response import TestResponse
from gooddata_api_client.model.test_destination_request import TestDestinationRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    test_destination_request = TestDestinationRequest(
        destination=DeclarativeNotificationChannelDestination(None),
    ) # TestDestinationRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Test notification channel.
        api_response = api_instance.test_notification_channel(test_destination_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.trigger_automation_request import TriggerAutomationRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    trigger_automation_request = TriggerAutomationRequest(
        automation=AdHocAutomation(
            alert=AutomationAlert(
                condition=AutomationAlertCondition(None),
                execution=AlertAfm(
                    attributes=[
                        AttributeItem(
                            label=AfmObjectIdentifierLabel(
                                identifier=AfmObjectIdentifierLabelIdentifier(
                                    id="sample_item.price",
                                    type="label",
                                ),
                            ),
                            local_identifier="attribute_1",
                            show_all_values=False,
                        ),
                    ],
                    aux_measures=[
                        MeasureItem(
                            definition=MeasureDefinition(),
                            local_identifier="metric_1",
                        ),
                    ],
                    filters=[
                        FilterDefinition(),
                    ],
                    measures=[
                        MeasureItem(
                            definition=MeasureDefinition(),
                            local_identifier="metric_1",
                        ),
                    ],
                ),
                trigger="ALWAYS",
            ),
            analytical_dashboard=DeclarativeAnalyticalDashboardIdentifier(
                id="dashboard123",
                type="analyticalDashboard",
            ),
            description="description_example",
            details={
                "key": "key_example",
            },
            external_recipients=[
                AutomationExternalRecipient(
                    email="email_example",
                ),
            ],
            image_exports=[
                AutomationImageExport(
                    request_payload=ImageExportRequest(
                        dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                        file_name="filename",
                        format="PNG",
                        metadata=JsonNode(),
                        widget_ids=[
                            "widget_ids_example",
                        ],
                    ),
                ),
            ],
            metadata=AutomationMetadata(
                visible_filters=[
                    VisibleFilter(
                        is_all_time_date_filter=False,
                        local_identifier="local_identifier_example",
                        title="title_example",
                    ),
                ],
                widget="widget_example",
            ),
            notification_channel=DeclarativeNotificationChannelIdentifier(
                id="webhook123",
                type="notificationChannel",
            ),
            recipients=[
                DeclarativeUserIdentifier(
                    id="employee123",
                    type="user",
                ),
            ],
            tabular_exports=[
                AutomationTabularExport(
                    request_payload=TabularExportRequest(
                        custom_override=CustomOverride(
                            labels={
                                "key": CustomLabel(
                                    title="title_example",
                                ),
                            },
                            metrics={
                                "key": CustomMetric(
                                    format="format_example",
                                    title="title_example",
                                ),
                            },
                        ),
                        execution_result="ff483727196c9dc862c7fd3a5a84df55c96d61a4",
                        file_name="result",
                        format="CSV",
                        metadata=JsonNode(),
                        related_dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                        settings=Settings(
                            merge_headers=True,
                            pdf_page_size="a4 landscape",
                            pdf_table_style=[
                                PdfTableStyle(
                                    properties=[
                                        PdfTableStyleProperty(
                                            key="key_example",
                                            value="value_example",
                                        ),
                                    ],
                                    selector="selector_example",
                                ),
                            ],
                            pdf_top_left_content="Good",
                            pdf_top_right_content="Morning",
                            show_filters=False,
                        ),
                        visualization_object="f7c359bc-c230-4487-b15b-ad9685bcb537",
                        visualization_object_custom_filters=[
                            {},
                        ],
                    ),
                ),
            ],
            tags=["Revenue","Sales"],
            title="title_example",
            visual_exports=[
                AutomationVisualExport(
                    request_payload=VisualExportRequest(
                        dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                        file_name="filename",
                        metadata={},
                    ),
                ),
            ],
        ),
    ) # TriggerAutomationRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Trigger automation.
        api_instance.trigger_automation(workspace_id, trigger_automation_request)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    automation_id = "automationId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Trigger existing automation.
        api_instance.trigger_existing_automation(workspace_id, automation_id)
    except gooddata_api_client.ApiException as e:
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

# **unsubscribe_all_automations**
> unsubscribe_all_automations()

Unsubscribe from all automations in all workspaces

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Unsubscribe from all automations in all workspaces
        api_instance.unsubscribe_all_automations()
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    automation_id = "automationId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Unsubscribe from an automation
        api_instance.unsubscribe_automation(workspace_id, automation_id)
    except gooddata_api_client.ApiException as e:
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

# **unsubscribe_workspace_automations**
> unsubscribe_workspace_automations(workspace_id)

Unsubscribe from all automations in the workspace

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Unsubscribe from all automations in the workspace
        api_instance.unsubscribe_workspace_automations(workspace_id)
    except gooddata_api_client.ApiException as e:
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

# **workspace_resolve_all_settings**
> [ResolvedSetting] workspace_resolve_all_settings(workspace_id)

Values for all settings.

Resolves values for all settings in a workspace by current user, workspace, organization, or default settings.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.resolved_setting import ResolvedSetting
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Values for all settings.
        api_response = api_instance.workspace_resolve_all_settings(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->workspace_resolve_all_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |

### Return type

[**[ResolvedSetting]**](ResolvedSetting.md)

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
> [ResolvedSetting] workspace_resolve_settings(workspace_id, resolve_settings_request)

Values for selected settings.

Resolves value for selected settings in a workspace by current user, workspace, organization, or default settings.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.resolved_setting import ResolvedSetting
from gooddata_api_client.model.resolve_settings_request import ResolveSettingsRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    resolve_settings_request = ResolveSettingsRequest(
        settings=["timezone"],
    ) # ResolveSettingsRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Values for selected settings.
        api_response = api_instance.workspace_resolve_settings(workspace_id, resolve_settings_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->workspace_resolve_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **resolve_settings_request** | [**ResolveSettingsRequest**](ResolveSettingsRequest.md)|  |

### Return type

[**[ResolvedSetting]**](ResolvedSetting.md)

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


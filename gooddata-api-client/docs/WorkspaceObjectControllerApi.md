# gooddata_api_client.WorkspaceObjectControllerApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_analytical_dashboards**](WorkspaceObjectControllerApi.md#create_entity_analytical_dashboards) | **POST** /api/v1/entities/workspaces/{workspaceId}/analyticalDashboards | Post Dashboards
[**create_entity_custom_application_settings**](WorkspaceObjectControllerApi.md#create_entity_custom_application_settings) | **POST** /api/v1/entities/workspaces/{workspaceId}/customApplicationSettings | Post Custom Application Settings
[**create_entity_dashboard_plugins**](WorkspaceObjectControllerApi.md#create_entity_dashboard_plugins) | **POST** /api/v1/entities/workspaces/{workspaceId}/dashboardPlugins | Post Plugins
[**create_entity_filter_contexts**](WorkspaceObjectControllerApi.md#create_entity_filter_contexts) | **POST** /api/v1/entities/workspaces/{workspaceId}/filterContexts | Post Context Filters
[**create_entity_metrics**](WorkspaceObjectControllerApi.md#create_entity_metrics) | **POST** /api/v1/entities/workspaces/{workspaceId}/metrics | Post Metrics
[**create_entity_user_data_filters**](WorkspaceObjectControllerApi.md#create_entity_user_data_filters) | **POST** /api/v1/entities/workspaces/{workspaceId}/userDataFilters | Post User Data Filters
[**create_entity_visualization_objects**](WorkspaceObjectControllerApi.md#create_entity_visualization_objects) | **POST** /api/v1/entities/workspaces/{workspaceId}/visualizationObjects | Post Visualization Objects
[**create_entity_workspace_data_filter_settings**](WorkspaceObjectControllerApi.md#create_entity_workspace_data_filter_settings) | **POST** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilterSettings | Post Settings for Workspace Data Filters
[**create_entity_workspace_data_filters**](WorkspaceObjectControllerApi.md#create_entity_workspace_data_filters) | **POST** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilters | Post Workspace Data Filters
[**create_entity_workspace_settings**](WorkspaceObjectControllerApi.md#create_entity_workspace_settings) | **POST** /api/v1/entities/workspaces/{workspaceId}/workspaceSettings | Post Settings for Workspaces
[**delete_entity_analytical_dashboards**](WorkspaceObjectControllerApi.md#delete_entity_analytical_dashboards) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/analyticalDashboards/{objectId} | Delete a Dashboard
[**delete_entity_custom_application_settings**](WorkspaceObjectControllerApi.md#delete_entity_custom_application_settings) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/customApplicationSettings/{objectId} | Delete a Custom Application Setting
[**delete_entity_dashboard_plugins**](WorkspaceObjectControllerApi.md#delete_entity_dashboard_plugins) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/dashboardPlugins/{objectId} | Delete a Plugin
[**delete_entity_filter_contexts**](WorkspaceObjectControllerApi.md#delete_entity_filter_contexts) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/filterContexts/{objectId} | Delete a Context Filter
[**delete_entity_metrics**](WorkspaceObjectControllerApi.md#delete_entity_metrics) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/metrics/{objectId} | Delete a Metric
[**delete_entity_user_data_filters**](WorkspaceObjectControllerApi.md#delete_entity_user_data_filters) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/userDataFilters/{objectId} | Delete a User Data Filter
[**delete_entity_visualization_objects**](WorkspaceObjectControllerApi.md#delete_entity_visualization_objects) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/visualizationObjects/{objectId} | Delete a Visualization Object
[**delete_entity_workspace_data_filter_settings**](WorkspaceObjectControllerApi.md#delete_entity_workspace_data_filter_settings) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilterSettings/{objectId} | Delete a Settings for Workspace Data Filter
[**delete_entity_workspace_data_filters**](WorkspaceObjectControllerApi.md#delete_entity_workspace_data_filters) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilters/{objectId} | Delete a Workspace Data Filter
[**delete_entity_workspace_settings**](WorkspaceObjectControllerApi.md#delete_entity_workspace_settings) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/workspaceSettings/{objectId} | Delete a Setting for Workspace
[**get_all_entities_analytical_dashboards**](WorkspaceObjectControllerApi.md#get_all_entities_analytical_dashboards) | **GET** /api/v1/entities/workspaces/{workspaceId}/analyticalDashboards | Get all Dashboards
[**get_all_entities_attributes**](WorkspaceObjectControllerApi.md#get_all_entities_attributes) | **GET** /api/v1/entities/workspaces/{workspaceId}/attributes | Get all Attributes
[**get_all_entities_custom_application_settings**](WorkspaceObjectControllerApi.md#get_all_entities_custom_application_settings) | **GET** /api/v1/entities/workspaces/{workspaceId}/customApplicationSettings | Get all Custom Application Settings
[**get_all_entities_dashboard_plugins**](WorkspaceObjectControllerApi.md#get_all_entities_dashboard_plugins) | **GET** /api/v1/entities/workspaces/{workspaceId}/dashboardPlugins | Get all Plugins
[**get_all_entities_datasets**](WorkspaceObjectControllerApi.md#get_all_entities_datasets) | **GET** /api/v1/entities/workspaces/{workspaceId}/datasets | Get all Datasets
[**get_all_entities_facts**](WorkspaceObjectControllerApi.md#get_all_entities_facts) | **GET** /api/v1/entities/workspaces/{workspaceId}/facts | Get all Facts
[**get_all_entities_filter_contexts**](WorkspaceObjectControllerApi.md#get_all_entities_filter_contexts) | **GET** /api/v1/entities/workspaces/{workspaceId}/filterContexts | Get all Context Filters
[**get_all_entities_labels**](WorkspaceObjectControllerApi.md#get_all_entities_labels) | **GET** /api/v1/entities/workspaces/{workspaceId}/labels | Get all Labels
[**get_all_entities_metrics**](WorkspaceObjectControllerApi.md#get_all_entities_metrics) | **GET** /api/v1/entities/workspaces/{workspaceId}/metrics | Get all Metrics
[**get_all_entities_user_data_filters**](WorkspaceObjectControllerApi.md#get_all_entities_user_data_filters) | **GET** /api/v1/entities/workspaces/{workspaceId}/userDataFilters | Get all User Data Filters
[**get_all_entities_visualization_objects**](WorkspaceObjectControllerApi.md#get_all_entities_visualization_objects) | **GET** /api/v1/entities/workspaces/{workspaceId}/visualizationObjects | Get all Visualization Objects
[**get_all_entities_workspace_data_filter_settings**](WorkspaceObjectControllerApi.md#get_all_entities_workspace_data_filter_settings) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilterSettings | Get all Settings for Workspace Data Filters
[**get_all_entities_workspace_data_filters**](WorkspaceObjectControllerApi.md#get_all_entities_workspace_data_filters) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilters | Get all Workspace Data Filters
[**get_all_entities_workspace_settings**](WorkspaceObjectControllerApi.md#get_all_entities_workspace_settings) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceSettings | Get all Setting for Workspaces
[**get_entity_analytical_dashboards**](WorkspaceObjectControllerApi.md#get_entity_analytical_dashboards) | **GET** /api/v1/entities/workspaces/{workspaceId}/analyticalDashboards/{objectId} | Get a Dashboard
[**get_entity_attributes**](WorkspaceObjectControllerApi.md#get_entity_attributes) | **GET** /api/v1/entities/workspaces/{workspaceId}/attributes/{objectId} | Get a Attribute
[**get_entity_custom_application_settings**](WorkspaceObjectControllerApi.md#get_entity_custom_application_settings) | **GET** /api/v1/entities/workspaces/{workspaceId}/customApplicationSettings/{objectId} | Get a Custom Application Setting
[**get_entity_dashboard_plugins**](WorkspaceObjectControllerApi.md#get_entity_dashboard_plugins) | **GET** /api/v1/entities/workspaces/{workspaceId}/dashboardPlugins/{objectId} | Get a Plugin
[**get_entity_datasets**](WorkspaceObjectControllerApi.md#get_entity_datasets) | **GET** /api/v1/entities/workspaces/{workspaceId}/datasets/{objectId} | Get a Dataset
[**get_entity_facts**](WorkspaceObjectControllerApi.md#get_entity_facts) | **GET** /api/v1/entities/workspaces/{workspaceId}/facts/{objectId} | Get a Fact
[**get_entity_filter_contexts**](WorkspaceObjectControllerApi.md#get_entity_filter_contexts) | **GET** /api/v1/entities/workspaces/{workspaceId}/filterContexts/{objectId} | Get a Context Filter
[**get_entity_labels**](WorkspaceObjectControllerApi.md#get_entity_labels) | **GET** /api/v1/entities/workspaces/{workspaceId}/labels/{objectId} | Get a Label
[**get_entity_metrics**](WorkspaceObjectControllerApi.md#get_entity_metrics) | **GET** /api/v1/entities/workspaces/{workspaceId}/metrics/{objectId} | Get a Metric
[**get_entity_user_data_filters**](WorkspaceObjectControllerApi.md#get_entity_user_data_filters) | **GET** /api/v1/entities/workspaces/{workspaceId}/userDataFilters/{objectId} | Get a User Data Filter
[**get_entity_visualization_objects**](WorkspaceObjectControllerApi.md#get_entity_visualization_objects) | **GET** /api/v1/entities/workspaces/{workspaceId}/visualizationObjects/{objectId} | Get a Visualization Object
[**get_entity_workspace_data_filter_settings**](WorkspaceObjectControllerApi.md#get_entity_workspace_data_filter_settings) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilterSettings/{objectId} | Get a Setting for Workspace Data Filter
[**get_entity_workspace_data_filters**](WorkspaceObjectControllerApi.md#get_entity_workspace_data_filters) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilters/{objectId} | Get a Workspace Data Filter
[**get_entity_workspace_settings**](WorkspaceObjectControllerApi.md#get_entity_workspace_settings) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceSettings/{objectId} | Get a Setting for Workspace
[**patch_entity_analytical_dashboards**](WorkspaceObjectControllerApi.md#patch_entity_analytical_dashboards) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/analyticalDashboards/{objectId} | Patch a Dashboard
[**patch_entity_custom_application_settings**](WorkspaceObjectControllerApi.md#patch_entity_custom_application_settings) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/customApplicationSettings/{objectId} | Patch a Custom Application Setting
[**patch_entity_dashboard_plugins**](WorkspaceObjectControllerApi.md#patch_entity_dashboard_plugins) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/dashboardPlugins/{objectId} | Patch a Plugin
[**patch_entity_filter_contexts**](WorkspaceObjectControllerApi.md#patch_entity_filter_contexts) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/filterContexts/{objectId} | Patch a Context Filter
[**patch_entity_metrics**](WorkspaceObjectControllerApi.md#patch_entity_metrics) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/metrics/{objectId} | Patch a Metric
[**patch_entity_user_data_filters**](WorkspaceObjectControllerApi.md#patch_entity_user_data_filters) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/userDataFilters/{objectId} | Patch a User Data Filter
[**patch_entity_visualization_objects**](WorkspaceObjectControllerApi.md#patch_entity_visualization_objects) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/visualizationObjects/{objectId} | Patch a Visualization Object
[**patch_entity_workspace_data_filter_settings**](WorkspaceObjectControllerApi.md#patch_entity_workspace_data_filter_settings) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilterSettings/{objectId} | Patch a Settings for Workspace Data Filter
[**patch_entity_workspace_data_filters**](WorkspaceObjectControllerApi.md#patch_entity_workspace_data_filters) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilters/{objectId} | Patch a Workspace Data Filter
[**patch_entity_workspace_settings**](WorkspaceObjectControllerApi.md#patch_entity_workspace_settings) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/workspaceSettings/{objectId} | Patch a Setting for Workspace
[**update_entity_analytical_dashboards**](WorkspaceObjectControllerApi.md#update_entity_analytical_dashboards) | **PUT** /api/v1/entities/workspaces/{workspaceId}/analyticalDashboards/{objectId} | Put Dashboards
[**update_entity_custom_application_settings**](WorkspaceObjectControllerApi.md#update_entity_custom_application_settings) | **PUT** /api/v1/entities/workspaces/{workspaceId}/customApplicationSettings/{objectId} | Put a Custom Application Setting
[**update_entity_dashboard_plugins**](WorkspaceObjectControllerApi.md#update_entity_dashboard_plugins) | **PUT** /api/v1/entities/workspaces/{workspaceId}/dashboardPlugins/{objectId} | Put a Plugin
[**update_entity_filter_contexts**](WorkspaceObjectControllerApi.md#update_entity_filter_contexts) | **PUT** /api/v1/entities/workspaces/{workspaceId}/filterContexts/{objectId} | Put a Context Filter
[**update_entity_metrics**](WorkspaceObjectControllerApi.md#update_entity_metrics) | **PUT** /api/v1/entities/workspaces/{workspaceId}/metrics/{objectId} | Put a Metric
[**update_entity_user_data_filters**](WorkspaceObjectControllerApi.md#update_entity_user_data_filters) | **PUT** /api/v1/entities/workspaces/{workspaceId}/userDataFilters/{objectId} | Put a User Data Filter
[**update_entity_visualization_objects**](WorkspaceObjectControllerApi.md#update_entity_visualization_objects) | **PUT** /api/v1/entities/workspaces/{workspaceId}/visualizationObjects/{objectId} | Put a Visualization Object
[**update_entity_workspace_data_filter_settings**](WorkspaceObjectControllerApi.md#update_entity_workspace_data_filter_settings) | **PUT** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilterSettings/{objectId} | Put a Settings for Workspace Data Filter
[**update_entity_workspace_data_filters**](WorkspaceObjectControllerApi.md#update_entity_workspace_data_filters) | **PUT** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilters/{objectId} | Put a Workspace Data Filter
[**update_entity_workspace_settings**](WorkspaceObjectControllerApi.md#update_entity_workspace_settings) | **PUT** /api/v1/entities/workspaces/{workspaceId}/workspaceSettings/{objectId} | Put a Setting for a Workspace


# **create_entity_analytical_dashboards**
> JsonApiAnalyticalDashboardOutDocument create_entity_analytical_dashboards(workspace_id, json_api_analytical_dashboard_post_optional_id_document)

Post Dashboards

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_analytical_dashboards: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Dashboards
        api_response = api_instance.create_entity_analytical_dashboards(workspace_id, json_api_analytical_dashboard_post_optional_id_document, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_analytical_dashboards: %s\n" % e)
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

# **create_entity_custom_application_settings**
> JsonApiCustomApplicationSettingOutDocument create_entity_custom_application_settings(workspace_id, json_api_custom_application_setting_post_optional_id_document)

Post Custom Application Settings

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_custom_application_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Custom Application Settings
        api_response = api_instance.create_entity_custom_application_settings(workspace_id, json_api_custom_application_setting_post_optional_id_document, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_custom_application_settings: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_dashboard_plugins: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Plugins
        api_response = api_instance.create_entity_dashboard_plugins(workspace_id, json_api_dashboard_plugin_post_optional_id_document, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_dashboard_plugins: %s\n" % e)
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

# **create_entity_filter_contexts**
> JsonApiFilterContextOutDocument create_entity_filter_contexts(workspace_id, json_api_filter_context_post_optional_id_document)

Post Context Filters

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_filter_contexts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Context Filters
        api_response = api_instance.create_entity_filter_contexts(workspace_id, json_api_filter_context_post_optional_id_document, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_filter_contexts: %s\n" % e)
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

# **create_entity_metrics**
> JsonApiMetricOutDocument create_entity_metrics(workspace_id, json_api_metric_post_optional_id_document)

Post Metrics

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_metrics: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Metrics
        api_response = api_instance.create_entity_metrics(workspace_id, json_api_metric_post_optional_id_document, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_metrics: %s\n" % e)
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

# **create_entity_user_data_filters**
> JsonApiUserDataFilterOutDocument create_entity_user_data_filters(workspace_id, json_api_user_data_filter_post_optional_id_document)

Post User Data Filters

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_user_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post User Data Filters
        api_response = api_instance.create_entity_user_data_filters(workspace_id, json_api_user_data_filter_post_optional_id_document, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_user_data_filters: %s\n" % e)
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

# **create_entity_visualization_objects**
> JsonApiVisualizationObjectOutDocument create_entity_visualization_objects(workspace_id, json_api_visualization_object_post_optional_id_document)

Post Visualization Objects

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_visualization_objects: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Visualization Objects
        api_response = api_instance.create_entity_visualization_objects(workspace_id, json_api_visualization_object_post_optional_id_document, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_visualization_objects: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_workspace_data_filter_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Settings for Workspace Data Filters
        api_response = api_instance.create_entity_workspace_data_filter_settings(workspace_id, json_api_workspace_data_filter_setting_in_document, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_workspace_data_filter_settings: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_workspace_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Workspace Data Filters
        api_response = api_instance.create_entity_workspace_data_filters(workspace_id, json_api_workspace_data_filter_in_document, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_workspace_data_filters: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_workspace_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Settings for Workspaces
        api_response = api_instance.create_entity_workspace_settings(workspace_id, json_api_workspace_setting_post_optional_id_document, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_workspace_settings: %s\n" % e)
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

# **delete_entity_analytical_dashboards**
> delete_entity_analytical_dashboards(workspace_id, object_id)

Delete a Dashboard

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Dashboard
        api_instance.delete_entity_analytical_dashboards(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_analytical_dashboards: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Dashboard
        api_instance.delete_entity_analytical_dashboards(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_analytical_dashboards: %s\n" % e)
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

# **delete_entity_custom_application_settings**
> delete_entity_custom_application_settings(workspace_id, object_id)

Delete a Custom Application Setting

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=applicationName==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Custom Application Setting
        api_instance.delete_entity_custom_application_settings(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_custom_application_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Custom Application Setting
        api_instance.delete_entity_custom_application_settings(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_custom_application_settings: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Plugin
        api_instance.delete_entity_dashboard_plugins(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_dashboard_plugins: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Plugin
        api_instance.delete_entity_dashboard_plugins(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_dashboard_plugins: %s\n" % e)
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

# **delete_entity_filter_contexts**
> delete_entity_filter_contexts(workspace_id, object_id)

Delete a Context Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Context Filter
        api_instance.delete_entity_filter_contexts(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_filter_contexts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Context Filter
        api_instance.delete_entity_filter_contexts(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_filter_contexts: %s\n" % e)
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

# **delete_entity_metrics**
> delete_entity_metrics(workspace_id, object_id)

Delete a Metric

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Metric
        api_instance.delete_entity_metrics(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_metrics: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Metric
        api_instance.delete_entity_metrics(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_metrics: %s\n" % e)
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

# **delete_entity_user_data_filters**
> delete_entity_user_data_filters(workspace_id, object_id)

Delete a User Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString;user.id==321;userGroup.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a User Data Filter
        api_instance.delete_entity_user_data_filters(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_user_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a User Data Filter
        api_instance.delete_entity_user_data_filters(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_user_data_filters: %s\n" % e)
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

# **delete_entity_visualization_objects**
> delete_entity_visualization_objects(workspace_id, object_id)

Delete a Visualization Object

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Visualization Object
        api_instance.delete_entity_visualization_objects(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_visualization_objects: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Visualization Object
        api_instance.delete_entity_visualization_objects(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_visualization_objects: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString;workspaceDataFilter.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Settings for Workspace Data Filter
        api_instance.delete_entity_workspace_data_filter_settings(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_workspace_data_filter_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Settings for Workspace Data Filter
        api_instance.delete_entity_workspace_data_filter_settings(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_workspace_data_filter_settings: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Workspace Data Filter
        api_instance.delete_entity_workspace_data_filters(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_workspace_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Workspace Data Filter
        api_instance.delete_entity_workspace_data_filters(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_workspace_data_filters: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=content==JsonNodeValue;type==SettingConfigurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Setting for Workspace
        api_instance.delete_entity_workspace_settings(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_workspace_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Setting for Workspace
        api_instance.delete_entity_workspace_settings(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_workspace_settings: %s\n" % e)
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

# **get_all_entities_analytical_dashboards**
> JsonApiAnalyticalDashboardOutList get_all_entities_analytical_dashboards(workspace_id)

Get all Dashboards

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_analytical_dashboards: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Dashboards
        api_response = api_instance.get_all_entities_analytical_dashboards(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_analytical_dashboards: %s\n" % e)
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

# **get_all_entities_attributes**
> JsonApiAttributeOutList get_all_entities_attributes(workspace_id)

Get all Attributes

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_attributes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Attributes
        api_response = api_instance.get_all_entities_attributes(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_attributes: %s\n" % e)
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

# **get_all_entities_custom_application_settings**
> JsonApiCustomApplicationSettingOutList get_all_entities_custom_application_settings(workspace_id)

Get all Custom Application Settings

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_custom_application_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Custom Application Settings
        api_response = api_instance.get_all_entities_custom_application_settings(workspace_id, origin=origin, filter=filter, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_custom_application_settings: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_dashboard_plugins: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Plugins
        api_response = api_instance.get_all_entities_dashboard_plugins(workspace_id, origin=origin, filter=filter, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_dashboard_plugins: %s\n" % e)
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

# **get_all_entities_datasets**
> JsonApiDatasetOutList get_all_entities_datasets(workspace_id)

Get all Datasets

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_datasets: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Datasets
        api_response = api_instance.get_all_entities_datasets(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_datasets: %s\n" % e)
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

# **get_all_entities_facts**
> JsonApiFactOutList get_all_entities_facts(workspace_id)

Get all Facts

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_facts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Facts
        api_response = api_instance.get_all_entities_facts(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_facts: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_filter_contexts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Context Filters
        api_response = api_instance.get_all_entities_filter_contexts(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_filter_contexts: %s\n" % e)
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

# **get_all_entities_labels**
> JsonApiLabelOutList get_all_entities_labels(workspace_id)

Get all Labels

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_labels: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Labels
        api_response = api_instance.get_all_entities_labels(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_labels: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_metrics: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Metrics
        api_response = api_instance.get_all_entities_metrics(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_metrics: %s\n" % e)
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

# **get_all_entities_user_data_filters**
> JsonApiUserDataFilterOutList get_all_entities_user_data_filters(workspace_id)

Get all User Data Filters

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_user_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all User Data Filters
        api_response = api_instance.get_all_entities_user_data_filters(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_user_data_filters: %s\n" % e)
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

# **get_all_entities_visualization_objects**
> JsonApiVisualizationObjectOutList get_all_entities_visualization_objects(workspace_id)

Get all Visualization Objects

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_visualization_objects: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Visualization Objects
        api_response = api_instance.get_all_entities_visualization_objects(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_visualization_objects: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_workspace_data_filter_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Settings for Workspace Data Filters
        api_response = api_instance.get_all_entities_workspace_data_filter_settings(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_workspace_data_filter_settings: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_workspace_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Workspace Data Filters
        api_response = api_instance.get_all_entities_workspace_data_filters(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_workspace_data_filters: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_workspace_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Setting for Workspaces
        api_response = api_instance.get_all_entities_workspace_settings(workspace_id, origin=origin, filter=filter, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_workspace_settings: %s\n" % e)
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

# **get_entity_analytical_dashboards**
> JsonApiAnalyticalDashboardOutDocument get_entity_analytical_dashboards(workspace_id, object_id)

Get a Dashboard

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_analytical_dashboards: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Dashboard
        api_response = api_instance.get_entity_analytical_dashboards(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_analytical_dashboards: %s\n" % e)
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

# **get_entity_attributes**
> JsonApiAttributeOutDocument get_entity_attributes(workspace_id, object_id)

Get a Attribute

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_attributes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Attribute
        api_response = api_instance.get_entity_attributes(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_attributes: %s\n" % e)
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

# **get_entity_custom_application_settings**
> JsonApiCustomApplicationSettingOutDocument get_entity_custom_application_settings(workspace_id, object_id)

Get a Custom Application Setting

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_custom_application_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Custom Application Setting
        api_response = api_instance.get_entity_custom_application_settings(workspace_id, object_id, filter=filter, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_custom_application_settings: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_dashboard_plugins: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Plugin
        api_response = api_instance.get_entity_dashboard_plugins(workspace_id, object_id, filter=filter, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_dashboard_plugins: %s\n" % e)
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

# **get_entity_datasets**
> JsonApiDatasetOutDocument get_entity_datasets(workspace_id, object_id)

Get a Dataset

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_datasets: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Dataset
        api_response = api_instance.get_entity_datasets(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_datasets: %s\n" % e)
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

# **get_entity_facts**
> JsonApiFactOutDocument get_entity_facts(workspace_id, object_id)

Get a Fact

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_facts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Fact
        api_response = api_instance.get_entity_facts(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_facts: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_filter_contexts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Context Filter
        api_response = api_instance.get_entity_filter_contexts(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_filter_contexts: %s\n" % e)
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

# **get_entity_labels**
> JsonApiLabelOutDocument get_entity_labels(workspace_id, object_id)

Get a Label

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_labels: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Label
        api_response = api_instance.get_entity_labels(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_labels: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_metrics: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Metric
        api_response = api_instance.get_entity_metrics(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_metrics: %s\n" % e)
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

# **get_entity_user_data_filters**
> JsonApiUserDataFilterOutDocument get_entity_user_data_filters(workspace_id, object_id)

Get a User Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_user_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a User Data Filter
        api_response = api_instance.get_entity_user_data_filters(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_user_data_filters: %s\n" % e)
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

# **get_entity_visualization_objects**
> JsonApiVisualizationObjectOutDocument get_entity_visualization_objects(workspace_id, object_id)

Get a Visualization Object

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_visualization_objects: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Visualization Object
        api_response = api_instance.get_entity_visualization_objects(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_visualization_objects: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_workspace_data_filter_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Setting for Workspace Data Filter
        api_response = api_instance.get_entity_workspace_data_filter_settings(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_workspace_data_filter_settings: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_workspace_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Workspace Data Filter
        api_response = api_instance.get_entity_workspace_data_filters(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_workspace_data_filters: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_workspace_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Setting for Workspace
        api_response = api_instance.get_entity_workspace_settings(workspace_id, object_id, filter=filter, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_workspace_settings: %s\n" % e)
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

# **patch_entity_analytical_dashboards**
> JsonApiAnalyticalDashboardOutDocument patch_entity_analytical_dashboards(workspace_id, object_id, json_api_analytical_dashboard_patch_document)

Patch a Dashboard

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->patch_entity_analytical_dashboards: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Dashboard
        api_response = api_instance.patch_entity_analytical_dashboards(workspace_id, object_id, json_api_analytical_dashboard_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->patch_entity_analytical_dashboards: %s\n" % e)
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

# **patch_entity_custom_application_settings**
> JsonApiCustomApplicationSettingOutDocument patch_entity_custom_application_settings(workspace_id, object_id, json_api_custom_application_setting_patch_document)

Patch a Custom Application Setting

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->patch_entity_custom_application_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Custom Application Setting
        api_response = api_instance.patch_entity_custom_application_settings(workspace_id, object_id, json_api_custom_application_setting_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->patch_entity_custom_application_settings: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->patch_entity_dashboard_plugins: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Plugin
        api_response = api_instance.patch_entity_dashboard_plugins(workspace_id, object_id, json_api_dashboard_plugin_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->patch_entity_dashboard_plugins: %s\n" % e)
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

# **patch_entity_filter_contexts**
> JsonApiFilterContextOutDocument patch_entity_filter_contexts(workspace_id, object_id, json_api_filter_context_patch_document)

Patch a Context Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->patch_entity_filter_contexts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Context Filter
        api_response = api_instance.patch_entity_filter_contexts(workspace_id, object_id, json_api_filter_context_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->patch_entity_filter_contexts: %s\n" % e)
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

# **patch_entity_metrics**
> JsonApiMetricOutDocument patch_entity_metrics(workspace_id, object_id, json_api_metric_patch_document)

Patch a Metric

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->patch_entity_metrics: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Metric
        api_response = api_instance.patch_entity_metrics(workspace_id, object_id, json_api_metric_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->patch_entity_metrics: %s\n" % e)
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

# **patch_entity_user_data_filters**
> JsonApiUserDataFilterOutDocument patch_entity_user_data_filters(workspace_id, object_id, json_api_user_data_filter_patch_document)

Patch a User Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->patch_entity_user_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a User Data Filter
        api_response = api_instance.patch_entity_user_data_filters(workspace_id, object_id, json_api_user_data_filter_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->patch_entity_user_data_filters: %s\n" % e)
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

# **patch_entity_visualization_objects**
> JsonApiVisualizationObjectOutDocument patch_entity_visualization_objects(workspace_id, object_id, json_api_visualization_object_patch_document)

Patch a Visualization Object

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->patch_entity_visualization_objects: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Visualization Object
        api_response = api_instance.patch_entity_visualization_objects(workspace_id, object_id, json_api_visualization_object_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->patch_entity_visualization_objects: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->patch_entity_workspace_data_filter_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Settings for Workspace Data Filter
        api_response = api_instance.patch_entity_workspace_data_filter_settings(workspace_id, object_id, json_api_workspace_data_filter_setting_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->patch_entity_workspace_data_filter_settings: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->patch_entity_workspace_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Workspace Data Filter
        api_response = api_instance.patch_entity_workspace_data_filters(workspace_id, object_id, json_api_workspace_data_filter_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->patch_entity_workspace_data_filters: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->patch_entity_workspace_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Setting for Workspace
        api_response = api_instance.patch_entity_workspace_settings(workspace_id, object_id, json_api_workspace_setting_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->patch_entity_workspace_settings: %s\n" % e)
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

# **update_entity_analytical_dashboards**
> JsonApiAnalyticalDashboardOutDocument update_entity_analytical_dashboards(workspace_id, object_id, json_api_analytical_dashboard_in_document)

Put Dashboards

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_analytical_dashboards: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put Dashboards
        api_response = api_instance.update_entity_analytical_dashboards(workspace_id, object_id, json_api_analytical_dashboard_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_analytical_dashboards: %s\n" % e)
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

# **update_entity_custom_application_settings**
> JsonApiCustomApplicationSettingOutDocument update_entity_custom_application_settings(workspace_id, object_id, json_api_custom_application_setting_in_document)

Put a Custom Application Setting

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_custom_application_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Custom Application Setting
        api_response = api_instance.update_entity_custom_application_settings(workspace_id, object_id, json_api_custom_application_setting_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_custom_application_settings: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_dashboard_plugins: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Plugin
        api_response = api_instance.update_entity_dashboard_plugins(workspace_id, object_id, json_api_dashboard_plugin_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_dashboard_plugins: %s\n" % e)
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

# **update_entity_filter_contexts**
> JsonApiFilterContextOutDocument update_entity_filter_contexts(workspace_id, object_id, json_api_filter_context_in_document)

Put a Context Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_filter_contexts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Context Filter
        api_response = api_instance.update_entity_filter_contexts(workspace_id, object_id, json_api_filter_context_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_filter_contexts: %s\n" % e)
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

# **update_entity_metrics**
> JsonApiMetricOutDocument update_entity_metrics(workspace_id, object_id, json_api_metric_in_document)

Put a Metric

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_metrics: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Metric
        api_response = api_instance.update_entity_metrics(workspace_id, object_id, json_api_metric_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_metrics: %s\n" % e)
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

# **update_entity_user_data_filters**
> JsonApiUserDataFilterOutDocument update_entity_user_data_filters(workspace_id, object_id, json_api_user_data_filter_in_document)

Put a User Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_user_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a User Data Filter
        api_response = api_instance.update_entity_user_data_filters(workspace_id, object_id, json_api_user_data_filter_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_user_data_filters: %s\n" % e)
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

# **update_entity_visualization_objects**
> JsonApiVisualizationObjectOutDocument update_entity_visualization_objects(workspace_id, object_id, json_api_visualization_object_in_document)

Put a Visualization Object

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_visualization_objects: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Visualization Object
        api_response = api_instance.update_entity_visualization_objects(workspace_id, object_id, json_api_visualization_object_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_visualization_objects: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_workspace_data_filter_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Settings for Workspace Data Filter
        api_response = api_instance.update_entity_workspace_data_filter_settings(workspace_id, object_id, json_api_workspace_data_filter_setting_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_workspace_data_filter_settings: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_workspace_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Workspace Data Filter
        api_response = api_instance.update_entity_workspace_data_filters(workspace_id, object_id, json_api_workspace_data_filter_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_workspace_data_filters: %s\n" % e)
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
from gooddata_api_client.api import workspace_object_controller_api
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
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
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
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_workspace_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Setting for a Workspace
        api_response = api_instance.update_entity_workspace_settings(workspace_id, object_id, json_api_workspace_setting_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_workspace_settings: %s\n" % e)
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


# gooddata_api_client.PluginsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_dashboard_plugins**](PluginsApi.md#create_entity_dashboard_plugins) | **POST** /api/v1/entities/workspaces/{workspaceId}/dashboardPlugins | Post Plugins
[**delete_entity_dashboard_plugins**](PluginsApi.md#delete_entity_dashboard_plugins) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/dashboardPlugins/{objectId} | Delete a Plugin
[**get_all_entities_dashboard_plugins**](PluginsApi.md#get_all_entities_dashboard_plugins) | **GET** /api/v1/entities/workspaces/{workspaceId}/dashboardPlugins | Get all Plugins
[**get_entity_dashboard_plugins**](PluginsApi.md#get_entity_dashboard_plugins) | **GET** /api/v1/entities/workspaces/{workspaceId}/dashboardPlugins/{objectId} | Get a Plugin
[**patch_entity_dashboard_plugins**](PluginsApi.md#patch_entity_dashboard_plugins) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/dashboardPlugins/{objectId} | Patch a Plugin
[**update_entity_dashboard_plugins**](PluginsApi.md#update_entity_dashboard_plugins) | **PUT** /api/v1/entities/workspaces/{workspaceId}/dashboardPlugins/{objectId} | Put a Plugin


# **create_entity_dashboard_plugins**
> JsonApiDashboardPluginOutDocument create_entity_dashboard_plugins(workspace_id, json_api_dashboard_plugin_post_optional_id_document)

Post Plugins

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import plugins_api
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
    api_instance = plugins_api.PluginsApi(api_client)
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
        print("Exception when calling PluginsApi->create_entity_dashboard_plugins: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Plugins
        api_response = api_instance.create_entity_dashboard_plugins(workspace_id, json_api_dashboard_plugin_post_optional_id_document, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PluginsApi->create_entity_dashboard_plugins: %s\n" % e)
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

# **delete_entity_dashboard_plugins**
> delete_entity_dashboard_plugins(workspace_id, object_id)

Delete a Plugin

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import plugins_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = plugins_api.PluginsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Plugin
        api_instance.delete_entity_dashboard_plugins(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PluginsApi->delete_entity_dashboard_plugins: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Plugin
        api_instance.delete_entity_dashboard_plugins(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PluginsApi->delete_entity_dashboard_plugins: %s\n" % e)
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

# **get_all_entities_dashboard_plugins**
> JsonApiDashboardPluginOutList get_all_entities_dashboard_plugins(workspace_id)

Get all Plugins

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import plugins_api
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
    api_instance = plugins_api.PluginsApi(api_client)
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
        print("Exception when calling PluginsApi->get_all_entities_dashboard_plugins: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Plugins
        api_response = api_instance.get_all_entities_dashboard_plugins(workspace_id, origin=origin, filter=filter, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PluginsApi->get_all_entities_dashboard_plugins: %s\n" % e)
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

# **get_entity_dashboard_plugins**
> JsonApiDashboardPluginOutDocument get_entity_dashboard_plugins(workspace_id, object_id)

Get a Plugin

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import plugins_api
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
    api_instance = plugins_api.PluginsApi(api_client)
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
        print("Exception when calling PluginsApi->get_entity_dashboard_plugins: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Plugin
        api_response = api_instance.get_entity_dashboard_plugins(workspace_id, object_id, filter=filter, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PluginsApi->get_entity_dashboard_plugins: %s\n" % e)
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

# **patch_entity_dashboard_plugins**
> JsonApiDashboardPluginOutDocument patch_entity_dashboard_plugins(workspace_id, object_id, json_api_dashboard_plugin_patch_document)

Patch a Plugin

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import plugins_api
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
    api_instance = plugins_api.PluginsApi(api_client)
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
        print("Exception when calling PluginsApi->patch_entity_dashboard_plugins: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Plugin
        api_response = api_instance.patch_entity_dashboard_plugins(workspace_id, object_id, json_api_dashboard_plugin_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PluginsApi->patch_entity_dashboard_plugins: %s\n" % e)
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

# **update_entity_dashboard_plugins**
> JsonApiDashboardPluginOutDocument update_entity_dashboard_plugins(workspace_id, object_id, json_api_dashboard_plugin_in_document)

Put a Plugin

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import plugins_api
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
    api_instance = plugins_api.PluginsApi(api_client)
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
        print("Exception when calling PluginsApi->update_entity_dashboard_plugins: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Plugin
        api_response = api_instance.update_entity_dashboard_plugins(workspace_id, object_id, json_api_dashboard_plugin_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PluginsApi->update_entity_dashboard_plugins: %s\n" % e)
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


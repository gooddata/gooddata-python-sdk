# gooddata_api_client.WorkspaceThemeControllerApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_workspace_themes**](WorkspaceThemeControllerApi.md#create_entity_workspace_themes) | **POST** /api/v1/entities/workspaces/{workspaceId}/workspaceThemes | Post Workspace Theme
[**delete_entity_workspace_themes**](WorkspaceThemeControllerApi.md#delete_entity_workspace_themes) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/workspaceThemes/{objectId} | Delete a Workspace Theme
[**get_all_entities_workspace_themes**](WorkspaceThemeControllerApi.md#get_all_entities_workspace_themes) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceThemes | Get all Workspace Themes
[**get_entity_workspace_themes**](WorkspaceThemeControllerApi.md#get_entity_workspace_themes) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceThemes/{objectId} | Get a Workspace Theme
[**patch_entity_workspace_themes**](WorkspaceThemeControllerApi.md#patch_entity_workspace_themes) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/workspaceThemes/{objectId} | Patch a Workspace Theme
[**update_entity_workspace_themes**](WorkspaceThemeControllerApi.md#update_entity_workspace_themes) | **PUT** /api/v1/entities/workspaces/{workspaceId}/workspaceThemes/{objectId} | Put a Workspace Theme


# **create_entity_workspace_themes**
> JsonApiWorkspaceThemeOutDocument create_entity_workspace_themes(workspace_id, json_api_workspace_theme_in_document)

Post Workspace Theme

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_theme_controller_api
from gooddata_api_client.model.json_api_workspace_theme_out_document import JsonApiWorkspaceThemeOutDocument
from gooddata_api_client.model.json_api_workspace_theme_in_document import JsonApiWorkspaceThemeInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_theme_controller_api.WorkspaceThemeControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_workspace_theme_in_document = JsonApiWorkspaceThemeInDocument(
        data=JsonApiWorkspaceThemeIn(
            attributes=JsonApiColorPaletteInAttributes(
                content={},
                name="name_example",
            ),
            id="id1",
            type="workspaceTheme",
        ),
    ) # JsonApiWorkspaceThemeInDocument | 
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Workspace Theme
        api_response = api_instance.create_entity_workspace_themes(workspace_id, json_api_workspace_theme_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceThemeControllerApi->create_entity_workspace_themes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Workspace Theme
        api_response = api_instance.create_entity_workspace_themes(workspace_id, json_api_workspace_theme_in_document, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceThemeControllerApi->create_entity_workspace_themes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_workspace_theme_in_document** | [**JsonApiWorkspaceThemeInDocument**](JsonApiWorkspaceThemeInDocument.md)|  |
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiWorkspaceThemeOutDocument**](JsonApiWorkspaceThemeOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_workspace_themes**
> delete_entity_workspace_themes(workspace_id, object_id)

Delete a Workspace Theme

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_theme_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_theme_controller_api.WorkspaceThemeControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Delete a Workspace Theme
        api_instance.delete_entity_workspace_themes(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceThemeControllerApi->delete_entity_workspace_themes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |

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

# **get_all_entities_workspace_themes**
> JsonApiWorkspaceThemeOutList get_all_entities_workspace_themes(workspace_id)

Get all Workspace Themes

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_theme_controller_api
from gooddata_api_client.model.json_api_workspace_theme_out_list import JsonApiWorkspaceThemeOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_theme_controller_api.WorkspaceThemeControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "name==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,page,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get all Workspace Themes
        api_response = api_instance.get_all_entities_workspace_themes(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceThemeControllerApi->get_all_entities_workspace_themes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Workspace Themes
        api_response = api_instance.get_all_entities_workspace_themes(workspace_id, origin=origin, filter=filter, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceThemeControllerApi->get_all_entities_workspace_themes: %s\n" % e)
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

[**JsonApiWorkspaceThemeOutList**](JsonApiWorkspaceThemeOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_workspace_themes**
> JsonApiWorkspaceThemeOutDocument get_entity_workspace_themes(workspace_id, object_id)

Get a Workspace Theme

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_theme_controller_api
from gooddata_api_client.model.json_api_workspace_theme_out_document import JsonApiWorkspaceThemeOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_theme_controller_api.WorkspaceThemeControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "name==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a Workspace Theme
        api_response = api_instance.get_entity_workspace_themes(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceThemeControllerApi->get_entity_workspace_themes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Workspace Theme
        api_response = api_instance.get_entity_workspace_themes(workspace_id, object_id, filter=filter, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceThemeControllerApi->get_entity_workspace_themes: %s\n" % e)
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

[**JsonApiWorkspaceThemeOutDocument**](JsonApiWorkspaceThemeOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_workspace_themes**
> JsonApiWorkspaceThemeOutDocument patch_entity_workspace_themes(workspace_id, object_id, json_api_workspace_theme_patch_document)

Patch a Workspace Theme

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_theme_controller_api
from gooddata_api_client.model.json_api_workspace_theme_out_document import JsonApiWorkspaceThemeOutDocument
from gooddata_api_client.model.json_api_workspace_theme_patch_document import JsonApiWorkspaceThemePatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_theme_controller_api.WorkspaceThemeControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_workspace_theme_patch_document = JsonApiWorkspaceThemePatchDocument(
        data=JsonApiWorkspaceThemePatch(
            attributes=JsonApiColorPalettePatchAttributes(
                content={},
                name="name_example",
            ),
            id="id1",
            type="workspaceTheme",
        ),
    ) # JsonApiWorkspaceThemePatchDocument | 
    filter = "name==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch a Workspace Theme
        api_response = api_instance.patch_entity_workspace_themes(workspace_id, object_id, json_api_workspace_theme_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceThemeControllerApi->patch_entity_workspace_themes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Workspace Theme
        api_response = api_instance.patch_entity_workspace_themes(workspace_id, object_id, json_api_workspace_theme_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceThemeControllerApi->patch_entity_workspace_themes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_workspace_theme_patch_document** | [**JsonApiWorkspaceThemePatchDocument**](JsonApiWorkspaceThemePatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiWorkspaceThemeOutDocument**](JsonApiWorkspaceThemeOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_workspace_themes**
> JsonApiWorkspaceThemeOutDocument update_entity_workspace_themes(workspace_id, object_id, json_api_workspace_theme_in_document)

Put a Workspace Theme

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_theme_controller_api
from gooddata_api_client.model.json_api_workspace_theme_out_document import JsonApiWorkspaceThemeOutDocument
from gooddata_api_client.model.json_api_workspace_theme_in_document import JsonApiWorkspaceThemeInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_theme_controller_api.WorkspaceThemeControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_workspace_theme_in_document = JsonApiWorkspaceThemeInDocument(
        data=JsonApiWorkspaceThemeIn(
            attributes=JsonApiColorPaletteInAttributes(
                content={},
                name="name_example",
            ),
            id="id1",
            type="workspaceTheme",
        ),
    ) # JsonApiWorkspaceThemeInDocument | 
    filter = "name==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put a Workspace Theme
        api_response = api_instance.update_entity_workspace_themes(workspace_id, object_id, json_api_workspace_theme_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceThemeControllerApi->update_entity_workspace_themes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Workspace Theme
        api_response = api_instance.update_entity_workspace_themes(workspace_id, object_id, json_api_workspace_theme_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceThemeControllerApi->update_entity_workspace_themes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_workspace_theme_in_document** | [**JsonApiWorkspaceThemeInDocument**](JsonApiWorkspaceThemeInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiWorkspaceThemeOutDocument**](JsonApiWorkspaceThemeOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


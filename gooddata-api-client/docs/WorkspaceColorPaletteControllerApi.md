# gooddata_api_client.WorkspaceColorPaletteControllerApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_workspace_color_palettes**](WorkspaceColorPaletteControllerApi.md#create_entity_workspace_color_palettes) | **POST** /api/v1/entities/workspaces/{workspaceId}/workspaceColorPalettes | Post Workspace Color Palette
[**delete_entity_workspace_color_palettes**](WorkspaceColorPaletteControllerApi.md#delete_entity_workspace_color_palettes) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/workspaceColorPalettes/{objectId} | Delete a Workspace Color Palette
[**get_all_entities_workspace_color_palettes**](WorkspaceColorPaletteControllerApi.md#get_all_entities_workspace_color_palettes) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceColorPalettes | Get all Workspace Color Palettes
[**get_entity_workspace_color_palettes**](WorkspaceColorPaletteControllerApi.md#get_entity_workspace_color_palettes) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceColorPalettes/{objectId} | Get a Workspace Color Palette
[**patch_entity_workspace_color_palettes**](WorkspaceColorPaletteControllerApi.md#patch_entity_workspace_color_palettes) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/workspaceColorPalettes/{objectId} | Patch a Workspace Color Palette
[**update_entity_workspace_color_palettes**](WorkspaceColorPaletteControllerApi.md#update_entity_workspace_color_palettes) | **PUT** /api/v1/entities/workspaces/{workspaceId}/workspaceColorPalettes/{objectId} | Put a Workspace Color Palette


# **create_entity_workspace_color_palettes**
> JsonApiWorkspaceColorPaletteOutDocument create_entity_workspace_color_palettes(workspace_id, json_api_workspace_color_palette_in_document)

Post Workspace Color Palette

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_color_palette_controller_api
from gooddata_api_client.model.json_api_workspace_color_palette_out_document import JsonApiWorkspaceColorPaletteOutDocument
from gooddata_api_client.model.json_api_workspace_color_palette_in_document import JsonApiWorkspaceColorPaletteInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_color_palette_controller_api.WorkspaceColorPaletteControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_workspace_color_palette_in_document = JsonApiWorkspaceColorPaletteInDocument(
        data=JsonApiWorkspaceColorPaletteIn(
            attributes=JsonApiColorPaletteInAttributes(
                content={},
                name="name_example",
            ),
            id="id1",
            type="workspaceColorPalette",
        ),
    ) # JsonApiWorkspaceColorPaletteInDocument | 
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Workspace Color Palette
        api_response = api_instance.create_entity_workspace_color_palettes(workspace_id, json_api_workspace_color_palette_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceColorPaletteControllerApi->create_entity_workspace_color_palettes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Workspace Color Palette
        api_response = api_instance.create_entity_workspace_color_palettes(workspace_id, json_api_workspace_color_palette_in_document, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceColorPaletteControllerApi->create_entity_workspace_color_palettes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_workspace_color_palette_in_document** | [**JsonApiWorkspaceColorPaletteInDocument**](JsonApiWorkspaceColorPaletteInDocument.md)|  |
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiWorkspaceColorPaletteOutDocument**](JsonApiWorkspaceColorPaletteOutDocument.md)

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

# **delete_entity_workspace_color_palettes**
> delete_entity_workspace_color_palettes(workspace_id, object_id)

Delete a Workspace Color Palette

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_color_palette_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_color_palette_controller_api.WorkspaceColorPaletteControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Delete a Workspace Color Palette
        api_instance.delete_entity_workspace_color_palettes(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceColorPaletteControllerApi->delete_entity_workspace_color_palettes: %s\n" % e)
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

# **get_all_entities_workspace_color_palettes**
> JsonApiWorkspaceColorPaletteOutList get_all_entities_workspace_color_palettes(workspace_id)

Get all Workspace Color Palettes

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_color_palette_controller_api
from gooddata_api_client.model.json_api_workspace_color_palette_out_list import JsonApiWorkspaceColorPaletteOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_color_palette_controller_api.WorkspaceColorPaletteControllerApi(api_client)
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
        # Get all Workspace Color Palettes
        api_response = api_instance.get_all_entities_workspace_color_palettes(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceColorPaletteControllerApi->get_all_entities_workspace_color_palettes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Workspace Color Palettes
        api_response = api_instance.get_all_entities_workspace_color_palettes(workspace_id, origin=origin, filter=filter, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceColorPaletteControllerApi->get_all_entities_workspace_color_palettes: %s\n" % e)
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

[**JsonApiWorkspaceColorPaletteOutList**](JsonApiWorkspaceColorPaletteOutList.md)

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

# **get_entity_workspace_color_palettes**
> JsonApiWorkspaceColorPaletteOutDocument get_entity_workspace_color_palettes(workspace_id, object_id)

Get a Workspace Color Palette

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_color_palette_controller_api
from gooddata_api_client.model.json_api_workspace_color_palette_out_document import JsonApiWorkspaceColorPaletteOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_color_palette_controller_api.WorkspaceColorPaletteControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "name==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a Workspace Color Palette
        api_response = api_instance.get_entity_workspace_color_palettes(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceColorPaletteControllerApi->get_entity_workspace_color_palettes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Workspace Color Palette
        api_response = api_instance.get_entity_workspace_color_palettes(workspace_id, object_id, filter=filter, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceColorPaletteControllerApi->get_entity_workspace_color_palettes: %s\n" % e)
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

[**JsonApiWorkspaceColorPaletteOutDocument**](JsonApiWorkspaceColorPaletteOutDocument.md)

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

# **patch_entity_workspace_color_palettes**
> JsonApiWorkspaceColorPaletteOutDocument patch_entity_workspace_color_palettes(workspace_id, object_id, json_api_workspace_color_palette_patch_document)

Patch a Workspace Color Palette

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_color_palette_controller_api
from gooddata_api_client.model.json_api_workspace_color_palette_out_document import JsonApiWorkspaceColorPaletteOutDocument
from gooddata_api_client.model.json_api_workspace_color_palette_patch_document import JsonApiWorkspaceColorPalettePatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_color_palette_controller_api.WorkspaceColorPaletteControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_workspace_color_palette_patch_document = JsonApiWorkspaceColorPalettePatchDocument(
        data=JsonApiWorkspaceColorPalettePatch(
            attributes=JsonApiColorPalettePatchAttributes(
                content={},
                name="name_example",
            ),
            id="id1",
            type="workspaceColorPalette",
        ),
    ) # JsonApiWorkspaceColorPalettePatchDocument | 
    filter = "name==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch a Workspace Color Palette
        api_response = api_instance.patch_entity_workspace_color_palettes(workspace_id, object_id, json_api_workspace_color_palette_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceColorPaletteControllerApi->patch_entity_workspace_color_palettes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Workspace Color Palette
        api_response = api_instance.patch_entity_workspace_color_palettes(workspace_id, object_id, json_api_workspace_color_palette_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceColorPaletteControllerApi->patch_entity_workspace_color_palettes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_workspace_color_palette_patch_document** | [**JsonApiWorkspaceColorPalettePatchDocument**](JsonApiWorkspaceColorPalettePatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiWorkspaceColorPaletteOutDocument**](JsonApiWorkspaceColorPaletteOutDocument.md)

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

# **update_entity_workspace_color_palettes**
> JsonApiWorkspaceColorPaletteOutDocument update_entity_workspace_color_palettes(workspace_id, object_id, json_api_workspace_color_palette_in_document)

Put a Workspace Color Palette

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_color_palette_controller_api
from gooddata_api_client.model.json_api_workspace_color_palette_out_document import JsonApiWorkspaceColorPaletteOutDocument
from gooddata_api_client.model.json_api_workspace_color_palette_in_document import JsonApiWorkspaceColorPaletteInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_color_palette_controller_api.WorkspaceColorPaletteControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_workspace_color_palette_in_document = JsonApiWorkspaceColorPaletteInDocument(
        data=JsonApiWorkspaceColorPaletteIn(
            attributes=JsonApiColorPaletteInAttributes(
                content={},
                name="name_example",
            ),
            id="id1",
            type="workspaceColorPalette",
        ),
    ) # JsonApiWorkspaceColorPaletteInDocument | 
    filter = "name==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put a Workspace Color Palette
        api_response = api_instance.update_entity_workspace_color_palettes(workspace_id, object_id, json_api_workspace_color_palette_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceColorPaletteControllerApi->update_entity_workspace_color_palettes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Workspace Color Palette
        api_response = api_instance.update_entity_workspace_color_palettes(workspace_id, object_id, json_api_workspace_color_palette_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceColorPaletteControllerApi->update_entity_workspace_color_palettes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_workspace_color_palette_in_document** | [**JsonApiWorkspaceColorPaletteInDocument**](JsonApiWorkspaceColorPaletteInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiWorkspaceColorPaletteOutDocument**](JsonApiWorkspaceColorPaletteOutDocument.md)

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


# gooddata_api_client.AppearanceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_color_palettes**](AppearanceApi.md#create_entity_color_palettes) | **POST** /api/v1/entities/colorPalettes | Post Color Pallettes
[**create_entity_themes**](AppearanceApi.md#create_entity_themes) | **POST** /api/v1/entities/themes | Post Theming
[**create_entity_workspace_color_palettes**](AppearanceApi.md#create_entity_workspace_color_palettes) | **POST** /api/v1/entities/workspaces/{workspaceId}/workspaceColorPalettes | Post Workspace Color Palette
[**create_entity_workspace_themes**](AppearanceApi.md#create_entity_workspace_themes) | **POST** /api/v1/entities/workspaces/{workspaceId}/workspaceThemes | Post Workspace Theme
[**delete_entity_color_palettes**](AppearanceApi.md#delete_entity_color_palettes) | **DELETE** /api/v1/entities/colorPalettes/{id} | Delete a Color Pallette
[**delete_entity_themes**](AppearanceApi.md#delete_entity_themes) | **DELETE** /api/v1/entities/themes/{id} | Delete Theming
[**delete_entity_workspace_color_palettes**](AppearanceApi.md#delete_entity_workspace_color_palettes) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/workspaceColorPalettes/{objectId} | Delete a Workspace Color Palette
[**delete_entity_workspace_themes**](AppearanceApi.md#delete_entity_workspace_themes) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/workspaceThemes/{objectId} | Delete a Workspace Theme
[**get_all_entities_color_palettes**](AppearanceApi.md#get_all_entities_color_palettes) | **GET** /api/v1/entities/colorPalettes | Get all Color Pallettes
[**get_all_entities_themes**](AppearanceApi.md#get_all_entities_themes) | **GET** /api/v1/entities/themes | Get all Theming entities
[**get_all_entities_workspace_color_palettes**](AppearanceApi.md#get_all_entities_workspace_color_palettes) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceColorPalettes | Get all Workspace Color Palettes
[**get_all_entities_workspace_themes**](AppearanceApi.md#get_all_entities_workspace_themes) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceThemes | Get all Workspace Themes
[**get_entity_color_palettes**](AppearanceApi.md#get_entity_color_palettes) | **GET** /api/v1/entities/colorPalettes/{id} | Get Color Pallette
[**get_entity_themes**](AppearanceApi.md#get_entity_themes) | **GET** /api/v1/entities/themes/{id} | Get Theming
[**get_entity_workspace_color_palettes**](AppearanceApi.md#get_entity_workspace_color_palettes) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceColorPalettes/{objectId} | Get a Workspace Color Palette
[**get_entity_workspace_themes**](AppearanceApi.md#get_entity_workspace_themes) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceThemes/{objectId} | Get a Workspace Theme
[**patch_entity_color_palettes**](AppearanceApi.md#patch_entity_color_palettes) | **PATCH** /api/v1/entities/colorPalettes/{id} | Patch Color Pallette
[**patch_entity_themes**](AppearanceApi.md#patch_entity_themes) | **PATCH** /api/v1/entities/themes/{id} | Patch Theming
[**patch_entity_workspace_color_palettes**](AppearanceApi.md#patch_entity_workspace_color_palettes) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/workspaceColorPalettes/{objectId} | Patch a Workspace Color Palette
[**patch_entity_workspace_themes**](AppearanceApi.md#patch_entity_workspace_themes) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/workspaceThemes/{objectId} | Patch a Workspace Theme
[**update_entity_color_palettes**](AppearanceApi.md#update_entity_color_palettes) | **PUT** /api/v1/entities/colorPalettes/{id} | Put Color Pallette
[**update_entity_themes**](AppearanceApi.md#update_entity_themes) | **PUT** /api/v1/entities/themes/{id} | Put Theming
[**update_entity_workspace_color_palettes**](AppearanceApi.md#update_entity_workspace_color_palettes) | **PUT** /api/v1/entities/workspaces/{workspaceId}/workspaceColorPalettes/{objectId} | Put a Workspace Color Palette
[**update_entity_workspace_themes**](AppearanceApi.md#update_entity_workspace_themes) | **PUT** /api/v1/entities/workspaces/{workspaceId}/workspaceThemes/{objectId} | Put a Workspace Theme


# **create_entity_color_palettes**
> JsonApiColorPaletteOutDocument create_entity_color_palettes(json_api_color_palette_in_document)

Post Color Pallettes

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import appearance_api
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
    api_instance = appearance_api.AppearanceApi(api_client)
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
        print("Exception when calling AppearanceApi->create_entity_color_palettes: %s\n" % e)
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

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
 - **Accept**: application/json, application/vnd.gooddata.api+json


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
from gooddata_api_client.api import appearance_api
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
    api_instance = appearance_api.AppearanceApi(api_client)
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
        print("Exception when calling AppearanceApi->create_entity_themes: %s\n" % e)
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

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_entity_workspace_color_palettes**
> JsonApiWorkspaceColorPaletteOutDocument create_entity_workspace_color_palettes(workspace_id, json_api_workspace_color_palette_in_document)

Post Workspace Color Palette

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import appearance_api
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
    api_instance = appearance_api.AppearanceApi(api_client)
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
        print("Exception when calling AppearanceApi->create_entity_workspace_color_palettes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Workspace Color Palette
        api_response = api_instance.create_entity_workspace_color_palettes(workspace_id, json_api_workspace_color_palette_in_document, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->create_entity_workspace_color_palettes: %s\n" % e)
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

# **create_entity_workspace_themes**
> JsonApiWorkspaceThemeOutDocument create_entity_workspace_themes(workspace_id, json_api_workspace_theme_in_document)

Post Workspace Theme

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import appearance_api
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
    api_instance = appearance_api.AppearanceApi(api_client)
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
        print("Exception when calling AppearanceApi->create_entity_workspace_themes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Workspace Theme
        api_response = api_instance.create_entity_workspace_themes(workspace_id, json_api_workspace_theme_in_document, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->create_entity_workspace_themes: %s\n" % e)
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

# **delete_entity_color_palettes**
> delete_entity_color_palettes(id)

Delete a Color Pallette

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import appearance_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = appearance_api.AppearanceApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Delete a Color Pallette
        api_instance.delete_entity_color_palettes(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->delete_entity_color_palettes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |

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
from gooddata_api_client.api import appearance_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = appearance_api.AppearanceApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Delete Theming
        api_instance.delete_entity_themes(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->delete_entity_themes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |

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

# **delete_entity_workspace_color_palettes**
> delete_entity_workspace_color_palettes(workspace_id, object_id)

Delete a Workspace Color Palette

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import appearance_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = appearance_api.AppearanceApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Delete a Workspace Color Palette
        api_instance.delete_entity_workspace_color_palettes(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->delete_entity_workspace_color_palettes: %s\n" % e)
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

# **delete_entity_workspace_themes**
> delete_entity_workspace_themes(workspace_id, object_id)

Delete a Workspace Theme

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import appearance_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = appearance_api.AppearanceApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Delete a Workspace Theme
        api_instance.delete_entity_workspace_themes(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->delete_entity_workspace_themes: %s\n" % e)
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

# **get_all_entities_color_palettes**
> JsonApiColorPaletteOutList get_all_entities_color_palettes()

Get all Color Pallettes

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import appearance_api
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
    api_instance = appearance_api.AppearanceApi(api_client)
    filter = "name==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = [
        "metaInclude=page,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Color Pallettes
        api_response = api_instance.get_all_entities_color_palettes(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->get_all_entities_color_palettes: %s\n" % e)
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

[**JsonApiColorPaletteOutList**](JsonApiColorPaletteOutList.md)

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

# **get_all_entities_themes**
> JsonApiThemeOutList get_all_entities_themes()

Get all Theming entities

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import appearance_api
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
    api_instance = appearance_api.AppearanceApi(api_client)
    filter = "name==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = [
        "metaInclude=page,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Theming entities
        api_response = api_instance.get_all_entities_themes(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->get_all_entities_themes: %s\n" % e)
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

[**JsonApiThemeOutList**](JsonApiThemeOutList.md)

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

# **get_all_entities_workspace_color_palettes**
> JsonApiWorkspaceColorPaletteOutList get_all_entities_workspace_color_palettes(workspace_id)

Get all Workspace Color Palettes

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import appearance_api
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
    api_instance = appearance_api.AppearanceApi(api_client)
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
        print("Exception when calling AppearanceApi->get_all_entities_workspace_color_palettes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Workspace Color Palettes
        api_response = api_instance.get_all_entities_workspace_color_palettes(workspace_id, origin=origin, filter=filter, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->get_all_entities_workspace_color_palettes: %s\n" % e)
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

# **get_all_entities_workspace_themes**
> JsonApiWorkspaceThemeOutList get_all_entities_workspace_themes(workspace_id)

Get all Workspace Themes

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import appearance_api
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
    api_instance = appearance_api.AppearanceApi(api_client)
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
        print("Exception when calling AppearanceApi->get_all_entities_workspace_themes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Workspace Themes
        api_response = api_instance.get_all_entities_workspace_themes(workspace_id, origin=origin, filter=filter, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->get_all_entities_workspace_themes: %s\n" % e)
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

# **get_entity_color_palettes**
> JsonApiColorPaletteOutDocument get_entity_color_palettes(id)

Get Color Pallette

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import appearance_api
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
    api_instance = appearance_api.AppearanceApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "name==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get Color Pallette
        api_response = api_instance.get_entity_color_palettes(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->get_entity_color_palettes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Color Pallette
        api_response = api_instance.get_entity_color_palettes(id, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->get_entity_color_palettes: %s\n" % e)
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
 - **Accept**: application/json, application/vnd.gooddata.api+json


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
from gooddata_api_client.api import appearance_api
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
    api_instance = appearance_api.AppearanceApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "name==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get Theming
        api_response = api_instance.get_entity_themes(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->get_entity_themes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Theming
        api_response = api_instance.get_entity_themes(id, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->get_entity_themes: %s\n" % e)
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
from gooddata_api_client.api import appearance_api
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
    api_instance = appearance_api.AppearanceApi(api_client)
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
        print("Exception when calling AppearanceApi->get_entity_workspace_color_palettes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Workspace Color Palette
        api_response = api_instance.get_entity_workspace_color_palettes(workspace_id, object_id, filter=filter, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->get_entity_workspace_color_palettes: %s\n" % e)
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

# **get_entity_workspace_themes**
> JsonApiWorkspaceThemeOutDocument get_entity_workspace_themes(workspace_id, object_id)

Get a Workspace Theme

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import appearance_api
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
    api_instance = appearance_api.AppearanceApi(api_client)
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
        print("Exception when calling AppearanceApi->get_entity_workspace_themes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Workspace Theme
        api_response = api_instance.get_entity_workspace_themes(workspace_id, object_id, filter=filter, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->get_entity_workspace_themes: %s\n" % e)
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

# **patch_entity_color_palettes**
> JsonApiColorPaletteOutDocument patch_entity_color_palettes(id, json_api_color_palette_patch_document)

Patch Color Pallette

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import appearance_api
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
    api_instance = appearance_api.AppearanceApi(api_client)
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
    filter = "name==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch Color Pallette
        api_response = api_instance.patch_entity_color_palettes(id, json_api_color_palette_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->patch_entity_color_palettes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch Color Pallette
        api_response = api_instance.patch_entity_color_palettes(id, json_api_color_palette_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->patch_entity_color_palettes: %s\n" % e)
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

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
 - **Accept**: application/json, application/vnd.gooddata.api+json


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
from gooddata_api_client.api import appearance_api
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
    api_instance = appearance_api.AppearanceApi(api_client)
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
    filter = "name==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch Theming
        api_response = api_instance.patch_entity_themes(id, json_api_theme_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->patch_entity_themes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch Theming
        api_response = api_instance.patch_entity_themes(id, json_api_theme_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->patch_entity_themes: %s\n" % e)
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

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
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
from gooddata_api_client.api import appearance_api
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
    api_instance = appearance_api.AppearanceApi(api_client)
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
        print("Exception when calling AppearanceApi->patch_entity_workspace_color_palettes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Workspace Color Palette
        api_response = api_instance.patch_entity_workspace_color_palettes(workspace_id, object_id, json_api_workspace_color_palette_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->patch_entity_workspace_color_palettes: %s\n" % e)
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

# **patch_entity_workspace_themes**
> JsonApiWorkspaceThemeOutDocument patch_entity_workspace_themes(workspace_id, object_id, json_api_workspace_theme_patch_document)

Patch a Workspace Theme

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import appearance_api
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
    api_instance = appearance_api.AppearanceApi(api_client)
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
        print("Exception when calling AppearanceApi->patch_entity_workspace_themes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Workspace Theme
        api_response = api_instance.patch_entity_workspace_themes(workspace_id, object_id, json_api_workspace_theme_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->patch_entity_workspace_themes: %s\n" % e)
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

# **update_entity_color_palettes**
> JsonApiColorPaletteOutDocument update_entity_color_palettes(id, json_api_color_palette_in_document)

Put Color Pallette

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import appearance_api
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
    api_instance = appearance_api.AppearanceApi(api_client)
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
    filter = "name==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put Color Pallette
        api_response = api_instance.update_entity_color_palettes(id, json_api_color_palette_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->update_entity_color_palettes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put Color Pallette
        api_response = api_instance.update_entity_color_palettes(id, json_api_color_palette_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->update_entity_color_palettes: %s\n" % e)
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

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
 - **Accept**: application/json, application/vnd.gooddata.api+json


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
from gooddata_api_client.api import appearance_api
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
    api_instance = appearance_api.AppearanceApi(api_client)
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
    filter = "name==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put Theming
        api_response = api_instance.update_entity_themes(id, json_api_theme_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->update_entity_themes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put Theming
        api_response = api_instance.update_entity_themes(id, json_api_theme_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->update_entity_themes: %s\n" % e)
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
from gooddata_api_client.api import appearance_api
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
    api_instance = appearance_api.AppearanceApi(api_client)
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
        print("Exception when calling AppearanceApi->update_entity_workspace_color_palettes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Workspace Color Palette
        api_response = api_instance.update_entity_workspace_color_palettes(workspace_id, object_id, json_api_workspace_color_palette_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->update_entity_workspace_color_palettes: %s\n" % e)
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

# **update_entity_workspace_themes**
> JsonApiWorkspaceThemeOutDocument update_entity_workspace_themes(workspace_id, object_id, json_api_workspace_theme_in_document)

Put a Workspace Theme

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import appearance_api
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
    api_instance = appearance_api.AppearanceApi(api_client)
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
        print("Exception when calling AppearanceApi->update_entity_workspace_themes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Workspace Theme
        api_response = api_instance.update_entity_workspace_themes(workspace_id, object_id, json_api_workspace_theme_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AppearanceApi->update_entity_workspace_themes: %s\n" % e)
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


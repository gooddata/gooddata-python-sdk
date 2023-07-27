<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.plugins_api.PluginsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_dashboard_plugins**](#create_entity_dashboard_plugins) | **post** /api/v1/entities/workspaces/{workspaceId}/dashboardPlugins | Post Plugins
[**delete_entity_dashboard_plugins**](#delete_entity_dashboard_plugins) | **delete** /api/v1/entities/workspaces/{workspaceId}/dashboardPlugins/{objectId} | Delete a Plugin
[**get_all_entities_dashboard_plugins**](#get_all_entities_dashboard_plugins) | **get** /api/v1/entities/workspaces/{workspaceId}/dashboardPlugins | Get all Plugins
[**get_entity_dashboard_plugins**](#get_entity_dashboard_plugins) | **get** /api/v1/entities/workspaces/{workspaceId}/dashboardPlugins/{objectId} | Get a Plugin
[**patch_entity_dashboard_plugins**](#patch_entity_dashboard_plugins) | **patch** /api/v1/entities/workspaces/{workspaceId}/dashboardPlugins/{objectId} | Patch a Plugin
[**update_entity_dashboard_plugins**](#update_entity_dashboard_plugins) | **put** /api/v1/entities/workspaces/{workspaceId}/dashboardPlugins/{objectId} | Put a Plugin

# **create_entity_dashboard_plugins**
<a id="create_entity_dashboard_plugins"></a>
> JsonApiDashboardPluginOutDocument create_entity_dashboard_plugins(workspace_idjson_api_dashboard_plugin_post_optional_id_document)

Post Plugins

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import plugins_api
from gooddata_api_client.model.json_api_dashboard_plugin_post_optional_id_document import JsonApiDashboardPluginPostOptionalIdDocument
from gooddata_api_client.model.json_api_dashboard_plugin_out_document import JsonApiDashboardPluginOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plugins_api.PluginsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
    }
    body = JsonApiDashboardPluginPostOptionalIdDocument(
        data=JsonApiDashboardPluginPostOptionalId(
            attributes=dict(
                are_relations_valid=True,
                content=dict(),
                description="description_example",
                tags=[
                    "tags_example"
                ],
                title="title_example",
            ),
            id="id1",
            type="dashboardPlugin",
        ),
    )
    try:
        # Post Plugins
        api_response = api_instance.create_entity_dashboard_plugins(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PluginsApi->create_entity_dashboard_plugins: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
        'metaInclude': [
        "metaInclude=origin,all"
    ],
    }
    body = JsonApiDashboardPluginPostOptionalIdDocument(
        data=JsonApiDashboardPluginPostOptionalId(
            attributes=dict(
                are_relations_valid=True,
                content=dict(),
                description="description_example",
                tags=[
                    "tags_example"
                ],
                title="title_example",
            ),
            id="id1",
            type="dashboardPlugin",
        ),
    )
    try:
        # Post Plugins
        api_response = api_instance.create_entity_dashboard_plugins(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PluginsApi->create_entity_dashboard_plugins: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDashboardPluginPostOptionalIdDocument**](../../models/JsonApiDashboardPluginPostOptionalIdDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
metaInclude | MetaIncludeSchema | | optional


# MetaIncludeSchema

Included meta objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Included meta objects | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["origin", "all", "ALL", ] 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#create_entity_dashboard_plugins.ApiResponseFor201) | Request successfully processed

#### create_entity_dashboard_plugins.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDashboardPluginOutDocument**](../../models/JsonApiDashboardPluginOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_entity_dashboard_plugins**
<a id="delete_entity_dashboard_plugins"></a>
> delete_entity_dashboard_plugins(workspace_idobject_id)

Delete a Plugin

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import plugins_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plugins_api.PluginsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
    }
    try:
        # Delete a Plugin
        api_response = api_instance.delete_entity_dashboard_plugins(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PluginsApi->delete_entity_dashboard_plugins: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
        'filter': "filter=title==someString;description==someString",
    }
    try:
        # Delete a Plugin
        api_response = api_instance.delete_entity_dashboard_plugins(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PluginsApi->delete_entity_dashboard_plugins: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 
objectId | ObjectIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# ObjectIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#delete_entity_dashboard_plugins.ApiResponseFor204) | Successfully deleted

#### delete_entity_dashboard_plugins.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_dashboard_plugins**
<a id="get_all_entities_dashboard_plugins"></a>
> JsonApiDashboardPluginOutList get_all_entities_dashboard_plugins(workspace_id)

Get all Plugins

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import plugins_api
from gooddata_api_client.model.json_api_dashboard_plugin_out_list import JsonApiDashboardPluginOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plugins_api.PluginsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
    }
    header_params = {
    }
    try:
        # Get all Plugins
        api_response = api_instance.get_all_entities_dashboard_plugins(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PluginsApi->get_all_entities_dashboard_plugins: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
        'origin': "ALL",
        'filter': "filter=title==someString;description==someString",
        'page': 0,
        'size': 20,
        'sort': [
        "sort_example"
    ],
        'metaInclude': [
        "metaInclude=origin,all"
    ],
    }
    header_params = {
        'X-GDC-VALIDATE-RELATIONS': False,
    }
    try:
        # Get all Plugins
        api_response = api_instance.get_all_entities_dashboard_plugins(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PluginsApi->get_all_entities_dashboard_plugins: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
header_params | RequestHeaderParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
origin | OriginSchema | | optional
filter | FilterSchema | | optional
page | PageSchema | | optional
size | SizeSchema | | optional
sort | SortSchema | | optional
metaInclude | MetaIncludeSchema | | optional


# OriginSchema

Defines scope of origin of objects. All by default.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Defines scope of origin of objects. All by default. | must be one of ["ALL", "PARENTS", "NATIVE", ] if omitted the server will use the default value of "ALL"

# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# PageSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 0

# SizeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 20

# SortSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

# MetaIncludeSchema

Included meta objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Included meta objects | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["origin", "all", "ALL", ] 

### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
X-GDC-VALIDATE-RELATIONS | XGDCVALIDATERELATIONSSchema | | optional

# XGDCVALIDATERELATIONSSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bool,  | BoolClass,  |  | if omitted the server will use the default value of False

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_all_entities_dashboard_plugins.ApiResponseFor200) | Request successfully processed

#### get_all_entities_dashboard_plugins.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDashboardPluginOutList**](../../models/JsonApiDashboardPluginOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_dashboard_plugins**
<a id="get_entity_dashboard_plugins"></a>
> JsonApiDashboardPluginOutDocument get_entity_dashboard_plugins(workspace_idobject_id)

Get a Plugin

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import plugins_api
from gooddata_api_client.model.json_api_dashboard_plugin_out_document import JsonApiDashboardPluginOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plugins_api.PluginsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
    }
    header_params = {
    }
    try:
        # Get a Plugin
        api_response = api_instance.get_entity_dashboard_plugins(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PluginsApi->get_entity_dashboard_plugins: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
        'filter': "filter=title==someString;description==someString",
        'metaInclude': [
        "metaInclude=origin,all"
    ],
    }
    header_params = {
        'X-GDC-VALIDATE-RELATIONS': False,
    }
    try:
        # Get a Plugin
        api_response = api_instance.get_entity_dashboard_plugins(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PluginsApi->get_entity_dashboard_plugins: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
header_params | RequestHeaderParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
metaInclude | MetaIncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# MetaIncludeSchema

Included meta objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Included meta objects | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["origin", "all", "ALL", ] 

### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
X-GDC-VALIDATE-RELATIONS | XGDCVALIDATERELATIONSSchema | | optional

# XGDCVALIDATERELATIONSSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bool,  | BoolClass,  |  | if omitted the server will use the default value of False

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 
objectId | ObjectIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# ObjectIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_entity_dashboard_plugins.ApiResponseFor200) | Request successfully processed

#### get_entity_dashboard_plugins.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDashboardPluginOutDocument**](../../models/JsonApiDashboardPluginOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **patch_entity_dashboard_plugins**
<a id="patch_entity_dashboard_plugins"></a>
> JsonApiDashboardPluginOutDocument patch_entity_dashboard_plugins(workspace_idobject_idjson_api_dashboard_plugin_patch_document)

Patch a Plugin

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import plugins_api
from gooddata_api_client.model.json_api_dashboard_plugin_out_document import JsonApiDashboardPluginOutDocument
from gooddata_api_client.model.json_api_dashboard_plugin_patch_document import JsonApiDashboardPluginPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plugins_api.PluginsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
    }
    body = JsonApiDashboardPluginPatchDocument(
        data=JsonApiDashboardPluginPatch(
            attributes=dict(
                are_relations_valid=True,
                content=dict(),
                description="description_example",
                tags=[
                    "tags_example"
                ],
                title="title_example",
            ),
            id="id1",
            type="dashboardPlugin",
        ),
    )
    try:
        # Patch a Plugin
        api_response = api_instance.patch_entity_dashboard_plugins(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PluginsApi->patch_entity_dashboard_plugins: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
        'filter': "filter=title==someString;description==someString",
    }
    body = JsonApiDashboardPluginPatchDocument(
        data=JsonApiDashboardPluginPatch(
            attributes=dict(
                are_relations_valid=True,
                content=dict(),
                description="description_example",
                tags=[
                    "tags_example"
                ],
                title="title_example",
            ),
            id="id1",
            type="dashboardPlugin",
        ),
    )
    try:
        # Patch a Plugin
        api_response = api_instance.patch_entity_dashboard_plugins(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PluginsApi->patch_entity_dashboard_plugins: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDashboardPluginPatchDocument**](../../models/JsonApiDashboardPluginPatchDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 
objectId | ObjectIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# ObjectIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#patch_entity_dashboard_plugins.ApiResponseFor200) | Request successfully processed

#### patch_entity_dashboard_plugins.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDashboardPluginOutDocument**](../../models/JsonApiDashboardPluginOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_entity_dashboard_plugins**
<a id="update_entity_dashboard_plugins"></a>
> JsonApiDashboardPluginOutDocument update_entity_dashboard_plugins(workspace_idobject_idjson_api_dashboard_plugin_in_document)

Put a Plugin

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import plugins_api
from gooddata_api_client.model.json_api_dashboard_plugin_out_document import JsonApiDashboardPluginOutDocument
from gooddata_api_client.model.json_api_dashboard_plugin_in_document import JsonApiDashboardPluginInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plugins_api.PluginsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
    }
    body = JsonApiDashboardPluginInDocument(
        data=JsonApiDashboardPluginIn(
            attributes=dict(
                are_relations_valid=True,
                content=dict(),
                description="description_example",
                tags=[
                    "tags_example"
                ],
                title="title_example",
            ),
            id="id1",
            type="dashboardPlugin",
        ),
    )
    try:
        # Put a Plugin
        api_response = api_instance.update_entity_dashboard_plugins(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PluginsApi->update_entity_dashboard_plugins: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
        'filter': "filter=title==someString;description==someString",
    }
    body = JsonApiDashboardPluginInDocument(
        data=JsonApiDashboardPluginIn(
            attributes=dict(
                are_relations_valid=True,
                content=dict(),
                description="description_example",
                tags=[
                    "tags_example"
                ],
                title="title_example",
            ),
            id="id1",
            type="dashboardPlugin",
        ),
    )
    try:
        # Put a Plugin
        api_response = api_instance.update_entity_dashboard_plugins(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PluginsApi->update_entity_dashboard_plugins: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDashboardPluginInDocument**](../../models/JsonApiDashboardPluginInDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 
objectId | ObjectIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# ObjectIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_entity_dashboard_plugins.ApiResponseFor200) | Request successfully processed

#### update_entity_dashboard_plugins.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDashboardPluginOutDocument**](../../models/JsonApiDashboardPluginOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


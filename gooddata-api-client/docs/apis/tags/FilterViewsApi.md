<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.filter_views_api.FilterViewsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_filter_views**](#create_entity_filter_views) | **post** /api/v1/entities/workspaces/{workspaceId}/filterViews | Post Filter views
[**delete_entity_filter_views**](#delete_entity_filter_views) | **delete** /api/v1/entities/workspaces/{workspaceId}/filterViews/{objectId} | Delete Filter view
[**get_all_entities_filter_views**](#get_all_entities_filter_views) | **get** /api/v1/entities/workspaces/{workspaceId}/filterViews | Get all Filter views
[**get_entity_filter_views**](#get_entity_filter_views) | **get** /api/v1/entities/workspaces/{workspaceId}/filterViews/{objectId} | Get Filter view
[**get_filter_views**](#get_filter_views) | **get** /api/v1/layout/workspaces/{workspaceId}/filterViews | Get filter views
[**patch_entity_filter_views**](#patch_entity_filter_views) | **patch** /api/v1/entities/workspaces/{workspaceId}/filterViews/{objectId} | Patch Filter view
[**search_entities_filter_views**](#search_entities_filter_views) | **post** /api/v1/entities/workspaces/{workspaceId}/filterViews/search | Search request for FilterView
[**set_filter_views**](#set_filter_views) | **put** /api/v1/layout/workspaces/{workspaceId}/filterViews | Set filter views
[**update_entity_filter_views**](#update_entity_filter_views) | **put** /api/v1/entities/workspaces/{workspaceId}/filterViews/{objectId} | Put Filter views

# **create_entity_filter_views**
<a id="create_entity_filter_views"></a>
> JsonApiFilterViewOutDocument create_entity_filter_views(workspace_idjson_api_filter_view_in_document)

Post Filter views

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import filter_views_api
from gooddata_api_client.model.json_api_filter_view_in_document import JsonApiFilterViewInDocument
from gooddata_api_client.model.json_api_filter_view_out_document import JsonApiFilterViewOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = filter_views_api.FilterViewsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
    }
    body = JsonApiFilterViewInDocument(
        data=JsonApiFilterViewIn(
            attributes=dict(
                are_relations_valid=True,
                content=dict(),
                description="description_example",
                is_default=True,
                tags=[
                    "tags_example"
                ],
                title="title_example",
            ),
            id="id1",
            relationships=dict(
                analytical_dashboard=dict(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                user=dict(
                    data=JsonApiUserToOneLinkage(None),
                ),
            ),
            type="filterView",
        ),
    )
    try:
        # Post Filter views
        api_response = api_instance.create_entity_filter_views(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->create_entity_filter_views: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
        'include': [
        "analyticalDashboard,user"
    ],
    }
    body = JsonApiFilterViewInDocument(
        data=JsonApiFilterViewIn(
            attributes=dict(
                are_relations_valid=True,
                content=dict(),
                description="description_example",
                is_default=True,
                tags=[
                    "tags_example"
                ],
                title="title_example",
            ),
            id="id1",
            relationships=dict(
                analytical_dashboard=dict(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                user=dict(
                    data=JsonApiUserToOneLinkage(None),
                ),
            ),
            type="filterView",
        ),
    )
    try:
        # Post Filter views
        api_response = api_instance.create_entity_filter_views(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->create_entity_filter_views: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiFilterViewInDocument**](../../models/JsonApiFilterViewInDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiFilterViewInDocument**](../../models/JsonApiFilterViewInDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
include | IncludeSchema | | optional


# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["analyticalDashboards", "users", "analyticalDashboard", "user", "ALL", ] 

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
201 | [ApiResponseFor201](#create_entity_filter_views.ApiResponseFor201) | Request successfully processed

#### create_entity_filter_views.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationJson, SchemaFor201ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiFilterViewOutDocument**](../../models/JsonApiFilterViewOutDocument.md) |  | 


# SchemaFor201ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiFilterViewOutDocument**](../../models/JsonApiFilterViewOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_entity_filter_views**
<a id="delete_entity_filter_views"></a>
> delete_entity_filter_views(workspace_idobject_id)

Delete Filter view

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import filter_views_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = filter_views_api.FilterViewsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
    }
    try:
        # Delete Filter view
        api_response = api_instance.delete_entity_filter_views(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->delete_entity_filter_views: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
        'filter': "title==someString;description==someString;analyticalDashboard.id==321;user.id==321",
    }
    try:
        # Delete Filter view
        api_response = api_instance.delete_entity_filter_views(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->delete_entity_filter_views: %s\n" % e)
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
204 | [ApiResponseFor204](#delete_entity_filter_views.ApiResponseFor204) | Successfully deleted

#### delete_entity_filter_views.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_filter_views**
<a id="get_all_entities_filter_views"></a>
> JsonApiFilterViewOutList get_all_entities_filter_views(workspace_id)

Get all Filter views

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import filter_views_api
from gooddata_api_client.model.json_api_filter_view_out_list import JsonApiFilterViewOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = filter_views_api.FilterViewsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
    }
    header_params = {
    }
    try:
        # Get all Filter views
        api_response = api_instance.get_all_entities_filter_views(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->get_all_entities_filter_views: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
        'origin': "ALL",
        'filter': "title==someString;description==someString;analyticalDashboard.id==321;user.id==321",
        'include': [
        "analyticalDashboard,user"
    ],
        'page': 0,
        'size': 20,
        'sort': [
        "sort_example"
    ],
        'metaInclude': [
        "metaInclude=page,all"
    ],
    }
    header_params = {
        'X-GDC-VALIDATE-RELATIONS': False,
    }
    try:
        # Get all Filter views
        api_response = api_instance.get_all_entities_filter_views(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->get_all_entities_filter_views: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
header_params | RequestHeaderParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
origin | OriginSchema | | optional
filter | FilterSchema | | optional
include | IncludeSchema | | optional
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

# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["analyticalDashboards", "users", "analyticalDashboard", "user", "ALL", ] 

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
items | str,  | str,  |  | must be one of ["page", "all", "ALL", ] 

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
200 | [ApiResponseFor200](#get_all_entities_filter_views.ApiResponseFor200) | Request successfully processed

#### get_all_entities_filter_views.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiFilterViewOutList**](../../models/JsonApiFilterViewOutList.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiFilterViewOutList**](../../models/JsonApiFilterViewOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_filter_views**
<a id="get_entity_filter_views"></a>
> JsonApiFilterViewOutDocument get_entity_filter_views(workspace_idobject_id)

Get Filter view

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import filter_views_api
from gooddata_api_client.model.json_api_filter_view_out_document import JsonApiFilterViewOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = filter_views_api.FilterViewsApi(api_client)

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
        # Get Filter view
        api_response = api_instance.get_entity_filter_views(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->get_entity_filter_views: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
        'filter': "title==someString;description==someString;analyticalDashboard.id==321;user.id==321",
        'include': [
        "analyticalDashboard,user"
    ],
    }
    header_params = {
        'X-GDC-VALIDATE-RELATIONS': False,
    }
    try:
        # Get Filter view
        api_response = api_instance.get_entity_filter_views(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->get_entity_filter_views: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
header_params | RequestHeaderParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
include | IncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["analyticalDashboards", "users", "analyticalDashboard", "user", "ALL", ] 

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
200 | [ApiResponseFor200](#get_entity_filter_views.ApiResponseFor200) | Request successfully processed

#### get_entity_filter_views.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiFilterViewOutDocument**](../../models/JsonApiFilterViewOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiFilterViewOutDocument**](../../models/JsonApiFilterViewOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_filter_views**
<a id="get_filter_views"></a>
> [DeclarativeFilterView] get_filter_views(workspace_id)

Get filter views

Retrieve filter views for the specific workspace

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import filter_views_api
from gooddata_api_client.model.declarative_filter_view import DeclarativeFilterView
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = filter_views_api.FilterViewsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
    }
    try:
        # Get filter views
        api_response = api_instance.get_filter_views(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->get_filter_views: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
        'exclude': [
        "ACTIVITY_INFO"
    ],
    }
    try:
        # Get filter views
        api_response = api_instance.get_filter_views(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->get_filter_views: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
exclude | ExcludeSchema | | optional


# ExcludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  | Defines properties which should not be included in the payload. | must be one of ["ACTIVITY_INFO", ] 

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
200 | [ApiResponseFor200](#get_filter_views.ApiResponseFor200) | Retrieved filterViews.

#### get_filter_views.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeFilterView**]({{complexTypePrefix}}DeclarativeFilterView.md) | [**DeclarativeFilterView**]({{complexTypePrefix}}DeclarativeFilterView.md) | [**DeclarativeFilterView**]({{complexTypePrefix}}DeclarativeFilterView.md) |  | 

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **patch_entity_filter_views**
<a id="patch_entity_filter_views"></a>
> JsonApiFilterViewOutDocument patch_entity_filter_views(workspace_idobject_idjson_api_filter_view_patch_document)

Patch Filter view

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import filter_views_api
from gooddata_api_client.model.json_api_filter_view_patch_document import JsonApiFilterViewPatchDocument
from gooddata_api_client.model.json_api_filter_view_out_document import JsonApiFilterViewOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = filter_views_api.FilterViewsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
    }
    body = JsonApiFilterViewPatchDocument(
        data=JsonApiFilterViewPatch(
            attributes=dict(
                are_relations_valid=True,
                content=dict(),
                description="description_example",
                is_default=True,
                tags=[
                    "tags_example"
                ],
                title="title_example",
            ),
            id="id1",
            relationships=dict(
                analytical_dashboard=dict(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                user=dict(
                    data=JsonApiUserToOneLinkage(None),
                ),
            ),
            type="filterView",
        ),
    )
    try:
        # Patch Filter view
        api_response = api_instance.patch_entity_filter_views(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->patch_entity_filter_views: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
        'filter': "title==someString;description==someString;analyticalDashboard.id==321;user.id==321",
        'include': [
        "analyticalDashboard,user"
    ],
    }
    body = JsonApiFilterViewPatchDocument(
        data=JsonApiFilterViewPatch(
            attributes=dict(
                are_relations_valid=True,
                content=dict(),
                description="description_example",
                is_default=True,
                tags=[
                    "tags_example"
                ],
                title="title_example",
            ),
            id="id1",
            relationships=dict(
                analytical_dashboard=dict(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                user=dict(
                    data=JsonApiUserToOneLinkage(None),
                ),
            ),
            type="filterView",
        ),
    )
    try:
        # Patch Filter view
        api_response = api_instance.patch_entity_filter_views(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->patch_entity_filter_views: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiFilterViewPatchDocument**](../../models/JsonApiFilterViewPatchDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiFilterViewPatchDocument**](../../models/JsonApiFilterViewPatchDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
include | IncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["analyticalDashboards", "users", "analyticalDashboard", "user", "ALL", ] 

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
200 | [ApiResponseFor200](#patch_entity_filter_views.ApiResponseFor200) | Request successfully processed

#### patch_entity_filter_views.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiFilterViewOutDocument**](../../models/JsonApiFilterViewOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiFilterViewOutDocument**](../../models/JsonApiFilterViewOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **search_entities_filter_views**
<a id="search_entities_filter_views"></a>
> JsonApiFilterViewOutList search_entities_filter_views(workspace_identity_search_body)

Search request for FilterView

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import filter_views_api
from gooddata_api_client.model.json_api_filter_view_out_list import JsonApiFilterViewOutList
from gooddata_api_client.model.entity_search_body import EntitySearchBody
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = filter_views_api.FilterViewsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
    }
    header_params = {
    }
    body = EntitySearchBody(
        filter="filter_example",
        include=[
            "include_example"
        ],
        meta_include=[
            "meta_include_example"
        ],
        page=EntitySearchPage(
            index=0,
            size=100,
        ),
        sort=[
            EntitySearchSort(
                direction="ASC",
                _property="_property_example",
            )
        ],
    )
    try:
        # Search request for FilterView
        api_response = api_instance.search_entities_filter_views(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->search_entities_filter_views: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
        'origin': "ALL",
    }
    header_params = {
        'X-GDC-VALIDATE-RELATIONS': False,
    }
    body = EntitySearchBody(
        filter="filter_example",
        include=[
            "include_example"
        ],
        meta_include=[
            "meta_include_example"
        ],
        page=EntitySearchPage(
            index=0,
            size=100,
        ),
        sort=[
            EntitySearchSort(
                direction="ASC",
                _property="_property_example",
            )
        ],
    )
    try:
        # Search request for FilterView
        api_response = api_instance.search_entities_filter_views(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->search_entities_filter_views: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
query_params | RequestQueryParams | |
header_params | RequestHeaderParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**EntitySearchBody**](../../models/EntitySearchBody.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
origin | OriginSchema | | optional


# OriginSchema

Defines scope of origin of objects. All by default.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Defines scope of origin of objects. All by default. | must be one of ["ALL", "PARENTS", "NATIVE", ] if omitted the server will use the default value of "ALL"

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
200 | [ApiResponseFor200](#search_entities_filter_views.ApiResponseFor200) | Request successfully processed

#### search_entities_filter_views.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiFilterViewOutList**](../../models/JsonApiFilterViewOutList.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiFilterViewOutList**](../../models/JsonApiFilterViewOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **set_filter_views**
<a id="set_filter_views"></a>
> set_filter_views(workspace_iddeclarative_filter_view)

Set filter views

Set filter views for the specific workspace.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import filter_views_api
from gooddata_api_client.model.declarative_filter_view import DeclarativeFilterView
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = filter_views_api.FilterViewsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    body = [
        DeclarativeFilterView(
            analytical_dashboard=DeclarativeAnalyticalDashboardIdentifier(
                id="dashboard123",
                type="analyticalDashboard",
            ),
            content=JsonNode(),
            description="description_example",
            id="filterView-1",
            is_default=True,
            tags=[
                "[\"Revenue\",\"Sales\"]"
            ],
            title="title_example",
            user=DeclarativeUserIdentifier(
                id="employee123",
                type="user",
            ),
        )
    ]
    try:
        # Set filter views
        api_response = api_instance.set_filter_views(
            path_params=path_params,
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->set_filter_views: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeFilterView**]({{complexTypePrefix}}DeclarativeFilterView.md) | [**DeclarativeFilterView**]({{complexTypePrefix}}DeclarativeFilterView.md) | [**DeclarativeFilterView**]({{complexTypePrefix}}DeclarativeFilterView.md) |  | 

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
204 | [ApiResponseFor204](#set_filter_views.ApiResponseFor204) | FilterViews successfully set.

#### set_filter_views.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_entity_filter_views**
<a id="update_entity_filter_views"></a>
> JsonApiFilterViewOutDocument update_entity_filter_views(workspace_idobject_idjson_api_filter_view_in_document)

Put Filter views

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import filter_views_api
from gooddata_api_client.model.json_api_filter_view_in_document import JsonApiFilterViewInDocument
from gooddata_api_client.model.json_api_filter_view_out_document import JsonApiFilterViewOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = filter_views_api.FilterViewsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
    }
    body = JsonApiFilterViewInDocument(
        data=JsonApiFilterViewIn(
            attributes=dict(
                are_relations_valid=True,
                content=dict(),
                description="description_example",
                is_default=True,
                tags=[
                    "tags_example"
                ],
                title="title_example",
            ),
            id="id1",
            relationships=dict(
                analytical_dashboard=dict(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                user=dict(
                    data=JsonApiUserToOneLinkage(None),
                ),
            ),
            type="filterView",
        ),
    )
    try:
        # Put Filter views
        api_response = api_instance.update_entity_filter_views(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->update_entity_filter_views: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
        'filter': "title==someString;description==someString;analyticalDashboard.id==321;user.id==321",
        'include': [
        "analyticalDashboard,user"
    ],
    }
    body = JsonApiFilterViewInDocument(
        data=JsonApiFilterViewIn(
            attributes=dict(
                are_relations_valid=True,
                content=dict(),
                description="description_example",
                is_default=True,
                tags=[
                    "tags_example"
                ],
                title="title_example",
            ),
            id="id1",
            relationships=dict(
                analytical_dashboard=dict(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                user=dict(
                    data=JsonApiUserToOneLinkage(None),
                ),
            ),
            type="filterView",
        ),
    )
    try:
        # Put Filter views
        api_response = api_instance.update_entity_filter_views(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->update_entity_filter_views: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiFilterViewInDocument**](../../models/JsonApiFilterViewInDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiFilterViewInDocument**](../../models/JsonApiFilterViewInDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
include | IncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["analyticalDashboards", "users", "analyticalDashboard", "user", "ALL", ] 

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
200 | [ApiResponseFor200](#update_entity_filter_views.ApiResponseFor200) | Request successfully processed

#### update_entity_filter_views.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiFilterViewOutDocument**](../../models/JsonApiFilterViewOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiFilterViewOutDocument**](../../models/JsonApiFilterViewOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


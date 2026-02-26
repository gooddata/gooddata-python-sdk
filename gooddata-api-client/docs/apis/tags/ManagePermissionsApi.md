<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.manage_permissions_api.ManagePermissionsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_data_source_permissions**](#get_data_source_permissions) | **get** /api/v1/layout/dataSources/{dataSourceId}/permissions | Get permissions for the data source
[**manage_data_source_permissions**](#manage_data_source_permissions) | **post** /api/v1/actions/dataSources/{dataSourceId}/managePermissions | Manage Permissions for a Data Source
[**set_data_source_permissions**](#set_data_source_permissions) | **put** /api/v1/layout/dataSources/{dataSourceId}/permissions | Set data source permissions.

# **get_data_source_permissions**
<a id="get_data_source_permissions"></a>
> DeclarativeDataSourcePermissions get_data_source_permissions(data_source_id)

Get permissions for the data source

Retrieve current set of permissions of the data source in a declarative form.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import manage_permissions_api
from gooddata_api_client.model.declarative_data_source_permissions import DeclarativeDataSourcePermissions
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = manage_permissions_api.ManagePermissionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'dataSourceId': "dataSourceId_example",
    }
    try:
        # Get permissions for the data source
        api_response = api_instance.get_data_source_permissions(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ManagePermissionsApi->get_data_source_permissions: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
dataSourceId | DataSourceIdSchema | | 

# DataSourceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_data_source_permissions.ApiResponseFor200) | Retrieved current set of permissions.

#### get_data_source_permissions.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeDataSourcePermissions**](../../models/DeclarativeDataSourcePermissions.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **manage_data_source_permissions**
<a id="manage_data_source_permissions"></a>
> manage_data_source_permissions(data_source_iddata_source_permission_assignment)

Manage Permissions for a Data Source

Manage Permissions for a Data Source

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import manage_permissions_api
from gooddata_api_client.model.data_source_permission_assignment import DataSourcePermissionAssignment
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = manage_permissions_api.ManagePermissionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'dataSourceId': "dataSourceId_example",
    }
    body = [
        DataSourcePermissionAssignment(
            assignee_identifier=AssigneeIdentifier(
                id="id_example",
                type="user",
            ),
            permissions=[
                "MANAGE"
            ],
        )
    ]
    try:
        # Manage Permissions for a Data Source
        api_response = api_instance.manage_data_source_permissions(
            path_params=path_params,
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ManagePermissionsApi->manage_data_source_permissions: %s\n" % e)
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

An array of data source permissions assignments

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | An array of data source permissions assignments | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DataSourcePermissionAssignment**]({{complexTypePrefix}}DataSourcePermissionAssignment.md) | [**DataSourcePermissionAssignment**]({{complexTypePrefix}}DataSourcePermissionAssignment.md) | [**DataSourcePermissionAssignment**]({{complexTypePrefix}}DataSourcePermissionAssignment.md) |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
dataSourceId | DataSourceIdSchema | | 

# DataSourceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#manage_data_source_permissions.ApiResponseFor204) | No Content

#### manage_data_source_permissions.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **set_data_source_permissions**
<a id="set_data_source_permissions"></a>
> set_data_source_permissions(data_source_iddeclarative_data_source_permissions)

Set data source permissions.

set data source permissions.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import manage_permissions_api
from gooddata_api_client.model.declarative_data_source_permissions import DeclarativeDataSourcePermissions
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = manage_permissions_api.ManagePermissionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'dataSourceId': "dataSourceId_example",
    }
    body = DeclarativeDataSourcePermissions(
        permissions=[
            DeclarativeDataSourcePermission(
                assignee=AssigneeIdentifier(
                    id="id_example",
                    type="user",
                ),
                name="MANAGE",
            )
        ],
    )
    try:
        # Set data source permissions.
        api_response = api_instance.set_data_source_permissions(
            path_params=path_params,
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ManagePermissionsApi->set_data_source_permissions: %s\n" % e)
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
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeDataSourcePermissions**](../../models/DeclarativeDataSourcePermissions.md) |  | 


### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
dataSourceId | DataSourceIdSchema | | 

# DataSourceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#set_data_source_permissions.ApiResponseFor204) | No Content

#### set_data_source_permissions.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.layout_api.LayoutApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_analytics_model**](#get_analytics_model) | **get** /api/v1/layout/workspaces/{workspaceId}/analyticsModel | Get analytics model
[**get_data_sources_layout**](#get_data_sources_layout) | **get** /api/v1/layout/dataSources | Get all data sources
[**get_logical_model**](#get_logical_model) | **get** /api/v1/layout/workspaces/{workspaceId}/logicalModel | Get logical model
[**get_organization_layout**](#get_organization_layout) | **get** /api/v1/layout/organization | Get organization layout
[**get_pdm_layout**](#get_pdm_layout) | **get** /api/v1/layout/dataSources/{dataSourceId}/physicalModel | Get data source physical model layout
[**get_user_data_filters**](#get_user_data_filters) | **get** /api/v1/layout/workspaces/{workspaceId}/userDataFilters | Get user data filters
[**get_user_group_permissions**](#get_user_group_permissions) | **get** /api/v1/layout/userGroups/{userGroupId}/permissions | Get permissions for the user-group
[**get_user_groups_layout**](#get_user_groups_layout) | **get** /api/v1/layout/userGroups | Get all user groups
[**get_user_permissions**](#get_user_permissions) | **get** /api/v1/layout/users/{userId}/permissions | Get permissions for the user
[**get_users_layout**](#get_users_layout) | **get** /api/v1/layout/users | Get all users
[**get_users_user_groups_layout**](#get_users_user_groups_layout) | **get** /api/v1/layout/usersAndUserGroups | Get all users and user groups
[**get_workspace_data_filters_layout**](#get_workspace_data_filters_layout) | **get** /api/v1/layout/workspaceDataFilters | Get workspace data filters for all workspaces
[**get_workspace_layout**](#get_workspace_layout) | **get** /api/v1/layout/workspaces/{workspaceId} | Get workspace layout
[**get_workspace_permissions**](#get_workspace_permissions) | **get** /api/v1/layout/workspaces/{workspaceId}/permissions | Get permissions for the workspace
[**get_workspaces_layout**](#get_workspaces_layout) | **get** /api/v1/layout/workspaces | Get all workspaces layout
[**put_data_sources_layout**](#put_data_sources_layout) | **put** /api/v1/layout/dataSources | Put all data sources
[**put_user_groups_layout**](#put_user_groups_layout) | **put** /api/v1/layout/userGroups | Put all user groups
[**put_users_layout**](#put_users_layout) | **put** /api/v1/layout/users | Put all users
[**put_users_user_groups_layout**](#put_users_user_groups_layout) | **put** /api/v1/layout/usersAndUserGroups | Put all users and user groups
[**put_workspace_layout**](#put_workspace_layout) | **put** /api/v1/layout/workspaces/{workspaceId} | Set workspace layout
[**set_analytics_model**](#set_analytics_model) | **put** /api/v1/layout/workspaces/{workspaceId}/analyticsModel | Set analytics model
[**set_logical_model**](#set_logical_model) | **put** /api/v1/layout/workspaces/{workspaceId}/logicalModel | Set logical model
[**set_organization_layout**](#set_organization_layout) | **put** /api/v1/layout/organization | Set organization layout
[**set_pdm_layout**](#set_pdm_layout) | **put** /api/v1/layout/dataSources/{dataSourceId}/physicalModel | Set data source physical model layout
[**set_user_data_filters**](#set_user_data_filters) | **put** /api/v1/layout/workspaces/{workspaceId}/userDataFilters | Set user data filters
[**set_user_group_permissions**](#set_user_group_permissions) | **put** /api/v1/layout/userGroups/{userGroupId}/permissions | Set permissions for the user-group
[**set_user_permissions**](#set_user_permissions) | **put** /api/v1/layout/users/{userId}/permissions | Set permissions for the user
[**set_workspace_data_filters_layout**](#set_workspace_data_filters_layout) | **put** /api/v1/layout/workspaceDataFilters | Set all workspace data filters
[**set_workspace_permissions**](#set_workspace_permissions) | **put** /api/v1/layout/workspaces/{workspaceId}/permissions | Set permissions for the workspace
[**set_workspaces_layout**](#set_workspaces_layout) | **put** /api/v1/layout/workspaces | Set all workspaces layout

# **get_analytics_model**
<a id="get_analytics_model"></a>
> DeclarativeAnalytics get_analytics_model(workspace_id)

Get analytics model

Retrieve current analytics model of the workspace.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_analytics import DeclarativeAnalytics
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    try:
        # Get analytics model
        api_response = api_instance.get_analytics_model(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_analytics_model: %s\n" % e)
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
200 | [ApiResponseFor200](#get_analytics_model.ApiResponseFor200) | Retrieved current analytics model.

#### get_analytics_model.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeAnalytics**](../../models/DeclarativeAnalytics.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_data_sources_layout**
<a id="get_data_sources_layout"></a>
> DeclarativeDataSources get_data_sources_layout()

Get all data sources

Retrieve all data sources including related physical model.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_data_sources import DeclarativeDataSources
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get all data sources
        api_response = api_instance.get_data_sources_layout()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_data_sources_layout: %s\n" % e)
```
### Parameters
This endpoint does not need any parameter.

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_data_sources_layout.ApiResponseFor200) | Retrieved all data sources.

#### get_data_sources_layout.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeDataSources**](../../models/DeclarativeDataSources.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_logical_model**
<a id="get_logical_model"></a>
> DeclarativeModel get_logical_model(workspace_id)

Get logical model

Retrieve current logical model of the workspace in declarative form.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_model import DeclarativeModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
    }
    try:
        # Get logical model
        api_response = api_instance.get_logical_model(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_logical_model: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
        'includeParents': True,
    }
    try:
        # Get logical model
        api_response = api_instance.get_logical_model(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_logical_model: %s\n" % e)
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
includeParents | IncludeParentsSchema | | optional


# IncludeParentsSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bool,  | BoolClass,  |  | 

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
200 | [ApiResponseFor200](#get_logical_model.ApiResponseFor200) | Retrieved current logical model.

#### get_logical_model.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeModel**](../../models/DeclarativeModel.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_organization_layout**
<a id="get_organization_layout"></a>
> DeclarativeOrganization get_organization_layout()

Get organization layout

Retrieve complete layout of organization, workspaces, user-groups, etc.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_organization import DeclarativeOrganization
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get organization layout
        api_response = api_instance.get_organization_layout()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_organization_layout: %s\n" % e)
```
### Parameters
This endpoint does not need any parameter.

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_organization_layout.ApiResponseFor200) | Retrieved all parts of an organization.

#### get_organization_layout.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeOrganization**](../../models/DeclarativeOrganization.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_pdm_layout**
<a id="get_pdm_layout"></a>
> DeclarativePdm get_pdm_layout(data_source_id)

Get data source physical model layout

Retrieve complete layout of tables with their columns

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_pdm import DeclarativePdm
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'dataSourceId': "dataSourceId_example",
    }
    try:
        # Get data source physical model layout
        api_response = api_instance.get_pdm_layout(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_pdm_layout: %s\n" % e)
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
200 | [ApiResponseFor200](#get_pdm_layout.ApiResponseFor200) | Retrieved data source physical mode layout.

#### get_pdm_layout.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativePdm**](../../models/DeclarativePdm.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_user_data_filters**
<a id="get_user_data_filters"></a>
> DeclarativeUserDataFilters get_user_data_filters(workspace_id)

Get user data filters

Retrieve current user data filters assigned to the workspace.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_user_data_filters import DeclarativeUserDataFilters
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    try:
        # Get user data filters
        api_response = api_instance.get_user_data_filters(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_user_data_filters: %s\n" % e)
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
200 | [ApiResponseFor200](#get_user_data_filters.ApiResponseFor200) | Retrieved current user data filters.

#### get_user_data_filters.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeUserDataFilters**](../../models/DeclarativeUserDataFilters.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_user_group_permissions**
<a id="get_user_group_permissions"></a>
> DeclarativeUserGroupPermissions get_user_group_permissions(user_group_id)

Get permissions for the user-group

Retrieve current set of permissions of the user-group in a declarative form.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_user_group_permissions import DeclarativeUserGroupPermissions
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'userGroupId': "userGroupId_example",
    }
    try:
        # Get permissions for the user-group
        api_response = api_instance.get_user_group_permissions(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_user_group_permissions: %s\n" % e)
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
userGroupId | UserGroupIdSchema | | 

# UserGroupIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_user_group_permissions.ApiResponseFor200) | Retrieved current set of permissions.

#### get_user_group_permissions.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeUserGroupPermissions**](../../models/DeclarativeUserGroupPermissions.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_user_groups_layout**
<a id="get_user_groups_layout"></a>
> DeclarativeUserGroups get_user_groups_layout()

Get all user groups

Retrieve all user-groups eventually with parent group.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_user_groups import DeclarativeUserGroups
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get all user groups
        api_response = api_instance.get_user_groups_layout()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_user_groups_layout: %s\n" % e)
```
### Parameters
This endpoint does not need any parameter.

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_user_groups_layout.ApiResponseFor200) | Retrieved all user groups.

#### get_user_groups_layout.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeUserGroups**](../../models/DeclarativeUserGroups.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_user_permissions**
<a id="get_user_permissions"></a>
> DeclarativeUserPermissions get_user_permissions(user_id)

Get permissions for the user

Retrieve current set of permissions of the user in a declarative form.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_user_permissions import DeclarativeUserPermissions
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'userId': "userId_example",
    }
    try:
        # Get permissions for the user
        api_response = api_instance.get_user_permissions(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_user_permissions: %s\n" % e)
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
userId | UserIdSchema | | 

# UserIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_user_permissions.ApiResponseFor200) | Retrieved current set of permissions.

#### get_user_permissions.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeUserPermissions**](../../models/DeclarativeUserPermissions.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_users_layout**
<a id="get_users_layout"></a>
> DeclarativeUsers get_users_layout()

Get all users

Retrieve all users including authentication properties.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_users import DeclarativeUsers
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get all users
        api_response = api_instance.get_users_layout()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_users_layout: %s\n" % e)
```
### Parameters
This endpoint does not need any parameter.

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_users_layout.ApiResponseFor200) | Retrieved all users.

#### get_users_layout.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeUsers**](../../models/DeclarativeUsers.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_users_user_groups_layout**
<a id="get_users_user_groups_layout"></a>
> DeclarativeUsersUserGroups get_users_user_groups_layout()

Get all users and user groups

Retrieve all users and user groups with theirs properties.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_users_user_groups import DeclarativeUsersUserGroups
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get all users and user groups
        api_response = api_instance.get_users_user_groups_layout()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_users_user_groups_layout: %s\n" % e)
```
### Parameters
This endpoint does not need any parameter.

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_users_user_groups_layout.ApiResponseFor200) | Retrieved all users and user groups.

#### get_users_user_groups_layout.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeUsersUserGroups**](../../models/DeclarativeUsersUserGroups.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_workspace_data_filters_layout**
<a id="get_workspace_data_filters_layout"></a>
> DeclarativeWorkspaceDataFilters get_workspace_data_filters_layout()

Get workspace data filters for all workspaces

Retrieve all workspaces and related workspace data filters (and their settings / values).

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_workspace_data_filters import DeclarativeWorkspaceDataFilters
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get workspace data filters for all workspaces
        api_response = api_instance.get_workspace_data_filters_layout()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_workspace_data_filters_layout: %s\n" % e)
```
### Parameters
This endpoint does not need any parameter.

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_workspace_data_filters_layout.ApiResponseFor200) | Retrieved all workspace data filters.

#### get_workspace_data_filters_layout.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeWorkspaceDataFilters**](../../models/DeclarativeWorkspaceDataFilters.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_workspace_layout**
<a id="get_workspace_layout"></a>
> DeclarativeWorkspaceModel get_workspace_layout(workspace_id)

Get workspace layout

Retrieve current model of the workspace in declarative form.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_workspace_model import DeclarativeWorkspaceModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    try:
        # Get workspace layout
        api_response = api_instance.get_workspace_layout(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_workspace_layout: %s\n" % e)
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
200 | [ApiResponseFor200](#get_workspace_layout.ApiResponseFor200) | Retrieved the workspace model.

#### get_workspace_layout.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeWorkspaceModel**](../../models/DeclarativeWorkspaceModel.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_workspace_permissions**
<a id="get_workspace_permissions"></a>
> DeclarativeWorkspacePermissions get_workspace_permissions(workspace_id)

Get permissions for the workspace

Retrieve current set of permissions of the workspace in a declarative form.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_workspace_permissions import DeclarativeWorkspacePermissions
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    try:
        # Get permissions for the workspace
        api_response = api_instance.get_workspace_permissions(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_workspace_permissions: %s\n" % e)
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
200 | [ApiResponseFor200](#get_workspace_permissions.ApiResponseFor200) | Retrieved current set of permissions.

#### get_workspace_permissions.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeWorkspacePermissions**](../../models/DeclarativeWorkspacePermissions.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_workspaces_layout**
<a id="get_workspaces_layout"></a>
> DeclarativeWorkspaces get_workspaces_layout()

Get all workspaces layout

Gets complete layout of workspaces, their hierarchy, models.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_workspaces import DeclarativeWorkspaces
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get all workspaces layout
        api_response = api_instance.get_workspaces_layout()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_workspaces_layout: %s\n" % e)
```
### Parameters
This endpoint does not need any parameter.

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_workspaces_layout.ApiResponseFor200) | Retrieved layout of all workspaces.

#### get_workspaces_layout.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeWorkspaces**](../../models/DeclarativeWorkspaces.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **put_data_sources_layout**
<a id="put_data_sources_layout"></a>
> put_data_sources_layout(declarative_data_sources)

Put all data sources

Set all data sources including related physical model.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_data_sources import DeclarativeDataSources
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example passing only required values which don't have defaults set
    body = DeclarativeDataSources(
        data_sources=[
            DeclarativeDataSource(
                cache_path=[
                    "[ \"dfs\", \"data\" ]. Example used in Apache Drill."
                ],
                decoded_parameters=[
                    Parameter(
                        name="name_example",
                        value="value_example",
                    )
                ],
                enable_caching=False,
                id="pg_local_docker-demo",
                name="postgres demo",
,
                password="*****",
                pdm=DeclarativeTables(
                    tables=[
                        DeclarativeTable(
                            columns=[
                                DeclarativeColumn(
                                    data_type="INT",
                                    is_primary_key=True,
                                    name="customer_id",
                                    referenced_table_column="customer_id",
                                    referenced_table_id="customers",
                                )
                            ],
                            id="customers",
                            name_prefix="out_gooddata",
                            path=["table_schema","table_name"],
                            type="VIEW",
                        )
                    ],
                ),
                permissions=[
                    DeclarativeDataSourcePermission(
                        assignee=AssigneeIdentifier(
                            id="id_example",
                            type="user",
                        ),
                        name="MANAGE",
                    )
                ],
                schema="demo",
                token="Bigquery service account JSON. Encode it using base64!",
                type="POSTGRESQL",
                url="jdbc:postgresql://postgres:5432/gooddata",
                username="demo",
            )
        ],
    )
    try:
        # Put all data sources
        api_response = api_instance.put_data_sources_layout(
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->put_data_sources_layout: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeDataSources**](../../models/DeclarativeDataSources.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#put_data_sources_layout.ApiResponseFor200) | Defined all data sources.

#### put_data_sources_layout.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **put_user_groups_layout**
<a id="put_user_groups_layout"></a>
> put_user_groups_layout(declarative_user_groups)

Put all user groups

Define all user groups with their parents eventually.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_user_groups import DeclarativeUserGroups
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example passing only required values which don't have defaults set
    body = DeclarativeUserGroups(
        user_groups=[
            DeclarativeUserGroup(
                id="employees.all",
                name="admins",
                parents=[
                    UserGroupIdentifier(
                        id="group.admins",
                        type="userGroup",
                    )
                ],
                permissions=[
                    DeclarativeUserGroupPermission(
                        assignee=AssigneeIdentifier(
                            id="id_example",
                            type="user",
                        ),
                        name="SEE",
                    )
                ],
            )
        ],
    )
    try:
        # Put all user groups
        api_response = api_instance.put_user_groups_layout(
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->put_user_groups_layout: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeUserGroups**](../../models/DeclarativeUserGroups.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#put_user_groups_layout.ApiResponseFor200) | Defined all user groups.

#### put_user_groups_layout.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **put_users_layout**
<a id="put_users_layout"></a>
> put_users_layout(declarative_users)

Put all users

Set all users and their authentication properties.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_users import DeclarativeUsers
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example passing only required values which don't have defaults set
    body = DeclarativeUsers(
        users=[
            DeclarativeUser(
                auth_id="auth_id_example",
                email="user@example.com",
                firstname="John",
                id="employee123",
                lastname="Wick",
                permissions=[
                    DeclarativeUserPermission(
                        assignee=AssigneeIdentifier(
                            id="id_example",
                            type="user",
                        ),
                        name="SEE",
                    )
                ],
                settings=[
                    DeclarativeSetting(
                        content=dict(),
                        id="/6bUUGjjNSwg0_bs",
                        type="TIMEZONE",
                    )
                ],
                user_groups=[
                    UserGroupIdentifier(
                        id="group.admins",
                        type="userGroup",
                    )
                ],
            )
        ],
    )
    try:
        # Put all users
        api_response = api_instance.put_users_layout(
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->put_users_layout: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeUsers**](../../models/DeclarativeUsers.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#put_users_layout.ApiResponseFor200) | Defined all users.

#### put_users_layout.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **put_users_user_groups_layout**
<a id="put_users_user_groups_layout"></a>
> put_users_user_groups_layout(declarative_users_user_groups)

Put all users and user groups

Define all users and user groups with theirs properties.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_users_user_groups import DeclarativeUsersUserGroups
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example passing only required values which don't have defaults set
    body = DeclarativeUsersUserGroups(
        user_groups=[
            DeclarativeUserGroup(
                id="employees.all",
                name="admins",
                parents=[
                    UserGroupIdentifier(
                        id="group.admins",
                        type="userGroup",
                    )
                ],
                permissions=[
                    DeclarativeUserGroupPermission(
                        assignee=AssigneeIdentifier(
                            id="id_example",
                            type="user",
                        ),
                        name="SEE",
                    )
                ],
            )
        ],
        users=[
            DeclarativeUser(
                auth_id="auth_id_example",
                email="user@example.com",
                firstname="John",
                id="employee123",
                lastname="Wick",
                permissions=[
                    DeclarativeUserPermission(
                        assignee=AssigneeIdentifier(),
                        name="SEE",
                    )
                ],
                settings=[
                    DeclarativeSetting(
                        content=dict(),
                        id="/6bUUGjjNSwg0_bs",
                        type="TIMEZONE",
                    )
                ],
,
            )
        ],
    )
    try:
        # Put all users and user groups
        api_response = api_instance.put_users_user_groups_layout(
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->put_users_user_groups_layout: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeUsersUserGroups**](../../models/DeclarativeUsersUserGroups.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#put_users_user_groups_layout.ApiResponseFor200) | Defined all users and user groups.

#### put_users_user_groups_layout.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **put_workspace_layout**
<a id="put_workspace_layout"></a>
> put_workspace_layout(workspace_iddeclarative_workspace_model)

Set workspace layout

Set complete layout of workspace, like model, authorization, etc.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_workspace_model import DeclarativeWorkspaceModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    body = DeclarativeWorkspaceModel(
        analytics=DeclarativeAnalyticsLayer(
            analytical_dashboard_extensions=[
                DeclarativeAnalyticalDashboardExtension(
                    id="revenues-analysis",
                    permissions=[
                        DeclarativeAnalyticalDashboardPermission(
                            assignee=AssigneeIdentifier(
                                id="id_example",
                                type="user",
                            ),
                            name="EDIT",
                        )
                    ],
                )
            ],
            analytical_dashboards=[
                DeclarativeAnalyticalDashboard(
                    content=dict(),
                    description="Period to period comparison of revenues in main sectors.",
                    id="revenues-analysis",
,
                    tags=["Revenues"],
                    title="Revenues analysis",
                )
            ],
            dashboard_plugins=[
                DeclarativeDashboardPlugin(
                    content=dict(),
                    description="Three dimensional view of data.",
                    id="dashboard-plugin-1",
                    tags=["Revenues"],
                    title="3D map renderer",
                )
            ],
            filter_contexts=[
                DeclarativeFilterContext(
                    content=dict(),
                    description="Filter Context for Sales team.",
                    id="filter-sales",
                    tags=["Revenues"],
                    title="Filter Context for Sales team",
                )
            ],
            metrics=[
                DeclarativeMetric(
                    content=dict(),
                    description="Sales for all the data available.",
                    id="total-sales",
                    tags=["Revenues"],
                    title="Total sales",
                )
            ],
            visualization_objects=[
                DeclarativeVisualizationObject(
                    content=dict(),
                    description="Simple number for total goods in current production.",
                    id="visualization-1",
                    tags=["Revenues"],
                    title="Count of goods",
                )
            ],
        ),
        ldm=DeclarativeLdm(
            datasets=[
                DeclarativeDataset(
                    attributes=[
                        DeclarativeAttribute(
                            default_view=LabelIdentifier(
                                id="label_id",
                                type="label",
                            ),
                            description="Customer name including first and last name.",
                            id="attr.customers.customer_name",
                            labels=[
                                DeclarativeLabel(
                                    description="Customer name",
                                    id="label.customer_name",
                                    source_column="customer_name",
                                    source_column_data_type="STRING",
                                    tags=["Customers"],
                                    title="Customer name",
                                    value_type="\"TEXT\" | \"HYPERLINK\" | \"GEO\" | \"GEO_LONGITUDE\" | \"GEO_LATITUDE\"",
                                )
                            ],
                            sort_column="customer_name",
                            sort_direction="\"ASC\" | \"DESC\"",
                            source_column="customer_name",
                            source_column_data_type="STRING",
                            tags=["Customers"],
                            title="Customer Name",
                        )
                    ],
                    data_source_table_id=DataSourceTableIdentifier(
                        data_source_id="my-postgres",
                        id="customers",
                        type="dataSource",
                    ),
                    description="The customers of ours.",
                    facts=[
                        DeclarativeFact(
                            description="A number of orders created by the customer - including all orders, even the non-delivered ones.",
                            id="fact.customer_order_count",
                            source_column="customer_order_count",
                            source_column_data_type="NUMERIC",
                            tags=["Customers"],
                            title="Customer order count",
                        )
                    ],
                    grain=[
                        GrainIdentifier(
                            id="attr.customers.customer_name",
                            type="ATTRIBUTE",
                        )
                    ],
                    id="customers",
                    references=[
                        DeclarativeReference(
                            identifier=ReferenceIdentifier(
                                id="customers",
                                type="DATASET",
                            ),
                            multivalue=False,
                            source_column_data_types=[
                                "source_column_data_types_example"
                            ],
                            source_columns=["customer_id"],
                        )
                    ],
                    sql=DeclarativeDatasetSql(
                        data_source_id="my-postgres",
                        statement="SELECT * FROM some_table",
                    ),
                    tags=["Customers"],
                    title="Customers",
                    workspace_data_filter_columns=[
                        DeclarativeWorkspaceDataFilterColumn(
                            data_type="INT",
                            name="customer_id",
                        )
                    ],
                )
            ],
            date_instances=[
                DeclarativeDateDataset(
                    description="A customer order date",
                    granularities=[
                        "MINUTE"
                    ],
                    granularities_formatting=GranularitiesFormatting(
                        title_base="title_base_example",
                        title_pattern="%titleBase - %granularityTitle",
                    ),
                    id="date",
                    tags=["Customer dates"],
                    title="Date",
                )
            ],
        ),
    )
    try:
        # Set workspace layout
        api_response = api_instance.put_workspace_layout(
            path_params=path_params,
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->put_workspace_layout: %s\n" % e)
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
[**DeclarativeWorkspaceModel**](../../models/DeclarativeWorkspaceModel.md) |  | 


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
204 | [ApiResponseFor204](#put_workspace_layout.ApiResponseFor204) | The model of the workspace was set.

#### put_workspace_layout.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **set_analytics_model**
<a id="set_analytics_model"></a>
> set_analytics_model(workspace_iddeclarative_analytics)

Set analytics model

Set effective analytics model of the workspace.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_analytics import DeclarativeAnalytics
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    body = DeclarativeAnalytics(
        analytics=DeclarativeAnalyticsLayer(
            analytical_dashboard_extensions=[
                DeclarativeAnalyticalDashboardExtension(
                    id="revenues-analysis",
                    permissions=[
                        DeclarativeAnalyticalDashboardPermission(
                            assignee=AssigneeIdentifier(
                                id="id_example",
                                type="user",
                            ),
                            name="EDIT",
                        )
                    ],
                )
            ],
            analytical_dashboards=[
                DeclarativeAnalyticalDashboard(
                    content=dict(),
                    description="Period to period comparison of revenues in main sectors.",
                    id="revenues-analysis",
,
                    tags=["Revenues"],
                    title="Revenues analysis",
                )
            ],
            dashboard_plugins=[
                DeclarativeDashboardPlugin(
                    content=dict(),
                    description="Three dimensional view of data.",
                    id="dashboard-plugin-1",
                    tags=["Revenues"],
                    title="3D map renderer",
                )
            ],
            filter_contexts=[
                DeclarativeFilterContext(
                    content=dict(),
                    description="Filter Context for Sales team.",
                    id="filter-sales",
                    tags=["Revenues"],
                    title="Filter Context for Sales team",
                )
            ],
            metrics=[
                DeclarativeMetric(
                    content=dict(),
                    description="Sales for all the data available.",
                    id="total-sales",
                    tags=["Revenues"],
                    title="Total sales",
                )
            ],
            visualization_objects=[
                DeclarativeVisualizationObject(
                    content=dict(),
                    description="Simple number for total goods in current production.",
                    id="visualization-1",
                    tags=["Revenues"],
                    title="Count of goods",
                )
            ],
        ),
    )
    try:
        # Set analytics model
        api_response = api_instance.set_analytics_model(
            path_params=path_params,
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->set_analytics_model: %s\n" % e)
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
[**DeclarativeAnalytics**](../../models/DeclarativeAnalytics.md) |  | 


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
204 | [ApiResponseFor204](#set_analytics_model.ApiResponseFor204) | Analytics model successfully set.

#### set_analytics_model.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **set_logical_model**
<a id="set_logical_model"></a>
> set_logical_model(workspace_iddeclarative_model)

Set logical model

Set effective logical model of the workspace.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_model import DeclarativeModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    body = DeclarativeModel(
        ldm=DeclarativeLdm(
            datasets=[
                DeclarativeDataset(
                    attributes=[
                        DeclarativeAttribute(
                            default_view=LabelIdentifier(
                                id="label_id",
                                type="label",
                            ),
                            description="Customer name including first and last name.",
                            id="attr.customers.customer_name",
                            labels=[
                                DeclarativeLabel(
                                    description="Customer name",
                                    id="label.customer_name",
                                    source_column="customer_name",
                                    source_column_data_type="STRING",
                                    tags=["Customers"],
                                    title="Customer name",
                                    value_type="\"TEXT\" | \"HYPERLINK\" | \"GEO\" | \"GEO_LONGITUDE\" | \"GEO_LATITUDE\"",
                                )
                            ],
                            sort_column="customer_name",
                            sort_direction="\"ASC\" | \"DESC\"",
                            source_column="customer_name",
                            source_column_data_type="STRING",
                            tags=["Customers"],
                            title="Customer Name",
                        )
                    ],
                    data_source_table_id=DataSourceTableIdentifier(
                        data_source_id="my-postgres",
                        id="customers",
                        type="dataSource",
                    ),
                    description="The customers of ours.",
                    facts=[
                        DeclarativeFact(
                            description="A number of orders created by the customer - including all orders, even the non-delivered ones.",
                            id="fact.customer_order_count",
                            source_column="customer_order_count",
                            source_column_data_type="NUMERIC",
                            tags=["Customers"],
                            title="Customer order count",
                        )
                    ],
                    grain=[
                        GrainIdentifier(
                            id="attr.customers.customer_name",
                            type="ATTRIBUTE",
                        )
                    ],
                    id="customers",
                    references=[
                        DeclarativeReference(
                            identifier=ReferenceIdentifier(
                                id="customers",
                                type="DATASET",
                            ),
                            multivalue=False,
                            source_column_data_types=[
                                "source_column_data_types_example"
                            ],
                            source_columns=["customer_id"],
                        )
                    ],
                    sql=DeclarativeDatasetSql(
                        data_source_id="my-postgres",
                        statement="SELECT * FROM some_table",
                    ),
                    tags=["Customers"],
                    title="Customers",
                    workspace_data_filter_columns=[
                        DeclarativeWorkspaceDataFilterColumn(
                            data_type="INT",
                            name="customer_id",
                        )
                    ],
                )
            ],
            date_instances=[
                DeclarativeDateDataset(
                    description="A customer order date",
                    granularities=[
                        "MINUTE"
                    ],
                    granularities_formatting=GranularitiesFormatting(
                        title_base="title_base_example",
                        title_pattern="%titleBase - %granularityTitle",
                    ),
                    id="date",
                    tags=["Customer dates"],
                    title="Date",
                )
            ],
        ),
    )
    try:
        # Set logical model
        api_response = api_instance.set_logical_model(
            path_params=path_params,
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->set_logical_model: %s\n" % e)
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
[**DeclarativeModel**](../../models/DeclarativeModel.md) |  | 


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
204 | [ApiResponseFor204](#set_logical_model.ApiResponseFor204) | Logical model successfully set.

#### set_logical_model.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **set_organization_layout**
<a id="set_organization_layout"></a>
> set_organization_layout(declarative_organization)

Set organization layout

Sets complete layout of organization, like workspaces, user-groups, etc.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_organization import DeclarativeOrganization
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example passing only required values which don't have defaults set
    body = DeclarativeOrganization(
        data_sources=[
            DeclarativeDataSource(
                cache_path=[
                    "[ \"dfs\", \"data\" ]. Example used in Apache Drill."
                ],
                decoded_parameters=[
                    Parameter(
                        name="name_example",
                        value="value_example",
                    )
                ],
                enable_caching=False,
                id="pg_local_docker-demo",
                name="postgres demo",
,
                password="*****",
                pdm=DeclarativeTables(
                    tables=[
                        DeclarativeTable(
                            columns=[
                                DeclarativeColumn(
                                    data_type="INT",
                                    is_primary_key=True,
                                    name="customer_id",
                                    referenced_table_column="customer_id",
                                    referenced_table_id="customers",
                                )
                            ],
                            id="customers",
                            name_prefix="out_gooddata",
                            path=["table_schema","table_name"],
                            type="VIEW",
                        )
                    ],
                ),
                permissions=[
                    DeclarativeDataSourcePermission(
                        assignee=AssigneeIdentifier(
                            id="id_example",
                            type="user",
                        ),
                        name="MANAGE",
                    )
                ],
                schema="demo",
                token="Bigquery service account JSON. Encode it using base64!",
                type="POSTGRESQL",
                url="jdbc:postgresql://postgres:5432/gooddata",
                username="demo",
            )
        ],
        organization=DeclarativeOrganizationInfo(
            color_palettes=[
                DeclarativeColorPalette(
                    content=dict(),
                    id="id_example",
                    name="name_example",
                )
            ],
            csp_directives=[
                DeclarativeCspDirective(
                    directive="directive_example",
                    sources=[
                        "sources_example"
                    ],
                )
            ],
            early_access="early_access_example",
            hostname="alpha.com",
            id="Alpha corporation",
            name="Alpha corporation",
            oauth_client_id="oauth_client_id_example",
            oauth_client_secret="oauth_client_secret_example",
            oauth_issuer_id="myOidcProvider",
            oauth_issuer_location="oauth_issuer_location_example",
            permissions=[
                DeclarativeOrganizationPermission(
                    assignee=AssigneeIdentifier(),
                    name="MANAGE",
                )
            ],
            settings=[
                DeclarativeSetting(
                    content=dict(),
                    id="/6bUUGjjNSwg0_bs",
                    type="TIMEZONE",
                )
            ],
            themes=[
                DeclarativeTheme(
                    content=dict(),
                    id="id_example",
                    name="name_example",
                )
            ],
        ),
        user_groups=[
            DeclarativeUserGroup(
                id="employees.all",
                name="admins",
                parents=[
                    UserGroupIdentifier(
                        id="group.admins",
                        type="userGroup",
                    )
                ],
                permissions=[
                    DeclarativeUserGroupPermission(
                        assignee=AssigneeIdentifier(),
                        name="SEE",
                    )
                ],
            )
        ],
        users=[
            DeclarativeUser(
                auth_id="auth_id_example",
                email="user@example.com",
                firstname="John",
                id="employee123",
                lastname="Wick",
                permissions=[
                    DeclarativeUserPermission(
                        assignee=AssigneeIdentifier(),
                        name="SEE",
                    )
                ],
                settings=[
                    DeclarativeSetting()
                ],
,
            )
        ],
        workspace_data_filters=[
            DeclarativeWorkspaceDataFilter(
                column_name="country_id",
                description="ID of country",
                id="country_id",
                title="Country ID",
                workspace=WorkspaceIdentifier(
                    id="alpha.sales",
                    type="workspace",
                ),
                workspace_data_filter_settings=[
                    DeclarativeWorkspaceDataFilterSetting(
                        description="ID of country setting",
                        filter_values=["US"],
                        id="country_id_setting",
                        title="Country ID setting",
                        workspace=WorkspaceIdentifier(),
                    )
                ],
            )
        ],
        workspaces=[
            DeclarativeWorkspace(
                custom_application_settings=[
                    DeclarativeCustomApplicationSetting(
                        application_name="Modeler",
                        content=dict(),
                        id="modeler.demo",
                    )
                ],
                description="description_example",
                early_access="early_access_example",
                hierarchy_permissions=[
                    DeclarativeWorkspaceHierarchyPermission(
                        assignee=AssigneeIdentifier(),
                        name="MANAGE",
                    )
                ],
                id="alpha.sales",
                model=DeclarativeWorkspaceModel(
                    analytics=DeclarativeAnalyticsLayer(
                        analytical_dashboard_extensions=[
                            DeclarativeAnalyticalDashboardExtension(
                                id="revenues-analysis",
                                permissions=[
                                    DeclarativeAnalyticalDashboardPermission(
                                        assignee=AssigneeIdentifier(),
                                        name="EDIT",
                                    )
                                ],
                            )
                        ],
                        analytical_dashboards=[
                            DeclarativeAnalyticalDashboard(
                                content=dict(),
                                description="Period to period comparison of revenues in main sectors.",
                                id="revenues-analysis",
,
                                tags=["Revenues"],
                                title="Revenues analysis",
                            )
                        ],
                        dashboard_plugins=[
                            DeclarativeDashboardPlugin(
                                content=dict(),
                                description="Three dimensional view of data.",
                                id="dashboard-plugin-1",
                                tags=["Revenues"],
                                title="3D map renderer",
                            )
                        ],
                        filter_contexts=[
                            DeclarativeFilterContext(
                                content=dict(),
                                description="Filter Context for Sales team.",
                                id="filter-sales",
                                tags=["Revenues"],
                                title="Filter Context for Sales team",
                            )
                        ],
                        metrics=[
                            DeclarativeMetric(
                                content=dict(),
                                description="Sales for all the data available.",
                                id="total-sales",
                                tags=["Revenues"],
                                title="Total sales",
                            )
                        ],
                        visualization_objects=[
                            DeclarativeVisualizationObject(
                                content=dict(),
                                description="Simple number for total goods in current production.",
                                id="visualization-1",
                                tags=["Revenues"],
                                title="Count of goods",
                            )
                        ],
                    ),
                    ldm=DeclarativeLdm(
                        datasets=[
                            DeclarativeDataset(
                                attributes=[
                                    DeclarativeAttribute(
                                        default_view=LabelIdentifier(
                                            id="label_id",
                                            type="label",
                                        ),
                                        description="Customer name including first and last name.",
                                        id="attr.customers.customer_name",
                                        labels=[
                                            DeclarativeLabel(
                                                description="Customer name",
                                                id="label.customer_name",
                                                source_column="customer_name",
                                                source_column_data_type="STRING",
                                                tags=["Customers"],
                                                title="Customer name",
                                                value_type="\"TEXT\" | \"HYPERLINK\" | \"GEO\" | \"GEO_LONGITUDE\" | \"GEO_LATITUDE\"",
                                            )
                                        ],
                                        sort_column="customer_name",
                                        sort_direction="\"ASC\" | \"DESC\"",
                                        source_column="customer_name",
                                        source_column_data_type="STRING",
                                        tags=["Customers"],
                                        title="Customer Name",
                                    )
                                ],
                                data_source_table_id=DataSourceTableIdentifier(
                                    data_source_id="my-postgres",
                                    id="customers",
                                    type="dataSource",
                                ),
                                description="The customers of ours.",
                                facts=[
                                    DeclarativeFact(
                                        description="A number of orders created by the customer - including all orders, even the non-delivered ones.",
                                        id="fact.customer_order_count",
                                        source_column="customer_order_count",
                                        source_column_data_type="NUMERIC",
                                        tags=["Customers"],
                                        title="Customer order count",
                                    )
                                ],
                                grain=[
                                    GrainIdentifier(
                                        id="attr.customers.customer_name",
                                        type="ATTRIBUTE",
                                    )
                                ],
                                id="customers",
                                references=[
                                    DeclarativeReference(
                                        identifier=ReferenceIdentifier(
                                            id="customers",
                                            type="DATASET",
                                        ),
                                        multivalue=False,
                                        source_column_data_types=[
                                            "source_column_data_types_example"
                                        ],
                                        source_columns=["customer_id"],
                                    )
                                ],
                                sql=DeclarativeDatasetSql(
                                    data_source_id="my-postgres",
                                    statement="SELECT * FROM some_table",
                                ),
                                tags=["Customers"],
                                title="Customers",
                                workspace_data_filter_columns=[
                                    DeclarativeWorkspaceDataFilterColumn(
                                        data_type="INT",
                                        name="customer_id",
                                    )
                                ],
                            )
                        ],
                        date_instances=[
                            DeclarativeDateDataset(
                                description="A customer order date",
                                granularities=[
                                    "MINUTE"
                                ],
                                granularities_formatting=GranularitiesFormatting(
                                    title_base="title_base_example",
                                    title_pattern="%titleBase - %granularityTitle",
                                ),
                                id="date",
                                tags=["Customer dates"],
                                title="Date",
                            )
                        ],
                    ),
                ),
                name="Alpha Sales",
                parent=WorkspaceIdentifier(),
                permissions=[
                    DeclarativeSingleWorkspacePermission()
                ],
                prefix="/6bUUGjjNSwg0_bs",
                settings=[
                    DeclarativeSetting()
                ],
                user_data_filters=[
                    DeclarativeUserDataFilter(
                        description="ID of country setting",
                        id="country_id_setting",
                        maql="{label/country} = \"USA\" AND {label/date.year} = THIS(YEAR)",
                        tags=["Revenues"],
                        title="Country ID setting",
                        user=UserIdentifier(
                            id="employee123",
                            type="user",
                        ),
                        user_group=UserGroupIdentifier(),
                    )
                ],
            )
        ],
    )
    try:
        # Set organization layout
        api_response = api_instance.set_organization_layout(
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->set_organization_layout: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeOrganization**](../../models/DeclarativeOrganization.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#set_organization_layout.ApiResponseFor204) | Defined all parts of an organization.

#### set_organization_layout.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **set_pdm_layout**
<a id="set_pdm_layout"></a>
> set_pdm_layout(data_source_iddeclarative_pdm)

Set data source physical model layout

Sets complete layout of tables with their columns under corresponding Data Source.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_pdm import DeclarativePdm
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'dataSourceId': "dataSourceId_example",
    }
    body = DeclarativePdm(
        pdm=DeclarativeTables(
            tables=[
                DeclarativeTable(
                    columns=[
                        DeclarativeColumn(
                            data_type="INT",
                            is_primary_key=True,
                            name="customer_id",
                            referenced_table_column="customer_id",
                            referenced_table_id="customers",
                        )
                    ],
                    id="customers",
                    name_prefix="out_gooddata",
                    path=["table_schema","table_name"],
                    type="VIEW",
                )
            ],
        ),
    )
    try:
        # Set data source physical model layout
        api_response = api_instance.set_pdm_layout(
            path_params=path_params,
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->set_pdm_layout: %s\n" % e)
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
[**DeclarativePdm**](../../models/DeclarativePdm.md) |  | 


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
204 | [ApiResponseFor204](#set_pdm_layout.ApiResponseFor204) | Data source physical mode layout set successfully.

#### set_pdm_layout.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **set_user_data_filters**
<a id="set_user_data_filters"></a>
> set_user_data_filters(workspace_iddeclarative_user_data_filters)

Set user data filters

Set user data filters assigned to the workspace.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_user_data_filters import DeclarativeUserDataFilters
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    body = DeclarativeUserDataFilters(
        user_data_filters=[
            DeclarativeUserDataFilter(
                description="ID of country setting",
                id="country_id_setting",
                maql="{label/country} = \"USA\" AND {label/date.year} = THIS(YEAR)",
                tags=["Revenues"],
                title="Country ID setting",
                user=UserIdentifier(
                    id="employee123",
                    type="user",
                ),
                user_group=UserGroupIdentifier(
                    id="group.admins",
                    type="userGroup",
                ),
            )
        ],
    )
    try:
        # Set user data filters
        api_response = api_instance.set_user_data_filters(
            path_params=path_params,
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->set_user_data_filters: %s\n" % e)
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
[**DeclarativeUserDataFilters**](../../models/DeclarativeUserDataFilters.md) |  | 


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
204 | [ApiResponseFor204](#set_user_data_filters.ApiResponseFor204) | User data filters successfully set.

#### set_user_data_filters.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **set_user_group_permissions**
<a id="set_user_group_permissions"></a>
> set_user_group_permissions(user_group_iddeclarative_user_group_permissions)

Set permissions for the user-group

Set effective permissions for the user-group

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_user_group_permissions import DeclarativeUserGroupPermissions
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'userGroupId': "userGroupId_example",
    }
    body = DeclarativeUserGroupPermissions(
        permissions=[
            DeclarativeUserGroupPermission(
                assignee=AssigneeIdentifier(
                    id="id_example",
                    type="user",
                ),
                name="SEE",
            )
        ],
    )
    try:
        # Set permissions for the user-group
        api_response = api_instance.set_user_group_permissions(
            path_params=path_params,
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->set_user_group_permissions: %s\n" % e)
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
[**DeclarativeUserGroupPermissions**](../../models/DeclarativeUserGroupPermissions.md) |  | 


### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
userGroupId | UserGroupIdSchema | | 

# UserGroupIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#set_user_group_permissions.ApiResponseFor204) | User-group permissions successfully set.

#### set_user_group_permissions.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **set_user_permissions**
<a id="set_user_permissions"></a>
> set_user_permissions(user_iddeclarative_user_permissions)

Set permissions for the user

Set effective permissions for the user

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_user_permissions import DeclarativeUserPermissions
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'userId': "userId_example",
    }
    body = DeclarativeUserPermissions(
        permissions=[
            DeclarativeUserPermission(
                assignee=AssigneeIdentifier(
                    id="id_example",
                    type="user",
                ),
                name="SEE",
            )
        ],
    )
    try:
        # Set permissions for the user
        api_response = api_instance.set_user_permissions(
            path_params=path_params,
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->set_user_permissions: %s\n" % e)
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
[**DeclarativeUserPermissions**](../../models/DeclarativeUserPermissions.md) |  | 


### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
userId | UserIdSchema | | 

# UserIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#set_user_permissions.ApiResponseFor204) | User permissions successfully set.

#### set_user_permissions.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **set_workspace_data_filters_layout**
<a id="set_workspace_data_filters_layout"></a>
> set_workspace_data_filters_layout(declarative_workspace_data_filters)

Set all workspace data filters

Sets workspace data filters in all workspaces in entire organization.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_workspace_data_filters import DeclarativeWorkspaceDataFilters
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example passing only required values which don't have defaults set
    body = DeclarativeWorkspaceDataFilters(
        workspace_data_filters=[
            DeclarativeWorkspaceDataFilter(
                column_name="country_id",
                description="ID of country",
                id="country_id",
                title="Country ID",
                workspace=WorkspaceIdentifier(
                    id="alpha.sales",
                    type="workspace",
                ),
                workspace_data_filter_settings=[
                    DeclarativeWorkspaceDataFilterSetting(
                        description="ID of country setting",
                        filter_values=["US"],
                        id="country_id_setting",
                        title="Country ID setting",
                        workspace=WorkspaceIdentifier(),
                    )
                ],
            )
        ],
    )
    try:
        # Set all workspace data filters
        api_response = api_instance.set_workspace_data_filters_layout(
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->set_workspace_data_filters_layout: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeWorkspaceDataFilters**](../../models/DeclarativeWorkspaceDataFilters.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#set_workspace_data_filters_layout.ApiResponseFor204) | All workspace data filters set.

#### set_workspace_data_filters_layout.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **set_workspace_permissions**
<a id="set_workspace_permissions"></a>
> set_workspace_permissions(workspace_iddeclarative_workspace_permissions)

Set permissions for the workspace

Set effective permissions for the workspace

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_workspace_permissions import DeclarativeWorkspacePermissions
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    body = DeclarativeWorkspacePermissions(
        hierarchy_permissions=[
            DeclarativeWorkspaceHierarchyPermission(
                assignee=AssigneeIdentifier(
                    id="id_example",
                    type="user",
                ),
                name="MANAGE",
            )
        ],
        permissions=[
            DeclarativeSingleWorkspacePermission()
        ],
    )
    try:
        # Set permissions for the workspace
        api_response = api_instance.set_workspace_permissions(
            path_params=path_params,
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->set_workspace_permissions: %s\n" % e)
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
[**DeclarativeWorkspacePermissions**](../../models/DeclarativeWorkspacePermissions.md) |  | 


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
204 | [ApiResponseFor204](#set_workspace_permissions.ApiResponseFor204) | Workspace permissions successfully set.

#### set_workspace_permissions.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **set_workspaces_layout**
<a id="set_workspaces_layout"></a>
> set_workspaces_layout(declarative_workspaces)

Set all workspaces layout

Sets complete layout of workspaces, their hierarchy, models.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import layout_api
from gooddata_api_client.model.declarative_workspaces import DeclarativeWorkspaces
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)

    # example passing only required values which don't have defaults set
    body = DeclarativeWorkspaces(
        workspace_data_filters=[
            DeclarativeWorkspaceDataFilter(
                column_name="country_id",
                description="ID of country",
                id="country_id",
                title="Country ID",
                workspace=WorkspaceIdentifier(
                    id="alpha.sales",
                    type="workspace",
                ),
                workspace_data_filter_settings=[
                    DeclarativeWorkspaceDataFilterSetting(
                        description="ID of country setting",
                        filter_values=["US"],
                        id="country_id_setting",
                        title="Country ID setting",
                        workspace=WorkspaceIdentifier(),
                    )
                ],
            )
        ],
        workspaces=[
            DeclarativeWorkspace(
                custom_application_settings=[
                    DeclarativeCustomApplicationSetting(
                        application_name="Modeler",
                        content=dict(),
                        id="modeler.demo",
                    )
                ],
                description="description_example",
                early_access="early_access_example",
                hierarchy_permissions=[
                    DeclarativeWorkspaceHierarchyPermission(
                        assignee=AssigneeIdentifier(
                            id="id_example",
                            type="user",
                        ),
                        name="MANAGE",
                    )
                ],
                id="alpha.sales",
                model=DeclarativeWorkspaceModel(
                    analytics=DeclarativeAnalyticsLayer(
                        analytical_dashboard_extensions=[
                            DeclarativeAnalyticalDashboardExtension(
                                id="revenues-analysis",
                                permissions=[
                                    DeclarativeAnalyticalDashboardPermission(
                                        assignee=AssigneeIdentifier(),
                                        name="EDIT",
                                    )
                                ],
                            )
                        ],
                        analytical_dashboards=[
                            DeclarativeAnalyticalDashboard(
                                content=dict(),
                                description="Period to period comparison of revenues in main sectors.",
                                id="revenues-analysis",
,
                                tags=["Revenues"],
                                title="Revenues analysis",
                            )
                        ],
                        dashboard_plugins=[
                            DeclarativeDashboardPlugin(
                                content=dict(),
                                description="Three dimensional view of data.",
                                id="dashboard-plugin-1",
                                tags=["Revenues"],
                                title="3D map renderer",
                            )
                        ],
                        filter_contexts=[
                            DeclarativeFilterContext(
                                content=dict(),
                                description="Filter Context for Sales team.",
                                id="filter-sales",
                                tags=["Revenues"],
                                title="Filter Context for Sales team",
                            )
                        ],
                        metrics=[
                            DeclarativeMetric(
                                content=dict(),
                                description="Sales for all the data available.",
                                id="total-sales",
                                tags=["Revenues"],
                                title="Total sales",
                            )
                        ],
                        visualization_objects=[
                            DeclarativeVisualizationObject(
                                content=dict(),
                                description="Simple number for total goods in current production.",
                                id="visualization-1",
                                tags=["Revenues"],
                                title="Count of goods",
                            )
                        ],
                    ),
                    ldm=DeclarativeLdm(
                        datasets=[
                            DeclarativeDataset(
                                attributes=[
                                    DeclarativeAttribute(
                                        default_view=LabelIdentifier(
                                            id="label_id",
                                            type="label",
                                        ),
                                        description="Customer name including first and last name.",
                                        id="attr.customers.customer_name",
                                        labels=[
                                            DeclarativeLabel(
                                                description="Customer name",
                                                id="label.customer_name",
                                                source_column="customer_name",
                                                source_column_data_type="STRING",
                                                tags=["Customers"],
                                                title="Customer name",
                                                value_type="\"TEXT\" | \"HYPERLINK\" | \"GEO\" | \"GEO_LONGITUDE\" | \"GEO_LATITUDE\"",
                                            )
                                        ],
                                        sort_column="customer_name",
                                        sort_direction="\"ASC\" | \"DESC\"",
                                        source_column="customer_name",
                                        source_column_data_type="STRING",
                                        tags=["Customers"],
                                        title="Customer Name",
                                    )
                                ],
                                data_source_table_id=DataSourceTableIdentifier(
                                    data_source_id="my-postgres",
                                    id="customers",
                                    type="dataSource",
                                ),
                                description="The customers of ours.",
                                facts=[
                                    DeclarativeFact(
                                        description="A number of orders created by the customer - including all orders, even the non-delivered ones.",
                                        id="fact.customer_order_count",
                                        source_column="customer_order_count",
                                        source_column_data_type="NUMERIC",
                                        tags=["Customers"],
                                        title="Customer order count",
                                    )
                                ],
                                grain=[
                                    GrainIdentifier(
                                        id="attr.customers.customer_name",
                                        type="ATTRIBUTE",
                                    )
                                ],
                                id="customers",
                                references=[
                                    DeclarativeReference(
                                        identifier=ReferenceIdentifier(
                                            id="customers",
                                            type="DATASET",
                                        ),
                                        multivalue=False,
                                        source_column_data_types=[
                                            "source_column_data_types_example"
                                        ],
                                        source_columns=["customer_id"],
                                    )
                                ],
                                sql=DeclarativeDatasetSql(
                                    data_source_id="my-postgres",
                                    statement="SELECT * FROM some_table",
                                ),
                                tags=["Customers"],
                                title="Customers",
                                workspace_data_filter_columns=[
                                    DeclarativeWorkspaceDataFilterColumn(
                                        data_type="INT",
                                        name="customer_id",
                                    )
                                ],
                            )
                        ],
                        date_instances=[
                            DeclarativeDateDataset(
                                description="A customer order date",
                                granularities=[
                                    "MINUTE"
                                ],
                                granularities_formatting=GranularitiesFormatting(
                                    title_base="title_base_example",
                                    title_pattern="%titleBase - %granularityTitle",
                                ),
                                id="date",
                                tags=["Customer dates"],
                                title="Date",
                            )
                        ],
                    ),
                ),
                name="Alpha Sales",
                parent=WorkspaceIdentifier(),
                permissions=[
                    DeclarativeSingleWorkspacePermission()
                ],
                prefix="/6bUUGjjNSwg0_bs",
                settings=[
                    DeclarativeSetting(
                        content=dict(),
                        id="/6bUUGjjNSwg0_bs",
                        type="TIMEZONE",
                    )
                ],
                user_data_filters=[
                    DeclarativeUserDataFilter(
                        description="ID of country setting",
                        id="country_id_setting",
                        maql="{label/country} = \"USA\" AND {label/date.year} = THIS(YEAR)",
                        tags=["Revenues"],
                        title="Country ID setting",
                        user=UserIdentifier(
                            id="employee123",
                            type="user",
                        ),
                        user_group=UserGroupIdentifier(
                            id="group.admins",
                            type="userGroup",
                        ),
                    )
                ],
            )
        ],
    )
    try:
        # Set all workspaces layout
        api_response = api_instance.set_workspaces_layout(
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->set_workspaces_layout: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeWorkspaces**](../../models/DeclarativeWorkspaces.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#set_workspaces_layout.ApiResponseFor204) | All workspaces layout set.

#### set_workspaces_layout.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


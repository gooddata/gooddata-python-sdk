# gooddata_api_client.UserManagementApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_group_members**](UserManagementApi.md#add_group_members) | **POST** /api/v1/actions/userManagement/userGroups/{userGroupId}/addMembers | 
[**assign_permissions**](UserManagementApi.md#assign_permissions) | **POST** /api/v1/actions/userManagement/assignPermissions | 
[**get_group_members**](UserManagementApi.md#get_group_members) | **GET** /api/v1/actions/userManagement/userGroups/{userGroupId}/members | 
[**list_permissions_for_user**](UserManagementApi.md#list_permissions_for_user) | **GET** /api/v1/actions/userManagement/users/{userId}/permissions | 
[**list_permissions_for_user_group**](UserManagementApi.md#list_permissions_for_user_group) | **GET** /api/v1/actions/userManagement/userGroups/{userGroupId}/permissions | 
[**list_user_groups**](UserManagementApi.md#list_user_groups) | **GET** /api/v1/actions/userManagement/userGroups | 
[**list_users**](UserManagementApi.md#list_users) | **GET** /api/v1/actions/userManagement/users | 
[**list_workspace_user_groups**](UserManagementApi.md#list_workspace_user_groups) | **GET** /api/v1/actions/workspaces/{workspaceId}/userGroups | 
[**list_workspace_users**](UserManagementApi.md#list_workspace_users) | **GET** /api/v1/actions/workspaces/{workspaceId}/users | 
[**manage_permissions_for_user**](UserManagementApi.md#manage_permissions_for_user) | **POST** /api/v1/actions/userManagement/users/{userId}/permissions | 
[**manage_permissions_for_user_group**](UserManagementApi.md#manage_permissions_for_user_group) | **POST** /api/v1/actions/userManagement/userGroups/{userGroupId}/permissions | 
[**remove_group_members**](UserManagementApi.md#remove_group_members) | **POST** /api/v1/actions/userManagement/userGroups/{userGroupId}/removeMembers | 
[**remove_users_user_groups**](UserManagementApi.md#remove_users_user_groups) | **POST** /api/v1/actions/userManagement/removeUsersUserGroups | 
[**revoke_permissions**](UserManagementApi.md#revoke_permissions) | **POST** /api/v1/actions/userManagement/revokePermissions | 


# **add_group_members**
> add_group_members(user_group_id, user_management_user_group_members)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_management_api
from gooddata_api_client.model.user_management_user_group_members import UserManagementUserGroupMembers
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_management_api.UserManagementApi(api_client)
    user_group_id = "userGroupId_example" # str | 
    user_management_user_group_members = UserManagementUserGroupMembers(
        members=[
            UserManagementUserGroupMember(
                id="id_example",
            ),
        ],
    ) # UserManagementUserGroupMembers | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.add_group_members(user_group_id, user_management_user_group_members)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserManagementApi->add_group_members: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_group_id** | **str**|  |
 **user_management_user_group_members** | [**UserManagementUserGroupMembers**](UserManagementUserGroupMembers.md)|  |

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

# **assign_permissions**
> assign_permissions(permissions_assignment)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_management_api
from gooddata_api_client.model.permissions_assignment import PermissionsAssignment
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_management_api.UserManagementApi(api_client)
    permissions_assignment = PermissionsAssignment(
        assignees=[
            AssigneeIdentifier(
                id="id_example",
                type="user",
            ),
        ],
        data_sources=[
            UserManagementDataSourcePermissionAssignment(
                id="id_example",
                permissions=[
                    "MANAGE",
                ],
            ),
        ],
        workspaces=[
            UserManagementWorkspacePermissionAssignment(
                hierarchy_permissions=[
                    "MANAGE",
                ],
                id="id_example",
                permissions=[
                    "MANAGE",
                ],
            ),
        ],
    ) # PermissionsAssignment | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.assign_permissions(permissions_assignment)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserManagementApi->assign_permissions: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **permissions_assignment** | [**PermissionsAssignment**](PermissionsAssignment.md)|  |

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
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_group_members**
> UserManagementUserGroupMembers get_group_members(user_group_id)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_management_api
from gooddata_api_client.model.user_management_user_group_members import UserManagementUserGroupMembers
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_management_api.UserManagementApi(api_client)
    user_group_id = "userGroupId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_group_members(user_group_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserManagementApi->get_group_members: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_group_id** | **str**|  |

### Return type

[**UserManagementUserGroupMembers**](UserManagementUserGroupMembers.md)

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

# **list_permissions_for_user**
> UserManagementPermissionAssignments list_permissions_for_user(user_id)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_management_api
from gooddata_api_client.model.user_management_permission_assignments import UserManagementPermissionAssignments
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_management_api.UserManagementApi(api_client)
    user_id = "userId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.list_permissions_for_user(user_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserManagementApi->list_permissions_for_user: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  |

### Return type

[**UserManagementPermissionAssignments**](UserManagementPermissionAssignments.md)

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

# **list_permissions_for_user_group**
> UserManagementPermissionAssignments list_permissions_for_user_group(user_group_id)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_management_api
from gooddata_api_client.model.user_management_permission_assignments import UserManagementPermissionAssignments
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_management_api.UserManagementApi(api_client)
    user_group_id = "userGroupId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.list_permissions_for_user_group(user_group_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserManagementApi->list_permissions_for_user_group: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_group_id** | **str**|  |

### Return type

[**UserManagementPermissionAssignments**](UserManagementPermissionAssignments.md)

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

# **list_user_groups**
> UserManagementUserGroups list_user_groups()



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_management_api
from gooddata_api_client.model.user_management_user_groups import UserManagementUserGroups
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_management_api.UserManagementApi(api_client)
    page = page=0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = size=20 # int | The size of the page to be returned. (optional) if omitted the server will use the default value of 20
    name = "name=charles" # str | Filter by user name. Note that user name is case insensitive. (optional)
    workspace = "workspace=demo" # str | Filter by workspaceId. (optional)
    data_source = "dataSource=demo-test-ds" # str | Filter by dataSourceId. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.list_user_groups(page=page, size=size, name=name, workspace=workspace, data_source=data_source)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserManagementApi->list_user_groups: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned. | [optional] if omitted the server will use the default value of 20
 **name** | **str**| Filter by user name. Note that user name is case insensitive. | [optional]
 **workspace** | **str**| Filter by workspaceId. | [optional]
 **data_source** | **str**| Filter by dataSourceId. | [optional]

### Return type

[**UserManagementUserGroups**](UserManagementUserGroups.md)

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

# **list_users**
> UserManagementUsers list_users()



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_management_api
from gooddata_api_client.model.user_management_users import UserManagementUsers
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_management_api.UserManagementApi(api_client)
    page = page=0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = size=20 # int | The size of the page to be returned. (optional) if omitted the server will use the default value of 20
    name = "name=charles" # str | Filter by user name. Note that user name is case insensitive. (optional)
    workspace = "workspace=demo" # str | Filter by workspaceId. (optional)
    group = "group=admin" # str | Filter by userGroupId. (optional)
    data_source = "dataSource=demo-test-ds" # str | Filter by dataSourceId. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.list_users(page=page, size=size, name=name, workspace=workspace, group=group, data_source=data_source)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserManagementApi->list_users: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned. | [optional] if omitted the server will use the default value of 20
 **name** | **str**| Filter by user name. Note that user name is case insensitive. | [optional]
 **workspace** | **str**| Filter by workspaceId. | [optional]
 **group** | **str**| Filter by userGroupId. | [optional]
 **data_source** | **str**| Filter by dataSourceId. | [optional]

### Return type

[**UserManagementUsers**](UserManagementUsers.md)

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
from gooddata_api_client.api import user_management_api
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
    api_instance = user_management_api.UserManagementApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    page = page=0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = size=20 # int | The size of the page to be returned. (optional) if omitted the server will use the default value of 20
    name = "name=charles" # str | Filter by user name. Note that user name is case insensitive. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.list_workspace_user_groups(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserManagementApi->list_workspace_user_groups: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.list_workspace_user_groups(workspace_id, page=page, size=size, name=name)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserManagementApi->list_workspace_user_groups: %s\n" % e)
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
from gooddata_api_client.api import user_management_api
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
    api_instance = user_management_api.UserManagementApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    page = page=0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = size=20 # int | The size of the page to be returned. (optional) if omitted the server will use the default value of 20
    name = "name=charles" # str | Filter by user name. Note that user name is case insensitive. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.list_workspace_users(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserManagementApi->list_workspace_users: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.list_workspace_users(workspace_id, page=page, size=size, name=name)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserManagementApi->list_workspace_users: %s\n" % e)
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

# **manage_permissions_for_user**
> manage_permissions_for_user(user_id, user_management_permission_assignments)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_management_api
from gooddata_api_client.model.user_management_permission_assignments import UserManagementPermissionAssignments
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_management_api.UserManagementApi(api_client)
    user_id = "userId_example" # str | 
    user_management_permission_assignments = UserManagementPermissionAssignments(
        data_sources=[
            UserManagementDataSourcePermissionAssignment(
                id="id_example",
                permissions=[
                    "MANAGE",
                ],
            ),
        ],
        workspaces=[
            UserManagementWorkspacePermissionAssignment(
                hierarchy_permissions=[
                    "MANAGE",
                ],
                id="id_example",
                permissions=[
                    "MANAGE",
                ],
            ),
        ],
    ) # UserManagementPermissionAssignments | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.manage_permissions_for_user(user_id, user_management_permission_assignments)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserManagementApi->manage_permissions_for_user: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  |
 **user_management_permission_assignments** | [**UserManagementPermissionAssignments**](UserManagementPermissionAssignments.md)|  |

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

# **manage_permissions_for_user_group**
> manage_permissions_for_user_group(user_group_id, user_management_permission_assignments)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_management_api
from gooddata_api_client.model.user_management_permission_assignments import UserManagementPermissionAssignments
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_management_api.UserManagementApi(api_client)
    user_group_id = "userGroupId_example" # str | 
    user_management_permission_assignments = UserManagementPermissionAssignments(
        data_sources=[
            UserManagementDataSourcePermissionAssignment(
                id="id_example",
                permissions=[
                    "MANAGE",
                ],
            ),
        ],
        workspaces=[
            UserManagementWorkspacePermissionAssignment(
                hierarchy_permissions=[
                    "MANAGE",
                ],
                id="id_example",
                permissions=[
                    "MANAGE",
                ],
            ),
        ],
    ) # UserManagementPermissionAssignments | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.manage_permissions_for_user_group(user_group_id, user_management_permission_assignments)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserManagementApi->manage_permissions_for_user_group: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_group_id** | **str**|  |
 **user_management_permission_assignments** | [**UserManagementPermissionAssignments**](UserManagementPermissionAssignments.md)|  |

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

# **remove_group_members**
> remove_group_members(user_group_id, user_management_user_group_members)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_management_api
from gooddata_api_client.model.user_management_user_group_members import UserManagementUserGroupMembers
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_management_api.UserManagementApi(api_client)
    user_group_id = "userGroupId_example" # str | 
    user_management_user_group_members = UserManagementUserGroupMembers(
        members=[
            UserManagementUserGroupMember(
                id="id_example",
            ),
        ],
    ) # UserManagementUserGroupMembers | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.remove_group_members(user_group_id, user_management_user_group_members)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserManagementApi->remove_group_members: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_group_id** | **str**|  |
 **user_management_user_group_members** | [**UserManagementUserGroupMembers**](UserManagementUserGroupMembers.md)|  |

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

# **remove_users_user_groups**
> remove_users_user_groups(assignee_identifier)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_management_api
from gooddata_api_client.model.assignee_identifier import AssigneeIdentifier
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_management_api.UserManagementApi(api_client)
    assignee_identifier = [
        AssigneeIdentifier(
            id="id_example",
            type="user",
        ),
    ] # [AssigneeIdentifier] | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.remove_users_user_groups(assignee_identifier)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserManagementApi->remove_users_user_groups: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **assignee_identifier** | [**[AssigneeIdentifier]**](AssigneeIdentifier.md)|  |

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
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **revoke_permissions**
> revoke_permissions(permissions_assignment)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_management_api
from gooddata_api_client.model.permissions_assignment import PermissionsAssignment
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_management_api.UserManagementApi(api_client)
    permissions_assignment = PermissionsAssignment(
        assignees=[
            AssigneeIdentifier(
                id="id_example",
                type="user",
            ),
        ],
        data_sources=[
            UserManagementDataSourcePermissionAssignment(
                id="id_example",
                permissions=[
                    "MANAGE",
                ],
            ),
        ],
        workspaces=[
            UserManagementWorkspacePermissionAssignment(
                hierarchy_permissions=[
                    "MANAGE",
                ],
                id="id_example",
                permissions=[
                    "MANAGE",
                ],
            ),
        ],
    ) # PermissionsAssignment | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.revoke_permissions(permissions_assignment)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserManagementApi->revoke_permissions: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **permissions_assignment** | [**PermissionsAssignment**](PermissionsAssignment.md)|  |

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
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


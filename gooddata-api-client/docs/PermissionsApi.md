# gooddata_api_client.PermissionsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**available_assignees**](PermissionsApi.md#available_assignees) | **GET** /api/v1/actions/workspaces/{workspaceId}/analyticalDashboards/{dashboardId}/availableAssignees | Get Available Assignees
[**dashboard_permissions**](PermissionsApi.md#dashboard_permissions) | **GET** /api/v1/actions/workspaces/{workspaceId}/analyticalDashboards/{dashboardId}/permissions | Get Dashboard Permissions
[**get_organization_permissions**](PermissionsApi.md#get_organization_permissions) | **GET** /api/v1/layout/organization/permissions | Get organization permissions
[**get_user_group_permissions**](PermissionsApi.md#get_user_group_permissions) | **GET** /api/v1/layout/userGroups/{userGroupId}/permissions | Get permissions for the user-group
[**get_user_permissions**](PermissionsApi.md#get_user_permissions) | **GET** /api/v1/layout/users/{userId}/permissions | Get permissions for the user
[**get_workspace_permissions**](PermissionsApi.md#get_workspace_permissions) | **GET** /api/v1/layout/workspaces/{workspaceId}/permissions | Get permissions for the workspace
[**manage_dashboard_permissions**](PermissionsApi.md#manage_dashboard_permissions) | **POST** /api/v1/actions/workspaces/{workspaceId}/analyticalDashboards/{dashboardId}/managePermissions | Manage Permissions for a Dashboard
[**manage_data_source_permissions**](PermissionsApi.md#manage_data_source_permissions) | **POST** /api/v1/actions/dataSources/{dataSourceId}/managePermissions | Manage Permissions for a Data Source
[**manage_organization_permissions**](PermissionsApi.md#manage_organization_permissions) | **POST** /api/v1/actions/organization/managePermissions | Manage Permissions for a Organization
[**manage_workspace_permissions**](PermissionsApi.md#manage_workspace_permissions) | **POST** /api/v1/actions/workspaces/{workspaceId}/managePermissions | Manage Permissions for a Workspace
[**set_organization_permissions**](PermissionsApi.md#set_organization_permissions) | **PUT** /api/v1/layout/organization/permissions | Set organization permissions
[**set_user_group_permissions**](PermissionsApi.md#set_user_group_permissions) | **PUT** /api/v1/layout/userGroups/{userGroupId}/permissions | Set permissions for the user-group
[**set_user_permissions**](PermissionsApi.md#set_user_permissions) | **PUT** /api/v1/layout/users/{userId}/permissions | Set permissions for the user
[**set_workspace_permissions**](PermissionsApi.md#set_workspace_permissions) | **PUT** /api/v1/layout/workspaces/{workspaceId}/permissions | Set permissions for the workspace


# **available_assignees**
> AvailableAssignees available_assignees(workspace_id, dashboard_id)

Get Available Assignees

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.available_assignees import AvailableAssignees
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.PermissionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    dashboard_id = 'dashboard_id_example' # str | 

    try:
        # Get Available Assignees
        api_response = api_instance.available_assignees(workspace_id, dashboard_id)
        print("The response of PermissionsApi->available_assignees:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PermissionsApi->available_assignees: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **dashboard_id** | **str**|  | 

### Return type

[**AvailableAssignees**](AvailableAssignees.md)

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

# **dashboard_permissions**
> DashboardPermissions dashboard_permissions(workspace_id, dashboard_id)

Get Dashboard Permissions

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.dashboard_permissions import DashboardPermissions
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.PermissionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    dashboard_id = 'dashboard_id_example' # str | 

    try:
        # Get Dashboard Permissions
        api_response = api_instance.dashboard_permissions(workspace_id, dashboard_id)
        print("The response of PermissionsApi->dashboard_permissions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PermissionsApi->dashboard_permissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **dashboard_id** | **str**|  | 

### Return type

[**DashboardPermissions**](DashboardPermissions.md)

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

# **get_organization_permissions**
> List[DeclarativeOrganizationPermission] get_organization_permissions()

Get organization permissions

Retrieve organization permissions

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_organization_permission import DeclarativeOrganizationPermission
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.PermissionsApi(api_client)

    try:
        # Get organization permissions
        api_response = api_instance.get_organization_permissions()
        print("The response of PermissionsApi->get_organization_permissions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PermissionsApi->get_organization_permissions: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[DeclarativeOrganizationPermission]**](DeclarativeOrganizationPermission.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved all organization permissions. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_group_permissions**
> DeclarativeUserGroupPermissions get_user_group_permissions(user_group_id)

Get permissions for the user-group

Retrieve current set of permissions of the user-group in a declarative form.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_user_group_permissions import DeclarativeUserGroupPermissions
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.PermissionsApi(api_client)
    user_group_id = 'user_group_id_example' # str | 

    try:
        # Get permissions for the user-group
        api_response = api_instance.get_user_group_permissions(user_group_id)
        print("The response of PermissionsApi->get_user_group_permissions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PermissionsApi->get_user_group_permissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_group_id** | **str**|  | 

### Return type

[**DeclarativeUserGroupPermissions**](DeclarativeUserGroupPermissions.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved current set of permissions. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_permissions**
> DeclarativeUserPermissions get_user_permissions(user_id)

Get permissions for the user

Retrieve current set of permissions of the user in a declarative form.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_user_permissions import DeclarativeUserPermissions
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.PermissionsApi(api_client)
    user_id = 'user_id_example' # str | 

    try:
        # Get permissions for the user
        api_response = api_instance.get_user_permissions(user_id)
        print("The response of PermissionsApi->get_user_permissions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PermissionsApi->get_user_permissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  | 

### Return type

[**DeclarativeUserPermissions**](DeclarativeUserPermissions.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved current set of permissions. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_workspace_permissions**
> DeclarativeWorkspacePermissions get_workspace_permissions(workspace_id)

Get permissions for the workspace

Retrieve current set of permissions of the workspace in a declarative form.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_workspace_permissions import DeclarativeWorkspacePermissions
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.PermissionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 

    try:
        # Get permissions for the workspace
        api_response = api_instance.get_workspace_permissions(workspace_id)
        print("The response of PermissionsApi->get_workspace_permissions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PermissionsApi->get_workspace_permissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 

### Return type

[**DeclarativeWorkspacePermissions**](DeclarativeWorkspacePermissions.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved current set of permissions. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **manage_dashboard_permissions**
> manage_dashboard_permissions(workspace_id, dashboard_id, manage_dashboard_permissions_request_inner)

Manage Permissions for a Dashboard

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.manage_dashboard_permissions_request_inner import ManageDashboardPermissionsRequestInner
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.PermissionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    dashboard_id = 'dashboard_id_example' # str | 
    manage_dashboard_permissions_request_inner = [gooddata_api_client.ManageDashboardPermissionsRequestInner()] # List[ManageDashboardPermissionsRequestInner] | 

    try:
        # Manage Permissions for a Dashboard
        api_instance.manage_dashboard_permissions(workspace_id, dashboard_id, manage_dashboard_permissions_request_inner)
    except Exception as e:
        print("Exception when calling PermissionsApi->manage_dashboard_permissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **dashboard_id** | **str**|  | 
 **manage_dashboard_permissions_request_inner** | [**List[ManageDashboardPermissionsRequestInner]**](ManageDashboardPermissionsRequestInner.md)|  | 

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

# **manage_data_source_permissions**
> manage_data_source_permissions(data_source_id, data_source_permission_assignment)

Manage Permissions for a Data Source

Manage Permissions for a Data Source

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.data_source_permission_assignment import DataSourcePermissionAssignment
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.PermissionsApi(api_client)
    data_source_id = 'data_source_id_example' # str | 
    data_source_permission_assignment = [gooddata_api_client.DataSourcePermissionAssignment()] # List[DataSourcePermissionAssignment] | 

    try:
        # Manage Permissions for a Data Source
        api_instance.manage_data_source_permissions(data_source_id, data_source_permission_assignment)
    except Exception as e:
        print("Exception when calling PermissionsApi->manage_data_source_permissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  | 
 **data_source_permission_assignment** | [**List[DataSourcePermissionAssignment]**](DataSourcePermissionAssignment.md)|  | 

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

# **manage_organization_permissions**
> manage_organization_permissions(organization_permission_assignment)

Manage Permissions for a Organization

Manage Permissions for a Organization

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.organization_permission_assignment import OrganizationPermissionAssignment
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.PermissionsApi(api_client)
    organization_permission_assignment = [gooddata_api_client.OrganizationPermissionAssignment()] # List[OrganizationPermissionAssignment] | 

    try:
        # Manage Permissions for a Organization
        api_instance.manage_organization_permissions(organization_permission_assignment)
    except Exception as e:
        print("Exception when calling PermissionsApi->manage_organization_permissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_permission_assignment** | [**List[OrganizationPermissionAssignment]**](OrganizationPermissionAssignment.md)|  | 

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

# **manage_workspace_permissions**
> manage_workspace_permissions(workspace_id, workspace_permission_assignment)

Manage Permissions for a Workspace

Manage Permissions for a Workspace and its Workspace Hierarchy

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.workspace_permission_assignment import WorkspacePermissionAssignment
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.PermissionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    workspace_permission_assignment = [gooddata_api_client.WorkspacePermissionAssignment()] # List[WorkspacePermissionAssignment] | 

    try:
        # Manage Permissions for a Workspace
        api_instance.manage_workspace_permissions(workspace_id, workspace_permission_assignment)
    except Exception as e:
        print("Exception when calling PermissionsApi->manage_workspace_permissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **workspace_permission_assignment** | [**List[WorkspacePermissionAssignment]**](WorkspacePermissionAssignment.md)|  | 

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

# **set_organization_permissions**
> set_organization_permissions(declarative_organization_permission)

Set organization permissions

Sets organization permissions

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_organization_permission import DeclarativeOrganizationPermission
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.PermissionsApi(api_client)
    declarative_organization_permission = [gooddata_api_client.DeclarativeOrganizationPermission()] # List[DeclarativeOrganizationPermission] | 

    try:
        # Set organization permissions
        api_instance.set_organization_permissions(declarative_organization_permission)
    except Exception as e:
        print("Exception when calling PermissionsApi->set_organization_permissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **declarative_organization_permission** | [**List[DeclarativeOrganizationPermission]**](DeclarativeOrganizationPermission.md)|  | 

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
**204** | Organization permissions set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_user_group_permissions**
> set_user_group_permissions(user_group_id, declarative_user_group_permissions)

Set permissions for the user-group

Set effective permissions for the user-group

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_user_group_permissions import DeclarativeUserGroupPermissions
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.PermissionsApi(api_client)
    user_group_id = 'user_group_id_example' # str | 
    declarative_user_group_permissions = gooddata_api_client.DeclarativeUserGroupPermissions() # DeclarativeUserGroupPermissions | 

    try:
        # Set permissions for the user-group
        api_instance.set_user_group_permissions(user_group_id, declarative_user_group_permissions)
    except Exception as e:
        print("Exception when calling PermissionsApi->set_user_group_permissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_group_id** | **str**|  | 
 **declarative_user_group_permissions** | [**DeclarativeUserGroupPermissions**](DeclarativeUserGroupPermissions.md)|  | 

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
**204** | User-group permissions successfully set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_user_permissions**
> set_user_permissions(user_id, declarative_user_permissions)

Set permissions for the user

Set effective permissions for the user

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_user_permissions import DeclarativeUserPermissions
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.PermissionsApi(api_client)
    user_id = 'user_id_example' # str | 
    declarative_user_permissions = gooddata_api_client.DeclarativeUserPermissions() # DeclarativeUserPermissions | 

    try:
        # Set permissions for the user
        api_instance.set_user_permissions(user_id, declarative_user_permissions)
    except Exception as e:
        print("Exception when calling PermissionsApi->set_user_permissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  | 
 **declarative_user_permissions** | [**DeclarativeUserPermissions**](DeclarativeUserPermissions.md)|  | 

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
**204** | User permissions successfully set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_workspace_permissions**
> set_workspace_permissions(workspace_id, declarative_workspace_permissions)

Set permissions for the workspace

Set effective permissions for the workspace

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_workspace_permissions import DeclarativeWorkspacePermissions
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.PermissionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    declarative_workspace_permissions = gooddata_api_client.DeclarativeWorkspacePermissions() # DeclarativeWorkspacePermissions | 

    try:
        # Set permissions for the workspace
        api_instance.set_workspace_permissions(workspace_id, declarative_workspace_permissions)
    except Exception as e:
        print("Exception when calling PermissionsApi->set_workspace_permissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **declarative_workspace_permissions** | [**DeclarativeWorkspacePermissions**](DeclarativeWorkspacePermissions.md)|  | 

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
**204** | Workspace permissions successfully set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


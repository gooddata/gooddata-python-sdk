# gooddata_api_client.PermissionsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**available_assignees**](PermissionsApi.md#available_assignees) | **GET** /api/v1/actions/workspaces/{workspaceId}/analyticalDashboards/{dashboardId}/availableAssignees | Get Available Assignees
[**dashboard_permissions**](PermissionsApi.md#dashboard_permissions) | **GET** /api/v1/actions/workspaces/{workspaceId}/analyticalDashboards/{dashboardId}/permissions | Get Dashboard Permissions
[**get_workspace_permissions**](PermissionsApi.md#get_workspace_permissions) | **GET** /api/v1/layout/workspaces/{workspaceId}/permissions | Get permissions for the workspace
[**manage_dashboard_permissions**](PermissionsApi.md#manage_dashboard_permissions) | **POST** /api/v1/actions/workspaces/{workspaceId}/analyticalDashboards/{dashboardId}/managePermissions | Manage Permissions for a Dashboard
[**set_workspace_permissions**](PermissionsApi.md#set_workspace_permissions) | **PUT** /api/v1/layout/workspaces/{workspaceId}/permissions | Set permissions for the workspace


# **available_assignees**
> AvailableAssignees available_assignees(workspace_id, dashboard_id)

Get Available Assignees

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import permissions_api
from gooddata_api_client.model.available_assignees import AvailableAssignees
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = permissions_api.PermissionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    dashboard_id = "dashboardId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get Available Assignees
        api_response = api_instance.available_assignees(workspace_id, dashboard_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import permissions_api
from gooddata_api_client.model.dashboard_permissions import DashboardPermissions
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = permissions_api.PermissionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    dashboard_id = "dashboardId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get Dashboard Permissions
        api_response = api_instance.dashboard_permissions(workspace_id, dashboard_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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

# **get_workspace_permissions**
> DeclarativeWorkspacePermissions get_workspace_permissions(workspace_id)

Get permissions for the workspace

Retrieve current set of permissions of the workspace in a declarative form.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import permissions_api
from gooddata_api_client.model.declarative_workspace_permissions import DeclarativeWorkspacePermissions
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = permissions_api.PermissionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get permissions for the workspace
        api_response = api_instance.get_workspace_permissions(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
> manage_dashboard_permissions(workspace_id, dashboard_id, permissions_for_assignee)

Manage Permissions for a Dashboard

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import permissions_api
from gooddata_api_client.model.permissions_for_assignee import PermissionsForAssignee
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = permissions_api.PermissionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    dashboard_id = "dashboardId_example" # str | 
    permissions_for_assignee = [
        PermissionsForAssignee(
            assignee_identifier=AssigneeIdentifier(
                id="id_example",
                type="user",
            ),
            permissions=[
                "EDIT",
            ],
        ),
    ] # [PermissionsForAssignee] | 

    # example passing only required values which don't have defaults set
    try:
        # Manage Permissions for a Dashboard
        api_instance.manage_dashboard_permissions(workspace_id, dashboard_id, permissions_for_assignee)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PermissionsApi->manage_dashboard_permissions: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **dashboard_id** | **str**|  |
 **permissions_for_assignee** | [**[PermissionsForAssignee]**](PermissionsForAssignee.md)|  |

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

# **set_workspace_permissions**
> set_workspace_permissions(workspace_id, declarative_workspace_permissions)

Set permissions for the workspace

Set effective permissions for the workspace

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import permissions_api
from gooddata_api_client.model.declarative_workspace_permissions import DeclarativeWorkspacePermissions
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = permissions_api.PermissionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    declarative_workspace_permissions = DeclarativeWorkspacePermissions(
        hierarchy_permissions=[
            DeclarativeWorkspaceHierarchyPermission(
                assignee=AssigneeIdentifier(
                    id="id_example",
                    type="user",
                ),
                name="MANAGE",
            ),
        ],
        permissions=[
            DeclarativeSingleWorkspacePermission(
                assignee=AssigneeIdentifier(
                    id="id_example",
                    type="user",
                ),
                name="MANAGE",
            ),
        ],
    ) # DeclarativeWorkspacePermissions | 

    # example passing only required values which don't have defaults set
    try:
        # Set permissions for the workspace
        api_instance.set_workspace_permissions(workspace_id, declarative_workspace_permissions)
    except gooddata_api_client.ApiException as e:
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


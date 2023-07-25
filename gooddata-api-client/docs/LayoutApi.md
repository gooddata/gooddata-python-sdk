# gooddata_api_client.LayoutApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_analytics_model**](LayoutApi.md#get_analytics_model) | **GET** /api/v1/layout/workspaces/{workspaceId}/analyticsModel | Get analytics model
[**get_data_sources_layout**](LayoutApi.md#get_data_sources_layout) | **GET** /api/v1/layout/dataSources | Get all data sources
[**get_logical_model**](LayoutApi.md#get_logical_model) | **GET** /api/v1/layout/workspaces/{workspaceId}/logicalModel | Get logical model
[**get_organization_layout**](LayoutApi.md#get_organization_layout) | **GET** /api/v1/layout/organization | Get organization layout
[**get_pdm_layout**](LayoutApi.md#get_pdm_layout) | **GET** /api/v1/layout/dataSources/{dataSourceId}/physicalModel | Get data source physical model layout
[**get_user_data_filters**](LayoutApi.md#get_user_data_filters) | **GET** /api/v1/layout/workspaces/{workspaceId}/userDataFilters | Get user data filters
[**get_user_group_permissions**](LayoutApi.md#get_user_group_permissions) | **GET** /api/v1/layout/userGroups/{userGroupId}/permissions | Get permissions for the user-group
[**get_user_groups_layout**](LayoutApi.md#get_user_groups_layout) | **GET** /api/v1/layout/userGroups | Get all user groups
[**get_user_permissions**](LayoutApi.md#get_user_permissions) | **GET** /api/v1/layout/users/{userId}/permissions | Get permissions for the user
[**get_users_layout**](LayoutApi.md#get_users_layout) | **GET** /api/v1/layout/users | Get all users
[**get_users_user_groups_layout**](LayoutApi.md#get_users_user_groups_layout) | **GET** /api/v1/layout/usersAndUserGroups | Get all users and user groups
[**get_workspace_data_filters_layout**](LayoutApi.md#get_workspace_data_filters_layout) | **GET** /api/v1/layout/workspaceDataFilters | Get workspace data filters for all workspaces
[**get_workspace_layout**](LayoutApi.md#get_workspace_layout) | **GET** /api/v1/layout/workspaces/{workspaceId} | Get workspace layout
[**get_workspace_permissions**](LayoutApi.md#get_workspace_permissions) | **GET** /api/v1/layout/workspaces/{workspaceId}/permissions | Get permissions for the workspace
[**get_workspaces_layout**](LayoutApi.md#get_workspaces_layout) | **GET** /api/v1/layout/workspaces | Get all workspaces layout
[**put_data_sources_layout**](LayoutApi.md#put_data_sources_layout) | **PUT** /api/v1/layout/dataSources | Put all data sources
[**put_user_groups_layout**](LayoutApi.md#put_user_groups_layout) | **PUT** /api/v1/layout/userGroups | Put all user groups
[**put_users_layout**](LayoutApi.md#put_users_layout) | **PUT** /api/v1/layout/users | Put all users
[**put_users_user_groups_layout**](LayoutApi.md#put_users_user_groups_layout) | **PUT** /api/v1/layout/usersAndUserGroups | Put all users and user groups
[**put_workspace_layout**](LayoutApi.md#put_workspace_layout) | **PUT** /api/v1/layout/workspaces/{workspaceId} | Set workspace layout
[**set_analytics_model**](LayoutApi.md#set_analytics_model) | **PUT** /api/v1/layout/workspaces/{workspaceId}/analyticsModel | Set analytics model
[**set_logical_model**](LayoutApi.md#set_logical_model) | **PUT** /api/v1/layout/workspaces/{workspaceId}/logicalModel | Set logical model
[**set_organization_layout**](LayoutApi.md#set_organization_layout) | **PUT** /api/v1/layout/organization | Set organization layout
[**set_pdm_layout**](LayoutApi.md#set_pdm_layout) | **PUT** /api/v1/layout/dataSources/{dataSourceId}/physicalModel | Set data source physical model layout
[**set_user_data_filters**](LayoutApi.md#set_user_data_filters) | **PUT** /api/v1/layout/workspaces/{workspaceId}/userDataFilters | Set user data filters
[**set_user_group_permissions**](LayoutApi.md#set_user_group_permissions) | **PUT** /api/v1/layout/userGroups/{userGroupId}/permissions | Set permissions for the user-group
[**set_user_permissions**](LayoutApi.md#set_user_permissions) | **PUT** /api/v1/layout/users/{userId}/permissions | Set permissions for the user
[**set_workspace_data_filters_layout**](LayoutApi.md#set_workspace_data_filters_layout) | **PUT** /api/v1/layout/workspaceDataFilters | Set all workspace data filters
[**set_workspace_permissions**](LayoutApi.md#set_workspace_permissions) | **PUT** /api/v1/layout/workspaces/{workspaceId}/permissions | Set permissions for the workspace
[**set_workspaces_layout**](LayoutApi.md#set_workspaces_layout) | **PUT** /api/v1/layout/workspaces | Set all workspaces layout


# **get_analytics_model**
> DeclarativeAnalytics get_analytics_model(workspace_id)

Get analytics model

Retrieve current analytics model of the workspace.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_analytics import DeclarativeAnalytics
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get analytics model
        api_response = api_instance.get_analytics_model(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_analytics_model: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |

### Return type

[**DeclarativeAnalytics**](DeclarativeAnalytics.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved current analytics model. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_data_sources_layout**
> DeclarativeDataSources get_data_sources_layout()

Get all data sources

Retrieve all data sources including related physical model.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_data_sources import DeclarativeDataSources
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
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

### Return type

[**DeclarativeDataSources**](DeclarativeDataSources.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved all data sources. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_logical_model**
> DeclarativeModel get_logical_model(workspace_id)

Get logical model

Retrieve current logical model of the workspace in declarative form.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_model import DeclarativeModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    include_parents = True # bool |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get logical model
        api_response = api_instance.get_logical_model(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_logical_model: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get logical model
        api_response = api_instance.get_logical_model(workspace_id, include_parents=include_parents)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_logical_model: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **include_parents** | **bool**|  | [optional]

### Return type

[**DeclarativeModel**](DeclarativeModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved current logical model. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_organization_layout**
> DeclarativeOrganization get_organization_layout()

Get organization layout

Retrieve complete layout of organization, workspaces, user-groups, etc.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_organization import DeclarativeOrganization
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
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

### Return type

[**DeclarativeOrganization**](DeclarativeOrganization.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved all parts of an organization. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_pdm_layout**
> DeclarativePdm get_pdm_layout(data_source_id)

Get data source physical model layout

Retrieve complete layout of tables with their columns

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_pdm import DeclarativePdm
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)
    data_source_id = "dataSourceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get data source physical model layout
        api_response = api_instance.get_pdm_layout(data_source_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_pdm_layout: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  |

### Return type

[**DeclarativePdm**](DeclarativePdm.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved data source physical mode layout. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_data_filters**
> DeclarativeUserDataFilters get_user_data_filters(workspace_id)

Get user data filters

Retrieve current user data filters assigned to the workspace.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_user_data_filters import DeclarativeUserDataFilters
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get user data filters
        api_response = api_instance.get_user_data_filters(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_user_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |

### Return type

[**DeclarativeUserDataFilters**](DeclarativeUserDataFilters.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved current user data filters. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_group_permissions**
> DeclarativeUserGroupPermissions get_user_group_permissions(user_group_id)

Get permissions for the user-group

Retrieve current set of permissions of the user-group in a declarative form.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_user_group_permissions import DeclarativeUserGroupPermissions
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)
    user_group_id = "userGroupId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get permissions for the user-group
        api_response = api_instance.get_user_group_permissions(user_group_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_user_group_permissions: %s\n" % e)
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

# **get_user_groups_layout**
> DeclarativeUserGroups get_user_groups_layout()

Get all user groups

Retrieve all user-groups eventually with parent group.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_user_groups import DeclarativeUserGroups
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
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

### Return type

[**DeclarativeUserGroups**](DeclarativeUserGroups.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved all user groups. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_permissions**
> DeclarativeUserPermissions get_user_permissions(user_id)

Get permissions for the user

Retrieve current set of permissions of the user in a declarative form.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_user_permissions import DeclarativeUserPermissions
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)
    user_id = "userId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get permissions for the user
        api_response = api_instance.get_user_permissions(user_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_user_permissions: %s\n" % e)
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

# **get_users_layout**
> DeclarativeUsers get_users_layout()

Get all users

Retrieve all users including authentication properties.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_users import DeclarativeUsers
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
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

### Return type

[**DeclarativeUsers**](DeclarativeUsers.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved all users. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_users_user_groups_layout**
> DeclarativeUsersUserGroups get_users_user_groups_layout()

Get all users and user groups

Retrieve all users and user groups with theirs properties.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_users_user_groups import DeclarativeUsersUserGroups
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
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

### Return type

[**DeclarativeUsersUserGroups**](DeclarativeUsersUserGroups.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved all users and user groups. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_workspace_data_filters_layout**
> DeclarativeWorkspaceDataFilters get_workspace_data_filters_layout()

Get workspace data filters for all workspaces

Retrieve all workspaces and related workspace data filters (and their settings / values).

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_workspace_data_filters import DeclarativeWorkspaceDataFilters
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
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

### Return type

[**DeclarativeWorkspaceDataFilters**](DeclarativeWorkspaceDataFilters.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved all workspace data filters. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_workspace_layout**
> DeclarativeWorkspaceModel get_workspace_layout(workspace_id)

Get workspace layout

Retrieve current model of the workspace in declarative form.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_workspace_model import DeclarativeWorkspaceModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get workspace layout
        api_response = api_instance.get_workspace_layout(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_workspace_layout: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |

### Return type

[**DeclarativeWorkspaceModel**](DeclarativeWorkspaceModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved the workspace model. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_workspace_permissions**
> DeclarativeWorkspacePermissions get_workspace_permissions(workspace_id)

Get permissions for the workspace

Retrieve current set of permissions of the workspace in a declarative form.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
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
    api_instance = layout_api.LayoutApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get permissions for the workspace
        api_response = api_instance.get_workspace_permissions(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_workspace_permissions: %s\n" % e)
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

# **get_workspaces_layout**
> DeclarativeWorkspaces get_workspaces_layout()

Get all workspaces layout

Gets complete layout of workspaces, their hierarchy, models.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_workspaces import DeclarativeWorkspaces
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
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

### Return type

[**DeclarativeWorkspaces**](DeclarativeWorkspaces.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved layout of all workspaces. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_data_sources_layout**
> put_data_sources_layout(declarative_data_sources)

Put all data sources

Set all data sources including related physical model.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_data_sources import DeclarativeDataSources
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)
    declarative_data_sources = DeclarativeDataSources(
        data_sources=[
            DeclarativeDataSource(
                cache_path=[
                    "[ "dfs", "data" ]. Example used in Apache Drill.",
                ],
                decoded_parameters=[
                    Parameter(
                        name="name_example",
                        value="value_example",
                    ),
                ],
                enable_caching=False,
                id="pg_local_docker-demo",
                name="postgres demo",
                parameters=[
                    Parameter(
                        name="name_example",
                        value="value_example",
                    ),
                ],
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
                                ),
                            ],
                            id="customers",
                            name_prefix="out_gooddata",
                            path=["table_schema","table_name"],
                            type="TABLE",
                        ),
                    ],
                ),
                permissions=[
                    DeclarativeDataSourcePermission(
                        assignee=AssigneeIdentifier(
                            id="id_example",
                            type="user",
                        ),
                        name="MANAGE",
                    ),
                ],
                schema="demo",
                token="Bigquery service account JSON. Encode it using base64!",
                type="POSTGRESQL",
                url="jdbc:postgresql://postgres:5432/gooddata",
                username="demo",
            ),
        ],
    ) # DeclarativeDataSources | 

    # example passing only required values which don't have defaults set
    try:
        # Put all data sources
        api_instance.put_data_sources_layout(declarative_data_sources)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->put_data_sources_layout: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **declarative_data_sources** | [**DeclarativeDataSources**](DeclarativeDataSources.md)|  |

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
**204** | Defined all data sources. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_user_groups_layout**
> put_user_groups_layout(declarative_user_groups)

Put all user groups

Define all user groups with their parents eventually.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_user_groups import DeclarativeUserGroups
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)
    declarative_user_groups = DeclarativeUserGroups(
        user_groups=[
            DeclarativeUserGroup(
                id="employees.all",
                name="admins",
                parents=[
                    UserGroupIdentifier(
                        id="group.admins",
                        type="userGroup",
                    ),
                ],
                permissions=[
                    DeclarativeUserGroupPermission(
                        assignee=AssigneeIdentifier(
                            id="id_example",
                            type="user",
                        ),
                        name="SEE",
                    ),
                ],
            ),
        ],
    ) # DeclarativeUserGroups | 

    # example passing only required values which don't have defaults set
    try:
        # Put all user groups
        api_instance.put_user_groups_layout(declarative_user_groups)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->put_user_groups_layout: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **declarative_user_groups** | [**DeclarativeUserGroups**](DeclarativeUserGroups.md)|  |

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
**204** | Defined all user groups. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_users_layout**
> put_users_layout(declarative_users)

Put all users

Set all users and their authentication properties.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_users import DeclarativeUsers
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)
    declarative_users = DeclarativeUsers(
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
                    ),
                ],
                settings=[
                    DeclarativeSetting(
                        content={},
                        id="/6bUUGjjNSwg0_bs",
                        type="TIMEZONE",
                    ),
                ],
                user_groups=[
                    UserGroupIdentifier(
                        id="group.admins",
                        type="userGroup",
                    ),
                ],
            ),
        ],
    ) # DeclarativeUsers | 

    # example passing only required values which don't have defaults set
    try:
        # Put all users
        api_instance.put_users_layout(declarative_users)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->put_users_layout: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **declarative_users** | [**DeclarativeUsers**](DeclarativeUsers.md)|  |

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
**204** | Defined all users. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_users_user_groups_layout**
> put_users_user_groups_layout(declarative_users_user_groups)

Put all users and user groups

Define all users and user groups with theirs properties.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_users_user_groups import DeclarativeUsersUserGroups
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)
    declarative_users_user_groups = DeclarativeUsersUserGroups(
        user_groups=[
            DeclarativeUserGroup(
                id="employees.all",
                name="admins",
                parents=[
                    UserGroupIdentifier(
                        id="group.admins",
                        type="userGroup",
                    ),
                ],
                permissions=[
                    DeclarativeUserGroupPermission(
                        assignee=AssigneeIdentifier(
                            id="id_example",
                            type="user",
                        ),
                        name="SEE",
                    ),
                ],
            ),
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
                        assignee=AssigneeIdentifier(
                            id="id_example",
                            type="user",
                        ),
                        name="SEE",
                    ),
                ],
                settings=[
                    DeclarativeSetting(
                        content={},
                        id="/6bUUGjjNSwg0_bs",
                        type="TIMEZONE",
                    ),
                ],
                user_groups=[
                    UserGroupIdentifier(
                        id="group.admins",
                        type="userGroup",
                    ),
                ],
            ),
        ],
    ) # DeclarativeUsersUserGroups | 

    # example passing only required values which don't have defaults set
    try:
        # Put all users and user groups
        api_instance.put_users_user_groups_layout(declarative_users_user_groups)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->put_users_user_groups_layout: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **declarative_users_user_groups** | [**DeclarativeUsersUserGroups**](DeclarativeUsersUserGroups.md)|  |

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
**204** | Defined all users and user groups. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_workspace_layout**
> put_workspace_layout(workspace_id, declarative_workspace_model)

Set workspace layout

Set complete layout of workspace, like model, authorization, etc.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_workspace_model import DeclarativeWorkspaceModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    declarative_workspace_model = DeclarativeWorkspaceModel(
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
                        ),
                    ],
                ),
            ],
            analytical_dashboards=[
                DeclarativeAnalyticalDashboard(
                    content={},
                    description="Period to period comparison of revenues in main sectors.",
                    id="revenues-analysis",
                    permissions=[
                        DeclarativeAnalyticalDashboardPermission(
                            assignee=AssigneeIdentifier(
                                id="id_example",
                                type="user",
                            ),
                            name="EDIT",
                        ),
                    ],
                    tags=["Revenues"],
                    title="Revenues analysis",
                ),
            ],
            dashboard_plugins=[
                DeclarativeDashboardPlugin(
                    content={},
                    description="Three dimensional view of data.",
                    id="dashboard-plugin-1",
                    tags=["Revenues"],
                    title="3D map renderer",
                ),
            ],
            filter_contexts=[
                DeclarativeFilterContext(
                    content={},
                    description="Filter Context for Sales team.",
                    id="filter-sales",
                    tags=["Revenues"],
                    title="Filter Context for Sales team",
                ),
            ],
            metrics=[
                DeclarativeMetric(
                    content={},
                    description="Sales for all the data available.",
                    id="total-sales",
                    tags=["Revenues"],
                    title="Total sales",
                ),
            ],
            visualization_objects=[
                DeclarativeVisualizationObject(
                    content={},
                    description="Simple number for total goods in current production.",
                    id="visualization-1",
                    tags=["Revenues"],
                    title="Count of goods",
                ),
            ],
        ),
        ldm=DeclarativeLdm(
            dataset_extensions=[
                DeclarativeDatasetExtension(
                    id="customers",
                    workspace_data_filter_references=[
                        DeclarativeWorkspaceDataFilterReferences(
                            filter_column="filter_id",
                            filter_column_data_type="INT",
                            filter_id=DatasetWorkspaceDataFilterIdentifier(
                                id="country_id",
                                type="workspaceDataFilter",
                            ),
                        ),
                    ],
                ),
            ],
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
                                    value_type="TEXT" | "HYPERLINK" | "GEO" | "GEO_LONGITUDE" | "GEO_LATITUDE",
                                ),
                            ],
                            sort_column="customer_name",
                            sort_direction="ASC" | "DESC",
                            source_column="customer_name",
                            source_column_data_type="STRING",
                            tags=["Customers"],
                            title="Customer Name",
                        ),
                    ],
                    data_source_table_id=DataSourceTableIdentifier(
                        data_source_id="my-postgres",
                        id="customers",
                        path=["table_schema","table_name"],
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
                        ),
                    ],
                    grain=[
                        GrainIdentifier(
                            id="attr.customers.customer_name",
                            type="ATTRIBUTE",
                        ),
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
                                "INT",
                            ],
                            source_columns=["customer_id"],
                        ),
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
                        ),
                    ],
                    workspace_data_filter_references=[
                        DeclarativeWorkspaceDataFilterReferences(
                            filter_column="filter_id",
                            filter_column_data_type="INT",
                            filter_id=DatasetWorkspaceDataFilterIdentifier(
                                id="country_id",
                                type="workspaceDataFilter",
                            ),
                        ),
                    ],
                ),
            ],
            date_instances=[
                DeclarativeDateDataset(
                    description="A customer order date",
                    granularities=[
                        "MINUTE",
                    ],
                    granularities_formatting=GranularitiesFormatting(
                        title_base="title_base_example",
                        title_pattern="%titleBase - %granularityTitle",
                    ),
                    id="date",
                    tags=["Customer dates"],
                    title="Date",
                ),
            ],
        ),
    ) # DeclarativeWorkspaceModel | 

    # example passing only required values which don't have defaults set
    try:
        # Set workspace layout
        api_instance.put_workspace_layout(workspace_id, declarative_workspace_model)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->put_workspace_layout: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **declarative_workspace_model** | [**DeclarativeWorkspaceModel**](DeclarativeWorkspaceModel.md)|  |

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
**204** | The model of the workspace was set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_analytics_model**
> set_analytics_model(workspace_id, declarative_analytics)

Set analytics model

Set effective analytics model of the workspace.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_analytics import DeclarativeAnalytics
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    declarative_analytics = DeclarativeAnalytics(
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
                        ),
                    ],
                ),
            ],
            analytical_dashboards=[
                DeclarativeAnalyticalDashboard(
                    content={},
                    description="Period to period comparison of revenues in main sectors.",
                    id="revenues-analysis",
                    permissions=[
                        DeclarativeAnalyticalDashboardPermission(
                            assignee=AssigneeIdentifier(
                                id="id_example",
                                type="user",
                            ),
                            name="EDIT",
                        ),
                    ],
                    tags=["Revenues"],
                    title="Revenues analysis",
                ),
            ],
            dashboard_plugins=[
                DeclarativeDashboardPlugin(
                    content={},
                    description="Three dimensional view of data.",
                    id="dashboard-plugin-1",
                    tags=["Revenues"],
                    title="3D map renderer",
                ),
            ],
            filter_contexts=[
                DeclarativeFilterContext(
                    content={},
                    description="Filter Context for Sales team.",
                    id="filter-sales",
                    tags=["Revenues"],
                    title="Filter Context for Sales team",
                ),
            ],
            metrics=[
                DeclarativeMetric(
                    content={},
                    description="Sales for all the data available.",
                    id="total-sales",
                    tags=["Revenues"],
                    title="Total sales",
                ),
            ],
            visualization_objects=[
                DeclarativeVisualizationObject(
                    content={},
                    description="Simple number for total goods in current production.",
                    id="visualization-1",
                    tags=["Revenues"],
                    title="Count of goods",
                ),
            ],
        ),
    ) # DeclarativeAnalytics | 

    # example passing only required values which don't have defaults set
    try:
        # Set analytics model
        api_instance.set_analytics_model(workspace_id, declarative_analytics)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->set_analytics_model: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **declarative_analytics** | [**DeclarativeAnalytics**](DeclarativeAnalytics.md)|  |

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
**204** | Analytics model successfully set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_logical_model**
> set_logical_model(workspace_id, declarative_model)

Set logical model

Set effective logical model of the workspace.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_model import DeclarativeModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    declarative_model = DeclarativeModel(
        ldm=DeclarativeLdm(
            dataset_extensions=[
                DeclarativeDatasetExtension(
                    id="customers",
                    workspace_data_filter_references=[
                        DeclarativeWorkspaceDataFilterReferences(
                            filter_column="filter_id",
                            filter_column_data_type="INT",
                            filter_id=DatasetWorkspaceDataFilterIdentifier(
                                id="country_id",
                                type="workspaceDataFilter",
                            ),
                        ),
                    ],
                ),
            ],
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
                                    value_type="TEXT" | "HYPERLINK" | "GEO" | "GEO_LONGITUDE" | "GEO_LATITUDE",
                                ),
                            ],
                            sort_column="customer_name",
                            sort_direction="ASC" | "DESC",
                            source_column="customer_name",
                            source_column_data_type="STRING",
                            tags=["Customers"],
                            title="Customer Name",
                        ),
                    ],
                    data_source_table_id=DataSourceTableIdentifier(
                        data_source_id="my-postgres",
                        id="customers",
                        path=["table_schema","table_name"],
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
                        ),
                    ],
                    grain=[
                        GrainIdentifier(
                            id="attr.customers.customer_name",
                            type="ATTRIBUTE",
                        ),
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
                                "INT",
                            ],
                            source_columns=["customer_id"],
                        ),
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
                        ),
                    ],
                    workspace_data_filter_references=[
                        DeclarativeWorkspaceDataFilterReferences(
                            filter_column="filter_id",
                            filter_column_data_type="INT",
                            filter_id=DatasetWorkspaceDataFilterIdentifier(
                                id="country_id",
                                type="workspaceDataFilter",
                            ),
                        ),
                    ],
                ),
            ],
            date_instances=[
                DeclarativeDateDataset(
                    description="A customer order date",
                    granularities=[
                        "MINUTE",
                    ],
                    granularities_formatting=GranularitiesFormatting(
                        title_base="title_base_example",
                        title_pattern="%titleBase - %granularityTitle",
                    ),
                    id="date",
                    tags=["Customer dates"],
                    title="Date",
                ),
            ],
        ),
    ) # DeclarativeModel | 

    # example passing only required values which don't have defaults set
    try:
        # Set logical model
        api_instance.set_logical_model(workspace_id, declarative_model)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->set_logical_model: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **declarative_model** | [**DeclarativeModel**](DeclarativeModel.md)|  |

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
**204** | Logical model successfully set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_organization_layout**
> set_organization_layout(declarative_organization)

Set organization layout

Sets complete layout of organization, like workspaces, user-groups, etc.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_organization import DeclarativeOrganization
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)
    declarative_organization = DeclarativeOrganization(
        data_sources=[
            DeclarativeDataSource(
                cache_path=[
                    "[ "dfs", "data" ]. Example used in Apache Drill.",
                ],
                decoded_parameters=[
                    Parameter(
                        name="name_example",
                        value="value_example",
                    ),
                ],
                enable_caching=False,
                id="pg_local_docker-demo",
                name="postgres demo",
                parameters=[
                    Parameter(
                        name="name_example",
                        value="value_example",
                    ),
                ],
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
                                ),
                            ],
                            id="customers",
                            name_prefix="out_gooddata",
                            path=["table_schema","table_name"],
                            type="TABLE",
                        ),
                    ],
                ),
                permissions=[
                    DeclarativeDataSourcePermission(
                        assignee=AssigneeIdentifier(
                            id="id_example",
                            type="user",
                        ),
                        name="MANAGE",
                    ),
                ],
                schema="demo",
                token="Bigquery service account JSON. Encode it using base64!",
                type="POSTGRESQL",
                url="jdbc:postgresql://postgres:5432/gooddata",
                username="demo",
            ),
        ],
        organization=DeclarativeOrganizationInfo(
            color_palettes=[
                DeclarativeColorPalette(
                    content={},
                    id="id_example",
                    name="name_example",
                ),
            ],
            csp_directives=[
                DeclarativeCspDirective(
                    directive="directive_example",
                    sources=[
                        "sources_example",
                    ],
                ),
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
                    assignee=AssigneeIdentifier(
                        id="id_example",
                        type="user",
                    ),
                    name="MANAGE",
                ),
            ],
            settings=[
                DeclarativeSetting(
                    content={},
                    id="/6bUUGjjNSwg0_bs",
                    type="TIMEZONE",
                ),
            ],
            themes=[
                DeclarativeTheme(
                    content={},
                    id="id_example",
                    name="name_example",
                ),
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
                    ),
                ],
                permissions=[
                    DeclarativeUserGroupPermission(
                        assignee=AssigneeIdentifier(
                            id="id_example",
                            type="user",
                        ),
                        name="SEE",
                    ),
                ],
            ),
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
                        assignee=AssigneeIdentifier(
                            id="id_example",
                            type="user",
                        ),
                        name="SEE",
                    ),
                ],
                settings=[
                    DeclarativeSetting(
                        content={},
                        id="/6bUUGjjNSwg0_bs",
                        type="TIMEZONE",
                    ),
                ],
                user_groups=[
                    UserGroupIdentifier(
                        id="group.admins",
                        type="userGroup",
                    ),
                ],
            ),
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
                        workspace=WorkspaceIdentifier(
                            id="alpha.sales",
                            type="workspace",
                        ),
                    ),
                ],
            ),
        ],
        workspaces=[
            DeclarativeWorkspace(
                cache_extra_limit=1,
                custom_application_settings=[
                    DeclarativeCustomApplicationSetting(
                        application_name="Modeler",
                        content={},
                        id="modeler.demo",
                    ),
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
                    ),
                ],
                id="alpha.sales",
                model=DeclarativeWorkspaceModel(
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
                                    ),
                                ],
                            ),
                        ],
                        analytical_dashboards=[
                            DeclarativeAnalyticalDashboard(
                                content={},
                                description="Period to period comparison of revenues in main sectors.",
                                id="revenues-analysis",
                                permissions=[
                                    DeclarativeAnalyticalDashboardPermission(
                                        assignee=AssigneeIdentifier(
                                            id="id_example",
                                            type="user",
                                        ),
                                        name="EDIT",
                                    ),
                                ],
                                tags=["Revenues"],
                                title="Revenues analysis",
                            ),
                        ],
                        dashboard_plugins=[
                            DeclarativeDashboardPlugin(
                                content={},
                                description="Three dimensional view of data.",
                                id="dashboard-plugin-1",
                                tags=["Revenues"],
                                title="3D map renderer",
                            ),
                        ],
                        filter_contexts=[
                            DeclarativeFilterContext(
                                content={},
                                description="Filter Context for Sales team.",
                                id="filter-sales",
                                tags=["Revenues"],
                                title="Filter Context for Sales team",
                            ),
                        ],
                        metrics=[
                            DeclarativeMetric(
                                content={},
                                description="Sales for all the data available.",
                                id="total-sales",
                                tags=["Revenues"],
                                title="Total sales",
                            ),
                        ],
                        visualization_objects=[
                            DeclarativeVisualizationObject(
                                content={},
                                description="Simple number for total goods in current production.",
                                id="visualization-1",
                                tags=["Revenues"],
                                title="Count of goods",
                            ),
                        ],
                    ),
                    ldm=DeclarativeLdm(
                        dataset_extensions=[
                            DeclarativeDatasetExtension(
                                id="customers",
                                workspace_data_filter_references=[
                                    DeclarativeWorkspaceDataFilterReferences(
                                        filter_column="filter_id",
                                        filter_column_data_type="INT",
                                        filter_id=DatasetWorkspaceDataFilterIdentifier(
                                            id="country_id",
                                            type="workspaceDataFilter",
                                        ),
                                    ),
                                ],
                            ),
                        ],
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
                                                value_type="TEXT" | "HYPERLINK" | "GEO" | "GEO_LONGITUDE" | "GEO_LATITUDE",
                                            ),
                                        ],
                                        sort_column="customer_name",
                                        sort_direction="ASC" | "DESC",
                                        source_column="customer_name",
                                        source_column_data_type="STRING",
                                        tags=["Customers"],
                                        title="Customer Name",
                                    ),
                                ],
                                data_source_table_id=DataSourceTableIdentifier(
                                    data_source_id="my-postgres",
                                    id="customers",
                                    path=["table_schema","table_name"],
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
                                    ),
                                ],
                                grain=[
                                    GrainIdentifier(
                                        id="attr.customers.customer_name",
                                        type="ATTRIBUTE",
                                    ),
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
                                            "INT",
                                        ],
                                        source_columns=["customer_id"],
                                    ),
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
                                    ),
                                ],
                                workspace_data_filter_references=[
                                    DeclarativeWorkspaceDataFilterReferences(
                                        filter_column="filter_id",
                                        filter_column_data_type="INT",
                                        filter_id=DatasetWorkspaceDataFilterIdentifier(
                                            id="country_id",
                                            type="workspaceDataFilter",
                                        ),
                                    ),
                                ],
                            ),
                        ],
                        date_instances=[
                            DeclarativeDateDataset(
                                description="A customer order date",
                                granularities=[
                                    "MINUTE",
                                ],
                                granularities_formatting=GranularitiesFormatting(
                                    title_base="title_base_example",
                                    title_pattern="%titleBase - %granularityTitle",
                                ),
                                id="date",
                                tags=["Customer dates"],
                                title="Date",
                            ),
                        ],
                    ),
                ),
                name="Alpha Sales",
                parent=WorkspaceIdentifier(
                    id="alpha.sales",
                    type="workspace",
                ),
                permissions=[
                    DeclarativeSingleWorkspacePermission(
                        assignee=AssigneeIdentifier(
                            id="id_example",
                            type="user",
                        ),
                        name="MANAGE",
                    ),
                ],
                prefix="/6bUUGjjNSwg0_bs",
                settings=[
                    DeclarativeSetting(
                        content={},
                        id="/6bUUGjjNSwg0_bs",
                        type="TIMEZONE",
                    ),
                ],
                user_data_filters=[
                    DeclarativeUserDataFilter(
                        description="ID of country setting",
                        id="country_id_setting",
                        maql="{label/country} = "USA" AND {label/date.year} = THIS(YEAR)",
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
                    ),
                ],
            ),
        ],
    ) # DeclarativeOrganization | 

    # example passing only required values which don't have defaults set
    try:
        # Set organization layout
        api_instance.set_organization_layout(declarative_organization)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->set_organization_layout: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **declarative_organization** | [**DeclarativeOrganization**](DeclarativeOrganization.md)|  |

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
**204** | Defined all parts of an organization. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_pdm_layout**
> set_pdm_layout(data_source_id, declarative_pdm)

Set data source physical model layout

Sets complete layout of tables with their columns under corresponding Data Source.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_pdm import DeclarativePdm
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)
    data_source_id = "dataSourceId_example" # str | 
    declarative_pdm = DeclarativePdm(
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
                        ),
                    ],
                    id="customers",
                    name_prefix="out_gooddata",
                    path=["table_schema","table_name"],
                    type="TABLE",
                ),
            ],
        ),
    ) # DeclarativePdm | 

    # example passing only required values which don't have defaults set
    try:
        # Set data source physical model layout
        api_instance.set_pdm_layout(data_source_id, declarative_pdm)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->set_pdm_layout: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  |
 **declarative_pdm** | [**DeclarativePdm**](DeclarativePdm.md)|  |

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
**204** | Data source physical mode layout set successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_user_data_filters**
> set_user_data_filters(workspace_id, declarative_user_data_filters)

Set user data filters

Set user data filters assigned to the workspace.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_user_data_filters import DeclarativeUserDataFilters
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    declarative_user_data_filters = DeclarativeUserDataFilters(
        user_data_filters=[
            DeclarativeUserDataFilter(
                description="ID of country setting",
                id="country_id_setting",
                maql="{label/country} = "USA" AND {label/date.year} = THIS(YEAR)",
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
            ),
        ],
    ) # DeclarativeUserDataFilters | 

    # example passing only required values which don't have defaults set
    try:
        # Set user data filters
        api_instance.set_user_data_filters(workspace_id, declarative_user_data_filters)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->set_user_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **declarative_user_data_filters** | [**DeclarativeUserDataFilters**](DeclarativeUserDataFilters.md)|  |

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
**204** | User data filters successfully set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_user_group_permissions**
> set_user_group_permissions(user_group_id, declarative_user_group_permissions)

Set permissions for the user-group

Set effective permissions for the user-group

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_user_group_permissions import DeclarativeUserGroupPermissions
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)
    user_group_id = "userGroupId_example" # str | 
    declarative_user_group_permissions = DeclarativeUserGroupPermissions(
        permissions=[
            DeclarativeUserGroupPermission(
                assignee=AssigneeIdentifier(
                    id="id_example",
                    type="user",
                ),
                name="SEE",
            ),
        ],
    ) # DeclarativeUserGroupPermissions | 

    # example passing only required values which don't have defaults set
    try:
        # Set permissions for the user-group
        api_instance.set_user_group_permissions(user_group_id, declarative_user_group_permissions)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->set_user_group_permissions: %s\n" % e)
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
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_user_permissions import DeclarativeUserPermissions
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)
    user_id = "userId_example" # str | 
    declarative_user_permissions = DeclarativeUserPermissions(
        permissions=[
            DeclarativeUserPermission(
                assignee=AssigneeIdentifier(
                    id="id_example",
                    type="user",
                ),
                name="SEE",
            ),
        ],
    ) # DeclarativeUserPermissions | 

    # example passing only required values which don't have defaults set
    try:
        # Set permissions for the user
        api_instance.set_user_permissions(user_id, declarative_user_permissions)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->set_user_permissions: %s\n" % e)
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

# **set_workspace_data_filters_layout**
> set_workspace_data_filters_layout(declarative_workspace_data_filters)

Set all workspace data filters

Sets workspace data filters in all workspaces in entire organization.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_workspace_data_filters import DeclarativeWorkspaceDataFilters
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)
    declarative_workspace_data_filters = DeclarativeWorkspaceDataFilters(
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
                        workspace=WorkspaceIdentifier(
                            id="alpha.sales",
                            type="workspace",
                        ),
                    ),
                ],
            ),
        ],
    ) # DeclarativeWorkspaceDataFilters | 

    # example passing only required values which don't have defaults set
    try:
        # Set all workspace data filters
        api_instance.set_workspace_data_filters_layout(declarative_workspace_data_filters)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->set_workspace_data_filters_layout: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **declarative_workspace_data_filters** | [**DeclarativeWorkspaceDataFilters**](DeclarativeWorkspaceDataFilters.md)|  |

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
**204** | All workspace data filters set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_workspace_permissions**
> set_workspace_permissions(workspace_id, declarative_workspace_permissions)

Set permissions for the workspace

Set effective permissions for the workspace

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
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
    api_instance = layout_api.LayoutApi(api_client)
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
        print("Exception when calling LayoutApi->set_workspace_permissions: %s\n" % e)
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

# **set_workspaces_layout**
> set_workspaces_layout(declarative_workspaces)

Set all workspaces layout

Sets complete layout of workspaces, their hierarchy, models.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_workspaces import DeclarativeWorkspaces
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = layout_api.LayoutApi(api_client)
    declarative_workspaces = DeclarativeWorkspaces(
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
                        workspace=WorkspaceIdentifier(
                            id="alpha.sales",
                            type="workspace",
                        ),
                    ),
                ],
            ),
        ],
        workspaces=[
            DeclarativeWorkspace(
                cache_extra_limit=1,
                custom_application_settings=[
                    DeclarativeCustomApplicationSetting(
                        application_name="Modeler",
                        content={},
                        id="modeler.demo",
                    ),
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
                    ),
                ],
                id="alpha.sales",
                model=DeclarativeWorkspaceModel(
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
                                    ),
                                ],
                            ),
                        ],
                        analytical_dashboards=[
                            DeclarativeAnalyticalDashboard(
                                content={},
                                description="Period to period comparison of revenues in main sectors.",
                                id="revenues-analysis",
                                permissions=[
                                    DeclarativeAnalyticalDashboardPermission(
                                        assignee=AssigneeIdentifier(
                                            id="id_example",
                                            type="user",
                                        ),
                                        name="EDIT",
                                    ),
                                ],
                                tags=["Revenues"],
                                title="Revenues analysis",
                            ),
                        ],
                        dashboard_plugins=[
                            DeclarativeDashboardPlugin(
                                content={},
                                description="Three dimensional view of data.",
                                id="dashboard-plugin-1",
                                tags=["Revenues"],
                                title="3D map renderer",
                            ),
                        ],
                        filter_contexts=[
                            DeclarativeFilterContext(
                                content={},
                                description="Filter Context for Sales team.",
                                id="filter-sales",
                                tags=["Revenues"],
                                title="Filter Context for Sales team",
                            ),
                        ],
                        metrics=[
                            DeclarativeMetric(
                                content={},
                                description="Sales for all the data available.",
                                id="total-sales",
                                tags=["Revenues"],
                                title="Total sales",
                            ),
                        ],
                        visualization_objects=[
                            DeclarativeVisualizationObject(
                                content={},
                                description="Simple number for total goods in current production.",
                                id="visualization-1",
                                tags=["Revenues"],
                                title="Count of goods",
                            ),
                        ],
                    ),
                    ldm=DeclarativeLdm(
                        dataset_extensions=[
                            DeclarativeDatasetExtension(
                                id="customers",
                                workspace_data_filter_references=[
                                    DeclarativeWorkspaceDataFilterReferences(
                                        filter_column="filter_id",
                                        filter_column_data_type="INT",
                                        filter_id=DatasetWorkspaceDataFilterIdentifier(
                                            id="country_id",
                                            type="workspaceDataFilter",
                                        ),
                                    ),
                                ],
                            ),
                        ],
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
                                                value_type="TEXT" | "HYPERLINK" | "GEO" | "GEO_LONGITUDE" | "GEO_LATITUDE",
                                            ),
                                        ],
                                        sort_column="customer_name",
                                        sort_direction="ASC" | "DESC",
                                        source_column="customer_name",
                                        source_column_data_type="STRING",
                                        tags=["Customers"],
                                        title="Customer Name",
                                    ),
                                ],
                                data_source_table_id=DataSourceTableIdentifier(
                                    data_source_id="my-postgres",
                                    id="customers",
                                    path=["table_schema","table_name"],
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
                                    ),
                                ],
                                grain=[
                                    GrainIdentifier(
                                        id="attr.customers.customer_name",
                                        type="ATTRIBUTE",
                                    ),
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
                                            "INT",
                                        ],
                                        source_columns=["customer_id"],
                                    ),
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
                                    ),
                                ],
                                workspace_data_filter_references=[
                                    DeclarativeWorkspaceDataFilterReferences(
                                        filter_column="filter_id",
                                        filter_column_data_type="INT",
                                        filter_id=DatasetWorkspaceDataFilterIdentifier(
                                            id="country_id",
                                            type="workspaceDataFilter",
                                        ),
                                    ),
                                ],
                            ),
                        ],
                        date_instances=[
                            DeclarativeDateDataset(
                                description="A customer order date",
                                granularities=[
                                    "MINUTE",
                                ],
                                granularities_formatting=GranularitiesFormatting(
                                    title_base="title_base_example",
                                    title_pattern="%titleBase - %granularityTitle",
                                ),
                                id="date",
                                tags=["Customer dates"],
                                title="Date",
                            ),
                        ],
                    ),
                ),
                name="Alpha Sales",
                parent=WorkspaceIdentifier(
                    id="alpha.sales",
                    type="workspace",
                ),
                permissions=[
                    DeclarativeSingleWorkspacePermission(
                        assignee=AssigneeIdentifier(
                            id="id_example",
                            type="user",
                        ),
                        name="MANAGE",
                    ),
                ],
                prefix="/6bUUGjjNSwg0_bs",
                settings=[
                    DeclarativeSetting(
                        content={},
                        id="/6bUUGjjNSwg0_bs",
                        type="TIMEZONE",
                    ),
                ],
                user_data_filters=[
                    DeclarativeUserDataFilter(
                        description="ID of country setting",
                        id="country_id_setting",
                        maql="{label/country} = "USA" AND {label/date.year} = THIS(YEAR)",
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
                    ),
                ],
            ),
        ],
    ) # DeclarativeWorkspaces | 

    # example passing only required values which don't have defaults set
    try:
        # Set all workspaces layout
        api_instance.set_workspaces_layout(declarative_workspaces)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->set_workspaces_layout: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **declarative_workspaces** | [**DeclarativeWorkspaces**](DeclarativeWorkspaces.md)|  |

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
**204** | All workspaces layout set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


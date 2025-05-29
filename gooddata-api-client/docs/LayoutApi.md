# gooddata_api_client.LayoutApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_analytics_model**](LayoutApi.md#get_analytics_model) | **GET** /api/v1/layout/workspaces/{workspaceId}/analyticsModel | Get analytics model
[**get_automations**](LayoutApi.md#get_automations) | **GET** /api/v1/layout/workspaces/{workspaceId}/automations | Get automations
[**get_data_source_permissions**](LayoutApi.md#get_data_source_permissions) | **GET** /api/v1/layout/dataSources/{dataSourceId}/permissions | Get permissions for the data source
[**get_data_sources_layout**](LayoutApi.md#get_data_sources_layout) | **GET** /api/v1/layout/dataSources | Get all data sources
[**get_export_templates_layout**](LayoutApi.md#get_export_templates_layout) | **GET** /api/v1/layout/exportTemplates | Get all export templates layout
[**get_filter_views**](LayoutApi.md#get_filter_views) | **GET** /api/v1/layout/workspaces/{workspaceId}/filterViews | Get filter views
[**get_identity_providers_layout**](LayoutApi.md#get_identity_providers_layout) | **GET** /api/v1/layout/identityProviders | Get all identity providers layout
[**get_logical_model**](LayoutApi.md#get_logical_model) | **GET** /api/v1/layout/workspaces/{workspaceId}/logicalModel | Get logical model
[**get_notification_channels_layout**](LayoutApi.md#get_notification_channels_layout) | **GET** /api/v1/layout/notificationChannels | Get all notification channels layout
[**get_organization_layout**](LayoutApi.md#get_organization_layout) | **GET** /api/v1/layout/organization | Get organization layout
[**get_organization_permissions**](LayoutApi.md#get_organization_permissions) | **GET** /api/v1/layout/organization/permissions | Get organization permissions
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
[**set_automations**](LayoutApi.md#set_automations) | **PUT** /api/v1/layout/workspaces/{workspaceId}/automations | Set automations
[**set_data_source_permissions**](LayoutApi.md#set_data_source_permissions) | **PUT** /api/v1/layout/dataSources/{dataSourceId}/permissions | Set data source permissions.
[**set_export_templates**](LayoutApi.md#set_export_templates) | **PUT** /api/v1/layout/exportTemplates | Set all export templates
[**set_filter_views**](LayoutApi.md#set_filter_views) | **PUT** /api/v1/layout/workspaces/{workspaceId}/filterViews | Set filter views
[**set_identity_providers**](LayoutApi.md#set_identity_providers) | **PUT** /api/v1/layout/identityProviders | Set all identity providers
[**set_logical_model**](LayoutApi.md#set_logical_model) | **PUT** /api/v1/layout/workspaces/{workspaceId}/logicalModel | Set logical model
[**set_notification_channels**](LayoutApi.md#set_notification_channels) | **PUT** /api/v1/layout/notificationChannels | Set all notification channels
[**set_organization_layout**](LayoutApi.md#set_organization_layout) | **PUT** /api/v1/layout/organization | Set organization layout
[**set_organization_permissions**](LayoutApi.md#set_organization_permissions) | **PUT** /api/v1/layout/organization/permissions | Set organization permissions
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
    exclude = [
        "ACTIVITY_INFO",
    ] # [str] |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get analytics model
        api_response = api_instance.get_analytics_model(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_analytics_model: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get analytics model
        api_response = api_instance.get_analytics_model(workspace_id, exclude=exclude)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_analytics_model: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **exclude** | **[str]**|  | [optional]

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

# **get_automations**
> [DeclarativeAutomation] get_automations(workspace_id)

Get automations

Retrieve automations for the specific workspace

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_automation import DeclarativeAutomation
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
    exclude = [
        "ACTIVITY_INFO",
    ] # [str] |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get automations
        api_response = api_instance.get_automations(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_automations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get automations
        api_response = api_instance.get_automations(workspace_id, exclude=exclude)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_automations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **exclude** | **[str]**|  | [optional]

### Return type

[**[DeclarativeAutomation]**](DeclarativeAutomation.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved automations. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_data_source_permissions**
> DeclarativeDataSourcePermissions get_data_source_permissions(data_source_id)

Get permissions for the data source

Retrieve current set of permissions of the data source in a declarative form.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_data_source_permissions import DeclarativeDataSourcePermissions
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
        # Get permissions for the data source
        api_response = api_instance.get_data_source_permissions(data_source_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_data_source_permissions: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  |

### Return type

[**DeclarativeDataSourcePermissions**](DeclarativeDataSourcePermissions.md)

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

# **get_export_templates_layout**
> DeclarativeExportTemplates get_export_templates_layout()

Get all export templates layout

Gets complete layout of export templates.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_export_templates import DeclarativeExportTemplates
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
        # Get all export templates layout
        api_response = api_instance.get_export_templates_layout()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_export_templates_layout: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**DeclarativeExportTemplates**](DeclarativeExportTemplates.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved layout of all export templates. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_filter_views**
> [DeclarativeFilterView] get_filter_views(workspace_id)

Get filter views

Retrieve filter views for the specific workspace

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_filter_view import DeclarativeFilterView
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
    exclude = [
        "ACTIVITY_INFO",
    ] # [str] |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get filter views
        api_response = api_instance.get_filter_views(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_filter_views: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get filter views
        api_response = api_instance.get_filter_views(workspace_id, exclude=exclude)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_filter_views: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **exclude** | **[str]**|  | [optional]

### Return type

[**[DeclarativeFilterView]**](DeclarativeFilterView.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved filterViews. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_identity_providers_layout**
> [DeclarativeIdentityProvider] get_identity_providers_layout()

Get all identity providers layout

Gets complete layout of identity providers.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_identity_provider import DeclarativeIdentityProvider
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
        # Get all identity providers layout
        api_response = api_instance.get_identity_providers_layout()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_identity_providers_layout: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**[DeclarativeIdentityProvider]**](DeclarativeIdentityProvider.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved layout of all identity providers. |  -  |

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

# **get_notification_channels_layout**
> DeclarativeNotificationChannels get_notification_channels_layout()

Get all notification channels layout

Gets complete layout of notification channels.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_notification_channels import DeclarativeNotificationChannels
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
        # Get all notification channels layout
        api_response = api_instance.get_notification_channels_layout()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_notification_channels_layout: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**DeclarativeNotificationChannels**](DeclarativeNotificationChannels.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved layout of all notification channels. |  -  |

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
    exclude = [
        "ACTIVITY_INFO",
    ] # [str] |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get organization layout
        api_response = api_instance.get_organization_layout(exclude=exclude)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_organization_layout: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **exclude** | **[str]**|  | [optional]

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

# **get_organization_permissions**
> [DeclarativeOrganizationPermission] get_organization_permissions()

Get organization permissions

Retrieve organization permissions

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_organization_permission import DeclarativeOrganizationPermission
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
        # Get organization permissions
        api_response = api_instance.get_organization_permissions()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_organization_permissions: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**[DeclarativeOrganizationPermission]**](DeclarativeOrganizationPermission.md)

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
    exclude = [
        "ACTIVITY_INFO",
    ] # [str] |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get workspace layout
        api_response = api_instance.get_workspace_layout(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_workspace_layout: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get workspace layout
        api_response = api_instance.get_workspace_layout(workspace_id, exclude=exclude)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_workspace_layout: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **exclude** | **[str]**|  | [optional]

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
    exclude = [
        "ACTIVITY_INFO",
    ] # [str] |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all workspaces layout
        api_response = api_instance.get_workspaces_layout(exclude=exclude)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->get_workspaces_layout: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **exclude** | **[str]**|  | [optional]

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
                authentication_type="USERNAME_PASSWORD",
                cache_strategy="ALWAYS",
                client_id="client1234",
                client_secret="client_secret_example",
                decoded_parameters=[
                    Parameter(
                        name="name_example",
                        value="value_example",
                    ),
                ],
                id="pg_local_docker-demo",
                name="postgres demo",
                parameters=[
                    Parameter(
                        name="name_example",
                        value="value_example",
                    ),
                ],
                password="*****",
                permissions=[
                    DeclarativeDataSourcePermission(
                        assignee=AssigneeIdentifier(
                            id="id_example",
                            type="user",
                        ),
                        name="MANAGE",
                    ),
                ],
                private_key="private_key_example",
                private_key_passphrase="private_key_passphrase_example",
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
                    DeclarativeUserGroupIdentifier(
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
                        content=JsonNode(),
                        id="/6bUUGjjNSwg0_bs",
                        type="TIMEZONE",
                    ),
                ],
                user_groups=[
                    DeclarativeUserGroupIdentifier(
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
                    DeclarativeUserGroupIdentifier(
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
                        content=JsonNode(),
                        id="/6bUUGjjNSwg0_bs",
                        type="TIMEZONE",
                    ),
                ],
                user_groups=[
                    DeclarativeUserGroupIdentifier(
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
                        DeclarativeAnalyticalDashboardPermissionsInner(None),
                    ],
                ),
            ],
            analytical_dashboards=[
                DeclarativeAnalyticalDashboard(
                    content=JsonNode(),
                    created_at="2023-07-20 12:30",
                    created_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    description="Period to period comparison of revenues in main sectors.",
                    id="revenues-analysis",
                    modified_at="2023-07-20 12:30",
                    modified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    permissions=[
                        DeclarativeAnalyticalDashboardPermissionsInner(None),
                    ],
                    tags=["Revenues"],
                    title="Revenues analysis",
                ),
            ],
            attribute_hierarchies=[
                DeclarativeAttributeHierarchy(
                    content=JsonNode(),
                    created_at="["2023-07-20 12:30"]",
                    created_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    description="Simple number for total goods in current production.",
                    id="hierarchy-1",
                    modified_at="["2023-07-20 12:30"]",
                    modified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    tags=["Revenues"],
                    title="Count of goods",
                ),
            ],
            dashboard_plugins=[
                DeclarativeDashboardPlugin(
                    content=JsonNode(),
                    created_at="["2023-07-20 12:30"]",
                    created_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    description="Three dimensional view of data.",
                    id="dashboard-plugin-1",
                    modified_at="["2023-07-20 12:30"]",
                    modified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    tags=["Revenues"],
                    title="3D map renderer",
                ),
            ],
            export_definitions=[
                DeclarativeExportDefinition(
                    created_at="["2023-07-20 12:30"]",
                    created_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    description="Simple number for total goods in current production.",
                    id="export-definition-1",
                    modified_at="["2023-07-20 12:30"]",
                    modified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    request_payload=DeclarativeExportDefinitionRequestPayload(None),
                    tags=["Revenues"],
                    title="My regular export",
                ),
            ],
            filter_contexts=[
                DeclarativeFilterContext(
                    content=JsonNode(),
                    description="Filter Context for Sales team.",
                    id="filter-sales",
                    tags=["Revenues"],
                    title="Filter Context for Sales team",
                ),
            ],
            metrics=[
                DeclarativeMetric(
                    content=JsonNode(),
                    created_at="["2023-07-20 12:30"]",
                    created_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    description="Sales for all the data available.",
                    id="total-sales",
                    modified_at="["2023-07-20 12:30"]",
                    modified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    tags=["Revenues"],
                    title="Total sales",
                ),
            ],
            visualization_objects=[
                DeclarativeVisualizationObject(
                    content=JsonNode(),
                    created_at="["2023-07-20 12:30"]",
                    created_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    description="Simple number for total goods in current production.",
                    id="visualization-1",
                    modified_at="["2023-07-20 12:30"]",
                    modified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
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
                                    value_type="TEXT",
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
                            sources=[
                                DeclarativeReferenceSource(
                                    column="customer_id",
                                    data_type="STRING",
                                    target=GrainIdentifier(
                                        id="attr.customers.customer_name",
                                        type="ATTRIBUTE",
                                    ),
                                ),
                            ],
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
                        DeclarativeAnalyticalDashboardPermissionsInner(None),
                    ],
                ),
            ],
            analytical_dashboards=[
                DeclarativeAnalyticalDashboard(
                    content=JsonNode(),
                    created_at="2023-07-20 12:30",
                    created_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    description="Period to period comparison of revenues in main sectors.",
                    id="revenues-analysis",
                    modified_at="2023-07-20 12:30",
                    modified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    permissions=[
                        DeclarativeAnalyticalDashboardPermissionsInner(None),
                    ],
                    tags=["Revenues"],
                    title="Revenues analysis",
                ),
            ],
            attribute_hierarchies=[
                DeclarativeAttributeHierarchy(
                    content=JsonNode(),
                    created_at="["2023-07-20 12:30"]",
                    created_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    description="Simple number for total goods in current production.",
                    id="hierarchy-1",
                    modified_at="["2023-07-20 12:30"]",
                    modified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    tags=["Revenues"],
                    title="Count of goods",
                ),
            ],
            dashboard_plugins=[
                DeclarativeDashboardPlugin(
                    content=JsonNode(),
                    created_at="["2023-07-20 12:30"]",
                    created_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    description="Three dimensional view of data.",
                    id="dashboard-plugin-1",
                    modified_at="["2023-07-20 12:30"]",
                    modified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    tags=["Revenues"],
                    title="3D map renderer",
                ),
            ],
            export_definitions=[
                DeclarativeExportDefinition(
                    created_at="["2023-07-20 12:30"]",
                    created_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    description="Simple number for total goods in current production.",
                    id="export-definition-1",
                    modified_at="["2023-07-20 12:30"]",
                    modified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    request_payload=DeclarativeExportDefinitionRequestPayload(None),
                    tags=["Revenues"],
                    title="My regular export",
                ),
            ],
            filter_contexts=[
                DeclarativeFilterContext(
                    content=JsonNode(),
                    description="Filter Context for Sales team.",
                    id="filter-sales",
                    tags=["Revenues"],
                    title="Filter Context for Sales team",
                ),
            ],
            metrics=[
                DeclarativeMetric(
                    content=JsonNode(),
                    created_at="["2023-07-20 12:30"]",
                    created_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    description="Sales for all the data available.",
                    id="total-sales",
                    modified_at="["2023-07-20 12:30"]",
                    modified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    tags=["Revenues"],
                    title="Total sales",
                ),
            ],
            visualization_objects=[
                DeclarativeVisualizationObject(
                    content=JsonNode(),
                    created_at="["2023-07-20 12:30"]",
                    created_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    description="Simple number for total goods in current production.",
                    id="visualization-1",
                    modified_at="["2023-07-20 12:30"]",
                    modified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
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

# **set_automations**
> set_automations(workspace_id, declarative_automation)

Set automations

Set automations for the specific workspace.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_automation import DeclarativeAutomation
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
    declarative_automation = [
        DeclarativeAutomation(
            alert=AutomationAlert(
                condition=AutomationAlertCondition(None),
                execution=AlertAfm(
                    attributes=[
                        AttributeItem(
                            label=AfmObjectIdentifierLabel(
                                identifier=AfmObjectIdentifierLabelIdentifier(
                                    id="sample_item.price",
                                    type="label",
                                ),
                            ),
                            local_identifier="attribute_1",
                            show_all_values=False,
                        ),
                    ],
                    aux_measures=[
                        MeasureItem(
                            definition=MeasureDefinition(),
                            local_identifier="metric_1",
                        ),
                    ],
                    filters=[
                        FilterDefinition(),
                    ],
                    measures=[
                        MeasureItem(
                            definition=MeasureDefinition(),
                            local_identifier="metric_1",
                        ),
                    ],
                ),
                trigger="ALWAYS",
            ),
            analytical_dashboard=DeclarativeAnalyticalDashboardIdentifier(
                id="dashboard123",
                type="analyticalDashboard",
            ),
            created_at="2023-07-20 12:30",
            created_by=DeclarativeUserIdentifier(
                id="employee123",
                type="user",
            ),
            description="description_example",
            details={
                "key": "key_example",
            },
            export_definitions=[
                DeclarativeExportDefinitionIdentifier(
                    id="export123",
                    type="exportDefinition",
                ),
            ],
            external_recipients=[
                AutomationExternalRecipient(
                    email="email_example",
                ),
            ],
            id="/6bUUGjjNSwg0_bs",
            image_exports=[
                AutomationImageExport(
                    request_payload=ImageExportRequest(
                        dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                        file_name="filename",
                        format="PNG",
                        metadata=JsonNode(),
                        widget_ids=[
                            "widget_ids_example",
                        ],
                    ),
                ),
            ],
            metadata=AutomationMetadata(
                visible_filters=[
                    VisibleFilter(
                        is_all_time_date_filter=False,
                        local_identifier="local_identifier_example",
                        title="title_example",
                    ),
                ],
                widget="widget_example",
            ),
            modified_at="2023-07-20 12:30",
            modified_by=DeclarativeUserIdentifier(
                id="employee123",
                type="user",
            ),
            notification_channel=DeclarativeNotificationChannelIdentifier(
                id="webhook123",
                type="notificationChannel",
            ),
            recipients=[
                DeclarativeUserIdentifier(
                    id="employee123",
                    type="user",
                ),
            ],
            schedule=AutomationSchedule(
                cron="0 */30 9-17 ? * MON-FRI",
                first_run=dateutil_parser('2025-01-01T12:00:00Z'),
                timezone="Europe/Prague",
            ),
            state="ACTIVE",
            tabular_exports=[
                AutomationTabularExport(
                    request_payload=TabularExportRequest(
                        custom_override=CustomOverride(
                            labels={
                                "key": CustomLabel(
                                    title="title_example",
                                ),
                            },
                            metrics={
                                "key": CustomMetric(
                                    format="format_example",
                                    title="title_example",
                                ),
                            },
                        ),
                        execution_result="ff483727196c9dc862c7fd3a5a84df55c96d61a4",
                        file_name="result",
                        format="CSV",
                        metadata=JsonNode(),
                        related_dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                        settings=Settings(
                            merge_headers=True,
                            pdf_page_size="a4 landscape",
                            pdf_table_style=[
                                PdfTableStyle(
                                    properties=[
                                        PdfTableStyleProperty(
                                            key="key_example",
                                            value="value_example",
                                        ),
                                    ],
                                    selector="selector_example",
                                ),
                            ],
                            pdf_top_left_content="Good",
                            pdf_top_right_content="Morning",
                            show_filters=False,
                        ),
                        visualization_object="f7c359bc-c230-4487-b15b-ad9685bcb537",
                        visualization_object_custom_filters=[
                            {},
                        ],
                    ),
                ),
            ],
            tags=[
                "["Revenue","Sales"]",
            ],
            title="title_example",
            visual_exports=[
                AutomationVisualExport(
                    request_payload=VisualExportRequest(
                        dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                        file_name="filename",
                        metadata={},
                    ),
                ),
            ],
        ),
    ] # [DeclarativeAutomation] | 

    # example passing only required values which don't have defaults set
    try:
        # Set automations
        api_instance.set_automations(workspace_id, declarative_automation)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->set_automations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **declarative_automation** | [**[DeclarativeAutomation]**](DeclarativeAutomation.md)|  |

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
**204** | Automations successfully set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_data_source_permissions**
> set_data_source_permissions(data_source_id, declarative_data_source_permissions)

Set data source permissions.

set data source permissions.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_data_source_permissions import DeclarativeDataSourcePermissions
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
    declarative_data_source_permissions = DeclarativeDataSourcePermissions(
        permissions=[
            DeclarativeDataSourcePermission(
                assignee=AssigneeIdentifier(
                    id="id_example",
                    type="user",
                ),
                name="MANAGE",
            ),
        ],
    ) # DeclarativeDataSourcePermissions | 

    # example passing only required values which don't have defaults set
    try:
        # Set data source permissions.
        api_instance.set_data_source_permissions(data_source_id, declarative_data_source_permissions)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->set_data_source_permissions: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  |
 **declarative_data_source_permissions** | [**DeclarativeDataSourcePermissions**](DeclarativeDataSourcePermissions.md)|  |

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

# **set_export_templates**
> set_export_templates(declarative_export_templates)

Set all export templates

Sets export templates in organization.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_export_templates import DeclarativeExportTemplates
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
    declarative_export_templates = DeclarativeExportTemplates(
        export_templates=[
            DeclarativeExportTemplate(
                dashboard_slides_template=DashboardSlidesTemplate(
                    applied_on=["PDF","PPTX"],
                    content_slide=ContentSlideTemplate(
                        description_field="{{dashboardFilters}}",
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                    ),
                    cover_slide=CoverSlideTemplate(
                        background_image=True,
                        description_field="Exported at: {{exportedAt}}",
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                    ),
                    intro_slide=IntroSlideTemplate(
                        background_image=True,
                        description_field='''About:
{{dashboardDescription}}

{{dashboardFilters}}''',
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        title_field="Introduction",
                    ),
                    section_slide=SectionSlideTemplate(
                        background_image=True,
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                    ),
                ),
                id="default-export-template",
                name="My default export template",
                widget_slides_template=WidgetSlidesTemplate(
                    applied_on=["PDF","PPTX"],
                    content_slide=ContentSlideTemplate(
                        description_field="{{dashboardFilters}}",
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                    ),
                ),
            ),
        ],
    ) # DeclarativeExportTemplates | 

    # example passing only required values which don't have defaults set
    try:
        # Set all export templates
        api_instance.set_export_templates(declarative_export_templates)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->set_export_templates: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **declarative_export_templates** | [**DeclarativeExportTemplates**](DeclarativeExportTemplates.md)|  |

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
**204** | All export templates set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_filter_views**
> set_filter_views(workspace_id, declarative_filter_view)

Set filter views

Set filter views for the specific workspace.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_filter_view import DeclarativeFilterView
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
    declarative_filter_view = [
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
                "["Revenue","Sales"]",
            ],
            title="title_example",
            user=DeclarativeUserIdentifier(
                id="employee123",
                type="user",
            ),
        ),
    ] # [DeclarativeFilterView] | 

    # example passing only required values which don't have defaults set
    try:
        # Set filter views
        api_instance.set_filter_views(workspace_id, declarative_filter_view)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->set_filter_views: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **declarative_filter_view** | [**[DeclarativeFilterView]**](DeclarativeFilterView.md)|  |

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
**204** | FilterViews successfully set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_identity_providers**
> set_identity_providers(declarative_identity_provider)

Set all identity providers

Sets identity providers in organization.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_identity_provider import DeclarativeIdentityProvider
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
    declarative_identity_provider = [
        DeclarativeIdentityProvider(
            custom_claim_mapping={
                "key": "key_example",
            },
            id="filterView-1",
            identifiers=["gooddata.com"],
            oauth_client_id="oauth_client_id_example",
            oauth_client_secret="oauth_client_secret_example",
            oauth_issuer_location="oauth_issuer_location_example",
            saml_metadata="saml_metadata_example",
        ),
    ] # [DeclarativeIdentityProvider] | 

    # example passing only required values which don't have defaults set
    try:
        # Set all identity providers
        api_instance.set_identity_providers(declarative_identity_provider)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->set_identity_providers: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **declarative_identity_provider** | [**[DeclarativeIdentityProvider]**](DeclarativeIdentityProvider.md)|  |

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
**204** | All identity providers set. |  -  |

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
                                    value_type="TEXT",
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
                            sources=[
                                DeclarativeReferenceSource(
                                    column="customer_id",
                                    data_type="STRING",
                                    target=GrainIdentifier(
                                        id="attr.customers.customer_name",
                                        type="ATTRIBUTE",
                                    ),
                                ),
                            ],
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

# **set_notification_channels**
> set_notification_channels(declarative_notification_channels)

Set all notification channels

Sets notification channels in organization.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_notification_channels import DeclarativeNotificationChannels
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
    declarative_notification_channels = DeclarativeNotificationChannels(
        notification_channels=[
            DeclarativeNotificationChannel(
                allowed_recipients="INTERNAL",
                custom_dashboard_url="custom_dashboard_url_example",
                dashboard_link_visibility="INTERNAL_ONLY",
                description="This is a channel",
                destination=DeclarativeNotificationChannelDestination(None),
                id="notification-channel-1",
                in_platform_notification="DISABLED",
                name="channel",
            ),
        ],
    ) # DeclarativeNotificationChannels | 

    # example passing only required values which don't have defaults set
    try:
        # Set all notification channels
        api_instance.set_notification_channels(declarative_notification_channels)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->set_notification_channels: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **declarative_notification_channels** | [**DeclarativeNotificationChannels**](DeclarativeNotificationChannels.md)|  |

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
**204** | All notification channels set. |  -  |

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
                authentication_type="USERNAME_PASSWORD",
                cache_strategy="ALWAYS",
                client_id="client1234",
                client_secret="client_secret_example",
                decoded_parameters=[
                    Parameter(
                        name="name_example",
                        value="value_example",
                    ),
                ],
                id="pg_local_docker-demo",
                name="postgres demo",
                parameters=[
                    Parameter(
                        name="name_example",
                        value="value_example",
                    ),
                ],
                password="*****",
                permissions=[
                    DeclarativeDataSourcePermission(
                        assignee=AssigneeIdentifier(
                            id="id_example",
                            type="user",
                        ),
                        name="MANAGE",
                    ),
                ],
                private_key="private_key_example",
                private_key_passphrase="private_key_passphrase_example",
                schema="demo",
                token="Bigquery service account JSON. Encode it using base64!",
                type="POSTGRESQL",
                url="jdbc:postgresql://postgres:5432/gooddata",
                username="demo",
            ),
        ],
        export_templates=[
            DeclarativeExportTemplate(
                dashboard_slides_template=DashboardSlidesTemplate(
                    applied_on=["PDF","PPTX"],
                    content_slide=ContentSlideTemplate(
                        description_field="{{dashboardFilters}}",
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                    ),
                    cover_slide=CoverSlideTemplate(
                        background_image=True,
                        description_field="Exported at: {{exportedAt}}",
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                    ),
                    intro_slide=IntroSlideTemplate(
                        background_image=True,
                        description_field='''About:
{{dashboardDescription}}

{{dashboardFilters}}''',
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        title_field="Introduction",
                    ),
                    section_slide=SectionSlideTemplate(
                        background_image=True,
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                    ),
                ),
                id="default-export-template",
                name="My default export template",
                widget_slides_template=WidgetSlidesTemplate(
                    applied_on=["PDF","PPTX"],
                    content_slide=ContentSlideTemplate(
                        description_field="{{dashboardFilters}}",
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                    ),
                ),
            ),
        ],
        identity_providers=[
            DeclarativeIdentityProvider(
                custom_claim_mapping={
                    "key": "key_example",
                },
                id="filterView-1",
                identifiers=["gooddata.com"],
                oauth_client_id="oauth_client_id_example",
                oauth_client_secret="oauth_client_secret_example",
                oauth_issuer_location="oauth_issuer_location_example",
                saml_metadata="saml_metadata_example",
            ),
        ],
        jwks=[
            DeclarativeJwk(
                content=DeclarativeJwkSpecification(),
                id="jwk-1",
            ),
        ],
        notification_channels=[
            DeclarativeNotificationChannel(
                allowed_recipients="INTERNAL",
                custom_dashboard_url="custom_dashboard_url_example",
                dashboard_link_visibility="INTERNAL_ONLY",
                description="This is a channel",
                destination=DeclarativeNotificationChannelDestination(None),
                id="notification-channel-1",
                in_platform_notification="DISABLED",
                name="channel",
            ),
        ],
        organization=DeclarativeOrganizationInfo(
            allowed_origins=[
                "allowed_origins_example",
            ],
            color_palettes=[
                DeclarativeColorPalette(
                    content=JsonNode(),
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
            early_access_values=[
                "early_access_values_example",
            ],
            hostname="alpha.com",
            id="Alpha corporation",
            name="Alpha corporation",
            oauth_client_id="oauth_client_id_example",
            oauth_client_secret="oauth_client_secret_example",
            oauth_custom_auth_attributes={
                "key": "key_example",
            },
            oauth_custom_scopes=[
                "oauth_custom_scopes_example",
            ],
            oauth_issuer_id="myOidcProvider",
            oauth_issuer_location="oauth_issuer_location_example",
            oauth_subject_id_claim="oid",
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
                    content=JsonNode(),
                    id="/6bUUGjjNSwg0_bs",
                    type="TIMEZONE",
                ),
            ],
            themes=[
                DeclarativeTheme(
                    content=JsonNode(),
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
                    DeclarativeUserGroupIdentifier(
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
                        content=JsonNode(),
                        id="/6bUUGjjNSwg0_bs",
                        type="TIMEZONE",
                    ),
                ],
                user_groups=[
                    DeclarativeUserGroupIdentifier(
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
                automations=[
                    DeclarativeAutomation(
                        alert=AutomationAlert(
                            condition=AutomationAlertCondition(None),
                            execution=AlertAfm(
                                attributes=[
                                    AttributeItem(
                                        label=AfmObjectIdentifierLabel(
                                            identifier=AfmObjectIdentifierLabelIdentifier(
                                                id="sample_item.price",
                                                type="label",
                                            ),
                                        ),
                                        local_identifier="attribute_1",
                                        show_all_values=False,
                                    ),
                                ],
                                aux_measures=[
                                    MeasureItem(
                                        definition=MeasureDefinition(),
                                        local_identifier="metric_1",
                                    ),
                                ],
                                filters=[
                                    FilterDefinition(),
                                ],
                                measures=[
                                    MeasureItem(
                                        definition=MeasureDefinition(),
                                        local_identifier="metric_1",
                                    ),
                                ],
                            ),
                            trigger="ALWAYS",
                        ),
                        analytical_dashboard=DeclarativeAnalyticalDashboardIdentifier(
                            id="dashboard123",
                            type="analyticalDashboard",
                        ),
                        created_at="2023-07-20 12:30",
                        created_by=DeclarativeUserIdentifier(
                            id="employee123",
                            type="user",
                        ),
                        description="description_example",
                        details={
                            "key": "key_example",
                        },
                        export_definitions=[
                            DeclarativeExportDefinitionIdentifier(
                                id="export123",
                                type="exportDefinition",
                            ),
                        ],
                        external_recipients=[
                            AutomationExternalRecipient(
                                email="email_example",
                            ),
                        ],
                        id="/6bUUGjjNSwg0_bs",
                        image_exports=[
                            AutomationImageExport(
                                request_payload=ImageExportRequest(
                                    dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                                    file_name="filename",
                                    format="PNG",
                                    metadata=JsonNode(),
                                    widget_ids=[
                                        "widget_ids_example",
                                    ],
                                ),
                            ),
                        ],
                        metadata=AutomationMetadata(
                            visible_filters=[
                                VisibleFilter(
                                    is_all_time_date_filter=False,
                                    local_identifier="local_identifier_example",
                                    title="title_example",
                                ),
                            ],
                            widget="widget_example",
                        ),
                        modified_at="2023-07-20 12:30",
                        modified_by=DeclarativeUserIdentifier(
                            id="employee123",
                            type="user",
                        ),
                        notification_channel=DeclarativeNotificationChannelIdentifier(
                            id="webhook123",
                            type="notificationChannel",
                        ),
                        recipients=[
                            DeclarativeUserIdentifier(
                                id="employee123",
                                type="user",
                            ),
                        ],
                        schedule=AutomationSchedule(
                            cron="0 */30 9-17 ? * MON-FRI",
                            first_run=dateutil_parser('2025-01-01T12:00:00Z'),
                            timezone="Europe/Prague",
                        ),
                        state="ACTIVE",
                        tabular_exports=[
                            AutomationTabularExport(
                                request_payload=TabularExportRequest(
                                    custom_override=CustomOverride(
                                        labels={
                                            "key": CustomLabel(
                                                title="title_example",
                                            ),
                                        },
                                        metrics={
                                            "key": CustomMetric(
                                                format="format_example",
                                                title="title_example",
                                            ),
                                        },
                                    ),
                                    execution_result="ff483727196c9dc862c7fd3a5a84df55c96d61a4",
                                    file_name="result",
                                    format="CSV",
                                    metadata=JsonNode(),
                                    related_dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                                    settings=Settings(
                                        merge_headers=True,
                                        pdf_page_size="a4 landscape",
                                        pdf_table_style=[
                                            PdfTableStyle(
                                                properties=[
                                                    PdfTableStyleProperty(
                                                        key="key_example",
                                                        value="value_example",
                                                    ),
                                                ],
                                                selector="selector_example",
                                            ),
                                        ],
                                        pdf_top_left_content="Good",
                                        pdf_top_right_content="Morning",
                                        show_filters=False,
                                    ),
                                    visualization_object="f7c359bc-c230-4487-b15b-ad9685bcb537",
                                    visualization_object_custom_filters=[
                                        {},
                                    ],
                                ),
                            ),
                        ],
                        tags=[
                            "["Revenue","Sales"]",
                        ],
                        title="title_example",
                        visual_exports=[
                            AutomationVisualExport(
                                request_payload=VisualExportRequest(
                                    dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                                    file_name="filename",
                                    metadata={},
                                ),
                            ),
                        ],
                    ),
                ],
                cache_extra_limit=1,
                custom_application_settings=[
                    DeclarativeCustomApplicationSetting(
                        application_name="Modeler",
                        content=JsonNode(),
                        id="modeler.demo",
                    ),
                ],
                data_source=WorkspaceDataSource(
                    id="snowflake.instance.1",
                    schema_path=[
                        "subPath",
                    ],
                ),
                description="description_example",
                early_access="early_access_example",
                early_access_values=[
                    "early_access_values_example",
                ],
                filter_views=[
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
                            "["Revenue","Sales"]",
                        ],
                        title="title_example",
                        user=DeclarativeUserIdentifier(
                            id="employee123",
                            type="user",
                        ),
                    ),
                ],
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
                                    DeclarativeAnalyticalDashboardPermissionsInner(None),
                                ],
                            ),
                        ],
                        analytical_dashboards=[
                            DeclarativeAnalyticalDashboard(
                                content=JsonNode(),
                                created_at="2023-07-20 12:30",
                                created_by=DeclarativeUserIdentifier(
                                    id="employee123",
                                    type="user",
                                ),
                                description="Period to period comparison of revenues in main sectors.",
                                id="revenues-analysis",
                                modified_at="2023-07-20 12:30",
                                modified_by=DeclarativeUserIdentifier(
                                    id="employee123",
                                    type="user",
                                ),
                                permissions=[
                                    DeclarativeAnalyticalDashboardPermissionsInner(None),
                                ],
                                tags=["Revenues"],
                                title="Revenues analysis",
                            ),
                        ],
                        attribute_hierarchies=[
                            DeclarativeAttributeHierarchy(
                                content=JsonNode(),
                                created_at="["2023-07-20 12:30"]",
                                created_by=DeclarativeUserIdentifier(
                                    id="employee123",
                                    type="user",
                                ),
                                description="Simple number for total goods in current production.",
                                id="hierarchy-1",
                                modified_at="["2023-07-20 12:30"]",
                                modified_by=DeclarativeUserIdentifier(
                                    id="employee123",
                                    type="user",
                                ),
                                tags=["Revenues"],
                                title="Count of goods",
                            ),
                        ],
                        dashboard_plugins=[
                            DeclarativeDashboardPlugin(
                                content=JsonNode(),
                                created_at="["2023-07-20 12:30"]",
                                created_by=DeclarativeUserIdentifier(
                                    id="employee123",
                                    type="user",
                                ),
                                description="Three dimensional view of data.",
                                id="dashboard-plugin-1",
                                modified_at="["2023-07-20 12:30"]",
                                modified_by=DeclarativeUserIdentifier(
                                    id="employee123",
                                    type="user",
                                ),
                                tags=["Revenues"],
                                title="3D map renderer",
                            ),
                        ],
                        export_definitions=[
                            DeclarativeExportDefinition(
                                created_at="["2023-07-20 12:30"]",
                                created_by=DeclarativeUserIdentifier(
                                    id="employee123",
                                    type="user",
                                ),
                                description="Simple number for total goods in current production.",
                                id="export-definition-1",
                                modified_at="["2023-07-20 12:30"]",
                                modified_by=DeclarativeUserIdentifier(
                                    id="employee123",
                                    type="user",
                                ),
                                request_payload=DeclarativeExportDefinitionRequestPayload(None),
                                tags=["Revenues"],
                                title="My regular export",
                            ),
                        ],
                        filter_contexts=[
                            DeclarativeFilterContext(
                                content=JsonNode(),
                                description="Filter Context for Sales team.",
                                id="filter-sales",
                                tags=["Revenues"],
                                title="Filter Context for Sales team",
                            ),
                        ],
                        metrics=[
                            DeclarativeMetric(
                                content=JsonNode(),
                                created_at="["2023-07-20 12:30"]",
                                created_by=DeclarativeUserIdentifier(
                                    id="employee123",
                                    type="user",
                                ),
                                description="Sales for all the data available.",
                                id="total-sales",
                                modified_at="["2023-07-20 12:30"]",
                                modified_by=DeclarativeUserIdentifier(
                                    id="employee123",
                                    type="user",
                                ),
                                tags=["Revenues"],
                                title="Total sales",
                            ),
                        ],
                        visualization_objects=[
                            DeclarativeVisualizationObject(
                                content=JsonNode(),
                                created_at="["2023-07-20 12:30"]",
                                created_by=DeclarativeUserIdentifier(
                                    id="employee123",
                                    type="user",
                                ),
                                description="Simple number for total goods in current production.",
                                id="visualization-1",
                                modified_at="["2023-07-20 12:30"]",
                                modified_by=DeclarativeUserIdentifier(
                                    id="employee123",
                                    type="user",
                                ),
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
                                                value_type="TEXT",
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
                                        sources=[
                                            DeclarativeReferenceSource(
                                                column="customer_id",
                                                data_type="STRING",
                                                target=GrainIdentifier(
                                                    id="attr.customers.customer_name",
                                                    type="ATTRIBUTE",
                                                ),
                                            ),
                                        ],
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
                        content=JsonNode(),
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
                        user=DeclarativeUserIdentifier(
                            id="employee123",
                            type="user",
                        ),
                        user_group=DeclarativeUserGroupIdentifier(
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

# **set_organization_permissions**
> set_organization_permissions(declarative_organization_permission)

Set organization permissions

Sets organization permissions

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import layout_api
from gooddata_api_client.model.declarative_organization_permission import DeclarativeOrganizationPermission
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
    declarative_organization_permission = [
        DeclarativeOrganizationPermission(
            assignee=AssigneeIdentifier(
                id="id_example",
                type="user",
            ),
            name="MANAGE",
        ),
    ] # [DeclarativeOrganizationPermission] | 

    # example passing only required values which don't have defaults set
    try:
        # Set organization permissions
        api_instance.set_organization_permissions(declarative_organization_permission)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LayoutApi->set_organization_permissions: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **declarative_organization_permission** | [**[DeclarativeOrganizationPermission]**](DeclarativeOrganizationPermission.md)|  |

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
                user=DeclarativeUserIdentifier(
                    id="employee123",
                    type="user",
                ),
                user_group=DeclarativeUserGroupIdentifier(
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
                automations=[
                    DeclarativeAutomation(
                        alert=AutomationAlert(
                            condition=AutomationAlertCondition(None),
                            execution=AlertAfm(
                                attributes=[
                                    AttributeItem(
                                        label=AfmObjectIdentifierLabel(
                                            identifier=AfmObjectIdentifierLabelIdentifier(
                                                id="sample_item.price",
                                                type="label",
                                            ),
                                        ),
                                        local_identifier="attribute_1",
                                        show_all_values=False,
                                    ),
                                ],
                                aux_measures=[
                                    MeasureItem(
                                        definition=MeasureDefinition(),
                                        local_identifier="metric_1",
                                    ),
                                ],
                                filters=[
                                    FilterDefinition(),
                                ],
                                measures=[
                                    MeasureItem(
                                        definition=MeasureDefinition(),
                                        local_identifier="metric_1",
                                    ),
                                ],
                            ),
                            trigger="ALWAYS",
                        ),
                        analytical_dashboard=DeclarativeAnalyticalDashboardIdentifier(
                            id="dashboard123",
                            type="analyticalDashboard",
                        ),
                        created_at="2023-07-20 12:30",
                        created_by=DeclarativeUserIdentifier(
                            id="employee123",
                            type="user",
                        ),
                        description="description_example",
                        details={
                            "key": "key_example",
                        },
                        export_definitions=[
                            DeclarativeExportDefinitionIdentifier(
                                id="export123",
                                type="exportDefinition",
                            ),
                        ],
                        external_recipients=[
                            AutomationExternalRecipient(
                                email="email_example",
                            ),
                        ],
                        id="/6bUUGjjNSwg0_bs",
                        image_exports=[
                            AutomationImageExport(
                                request_payload=ImageExportRequest(
                                    dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                                    file_name="filename",
                                    format="PNG",
                                    metadata=JsonNode(),
                                    widget_ids=[
                                        "widget_ids_example",
                                    ],
                                ),
                            ),
                        ],
                        metadata=AutomationMetadata(
                            visible_filters=[
                                VisibleFilter(
                                    is_all_time_date_filter=False,
                                    local_identifier="local_identifier_example",
                                    title="title_example",
                                ),
                            ],
                            widget="widget_example",
                        ),
                        modified_at="2023-07-20 12:30",
                        modified_by=DeclarativeUserIdentifier(
                            id="employee123",
                            type="user",
                        ),
                        notification_channel=DeclarativeNotificationChannelIdentifier(
                            id="webhook123",
                            type="notificationChannel",
                        ),
                        recipients=[
                            DeclarativeUserIdentifier(
                                id="employee123",
                                type="user",
                            ),
                        ],
                        schedule=AutomationSchedule(
                            cron="0 */30 9-17 ? * MON-FRI",
                            first_run=dateutil_parser('2025-01-01T12:00:00Z'),
                            timezone="Europe/Prague",
                        ),
                        state="ACTIVE",
                        tabular_exports=[
                            AutomationTabularExport(
                                request_payload=TabularExportRequest(
                                    custom_override=CustomOverride(
                                        labels={
                                            "key": CustomLabel(
                                                title="title_example",
                                            ),
                                        },
                                        metrics={
                                            "key": CustomMetric(
                                                format="format_example",
                                                title="title_example",
                                            ),
                                        },
                                    ),
                                    execution_result="ff483727196c9dc862c7fd3a5a84df55c96d61a4",
                                    file_name="result",
                                    format="CSV",
                                    metadata=JsonNode(),
                                    related_dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                                    settings=Settings(
                                        merge_headers=True,
                                        pdf_page_size="a4 landscape",
                                        pdf_table_style=[
                                            PdfTableStyle(
                                                properties=[
                                                    PdfTableStyleProperty(
                                                        key="key_example",
                                                        value="value_example",
                                                    ),
                                                ],
                                                selector="selector_example",
                                            ),
                                        ],
                                        pdf_top_left_content="Good",
                                        pdf_top_right_content="Morning",
                                        show_filters=False,
                                    ),
                                    visualization_object="f7c359bc-c230-4487-b15b-ad9685bcb537",
                                    visualization_object_custom_filters=[
                                        {},
                                    ],
                                ),
                            ),
                        ],
                        tags=[
                            "["Revenue","Sales"]",
                        ],
                        title="title_example",
                        visual_exports=[
                            AutomationVisualExport(
                                request_payload=VisualExportRequest(
                                    dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                                    file_name="filename",
                                    metadata={},
                                ),
                            ),
                        ],
                    ),
                ],
                cache_extra_limit=1,
                custom_application_settings=[
                    DeclarativeCustomApplicationSetting(
                        application_name="Modeler",
                        content=JsonNode(),
                        id="modeler.demo",
                    ),
                ],
                data_source=WorkspaceDataSource(
                    id="snowflake.instance.1",
                    schema_path=[
                        "subPath",
                    ],
                ),
                description="description_example",
                early_access="early_access_example",
                early_access_values=[
                    "early_access_values_example",
                ],
                filter_views=[
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
                            "["Revenue","Sales"]",
                        ],
                        title="title_example",
                        user=DeclarativeUserIdentifier(
                            id="employee123",
                            type="user",
                        ),
                    ),
                ],
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
                                    DeclarativeAnalyticalDashboardPermissionsInner(None),
                                ],
                            ),
                        ],
                        analytical_dashboards=[
                            DeclarativeAnalyticalDashboard(
                                content=JsonNode(),
                                created_at="2023-07-20 12:30",
                                created_by=DeclarativeUserIdentifier(
                                    id="employee123",
                                    type="user",
                                ),
                                description="Period to period comparison of revenues in main sectors.",
                                id="revenues-analysis",
                                modified_at="2023-07-20 12:30",
                                modified_by=DeclarativeUserIdentifier(
                                    id="employee123",
                                    type="user",
                                ),
                                permissions=[
                                    DeclarativeAnalyticalDashboardPermissionsInner(None),
                                ],
                                tags=["Revenues"],
                                title="Revenues analysis",
                            ),
                        ],
                        attribute_hierarchies=[
                            DeclarativeAttributeHierarchy(
                                content=JsonNode(),
                                created_at="["2023-07-20 12:30"]",
                                created_by=DeclarativeUserIdentifier(
                                    id="employee123",
                                    type="user",
                                ),
                                description="Simple number for total goods in current production.",
                                id="hierarchy-1",
                                modified_at="["2023-07-20 12:30"]",
                                modified_by=DeclarativeUserIdentifier(
                                    id="employee123",
                                    type="user",
                                ),
                                tags=["Revenues"],
                                title="Count of goods",
                            ),
                        ],
                        dashboard_plugins=[
                            DeclarativeDashboardPlugin(
                                content=JsonNode(),
                                created_at="["2023-07-20 12:30"]",
                                created_by=DeclarativeUserIdentifier(
                                    id="employee123",
                                    type="user",
                                ),
                                description="Three dimensional view of data.",
                                id="dashboard-plugin-1",
                                modified_at="["2023-07-20 12:30"]",
                                modified_by=DeclarativeUserIdentifier(
                                    id="employee123",
                                    type="user",
                                ),
                                tags=["Revenues"],
                                title="3D map renderer",
                            ),
                        ],
                        export_definitions=[
                            DeclarativeExportDefinition(
                                created_at="["2023-07-20 12:30"]",
                                created_by=DeclarativeUserIdentifier(
                                    id="employee123",
                                    type="user",
                                ),
                                description="Simple number for total goods in current production.",
                                id="export-definition-1",
                                modified_at="["2023-07-20 12:30"]",
                                modified_by=DeclarativeUserIdentifier(
                                    id="employee123",
                                    type="user",
                                ),
                                request_payload=DeclarativeExportDefinitionRequestPayload(None),
                                tags=["Revenues"],
                                title="My regular export",
                            ),
                        ],
                        filter_contexts=[
                            DeclarativeFilterContext(
                                content=JsonNode(),
                                description="Filter Context for Sales team.",
                                id="filter-sales",
                                tags=["Revenues"],
                                title="Filter Context for Sales team",
                            ),
                        ],
                        metrics=[
                            DeclarativeMetric(
                                content=JsonNode(),
                                created_at="["2023-07-20 12:30"]",
                                created_by=DeclarativeUserIdentifier(
                                    id="employee123",
                                    type="user",
                                ),
                                description="Sales for all the data available.",
                                id="total-sales",
                                modified_at="["2023-07-20 12:30"]",
                                modified_by=DeclarativeUserIdentifier(
                                    id="employee123",
                                    type="user",
                                ),
                                tags=["Revenues"],
                                title="Total sales",
                            ),
                        ],
                        visualization_objects=[
                            DeclarativeVisualizationObject(
                                content=JsonNode(),
                                created_at="["2023-07-20 12:30"]",
                                created_by=DeclarativeUserIdentifier(
                                    id="employee123",
                                    type="user",
                                ),
                                description="Simple number for total goods in current production.",
                                id="visualization-1",
                                modified_at="["2023-07-20 12:30"]",
                                modified_by=DeclarativeUserIdentifier(
                                    id="employee123",
                                    type="user",
                                ),
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
                                                value_type="TEXT",
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
                                        sources=[
                                            DeclarativeReferenceSource(
                                                column="customer_id",
                                                data_type="STRING",
                                                target=GrainIdentifier(
                                                    id="attr.customers.customer_name",
                                                    type="ATTRIBUTE",
                                                ),
                                            ),
                                        ],
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
                        content=JsonNode(),
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
                        user=DeclarativeUserIdentifier(
                            id="employee123",
                            type="user",
                        ),
                        user_group=DeclarativeUserGroupIdentifier(
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


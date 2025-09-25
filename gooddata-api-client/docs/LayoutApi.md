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
> DeclarativeAnalytics get_analytics_model(workspace_id, exclude=exclude)

Get analytics model

Retrieve current analytics model of the workspace.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_analytics import DeclarativeAnalytics
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    exclude = ['exclude_example'] # List[str] |  (optional)

    try:
        # Get analytics model
        api_response = api_instance.get_analytics_model(workspace_id, exclude=exclude)
        print("The response of LayoutApi->get_analytics_model:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LayoutApi->get_analytics_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **exclude** | [**List[str]**](str.md)|  | [optional] 

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
> List[DeclarativeAutomation] get_automations(workspace_id, exclude=exclude)

Get automations

Retrieve automations for the specific workspace

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_automation import DeclarativeAutomation
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    exclude = ['exclude_example'] # List[str] |  (optional)

    try:
        # Get automations
        api_response = api_instance.get_automations(workspace_id, exclude=exclude)
        print("The response of LayoutApi->get_automations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LayoutApi->get_automations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **exclude** | [**List[str]**](str.md)|  | [optional] 

### Return type

[**List[DeclarativeAutomation]**](DeclarativeAutomation.md)

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
import gooddata_api_client
from gooddata_api_client.models.declarative_data_source_permissions import DeclarativeDataSourcePermissions
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    data_source_id = 'data_source_id_example' # str | 

    try:
        # Get permissions for the data source
        api_response = api_instance.get_data_source_permissions(data_source_id)
        print("The response of LayoutApi->get_data_source_permissions:\n")
        pprint(api_response)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.declarative_data_sources import DeclarativeDataSources
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
    api_instance = gooddata_api_client.LayoutApi(api_client)

    try:
        # Get all data sources
        api_response = api_instance.get_data_sources_layout()
        print("The response of LayoutApi->get_data_sources_layout:\n")
        pprint(api_response)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.declarative_export_templates import DeclarativeExportTemplates
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
    api_instance = gooddata_api_client.LayoutApi(api_client)

    try:
        # Get all export templates layout
        api_response = api_instance.get_export_templates_layout()
        print("The response of LayoutApi->get_export_templates_layout:\n")
        pprint(api_response)
    except Exception as e:
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
> List[DeclarativeFilterView] get_filter_views(workspace_id, exclude=exclude)

Get filter views

Retrieve filter views for the specific workspace

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_filter_view import DeclarativeFilterView
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    exclude = ['exclude_example'] # List[str] |  (optional)

    try:
        # Get filter views
        api_response = api_instance.get_filter_views(workspace_id, exclude=exclude)
        print("The response of LayoutApi->get_filter_views:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LayoutApi->get_filter_views: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **exclude** | [**List[str]**](str.md)|  | [optional] 

### Return type

[**List[DeclarativeFilterView]**](DeclarativeFilterView.md)

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
> List[DeclarativeIdentityProvider] get_identity_providers_layout()

Get all identity providers layout

Gets complete layout of identity providers.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_identity_provider import DeclarativeIdentityProvider
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
    api_instance = gooddata_api_client.LayoutApi(api_client)

    try:
        # Get all identity providers layout
        api_response = api_instance.get_identity_providers_layout()
        print("The response of LayoutApi->get_identity_providers_layout:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LayoutApi->get_identity_providers_layout: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[DeclarativeIdentityProvider]**](DeclarativeIdentityProvider.md)

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
> DeclarativeModel get_logical_model(workspace_id, include_parents=include_parents)

Get logical model

Retrieve current logical model of the workspace in declarative form.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_model import DeclarativeModel
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    include_parents = True # bool |  (optional)

    try:
        # Get logical model
        api_response = api_instance.get_logical_model(workspace_id, include_parents=include_parents)
        print("The response of LayoutApi->get_logical_model:\n")
        pprint(api_response)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.declarative_notification_channels import DeclarativeNotificationChannels
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
    api_instance = gooddata_api_client.LayoutApi(api_client)

    try:
        # Get all notification channels layout
        api_response = api_instance.get_notification_channels_layout()
        print("The response of LayoutApi->get_notification_channels_layout:\n")
        pprint(api_response)
    except Exception as e:
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
> DeclarativeOrganization get_organization_layout(exclude=exclude)

Get organization layout

Retrieve complete layout of organization, workspaces, user-groups, etc.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_organization import DeclarativeOrganization
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    exclude = ['exclude_example'] # List[str] |  (optional)

    try:
        # Get organization layout
        api_response = api_instance.get_organization_layout(exclude=exclude)
        print("The response of LayoutApi->get_organization_layout:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LayoutApi->get_organization_layout: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **exclude** | [**List[str]**](str.md)|  | [optional] 

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
    api_instance = gooddata_api_client.LayoutApi(api_client)

    try:
        # Get organization permissions
        api_response = api_instance.get_organization_permissions()
        print("The response of LayoutApi->get_organization_permissions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LayoutApi->get_organization_permissions: %s\n" % e)
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

# **get_user_data_filters**
> DeclarativeUserDataFilters get_user_data_filters(workspace_id)

Get user data filters

Retrieve current user data filters assigned to the workspace.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_user_data_filters import DeclarativeUserDataFilters
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    workspace_id = 'workspace_id_example' # str | 

    try:
        # Get user data filters
        api_response = api_instance.get_user_data_filters(workspace_id)
        print("The response of LayoutApi->get_user_data_filters:\n")
        pprint(api_response)
    except Exception as e:
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    user_group_id = 'user_group_id_example' # str | 

    try:
        # Get permissions for the user-group
        api_response = api_instance.get_user_group_permissions(user_group_id)
        print("The response of LayoutApi->get_user_group_permissions:\n")
        pprint(api_response)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.declarative_user_groups import DeclarativeUserGroups
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
    api_instance = gooddata_api_client.LayoutApi(api_client)

    try:
        # Get all user groups
        api_response = api_instance.get_user_groups_layout()
        print("The response of LayoutApi->get_user_groups_layout:\n")
        pprint(api_response)
    except Exception as e:
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    user_id = 'user_id_example' # str | 

    try:
        # Get permissions for the user
        api_response = api_instance.get_user_permissions(user_id)
        print("The response of LayoutApi->get_user_permissions:\n")
        pprint(api_response)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.declarative_users import DeclarativeUsers
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
    api_instance = gooddata_api_client.LayoutApi(api_client)

    try:
        # Get all users
        api_response = api_instance.get_users_layout()
        print("The response of LayoutApi->get_users_layout:\n")
        pprint(api_response)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.declarative_users_user_groups import DeclarativeUsersUserGroups
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
    api_instance = gooddata_api_client.LayoutApi(api_client)

    try:
        # Get all users and user groups
        api_response = api_instance.get_users_user_groups_layout()
        print("The response of LayoutApi->get_users_user_groups_layout:\n")
        pprint(api_response)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.declarative_workspace_data_filters import DeclarativeWorkspaceDataFilters
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
    api_instance = gooddata_api_client.LayoutApi(api_client)

    try:
        # Get workspace data filters for all workspaces
        api_response = api_instance.get_workspace_data_filters_layout()
        print("The response of LayoutApi->get_workspace_data_filters_layout:\n")
        pprint(api_response)
    except Exception as e:
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
> DeclarativeWorkspaceModel get_workspace_layout(workspace_id, exclude=exclude)

Get workspace layout

Retrieve current model of the workspace in declarative form.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_workspace_model import DeclarativeWorkspaceModel
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    exclude = ['exclude_example'] # List[str] |  (optional)

    try:
        # Get workspace layout
        api_response = api_instance.get_workspace_layout(workspace_id, exclude=exclude)
        print("The response of LayoutApi->get_workspace_layout:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LayoutApi->get_workspace_layout: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **exclude** | [**List[str]**](str.md)|  | [optional] 

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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    workspace_id = 'workspace_id_example' # str | 

    try:
        # Get permissions for the workspace
        api_response = api_instance.get_workspace_permissions(workspace_id)
        print("The response of LayoutApi->get_workspace_permissions:\n")
        pprint(api_response)
    except Exception as e:
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
> DeclarativeWorkspaces get_workspaces_layout(exclude=exclude)

Get all workspaces layout

Gets complete layout of workspaces, their hierarchy, models.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_workspaces import DeclarativeWorkspaces
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    exclude = ['exclude_example'] # List[str] |  (optional)

    try:
        # Get all workspaces layout
        api_response = api_instance.get_workspaces_layout(exclude=exclude)
        print("The response of LayoutApi->get_workspaces_layout:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LayoutApi->get_workspaces_layout: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **exclude** | [**List[str]**](str.md)|  | [optional] 

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
import gooddata_api_client
from gooddata_api_client.models.declarative_data_sources import DeclarativeDataSources
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    declarative_data_sources = gooddata_api_client.DeclarativeDataSources() # DeclarativeDataSources | 

    try:
        # Put all data sources
        api_instance.put_data_sources_layout(declarative_data_sources)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.declarative_user_groups import DeclarativeUserGroups
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    declarative_user_groups = gooddata_api_client.DeclarativeUserGroups() # DeclarativeUserGroups | 

    try:
        # Put all user groups
        api_instance.put_user_groups_layout(declarative_user_groups)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.declarative_users import DeclarativeUsers
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    declarative_users = gooddata_api_client.DeclarativeUsers() # DeclarativeUsers | 

    try:
        # Put all users
        api_instance.put_users_layout(declarative_users)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.declarative_users_user_groups import DeclarativeUsersUserGroups
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    declarative_users_user_groups = gooddata_api_client.DeclarativeUsersUserGroups() # DeclarativeUsersUserGroups | 

    try:
        # Put all users and user groups
        api_instance.put_users_user_groups_layout(declarative_users_user_groups)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.declarative_workspace_model import DeclarativeWorkspaceModel
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    declarative_workspace_model = gooddata_api_client.DeclarativeWorkspaceModel() # DeclarativeWorkspaceModel | 

    try:
        # Set workspace layout
        api_instance.put_workspace_layout(workspace_id, declarative_workspace_model)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.declarative_analytics import DeclarativeAnalytics
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    declarative_analytics = gooddata_api_client.DeclarativeAnalytics() # DeclarativeAnalytics | 

    try:
        # Set analytics model
        api_instance.set_analytics_model(workspace_id, declarative_analytics)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.declarative_automation import DeclarativeAutomation
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    declarative_automation = [gooddata_api_client.DeclarativeAutomation()] # List[DeclarativeAutomation] | 

    try:
        # Set automations
        api_instance.set_automations(workspace_id, declarative_automation)
    except Exception as e:
        print("Exception when calling LayoutApi->set_automations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **declarative_automation** | [**List[DeclarativeAutomation]**](DeclarativeAutomation.md)|  | 

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
import gooddata_api_client
from gooddata_api_client.models.declarative_data_source_permissions import DeclarativeDataSourcePermissions
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    data_source_id = 'data_source_id_example' # str | 
    declarative_data_source_permissions = gooddata_api_client.DeclarativeDataSourcePermissions() # DeclarativeDataSourcePermissions | 

    try:
        # Set data source permissions.
        api_instance.set_data_source_permissions(data_source_id, declarative_data_source_permissions)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.declarative_export_templates import DeclarativeExportTemplates
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    declarative_export_templates = gooddata_api_client.DeclarativeExportTemplates() # DeclarativeExportTemplates | 

    try:
        # Set all export templates
        api_instance.set_export_templates(declarative_export_templates)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.declarative_filter_view import DeclarativeFilterView
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    declarative_filter_view = [gooddata_api_client.DeclarativeFilterView()] # List[DeclarativeFilterView] | 

    try:
        # Set filter views
        api_instance.set_filter_views(workspace_id, declarative_filter_view)
    except Exception as e:
        print("Exception when calling LayoutApi->set_filter_views: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **declarative_filter_view** | [**List[DeclarativeFilterView]**](DeclarativeFilterView.md)|  | 

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
import gooddata_api_client
from gooddata_api_client.models.declarative_identity_provider import DeclarativeIdentityProvider
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    declarative_identity_provider = [gooddata_api_client.DeclarativeIdentityProvider()] # List[DeclarativeIdentityProvider] | 

    try:
        # Set all identity providers
        api_instance.set_identity_providers(declarative_identity_provider)
    except Exception as e:
        print("Exception when calling LayoutApi->set_identity_providers: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **declarative_identity_provider** | [**List[DeclarativeIdentityProvider]**](DeclarativeIdentityProvider.md)|  | 

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
import gooddata_api_client
from gooddata_api_client.models.declarative_model import DeclarativeModel
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    declarative_model = gooddata_api_client.DeclarativeModel() # DeclarativeModel | 

    try:
        # Set logical model
        api_instance.set_logical_model(workspace_id, declarative_model)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.declarative_notification_channels import DeclarativeNotificationChannels
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    declarative_notification_channels = gooddata_api_client.DeclarativeNotificationChannels() # DeclarativeNotificationChannels | 

    try:
        # Set all notification channels
        api_instance.set_notification_channels(declarative_notification_channels)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.declarative_organization import DeclarativeOrganization
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    declarative_organization = gooddata_api_client.DeclarativeOrganization() # DeclarativeOrganization | 

    try:
        # Set organization layout
        api_instance.set_organization_layout(declarative_organization)
    except Exception as e:
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    declarative_organization_permission = [gooddata_api_client.DeclarativeOrganizationPermission()] # List[DeclarativeOrganizationPermission] | 

    try:
        # Set organization permissions
        api_instance.set_organization_permissions(declarative_organization_permission)
    except Exception as e:
        print("Exception when calling LayoutApi->set_organization_permissions: %s\n" % e)
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

# **set_user_data_filters**
> set_user_data_filters(workspace_id, declarative_user_data_filters)

Set user data filters

Set user data filters assigned to the workspace.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_user_data_filters import DeclarativeUserDataFilters
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    declarative_user_data_filters = gooddata_api_client.DeclarativeUserDataFilters() # DeclarativeUserDataFilters | 

    try:
        # Set user data filters
        api_instance.set_user_data_filters(workspace_id, declarative_user_data_filters)
    except Exception as e:
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    user_group_id = 'user_group_id_example' # str | 
    declarative_user_group_permissions = gooddata_api_client.DeclarativeUserGroupPermissions() # DeclarativeUserGroupPermissions | 

    try:
        # Set permissions for the user-group
        api_instance.set_user_group_permissions(user_group_id, declarative_user_group_permissions)
    except Exception as e:
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    user_id = 'user_id_example' # str | 
    declarative_user_permissions = gooddata_api_client.DeclarativeUserPermissions() # DeclarativeUserPermissions | 

    try:
        # Set permissions for the user
        api_instance.set_user_permissions(user_id, declarative_user_permissions)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.declarative_workspace_data_filters import DeclarativeWorkspaceDataFilters
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    declarative_workspace_data_filters = gooddata_api_client.DeclarativeWorkspaceDataFilters() # DeclarativeWorkspaceDataFilters | 

    try:
        # Set all workspace data filters
        api_instance.set_workspace_data_filters_layout(declarative_workspace_data_filters)
    except Exception as e:
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    declarative_workspace_permissions = gooddata_api_client.DeclarativeWorkspacePermissions() # DeclarativeWorkspacePermissions | 

    try:
        # Set permissions for the workspace
        api_instance.set_workspace_permissions(workspace_id, declarative_workspace_permissions)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.declarative_workspaces import DeclarativeWorkspaces
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
    api_instance = gooddata_api_client.LayoutApi(api_client)
    declarative_workspaces = gooddata_api_client.DeclarativeWorkspaces() # DeclarativeWorkspaces | 

    try:
        # Set all workspaces layout
        api_instance.set_workspaces_layout(declarative_workspaces)
    except Exception as e:
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


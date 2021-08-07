# gooddata_metadata_client.DeclarativeLayoutControllerApi

All URIs are relative to *https://staging.anywhere.gooddata.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_analytics_model**](DeclarativeLayoutControllerApi.md#get_analytics_model) | **GET** /api/layout/workspaces/{workspaceId}/analyticsModel | Get analytics model
[**get_data_sources_layout**](DeclarativeLayoutControllerApi.md#get_data_sources_layout) | **GET** /api/layout/dataSources | Get all data sources
[**get_logical_model**](DeclarativeLayoutControllerApi.md#get_logical_model) | **GET** /api/layout/workspaces/{workspaceId}/logicalModel | Get logical model
[**get_organization_layout**](DeclarativeLayoutControllerApi.md#get_organization_layout) | **GET** /api/layout/organization | Get organization layout
[**get_user_groups_layout**](DeclarativeLayoutControllerApi.md#get_user_groups_layout) | **GET** /api/layout/userGroups | Get all users
[**get_users_layout**](DeclarativeLayoutControllerApi.md#get_users_layout) | **GET** /api/layout/users | Get all users
[**get_users_user_groups_layout**](DeclarativeLayoutControllerApi.md#get_users_user_groups_layout) | **GET** /api/layout/usersAndUserGroups | Get all users and user groups
[**get_workspace_data_filters_layout**](DeclarativeLayoutControllerApi.md#get_workspace_data_filters_layout) | **GET** /api/layout/workspaceDataFilters | Get workspace data filters for all workspaces
[**get_workspace_layout**](DeclarativeLayoutControllerApi.md#get_workspace_layout) | **GET** /api/layout/workspaces/{workspaceId} | Get workspace layout
[**get_workspaces_layout**](DeclarativeLayoutControllerApi.md#get_workspaces_layout) | **GET** /api/layout/workspaces | Get all workspaces layout
[**put_data_sources_layout**](DeclarativeLayoutControllerApi.md#put_data_sources_layout) | **PUT** /api/layout/usersAndUserGroups | Put all data sources
[**put_data_sources_layout1**](DeclarativeLayoutControllerApi.md#put_data_sources_layout1) | **PUT** /api/layout/dataSources | Put all data sources
[**put_user_groups_layout**](DeclarativeLayoutControllerApi.md#put_user_groups_layout) | **PUT** /api/layout/userGroups | Put all user groups
[**put_users_layout**](DeclarativeLayoutControllerApi.md#put_users_layout) | **PUT** /api/layout/users | Put all users
[**put_workspace_layout**](DeclarativeLayoutControllerApi.md#put_workspace_layout) | **PUT** /api/layout/workspaces/{workspaceId} | Set workspace layout
[**set_analytics_model**](DeclarativeLayoutControllerApi.md#set_analytics_model) | **PUT** /api/layout/workspaces/{workspaceId}/analyticsModel | Set analytics model
[**set_logical_model**](DeclarativeLayoutControllerApi.md#set_logical_model) | **PUT** /api/layout/workspaces/{workspaceId}/logicalModel | Set logical model
[**set_organization_layout**](DeclarativeLayoutControllerApi.md#set_organization_layout) | **PUT** /api/layout/organization | Set organization layout
[**set_workspace_data_filters_layout**](DeclarativeLayoutControllerApi.md#set_workspace_data_filters_layout) | **PUT** /api/layout/workspaceDataFilters | Set all workspace data filters
[**set_workspaces_layout**](DeclarativeLayoutControllerApi.md#set_workspaces_layout) | **PUT** /api/layout/workspaces | Set all workspaces layout


# **get_analytics_model**
> DeclarativeAnalytics get_analytics_model(workspace_id)

Get analytics model

Retrieve current analytics model of the workspace.

### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import declarative_layout_controller_api
from gooddata_metadata_client.model.declarative_analytics import DeclarativeAnalytics
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = declarative_layout_controller_api.DeclarativeLayoutControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get analytics model
        api_response = api_instance.get_analytics_model(workspace_id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling DeclarativeLayoutControllerApi->get_analytics_model: %s\n" % e)
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
 - **Accept**: */*


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
import gooddata_metadata_client
from gooddata_metadata_client.api import declarative_layout_controller_api
from gooddata_metadata_client.model.declarative_data_sources import DeclarativeDataSources
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = declarative_layout_controller_api.DeclarativeLayoutControllerApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get all data sources
        api_response = api_instance.get_data_sources_layout()
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling DeclarativeLayoutControllerApi->get_data_sources_layout: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**DeclarativeDataSources**](DeclarativeDataSources.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*


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
import gooddata_metadata_client
from gooddata_metadata_client.api import declarative_layout_controller_api
from gooddata_metadata_client.model.declarative_model import DeclarativeModel
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = declarative_layout_controller_api.DeclarativeLayoutControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get logical model
        api_response = api_instance.get_logical_model(workspace_id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling DeclarativeLayoutControllerApi->get_logical_model: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |

### Return type

[**DeclarativeModel**](DeclarativeModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*


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
import gooddata_metadata_client
from gooddata_metadata_client.api import declarative_layout_controller_api
from gooddata_metadata_client.model.declarative_organization import DeclarativeOrganization
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = declarative_layout_controller_api.DeclarativeLayoutControllerApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get organization layout
        api_response = api_instance.get_organization_layout()
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling DeclarativeLayoutControllerApi->get_organization_layout: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**DeclarativeOrganization**](DeclarativeOrganization.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved all parts of an organization. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_groups_layout**
> DeclarativeUserGroups get_user_groups_layout()

Get all users

Retrieve all user-groups eventually with parent group.

### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import declarative_layout_controller_api
from gooddata_metadata_client.model.declarative_user_groups import DeclarativeUserGroups
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = declarative_layout_controller_api.DeclarativeLayoutControllerApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get all users
        api_response = api_instance.get_user_groups_layout()
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling DeclarativeLayoutControllerApi->get_user_groups_layout: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**DeclarativeUserGroups**](DeclarativeUserGroups.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved all user groups. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_users_layout**
> DeclarativeUsers get_users_layout()

Get all users

Retrieve all users including authentication properties.

### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import declarative_layout_controller_api
from gooddata_metadata_client.model.declarative_users import DeclarativeUsers
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = declarative_layout_controller_api.DeclarativeLayoutControllerApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get all users
        api_response = api_instance.get_users_layout()
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling DeclarativeLayoutControllerApi->get_users_layout: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**DeclarativeUsers**](DeclarativeUsers.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*


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
import gooddata_metadata_client
from gooddata_metadata_client.api import declarative_layout_controller_api
from gooddata_metadata_client.model.declarative_users_user_groups import DeclarativeUsersUserGroups
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = declarative_layout_controller_api.DeclarativeLayoutControllerApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get all users and user groups
        api_response = api_instance.get_users_user_groups_layout()
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling DeclarativeLayoutControllerApi->get_users_user_groups_layout: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**DeclarativeUsersUserGroups**](DeclarativeUsersUserGroups.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*


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
import gooddata_metadata_client
from gooddata_metadata_client.api import declarative_layout_controller_api
from gooddata_metadata_client.model.declarative_workspace_data_filters import DeclarativeWorkspaceDataFilters
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = declarative_layout_controller_api.DeclarativeLayoutControllerApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get workspace data filters for all workspaces
        api_response = api_instance.get_workspace_data_filters_layout()
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling DeclarativeLayoutControllerApi->get_workspace_data_filters_layout: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**DeclarativeWorkspaceDataFilters**](DeclarativeWorkspaceDataFilters.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*


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
import gooddata_metadata_client
from gooddata_metadata_client.api import declarative_layout_controller_api
from gooddata_metadata_client.model.declarative_workspace_model import DeclarativeWorkspaceModel
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = declarative_layout_controller_api.DeclarativeLayoutControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get workspace layout
        api_response = api_instance.get_workspace_layout(workspace_id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling DeclarativeLayoutControllerApi->get_workspace_layout: %s\n" % e)
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
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved the workspace model. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_workspaces_layout**
> DeclarativeWorkspaces get_workspaces_layout()

Get all workspaces layout

Gets complete layout of workspaces, their hierarchy, models.

### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import declarative_layout_controller_api
from gooddata_metadata_client.model.declarative_workspaces import DeclarativeWorkspaces
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = declarative_layout_controller_api.DeclarativeLayoutControllerApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get all workspaces layout
        api_response = api_instance.get_workspaces_layout()
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling DeclarativeLayoutControllerApi->get_workspaces_layout: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**DeclarativeWorkspaces**](DeclarativeWorkspaces.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved layout of all workspaces. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_data_sources_layout**
> put_data_sources_layout(declarative_users_user_groups)

Put all data sources

Set all data sources including related physical model.

### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import declarative_layout_controller_api
from gooddata_metadata_client.model.declarative_users_user_groups import DeclarativeUsersUserGroups
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = declarative_layout_controller_api.DeclarativeLayoutControllerApi(api_client)
    declarative_users_user_groups = DeclarativeUsersUserGroups(
        users=[
            DeclarativeUser(
                id="employee123",
                auth_id="auth_id_example",
                user_groups=[
                    UserGroupIdentifier(
                        id="group.admins",
                        type="userGroup",
                    ),
                ],
            ),
        ],
        user_groups=[
            DeclarativeUserGroup(
                id="employees.all",
                parents=[
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
        # Put all data sources
        api_instance.put_data_sources_layout(declarative_users_user_groups)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling DeclarativeLayoutControllerApi->put_data_sources_layout: %s\n" % e)
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
**200** | Defined all data sources. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_data_sources_layout1**
> put_data_sources_layout1(declarative_data_sources)

Put all data sources

Set all data sources including related physical model.

### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import declarative_layout_controller_api
from gooddata_metadata_client.model.declarative_data_sources import DeclarativeDataSources
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = declarative_layout_controller_api.DeclarativeLayoutControllerApi(api_client)
    declarative_data_sources = DeclarativeDataSources(
        data_sources=[
            DeclarativeDataSource(
                id="pg_local_docker-demo",
                name="postgres demo",
                type="POSTGRESQL",
                url="jdbc:postgresql://postgres:5432/gooddata",
                schema="demo",
                username="demo",
                password="*****",
                token="Bigquery service account JSON. Encode it using base64!",
                pdm=DeclarativeTables(
                    tables=[
                        DeclarativeTable(
                            id="customers",
                            path=["table_schema","table_name"],
                            type="VIEW",
                            columns=[
                                DeclarativeColumn(
                                    name="customer_id",
                                    data_type="INT",
                                    is_primary_key=True,
                                    referenced_table_id="customers",
                                    referenced_table_column="customer_id",
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        ],
    ) # DeclarativeDataSources | 

    # example passing only required values which don't have defaults set
    try:
        # Put all data sources
        api_instance.put_data_sources_layout1(declarative_data_sources)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling DeclarativeLayoutControllerApi->put_data_sources_layout1: %s\n" % e)
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
**200** | Defined all data sources. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_user_groups_layout**
> put_user_groups_layout(declarative_user_groups)

Put all user groups

Define all user groups with their parents eventually.

### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import declarative_layout_controller_api
from gooddata_metadata_client.model.declarative_user_groups import DeclarativeUserGroups
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = declarative_layout_controller_api.DeclarativeLayoutControllerApi(api_client)
    declarative_user_groups = DeclarativeUserGroups(
        user_groups=[
            DeclarativeUserGroup(
                id="employees.all",
                parents=[
                    UserGroupIdentifier(
                        id="group.admins",
                        type="userGroup",
                    ),
                ],
            ),
        ],
    ) # DeclarativeUserGroups | 

    # example passing only required values which don't have defaults set
    try:
        # Put all user groups
        api_instance.put_user_groups_layout(declarative_user_groups)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling DeclarativeLayoutControllerApi->put_user_groups_layout: %s\n" % e)
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
**200** | Defined all user groups. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_users_layout**
> put_users_layout(declarative_users)

Put all users

Set all users and their authentication properties.

### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import declarative_layout_controller_api
from gooddata_metadata_client.model.declarative_users import DeclarativeUsers
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = declarative_layout_controller_api.DeclarativeLayoutControllerApi(api_client)
    declarative_users = DeclarativeUsers(
        users=[
            DeclarativeUser(
                id="employee123",
                auth_id="auth_id_example",
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
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling DeclarativeLayoutControllerApi->put_users_layout: %s\n" % e)
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
**200** | Defined all users. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_workspace_layout**
> put_workspace_layout(workspace_id, declarative_workspace_model)

Set workspace layout

Set complete layout of workspace, like model, ACLs, etc.

### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import declarative_layout_controller_api
from gooddata_metadata_client.model.declarative_workspace_model import DeclarativeWorkspaceModel
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = declarative_layout_controller_api.DeclarativeLayoutControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    declarative_workspace_model = DeclarativeWorkspaceModel(
        ldm=DeclarativeLdm(
            datasets=[
                DeclarativeDataset(
                    id="customers",
                    title="Customers",
                    description="The customers of ours.",
                    grain=[
                        GrainIdentifier(
                            id="attr.customers.customer_name",
                            type="ATTRIBUTE",
                        ),
                    ],
                    attributes=[
                        DeclarativeAttribute(
                            id="attr.customers.customer_name",
                            title="Customer name",
                            description="Customer name including first and last name.",
                            labels=[
                                DeclarativeLabel(
                                    id="label.customer_name",
                                    title="Customer name",
                                    description="Customer name",
                                    primary=False,
                                    source_column="customer_name",
                                    tags=["Customers"],
                                ),
                            ],
                            tags=["Customers"],
                        ),
                    ],
                    facts=[
                        DeclarativeFact(
                            id="fact.customer_order_count",
                            title="Customer order count",
                            description="A number of orders created by the customer - including all orders, even the non-delivered ones.",
                            source_column="customer_order_count",
                            tags=["Customers"],
                        ),
                    ],
                    references=[
                        DeclarativeReference(
                            identifier=ReferenceIdentifier(
                                id="customers",
                                type="DATASET",
                            ),
                            multivalue=False,
                            source_columns=["customer_id"],
                        ),
                    ],
                    data_source_table_id=DataSourceTableIdentifier(
                        id="customers",
                        data_source_id="my-postgres",
                        type="dataSource",
                    ),
                    tags=["Customers"],
                ),
            ],
            date_instances=[
                DeclarativeDateDataset(
                    id="date",
                    title="Date",
                    description="A customer order date",
                    granularities_formatting=GranularitiesFormatting(
                        title_base="title_base_example",
                        title_pattern="%titleBase - %granularityTitle",
                    ),
                    granularities=[
                        "MINUTE",
                    ],
                    tags=["Customer dates"],
                ),
            ],
        ),
        analytics=DeclarativeAnalyticsLayer(
            analytical_dashboards=[
                DeclarativeAnalyticalDashboard(
                    id="revenues-analysis",
                    title="Revenues analysis",
                    description="Period to period comparison of revenues in main sectors.",
                    content={},
                    tags=["Revenues"],
                ),
            ],
            filter_contexts=[
                DeclarativeFilterContext(
                    id="filter-sales",
                    title="Filter Context for Sales team",
                    description="Filter Context for Sales team.",
                    content={},
                    tags=["Revenues"],
                ),
            ],
            metrics=[
                DeclarativeMetric(
                    id="total-sales",
                    title="Total sales",
                    description="Sales for all the data available.",
                    content={},
                    tags=["Revenues"],
                ),
            ],
            visualization_objects=[
                DeclarativeVisualizationObject(
                    id="visualization-1",
                    title="Count of goods",
                    description="Simple number for total goods in current production.",
                    content={},
                    tags=["Revenues"],
                ),
            ],
        ),
    ) # DeclarativeWorkspaceModel | 

    # example passing only required values which don't have defaults set
    try:
        # Set workspace layout
        api_instance.put_workspace_layout(workspace_id, declarative_workspace_model)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling DeclarativeLayoutControllerApi->put_workspace_layout: %s\n" % e)
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
import gooddata_metadata_client
from gooddata_metadata_client.api import declarative_layout_controller_api
from gooddata_metadata_client.model.declarative_analytics import DeclarativeAnalytics
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = declarative_layout_controller_api.DeclarativeLayoutControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    declarative_analytics = DeclarativeAnalytics(
        analytics=DeclarativeAnalyticsLayer(
            analytical_dashboards=[
                DeclarativeAnalyticalDashboard(
                    id="revenues-analysis",
                    title="Revenues analysis",
                    description="Period to period comparison of revenues in main sectors.",
                    content={},
                    tags=["Revenues"],
                ),
            ],
            filter_contexts=[
                DeclarativeFilterContext(
                    id="filter-sales",
                    title="Filter Context for Sales team",
                    description="Filter Context for Sales team.",
                    content={},
                    tags=["Revenues"],
                ),
            ],
            metrics=[
                DeclarativeMetric(
                    id="total-sales",
                    title="Total sales",
                    description="Sales for all the data available.",
                    content={},
                    tags=["Revenues"],
                ),
            ],
            visualization_objects=[
                DeclarativeVisualizationObject(
                    id="visualization-1",
                    title="Count of goods",
                    description="Simple number for total goods in current production.",
                    content={},
                    tags=["Revenues"],
                ),
            ],
        ),
    ) # DeclarativeAnalytics | 

    # example passing only required values which don't have defaults set
    try:
        # Set analytics model
        api_instance.set_analytics_model(workspace_id, declarative_analytics)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling DeclarativeLayoutControllerApi->set_analytics_model: %s\n" % e)
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
import gooddata_metadata_client
from gooddata_metadata_client.api import declarative_layout_controller_api
from gooddata_metadata_client.model.declarative_model import DeclarativeModel
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = declarative_layout_controller_api.DeclarativeLayoutControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    declarative_model = DeclarativeModel(
        ldm=DeclarativeLdm(
            datasets=[
                DeclarativeDataset(
                    id="customers",
                    title="Customers",
                    description="The customers of ours.",
                    grain=[
                        GrainIdentifier(
                            id="attr.customers.customer_name",
                            type="ATTRIBUTE",
                        ),
                    ],
                    attributes=[
                        DeclarativeAttribute(
                            id="attr.customers.customer_name",
                            title="Customer name",
                            description="Customer name including first and last name.",
                            labels=[
                                DeclarativeLabel(
                                    id="label.customer_name",
                                    title="Customer name",
                                    description="Customer name",
                                    primary=False,
                                    source_column="customer_name",
                                    tags=["Customers"],
                                ),
                            ],
                            tags=["Customers"],
                        ),
                    ],
                    facts=[
                        DeclarativeFact(
                            id="fact.customer_order_count",
                            title="Customer order count",
                            description="A number of orders created by the customer - including all orders, even the non-delivered ones.",
                            source_column="customer_order_count",
                            tags=["Customers"],
                        ),
                    ],
                    references=[
                        DeclarativeReference(
                            identifier=ReferenceIdentifier(
                                id="customers",
                                type="DATASET",
                            ),
                            multivalue=False,
                            source_columns=["customer_id"],
                        ),
                    ],
                    data_source_table_id=DataSourceTableIdentifier(
                        id="customers",
                        data_source_id="my-postgres",
                        type="dataSource",
                    ),
                    tags=["Customers"],
                ),
            ],
            date_instances=[
                DeclarativeDateDataset(
                    id="date",
                    title="Date",
                    description="A customer order date",
                    granularities_formatting=GranularitiesFormatting(
                        title_base="title_base_example",
                        title_pattern="%titleBase - %granularityTitle",
                    ),
                    granularities=[
                        "MINUTE",
                    ],
                    tags=["Customer dates"],
                ),
            ],
        ),
    ) # DeclarativeModel | 

    # example passing only required values which don't have defaults set
    try:
        # Set logical model
        api_instance.set_logical_model(workspace_id, declarative_model)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling DeclarativeLayoutControllerApi->set_logical_model: %s\n" % e)
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
import gooddata_metadata_client
from gooddata_metadata_client.api import declarative_layout_controller_api
from gooddata_metadata_client.model.declarative_organization import DeclarativeOrganization
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = declarative_layout_controller_api.DeclarativeLayoutControllerApi(api_client)
    declarative_organization = DeclarativeOrganization(
        organization=DeclarativeOrganizationInfo(
            id="Alpha corporation",
            name="Alpha corporation",
            hostname="alpha.com",
            oauth_issuer_location="oauth_issuer_location_example",
            oauth_client_id="oauth_client_id_example",
            oauth_client_secret="oauth_client_secret_example",
        ),
        users=[
            DeclarativeUser(
                id="employee123",
                auth_id="auth_id_example",
                user_groups=[
                    UserGroupIdentifier(
                        id="group.admins",
                        type="userGroup",
                    ),
                ],
            ),
        ],
        user_groups=[
            DeclarativeUserGroup(
                id="employees.all",
                parents=[
                    UserGroupIdentifier(
                        id="group.admins",
                        type="userGroup",
                    ),
                ],
            ),
        ],
        data_sources=[
            DeclarativeDataSource(
                id="pg_local_docker-demo",
                name="postgres demo",
                type="POSTGRESQL",
                url="jdbc:postgresql://postgres:5432/gooddata",
                schema="demo",
                username="demo",
                password="*****",
                token="Bigquery service account JSON. Encode it using base64!",
                pdm=DeclarativeTables(
                    tables=[
                        DeclarativeTable(
                            id="customers",
                            path=["table_schema","table_name"],
                            type="VIEW",
                            columns=[
                                DeclarativeColumn(
                                    name="customer_id",
                                    data_type="INT",
                                    is_primary_key=True,
                                    referenced_table_id="customers",
                                    referenced_table_column="customer_id",
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        ],
        workspaces=[
            DeclarativeWorkspace(
                id="alpha.sales",
                name="Alpha Sales",
                model=DeclarativeWorkspaceModel(
                    ldm=DeclarativeLdm(
                        datasets=[
                            DeclarativeDataset(
                                id="customers",
                                title="Customers",
                                description="The customers of ours.",
                                grain=[
                                    GrainIdentifier(
                                        id="attr.customers.customer_name",
                                        type="ATTRIBUTE",
                                    ),
                                ],
                                attributes=[
                                    DeclarativeAttribute(
                                        id="attr.customers.customer_name",
                                        title="Customer name",
                                        description="Customer name including first and last name.",
                                        labels=[
                                            DeclarativeLabel(
                                                id="label.customer_name",
                                                title="Customer name",
                                                description="Customer name",
                                                primary=False,
                                                source_column="customer_name",
                                                tags=["Customers"],
                                            ),
                                        ],
                                        tags=["Customers"],
                                    ),
                                ],
                                facts=[
                                    DeclarativeFact(
                                        id="fact.customer_order_count",
                                        title="Customer order count",
                                        description="A number of orders created by the customer - including all orders, even the non-delivered ones.",
                                        source_column="customer_order_count",
                                        tags=["Customers"],
                                    ),
                                ],
                                references=[
                                    DeclarativeReference(
                                        identifier=ReferenceIdentifier(
                                            id="customers",
                                            type="DATASET",
                                        ),
                                        multivalue=False,
                                        source_columns=["customer_id"],
                                    ),
                                ],
                                data_source_table_id=DataSourceTableIdentifier(
                                    id="customers",
                                    data_source_id="my-postgres",
                                    type="dataSource",
                                ),
                                tags=["Customers"],
                            ),
                        ],
                        date_instances=[
                            DeclarativeDateDataset(
                                id="date",
                                title="Date",
                                description="A customer order date",
                                granularities_formatting=GranularitiesFormatting(
                                    title_base="title_base_example",
                                    title_pattern="%titleBase - %granularityTitle",
                                ),
                                granularities=[
                                    "MINUTE",
                                ],
                                tags=["Customer dates"],
                            ),
                        ],
                    ),
                    analytics=DeclarativeAnalyticsLayer(
                        analytical_dashboards=[
                            DeclarativeAnalyticalDashboard(
                                id="revenues-analysis",
                                title="Revenues analysis",
                                description="Period to period comparison of revenues in main sectors.",
                                content={},
                                tags=["Revenues"],
                            ),
                        ],
                        filter_contexts=[
                            DeclarativeFilterContext(
                                id="filter-sales",
                                title="Filter Context for Sales team",
                                description="Filter Context for Sales team.",
                                content={},
                                tags=["Revenues"],
                            ),
                        ],
                        metrics=[
                            DeclarativeMetric(
                                id="total-sales",
                                title="Total sales",
                                description="Sales for all the data available.",
                                content={},
                                tags=["Revenues"],
                            ),
                        ],
                        visualization_objects=[
                            DeclarativeVisualizationObject(
                                id="visualization-1",
                                title="Count of goods",
                                description="Simple number for total goods in current production.",
                                content={},
                                tags=["Revenues"],
                            ),
                        ],
                    ),
                ),
                parent=WorkspaceIdentifier(
                    id="alpha.sales",
                    type="workspace",
                ),
            ),
        ],
        workspace_data_filters=[
            DeclarativeWorkspaceDataFilter(
                id="country_id",
                title="Country ID",
                description="ID of country",
                column_name="country_id",
                workspace_data_filter_settings=[
                    DeclarativeWorkspaceDataFilterSetting(
                        id="country_id_setting",
                        title="Country ID setting",
                        description="ID of country setting",
                        filter_values=["US"],
                        workspace=WorkspaceIdentifier(
                            id="alpha.sales",
                            type="workspace",
                        ),
                    ),
                ],
                workspace=WorkspaceIdentifier(
                    id="alpha.sales",
                    type="workspace",
                ),
            ),
        ],
    ) # DeclarativeOrganization | 

    # example passing only required values which don't have defaults set
    try:
        # Set organization layout
        api_instance.set_organization_layout(declarative_organization)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling DeclarativeLayoutControllerApi->set_organization_layout: %s\n" % e)
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
**201** | Defined all parts of an organization. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_workspace_data_filters_layout**
> set_workspace_data_filters_layout(declarative_workspace_data_filters)

Set all workspace data filters

Sets workspace data filters in all workspaces in entire organization.

### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import declarative_layout_controller_api
from gooddata_metadata_client.model.declarative_workspace_data_filters import DeclarativeWorkspaceDataFilters
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = declarative_layout_controller_api.DeclarativeLayoutControllerApi(api_client)
    declarative_workspace_data_filters = DeclarativeWorkspaceDataFilters(
        workspace_data_filters=[
            DeclarativeWorkspaceDataFilter(
                id="country_id",
                title="Country ID",
                description="ID of country",
                column_name="country_id",
                workspace_data_filter_settings=[
                    DeclarativeWorkspaceDataFilterSetting(
                        id="country_id_setting",
                        title="Country ID setting",
                        description="ID of country setting",
                        filter_values=["US"],
                        workspace=WorkspaceIdentifier(
                            id="alpha.sales",
                            type="workspace",
                        ),
                    ),
                ],
                workspace=WorkspaceIdentifier(
                    id="alpha.sales",
                    type="workspace",
                ),
            ),
        ],
    ) # DeclarativeWorkspaceDataFilters | 

    # example passing only required values which don't have defaults set
    try:
        # Set all workspace data filters
        api_instance.set_workspace_data_filters_layout(declarative_workspace_data_filters)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling DeclarativeLayoutControllerApi->set_workspace_data_filters_layout: %s\n" % e)
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

# **set_workspaces_layout**
> set_workspaces_layout(declarative_workspaces)

Set all workspaces layout

Sets complete layout of workspaces, their hierarchy, models.

### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import declarative_layout_controller_api
from gooddata_metadata_client.model.declarative_workspaces import DeclarativeWorkspaces
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = declarative_layout_controller_api.DeclarativeLayoutControllerApi(api_client)
    declarative_workspaces = DeclarativeWorkspaces(
        workspaces=[
            DeclarativeWorkspace(
                id="alpha.sales",
                name="Alpha Sales",
                model=DeclarativeWorkspaceModel(
                    ldm=DeclarativeLdm(
                        datasets=[
                            DeclarativeDataset(
                                id="customers",
                                title="Customers",
                                description="The customers of ours.",
                                grain=[
                                    GrainIdentifier(
                                        id="attr.customers.customer_name",
                                        type="ATTRIBUTE",
                                    ),
                                ],
                                attributes=[
                                    DeclarativeAttribute(
                                        id="attr.customers.customer_name",
                                        title="Customer name",
                                        description="Customer name including first and last name.",
                                        labels=[
                                            DeclarativeLabel(
                                                id="label.customer_name",
                                                title="Customer name",
                                                description="Customer name",
                                                primary=False,
                                                source_column="customer_name",
                                                tags=["Customers"],
                                            ),
                                        ],
                                        tags=["Customers"],
                                    ),
                                ],
                                facts=[
                                    DeclarativeFact(
                                        id="fact.customer_order_count",
                                        title="Customer order count",
                                        description="A number of orders created by the customer - including all orders, even the non-delivered ones.",
                                        source_column="customer_order_count",
                                        tags=["Customers"],
                                    ),
                                ],
                                references=[
                                    DeclarativeReference(
                                        identifier=ReferenceIdentifier(
                                            id="customers",
                                            type="DATASET",
                                        ),
                                        multivalue=False,
                                        source_columns=["customer_id"],
                                    ),
                                ],
                                data_source_table_id=DataSourceTableIdentifier(
                                    id="customers",
                                    data_source_id="my-postgres",
                                    type="dataSource",
                                ),
                                tags=["Customers"],
                            ),
                        ],
                        date_instances=[
                            DeclarativeDateDataset(
                                id="date",
                                title="Date",
                                description="A customer order date",
                                granularities_formatting=GranularitiesFormatting(
                                    title_base="title_base_example",
                                    title_pattern="%titleBase - %granularityTitle",
                                ),
                                granularities=[
                                    "MINUTE",
                                ],
                                tags=["Customer dates"],
                            ),
                        ],
                    ),
                    analytics=DeclarativeAnalyticsLayer(
                        analytical_dashboards=[
                            DeclarativeAnalyticalDashboard(
                                id="revenues-analysis",
                                title="Revenues analysis",
                                description="Period to period comparison of revenues in main sectors.",
                                content={},
                                tags=["Revenues"],
                            ),
                        ],
                        filter_contexts=[
                            DeclarativeFilterContext(
                                id="filter-sales",
                                title="Filter Context for Sales team",
                                description="Filter Context for Sales team.",
                                content={},
                                tags=["Revenues"],
                            ),
                        ],
                        metrics=[
                            DeclarativeMetric(
                                id="total-sales",
                                title="Total sales",
                                description="Sales for all the data available.",
                                content={},
                                tags=["Revenues"],
                            ),
                        ],
                        visualization_objects=[
                            DeclarativeVisualizationObject(
                                id="visualization-1",
                                title="Count of goods",
                                description="Simple number for total goods in current production.",
                                content={},
                                tags=["Revenues"],
                            ),
                        ],
                    ),
                ),
                parent=WorkspaceIdentifier(
                    id="alpha.sales",
                    type="workspace",
                ),
            ),
        ],
        workspace_data_filters=[
            DeclarativeWorkspaceDataFilter(
                id="country_id",
                title="Country ID",
                description="ID of country",
                column_name="country_id",
                workspace_data_filter_settings=[
                    DeclarativeWorkspaceDataFilterSetting(
                        id="country_id_setting",
                        title="Country ID setting",
                        description="ID of country setting",
                        filter_values=["US"],
                        workspace=WorkspaceIdentifier(
                            id="alpha.sales",
                            type="workspace",
                        ),
                    ),
                ],
                workspace=WorkspaceIdentifier(
                    id="alpha.sales",
                    type="workspace",
                ),
            ),
        ],
    ) # DeclarativeWorkspaces | 

    # example passing only required values which don't have defaults set
    try:
        # Set all workspaces layout
        api_instance.set_workspaces_layout(declarative_workspaces)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling DeclarativeLayoutControllerApi->set_workspaces_layout: %s\n" % e)
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


# gooddata_api_client.ManagePermissionsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_data_source_permissions**](ManagePermissionsApi.md#get_data_source_permissions) | **GET** /api/v1/layout/dataSources/{dataSourceId}/permissions | Get permissions for the data source
[**manage_data_source_permissions**](ManagePermissionsApi.md#manage_data_source_permissions) | **POST** /api/v1/actions/dataSources/{dataSourceId}/managePermissions | Manage Permissions for a Data Source
[**set_data_source_permissions**](ManagePermissionsApi.md#set_data_source_permissions) | **PUT** /api/v1/layout/dataSources/{dataSourceId}/permissions | Set data source permissions.


# **get_data_source_permissions**
> DeclarativeDataSourcePermissions get_data_source_permissions(data_source_id)

Get permissions for the data source

Retrieve current set of permissions of the data source in a declarative form.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import manage_permissions_api
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
    api_instance = manage_permissions_api.ManagePermissionsApi(api_client)
    data_source_id = "dataSourceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get permissions for the data source
        api_response = api_instance.get_data_source_permissions(data_source_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ManagePermissionsApi->get_data_source_permissions: %s\n" % e)
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

# **manage_data_source_permissions**
> manage_data_source_permissions(data_source_id, data_source_permission_assignment)

Manage Permissions for a Data Source

Manage Permissions for a Data Source

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import manage_permissions_api
from gooddata_api_client.model.data_source_permission_assignment import DataSourcePermissionAssignment
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = manage_permissions_api.ManagePermissionsApi(api_client)
    data_source_id = "dataSourceId_example" # str | 
    data_source_permission_assignment = [
        DataSourcePermissionAssignment(
            assignee_identifier=AssigneeIdentifier(
                id="id_example",
                type="user",
            ),
            permissions=[
                "MANAGE",
            ],
        ),
    ] # [DataSourcePermissionAssignment] | 

    # example passing only required values which don't have defaults set
    try:
        # Manage Permissions for a Data Source
        api_instance.manage_data_source_permissions(data_source_id, data_source_permission_assignment)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ManagePermissionsApi->manage_data_source_permissions: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  |
 **data_source_permission_assignment** | [**[DataSourcePermissionAssignment]**](DataSourcePermissionAssignment.md)|  |

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

# **set_data_source_permissions**
> set_data_source_permissions(data_source_id, declarative_data_source_permissions)

Set data source permissions.

set data source permissions.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import manage_permissions_api
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
    api_instance = manage_permissions_api.ManagePermissionsApi(api_client)
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
        print("Exception when calling ManagePermissionsApi->set_data_source_permissions: %s\n" % e)
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


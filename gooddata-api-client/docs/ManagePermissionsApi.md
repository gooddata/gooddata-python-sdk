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
    api_instance = gooddata_api_client.ManagePermissionsApi(api_client)
    data_source_id = 'data_source_id_example' # str | 

    try:
        # Get permissions for the data source
        api_response = api_instance.get_data_source_permissions(data_source_id)
        print("The response of ManagePermissionsApi->get_data_source_permissions:\n")
        pprint(api_response)
    except Exception as e:
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
    api_instance = gooddata_api_client.ManagePermissionsApi(api_client)
    data_source_id = 'data_source_id_example' # str | 
    data_source_permission_assignment = [gooddata_api_client.DataSourcePermissionAssignment()] # List[DataSourcePermissionAssignment] | 

    try:
        # Manage Permissions for a Data Source
        api_instance.manage_data_source_permissions(data_source_id, data_source_permission_assignment)
    except Exception as e:
        print("Exception when calling ManagePermissionsApi->manage_data_source_permissions: %s\n" % e)
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
    api_instance = gooddata_api_client.ManagePermissionsApi(api_client)
    data_source_id = 'data_source_id_example' # str | 
    declarative_data_source_permissions = gooddata_api_client.DeclarativeDataSourcePermissions() # DeclarativeDataSourcePermissions | 

    try:
        # Set data source permissions.
        api_instance.set_data_source_permissions(data_source_id, declarative_data_source_permissions)
    except Exception as e:
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


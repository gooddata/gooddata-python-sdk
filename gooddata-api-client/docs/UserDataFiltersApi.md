# gooddata_api_client.UserDataFiltersApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_user_data_filters**](UserDataFiltersApi.md#get_user_data_filters) | **GET** /api/v1/layout/workspaces/{workspaceId}/userDataFilters | Get user data filters
[**set_user_data_filters**](UserDataFiltersApi.md#set_user_data_filters) | **PUT** /api/v1/layout/workspaces/{workspaceId}/userDataFilters | Set user data filters


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
    api_instance = gooddata_api_client.UserDataFiltersApi(api_client)
    workspace_id = 'workspace_id_example' # str | 

    try:
        # Get user data filters
        api_response = api_instance.get_user_data_filters(workspace_id)
        print("The response of UserDataFiltersApi->get_user_data_filters:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserDataFiltersApi->get_user_data_filters: %s\n" % e)
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
    api_instance = gooddata_api_client.UserDataFiltersApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    declarative_user_data_filters = gooddata_api_client.DeclarativeUserDataFilters() # DeclarativeUserDataFilters | 

    try:
        # Set user data filters
        api_instance.set_user_data_filters(workspace_id, declarative_user_data_filters)
    except Exception as e:
        print("Exception when calling UserDataFiltersApi->set_user_data_filters: %s\n" % e)
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


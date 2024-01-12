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
import time
import gooddata_api_client
from gooddata_api_client.api import user_data_filters_api
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
    api_instance = user_data_filters_api.UserDataFiltersApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get user data filters
        api_response = api_instance.get_user_data_filters(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import user_data_filters_api
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
    api_instance = user_data_filters_api.UserDataFiltersApi(api_client)
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


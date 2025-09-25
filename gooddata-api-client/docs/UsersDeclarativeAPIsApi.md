# gooddata_api_client.UsersDeclarativeAPIsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_users_layout**](UsersDeclarativeAPIsApi.md#get_users_layout) | **GET** /api/v1/layout/users | Get all users
[**put_users_layout**](UsersDeclarativeAPIsApi.md#put_users_layout) | **PUT** /api/v1/layout/users | Put all users


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
    api_instance = gooddata_api_client.UsersDeclarativeAPIsApi(api_client)

    try:
        # Get all users
        api_response = api_instance.get_users_layout()
        print("The response of UsersDeclarativeAPIsApi->get_users_layout:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersDeclarativeAPIsApi->get_users_layout: %s\n" % e)
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
    api_instance = gooddata_api_client.UsersDeclarativeAPIsApi(api_client)
    declarative_users = gooddata_api_client.DeclarativeUsers() # DeclarativeUsers | 

    try:
        # Put all users
        api_instance.put_users_layout(declarative_users)
    except Exception as e:
        print("Exception when calling UsersDeclarativeAPIsApi->put_users_layout: %s\n" % e)
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


# gooddata_api_client.UserGroupsDeclarativeAPIsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_user_groups_layout**](UserGroupsDeclarativeAPIsApi.md#get_user_groups_layout) | **GET** /api/v1/layout/userGroups | Get all user groups
[**get_users_user_groups_layout**](UserGroupsDeclarativeAPIsApi.md#get_users_user_groups_layout) | **GET** /api/v1/layout/usersAndUserGroups | Get all users and user groups
[**put_user_groups_layout**](UserGroupsDeclarativeAPIsApi.md#put_user_groups_layout) | **PUT** /api/v1/layout/userGroups | Put all user groups
[**put_users_user_groups_layout**](UserGroupsDeclarativeAPIsApi.md#put_users_user_groups_layout) | **PUT** /api/v1/layout/usersAndUserGroups | Put all users and user groups


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
    api_instance = gooddata_api_client.UserGroupsDeclarativeAPIsApi(api_client)

    try:
        # Get all user groups
        api_response = api_instance.get_user_groups_layout()
        print("The response of UserGroupsDeclarativeAPIsApi->get_user_groups_layout:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserGroupsDeclarativeAPIsApi->get_user_groups_layout: %s\n" % e)
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
    api_instance = gooddata_api_client.UserGroupsDeclarativeAPIsApi(api_client)

    try:
        # Get all users and user groups
        api_response = api_instance.get_users_user_groups_layout()
        print("The response of UserGroupsDeclarativeAPIsApi->get_users_user_groups_layout:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserGroupsDeclarativeAPIsApi->get_users_user_groups_layout: %s\n" % e)
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
    api_instance = gooddata_api_client.UserGroupsDeclarativeAPIsApi(api_client)
    declarative_user_groups = gooddata_api_client.DeclarativeUserGroups() # DeclarativeUserGroups | 

    try:
        # Put all user groups
        api_instance.put_user_groups_layout(declarative_user_groups)
    except Exception as e:
        print("Exception when calling UserGroupsDeclarativeAPIsApi->put_user_groups_layout: %s\n" % e)
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
    api_instance = gooddata_api_client.UserGroupsDeclarativeAPIsApi(api_client)
    declarative_users_user_groups = gooddata_api_client.DeclarativeUsersUserGroups() # DeclarativeUsersUserGroups | 

    try:
        # Put all users and user groups
        api_instance.put_users_user_groups_layout(declarative_users_user_groups)
    except Exception as e:
        print("Exception when calling UserGroupsDeclarativeAPIsApi->put_users_user_groups_layout: %s\n" % e)
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


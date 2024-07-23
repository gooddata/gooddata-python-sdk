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
import time
import gooddata_api_client
from gooddata_api_client.api import users_declarative_apis_api
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
    api_instance = users_declarative_apis_api.UsersDeclarativeAPIsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get all users
        api_response = api_instance.get_users_layout()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import users_declarative_apis_api
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
    api_instance = users_declarative_apis_api.UsersDeclarativeAPIsApi(api_client)
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


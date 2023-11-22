<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.users_declarative_apis_api.UsersDeclarativeAPIsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_users_layout**](#get_users_layout) | **get** /api/v1/layout/users | Get all users
[**put_users_layout**](#put_users_layout) | **put** /api/v1/layout/users | Put all users

# **get_users_layout**
<a id="get_users_layout"></a>
> DeclarativeUsers get_users_layout()

Get all users

Retrieve all users including authentication properties.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import users_declarative_apis_api
from gooddata_api_client.model.declarative_users import DeclarativeUsers
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
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

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_users_layout.ApiResponseFor200) | Retrieved all users.

#### get_users_layout.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeUsers**](../../models/DeclarativeUsers.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **put_users_layout**
<a id="put_users_layout"></a>
> put_users_layout(declarative_users)

Put all users

Set all users and their authentication properties.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import users_declarative_apis_api
from gooddata_api_client.model.declarative_users import DeclarativeUsers
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = users_declarative_apis_api.UsersDeclarativeAPIsApi(api_client)

    # example passing only required values which don't have defaults set
    body = DeclarativeUsers(
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
                    )
                ],
                settings=[
                    DeclarativeSetting(
                        content=dict(),
                        id="/6bUUGjjNSwg0_bs",
                        type="TIMEZONE",
                    )
                ],
                user_groups=[
                    UserGroupIdentifier(
                        id="group.admins",
                        type="userGroup",
                    )
                ],
            )
        ],
    )
    try:
        # Put all users
        api_response = api_instance.put_users_layout(
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UsersDeclarativeAPIsApi->put_users_layout: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeUsers**](../../models/DeclarativeUsers.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#put_users_layout.ApiResponseFor200) | Defined all users.

#### put_users_layout.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


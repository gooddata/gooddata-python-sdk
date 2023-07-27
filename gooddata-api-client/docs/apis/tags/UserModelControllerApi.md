<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.user_model_controller_api.UserModelControllerApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_api_tokens**](#create_entity_api_tokens) | **post** /api/v1/entities/users/{userId}/apiTokens | Post a new API token for the user
[**create_entity_user_settings**](#create_entity_user_settings) | **post** /api/v1/entities/users/{userId}/userSettings | Post new user settings for the user
[**delete_entity_api_tokens**](#delete_entity_api_tokens) | **delete** /api/v1/entities/users/{userId}/apiTokens/{id} | Delete an API Token for a user
[**delete_entity_user_settings**](#delete_entity_user_settings) | **delete** /api/v1/entities/users/{userId}/userSettings/{id} | Delete a setting for a user
[**get_all_entities_api_tokens**](#get_all_entities_api_tokens) | **get** /api/v1/entities/users/{userId}/apiTokens | List all api tokens for a user
[**get_all_entities_user_settings**](#get_all_entities_user_settings) | **get** /api/v1/entities/users/{userId}/userSettings | List all settings for a user
[**get_entity_api_tokens**](#get_entity_api_tokens) | **get** /api/v1/entities/users/{userId}/apiTokens/{id} | Get an API Token for a user
[**get_entity_user_settings**](#get_entity_user_settings) | **get** /api/v1/entities/users/{userId}/userSettings/{id} | Get a setting for a user
[**update_entity_api_tokens**](#update_entity_api_tokens) | **put** /api/v1/entities/users/{userId}/apiTokens/{id} | Put new API token for the user
[**update_entity_user_settings**](#update_entity_user_settings) | **put** /api/v1/entities/users/{userId}/userSettings/{id} | Put new user settings for the user

# **create_entity_api_tokens**
<a id="create_entity_api_tokens"></a>
> JsonApiApiTokenOutDocument create_entity_api_tokens(user_idjson_api_api_token_in_document)

Post a new API token for the user

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import user_model_controller_api
from gooddata_api_client.model.json_api_api_token_out_document import JsonApiApiTokenOutDocument
from gooddata_api_client.model.json_api_api_token_in_document import JsonApiApiTokenInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_model_controller_api.UserModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'userId': "userId_example",
    }
    body = JsonApiApiTokenInDocument(
        data=JsonApiApiTokenIn(
            id="id1",
            type="apiToken",
        ),
    )
    try:
        # Post a new API token for the user
        api_response = api_instance.create_entity_api_tokens(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserModelControllerApi->create_entity_api_tokens: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiApiTokenInDocument**](../../models/JsonApiApiTokenInDocument.md) |  | 


### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
userId | UserIdSchema | | 

# UserIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#create_entity_api_tokens.ApiResponseFor201) | Request successfully processed

#### create_entity_api_tokens.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiApiTokenOutDocument**](../../models/JsonApiApiTokenOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **create_entity_user_settings**
<a id="create_entity_user_settings"></a>
> JsonApiUserSettingOutDocument create_entity_user_settings(user_idjson_api_user_setting_in_document)

Post new user settings for the user

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import user_model_controller_api
from gooddata_api_client.model.json_api_user_setting_out_document import JsonApiUserSettingOutDocument
from gooddata_api_client.model.json_api_user_setting_in_document import JsonApiUserSettingInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_model_controller_api.UserModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'userId': "userId_example",
    }
    body = JsonApiUserSettingInDocument(
        data=JsonApiUserSettingIn(
            attributes=dict(
                content=dict(),
                type="TIMEZONE",
            ),
            id="id1",
            type="userSetting",
        ),
    )
    try:
        # Post new user settings for the user
        api_response = api_instance.create_entity_user_settings(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserModelControllerApi->create_entity_user_settings: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiUserSettingInDocument**](../../models/JsonApiUserSettingInDocument.md) |  | 


### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
userId | UserIdSchema | | 

# UserIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#create_entity_user_settings.ApiResponseFor201) | Request successfully processed

#### create_entity_user_settings.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiUserSettingOutDocument**](../../models/JsonApiUserSettingOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_entity_api_tokens**
<a id="delete_entity_api_tokens"></a>
> delete_entity_api_tokens(user_idid)

Delete an API Token for a user

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import user_model_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_model_controller_api.UserModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'userId': "userId_example",
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Delete an API Token for a user
        api_response = api_instance.delete_entity_api_tokens(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserModelControllerApi->delete_entity_api_tokens: %s\n" % e)

    # example passing only optional values
    path_params = {
        'userId': "userId_example",
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=bearerToken==someString",
    }
    try:
        # Delete an API Token for a user
        api_response = api_instance.delete_entity_api_tokens(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserModelControllerApi->delete_entity_api_tokens: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
userId | UserIdSchema | | 
id | IdSchema | | 

# UserIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#delete_entity_api_tokens.ApiResponseFor204) | Successfully deleted

#### delete_entity_api_tokens.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_entity_user_settings**
<a id="delete_entity_user_settings"></a>
> delete_entity_user_settings(user_idid)

Delete a setting for a user

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import user_model_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_model_controller_api.UserModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'userId': "userId_example",
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Delete a setting for a user
        api_response = api_instance.delete_entity_user_settings(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserModelControllerApi->delete_entity_user_settings: %s\n" % e)

    # example passing only optional values
    path_params = {
        'userId': "userId_example",
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=content==JsonNodeValue;type==SettingConfigurationValue",
    }
    try:
        # Delete a setting for a user
        api_response = api_instance.delete_entity_user_settings(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserModelControllerApi->delete_entity_user_settings: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
userId | UserIdSchema | | 
id | IdSchema | | 

# UserIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#delete_entity_user_settings.ApiResponseFor204) | Successfully deleted

#### delete_entity_user_settings.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_api_tokens**
<a id="get_all_entities_api_tokens"></a>
> JsonApiApiTokenOutList get_all_entities_api_tokens(user_id)

List all api tokens for a user

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import user_model_controller_api
from gooddata_api_client.model.json_api_api_token_out_list import JsonApiApiTokenOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_model_controller_api.UserModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'userId': "userId_example",
    }
    query_params = {
    }
    try:
        # List all api tokens for a user
        api_response = api_instance.get_all_entities_api_tokens(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserModelControllerApi->get_all_entities_api_tokens: %s\n" % e)

    # example passing only optional values
    path_params = {
        'userId': "userId_example",
    }
    query_params = {
        'filter': "filter=bearerToken==someString",
        'page': 0,
        'size': 20,
        'sort': [
        "sort_example"
    ],
    }
    try:
        # List all api tokens for a user
        api_response = api_instance.get_all_entities_api_tokens(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserModelControllerApi->get_all_entities_api_tokens: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
page | PageSchema | | optional
size | SizeSchema | | optional
sort | SortSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# PageSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 0

# SizeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 20

# SortSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
userId | UserIdSchema | | 

# UserIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_all_entities_api_tokens.ApiResponseFor200) | Request successfully processed

#### get_all_entities_api_tokens.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiApiTokenOutList**](../../models/JsonApiApiTokenOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_user_settings**
<a id="get_all_entities_user_settings"></a>
> JsonApiUserSettingOutList get_all_entities_user_settings(user_id)

List all settings for a user

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import user_model_controller_api
from gooddata_api_client.model.json_api_user_setting_out_list import JsonApiUserSettingOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_model_controller_api.UserModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'userId': "userId_example",
    }
    query_params = {
    }
    try:
        # List all settings for a user
        api_response = api_instance.get_all_entities_user_settings(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserModelControllerApi->get_all_entities_user_settings: %s\n" % e)

    # example passing only optional values
    path_params = {
        'userId': "userId_example",
    }
    query_params = {
        'filter': "filter=content==JsonNodeValue;type==SettingConfigurationValue",
        'page': 0,
        'size': 20,
        'sort': [
        "sort_example"
    ],
    }
    try:
        # List all settings for a user
        api_response = api_instance.get_all_entities_user_settings(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserModelControllerApi->get_all_entities_user_settings: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
page | PageSchema | | optional
size | SizeSchema | | optional
sort | SortSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# PageSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 0

# SizeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 20

# SortSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
userId | UserIdSchema | | 

# UserIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_all_entities_user_settings.ApiResponseFor200) | Request successfully processed

#### get_all_entities_user_settings.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiUserSettingOutList**](../../models/JsonApiUserSettingOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_api_tokens**
<a id="get_entity_api_tokens"></a>
> JsonApiApiTokenOutDocument get_entity_api_tokens(user_idid)

Get an API Token for a user

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import user_model_controller_api
from gooddata_api_client.model.json_api_api_token_out_document import JsonApiApiTokenOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_model_controller_api.UserModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'userId': "userId_example",
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Get an API Token for a user
        api_response = api_instance.get_entity_api_tokens(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserModelControllerApi->get_entity_api_tokens: %s\n" % e)

    # example passing only optional values
    path_params = {
        'userId': "userId_example",
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=bearerToken==someString",
    }
    try:
        # Get an API Token for a user
        api_response = api_instance.get_entity_api_tokens(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserModelControllerApi->get_entity_api_tokens: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
userId | UserIdSchema | | 
id | IdSchema | | 

# UserIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_entity_api_tokens.ApiResponseFor200) | Request successfully processed

#### get_entity_api_tokens.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiApiTokenOutDocument**](../../models/JsonApiApiTokenOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_user_settings**
<a id="get_entity_user_settings"></a>
> JsonApiUserSettingOutDocument get_entity_user_settings(user_idid)

Get a setting for a user

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import user_model_controller_api
from gooddata_api_client.model.json_api_user_setting_out_document import JsonApiUserSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_model_controller_api.UserModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'userId': "userId_example",
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Get a setting for a user
        api_response = api_instance.get_entity_user_settings(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserModelControllerApi->get_entity_user_settings: %s\n" % e)

    # example passing only optional values
    path_params = {
        'userId': "userId_example",
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=content==JsonNodeValue;type==SettingConfigurationValue",
    }
    try:
        # Get a setting for a user
        api_response = api_instance.get_entity_user_settings(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserModelControllerApi->get_entity_user_settings: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
userId | UserIdSchema | | 
id | IdSchema | | 

# UserIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_entity_user_settings.ApiResponseFor200) | Request successfully processed

#### get_entity_user_settings.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiUserSettingOutDocument**](../../models/JsonApiUserSettingOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_entity_api_tokens**
<a id="update_entity_api_tokens"></a>
> JsonApiApiTokenOutDocument update_entity_api_tokens(user_ididjson_api_api_token_in_document)

Put new API token for the user

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import user_model_controller_api
from gooddata_api_client.model.json_api_api_token_out_document import JsonApiApiTokenOutDocument
from gooddata_api_client.model.json_api_api_token_in_document import JsonApiApiTokenInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_model_controller_api.UserModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'userId': "userId_example",
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiApiTokenInDocument(
        data=JsonApiApiTokenIn(
            id="id1",
            type="apiToken",
        ),
    )
    try:
        # Put new API token for the user
        api_response = api_instance.update_entity_api_tokens(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserModelControllerApi->update_entity_api_tokens: %s\n" % e)

    # example passing only optional values
    path_params = {
        'userId': "userId_example",
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=bearerToken==someString",
    }
    body = JsonApiApiTokenInDocument(
        data=JsonApiApiTokenIn(
            id="id1",
            type="apiToken",
        ),
    )
    try:
        # Put new API token for the user
        api_response = api_instance.update_entity_api_tokens(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserModelControllerApi->update_entity_api_tokens: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiApiTokenInDocument**](../../models/JsonApiApiTokenInDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
userId | UserIdSchema | | 
id | IdSchema | | 

# UserIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_entity_api_tokens.ApiResponseFor200) | Request successfully processed

#### update_entity_api_tokens.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiApiTokenOutDocument**](../../models/JsonApiApiTokenOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_entity_user_settings**
<a id="update_entity_user_settings"></a>
> JsonApiUserSettingOutDocument update_entity_user_settings(user_ididjson_api_user_setting_in_document)

Put new user settings for the user

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import user_model_controller_api
from gooddata_api_client.model.json_api_user_setting_out_document import JsonApiUserSettingOutDocument
from gooddata_api_client.model.json_api_user_setting_in_document import JsonApiUserSettingInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_model_controller_api.UserModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'userId': "userId_example",
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiUserSettingInDocument(
        data=JsonApiUserSettingIn(
            attributes=dict(
                content=dict(),
                type="TIMEZONE",
            ),
            id="id1",
            type="userSetting",
        ),
    )
    try:
        # Put new user settings for the user
        api_response = api_instance.update_entity_user_settings(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserModelControllerApi->update_entity_user_settings: %s\n" % e)

    # example passing only optional values
    path_params = {
        'userId': "userId_example",
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=content==JsonNodeValue;type==SettingConfigurationValue",
    }
    body = JsonApiUserSettingInDocument(
        data=JsonApiUserSettingIn(
            attributes=dict(
                content=dict(),
                type="TIMEZONE",
            ),
            id="id1",
            type="userSetting",
        ),
    )
    try:
        # Put new user settings for the user
        api_response = api_instance.update_entity_user_settings(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserModelControllerApi->update_entity_user_settings: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiUserSettingInDocument**](../../models/JsonApiUserSettingInDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
userId | UserIdSchema | | 
id | IdSchema | | 

# UserIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_entity_user_settings.ApiResponseFor200) | Request successfully processed

#### update_entity_user_settings.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiUserSettingOutDocument**](../../models/JsonApiUserSettingOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


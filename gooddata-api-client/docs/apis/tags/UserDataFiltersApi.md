<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.user_data_filters_api.UserDataFiltersApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_user_data_filters**](#get_user_data_filters) | **get** /api/v1/layout/workspaces/{workspaceId}/userDataFilters | Get user data filters
[**set_user_data_filters**](#set_user_data_filters) | **put** /api/v1/layout/workspaces/{workspaceId}/userDataFilters | Set user data filters

# **get_user_data_filters**
<a id="get_user_data_filters"></a>
> DeclarativeUserDataFilters get_user_data_filters(workspace_id)

Get user data filters

Retrieve current user data filters assigned to the workspace.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import user_data_filters_api
from gooddata_api_client.model.declarative_user_data_filters import DeclarativeUserDataFilters
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_data_filters_api.UserDataFiltersApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    try:
        # Get user data filters
        api_response = api_instance.get_user_data_filters(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserDataFiltersApi->get_user_data_filters: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_user_data_filters.ApiResponseFor200) | Retrieved current user data filters.

#### get_user_data_filters.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeUserDataFilters**](../../models/DeclarativeUserDataFilters.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **set_user_data_filters**
<a id="set_user_data_filters"></a>
> set_user_data_filters(workspace_iddeclarative_user_data_filters)

Set user data filters

Set user data filters assigned to the workspace.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import user_data_filters_api
from gooddata_api_client.model.declarative_user_data_filters import DeclarativeUserDataFilters
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_data_filters_api.UserDataFiltersApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    body = DeclarativeUserDataFilters(
        user_data_filters=[
            DeclarativeUserDataFilter(
                description="ID of country setting",
                id="country_id_setting",
                maql="{label/country} = \"USA\" AND {label/date.year} = THIS(YEAR)",
                tags=["Revenues"],
                title="Country ID setting",
                user=UserIdentifier(
                    id="employee123",
                    type="user",
                ),
                user_group=UserGroupIdentifier(
                    id="group.admins",
                    type="userGroup",
                ),
            )
        ],
    )
    try:
        # Set user data filters
        api_response = api_instance.set_user_data_filters(
            path_params=path_params,
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserDataFiltersApi->set_user_data_filters: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeUserDataFilters**](../../models/DeclarativeUserDataFilters.md) |  | 


### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#set_user_data_filters.ApiResponseFor204) | User data filters successfully set.

#### set_user_data_filters.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


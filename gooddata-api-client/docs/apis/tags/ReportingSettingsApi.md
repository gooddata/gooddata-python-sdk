<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.reporting_settings_api.ReportingSettingsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**resolve_all_settings_without_workspace**](#resolve_all_settings_without_workspace) | **get** /api/v1/actions/resolveSettings | Values for all settings without workspace.
[**resolve_settings_without_workspace**](#resolve_settings_without_workspace) | **post** /api/v1/actions/resolveSettings | Values for selected settings without workspace.

# **resolve_all_settings_without_workspace**
<a id="resolve_all_settings_without_workspace"></a>
> [ResolvedSetting] resolve_all_settings_without_workspace()

Values for all settings without workspace.

Resolves values for all settings without workspace by current user, organization, or default settings.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import reporting_settings_api
from gooddata_api_client.model.resolved_setting import ResolvedSetting
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = reporting_settings_api.ReportingSettingsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Values for all settings without workspace.
        api_response = api_instance.resolve_all_settings_without_workspace()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ReportingSettingsApi->resolve_all_settings_without_workspace: %s\n" % e)
```
### Parameters
This endpoint does not need any parameter.

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#resolve_all_settings_without_workspace.ApiResponseFor200) | Values for selected settings.

#### resolve_all_settings_without_workspace.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**ResolvedSetting**]({{complexTypePrefix}}ResolvedSetting.md) | [**ResolvedSetting**]({{complexTypePrefix}}ResolvedSetting.md) | [**ResolvedSetting**]({{complexTypePrefix}}ResolvedSetting.md) |  | 

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **resolve_settings_without_workspace**
<a id="resolve_settings_without_workspace"></a>
> [ResolvedSetting] resolve_settings_without_workspace(resolve_settings_request)

Values for selected settings without workspace.

Resolves values for selected settings without workspace by current user, organization, or default settings.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import reporting_settings_api
from gooddata_api_client.model.resolved_setting import ResolvedSetting
from gooddata_api_client.model.resolve_settings_request import ResolveSettingsRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = reporting_settings_api.ReportingSettingsApi(api_client)

    # example passing only required values which don't have defaults set
    body = ResolveSettingsRequest(
        settings=["timezone"],
    )
    try:
        # Values for selected settings without workspace.
        api_response = api_instance.resolve_settings_without_workspace(
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ReportingSettingsApi->resolve_settings_without_workspace: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ResolveSettingsRequest**](../../models/ResolveSettingsRequest.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#resolve_settings_without_workspace.ApiResponseFor200) | Values for selected settings.

#### resolve_settings_without_workspace.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**ResolvedSetting**]({{complexTypePrefix}}ResolvedSetting.md) | [**ResolvedSetting**]({{complexTypePrefix}}ResolvedSetting.md) | [**ResolvedSetting**]({{complexTypePrefix}}ResolvedSetting.md) |  | 

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


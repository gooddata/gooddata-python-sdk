<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.invalidate_cache_api.InvalidateCacheApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**register_upload_notification**](#register_upload_notification) | **post** /api/v1/actions/dataSources/{dataSourceId}/uploadNotification | Register an upload notification

# **register_upload_notification**
<a id="register_upload_notification"></a>
> register_upload_notification(data_source_id)

Register an upload notification

Notification sets up all reports to be computed again with new data.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import invalidate_cache_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = invalidate_cache_api.InvalidateCacheApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'dataSourceId': "dataSourceId_example",
    }
    try:
        # Register an upload notification
        api_response = api_instance.register_upload_notification(
            path_params=path_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling InvalidateCacheApi->register_upload_notification: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
dataSourceId | DataSourceIdSchema | | 

# DataSourceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#register_upload_notification.ApiResponseFor204) | An upload notification has been successfully registered.

#### register_upload_notification.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


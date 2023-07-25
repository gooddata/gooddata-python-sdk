<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.usage_api.UsageApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**all_platform_usage**](#all_platform_usage) | **get** /api/v1/actions/collectUsage | Info about the platform usage.
[**particular_platform_usage**](#particular_platform_usage) | **post** /api/v1/actions/collectUsage | Info about the platform usage for particular items.

# **all_platform_usage**
<a id="all_platform_usage"></a>
> [PlatformUsage] all_platform_usage()

Info about the platform usage.

Provides information about platform usage, like amount of users, workspaces, ...

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import usage_api
from gooddata_api_client.model.platform_usage import PlatformUsage
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = usage_api.UsageApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Info about the platform usage.
        api_response = api_instance.all_platform_usage()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UsageApi->all_platform_usage: %s\n" % e)
```
### Parameters
This endpoint does not need any parameter.

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#all_platform_usage.ApiResponseFor200) | OK

#### all_platform_usage.ApiResponseFor200
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
[**PlatformUsage**]({{complexTypePrefix}}PlatformUsage.md) | [**PlatformUsage**]({{complexTypePrefix}}PlatformUsage.md) | [**PlatformUsage**]({{complexTypePrefix}}PlatformUsage.md) |  | 

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **particular_platform_usage**
<a id="particular_platform_usage"></a>
> [PlatformUsage] particular_platform_usage(platform_usage_request)

Info about the platform usage for particular items.

Provides information about platform usage, like amount of users, workspaces, ...

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import usage_api
from gooddata_api_client.model.platform_usage_request import PlatformUsageRequest
from gooddata_api_client.model.platform_usage import PlatformUsage
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = usage_api.UsageApi(api_client)

    # example passing only required values which don't have defaults set
    body = PlatformUsageRequest(
        usage_item_names=[
            "UserCount"
        ],
    )
    try:
        # Info about the platform usage for particular items.
        api_response = api_instance.particular_platform_usage(
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UsageApi->particular_platform_usage: %s\n" % e)
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
[**PlatformUsageRequest**](../../models/PlatformUsageRequest.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#particular_platform_usage.ApiResponseFor200) | OK

#### particular_platform_usage.ApiResponseFor200
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
[**PlatformUsage**]({{complexTypePrefix}}PlatformUsage.md) | [**PlatformUsage**]({{complexTypePrefix}}PlatformUsage.md) | [**PlatformUsage**]({{complexTypePrefix}}PlatformUsage.md) |  | 

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


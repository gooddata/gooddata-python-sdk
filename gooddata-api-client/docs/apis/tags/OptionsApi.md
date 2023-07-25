<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.options_api.OptionsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_all_options**](#get_all_options) | **get** /api/v1/options | Links for all configuration options

# **get_all_options**
<a id="get_all_options"></a>
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} get_all_options()

Links for all configuration options

Retrieves links for all options for different configurations.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import options_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = options_api.OptionsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Links for all configuration options
        api_response = api_instance.get_all_options()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OptionsApi->get_all_options: %s\n" % e)
```
### Parameters
This endpoint does not need any parameter.

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_all_options.ApiResponseFor200) | Links for all configuration options.

#### get_all_options.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


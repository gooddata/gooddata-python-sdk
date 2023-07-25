<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.available_drivers_api.AvailableDriversApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_data_source_drivers**](#get_data_source_drivers) | **get** /api/v1/options/availableDrivers | Get all available data source drivers

# **get_data_source_drivers**
<a id="get_data_source_drivers"></a>
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} get_data_source_drivers()

Get all available data source drivers

Retrieves a list of all supported data sources along with information about the used drivers.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import available_drivers_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = available_drivers_api.AvailableDriversApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get all available data source drivers
        api_response = api_instance.get_data_source_drivers()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AvailableDriversApi->get_data_source_drivers: %s\n" % e)
```
### Parameters
This endpoint does not need any parameter.

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_data_source_drivers.ApiResponseFor200) | A list of all available data source drivers.

#### get_data_source_drivers.ApiResponseFor200
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


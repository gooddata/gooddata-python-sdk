# gooddata_api_client.AvailableDriversApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_data_source_drivers**](AvailableDriversApi.md#get_data_source_drivers) | **GET** /api/v1/options/availableDrivers | Get all available data source drivers


# **get_data_source_drivers**
> Dict[str, str] get_data_source_drivers()

Get all available data source drivers

Retrieves a list of all supported data sources along with information about the used drivers.

### Example


```python
import gooddata_api_client
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
    api_instance = gooddata_api_client.AvailableDriversApi(api_client)

    try:
        # Get all available data source drivers
        api_response = api_instance.get_data_source_drivers()
        print("The response of AvailableDriversApi->get_data_source_drivers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AvailableDriversApi->get_data_source_drivers: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**Dict[str, str]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of all available data source drivers. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


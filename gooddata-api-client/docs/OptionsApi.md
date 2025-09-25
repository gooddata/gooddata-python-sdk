# gooddata_api_client.OptionsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_all_options**](OptionsApi.md#get_all_options) | **GET** /api/v1/options | Links for all configuration options


# **get_all_options**
> object get_all_options()

Links for all configuration options

Retrieves links for all options for different configurations.

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
    api_instance = gooddata_api_client.OptionsApi(api_client)

    try:
        # Links for all configuration options
        api_response = api_instance.get_all_options()
        print("The response of OptionsApi->get_all_options:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OptionsApi->get_all_options: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Links for all configuration options. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


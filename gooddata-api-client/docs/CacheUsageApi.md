# gooddata_api_client.CacheUsageApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**collect_cache_usage**](CacheUsageApi.md#collect_cache_usage) | **GET** /api/v1/actions/collectCacheUsage | Collect data about the current cache usage


# **collect_cache_usage**
> CacheUsageData collect_cache_usage()

Collect data about the current cache usage

Get the detailed data about how much cache your organization is currently using, broken down by individual workspaces.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import cache_usage_api
from gooddata_api_client.model.cache_usage_data import CacheUsageData
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = cache_usage_api.CacheUsageApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Collect data about the current cache usage
        api_response = api_instance.collect_cache_usage()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling CacheUsageApi->collect_cache_usage: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**CacheUsageData**](CacheUsageData.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


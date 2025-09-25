# gooddata_api_client.UsageApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**all_platform_usage**](UsageApi.md#all_platform_usage) | **GET** /api/v1/actions/collectUsage | Info about the platform usage.
[**particular_platform_usage**](UsageApi.md#particular_platform_usage) | **POST** /api/v1/actions/collectUsage | Info about the platform usage for particular items.


# **all_platform_usage**
> List[PlatformUsage] all_platform_usage()

Info about the platform usage.

Provides information about platform usage, like amount of users, workspaces, ...  _NOTE_: The `admin` user is always excluded from this amount.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.platform_usage import PlatformUsage
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
    api_instance = gooddata_api_client.UsageApi(api_client)

    try:
        # Info about the platform usage.
        api_response = api_instance.all_platform_usage()
        print("The response of UsageApi->all_platform_usage:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsageApi->all_platform_usage: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[PlatformUsage]**](PlatformUsage.md)

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

# **particular_platform_usage**
> List[PlatformUsage] particular_platform_usage(platform_usage_request)

Info about the platform usage for particular items.

Provides information about platform usage, like amount of users, workspaces, ...  _NOTE_: The `admin` user is always excluded from this amount.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.platform_usage import PlatformUsage
from gooddata_api_client.models.platform_usage_request import PlatformUsageRequest
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
    api_instance = gooddata_api_client.UsageApi(api_client)
    platform_usage_request = gooddata_api_client.PlatformUsageRequest() # PlatformUsageRequest | 

    try:
        # Info about the platform usage for particular items.
        api_response = api_instance.particular_platform_usage(platform_usage_request)
        print("The response of UsageApi->particular_platform_usage:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsageApi->particular_platform_usage: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **platform_usage_request** | [**PlatformUsageRequest**](PlatformUsageRequest.md)|  | 

### Return type

[**List[PlatformUsage]**](PlatformUsage.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


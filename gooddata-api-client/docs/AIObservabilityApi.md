# gooddata_api_client.AIObservabilityApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**reload_observability_layout**](AIObservabilityApi.md#reload_observability_layout) | **POST** /api/v1/actions/organization/reloadObservabilityLayout | Reload the managed AI observability layout


# **reload_observability_layout**
> reload_observability_layout()

Reload the managed AI observability layout

Re-applies the latest GoodData-managed AI observability layout to the organization. Requires the AI_OBSERVABILITY entitlement and organization MANAGE permission. Idempotent; customer-authored content is left untouched.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_observability_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ai_observability_api.AIObservabilityApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Reload the managed AI observability layout
        api_instance.reload_observability_layout()
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIObservabilityApi->reload_observability_layout: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


# gooddata_api_client.MetadataSynchronizationApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**sync_metadata**](MetadataSynchronizationApi.md#sync_metadata) | **POST** /api/v1/actions/organization/syncMetadata | Trigger metadata synchronization


# **sync_metadata**
> sync_metadata()

Trigger metadata synchronization

Enqueues an organization-scoped metadata resync, fanning out the organization's current metadata to GenAI, GW Forge, and Automations. Requires organization MANAGE permission. Requests are deduplicated while a resync session is pending for the organization.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import metadata_synchronization_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = metadata_synchronization_api.MetadataSynchronizationApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Trigger metadata synchronization
        api_instance.sync_metadata()
    except gooddata_api_client.ApiException as e:
        print("Exception when calling MetadataSynchronizationApi->sync_metadata: %s\n" % e)
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


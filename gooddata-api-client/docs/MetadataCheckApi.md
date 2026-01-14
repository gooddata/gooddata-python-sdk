# gooddata_api_client.MetadataCheckApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**metadata_check_organization**](MetadataCheckApi.md#metadata_check_organization) | **POST** /api/v1/actions/organization/metadataCheck | (BETA) Check Organization Metadata Inconsistencies


# **metadata_check_organization**
> metadata_check_organization()

(BETA) Check Organization Metadata Inconsistencies

(BETA) Temporary solution. Resyncs all organization objects and full workspaces within the organization with target GEN_AI_CHECK.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import metadata_check_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = metadata_check_api.MetadataCheckApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # (BETA) Check Organization Metadata Inconsistencies
        api_instance.metadata_check_organization()
    except gooddata_api_client.ApiException as e:
        print("Exception when calling MetadataCheckApi->metadata_check_organization: %s\n" % e)
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
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


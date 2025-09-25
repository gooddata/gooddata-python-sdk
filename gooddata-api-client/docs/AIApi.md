# gooddata_api_client.AIApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**metadata_sync**](AIApi.md#metadata_sync) | **POST** /api/v1/actions/workspaces/{workspaceId}/metadataSync | (BETA) Sync Metadata to other services
[**metadata_sync_organization**](AIApi.md#metadata_sync_organization) | **POST** /api/v1/actions/organization/metadataSync | (BETA) Sync organization scope Metadata to other services


# **metadata_sync**
> metadata_sync(workspace_id)

(BETA) Sync Metadata to other services

(BETA) Temporary solution. Later relevant metadata actions will trigger it in its scope only.

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
    api_instance = gooddata_api_client.AIApi(api_client)
    workspace_id = 'workspace_id_example' # str | 

    try:
        # (BETA) Sync Metadata to other services
        api_instance.metadata_sync(workspace_id)
    except Exception as e:
        print("Exception when calling AIApi->metadata_sync: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 

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

# **metadata_sync_organization**
> metadata_sync_organization()

(BETA) Sync organization scope Metadata to other services

(BETA) Temporary solution. Later relevant metadata actions will trigger sync in their scope only.

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
    api_instance = gooddata_api_client.AIApi(api_client)

    try:
        # (BETA) Sync organization scope Metadata to other services
        api_instance.metadata_sync_organization()
    except Exception as e:
        print("Exception when calling AIApi->metadata_sync_organization: %s\n" % e)
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


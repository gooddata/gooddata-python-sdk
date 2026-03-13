# gooddata_api_client.DataSourceFilesManifestReadApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**read_csv_file_manifests**](DataSourceFilesManifestReadApi.md#read_csv_file_manifests) | **POST** /api/v1/actions/fileStorage/dataSources/{dataSourceId}/readCsvFileManifests | Read CSV file manifests


# **read_csv_file_manifests**
> [ReadCsvFileManifestsResponse] read_csv_file_manifests(data_source_id, read_csv_file_manifests_request)

Read CSV file manifests

Read the manifests of the CSV files in the given data source.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_source_files_manifest_read_api
from gooddata_api_client.model.read_csv_file_manifests_response import ReadCsvFileManifestsResponse
from gooddata_api_client.model.read_csv_file_manifests_request import ReadCsvFileManifestsRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_source_files_manifest_read_api.DataSourceFilesManifestReadApi(api_client)
    data_source_id = "dataSourceId_example" # str | 
    read_csv_file_manifests_request = ReadCsvFileManifestsRequest(
        manifest_requests=[
            ReadCsvFileManifestsRequestItem(
                file_name="file_name_example",
                version=1,
            ),
        ],
    ) # ReadCsvFileManifestsRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Read CSV file manifests
        api_response = api_instance.read_csv_file_manifests(data_source_id, read_csv_file_manifests_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceFilesManifestReadApi->read_csv_file_manifests: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  |
 **read_csv_file_manifests_request** | [**ReadCsvFileManifestsRequest**](ReadCsvFileManifestsRequest.md)|  |

### Return type

[**[ReadCsvFileManifestsResponse]**](ReadCsvFileManifestsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful listing. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


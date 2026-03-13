# gooddata_api_client.DataSourceFilesListingApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**list_files**](DataSourceFilesListingApi.md#list_files) | **POST** /api/v1/actions/fileStorage/dataSources/{dataSourceId}/listFiles | List datasource files


# **list_files**
> [GdStorageFile] list_files(data_source_id)

List datasource files

List all the files in the given data source.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_source_files_listing_api
from gooddata_api_client.model.gd_storage_file import GdStorageFile
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_source_files_listing_api.DataSourceFilesListingApi(api_client)
    data_source_id = "dataSourceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # List datasource files
        api_response = api_instance.list_files(data_source_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceFilesListingApi->list_files: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  |

### Return type

[**[GdStorageFile]**](GdStorageFile.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful listing. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


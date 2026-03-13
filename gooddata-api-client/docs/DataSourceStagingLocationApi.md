# gooddata_api_client.DataSourceStagingLocationApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**staging_upload**](DataSourceStagingLocationApi.md#staging_upload) | **POST** /api/v1/actions/fileStorage/staging/upload | Upload a file to the staging area


# **staging_upload**
> UploadFileResponse staging_upload(file)

Upload a file to the staging area

Provides a location for uploading staging files.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_source_staging_location_api
from gooddata_api_client.model.upload_file_response import UploadFileResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_source_staging_location_api.DataSourceStagingLocationApi(api_client)
    file = open('/path/to/file', 'rb') # file_type | The file to upload.

    # example passing only required values which don't have defaults set
    try:
        # Upload a file to the staging area
        api_response = api_instance.staging_upload(file)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceStagingLocationApi->staging_upload: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **file_type**| The file to upload. |

### Return type

[**UploadFileResponse**](UploadFileResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Upload was successful. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


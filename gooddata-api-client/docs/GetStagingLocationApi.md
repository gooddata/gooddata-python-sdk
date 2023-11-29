# gooddata_api_client.GetStagingLocationApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_staging_upload_location**](GetStagingLocationApi.md#get_staging_upload_location) | **POST** /api/v1/actions/dataSources/{dataSourceId}/staging/upload | Get a staging upload location


# **get_staging_upload_location**
> StagingUploadLocation get_staging_upload_location(data_source_id)

Get a staging upload location

Provides a location for uploading staging files.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import get_staging_location_api
from gooddata_api_client.model.staging_upload_location import StagingUploadLocation
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = get_staging_location_api.GetStagingLocationApi(api_client)
    data_source_id = "dataSourceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get a staging upload location
        api_response = api_instance.get_staging_upload_location(data_source_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling GetStagingLocationApi->get_staging_upload_location: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  |

### Return type

[**StagingUploadLocation**](StagingUploadLocation.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Staging upload location was registered. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


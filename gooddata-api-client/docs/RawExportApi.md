# gooddata_api_client.RawExportApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_raw_export**](RawExportApi.md#create_raw_export) | **POST** /api/v1/actions/workspaces/{workspaceId}/export/raw | (EXPERIMENTAL) Create raw export request
[**get_raw_export**](RawExportApi.md#get_raw_export) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/raw/{exportId} | (EXPERIMENTAL) Retrieve exported files


# **create_raw_export**
> ExportResponse create_raw_export(workspace_id, raw_export_request)

(EXPERIMENTAL) Create raw export request

Note: This API is an experimental and is going to change. Please, use it accordingly.An raw export job will be created based on the export request and put to queue to be executed. The result of the operation will be an exportResult identifier that will be assembled by the client into a url that can be polled.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.export_response import ExportResponse
from gooddata_api_client.models.raw_export_request import RawExportRequest
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
    api_instance = gooddata_api_client.RawExportApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    raw_export_request = gooddata_api_client.RawExportRequest() # RawExportRequest | 

    try:
        # (EXPERIMENTAL) Create raw export request
        api_response = api_instance.create_raw_export(workspace_id, raw_export_request)
        print("The response of RawExportApi->create_raw_export:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RawExportApi->create_raw_export: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **raw_export_request** | [**RawExportRequest**](RawExportRequest.md)|  | 

### Return type

[**ExportResponse**](ExportResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Raw export request created successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_raw_export**
> bytearray get_raw_export(workspace_id, export_id)

(EXPERIMENTAL) Retrieve exported files

Note: This API is an experimental and is going to change. Please, use it accordingly.After clients creates a POST export request, the processing of it will start shortly asynchronously. To retrieve the result, client has to check periodically for the result on this endpoint. In case the result isn't ready yet, the service returns 202. If the result is ready, it returns 200 and octet stream of the result file with provided filename.

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
    api_instance = gooddata_api_client.RawExportApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    export_id = 'export_id_example' # str | 

    try:
        # (EXPERIMENTAL) Retrieve exported files
        api_response = api_instance.get_raw_export(workspace_id, export_id)
        print("The response of RawExportApi->get_raw_export:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RawExportApi->get_raw_export: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **export_id** | **str**|  | 

### Return type

**bytearray**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.apache.arrow.file, application/vnd.apache.arrow.stream, text/csv

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Binary export result. |  * Content-Disposition -  <br>  |
**202** | Request is accepted, provided exportId exists, but export is not yet ready. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


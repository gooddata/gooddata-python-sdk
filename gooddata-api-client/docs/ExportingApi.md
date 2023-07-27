# gooddata_api_client.ExportingApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_pdf_export**](ExportingApi.md#create_pdf_export) | **POST** /api/v1/actions/workspaces/{workspaceId}/export/visual | Create visual - pdf export request
[**get_exported_file**](ExportingApi.md#get_exported_file) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/visual/{exportId} | Retrieve exported files
[**get_metadata**](ExportingApi.md#get_metadata) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/visual/{exportId}/metadata | Retrieve metadata context


# **create_pdf_export**
> ExportResponse create_pdf_export(workspace_id, pdf_export_request)

Create visual - pdf export request

An visual export job will be created based on the export request and put to queue to be executed. The result of the operation will be an exportResult identifier that will be assembled by the client into a url that can be polled.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import exporting_api
from gooddata_api_client.model.export_response import ExportResponse
from gooddata_api_client.model.pdf_export_request import PdfExportRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = exporting_api.ExportingApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    pdf_export_request = PdfExportRequest(
        dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
        file_name="filename",
        metadata={},
    ) # PdfExportRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Create visual - pdf export request
        api_response = api_instance.create_pdf_export(workspace_id, pdf_export_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ExportingApi->create_pdf_export: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **pdf_export_request** | [**PdfExportRequest**](PdfExportRequest.md)|  |

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
**201** | Visual export request created successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_exported_file**
> get_exported_file(workspace_id, export_id)

Retrieve exported files

Returns 202 until original POST export request is not processed.Returns 200 with exported data once the export is done.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import exporting_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = exporting_api.ExportingApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    export_id = "exportId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Retrieve exported files
        api_instance.get_exported_file(workspace_id, export_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ExportingApi->get_exported_file: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **export_id** | **str**|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/pdf


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Binary export result. |  * Content-Disposition -  <br>  |
**202** | Request is accepted, provided exportId exists, but export is not yet ready. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_metadata**
> get_metadata(workspace_id, export_id)

Retrieve metadata context

This endpoints serves as a cache for user defined metadata for the front end ui to retrieve them, if one was created using the POST ../export/visual endpoint. The metadata structure is not verified. If metadata for given {exportId} has been found, endpoint returns the value 200 else 404.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import exporting_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = exporting_api.ExportingApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    export_id = "exportId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Retrieve metadata context
        api_instance.get_metadata(workspace_id, export_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ExportingApi->get_metadata: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **export_id** | **str**|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Json metadata representation |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


# gooddata_api_client.VisualExportApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_pdf_export**](VisualExportApi.md#create_pdf_export) | **POST** /api/v1/actions/workspaces/{workspaceId}/export/visual | Create visual - pdf export request
[**get_exported_file**](VisualExportApi.md#get_exported_file) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/visual/{exportId} | Retrieve exported files
[**get_metadata**](VisualExportApi.md#get_metadata) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/visual/{exportId}/metadata | Retrieve metadata context


# **create_pdf_export**
> ExportResponse create_pdf_export(workspace_id, visual_export_request, x_gdc_debug=x_gdc_debug)

Create visual - pdf export request

An visual export job will be created based on the export request and put to queue to be executed. The result of the operation will be an exportResult identifier that will be assembled by the client into a url that can be polled.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.export_response import ExportResponse
from gooddata_api_client.models.visual_export_request import VisualExportRequest
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
    api_instance = gooddata_api_client.VisualExportApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    visual_export_request = gooddata_api_client.VisualExportRequest() # VisualExportRequest | 
    x_gdc_debug = False # bool |  (optional) (default to False)

    try:
        # Create visual - pdf export request
        api_response = api_instance.create_pdf_export(workspace_id, visual_export_request, x_gdc_debug=x_gdc_debug)
        print("The response of VisualExportApi->create_pdf_export:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VisualExportApi->create_pdf_export: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **visual_export_request** | [**VisualExportRequest**](VisualExportRequest.md)|  | 
 **x_gdc_debug** | **bool**|  | [optional] [default to False]

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
> bytearray get_exported_file(workspace_id, export_id)

Retrieve exported files

Returns 202 until original POST export request is not processed.Returns 200 with exported data once the export is done.

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
    api_instance = gooddata_api_client.VisualExportApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    export_id = 'export_id_example' # str | 

    try:
        # Retrieve exported files
        api_response = api_instance.get_exported_file(workspace_id, export_id)
        print("The response of VisualExportApi->get_exported_file:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VisualExportApi->get_exported_file: %s\n" % e)
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

This endpoint serves as a cache for user-defined metadata of the export for the front end UI to retrieve it, if one was created using the POST ../export/visual endpoint. The metadata structure is not verified.

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
    api_instance = gooddata_api_client.VisualExportApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    export_id = 'export_id_example' # str | 

    try:
        # Retrieve metadata context
        api_instance.get_metadata(workspace_id, export_id)
    except Exception as e:
        print("Exception when calling VisualExportApi->get_metadata: %s\n" % e)
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


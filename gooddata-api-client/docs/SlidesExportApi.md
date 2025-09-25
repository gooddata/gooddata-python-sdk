# gooddata_api_client.SlidesExportApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_slides_export**](SlidesExportApi.md#create_slides_export) | **POST** /api/v1/actions/workspaces/{workspaceId}/export/slides | (EXPERIMENTAL) Create slides export request
[**get_slides_export**](SlidesExportApi.md#get_slides_export) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/slides/{exportId} | (EXPERIMENTAL) Retrieve exported files
[**get_slides_export_metadata**](SlidesExportApi.md#get_slides_export_metadata) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/slides/{exportId}/metadata | (EXPERIMENTAL) Retrieve metadata context


# **create_slides_export**
> ExportResponse create_slides_export(workspace_id, slides_export_request, x_gdc_debug=x_gdc_debug)

(EXPERIMENTAL) Create slides export request

Note: This API is an experimental and is going to change. Please, use it accordingly. A slides export job will be created based on the export request and put to queue to be executed. The result of the operation will be an exportResult identifier that will be assembled by the client into a url that can be polled.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.export_response import ExportResponse
from gooddata_api_client.models.slides_export_request import SlidesExportRequest
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
    api_instance = gooddata_api_client.SlidesExportApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    slides_export_request = gooddata_api_client.SlidesExportRequest() # SlidesExportRequest | 
    x_gdc_debug = False # bool |  (optional) (default to False)

    try:
        # (EXPERIMENTAL) Create slides export request
        api_response = api_instance.create_slides_export(workspace_id, slides_export_request, x_gdc_debug=x_gdc_debug)
        print("The response of SlidesExportApi->create_slides_export:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SlidesExportApi->create_slides_export: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **slides_export_request** | [**SlidesExportRequest**](SlidesExportRequest.md)|  | 
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
**201** | Slides export request created successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_slides_export**
> bytearray get_slides_export(workspace_id, export_id)

(EXPERIMENTAL) Retrieve exported files

Note: This API is an experimental and is going to change. Please, use it accordingly. After clients creates a POST export request, the processing of it will start shortly asynchronously. To retrieve the result, client has to check periodically for the result on this endpoint. In case the result isn't ready yet, the service returns 202. If the result is ready, it returns 200 and octet stream of the result file with provided filename.

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
    api_instance = gooddata_api_client.SlidesExportApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    export_id = 'export_id_example' # str | 

    try:
        # (EXPERIMENTAL) Retrieve exported files
        api_response = api_instance.get_slides_export(workspace_id, export_id)
        print("The response of SlidesExportApi->get_slides_export:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SlidesExportApi->get_slides_export: %s\n" % e)
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
 - **Accept**: application/pdf, application/vnd.openxmlformats-officedocument.presentationml.presentation

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Binary export result. |  * Content-Disposition -  <br>  |
**202** | Request is accepted, provided exportId exists, but export is not yet ready. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_slides_export_metadata**
> get_slides_export_metadata(workspace_id, export_id)

(EXPERIMENTAL) Retrieve metadata context

Note: This API is an experimental and is going to change. Please, use it accordingly. This endpoint serves as a cache for user-defined metadata of the export for the front end UI to retrieve it, if one was created using the POST ../export/slides endpoint. The metadata structure is not verified.

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
    api_instance = gooddata_api_client.SlidesExportApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    export_id = 'export_id_example' # str | 

    try:
        # (EXPERIMENTAL) Retrieve metadata context
        api_instance.get_slides_export_metadata(workspace_id, export_id)
    except Exception as e:
        print("Exception when calling SlidesExportApi->get_slides_export_metadata: %s\n" % e)
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


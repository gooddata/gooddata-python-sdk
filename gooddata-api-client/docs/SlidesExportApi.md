# gooddata_api_client.SlidesExportApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_slides_export**](SlidesExportApi.md#create_slides_export) | **POST** /api/v1/actions/workspaces/{workspaceId}/export/slides | (EXPERIMENTAL) Create slides export request
[**get_slides_export**](SlidesExportApi.md#get_slides_export) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/slides/{exportId} | (EXPERIMENTAL) Retrieve exported files
[**get_slides_export_metadata**](SlidesExportApi.md#get_slides_export_metadata) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/slides/{exportId}/metadata | (EXPERIMENTAL) Retrieve metadata context


# **create_slides_export**
> ExportResponse create_slides_export(workspace_id, slides_export_request)

(EXPERIMENTAL) Create slides export request

Note: This API is an experimental and is going to change. Please, use it accordingly. A slides export job will be created based on the export request and put to queue to be executed. The result of the operation will be an exportResult identifier that will be assembled by the client into a url that can be polled.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import slides_export_api
from gooddata_api_client.model.export_response import ExportResponse
from gooddata_api_client.model.slides_export_request import SlidesExportRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = slides_export_api.SlidesExportApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    slides_export_request = SlidesExportRequest(
        dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
        file_name="filename",
        format="PDF",
        metadata=JsonNode(),
        template_id="template_id_example",
        visualization_ids=[
            "visualization_ids_example",
        ],
        widget_ids=[
            "widget_ids_example",
        ],
    ) # SlidesExportRequest | 

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Create slides export request
        api_response = api_instance.create_slides_export(workspace_id, slides_export_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SlidesExportApi->create_slides_export: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **slides_export_request** | [**SlidesExportRequest**](SlidesExportRequest.md)|  |

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
> get_slides_export(workspace_id, export_id)

(EXPERIMENTAL) Retrieve exported files

Note: This API is an experimental and is going to change. Please, use it accordingly. After clients creates a POST export request, the processing of it will start shortly asynchronously. To retrieve the result, client has to check periodically for the result on this endpoint. In case the result isn't ready yet, the service returns 202. If the result is ready, it returns 200 and octet stream of the result file with provided filename.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import slides_export_api
from gooddata_api_client.model.get_image_export202_response_inner import GetImageExport202ResponseInner
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = slides_export_api.SlidesExportApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    export_id = "exportId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Retrieve exported files
        api_instance.get_slides_export(workspace_id, export_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SlidesExportApi->get_slides_export: %s\n" % e)
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
import time
import gooddata_api_client
from gooddata_api_client.api import slides_export_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = slides_export_api.SlidesExportApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    export_id = "exportId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Retrieve metadata context
        api_instance.get_slides_export_metadata(workspace_id, export_id)
    except gooddata_api_client.ApiException as e:
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


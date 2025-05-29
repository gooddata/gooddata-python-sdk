# gooddata_api_client.ImageExportApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_image_export**](ImageExportApi.md#create_image_export) | **POST** /api/v1/actions/workspaces/{workspaceId}/export/image | (EXPERIMENTAL) Create image export request
[**get_image_export**](ImageExportApi.md#get_image_export) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/image/{exportId} | (EXPERIMENTAL) Retrieve exported files
[**get_image_export_metadata**](ImageExportApi.md#get_image_export_metadata) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/image/{exportId}/metadata | (EXPERIMENTAL) Retrieve metadata context


# **create_image_export**
> ExportResponse create_image_export(workspace_id, image_export_request)

(EXPERIMENTAL) Create image export request

Note: This API is an experimental and is going to change. Please, use it accordingly. An image export job will be created based on the export request and put to queue to be executed. The result of the operation will be an exportResult identifier that will be assembled by the client into a url that can be polled.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import image_export_api
from gooddata_api_client.model.export_response import ExportResponse
from gooddata_api_client.model.image_export_request import ImageExportRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = image_export_api.ImageExportApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    image_export_request = ImageExportRequest(
        dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
        file_name="filename",
        format="PNG",
        metadata=JsonNode(),
        widget_ids=[
            "widget_ids_example",
        ],
    ) # ImageExportRequest | 

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Create image export request
        api_response = api_instance.create_image_export(workspace_id, image_export_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ImageExportApi->create_image_export: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **image_export_request** | [**ImageExportRequest**](ImageExportRequest.md)|  |

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
**201** | Image export request created successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_image_export**
> get_image_export(workspace_id, export_id)

(EXPERIMENTAL) Retrieve exported files

Note: This API is an experimental and is going to change. Please, use it accordingly. After clients creates a POST export request, the processing of it will start shortly asynchronously. To retrieve the result, client has to check periodically for the result on this endpoint. In case the result isn't ready yet, the service returns 202. If the result is ready, it returns 200 and octet stream of the result file with provided filename.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import image_export_api
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
    api_instance = image_export_api.ImageExportApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    export_id = "exportId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Retrieve exported files
        api_instance.get_image_export(workspace_id, export_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ImageExportApi->get_image_export: %s\n" % e)
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
 - **Accept**: image/png


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Binary export result. |  * Content-Disposition -  <br>  |
**202** | Request is accepted, provided exportId exists, but export is not yet ready. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_image_export_metadata**
> get_image_export_metadata(workspace_id, export_id)

(EXPERIMENTAL) Retrieve metadata context

Note: This API is an experimental and is going to change. Please, use it accordingly. This endpoint serves as a cache for user-defined metadata of the export for the front end UI to retrieve it, if one was created using the POST ../export/image endpoint. The metadata structure is not verified.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import image_export_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = image_export_api.ImageExportApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    export_id = "exportId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Retrieve metadata context
        api_instance.get_image_export_metadata(workspace_id, export_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ImageExportApi->get_image_export_metadata: %s\n" % e)
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


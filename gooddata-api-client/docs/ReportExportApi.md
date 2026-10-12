# gooddata_api_client.ReportExportApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_report_export**](ReportExportApi.md#create_report_export) | **POST** /api/v1/actions/workspaces/{workspaceId}/export/report | (EXPERIMENTAL) Create report export request
[**get_report_export**](ReportExportApi.md#get_report_export) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/report/{exportId} | (EXPERIMENTAL) Retrieve exported files
[**get_report_export_metadata**](ReportExportApi.md#get_report_export_metadata) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/report/{exportId}/metadata | (EXPERIMENTAL) Retrieve metadata context


# **create_report_export**
> ExportResponse create_report_export(workspace_id, report_export_request)

(EXPERIMENTAL) Create report export request

Note: This API is an experimental and is going to change. Please, use it accordingly. A report export job will be created based on the export request and put to queue to be executed. The result of the operation will be an exportResult identifier that will be assembled by the client into a url that can be polled.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import report_export_api
from gooddata_api_client.model.export_response import ExportResponse
from gooddata_api_client.model.report_export_request import ReportExportRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = report_export_api.ReportExportApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    report_export_request = ReportExportRequest(
        file_name="filename",
        format="PDF",
        metadata=JsonNode(),
        report_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
        timezone_id="Asia/Kolkata",
    ) # ReportExportRequest | 
    x_gdc_debug = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Create report export request
        api_response = api_instance.create_report_export(workspace_id, report_export_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ReportExportApi->create_report_export: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (EXPERIMENTAL) Create report export request
        api_response = api_instance.create_report_export(workspace_id, report_export_request, x_gdc_debug=x_gdc_debug)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ReportExportApi->create_report_export: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **report_export_request** | [**ReportExportRequest**](ReportExportRequest.md)|  |
 **x_gdc_debug** | **bool**|  | [optional] if omitted the server will use the default value of False

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
**201** | Report export request created successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_report_export**
> file_type get_report_export(workspace_id, export_id)

(EXPERIMENTAL) Retrieve exported files

Note: This API is an experimental and is going to change. Please, use it accordingly. After clients creates a POST export request, the processing of it will start shortly asynchronously. To retrieve the result, client has to check periodically for the result on this endpoint. In case the result isn't ready yet, the service returns 202. If the result is ready, it returns 200 and octet stream of the result file with provided filename.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import report_export_api
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
    api_instance = report_export_api.ReportExportApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    export_id = "exportId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Retrieve exported files
        api_response = api_instance.get_report_export(workspace_id, export_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ReportExportApi->get_report_export: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **export_id** | **str**|  |

### Return type

**file_type**

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

# **get_report_export_metadata**
> get_report_export_metadata(workspace_id, export_id)

(EXPERIMENTAL) Retrieve metadata context

Note: This API is an experimental and is going to change. Please, use it accordingly. This endpoint serves as a cache for user-defined metadata of the export for the front end UI to retrieve it, if one was created using the POST ../export/report endpoint. The metadata structure is not verified.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import report_export_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = report_export_api.ReportExportApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    export_id = "exportId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Retrieve metadata context
        api_instance.get_report_export_metadata(workspace_id, export_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ReportExportApi->get_report_export_metadata: %s\n" % e)
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


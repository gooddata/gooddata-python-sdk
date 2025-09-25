# gooddata_api_client.TabularExportApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_dashboard_export_request**](TabularExportApi.md#create_dashboard_export_request) | **POST** /api/v1/actions/workspaces/{workspaceId}/analyticalDashboards/{dashboardId}/export/tabular | (EXPERIMENTAL) Create dashboard tabular export request
[**create_tabular_export**](TabularExportApi.md#create_tabular_export) | **POST** /api/v1/actions/workspaces/{workspaceId}/export/tabular | Create tabular export request
[**get_tabular_export**](TabularExportApi.md#get_tabular_export) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/tabular/{exportId} | Retrieve exported files


# **create_dashboard_export_request**
> ExportResponse create_dashboard_export_request(workspace_id, dashboard_id, dashboard_tabular_export_request)

(EXPERIMENTAL) Create dashboard tabular export request

Note: This API is an experimental and is going to change. Please, use it accordingly.An tabular export job will be created based on the export request and put to queue to be executed. The result of the operation will be an exportResult identifier that will be assembled by the client into a url that can be polled.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.dashboard_tabular_export_request import DashboardTabularExportRequest
from gooddata_api_client.models.export_response import ExportResponse
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
    api_instance = gooddata_api_client.TabularExportApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    dashboard_id = 'dashboard_id_example' # str | 
    dashboard_tabular_export_request = gooddata_api_client.DashboardTabularExportRequest() # DashboardTabularExportRequest | 

    try:
        # (EXPERIMENTAL) Create dashboard tabular export request
        api_response = api_instance.create_dashboard_export_request(workspace_id, dashboard_id, dashboard_tabular_export_request)
        print("The response of TabularExportApi->create_dashboard_export_request:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TabularExportApi->create_dashboard_export_request: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **dashboard_id** | **str**|  | 
 **dashboard_tabular_export_request** | [**DashboardTabularExportRequest**](DashboardTabularExportRequest.md)|  | 

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
**201** | Tabular export request created successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_tabular_export**
> ExportResponse create_tabular_export(workspace_id, tabular_export_request)

Create tabular export request

An tabular export job will be created based on the export request and put to queue to be executed. The result of the operation will be an exportResult identifier that will be assembled by the client into a url that can be polled.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.export_response import ExportResponse
from gooddata_api_client.models.tabular_export_request import TabularExportRequest
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
    api_instance = gooddata_api_client.TabularExportApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    tabular_export_request = gooddata_api_client.TabularExportRequest() # TabularExportRequest | 

    try:
        # Create tabular export request
        api_response = api_instance.create_tabular_export(workspace_id, tabular_export_request)
        print("The response of TabularExportApi->create_tabular_export:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TabularExportApi->create_tabular_export: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **tabular_export_request** | [**TabularExportRequest**](TabularExportRequest.md)|  | 

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
**201** | Tabular export request created successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_tabular_export**
> bytearray get_tabular_export(workspace_id, export_id)

Retrieve exported files

After clients creates a POST export request, the processing of it will start shortly asynchronously. To retrieve the result, client has to check periodically for the result on this endpoint. In case the result isn't ready yet, the service returns 202. If the result is ready, it returns 200 and octet stream of the result file with provided filename.

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
    api_instance = gooddata_api_client.TabularExportApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    export_id = 'export_id_example' # str | 

    try:
        # Retrieve exported files
        api_response = api_instance.get_tabular_export(workspace_id, export_id)
        print("The response of TabularExportApi->get_tabular_export:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TabularExportApi->get_tabular_export: %s\n" % e)
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
 - **Accept**: application/pdf, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, text/csv, text/html

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Binary export result. |  * Content-Disposition -  <br>  |
**202** | Request is accepted, provided exportId exists, but export is not yet ready. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


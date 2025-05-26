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
import time
import gooddata_api_client
from gooddata_api_client.api import tabular_export_api
from gooddata_api_client.model.export_response import ExportResponse
from gooddata_api_client.model.dashboard_tabular_export_request import DashboardTabularExportRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = tabular_export_api.TabularExportApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    dashboard_id = "dashboardId_example" # str | 
    dashboard_tabular_export_request = DashboardTabularExportRequest(
        dashboard_filters_override=[
            DashboardTabularExportRequestDashboardFiltersOverrideInner(None),
        ],
        file_name="result",
        format="XLSX",
    ) # DashboardTabularExportRequest | 

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Create dashboard tabular export request
        api_response = api_instance.create_dashboard_export_request(workspace_id, dashboard_id, dashboard_tabular_export_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import tabular_export_api
from gooddata_api_client.model.export_response import ExportResponse
from gooddata_api_client.model.tabular_export_request import TabularExportRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = tabular_export_api.TabularExportApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    tabular_export_request = TabularExportRequest(
        custom_override=CustomOverride(
            labels={
                "key": CustomLabel(
                    title="title_example",
                ),
            },
            metrics={
                "key": CustomMetric(
                    format="format_example",
                    title="title_example",
                ),
            },
        ),
        execution_result="ff483727196c9dc862c7fd3a5a84df55c96d61a4",
        file_name="result",
        format="CSV",
        metadata=JsonNode(),
        related_dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
        settings=Settings(
            merge_headers=True,
            pdf_page_size="a4 landscape",
            pdf_table_style=[
                PdfTableStyle(
                    properties=[
                        PdfTableStyleProperty(
                            key="key_example",
                            value="value_example",
                        ),
                    ],
                    selector="selector_example",
                ),
            ],
            pdf_top_left_content="Good",
            pdf_top_right_content="Morning",
            show_filters=False,
        ),
        visualization_object="f7c359bc-c230-4487-b15b-ad9685bcb537",
        visualization_object_custom_filters=[
            {},
        ],
    ) # TabularExportRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Create tabular export request
        api_response = api_instance.create_tabular_export(workspace_id, tabular_export_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
> get_tabular_export(workspace_id, export_id)

Retrieve exported files

After clients creates a POST export request, the processing of it will start shortly asynchronously. To retrieve the result, client has to check periodically for the result on this endpoint. In case the result isn't ready yet, the service returns 202. If the result is ready, it returns 200 and octet stream of the result file with provided filename.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import tabular_export_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = tabular_export_api.TabularExportApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    export_id = "exportId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Retrieve exported files
        api_instance.get_tabular_export(workspace_id, export_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling TabularExportApi->get_tabular_export: %s\n" % e)
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
 - **Accept**: application/pdf, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, text/csv, text/html


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Binary export result. |  * Content-Disposition -  <br>  |
**202** | Request is accepted, provided exportId exists, but export is not yet ready. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


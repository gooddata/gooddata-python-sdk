<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.tabular_export_api.TabularExportApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_dashboard_export_request**](#create_dashboard_export_request) | **post** /api/v1/actions/workspaces/{workspaceId}/analyticalDashboards/{dashboardId}/export/tabular | (EXPERIMENTAL) Create dashboard tabular export request
[**create_tabular_export**](#create_tabular_export) | **post** /api/v1/actions/workspaces/{workspaceId}/export/tabular | Create tabular export request
[**get_tabular_export**](#get_tabular_export) | **get** /api/v1/actions/workspaces/{workspaceId}/export/tabular/{exportId} | Retrieve exported files

# **create_dashboard_export_request**
<a id="create_dashboard_export_request"></a>
> ExportResponse create_dashboard_export_request(workspace_iddashboard_iddashboard_tabular_export_request)

(EXPERIMENTAL) Create dashboard tabular export request

Note: This API is an experimental and is going to change. Please, use it accordingly.An tabular export job will be created based on the export request and put to queue to be executed. The result of the operation will be an exportResult identifier that will be assembled by the client into a url that can be polled.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import tabular_export_api
from gooddata_api_client.model.export_response import ExportResponse
from gooddata_api_client.model.dashboard_tabular_export_request import DashboardTabularExportRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tabular_export_api.TabularExportApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
        'dashboardId': "dashboardId_example",
    }
    body = DashboardTabularExportRequest(
        dashboard_filters_override=[
            DashboardFilter()
        ],
        dashboard_tabs_filters_overrides=dict(
            "key": [
                DashboardFilter()
            ],
        ),
        file_name="result",
        format="XLSX",
        settings=DashboardExportSettings(
            export_info=True,
            merge_headers=True,
            page_orientation="PORTRAIT",
            page_size="A4",
        ),
        widget_ids=[
            "widget_ids_example"
        ],
    )
    try:
        # (EXPERIMENTAL) Create dashboard tabular export request
        api_response = api_instance.create_dashboard_export_request(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling TabularExportApi->create_dashboard_export_request: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DashboardTabularExportRequest**](../../models/DashboardTabularExportRequest.md) |  | 


### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 
dashboardId | DashboardIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# DashboardIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#create_dashboard_export_request.ApiResponseFor201) | Tabular export request created successfully.

#### create_dashboard_export_request.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ExportResponse**](../../models/ExportResponse.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **create_tabular_export**
<a id="create_tabular_export"></a>
> ExportResponse create_tabular_export(workspace_idtabular_export_request)

Create tabular export request

An tabular export job will be created based on the export request and put to queue to be executed. The result of the operation will be an exportResult identifier that will be assembled by the client into a url that can be polled.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import tabular_export_api
from gooddata_api_client.model.export_response import ExportResponse
from gooddata_api_client.model.tabular_export_request import TabularExportRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tabular_export_api.TabularExportApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    body = TabularExportRequest(
        custom_override=CustomOverride(
            labels=dict(
                "key": CustomLabel(
                    title="title_example",
                ),
            ),
            metrics=dict(
                "key": CustomMetric(
                    format="format_example",
                    title="title_example",
                ),
            ),
        ),
        execution_result="ff483727196c9dc862c7fd3a5a84df55c96d61a4",
        file_name="result",
        format="CSV",
        metadata=JsonNode(),
        related_dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
        settings=Settings(
            delimiter="U",
            export_info=True,
            merge_headers=True,
            page_orientation="PORTRAIT",
            page_size="A4",
            pdf_page_size="a4 landscape",
            pdf_table_style=[{"properties":[{"key":"font-size","value":"30px"}],"selector":"th"}],
            pdf_top_left_content="Good",
            pdf_top_right_content="Morning",
            show_filters=False,
        ),
        visualization_object="f7c359bc-c230-4487-b15b-ad9685bcb537",
        visualization_object_custom_filters=[
            dict()
        ],
    )
    try:
        # Create tabular export request
        api_response = api_instance.create_tabular_export(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling TabularExportApi->create_tabular_export: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**TabularExportRequest**](../../models/TabularExportRequest.md) |  | 


### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#create_tabular_export.ApiResponseFor201) | Tabular export request created successfully.

#### create_tabular_export.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ExportResponse**](../../models/ExportResponse.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_tabular_export**
<a id="get_tabular_export"></a>
> file_type get_tabular_export(workspace_idexport_id)

Retrieve exported files

After clients creates a POST export request, the processing of it will start shortly asynchronously. To retrieve the result, client has to check periodically for the result on this endpoint. In case the result isn't ready yet, the service returns 202. If the result is ready, it returns 200 and octet stream of the result file with provided filename.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import tabular_export_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tabular_export_api.TabularExportApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
        'exportId': "exportId_example",
    }
    try:
        # Retrieve exported files
        api_response = api_instance.get_tabular_export(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling TabularExportApi->get_tabular_export: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/pdf', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/zip', 'text/csv', 'text/html', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 
exportId | ExportIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# ExportIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_tabular_export.ApiResponseFor200) | Binary export result.
202 | [ApiResponseFor202](#get_tabular_export.ApiResponseFor202) | Request is accepted, provided exportId exists, but export is not yet ready.

#### get_tabular_export.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationPdf, SchemaFor200ResponseBodyApplicationVndOpenxmlformatsOfficedocumentSpreadsheetmlSheet, SchemaFor200ResponseBodyApplicationZip, SchemaFor200ResponseBodyTextCsv, SchemaFor200ResponseBodyTextHtml, ] |  |
headers | ResponseHeadersFor200 |  |

# SchemaFor200ResponseBodyApplicationPdf

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bytes, io.FileIO, io.BufferedReader,  | bytes, FileIO,  |  | 

# SchemaFor200ResponseBodyApplicationVndOpenxmlformatsOfficedocumentSpreadsheetmlSheet

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bytes, io.FileIO, io.BufferedReader,  | bytes, FileIO,  |  | 

# SchemaFor200ResponseBodyApplicationZip

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bytes, io.FileIO, io.BufferedReader,  | bytes, FileIO,  |  | 

# SchemaFor200ResponseBodyTextCsv

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bytes, io.FileIO, io.BufferedReader,  | bytes, FileIO,  |  | 

# SchemaFor200ResponseBodyTextHtml

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bytes, io.FileIO, io.BufferedReader,  | bytes, FileIO,  |  | 
#### ResponseHeadersFor200

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
Content-Disposition | ContentDispositionSchema | | optional

# ContentDispositionSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 


#### get_tabular_export.ApiResponseFor202
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor202ResponseBodyApplicationPdf, SchemaFor202ResponseBodyApplicationVndOpenxmlformatsOfficedocumentSpreadsheetmlSheet, SchemaFor202ResponseBodyApplicationZip, SchemaFor202ResponseBodyTextCsv, SchemaFor202ResponseBodyTextHtml, ] |  |
headers | Unset | headers were not defined |

# SchemaFor202ResponseBodyApplicationPdf

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bytes, io.FileIO, io.BufferedReader,  | bytes, FileIO,  |  | 

# SchemaFor202ResponseBodyApplicationVndOpenxmlformatsOfficedocumentSpreadsheetmlSheet

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bytes, io.FileIO, io.BufferedReader,  | bytes, FileIO,  |  | 

# SchemaFor202ResponseBodyApplicationZip

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bytes, io.FileIO, io.BufferedReader,  | bytes, FileIO,  |  | 

# SchemaFor202ResponseBodyTextCsv

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bytes, io.FileIO, io.BufferedReader,  | bytes, FileIO,  |  | 

# SchemaFor202ResponseBodyTextHtml

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bytes, io.FileIO, io.BufferedReader,  | bytes, FileIO,  |  | 

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


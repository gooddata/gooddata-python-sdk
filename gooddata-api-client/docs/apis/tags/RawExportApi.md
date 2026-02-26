<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.raw_export_api.RawExportApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_raw_export**](#create_raw_export) | **post** /api/v1/actions/workspaces/{workspaceId}/export/raw | (EXPERIMENTAL) Create raw export request
[**get_raw_export**](#get_raw_export) | **get** /api/v1/actions/workspaces/{workspaceId}/export/raw/{exportId} | (EXPERIMENTAL) Retrieve exported files

# **create_raw_export**
<a id="create_raw_export"></a>
> ExportResponse create_raw_export(workspace_idraw_export_request)

(EXPERIMENTAL) Create raw export request

Note: This API is an experimental and is going to change. Please, use it accordingly.An raw export job will be created based on the export request and put to queue to be executed. The result of the operation will be an exportResult identifier that will be assembled by the client into a url that can be polled.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import raw_export_api
from gooddata_api_client.model.export_response import ExportResponse
from gooddata_api_client.model.raw_export_request import RawExportRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = raw_export_api.RawExportApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    body = RawExportRequest(
        custom_override=RawCustomOverride(
            labels=dict(
                "key": RawCustomLabel(
                    title="title_example",
                ),
            ),
            metrics=dict(
                "key": RawCustomMetric(
                    title="title_example",
                ),
            ),
        ),
        delimiter="U",
        execution=AFM(
            attributes=[
                AttributeItem(
                    label=AfmObjectIdentifierLabel(
                        identifier=dict(
                            id="sample_item.price",
                            type="label",
                        ),
                    ),
                    local_identifier="attribute_1",
                    show_all_values=False,
                )
            ],
            aux_measures=[
                MeasureItem(
                    definition=MeasureDefinition(),
                    local_identifier="metric_1",
                )
            ],
            filters=[
                FilterDefinition()
            ],
            measure_definition_overrides=[
                MetricDefinitionOverride(
                    definition=InlineMeasureDefinition(
                        inline=dict(
                            maql="maql_example",
                        ),
                    ),
                    item=AfmObjectIdentifierCore(
                        identifier=dict(
                            id="sample_item.price",
                            type="attribute",
                        ),
                    ),
                )
            ],
            measures=[
                MeasureItem()
            ],
        ),
        execution_settings=ExecutionSettings(
            data_sampling_percentage=0,
            timestamp="1970-01-01T00:00:00.00Z",
        ),
        file_name="result",
        format="CSV",
    )
    try:
        # (EXPERIMENTAL) Create raw export request
        api_response = api_instance.create_raw_export(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling RawExportApi->create_raw_export: %s\n" % e)
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
[**RawExportRequest**](../../models/RawExportRequest.md) |  | 


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
201 | [ApiResponseFor201](#create_raw_export.ApiResponseFor201) | Raw export request created successfully.

#### create_raw_export.ApiResponseFor201
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

# **get_raw_export**
<a id="get_raw_export"></a>
> file_type get_raw_export(workspace_idexport_id)

(EXPERIMENTAL) Retrieve exported files

Note: This API is an experimental and is going to change. Please, use it accordingly.After clients creates a POST export request, the processing of it will start shortly asynchronously. To retrieve the result, client has to check periodically for the result on this endpoint. In case the result isn't ready yet, the service returns 202. If the result is ready, it returns 200 and octet stream of the result file with provided filename.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import raw_export_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = raw_export_api.RawExportApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
        'exportId': "exportId_example",
    }
    try:
        # (EXPERIMENTAL) Retrieve exported files
        api_response = api_instance.get_raw_export(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling RawExportApi->get_raw_export: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.apache.arrow.file', 'application/vnd.apache.arrow.stream', 'text/csv', ) | Tells the server the content type(s) that are accepted by the client
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
200 | [ApiResponseFor200](#get_raw_export.ApiResponseFor200) | Binary export result.
202 | [ApiResponseFor202](#get_raw_export.ApiResponseFor202) | Request is accepted, provided exportId exists, but export is not yet ready.

#### get_raw_export.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndApacheArrowFile, SchemaFor200ResponseBodyApplicationVndApacheArrowStream, SchemaFor200ResponseBodyTextCsv, ] |  |
headers | ResponseHeadersFor200 |  |

# SchemaFor200ResponseBodyApplicationVndApacheArrowFile

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bytes, io.FileIO, io.BufferedReader,  | bytes, FileIO,  |  | 

# SchemaFor200ResponseBodyApplicationVndApacheArrowStream

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bytes, io.FileIO, io.BufferedReader,  | bytes, FileIO,  |  | 

# SchemaFor200ResponseBodyTextCsv

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


#### get_raw_export.ApiResponseFor202
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor202ResponseBodyApplicationVndApacheArrowFile, SchemaFor202ResponseBodyApplicationVndApacheArrowStream, SchemaFor202ResponseBodyTextCsv, ] |  |
headers | Unset | headers were not defined |

# SchemaFor202ResponseBodyApplicationVndApacheArrowFile

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bytes, io.FileIO, io.BufferedReader,  | bytes, FileIO,  |  | 

# SchemaFor202ResponseBodyApplicationVndApacheArrowStream

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bytes, io.FileIO, io.BufferedReader,  | bytes, FileIO,  |  | 

# SchemaFor202ResponseBodyTextCsv

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bytes, io.FileIO, io.BufferedReader,  | bytes, FileIO,  |  | 

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


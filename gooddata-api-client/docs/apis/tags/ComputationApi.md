<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.computation_api.ComputationApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**compute_label_elements_post**](#compute_label_elements_post) | **post** /api/v1/actions/workspaces/{workspaceId}/execution/collectLabelElements | Listing of label values. The resulting data are limited by the static platform limit to the maximum of 10000 rows.
[**compute_report**](#compute_report) | **post** /api/v1/actions/workspaces/{workspaceId}/execution/afm/execute | Executes analytical request and returns link to the result
[**compute_valid_objects**](#compute_valid_objects) | **post** /api/v1/actions/workspaces/{workspaceId}/execution/afm/computeValidObjects | Valid objects
[**create_tabular_export**](#create_tabular_export) | **post** /api/v1/actions/workspaces/{workspaceId}/export/tabular | Create tabular export request
[**explain_afm**](#explain_afm) | **post** /api/v1/actions/workspaces/{workspaceId}/execution/afm/explain | AFM explain resource.
[**get_tabular_export**](#get_tabular_export) | **get** /api/v1/actions/workspaces/{workspaceId}/export/tabular/{exportId} | Retrieve exported files
[**retrieve_execution_metadata**](#retrieve_execution_metadata) | **get** /api/v1/actions/workspaces/{workspaceId}/execution/afm/execute/result/{resultId}/metadata | Get a single execution result&#x27;s metadata.
[**retrieve_result**](#retrieve_result) | **get** /api/v1/actions/workspaces/{workspaceId}/execution/afm/execute/result/{resultId} | Get a single execution result

# **compute_label_elements_post**
<a id="compute_label_elements_post"></a>
> ElementsResponse compute_label_elements_post(workspace_idelements_request)

Listing of label values. The resulting data are limited by the static platform limit to the maximum of 10000 rows.

Returns paged list of elements (values) of given label satisfying given filtering criteria.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import computation_api
from gooddata_api_client.model.elements_request import ElementsRequest
from gooddata_api_client.model.elements_response import ElementsResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = computation_api.ComputationApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    header_params = {
    }
    body = ElementsRequest(
        complement_filter=False,
        data_sampling_percentage=100,
        exact_filter=[
            "exact_filter_example"
        ],
        exclude_primary_label=False,
        filter_by=FilterBy(
            label_type="REQUESTED",
        ),
        label="/6bUUGjjNSwg0_bs",
        pattern_filter="pattern_filter_example",
        sort_order="ASC",
    )
    try:
        # Listing of label values. The resulting data are limited by the static platform limit to the maximum of 10000 rows.
        api_response = api_instance.compute_label_elements_post(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputationApi->compute_label_elements_post: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'offset': 0,
        'limit': 1000,
    }
    header_params = {
        'skip-cache': False,
    }
    body = ElementsRequest(
        complement_filter=False,
        data_sampling_percentage=100,
        exact_filter=[
            "exact_filter_example"
        ],
        exclude_primary_label=False,
        filter_by=FilterBy(
            label_type="REQUESTED",
        ),
        label="/6bUUGjjNSwg0_bs",
        pattern_filter="pattern_filter_example",
        sort_order="ASC",
    )
    try:
        # Listing of label values. The resulting data are limited by the static platform limit to the maximum of 10000 rows.
        api_response = api_instance.compute_label_elements_post(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputationApi->compute_label_elements_post: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
query_params | RequestQueryParams | |
header_params | RequestHeaderParams | |
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
[**ElementsRequest**](../../models/ElementsRequest.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
offset | OffsetSchema | | optional
limit | LimitSchema | | optional


# OffsetSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 0value must be a 32 bit integer

# LimitSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 1000value must be a 32 bit integer

### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
skip-cache | SkipCacheSchema | | optional

# SkipCacheSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bool,  | BoolClass,  |  | if omitted the server will use the default value of False

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
200 | [ApiResponseFor200](#compute_label_elements_post.ApiResponseFor200) | List of label values.

#### compute_label_elements_post.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ElementsResponse**](../../models/ElementsResponse.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **compute_report**
<a id="compute_report"></a>
> AfmExecutionResponse compute_report(workspace_idafm_execution)

Executes analytical request and returns link to the result

AFM is a combination of attributes, measures and filters that describe a query you want to execute.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import computation_api
from gooddata_api_client.model.afm_execution_response import AfmExecutionResponse
from gooddata_api_client.model.afm_execution import AfmExecution
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = computation_api.ComputationApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
    }
    header_params = {
    }
    body = AfmExecution(
        execution=AFM(
            attributes=[
                AttributeItem(
                    label=AfmObjectIdentifierLabel(
                        identifier=dict(
                            id="sample_item.price",
                            type="label",
                        ),
                    ),
                    local_identifier="2",
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
            measures=[
                MeasureItem()
            ],
        ),
        result_spec=ResultSpec(
            dimensions=[
                Dimension(
                    item_identifiers=["attribute_1","measureGroup"],
                    local_identifier="firstDimension",
                    sorting=[
                        SortKey()
                    ],
                )
            ],
            totals=[
                Total(
                    function="SUM",
                    local_identifier="firstTotal",
                    metric="metric_1",
                    total_dimensions=[
                        TotalDimension(
                            dimension_identifier="firstDimension",
                            total_dimension_items=["measureGroup"],
                        )
                    ],
                )
            ],
        ),
        settings=ExecutionSettings(
            data_sampling_percentage=0,
        ),
    )
    try:
        # Executes analytical request and returns link to the result
        api_response = api_instance.compute_report(
            path_params=path_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputationApi->compute_report: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
    }
    header_params = {
        'skip-cache': False,
        'timestamp': "2020-06-03T10:15:30+01:00",
    }
    body = AfmExecution(
        execution=AFM(
            attributes=[
                AttributeItem(
                    label=AfmObjectIdentifierLabel(
                        identifier=dict(
                            id="sample_item.price",
                            type="label",
                        ),
                    ),
                    local_identifier="2",
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
            measures=[
                MeasureItem()
            ],
        ),
        result_spec=ResultSpec(
            dimensions=[
                Dimension(
                    item_identifiers=["attribute_1","measureGroup"],
                    local_identifier="firstDimension",
                    sorting=[
                        SortKey()
                    ],
                )
            ],
            totals=[
                Total(
                    function="SUM",
                    local_identifier="firstTotal",
                    metric="metric_1",
                    total_dimensions=[
                        TotalDimension(
                            dimension_identifier="firstDimension",
                            total_dimension_items=["measureGroup"],
                        )
                    ],
                )
            ],
        ),
        settings=ExecutionSettings(
            data_sampling_percentage=0,
        ),
    )
    try:
        # Executes analytical request and returns link to the result
        api_response = api_instance.compute_report(
            path_params=path_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputationApi->compute_report: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
header_params | RequestHeaderParams | |
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
[**AfmExecution**](../../models/AfmExecution.md) |  | 


### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
skip-cache | SkipCacheSchema | | optional
timestamp | TimestampSchema | | optional

# SkipCacheSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bool,  | BoolClass,  |  | if omitted the server will use the default value of False

# TimestampSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

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
200 | [ApiResponseFor200](#compute_report.ApiResponseFor200) | AFM Execution response with links to the result and server-enhanced dimensions from the original request.

#### compute_report.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**AfmExecutionResponse**](../../models/AfmExecutionResponse.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **compute_valid_objects**
<a id="compute_valid_objects"></a>
> AfmValidObjectsResponse compute_valid_objects(workspace_idafm_valid_objects_query)

Valid objects

Returns list containing attributes, facts, or metrics, which can be added to given AFM while still keeping it computable.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import computation_api
from gooddata_api_client.model.afm_valid_objects_query import AfmValidObjectsQuery
from gooddata_api_client.model.afm_valid_objects_response import AfmValidObjectsResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = computation_api.ComputationApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
    }
    body = AfmValidObjectsQuery(
        afm=AFM(
            attributes=[
                AttributeItem(
                    label=AfmObjectIdentifierLabel(
                        identifier=dict(
                            id="sample_item.price",
                            type="label",
                        ),
                    ),
                    local_identifier="2",
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
            measures=[
                MeasureItem()
            ],
        ),
        types=[
            "facts"
        ],
    )
    try:
        # Valid objects
        api_response = api_instance.compute_valid_objects(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputationApi->compute_valid_objects: %s\n" % e)
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
[**AfmValidObjectsQuery**](../../models/AfmValidObjectsQuery.md) |  | 


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
200 | [ApiResponseFor200](#compute_valid_objects.ApiResponseFor200) | List of attributes, facts and metrics valid with respect to given AFM.

#### compute_valid_objects.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**AfmValidObjectsResponse**](../../models/AfmValidObjectsResponse.md) |  | 


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
from gooddata_api_client.apis.tags import computation_api
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
    api_instance = computation_api.ComputationApi(api_client)

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
        settings=Settings(
            merge_headers=True,
            show_filters=False,
        ),
    )
    try:
        # Create tabular export request
        api_response = api_instance.create_tabular_export(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputationApi->create_tabular_export: %s\n" % e)
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

# **explain_afm**
<a id="explain_afm"></a>
> explain_afm(workspace_idafm_execution)

AFM explain resource.

The resource provides static structures needed for investigation of a problem with given AFM.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import computation_api
from gooddata_api_client.model.afm_execution import AfmExecution
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = computation_api.ComputationApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = AfmExecution(
        execution=AFM(
            attributes=[
                AttributeItem(
                    label=AfmObjectIdentifierLabel(
                        identifier=dict(
                            id="sample_item.price",
                            type="label",
                        ),
                    ),
                    local_identifier="2",
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
            measures=[
                MeasureItem()
            ],
        ),
        result_spec=ResultSpec(
            dimensions=[
                Dimension(
                    item_identifiers=["attribute_1","measureGroup"],
                    local_identifier="firstDimension",
                    sorting=[
                        SortKey()
                    ],
                )
            ],
            totals=[
                Total(
                    function="SUM",
                    local_identifier="firstTotal",
                    metric="metric_1",
                    total_dimensions=[
                        TotalDimension(
                            dimension_identifier="firstDimension",
                            total_dimension_items=["measureGroup"],
                        )
                    ],
                )
            ],
        ),
        settings=ExecutionSettings(
            data_sampling_percentage=0,
        ),
    )
    try:
        # AFM explain resource.
        api_response = api_instance.explain_afm(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputationApi->explain_afm: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'explainType': "MAQL",
    }
    body = AfmExecution(
        execution=AFM(
            attributes=[
                AttributeItem(
                    label=AfmObjectIdentifierLabel(
                        identifier=dict(
                            id="sample_item.price",
                            type="label",
                        ),
                    ),
                    local_identifier="2",
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
            measures=[
                MeasureItem()
            ],
        ),
        result_spec=ResultSpec(
            dimensions=[
                Dimension(
                    item_identifiers=["attribute_1","measureGroup"],
                    local_identifier="firstDimension",
                    sorting=[
                        SortKey()
                    ],
                )
            ],
            totals=[
                Total(
                    function="SUM",
                    local_identifier="firstTotal",
                    metric="metric_1",
                    total_dimensions=[
                        TotalDimension(
                            dimension_identifier="firstDimension",
                            total_dimension_items=["measureGroup"],
                        )
                    ],
                )
            ],
        ),
        settings=ExecutionSettings(
            data_sampling_percentage=0,
        ),
    )
    try:
        # AFM explain resource.
        api_response = api_instance.explain_afm(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputationApi->explain_afm: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/sql', 'application/zip', 'image/svg+xml', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**AfmExecution**](../../models/AfmExecution.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
explainType | ExplainTypeSchema | | optional


# ExplainTypeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | must be one of ["MAQL", "GRPC_MODEL", "GRPC_MODEL_SVG", "WDF", "QT", "QT_SVG", "OPT_QT", "OPT_QT_SVG", "SQL", "SETTINGS", ] 

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
200 | [ApiResponseFor200](#explain_afm.ApiResponseFor200) | Requested resource

#### explain_afm.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[Unset, Unset, SchemaFor200ResponseBodyApplicationZip, Unset, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationZip

ZIP with MAQL, GRPC_MODEL, GRPC_MODEL_SVG, WDF, QT, QT_SVG, OPT_QT, OPT_QT_SVG and SQL files

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bytes, io.FileIO, io.BufferedReader,  | bytes, FileIO,  | ZIP with MAQL, GRPC_MODEL, GRPC_MODEL_SVG, WDF, QT, QT_SVG, OPT_QT, OPT_QT_SVG and SQL files | 

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_tabular_export**
<a id="get_tabular_export"></a>
> get_tabular_export(workspace_idexport_id)

Retrieve exported files

After clients creates a POST export request, the processing of it will start shortly asynchronously. To retrieve the result, client has to check periodically for the result on this endpoint. In case the result isn't ready yet, the service returns 202. If the result is ready, it returns 200 and octet stream of the result file with provided filename.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import computation_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = computation_api.ComputationApi(api_client)

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
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputationApi->get_tabular_export: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'text/csv', ) | Tells the server the content type(s) that are accepted by the client
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
body | typing.Union[Unset, Unset, ] |  |
headers | ResponseHeadersFor200 |  |
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
body | typing.Union[SchemaFor202ResponseBodyApplicationVndOpenxmlformatsOfficedocumentSpreadsheetmlSheet, SchemaFor202ResponseBodyTextCsv, ] |  |
headers | Unset | headers were not defined |

# SchemaFor202ResponseBodyApplicationVndOpenxmlformatsOfficedocumentSpreadsheetmlSheet

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

# **retrieve_execution_metadata**
<a id="retrieve_execution_metadata"></a>
> ResultCacheMetadata retrieve_execution_metadata(workspace_idresult_id)

Get a single execution result's metadata.

The resource provides execution result's metadata as AFM and resultSpec used in execution request and an executionResponse

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import computation_api
from gooddata_api_client.model.result_cache_metadata import ResultCacheMetadata
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = computation_api.ComputationApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
        'resultId': "a9b28f9dc55f37ea9f4a5fb0c76895923591e781",
    }
    try:
        # Get a single execution result's metadata.
        api_response = api_instance.retrieve_execution_metadata(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputationApi->retrieve_execution_metadata: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 
resultId | ResultIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# ResultIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#retrieve_execution_metadata.ApiResponseFor200) | Execution result&#x27;s metadata was found and returned.

#### retrieve_execution_metadata.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ResultCacheMetadata**](../../models/ResultCacheMetadata.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **retrieve_result**
<a id="retrieve_result"></a>
> ExecutionResult retrieve_result(workspace_idresult_id)

Get a single execution result

Gets a single execution result.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import computation_api
from gooddata_api_client.model.execution_result import ExecutionResult
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = computation_api.ComputationApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
        'resultId': "a9b28f9dc55f37ea9f4a5fb0c76895923591e781",
    }
    query_params = {
    }
    try:
        # Get a single execution result
        api_response = api_instance.retrieve_result(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputationApi->retrieve_result: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
        'resultId': "a9b28f9dc55f37ea9f4a5fb0c76895923591e781",
    }
    query_params = {
        'offset': [
        offset=1,10
    ],
        'limit': [
        limit=1,10
    ],
        'excludedTotalDimensions': [
        "excludedTotalDimensions=dim_0,dim_1"
    ],
    }
    try:
        # Get a single execution result
        api_response = api_instance.retrieve_result(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputationApi->retrieve_result: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
offset | OffsetSchema | | optional
limit | LimitSchema | | optional
excludedTotalDimensions | ExcludedTotalDimensionsSchema | | optional


# OffsetSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | decimal.Decimal, int,  | decimal.Decimal,  |  | value must be a 32 bit integer

# LimitSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | decimal.Decimal, int,  | decimal.Decimal,  |  | value must be a 32 bit integer

# ExcludedTotalDimensionsSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 
resultId | ResultIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# ResultIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#retrieve_result.ApiResponseFor200) | Execution result was found and returned.

#### retrieve_result.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ExecutionResult**](../../models/ExecutionResult.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


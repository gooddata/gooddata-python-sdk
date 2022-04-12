# gooddata_afm_client.ActionsApi

All URIs are relative to *http://gooddata-cn-ce:3000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**compute_label_elements_post**](ActionsApi.md#compute_label_elements_post) | **POST** /api/actions/workspaces/{workspaceId}/execution/collectLabelElements | Listing of label values. The resulting data are limited by the static platform limit to the maximum of 10000 rows.
[**compute_report**](ActionsApi.md#compute_report) | **POST** /api/actions/workspaces/{workspaceId}/execution/afm/execute | Executes analytical request and returns link to the result
[**compute_valid_objects**](ActionsApi.md#compute_valid_objects) | **POST** /api/actions/workspaces/{workspaceId}/execution/afm/computeValidObjects | Valid objects
[**explain_afm**](ActionsApi.md#explain_afm) | **POST** /api/actions/workspaces/{workspaceId}/execution/afm/explain | AFM explain resource.
[**retrieve_result**](ActionsApi.md#retrieve_result) | **GET** /api/actions/workspaces/{workspaceId}/execution/afm/execute/result/{resultId} | Get a single execution result


# **compute_label_elements_post**
> ElementsResponse compute_label_elements_post(workspace_id, elements_request)

Listing of label values. The resulting data are limited by the static platform limit to the maximum of 10000 rows.

Returns paged list of elements (values) of given label satisfying given filtering criteria.

### Example


```python
import time
import gooddata_afm_client
from gooddata_afm_client.api import actions_api
from gooddata_afm_client.model.elements_request import ElementsRequest
from gooddata_afm_client.model.elements_response import ElementsResponse
from pprint import pprint
# Defining the host is optional and defaults to http://gooddata-cn-ce:3000
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_afm_client.Configuration(
    host = "http://gooddata-cn-ce:3000"
)


# Enter a context with an instance of the API client
with gooddata_afm_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    elements_request = ElementsRequest(
        label="label_example",
        filter_by=ElementsRequestFilterBy(
            label_type="REQUESTED",
        ),
        sort_order="ASC",
        complement_filter=False,
        pattern_filter="pattern_filter_example",
        exact_filter=[
            "exact_filter_example",
        ],
        data_sampling_percentage=100,
    ) # ElementsRequest | 
    offset = 0 # int | Request page with this offset. Must be positive integer. The API is limited to the maximum of 10000 items. Therefore this parameter is limited to this number as well. (optional) if omitted the server will use the default value of 0
    limit = 1000 # int | Return only this number of items. Must be positive integer. The API is limited to the maximum of 10000 items. Therefore this parameter is limited to this number as well. (optional) if omitted the server will use the default value of 1000
    skip_cache = True # bool | Ignore all caches during execution of current request. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Listing of label values. The resulting data are limited by the static platform limit to the maximum of 10000 rows.
        api_response = api_instance.compute_label_elements_post(workspace_id, elements_request)
        pprint(api_response)
    except gooddata_afm_client.ApiException as e:
        print("Exception when calling ActionsApi->compute_label_elements_post: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Listing of label values. The resulting data are limited by the static platform limit to the maximum of 10000 rows.
        api_response = api_instance.compute_label_elements_post(workspace_id, elements_request, offset=offset, limit=limit, skip_cache=skip_cache)
        pprint(api_response)
    except gooddata_afm_client.ApiException as e:
        print("Exception when calling ActionsApi->compute_label_elements_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **elements_request** | [**ElementsRequest**](ElementsRequest.md)|  |
 **offset** | **int**| Request page with this offset. Must be positive integer. The API is limited to the maximum of 10000 items. Therefore this parameter is limited to this number as well. | [optional] if omitted the server will use the default value of 0
 **limit** | **int**| Return only this number of items. Must be positive integer. The API is limited to the maximum of 10000 items. Therefore this parameter is limited to this number as well. | [optional] if omitted the server will use the default value of 1000
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional]

### Return type

[**ElementsResponse**](ElementsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of label values. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **compute_report**
> AfmExecutionResponse compute_report(workspace_id, afm_execution)

Executes analytical request and returns link to the result

AFM is a combination of attributes, measures and filters that describe a query you want to execute.

### Example


```python
import time
import gooddata_afm_client
from gooddata_afm_client.api import actions_api
from gooddata_afm_client.model.afm_execution_response import AfmExecutionResponse
from gooddata_afm_client.model.afm_execution import AfmExecution
from pprint import pprint
# Defining the host is optional and defaults to http://gooddata-cn-ce:3000
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_afm_client.Configuration(
    host = "http://gooddata-cn-ce:3000"
)


# Enter a context with an instance of the API client
with gooddata_afm_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    afm_execution = AfmExecution(
        execution=AFM(
            attributes=[
                AttributeItem(
                    local_identifier="2",
                    label=AfmObjectIdentifier(
                        identifier=ObjectIdentifier(
                            id="sample_item.price",
                            type="fact",
                        ),
                    ),
                ),
            ],
            filters=[
                FilterDefinition(),
            ],
            measures=[
                MeasureItem(
                    local_identifier="sampleAutoGenerated0123_ID",
                    definition=MeasureDefinition(),
                ),
            ],
            aux_measures=[
                MeasureItem(
                    local_identifier="sampleAutoGenerated0123_ID",
                    definition=MeasureDefinition(),
                ),
            ],
        ),
        result_spec=ResultSpec(
            dimensions=[
                Dimension(
                    item_identifiers=[
                        "[ "attribute1", "measureGroup"]",
                    ],
                    local_identifier="firstDimension",
                    sorting=[
                        None,
                    ],
                ),
            ],
            grand_totals=[
                GrandTotal(
                    local_identifier="firstGrandTotal",
                    function="SUM",
                    included_dimensions={
                        "key": IncludedDimensionProps(
                            dimension_attributes_values={
                                "key": [
                                    "key_example",
                                ],
                            },
                        ),
                    },
                ),
            ],
        ),
        settings=ExecutionSettings(
            data_sampling_percentage=0,
        ),
    ) # AfmExecution | 
    skip_cache = False # bool | Ignore all caches during execution of current request. (optional) if omitted the server will use the default value of False
    timestamp = "2020-06-03T10:15:30+01:00" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Executes analytical request and returns link to the result
        api_response = api_instance.compute_report(workspace_id, afm_execution)
        pprint(api_response)
    except gooddata_afm_client.ApiException as e:
        print("Exception when calling ActionsApi->compute_report: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Executes analytical request and returns link to the result
        api_response = api_instance.compute_report(workspace_id, afm_execution, skip_cache=skip_cache, timestamp=timestamp)
        pprint(api_response)
    except gooddata_afm_client.ApiException as e:
        print("Exception when calling ActionsApi->compute_report: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **afm_execution** | [**AfmExecution**](AfmExecution.md)|  |
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional] if omitted the server will use the default value of False
 **timestamp** | **str**|  | [optional]

### Return type

[**AfmExecutionResponse**](AfmExecutionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | AFM Execution response with links to the result and server-enhanced dimensions from the original request. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **compute_valid_objects**
> AfmValidObjectsResponse compute_valid_objects(workspace_id, afm_valid_objects_query)

Valid objects

Returns list containing attributes, facts, or metrics, which can be added to given AFM while still keeping it computable.

### Example


```python
import time
import gooddata_afm_client
from gooddata_afm_client.api import actions_api
from gooddata_afm_client.model.afm_valid_objects_query import AfmValidObjectsQuery
from gooddata_afm_client.model.afm_valid_objects_response import AfmValidObjectsResponse
from pprint import pprint
# Defining the host is optional and defaults to http://gooddata-cn-ce:3000
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_afm_client.Configuration(
    host = "http://gooddata-cn-ce:3000"
)


# Enter a context with an instance of the API client
with gooddata_afm_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    afm_valid_objects_query = AfmValidObjectsQuery(
        types=[
            "facts",
        ],
        afm=AFM(
            attributes=[
                AttributeItem(
                    local_identifier="2",
                    label=AfmObjectIdentifier(
                        identifier=ObjectIdentifier(
                            id="sample_item.price",
                            type="fact",
                        ),
                    ),
                ),
            ],
            filters=[
                FilterDefinition(),
            ],
            measures=[
                MeasureItem(
                    local_identifier="sampleAutoGenerated0123_ID",
                    definition=MeasureDefinition(),
                ),
            ],
            aux_measures=[
                MeasureItem(
                    local_identifier="sampleAutoGenerated0123_ID",
                    definition=MeasureDefinition(),
                ),
            ],
        ),
    ) # AfmValidObjectsQuery | 

    # example passing only required values which don't have defaults set
    try:
        # Valid objects
        api_response = api_instance.compute_valid_objects(workspace_id, afm_valid_objects_query)
        pprint(api_response)
    except gooddata_afm_client.ApiException as e:
        print("Exception when calling ActionsApi->compute_valid_objects: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **afm_valid_objects_query** | [**AfmValidObjectsQuery**](AfmValidObjectsQuery.md)|  |

### Return type

[**AfmValidObjectsResponse**](AfmValidObjectsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of attributes, facts and metrics valid with respect to given AFM. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **explain_afm**
> file_type explain_afm(workspace_id, afm_execution)

AFM explain resource.

The resource provides static structures needed for investigation of a problem with given AFM. The structures differs for AQE and for Calcique. They are either MAQL (internal form of AFM) and logical and physical models (LDM and PDM) of corresponding workspace or MAQL and GRPC and WDF models.

### Example


```python
import time
import gooddata_afm_client
from gooddata_afm_client.api import actions_api
from gooddata_afm_client.model.afm_execution import AfmExecution
from pprint import pprint
# Defining the host is optional and defaults to http://gooddata-cn-ce:3000
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_afm_client.Configuration(
    host = "http://gooddata-cn-ce:3000"
)


# Enter a context with an instance of the API client
with gooddata_afm_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    afm_execution = AfmExecution(
        execution=AFM(
            attributes=[
                AttributeItem(
                    local_identifier="2",
                    label=AfmObjectIdentifier(
                        identifier=ObjectIdentifier(
                            id="sample_item.price",
                            type="fact",
                        ),
                    ),
                ),
            ],
            filters=[
                FilterDefinition(),
            ],
            measures=[
                MeasureItem(
                    local_identifier="sampleAutoGenerated0123_ID",
                    definition=MeasureDefinition(),
                ),
            ],
            aux_measures=[
                MeasureItem(
                    local_identifier="sampleAutoGenerated0123_ID",
                    definition=MeasureDefinition(),
                ),
            ],
        ),
        result_spec=ResultSpec(
            dimensions=[
                Dimension(
                    item_identifiers=[
                        "[ "attribute1", "measureGroup"]",
                    ],
                    local_identifier="firstDimension",
                    sorting=[
                        None,
                    ],
                ),
            ],
            grand_totals=[
                GrandTotal(
                    local_identifier="firstGrandTotal",
                    function="SUM",
                    included_dimensions={
                        "key": IncludedDimensionProps(
                            dimension_attributes_values={
                                "key": [
                                    "key_example",
                                ],
                            },
                        ),
                    },
                ),
            ],
        ),
        settings=ExecutionSettings(
            data_sampling_percentage=0,
        ),
    ) # AfmExecution | 
    explain_type = "explainType_example" # str | Requested explain type (LDM, PDM, GRPC_MODEL, WDF or MAQL). If not specified all types are bundled in a ZIP archive. (optional)

    # example passing only required values which don't have defaults set
    try:
        # AFM explain resource.
        api_response = api_instance.explain_afm(workspace_id, afm_execution)
        pprint(api_response)
    except gooddata_afm_client.ApiException as e:
        print("Exception when calling ActionsApi->explain_afm: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # AFM explain resource.
        api_response = api_instance.explain_afm(workspace_id, afm_execution, explain_type=explain_type)
        pprint(api_response)
    except gooddata_afm_client.ApiException as e:
        print("Exception when calling ActionsApi->explain_afm: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **afm_execution** | [**AfmExecution**](AfmExecution.md)|  |
 **explain_type** | **str**| Requested explain type (LDM, PDM, GRPC_MODEL, WDF or MAQL). If not specified all types are bundled in a ZIP archive. | [optional]

### Return type

**file_type**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/zip


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | ZIP archive with MAQL, LDM and PDM files; or with MAQL, GRPC_MODEL and WDF files |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_result**
> ExecutionResult retrieve_result(workspace_id, result_id)

Get a single execution result

Gets a single execution result.

### Example


```python
import time
import gooddata_afm_client
from gooddata_afm_client.api import actions_api
from gooddata_afm_client.model.execution_result import ExecutionResult
from gooddata_afm_client.model.error_message import ErrorMessage
from pprint import pprint
# Defining the host is optional and defaults to http://gooddata-cn-ce:3000
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_afm_client.Configuration(
    host = "http://gooddata-cn-ce:3000"
)


# Enter a context with an instance of the API client
with gooddata_afm_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    result_id = "a9b28f9dc55f37ea9f4a5fb0c76895923591e781" # str | Result ID
    offset = [
        offset=1,10,
    ] # [int] | Request page with these offsets. Format is offset=1,2,3,... - one offset for each dimensions in ResultSpec from originating AFM. (optional) if omitted the server will use the default value of []
    limit = [
        limit=1,10,
    ] # [int] | Return only this number of items. Format is limit=1,2,3,... - one limit for each dimensions in ResultSpec from originating AFM. (optional) if omitted the server will use the default value of []

    # example passing only required values which don't have defaults set
    try:
        # Get a single execution result
        api_response = api_instance.retrieve_result(workspace_id, result_id)
        pprint(api_response)
    except gooddata_afm_client.ApiException as e:
        print("Exception when calling ActionsApi->retrieve_result: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a single execution result
        api_response = api_instance.retrieve_result(workspace_id, result_id, offset=offset, limit=limit)
        pprint(api_response)
    except gooddata_afm_client.ApiException as e:
        print("Exception when calling ActionsApi->retrieve_result: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **result_id** | **str**| Result ID |
 **offset** | **[int]**| Request page with these offsets. Format is offset&#x3D;1,2,3,... - one offset for each dimensions in ResultSpec from originating AFM. | [optional] if omitted the server will use the default value of []
 **limit** | **[int]**| Return only this number of items. Format is limit&#x3D;1,2,3,... - one limit for each dimensions in ResultSpec from originating AFM. | [optional] if omitted the server will use the default value of []

### Return type

[**ExecutionResult**](ExecutionResult.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Execution result was found and returned. |  -  |
**400** | Limit and/or offset query parameters (paging) were invalid. |  -  |
**404** | Execution result was not found. |  -  |
**500** | The result processing has failed unexpectedly. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


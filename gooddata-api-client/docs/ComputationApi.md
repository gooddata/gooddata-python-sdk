# gooddata_api_client.ComputationApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**compute_label_elements_post**](ComputationApi.md#compute_label_elements_post) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/collectLabelElements | Listing of label values. The resulting data are limited by the static platform limit to the maximum of 10000 rows.
[**compute_report**](ComputationApi.md#compute_report) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/afm/execute | Executes analytical request and returns link to the result
[**compute_valid_descendants**](ComputationApi.md#compute_valid_descendants) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/afm/computeValidDescendants | (BETA) Valid descendants
[**compute_valid_objects**](ComputationApi.md#compute_valid_objects) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/afm/computeValidObjects | Valid objects
[**explain_afm**](ComputationApi.md#explain_afm) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/afm/explain | AFM explain resource.
[**key_driver_analysis**](ComputationApi.md#key_driver_analysis) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/computeKeyDrivers | (EXPERIMENTAL) Compute key driver analysis
[**key_driver_analysis_result**](ComputationApi.md#key_driver_analysis_result) | **GET** /api/v1/actions/workspaces/{workspaceId}/execution/computeKeyDrivers/result/{resultId} | (EXPERIMENTAL) Get key driver analysis result
[**retrieve_execution_metadata**](ComputationApi.md#retrieve_execution_metadata) | **GET** /api/v1/actions/workspaces/{workspaceId}/execution/afm/execute/result/{resultId}/metadata | Get a single execution result&#39;s metadata.
[**retrieve_result**](ComputationApi.md#retrieve_result) | **GET** /api/v1/actions/workspaces/{workspaceId}/execution/afm/execute/result/{resultId} | Get a single execution result


# **compute_label_elements_post**
> ElementsResponse compute_label_elements_post(workspace_id, elements_request)

Listing of label values. The resulting data are limited by the static platform limit to the maximum of 10000 rows.

Returns paged list of elements (values) of given label satisfying given filtering criteria.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import computation_api
from gooddata_api_client.model.elements_request import ElementsRequest
from gooddata_api_client.model.elements_response import ElementsResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = computation_api.ComputationApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    elements_request = ElementsRequest(
        cache_id="cache_id_example",
        complement_filter=False,
        data_sampling_percentage=100.0,
        depends_on=[
            ElementsRequestDependsOnInner(None),
        ],
        exact_filter=[
            "exact_filter_example",
        ],
        exclude_primary_label=False,
        filter_by=FilterBy(
            label_type="REQUESTED",
        ),
        label="label_id",
        pattern_filter="pattern_filter_example",
        sort_order="ASC",
        validate_by=[
            ValidateByItem(
                id="id_example",
                type="fact",
            ),
        ],
    ) # ElementsRequest | 
    offset = 0 # int | Request page with this offset. Must be positive integer. The API is limited to the maximum of 10000 items. Therefore this parameter is limited to this number as well. (optional) if omitted the server will use the default value of 0
    limit = 1000 # int | Return only this number of items. Must be positive integer. The API is limited to the maximum of 10000 items. Therefore this parameter is limited to this number as well. (optional) if omitted the server will use the default value of 1000
    skip_cache = False # bool | Ignore all caches during execution of current request. (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # Listing of label values. The resulting data are limited by the static platform limit to the maximum of 10000 rows.
        api_response = api_instance.compute_label_elements_post(workspace_id, elements_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputationApi->compute_label_elements_post: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Listing of label values. The resulting data are limited by the static platform limit to the maximum of 10000 rows.
        api_response = api_instance.compute_label_elements_post(workspace_id, elements_request, offset=offset, limit=limit, skip_cache=skip_cache)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputationApi->compute_label_elements_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **elements_request** | [**ElementsRequest**](ElementsRequest.md)|  |
 **offset** | **int**| Request page with this offset. Must be positive integer. The API is limited to the maximum of 10000 items. Therefore this parameter is limited to this number as well. | [optional] if omitted the server will use the default value of 0
 **limit** | **int**| Return only this number of items. Must be positive integer. The API is limited to the maximum of 10000 items. Therefore this parameter is limited to this number as well. | [optional] if omitted the server will use the default value of 1000
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional] if omitted the server will use the default value of False

### Return type

[**ElementsResponse**](ElementsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


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
import gooddata_api_client
from gooddata_api_client.api import computation_api
from gooddata_api_client.model.afm_execution_response import AfmExecutionResponse
from gooddata_api_client.model.afm_execution import AfmExecution
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = computation_api.ComputationApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    afm_execution = AfmExecution(
        execution=AFM(
            attributes=[
                AttributeItem(
                    label=AfmObjectIdentifierLabel(
                        identifier=AfmObjectIdentifierLabelIdentifier(
                            id="sample_item.price",
                            type="label",
                        ),
                    ),
                    local_identifier="attribute_1",
                    show_all_values=False,
                ),
            ],
            aux_measures=[
                MeasureItem(
                    definition=MeasureDefinition(),
                    local_identifier="metric_1",
                ),
            ],
            filters=[
                FilterDefinition(),
            ],
            measures=[
                MeasureItem(
                    definition=MeasureDefinition(),
                    local_identifier="metric_1",
                ),
            ],
        ),
        result_spec=ResultSpec(
            dimensions=[
                Dimension(
                    item_identifiers=["attribute_1","measureGroup"],
                    local_identifier="firstDimension",
                    sorting=[
                        SortKey(),
                    ],
                ),
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
                        ),
                    ],
                ),
            ],
        ),
        settings=ExecutionSettings(
            data_sampling_percentage=0,
            timestamp=dateutil_parser('1970-01-01T00:00:00.00Z'),
        ),
    ) # AfmExecution | 
    skip_cache = False # bool | Ignore all caches during execution of current request. (optional) if omitted the server will use the default value of False
    timestamp = "2020-06-03T10:15:30+01:00" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Executes analytical request and returns link to the result
        api_response = api_instance.compute_report(workspace_id, afm_execution)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputationApi->compute_report: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Executes analytical request and returns link to the result
        api_response = api_instance.compute_report(workspace_id, afm_execution, skip_cache=skip_cache, timestamp=timestamp)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputationApi->compute_report: %s\n" % e)
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
**200** | AFM Execution response with links to the result and server-enhanced dimensions from the original request. |  * X-GDC-CANCEL-TOKEN - A token that can be used to cancel this execution <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **compute_valid_descendants**
> AfmValidDescendantsResponse compute_valid_descendants(workspace_id, afm_valid_descendants_query)

(BETA) Valid descendants

(BETA) Returns map of lists of attributes that can be used as descendants of the given attributes.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import computation_api
from gooddata_api_client.model.afm_valid_descendants_query import AfmValidDescendantsQuery
from gooddata_api_client.model.afm_valid_descendants_response import AfmValidDescendantsResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = computation_api.ComputationApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    afm_valid_descendants_query = AfmValidDescendantsQuery(
        attributes=[
            AfmObjectIdentifierAttribute(
                identifier=AfmObjectIdentifierAttributeIdentifier(
                    id="sample_item.price",
                    type="attribute",
                ),
            ),
        ],
    ) # AfmValidDescendantsQuery | 

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Valid descendants
        api_response = api_instance.compute_valid_descendants(workspace_id, afm_valid_descendants_query)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputationApi->compute_valid_descendants: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **afm_valid_descendants_query** | [**AfmValidDescendantsQuery**](AfmValidDescendantsQuery.md)|  |

### Return type

[**AfmValidDescendantsResponse**](AfmValidDescendantsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Map of lists of attributes valid as descendants of the given attributes. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **compute_valid_objects**
> AfmValidObjectsResponse compute_valid_objects(workspace_id, afm_valid_objects_query)

Valid objects

Returns list containing attributes, facts, or metrics, which can be added to given AFM while still keeping it computable.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import computation_api
from gooddata_api_client.model.afm_valid_objects_query import AfmValidObjectsQuery
from gooddata_api_client.model.afm_valid_objects_response import AfmValidObjectsResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = computation_api.ComputationApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    afm_valid_objects_query = AfmValidObjectsQuery(
        afm=AFM(
            attributes=[
                AttributeItem(
                    label=AfmObjectIdentifierLabel(
                        identifier=AfmObjectIdentifierLabelIdentifier(
                            id="sample_item.price",
                            type="label",
                        ),
                    ),
                    local_identifier="attribute_1",
                    show_all_values=False,
                ),
            ],
            aux_measures=[
                MeasureItem(
                    definition=MeasureDefinition(),
                    local_identifier="metric_1",
                ),
            ],
            filters=[
                FilterDefinition(),
            ],
            measures=[
                MeasureItem(
                    definition=MeasureDefinition(),
                    local_identifier="metric_1",
                ),
            ],
        ),
        types=[
            "facts",
        ],
    ) # AfmValidObjectsQuery | 

    # example passing only required values which don't have defaults set
    try:
        # Valid objects
        api_response = api_instance.compute_valid_objects(workspace_id, afm_valid_objects_query)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputationApi->compute_valid_objects: %s\n" % e)
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
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of attributes, facts and metrics valid with respect to given AFM. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **explain_afm**
> explain_afm(workspace_id, afm_execution)

AFM explain resource.

The resource provides static structures needed for investigation of a problem with given AFM.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import computation_api
from gooddata_api_client.model.afm_execution import AfmExecution
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = computation_api.ComputationApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    afm_execution = AfmExecution(
        execution=AFM(
            attributes=[
                AttributeItem(
                    label=AfmObjectIdentifierLabel(
                        identifier=AfmObjectIdentifierLabelIdentifier(
                            id="sample_item.price",
                            type="label",
                        ),
                    ),
                    local_identifier="attribute_1",
                    show_all_values=False,
                ),
            ],
            aux_measures=[
                MeasureItem(
                    definition=MeasureDefinition(),
                    local_identifier="metric_1",
                ),
            ],
            filters=[
                FilterDefinition(),
            ],
            measures=[
                MeasureItem(
                    definition=MeasureDefinition(),
                    local_identifier="metric_1",
                ),
            ],
        ),
        result_spec=ResultSpec(
            dimensions=[
                Dimension(
                    item_identifiers=["attribute_1","measureGroup"],
                    local_identifier="firstDimension",
                    sorting=[
                        SortKey(),
                    ],
                ),
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
                        ),
                    ],
                ),
            ],
        ),
        settings=ExecutionSettings(
            data_sampling_percentage=0,
            timestamp=dateutil_parser('1970-01-01T00:00:00.00Z'),
        ),
    ) # AfmExecution | 
    explain_type = "MAQL" # str | Requested explain type. If not specified all types are bundled in a ZIP archive.  `MAQL` - MAQL Abstract Syntax Tree, execution dimensions and related info  `GRPC_MODEL` - Datasets used in execution  `GRPC_MODEL_SVG` - Generated SVG image of the datasets  `WDF` - Workspace data filters in execution workspace context  `QT` - Query Tree, created from MAQL AST using Logical Data Model,  contains all information needed to generate SQL  `QT_SVG` - Generated SVG image of the Query Tree  `OPT_QT` - Optimized Query Tree  `OPT_QT_SVG` - Generated SVG image of the Optimized Query Tree  `SQL` - Final SQL to be executed  `SETTINGS` - Settings used to execute explain request (optional)

    # example passing only required values which don't have defaults set
    try:
        # AFM explain resource.
        api_instance.explain_afm(workspace_id, afm_execution)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputationApi->explain_afm: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # AFM explain resource.
        api_instance.explain_afm(workspace_id, afm_execution, explain_type=explain_type)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputationApi->explain_afm: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **afm_execution** | [**AfmExecution**](AfmExecution.md)|  |
 **explain_type** | **str**| Requested explain type. If not specified all types are bundled in a ZIP archive.  &#x60;MAQL&#x60; - MAQL Abstract Syntax Tree, execution dimensions and related info  &#x60;GRPC_MODEL&#x60; - Datasets used in execution  &#x60;GRPC_MODEL_SVG&#x60; - Generated SVG image of the datasets  &#x60;WDF&#x60; - Workspace data filters in execution workspace context  &#x60;QT&#x60; - Query Tree, created from MAQL AST using Logical Data Model,  contains all information needed to generate SQL  &#x60;QT_SVG&#x60; - Generated SVG image of the Query Tree  &#x60;OPT_QT&#x60; - Optimized Query Tree  &#x60;OPT_QT_SVG&#x60; - Generated SVG image of the Optimized Query Tree  &#x60;SQL&#x60; - Final SQL to be executed  &#x60;SETTINGS&#x60; - Settings used to execute explain request | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/sql, application/zip, image/svg+xml


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Requested resource |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **key_driver_analysis**
> KeyDriversResponse key_driver_analysis(workspace_id, key_drivers_request)

(EXPERIMENTAL) Compute key driver analysis

(EXPERIMENTAL) Computes key driver analysis for the provided execution definition.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import computation_api
from gooddata_api_client.model.key_drivers_response import KeyDriversResponse
from gooddata_api_client.model.key_drivers_request import KeyDriversRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = computation_api.ComputationApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    key_drivers_request = KeyDriversRequest(
        aux_metrics=[
            MeasureItem(
                definition=MeasureDefinition(),
                local_identifier="metric_1",
            ),
        ],
        metric=MeasureItem(
            definition=MeasureDefinition(),
            local_identifier="metric_1",
        ),
        sort_direction="DESC",
    ) # KeyDriversRequest | 
    skip_cache = False # bool | Ignore all caches during execution of current request. (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Compute key driver analysis
        api_response = api_instance.key_driver_analysis(workspace_id, key_drivers_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputationApi->key_driver_analysis: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (EXPERIMENTAL) Compute key driver analysis
        api_response = api_instance.key_driver_analysis(workspace_id, key_drivers_request, skip_cache=skip_cache)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputationApi->key_driver_analysis: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **key_drivers_request** | [**KeyDriversRequest**](KeyDriversRequest.md)|  |
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional] if omitted the server will use the default value of False

### Return type

[**KeyDriversResponse**](KeyDriversResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **key_driver_analysis_result**
> KeyDriversResult key_driver_analysis_result(workspace_id, result_id)

(EXPERIMENTAL) Get key driver analysis result

(EXPERIMENTAL) Gets key driver analysis.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import computation_api
from gooddata_api_client.model.key_drivers_result import KeyDriversResult
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = computation_api.ComputationApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    result_id = "a9b28f9dc55f37ea9f4a5fb0c76895923591e781" # str | Result ID
    offset = 1 # int |  (optional)
    limit = 1 # int |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Get key driver analysis result
        api_response = api_instance.key_driver_analysis_result(workspace_id, result_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputationApi->key_driver_analysis_result: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (EXPERIMENTAL) Get key driver analysis result
        api_response = api_instance.key_driver_analysis_result(workspace_id, result_id, offset=offset, limit=limit)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputationApi->key_driver_analysis_result: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **result_id** | **str**| Result ID |
 **offset** | **int**|  | [optional]
 **limit** | **int**|  | [optional]

### Return type

[**KeyDriversResult**](KeyDriversResult.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_execution_metadata**
> ResultCacheMetadata retrieve_execution_metadata(workspace_id, result_id)

Get a single execution result's metadata.

The resource provides execution result's metadata as AFM and resultSpec used in execution request and an executionResponse

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import computation_api
from gooddata_api_client.model.result_cache_metadata import ResultCacheMetadata
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = computation_api.ComputationApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    result_id = "a9b28f9dc55f37ea9f4a5fb0c76895923591e781" # str | Result ID

    # example passing only required values which don't have defaults set
    try:
        # Get a single execution result's metadata.
        api_response = api_instance.retrieve_execution_metadata(workspace_id, result_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputationApi->retrieve_execution_metadata: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **result_id** | **str**| Result ID |

### Return type

[**ResultCacheMetadata**](ResultCacheMetadata.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Execution result&#39;s metadata was found and returned. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_result**
> ExecutionResult retrieve_result(workspace_id, result_id)

Get a single execution result

Gets a single execution result.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import computation_api
from gooddata_api_client.model.execution_result import ExecutionResult
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = computation_api.ComputationApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    result_id = "a9b28f9dc55f37ea9f4a5fb0c76895923591e781" # str | Result ID
    offset = [
        offset=1,10,
    ] # [int] | Request page with these offsets. Format is offset=1,2,3,... - one offset for each dimensions in ResultSpec from originating AFM. (optional) if omitted the server will use the default value of []
    limit = [
        limit=1,10,
    ] # [int] | Return only this number of items. Format is limit=1,2,3,... - one limit for each dimensions in ResultSpec from originating AFM. (optional) if omitted the server will use the default value of []
    excluded_total_dimensions = [
        "excludedTotalDimensions=dim_0,dim_1",
    ] # [str] | Identifiers of the dimensions where grand total data should not be returned for this request. A grand total will not be returned if all of its totalDimensions are in excludedTotalDimensions. (optional) if omitted the server will use the default value of []
    x_gdc_cancel_token = "X-GDC-CANCEL-TOKEN_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a single execution result
        api_response = api_instance.retrieve_result(workspace_id, result_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputationApi->retrieve_result: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a single execution result
        api_response = api_instance.retrieve_result(workspace_id, result_id, offset=offset, limit=limit, excluded_total_dimensions=excluded_total_dimensions, x_gdc_cancel_token=x_gdc_cancel_token)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputationApi->retrieve_result: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **result_id** | **str**| Result ID |
 **offset** | **[int]**| Request page with these offsets. Format is offset&#x3D;1,2,3,... - one offset for each dimensions in ResultSpec from originating AFM. | [optional] if omitted the server will use the default value of []
 **limit** | **[int]**| Return only this number of items. Format is limit&#x3D;1,2,3,... - one limit for each dimensions in ResultSpec from originating AFM. | [optional] if omitted the server will use the default value of []
 **excluded_total_dimensions** | **[str]**| Identifiers of the dimensions where grand total data should not be returned for this request. A grand total will not be returned if all of its totalDimensions are in excludedTotalDimensions. | [optional] if omitted the server will use the default value of []
 **x_gdc_cancel_token** | **str**|  | [optional]

### Return type

[**ExecutionResult**](ExecutionResult.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Execution result was found and returned. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


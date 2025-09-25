# gooddata_api_client.ComputationApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**column_statistics**](ComputationApi.md#column_statistics) | **POST** /api/v1/actions/dataSources/{dataSourceId}/computeColumnStatistics | (EXPERIMENTAL) Compute column statistics
[**compute_label_elements_post**](ComputationApi.md#compute_label_elements_post) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/collectLabelElements | Listing of label values. The resulting data are limited by the static platform limit to the maximum of 10000 rows.
[**compute_report**](ComputationApi.md#compute_report) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/afm/execute | Executes analytical request and returns link to the result
[**compute_valid_descendants**](ComputationApi.md#compute_valid_descendants) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/afm/computeValidDescendants | (BETA) Valid descendants
[**compute_valid_objects**](ComputationApi.md#compute_valid_objects) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/afm/computeValidObjects | Valid objects
[**explain_afm**](ComputationApi.md#explain_afm) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/afm/explain | AFM explain resource.
[**key_driver_analysis**](ComputationApi.md#key_driver_analysis) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/computeKeyDrivers | (EXPERIMENTAL) Compute key driver analysis
[**key_driver_analysis_result**](ComputationApi.md#key_driver_analysis_result) | **GET** /api/v1/actions/workspaces/{workspaceId}/execution/computeKeyDrivers/result/{resultId} | (EXPERIMENTAL) Get key driver analysis result
[**retrieve_execution_metadata**](ComputationApi.md#retrieve_execution_metadata) | **GET** /api/v1/actions/workspaces/{workspaceId}/execution/afm/execute/result/{resultId}/metadata | Get a single execution result&#39;s metadata.
[**retrieve_result**](ComputationApi.md#retrieve_result) | **GET** /api/v1/actions/workspaces/{workspaceId}/execution/afm/execute/result/{resultId} | Get a single execution result


# **column_statistics**
> ColumnStatisticsResponse column_statistics(data_source_id, column_statistics_request)

(EXPERIMENTAL) Compute column statistics

(EXPERIMENTAL) Computes the requested statistical parameters of a column in a data source.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.column_statistics_request import ColumnStatisticsRequest
from gooddata_api_client.models.column_statistics_response import ColumnStatisticsResponse
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
    api_instance = gooddata_api_client.ComputationApi(api_client)
    data_source_id = 'data_source_id_example' # str | 
    column_statistics_request = gooddata_api_client.ColumnStatisticsRequest() # ColumnStatisticsRequest | 

    try:
        # (EXPERIMENTAL) Compute column statistics
        api_response = api_instance.column_statistics(data_source_id, column_statistics_request)
        print("The response of ComputationApi->column_statistics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ComputationApi->column_statistics: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  | 
 **column_statistics_request** | [**ColumnStatisticsRequest**](ColumnStatisticsRequest.md)|  | 

### Return type

[**ColumnStatisticsResponse**](ColumnStatisticsResponse.md)

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

# **compute_label_elements_post**
> ElementsResponse compute_label_elements_post(workspace_id, elements_request, offset=offset, limit=limit, skip_cache=skip_cache)

Listing of label values. The resulting data are limited by the static platform limit to the maximum of 10000 rows.

Returns paged list of elements (values) of given label satisfying given filtering criteria.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.elements_request import ElementsRequest
from gooddata_api_client.models.elements_response import ElementsResponse
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
    api_instance = gooddata_api_client.ComputationApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    elements_request = gooddata_api_client.ElementsRequest() # ElementsRequest | 
    offset = 0 # int | Request page with this offset. Must be positive integer. The API is limited to the maximum of 10000 items. Therefore this parameter is limited to this number as well. (optional) (default to 0)
    limit = 1000 # int | Return only this number of items. Must be positive integer. The API is limited to the maximum of 10000 items. Therefore this parameter is limited to this number as well. (optional) (default to 1000)
    skip_cache = False # bool | Ignore all caches during execution of current request. (optional) (default to False)

    try:
        # Listing of label values. The resulting data are limited by the static platform limit to the maximum of 10000 rows.
        api_response = api_instance.compute_label_elements_post(workspace_id, elements_request, offset=offset, limit=limit, skip_cache=skip_cache)
        print("The response of ComputationApi->compute_label_elements_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ComputationApi->compute_label_elements_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **elements_request** | [**ElementsRequest**](ElementsRequest.md)|  | 
 **offset** | **int**| Request page with this offset. Must be positive integer. The API is limited to the maximum of 10000 items. Therefore this parameter is limited to this number as well. | [optional] [default to 0]
 **limit** | **int**| Return only this number of items. Must be positive integer. The API is limited to the maximum of 10000 items. Therefore this parameter is limited to this number as well. | [optional] [default to 1000]
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional] [default to False]

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
> AfmExecutionResponse compute_report(workspace_id, afm_execution, skip_cache=skip_cache, timestamp=timestamp)

Executes analytical request and returns link to the result

AFM is a combination of attributes, measures and filters that describe a query you want to execute.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.afm_execution import AfmExecution
from gooddata_api_client.models.afm_execution_response import AfmExecutionResponse
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
    api_instance = gooddata_api_client.ComputationApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    afm_execution = gooddata_api_client.AfmExecution() # AfmExecution | 
    skip_cache = False # bool | Ignore all caches during execution of current request. (optional) (default to False)
    timestamp = '2020-06-03T10:15:30+01:00' # str |  (optional)

    try:
        # Executes analytical request and returns link to the result
        api_response = api_instance.compute_report(workspace_id, afm_execution, skip_cache=skip_cache, timestamp=timestamp)
        print("The response of ComputationApi->compute_report:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ComputationApi->compute_report: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **afm_execution** | [**AfmExecution**](AfmExecution.md)|  | 
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional] [default to False]
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
import gooddata_api_client
from gooddata_api_client.models.afm_valid_descendants_query import AfmValidDescendantsQuery
from gooddata_api_client.models.afm_valid_descendants_response import AfmValidDescendantsResponse
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
    api_instance = gooddata_api_client.ComputationApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    afm_valid_descendants_query = gooddata_api_client.AfmValidDescendantsQuery() # AfmValidDescendantsQuery | 

    try:
        # (BETA) Valid descendants
        api_response = api_instance.compute_valid_descendants(workspace_id, afm_valid_descendants_query)
        print("The response of ComputationApi->compute_valid_descendants:\n")
        pprint(api_response)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.afm_valid_objects_query import AfmValidObjectsQuery
from gooddata_api_client.models.afm_valid_objects_response import AfmValidObjectsResponse
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
    api_instance = gooddata_api_client.ComputationApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    afm_valid_objects_query = gooddata_api_client.AfmValidObjectsQuery() # AfmValidObjectsQuery | 

    try:
        # Valid objects
        api_response = api_instance.compute_valid_objects(workspace_id, afm_valid_objects_query)
        print("The response of ComputationApi->compute_valid_objects:\n")
        pprint(api_response)
    except Exception as e:
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
> explain_afm(workspace_id, afm_execution, explain_type=explain_type)

AFM explain resource.

The resource provides static structures needed for investigation of a problem with given AFM.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.afm_execution import AfmExecution
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
    api_instance = gooddata_api_client.ComputationApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    afm_execution = gooddata_api_client.AfmExecution() # AfmExecution | 
    explain_type = 'explain_type_example' # str | Requested explain type. If not specified all types are bundled in a ZIP archive.  `MAQL` - MAQL Abstract Syntax Tree, execution dimensions and related info  `GRPC_MODEL` - Datasets used in execution  `GRPC_MODEL_SVG` - Generated SVG image of the datasets  `COMPRESSED_GRPC_MODEL_SVG` - Generated SVG image of the model fragment used in the query  `WDF` - Workspace data filters in execution workspace context  `QT` - Query Tree, created from MAQL AST using Logical Data Model,  contains all information needed to generate SQL  `QT_SVG` - Generated SVG image of the Query Tree  `OPT_QT` - Optimized Query Tree  `OPT_QT_SVG` - Generated SVG image of the Optimized Query Tree  `SQL` - Final SQL to be executed  `COMPRESSED_SQL` - Final SQL to be executed with rolled SQL datasets  `SETTINGS` - Settings used to execute explain request (optional)

    try:
        # AFM explain resource.
        api_instance.explain_afm(workspace_id, afm_execution, explain_type=explain_type)
    except Exception as e:
        print("Exception when calling ComputationApi->explain_afm: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **afm_execution** | [**AfmExecution**](AfmExecution.md)|  | 
 **explain_type** | **str**| Requested explain type. If not specified all types are bundled in a ZIP archive.  &#x60;MAQL&#x60; - MAQL Abstract Syntax Tree, execution dimensions and related info  &#x60;GRPC_MODEL&#x60; - Datasets used in execution  &#x60;GRPC_MODEL_SVG&#x60; - Generated SVG image of the datasets  &#x60;COMPRESSED_GRPC_MODEL_SVG&#x60; - Generated SVG image of the model fragment used in the query  &#x60;WDF&#x60; - Workspace data filters in execution workspace context  &#x60;QT&#x60; - Query Tree, created from MAQL AST using Logical Data Model,  contains all information needed to generate SQL  &#x60;QT_SVG&#x60; - Generated SVG image of the Query Tree  &#x60;OPT_QT&#x60; - Optimized Query Tree  &#x60;OPT_QT_SVG&#x60; - Generated SVG image of the Optimized Query Tree  &#x60;SQL&#x60; - Final SQL to be executed  &#x60;COMPRESSED_SQL&#x60; - Final SQL to be executed with rolled SQL datasets  &#x60;SETTINGS&#x60; - Settings used to execute explain request | [optional] 

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
> KeyDriversResponse key_driver_analysis(workspace_id, key_drivers_request, skip_cache=skip_cache)

(EXPERIMENTAL) Compute key driver analysis

(EXPERIMENTAL) Computes key driver analysis for the provided execution definition.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.key_drivers_request import KeyDriversRequest
from gooddata_api_client.models.key_drivers_response import KeyDriversResponse
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
    api_instance = gooddata_api_client.ComputationApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    key_drivers_request = gooddata_api_client.KeyDriversRequest() # KeyDriversRequest | 
    skip_cache = False # bool | Ignore all caches during execution of current request. (optional) (default to False)

    try:
        # (EXPERIMENTAL) Compute key driver analysis
        api_response = api_instance.key_driver_analysis(workspace_id, key_drivers_request, skip_cache=skip_cache)
        print("The response of ComputationApi->key_driver_analysis:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ComputationApi->key_driver_analysis: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **key_drivers_request** | [**KeyDriversRequest**](KeyDriversRequest.md)|  | 
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional] [default to False]

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
> KeyDriversResult key_driver_analysis_result(workspace_id, result_id, offset=offset, limit=limit)

(EXPERIMENTAL) Get key driver analysis result

(EXPERIMENTAL) Gets key driver analysis.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.key_drivers_result import KeyDriversResult
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
    api_instance = gooddata_api_client.ComputationApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    result_id = 'a9b28f9dc55f37ea9f4a5fb0c76895923591e781' # str | Result ID
    offset = 56 # int |  (optional)
    limit = 56 # int |  (optional)

    try:
        # (EXPERIMENTAL) Get key driver analysis result
        api_response = api_instance.key_driver_analysis_result(workspace_id, result_id, offset=offset, limit=limit)
        print("The response of ComputationApi->key_driver_analysis_result:\n")
        pprint(api_response)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.result_cache_metadata import ResultCacheMetadata
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
    api_instance = gooddata_api_client.ComputationApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    result_id = 'a9b28f9dc55f37ea9f4a5fb0c76895923591e781' # str | Result ID

    try:
        # Get a single execution result's metadata.
        api_response = api_instance.retrieve_execution_metadata(workspace_id, result_id)
        print("The response of ComputationApi->retrieve_execution_metadata:\n")
        pprint(api_response)
    except Exception as e:
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
> ExecutionResult retrieve_result(workspace_id, result_id, offset=offset, limit=limit, excluded_total_dimensions=excluded_total_dimensions, x_gdc_cancel_token=x_gdc_cancel_token)

Get a single execution result

Gets a single execution result.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.execution_result import ExecutionResult
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
    api_instance = gooddata_api_client.ComputationApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    result_id = 'a9b28f9dc55f37ea9f4a5fb0c76895923591e781' # str | Result ID
    offset = [] # List[int] | Request page with these offsets. Format is offset=1,2,3,... - one offset for each dimensions in ResultSpec from originating AFM. (optional) (default to [])
    limit = [] # List[int] | Return only this number of items. Format is limit=1,2,3,... - one limit for each dimensions in ResultSpec from originating AFM. (optional) (default to [])
    excluded_total_dimensions = [] # List[str] | Identifiers of the dimensions where grand total data should not be returned for this request. A grand total will not be returned if all of its totalDimensions are in excludedTotalDimensions. (optional) (default to [])
    x_gdc_cancel_token = 'x_gdc_cancel_token_example' # str |  (optional)

    try:
        # Get a single execution result
        api_response = api_instance.retrieve_result(workspace_id, result_id, offset=offset, limit=limit, excluded_total_dimensions=excluded_total_dimensions, x_gdc_cancel_token=x_gdc_cancel_token)
        print("The response of ComputationApi->retrieve_result:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ComputationApi->retrieve_result: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **result_id** | **str**| Result ID | 
 **offset** | [**List[int]**](int.md)| Request page with these offsets. Format is offset&#x3D;1,2,3,... - one offset for each dimensions in ResultSpec from originating AFM. | [optional] [default to []]
 **limit** | [**List[int]**](int.md)| Return only this number of items. Format is limit&#x3D;1,2,3,... - one limit for each dimensions in ResultSpec from originating AFM. | [optional] [default to []]
 **excluded_total_dimensions** | [**List[str]**](str.md)| Identifiers of the dimensions where grand total data should not be returned for this request. A grand total will not be returned if all of its totalDimensions are in excludedTotalDimensions. | [optional] [default to []]
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


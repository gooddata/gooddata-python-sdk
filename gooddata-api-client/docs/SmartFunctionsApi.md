# gooddata_api_client.SmartFunctionsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**ai_chat**](SmartFunctionsApi.md#ai_chat) | **POST** /api/v1/actions/workspaces/{workspaceId}/ai/chat | (BETA) Chat with AI
[**ai_chat_history**](SmartFunctionsApi.md#ai_chat_history) | **POST** /api/v1/actions/workspaces/{workspaceId}/ai/chatHistory | (BETA) Get Chat History
[**ai_chat_stream**](SmartFunctionsApi.md#ai_chat_stream) | **POST** /api/v1/actions/workspaces/{workspaceId}/ai/chatStream | (BETA) Chat with AI
[**ai_chat_usage**](SmartFunctionsApi.md#ai_chat_usage) | **GET** /api/v1/actions/workspaces/{workspaceId}/ai/chatUsage | Get Chat Usage
[**ai_search**](SmartFunctionsApi.md#ai_search) | **POST** /api/v1/actions/workspaces/{workspaceId}/ai/search | (BETA) Semantic Search in Metadata
[**anomaly_detection**](SmartFunctionsApi.md#anomaly_detection) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/functions/anomalyDetection/{resultId} | (EXPERIMENTAL) Smart functions - Anomaly Detection
[**anomaly_detection_result**](SmartFunctionsApi.md#anomaly_detection_result) | **GET** /api/v1/actions/workspaces/{workspaceId}/execution/functions/anomalyDetection/result/{resultId} | (EXPERIMENTAL) Smart functions - Anomaly Detection Result
[**clustering**](SmartFunctionsApi.md#clustering) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/functions/clustering/{resultId} | (EXPERIMENTAL) Smart functions - Clustering
[**clustering_result**](SmartFunctionsApi.md#clustering_result) | **GET** /api/v1/actions/workspaces/{workspaceId}/execution/functions/clustering/result/{resultId} | (EXPERIMENTAL) Smart functions - Clustering Result
[**create_memory_item**](SmartFunctionsApi.md#create_memory_item) | **POST** /api/v1/actions/workspaces/{workspaceId}/ai/memory | (EXPERIMENTAL) Create new memory item
[**forecast**](SmartFunctionsApi.md#forecast) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/functions/forecast/{resultId} | (BETA) Smart functions - Forecast
[**forecast_result**](SmartFunctionsApi.md#forecast_result) | **GET** /api/v1/actions/workspaces/{workspaceId}/execution/functions/forecast/result/{resultId} | (BETA) Smart functions - Forecast Result
[**get_memory_item**](SmartFunctionsApi.md#get_memory_item) | **GET** /api/v1/actions/workspaces/{workspaceId}/ai/memory/{memoryId} | (EXPERIMENTAL) Get memory item
[**get_quality_issues**](SmartFunctionsApi.md#get_quality_issues) | **GET** /api/v1/actions/workspaces/{workspaceId}/ai/issues | Get Quality Issues
[**list_memory_items**](SmartFunctionsApi.md#list_memory_items) | **GET** /api/v1/actions/workspaces/{workspaceId}/ai/memory | (EXPERIMENTAL) List all memory items
[**remove_memory_item**](SmartFunctionsApi.md#remove_memory_item) | **DELETE** /api/v1/actions/workspaces/{workspaceId}/ai/memory/{memoryId} | (EXPERIMENTAL) Remove memory item
[**resolve_llm_endpoints**](SmartFunctionsApi.md#resolve_llm_endpoints) | **GET** /api/v1/actions/workspaces/{workspaceId}/ai/resolveLlmEndpoints | Get Active LLM Endpoints for this workspace
[**tags**](SmartFunctionsApi.md#tags) | **GET** /api/v1/actions/workspaces/{workspaceId}/ai/analyticsCatalog/tags | Get Analytics Catalog Tags
[**update_memory_item**](SmartFunctionsApi.md#update_memory_item) | **PUT** /api/v1/actions/workspaces/{workspaceId}/ai/memory/{memoryId} | (EXPERIMENTAL) Update memory item
[**validate_llm_endpoint**](SmartFunctionsApi.md#validate_llm_endpoint) | **POST** /api/v1/actions/ai/llmEndpoint/test | Validate LLM Endpoint
[**validate_llm_endpoint_by_id**](SmartFunctionsApi.md#validate_llm_endpoint_by_id) | **POST** /api/v1/actions/ai/llmEndpoint/{llmEndpointId}/test | Validate LLM Endpoint By Id


# **ai_chat**
> ChatResult ai_chat(workspace_id, chat_request)

(BETA) Chat with AI

(BETA) Combines multiple use cases such as search, create visualizations, ...

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.chat_request import ChatRequest
from gooddata_api_client.models.chat_result import ChatResult
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
    api_instance = gooddata_api_client.SmartFunctionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    chat_request = gooddata_api_client.ChatRequest() # ChatRequest | 

    try:
        # (BETA) Chat with AI
        api_response = api_instance.ai_chat(workspace_id, chat_request)
        print("The response of SmartFunctionsApi->ai_chat:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SmartFunctionsApi->ai_chat: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **chat_request** | [**ChatRequest**](ChatRequest.md)|  | 

### Return type

[**ChatResult**](ChatResult.md)

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

# **ai_chat_history**
> ChatHistoryResult ai_chat_history(workspace_id, chat_history_request)

(BETA) Get Chat History

(BETA) Post thread ID (and optionally interaction ID) to get full/partial chat history.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.chat_history_request import ChatHistoryRequest
from gooddata_api_client.models.chat_history_result import ChatHistoryResult
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
    api_instance = gooddata_api_client.SmartFunctionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    chat_history_request = gooddata_api_client.ChatHistoryRequest() # ChatHistoryRequest | 

    try:
        # (BETA) Get Chat History
        api_response = api_instance.ai_chat_history(workspace_id, chat_history_request)
        print("The response of SmartFunctionsApi->ai_chat_history:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SmartFunctionsApi->ai_chat_history: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **chat_history_request** | [**ChatHistoryRequest**](ChatHistoryRequest.md)|  | 

### Return type

[**ChatHistoryResult**](ChatHistoryResult.md)

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

# **ai_chat_stream**
> List[object] ai_chat_stream(workspace_id, chat_request)

(BETA) Chat with AI

(BETA) Combines multiple use cases such as search, create visualizations, ...

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.chat_request import ChatRequest
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
    api_instance = gooddata_api_client.SmartFunctionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    chat_request = gooddata_api_client.ChatRequest() # ChatRequest | 

    try:
        # (BETA) Chat with AI
        api_response = api_instance.ai_chat_stream(workspace_id, chat_request)
        print("The response of SmartFunctionsApi->ai_chat_stream:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SmartFunctionsApi->ai_chat_stream: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **chat_request** | [**ChatRequest**](ChatRequest.md)|  | 

### Return type

**List[object]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/event-stream

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ai_chat_usage**
> ChatUsageResponse ai_chat_usage(workspace_id)

Get Chat Usage

Returns usage statistics of chat for a user in a workspace.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.chat_usage_response import ChatUsageResponse
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
    api_instance = gooddata_api_client.SmartFunctionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier

    try:
        # Get Chat Usage
        api_response = api_instance.ai_chat_usage(workspace_id)
        print("The response of SmartFunctionsApi->ai_chat_usage:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SmartFunctionsApi->ai_chat_usage: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 

### Return type

[**ChatUsageResponse**](ChatUsageResponse.md)

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

# **ai_search**
> SearchResult ai_search(workspace_id, search_request)

(BETA) Semantic Search in Metadata

(BETA) Uses similarity (e.g. cosine distance) search to find top X most similar metadata objects.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.search_request import SearchRequest
from gooddata_api_client.models.search_result import SearchResult
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
    api_instance = gooddata_api_client.SmartFunctionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    search_request = gooddata_api_client.SearchRequest() # SearchRequest | 

    try:
        # (BETA) Semantic Search in Metadata
        api_response = api_instance.ai_search(workspace_id, search_request)
        print("The response of SmartFunctionsApi->ai_search:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SmartFunctionsApi->ai_search: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **search_request** | [**SearchRequest**](SearchRequest.md)|  | 

### Return type

[**SearchResult**](SearchResult.md)

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

# **anomaly_detection**
> SmartFunctionResponse anomaly_detection(workspace_id, result_id, anomaly_detection_request, skip_cache=skip_cache)

(EXPERIMENTAL) Smart functions - Anomaly Detection

(EXPERIMENTAL) Computes anomaly detection.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.anomaly_detection_request import AnomalyDetectionRequest
from gooddata_api_client.models.smart_function_response import SmartFunctionResponse
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
    api_instance = gooddata_api_client.SmartFunctionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    result_id = '9bd52018570364264fcf62d373da6bed313120e8' # str | Input result ID to be used in the computation
    anomaly_detection_request = gooddata_api_client.AnomalyDetectionRequest() # AnomalyDetectionRequest | 
    skip_cache = False # bool | Ignore all caches during execution of current request. (optional) (default to False)

    try:
        # (EXPERIMENTAL) Smart functions - Anomaly Detection
        api_response = api_instance.anomaly_detection(workspace_id, result_id, anomaly_detection_request, skip_cache=skip_cache)
        print("The response of SmartFunctionsApi->anomaly_detection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SmartFunctionsApi->anomaly_detection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **result_id** | **str**| Input result ID to be used in the computation | 
 **anomaly_detection_request** | [**AnomalyDetectionRequest**](AnomalyDetectionRequest.md)|  | 
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional] [default to False]

### Return type

[**SmartFunctionResponse**](SmartFunctionResponse.md)

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

# **anomaly_detection_result**
> AnomalyDetectionResult anomaly_detection_result(workspace_id, result_id, offset=offset, limit=limit)

(EXPERIMENTAL) Smart functions - Anomaly Detection Result

(EXPERIMENTAL) Gets anomalies.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.anomaly_detection_result import AnomalyDetectionResult
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
    api_instance = gooddata_api_client.SmartFunctionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    result_id = 'a9b28f9dc55f37ea9f4a5fb0c76895923591e781' # str | Result ID
    offset = 56 # int |  (optional)
    limit = 56 # int |  (optional)

    try:
        # (EXPERIMENTAL) Smart functions - Anomaly Detection Result
        api_response = api_instance.anomaly_detection_result(workspace_id, result_id, offset=offset, limit=limit)
        print("The response of SmartFunctionsApi->anomaly_detection_result:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SmartFunctionsApi->anomaly_detection_result: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **result_id** | **str**| Result ID | 
 **offset** | **int**|  | [optional] 
 **limit** | **int**|  | [optional] 

### Return type

[**AnomalyDetectionResult**](AnomalyDetectionResult.md)

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

# **clustering**
> SmartFunctionResponse clustering(workspace_id, result_id, clustering_request, skip_cache=skip_cache)

(EXPERIMENTAL) Smart functions - Clustering

(EXPERIMENTAL) Computes clusters for data points from the provided execution result and parameters.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.clustering_request import ClusteringRequest
from gooddata_api_client.models.smart_function_response import SmartFunctionResponse
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
    api_instance = gooddata_api_client.SmartFunctionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    result_id = '9bd52018570364264fcf62d373da6bed313120e8' # str | Input result ID to be used in the computation
    clustering_request = gooddata_api_client.ClusteringRequest() # ClusteringRequest | 
    skip_cache = False # bool | Ignore all caches during execution of current request. (optional) (default to False)

    try:
        # (EXPERIMENTAL) Smart functions - Clustering
        api_response = api_instance.clustering(workspace_id, result_id, clustering_request, skip_cache=skip_cache)
        print("The response of SmartFunctionsApi->clustering:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SmartFunctionsApi->clustering: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **result_id** | **str**| Input result ID to be used in the computation | 
 **clustering_request** | [**ClusteringRequest**](ClusteringRequest.md)|  | 
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional] [default to False]

### Return type

[**SmartFunctionResponse**](SmartFunctionResponse.md)

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

# **clustering_result**
> ClusteringResult clustering_result(workspace_id, result_id, offset=offset, limit=limit)

(EXPERIMENTAL) Smart functions - Clustering Result

(EXPERIMENTAL) Gets clustering result.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.clustering_result import ClusteringResult
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
    api_instance = gooddata_api_client.SmartFunctionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    result_id = 'a9b28f9dc55f37ea9f4a5fb0c76895923591e781' # str | Result ID
    offset = 56 # int |  (optional)
    limit = 56 # int |  (optional)

    try:
        # (EXPERIMENTAL) Smart functions - Clustering Result
        api_response = api_instance.clustering_result(workspace_id, result_id, offset=offset, limit=limit)
        print("The response of SmartFunctionsApi->clustering_result:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SmartFunctionsApi->clustering_result: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **result_id** | **str**| Result ID | 
 **offset** | **int**|  | [optional] 
 **limit** | **int**|  | [optional] 

### Return type

[**ClusteringResult**](ClusteringResult.md)

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

# **create_memory_item**
> MemoryItem create_memory_item(workspace_id, memory_item)

(EXPERIMENTAL) Create new memory item

(EXPERIMENTAL) Creates a new memory item and returns it

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.memory_item import MemoryItem
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
    api_instance = gooddata_api_client.SmartFunctionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    memory_item = gooddata_api_client.MemoryItem() # MemoryItem | 

    try:
        # (EXPERIMENTAL) Create new memory item
        api_response = api_instance.create_memory_item(workspace_id, memory_item)
        print("The response of SmartFunctionsApi->create_memory_item:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SmartFunctionsApi->create_memory_item: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **memory_item** | [**MemoryItem**](MemoryItem.md)|  | 

### Return type

[**MemoryItem**](MemoryItem.md)

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

# **forecast**
> SmartFunctionResponse forecast(workspace_id, result_id, forecast_request, skip_cache=skip_cache)

(BETA) Smart functions - Forecast

(BETA) Computes forecasted data points from the provided execution result and parameters.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.forecast_request import ForecastRequest
from gooddata_api_client.models.smart_function_response import SmartFunctionResponse
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
    api_instance = gooddata_api_client.SmartFunctionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    result_id = '9bd52018570364264fcf62d373da6bed313120e8' # str | Input result ID to be used in the computation
    forecast_request = gooddata_api_client.ForecastRequest() # ForecastRequest | 
    skip_cache = False # bool | Ignore all caches during execution of current request. (optional) (default to False)

    try:
        # (BETA) Smart functions - Forecast
        api_response = api_instance.forecast(workspace_id, result_id, forecast_request, skip_cache=skip_cache)
        print("The response of SmartFunctionsApi->forecast:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SmartFunctionsApi->forecast: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **result_id** | **str**| Input result ID to be used in the computation | 
 **forecast_request** | [**ForecastRequest**](ForecastRequest.md)|  | 
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional] [default to False]

### Return type

[**SmartFunctionResponse**](SmartFunctionResponse.md)

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

# **forecast_result**
> ForecastResult forecast_result(workspace_id, result_id, offset=offset, limit=limit)

(BETA) Smart functions - Forecast Result

(BETA) Gets forecast result.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.forecast_result import ForecastResult
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
    api_instance = gooddata_api_client.SmartFunctionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    result_id = 'a9b28f9dc55f37ea9f4a5fb0c76895923591e781' # str | Result ID
    offset = 56 # int |  (optional)
    limit = 56 # int |  (optional)

    try:
        # (BETA) Smart functions - Forecast Result
        api_response = api_instance.forecast_result(workspace_id, result_id, offset=offset, limit=limit)
        print("The response of SmartFunctionsApi->forecast_result:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SmartFunctionsApi->forecast_result: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **result_id** | **str**| Result ID | 
 **offset** | **int**|  | [optional] 
 **limit** | **int**|  | [optional] 

### Return type

[**ForecastResult**](ForecastResult.md)

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

# **get_memory_item**
> MemoryItem get_memory_item(workspace_id, memory_id)

(EXPERIMENTAL) Get memory item

(EXPERIMENTAL) Get memory item by id

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.memory_item import MemoryItem
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
    api_instance = gooddata_api_client.SmartFunctionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    memory_id = 'memory_id_example' # str | 

    try:
        # (EXPERIMENTAL) Get memory item
        api_response = api_instance.get_memory_item(workspace_id, memory_id)
        print("The response of SmartFunctionsApi->get_memory_item:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SmartFunctionsApi->get_memory_item: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **memory_id** | **str**|  | 

### Return type

[**MemoryItem**](MemoryItem.md)

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

# **get_quality_issues**
> GetQualityIssuesResponse get_quality_issues(workspace_id)

Get Quality Issues

Returns metadata quality issues detected by the platform linter.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.get_quality_issues_response import GetQualityIssuesResponse
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
    api_instance = gooddata_api_client.SmartFunctionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier

    try:
        # Get Quality Issues
        api_response = api_instance.get_quality_issues(workspace_id)
        print("The response of SmartFunctionsApi->get_quality_issues:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SmartFunctionsApi->get_quality_issues: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 

### Return type

[**GetQualityIssuesResponse**](GetQualityIssuesResponse.md)

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

# **list_memory_items**
> List[MemoryItem] list_memory_items(workspace_id)

(EXPERIMENTAL) List all memory items

(EXPERIMENTAL) Returns a list of memory items

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.memory_item import MemoryItem
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
    api_instance = gooddata_api_client.SmartFunctionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier

    try:
        # (EXPERIMENTAL) List all memory items
        api_response = api_instance.list_memory_items(workspace_id)
        print("The response of SmartFunctionsApi->list_memory_items:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SmartFunctionsApi->list_memory_items: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 

### Return type

[**List[MemoryItem]**](MemoryItem.md)

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

# **remove_memory_item**
> remove_memory_item(workspace_id, memory_id)

(EXPERIMENTAL) Remove memory item

(EXPERIMENTAL) Removes memory item

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
    api_instance = gooddata_api_client.SmartFunctionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    memory_id = 'memory_id_example' # str | 

    try:
        # (EXPERIMENTAL) Remove memory item
        api_instance.remove_memory_item(workspace_id, memory_id)
    except Exception as e:
        print("Exception when calling SmartFunctionsApi->remove_memory_item: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **memory_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resolve_llm_endpoints**
> ResolvedLlmEndpoints resolve_llm_endpoints(workspace_id)

Get Active LLM Endpoints for this workspace

Returns a list of available LLM Endpoints

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.resolved_llm_endpoints import ResolvedLlmEndpoints
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
    api_instance = gooddata_api_client.SmartFunctionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier

    try:
        # Get Active LLM Endpoints for this workspace
        api_response = api_instance.resolve_llm_endpoints(workspace_id)
        print("The response of SmartFunctionsApi->resolve_llm_endpoints:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SmartFunctionsApi->resolve_llm_endpoints: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 

### Return type

[**ResolvedLlmEndpoints**](ResolvedLlmEndpoints.md)

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

# **tags**
> AnalyticsCatalogTags tags(workspace_id)

Get Analytics Catalog Tags

Returns a list of tags for this workspace

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.analytics_catalog_tags import AnalyticsCatalogTags
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
    api_instance = gooddata_api_client.SmartFunctionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier

    try:
        # Get Analytics Catalog Tags
        api_response = api_instance.tags(workspace_id)
        print("The response of SmartFunctionsApi->tags:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SmartFunctionsApi->tags: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 

### Return type

[**AnalyticsCatalogTags**](AnalyticsCatalogTags.md)

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

# **update_memory_item**
> MemoryItem update_memory_item(workspace_id, memory_id, memory_item)

(EXPERIMENTAL) Update memory item

(EXPERIMENTAL) Updates memory item and returns it

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.memory_item import MemoryItem
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
    api_instance = gooddata_api_client.SmartFunctionsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace identifier
    memory_id = 'memory_id_example' # str | 
    memory_item = gooddata_api_client.MemoryItem() # MemoryItem | 

    try:
        # (EXPERIMENTAL) Update memory item
        api_response = api_instance.update_memory_item(workspace_id, memory_id, memory_item)
        print("The response of SmartFunctionsApi->update_memory_item:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SmartFunctionsApi->update_memory_item: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier | 
 **memory_id** | **str**|  | 
 **memory_item** | [**MemoryItem**](MemoryItem.md)|  | 

### Return type

[**MemoryItem**](MemoryItem.md)

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

# **validate_llm_endpoint**
> ValidateLLMEndpointResponse validate_llm_endpoint(validate_llm_endpoint_request)

Validate LLM Endpoint

Validates LLM endpoint with provided parameters.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.validate_llm_endpoint_request import ValidateLLMEndpointRequest
from gooddata_api_client.models.validate_llm_endpoint_response import ValidateLLMEndpointResponse
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
    api_instance = gooddata_api_client.SmartFunctionsApi(api_client)
    validate_llm_endpoint_request = gooddata_api_client.ValidateLLMEndpointRequest() # ValidateLLMEndpointRequest | 

    try:
        # Validate LLM Endpoint
        api_response = api_instance.validate_llm_endpoint(validate_llm_endpoint_request)
        print("The response of SmartFunctionsApi->validate_llm_endpoint:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SmartFunctionsApi->validate_llm_endpoint: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **validate_llm_endpoint_request** | [**ValidateLLMEndpointRequest**](ValidateLLMEndpointRequest.md)|  | 

### Return type

[**ValidateLLMEndpointResponse**](ValidateLLMEndpointResponse.md)

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

# **validate_llm_endpoint_by_id**
> ValidateLLMEndpointResponse validate_llm_endpoint_by_id(llm_endpoint_id, validate_llm_endpoint_by_id_request=validate_llm_endpoint_by_id_request)

Validate LLM Endpoint By Id

Validates existing LLM endpoint with provided parameters and updates it if they are valid.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.validate_llm_endpoint_by_id_request import ValidateLLMEndpointByIdRequest
from gooddata_api_client.models.validate_llm_endpoint_response import ValidateLLMEndpointResponse
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
    api_instance = gooddata_api_client.SmartFunctionsApi(api_client)
    llm_endpoint_id = 'llm_endpoint_id_example' # str | 
    validate_llm_endpoint_by_id_request = gooddata_api_client.ValidateLLMEndpointByIdRequest() # ValidateLLMEndpointByIdRequest |  (optional)

    try:
        # Validate LLM Endpoint By Id
        api_response = api_instance.validate_llm_endpoint_by_id(llm_endpoint_id, validate_llm_endpoint_by_id_request=validate_llm_endpoint_by_id_request)
        print("The response of SmartFunctionsApi->validate_llm_endpoint_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SmartFunctionsApi->validate_llm_endpoint_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **llm_endpoint_id** | **str**|  | 
 **validate_llm_endpoint_by_id_request** | [**ValidateLLMEndpointByIdRequest**](ValidateLLMEndpointByIdRequest.md)|  | [optional] 

### Return type

[**ValidateLLMEndpointResponse**](ValidateLLMEndpointResponse.md)

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


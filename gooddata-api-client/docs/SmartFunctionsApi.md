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
import time
import gooddata_api_client
from gooddata_api_client.api import smart_functions_api
from gooddata_api_client.model.chat_result import ChatResult
from gooddata_api_client.model.chat_request import ChatRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    chat_request = ChatRequest(
        limit_create=3,
        limit_create_context=10,
        limit_search=5,
        question="question_example",
        relevant_score_threshold=0.45,
        search_score_threshold=0.9,
        thread_id_suffix="thread_id_suffix_example",
        title_to_descriptor_ratio=0.7,
        user_context=UserContext(
            active_object=ActiveObjectIdentification(
                id="id_example",
                type="type_example",
                workspace_id="workspace_id_example",
            ),
        ),
    ) # ChatRequest | 

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Chat with AI
        api_response = api_instance.ai_chat(workspace_id, chat_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import smart_functions_api
from gooddata_api_client.model.chat_history_result import ChatHistoryResult
from gooddata_api_client.model.chat_history_request import ChatHistoryRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    chat_history_request = ChatHistoryRequest(
        chat_history_interaction_id="chat_history_interaction_id_example",
        reset=True,
        response_state="SUCCESSFUL",
        saved_visualization=SavedVisualization(
            created_visualization_id="created_visualization_id_example",
            saved_visualization_id="saved_visualization_id_example",
        ),
        thread_id_suffix="thread_id_suffix_example",
        user_feedback="POSITIVE",
    ) # ChatHistoryRequest | 

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Get Chat History
        api_response = api_instance.ai_chat_history(workspace_id, chat_history_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
> [dict] ai_chat_stream(workspace_id, chat_request)

(BETA) Chat with AI

(BETA) Combines multiple use cases such as search, create visualizations, ...

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import smart_functions_api
from gooddata_api_client.model.chat_request import ChatRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    chat_request = ChatRequest(
        limit_create=3,
        limit_create_context=10,
        limit_search=5,
        question="question_example",
        relevant_score_threshold=0.45,
        search_score_threshold=0.9,
        thread_id_suffix="thread_id_suffix_example",
        title_to_descriptor_ratio=0.7,
        user_context=UserContext(
            active_object=ActiveObjectIdentification(
                id="id_example",
                type="type_example",
                workspace_id="workspace_id_example",
            ),
        ),
    ) # ChatRequest | 

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Chat with AI
        api_response = api_instance.ai_chat_stream(workspace_id, chat_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->ai_chat_stream: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **chat_request** | [**ChatRequest**](ChatRequest.md)|  |

### Return type

**[dict]**

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
import time
import gooddata_api_client
from gooddata_api_client.api import smart_functions_api
from gooddata_api_client.model.chat_usage_response import ChatUsageResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier

    # example passing only required values which don't have defaults set
    try:
        # Get Chat Usage
        api_response = api_instance.ai_chat_usage(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import smart_functions_api
from gooddata_api_client.model.search_result import SearchResult
from gooddata_api_client.model.search_request import SearchRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    search_request = SearchRequest(
        deep_search=False,
        include_hidden=False,
        limit=10,
        object_types=[
            "attribute",
        ],
        question="question_example",
        relevant_score_threshold=0.3,
        title_to_descriptor_ratio=0.7,
    ) # SearchRequest | 

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Semantic Search in Metadata
        api_response = api_instance.ai_search(workspace_id, search_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
> SmartFunctionResponse anomaly_detection(workspace_id, result_id, anomaly_detection_request)

(EXPERIMENTAL) Smart functions - Anomaly Detection

(EXPERIMENTAL) Computes anomaly detection.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import smart_functions_api
from gooddata_api_client.model.anomaly_detection_request import AnomalyDetectionRequest
from gooddata_api_client.model.smart_function_response import SmartFunctionResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    result_id = "9bd52018570364264fcf62d373da6bed313120e8" # str | Input result ID to be used in the computation
    anomaly_detection_request = AnomalyDetectionRequest(
        sensitivity=3.14,
    ) # AnomalyDetectionRequest | 
    skip_cache = False # bool | Ignore all caches during execution of current request. (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Smart functions - Anomaly Detection
        api_response = api_instance.anomaly_detection(workspace_id, result_id, anomaly_detection_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->anomaly_detection: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (EXPERIMENTAL) Smart functions - Anomaly Detection
        api_response = api_instance.anomaly_detection(workspace_id, result_id, anomaly_detection_request, skip_cache=skip_cache)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->anomaly_detection: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **result_id** | **str**| Input result ID to be used in the computation |
 **anomaly_detection_request** | [**AnomalyDetectionRequest**](AnomalyDetectionRequest.md)|  |
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional] if omitted the server will use the default value of False

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
> AnomalyDetectionResult anomaly_detection_result(workspace_id, result_id)

(EXPERIMENTAL) Smart functions - Anomaly Detection Result

(EXPERIMENTAL) Gets anomalies.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import smart_functions_api
from gooddata_api_client.model.anomaly_detection_result import AnomalyDetectionResult
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    result_id = "a9b28f9dc55f37ea9f4a5fb0c76895923591e781" # str | Result ID
    offset = 1 # int |  (optional)
    limit = 1 # int |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Smart functions - Anomaly Detection Result
        api_response = api_instance.anomaly_detection_result(workspace_id, result_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->anomaly_detection_result: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (EXPERIMENTAL) Smart functions - Anomaly Detection Result
        api_response = api_instance.anomaly_detection_result(workspace_id, result_id, offset=offset, limit=limit)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
> SmartFunctionResponse clustering(workspace_id, result_id, clustering_request)

(EXPERIMENTAL) Smart functions - Clustering

(EXPERIMENTAL) Computes clusters for data points from the provided execution result and parameters.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import smart_functions_api
from gooddata_api_client.model.clustering_request import ClusteringRequest
from gooddata_api_client.model.smart_function_response import SmartFunctionResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    result_id = "9bd52018570364264fcf62d373da6bed313120e8" # str | Input result ID to be used in the computation
    clustering_request = ClusteringRequest(
        number_of_clusters=1,
        threshold=0.03,
    ) # ClusteringRequest | 
    skip_cache = False # bool | Ignore all caches during execution of current request. (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Smart functions - Clustering
        api_response = api_instance.clustering(workspace_id, result_id, clustering_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->clustering: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (EXPERIMENTAL) Smart functions - Clustering
        api_response = api_instance.clustering(workspace_id, result_id, clustering_request, skip_cache=skip_cache)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->clustering: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **result_id** | **str**| Input result ID to be used in the computation |
 **clustering_request** | [**ClusteringRequest**](ClusteringRequest.md)|  |
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional] if omitted the server will use the default value of False

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
> ClusteringResult clustering_result(workspace_id, result_id)

(EXPERIMENTAL) Smart functions - Clustering Result

(EXPERIMENTAL) Gets clustering result.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import smart_functions_api
from gooddata_api_client.model.clustering_result import ClusteringResult
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    result_id = "a9b28f9dc55f37ea9f4a5fb0c76895923591e781" # str | Result ID
    offset = 1 # int |  (optional)
    limit = 1 # int |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Smart functions - Clustering Result
        api_response = api_instance.clustering_result(workspace_id, result_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->clustering_result: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (EXPERIMENTAL) Smart functions - Clustering Result
        api_response = api_instance.clustering_result(workspace_id, result_id, offset=offset, limit=limit)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import smart_functions_api
from gooddata_api_client.model.memory_item import MemoryItem
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    memory_item = MemoryItem(
        id="id_example",
        instruction="instruction_example",
        keywords=[
            "keywords_example",
        ],
        strategy="MEMORY_ITEM_STRATEGY_ALLWAYS",
        use_cases=MemoryItemUseCases(
            general=True,
            howto=True,
            keywords=True,
            metric=True,
            normalize=True,
            router=True,
            search=True,
            visualization=True,
        ),
    ) # MemoryItem | 

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Create new memory item
        api_response = api_instance.create_memory_item(workspace_id, memory_item)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
> SmartFunctionResponse forecast(workspace_id, result_id, forecast_request)

(BETA) Smart functions - Forecast

(BETA) Computes forecasted data points from the provided execution result and parameters.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import smart_functions_api
from gooddata_api_client.model.forecast_request import ForecastRequest
from gooddata_api_client.model.smart_function_response import SmartFunctionResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    result_id = "9bd52018570364264fcf62d373da6bed313120e8" # str | Input result ID to be used in the computation
    forecast_request = ForecastRequest(
        confidence_level=0.95,
        forecast_period=1,
        seasonal=False,
    ) # ForecastRequest | 
    skip_cache = False # bool | Ignore all caches during execution of current request. (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Smart functions - Forecast
        api_response = api_instance.forecast(workspace_id, result_id, forecast_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->forecast: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) Smart functions - Forecast
        api_response = api_instance.forecast(workspace_id, result_id, forecast_request, skip_cache=skip_cache)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->forecast: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **result_id** | **str**| Input result ID to be used in the computation |
 **forecast_request** | [**ForecastRequest**](ForecastRequest.md)|  |
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional] if omitted the server will use the default value of False

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
> ForecastResult forecast_result(workspace_id, result_id)

(BETA) Smart functions - Forecast Result

(BETA) Gets forecast result.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import smart_functions_api
from gooddata_api_client.model.forecast_result import ForecastResult
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    result_id = "a9b28f9dc55f37ea9f4a5fb0c76895923591e781" # str | Result ID
    offset = 1 # int |  (optional)
    limit = 1 # int |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Smart functions - Forecast Result
        api_response = api_instance.forecast_result(workspace_id, result_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->forecast_result: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) Smart functions - Forecast Result
        api_response = api_instance.forecast_result(workspace_id, result_id, offset=offset, limit=limit)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import smart_functions_api
from gooddata_api_client.model.memory_item import MemoryItem
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    memory_id = "memoryId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Get memory item
        api_response = api_instance.get_memory_item(workspace_id, memory_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import smart_functions_api
from gooddata_api_client.model.get_quality_issues_response import GetQualityIssuesResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier

    # example passing only required values which don't have defaults set
    try:
        # Get Quality Issues
        api_response = api_instance.get_quality_issues(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
> [MemoryItem] list_memory_items(workspace_id)

(EXPERIMENTAL) List all memory items

(EXPERIMENTAL) Returns a list of memory items

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import smart_functions_api
from gooddata_api_client.model.memory_item import MemoryItem
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) List all memory items
        api_response = api_instance.list_memory_items(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->list_memory_items: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |

### Return type

[**[MemoryItem]**](MemoryItem.md)

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
import time
import gooddata_api_client
from gooddata_api_client.api import smart_functions_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    memory_id = "memoryId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Remove memory item
        api_instance.remove_memory_item(workspace_id, memory_id)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import smart_functions_api
from gooddata_api_client.model.resolved_llm_endpoints import ResolvedLlmEndpoints
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier

    # example passing only required values which don't have defaults set
    try:
        # Get Active LLM Endpoints for this workspace
        api_response = api_instance.resolve_llm_endpoints(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import smart_functions_api
from gooddata_api_client.model.analytics_catalog_tags import AnalyticsCatalogTags
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier

    # example passing only required values which don't have defaults set
    try:
        # Get Analytics Catalog Tags
        api_response = api_instance.tags(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import smart_functions_api
from gooddata_api_client.model.memory_item import MemoryItem
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    memory_id = "memoryId_example" # str | 
    memory_item = MemoryItem(
        id="id_example",
        instruction="instruction_example",
        keywords=[
            "keywords_example",
        ],
        strategy="MEMORY_ITEM_STRATEGY_ALLWAYS",
        use_cases=MemoryItemUseCases(
            general=True,
            howto=True,
            keywords=True,
            metric=True,
            normalize=True,
            router=True,
            search=True,
            visualization=True,
        ),
    ) # MemoryItem | 

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Update memory item
        api_response = api_instance.update_memory_item(workspace_id, memory_id, memory_item)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import smart_functions_api
from gooddata_api_client.model.validate_llm_endpoint_response import ValidateLLMEndpointResponse
from gooddata_api_client.model.validate_llm_endpoint_request import ValidateLLMEndpointRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    validate_llm_endpoint_request = ValidateLLMEndpointRequest(
        base_url="base_url_example",
        llm_model="llm_model_example",
        llm_organization="llm_organization_example",
        provider="provider_example",
        token="token_example",
    ) # ValidateLLMEndpointRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Validate LLM Endpoint
        api_response = api_instance.validate_llm_endpoint(validate_llm_endpoint_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
> ValidateLLMEndpointResponse validate_llm_endpoint_by_id(llm_endpoint_id)

Validate LLM Endpoint By Id

Validates existing LLM endpoint with provided parameters and updates it if they are valid.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import smart_functions_api
from gooddata_api_client.model.validate_llm_endpoint_response import ValidateLLMEndpointResponse
from gooddata_api_client.model.validate_llm_endpoint_by_id_request import ValidateLLMEndpointByIdRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    llm_endpoint_id = "llmEndpointId_example" # str | 
    validate_llm_endpoint_by_id_request = ValidateLLMEndpointByIdRequest(
        base_url="base_url_example",
        llm_model="llm_model_example",
        llm_organization="llm_organization_example",
        provider="provider_example",
        token="token_example",
    ) # ValidateLLMEndpointByIdRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Validate LLM Endpoint By Id
        api_response = api_instance.validate_llm_endpoint_by_id(llm_endpoint_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->validate_llm_endpoint_by_id: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Validate LLM Endpoint By Id
        api_response = api_instance.validate_llm_endpoint_by_id(llm_endpoint_id, validate_llm_endpoint_by_id_request=validate_llm_endpoint_by_id_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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


<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.smart_functions_api.SmartFunctionsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**ai_chat**](#ai_chat) | **post** /api/v1/actions/workspaces/{workspaceId}/ai/chat | (BETA) Chat with AI
[**ai_chat_history**](#ai_chat_history) | **post** /api/v1/actions/workspaces/{workspaceId}/ai/chatHistory | (BETA) Get Chat History
[**ai_chat_stream**](#ai_chat_stream) | **post** /api/v1/actions/workspaces/{workspaceId}/ai/chatStream | (BETA) Chat with AI
[**ai_chat_usage**](#ai_chat_usage) | **get** /api/v1/actions/workspaces/{workspaceId}/ai/chatUsage | Get Chat Usage
[**ai_search**](#ai_search) | **post** /api/v1/actions/workspaces/{workspaceId}/ai/search | (BETA) Semantic Search in Metadata
[**anomaly_detection**](#anomaly_detection) | **post** /api/v1/actions/workspaces/{workspaceId}/execution/functions/anomalyDetection/{resultId} | (EXPERIMENTAL) Smart functions - Anomaly Detection
[**anomaly_detection_result**](#anomaly_detection_result) | **get** /api/v1/actions/workspaces/{workspaceId}/execution/functions/anomalyDetection/result/{resultId} | (EXPERIMENTAL) Smart functions - Anomaly Detection Result
[**clustering**](#clustering) | **post** /api/v1/actions/workspaces/{workspaceId}/execution/functions/clustering/{resultId} | (EXPERIMENTAL) Smart functions - Clustering
[**clustering_result**](#clustering_result) | **get** /api/v1/actions/workspaces/{workspaceId}/execution/functions/clustering/result/{resultId} | (EXPERIMENTAL) Smart functions - Clustering Result
[**created_by**](#created_by) | **get** /api/v1/actions/workspaces/{workspaceId}/ai/analyticsCatalog/createdBy | Get Analytics Catalog CreatedBy Users
[**forecast**](#forecast) | **post** /api/v1/actions/workspaces/{workspaceId}/execution/functions/forecast/{resultId} | (BETA) Smart functions - Forecast
[**forecast_result**](#forecast_result) | **get** /api/v1/actions/workspaces/{workspaceId}/execution/functions/forecast/result/{resultId} | (BETA) Smart functions - Forecast Result
[**generate_description**](#generate_description) | **post** /api/v1/actions/workspaces/{workspaceId}/ai/analyticsCatalog/generateDescription | Generate Description for Analytics Object
[**generate_title**](#generate_title) | **post** /api/v1/actions/workspaces/{workspaceId}/ai/analyticsCatalog/generateTitle | Generate Title for Analytics Object
[**get_quality_issues**](#get_quality_issues) | **get** /api/v1/actions/workspaces/{workspaceId}/ai/issues | Get Quality Issues
[**get_quality_issues_calculation_status**](#get_quality_issues_calculation_status) | **get** /api/v1/actions/workspaces/{workspaceId}/ai/issues/status/{processId} | Get Quality Issues Calculation Status
[**memory_created_by_users**](#memory_created_by_users) | **get** /api/v1/actions/workspaces/{workspaceId}/ai/memory/createdBy | Get AI Memory CreatedBy Users
[**resolve_llm_endpoints**](#resolve_llm_endpoints) | **get** /api/v1/actions/workspaces/{workspaceId}/ai/resolveLlmEndpoints | Get Active LLM Endpoints for this workspace
[**tags**](#tags) | **get** /api/v1/actions/workspaces/{workspaceId}/ai/analyticsCatalog/tags | Get Analytics Catalog Tags
[**test_llm_provider**](#test_llm_provider) | **post** /api/v1/actions/ai/llmProvider/test | Test LLM Provider
[**test_llm_provider_by_id**](#test_llm_provider_by_id) | **post** /api/v1/actions/ai/llmProvider/{llmProviderId}/test | Test LLM Provider By Id
[**trigger_quality_issues_calculation**](#trigger_quality_issues_calculation) | **post** /api/v1/actions/workspaces/{workspaceId}/ai/issues/triggerCheck | Trigger Quality Issues Calculation
[**validate_llm_endpoint**](#validate_llm_endpoint) | **post** /api/v1/actions/ai/llmEndpoint/test | Validate LLM Endpoint
[**validate_llm_endpoint_by_id**](#validate_llm_endpoint_by_id) | **post** /api/v1/actions/ai/llmEndpoint/{llmEndpointId}/test | Validate LLM Endpoint By Id

# **ai_chat**
<a id="ai_chat"></a>
> ChatResult ai_chat(workspace_idchat_request)

(BETA) Chat with AI

(BETA) Combines multiple use cases such as search, create visualizations, ...

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import smart_functions_api
from gooddata_api_client.model.chat_result import ChatResult
from gooddata_api_client.model.chat_request import ChatRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
    }
    body = ChatRequest(
        allowed_relationship_types=[
            AllowedRelationshipType(
                allow_orphans=True,
                source_type="attribute",
                target_type="attribute",
            )
        ],
        include_hidden=False,
        limit_create=3,
        limit_create_context=10,
        limit_search=5,
        object_types=[
            "attribute"
        ],
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
    )
    try:
        # (BETA) Chat with AI
        api_response = api_instance.ai_chat(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->ai_chat: %s\n" % e)
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
[**ChatRequest**](../../models/ChatRequest.md) |  | 


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
200 | [ApiResponseFor200](#ai_chat.ApiResponseFor200) | OK

#### ai_chat.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ChatResult**](../../models/ChatResult.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **ai_chat_history**
<a id="ai_chat_history"></a>
> ChatHistoryResult ai_chat_history(workspace_idchat_history_request)

(BETA) Get Chat History

(BETA) Post thread ID (and optionally interaction ID) to get full/partial chat history.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import smart_functions_api
from gooddata_api_client.model.chat_history_result import ChatHistoryResult
from gooddata_api_client.model.chat_history_request import ChatHistoryRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
    }
    body = ChatHistoryRequest(
        chat_history_interaction_id="chat_history_interaction_id_example",
        reset=True,
        response_state="SUCCESSFUL",
        saved_visualization=SavedVisualization(
            created_visualization_id="created_visualization_id_example",
            saved_visualization_id="saved_visualization_id_example",
        ),
        thread_id_suffix="thread_id_suffix_example",
        user_feedback="POSITIVE",
        user_text_feedback="user_text_feedback_example",
    )
    try:
        # (BETA) Get Chat History
        api_response = api_instance.ai_chat_history(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->ai_chat_history: %s\n" % e)
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
[**ChatHistoryRequest**](../../models/ChatHistoryRequest.md) |  | 


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
200 | [ApiResponseFor200](#ai_chat_history.ApiResponseFor200) | OK

#### ai_chat_history.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ChatHistoryResult**](../../models/ChatHistoryResult.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **ai_chat_stream**
<a id="ai_chat_stream"></a>
> [object] ai_chat_stream(workspace_idchat_request)

(BETA) Chat with AI

(BETA) Combines multiple use cases such as search, create visualizations, ...

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import smart_functions_api
from gooddata_api_client.model.chat_request import ChatRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
    }
    body = ChatRequest(
        allowed_relationship_types=[
            AllowedRelationshipType(
                allow_orphans=True,
                source_type="attribute",
                target_type="attribute",
            )
        ],
        include_hidden=False,
        limit_create=3,
        limit_create_context=10,
        limit_search=5,
        object_types=[
            "attribute"
        ],
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
    )
    try:
        # (BETA) Chat with AI
        api_response = api_instance.ai_chat_stream(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->ai_chat_stream: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('text/event-stream', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ChatRequest**](../../models/ChatRequest.md) |  | 


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
200 | [ApiResponseFor200](#ai_chat_stream.ApiResponseFor200) | OK

#### ai_chat_stream.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyTextEventStream, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyTextEventStream

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[items](#items) | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

# items

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **ai_chat_usage**
<a id="ai_chat_usage"></a>
> ChatUsageResponse ai_chat_usage(workspace_id)

Get Chat Usage

Returns usage statistics of chat for a user in a workspace.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import smart_functions_api
from gooddata_api_client.model.chat_usage_response import ChatUsageResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
    }
    try:
        # Get Chat Usage
        api_response = api_instance.ai_chat_usage(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->ai_chat_usage: %s\n" % e)
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

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#ai_chat_usage.ApiResponseFor200) | OK

#### ai_chat_usage.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ChatUsageResponse**](../../models/ChatUsageResponse.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **ai_search**
<a id="ai_search"></a>
> SearchResult ai_search(workspace_idsearch_request)

(BETA) Semantic Search in Metadata

(BETA) Uses similarity (e.g. cosine distance) search to find top X most similar metadata objects.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import smart_functions_api
from gooddata_api_client.model.search_result import SearchResult
from gooddata_api_client.model.search_request import SearchRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
    }
    body = SearchRequest(
        allowed_relationship_types=[
            AllowedRelationshipType(
                allow_orphans=True,
                source_type="attribute",
                target_type="attribute",
            )
        ],
        deep_search=False,
        enable_hybrid_search=False,
        exclude_tags=[
            "exclude_tags_example"
        ],
        include_hidden=False,
        include_tags=[
            "include_tags_example"
        ],
        limit=10,
        object_types=[
            "attribute"
        ],
        question="question_example",
        relevant_score_threshold=0.3,
        title_to_descriptor_ratio=0.7,
    )
    try:
        # (BETA) Semantic Search in Metadata
        api_response = api_instance.ai_search(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->ai_search: %s\n" % e)
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
[**SearchRequest**](../../models/SearchRequest.md) |  | 


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
200 | [ApiResponseFor200](#ai_search.ApiResponseFor200) | OK

#### ai_search.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**SearchResult**](../../models/SearchResult.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **anomaly_detection**
<a id="anomaly_detection"></a>
> SmartFunctionResponse anomaly_detection(workspace_idresult_idanomaly_detection_request)

(EXPERIMENTAL) Smart functions - Anomaly Detection

(EXPERIMENTAL) Computes anomaly detection.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import smart_functions_api
from gooddata_api_client.model.anomaly_detection_request import AnomalyDetectionRequest
from gooddata_api_client.model.smart_function_response import SmartFunctionResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
        'resultId': "9bd52018570364264fcf62d373da6bed313120e8",
    }
    header_params = {
    }
    body = AnomalyDetectionRequest(
        sensitivity=3.14,
    )
    try:
        # (EXPERIMENTAL) Smart functions - Anomaly Detection
        api_response = api_instance.anomaly_detection(
            path_params=path_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->anomaly_detection: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
        'resultId': "9bd52018570364264fcf62d373da6bed313120e8",
    }
    header_params = {
        'skip-cache': False,
    }
    body = AnomalyDetectionRequest(
        sensitivity=3.14,
    )
    try:
        # (EXPERIMENTAL) Smart functions - Anomaly Detection
        api_response = api_instance.anomaly_detection(
            path_params=path_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->anomaly_detection: %s\n" % e)
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
[**AnomalyDetectionRequest**](../../models/AnomalyDetectionRequest.md) |  | 


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
200 | [ApiResponseFor200](#anomaly_detection.ApiResponseFor200) | OK

#### anomaly_detection.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**SmartFunctionResponse**](../../models/SmartFunctionResponse.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **anomaly_detection_result**
<a id="anomaly_detection_result"></a>
> AnomalyDetectionResult anomaly_detection_result(workspace_idresult_id)

(EXPERIMENTAL) Smart functions - Anomaly Detection Result

(EXPERIMENTAL) Gets anomalies.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import smart_functions_api
from gooddata_api_client.model.anomaly_detection_result import AnomalyDetectionResult
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
        'resultId': "a9b28f9dc55f37ea9f4a5fb0c76895923591e781",
    }
    query_params = {
    }
    try:
        # (EXPERIMENTAL) Smart functions - Anomaly Detection Result
        api_response = api_instance.anomaly_detection_result(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->anomaly_detection_result: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
        'resultId': "a9b28f9dc55f37ea9f4a5fb0c76895923591e781",
    }
    query_params = {
        'offset': 1,
        'limit': 1,
    }
    try:
        # (EXPERIMENTAL) Smart functions - Anomaly Detection Result
        api_response = api_instance.anomaly_detection_result(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->anomaly_detection_result: %s\n" % e)
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


# OffsetSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | value must be a 32 bit integer

# LimitSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | value must be a 32 bit integer

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
200 | [ApiResponseFor200](#anomaly_detection_result.ApiResponseFor200) | OK

#### anomaly_detection_result.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**AnomalyDetectionResult**](../../models/AnomalyDetectionResult.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **clustering**
<a id="clustering"></a>
> SmartFunctionResponse clustering(workspace_idresult_idclustering_request)

(EXPERIMENTAL) Smart functions - Clustering

(EXPERIMENTAL) Computes clusters for data points from the provided execution result and parameters.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import smart_functions_api
from gooddata_api_client.model.clustering_request import ClusteringRequest
from gooddata_api_client.model.smart_function_response import SmartFunctionResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
        'resultId': "9bd52018570364264fcf62d373da6bed313120e8",
    }
    header_params = {
    }
    body = ClusteringRequest(
        number_of_clusters=1,
        threshold=0.03,
    )
    try:
        # (EXPERIMENTAL) Smart functions - Clustering
        api_response = api_instance.clustering(
            path_params=path_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->clustering: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
        'resultId': "9bd52018570364264fcf62d373da6bed313120e8",
    }
    header_params = {
        'skip-cache': False,
    }
    body = ClusteringRequest(
        number_of_clusters=1,
        threshold=0.03,
    )
    try:
        # (EXPERIMENTAL) Smart functions - Clustering
        api_response = api_instance.clustering(
            path_params=path_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->clustering: %s\n" % e)
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
[**ClusteringRequest**](../../models/ClusteringRequest.md) |  | 


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
200 | [ApiResponseFor200](#clustering.ApiResponseFor200) | OK

#### clustering.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**SmartFunctionResponse**](../../models/SmartFunctionResponse.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **clustering_result**
<a id="clustering_result"></a>
> ClusteringResult clustering_result(workspace_idresult_id)

(EXPERIMENTAL) Smart functions - Clustering Result

(EXPERIMENTAL) Gets clustering result.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import smart_functions_api
from gooddata_api_client.model.clustering_result import ClusteringResult
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
        'resultId': "a9b28f9dc55f37ea9f4a5fb0c76895923591e781",
    }
    query_params = {
    }
    try:
        # (EXPERIMENTAL) Smart functions - Clustering Result
        api_response = api_instance.clustering_result(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->clustering_result: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
        'resultId': "a9b28f9dc55f37ea9f4a5fb0c76895923591e781",
    }
    query_params = {
        'offset': 1,
        'limit': 1,
    }
    try:
        # (EXPERIMENTAL) Smart functions - Clustering Result
        api_response = api_instance.clustering_result(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->clustering_result: %s\n" % e)
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


# OffsetSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | value must be a 32 bit integer

# LimitSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | value must be a 32 bit integer

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
200 | [ApiResponseFor200](#clustering_result.ApiResponseFor200) | OK

#### clustering_result.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ClusteringResult**](../../models/ClusteringResult.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **created_by**
<a id="created_by"></a>
> AnalyticsCatalogCreatedBy created_by(workspace_id)

Get Analytics Catalog CreatedBy Users

Returns a list of Users who created any object for this workspace

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import smart_functions_api
from gooddata_api_client.model.analytics_catalog_created_by import AnalyticsCatalogCreatedBy
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
    }
    try:
        # Get Analytics Catalog CreatedBy Users
        api_response = api_instance.created_by(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->created_by: %s\n" % e)
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

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#created_by.ApiResponseFor200) | OK

#### created_by.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**AnalyticsCatalogCreatedBy**](../../models/AnalyticsCatalogCreatedBy.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **forecast**
<a id="forecast"></a>
> SmartFunctionResponse forecast(workspace_idresult_idforecast_request)

(BETA) Smart functions - Forecast

(BETA) Computes forecasted data points from the provided execution result and parameters.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import smart_functions_api
from gooddata_api_client.model.forecast_request import ForecastRequest
from gooddata_api_client.model.smart_function_response import SmartFunctionResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
        'resultId': "9bd52018570364264fcf62d373da6bed313120e8",
    }
    header_params = {
    }
    body = ForecastRequest(
        confidence_level=0.95,
        forecast_period=1,
        seasonal=False,
    )
    try:
        # (BETA) Smart functions - Forecast
        api_response = api_instance.forecast(
            path_params=path_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->forecast: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
        'resultId': "9bd52018570364264fcf62d373da6bed313120e8",
    }
    header_params = {
        'skip-cache': False,
    }
    body = ForecastRequest(
        confidence_level=0.95,
        forecast_period=1,
        seasonal=False,
    )
    try:
        # (BETA) Smart functions - Forecast
        api_response = api_instance.forecast(
            path_params=path_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->forecast: %s\n" % e)
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
[**ForecastRequest**](../../models/ForecastRequest.md) |  | 


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
200 | [ApiResponseFor200](#forecast.ApiResponseFor200) | OK

#### forecast.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**SmartFunctionResponse**](../../models/SmartFunctionResponse.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **forecast_result**
<a id="forecast_result"></a>
> ForecastResult forecast_result(workspace_idresult_id)

(BETA) Smart functions - Forecast Result

(BETA) Gets forecast result.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import smart_functions_api
from gooddata_api_client.model.forecast_result import ForecastResult
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
        'resultId': "a9b28f9dc55f37ea9f4a5fb0c76895923591e781",
    }
    query_params = {
    }
    try:
        # (BETA) Smart functions - Forecast Result
        api_response = api_instance.forecast_result(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->forecast_result: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
        'resultId': "a9b28f9dc55f37ea9f4a5fb0c76895923591e781",
    }
    query_params = {
        'offset': 1,
        'limit': 1,
    }
    try:
        # (BETA) Smart functions - Forecast Result
        api_response = api_instance.forecast_result(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->forecast_result: %s\n" % e)
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


# OffsetSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | value must be a 32 bit integer

# LimitSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | value must be a 32 bit integer

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
200 | [ApiResponseFor200](#forecast_result.ApiResponseFor200) | OK

#### forecast_result.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ForecastResult**](../../models/ForecastResult.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **generate_description**
<a id="generate_description"></a>
> GenerateDescriptionResponse generate_description(workspace_idgenerate_description_request)

Generate Description for Analytics Object

Generates a description for the specified analytics object. Returns description and a note with details if generation was not performed.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import smart_functions_api
from gooddata_api_client.model.generate_description_request import GenerateDescriptionRequest
from gooddata_api_client.model.generate_description_response import GenerateDescriptionResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
    }
    body = GenerateDescriptionRequest(
        object_id="object_id_example",
        object_type="Visualization",
    )
    try:
        # Generate Description for Analytics Object
        api_response = api_instance.generate_description(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->generate_description: %s\n" % e)
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
[**GenerateDescriptionRequest**](../../models/GenerateDescriptionRequest.md) |  | 


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
200 | [ApiResponseFor200](#generate_description.ApiResponseFor200) | OK

#### generate_description.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**GenerateDescriptionResponse**](../../models/GenerateDescriptionResponse.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **generate_title**
<a id="generate_title"></a>
> GenerateTitleResponse generate_title(workspace_idgenerate_title_request)

Generate Title for Analytics Object

Generates a title for the specified analytics object. Returns title and a note with details if generation was not performed.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import smart_functions_api
from gooddata_api_client.model.generate_title_request import GenerateTitleRequest
from gooddata_api_client.model.generate_title_response import GenerateTitleResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
    }
    body = GenerateTitleRequest(
        object_id="object_id_example",
        object_type="Visualization",
    )
    try:
        # Generate Title for Analytics Object
        api_response = api_instance.generate_title(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->generate_title: %s\n" % e)
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
[**GenerateTitleRequest**](../../models/GenerateTitleRequest.md) |  | 


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
200 | [ApiResponseFor200](#generate_title.ApiResponseFor200) | OK

#### generate_title.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**GenerateTitleResponse**](../../models/GenerateTitleResponse.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_quality_issues**
<a id="get_quality_issues"></a>
> GetQualityIssuesResponse get_quality_issues(workspace_id)

Get Quality Issues

Returns metadata quality issues detected by the platform linter.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import smart_functions_api
from gooddata_api_client.model.get_quality_issues_response import GetQualityIssuesResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
    }
    try:
        # Get Quality Issues
        api_response = api_instance.get_quality_issues(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->get_quality_issues: %s\n" % e)
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

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_quality_issues.ApiResponseFor200) | OK

#### get_quality_issues.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**GetQualityIssuesResponse**](../../models/GetQualityIssuesResponse.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_quality_issues_calculation_status**
<a id="get_quality_issues_calculation_status"></a>
> QualityIssuesCalculationStatusResponse get_quality_issues_calculation_status(workspace_idprocess_id)

Get Quality Issues Calculation Status

Returns the status of a quality issues calculation process identified by process ID.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import smart_functions_api
from gooddata_api_client.model.quality_issues_calculation_status_response import QualityIssuesCalculationStatusResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
        'processId': "processId_example",
    }
    try:
        # Get Quality Issues Calculation Status
        api_response = api_instance.get_quality_issues_calculation_status(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->get_quality_issues_calculation_status: %s\n" % e)
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
processId | ProcessIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# ProcessIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_quality_issues_calculation_status.ApiResponseFor200) | OK

#### get_quality_issues_calculation_status.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**QualityIssuesCalculationStatusResponse**](../../models/QualityIssuesCalculationStatusResponse.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **memory_created_by_users**
<a id="memory_created_by_users"></a>
> MemoryItemCreatedByUsers memory_created_by_users(workspace_id)

Get AI Memory CreatedBy Users

Returns a list of Users who created any memory item for this workspace

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import smart_functions_api
from gooddata_api_client.model.memory_item_created_by_users import MemoryItemCreatedByUsers
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
    }
    try:
        # Get AI Memory CreatedBy Users
        api_response = api_instance.memory_created_by_users(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->memory_created_by_users: %s\n" % e)
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

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#memory_created_by_users.ApiResponseFor200) | OK

#### memory_created_by_users.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**MemoryItemCreatedByUsers**](../../models/MemoryItemCreatedByUsers.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **resolve_llm_endpoints**
<a id="resolve_llm_endpoints"></a>
> ResolvedLlmEndpoints resolve_llm_endpoints(workspace_id)

Get Active LLM Endpoints for this workspace

Returns a list of available LLM Endpoints

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import smart_functions_api
from gooddata_api_client.model.resolved_llm_endpoints import ResolvedLlmEndpoints
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
    }
    try:
        # Get Active LLM Endpoints for this workspace
        api_response = api_instance.resolve_llm_endpoints(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->resolve_llm_endpoints: %s\n" % e)
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

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#resolve_llm_endpoints.ApiResponseFor200) | OK

#### resolve_llm_endpoints.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ResolvedLlmEndpoints**](../../models/ResolvedLlmEndpoints.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **tags**
<a id="tags"></a>
> AnalyticsCatalogTags tags(workspace_id)

Get Analytics Catalog Tags

Returns a list of tags for this workspace

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import smart_functions_api
from gooddata_api_client.model.analytics_catalog_tags import AnalyticsCatalogTags
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
    }
    try:
        # Get Analytics Catalog Tags
        api_response = api_instance.tags(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->tags: %s\n" % e)
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

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#tags.ApiResponseFor200) | OK

#### tags.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**AnalyticsCatalogTags**](../../models/AnalyticsCatalogTags.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **test_llm_provider**
<a id="test_llm_provider"></a>
> TestLlmProviderResponse test_llm_provider(test_llm_provider_definition_request)

Test LLM Provider

Tests LLM provider connectivity with a full definition.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import smart_functions_api
from gooddata_api_client.model.test_llm_provider_response import TestLlmProviderResponse
from gooddata_api_client.model.test_llm_provider_definition_request import TestLlmProviderDefinitionRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)

    # example passing only required values which don't have defaults set
    body = TestLlmProviderDefinitionRequest(
        models=[
            LlmModel(
                family="OPENAI",
                id="id_example",
            )
        ],
        provider_config=None,
    )
    try:
        # Test LLM Provider
        api_response = api_instance.test_llm_provider(
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->test_llm_provider: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**TestLlmProviderDefinitionRequest**](../../models/TestLlmProviderDefinitionRequest.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#test_llm_provider.ApiResponseFor200) | OK

#### test_llm_provider.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**TestLlmProviderResponse**](../../models/TestLlmProviderResponse.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **test_llm_provider_by_id**
<a id="test_llm_provider_by_id"></a>
> TestLlmProviderResponse test_llm_provider_by_id(llm_provider_id)

Test LLM Provider By Id

Tests an existing LLM provider connectivity by its ID.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import smart_functions_api
from gooddata_api_client.model.test_llm_provider_response import TestLlmProviderResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'llmProviderId': "llmProviderId_example",
    }
    try:
        # Test LLM Provider By Id
        api_response = api_instance.test_llm_provider_by_id(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->test_llm_provider_by_id: %s\n" % e)
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
llmProviderId | LlmProviderIdSchema | | 

# LlmProviderIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#test_llm_provider_by_id.ApiResponseFor200) | OK

#### test_llm_provider_by_id.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**TestLlmProviderResponse**](../../models/TestLlmProviderResponse.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **trigger_quality_issues_calculation**
<a id="trigger_quality_issues_calculation"></a>
> TriggerQualityIssuesCalculationResponse trigger_quality_issues_calculation(workspace_id)

Trigger Quality Issues Calculation

Triggers asynchronous calculation of metadata quality issues and returns a process ID for status tracking.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import smart_functions_api
from gooddata_api_client.model.trigger_quality_issues_calculation_response import TriggerQualityIssuesCalculationResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "/6bUUGjjNSwg0_bs",
    }
    try:
        # Trigger Quality Issues Calculation
        api_response = api_instance.trigger_quality_issues_calculation(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->trigger_quality_issues_calculation: %s\n" % e)
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

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#trigger_quality_issues_calculation.ApiResponseFor200) | OK

#### trigger_quality_issues_calculation.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**TriggerQualityIssuesCalculationResponse**](../../models/TriggerQualityIssuesCalculationResponse.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **validate_llm_endpoint**
<a id="validate_llm_endpoint"></a>
> ValidateLLMEndpointResponse validate_llm_endpoint(validate_llm_endpoint_request)

Validate LLM Endpoint

Validates LLM endpoint with provided parameters.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import smart_functions_api
from gooddata_api_client.model.validate_llm_endpoint_response import ValidateLLMEndpointResponse
from gooddata_api_client.model.validate_llm_endpoint_request import ValidateLLMEndpointRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)

    # example passing only required values which don't have defaults set
    body = ValidateLLMEndpointRequest(
        base_url="base_url_example",
        llm_model="llm_model_example",
        llm_organization="llm_organization_example",
        provider="provider_example",
        token="token_example",
    )
    try:
        # Validate LLM Endpoint
        api_response = api_instance.validate_llm_endpoint(
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->validate_llm_endpoint: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ValidateLLMEndpointRequest**](../../models/ValidateLLMEndpointRequest.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#validate_llm_endpoint.ApiResponseFor200) | OK

#### validate_llm_endpoint.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ValidateLLMEndpointResponse**](../../models/ValidateLLMEndpointResponse.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **validate_llm_endpoint_by_id**
<a id="validate_llm_endpoint_by_id"></a>
> ValidateLLMEndpointResponse validate_llm_endpoint_by_id(llm_endpoint_id)

Validate LLM Endpoint By Id

Validates existing LLM endpoint with provided parameters and updates it if they are valid.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import smart_functions_api
from gooddata_api_client.model.validate_llm_endpoint_response import ValidateLLMEndpointResponse
from gooddata_api_client.model.validate_llm_endpoint_by_id_request import ValidateLLMEndpointByIdRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'llmEndpointId': "llmEndpointId_example",
    }
    try:
        # Validate LLM Endpoint By Id
        api_response = api_instance.validate_llm_endpoint_by_id(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->validate_llm_endpoint_by_id: %s\n" % e)

    # example passing only optional values
    path_params = {
        'llmEndpointId': "llmEndpointId_example",
    }
    body = ValidateLLMEndpointByIdRequest(
        base_url="base_url_example",
        llm_model="llm_model_example",
        llm_organization="llm_organization_example",
        provider="provider_example",
        token="token_example",
    )
    try:
        # Validate LLM Endpoint By Id
        api_response = api_instance.validate_llm_endpoint_by_id(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling SmartFunctionsApi->validate_llm_endpoint_by_id: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, Unset] | optional, default is unset |
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
[**ValidateLLMEndpointByIdRequest**](../../models/ValidateLLMEndpointByIdRequest.md) |  | 


### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
llmEndpointId | LlmEndpointIdSchema | | 

# LlmEndpointIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#validate_llm_endpoint_by_id.ApiResponseFor200) | OK

#### validate_llm_endpoint_by_id.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ValidateLLMEndpointResponse**](../../models/ValidateLLMEndpointResponse.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


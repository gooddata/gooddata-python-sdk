# gooddata_api_client.FlowApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**cancel_flows**](FlowApi.md#cancel_flows) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/flow/cancel | (EXPERIMENTAL) Apply the given cancel tokens to flows
[**execute_flow**](FlowApi.md#execute_flow) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/flow | (EXPERIMENTAL) Execute a flow
[**list_flow_operations**](FlowApi.md#list_flow_operations) | **GET** /api/v1/actions/workspaces/{workspaceId}/execution/flow/operations | (EXPERIMENTAL) List the operations of flows
[**retrieve_flow_result_binary**](FlowApi.md#retrieve_flow_result_binary) | **GET** /api/v1/actions/workspaces/{workspaceId}/execution/flow/result/{resultId}/binary | (EXPERIMENTAL) Get a flow result in Apache Arrow File or Stream format
[**retrieve_flow_result_metadata**](FlowApi.md#retrieve_flow_result_metadata) | **GET** /api/v1/actions/workspaces/{workspaceId}/execution/flow/result/{resultId}/metadata | (EXPERIMENTAL) Get the metadata of a flow result
[**retrieve_flow_result_table**](FlowApi.md#retrieve_flow_result_table) | **GET** /api/v1/actions/workspaces/{workspaceId}/execution/flow/result/{resultId}/table | (EXPERIMENTAL) Get a page of a flow result


# **cancel_flows**
> AfmCancelTokens cancel_flows(workspace_id, afm_cancel_tokens)

(EXPERIMENTAL) Apply the given cancel tokens to flows

Note: This API is experimental and is going to change. Please, use it accordingly. Each result has one cancel token, which the submit of its flow returns. Applying the token cancels the flow that computes the result.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import flow_api
from gooddata_api_client.model.afm_cancel_tokens import AfmCancelTokens
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = flow_api.FlowApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    afm_cancel_tokens = AfmCancelTokens(
        result_id_to_cancel_token_pairs={
            "key": "key_example",
        },
    ) # AfmCancelTokens | 

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Apply the given cancel tokens to flows
        api_response = api_instance.cancel_flows(workspace_id, afm_cancel_tokens)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FlowApi->cancel_flows: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **afm_cancel_tokens** | [**AfmCancelTokens**](AfmCancelTokens.md)|  |

### Return type

[**AfmCancelTokens**](AfmCancelTokens.md)

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

# **execute_flow**
> FlowExecutionResponse execute_flow(workspace_id, flow_request)

(EXPERIMENTAL) Execute a flow

Note: This API is experimental and is going to change. Please, use it accordingly. Runs the transformations of a flow over its inputs and stores the result. The response links to the result.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import flow_api
from gooddata_api_client.model.flow_execution_response import FlowExecutionResponse
from gooddata_api_client.model.flow_request import FlowRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = flow_api.FlowApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    flow_request = FlowRequest(
        inputs={
            "key": FlowInput(),
        },
        transformations=[
            FlowTransformation(
                id="id_example",
                input_refs={
                    "key": "key_example",
                },
                operation="survey_weighting",
                parameters={},
            ),
        ],
    ) # FlowRequest | 

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Execute a flow
        api_response = api_instance.execute_flow(workspace_id, flow_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FlowApi->execute_flow: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **flow_request** | [**FlowRequest**](FlowRequest.md)|  |

### Return type

[**FlowExecutionResponse**](FlowExecutionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The flow was accepted. |  * X-GDC-CANCEL-TOKEN - A token that can be used to cancel this execution <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_flow_operations**
> FlowOperations list_flow_operations(workspace_id)

(EXPERIMENTAL) List the operations of flows

Note: This API is experimental and is going to change. Please, use it accordingly. Lists the operations that the transformations of a flow can run, with their inputs and the JSON Schema of their parameters.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import flow_api
from gooddata_api_client.model.flow_operations import FlowOperations
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = flow_api.FlowApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) List the operations of flows
        api_response = api_instance.list_flow_operations(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FlowApi->list_flow_operations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |

### Return type

[**FlowOperations**](FlowOperations.md)

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

# **retrieve_flow_result_binary**
> file_type retrieve_flow_result_binary(workspace_id, result_id)

(EXPERIMENTAL) Get a flow result in Apache Arrow File or Stream format

Note: This API is experimental and is going to change. Please, use it accordingly. Gets a window of rows and columns of a flow result as an Apache Arrow IPC File or Stream.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import flow_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = flow_api.FlowApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    result_id = "a9b28f9dc55f37ea9f4a5fb0c76895923591e781" # str | Result ID
    row_offset = 1 # int | Index of the first row to return. The default is 0. (optional)
    row_limit = 1 # int | Maximum number of rows to return. The default is all remaining rows. (optional)
    column_offset = 1 # int | Index of the first column to return. The default is 0. (optional)
    column_limit = 1 # int | Maximum number of columns to return. The default is all remaining columns. (optional)

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Get a flow result in Apache Arrow File or Stream format
        api_response = api_instance.retrieve_flow_result_binary(workspace_id, result_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FlowApi->retrieve_flow_result_binary: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (EXPERIMENTAL) Get a flow result in Apache Arrow File or Stream format
        api_response = api_instance.retrieve_flow_result_binary(workspace_id, result_id, row_offset=row_offset, row_limit=row_limit, column_offset=column_offset, column_limit=column_limit)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FlowApi->retrieve_flow_result_binary: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **result_id** | **str**| Result ID |
 **row_offset** | **int**| Index of the first row to return. The default is 0. | [optional]
 **row_limit** | **int**| Maximum number of rows to return. The default is all remaining rows. | [optional]
 **column_offset** | **int**| Index of the first column to return. The default is 0. | [optional]
 **column_limit** | **int**| Maximum number of columns to return. The default is all remaining columns. | [optional]

### Return type

**file_type**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.apache.arrow.file, application/vnd.apache.arrow.stream


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The result. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_flow_result_metadata**
> FlowResultMetadata retrieve_flow_result_metadata(workspace_id, result_id)

(EXPERIMENTAL) Get the metadata of a flow result

Note: This API is experimental and is going to change. Please, use it accordingly. Gets the columns and the number of rows of a flow result.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import flow_api
from gooddata_api_client.model.flow_result_metadata import FlowResultMetadata
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = flow_api.FlowApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    result_id = "a9b28f9dc55f37ea9f4a5fb0c76895923591e781" # str | Result ID

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Get the metadata of a flow result
        api_response = api_instance.retrieve_flow_result_metadata(workspace_id, result_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FlowApi->retrieve_flow_result_metadata: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **result_id** | **str**| Result ID |

### Return type

[**FlowResultMetadata**](FlowResultMetadata.md)

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

# **retrieve_flow_result_table**
> FlowTableResult retrieve_flow_result_table(workspace_id, result_id)

(EXPERIMENTAL) Get a page of a flow result

Note: This API is experimental and is going to change. Please, use it accordingly. Gets a window of rows and columns of a flow result.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import flow_api
from gooddata_api_client.model.flow_table_result import FlowTableResult
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = flow_api.FlowApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    result_id = "a9b28f9dc55f37ea9f4a5fb0c76895923591e781" # str | Result ID
    row_offset = 1 # int | Index of the first row to return. The default is 0. (optional)
    row_limit = 1 # int | Maximum number of rows to return. The default is all remaining rows. (optional)
    column_offset = 1 # int | Index of the first column to return. The default is 0. (optional)
    column_limit = 1 # int | Maximum number of columns to return. The default is all remaining columns. (optional)

    # example passing only required values which don't have defaults set
    try:
        # (EXPERIMENTAL) Get a page of a flow result
        api_response = api_instance.retrieve_flow_result_table(workspace_id, result_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FlowApi->retrieve_flow_result_table: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (EXPERIMENTAL) Get a page of a flow result
        api_response = api_instance.retrieve_flow_result_table(workspace_id, result_id, row_offset=row_offset, row_limit=row_limit, column_offset=column_offset, column_limit=column_limit)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FlowApi->retrieve_flow_result_table: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **result_id** | **str**| Result ID |
 **row_offset** | **int**| Index of the first row to return. The default is 0. | [optional]
 **row_limit** | **int**| Maximum number of rows to return. The default is all remaining rows. | [optional]
 **column_offset** | **int**| Index of the first column to return. The default is 0. | [optional]
 **column_limit** | **int**| Maximum number of columns to return. The default is all remaining columns. | [optional]

### Return type

[**FlowTableResult**](FlowTableResult.md)

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


# gooddata_afm_client.ResultControllerApi

All URIs are relative to *https://staging.anywhere.gooddata.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**retrieve_result**](ResultControllerApi.md#retrieve_result) | **GET** /api/actions/workspaces/{workspaceId}/execution/afm/execute/result/{resultId} | Get a single execution result


# **retrieve_result**
> ExecutionResult retrieve_result(workspace_id, result_id)

Get a single execution result

Gets a single execution result.

### Example

```python
import time
import gooddata_afm_client
from gooddata_afm_client.api import result_controller_api
from gooddata_afm_client.model.execution_result import ExecutionResult
from gooddata_afm_client.model.error_message import ErrorMessage
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_afm_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_afm_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = result_controller_api.ResultControllerApi(api_client)
    workspace_id = "26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1RA89q3w1l4eH4XxEz.5awxoFZxHzs6ED.kjUSnTINkYPUndNl8pmPg5K897Fu1JEFj9R1_dz9rEoBi0LnU8SsOWJ7wYrcziVQdt8mVLxbg4bCLrLBcmXxWQK6MzKSg5jphei0IfRRwpnT_Z.qKa_YppZepezJ0.VmLSUTLYyW" # str | Workspace identifier
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
        print("Exception when calling ResultControllerApi->retrieve_result: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a single execution result
        api_response = api_instance.retrieve_result(workspace_id, result_id, offset=offset, limit=limit)
        pprint(api_response)
    except gooddata_afm_client.ApiException as e:
        print("Exception when calling ResultControllerApi->retrieve_result: %s\n" % e)
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


# gooddata_api_client.UnsubscribeApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**unsubscribe_all_automations**](UnsubscribeApi.md#unsubscribe_all_automations) | **DELETE** /api/v1/actions/organization/automations/unsubscribe | Unsubscribe from all automations in all workspaces
[**unsubscribe_automation**](UnsubscribeApi.md#unsubscribe_automation) | **DELETE** /api/v1/actions/workspaces/{workspaceId}/automations/{automationId}/unsubscribe | Unsubscribe from an automation
[**unsubscribe_workspace_automations**](UnsubscribeApi.md#unsubscribe_workspace_automations) | **DELETE** /api/v1/actions/workspaces/{workspaceId}/automations/unsubscribe | Unsubscribe from all automations in the workspace


# **unsubscribe_all_automations**
> unsubscribe_all_automations()

Unsubscribe from all automations in all workspaces

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import unsubscribe_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = unsubscribe_api.UnsubscribeApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Unsubscribe from all automations in all workspaces
        api_instance.unsubscribe_all_automations()
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UnsubscribeApi->unsubscribe_all_automations: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

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

# **unsubscribe_automation**
> unsubscribe_automation(workspace_id, automation_id)

Unsubscribe from an automation

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import unsubscribe_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = unsubscribe_api.UnsubscribeApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    automation_id = "automationId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Unsubscribe from an automation
        api_instance.unsubscribe_automation(workspace_id, automation_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UnsubscribeApi->unsubscribe_automation: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **automation_id** | **str**|  |

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

# **unsubscribe_workspace_automations**
> unsubscribe_workspace_automations(workspace_id)

Unsubscribe from all automations in the workspace

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import unsubscribe_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = unsubscribe_api.UnsubscribeApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Unsubscribe from all automations in the workspace
        api_instance.unsubscribe_workspace_automations(workspace_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UnsubscribeApi->unsubscribe_workspace_automations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |

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


# gooddata_api_client.AnalyticsModelApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_analytics_model**](AnalyticsModelApi.md#get_analytics_model) | **GET** /api/v1/layout/workspaces/{workspaceId}/analyticsModel | Get analytics model
[**set_analytics_model**](AnalyticsModelApi.md#set_analytics_model) | **PUT** /api/v1/layout/workspaces/{workspaceId}/analyticsModel | Set analytics model


# **get_analytics_model**
> DeclarativeAnalytics get_analytics_model(workspace_id, exclude=exclude)

Get analytics model

Retrieve current analytics model of the workspace.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_analytics import DeclarativeAnalytics
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
    api_instance = gooddata_api_client.AnalyticsModelApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    exclude = ['exclude_example'] # List[str] |  (optional)

    try:
        # Get analytics model
        api_response = api_instance.get_analytics_model(workspace_id, exclude=exclude)
        print("The response of AnalyticsModelApi->get_analytics_model:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AnalyticsModelApi->get_analytics_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **exclude** | [**List[str]**](str.md)|  | [optional] 

### Return type

[**DeclarativeAnalytics**](DeclarativeAnalytics.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved current analytics model. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_analytics_model**
> set_analytics_model(workspace_id, declarative_analytics)

Set analytics model

Set effective analytics model of the workspace.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_analytics import DeclarativeAnalytics
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
    api_instance = gooddata_api_client.AnalyticsModelApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    declarative_analytics = gooddata_api_client.DeclarativeAnalytics() # DeclarativeAnalytics | 

    try:
        # Set analytics model
        api_instance.set_analytics_model(workspace_id, declarative_analytics)
    except Exception as e:
        print("Exception when calling AnalyticsModelApi->set_analytics_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **declarative_analytics** | [**DeclarativeAnalytics**](DeclarativeAnalytics.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Analytics model successfully set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


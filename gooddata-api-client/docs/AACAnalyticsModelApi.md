# gooddata_api_client.AACAnalyticsModelApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_analytics_model_aac**](AACAnalyticsModelApi.md#get_analytics_model_aac) | **GET** /api/v1/aac/workspaces/{workspaceId}/analyticsModel | Get analytics model in AAC format
[**set_analytics_model_aac**](AACAnalyticsModelApi.md#set_analytics_model_aac) | **PUT** /api/v1/aac/workspaces/{workspaceId}/analyticsModel | Set analytics model from AAC format


# **get_analytics_model_aac**
> AacAnalyticsModel get_analytics_model_aac(workspace_id)

Get analytics model in AAC format

             Retrieve the analytics model of the workspace in Analytics as Code format.                          The returned format is compatible with the YAML definitions used by the              GoodData Analytics as Code VSCode extension. This includes metrics,              dashboards, visualizations, plugins, and attribute hierarchies.         

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import aac_analytics_model_api
from gooddata_api_client.model.aac_analytics_model import AacAnalyticsModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = aac_analytics_model_api.AACAnalyticsModelApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    exclude = [
        "ACTIVITY_INFO",
    ] # [str] |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get analytics model in AAC format
        api_response = api_instance.get_analytics_model_aac(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AACAnalyticsModelApi->get_analytics_model_aac: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get analytics model in AAC format
        api_response = api_instance.get_analytics_model_aac(workspace_id, exclude=exclude)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AACAnalyticsModelApi->get_analytics_model_aac: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **exclude** | **[str]**|  | [optional]

### Return type

[**AacAnalyticsModel**](AacAnalyticsModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved current analytics model in AAC format. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_analytics_model_aac**
> set_analytics_model_aac(workspace_id, aac_analytics_model)

Set analytics model from AAC format

             Set the analytics model of the workspace using Analytics as Code format.                          The input format is compatible with the YAML definitions used by the              GoodData Analytics as Code VSCode extension. This replaces the entire              analytics model with the provided definition, including metrics,              dashboards, visualizations, plugins, and attribute hierarchies.         

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import aac_analytics_model_api
from gooddata_api_client.model.aac_analytics_model import AacAnalyticsModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = aac_analytics_model_api.AACAnalyticsModelApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    aac_analytics_model = AacAnalyticsModel(
        attribute_hierarchies=[
            AacAttributeHierarchy(
                attributes=["attribute/country","attribute/state","attribute/city"],
                description="description_example",
                id="geo-hierarchy",
                tags=[
                    "tags_example",
                ],
                title="Geographic Hierarchy",
                type="attribute_hierarchy",
            ),
        ],
        dashboards=[
            AacDashboard(None),
        ],
        metrics=[
            AacMetric(
                description="description_example",
                format="#,##0.00",
                id="total-sales",
                is_hidden=True,
                is_hidden_from_kda=True,
                maql="SELECT SUM({fact/amount})",
                show_in_ai_results=True,
                tags=[
                    "tags_example",
                ],
                title="Total Sales",
                type="metric",
            ),
        ],
        plugins=[
            AacPlugin(
                description="description_example",
                id="my-plugin",
                tags=[
                    "tags_example",
                ],
                title="My Plugin",
                type="plugin",
                url="https://example.com/plugin.js",
            ),
        ],
        visualizations=[
            AacVisualization(None),
        ],
    ) # AacAnalyticsModel | 

    # example passing only required values which don't have defaults set
    try:
        # Set analytics model from AAC format
        api_instance.set_analytics_model_aac(workspace_id, aac_analytics_model)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AACAnalyticsModelApi->set_analytics_model_aac: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **aac_analytics_model** | [**AacAnalyticsModel**](AacAnalyticsModel.md)|  |

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


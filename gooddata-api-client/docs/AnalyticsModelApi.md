# gooddata_api_client.AnalyticsModelApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_analytics_model**](AnalyticsModelApi.md#get_analytics_model) | **GET** /api/v1/layout/workspaces/{workspaceId}/analyticsModel | Get analytics model
[**set_analytics_model**](AnalyticsModelApi.md#set_analytics_model) | **PUT** /api/v1/layout/workspaces/{workspaceId}/analyticsModel | Set analytics model


# **get_analytics_model**
> DeclarativeAnalytics get_analytics_model(workspace_id)

Get analytics model

Retrieve current analytics model of the workspace.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import analytics_model_api
from gooddata_api_client.model.declarative_analytics import DeclarativeAnalytics
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = analytics_model_api.AnalyticsModelApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    exclude = [
        "ACTIVITY_INFO",
    ] # [str] |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get analytics model
        api_response = api_instance.get_analytics_model(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AnalyticsModelApi->get_analytics_model: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get analytics model
        api_response = api_instance.get_analytics_model(workspace_id, exclude=exclude)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AnalyticsModelApi->get_analytics_model: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **exclude** | **[str]**|  | [optional]

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
import time
import gooddata_api_client
from gooddata_api_client.api import analytics_model_api
from gooddata_api_client.model.declarative_analytics import DeclarativeAnalytics
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = analytics_model_api.AnalyticsModelApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    declarative_analytics = DeclarativeAnalytics(
        analytics=DeclarativeAnalyticsLayer(
            analytical_dashboard_extensions=[
                DeclarativeAnalyticalDashboardExtension(
                    id="revenues-analysis",
                    permissions=[
                        DeclarativeAnalyticalDashboardPermissionsInner(None),
                    ],
                ),
            ],
            analytical_dashboards=[
                DeclarativeAnalyticalDashboard(
                    content=JsonNode(),
                    created_at="2023-07-20 12:30",
                    created_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    description="Period to period comparison of revenues in main sectors.",
                    id="revenues-analysis",
                    modified_at="2023-07-20 12:30",
                    modified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    permissions=[
                        DeclarativeAnalyticalDashboardPermissionsInner(None),
                    ],
                    tags=["Revenues"],
                    title="Revenues analysis",
                ),
            ],
            attribute_hierarchies=[
                DeclarativeAttributeHierarchy(
                    content=JsonNode(),
                    created_at="["2023-07-20 12:30"]",
                    created_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    description="Simple number for total goods in current production.",
                    id="hierarchy-1",
                    modified_at="["2023-07-20 12:30"]",
                    modified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    tags=["Revenues"],
                    title="Count of goods",
                ),
            ],
            dashboard_plugins=[
                DeclarativeDashboardPlugin(
                    content=JsonNode(),
                    created_at="["2023-07-20 12:30"]",
                    created_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    description="Three dimensional view of data.",
                    id="dashboard-plugin-1",
                    modified_at="["2023-07-20 12:30"]",
                    modified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    tags=["Revenues"],
                    title="3D map renderer",
                ),
            ],
            export_definitions=[
                DeclarativeExportDefinition(
                    created_at="["2023-07-20 12:30"]",
                    created_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    description="Simple number for total goods in current production.",
                    id="export-definition-1",
                    modified_at="["2023-07-20 12:30"]",
                    modified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    request_payload=DeclarativeExportDefinitionRequestPayload(None),
                    tags=["Revenues"],
                    title="My regular export",
                ),
            ],
            filter_contexts=[
                DeclarativeFilterContext(
                    content=JsonNode(),
                    description="Filter Context for Sales team.",
                    id="filter-sales",
                    tags=["Revenues"],
                    title="Filter Context for Sales team",
                ),
            ],
            metrics=[
                DeclarativeMetric(
                    content=JsonNode(),
                    created_at="["2023-07-20 12:30"]",
                    created_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    description="Sales for all the data available.",
                    id="total-sales",
                    modified_at="["2023-07-20 12:30"]",
                    modified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    tags=["Revenues"],
                    title="Total sales",
                ),
            ],
            visualization_objects=[
                DeclarativeVisualizationObject(
                    content=JsonNode(),
                    created_at="["2023-07-20 12:30"]",
                    created_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    description="Simple number for total goods in current production.",
                    id="visualization-1",
                    modified_at="["2023-07-20 12:30"]",
                    modified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    tags=["Revenues"],
                    title="Count of goods",
                ),
            ],
        ),
    ) # DeclarativeAnalytics | 

    # example passing only required values which don't have defaults set
    try:
        # Set analytics model
        api_instance.set_analytics_model(workspace_id, declarative_analytics)
    except gooddata_api_client.ApiException as e:
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


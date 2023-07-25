<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.analytics_model_api.AnalyticsModelApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_analytics_model**](#get_analytics_model) | **get** /api/v1/layout/workspaces/{workspaceId}/analyticsModel | Get analytics model
[**set_analytics_model**](#set_analytics_model) | **put** /api/v1/layout/workspaces/{workspaceId}/analyticsModel | Set analytics model

# **get_analytics_model**
<a id="get_analytics_model"></a>
> DeclarativeAnalytics get_analytics_model(workspace_id)

Get analytics model

Retrieve current analytics model of the workspace.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import analytics_model_api
from gooddata_api_client.model.declarative_analytics import DeclarativeAnalytics
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = analytics_model_api.AnalyticsModelApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    try:
        # Get analytics model
        api_response = api_instance.get_analytics_model(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AnalyticsModelApi->get_analytics_model: %s\n" % e)
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
200 | [ApiResponseFor200](#get_analytics_model.ApiResponseFor200) | Retrieved current analytics model.

#### get_analytics_model.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeAnalytics**](../../models/DeclarativeAnalytics.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **set_analytics_model**
<a id="set_analytics_model"></a>
> set_analytics_model(workspace_iddeclarative_analytics)

Set analytics model

Set effective analytics model of the workspace.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import analytics_model_api
from gooddata_api_client.model.declarative_analytics import DeclarativeAnalytics
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = analytics_model_api.AnalyticsModelApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    body = DeclarativeAnalytics(
        analytics=DeclarativeAnalyticsLayer(
            analytical_dashboard_extensions=[
                DeclarativeAnalyticalDashboardExtension(
                    id="revenues-analysis",
                    permissions=[
                        DeclarativeAnalyticalDashboardPermission(
                            assignee=AssigneeIdentifier(
                                id="id_example",
                                type="user",
                            ),
                            name="EDIT",
                        )
                    ],
                )
            ],
            analytical_dashboards=[
                DeclarativeAnalyticalDashboard(
                    content=dict(),
                    description="Period to period comparison of revenues in main sectors.",
                    id="revenues-analysis",
,
                    tags=["Revenues"],
                    title="Revenues analysis",
                )
            ],
            dashboard_plugins=[
                DeclarativeDashboardPlugin(
                    content=dict(),
                    description="Three dimensional view of data.",
                    id="dashboard-plugin-1",
                    tags=["Revenues"],
                    title="3D map renderer",
                )
            ],
            filter_contexts=[
                DeclarativeFilterContext(
                    content=dict(),
                    description="Filter Context for Sales team.",
                    id="filter-sales",
                    tags=["Revenues"],
                    title="Filter Context for Sales team",
                )
            ],
            metrics=[
                DeclarativeMetric(
                    content=dict(),
                    description="Sales for all the data available.",
                    id="total-sales",
                    tags=["Revenues"],
                    title="Total sales",
                )
            ],
            visualization_objects=[
                DeclarativeVisualizationObject(
                    content=dict(),
                    description="Simple number for total goods in current production.",
                    id="visualization-1",
                    tags=["Revenues"],
                    title="Count of goods",
                )
            ],
        ),
    )
    try:
        # Set analytics model
        api_response = api_instance.set_analytics_model(
            path_params=path_params,
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AnalyticsModelApi->set_analytics_model: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeAnalytics**](../../models/DeclarativeAnalytics.md) |  | 


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
204 | [ApiResponseFor204](#set_analytics_model.ApiResponseFor204) | Analytics model successfully set.

#### set_analytics_model.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


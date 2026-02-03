# gooddata_api_client.AacApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_analytics_model_aac**](AacApi.md#get_analytics_model_aac) | **GET** /api/v1/aac/workspaces/{workspaceId}/analyticsModel | Get analytics model in AAC format
[**get_logical_model_aac**](AacApi.md#get_logical_model_aac) | **GET** /api/v1/aac/workspaces/{workspaceId}/logicalModel | Get logical model in AAC format
[**set_analytics_model_aac**](AacApi.md#set_analytics_model_aac) | **PUT** /api/v1/aac/workspaces/{workspaceId}/analyticsModel | Set analytics model from AAC format
[**set_logical_model_aac**](AacApi.md#set_logical_model_aac) | **PUT** /api/v1/aac/workspaces/{workspaceId}/logicalModel | Set logical model from AAC format


# **get_analytics_model_aac**
> AacAnalyticsModel get_analytics_model_aac(workspace_id)

Get analytics model in AAC format

             Retrieve the analytics model of the workspace in Analytics as Code format.                          The returned format is compatible with the YAML definitions used by the              GoodData Analytics as Code VSCode extension. This includes metrics,              dashboards, visualizations, plugins, and attribute hierarchies.         

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import aac_api
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
    api_instance = aac_api.AacApi(api_client)
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
        print("Exception when calling AacApi->get_analytics_model_aac: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get analytics model in AAC format
        api_response = api_instance.get_analytics_model_aac(workspace_id, exclude=exclude)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AacApi->get_analytics_model_aac: %s\n" % e)
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

# **get_logical_model_aac**
> AacLogicalModel get_logical_model_aac(workspace_id)

Get logical model in AAC format

             Retrieve the logical data model of the workspace in Analytics as Code format.                          The returned format is compatible with the YAML definitions used by the              GoodData Analytics as Code VSCode extension. Use this for exporting models             that can be directly used as YAML configuration files.         

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import aac_api
from gooddata_api_client.model.aac_logical_model import AacLogicalModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = aac_api.AacApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    include_parents = True # bool |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get logical model in AAC format
        api_response = api_instance.get_logical_model_aac(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AacApi->get_logical_model_aac: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get logical model in AAC format
        api_response = api_instance.get_logical_model_aac(workspace_id, include_parents=include_parents)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AacApi->get_logical_model_aac: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **include_parents** | **bool**|  | [optional]

### Return type

[**AacLogicalModel**](AacLogicalModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved current logical model in AAC format. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_analytics_model_aac**
> set_analytics_model_aac(workspace_id, aac_analytics_model)

Set analytics model from AAC format

             Set the analytics model of the workspace using Analytics as Code format.                          The input format is compatible with the YAML definitions used by the              GoodData Analytics as Code VSCode extension. This replaces the entire              analytics model with the provided definition, including metrics,              dashboards, visualizations, plugins, and attribute hierarchies.         

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import aac_api
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
    api_instance = aac_api.AacApi(api_client)
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
        print("Exception when calling AacApi->set_analytics_model_aac: %s\n" % e)
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

# **set_logical_model_aac**
> set_logical_model_aac(workspace_id, aac_logical_model)

Set logical model from AAC format

             Set the logical data model of the workspace using Analytics as Code format.                          The input format is compatible with the YAML definitions used by the              GoodData Analytics as Code VSCode extension. This replaces the entire              logical model with the provided definition.         

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import aac_api
from gooddata_api_client.model.aac_logical_model import AacLogicalModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = aac_api.AacApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    aac_logical_model = AacLogicalModel(
        datasets=[
            AacDataset(
                data_source="my-postgres",
                description="description_example",
                fields={
                    "key": AacField(
                        aggregated_as="SUM",
                        assigned_to="assigned_to_example",
                        data_type="STRING",
                        default_view="default_view_example",
                        description="description_example",
                        is_hidden=True,
                        labels={
                            "key": AacLabel(
                                data_type="INT",
                                description="description_example",
                                geo_area_config=AacGeoAreaConfig(
                                    collection=AacGeoCollectionIdentifier(
                                        id="id_example",
                                        kind="STATIC",
                                    ),
                                ),
                                is_hidden=True,
                                locale="locale_example",
                                show_in_ai_results=True,
                                source_column="source_column_example",
                                tags=[
                                    "tags_example",
                                ],
                                title="title_example",
                                translations=[
                                    AacLabelTranslation(
                                        locale="locale_example",
                                        source_column="source_column_example",
                                    ),
                                ],
                                value_type="TEXT",
                            ),
                        },
                        locale="locale_example",
                        show_in_ai_results=True,
                        sort_column="sort_column_example",
                        sort_direction="ASC",
                        source_column="source_column_example",
                        tags=[
                            "tags_example",
                        ],
                        title="title_example",
                        type="attribute",
                    ),
                },
                id="customers",
                precedence=1,
                primary_key=AacDatasetPrimaryKey(None),
                references=[
                    AacReference(
                        dataset="orders",
                        multi_directional=True,
                        sources=[
                            AacReferenceSource(
                                data_type="INT",
                                source_column="source_column_example",
                                target="target_example",
                            ),
                        ],
                    ),
                ],
                sql="sql_example",
                table_path="public/customers",
                tags=[
                    "tags_example",
                ],
                title="Customers",
                type="dataset",
                workspace_data_filters=[
                    AacWorkspaceDataFilter(
                        data_type="INT",
                        filter_id="filter_id_example",
                        source_column="source_column_example",
                    ),
                ],
            ),
        ],
        date_datasets=[
            AacDateDataset(
                description="description_example",
                granularities=[
                    "granularities_example",
                ],
                id="date",
                tags=[
                    "tags_example",
                ],
                title="Date",
                title_base="title_base_example",
                title_pattern="title_pattern_example",
                type="date",
            ),
        ],
    ) # AacLogicalModel | 

    # example passing only required values which don't have defaults set
    try:
        # Set logical model from AAC format
        api_instance.set_logical_model_aac(workspace_id, aac_logical_model)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AacApi->set_logical_model_aac: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **aac_logical_model** | [**AacLogicalModel**](AacLogicalModel.md)|  |

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
**204** | Logical model successfully set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


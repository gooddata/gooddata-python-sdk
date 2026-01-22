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
            AacDashboard(
                active_tab_id="active_tab_id_example",
                cross_filtering=True,
                description="description_example",
                enable_section_headers=True,
                filter_views=True,
                filters={
                    "key": AacDashboardFilter(
                        date="date_example",
                        display_as="display_as_example",
                        _from=AacDashboardFilterFrom(None),
                        granularity="granularity_example",
                        metric_filters=[
                            "metric_filters_example",
                        ],
                        mode="active",
                        multiselect=True,
                        parents=[
                            JsonNode(),
                        ],
                        state=AacFilterState(
                            exclude=[
                                "exclude_example",
                            ],
                            include=[
                                "include_example",
                            ],
                        ),
                        title="title_example",
                        to=AacDashboardFilterFrom(None),
                        type="attribute_filter",
                        using="using_example",
                    ),
                },
                id="sales-overview",
                permissions=AacDashboardPermissions(
                    edit=AacPermission(
                        all=True,
                        user_groups=[
                            "user_groups_example",
                        ],
                        users=[
                            "users_example",
                        ],
                    ),
                    share=AacPermission(
                        all=True,
                        user_groups=[
                            "user_groups_example",
                        ],
                        users=[
                            "users_example",
                        ],
                    ),
                    view=AacPermission(
                        all=True,
                        user_groups=[
                            "user_groups_example",
                        ],
                        users=[
                            "users_example",
                        ],
                    ),
                ),
                plugins=[
                    AacDashboardPluginLink(
                        id="id_example",
                        parameters=JsonNode(),
                    ),
                ],
                sections=[
                    AacSection(
                        description="description_example",
                        header=True,
                        title="title_example",
                        widgets=[
                            AacWidget(
                                additional_properties={
                                    "key": JsonNode(),
                                },
                                columns=1,
                                content="content_example",
                                date="date_example",
                                description=AacWidgetDescription(None),
                                drill_down=JsonNode(),
                                ignore_dashboard_filters=[
                                    "ignore_dashboard_filters_example",
                                ],
                                ignored_filters=[
                                    "ignored_filters_example",
                                ],
                                interactions=[
                                    JsonNode(),
                                ],
                                metric="metric_example",
                                rows=1,
                                sections=[
                                    AacSection(),
                                ],
                                size=AacWidgetSize(
                                    height=1,
                                    height_as_ratio=True,
                                    width=1,
                                ),
                                title=AacWidgetDescription(None),
                                type="visualization",
                                visualization="visualization_example",
                                zoom_data=True,
                            ),
                        ],
                    ),
                ],
                tabs=[
                    AacTab(
                        filters={
                            "key": AacDashboardFilter(
                                date="date_example",
                                display_as="display_as_example",
                                _from=AacDashboardFilterFrom(None),
                                granularity="granularity_example",
                                metric_filters=[
                                    "metric_filters_example",
                                ],
                                mode="active",
                                multiselect=True,
                                parents=[
                                    JsonNode(),
                                ],
                                state=AacFilterState(
                                    exclude=[
                                        "exclude_example",
                                    ],
                                    include=[
                                        "include_example",
                                    ],
                                ),
                                title="title_example",
                                to=AacDashboardFilterFrom(None),
                                type="attribute_filter",
                                using="using_example",
                            ),
                        },
                        id="id_example",
                        sections=[
                            AacSection(
                                description="description_example",
                                header=True,
                                title="title_example",
                                widgets=[
                                    AacWidget(
                                        additional_properties={
                                            "key": JsonNode(),
                                        },
                                        columns=1,
                                        content="content_example",
                                        date="date_example",
                                        description=AacWidgetDescription(None),
                                        drill_down=JsonNode(),
                                        ignore_dashboard_filters=[
                                            "ignore_dashboard_filters_example",
                                        ],
                                        ignored_filters=[
                                            "ignored_filters_example",
                                        ],
                                        interactions=[
                                            JsonNode(),
                                        ],
                                        metric="metric_example",
                                        rows=1,
                                        sections=[
                                            AacSection(),
                                        ],
                                        size=AacWidgetSize(
                                            height=1,
                                            height_as_ratio=True,
                                            width=1,
                                        ),
                                        title=AacWidgetDescription(None),
                                        type="visualization",
                                        visualization="visualization_example",
                                        zoom_data=True,
                                    ),
                                ],
                            ),
                        ],
                        title="title_example",
                    ),
                ],
                tags=[
                    "tags_example",
                ],
                title="Sales Overview",
                type="dashboard",
                user_filters_reset=True,
                user_filters_save=True,
            ),
        ],
        metrics=[
            AacMetric(
                description="description_example",
                format="#,##0.00",
                id="total-sales",
                is_hidden=True,
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
            AacVisualization(
                additional_properties={
                    "key": JsonNode(),
                },
                attribute=[
                    AacQueryFieldsValue(None),
                ],
                color=[
                    AacQueryFieldsValue(None),
                ],
                columns=[
                    AacQueryFieldsValue(None),
                ],
                config=JsonNode(),
                description="description_example",
                id="sales-by-region",
                is_hidden=True,
                location=[
                    AacQueryFieldsValue(None),
                ],
                metrics=[
                    AacQueryFieldsValue(None),
                ],
                primary_measures=[
                    AacQueryFieldsValue(None),
                ],
                query=AacQuery(
                    fields={
                        "key": AacQueryFieldsValue(None),
                    },
                    filter_by={
                        "key": AacQueryFilter(
                            additional_properties={
                                "key": JsonNode(),
                            },
                            attribute="attribute_example",
                            bottom=1,
                            condition="condition_example",
                            _from=AacDashboardFilterFrom(None),
                            granularity="granularity_example",
                            state=AacFilterState(
                                exclude=[
                                    "exclude_example",
                                ],
                                include=[
                                    "include_example",
                                ],
                            ),
                            to=AacDashboardFilterFrom(None),
                            top=1,
                            type="date_filter",
                            using="using_example",
                            value=3.14,
                        ),
                    },
                    sort_by=[
                        JsonNode(),
                    ],
                ),
                rows=[
                    AacQueryFieldsValue(None),
                ],
                secondary_measures=[
                    AacQueryFieldsValue(None),
                ],
                segment_by=[
                    AacQueryFieldsValue(None),
                ],
                show_in_ai_results=True,
                size=[
                    AacQueryFieldsValue(None),
                ],
                stack=[
                    AacQueryFieldsValue(None),
                ],
                tags=[
                    "tags_example",
                ],
                title="Sales by Region",
                trend=[
                    AacQueryFieldsValue(None),
                ],
                type="bar_chart",
                view_by=[
                    AacQueryFieldsValue(None),
                ],
            ),
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


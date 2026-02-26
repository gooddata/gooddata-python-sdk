<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.aac_api.AacApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_analytics_model_aac**](#get_analytics_model_aac) | **get** /api/v1/aac/workspaces/{workspaceId}/analyticsModel | Get analytics model in AAC format
[**get_logical_model_aac**](#get_logical_model_aac) | **get** /api/v1/aac/workspaces/{workspaceId}/logicalModel | Get logical model in AAC format
[**set_analytics_model_aac**](#set_analytics_model_aac) | **put** /api/v1/aac/workspaces/{workspaceId}/analyticsModel | Set analytics model from AAC format
[**set_logical_model_aac**](#set_logical_model_aac) | **put** /api/v1/aac/workspaces/{workspaceId}/logicalModel | Set logical model from AAC format

# **get_analytics_model_aac**
<a id="get_analytics_model_aac"></a>
> AacAnalyticsModel get_analytics_model_aac(workspace_id)

Get analytics model in AAC format

             Retrieve the analytics model of the workspace in Analytics as Code format.                          The returned format is compatible with the YAML definitions used by the              GoodData Analytics as Code VSCode extension. This includes metrics,              dashboards, visualizations, plugins, and attribute hierarchies.         

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import aac_api
from gooddata_api_client.model.aac_analytics_model import AacAnalyticsModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = aac_api.AacApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
    }
    try:
        # Get analytics model in AAC format
        api_response = api_instance.get_analytics_model_aac(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AacApi->get_analytics_model_aac: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
        'exclude': [
        "ACTIVITY_INFO"
    ],
    }
    try:
        # Get analytics model in AAC format
        api_response = api_instance.get_analytics_model_aac(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AacApi->get_analytics_model_aac: %s\n" % e)
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
exclude | ExcludeSchema | | optional


# ExcludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  | Defines properties which should not be included in the payload. | must be one of ["ACTIVITY_INFO", ] 

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
200 | [ApiResponseFor200](#get_analytics_model_aac.ApiResponseFor200) | Retrieved current analytics model in AAC format.

#### get_analytics_model_aac.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**AacAnalyticsModel**](../../models/AacAnalyticsModel.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_logical_model_aac**
<a id="get_logical_model_aac"></a>
> AacLogicalModel get_logical_model_aac(workspace_id)

Get logical model in AAC format

             Retrieve the logical data model of the workspace in Analytics as Code format.                          The returned format is compatible with the YAML definitions used by the              GoodData Analytics as Code VSCode extension. Use this for exporting models             that can be directly used as YAML configuration files.         

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import aac_api
from gooddata_api_client.model.aac_logical_model import AacLogicalModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = aac_api.AacApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
    }
    try:
        # Get logical model in AAC format
        api_response = api_instance.get_logical_model_aac(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AacApi->get_logical_model_aac: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
        'includeParents': True,
    }
    try:
        # Get logical model in AAC format
        api_response = api_instance.get_logical_model_aac(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AacApi->get_logical_model_aac: %s\n" % e)
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
includeParents | IncludeParentsSchema | | optional


# IncludeParentsSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bool,  | BoolClass,  |  | 

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
200 | [ApiResponseFor200](#get_logical_model_aac.ApiResponseFor200) | Retrieved current logical model in AAC format.

#### get_logical_model_aac.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**AacLogicalModel**](../../models/AacLogicalModel.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **set_analytics_model_aac**
<a id="set_analytics_model_aac"></a>
> set_analytics_model_aac(workspace_idaac_analytics_model)

Set analytics model from AAC format

             Set the analytics model of the workspace using Analytics as Code format.                          The input format is compatible with the YAML definitions used by the              GoodData Analytics as Code VSCode extension. This replaces the entire              analytics model with the provided definition, including metrics,              dashboards, visualizations, plugins, and attribute hierarchies.         

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import aac_api
from gooddata_api_client.model.aac_analytics_model import AacAnalyticsModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = aac_api.AacApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    body = AacAnalyticsModel(
        attribute_hierarchies=[
            AacAttributeHierarchy(
                attributes=["attribute/country","attribute/state","attribute/city"],
                description="description_example",
                id="geo-hierarchy",
                tags=[
                    "tags_example"
                ],
                title="Geographic Hierarchy",
                type="attribute_hierarchy",
            )
        ],
        dashboards=[
            AacDashboard(None)
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
,
                title="Total Sales",
                type="metric",
            )
        ],
        plugins=[
            AacPlugin(
                description="description_example",
                id="my-plugin",
,
                title="My Plugin",
                type="plugin",
                url="https://example.com/plugin.js",
            )
        ],
        visualizations=[
            AacVisualization(
                additional_properties=dict(
                    "key": JsonNode(),
                ),
                attributes=[
                    None
                ],
                columns=[],
                config=JsonNode(),
                description="description_example",
                _from=JsonNode(),
                id="sales-by-region",
                is_hidden=True,
                layers=[
                    AacVisualizationLayer(
                        additional_properties=dict(),
                        config=JsonNode(),
                        filters=dict(
                            "key": AacQueryFilter(
                                additional_properties=dict(),
                                attribute="attribute_example",
                                bottom=1,
                                condition="condition_example",
                                dimensionality=[
                                    "dimensionality_example"
                                ],
                                display_as="display_as_example",
                                _from=None,
                                granularity="granularity_example",
                                null_values_as_zero=True,
                                state=AacFilterState(
                                    exclude=[
                                        "exclude_example"
                                    ],
                                    include=[
                                        "include_example"
                                    ],
                                ),
,
                                top=1,
                                type="date_filter",
                                using="using_example",
                                value=3.14,
                            ),
                        ),
                        id="id_example",
                        metrics=[],
                        segment_by=[],
                        sorts=[
                            JsonNode()
                        ],
                        title="title_example",
                        type="pushpin",
                        view_by=[],
                    )
                ],
                metrics=[],
                query=AacQuery(
                    fields=dict(
,
                    ),
                    filter_by=dict(
                        "key": AacQueryFilter(),
                    ),
                    sort_by=[
                        JsonNode()
                    ],
                ),
                rows=[],
                segment_by=[],
                show_in_ai_results=True,
                size_by=[],
                stack_by=[],
,
                title="Sales by Region",
                to=JsonNode(),
                trend_by=[],
                type="AacVisualizationBasicBuckets",
                view_by=[],
            )
        ],
    )
    try:
        # Set analytics model from AAC format
        api_response = api_instance.set_analytics_model_aac(
            path_params=path_params,
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AacApi->set_analytics_model_aac: %s\n" % e)
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
[**AacAnalyticsModel**](../../models/AacAnalyticsModel.md) |  | 


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
204 | [ApiResponseFor204](#set_analytics_model_aac.ApiResponseFor204) | Analytics model successfully set.

#### set_analytics_model_aac.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **set_logical_model_aac**
<a id="set_logical_model_aac"></a>
> set_logical_model_aac(workspace_idaac_logical_model)

Set logical model from AAC format

             Set the logical data model of the workspace using Analytics as Code format.                          The input format is compatible with the YAML definitions used by the              GoodData Analytics as Code VSCode extension. This replaces the entire              logical model with the provided definition.         

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import aac_api
from gooddata_api_client.model.aac_logical_model import AacLogicalModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = aac_api.AacApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    body = AacLogicalModel(
        datasets=[
            AacDataset(
                data_source="my-postgres",
                description="description_example",
                fields=dict(
                    "key": AacField(
                        aggregated_as="SUM",
                        assigned_to="assigned_to_example",
                        data_type="STRING",
                        default_view="default_view_example",
                        description="description_example",
                        is_hidden=True,
                        labels=dict(
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
                                    "tags_example"
                                ],
                                title="title_example",
                                translations=[
                                    AacLabelTranslation(
                                        locale="locale_example",
                                        source_column="source_column_example",
                                    )
                                ],
                                value_type="TEXT",
                            ),
                        ),
                        locale="locale_example",
                        show_in_ai_results=True,
                        sort_column="sort_column_example",
                        sort_direction="ASC",
                        source_column="source_column_example",
,
                        title="title_example",
                        type="attribute",
                    ),
                ),
                id="customers",
                precedence=1,
                primary_key=None,
                references=[
                    AacReference(
                        dataset="orders",
                        multi_directional=True,
                        sources=[
                            AacReferenceSource(
                                data_type="INT",
                                source_column="source_column_example",
                                target="target_example",
                            )
                        ],
                    )
                ],
                sql="sql_example",
                table_path="public/customers",
,
                title="Customers",
                type="dataset",
                workspace_data_filters=[
                    AacWorkspaceDataFilter(
                        data_type="INT",
                        filter_id="filter_id_example",
                        source_column="source_column_example",
                    )
                ],
            )
        ],
        date_datasets=[
            AacDateDataset(
                description="description_example",
                granularities=[
                    "granularities_example"
                ],
                id="date",
,
                title="Date",
                title_base="title_base_example",
                title_pattern="title_pattern_example",
                type="date",
            )
        ],
    )
    try:
        # Set logical model from AAC format
        api_response = api_instance.set_logical_model_aac(
            path_params=path_params,
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AacApi->set_logical_model_aac: %s\n" % e)
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
[**AacLogicalModel**](../../models/AacLogicalModel.md) |  | 


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
204 | [ApiResponseFor204](#set_logical_model_aac.ApiResponseFor204) | Logical model successfully set.

#### set_logical_model_aac.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


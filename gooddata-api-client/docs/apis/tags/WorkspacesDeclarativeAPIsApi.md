<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.workspaces_declarative_apis_api.WorkspacesDeclarativeAPIsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_workspace_layout**](#get_workspace_layout) | **get** /api/v1/layout/workspaces/{workspaceId} | Get workspace layout
[**get_workspaces_layout**](#get_workspaces_layout) | **get** /api/v1/layout/workspaces | Get all workspaces layout
[**put_workspace_layout**](#put_workspace_layout) | **put** /api/v1/layout/workspaces/{workspaceId} | Set workspace layout
[**set_workspaces_layout**](#set_workspaces_layout) | **put** /api/v1/layout/workspaces | Set all workspaces layout

# **get_workspace_layout**
<a id="get_workspace_layout"></a>
> DeclarativeWorkspaceModel get_workspace_layout(workspace_id)

Get workspace layout

Retrieve current model of the workspace in declarative form.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import workspaces_declarative_apis_api
from gooddata_api_client.model.declarative_workspace_model import DeclarativeWorkspaceModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = workspaces_declarative_apis_api.WorkspacesDeclarativeAPIsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    try:
        # Get workspace layout
        api_response = api_instance.get_workspace_layout(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesDeclarativeAPIsApi->get_workspace_layout: %s\n" % e)
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
200 | [ApiResponseFor200](#get_workspace_layout.ApiResponseFor200) | Retrieved the workspace model.

#### get_workspace_layout.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeWorkspaceModel**](../../models/DeclarativeWorkspaceModel.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_workspaces_layout**
<a id="get_workspaces_layout"></a>
> DeclarativeWorkspaces get_workspaces_layout()

Get all workspaces layout

Gets complete layout of workspaces, their hierarchy, models.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import workspaces_declarative_apis_api
from gooddata_api_client.model.declarative_workspaces import DeclarativeWorkspaces
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = workspaces_declarative_apis_api.WorkspacesDeclarativeAPIsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get all workspaces layout
        api_response = api_instance.get_workspaces_layout()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesDeclarativeAPIsApi->get_workspaces_layout: %s\n" % e)
```
### Parameters
This endpoint does not need any parameter.

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_workspaces_layout.ApiResponseFor200) | Retrieved layout of all workspaces.

#### get_workspaces_layout.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeWorkspaces**](../../models/DeclarativeWorkspaces.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **put_workspace_layout**
<a id="put_workspace_layout"></a>
> put_workspace_layout(workspace_iddeclarative_workspace_model)

Set workspace layout

Set complete layout of workspace, like model, authorization, etc.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import workspaces_declarative_apis_api
from gooddata_api_client.model.declarative_workspace_model import DeclarativeWorkspaceModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = workspaces_declarative_apis_api.WorkspacesDeclarativeAPIsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    body = DeclarativeWorkspaceModel(
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
        ldm=DeclarativeLdm(
            datasets=[
                DeclarativeDataset(
                    attributes=[
                        DeclarativeAttribute(
                            default_view=LabelIdentifier(
                                id="label_id",
                                type="label",
                            ),
                            description="Customer name including first and last name.",
                            id="attr.customers.customer_name",
                            labels=[
                                DeclarativeLabel(
                                    description="Customer name",
                                    id="label.customer_name",
                                    source_column="customer_name",
                                    source_column_data_type="STRING",
                                    tags=["Customers"],
                                    title="Customer name",
                                    value_type="\"TEXT\" | \"HYPERLINK\" | \"GEO\" | \"GEO_LONGITUDE\" | \"GEO_LATITUDE\"",
                                )
                            ],
                            sort_column="customer_name",
                            sort_direction="\"ASC\" | \"DESC\"",
                            source_column="customer_name",
                            source_column_data_type="STRING",
                            tags=["Customers"],
                            title="Customer Name",
                        )
                    ],
                    data_source_table_id=DataSourceTableIdentifier(
                        data_source_id="my-postgres",
                        id="customers",
                        type="dataSource",
                    ),
                    description="The customers of ours.",
                    facts=[
                        DeclarativeFact(
                            description="A number of orders created by the customer - including all orders, even the non-delivered ones.",
                            id="fact.customer_order_count",
                            source_column="customer_order_count",
                            source_column_data_type="NUMERIC",
                            tags=["Customers"],
                            title="Customer order count",
                        )
                    ],
                    grain=[
                        GrainIdentifier(
                            id="attr.customers.customer_name",
                            type="ATTRIBUTE",
                        )
                    ],
                    id="customers",
                    references=[
                        DeclarativeReference(
                            identifier=ReferenceIdentifier(
                                id="customers",
                                type="DATASET",
                            ),
                            multivalue=False,
                            source_column_data_types=[
                                "source_column_data_types_example"
                            ],
                            source_columns=["customer_id"],
                        )
                    ],
                    sql=DeclarativeDatasetSql(
                        data_source_id="my-postgres",
                        statement="SELECT * FROM some_table",
                    ),
                    tags=["Customers"],
                    title="Customers",
                    workspace_data_filter_columns=[
                        DeclarativeWorkspaceDataFilterColumn(
                            data_type="INT",
                            name="customer_id",
                        )
                    ],
                )
            ],
            date_instances=[
                DeclarativeDateDataset(
                    description="A customer order date",
                    granularities=[
                        "MINUTE"
                    ],
                    granularities_formatting=GranularitiesFormatting(
                        title_base="title_base_example",
                        title_pattern="%titleBase - %granularityTitle",
                    ),
                    id="date",
                    tags=["Customer dates"],
                    title="Date",
                )
            ],
        ),
    )
    try:
        # Set workspace layout
        api_response = api_instance.put_workspace_layout(
            path_params=path_params,
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesDeclarativeAPIsApi->put_workspace_layout: %s\n" % e)
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
[**DeclarativeWorkspaceModel**](../../models/DeclarativeWorkspaceModel.md) |  | 


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
204 | [ApiResponseFor204](#put_workspace_layout.ApiResponseFor204) | The model of the workspace was set.

#### put_workspace_layout.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **set_workspaces_layout**
<a id="set_workspaces_layout"></a>
> set_workspaces_layout(declarative_workspaces)

Set all workspaces layout

Sets complete layout of workspaces, their hierarchy, models.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import workspaces_declarative_apis_api
from gooddata_api_client.model.declarative_workspaces import DeclarativeWorkspaces
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = workspaces_declarative_apis_api.WorkspacesDeclarativeAPIsApi(api_client)

    # example passing only required values which don't have defaults set
    body = DeclarativeWorkspaces(
        workspace_data_filters=[
            DeclarativeWorkspaceDataFilter(
                column_name="country_id",
                description="ID of country",
                id="country_id",
                title="Country ID",
                workspace=WorkspaceIdentifier(
                    id="alpha.sales",
                    type="workspace",
                ),
                workspace_data_filter_settings=[
                    DeclarativeWorkspaceDataFilterSetting(
                        description="ID of country setting",
                        filter_values=["US"],
                        id="country_id_setting",
                        title="Country ID setting",
                        workspace=WorkspaceIdentifier(),
                    )
                ],
            )
        ],
        workspaces=[
            DeclarativeWorkspace(
                custom_application_settings=[
                    DeclarativeCustomApplicationSetting(
                        application_name="Modeler",
                        content=dict(),
                        id="modeler.demo",
                    )
                ],
                description="description_example",
                early_access="early_access_example",
                hierarchy_permissions=[
                    DeclarativeWorkspaceHierarchyPermission(
                        assignee=AssigneeIdentifier(
                            id="id_example",
                            type="user",
                        ),
                        name="MANAGE",
                    )
                ],
                id="alpha.sales",
                model=DeclarativeWorkspaceModel(
                    analytics=DeclarativeAnalyticsLayer(
                        analytical_dashboard_extensions=[
                            DeclarativeAnalyticalDashboardExtension(
                                id="revenues-analysis",
                                permissions=[
                                    DeclarativeAnalyticalDashboardPermission(
                                        assignee=AssigneeIdentifier(),
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
                    ldm=DeclarativeLdm(
                        datasets=[
                            DeclarativeDataset(
                                attributes=[
                                    DeclarativeAttribute(
                                        default_view=LabelIdentifier(
                                            id="label_id",
                                            type="label",
                                        ),
                                        description="Customer name including first and last name.",
                                        id="attr.customers.customer_name",
                                        labels=[
                                            DeclarativeLabel(
                                                description="Customer name",
                                                id="label.customer_name",
                                                source_column="customer_name",
                                                source_column_data_type="STRING",
                                                tags=["Customers"],
                                                title="Customer name",
                                                value_type="\"TEXT\" | \"HYPERLINK\" | \"GEO\" | \"GEO_LONGITUDE\" | \"GEO_LATITUDE\"",
                                            )
                                        ],
                                        sort_column="customer_name",
                                        sort_direction="\"ASC\" | \"DESC\"",
                                        source_column="customer_name",
                                        source_column_data_type="STRING",
                                        tags=["Customers"],
                                        title="Customer Name",
                                    )
                                ],
                                data_source_table_id=DataSourceTableIdentifier(
                                    data_source_id="my-postgres",
                                    id="customers",
                                    type="dataSource",
                                ),
                                description="The customers of ours.",
                                facts=[
                                    DeclarativeFact(
                                        description="A number of orders created by the customer - including all orders, even the non-delivered ones.",
                                        id="fact.customer_order_count",
                                        source_column="customer_order_count",
                                        source_column_data_type="NUMERIC",
                                        tags=["Customers"],
                                        title="Customer order count",
                                    )
                                ],
                                grain=[
                                    GrainIdentifier(
                                        id="attr.customers.customer_name",
                                        type="ATTRIBUTE",
                                    )
                                ],
                                id="customers",
                                references=[
                                    DeclarativeReference(
                                        identifier=ReferenceIdentifier(
                                            id="customers",
                                            type="DATASET",
                                        ),
                                        multivalue=False,
                                        source_column_data_types=[
                                            "source_column_data_types_example"
                                        ],
                                        source_columns=["customer_id"],
                                    )
                                ],
                                sql=DeclarativeDatasetSql(
                                    data_source_id="my-postgres",
                                    statement="SELECT * FROM some_table",
                                ),
                                tags=["Customers"],
                                title="Customers",
                                workspace_data_filter_columns=[
                                    DeclarativeWorkspaceDataFilterColumn(
                                        data_type="INT",
                                        name="customer_id",
                                    )
                                ],
                            )
                        ],
                        date_instances=[
                            DeclarativeDateDataset(
                                description="A customer order date",
                                granularities=[
                                    "MINUTE"
                                ],
                                granularities_formatting=GranularitiesFormatting(
                                    title_base="title_base_example",
                                    title_pattern="%titleBase - %granularityTitle",
                                ),
                                id="date",
                                tags=["Customer dates"],
                                title="Date",
                            )
                        ],
                    ),
                ),
                name="Alpha Sales",
                parent=WorkspaceIdentifier(),
                permissions=[
                    DeclarativeSingleWorkspacePermission()
                ],
                prefix="/6bUUGjjNSwg0_bs",
                settings=[
                    DeclarativeSetting(
                        content=dict(),
                        id="/6bUUGjjNSwg0_bs",
                        type="TIMEZONE",
                    )
                ],
                user_data_filters=[
                    DeclarativeUserDataFilter(
                        description="ID of country setting",
                        id="country_id_setting",
                        maql="{label/country} = \"USA\" AND {label/date.year} = THIS(YEAR)",
                        tags=["Revenues"],
                        title="Country ID setting",
                        user=UserIdentifier(
                            id="employee123",
                            type="user",
                        ),
                        user_group=UserGroupIdentifier(
                            id="group.admins",
                            type="userGroup",
                        ),
                    )
                ],
            )
        ],
    )
    try:
        # Set all workspaces layout
        api_response = api_instance.set_workspaces_layout(
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesDeclarativeAPIsApi->set_workspaces_layout: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeWorkspaces**](../../models/DeclarativeWorkspaces.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#set_workspaces_layout.ApiResponseFor204) | All workspaces layout set.

#### set_workspaces_layout.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


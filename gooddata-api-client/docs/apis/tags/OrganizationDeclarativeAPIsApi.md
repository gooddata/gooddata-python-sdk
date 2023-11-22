<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.organization_declarative_apis_api.OrganizationDeclarativeAPIsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_organization_layout**](#get_organization_layout) | **get** /api/v1/layout/organization | Get organization layout
[**set_organization_layout**](#set_organization_layout) | **put** /api/v1/layout/organization | Set organization layout

# **get_organization_layout**
<a id="get_organization_layout"></a>
> DeclarativeOrganization get_organization_layout()

Get organization layout

Retrieve complete layout of organization, workspaces, user-groups, etc.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_declarative_apis_api
from gooddata_api_client.model.declarative_organization import DeclarativeOrganization
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_declarative_apis_api.OrganizationDeclarativeAPIsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get organization layout
        api_response = api_instance.get_organization_layout()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationDeclarativeAPIsApi->get_organization_layout: %s\n" % e)
```
### Parameters
This endpoint does not need any parameter.

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_organization_layout.ApiResponseFor200) | Retrieved all parts of an organization.

#### get_organization_layout.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeOrganization**](../../models/DeclarativeOrganization.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **set_organization_layout**
<a id="set_organization_layout"></a>
> set_organization_layout(declarative_organization)

Set organization layout

Sets complete layout of organization, like workspaces, user-groups, etc.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_declarative_apis_api
from gooddata_api_client.model.declarative_organization import DeclarativeOrganization
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_declarative_apis_api.OrganizationDeclarativeAPIsApi(api_client)

    # example passing only required values which don't have defaults set
    body = DeclarativeOrganization(
        data_sources=[
            DeclarativeDataSource(
                cache_path=[
                    "[ \"dfs\", \"data\" ]. Example used in Apache Drill."
                ],
                decoded_parameters=[
                    Parameter(
                        name="name_example",
                        value="value_example",
                    )
                ],
                enable_caching=False,
                id="pg_local_docker-demo",
                name="postgres demo",
,
                password="*****",
                pdm=DeclarativeTables(
                    tables=[
                        DeclarativeTable(
                            columns=[
                                DeclarativeColumn(
                                    data_type="INT",
                                    is_primary_key=True,
                                    name="customer_id",
                                    referenced_table_column="customer_id",
                                    referenced_table_id="customers",
                                )
                            ],
                            id="customers",
                            name_prefix="out_gooddata",
                            path=["table_schema","table_name"],
                            type="VIEW",
                        )
                    ],
                ),
                permissions=[
                    DeclarativeDataSourcePermission(
                        assignee=AssigneeIdentifier(
                            id="id_example",
                            type="user",
                        ),
                        name="MANAGE",
                    )
                ],
                schema="demo",
                token="Bigquery service account JSON. Encode it using base64!",
                type="POSTGRESQL",
                url="jdbc:postgresql://postgres:5432/gooddata",
                username="demo",
            )
        ],
        organization=DeclarativeOrganizationInfo(
            color_palettes=[
                DeclarativeColorPalette(
                    content=dict(),
                    id="id_example",
                    name="name_example",
                )
            ],
            csp_directives=[
                DeclarativeCspDirective(
                    directive="directive_example",
                    sources=[
                        "sources_example"
                    ],
                )
            ],
            early_access="early_access_example",
            hostname="alpha.com",
            id="Alpha corporation",
            name="Alpha corporation",
            oauth_client_id="oauth_client_id_example",
            oauth_client_secret="oauth_client_secret_example",
            oauth_issuer_id="myOidcProvider",
            oauth_issuer_location="oauth_issuer_location_example",
            permissions=[
                DeclarativeOrganizationPermission(
                    assignee=AssigneeIdentifier(),
                    name="MANAGE",
                )
            ],
            settings=[
                DeclarativeSetting(
                    content=dict(),
                    id="/6bUUGjjNSwg0_bs",
                    type="TIMEZONE",
                )
            ],
            themes=[
                DeclarativeTheme(
                    content=dict(),
                    id="id_example",
                    name="name_example",
                )
            ],
        ),
        user_groups=[
            DeclarativeUserGroup(
                id="employees.all",
                name="admins",
                parents=[
                    UserGroupIdentifier(
                        id="group.admins",
                        type="userGroup",
                    )
                ],
                permissions=[
                    DeclarativeUserGroupPermission(
                        assignee=AssigneeIdentifier(),
                        name="SEE",
                    )
                ],
            )
        ],
        users=[
            DeclarativeUser(
                auth_id="auth_id_example",
                email="user@example.com",
                firstname="John",
                id="employee123",
                lastname="Wick",
                permissions=[
                    DeclarativeUserPermission(
                        assignee=AssigneeIdentifier(),
                        name="SEE",
                    )
                ],
                settings=[
                    DeclarativeSetting()
                ],
,
            )
        ],
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
                        assignee=AssigneeIdentifier(),
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
                    DeclarativeSetting()
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
                        user_group=UserGroupIdentifier(),
                    )
                ],
            )
        ],
    )
    try:
        # Set organization layout
        api_response = api_instance.set_organization_layout(
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationDeclarativeAPIsApi->set_organization_layout: %s\n" % e)
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
[**DeclarativeOrganization**](../../models/DeclarativeOrganization.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#set_organization_layout.ApiResponseFor204) | Defined all parts of an organization.

#### set_organization_layout.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


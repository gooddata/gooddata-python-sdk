# gooddata_api_client.OrganizationDeclarativeAPIsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_organization_layout**](OrganizationDeclarativeAPIsApi.md#get_organization_layout) | **GET** /api/v1/layout/organization | Get organization layout
[**set_organization_layout**](OrganizationDeclarativeAPIsApi.md#set_organization_layout) | **PUT** /api/v1/layout/organization | Set organization layout


# **get_organization_layout**
> DeclarativeOrganization get_organization_layout()

Get organization layout

Retrieve complete layout of organization, workspaces, user-groups, etc.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import organization_declarative_apis_api
from gooddata_api_client.model.declarative_organization import DeclarativeOrganization
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
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

### Return type

[**DeclarativeOrganization**](DeclarativeOrganization.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved all parts of an organization. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_organization_layout**
> set_organization_layout(declarative_organization)

Set organization layout

Sets complete layout of organization, like workspaces, user-groups, etc.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import organization_declarative_apis_api
from gooddata_api_client.model.declarative_organization import DeclarativeOrganization
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_declarative_apis_api.OrganizationDeclarativeAPIsApi(api_client)
    declarative_organization = DeclarativeOrganization(
        data_sources=[
            DeclarativeDataSource(
                cache_path=[
                    "[ "dfs", "data" ]. Example used in Apache Drill.",
                ],
                decoded_parameters=[
                    Parameter(
                        name="name_example",
                        value="value_example",
                    ),
                ],
                enable_caching=False,
                id="pg_local_docker-demo",
                name="postgres demo",
                parameters=[
                    Parameter(
                        name="name_example",
                        value="value_example",
                    ),
                ],
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
                                ),
                            ],
                            id="customers",
                            name_prefix="out_gooddata",
                            path=["table_schema","table_name"],
                            type="TABLE",
                        ),
                    ],
                ),
                permissions=[
                    DeclarativeDataSourcePermission(
                        assignee=AssigneeIdentifier(
                            id="id_example",
                            type="user",
                        ),
                        name="MANAGE",
                    ),
                ],
                schema="demo",
                token="Bigquery service account JSON. Encode it using base64!",
                type="POSTGRESQL",
                url="jdbc:postgresql://postgres:5432/gooddata",
                username="demo",
            ),
        ],
        organization=DeclarativeOrganizationInfo(
            color_palettes=[
                DeclarativeColorPalette(
                    content={},
                    id="id_example",
                    name="name_example",
                ),
            ],
            csp_directives=[
                DeclarativeCspDirective(
                    directive="directive_example",
                    sources=[
                        "sources_example",
                    ],
                ),
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
                    assignee=AssigneeIdentifier(
                        id="id_example",
                        type="user",
                    ),
                    name="MANAGE",
                ),
            ],
            settings=[
                DeclarativeSetting(
                    content={},
                    id="/6bUUGjjNSwg0_bs",
                    type="TIMEZONE",
                ),
            ],
            themes=[
                DeclarativeTheme(
                    content={},
                    id="id_example",
                    name="name_example",
                ),
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
                    ),
                ],
                permissions=[
                    DeclarativeUserGroupPermission(
                        assignee=AssigneeIdentifier(
                            id="id_example",
                            type="user",
                        ),
                        name="SEE",
                    ),
                ],
            ),
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
                        assignee=AssigneeIdentifier(
                            id="id_example",
                            type="user",
                        ),
                        name="SEE",
                    ),
                ],
                settings=[
                    DeclarativeSetting(
                        content={},
                        id="/6bUUGjjNSwg0_bs",
                        type="TIMEZONE",
                    ),
                ],
                user_groups=[
                    UserGroupIdentifier(
                        id="group.admins",
                        type="userGroup",
                    ),
                ],
            ),
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
                        workspace=WorkspaceIdentifier(
                            id="alpha.sales",
                            type="workspace",
                        ),
                    ),
                ],
            ),
        ],
        workspaces=[
            DeclarativeWorkspace(
                cache_extra_limit=1,
                custom_application_settings=[
                    DeclarativeCustomApplicationSetting(
                        application_name="Modeler",
                        content={},
                        id="modeler.demo",
                    ),
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
                    ),
                ],
                id="alpha.sales",
                model=DeclarativeWorkspaceModel(
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
                                    ),
                                ],
                            ),
                        ],
                        analytical_dashboards=[
                            DeclarativeAnalyticalDashboard(
                                content={},
                                description="Period to period comparison of revenues in main sectors.",
                                id="revenues-analysis",
                                permissions=[
                                    DeclarativeAnalyticalDashboardPermission(
                                        assignee=AssigneeIdentifier(
                                            id="id_example",
                                            type="user",
                                        ),
                                        name="EDIT",
                                    ),
                                ],
                                tags=["Revenues"],
                                title="Revenues analysis",
                            ),
                        ],
                        dashboard_plugins=[
                            DeclarativeDashboardPlugin(
                                content={},
                                description="Three dimensional view of data.",
                                id="dashboard-plugin-1",
                                tags=["Revenues"],
                                title="3D map renderer",
                            ),
                        ],
                        filter_contexts=[
                            DeclarativeFilterContext(
                                content={},
                                description="Filter Context for Sales team.",
                                id="filter-sales",
                                tags=["Revenues"],
                                title="Filter Context for Sales team",
                            ),
                        ],
                        metrics=[
                            DeclarativeMetric(
                                content={},
                                description="Sales for all the data available.",
                                id="total-sales",
                                tags=["Revenues"],
                                title="Total sales",
                            ),
                        ],
                        visualization_objects=[
                            DeclarativeVisualizationObject(
                                content={},
                                description="Simple number for total goods in current production.",
                                id="visualization-1",
                                tags=["Revenues"],
                                title="Count of goods",
                            ),
                        ],
                    ),
                    ldm=DeclarativeLdm(
                        dataset_extensions=[
                            DeclarativeDatasetExtension(
                                id="customers",
                                workspace_data_filter_references=[
                                    DeclarativeWorkspaceDataFilterReferences(
                                        filter_column="filter_id",
                                        filter_column_data_type="INT",
                                        filter_id=DatasetWorkspaceDataFilterIdentifier(
                                            id="country_id",
                                            type="workspaceDataFilter",
                                        ),
                                    ),
                                ],
                            ),
                        ],
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
                                                value_type="TEXT" | "HYPERLINK" | "GEO" | "GEO_LONGITUDE" | "GEO_LATITUDE",
                                            ),
                                        ],
                                        sort_column="customer_name",
                                        sort_direction="ASC" | "DESC",
                                        source_column="customer_name",
                                        source_column_data_type="STRING",
                                        tags=["Customers"],
                                        title="Customer Name",
                                    ),
                                ],
                                data_source_table_id=DataSourceTableIdentifier(
                                    data_source_id="my-postgres",
                                    id="customers",
                                    path=["table_schema","table_name"],
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
                                    ),
                                ],
                                grain=[
                                    GrainIdentifier(
                                        id="attr.customers.customer_name",
                                        type="ATTRIBUTE",
                                    ),
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
                                            "INT",
                                        ],
                                        source_columns=["customer_id"],
                                    ),
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
                                    ),
                                ],
                                workspace_data_filter_references=[
                                    DeclarativeWorkspaceDataFilterReferences(
                                        filter_column="filter_id",
                                        filter_column_data_type="INT",
                                        filter_id=DatasetWorkspaceDataFilterIdentifier(
                                            id="country_id",
                                            type="workspaceDataFilter",
                                        ),
                                    ),
                                ],
                            ),
                        ],
                        date_instances=[
                            DeclarativeDateDataset(
                                description="A customer order date",
                                granularities=[
                                    "MINUTE",
                                ],
                                granularities_formatting=GranularitiesFormatting(
                                    title_base="title_base_example",
                                    title_pattern="%titleBase - %granularityTitle",
                                ),
                                id="date",
                                tags=["Customer dates"],
                                title="Date",
                            ),
                        ],
                    ),
                ),
                name="Alpha Sales",
                parent=WorkspaceIdentifier(
                    id="alpha.sales",
                    type="workspace",
                ),
                permissions=[
                    DeclarativeSingleWorkspacePermission(
                        assignee=AssigneeIdentifier(
                            id="id_example",
                            type="user",
                        ),
                        name="MANAGE",
                    ),
                ],
                prefix="/6bUUGjjNSwg0_bs",
                settings=[
                    DeclarativeSetting(
                        content={},
                        id="/6bUUGjjNSwg0_bs",
                        type="TIMEZONE",
                    ),
                ],
                user_data_filters=[
                    DeclarativeUserDataFilter(
                        description="ID of country setting",
                        id="country_id_setting",
                        maql="{label/country} = "USA" AND {label/date.year} = THIS(YEAR)",
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
                    ),
                ],
            ),
        ],
    ) # DeclarativeOrganization | 

    # example passing only required values which don't have defaults set
    try:
        # Set organization layout
        api_instance.set_organization_layout(declarative_organization)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationDeclarativeAPIsApi->set_organization_layout: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **declarative_organization** | [**DeclarativeOrganization**](DeclarativeOrganization.md)|  |

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
**204** | Defined all parts of an organization. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


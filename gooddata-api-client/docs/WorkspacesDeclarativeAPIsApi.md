# gooddata_api_client.WorkspacesDeclarativeAPIsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_workspace_layout**](WorkspacesDeclarativeAPIsApi.md#get_workspace_layout) | **GET** /api/v1/layout/workspaces/{workspaceId} | Get workspace layout
[**get_workspaces_layout**](WorkspacesDeclarativeAPIsApi.md#get_workspaces_layout) | **GET** /api/v1/layout/workspaces | Get all workspaces layout
[**put_workspace_layout**](WorkspacesDeclarativeAPIsApi.md#put_workspace_layout) | **PUT** /api/v1/layout/workspaces/{workspaceId} | Set workspace layout
[**set_workspaces_layout**](WorkspacesDeclarativeAPIsApi.md#set_workspaces_layout) | **PUT** /api/v1/layout/workspaces | Set all workspaces layout


# **get_workspace_layout**
> DeclarativeWorkspaceModel get_workspace_layout(workspace_id)

Get workspace layout

Retrieve current model of the workspace in declarative form.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspaces_declarative_apis_api
from gooddata_api_client.model.declarative_workspace_model import DeclarativeWorkspaceModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspaces_declarative_apis_api.WorkspacesDeclarativeAPIsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    exclude = [
        "ACTIVITY_INFO",
    ] # [str] |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get workspace layout
        api_response = api_instance.get_workspace_layout(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesDeclarativeAPIsApi->get_workspace_layout: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get workspace layout
        api_response = api_instance.get_workspace_layout(workspace_id, exclude=exclude)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesDeclarativeAPIsApi->get_workspace_layout: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **exclude** | **[str]**|  | [optional]

### Return type

[**DeclarativeWorkspaceModel**](DeclarativeWorkspaceModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved the workspace model. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_workspaces_layout**
> DeclarativeWorkspaces get_workspaces_layout()

Get all workspaces layout

Gets complete layout of workspaces, their hierarchy, models.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspaces_declarative_apis_api
from gooddata_api_client.model.declarative_workspaces import DeclarativeWorkspaces
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspaces_declarative_apis_api.WorkspacesDeclarativeAPIsApi(api_client)
    exclude = [
        "ACTIVITY_INFO",
    ] # [str] |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all workspaces layout
        api_response = api_instance.get_workspaces_layout(exclude=exclude)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesDeclarativeAPIsApi->get_workspaces_layout: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **exclude** | **[str]**|  | [optional]

### Return type

[**DeclarativeWorkspaces**](DeclarativeWorkspaces.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved layout of all workspaces. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_workspace_layout**
> put_workspace_layout(workspace_id, declarative_workspace_model)

Set workspace layout

Set complete layout of workspace, like model, authorization, etc.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspaces_declarative_apis_api
from gooddata_api_client.model.declarative_workspace_model import DeclarativeWorkspaceModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspaces_declarative_apis_api.WorkspacesDeclarativeAPIsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    declarative_workspace_model = DeclarativeWorkspaceModel(
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
                                    value_type="TEXT",
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
                            sources=[
                                DeclarativeReferenceSource(
                                    column="customer_id",
                                    data_type="STRING",
                                    target=GrainIdentifier(
                                        id="attr.customers.customer_name",
                                        type="ATTRIBUTE",
                                    ),
                                ),
                            ],
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
    ) # DeclarativeWorkspaceModel | 

    # example passing only required values which don't have defaults set
    try:
        # Set workspace layout
        api_instance.put_workspace_layout(workspace_id, declarative_workspace_model)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesDeclarativeAPIsApi->put_workspace_layout: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **declarative_workspace_model** | [**DeclarativeWorkspaceModel**](DeclarativeWorkspaceModel.md)|  |

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
**204** | The model of the workspace was set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_workspaces_layout**
> set_workspaces_layout(declarative_workspaces)

Set all workspaces layout

Sets complete layout of workspaces, their hierarchy, models.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspaces_declarative_apis_api
from gooddata_api_client.model.declarative_workspaces import DeclarativeWorkspaces
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspaces_declarative_apis_api.WorkspacesDeclarativeAPIsApi(api_client)
    declarative_workspaces = DeclarativeWorkspaces(
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
                automations=[
                    DeclarativeAutomation(
                        alert=AutomationAlert(
                            condition=AutomationAlertCondition(None),
                            execution=AlertAfm(
                                attributes=[
                                    AttributeItem(
                                        label=AfmObjectIdentifierLabel(
                                            identifier=AfmObjectIdentifierLabelIdentifier(
                                                id="sample_item.price",
                                                type="label",
                                            ),
                                        ),
                                        local_identifier="attribute_1",
                                        show_all_values=False,
                                    ),
                                ],
                                aux_measures=[
                                    MeasureItem(
                                        definition=MeasureDefinition(),
                                        local_identifier="metric_1",
                                    ),
                                ],
                                filters=[
                                    FilterDefinition(),
                                ],
                                measures=[
                                    MeasureItem(
                                        definition=MeasureDefinition(),
                                        local_identifier="metric_1",
                                    ),
                                ],
                            ),
                            trigger="ALWAYS",
                        ),
                        analytical_dashboard=DeclarativeAnalyticalDashboardIdentifier(
                            id="dashboard123",
                            type="analyticalDashboard",
                        ),
                        created_at="2023-07-20 12:30",
                        created_by=DeclarativeUserIdentifier(
                            id="employee123",
                            type="user",
                        ),
                        description="description_example",
                        details={
                            "key": "key_example",
                        },
                        export_definitions=[
                            DeclarativeExportDefinitionIdentifier(
                                id="export123",
                                type="exportDefinition",
                            ),
                        ],
                        external_recipients=[
                            AutomationExternalRecipient(
                                email="email_example",
                            ),
                        ],
                        id="/6bUUGjjNSwg0_bs",
                        image_exports=[
                            AutomationImageExport(
                                request_payload=ImageExportRequest(
                                    dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                                    file_name="filename",
                                    format="PNG",
                                    metadata=JsonNode(),
                                    widget_ids=[
                                        "widget_ids_example",
                                    ],
                                ),
                            ),
                        ],
                        metadata=AutomationMetadata(
                            visible_filters=[
                                VisibleFilter(
                                    is_all_time_date_filter=False,
                                    local_identifier="local_identifier_example",
                                    title="title_example",
                                ),
                            ],
                            widget="widget_example",
                        ),
                        modified_at="2023-07-20 12:30",
                        modified_by=DeclarativeUserIdentifier(
                            id="employee123",
                            type="user",
                        ),
                        notification_channel=DeclarativeNotificationChannelIdentifier(
                            id="webhook123",
                            type="notificationChannel",
                        ),
                        recipients=[
                            DeclarativeUserIdentifier(
                                id="employee123",
                                type="user",
                            ),
                        ],
                        schedule=AutomationSchedule(
                            cron="0 */30 9-17 ? * MON-FRI",
                            first_run=dateutil_parser('2025-01-01T12:00:00Z'),
                            timezone="Europe/Prague",
                        ),
                        state="ACTIVE",
                        tabular_exports=[
                            AutomationTabularExport(
                                request_payload=TabularExportRequest(
                                    custom_override=CustomOverride(
                                        labels={
                                            "key": CustomLabel(
                                                title="title_example",
                                            ),
                                        },
                                        metrics={
                                            "key": CustomMetric(
                                                format="format_example",
                                                title="title_example",
                                            ),
                                        },
                                    ),
                                    execution_result="ff483727196c9dc862c7fd3a5a84df55c96d61a4",
                                    file_name="result",
                                    format="CSV",
                                    metadata=JsonNode(),
                                    related_dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                                    settings=Settings(
                                        merge_headers=True,
                                        pdf_page_size="a4 landscape",
                                        pdf_table_style=[
                                            PdfTableStyle(
                                                properties=[
                                                    PdfTableStyleProperty(
                                                        key="key_example",
                                                        value="value_example",
                                                    ),
                                                ],
                                                selector="selector_example",
                                            ),
                                        ],
                                        pdf_top_left_content="Good",
                                        pdf_top_right_content="Morning",
                                        show_filters=False,
                                    ),
                                    visualization_object="f7c359bc-c230-4487-b15b-ad9685bcb537",
                                    visualization_object_custom_filters=[
                                        {},
                                    ],
                                ),
                            ),
                        ],
                        tags=[
                            "["Revenue","Sales"]",
                        ],
                        title="title_example",
                        visual_exports=[
                            AutomationVisualExport(
                                request_payload=VisualExportRequest(
                                    dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                                    file_name="filename",
                                    metadata={},
                                ),
                            ),
                        ],
                    ),
                ],
                cache_extra_limit=1,
                custom_application_settings=[
                    DeclarativeCustomApplicationSetting(
                        application_name="Modeler",
                        content=JsonNode(),
                        id="modeler.demo",
                    ),
                ],
                data_source=WorkspaceDataSource(
                    id="snowflake.instance.1",
                    schema_path=[
                        "subPath",
                    ],
                ),
                description="description_example",
                early_access="early_access_example",
                early_access_values=[
                    "early_access_values_example",
                ],
                filter_views=[
                    DeclarativeFilterView(
                        analytical_dashboard=DeclarativeAnalyticalDashboardIdentifier(
                            id="dashboard123",
                            type="analyticalDashboard",
                        ),
                        content=JsonNode(),
                        description="description_example",
                        id="filterView-1",
                        is_default=True,
                        tags=[
                            "["Revenue","Sales"]",
                        ],
                        title="title_example",
                        user=DeclarativeUserIdentifier(
                            id="employee123",
                            type="user",
                        ),
                    ),
                ],
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
                                                value_type="TEXT",
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
                                        sources=[
                                            DeclarativeReferenceSource(
                                                column="customer_id",
                                                data_type="STRING",
                                                target=GrainIdentifier(
                                                    id="attr.customers.customer_name",
                                                    type="ATTRIBUTE",
                                                ),
                                            ),
                                        ],
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
                        content=JsonNode(),
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
                        user=DeclarativeUserIdentifier(
                            id="employee123",
                            type="user",
                        ),
                        user_group=DeclarativeUserGroupIdentifier(
                            id="group.admins",
                            type="userGroup",
                        ),
                    ),
                ],
            ),
        ],
    ) # DeclarativeWorkspaces | 

    # example passing only required values which don't have defaults set
    try:
        # Set all workspaces layout
        api_instance.set_workspaces_layout(declarative_workspaces)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesDeclarativeAPIsApi->set_workspaces_layout: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **declarative_workspaces** | [**DeclarativeWorkspaces**](DeclarativeWorkspaces.md)|  |

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
**204** | All workspaces layout set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


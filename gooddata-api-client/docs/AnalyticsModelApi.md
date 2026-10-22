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
                    certification="CERTIFIED",
                    certification_message="certification_message_example",
                    certified_at="0480-72-88 80:01",
                    certified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
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
                    summary="summary_example",
                    tags=["Revenues"],
                    title="Revenues analysis",
                ),
            ],
            attribute_hierarchies=[
                DeclarativeAttributeHierarchy(
                    content=JsonNode(),
                    created_at="2023-07-20 12:30",
                    created_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    description="Simple number for total goods in current production.",
                    id="hierarchy-1",
                    modified_at="2023-07-20 12:30",
                    modified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    tags=["Revenues"],
                    title="Count of goods",
                ),
            ],
            computed_attributes=[
                DeclarativeComputedAttribute(
                    certification="CERTIFIED",
                    certification_message="certification_message_example",
                    certified_at="0480-72-88 80:01",
                    certified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    content=DeclarativeComputedAttributeContent(
                        format="%0.2f",
                        maql="SELECT 1",
                        metric_type="UNSPECIFIED",
                    ),
                    created_at="2023-07-20 12:30",
                    created_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    data_type="STRING",
                    description="Sales for all the data available.",
                    id="total-sales",
                    is_hidden=False,
                    is_nullable=False,
                    locale="en-US",
                    modified_at="2023-07-20 12:30",
                    modified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    null_value="empty_value",
                    tags=["Revenues"],
                    title="Total sales",
                    value_type="TEXT",
                ),
            ],
            dashboard_plugins=[
                DeclarativeDashboardPlugin(
                    content=JsonNode(),
                    created_at="2023-07-20 12:30",
                    created_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    description="Three dimensional view of data.",
                    id="dashboard-plugin-1",
                    modified_at="2023-07-20 12:30",
                    modified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    tags=["Revenues"],
                    title="3D map renderer",
                ),
            ],
            document_templates=[
                DeclarativePublisherDocumentTemplate(
                    content=PublisherDocumentContent(
                        attribute_filter_configs=[
                            PublisherDocumentAttributeFilterConfig(
                                display_as_label=PublisherDocumentObjRef(
                                    identifier="identifier_example",
                                    type="type_example",
                                ),
                                local_identifier="26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1",
                                mode="readonly",
                                selection_type="list",
                            ),
                        ],
                        defaults=PublisherDocumentDefaults(
                            page_size="widescreen",
                            period=PublisherDocumentPeriod(),
                            takeaway=PublisherDocumentTakeawayDefaults(
                                generation=PublisherDocumentTakeawayGeneration(
                                    context=PublisherDocumentTakeawayContext(
                                        filters=True,
                                        other_pages=True,
                                        page_title=True,
                                        widgets=[
                                            "26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1",
                                        ],
                                    ),
                                    instructions="instructions_example",
                                ),
                            ),
                        ),
                        filters=[
                            PublisherDocumentFilter(),
                        ],
                        format_locale="format_locale_example",
                        locale="locale_example",
                        pages=[
                            PublisherDocumentPage(
                                filters=[
                                    PublisherDocumentFilter(),
                                ],
                                id="26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1",
                                kind="cover",
                                layout=PublisherDocumentLayoutNode(),
                                notes="notes_example",
                                page_size="widescreen",
                                style=PublisherDocumentPageStyle(
                                    background_color="background_color_example",
                                    background_fit="cover",
                                    background_horizontal_align="left",
                                    background_image="background_image_example",
                                    background_image_opacity=0,
                                    background_offset=0,
                                    background_offset_bottom=0,
                                    background_offset_left=0,
                                    background_offset_right=0,
                                    background_offset_top=0,
                                    background_opacity=0,
                                    background_vertical_align="top",
                                    font_size=0,
                                    font_style="normal",
                                    font_weight=1,
                                    gap=PublisherDocumentAreaStyleGap(None),
                                    horizontal_align="left",
                                    letter_spacing=3.14,
                                    line_height=3.14,
                                    padding=PublisherDocumentContainerStylePadding(None),
                                    padding_bottom=PublisherDocumentContainerStylePadding(None),
                                    padding_left=PublisherDocumentContainerStylePadding(None),
                                    padding_right=PublisherDocumentContainerStylePadding(None),
                                    padding_top=PublisherDocumentContainerStylePadding(None),
                                    text_color="text_color_example",
                                    text_overflow="shrink",
                                    text_style="title",
                                    text_transform="none",
                                    vertical_align="top",
                                ),
                                visible=True,
                            ),
                        ],
                        sections=[
                            PublisherDocumentSection(
                                description="description_example",
                                id="26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1",
                                pages=[
                                    PublisherDocumentPage(
                                        filters=[
                                            PublisherDocumentFilter(),
                                        ],
                                        id="26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1",
                                        kind="cover",
                                        layout=PublisherDocumentLayoutNode(),
                                        notes="notes_example",
                                        page_size="widescreen",
                                        style=PublisherDocumentPageStyle(
                                            background_color="background_color_example",
                                            background_fit="cover",
                                            background_horizontal_align="left",
                                            background_image="background_image_example",
                                            background_image_opacity=0,
                                            background_offset=0,
                                            background_offset_bottom=0,
                                            background_offset_left=0,
                                            background_offset_right=0,
                                            background_offset_top=0,
                                            background_opacity=0,
                                            background_vertical_align="top",
                                            font_size=0,
                                            font_style="normal",
                                            font_weight=1,
                                            gap=PublisherDocumentAreaStyleGap(None),
                                            horizontal_align="left",
                                            letter_spacing=3.14,
                                            line_height=3.14,
                                            padding=PublisherDocumentContainerStylePadding(None),
                                            padding_bottom=PublisherDocumentContainerStylePadding(None),
                                            padding_left=PublisherDocumentContainerStylePadding(None),
                                            padding_right=PublisherDocumentContainerStylePadding(None),
                                            padding_top=PublisherDocumentContainerStylePadding(None),
                                            text_color="text_color_example",
                                            text_overflow="shrink",
                                            text_style="title",
                                            text_transform="none",
                                            vertical_align="top",
                                        ),
                                        visible=True,
                                    ),
                                ],
                                title="title_example",
                            ),
                        ],
                        style=PublisherDocumentAreaStyle(
                            background_color="background_color_example",
                            background_fit="cover",
                            background_horizontal_align="left",
                            background_image="background_image_example",
                            background_image_opacity=0,
                            background_offset=0,
                            background_offset_bottom=0,
                            background_offset_left=0,
                            background_offset_right=0,
                            background_offset_top=0,
                            background_opacity=0,
                            background_vertical_align="top",
                            gap=PublisherDocumentAreaStyleGap(None),
                        ),
                    ),
                    description="description_example",
                    id="brand-review",
                    tags=[
                        "["brand"]",
                    ],
                    title="title_example",
                    version="2",
                ),
            ],
            documents=[
                DeclarativePublisherDocument(
                    content=PublisherDocumentContent(
                        attribute_filter_configs=[
                            PublisherDocumentAttributeFilterConfig(
                                display_as_label=PublisherDocumentObjRef(
                                    identifier="identifier_example",
                                    type="type_example",
                                ),
                                local_identifier="26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1",
                                mode="readonly",
                                selection_type="list",
                            ),
                        ],
                        defaults=PublisherDocumentDefaults(
                            page_size="widescreen",
                            period=PublisherDocumentPeriod(),
                            takeaway=PublisherDocumentTakeawayDefaults(
                                generation=PublisherDocumentTakeawayGeneration(
                                    context=PublisherDocumentTakeawayContext(
                                        filters=True,
                                        other_pages=True,
                                        page_title=True,
                                        widgets=[
                                            "26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1",
                                        ],
                                    ),
                                    instructions="instructions_example",
                                ),
                            ),
                        ),
                        filters=[
                            PublisherDocumentFilter(),
                        ],
                        format_locale="format_locale_example",
                        locale="locale_example",
                        pages=[
                            PublisherDocumentPage(
                                filters=[
                                    PublisherDocumentFilter(),
                                ],
                                id="26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1",
                                kind="cover",
                                layout=PublisherDocumentLayoutNode(),
                                notes="notes_example",
                                page_size="widescreen",
                                style=PublisherDocumentPageStyle(
                                    background_color="background_color_example",
                                    background_fit="cover",
                                    background_horizontal_align="left",
                                    background_image="background_image_example",
                                    background_image_opacity=0,
                                    background_offset=0,
                                    background_offset_bottom=0,
                                    background_offset_left=0,
                                    background_offset_right=0,
                                    background_offset_top=0,
                                    background_opacity=0,
                                    background_vertical_align="top",
                                    font_size=0,
                                    font_style="normal",
                                    font_weight=1,
                                    gap=PublisherDocumentAreaStyleGap(None),
                                    horizontal_align="left",
                                    letter_spacing=3.14,
                                    line_height=3.14,
                                    padding=PublisherDocumentContainerStylePadding(None),
                                    padding_bottom=PublisherDocumentContainerStylePadding(None),
                                    padding_left=PublisherDocumentContainerStylePadding(None),
                                    padding_right=PublisherDocumentContainerStylePadding(None),
                                    padding_top=PublisherDocumentContainerStylePadding(None),
                                    text_color="text_color_example",
                                    text_overflow="shrink",
                                    text_style="title",
                                    text_transform="none",
                                    vertical_align="top",
                                ),
                                visible=True,
                            ),
                        ],
                        sections=[
                            PublisherDocumentSection(
                                description="description_example",
                                id="26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1",
                                pages=[
                                    PublisherDocumentPage(
                                        filters=[
                                            PublisherDocumentFilter(),
                                        ],
                                        id="26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1",
                                        kind="cover",
                                        layout=PublisherDocumentLayoutNode(),
                                        notes="notes_example",
                                        page_size="widescreen",
                                        style=PublisherDocumentPageStyle(
                                            background_color="background_color_example",
                                            background_fit="cover",
                                            background_horizontal_align="left",
                                            background_image="background_image_example",
                                            background_image_opacity=0,
                                            background_offset=0,
                                            background_offset_bottom=0,
                                            background_offset_left=0,
                                            background_offset_right=0,
                                            background_offset_top=0,
                                            background_opacity=0,
                                            background_vertical_align="top",
                                            font_size=0,
                                            font_style="normal",
                                            font_weight=1,
                                            gap=PublisherDocumentAreaStyleGap(None),
                                            horizontal_align="left",
                                            letter_spacing=3.14,
                                            line_height=3.14,
                                            padding=PublisherDocumentContainerStylePadding(None),
                                            padding_bottom=PublisherDocumentContainerStylePadding(None),
                                            padding_left=PublisherDocumentContainerStylePadding(None),
                                            padding_right=PublisherDocumentContainerStylePadding(None),
                                            padding_top=PublisherDocumentContainerStylePadding(None),
                                            text_color="text_color_example",
                                            text_overflow="shrink",
                                            text_style="title",
                                            text_transform="none",
                                            vertical_align="top",
                                        ),
                                        visible=True,
                                    ),
                                ],
                                title="title_example",
                            ),
                        ],
                        style=PublisherDocumentAreaStyle(
                            background_color="background_color_example",
                            background_fit="cover",
                            background_horizontal_align="left",
                            background_image="background_image_example",
                            background_image_opacity=0,
                            background_offset=0,
                            background_offset_bottom=0,
                            background_offset_left=0,
                            background_offset_right=0,
                            background_offset_top=0,
                            background_opacity=0,
                            background_vertical_align="top",
                            gap=PublisherDocumentAreaStyleGap(None),
                        ),
                    ),
                    description="description_example",
                    id="levis-h1-2026",
                    period=PublisherDocumentPeriod(),
                    tags=[
                        "["brand"]",
                    ],
                    title="title_example",
                    version="2",
                ),
            ],
            export_definitions=[
                DeclarativeExportDefinition(
                    created_at="2023-07-20 12:30",
                    created_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    description="Simple number for total goods in current production.",
                    id="export-definition-1",
                    modified_at="2023-07-20 12:30",
                    modified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    request_payload=ExportRequest(),
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
            memory_items=[
                DeclarativeMemoryItem(
                    created_at="2023-07-20 12:30",
                    created_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    description="Context about sales data for AI assistant.",
                    id="sales-context",
                    instruction="When discussing sales, always consider quarterly trends.",
                    is_disabled=False,
                    keywords=[
                        "keywords_example",
                    ],
                    modified_at="2023-07-20 12:30",
                    modified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    strategy="AUTO",
                    tags=["AI","Context"],
                    title="Sales Context",
                ),
            ],
            metrics=[
                DeclarativeMetric(
                    certification="CERTIFIED",
                    certification_message="certification_message_example",
                    certified_at="0480-72-88 80:01",
                    certified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    conditional_formatting=ObjectConditionalFormatting(
                        conditions=[
                            ConditionalFormattingCondition(
                                format=ConditionalFormattingFormat(
                                    background_color="#3DB36B",
                                    color="#E54D40",
                                    scope="cell",
                                ),
                                id="d0538854-aac3-4fc6-9603-61f49bab6aa3",
                                operator="ALL",
                                value=ConditionalFormattingValue(),
                            ),
                        ],
                        enabled=True,
                    ),
                    content=JsonNode(),
                    created_at="2023-07-20 12:30",
                    created_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    description="Sales for all the data available.",
                    id="total-sales",
                    is_hidden=False,
                    is_hidden_from_kda=False,
                    modified_at="2023-07-20 12:30",
                    modified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    permissions=[
                        DeclarativeMetricPermissionsInner(None),
                    ],
                    tags=["Revenues"],
                    title="Total sales",
                ),
            ],
            page_templates=[
                DeclarativePublisherDocumentPageTemplate(
                    content=PublisherDocumentPageTemplateContent(
                        filters=[
                            PublisherDocumentFilter(),
                        ],
                        kind="cover",
                        layout=PublisherDocumentLayoutNode(),
                        notes="notes_example",
                        page_size="widescreen",
                        style=PublisherDocumentPageStyle(
                            background_color="background_color_example",
                            background_fit="cover",
                            background_horizontal_align="left",
                            background_image="background_image_example",
                            background_image_opacity=0,
                            background_offset=0,
                            background_offset_bottom=0,
                            background_offset_left=0,
                            background_offset_right=0,
                            background_offset_top=0,
                            background_opacity=0,
                            background_vertical_align="top",
                            font_size=0,
                            font_style="normal",
                            font_weight=1,
                            gap=PublisherDocumentAreaStyleGap(None),
                            horizontal_align="left",
                            letter_spacing=3.14,
                            line_height=3.14,
                            padding=PublisherDocumentContainerStylePadding(None),
                            padding_bottom=PublisherDocumentContainerStylePadding(None),
                            padding_left=PublisherDocumentContainerStylePadding(None),
                            padding_right=PublisherDocumentContainerStylePadding(None),
                            padding_top=PublisherDocumentContainerStylePadding(None),
                            text_color="text_color_example",
                            text_overflow="shrink",
                            text_style="title",
                            text_transform="none",
                            vertical_align="top",
                        ),
                    ),
                    description="description_example",
                    id="brand-cover",
                    tags=[
                        "["brand"]",
                    ],
                    title="title_example",
                    version="2",
                ),
            ],
            parameters=[
                DeclarativeParameter(
                    content=ParameterDefinition(),
                    created_at="2023-07-20 12:30",
                    created_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    description="Rate applied to discounted items.",
                    id="discount-rate",
                    modified_at="2023-07-20 12:30",
                    modified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    tags=["Finance"],
                    title="Discount Rate",
                ),
            ],
            report_page_layouts=[
                DeclarativeReportPageLayout(
                    content=JsonNode(),
                    description="description_example",
                    id="brand-cover",
                    tags=[
                        "["brand"]",
                    ],
                    title="title_example",
                ),
            ],
            report_templates=[
                DeclarativeReportTemplate(
                    content=JsonNode(),
                    description="description_example",
                    id="quarterly-review-template",
                    tags=[
                        "["brand"]",
                    ],
                    title="title_example",
                ),
            ],
            reports=[
                DeclarativeReport(
                    content=JsonNode(),
                    description="description_example",
                    id="quarterly-review-2026-h1",
                    period_end=dateutil_parser('Tue Jun 30 00:00:00 UTC 2026').date(),
                    period_start=dateutil_parser('Thu Jan 01 00:00:00 UTC 2026').date(),
                    tags=[
                        "["brand"]",
                    ],
                    title="title_example",
                    variable_values={
                        "key": "key_example",
                    },
                ),
            ],
            visualization_objects=[
                DeclarativeVisualizationObject(
                    certification="CERTIFIED",
                    certification_message="certification_message_example",
                    certified_at="0480-72-88 80:01",
                    certified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    conditional_formatting=ConditionalFormatting(
                        enabled=True,
                        rules=[
                            ConditionalFormattingRule(
                                conditions=[
                                    ConditionalFormattingCondition(
                                        format=ConditionalFormattingFormat(
                                            background_color="#3DB36B",
                                            color="#E54D40",
                                            scope="cell",
                                        ),
                                        id="d0538854-aac3-4fc6-9603-61f49bab6aa3",
                                        operator="ALL",
                                        value=ConditionalFormattingValue(),
                                    ),
                                ],
                                id="bb955b38-a9e6-45f5-b068-155cb7ce509a",
                                target=ConditionalFormattingTarget(),
                            ),
                        ],
                    ),
                    content=JsonNode(),
                    created_at="2023-07-20 12:30",
                    created_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    description="Simple number for total goods in current production.",
                    id="visualization-1",
                    is_hidden=False,
                    modified_at="2023-07-20 12:30",
                    modified_by=DeclarativeUserIdentifier(
                        id="employee123",
                        type="user",
                    ),
                    permissions=[
                        DeclarativeVisualizationObjectPermissionsInner(None),
                    ],
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


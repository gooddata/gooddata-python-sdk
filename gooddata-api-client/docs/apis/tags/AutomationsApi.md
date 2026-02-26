<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.automations_api.AutomationsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_automations**](#create_entity_automations) | **post** /api/v1/entities/workspaces/{workspaceId}/automations | Post Automations
[**delete_entity_automations**](#delete_entity_automations) | **delete** /api/v1/entities/workspaces/{workspaceId}/automations/{objectId} | Delete an Automation
[**delete_organization_automations**](#delete_organization_automations) | **post** /api/v1/actions/organization/automations/delete | Delete selected automations across all workspaces
[**delete_workspace_automations**](#delete_workspace_automations) | **post** /api/v1/actions/workspaces/{workspaceId}/automations/delete | Delete selected automations in the workspace
[**get_all_automations_workspace_automations**](#get_all_automations_workspace_automations) | **get** /api/v1/entities/organization/workspaceAutomations | Get all Automations across all Workspaces
[**get_all_entities_automations**](#get_all_entities_automations) | **get** /api/v1/entities/workspaces/{workspaceId}/automations | Get all Automations
[**get_automations**](#get_automations) | **get** /api/v1/layout/workspaces/{workspaceId}/automations | Get automations
[**get_entity_automations**](#get_entity_automations) | **get** /api/v1/entities/workspaces/{workspaceId}/automations/{objectId} | Get an Automation
[**patch_entity_automations**](#patch_entity_automations) | **patch** /api/v1/entities/workspaces/{workspaceId}/automations/{objectId} | Patch an Automation
[**pause_organization_automations**](#pause_organization_automations) | **post** /api/v1/actions/organization/automations/pause | Pause selected automations across all workspaces
[**pause_workspace_automations**](#pause_workspace_automations) | **post** /api/v1/actions/workspaces/{workspaceId}/automations/pause | Pause selected automations in the workspace
[**search_entities_automation_results**](#search_entities_automation_results) | **post** /api/v1/entities/workspaces/{workspaceId}/automationResults/search | Search request for AutomationResult
[**search_entities_automations**](#search_entities_automations) | **post** /api/v1/entities/workspaces/{workspaceId}/automations/search | Search request for Automation
[**set_automations**](#set_automations) | **put** /api/v1/layout/workspaces/{workspaceId}/automations | Set automations
[**trigger_automation**](#trigger_automation) | **post** /api/v1/actions/workspaces/{workspaceId}/automations/trigger | Trigger automation.
[**trigger_existing_automation**](#trigger_existing_automation) | **post** /api/v1/actions/workspaces/{workspaceId}/automations/{automationId}/trigger | Trigger existing automation.
[**unpause_organization_automations**](#unpause_organization_automations) | **post** /api/v1/actions/organization/automations/unpause | Unpause selected automations across all workspaces
[**unpause_workspace_automations**](#unpause_workspace_automations) | **post** /api/v1/actions/workspaces/{workspaceId}/automations/unpause | Unpause selected automations in the workspace
[**unsubscribe_all_automations**](#unsubscribe_all_automations) | **delete** /api/v1/actions/organization/automations/unsubscribe | Unsubscribe from all automations in all workspaces
[**unsubscribe_automation**](#unsubscribe_automation) | **delete** /api/v1/actions/workspaces/{workspaceId}/automations/{automationId}/unsubscribe | Unsubscribe from an automation
[**unsubscribe_organization_automations**](#unsubscribe_organization_automations) | **post** /api/v1/actions/organization/automations/unsubscribe | Unsubscribe from selected automations across all workspaces
[**unsubscribe_selected_workspace_automations**](#unsubscribe_selected_workspace_automations) | **post** /api/v1/actions/workspaces/{workspaceId}/automations/unsubscribe | Unsubscribe from selected automations in the workspace
[**unsubscribe_workspace_automations**](#unsubscribe_workspace_automations) | **delete** /api/v1/actions/workspaces/{workspaceId}/automations/unsubscribe | Unsubscribe from all automations in the workspace
[**update_entity_automations**](#update_entity_automations) | **put** /api/v1/entities/workspaces/{workspaceId}/automations/{objectId} | Put an Automation

# **create_entity_automations**
<a id="create_entity_automations"></a>
> JsonApiAutomationOutDocument create_entity_automations(workspace_idjson_api_automation_in_document)

Post Automations

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import automations_api
from gooddata_api_client.model.json_api_automation_in_document import JsonApiAutomationInDocument
from gooddata_api_client.model.json_api_automation_out_document import JsonApiAutomationOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
    }
    body = JsonApiAutomationInDocument(
        data=JsonApiAutomationIn(
            attributes=dict(
                alert=dict(
                    condition=AlertCondition(),
                    execution=AlertAfm(
                        attributes=[
                            AttributeItem(
                                label=AfmObjectIdentifierLabel(
                                    identifier=dict(
                                        id="sample_item.price",
                                        type="label",
                                    ),
                                ),
                                local_identifier="attribute_1",
                                show_all_values=False,
                            )
                        ],
                        aux_measures=[
                            MeasureItem(
                                definition=MeasureDefinition(),
                                local_identifier="metric_1",
                            )
                        ],
                        filters=[
                            FilterDefinition()
                        ],
                        measures=[
                            MeasureItem()
                        ],
                    ),
                    interval="DAY",
                    trigger="ALWAYS",
                ),
                are_relations_valid=True,
                dashboard_tabular_exports=[
                    dict(
                        request_payload=DashboardTabularExportRequestV2(
                            dashboard_filters_override=[
                                DashboardFilter()
                            ],
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            dashboard_tabs_filters_overrides=dict(
                                "key": [
                                    DashboardFilter()
                                ],
                            ),
                            file_name="result",
                            format="XLSX",
                            settings=DashboardExportSettings(
                                export_info=True,
                                merge_headers=True,
                                page_orientation="PORTRAIT",
                                page_size="A4",
                            ),
                            widget_ids=[
                                "widget_ids_example"
                            ],
                        ),
                    )
                ],
                description="description_example",
                details=dict(),
                evaluation_mode="SHARED",
                external_recipients=[
                    dict(
                        email="email_example",
                    )
                ],
                image_exports=[
                    dict(
                        request_payload=ImageExportRequest(
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            file_name="filename",
                            format="PNG",
                            metadata=JsonNode(),
                            widget_ids=[
                                "widget_ids_example"
                            ],
                        ),
                    )
                ],
                metadata=dict(
                    visible_filters=[
                        VisibleFilter(
                            is_all_time_date_filter=False,
                            local_identifier="local_identifier_example",
                            title="title_example",
                        )
                    ],
                    widget="widget_example",
                ),
                raw_exports=[
                    dict(
                        request_payload=RawExportAutomationRequest(
                            custom_override=RawCustomOverride(
                                labels=dict(
                                    "key": RawCustomLabel(
                                        title="title_example",
                                    ),
                                ),
                                metrics=dict(
                                    "key": RawCustomMetric(
                                        title="title_example",
                                    ),
                                ),
                            ),
                            delimiter="U",
                            execution=AFM(
                                attributes=[
                                    AttributeItem()
                                ],
,
                                filters=[
                                    FilterDefinition()
                                ],
                                measure_definition_overrides=[
                                    MetricDefinitionOverride(
                                        definition=InlineMeasureDefinition(
                                            inline=dict(
                                                maql="maql_example",
                                            ),
                                        ),
                                        item=AfmObjectIdentifierCore(
                                            identifier=dict(
                                                id="sample_item.price",
                                                type="attribute",
                                            ),
                                        ),
                                    )
                                ],
                                measures=[
                                    MeasureItem()
                                ],
                            ),
                            execution_settings=ExecutionSettings(
                                data_sampling_percentage=0,
                                timestamp="1970-01-01T00:00:00.00Z",
                            ),
                            file_name="result",
                            format="CSV",
                            metadata=JsonNode(),
                        ),
                    )
                ],
                schedule=dict(
                    cron="0 */30 9-17 ? * MON-FRI",
                    cron_description="cron_description_example",
                    first_run="2025-01-01T12:00Z",
                    timezone="Europe/Prague",
                ),
                slides_exports=[
                    dict(
                        request_payload=SlidesExportRequest(
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            file_name="filename",
                            format="PDF",
                            metadata=JsonNode(),
                            template_id="template_id_example",
                            visualization_ids=[
                                "visualization_ids_example"
                            ],
                            widget_ids=[
                                "widget_ids_example"
                            ],
                        ),
                    )
                ],
                state="ACTIVE",
                tabular_exports=[
                    dict(
                        request_payload=TabularExportRequest(
                            custom_override=CustomOverride(
                                labels=dict(
                                    "key": CustomLabel(),
                                ),
                                metrics=dict(
                                    "key": CustomMetric(
                                        format="format_example",
                                        title="title_example",
                                    ),
                                ),
                            ),
                            execution_result="ff483727196c9dc862c7fd3a5a84df55c96d61a4",
                            file_name="result",
                            format="CSV",
                            metadata=JsonNode(),
                            related_dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            settings=Settings(
                                delimiter="U",
                                export_info=True,
                                merge_headers=True,
                                page_orientation="PORTRAIT",
                                page_size="A4",
                                pdf_page_size="a4 landscape",
                                pdf_table_style=[{"properties":[{"key":"font-size","value":"30px"}],"selector":"th"}],
                                pdf_top_left_content="Good",
                                pdf_top_right_content="Morning",
                                show_filters=False,
                            ),
                            visualization_object="f7c359bc-c230-4487-b15b-ad9685bcb537",
                            visualization_object_custom_filters=[
                                dict()
                            ],
                        ),
                    )
                ],
                tags=[
                    "tags_example"
                ],
                title="title_example",
                visual_exports=[
                    dict(
                        request_payload=VisualExportRequest(
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            file_name="filename",
                            metadata=dict(),
                        ),
                    )
                ],
            ),
            id="id1",
            relationships=dict(
                analytical_dashboard=dict(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                export_definitions=dict(
                    data=JsonApiExportDefinitionToManyLinkage([
                        JsonApiExportDefinitionLinkage(
                            id="id_example",
                            type="exportDefinition",
                        )
                    ]),
                ),
                notification_channel=dict(
                    data=JsonApiNotificationChannelToOneLinkage(None),
                ),
                recipients=dict(
                    data=JsonApiUserToManyLinkage([
                        JsonApiUserLinkage(
                            id="id_example",
                            type="user",
                        )
                    ]),
                ),
            ),
            type="automation",
        ),
    )
    try:
        # Post Automations
        api_response = api_instance.create_entity_automations(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->create_entity_automations: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
        'include': [
        "notificationChannel,analyticalDashboard,createdBy,modifiedBy,exportDefinitions,recipients,automationResults"
    ],
        'metaInclude': [
        "metaInclude=origin,all"
    ],
    }
    body = JsonApiAutomationInDocument(
        data=JsonApiAutomationIn(
            attributes=dict(
                alert=dict(
                    condition=AlertCondition(),
                    execution=AlertAfm(
                        attributes=[
                            AttributeItem(
                                label=AfmObjectIdentifierLabel(
                                    identifier=dict(
                                        id="sample_item.price",
                                        type="label",
                                    ),
                                ),
                                local_identifier="attribute_1",
                                show_all_values=False,
                            )
                        ],
                        aux_measures=[
                            MeasureItem(
                                definition=MeasureDefinition(),
                                local_identifier="metric_1",
                            )
                        ],
                        filters=[
                            FilterDefinition()
                        ],
                        measures=[
                            MeasureItem()
                        ],
                    ),
                    interval="DAY",
                    trigger="ALWAYS",
                ),
                are_relations_valid=True,
                dashboard_tabular_exports=[
                    dict(
                        request_payload=DashboardTabularExportRequestV2(
                            dashboard_filters_override=[
                                DashboardFilter()
                            ],
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            dashboard_tabs_filters_overrides=dict(
                                "key": [
                                    DashboardFilter()
                                ],
                            ),
                            file_name="result",
                            format="XLSX",
                            settings=DashboardExportSettings(
                                export_info=True,
                                merge_headers=True,
                                page_orientation="PORTRAIT",
                                page_size="A4",
                            ),
                            widget_ids=[
                                "widget_ids_example"
                            ],
                        ),
                    )
                ],
                description="description_example",
                details=dict(),
                evaluation_mode="SHARED",
                external_recipients=[
                    dict(
                        email="email_example",
                    )
                ],
                image_exports=[
                    dict(
                        request_payload=ImageExportRequest(
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            file_name="filename",
                            format="PNG",
                            metadata=JsonNode(),
                            widget_ids=[
                                "widget_ids_example"
                            ],
                        ),
                    )
                ],
                metadata=dict(
                    visible_filters=[
                        VisibleFilter(
                            is_all_time_date_filter=False,
                            local_identifier="local_identifier_example",
                            title="title_example",
                        )
                    ],
                    widget="widget_example",
                ),
                raw_exports=[
                    dict(
                        request_payload=RawExportAutomationRequest(
                            custom_override=RawCustomOverride(
                                labels=dict(
                                    "key": RawCustomLabel(
                                        title="title_example",
                                    ),
                                ),
                                metrics=dict(
                                    "key": RawCustomMetric(
                                        title="title_example",
                                    ),
                                ),
                            ),
                            delimiter="U",
                            execution=AFM(
                                attributes=[
                                    AttributeItem()
                                ],
,
                                filters=[
                                    FilterDefinition()
                                ],
                                measure_definition_overrides=[
                                    MetricDefinitionOverride(
                                        definition=InlineMeasureDefinition(
                                            inline=dict(
                                                maql="maql_example",
                                            ),
                                        ),
                                        item=AfmObjectIdentifierCore(
                                            identifier=dict(
                                                id="sample_item.price",
                                                type="attribute",
                                            ),
                                        ),
                                    )
                                ],
                                measures=[
                                    MeasureItem()
                                ],
                            ),
                            execution_settings=ExecutionSettings(
                                data_sampling_percentage=0,
                                timestamp="1970-01-01T00:00:00.00Z",
                            ),
                            file_name="result",
                            format="CSV",
                            metadata=JsonNode(),
                        ),
                    )
                ],
                schedule=dict(
                    cron="0 */30 9-17 ? * MON-FRI",
                    cron_description="cron_description_example",
                    first_run="2025-01-01T12:00Z",
                    timezone="Europe/Prague",
                ),
                slides_exports=[
                    dict(
                        request_payload=SlidesExportRequest(
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            file_name="filename",
                            format="PDF",
                            metadata=JsonNode(),
                            template_id="template_id_example",
                            visualization_ids=[
                                "visualization_ids_example"
                            ],
                            widget_ids=[
                                "widget_ids_example"
                            ],
                        ),
                    )
                ],
                state="ACTIVE",
                tabular_exports=[
                    dict(
                        request_payload=TabularExportRequest(
                            custom_override=CustomOverride(
                                labels=dict(
                                    "key": CustomLabel(),
                                ),
                                metrics=dict(
                                    "key": CustomMetric(
                                        format="format_example",
                                        title="title_example",
                                    ),
                                ),
                            ),
                            execution_result="ff483727196c9dc862c7fd3a5a84df55c96d61a4",
                            file_name="result",
                            format="CSV",
                            metadata=JsonNode(),
                            related_dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            settings=Settings(
                                delimiter="U",
                                export_info=True,
                                merge_headers=True,
                                page_orientation="PORTRAIT",
                                page_size="A4",
                                pdf_page_size="a4 landscape",
                                pdf_table_style=[{"properties":[{"key":"font-size","value":"30px"}],"selector":"th"}],
                                pdf_top_left_content="Good",
                                pdf_top_right_content="Morning",
                                show_filters=False,
                            ),
                            visualization_object="f7c359bc-c230-4487-b15b-ad9685bcb537",
                            visualization_object_custom_filters=[
                                dict()
                            ],
                        ),
                    )
                ],
                tags=[
                    "tags_example"
                ],
                title="title_example",
                visual_exports=[
                    dict(
                        request_payload=VisualExportRequest(
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            file_name="filename",
                            metadata=dict(),
                        ),
                    )
                ],
            ),
            id="id1",
            relationships=dict(
                analytical_dashboard=dict(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                export_definitions=dict(
                    data=JsonApiExportDefinitionToManyLinkage([
                        JsonApiExportDefinitionLinkage(
                            id="id_example",
                            type="exportDefinition",
                        )
                    ]),
                ),
                notification_channel=dict(
                    data=JsonApiNotificationChannelToOneLinkage(None),
                ),
                recipients=dict(
                    data=JsonApiUserToManyLinkage([
                        JsonApiUserLinkage(
                            id="id_example",
                            type="user",
                        )
                    ]),
                ),
            ),
            type="automation",
        ),
    )
    try:
        # Post Automations
        api_response = api_instance.create_entity_automations(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->create_entity_automations: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAutomationInDocument**](../../models/JsonApiAutomationInDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAutomationInDocument**](../../models/JsonApiAutomationInDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
include | IncludeSchema | | optional
metaInclude | MetaIncludeSchema | | optional


# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["notificationChannels", "analyticalDashboards", "userIdentifiers", "exportDefinitions", "users", "automationResults", "notificationChannel", "analyticalDashboard", "createdBy", "modifiedBy", "recipients", "ALL", ] 

# MetaIncludeSchema

Included meta objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Included meta objects | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["origin", "all", "ALL", ] 

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
201 | [ApiResponseFor201](#create_entity_automations.ApiResponseFor201) | Request successfully processed

#### create_entity_automations.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationJson, SchemaFor201ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAutomationOutDocument**](../../models/JsonApiAutomationOutDocument.md) |  | 


# SchemaFor201ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAutomationOutDocument**](../../models/JsonApiAutomationOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_entity_automations**
<a id="delete_entity_automations"></a>
> delete_entity_automations(workspace_idobject_id)

Delete an Automation

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import automations_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
    }
    try:
        # Delete an Automation
        api_response = api_instance.delete_entity_automations(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->delete_entity_automations: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
        'filter': "title==someString;description==someString;notificationChannel.id==321;analyticalDashboard.id==321",
    }
    try:
        # Delete an Automation
        api_response = api_instance.delete_entity_automations(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->delete_entity_automations: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 
objectId | ObjectIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# ObjectIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#delete_entity_automations.ApiResponseFor204) | Successfully deleted

#### delete_entity_automations.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_organization_automations**
<a id="delete_organization_automations"></a>
> delete_organization_automations(organization_automation_management_bulk_request)

Delete selected automations across all workspaces

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import automations_api
from gooddata_api_client.model.organization_automation_management_bulk_request import OrganizationAutomationManagementBulkRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)

    # example passing only required values which don't have defaults set
    body = OrganizationAutomationManagementBulkRequest(
        automations=[
            OrganizationAutomationIdentifier(
                id="id_example",
                workspace_id="workspace_id_example",
            )
        ],
    )
    try:
        # Delete selected automations across all workspaces
        api_response = api_instance.delete_organization_automations(
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->delete_organization_automations: %s\n" % e)
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
[**OrganizationAutomationManagementBulkRequest**](../../models/OrganizationAutomationManagementBulkRequest.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#delete_organization_automations.ApiResponseFor204) | No Content

#### delete_organization_automations.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_workspace_automations**
<a id="delete_workspace_automations"></a>
> delete_workspace_automations(workspace_idworkspace_automation_management_bulk_request)

Delete selected automations in the workspace

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import automations_api
from gooddata_api_client.model.workspace_automation_management_bulk_request import WorkspaceAutomationManagementBulkRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    body = WorkspaceAutomationManagementBulkRequest(
        automations=[
            WorkspaceAutomationIdentifier(
                id="id_example",
            )
        ],
    )
    try:
        # Delete selected automations in the workspace
        api_response = api_instance.delete_workspace_automations(
            path_params=path_params,
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->delete_workspace_automations: %s\n" % e)
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
[**WorkspaceAutomationManagementBulkRequest**](../../models/WorkspaceAutomationManagementBulkRequest.md) |  | 


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
204 | [ApiResponseFor204](#delete_workspace_automations.ApiResponseFor204) | No Content

#### delete_workspace_automations.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_automations_workspace_automations**
<a id="get_all_automations_workspace_automations"></a>
> JsonApiWorkspaceAutomationOutList get_all_automations_workspace_automations()

Get all Automations across all Workspaces

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import automations_api
from gooddata_api_client.model.json_api_workspace_automation_out_list import JsonApiWorkspaceAutomationOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)

    # example passing only optional values
    query_params = {
        'filter': "title==someString;description==someString;workspace.id==321;notificationChannel.id==321",
        'include': [
        "workspace,notificationChannel,analyticalDashboard,createdBy,modifiedBy,exportDefinitions,recipients,automationResults"
    ],
        'page': 0,
        'size': 20,
        'sort': [
        "sort_example"
    ],
        'metaInclude': [
        "metaInclude=page,all"
    ],
    }
    try:
        # Get all Automations across all Workspaces
        api_response = api_instance.get_all_automations_workspace_automations(
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->get_all_automations_workspace_automations: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
include | IncludeSchema | | optional
page | PageSchema | | optional
size | SizeSchema | | optional
sort | SortSchema | | optional
metaInclude | MetaIncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["workspaces", "notificationChannels", "analyticalDashboards", "userIdentifiers", "exportDefinitions", "users", "automationResults", "workspace", "notificationChannel", "analyticalDashboard", "createdBy", "modifiedBy", "recipients", "ALL", ] 

# PageSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 0

# SizeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 20

# SortSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

# MetaIncludeSchema

Included meta objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Included meta objects | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["page", "all", "ALL", ] 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_all_automations_workspace_automations.ApiResponseFor200) | Request successfully processed

#### get_all_automations_workspace_automations.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiWorkspaceAutomationOutList**](../../models/JsonApiWorkspaceAutomationOutList.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiWorkspaceAutomationOutList**](../../models/JsonApiWorkspaceAutomationOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_automations**
<a id="get_all_entities_automations"></a>
> JsonApiAutomationOutList get_all_entities_automations(workspace_id)

Get all Automations

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import automations_api
from gooddata_api_client.model.json_api_automation_out_list import JsonApiAutomationOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
    }
    header_params = {
    }
    try:
        # Get all Automations
        api_response = api_instance.get_all_entities_automations(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->get_all_entities_automations: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
        'origin': "ALL",
        'filter': "title==someString;description==someString;notificationChannel.id==321;analyticalDashboard.id==321",
        'include': [
        "notificationChannel,analyticalDashboard,createdBy,modifiedBy,exportDefinitions,recipients,automationResults"
    ],
        'page': 0,
        'size': 20,
        'sort': [
        "sort_example"
    ],
        'metaInclude': [
        "metaInclude=origin,page,all"
    ],
    }
    header_params = {
        'X-GDC-VALIDATE-RELATIONS': False,
    }
    try:
        # Get all Automations
        api_response = api_instance.get_all_entities_automations(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->get_all_entities_automations: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
header_params | RequestHeaderParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
origin | OriginSchema | | optional
filter | FilterSchema | | optional
include | IncludeSchema | | optional
page | PageSchema | | optional
size | SizeSchema | | optional
sort | SortSchema | | optional
metaInclude | MetaIncludeSchema | | optional


# OriginSchema

Defines scope of origin of objects. All by default.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Defines scope of origin of objects. All by default. | must be one of ["ALL", "PARENTS", "NATIVE", ] if omitted the server will use the default value of "ALL"

# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["notificationChannels", "analyticalDashboards", "userIdentifiers", "exportDefinitions", "users", "automationResults", "notificationChannel", "analyticalDashboard", "createdBy", "modifiedBy", "recipients", "ALL", ] 

# PageSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 0

# SizeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 20

# SortSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

# MetaIncludeSchema

Included meta objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Included meta objects | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["origin", "page", "all", "ALL", ] 

### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
X-GDC-VALIDATE-RELATIONS | XGDCVALIDATERELATIONSSchema | | optional

# XGDCVALIDATERELATIONSSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bool,  | BoolClass,  |  | if omitted the server will use the default value of False

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
200 | [ApiResponseFor200](#get_all_entities_automations.ApiResponseFor200) | Request successfully processed

#### get_all_entities_automations.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAutomationOutList**](../../models/JsonApiAutomationOutList.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAutomationOutList**](../../models/JsonApiAutomationOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_automations**
<a id="get_automations"></a>
> [DeclarativeAutomation] get_automations(workspace_id)

Get automations

Retrieve automations for the specific workspace

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import automations_api
from gooddata_api_client.model.declarative_automation import DeclarativeAutomation
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
    }
    try:
        # Get automations
        api_response = api_instance.get_automations(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->get_automations: %s\n" % e)

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
        # Get automations
        api_response = api_instance.get_automations(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->get_automations: %s\n" % e)
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
200 | [ApiResponseFor200](#get_automations.ApiResponseFor200) | Retrieved automations.

#### get_automations.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeAutomation**]({{complexTypePrefix}}DeclarativeAutomation.md) | [**DeclarativeAutomation**]({{complexTypePrefix}}DeclarativeAutomation.md) | [**DeclarativeAutomation**]({{complexTypePrefix}}DeclarativeAutomation.md) |  | 

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_automations**
<a id="get_entity_automations"></a>
> JsonApiAutomationOutDocument get_entity_automations(workspace_idobject_id)

Get an Automation

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import automations_api
from gooddata_api_client.model.json_api_automation_out_document import JsonApiAutomationOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
    }
    header_params = {
    }
    try:
        # Get an Automation
        api_response = api_instance.get_entity_automations(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->get_entity_automations: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
        'filter': "title==someString;description==someString;notificationChannel.id==321;analyticalDashboard.id==321",
        'include': [
        "notificationChannel,analyticalDashboard,createdBy,modifiedBy,exportDefinitions,recipients,automationResults"
    ],
        'metaInclude': [
        "metaInclude=origin,all"
    ],
    }
    header_params = {
        'X-GDC-VALIDATE-RELATIONS': False,
    }
    try:
        # Get an Automation
        api_response = api_instance.get_entity_automations(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->get_entity_automations: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
header_params | RequestHeaderParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
include | IncludeSchema | | optional
metaInclude | MetaIncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["notificationChannels", "analyticalDashboards", "userIdentifiers", "exportDefinitions", "users", "automationResults", "notificationChannel", "analyticalDashboard", "createdBy", "modifiedBy", "recipients", "ALL", ] 

# MetaIncludeSchema

Included meta objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Included meta objects | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["origin", "all", "ALL", ] 

### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
X-GDC-VALIDATE-RELATIONS | XGDCVALIDATERELATIONSSchema | | optional

# XGDCVALIDATERELATIONSSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bool,  | BoolClass,  |  | if omitted the server will use the default value of False

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 
objectId | ObjectIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# ObjectIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_entity_automations.ApiResponseFor200) | Request successfully processed

#### get_entity_automations.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAutomationOutDocument**](../../models/JsonApiAutomationOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAutomationOutDocument**](../../models/JsonApiAutomationOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **patch_entity_automations**
<a id="patch_entity_automations"></a>
> JsonApiAutomationOutDocument patch_entity_automations(workspace_idobject_idjson_api_automation_patch_document)

Patch an Automation

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import automations_api
from gooddata_api_client.model.json_api_automation_out_document import JsonApiAutomationOutDocument
from gooddata_api_client.model.json_api_automation_patch_document import JsonApiAutomationPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
    }
    body = JsonApiAutomationPatchDocument(
        data=JsonApiAutomationPatch(
            attributes=dict(
                alert=dict(
                    condition=AlertCondition(),
                    execution=AlertAfm(
                        attributes=[
                            AttributeItem(
                                label=AfmObjectIdentifierLabel(
                                    identifier=dict(
                                        id="sample_item.price",
                                        type="label",
                                    ),
                                ),
                                local_identifier="attribute_1",
                                show_all_values=False,
                            )
                        ],
                        aux_measures=[
                            MeasureItem(
                                definition=MeasureDefinition(),
                                local_identifier="metric_1",
                            )
                        ],
                        filters=[
                            FilterDefinition()
                        ],
                        measures=[
                            MeasureItem()
                        ],
                    ),
                    interval="DAY",
                    trigger="ALWAYS",
                ),
                are_relations_valid=True,
                dashboard_tabular_exports=[
                    dict(
                        request_payload=DashboardTabularExportRequestV2(
                            dashboard_filters_override=[
                                DashboardFilter()
                            ],
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            dashboard_tabs_filters_overrides=dict(
                                "key": [
                                    DashboardFilter()
                                ],
                            ),
                            file_name="result",
                            format="XLSX",
                            settings=DashboardExportSettings(
                                export_info=True,
                                merge_headers=True,
                                page_orientation="PORTRAIT",
                                page_size="A4",
                            ),
                            widget_ids=[
                                "widget_ids_example"
                            ],
                        ),
                    )
                ],
                description="description_example",
                details=dict(),
                evaluation_mode="SHARED",
                external_recipients=[
                    dict(
                        email="email_example",
                    )
                ],
                image_exports=[
                    dict(
                        request_payload=ImageExportRequest(
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            file_name="filename",
                            format="PNG",
                            metadata=JsonNode(),
                            widget_ids=[
                                "widget_ids_example"
                            ],
                        ),
                    )
                ],
                metadata=dict(
                    visible_filters=[
                        VisibleFilter(
                            is_all_time_date_filter=False,
                            local_identifier="local_identifier_example",
                            title="title_example",
                        )
                    ],
                    widget="widget_example",
                ),
                raw_exports=[
                    dict(
                        request_payload=RawExportAutomationRequest(
                            custom_override=RawCustomOverride(
                                labels=dict(
                                    "key": RawCustomLabel(
                                        title="title_example",
                                    ),
                                ),
                                metrics=dict(
                                    "key": RawCustomMetric(
                                        title="title_example",
                                    ),
                                ),
                            ),
                            delimiter="U",
                            execution=AFM(
                                attributes=[
                                    AttributeItem()
                                ],
,
                                filters=[
                                    FilterDefinition()
                                ],
                                measure_definition_overrides=[
                                    MetricDefinitionOverride(
                                        definition=InlineMeasureDefinition(
                                            inline=dict(
                                                maql="maql_example",
                                            ),
                                        ),
                                        item=AfmObjectIdentifierCore(
                                            identifier=dict(
                                                id="sample_item.price",
                                                type="attribute",
                                            ),
                                        ),
                                    )
                                ],
                                measures=[
                                    MeasureItem()
                                ],
                            ),
                            execution_settings=ExecutionSettings(
                                data_sampling_percentage=0,
                                timestamp="1970-01-01T00:00:00.00Z",
                            ),
                            file_name="result",
                            format="CSV",
                            metadata=JsonNode(),
                        ),
                    )
                ],
                schedule=dict(
                    cron="0 */30 9-17 ? * MON-FRI",
                    cron_description="cron_description_example",
                    first_run="2025-01-01T12:00Z",
                    timezone="Europe/Prague",
                ),
                slides_exports=[
                    dict(
                        request_payload=SlidesExportRequest(
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            file_name="filename",
                            format="PDF",
                            metadata=JsonNode(),
                            template_id="template_id_example",
                            visualization_ids=[
                                "visualization_ids_example"
                            ],
                            widget_ids=[
                                "widget_ids_example"
                            ],
                        ),
                    )
                ],
                state="ACTIVE",
                tabular_exports=[
                    dict(
                        request_payload=TabularExportRequest(
                            custom_override=CustomOverride(
                                labels=dict(
                                    "key": CustomLabel(),
                                ),
                                metrics=dict(
                                    "key": CustomMetric(
                                        format="format_example",
                                        title="title_example",
                                    ),
                                ),
                            ),
                            execution_result="ff483727196c9dc862c7fd3a5a84df55c96d61a4",
                            file_name="result",
                            format="CSV",
                            metadata=JsonNode(),
                            related_dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            settings=Settings(
                                delimiter="U",
                                export_info=True,
                                merge_headers=True,
                                page_orientation="PORTRAIT",
                                page_size="A4",
                                pdf_page_size="a4 landscape",
                                pdf_table_style=[{"properties":[{"key":"font-size","value":"30px"}],"selector":"th"}],
                                pdf_top_left_content="Good",
                                pdf_top_right_content="Morning",
                                show_filters=False,
                            ),
                            visualization_object="f7c359bc-c230-4487-b15b-ad9685bcb537",
                            visualization_object_custom_filters=[
                                dict()
                            ],
                        ),
                    )
                ],
                tags=[
                    "tags_example"
                ],
                title="title_example",
                visual_exports=[
                    dict(
                        request_payload=VisualExportRequest(
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            file_name="filename",
                            metadata=dict(),
                        ),
                    )
                ],
            ),
            id="id1",
            relationships=dict(
                analytical_dashboard=dict(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                export_definitions=dict(
                    data=JsonApiExportDefinitionToManyLinkage([
                        JsonApiExportDefinitionLinkage(
                            id="id_example",
                            type="exportDefinition",
                        )
                    ]),
                ),
                notification_channel=dict(
                    data=JsonApiNotificationChannelToOneLinkage(None),
                ),
                recipients=dict(
                    data=JsonApiUserToManyLinkage([
                        JsonApiUserLinkage(
                            id="id_example",
                            type="user",
                        )
                    ]),
                ),
            ),
            type="automation",
        ),
    )
    try:
        # Patch an Automation
        api_response = api_instance.patch_entity_automations(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->patch_entity_automations: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
        'filter': "title==someString;description==someString;notificationChannel.id==321;analyticalDashboard.id==321",
        'include': [
        "notificationChannel,analyticalDashboard,createdBy,modifiedBy,exportDefinitions,recipients,automationResults"
    ],
    }
    body = JsonApiAutomationPatchDocument(
        data=JsonApiAutomationPatch(
            attributes=dict(
                alert=dict(
                    condition=AlertCondition(),
                    execution=AlertAfm(
                        attributes=[
                            AttributeItem(
                                label=AfmObjectIdentifierLabel(
                                    identifier=dict(
                                        id="sample_item.price",
                                        type="label",
                                    ),
                                ),
                                local_identifier="attribute_1",
                                show_all_values=False,
                            )
                        ],
                        aux_measures=[
                            MeasureItem(
                                definition=MeasureDefinition(),
                                local_identifier="metric_1",
                            )
                        ],
                        filters=[
                            FilterDefinition()
                        ],
                        measures=[
                            MeasureItem()
                        ],
                    ),
                    interval="DAY",
                    trigger="ALWAYS",
                ),
                are_relations_valid=True,
                dashboard_tabular_exports=[
                    dict(
                        request_payload=DashboardTabularExportRequestV2(
                            dashboard_filters_override=[
                                DashboardFilter()
                            ],
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            dashboard_tabs_filters_overrides=dict(
                                "key": [
                                    DashboardFilter()
                                ],
                            ),
                            file_name="result",
                            format="XLSX",
                            settings=DashboardExportSettings(
                                export_info=True,
                                merge_headers=True,
                                page_orientation="PORTRAIT",
                                page_size="A4",
                            ),
                            widget_ids=[
                                "widget_ids_example"
                            ],
                        ),
                    )
                ],
                description="description_example",
                details=dict(),
                evaluation_mode="SHARED",
                external_recipients=[
                    dict(
                        email="email_example",
                    )
                ],
                image_exports=[
                    dict(
                        request_payload=ImageExportRequest(
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            file_name="filename",
                            format="PNG",
                            metadata=JsonNode(),
                            widget_ids=[
                                "widget_ids_example"
                            ],
                        ),
                    )
                ],
                metadata=dict(
                    visible_filters=[
                        VisibleFilter(
                            is_all_time_date_filter=False,
                            local_identifier="local_identifier_example",
                            title="title_example",
                        )
                    ],
                    widget="widget_example",
                ),
                raw_exports=[
                    dict(
                        request_payload=RawExportAutomationRequest(
                            custom_override=RawCustomOverride(
                                labels=dict(
                                    "key": RawCustomLabel(
                                        title="title_example",
                                    ),
                                ),
                                metrics=dict(
                                    "key": RawCustomMetric(
                                        title="title_example",
                                    ),
                                ),
                            ),
                            delimiter="U",
                            execution=AFM(
                                attributes=[
                                    AttributeItem()
                                ],
,
                                filters=[
                                    FilterDefinition()
                                ],
                                measure_definition_overrides=[
                                    MetricDefinitionOverride(
                                        definition=InlineMeasureDefinition(
                                            inline=dict(
                                                maql="maql_example",
                                            ),
                                        ),
                                        item=AfmObjectIdentifierCore(
                                            identifier=dict(
                                                id="sample_item.price",
                                                type="attribute",
                                            ),
                                        ),
                                    )
                                ],
                                measures=[
                                    MeasureItem()
                                ],
                            ),
                            execution_settings=ExecutionSettings(
                                data_sampling_percentage=0,
                                timestamp="1970-01-01T00:00:00.00Z",
                            ),
                            file_name="result",
                            format="CSV",
                            metadata=JsonNode(),
                        ),
                    )
                ],
                schedule=dict(
                    cron="0 */30 9-17 ? * MON-FRI",
                    cron_description="cron_description_example",
                    first_run="2025-01-01T12:00Z",
                    timezone="Europe/Prague",
                ),
                slides_exports=[
                    dict(
                        request_payload=SlidesExportRequest(
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            file_name="filename",
                            format="PDF",
                            metadata=JsonNode(),
                            template_id="template_id_example",
                            visualization_ids=[
                                "visualization_ids_example"
                            ],
                            widget_ids=[
                                "widget_ids_example"
                            ],
                        ),
                    )
                ],
                state="ACTIVE",
                tabular_exports=[
                    dict(
                        request_payload=TabularExportRequest(
                            custom_override=CustomOverride(
                                labels=dict(
                                    "key": CustomLabel(),
                                ),
                                metrics=dict(
                                    "key": CustomMetric(
                                        format="format_example",
                                        title="title_example",
                                    ),
                                ),
                            ),
                            execution_result="ff483727196c9dc862c7fd3a5a84df55c96d61a4",
                            file_name="result",
                            format="CSV",
                            metadata=JsonNode(),
                            related_dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            settings=Settings(
                                delimiter="U",
                                export_info=True,
                                merge_headers=True,
                                page_orientation="PORTRAIT",
                                page_size="A4",
                                pdf_page_size="a4 landscape",
                                pdf_table_style=[{"properties":[{"key":"font-size","value":"30px"}],"selector":"th"}],
                                pdf_top_left_content="Good",
                                pdf_top_right_content="Morning",
                                show_filters=False,
                            ),
                            visualization_object="f7c359bc-c230-4487-b15b-ad9685bcb537",
                            visualization_object_custom_filters=[
                                dict()
                            ],
                        ),
                    )
                ],
                tags=[
                    "tags_example"
                ],
                title="title_example",
                visual_exports=[
                    dict(
                        request_payload=VisualExportRequest(
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            file_name="filename",
                            metadata=dict(),
                        ),
                    )
                ],
            ),
            id="id1",
            relationships=dict(
                analytical_dashboard=dict(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                export_definitions=dict(
                    data=JsonApiExportDefinitionToManyLinkage([
                        JsonApiExportDefinitionLinkage(
                            id="id_example",
                            type="exportDefinition",
                        )
                    ]),
                ),
                notification_channel=dict(
                    data=JsonApiNotificationChannelToOneLinkage(None),
                ),
                recipients=dict(
                    data=JsonApiUserToManyLinkage([
                        JsonApiUserLinkage(
                            id="id_example",
                            type="user",
                        )
                    ]),
                ),
            ),
            type="automation",
        ),
    )
    try:
        # Patch an Automation
        api_response = api_instance.patch_entity_automations(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->patch_entity_automations: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAutomationPatchDocument**](../../models/JsonApiAutomationPatchDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAutomationPatchDocument**](../../models/JsonApiAutomationPatchDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
include | IncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["notificationChannels", "analyticalDashboards", "userIdentifiers", "exportDefinitions", "users", "automationResults", "notificationChannel", "analyticalDashboard", "createdBy", "modifiedBy", "recipients", "ALL", ] 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 
objectId | ObjectIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# ObjectIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#patch_entity_automations.ApiResponseFor200) | Request successfully processed

#### patch_entity_automations.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAutomationOutDocument**](../../models/JsonApiAutomationOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAutomationOutDocument**](../../models/JsonApiAutomationOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **pause_organization_automations**
<a id="pause_organization_automations"></a>
> pause_organization_automations(organization_automation_management_bulk_request)

Pause selected automations across all workspaces

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import automations_api
from gooddata_api_client.model.organization_automation_management_bulk_request import OrganizationAutomationManagementBulkRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)

    # example passing only required values which don't have defaults set
    body = OrganizationAutomationManagementBulkRequest(
        automations=[
            OrganizationAutomationIdentifier(
                id="id_example",
                workspace_id="workspace_id_example",
            )
        ],
    )
    try:
        # Pause selected automations across all workspaces
        api_response = api_instance.pause_organization_automations(
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->pause_organization_automations: %s\n" % e)
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
[**OrganizationAutomationManagementBulkRequest**](../../models/OrganizationAutomationManagementBulkRequest.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#pause_organization_automations.ApiResponseFor204) | No Content

#### pause_organization_automations.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **pause_workspace_automations**
<a id="pause_workspace_automations"></a>
> pause_workspace_automations(workspace_idworkspace_automation_management_bulk_request)

Pause selected automations in the workspace

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import automations_api
from gooddata_api_client.model.workspace_automation_management_bulk_request import WorkspaceAutomationManagementBulkRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    body = WorkspaceAutomationManagementBulkRequest(
        automations=[
            WorkspaceAutomationIdentifier(
                id="id_example",
            )
        ],
    )
    try:
        # Pause selected automations in the workspace
        api_response = api_instance.pause_workspace_automations(
            path_params=path_params,
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->pause_workspace_automations: %s\n" % e)
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
[**WorkspaceAutomationManagementBulkRequest**](../../models/WorkspaceAutomationManagementBulkRequest.md) |  | 


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
204 | [ApiResponseFor204](#pause_workspace_automations.ApiResponseFor204) | No Content

#### pause_workspace_automations.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **search_entities_automation_results**
<a id="search_entities_automation_results"></a>
> JsonApiAutomationResultOutList search_entities_automation_results(workspace_identity_search_body)

Search request for AutomationResult

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import automations_api
from gooddata_api_client.model.json_api_automation_result_out_list import JsonApiAutomationResultOutList
from gooddata_api_client.model.entity_search_body import EntitySearchBody
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
    }
    header_params = {
    }
    body = EntitySearchBody(
        filter="filter_example",
        include=[
            "include_example"
        ],
        meta_include=[
            "meta_include_example"
        ],
        page=EntitySearchPage(
            index=0,
            size=100,
        ),
        sort=[
            EntitySearchSort(
                direction="ASC",
                _property="_property_example",
            )
        ],
    )
    try:
        # Search request for AutomationResult
        api_response = api_instance.search_entities_automation_results(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->search_entities_automation_results: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
        'origin': "ALL",
    }
    header_params = {
        'X-GDC-VALIDATE-RELATIONS': False,
    }
    body = EntitySearchBody(
        filter="filter_example",
        include=[
            "include_example"
        ],
        meta_include=[
            "meta_include_example"
        ],
        page=EntitySearchPage(
            index=0,
            size=100,
        ),
        sort=[
            EntitySearchSort(
                direction="ASC",
                _property="_property_example",
            )
        ],
    )
    try:
        # Search request for AutomationResult
        api_response = api_instance.search_entities_automation_results(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->search_entities_automation_results: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
query_params | RequestQueryParams | |
header_params | RequestHeaderParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**EntitySearchBody**](../../models/EntitySearchBody.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
origin | OriginSchema | | optional


# OriginSchema

Defines scope of origin of objects. All by default.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Defines scope of origin of objects. All by default. | must be one of ["ALL", "PARENTS", "NATIVE", ] if omitted the server will use the default value of "ALL"

### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
X-GDC-VALIDATE-RELATIONS | XGDCVALIDATERELATIONSSchema | | optional

# XGDCVALIDATERELATIONSSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bool,  | BoolClass,  |  | if omitted the server will use the default value of False

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
200 | [ApiResponseFor200](#search_entities_automation_results.ApiResponseFor200) | Request successfully processed

#### search_entities_automation_results.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAutomationResultOutList**](../../models/JsonApiAutomationResultOutList.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAutomationResultOutList**](../../models/JsonApiAutomationResultOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **search_entities_automations**
<a id="search_entities_automations"></a>
> JsonApiAutomationOutList search_entities_automations(workspace_identity_search_body)

Search request for Automation

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import automations_api
from gooddata_api_client.model.json_api_automation_out_list import JsonApiAutomationOutList
from gooddata_api_client.model.entity_search_body import EntitySearchBody
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
    }
    header_params = {
    }
    body = EntitySearchBody(
        filter="filter_example",
        include=[
            "include_example"
        ],
        meta_include=[
            "meta_include_example"
        ],
        page=EntitySearchPage(
            index=0,
            size=100,
        ),
        sort=[
            EntitySearchSort(
                direction="ASC",
                _property="_property_example",
            )
        ],
    )
    try:
        # Search request for Automation
        api_response = api_instance.search_entities_automations(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->search_entities_automations: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
        'origin': "ALL",
    }
    header_params = {
        'X-GDC-VALIDATE-RELATIONS': False,
    }
    body = EntitySearchBody(
        filter="filter_example",
        include=[
            "include_example"
        ],
        meta_include=[
            "meta_include_example"
        ],
        page=EntitySearchPage(
            index=0,
            size=100,
        ),
        sort=[
            EntitySearchSort(
                direction="ASC",
                _property="_property_example",
            )
        ],
    )
    try:
        # Search request for Automation
        api_response = api_instance.search_entities_automations(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->search_entities_automations: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
query_params | RequestQueryParams | |
header_params | RequestHeaderParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**EntitySearchBody**](../../models/EntitySearchBody.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
origin | OriginSchema | | optional


# OriginSchema

Defines scope of origin of objects. All by default.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Defines scope of origin of objects. All by default. | must be one of ["ALL", "PARENTS", "NATIVE", ] if omitted the server will use the default value of "ALL"

### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
X-GDC-VALIDATE-RELATIONS | XGDCVALIDATERELATIONSSchema | | optional

# XGDCVALIDATERELATIONSSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bool,  | BoolClass,  |  | if omitted the server will use the default value of False

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
200 | [ApiResponseFor200](#search_entities_automations.ApiResponseFor200) | Request successfully processed

#### search_entities_automations.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAutomationOutList**](../../models/JsonApiAutomationOutList.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAutomationOutList**](../../models/JsonApiAutomationOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **set_automations**
<a id="set_automations"></a>
> set_automations(workspace_iddeclarative_automation)

Set automations

Set automations for the specific workspace.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import automations_api
from gooddata_api_client.model.declarative_automation import DeclarativeAutomation
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    body = [
        DeclarativeAutomation(
            alert=AutomationAlert(
                condition=None,
                execution=AlertAfm(
                    attributes=[
                        AttributeItem(
                            label=AfmObjectIdentifierLabel(
                                identifier=dict(
                                    id="sample_item.price",
                                    type="label",
                                ),
                            ),
                            local_identifier="attribute_1",
                            show_all_values=False,
                        )
                    ],
                    aux_measures=[
                        MeasureItem(
                            definition=MeasureDefinition(),
                            local_identifier="metric_1",
                        )
                    ],
                    filters=[
                        FilterDefinition()
                    ],
                    measures=[
                        MeasureItem()
                    ],
                ),
                interval="DAY",
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
            dashboard_tabular_exports=[
                AutomationDashboardTabularExport(
                    request_payload=DashboardTabularExportRequestV2(
                        dashboard_filters_override=[
                            DashboardFilter()
                        ],
                        dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                        dashboard_tabs_filters_overrides=dict(
                            "key": [
                                DashboardFilter()
                            ],
                        ),
                        file_name="result",
                        format="XLSX",
                        settings=DashboardExportSettings(
                            export_info=True,
                            merge_headers=True,
                            page_orientation="PORTRAIT",
                            page_size="A4",
                        ),
                        widget_ids=[
                            "widget_ids_example"
                        ],
                    ),
                )
            ],
            description="description_example",
            details=dict(
                "key": "key_example",
            ),
            evaluation_mode="PER_RECIPIENT",
            export_definitions=[
                DeclarativeExportDefinitionIdentifier(
                    id="export123",
                    type="exportDefinition",
                )
            ],
            external_recipients=[
                AutomationExternalRecipient(
                    email="email_example",
                )
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
                            "widget_ids_example"
                        ],
                    ),
                )
            ],
            metadata=AutomationMetadata(
                visible_filters=[
                    VisibleFilter(
                        is_all_time_date_filter=False,
                        local_identifier="local_identifier_example",
                        title="title_example",
                    )
                ],
                widget="widget_example",
            ),
            modified_at="2023-07-20 12:30",
            modified_by=DeclarativeUserIdentifier(),
            notification_channel=DeclarativeNotificationChannelIdentifier(
                id="webhook123",
                type="notificationChannel",
            ),
            raw_exports=[
                AutomationRawExport(
                    request_payload=RawExportAutomationRequest(
                        custom_override=RawCustomOverride(
                            labels=dict(
                                "key": RawCustomLabel(
                                    title="title_example",
                                ),
                            ),
                            metrics=dict(
                                "key": RawCustomMetric(
                                    title="title_example",
                                ),
                            ),
                        ),
                        delimiter="U",
                        execution=AFM(
                            attributes=[
                                AttributeItem()
                            ],
,
                            filters=[
                                FilterDefinition()
                            ],
                            measure_definition_overrides=[
                                MetricDefinitionOverride(
                                    definition=InlineMeasureDefinition(
                                        inline=dict(
                                            maql="maql_example",
                                        ),
                                    ),
                                    item=AfmObjectIdentifierCore(
                                        identifier=dict(
                                            id="sample_item.price",
                                            type="attribute",
                                        ),
                                    ),
                                )
                            ],
                            measures=[
                                MeasureItem()
                            ],
                        ),
                        execution_settings=ExecutionSettings(
                            data_sampling_percentage=0,
                            timestamp="1970-01-01T00:00:00.00Z",
                        ),
                        file_name="result",
                        format="CSV",
                        metadata=JsonNode(),
                    ),
                )
            ],
            recipients=[
                DeclarativeUserIdentifier()
            ],
            schedule=AutomationSchedule(
                cron="0 */30 9-17 ? * MON-FRI",
                cron_description="cron_description_example",
                first_run="2025-01-01T12:00Z",
                timezone="Europe/Prague",
            ),
            slides_exports=[
                AutomationSlidesExport(
                    request_payload=SlidesExportRequest(
                        dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                        file_name="filename",
                        format="PDF",
                        metadata=JsonNode(),
                        template_id="template_id_example",
                        visualization_ids=[
                            "visualization_ids_example"
                        ],
                        widget_ids=[
                            "widget_ids_example"
                        ],
                    ),
                )
            ],
            state="ACTIVE",
            tabular_exports=[
                AutomationTabularExport(
                    request_payload=TabularExportRequest(
                        custom_override=CustomOverride(
                            labels=dict(
                                "key": CustomLabel(),
                            ),
                            metrics=dict(
                                "key": CustomMetric(
                                    format="format_example",
                                    title="title_example",
                                ),
                            ),
                        ),
                        execution_result="ff483727196c9dc862c7fd3a5a84df55c96d61a4",
                        file_name="result",
                        format="CSV",
                        metadata=JsonNode(),
                        related_dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                        settings=Settings(
                            delimiter="U",
                            export_info=True,
                            merge_headers=True,
                            page_orientation="PORTRAIT",
                            page_size="A4",
                            pdf_page_size="a4 landscape",
                            pdf_table_style=[{"properties":[{"key":"font-size","value":"30px"}],"selector":"th"}],
                            pdf_top_left_content="Good",
                            pdf_top_right_content="Morning",
                            show_filters=False,
                        ),
                        visualization_object="f7c359bc-c230-4487-b15b-ad9685bcb537",
                        visualization_object_custom_filters=[
                            dict()
                        ],
                    ),
                )
            ],
            tags=[
                "[\"Revenue\",\"Sales\"]"
            ],
            title="title_example",
            visual_exports=[
                AutomationVisualExport(
                    request_payload=VisualExportRequest(
                        dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                        file_name="filename",
                        metadata=dict(),
                    ),
                )
            ],
        )
    ]
    try:
        # Set automations
        api_response = api_instance.set_automations(
            path_params=path_params,
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->set_automations: %s\n" % e)
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

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeAutomation**]({{complexTypePrefix}}DeclarativeAutomation.md) | [**DeclarativeAutomation**]({{complexTypePrefix}}DeclarativeAutomation.md) | [**DeclarativeAutomation**]({{complexTypePrefix}}DeclarativeAutomation.md) |  | 

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
204 | [ApiResponseFor204](#set_automations.ApiResponseFor204) | Automations successfully set.

#### set_automations.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **trigger_automation**
<a id="trigger_automation"></a>
> trigger_automation(workspace_idtrigger_automation_request)

Trigger automation.

Trigger the automation in the request.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import automations_api
from gooddata_api_client.model.trigger_automation_request import TriggerAutomationRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    body = TriggerAutomationRequest(
        automation=AdHocAutomation(
            alert=AutomationAlert(
                condition=None,
                execution=AlertAfm(
                    attributes=[
                        AttributeItem(
                            label=AfmObjectIdentifierLabel(
                                identifier=dict(
                                    id="sample_item.price",
                                    type="label",
                                ),
                            ),
                            local_identifier="attribute_1",
                            show_all_values=False,
                        )
                    ],
                    aux_measures=[
                        MeasureItem(
                            definition=MeasureDefinition(),
                            local_identifier="metric_1",
                        )
                    ],
                    filters=[
                        FilterDefinition()
                    ],
                    measures=[
                        MeasureItem()
                    ],
                ),
                interval="DAY",
                trigger="ALWAYS",
            ),
            analytical_dashboard=DeclarativeAnalyticalDashboardIdentifier(
                id="dashboard123",
                type="analyticalDashboard",
            ),
            dashboard_tabular_exports=[
                AutomationDashboardTabularExport(
                    request_payload=DashboardTabularExportRequestV2(
                        dashboard_filters_override=[
                            DashboardFilter()
                        ],
                        dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                        dashboard_tabs_filters_overrides=dict(
                            "key": [
                                DashboardFilter()
                            ],
                        ),
                        file_name="result",
                        format="XLSX",
                        settings=DashboardExportSettings(
                            export_info=True,
                            merge_headers=True,
                            page_orientation="PORTRAIT",
                            page_size="A4",
                        ),
                        widget_ids=[
                            "widget_ids_example"
                        ],
                    ),
                )
            ],
            description="description_example",
            details=dict(
                "key": "key_example",
            ),
            external_recipients=[
                AutomationExternalRecipient(
                    email="email_example",
                )
            ],
            image_exports=[
                AutomationImageExport(
                    request_payload=ImageExportRequest(
                        dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                        file_name="filename",
                        format="PNG",
                        metadata=JsonNode(),
                        widget_ids=[
                            "widget_ids_example"
                        ],
                    ),
                )
            ],
            metadata=AutomationMetadata(
                visible_filters=[
                    VisibleFilter(
                        is_all_time_date_filter=False,
                        local_identifier="local_identifier_example",
                        title="title_example",
                    )
                ],
                widget="widget_example",
            ),
            notification_channel=DeclarativeNotificationChannelIdentifier(
                id="webhook123",
                type="notificationChannel",
            ),
            raw_exports=[
                AutomationRawExport(
                    request_payload=RawExportAutomationRequest(
                        custom_override=RawCustomOverride(
                            labels=dict(
                                "key": RawCustomLabel(
                                    title="title_example",
                                ),
                            ),
                            metrics=dict(
                                "key": RawCustomMetric(
                                    title="title_example",
                                ),
                            ),
                        ),
                        delimiter="U",
                        execution=AFM(
                            attributes=[
                                AttributeItem()
                            ],
,
                            filters=[
                                FilterDefinition()
                            ],
                            measure_definition_overrides=[
                                MetricDefinitionOverride(
                                    definition=InlineMeasureDefinition(
                                        inline=dict(
                                            maql="maql_example",
                                        ),
                                    ),
                                    item=AfmObjectIdentifierCore(
                                        identifier=dict(
                                            id="sample_item.price",
                                            type="attribute",
                                        ),
                                    ),
                                )
                            ],
                            measures=[
                                MeasureItem()
                            ],
                        ),
                        execution_settings=ExecutionSettings(
                            data_sampling_percentage=0,
                            timestamp="1970-01-01T00:00:00.00Z",
                        ),
                        file_name="result",
                        format="CSV",
                        metadata=JsonNode(),
                    ),
                )
            ],
            recipients=[
                DeclarativeUserIdentifier(
                    id="employee123",
                    type="user",
                )
            ],
            slides_exports=[
                AutomationSlidesExport(
                    request_payload=SlidesExportRequest(
                        dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                        file_name="filename",
                        format="PDF",
                        metadata=JsonNode(),
                        template_id="template_id_example",
                        visualization_ids=[
                            "visualization_ids_example"
                        ],
                        widget_ids=[
                            "widget_ids_example"
                        ],
                    ),
                )
            ],
            tabular_exports=[
                AutomationTabularExport(
                    request_payload=TabularExportRequest(
                        custom_override=CustomOverride(
                            labels=dict(
                                "key": CustomLabel(),
                            ),
                            metrics=dict(
                                "key": CustomMetric(
                                    format="format_example",
                                    title="title_example",
                                ),
                            ),
                        ),
                        execution_result="ff483727196c9dc862c7fd3a5a84df55c96d61a4",
                        file_name="result",
                        format="CSV",
                        metadata=JsonNode(),
                        related_dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                        settings=Settings(
                            delimiter="U",
                            export_info=True,
                            merge_headers=True,
                            page_orientation="PORTRAIT",
                            page_size="A4",
                            pdf_page_size="a4 landscape",
                            pdf_table_style=[{"properties":[{"key":"font-size","value":"30px"}],"selector":"th"}],
                            pdf_top_left_content="Good",
                            pdf_top_right_content="Morning",
                            show_filters=False,
                        ),
                        visualization_object="f7c359bc-c230-4487-b15b-ad9685bcb537",
                        visualization_object_custom_filters=[
                            dict()
                        ],
                    ),
                )
            ],
            tags=["Revenue","Sales"],
            title="title_example",
            visual_exports=[
                AutomationVisualExport(
                    request_payload=VisualExportRequest(
                        dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                        file_name="filename",
                        metadata=dict(),
                    ),
                )
            ],
        ),
    )
    try:
        # Trigger automation.
        api_response = api_instance.trigger_automation(
            path_params=path_params,
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->trigger_automation: %s\n" % e)
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
[**TriggerAutomationRequest**](../../models/TriggerAutomationRequest.md) |  | 


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
204 | [ApiResponseFor204](#trigger_automation.ApiResponseFor204) | The automation is successfully triggered.

#### trigger_automation.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **trigger_existing_automation**
<a id="trigger_existing_automation"></a>
> trigger_existing_automation(workspace_idautomation_id)

Trigger existing automation.

Trigger the existing automation to execute immediately.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import automations_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
        'automationId': "automationId_example",
    }
    try:
        # Trigger existing automation.
        api_response = api_instance.trigger_existing_automation(
            path_params=path_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->trigger_existing_automation: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 
automationId | AutomationIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# AutomationIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#trigger_existing_automation.ApiResponseFor204) | The automation is successfully triggered.

#### trigger_existing_automation.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **unpause_organization_automations**
<a id="unpause_organization_automations"></a>
> unpause_organization_automations(organization_automation_management_bulk_request)

Unpause selected automations across all workspaces

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import automations_api
from gooddata_api_client.model.organization_automation_management_bulk_request import OrganizationAutomationManagementBulkRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)

    # example passing only required values which don't have defaults set
    body = OrganizationAutomationManagementBulkRequest(
        automations=[
            OrganizationAutomationIdentifier(
                id="id_example",
                workspace_id="workspace_id_example",
            )
        ],
    )
    try:
        # Unpause selected automations across all workspaces
        api_response = api_instance.unpause_organization_automations(
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->unpause_organization_automations: %s\n" % e)
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
[**OrganizationAutomationManagementBulkRequest**](../../models/OrganizationAutomationManagementBulkRequest.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#unpause_organization_automations.ApiResponseFor204) | No Content

#### unpause_organization_automations.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **unpause_workspace_automations**
<a id="unpause_workspace_automations"></a>
> unpause_workspace_automations(workspace_idworkspace_automation_management_bulk_request)

Unpause selected automations in the workspace

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import automations_api
from gooddata_api_client.model.workspace_automation_management_bulk_request import WorkspaceAutomationManagementBulkRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    body = WorkspaceAutomationManagementBulkRequest(
        automations=[
            WorkspaceAutomationIdentifier(
                id="id_example",
            )
        ],
    )
    try:
        # Unpause selected automations in the workspace
        api_response = api_instance.unpause_workspace_automations(
            path_params=path_params,
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->unpause_workspace_automations: %s\n" % e)
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
[**WorkspaceAutomationManagementBulkRequest**](../../models/WorkspaceAutomationManagementBulkRequest.md) |  | 


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
204 | [ApiResponseFor204](#unpause_workspace_automations.ApiResponseFor204) | No Content

#### unpause_workspace_automations.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **unsubscribe_all_automations**
<a id="unsubscribe_all_automations"></a>
> unsubscribe_all_automations()

Unsubscribe from all automations in all workspaces

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import automations_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Unsubscribe from all automations in all workspaces
        api_response = api_instance.unsubscribe_all_automations()
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->unsubscribe_all_automations: %s\n" % e)
```
### Parameters
This endpoint does not need any parameter.

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#unsubscribe_all_automations.ApiResponseFor204) | No Content

#### unsubscribe_all_automations.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **unsubscribe_automation**
<a id="unsubscribe_automation"></a>
> unsubscribe_automation(workspace_idautomation_id)

Unsubscribe from an automation

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import automations_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
        'automationId': "automationId_example",
    }
    try:
        # Unsubscribe from an automation
        api_response = api_instance.unsubscribe_automation(
            path_params=path_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->unsubscribe_automation: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 
automationId | AutomationIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# AutomationIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#unsubscribe_automation.ApiResponseFor204) | No Content

#### unsubscribe_automation.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **unsubscribe_organization_automations**
<a id="unsubscribe_organization_automations"></a>
> unsubscribe_organization_automations(organization_automation_management_bulk_request)

Unsubscribe from selected automations across all workspaces

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import automations_api
from gooddata_api_client.model.organization_automation_management_bulk_request import OrganizationAutomationManagementBulkRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)

    # example passing only required values which don't have defaults set
    body = OrganizationAutomationManagementBulkRequest(
        automations=[
            OrganizationAutomationIdentifier(
                id="id_example",
                workspace_id="workspace_id_example",
            )
        ],
    )
    try:
        # Unsubscribe from selected automations across all workspaces
        api_response = api_instance.unsubscribe_organization_automations(
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->unsubscribe_organization_automations: %s\n" % e)
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
[**OrganizationAutomationManagementBulkRequest**](../../models/OrganizationAutomationManagementBulkRequest.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#unsubscribe_organization_automations.ApiResponseFor204) | No Content

#### unsubscribe_organization_automations.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **unsubscribe_selected_workspace_automations**
<a id="unsubscribe_selected_workspace_automations"></a>
> unsubscribe_selected_workspace_automations(workspace_idworkspace_automation_management_bulk_request)

Unsubscribe from selected automations in the workspace

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import automations_api
from gooddata_api_client.model.workspace_automation_management_bulk_request import WorkspaceAutomationManagementBulkRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    body = WorkspaceAutomationManagementBulkRequest(
        automations=[
            WorkspaceAutomationIdentifier(
                id="id_example",
            )
        ],
    )
    try:
        # Unsubscribe from selected automations in the workspace
        api_response = api_instance.unsubscribe_selected_workspace_automations(
            path_params=path_params,
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->unsubscribe_selected_workspace_automations: %s\n" % e)
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
[**WorkspaceAutomationManagementBulkRequest**](../../models/WorkspaceAutomationManagementBulkRequest.md) |  | 


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
204 | [ApiResponseFor204](#unsubscribe_selected_workspace_automations.ApiResponseFor204) | No Content

#### unsubscribe_selected_workspace_automations.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **unsubscribe_workspace_automations**
<a id="unsubscribe_workspace_automations"></a>
> unsubscribe_workspace_automations(workspace_id)

Unsubscribe from all automations in the workspace

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import automations_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    try:
        # Unsubscribe from all automations in the workspace
        api_response = api_instance.unsubscribe_workspace_automations(
            path_params=path_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->unsubscribe_workspace_automations: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
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
204 | [ApiResponseFor204](#unsubscribe_workspace_automations.ApiResponseFor204) | No Content

#### unsubscribe_workspace_automations.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_entity_automations**
<a id="update_entity_automations"></a>
> JsonApiAutomationOutDocument update_entity_automations(workspace_idobject_idjson_api_automation_in_document)

Put an Automation

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import automations_api
from gooddata_api_client.model.json_api_automation_in_document import JsonApiAutomationInDocument
from gooddata_api_client.model.json_api_automation_out_document import JsonApiAutomationOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
    }
    body = JsonApiAutomationInDocument(
        data=JsonApiAutomationIn(
            attributes=dict(
                alert=dict(
                    condition=AlertCondition(),
                    execution=AlertAfm(
                        attributes=[
                            AttributeItem(
                                label=AfmObjectIdentifierLabel(
                                    identifier=dict(
                                        id="sample_item.price",
                                        type="label",
                                    ),
                                ),
                                local_identifier="attribute_1",
                                show_all_values=False,
                            )
                        ],
                        aux_measures=[
                            MeasureItem(
                                definition=MeasureDefinition(),
                                local_identifier="metric_1",
                            )
                        ],
                        filters=[
                            FilterDefinition()
                        ],
                        measures=[
                            MeasureItem()
                        ],
                    ),
                    interval="DAY",
                    trigger="ALWAYS",
                ),
                are_relations_valid=True,
                dashboard_tabular_exports=[
                    dict(
                        request_payload=DashboardTabularExportRequestV2(
                            dashboard_filters_override=[
                                DashboardFilter()
                            ],
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            dashboard_tabs_filters_overrides=dict(
                                "key": [
                                    DashboardFilter()
                                ],
                            ),
                            file_name="result",
                            format="XLSX",
                            settings=DashboardExportSettings(
                                export_info=True,
                                merge_headers=True,
                                page_orientation="PORTRAIT",
                                page_size="A4",
                            ),
                            widget_ids=[
                                "widget_ids_example"
                            ],
                        ),
                    )
                ],
                description="description_example",
                details=dict(),
                evaluation_mode="SHARED",
                external_recipients=[
                    dict(
                        email="email_example",
                    )
                ],
                image_exports=[
                    dict(
                        request_payload=ImageExportRequest(
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            file_name="filename",
                            format="PNG",
                            metadata=JsonNode(),
                            widget_ids=[
                                "widget_ids_example"
                            ],
                        ),
                    )
                ],
                metadata=dict(
                    visible_filters=[
                        VisibleFilter(
                            is_all_time_date_filter=False,
                            local_identifier="local_identifier_example",
                            title="title_example",
                        )
                    ],
                    widget="widget_example",
                ),
                raw_exports=[
                    dict(
                        request_payload=RawExportAutomationRequest(
                            custom_override=RawCustomOverride(
                                labels=dict(
                                    "key": RawCustomLabel(
                                        title="title_example",
                                    ),
                                ),
                                metrics=dict(
                                    "key": RawCustomMetric(
                                        title="title_example",
                                    ),
                                ),
                            ),
                            delimiter="U",
                            execution=AFM(
                                attributes=[
                                    AttributeItem()
                                ],
,
                                filters=[
                                    FilterDefinition()
                                ],
                                measure_definition_overrides=[
                                    MetricDefinitionOverride(
                                        definition=InlineMeasureDefinition(
                                            inline=dict(
                                                maql="maql_example",
                                            ),
                                        ),
                                        item=AfmObjectIdentifierCore(
                                            identifier=dict(
                                                id="sample_item.price",
                                                type="attribute",
                                            ),
                                        ),
                                    )
                                ],
                                measures=[
                                    MeasureItem()
                                ],
                            ),
                            execution_settings=ExecutionSettings(
                                data_sampling_percentage=0,
                                timestamp="1970-01-01T00:00:00.00Z",
                            ),
                            file_name="result",
                            format="CSV",
                            metadata=JsonNode(),
                        ),
                    )
                ],
                schedule=dict(
                    cron="0 */30 9-17 ? * MON-FRI",
                    cron_description="cron_description_example",
                    first_run="2025-01-01T12:00Z",
                    timezone="Europe/Prague",
                ),
                slides_exports=[
                    dict(
                        request_payload=SlidesExportRequest(
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            file_name="filename",
                            format="PDF",
                            metadata=JsonNode(),
                            template_id="template_id_example",
                            visualization_ids=[
                                "visualization_ids_example"
                            ],
                            widget_ids=[
                                "widget_ids_example"
                            ],
                        ),
                    )
                ],
                state="ACTIVE",
                tabular_exports=[
                    dict(
                        request_payload=TabularExportRequest(
                            custom_override=CustomOverride(
                                labels=dict(
                                    "key": CustomLabel(),
                                ),
                                metrics=dict(
                                    "key": CustomMetric(
                                        format="format_example",
                                        title="title_example",
                                    ),
                                ),
                            ),
                            execution_result="ff483727196c9dc862c7fd3a5a84df55c96d61a4",
                            file_name="result",
                            format="CSV",
                            metadata=JsonNode(),
                            related_dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            settings=Settings(
                                delimiter="U",
                                export_info=True,
                                merge_headers=True,
                                page_orientation="PORTRAIT",
                                page_size="A4",
                                pdf_page_size="a4 landscape",
                                pdf_table_style=[{"properties":[{"key":"font-size","value":"30px"}],"selector":"th"}],
                                pdf_top_left_content="Good",
                                pdf_top_right_content="Morning",
                                show_filters=False,
                            ),
                            visualization_object="f7c359bc-c230-4487-b15b-ad9685bcb537",
                            visualization_object_custom_filters=[
                                dict()
                            ],
                        ),
                    )
                ],
                tags=[
                    "tags_example"
                ],
                title="title_example",
                visual_exports=[
                    dict(
                        request_payload=VisualExportRequest(
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            file_name="filename",
                            metadata=dict(),
                        ),
                    )
                ],
            ),
            id="id1",
            relationships=dict(
                analytical_dashboard=dict(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                export_definitions=dict(
                    data=JsonApiExportDefinitionToManyLinkage([
                        JsonApiExportDefinitionLinkage(
                            id="id_example",
                            type="exportDefinition",
                        )
                    ]),
                ),
                notification_channel=dict(
                    data=JsonApiNotificationChannelToOneLinkage(None),
                ),
                recipients=dict(
                    data=JsonApiUserToManyLinkage([
                        JsonApiUserLinkage(
                            id="id_example",
                            type="user",
                        )
                    ]),
                ),
            ),
            type="automation",
        ),
    )
    try:
        # Put an Automation
        api_response = api_instance.update_entity_automations(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->update_entity_automations: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
        'filter': "title==someString;description==someString;notificationChannel.id==321;analyticalDashboard.id==321",
        'include': [
        "notificationChannel,analyticalDashboard,createdBy,modifiedBy,exportDefinitions,recipients,automationResults"
    ],
    }
    body = JsonApiAutomationInDocument(
        data=JsonApiAutomationIn(
            attributes=dict(
                alert=dict(
                    condition=AlertCondition(),
                    execution=AlertAfm(
                        attributes=[
                            AttributeItem(
                                label=AfmObjectIdentifierLabel(
                                    identifier=dict(
                                        id="sample_item.price",
                                        type="label",
                                    ),
                                ),
                                local_identifier="attribute_1",
                                show_all_values=False,
                            )
                        ],
                        aux_measures=[
                            MeasureItem(
                                definition=MeasureDefinition(),
                                local_identifier="metric_1",
                            )
                        ],
                        filters=[
                            FilterDefinition()
                        ],
                        measures=[
                            MeasureItem()
                        ],
                    ),
                    interval="DAY",
                    trigger="ALWAYS",
                ),
                are_relations_valid=True,
                dashboard_tabular_exports=[
                    dict(
                        request_payload=DashboardTabularExportRequestV2(
                            dashboard_filters_override=[
                                DashboardFilter()
                            ],
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            dashboard_tabs_filters_overrides=dict(
                                "key": [
                                    DashboardFilter()
                                ],
                            ),
                            file_name="result",
                            format="XLSX",
                            settings=DashboardExportSettings(
                                export_info=True,
                                merge_headers=True,
                                page_orientation="PORTRAIT",
                                page_size="A4",
                            ),
                            widget_ids=[
                                "widget_ids_example"
                            ],
                        ),
                    )
                ],
                description="description_example",
                details=dict(),
                evaluation_mode="SHARED",
                external_recipients=[
                    dict(
                        email="email_example",
                    )
                ],
                image_exports=[
                    dict(
                        request_payload=ImageExportRequest(
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            file_name="filename",
                            format="PNG",
                            metadata=JsonNode(),
                            widget_ids=[
                                "widget_ids_example"
                            ],
                        ),
                    )
                ],
                metadata=dict(
                    visible_filters=[
                        VisibleFilter(
                            is_all_time_date_filter=False,
                            local_identifier="local_identifier_example",
                            title="title_example",
                        )
                    ],
                    widget="widget_example",
                ),
                raw_exports=[
                    dict(
                        request_payload=RawExportAutomationRequest(
                            custom_override=RawCustomOverride(
                                labels=dict(
                                    "key": RawCustomLabel(
                                        title="title_example",
                                    ),
                                ),
                                metrics=dict(
                                    "key": RawCustomMetric(
                                        title="title_example",
                                    ),
                                ),
                            ),
                            delimiter="U",
                            execution=AFM(
                                attributes=[
                                    AttributeItem()
                                ],
,
                                filters=[
                                    FilterDefinition()
                                ],
                                measure_definition_overrides=[
                                    MetricDefinitionOverride(
                                        definition=InlineMeasureDefinition(
                                            inline=dict(
                                                maql="maql_example",
                                            ),
                                        ),
                                        item=AfmObjectIdentifierCore(
                                            identifier=dict(
                                                id="sample_item.price",
                                                type="attribute",
                                            ),
                                        ),
                                    )
                                ],
                                measures=[
                                    MeasureItem()
                                ],
                            ),
                            execution_settings=ExecutionSettings(
                                data_sampling_percentage=0,
                                timestamp="1970-01-01T00:00:00.00Z",
                            ),
                            file_name="result",
                            format="CSV",
                            metadata=JsonNode(),
                        ),
                    )
                ],
                schedule=dict(
                    cron="0 */30 9-17 ? * MON-FRI",
                    cron_description="cron_description_example",
                    first_run="2025-01-01T12:00Z",
                    timezone="Europe/Prague",
                ),
                slides_exports=[
                    dict(
                        request_payload=SlidesExportRequest(
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            file_name="filename",
                            format="PDF",
                            metadata=JsonNode(),
                            template_id="template_id_example",
                            visualization_ids=[
                                "visualization_ids_example"
                            ],
                            widget_ids=[
                                "widget_ids_example"
                            ],
                        ),
                    )
                ],
                state="ACTIVE",
                tabular_exports=[
                    dict(
                        request_payload=TabularExportRequest(
                            custom_override=CustomOverride(
                                labels=dict(
                                    "key": CustomLabel(),
                                ),
                                metrics=dict(
                                    "key": CustomMetric(
                                        format="format_example",
                                        title="title_example",
                                    ),
                                ),
                            ),
                            execution_result="ff483727196c9dc862c7fd3a5a84df55c96d61a4",
                            file_name="result",
                            format="CSV",
                            metadata=JsonNode(),
                            related_dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            settings=Settings(
                                delimiter="U",
                                export_info=True,
                                merge_headers=True,
                                page_orientation="PORTRAIT",
                                page_size="A4",
                                pdf_page_size="a4 landscape",
                                pdf_table_style=[{"properties":[{"key":"font-size","value":"30px"}],"selector":"th"}],
                                pdf_top_left_content="Good",
                                pdf_top_right_content="Morning",
                                show_filters=False,
                            ),
                            visualization_object="f7c359bc-c230-4487-b15b-ad9685bcb537",
                            visualization_object_custom_filters=[
                                dict()
                            ],
                        ),
                    )
                ],
                tags=[
                    "tags_example"
                ],
                title="title_example",
                visual_exports=[
                    dict(
                        request_payload=VisualExportRequest(
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            file_name="filename",
                            metadata=dict(),
                        ),
                    )
                ],
            ),
            id="id1",
            relationships=dict(
                analytical_dashboard=dict(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                export_definitions=dict(
                    data=JsonApiExportDefinitionToManyLinkage([
                        JsonApiExportDefinitionLinkage(
                            id="id_example",
                            type="exportDefinition",
                        )
                    ]),
                ),
                notification_channel=dict(
                    data=JsonApiNotificationChannelToOneLinkage(None),
                ),
                recipients=dict(
                    data=JsonApiUserToManyLinkage([
                        JsonApiUserLinkage(
                            id="id_example",
                            type="user",
                        )
                    ]),
                ),
            ),
            type="automation",
        ),
    )
    try:
        # Put an Automation
        api_response = api_instance.update_entity_automations(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->update_entity_automations: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAutomationInDocument**](../../models/JsonApiAutomationInDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAutomationInDocument**](../../models/JsonApiAutomationInDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
include | IncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["notificationChannels", "analyticalDashboards", "userIdentifiers", "exportDefinitions", "users", "automationResults", "notificationChannel", "analyticalDashboard", "createdBy", "modifiedBy", "recipients", "ALL", ] 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 
objectId | ObjectIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# ObjectIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_entity_automations.ApiResponseFor200) | Request successfully processed

#### update_entity_automations.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAutomationOutDocument**](../../models/JsonApiAutomationOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAutomationOutDocument**](../../models/JsonApiAutomationOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


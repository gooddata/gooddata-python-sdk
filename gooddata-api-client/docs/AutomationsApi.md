# gooddata_api_client.AutomationsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_automations**](AutomationsApi.md#create_entity_automations) | **POST** /api/v1/entities/workspaces/{workspaceId}/automations | Post Automations
[**delete_entity_automations**](AutomationsApi.md#delete_entity_automations) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/automations/{objectId} | Delete an Automation
[**delete_organization_automations**](AutomationsApi.md#delete_organization_automations) | **POST** /api/v1/actions/organization/automations/delete | Delete selected automations across all workspaces
[**delete_workspace_automations**](AutomationsApi.md#delete_workspace_automations) | **POST** /api/v1/actions/workspaces/{workspaceId}/automations/delete | Delete selected automations in the workspace
[**get_all_automations_workspace_automations**](AutomationsApi.md#get_all_automations_workspace_automations) | **GET** /api/v1/entities/organization/workspaceAutomations | Get all Automations across all Workspaces
[**get_all_entities_automations**](AutomationsApi.md#get_all_entities_automations) | **GET** /api/v1/entities/workspaces/{workspaceId}/automations | Get all Automations
[**get_automations**](AutomationsApi.md#get_automations) | **GET** /api/v1/layout/workspaces/{workspaceId}/automations | Get automations
[**get_entity_automations**](AutomationsApi.md#get_entity_automations) | **GET** /api/v1/entities/workspaces/{workspaceId}/automations/{objectId} | Get an Automation
[**patch_entity_automations**](AutomationsApi.md#patch_entity_automations) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/automations/{objectId} | Patch an Automation
[**pause_organization_automations**](AutomationsApi.md#pause_organization_automations) | **POST** /api/v1/actions/organization/automations/pause | Pause selected automations across all workspaces
[**pause_workspace_automations**](AutomationsApi.md#pause_workspace_automations) | **POST** /api/v1/actions/workspaces/{workspaceId}/automations/pause | Pause selected automations in the workspace
[**set_automations**](AutomationsApi.md#set_automations) | **PUT** /api/v1/layout/workspaces/{workspaceId}/automations | Set automations
[**trigger_automation**](AutomationsApi.md#trigger_automation) | **POST** /api/v1/actions/workspaces/{workspaceId}/automations/trigger | Trigger automation.
[**trigger_existing_automation**](AutomationsApi.md#trigger_existing_automation) | **POST** /api/v1/actions/workspaces/{workspaceId}/automations/{automationId}/trigger | Trigger existing automation.
[**unpause_organization_automations**](AutomationsApi.md#unpause_organization_automations) | **POST** /api/v1/actions/organization/automations/unpause | Unpause selected automations across all workspaces
[**unpause_workspace_automations**](AutomationsApi.md#unpause_workspace_automations) | **POST** /api/v1/actions/workspaces/{workspaceId}/automations/unpause | Unpause selected automations in the workspace
[**unsubscribe_all_automations**](AutomationsApi.md#unsubscribe_all_automations) | **DELETE** /api/v1/actions/organization/automations/unsubscribe | Unsubscribe from all automations in all workspaces
[**unsubscribe_automation**](AutomationsApi.md#unsubscribe_automation) | **DELETE** /api/v1/actions/workspaces/{workspaceId}/automations/{automationId}/unsubscribe | Unsubscribe from an automation
[**unsubscribe_organization_automations**](AutomationsApi.md#unsubscribe_organization_automations) | **POST** /api/v1/actions/organization/automations/unsubscribe | Unsubscribe from selected automations across all workspaces
[**unsubscribe_selected_workspace_automations**](AutomationsApi.md#unsubscribe_selected_workspace_automations) | **POST** /api/v1/actions/workspaces/{workspaceId}/automations/unsubscribe | Unsubscribe from selected automations in the workspace
[**unsubscribe_workspace_automations**](AutomationsApi.md#unsubscribe_workspace_automations) | **DELETE** /api/v1/actions/workspaces/{workspaceId}/automations/unsubscribe | Unsubscribe from all automations in the workspace
[**update_entity_automations**](AutomationsApi.md#update_entity_automations) | **PUT** /api/v1/entities/workspaces/{workspaceId}/automations/{objectId} | Put an Automation


# **create_entity_automations**
> JsonApiAutomationOutDocument create_entity_automations(workspace_id, json_api_automation_in_document)

Post Automations

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import automations_api
from gooddata_api_client.model.json_api_automation_in_document import JsonApiAutomationInDocument
from gooddata_api_client.model.json_api_automation_out_document import JsonApiAutomationOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_automation_in_document = JsonApiAutomationInDocument(
        data=JsonApiAutomationIn(
            attributes=JsonApiAutomationInAttributes(
                alert=JsonApiAutomationInAttributesAlert(
                    condition=AlertCondition(),
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
                are_relations_valid=True,
                dashboard_tabular_exports=[
                    JsonApiAutomationInAttributesDashboardTabularExportsInner(
                        request_payload=DashboardTabularExportRequestV2(
                            dashboard_filters_override=[
                                DashboardFilter(),
                            ],
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            file_name="result",
                            format="XLSX",
                            settings=DashboardExportSettings(
                                export_info=True,
                                merge_headers=True,
                                page_orientation="PORTRAIT",
                                page_size="A4",
                            ),
                            widget_ids=[
                                "widget_ids_example",
                            ],
                        ),
                    ),
                ],
                description="description_example",
                details={},
                evaluation_mode="SHARED",
                external_recipients=[
                    JsonApiAutomationInAttributesExternalRecipientsInner(
                        email="email_example",
                    ),
                ],
                image_exports=[
                    JsonApiAutomationInAttributesImageExportsInner(
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
                metadata=JsonApiAutomationInAttributesMetadata(),
                raw_exports=[
                    JsonApiAutomationInAttributesRawExportsInner(
                        request_payload=RawExportAutomationRequest(
                            custom_override=RawCustomOverride(
                                labels={
                                    "key": RawCustomLabel(
                                        title="title_example",
                                    ),
                                },
                                metrics={
                                    "key": RawCustomMetric(
                                        title="title_example",
                                    ),
                                },
                            ),
                            execution=AFM(
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
                            execution_settings=ExecutionSettings(
                                data_sampling_percentage=0,
                                timestamp=dateutil_parser('1970-01-01T00:00:00.00Z'),
                            ),
                            file_name="result",
                            format="CSV",
                            metadata=JsonNode(),
                        ),
                    ),
                ],
                schedule=JsonApiAutomationInAttributesSchedule(
                    cron="0 */30 9-17 ? * MON-FRI",
                    first_run=dateutil_parser('2025-01-01T12:00:00Z'),
                    timezone="Europe/Prague",
                ),
                slides_exports=[
                    JsonApiAutomationInAttributesSlidesExportsInner(
                        request_payload=SlidesExportRequest(
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            file_name="filename",
                            format="PDF",
                            metadata=JsonNode(),
                            template_id="template_id_example",
                            visualization_ids=[
                                "visualization_ids_example",
                            ],
                            widget_ids=[
                                "widget_ids_example",
                            ],
                        ),
                    ),
                ],
                state="ACTIVE",
                tabular_exports=[
                    JsonApiAutomationInAttributesTabularExportsInner(
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
                                export_info=True,
                                merge_headers=True,
                                page_orientation="PORTRAIT",
                                page_size="A4",
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
                    "tags_example",
                ],
                title="title_example",
                visual_exports=[
                    JsonApiAutomationInAttributesVisualExportsInner(
                        request_payload=VisualExportRequest(
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            file_name="filename",
                            metadata={},
                        ),
                    ),
                ],
            ),
            id="id1",
            relationships=JsonApiAutomationInRelationships(
                analytical_dashboard=JsonApiAutomationInRelationshipsAnalyticalDashboard(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                export_definitions=JsonApiAutomationInRelationshipsExportDefinitions(
                    data=JsonApiExportDefinitionToManyLinkage([
                        JsonApiExportDefinitionLinkage(
                            id="id_example",
                            type="exportDefinition",
                        ),
                    ]),
                ),
                notification_channel=JsonApiAutomationInRelationshipsNotificationChannel(
                    data=JsonApiNotificationChannelToOneLinkage(None),
                ),
                recipients=JsonApiAutomationInRelationshipsRecipients(
                    data=JsonApiUserToManyLinkage([
                        JsonApiUserLinkage(
                            id="id_example",
                            type="user",
                        ),
                    ]),
                ),
            ),
            type="automation",
        ),
    ) # JsonApiAutomationInDocument | 
    include = [
        "notificationChannel,analyticalDashboard,createdBy,modifiedBy,exportDefinitions,recipients,automationResults",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Automations
        api_response = api_instance.create_entity_automations(workspace_id, json_api_automation_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->create_entity_automations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Automations
        api_response = api_instance.create_entity_automations(workspace_id, json_api_automation_in_document, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->create_entity_automations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_automation_in_document** | [**JsonApiAutomationInDocument**](JsonApiAutomationInDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiAutomationOutDocument**](JsonApiAutomationOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_automations**
> delete_entity_automations(workspace_id, object_id)

Delete an Automation

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import automations_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "title==someString;description==someString;notificationChannel.id==321;analyticalDashboard.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete an Automation
        api_instance.delete_entity_automations(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->delete_entity_automations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete an Automation
        api_instance.delete_entity_automations(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->delete_entity_automations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_organization_automations**
> delete_organization_automations(organization_automation_management_bulk_request)

Delete selected automations across all workspaces

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import automations_api
from gooddata_api_client.model.organization_automation_management_bulk_request import OrganizationAutomationManagementBulkRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)
    organization_automation_management_bulk_request = OrganizationAutomationManagementBulkRequest(
        automations=[
            OrganizationAutomationIdentifier(
                id="id_example",
                workspace_id="workspace_id_example",
            ),
        ],
    ) # OrganizationAutomationManagementBulkRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Delete selected automations across all workspaces
        api_instance.delete_organization_automations(organization_automation_management_bulk_request)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->delete_organization_automations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_automation_management_bulk_request** | [**OrganizationAutomationManagementBulkRequest**](OrganizationAutomationManagementBulkRequest.md)|  |

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
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_workspace_automations**
> delete_workspace_automations(workspace_id, workspace_automation_management_bulk_request)

Delete selected automations in the workspace

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import automations_api
from gooddata_api_client.model.workspace_automation_management_bulk_request import WorkspaceAutomationManagementBulkRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    workspace_automation_management_bulk_request = WorkspaceAutomationManagementBulkRequest(
        automations=[
            WorkspaceAutomationIdentifier(
                id="id_example",
            ),
        ],
    ) # WorkspaceAutomationManagementBulkRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Delete selected automations in the workspace
        api_instance.delete_workspace_automations(workspace_id, workspace_automation_management_bulk_request)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->delete_workspace_automations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **workspace_automation_management_bulk_request** | [**WorkspaceAutomationManagementBulkRequest**](WorkspaceAutomationManagementBulkRequest.md)|  |

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
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_automations_workspace_automations**
> JsonApiWorkspaceAutomationOutList get_all_automations_workspace_automations()

Get all Automations across all Workspaces

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import automations_api
from gooddata_api_client.model.json_api_workspace_automation_out_list import JsonApiWorkspaceAutomationOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)
    filter = "title==someString;description==someString;workspace.id==321;notificationChannel.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "workspace,notificationChannel,analyticalDashboard,createdBy,modifiedBy,exportDefinitions,recipients,automationResults",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = [
        "metaInclude=page,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Automations across all Workspaces
        api_response = api_instance.get_all_automations_workspace_automations(filter=filter, include=include, page=page, size=size, sort=sort, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->get_all_automations_workspace_automations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiWorkspaceAutomationOutList**](JsonApiWorkspaceAutomationOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_automations**
> JsonApiAutomationOutList get_all_entities_automations(workspace_id)

Get all Automations

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import automations_api
from gooddata_api_client.model.json_api_automation_out_list import JsonApiAutomationOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "title==someString;description==someString;notificationChannel.id==321;analyticalDashboard.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "notificationChannel,analyticalDashboard,createdBy,modifiedBy,exportDefinitions,recipients,automationResults",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,page,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get all Automations
        api_response = api_instance.get_all_entities_automations(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->get_all_entities_automations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Automations
        api_response = api_instance.get_all_entities_automations(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->get_all_entities_automations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiAutomationOutList**](JsonApiAutomationOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_automations**
> [DeclarativeAutomation] get_automations(workspace_id)

Get automations

Retrieve automations for the specific workspace

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import automations_api
from gooddata_api_client.model.declarative_automation import DeclarativeAutomation
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    exclude = [
        "ACTIVITY_INFO",
    ] # [str] |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get automations
        api_response = api_instance.get_automations(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->get_automations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get automations
        api_response = api_instance.get_automations(workspace_id, exclude=exclude)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->get_automations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **exclude** | **[str]**|  | [optional]

### Return type

[**[DeclarativeAutomation]**](DeclarativeAutomation.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved automations. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_automations**
> JsonApiAutomationOutDocument get_entity_automations(workspace_id, object_id)

Get an Automation

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import automations_api
from gooddata_api_client.model.json_api_automation_out_document import JsonApiAutomationOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "title==someString;description==someString;notificationChannel.id==321;analyticalDashboard.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "notificationChannel,analyticalDashboard,createdBy,modifiedBy,exportDefinitions,recipients,automationResults",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get an Automation
        api_response = api_instance.get_entity_automations(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->get_entity_automations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get an Automation
        api_response = api_instance.get_entity_automations(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->get_entity_automations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiAutomationOutDocument**](JsonApiAutomationOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_automations**
> JsonApiAutomationOutDocument patch_entity_automations(workspace_id, object_id, json_api_automation_patch_document)

Patch an Automation

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import automations_api
from gooddata_api_client.model.json_api_automation_out_document import JsonApiAutomationOutDocument
from gooddata_api_client.model.json_api_automation_patch_document import JsonApiAutomationPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_automation_patch_document = JsonApiAutomationPatchDocument(
        data=JsonApiAutomationPatch(
            attributes=JsonApiAutomationInAttributes(
                alert=JsonApiAutomationInAttributesAlert(
                    condition=AlertCondition(),
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
                are_relations_valid=True,
                dashboard_tabular_exports=[
                    JsonApiAutomationInAttributesDashboardTabularExportsInner(
                        request_payload=DashboardTabularExportRequestV2(
                            dashboard_filters_override=[
                                DashboardFilter(),
                            ],
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            file_name="result",
                            format="XLSX",
                            settings=DashboardExportSettings(
                                export_info=True,
                                merge_headers=True,
                                page_orientation="PORTRAIT",
                                page_size="A4",
                            ),
                            widget_ids=[
                                "widget_ids_example",
                            ],
                        ),
                    ),
                ],
                description="description_example",
                details={},
                evaluation_mode="SHARED",
                external_recipients=[
                    JsonApiAutomationInAttributesExternalRecipientsInner(
                        email="email_example",
                    ),
                ],
                image_exports=[
                    JsonApiAutomationInAttributesImageExportsInner(
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
                metadata=JsonApiAutomationInAttributesMetadata(),
                raw_exports=[
                    JsonApiAutomationInAttributesRawExportsInner(
                        request_payload=RawExportAutomationRequest(
                            custom_override=RawCustomOverride(
                                labels={
                                    "key": RawCustomLabel(
                                        title="title_example",
                                    ),
                                },
                                metrics={
                                    "key": RawCustomMetric(
                                        title="title_example",
                                    ),
                                },
                            ),
                            execution=AFM(
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
                            execution_settings=ExecutionSettings(
                                data_sampling_percentage=0,
                                timestamp=dateutil_parser('1970-01-01T00:00:00.00Z'),
                            ),
                            file_name="result",
                            format="CSV",
                            metadata=JsonNode(),
                        ),
                    ),
                ],
                schedule=JsonApiAutomationInAttributesSchedule(
                    cron="0 */30 9-17 ? * MON-FRI",
                    first_run=dateutil_parser('2025-01-01T12:00:00Z'),
                    timezone="Europe/Prague",
                ),
                slides_exports=[
                    JsonApiAutomationInAttributesSlidesExportsInner(
                        request_payload=SlidesExportRequest(
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            file_name="filename",
                            format="PDF",
                            metadata=JsonNode(),
                            template_id="template_id_example",
                            visualization_ids=[
                                "visualization_ids_example",
                            ],
                            widget_ids=[
                                "widget_ids_example",
                            ],
                        ),
                    ),
                ],
                state="ACTIVE",
                tabular_exports=[
                    JsonApiAutomationInAttributesTabularExportsInner(
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
                                export_info=True,
                                merge_headers=True,
                                page_orientation="PORTRAIT",
                                page_size="A4",
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
                    "tags_example",
                ],
                title="title_example",
                visual_exports=[
                    JsonApiAutomationInAttributesVisualExportsInner(
                        request_payload=VisualExportRequest(
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            file_name="filename",
                            metadata={},
                        ),
                    ),
                ],
            ),
            id="id1",
            relationships=JsonApiAutomationInRelationships(
                analytical_dashboard=JsonApiAutomationInRelationshipsAnalyticalDashboard(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                export_definitions=JsonApiAutomationInRelationshipsExportDefinitions(
                    data=JsonApiExportDefinitionToManyLinkage([
                        JsonApiExportDefinitionLinkage(
                            id="id_example",
                            type="exportDefinition",
                        ),
                    ]),
                ),
                notification_channel=JsonApiAutomationInRelationshipsNotificationChannel(
                    data=JsonApiNotificationChannelToOneLinkage(None),
                ),
                recipients=JsonApiAutomationInRelationshipsRecipients(
                    data=JsonApiUserToManyLinkage([
                        JsonApiUserLinkage(
                            id="id_example",
                            type="user",
                        ),
                    ]),
                ),
            ),
            type="automation",
        ),
    ) # JsonApiAutomationPatchDocument | 
    filter = "title==someString;description==someString;notificationChannel.id==321;analyticalDashboard.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "notificationChannel,analyticalDashboard,createdBy,modifiedBy,exportDefinitions,recipients,automationResults",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch an Automation
        api_response = api_instance.patch_entity_automations(workspace_id, object_id, json_api_automation_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->patch_entity_automations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch an Automation
        api_response = api_instance.patch_entity_automations(workspace_id, object_id, json_api_automation_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->patch_entity_automations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_automation_patch_document** | [**JsonApiAutomationPatchDocument**](JsonApiAutomationPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiAutomationOutDocument**](JsonApiAutomationOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pause_organization_automations**
> pause_organization_automations(organization_automation_management_bulk_request)

Pause selected automations across all workspaces

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import automations_api
from gooddata_api_client.model.organization_automation_management_bulk_request import OrganizationAutomationManagementBulkRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)
    organization_automation_management_bulk_request = OrganizationAutomationManagementBulkRequest(
        automations=[
            OrganizationAutomationIdentifier(
                id="id_example",
                workspace_id="workspace_id_example",
            ),
        ],
    ) # OrganizationAutomationManagementBulkRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Pause selected automations across all workspaces
        api_instance.pause_organization_automations(organization_automation_management_bulk_request)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->pause_organization_automations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_automation_management_bulk_request** | [**OrganizationAutomationManagementBulkRequest**](OrganizationAutomationManagementBulkRequest.md)|  |

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
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pause_workspace_automations**
> pause_workspace_automations(workspace_id, workspace_automation_management_bulk_request)

Pause selected automations in the workspace

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import automations_api
from gooddata_api_client.model.workspace_automation_management_bulk_request import WorkspaceAutomationManagementBulkRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    workspace_automation_management_bulk_request = WorkspaceAutomationManagementBulkRequest(
        automations=[
            WorkspaceAutomationIdentifier(
                id="id_example",
            ),
        ],
    ) # WorkspaceAutomationManagementBulkRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Pause selected automations in the workspace
        api_instance.pause_workspace_automations(workspace_id, workspace_automation_management_bulk_request)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->pause_workspace_automations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **workspace_automation_management_bulk_request** | [**WorkspaceAutomationManagementBulkRequest**](WorkspaceAutomationManagementBulkRequest.md)|  |

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
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_automations**
> set_automations(workspace_id, declarative_automation)

Set automations

Set automations for the specific workspace.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import automations_api
from gooddata_api_client.model.declarative_automation import DeclarativeAutomation
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    declarative_automation = [
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
            dashboard_tabular_exports=[
                AutomationDashboardTabularExport(
                    request_payload=DashboardTabularExportRequestV2(
                        dashboard_filters_override=[
                            DashboardFilter(),
                        ],
                        dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                        file_name="result",
                        format="XLSX",
                        settings=DashboardExportSettings(
                            export_info=True,
                            merge_headers=True,
                            page_orientation="PORTRAIT",
                            page_size="A4",
                        ),
                        widget_ids=[
                            "widget_ids_example",
                        ],
                    ),
                ),
            ],
            description="description_example",
            details={
                "key": "key_example",
            },
            evaluation_mode="PER_RECIPIENT",
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
            metadata=AutomationMetadata(),
            modified_at="2023-07-20 12:30",
            modified_by=DeclarativeUserIdentifier(
                id="employee123",
                type="user",
            ),
            notification_channel=DeclarativeNotificationChannelIdentifier(
                id="webhook123",
                type="notificationChannel",
            ),
            raw_exports=[
                AutomationRawExport(
                    request_payload=RawExportAutomationRequest(
                        custom_override=RawCustomOverride(
                            labels={
                                "key": RawCustomLabel(
                                    title="title_example",
                                ),
                            },
                            metrics={
                                "key": RawCustomMetric(
                                    title="title_example",
                                ),
                            },
                        ),
                        execution=AFM(
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
                        execution_settings=ExecutionSettings(
                            data_sampling_percentage=0,
                            timestamp=dateutil_parser('1970-01-01T00:00:00.00Z'),
                        ),
                        file_name="result",
                        format="CSV",
                        metadata=JsonNode(),
                    ),
                ),
            ],
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
            slides_exports=[
                AutomationSlidesExport(
                    request_payload=SlidesExportRequest(
                        dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                        file_name="filename",
                        format="PDF",
                        metadata=JsonNode(),
                        template_id="template_id_example",
                        visualization_ids=[
                            "visualization_ids_example",
                        ],
                        widget_ids=[
                            "widget_ids_example",
                        ],
                    ),
                ),
            ],
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
                            export_info=True,
                            merge_headers=True,
                            page_orientation="PORTRAIT",
                            page_size="A4",
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
    ] # [DeclarativeAutomation] | 

    # example passing only required values which don't have defaults set
    try:
        # Set automations
        api_instance.set_automations(workspace_id, declarative_automation)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->set_automations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **declarative_automation** | [**[DeclarativeAutomation]**](DeclarativeAutomation.md)|  |

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
**204** | Automations successfully set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **trigger_automation**
> trigger_automation(workspace_id, trigger_automation_request)

Trigger automation.

Trigger the automation in the request.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import automations_api
from gooddata_api_client.model.trigger_automation_request import TriggerAutomationRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    trigger_automation_request = TriggerAutomationRequest(
        automation=AdHocAutomation(
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
            dashboard_tabular_exports=[
                AutomationDashboardTabularExport(
                    request_payload=DashboardTabularExportRequestV2(
                        dashboard_filters_override=[
                            DashboardFilter(),
                        ],
                        dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                        file_name="result",
                        format="XLSX",
                        settings=DashboardExportSettings(
                            export_info=True,
                            merge_headers=True,
                            page_orientation="PORTRAIT",
                            page_size="A4",
                        ),
                        widget_ids=[
                            "widget_ids_example",
                        ],
                    ),
                ),
            ],
            description="description_example",
            details={
                "key": "key_example",
            },
            external_recipients=[
                AutomationExternalRecipient(
                    email="email_example",
                ),
            ],
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
            metadata=AutomationMetadata(),
            notification_channel=DeclarativeNotificationChannelIdentifier(
                id="webhook123",
                type="notificationChannel",
            ),
            raw_exports=[
                AutomationRawExport(
                    request_payload=RawExportAutomationRequest(
                        custom_override=RawCustomOverride(
                            labels={
                                "key": RawCustomLabel(
                                    title="title_example",
                                ),
                            },
                            metrics={
                                "key": RawCustomMetric(
                                    title="title_example",
                                ),
                            },
                        ),
                        execution=AFM(
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
                        execution_settings=ExecutionSettings(
                            data_sampling_percentage=0,
                            timestamp=dateutil_parser('1970-01-01T00:00:00.00Z'),
                        ),
                        file_name="result",
                        format="CSV",
                        metadata=JsonNode(),
                    ),
                ),
            ],
            recipients=[
                DeclarativeUserIdentifier(
                    id="employee123",
                    type="user",
                ),
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
                            "visualization_ids_example",
                        ],
                        widget_ids=[
                            "widget_ids_example",
                        ],
                    ),
                ),
            ],
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
                            export_info=True,
                            merge_headers=True,
                            page_orientation="PORTRAIT",
                            page_size="A4",
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
            tags=["Revenue","Sales"],
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
    ) # TriggerAutomationRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Trigger automation.
        api_instance.trigger_automation(workspace_id, trigger_automation_request)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->trigger_automation: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **trigger_automation_request** | [**TriggerAutomationRequest**](TriggerAutomationRequest.md)|  |

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
**204** | The automation is successfully triggered. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **trigger_existing_automation**
> trigger_existing_automation(workspace_id, automation_id)

Trigger existing automation.

Trigger the existing automation to execute immediately.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import automations_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    automation_id = "automationId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Trigger existing automation.
        api_instance.trigger_existing_automation(workspace_id, automation_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->trigger_existing_automation: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **automation_id** | **str**|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | The automation is successfully triggered. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unpause_organization_automations**
> unpause_organization_automations(organization_automation_management_bulk_request)

Unpause selected automations across all workspaces

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import automations_api
from gooddata_api_client.model.organization_automation_management_bulk_request import OrganizationAutomationManagementBulkRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)
    organization_automation_management_bulk_request = OrganizationAutomationManagementBulkRequest(
        automations=[
            OrganizationAutomationIdentifier(
                id="id_example",
                workspace_id="workspace_id_example",
            ),
        ],
    ) # OrganizationAutomationManagementBulkRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Unpause selected automations across all workspaces
        api_instance.unpause_organization_automations(organization_automation_management_bulk_request)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->unpause_organization_automations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_automation_management_bulk_request** | [**OrganizationAutomationManagementBulkRequest**](OrganizationAutomationManagementBulkRequest.md)|  |

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
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unpause_workspace_automations**
> unpause_workspace_automations(workspace_id, workspace_automation_management_bulk_request)

Unpause selected automations in the workspace

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import automations_api
from gooddata_api_client.model.workspace_automation_management_bulk_request import WorkspaceAutomationManagementBulkRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    workspace_automation_management_bulk_request = WorkspaceAutomationManagementBulkRequest(
        automations=[
            WorkspaceAutomationIdentifier(
                id="id_example",
            ),
        ],
    ) # WorkspaceAutomationManagementBulkRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Unpause selected automations in the workspace
        api_instance.unpause_workspace_automations(workspace_id, workspace_automation_management_bulk_request)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->unpause_workspace_automations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **workspace_automation_management_bulk_request** | [**WorkspaceAutomationManagementBulkRequest**](WorkspaceAutomationManagementBulkRequest.md)|  |

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
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unsubscribe_all_automations**
> unsubscribe_all_automations()

Unsubscribe from all automations in all workspaces

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import automations_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Unsubscribe from all automations in all workspaces
        api_instance.unsubscribe_all_automations()
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->unsubscribe_all_automations: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unsubscribe_automation**
> unsubscribe_automation(workspace_id, automation_id)

Unsubscribe from an automation

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import automations_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    automation_id = "automationId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Unsubscribe from an automation
        api_instance.unsubscribe_automation(workspace_id, automation_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->unsubscribe_automation: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **automation_id** | **str**|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unsubscribe_organization_automations**
> unsubscribe_organization_automations(organization_automation_management_bulk_request)

Unsubscribe from selected automations across all workspaces

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import automations_api
from gooddata_api_client.model.organization_automation_management_bulk_request import OrganizationAutomationManagementBulkRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)
    organization_automation_management_bulk_request = OrganizationAutomationManagementBulkRequest(
        automations=[
            OrganizationAutomationIdentifier(
                id="id_example",
                workspace_id="workspace_id_example",
            ),
        ],
    ) # OrganizationAutomationManagementBulkRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Unsubscribe from selected automations across all workspaces
        api_instance.unsubscribe_organization_automations(organization_automation_management_bulk_request)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->unsubscribe_organization_automations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_automation_management_bulk_request** | [**OrganizationAutomationManagementBulkRequest**](OrganizationAutomationManagementBulkRequest.md)|  |

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
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unsubscribe_selected_workspace_automations**
> unsubscribe_selected_workspace_automations(workspace_id, workspace_automation_management_bulk_request)

Unsubscribe from selected automations in the workspace

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import automations_api
from gooddata_api_client.model.workspace_automation_management_bulk_request import WorkspaceAutomationManagementBulkRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    workspace_automation_management_bulk_request = WorkspaceAutomationManagementBulkRequest(
        automations=[
            WorkspaceAutomationIdentifier(
                id="id_example",
            ),
        ],
    ) # WorkspaceAutomationManagementBulkRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Unsubscribe from selected automations in the workspace
        api_instance.unsubscribe_selected_workspace_automations(workspace_id, workspace_automation_management_bulk_request)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->unsubscribe_selected_workspace_automations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **workspace_automation_management_bulk_request** | [**WorkspaceAutomationManagementBulkRequest**](WorkspaceAutomationManagementBulkRequest.md)|  |

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
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unsubscribe_workspace_automations**
> unsubscribe_workspace_automations(workspace_id)

Unsubscribe from all automations in the workspace

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import automations_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Unsubscribe from all automations in the workspace
        api_instance.unsubscribe_workspace_automations(workspace_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->unsubscribe_workspace_automations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_automations**
> JsonApiAutomationOutDocument update_entity_automations(workspace_id, object_id, json_api_automation_in_document)

Put an Automation

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import automations_api
from gooddata_api_client.model.json_api_automation_in_document import JsonApiAutomationInDocument
from gooddata_api_client.model.json_api_automation_out_document import JsonApiAutomationOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = automations_api.AutomationsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_automation_in_document = JsonApiAutomationInDocument(
        data=JsonApiAutomationIn(
            attributes=JsonApiAutomationInAttributes(
                alert=JsonApiAutomationInAttributesAlert(
                    condition=AlertCondition(),
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
                are_relations_valid=True,
                dashboard_tabular_exports=[
                    JsonApiAutomationInAttributesDashboardTabularExportsInner(
                        request_payload=DashboardTabularExportRequestV2(
                            dashboard_filters_override=[
                                DashboardFilter(),
                            ],
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            file_name="result",
                            format="XLSX",
                            settings=DashboardExportSettings(
                                export_info=True,
                                merge_headers=True,
                                page_orientation="PORTRAIT",
                                page_size="A4",
                            ),
                            widget_ids=[
                                "widget_ids_example",
                            ],
                        ),
                    ),
                ],
                description="description_example",
                details={},
                evaluation_mode="SHARED",
                external_recipients=[
                    JsonApiAutomationInAttributesExternalRecipientsInner(
                        email="email_example",
                    ),
                ],
                image_exports=[
                    JsonApiAutomationInAttributesImageExportsInner(
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
                metadata=JsonApiAutomationInAttributesMetadata(),
                raw_exports=[
                    JsonApiAutomationInAttributesRawExportsInner(
                        request_payload=RawExportAutomationRequest(
                            custom_override=RawCustomOverride(
                                labels={
                                    "key": RawCustomLabel(
                                        title="title_example",
                                    ),
                                },
                                metrics={
                                    "key": RawCustomMetric(
                                        title="title_example",
                                    ),
                                },
                            ),
                            execution=AFM(
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
                            execution_settings=ExecutionSettings(
                                data_sampling_percentage=0,
                                timestamp=dateutil_parser('1970-01-01T00:00:00.00Z'),
                            ),
                            file_name="result",
                            format="CSV",
                            metadata=JsonNode(),
                        ),
                    ),
                ],
                schedule=JsonApiAutomationInAttributesSchedule(
                    cron="0 */30 9-17 ? * MON-FRI",
                    first_run=dateutil_parser('2025-01-01T12:00:00Z'),
                    timezone="Europe/Prague",
                ),
                slides_exports=[
                    JsonApiAutomationInAttributesSlidesExportsInner(
                        request_payload=SlidesExportRequest(
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            file_name="filename",
                            format="PDF",
                            metadata=JsonNode(),
                            template_id="template_id_example",
                            visualization_ids=[
                                "visualization_ids_example",
                            ],
                            widget_ids=[
                                "widget_ids_example",
                            ],
                        ),
                    ),
                ],
                state="ACTIVE",
                tabular_exports=[
                    JsonApiAutomationInAttributesTabularExportsInner(
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
                                export_info=True,
                                merge_headers=True,
                                page_orientation="PORTRAIT",
                                page_size="A4",
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
                    "tags_example",
                ],
                title="title_example",
                visual_exports=[
                    JsonApiAutomationInAttributesVisualExportsInner(
                        request_payload=VisualExportRequest(
                            dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
                            file_name="filename",
                            metadata={},
                        ),
                    ),
                ],
            ),
            id="id1",
            relationships=JsonApiAutomationInRelationships(
                analytical_dashboard=JsonApiAutomationInRelationshipsAnalyticalDashboard(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                export_definitions=JsonApiAutomationInRelationshipsExportDefinitions(
                    data=JsonApiExportDefinitionToManyLinkage([
                        JsonApiExportDefinitionLinkage(
                            id="id_example",
                            type="exportDefinition",
                        ),
                    ]),
                ),
                notification_channel=JsonApiAutomationInRelationshipsNotificationChannel(
                    data=JsonApiNotificationChannelToOneLinkage(None),
                ),
                recipients=JsonApiAutomationInRelationshipsRecipients(
                    data=JsonApiUserToManyLinkage([
                        JsonApiUserLinkage(
                            id="id_example",
                            type="user",
                        ),
                    ]),
                ),
            ),
            type="automation",
        ),
    ) # JsonApiAutomationInDocument | 
    filter = "title==someString;description==someString;notificationChannel.id==321;analyticalDashboard.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "notificationChannel,analyticalDashboard,createdBy,modifiedBy,exportDefinitions,recipients,automationResults",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put an Automation
        api_response = api_instance.update_entity_automations(workspace_id, object_id, json_api_automation_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->update_entity_automations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put an Automation
        api_response = api_instance.update_entity_automations(workspace_id, object_id, json_api_automation_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationsApi->update_entity_automations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_automation_in_document** | [**JsonApiAutomationInDocument**](JsonApiAutomationInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiAutomationOutDocument**](JsonApiAutomationOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


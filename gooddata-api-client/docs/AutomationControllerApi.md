# gooddata_api_client.AutomationControllerApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_automations**](AutomationControllerApi.md#create_entity_automations) | **POST** /api/v1/entities/workspaces/{workspaceId}/automations | Post Automations
[**delete_entity_automations**](AutomationControllerApi.md#delete_entity_automations) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/automations/{objectId} | Delete an Automation
[**get_all_entities_automations**](AutomationControllerApi.md#get_all_entities_automations) | **GET** /api/v1/entities/workspaces/{workspaceId}/automations | Get all Automations
[**get_entity_automations**](AutomationControllerApi.md#get_entity_automations) | **GET** /api/v1/entities/workspaces/{workspaceId}/automations/{objectId} | Get an Automation
[**patch_entity_automations**](AutomationControllerApi.md#patch_entity_automations) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/automations/{objectId} | Patch an Automation
[**search_entities_automations**](AutomationControllerApi.md#search_entities_automations) | **POST** /api/v1/entities/workspaces/{workspaceId}/automations/search | The search endpoint (beta)
[**update_entity_automations**](AutomationControllerApi.md#update_entity_automations) | **PUT** /api/v1/entities/workspaces/{workspaceId}/automations/{objectId} | Put an Automation


# **create_entity_automations**
> JsonApiAutomationOutDocument create_entity_automations(workspace_id, json_api_automation_in_document)

Post Automations

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import automation_controller_api
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
    api_instance = automation_controller_api.AutomationControllerApi(api_client)
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
                    interval="DAY",
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
                            dashboard_tabs_filters_overrides={
                                "key": [
                                    DashboardFilter(),
                                ],
                            },
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
                            delimiter="-",
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
                                measure_definition_overrides=[
                                    MetricDefinitionOverride(
                                        definition=InlineMeasureDefinition(
                                            inline=InlineMeasureDefinitionInline(
                                                maql="maql_example",
                                            ),
                                        ),
                                        item=AfmObjectIdentifierCore(
                                            identifier=AfmObjectIdentifierCoreIdentifier(
                                                id="sample_item.price",
                                                type="attribute",
                                            ),
                                        ),
                                    ),
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
                                delimiter="-",
                                export_info=True,
                                grand_totals_position="pinnedBottom",
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
        print("Exception when calling AutomationControllerApi->create_entity_automations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Automations
        api_response = api_instance.create_entity_automations(workspace_id, json_api_automation_in_document, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationControllerApi->create_entity_automations: %s\n" % e)
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

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
 - **Accept**: application/json, application/vnd.gooddata.api+json


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
from gooddata_api_client.api import automation_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = automation_controller_api.AutomationControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "title==someString;description==someString;notificationChannel.id==321;analyticalDashboard.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete an Automation
        api_instance.delete_entity_automations(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationControllerApi->delete_entity_automations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete an Automation
        api_instance.delete_entity_automations(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationControllerApi->delete_entity_automations: %s\n" % e)
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

# **get_all_entities_automations**
> JsonApiAutomationOutList get_all_entities_automations(workspace_id)

Get all Automations

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import automation_controller_api
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
    api_instance = automation_controller_api.AutomationControllerApi(api_client)
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
        print("Exception when calling AutomationControllerApi->get_all_entities_automations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Automations
        api_response = api_instance.get_all_entities_automations(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationControllerApi->get_all_entities_automations: %s\n" % e)
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
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_automations**
> JsonApiAutomationOutDocument get_entity_automations(workspace_id, object_id)

Get an Automation

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import automation_controller_api
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
    api_instance = automation_controller_api.AutomationControllerApi(api_client)
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
        print("Exception when calling AutomationControllerApi->get_entity_automations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get an Automation
        api_response = api_instance.get_entity_automations(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationControllerApi->get_entity_automations: %s\n" % e)
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
 - **Accept**: application/json, application/vnd.gooddata.api+json


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
from gooddata_api_client.api import automation_controller_api
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
    api_instance = automation_controller_api.AutomationControllerApi(api_client)
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
                    interval="DAY",
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
                            dashboard_tabs_filters_overrides={
                                "key": [
                                    DashboardFilter(),
                                ],
                            },
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
                            delimiter="-",
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
                                measure_definition_overrides=[
                                    MetricDefinitionOverride(
                                        definition=InlineMeasureDefinition(
                                            inline=InlineMeasureDefinitionInline(
                                                maql="maql_example",
                                            ),
                                        ),
                                        item=AfmObjectIdentifierCore(
                                            identifier=AfmObjectIdentifierCoreIdentifier(
                                                id="sample_item.price",
                                                type="attribute",
                                            ),
                                        ),
                                    ),
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
                                delimiter="-",
                                export_info=True,
                                grand_totals_position="pinnedBottom",
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
        print("Exception when calling AutomationControllerApi->patch_entity_automations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch an Automation
        api_response = api_instance.patch_entity_automations(workspace_id, object_id, json_api_automation_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationControllerApi->patch_entity_automations: %s\n" % e)
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

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search_entities_automations**
> JsonApiAutomationOutList search_entities_automations(workspace_id, entity_search_body)

The search endpoint (beta)

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import automation_controller_api
from gooddata_api_client.model.json_api_automation_out_list import JsonApiAutomationOutList
from gooddata_api_client.model.entity_search_body import EntitySearchBody
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = automation_controller_api.AutomationControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    entity_search_body = EntitySearchBody(
        filter="filter_example",
        include=[
            "include_example",
        ],
        meta_include=[
            "meta_include_example",
        ],
        page=EntitySearchPage(
            index=0,
            size=100,
        ),
        sort=[
            EntitySearchSort(
                direction="ASC",
                _property="_property_example",
            ),
        ],
    ) # EntitySearchBody | Search request body with filter, pagination, and sorting options
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # The search endpoint (beta)
        api_response = api_instance.search_entities_automations(workspace_id, entity_search_body)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationControllerApi->search_entities_automations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # The search endpoint (beta)
        api_response = api_instance.search_entities_automations(workspace_id, entity_search_body, origin=origin, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationControllerApi->search_entities_automations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **entity_search_body** | [**EntitySearchBody**](EntitySearchBody.md)| Search request body with filter, pagination, and sorting options |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**JsonApiAutomationOutList**](JsonApiAutomationOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_automations**
> JsonApiAutomationOutDocument update_entity_automations(workspace_id, object_id, json_api_automation_in_document)

Put an Automation

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import automation_controller_api
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
    api_instance = automation_controller_api.AutomationControllerApi(api_client)
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
                    interval="DAY",
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
                            dashboard_tabs_filters_overrides={
                                "key": [
                                    DashboardFilter(),
                                ],
                            },
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
                            delimiter="-",
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
                                measure_definition_overrides=[
                                    MetricDefinitionOverride(
                                        definition=InlineMeasureDefinition(
                                            inline=InlineMeasureDefinitionInline(
                                                maql="maql_example",
                                            ),
                                        ),
                                        item=AfmObjectIdentifierCore(
                                            identifier=AfmObjectIdentifierCoreIdentifier(
                                                id="sample_item.price",
                                                type="attribute",
                                            ),
                                        ),
                                    ),
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
                                delimiter="-",
                                export_info=True,
                                grand_totals_position="pinnedBottom",
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
        print("Exception when calling AutomationControllerApi->update_entity_automations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put an Automation
        api_response = api_instance.update_entity_automations(workspace_id, object_id, json_api_automation_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AutomationControllerApi->update_entity_automations: %s\n" % e)
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

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


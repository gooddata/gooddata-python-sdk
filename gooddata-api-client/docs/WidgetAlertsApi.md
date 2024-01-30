# gooddata_api_client.WidgetAlertsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_widget_alerts**](WidgetAlertsApi.md#create_entity_widget_alerts) | **POST** /api/v1/entities/workspaces/{workspaceId}/widgetAlerts | Post Widget Alerts
[**delete_entity_widget_alerts**](WidgetAlertsApi.md#delete_entity_widget_alerts) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/widgetAlerts/{objectId} | Delete a Widget Alert
[**get_all_entities_widget_alerts**](WidgetAlertsApi.md#get_all_entities_widget_alerts) | **GET** /api/v1/entities/workspaces/{workspaceId}/widgetAlerts | Get all Widget Alerts
[**get_entity_widget_alerts**](WidgetAlertsApi.md#get_entity_widget_alerts) | **GET** /api/v1/entities/workspaces/{workspaceId}/widgetAlerts/{objectId} | Get a Widget Alert
[**patch_entity_widget_alerts**](WidgetAlertsApi.md#patch_entity_widget_alerts) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/widgetAlerts/{objectId} | Patch a Widget Alert
[**update_entity_widget_alerts**](WidgetAlertsApi.md#update_entity_widget_alerts) | **PUT** /api/v1/entities/workspaces/{workspaceId}/widgetAlerts/{objectId} | Put a Widget Alert


# **create_entity_widget_alerts**
> JsonApiWidgetAlertOutDocument create_entity_widget_alerts(workspace_id, json_api_widget_alert_in_document)

Post Widget Alerts

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import widget_alerts_api
from gooddata_api_client.model.json_api_widget_alert_in_document import JsonApiWidgetAlertInDocument
from gooddata_api_client.model.json_api_widget_alert_out_document import JsonApiWidgetAlertOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = widget_alerts_api.WidgetAlertsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_widget_alert_in_document = JsonApiWidgetAlertInDocument(
        data=JsonApiWidgetAlertIn(
            attributes=JsonApiWidgetAlertInAttributes(
                action_name="action_name_example",
                are_relations_valid=True,
                description="description_example",
                tags=[
                    "tags_example",
                ],
                threshold=3.14,
                title="title_example",
                when_triggered="when_triggered_example",
            ),
            id="id1",
            relationships=JsonApiWidgetAlertInRelationships(
                analytical_dashboard=JsonApiWidgetAlertInRelationshipsAnalyticalDashboard(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                filter_context=JsonApiWidgetAlertInRelationshipsFilterContext(
                    data=JsonApiFilterContextToOneLinkage(None),
                ),
                visualization_object=JsonApiWidgetAlertInRelationshipsVisualizationObject(
                    data=JsonApiVisualizationObjectToOneLinkage(None),
                ),
            ),
            type="widgetAlert",
        ),
    ) # JsonApiWidgetAlertInDocument | 
    include = [
        "include=visualizationObject,analyticalDashboard,filterContext,createdBy,modifiedBy",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Widget Alerts
        api_response = api_instance.create_entity_widget_alerts(workspace_id, json_api_widget_alert_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WidgetAlertsApi->create_entity_widget_alerts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Widget Alerts
        api_response = api_instance.create_entity_widget_alerts(workspace_id, json_api_widget_alert_in_document, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WidgetAlertsApi->create_entity_widget_alerts: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_widget_alert_in_document** | [**JsonApiWidgetAlertInDocument**](JsonApiWidgetAlertInDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiWidgetAlertOutDocument**](JsonApiWidgetAlertOutDocument.md)

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

# **delete_entity_widget_alerts**
> delete_entity_widget_alerts(workspace_id, object_id)

Delete a Widget Alert

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import widget_alerts_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = widget_alerts_api.WidgetAlertsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString;visualizationObject.id==321;analyticalDashboard.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Widget Alert
        api_instance.delete_entity_widget_alerts(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WidgetAlertsApi->delete_entity_widget_alerts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Widget Alert
        api_instance.delete_entity_widget_alerts(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WidgetAlertsApi->delete_entity_widget_alerts: %s\n" % e)
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

# **get_all_entities_widget_alerts**
> JsonApiWidgetAlertOutList get_all_entities_widget_alerts(workspace_id)

Get all Widget Alerts

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import widget_alerts_api
from gooddata_api_client.model.json_api_widget_alert_out_list import JsonApiWidgetAlertOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = widget_alerts_api.WidgetAlertsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "filter=title==someString;description==someString;visualizationObject.id==321;analyticalDashboard.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=visualizationObject,analyticalDashboard,filterContext,createdBy,modifiedBy",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get all Widget Alerts
        api_response = api_instance.get_all_entities_widget_alerts(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WidgetAlertsApi->get_all_entities_widget_alerts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Widget Alerts
        api_response = api_instance.get_all_entities_widget_alerts(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WidgetAlertsApi->get_all_entities_widget_alerts: %s\n" % e)
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

[**JsonApiWidgetAlertOutList**](JsonApiWidgetAlertOutList.md)

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

# **get_entity_widget_alerts**
> JsonApiWidgetAlertOutDocument get_entity_widget_alerts(workspace_id, object_id)

Get a Widget Alert

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import widget_alerts_api
from gooddata_api_client.model.json_api_widget_alert_out_document import JsonApiWidgetAlertOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = widget_alerts_api.WidgetAlertsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString;visualizationObject.id==321;analyticalDashboard.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=visualizationObject,analyticalDashboard,filterContext,createdBy,modifiedBy",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a Widget Alert
        api_response = api_instance.get_entity_widget_alerts(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WidgetAlertsApi->get_entity_widget_alerts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Widget Alert
        api_response = api_instance.get_entity_widget_alerts(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WidgetAlertsApi->get_entity_widget_alerts: %s\n" % e)
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

[**JsonApiWidgetAlertOutDocument**](JsonApiWidgetAlertOutDocument.md)

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

# **patch_entity_widget_alerts**
> JsonApiWidgetAlertOutDocument patch_entity_widget_alerts(workspace_id, object_id, json_api_widget_alert_patch_document)

Patch a Widget Alert

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import widget_alerts_api
from gooddata_api_client.model.json_api_widget_alert_out_document import JsonApiWidgetAlertOutDocument
from gooddata_api_client.model.json_api_widget_alert_patch_document import JsonApiWidgetAlertPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = widget_alerts_api.WidgetAlertsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_widget_alert_patch_document = JsonApiWidgetAlertPatchDocument(
        data=JsonApiWidgetAlertPatch(
            attributes=JsonApiWidgetAlertInAttributes(
                action_name="action_name_example",
                are_relations_valid=True,
                description="description_example",
                tags=[
                    "tags_example",
                ],
                threshold=3.14,
                title="title_example",
                when_triggered="when_triggered_example",
            ),
            id="id1",
            relationships=JsonApiWidgetAlertInRelationships(
                analytical_dashboard=JsonApiWidgetAlertInRelationshipsAnalyticalDashboard(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                filter_context=JsonApiWidgetAlertInRelationshipsFilterContext(
                    data=JsonApiFilterContextToOneLinkage(None),
                ),
                visualization_object=JsonApiWidgetAlertInRelationshipsVisualizationObject(
                    data=JsonApiVisualizationObjectToOneLinkage(None),
                ),
            ),
            type="widgetAlert",
        ),
    ) # JsonApiWidgetAlertPatchDocument | 
    filter = "filter=title==someString;description==someString;visualizationObject.id==321;analyticalDashboard.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=visualizationObject,analyticalDashboard,filterContext,createdBy,modifiedBy",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch a Widget Alert
        api_response = api_instance.patch_entity_widget_alerts(workspace_id, object_id, json_api_widget_alert_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WidgetAlertsApi->patch_entity_widget_alerts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Widget Alert
        api_response = api_instance.patch_entity_widget_alerts(workspace_id, object_id, json_api_widget_alert_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WidgetAlertsApi->patch_entity_widget_alerts: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_widget_alert_patch_document** | [**JsonApiWidgetAlertPatchDocument**](JsonApiWidgetAlertPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiWidgetAlertOutDocument**](JsonApiWidgetAlertOutDocument.md)

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

# **update_entity_widget_alerts**
> JsonApiWidgetAlertOutDocument update_entity_widget_alerts(workspace_id, object_id, json_api_widget_alert_in_document)

Put a Widget Alert

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import widget_alerts_api
from gooddata_api_client.model.json_api_widget_alert_in_document import JsonApiWidgetAlertInDocument
from gooddata_api_client.model.json_api_widget_alert_out_document import JsonApiWidgetAlertOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = widget_alerts_api.WidgetAlertsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_widget_alert_in_document = JsonApiWidgetAlertInDocument(
        data=JsonApiWidgetAlertIn(
            attributes=JsonApiWidgetAlertInAttributes(
                action_name="action_name_example",
                are_relations_valid=True,
                description="description_example",
                tags=[
                    "tags_example",
                ],
                threshold=3.14,
                title="title_example",
                when_triggered="when_triggered_example",
            ),
            id="id1",
            relationships=JsonApiWidgetAlertInRelationships(
                analytical_dashboard=JsonApiWidgetAlertInRelationshipsAnalyticalDashboard(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                filter_context=JsonApiWidgetAlertInRelationshipsFilterContext(
                    data=JsonApiFilterContextToOneLinkage(None),
                ),
                visualization_object=JsonApiWidgetAlertInRelationshipsVisualizationObject(
                    data=JsonApiVisualizationObjectToOneLinkage(None),
                ),
            ),
            type="widgetAlert",
        ),
    ) # JsonApiWidgetAlertInDocument | 
    filter = "filter=title==someString;description==someString;visualizationObject.id==321;analyticalDashboard.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=visualizationObject,analyticalDashboard,filterContext,createdBy,modifiedBy",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put a Widget Alert
        api_response = api_instance.update_entity_widget_alerts(workspace_id, object_id, json_api_widget_alert_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WidgetAlertsApi->update_entity_widget_alerts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Widget Alert
        api_response = api_instance.update_entity_widget_alerts(workspace_id, object_id, json_api_widget_alert_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WidgetAlertsApi->update_entity_widget_alerts: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_widget_alert_in_document** | [**JsonApiWidgetAlertInDocument**](JsonApiWidgetAlertInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiWidgetAlertOutDocument**](JsonApiWidgetAlertOutDocument.md)

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


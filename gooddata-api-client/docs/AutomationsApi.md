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
> JsonApiAutomationOutDocument create_entity_automations(workspace_id, json_api_automation_in_document, include=include, meta_include=meta_include)

Post Automations

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_automation_in_document import JsonApiAutomationInDocument
from gooddata_api_client.models.json_api_automation_out_document import JsonApiAutomationOutDocument
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.AutomationsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    json_api_automation_in_document = gooddata_api_client.JsonApiAutomationInDocument() # JsonApiAutomationInDocument | 
    include = ['notificationChannel,analyticalDashboard,createdBy,modifiedBy,exportDefinitions,recipients,automationResults'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = ['metaInclude=origin,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Post Automations
        api_response = api_instance.create_entity_automations(workspace_id, json_api_automation_in_document, include=include, meta_include=meta_include)
        print("The response of AutomationsApi->create_entity_automations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AutomationsApi->create_entity_automations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **json_api_automation_in_document** | [**JsonApiAutomationInDocument**](JsonApiAutomationInDocument.md)|  | 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

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
> delete_entity_automations(workspace_id, object_id, filter=filter)

Delete an Automation

### Example


```python
import gooddata_api_client
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.AutomationsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    object_id = 'object_id_example' # str | 
    filter = 'title==someString;description==someString;notificationChannel.id==321;analyticalDashboard.id==321' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Delete an Automation
        api_instance.delete_entity_automations(workspace_id, object_id, filter=filter)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.organization_automation_management_bulk_request import OrganizationAutomationManagementBulkRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.AutomationsApi(api_client)
    organization_automation_management_bulk_request = gooddata_api_client.OrganizationAutomationManagementBulkRequest() # OrganizationAutomationManagementBulkRequest | 

    try:
        # Delete selected automations across all workspaces
        api_instance.delete_organization_automations(organization_automation_management_bulk_request)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.workspace_automation_management_bulk_request import WorkspaceAutomationManagementBulkRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.AutomationsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    workspace_automation_management_bulk_request = gooddata_api_client.WorkspaceAutomationManagementBulkRequest() # WorkspaceAutomationManagementBulkRequest | 

    try:
        # Delete selected automations in the workspace
        api_instance.delete_workspace_automations(workspace_id, workspace_automation_management_bulk_request)
    except Exception as e:
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
> JsonApiWorkspaceAutomationOutList get_all_automations_workspace_automations(filter=filter, include=include, page=page, size=size, sort=sort, meta_include=meta_include)

Get all Automations across all Workspaces

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_workspace_automation_out_list import JsonApiWorkspaceAutomationOutList
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.AutomationsApi(api_client)
    filter = 'title==someString;description==someString;workspace.id==321;notificationChannel.id==321' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['workspace,notificationChannel,analyticalDashboard,createdBy,modifiedBy,exportDefinitions,recipients,automationResults'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get all Automations across all Workspaces
        api_response = api_instance.get_all_automations_workspace_automations(filter=filter, include=include, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of AutomationsApi->get_all_automations_workspace_automations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AutomationsApi->get_all_automations_workspace_automations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 
 **page** | **int**| Zero-based page index (0..N) | [optional] [default to 0]
 **size** | **int**| The size of the page to be returned | [optional] [default to 20]
 **sort** | [**List[str]**](str.md)| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

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
> JsonApiAutomationOutList get_all_entities_automations(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)

Get all Automations

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_automation_out_list import JsonApiAutomationOutList
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.AutomationsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    origin = ALL # str |  (optional) (default to ALL)
    filter = 'title==someString;description==someString;notificationChannel.id==321;analyticalDashboard.id==321' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['notificationChannel,analyticalDashboard,createdBy,modifiedBy,exportDefinitions,recipients,automationResults'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) (default to False)
    meta_include = ['metaInclude=origin,page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get all Automations
        api_response = api_instance.get_all_entities_automations(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        print("The response of AutomationsApi->get_all_entities_automations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AutomationsApi->get_all_entities_automations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **origin** | **str**|  | [optional] [default to ALL]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 
 **page** | **int**| Zero-based page index (0..N) | [optional] [default to 0]
 **size** | **int**| The size of the page to be returned | [optional] [default to 20]
 **sort** | [**List[str]**](str.md)| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional] 
 **x_gdc_validate_relations** | **bool**|  | [optional] [default to False]
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

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
> List[DeclarativeAutomation] get_automations(workspace_id, exclude=exclude)

Get automations

Retrieve automations for the specific workspace

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_automation import DeclarativeAutomation
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.AutomationsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    exclude = ['exclude_example'] # List[str] |  (optional)

    try:
        # Get automations
        api_response = api_instance.get_automations(workspace_id, exclude=exclude)
        print("The response of AutomationsApi->get_automations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AutomationsApi->get_automations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **exclude** | [**List[str]**](str.md)|  | [optional] 

### Return type

[**List[DeclarativeAutomation]**](DeclarativeAutomation.md)

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
> JsonApiAutomationOutDocument get_entity_automations(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)

Get an Automation

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_automation_out_document import JsonApiAutomationOutDocument
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.AutomationsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    object_id = 'object_id_example' # str | 
    filter = 'title==someString;description==someString;notificationChannel.id==321;analyticalDashboard.id==321' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['notificationChannel,analyticalDashboard,createdBy,modifiedBy,exportDefinitions,recipients,automationResults'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) (default to False)
    meta_include = ['metaInclude=origin,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get an Automation
        api_response = api_instance.get_entity_automations(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        print("The response of AutomationsApi->get_entity_automations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AutomationsApi->get_entity_automations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **object_id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 
 **x_gdc_validate_relations** | **bool**|  | [optional] [default to False]
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

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
> JsonApiAutomationOutDocument patch_entity_automations(workspace_id, object_id, json_api_automation_patch_document, filter=filter, include=include)

Patch an Automation

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_automation_out_document import JsonApiAutomationOutDocument
from gooddata_api_client.models.json_api_automation_patch_document import JsonApiAutomationPatchDocument
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.AutomationsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    object_id = 'object_id_example' # str | 
    json_api_automation_patch_document = gooddata_api_client.JsonApiAutomationPatchDocument() # JsonApiAutomationPatchDocument | 
    filter = 'title==someString;description==someString;notificationChannel.id==321;analyticalDashboard.id==321' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['notificationChannel,analyticalDashboard,createdBy,modifiedBy,exportDefinitions,recipients,automationResults'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    try:
        # Patch an Automation
        api_response = api_instance.patch_entity_automations(workspace_id, object_id, json_api_automation_patch_document, filter=filter, include=include)
        print("The response of AutomationsApi->patch_entity_automations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AutomationsApi->patch_entity_automations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **object_id** | **str**|  | 
 **json_api_automation_patch_document** | [**JsonApiAutomationPatchDocument**](JsonApiAutomationPatchDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 

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
import gooddata_api_client
from gooddata_api_client.models.organization_automation_management_bulk_request import OrganizationAutomationManagementBulkRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.AutomationsApi(api_client)
    organization_automation_management_bulk_request = gooddata_api_client.OrganizationAutomationManagementBulkRequest() # OrganizationAutomationManagementBulkRequest | 

    try:
        # Pause selected automations across all workspaces
        api_instance.pause_organization_automations(organization_automation_management_bulk_request)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.workspace_automation_management_bulk_request import WorkspaceAutomationManagementBulkRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.AutomationsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    workspace_automation_management_bulk_request = gooddata_api_client.WorkspaceAutomationManagementBulkRequest() # WorkspaceAutomationManagementBulkRequest | 

    try:
        # Pause selected automations in the workspace
        api_instance.pause_workspace_automations(workspace_id, workspace_automation_management_bulk_request)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.declarative_automation import DeclarativeAutomation
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.AutomationsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    declarative_automation = [gooddata_api_client.DeclarativeAutomation()] # List[DeclarativeAutomation] | 

    try:
        # Set automations
        api_instance.set_automations(workspace_id, declarative_automation)
    except Exception as e:
        print("Exception when calling AutomationsApi->set_automations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **declarative_automation** | [**List[DeclarativeAutomation]**](DeclarativeAutomation.md)|  | 

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
import gooddata_api_client
from gooddata_api_client.models.trigger_automation_request import TriggerAutomationRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.AutomationsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    trigger_automation_request = gooddata_api_client.TriggerAutomationRequest() # TriggerAutomationRequest | 

    try:
        # Trigger automation.
        api_instance.trigger_automation(workspace_id, trigger_automation_request)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.AutomationsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    automation_id = 'automation_id_example' # str | 

    try:
        # Trigger existing automation.
        api_instance.trigger_existing_automation(workspace_id, automation_id)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.organization_automation_management_bulk_request import OrganizationAutomationManagementBulkRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.AutomationsApi(api_client)
    organization_automation_management_bulk_request = gooddata_api_client.OrganizationAutomationManagementBulkRequest() # OrganizationAutomationManagementBulkRequest | 

    try:
        # Unpause selected automations across all workspaces
        api_instance.unpause_organization_automations(organization_automation_management_bulk_request)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.workspace_automation_management_bulk_request import WorkspaceAutomationManagementBulkRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.AutomationsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    workspace_automation_management_bulk_request = gooddata_api_client.WorkspaceAutomationManagementBulkRequest() # WorkspaceAutomationManagementBulkRequest | 

    try:
        # Unpause selected automations in the workspace
        api_instance.unpause_workspace_automations(workspace_id, workspace_automation_management_bulk_request)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.AutomationsApi(api_client)

    try:
        # Unsubscribe from all automations in all workspaces
        api_instance.unsubscribe_all_automations()
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.AutomationsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    automation_id = 'automation_id_example' # str | 

    try:
        # Unsubscribe from an automation
        api_instance.unsubscribe_automation(workspace_id, automation_id)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.organization_automation_management_bulk_request import OrganizationAutomationManagementBulkRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.AutomationsApi(api_client)
    organization_automation_management_bulk_request = gooddata_api_client.OrganizationAutomationManagementBulkRequest() # OrganizationAutomationManagementBulkRequest | 

    try:
        # Unsubscribe from selected automations across all workspaces
        api_instance.unsubscribe_organization_automations(organization_automation_management_bulk_request)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.workspace_automation_management_bulk_request import WorkspaceAutomationManagementBulkRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.AutomationsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    workspace_automation_management_bulk_request = gooddata_api_client.WorkspaceAutomationManagementBulkRequest() # WorkspaceAutomationManagementBulkRequest | 

    try:
        # Unsubscribe from selected automations in the workspace
        api_instance.unsubscribe_selected_workspace_automations(workspace_id, workspace_automation_management_bulk_request)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.AutomationsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 

    try:
        # Unsubscribe from all automations in the workspace
        api_instance.unsubscribe_workspace_automations(workspace_id)
    except Exception as e:
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
> JsonApiAutomationOutDocument update_entity_automations(workspace_id, object_id, json_api_automation_in_document, filter=filter, include=include)

Put an Automation

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_automation_in_document import JsonApiAutomationInDocument
from gooddata_api_client.models.json_api_automation_out_document import JsonApiAutomationOutDocument
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.AutomationsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    object_id = 'object_id_example' # str | 
    json_api_automation_in_document = gooddata_api_client.JsonApiAutomationInDocument() # JsonApiAutomationInDocument | 
    filter = 'title==someString;description==someString;notificationChannel.id==321;analyticalDashboard.id==321' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['notificationChannel,analyticalDashboard,createdBy,modifiedBy,exportDefinitions,recipients,automationResults'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    try:
        # Put an Automation
        api_response = api_instance.update_entity_automations(workspace_id, object_id, json_api_automation_in_document, filter=filter, include=include)
        print("The response of AutomationsApi->update_entity_automations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AutomationsApi->update_entity_automations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **object_id** | **str**|  | 
 **json_api_automation_in_document** | [**JsonApiAutomationInDocument**](JsonApiAutomationInDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 

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


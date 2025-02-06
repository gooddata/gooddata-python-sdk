# gooddata_api_client.WorkspacesEntityAPIsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_workspaces**](WorkspacesEntityAPIsApi.md#create_entity_workspaces) | **POST** /api/v1/entities/workspaces | Post Workspace entities
[**delete_entity_workspaces**](WorkspacesEntityAPIsApi.md#delete_entity_workspaces) | **DELETE** /api/v1/entities/workspaces/{id} | Delete Workspace entity
[**get_all_entities_workspaces**](WorkspacesEntityAPIsApi.md#get_all_entities_workspaces) | **GET** /api/v1/entities/workspaces | Get Workspace entities
[**get_entity_workspaces**](WorkspacesEntityAPIsApi.md#get_entity_workspaces) | **GET** /api/v1/entities/workspaces/{id} | Get Workspace entity
[**patch_entity_workspaces**](WorkspacesEntityAPIsApi.md#patch_entity_workspaces) | **PATCH** /api/v1/entities/workspaces/{id} | Patch Workspace entity
[**update_entity_workspaces**](WorkspacesEntityAPIsApi.md#update_entity_workspaces) | **PUT** /api/v1/entities/workspaces/{id} | Put Workspace entity


# **create_entity_workspaces**
> JsonApiWorkspaceOutDocument create_entity_workspaces(json_api_workspace_in_document)

Post Workspace entities

Space of the shared interest

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspaces_entity_apis_api
from gooddata_api_client.model.json_api_workspace_out_document import JsonApiWorkspaceOutDocument
from gooddata_api_client.model.json_api_workspace_in_document import JsonApiWorkspaceInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspaces_entity_apis_api.WorkspacesEntityAPIsApi(api_client)
    json_api_workspace_in_document = JsonApiWorkspaceInDocument(
        data=JsonApiWorkspaceIn(
            attributes=JsonApiWorkspaceInAttributes(
                cache_extra_limit=1,
                data_source=JsonApiWorkspaceInAttributesDataSource(
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
                name="name_example",
                prefix="/6bUUGjjNSwg0_bs",
            ),
            id="id1",
            relationships=JsonApiWorkspaceInRelationships(
                parent=JsonApiWorkspaceInRelationshipsParent(
                    data=JsonApiWorkspaceToOneLinkage(None),
                ),
            ),
            type="workspace",
        ),
    ) # JsonApiWorkspaceInDocument | 
    include = [
        "include=parent",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = [
        "metaInclude=config,permissions,hierarchy,dataModelDatasets,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Workspace entities
        api_response = api_instance.create_entity_workspaces(json_api_workspace_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesEntityAPIsApi->create_entity_workspaces: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Workspace entities
        api_response = api_instance.create_entity_workspaces(json_api_workspace_in_document, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesEntityAPIsApi->create_entity_workspaces: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_workspace_in_document** | [**JsonApiWorkspaceInDocument**](JsonApiWorkspaceInDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiWorkspaceOutDocument**](JsonApiWorkspaceOutDocument.md)

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

# **delete_entity_workspaces**
> delete_entity_workspaces(id)

Delete Workspace entity

Space of the shared interest

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspaces_entity_apis_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspaces_entity_apis_api.WorkspacesEntityAPIsApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=name==someString;earlyAccess==someString;parent.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete Workspace entity
        api_instance.delete_entity_workspaces(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesEntityAPIsApi->delete_entity_workspaces: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete Workspace entity
        api_instance.delete_entity_workspaces(id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesEntityAPIsApi->delete_entity_workspaces: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
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

# **get_all_entities_workspaces**
> JsonApiWorkspaceOutList get_all_entities_workspaces()

Get Workspace entities

Space of the shared interest

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspaces_entity_apis_api
from gooddata_api_client.model.json_api_workspace_out_list import JsonApiWorkspaceOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspaces_entity_apis_api.WorkspacesEntityAPIsApi(api_client)
    filter = "filter=name==someString;earlyAccess==someString;parent.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=parent",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = [
        "metaInclude=config,permissions,hierarchy,dataModelDatasets,page,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Workspace entities
        api_response = api_instance.get_all_entities_workspaces(filter=filter, include=include, page=page, size=size, sort=sort, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesEntityAPIsApi->get_all_entities_workspaces: %s\n" % e)
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

[**JsonApiWorkspaceOutList**](JsonApiWorkspaceOutList.md)

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

# **get_entity_workspaces**
> JsonApiWorkspaceOutDocument get_entity_workspaces(id)

Get Workspace entity

Space of the shared interest

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspaces_entity_apis_api
from gooddata_api_client.model.json_api_workspace_out_document import JsonApiWorkspaceOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspaces_entity_apis_api.WorkspacesEntityAPIsApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=name==someString;earlyAccess==someString;parent.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=parent",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = [
        "metaInclude=config,permissions,hierarchy,dataModelDatasets,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get Workspace entity
        api_response = api_instance.get_entity_workspaces(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesEntityAPIsApi->get_entity_workspaces: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Workspace entity
        api_response = api_instance.get_entity_workspaces(id, filter=filter, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesEntityAPIsApi->get_entity_workspaces: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiWorkspaceOutDocument**](JsonApiWorkspaceOutDocument.md)

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

# **patch_entity_workspaces**
> JsonApiWorkspaceOutDocument patch_entity_workspaces(id, json_api_workspace_patch_document)

Patch Workspace entity

Space of the shared interest

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspaces_entity_apis_api
from gooddata_api_client.model.json_api_workspace_out_document import JsonApiWorkspaceOutDocument
from gooddata_api_client.model.json_api_workspace_patch_document import JsonApiWorkspacePatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspaces_entity_apis_api.WorkspacesEntityAPIsApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_workspace_patch_document = JsonApiWorkspacePatchDocument(
        data=JsonApiWorkspacePatch(
            attributes=JsonApiWorkspaceInAttributes(
                cache_extra_limit=1,
                data_source=JsonApiWorkspaceInAttributesDataSource(
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
                name="name_example",
                prefix="/6bUUGjjNSwg0_bs",
            ),
            id="id1",
            relationships=JsonApiWorkspaceInRelationships(
                parent=JsonApiWorkspaceInRelationshipsParent(
                    data=JsonApiWorkspaceToOneLinkage(None),
                ),
            ),
            type="workspace",
        ),
    ) # JsonApiWorkspacePatchDocument | 
    filter = "filter=name==someString;earlyAccess==someString;parent.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=parent",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch Workspace entity
        api_response = api_instance.patch_entity_workspaces(id, json_api_workspace_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesEntityAPIsApi->patch_entity_workspaces: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch Workspace entity
        api_response = api_instance.patch_entity_workspaces(id, json_api_workspace_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesEntityAPIsApi->patch_entity_workspaces: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_workspace_patch_document** | [**JsonApiWorkspacePatchDocument**](JsonApiWorkspacePatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiWorkspaceOutDocument**](JsonApiWorkspaceOutDocument.md)

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

# **update_entity_workspaces**
> JsonApiWorkspaceOutDocument update_entity_workspaces(id, json_api_workspace_in_document)

Put Workspace entity

Space of the shared interest

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspaces_entity_apis_api
from gooddata_api_client.model.json_api_workspace_out_document import JsonApiWorkspaceOutDocument
from gooddata_api_client.model.json_api_workspace_in_document import JsonApiWorkspaceInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspaces_entity_apis_api.WorkspacesEntityAPIsApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_workspace_in_document = JsonApiWorkspaceInDocument(
        data=JsonApiWorkspaceIn(
            attributes=JsonApiWorkspaceInAttributes(
                cache_extra_limit=1,
                data_source=JsonApiWorkspaceInAttributesDataSource(
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
                name="name_example",
                prefix="/6bUUGjjNSwg0_bs",
            ),
            id="id1",
            relationships=JsonApiWorkspaceInRelationships(
                parent=JsonApiWorkspaceInRelationshipsParent(
                    data=JsonApiWorkspaceToOneLinkage(None),
                ),
            ),
            type="workspace",
        ),
    ) # JsonApiWorkspaceInDocument | 
    filter = "filter=name==someString;earlyAccess==someString;parent.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=parent",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put Workspace entity
        api_response = api_instance.update_entity_workspaces(id, json_api_workspace_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesEntityAPIsApi->update_entity_workspaces: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put Workspace entity
        api_response = api_instance.update_entity_workspaces(id, json_api_workspace_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesEntityAPIsApi->update_entity_workspaces: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_workspace_in_document** | [**JsonApiWorkspaceInDocument**](JsonApiWorkspaceInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiWorkspaceOutDocument**](JsonApiWorkspaceOutDocument.md)

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


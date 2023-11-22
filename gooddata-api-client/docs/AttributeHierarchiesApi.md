# gooddata_api_client.AttributeHierarchiesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_attribute_hierarchies**](AttributeHierarchiesApi.md#create_entity_attribute_hierarchies) | **POST** /api/v1/entities/workspaces/{workspaceId}/attributeHierarchies | Post Attribute Hierarchies
[**delete_entity_attribute_hierarchies**](AttributeHierarchiesApi.md#delete_entity_attribute_hierarchies) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/attributeHierarchies/{objectId} | Delete an Attribute Hierarchy
[**get_all_entities_attribute_hierarchies**](AttributeHierarchiesApi.md#get_all_entities_attribute_hierarchies) | **GET** /api/v1/entities/workspaces/{workspaceId}/attributeHierarchies | Get all Attribute Hierarchies
[**get_entity_attribute_hierarchies**](AttributeHierarchiesApi.md#get_entity_attribute_hierarchies) | **GET** /api/v1/entities/workspaces/{workspaceId}/attributeHierarchies/{objectId} | Get an Attribute Hierarchy
[**patch_entity_attribute_hierarchies**](AttributeHierarchiesApi.md#patch_entity_attribute_hierarchies) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/attributeHierarchies/{objectId} | Patch an Attribute Hierarchy
[**update_entity_attribute_hierarchies**](AttributeHierarchiesApi.md#update_entity_attribute_hierarchies) | **PUT** /api/v1/entities/workspaces/{workspaceId}/attributeHierarchies/{objectId} | Put an Attribute Hierarchy


# **create_entity_attribute_hierarchies**
> JsonApiAttributeHierarchyOutDocument create_entity_attribute_hierarchies(workspace_id, json_api_attribute_hierarchy_in_document)

Post Attribute Hierarchies

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import attribute_hierarchies_api
from gooddata_api_client.model.json_api_attribute_hierarchy_in_document import JsonApiAttributeHierarchyInDocument
from gooddata_api_client.model.json_api_attribute_hierarchy_out_document import JsonApiAttributeHierarchyOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = attribute_hierarchies_api.AttributeHierarchiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_attribute_hierarchy_in_document = JsonApiAttributeHierarchyInDocument(
        data=JsonApiAttributeHierarchyIn(
            attributes=JsonApiAttributeHierarchyInAttributes(
                are_relations_valid=True,
                content={},
                description="description_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            type="attributeHierarchy",
        ),
    ) # JsonApiAttributeHierarchyInDocument | 
    include = [
        "include=createdBy,modifiedBy,attributes",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Attribute Hierarchies
        api_response = api_instance.create_entity_attribute_hierarchies(workspace_id, json_api_attribute_hierarchy_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AttributeHierarchiesApi->create_entity_attribute_hierarchies: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Attribute Hierarchies
        api_response = api_instance.create_entity_attribute_hierarchies(workspace_id, json_api_attribute_hierarchy_in_document, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AttributeHierarchiesApi->create_entity_attribute_hierarchies: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_attribute_hierarchy_in_document** | [**JsonApiAttributeHierarchyInDocument**](JsonApiAttributeHierarchyInDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiAttributeHierarchyOutDocument**](JsonApiAttributeHierarchyOutDocument.md)

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

# **delete_entity_attribute_hierarchies**
> delete_entity_attribute_hierarchies(workspace_id, object_id)

Delete an Attribute Hierarchy

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import attribute_hierarchies_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = attribute_hierarchies_api.AttributeHierarchiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString;createdBy.id==321;modifiedBy.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete an Attribute Hierarchy
        api_instance.delete_entity_attribute_hierarchies(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AttributeHierarchiesApi->delete_entity_attribute_hierarchies: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete an Attribute Hierarchy
        api_instance.delete_entity_attribute_hierarchies(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AttributeHierarchiesApi->delete_entity_attribute_hierarchies: %s\n" % e)
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

# **get_all_entities_attribute_hierarchies**
> JsonApiAttributeHierarchyOutList get_all_entities_attribute_hierarchies(workspace_id)

Get all Attribute Hierarchies

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import attribute_hierarchies_api
from gooddata_api_client.model.json_api_attribute_hierarchy_out_list import JsonApiAttributeHierarchyOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = attribute_hierarchies_api.AttributeHierarchiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "filter=title==someString;description==someString;createdBy.id==321;modifiedBy.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=createdBy,modifiedBy,attributes",
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
        # Get all Attribute Hierarchies
        api_response = api_instance.get_all_entities_attribute_hierarchies(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AttributeHierarchiesApi->get_all_entities_attribute_hierarchies: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Attribute Hierarchies
        api_response = api_instance.get_all_entities_attribute_hierarchies(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AttributeHierarchiesApi->get_all_entities_attribute_hierarchies: %s\n" % e)
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

[**JsonApiAttributeHierarchyOutList**](JsonApiAttributeHierarchyOutList.md)

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

# **get_entity_attribute_hierarchies**
> JsonApiAttributeHierarchyOutDocument get_entity_attribute_hierarchies(workspace_id, object_id)

Get an Attribute Hierarchy

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import attribute_hierarchies_api
from gooddata_api_client.model.json_api_attribute_hierarchy_out_document import JsonApiAttributeHierarchyOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = attribute_hierarchies_api.AttributeHierarchiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString;createdBy.id==321;modifiedBy.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=createdBy,modifiedBy,attributes",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get an Attribute Hierarchy
        api_response = api_instance.get_entity_attribute_hierarchies(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AttributeHierarchiesApi->get_entity_attribute_hierarchies: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get an Attribute Hierarchy
        api_response = api_instance.get_entity_attribute_hierarchies(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AttributeHierarchiesApi->get_entity_attribute_hierarchies: %s\n" % e)
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

[**JsonApiAttributeHierarchyOutDocument**](JsonApiAttributeHierarchyOutDocument.md)

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

# **patch_entity_attribute_hierarchies**
> JsonApiAttributeHierarchyOutDocument patch_entity_attribute_hierarchies(workspace_id, object_id, json_api_attribute_hierarchy_patch_document)

Patch an Attribute Hierarchy

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import attribute_hierarchies_api
from gooddata_api_client.model.json_api_attribute_hierarchy_patch_document import JsonApiAttributeHierarchyPatchDocument
from gooddata_api_client.model.json_api_attribute_hierarchy_out_document import JsonApiAttributeHierarchyOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = attribute_hierarchies_api.AttributeHierarchiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_attribute_hierarchy_patch_document = JsonApiAttributeHierarchyPatchDocument(
        data=JsonApiAttributeHierarchyPatch(
            attributes=JsonApiAttributeHierarchyInAttributes(
                are_relations_valid=True,
                content={},
                description="description_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            type="attributeHierarchy",
        ),
    ) # JsonApiAttributeHierarchyPatchDocument | 
    filter = "filter=title==someString;description==someString;createdBy.id==321;modifiedBy.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=createdBy,modifiedBy,attributes",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch an Attribute Hierarchy
        api_response = api_instance.patch_entity_attribute_hierarchies(workspace_id, object_id, json_api_attribute_hierarchy_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AttributeHierarchiesApi->patch_entity_attribute_hierarchies: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch an Attribute Hierarchy
        api_response = api_instance.patch_entity_attribute_hierarchies(workspace_id, object_id, json_api_attribute_hierarchy_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AttributeHierarchiesApi->patch_entity_attribute_hierarchies: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_attribute_hierarchy_patch_document** | [**JsonApiAttributeHierarchyPatchDocument**](JsonApiAttributeHierarchyPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiAttributeHierarchyOutDocument**](JsonApiAttributeHierarchyOutDocument.md)

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

# **update_entity_attribute_hierarchies**
> JsonApiAttributeHierarchyOutDocument update_entity_attribute_hierarchies(workspace_id, object_id, json_api_attribute_hierarchy_in_document)

Put an Attribute Hierarchy

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import attribute_hierarchies_api
from gooddata_api_client.model.json_api_attribute_hierarchy_in_document import JsonApiAttributeHierarchyInDocument
from gooddata_api_client.model.json_api_attribute_hierarchy_out_document import JsonApiAttributeHierarchyOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = attribute_hierarchies_api.AttributeHierarchiesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_attribute_hierarchy_in_document = JsonApiAttributeHierarchyInDocument(
        data=JsonApiAttributeHierarchyIn(
            attributes=JsonApiAttributeHierarchyInAttributes(
                are_relations_valid=True,
                content={},
                description="description_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            type="attributeHierarchy",
        ),
    ) # JsonApiAttributeHierarchyInDocument | 
    filter = "filter=title==someString;description==someString;createdBy.id==321;modifiedBy.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=createdBy,modifiedBy,attributes",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put an Attribute Hierarchy
        api_response = api_instance.update_entity_attribute_hierarchies(workspace_id, object_id, json_api_attribute_hierarchy_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AttributeHierarchiesApi->update_entity_attribute_hierarchies: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put an Attribute Hierarchy
        api_response = api_instance.update_entity_attribute_hierarchies(workspace_id, object_id, json_api_attribute_hierarchy_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AttributeHierarchiesApi->update_entity_attribute_hierarchies: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_attribute_hierarchy_in_document** | [**JsonApiAttributeHierarchyInDocument**](JsonApiAttributeHierarchyInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiAttributeHierarchyOutDocument**](JsonApiAttributeHierarchyOutDocument.md)

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


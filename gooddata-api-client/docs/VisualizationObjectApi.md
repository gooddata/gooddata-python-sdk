# gooddata_api_client.VisualizationObjectApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_visualization_objects**](VisualizationObjectApi.md#create_entity_visualization_objects) | **POST** /api/v1/entities/workspaces/{workspaceId}/visualizationObjects | Post Visualization Objects
[**delete_entity_visualization_objects**](VisualizationObjectApi.md#delete_entity_visualization_objects) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/visualizationObjects/{objectId} | Delete a Visualization Object
[**get_all_entities_visualization_objects**](VisualizationObjectApi.md#get_all_entities_visualization_objects) | **GET** /api/v1/entities/workspaces/{workspaceId}/visualizationObjects | Get all Visualization Objects
[**get_entity_visualization_objects**](VisualizationObjectApi.md#get_entity_visualization_objects) | **GET** /api/v1/entities/workspaces/{workspaceId}/visualizationObjects/{objectId} | Get a Visualization Object
[**patch_entity_visualization_objects**](VisualizationObjectApi.md#patch_entity_visualization_objects) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/visualizationObjects/{objectId} | Patch a Visualization Object
[**update_entity_visualization_objects**](VisualizationObjectApi.md#update_entity_visualization_objects) | **PUT** /api/v1/entities/workspaces/{workspaceId}/visualizationObjects/{objectId} | Put a Visualization Object


# **create_entity_visualization_objects**
> JsonApiVisualizationObjectOutDocument create_entity_visualization_objects(workspace_id, json_api_visualization_object_post_optional_id_document)

Post Visualization Objects

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import visualization_object_api
from gooddata_api_client.model.json_api_visualization_object_out_document import JsonApiVisualizationObjectOutDocument
from gooddata_api_client.model.json_api_visualization_object_post_optional_id_document import JsonApiVisualizationObjectPostOptionalIdDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = visualization_object_api.VisualizationObjectApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_visualization_object_post_optional_id_document = JsonApiVisualizationObjectPostOptionalIdDocument(
        data=JsonApiVisualizationObjectPostOptionalId(
            attributes=JsonApiAnalyticalDashboardInAttributes(
                are_relations_valid=True,
                content={},
                description="description_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            type="visualizationObject",
        ),
    ) # JsonApiVisualizationObjectPostOptionalIdDocument | 
    include = [
        "include=facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Visualization Objects
        api_response = api_instance.create_entity_visualization_objects(workspace_id, json_api_visualization_object_post_optional_id_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling VisualizationObjectApi->create_entity_visualization_objects: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Visualization Objects
        api_response = api_instance.create_entity_visualization_objects(workspace_id, json_api_visualization_object_post_optional_id_document, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling VisualizationObjectApi->create_entity_visualization_objects: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_visualization_object_post_optional_id_document** | [**JsonApiVisualizationObjectPostOptionalIdDocument**](JsonApiVisualizationObjectPostOptionalIdDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiVisualizationObjectOutDocument**](JsonApiVisualizationObjectOutDocument.md)

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

# **delete_entity_visualization_objects**
> delete_entity_visualization_objects(workspace_id, object_id)

Delete a Visualization Object

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import visualization_object_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = visualization_object_api.VisualizationObjectApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Visualization Object
        api_instance.delete_entity_visualization_objects(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling VisualizationObjectApi->delete_entity_visualization_objects: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Visualization Object
        api_instance.delete_entity_visualization_objects(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling VisualizationObjectApi->delete_entity_visualization_objects: %s\n" % e)
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

# **get_all_entities_visualization_objects**
> JsonApiVisualizationObjectOutList get_all_entities_visualization_objects(workspace_id)

Get all Visualization Objects

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import visualization_object_api
from gooddata_api_client.model.json_api_visualization_object_out_list import JsonApiVisualizationObjectOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = visualization_object_api.VisualizationObjectApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=facts,attributes,labels,metrics,datasets",
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
        # Get all Visualization Objects
        api_response = api_instance.get_all_entities_visualization_objects(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling VisualizationObjectApi->get_all_entities_visualization_objects: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Visualization Objects
        api_response = api_instance.get_all_entities_visualization_objects(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling VisualizationObjectApi->get_all_entities_visualization_objects: %s\n" % e)
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

[**JsonApiVisualizationObjectOutList**](JsonApiVisualizationObjectOutList.md)

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

# **get_entity_visualization_objects**
> JsonApiVisualizationObjectOutDocument get_entity_visualization_objects(workspace_id, object_id)

Get a Visualization Object

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import visualization_object_api
from gooddata_api_client.model.json_api_visualization_object_out_document import JsonApiVisualizationObjectOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = visualization_object_api.VisualizationObjectApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a Visualization Object
        api_response = api_instance.get_entity_visualization_objects(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling VisualizationObjectApi->get_entity_visualization_objects: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Visualization Object
        api_response = api_instance.get_entity_visualization_objects(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling VisualizationObjectApi->get_entity_visualization_objects: %s\n" % e)
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

[**JsonApiVisualizationObjectOutDocument**](JsonApiVisualizationObjectOutDocument.md)

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

# **patch_entity_visualization_objects**
> JsonApiVisualizationObjectOutDocument patch_entity_visualization_objects(workspace_id, object_id, json_api_visualization_object_patch_document)

Patch a Visualization Object

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import visualization_object_api
from gooddata_api_client.model.json_api_visualization_object_out_document import JsonApiVisualizationObjectOutDocument
from gooddata_api_client.model.json_api_visualization_object_patch_document import JsonApiVisualizationObjectPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = visualization_object_api.VisualizationObjectApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_visualization_object_patch_document = JsonApiVisualizationObjectPatchDocument(
        data=JsonApiVisualizationObjectPatch(
            attributes=JsonApiAnalyticalDashboardInAttributes(
                are_relations_valid=True,
                content={},
                description="description_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            type="visualizationObject",
        ),
    ) # JsonApiVisualizationObjectPatchDocument | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch a Visualization Object
        api_response = api_instance.patch_entity_visualization_objects(workspace_id, object_id, json_api_visualization_object_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling VisualizationObjectApi->patch_entity_visualization_objects: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Visualization Object
        api_response = api_instance.patch_entity_visualization_objects(workspace_id, object_id, json_api_visualization_object_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling VisualizationObjectApi->patch_entity_visualization_objects: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_visualization_object_patch_document** | [**JsonApiVisualizationObjectPatchDocument**](JsonApiVisualizationObjectPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiVisualizationObjectOutDocument**](JsonApiVisualizationObjectOutDocument.md)

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

# **update_entity_visualization_objects**
> JsonApiVisualizationObjectOutDocument update_entity_visualization_objects(workspace_id, object_id, json_api_visualization_object_in_document)

Put a Visualization Object

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import visualization_object_api
from gooddata_api_client.model.json_api_visualization_object_out_document import JsonApiVisualizationObjectOutDocument
from gooddata_api_client.model.json_api_visualization_object_in_document import JsonApiVisualizationObjectInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = visualization_object_api.VisualizationObjectApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_visualization_object_in_document = JsonApiVisualizationObjectInDocument(
        data=JsonApiVisualizationObjectIn(
            attributes=JsonApiAnalyticalDashboardInAttributes(
                are_relations_valid=True,
                content={},
                description="description_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            type="visualizationObject",
        ),
    ) # JsonApiVisualizationObjectInDocument | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put a Visualization Object
        api_response = api_instance.update_entity_visualization_objects(workspace_id, object_id, json_api_visualization_object_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling VisualizationObjectApi->update_entity_visualization_objects: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Visualization Object
        api_response = api_instance.update_entity_visualization_objects(workspace_id, object_id, json_api_visualization_object_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling VisualizationObjectApi->update_entity_visualization_objects: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_visualization_object_in_document** | [**JsonApiVisualizationObjectInDocument**](JsonApiVisualizationObjectInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiVisualizationObjectOutDocument**](JsonApiVisualizationObjectOutDocument.md)

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


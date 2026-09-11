# gooddata_api_client.ComputedAttributesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_computed_attributes**](ComputedAttributesApi.md#create_entity_computed_attributes) | **POST** /api/v1/entities/workspaces/{workspaceId}/computedAttributes | Post Computed Attributes
[**delete_entity_computed_attributes**](ComputedAttributesApi.md#delete_entity_computed_attributes) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/computedAttributes/{objectId} | Delete a Computed Attribute
[**get_all_entities_computed_attributes**](ComputedAttributesApi.md#get_all_entities_computed_attributes) | **GET** /api/v1/entities/workspaces/{workspaceId}/computedAttributes | Get all Computed Attributes
[**get_entity_computed_attributes**](ComputedAttributesApi.md#get_entity_computed_attributes) | **GET** /api/v1/entities/workspaces/{workspaceId}/computedAttributes/{objectId} | Get a Computed Attribute
[**patch_entity_computed_attributes**](ComputedAttributesApi.md#patch_entity_computed_attributes) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/computedAttributes/{objectId} | Patch a Computed Attribute
[**search_entities_computed_attributes**](ComputedAttributesApi.md#search_entities_computed_attributes) | **POST** /api/v1/entities/workspaces/{workspaceId}/computedAttributes/search | The search endpoint (beta)
[**update_entity_computed_attributes**](ComputedAttributesApi.md#update_entity_computed_attributes) | **PUT** /api/v1/entities/workspaces/{workspaceId}/computedAttributes/{objectId} | Put a Computed Attribute


# **create_entity_computed_attributes**
> JsonApiComputedAttributeOutDocument create_entity_computed_attributes(workspace_id, json_api_computed_attribute_post_optional_id_document)

Post Computed Attributes

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import computed_attributes_api
from gooddata_api_client.model.json_api_computed_attribute_in_attributes import JsonApiComputedAttributeInAttributes
from gooddata_api_client.model.json_api_computed_attribute_in_attributes_content import JsonApiComputedAttributeInAttributesContent
from gooddata_api_client.model.json_api_computed_attribute_out_document import JsonApiComputedAttributeOutDocument
from gooddata_api_client.model.json_api_computed_attribute_post_optional_id import JsonApiComputedAttributePostOptionalId
from gooddata_api_client.model.json_api_computed_attribute_post_optional_id_document import JsonApiComputedAttributePostOptionalIdDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = computed_attributes_api.ComputedAttributesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_computed_attribute_post_optional_id_document = JsonApiComputedAttributePostOptionalIdDocument(
        data=JsonApiComputedAttributePostOptionalId(
            attributes=JsonApiComputedAttributeInAttributes(
                are_relations_valid=True,
                content=JsonApiComputedAttributeInAttributesContent(
                    format="format_example",
                    maql="maql_example",
                    metric_type="UNSPECIFIED",
                ),
                data_type="INT",
                description="description_example",
                is_hidden=True,
                is_nullable=True,
                locale="locale_example",
                null_value="null_value_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
                value_type="TEXT",
            ),
            id="id1",
            type="computedAttribute",
        ),
    ) # JsonApiComputedAttributePostOptionalIdDocument | 
    include = [
        "createdBy,modifiedBy,certifiedBy,facts,attributes,labels,computedAttributes,metrics,datasets,parameters",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Computed Attributes
        api_response = api_instance.create_entity_computed_attributes(workspace_id, json_api_computed_attribute_post_optional_id_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputedAttributesApi->create_entity_computed_attributes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Computed Attributes
        api_response = api_instance.create_entity_computed_attributes(workspace_id, json_api_computed_attribute_post_optional_id_document, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputedAttributesApi->create_entity_computed_attributes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_computed_attribute_post_optional_id_document** | [**JsonApiComputedAttributePostOptionalIdDocument**](JsonApiComputedAttributePostOptionalIdDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiComputedAttributeOutDocument**](JsonApiComputedAttributeOutDocument.md)

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

# **delete_entity_computed_attributes**
> delete_entity_computed_attributes(workspace_id, object_id)

Delete a Computed Attribute

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import computed_attributes_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = computed_attributes_api.ComputedAttributesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Delete a Computed Attribute
        api_instance.delete_entity_computed_attributes(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputedAttributesApi->delete_entity_computed_attributes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |

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

# **get_all_entities_computed_attributes**
> JsonApiComputedAttributeOutList get_all_entities_computed_attributes(workspace_id)

Get all Computed Attributes

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import computed_attributes_api
from gooddata_api_client.model.json_api_computed_attribute_out_list import JsonApiComputedAttributeOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = computed_attributes_api.ComputedAttributesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "title==someString;description==someString;createdBy.id==321;modifiedBy.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "createdBy,modifiedBy,certifiedBy,facts,attributes,labels,computedAttributes,metrics,datasets,parameters",
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
        # Get all Computed Attributes
        api_response = api_instance.get_all_entities_computed_attributes(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputedAttributesApi->get_all_entities_computed_attributes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Computed Attributes
        api_response = api_instance.get_all_entities_computed_attributes(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputedAttributesApi->get_all_entities_computed_attributes: %s\n" % e)
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

[**JsonApiComputedAttributeOutList**](JsonApiComputedAttributeOutList.md)

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

# **get_entity_computed_attributes**
> JsonApiComputedAttributeOutDocument get_entity_computed_attributes(workspace_id, object_id)

Get a Computed Attribute

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import computed_attributes_api
from gooddata_api_client.model.json_api_computed_attribute_out_document import JsonApiComputedAttributeOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = computed_attributes_api.ComputedAttributesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "title==someString;description==someString;createdBy.id==321;modifiedBy.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "createdBy,modifiedBy,certifiedBy,facts,attributes,labels,computedAttributes,metrics,datasets,parameters",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a Computed Attribute
        api_response = api_instance.get_entity_computed_attributes(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputedAttributesApi->get_entity_computed_attributes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Computed Attribute
        api_response = api_instance.get_entity_computed_attributes(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputedAttributesApi->get_entity_computed_attributes: %s\n" % e)
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

[**JsonApiComputedAttributeOutDocument**](JsonApiComputedAttributeOutDocument.md)

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

# **patch_entity_computed_attributes**
> JsonApiComputedAttributeOutDocument patch_entity_computed_attributes(workspace_id, object_id, json_api_computed_attribute_patch_document)

Patch a Computed Attribute

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import computed_attributes_api
from gooddata_api_client.model.json_api_computed_attribute_in_attributes_content import JsonApiComputedAttributeInAttributesContent
from gooddata_api_client.model.json_api_computed_attribute_out_document import JsonApiComputedAttributeOutDocument
from gooddata_api_client.model.json_api_computed_attribute_patch import JsonApiComputedAttributePatch
from gooddata_api_client.model.json_api_computed_attribute_patch_attributes import JsonApiComputedAttributePatchAttributes
from gooddata_api_client.model.json_api_computed_attribute_patch_document import JsonApiComputedAttributePatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = computed_attributes_api.ComputedAttributesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_computed_attribute_patch_document = JsonApiComputedAttributePatchDocument(
        data=JsonApiComputedAttributePatch(
            attributes=JsonApiComputedAttributePatchAttributes(
                are_relations_valid=True,
                content=JsonApiComputedAttributeInAttributesContent(
                    format="format_example",
                    maql="maql_example",
                    metric_type="UNSPECIFIED",
                ),
                data_type="INT",
                description="description_example",
                is_hidden=True,
                is_nullable=True,
                locale="locale_example",
                null_value="null_value_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
                value_type="TEXT",
            ),
            id="id1",
            type="computedAttribute",
        ),
    ) # JsonApiComputedAttributePatchDocument | 
    filter = "title==someString;description==someString;createdBy.id==321;modifiedBy.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "createdBy,modifiedBy,certifiedBy,facts,attributes,labels,computedAttributes,metrics,datasets,parameters",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch a Computed Attribute
        api_response = api_instance.patch_entity_computed_attributes(workspace_id, object_id, json_api_computed_attribute_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputedAttributesApi->patch_entity_computed_attributes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Computed Attribute
        api_response = api_instance.patch_entity_computed_attributes(workspace_id, object_id, json_api_computed_attribute_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputedAttributesApi->patch_entity_computed_attributes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_computed_attribute_patch_document** | [**JsonApiComputedAttributePatchDocument**](JsonApiComputedAttributePatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiComputedAttributeOutDocument**](JsonApiComputedAttributeOutDocument.md)

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

# **search_entities_computed_attributes**
> JsonApiComputedAttributeOutList search_entities_computed_attributes(workspace_id, entity_search_body)

The search endpoint (beta)

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import computed_attributes_api
from gooddata_api_client.model.entity_search_body import EntitySearchBody
from gooddata_api_client.model.entity_search_page import EntitySearchPage
from gooddata_api_client.model.entity_search_sort import EntitySearchSort
from gooddata_api_client.model.json_api_computed_attribute_out_list import JsonApiComputedAttributeOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = computed_attributes_api.ComputedAttributesApi(api_client)
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
        api_response = api_instance.search_entities_computed_attributes(workspace_id, entity_search_body)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputedAttributesApi->search_entities_computed_attributes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # The search endpoint (beta)
        api_response = api_instance.search_entities_computed_attributes(workspace_id, entity_search_body, origin=origin, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputedAttributesApi->search_entities_computed_attributes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **entity_search_body** | [**EntitySearchBody**](EntitySearchBody.md)| Search request body with filter, pagination, and sorting options |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**JsonApiComputedAttributeOutList**](JsonApiComputedAttributeOutList.md)

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

# **update_entity_computed_attributes**
> JsonApiComputedAttributeOutDocument update_entity_computed_attributes(workspace_id, object_id, json_api_computed_attribute_in_document)

Put a Computed Attribute

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import computed_attributes_api
from gooddata_api_client.model.json_api_computed_attribute_in import JsonApiComputedAttributeIn
from gooddata_api_client.model.json_api_computed_attribute_in_attributes import JsonApiComputedAttributeInAttributes
from gooddata_api_client.model.json_api_computed_attribute_in_attributes_content import JsonApiComputedAttributeInAttributesContent
from gooddata_api_client.model.json_api_computed_attribute_in_document import JsonApiComputedAttributeInDocument
from gooddata_api_client.model.json_api_computed_attribute_out_document import JsonApiComputedAttributeOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = computed_attributes_api.ComputedAttributesApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_computed_attribute_in_document = JsonApiComputedAttributeInDocument(
        data=JsonApiComputedAttributeIn(
            attributes=JsonApiComputedAttributeInAttributes(
                are_relations_valid=True,
                content=JsonApiComputedAttributeInAttributesContent(
                    format="format_example",
                    maql="maql_example",
                    metric_type="UNSPECIFIED",
                ),
                data_type="INT",
                description="description_example",
                is_hidden=True,
                is_nullable=True,
                locale="locale_example",
                null_value="null_value_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
                value_type="TEXT",
            ),
            id="id1",
            type="computedAttribute",
        ),
    ) # JsonApiComputedAttributeInDocument | 
    filter = "title==someString;description==someString;createdBy.id==321;modifiedBy.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "createdBy,modifiedBy,certifiedBy,facts,attributes,labels,computedAttributes,metrics,datasets,parameters",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put a Computed Attribute
        api_response = api_instance.update_entity_computed_attributes(workspace_id, object_id, json_api_computed_attribute_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputedAttributesApi->update_entity_computed_attributes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Computed Attribute
        api_response = api_instance.update_entity_computed_attributes(workspace_id, object_id, json_api_computed_attribute_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ComputedAttributesApi->update_entity_computed_attributes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_computed_attribute_in_document** | [**JsonApiComputedAttributeInDocument**](JsonApiComputedAttributeInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiComputedAttributeOutDocument**](JsonApiComputedAttributeOutDocument.md)

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


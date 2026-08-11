# gooddata_api_client.OrgMemoryItemControllerApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_org_memory_items**](OrgMemoryItemControllerApi.md#create_entity_org_memory_items) | **POST** /api/v1/entities/orgMemoryItems | Post organization Memory Item entities
[**delete_entity_org_memory_items**](OrgMemoryItemControllerApi.md#delete_entity_org_memory_items) | **DELETE** /api/v1/entities/orgMemoryItems/{id} | Delete an organization Memory Item entity
[**get_all_entities_org_memory_items**](OrgMemoryItemControllerApi.md#get_all_entities_org_memory_items) | **GET** /api/v1/entities/orgMemoryItems | Get all organization Memory Item entities
[**get_entity_org_memory_items**](OrgMemoryItemControllerApi.md#get_entity_org_memory_items) | **GET** /api/v1/entities/orgMemoryItems/{id} | Get an organization Memory Item entity
[**patch_entity_org_memory_items**](OrgMemoryItemControllerApi.md#patch_entity_org_memory_items) | **PATCH** /api/v1/entities/orgMemoryItems/{id} | Patch an organization Memory Item entity
[**update_entity_org_memory_items**](OrgMemoryItemControllerApi.md#update_entity_org_memory_items) | **PUT** /api/v1/entities/orgMemoryItems/{id} | Put an organization Memory Item entity


# **create_entity_org_memory_items**
> JsonApiOrgMemoryItemOutDocument create_entity_org_memory_items(json_api_org_memory_item_in_document)

Post organization Memory Item entities

Organization-scoped AI memory item

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import org_memory_item_controller_api
from gooddata_api_client.model.json_api_org_memory_item_in_document import JsonApiOrgMemoryItemInDocument
from gooddata_api_client.model.json_api_org_memory_item_out_document import JsonApiOrgMemoryItemOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = org_memory_item_controller_api.OrgMemoryItemControllerApi(api_client)
    json_api_org_memory_item_in_document = JsonApiOrgMemoryItemInDocument(
        data=JsonApiOrgMemoryItemIn(
            attributes=JsonApiOrgMemoryItemInAttributes(
                description="description_example",
                instruction="instruction_example",
                is_disabled=True,
                keywords=[
                    "keywords_example",
                ],
                strategy="ALWAYS",
                title="title_example",
            ),
            id="id1",
            type="orgMemoryItem",
        ),
    ) # JsonApiOrgMemoryItemInDocument | 
    include = [
        "createdBy,modifiedBy",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post organization Memory Item entities
        api_response = api_instance.create_entity_org_memory_items(json_api_org_memory_item_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrgMemoryItemControllerApi->create_entity_org_memory_items: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post organization Memory Item entities
        api_response = api_instance.create_entity_org_memory_items(json_api_org_memory_item_in_document, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrgMemoryItemControllerApi->create_entity_org_memory_items: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_org_memory_item_in_document** | [**JsonApiOrgMemoryItemInDocument**](JsonApiOrgMemoryItemInDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiOrgMemoryItemOutDocument**](JsonApiOrgMemoryItemOutDocument.md)

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

# **delete_entity_org_memory_items**
> delete_entity_org_memory_items(id)

Delete an organization Memory Item entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import org_memory_item_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = org_memory_item_controller_api.OrgMemoryItemControllerApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Delete an organization Memory Item entity
        api_instance.delete_entity_org_memory_items(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrgMemoryItemControllerApi->delete_entity_org_memory_items: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |

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

# **get_all_entities_org_memory_items**
> JsonApiOrgMemoryItemOutList get_all_entities_org_memory_items()

Get all organization Memory Item entities

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import org_memory_item_controller_api
from gooddata_api_client.model.json_api_org_memory_item_out_list import JsonApiOrgMemoryItemOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = org_memory_item_controller_api.OrgMemoryItemControllerApi(api_client)
    filter = "title==someString;description==someString;createdBy.id==321;modifiedBy.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "createdBy,modifiedBy",
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
        # Get all organization Memory Item entities
        api_response = api_instance.get_all_entities_org_memory_items(filter=filter, include=include, page=page, size=size, sort=sort, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrgMemoryItemControllerApi->get_all_entities_org_memory_items: %s\n" % e)
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

[**JsonApiOrgMemoryItemOutList**](JsonApiOrgMemoryItemOutList.md)

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

# **get_entity_org_memory_items**
> JsonApiOrgMemoryItemOutDocument get_entity_org_memory_items(id)

Get an organization Memory Item entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import org_memory_item_controller_api
from gooddata_api_client.model.json_api_org_memory_item_out_document import JsonApiOrgMemoryItemOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = org_memory_item_controller_api.OrgMemoryItemControllerApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "title==someString;description==someString;createdBy.id==321;modifiedBy.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "createdBy,modifiedBy",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get an organization Memory Item entity
        api_response = api_instance.get_entity_org_memory_items(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrgMemoryItemControllerApi->get_entity_org_memory_items: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get an organization Memory Item entity
        api_response = api_instance.get_entity_org_memory_items(id, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrgMemoryItemControllerApi->get_entity_org_memory_items: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiOrgMemoryItemOutDocument**](JsonApiOrgMemoryItemOutDocument.md)

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

# **patch_entity_org_memory_items**
> JsonApiOrgMemoryItemOutDocument patch_entity_org_memory_items(id, json_api_org_memory_item_patch_document)

Patch an organization Memory Item entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import org_memory_item_controller_api
from gooddata_api_client.model.json_api_org_memory_item_patch_document import JsonApiOrgMemoryItemPatchDocument
from gooddata_api_client.model.json_api_org_memory_item_out_document import JsonApiOrgMemoryItemOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = org_memory_item_controller_api.OrgMemoryItemControllerApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_org_memory_item_patch_document = JsonApiOrgMemoryItemPatchDocument(
        data=JsonApiOrgMemoryItemPatch(
            attributes=JsonApiOrgMemoryItemPatchAttributes(
                description="description_example",
                instruction="instruction_example",
                is_disabled=True,
                keywords=[
                    "keywords_example",
                ],
                strategy="ALWAYS",
                title="title_example",
            ),
            id="id1",
            type="orgMemoryItem",
        ),
    ) # JsonApiOrgMemoryItemPatchDocument | 
    filter = "title==someString;description==someString;createdBy.id==321;modifiedBy.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "createdBy,modifiedBy",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch an organization Memory Item entity
        api_response = api_instance.patch_entity_org_memory_items(id, json_api_org_memory_item_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrgMemoryItemControllerApi->patch_entity_org_memory_items: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch an organization Memory Item entity
        api_response = api_instance.patch_entity_org_memory_items(id, json_api_org_memory_item_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrgMemoryItemControllerApi->patch_entity_org_memory_items: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_org_memory_item_patch_document** | [**JsonApiOrgMemoryItemPatchDocument**](JsonApiOrgMemoryItemPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiOrgMemoryItemOutDocument**](JsonApiOrgMemoryItemOutDocument.md)

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

# **update_entity_org_memory_items**
> JsonApiOrgMemoryItemOutDocument update_entity_org_memory_items(id, json_api_org_memory_item_in_document)

Put an organization Memory Item entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import org_memory_item_controller_api
from gooddata_api_client.model.json_api_org_memory_item_in_document import JsonApiOrgMemoryItemInDocument
from gooddata_api_client.model.json_api_org_memory_item_out_document import JsonApiOrgMemoryItemOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = org_memory_item_controller_api.OrgMemoryItemControllerApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_org_memory_item_in_document = JsonApiOrgMemoryItemInDocument(
        data=JsonApiOrgMemoryItemIn(
            attributes=JsonApiOrgMemoryItemInAttributes(
                description="description_example",
                instruction="instruction_example",
                is_disabled=True,
                keywords=[
                    "keywords_example",
                ],
                strategy="ALWAYS",
                title="title_example",
            ),
            id="id1",
            type="orgMemoryItem",
        ),
    ) # JsonApiOrgMemoryItemInDocument | 
    filter = "title==someString;description==someString;createdBy.id==321;modifiedBy.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "createdBy,modifiedBy",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put an organization Memory Item entity
        api_response = api_instance.update_entity_org_memory_items(id, json_api_org_memory_item_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrgMemoryItemControllerApi->update_entity_org_memory_items: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put an organization Memory Item entity
        api_response = api_instance.update_entity_org_memory_items(id, json_api_org_memory_item_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrgMemoryItemControllerApi->update_entity_org_memory_items: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_org_memory_item_in_document** | [**JsonApiOrgMemoryItemInDocument**](JsonApiOrgMemoryItemInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiOrgMemoryItemOutDocument**](JsonApiOrgMemoryItemOutDocument.md)

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


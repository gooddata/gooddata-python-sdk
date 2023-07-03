# gooddata_api_client.UserGroupsEntityAPIsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_user_groups**](UserGroupsEntityAPIsApi.md#create_entity_user_groups) | **POST** /api/v1/entities/userGroups | Post User Group entities
[**delete_entity_user_groups**](UserGroupsEntityAPIsApi.md#delete_entity_user_groups) | **DELETE** /api/v1/entities/userGroups/{id} | Delete UserGroup entity
[**get_all_entities_user_groups**](UserGroupsEntityAPIsApi.md#get_all_entities_user_groups) | **GET** /api/v1/entities/userGroups | Get UserGroup entities
[**get_entity_user_groups**](UserGroupsEntityAPIsApi.md#get_entity_user_groups) | **GET** /api/v1/entities/userGroups/{id} | Get UserGroup entity
[**patch_entity_user_groups**](UserGroupsEntityAPIsApi.md#patch_entity_user_groups) | **PATCH** /api/v1/entities/userGroups/{id} | Patch UserGroup entity
[**update_entity_user_groups**](UserGroupsEntityAPIsApi.md#update_entity_user_groups) | **PUT** /api/v1/entities/userGroups/{id} | Put UserGroup entity


# **create_entity_user_groups**
> JsonApiUserGroupOutDocument create_entity_user_groups(json_api_user_group_in_document)

Post User Group entities

User Group - creates tree-like structure for categorizing users

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_groups_entity_apis_api
from gooddata_api_client.model.json_api_user_group_in_document import JsonApiUserGroupInDocument
from gooddata_api_client.model.json_api_user_group_out_document import JsonApiUserGroupOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_groups_entity_apis_api.UserGroupsEntityAPIsApi(api_client)
    json_api_user_group_in_document = JsonApiUserGroupInDocument(
        data=JsonApiUserGroupIn(
            attributes=JsonApiUserGroupInAttributes(
                name="name_example",
            ),
            id="id1",
            relationships=JsonApiUserGroupInRelationships(
                parents=JsonApiUserGroupInRelationshipsParents(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        ),
                    ]),
                ),
            ),
            type="userGroup",
        ),
    ) # JsonApiUserGroupInDocument | 
    include = [
        "include=parents",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post User Group entities
        api_response = api_instance.create_entity_user_groups(json_api_user_group_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserGroupsEntityAPIsApi->create_entity_user_groups: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post User Group entities
        api_response = api_instance.create_entity_user_groups(json_api_user_group_in_document, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserGroupsEntityAPIsApi->create_entity_user_groups: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_user_group_in_document** | [**JsonApiUserGroupInDocument**](JsonApiUserGroupInDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiUserGroupOutDocument**](JsonApiUserGroupOutDocument.md)

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

# **delete_entity_user_groups**
> delete_entity_user_groups(id)

Delete UserGroup entity

User Group - creates tree-like structure for categorizing users

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_groups_entity_apis_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_groups_entity_apis_api.UserGroupsEntityAPIsApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=name==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete UserGroup entity
        api_instance.delete_entity_user_groups(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserGroupsEntityAPIsApi->delete_entity_user_groups: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete UserGroup entity
        api_instance.delete_entity_user_groups(id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserGroupsEntityAPIsApi->delete_entity_user_groups: %s\n" % e)
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

# **get_all_entities_user_groups**
> JsonApiUserGroupOutList get_all_entities_user_groups()

Get UserGroup entities

User Group - creates tree-like structure for categorizing users

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_groups_entity_apis_api
from gooddata_api_client.model.json_api_user_group_out_list import JsonApiUserGroupOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_groups_entity_apis_api.UserGroupsEntityAPIsApi(api_client)
    filter = "filter=name==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=parents",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get UserGroup entities
        api_response = api_instance.get_all_entities_user_groups(filter=filter, include=include, page=page, size=size, sort=sort)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserGroupsEntityAPIsApi->get_all_entities_user_groups: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]

### Return type

[**JsonApiUserGroupOutList**](JsonApiUserGroupOutList.md)

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

# **get_entity_user_groups**
> JsonApiUserGroupOutDocument get_entity_user_groups(id)

Get UserGroup entity

User Group - creates tree-like structure for categorizing users

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_groups_entity_apis_api
from gooddata_api_client.model.json_api_user_group_out_document import JsonApiUserGroupOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_groups_entity_apis_api.UserGroupsEntityAPIsApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=name==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=parents",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get UserGroup entity
        api_response = api_instance.get_entity_user_groups(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserGroupsEntityAPIsApi->get_entity_user_groups: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get UserGroup entity
        api_response = api_instance.get_entity_user_groups(id, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserGroupsEntityAPIsApi->get_entity_user_groups: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiUserGroupOutDocument**](JsonApiUserGroupOutDocument.md)

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

# **patch_entity_user_groups**
> JsonApiUserGroupOutDocument patch_entity_user_groups(id, json_api_user_group_patch_document)

Patch UserGroup entity

User Group - creates tree-like structure for categorizing users

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_groups_entity_apis_api
from gooddata_api_client.model.json_api_user_group_out_document import JsonApiUserGroupOutDocument
from gooddata_api_client.model.json_api_user_group_patch_document import JsonApiUserGroupPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_groups_entity_apis_api.UserGroupsEntityAPIsApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_user_group_patch_document = JsonApiUserGroupPatchDocument(
        data=JsonApiUserGroupPatch(
            attributes=JsonApiUserGroupInAttributes(
                name="name_example",
            ),
            id="id1",
            relationships=JsonApiUserGroupInRelationships(
                parents=JsonApiUserGroupInRelationshipsParents(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        ),
                    ]),
                ),
            ),
            type="userGroup",
        ),
    ) # JsonApiUserGroupPatchDocument | 
    filter = "filter=name==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=parents",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch UserGroup entity
        api_response = api_instance.patch_entity_user_groups(id, json_api_user_group_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserGroupsEntityAPIsApi->patch_entity_user_groups: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch UserGroup entity
        api_response = api_instance.patch_entity_user_groups(id, json_api_user_group_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserGroupsEntityAPIsApi->patch_entity_user_groups: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_user_group_patch_document** | [**JsonApiUserGroupPatchDocument**](JsonApiUserGroupPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiUserGroupOutDocument**](JsonApiUserGroupOutDocument.md)

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

# **update_entity_user_groups**
> JsonApiUserGroupOutDocument update_entity_user_groups(id, json_api_user_group_in_document)

Put UserGroup entity

User Group - creates tree-like structure for categorizing users

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_groups_entity_apis_api
from gooddata_api_client.model.json_api_user_group_in_document import JsonApiUserGroupInDocument
from gooddata_api_client.model.json_api_user_group_out_document import JsonApiUserGroupOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_groups_entity_apis_api.UserGroupsEntityAPIsApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_user_group_in_document = JsonApiUserGroupInDocument(
        data=JsonApiUserGroupIn(
            attributes=JsonApiUserGroupInAttributes(
                name="name_example",
            ),
            id="id1",
            relationships=JsonApiUserGroupInRelationships(
                parents=JsonApiUserGroupInRelationshipsParents(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        ),
                    ]),
                ),
            ),
            type="userGroup",
        ),
    ) # JsonApiUserGroupInDocument | 
    filter = "filter=name==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=parents",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put UserGroup entity
        api_response = api_instance.update_entity_user_groups(id, json_api_user_group_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserGroupsEntityAPIsApi->update_entity_user_groups: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put UserGroup entity
        api_response = api_instance.update_entity_user_groups(id, json_api_user_group_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserGroupsEntityAPIsApi->update_entity_user_groups: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_user_group_in_document** | [**JsonApiUserGroupInDocument**](JsonApiUserGroupInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiUserGroupOutDocument**](JsonApiUserGroupOutDocument.md)

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


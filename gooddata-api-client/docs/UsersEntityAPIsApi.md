# gooddata_api_client.UsersEntityAPIsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_users**](UsersEntityAPIsApi.md#create_entity_users) | **POST** /api/v1/entities/users | Post User entities
[**delete_entity_users**](UsersEntityAPIsApi.md#delete_entity_users) | **DELETE** /api/v1/entities/users/{id} | Delete User entity
[**get_all_entities_users**](UsersEntityAPIsApi.md#get_all_entities_users) | **GET** /api/v1/entities/users | Get User entities
[**get_entity_users**](UsersEntityAPIsApi.md#get_entity_users) | **GET** /api/v1/entities/users/{id} | Get User entity
[**patch_entity_users**](UsersEntityAPIsApi.md#patch_entity_users) | **PATCH** /api/v1/entities/users/{id} | Patch User entity
[**update_entity_users**](UsersEntityAPIsApi.md#update_entity_users) | **PUT** /api/v1/entities/users/{id} | Put User entity


# **create_entity_users**
> JsonApiUserOutDocument create_entity_users(json_api_user_in_document)

Post User entities

User - represents entity interacting with platform

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import users_entity_apis_api
from gooddata_api_client.model.json_api_user_in_document import JsonApiUserInDocument
from gooddata_api_client.model.json_api_user_out_document import JsonApiUserOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = users_entity_apis_api.UsersEntityAPIsApi(api_client)
    json_api_user_in_document = JsonApiUserInDocument(
        data=JsonApiUserIn(
            attributes=JsonApiUserInAttributes(
                authentication_id="authentication_id_example",
                email="email_example",
                firstname="firstname_example",
                lastname="lastname_example",
            ),
            id="id1",
            relationships=JsonApiUserInRelationships(
                user_groups=JsonApiUserGroupInRelationshipsParents(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        ),
                    ]),
                ),
            ),
            type="user",
        ),
    ) # JsonApiUserInDocument | 
    include = [
        "include=userGroups",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post User entities
        api_response = api_instance.create_entity_users(json_api_user_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UsersEntityAPIsApi->create_entity_users: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post User entities
        api_response = api_instance.create_entity_users(json_api_user_in_document, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UsersEntityAPIsApi->create_entity_users: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_user_in_document** | [**JsonApiUserInDocument**](JsonApiUserInDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiUserOutDocument**](JsonApiUserOutDocument.md)

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

# **delete_entity_users**
> delete_entity_users(id)

Delete User entity

User - represents entity interacting with platform

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import users_entity_apis_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = users_entity_apis_api.UsersEntityAPIsApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=authenticationId==someString;firstname==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete User entity
        api_instance.delete_entity_users(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UsersEntityAPIsApi->delete_entity_users: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete User entity
        api_instance.delete_entity_users(id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UsersEntityAPIsApi->delete_entity_users: %s\n" % e)
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

# **get_all_entities_users**
> JsonApiUserOutList get_all_entities_users()

Get User entities

User - represents entity interacting with platform

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import users_entity_apis_api
from gooddata_api_client.model.json_api_user_out_list import JsonApiUserOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = users_entity_apis_api.UsersEntityAPIsApi(api_client)
    filter = "filter=authenticationId==someString;firstname==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=userGroups",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get User entities
        api_response = api_instance.get_all_entities_users(filter=filter, include=include, page=page, size=size, sort=sort)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UsersEntityAPIsApi->get_all_entities_users: %s\n" % e)
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

[**JsonApiUserOutList**](JsonApiUserOutList.md)

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

# **get_entity_users**
> JsonApiUserOutDocument get_entity_users(id)

Get User entity

User - represents entity interacting with platform

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import users_entity_apis_api
from gooddata_api_client.model.json_api_user_out_document import JsonApiUserOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = users_entity_apis_api.UsersEntityAPIsApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=authenticationId==someString;firstname==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=userGroups",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get User entity
        api_response = api_instance.get_entity_users(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UsersEntityAPIsApi->get_entity_users: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get User entity
        api_response = api_instance.get_entity_users(id, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UsersEntityAPIsApi->get_entity_users: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiUserOutDocument**](JsonApiUserOutDocument.md)

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

# **patch_entity_users**
> JsonApiUserOutDocument patch_entity_users(id, json_api_user_patch_document)

Patch User entity

User - represents entity interacting with platform

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import users_entity_apis_api
from gooddata_api_client.model.json_api_user_out_document import JsonApiUserOutDocument
from gooddata_api_client.model.json_api_user_patch_document import JsonApiUserPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = users_entity_apis_api.UsersEntityAPIsApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_user_patch_document = JsonApiUserPatchDocument(
        data=JsonApiUserPatch(
            attributes=JsonApiUserInAttributes(
                authentication_id="authentication_id_example",
                email="email_example",
                firstname="firstname_example",
                lastname="lastname_example",
            ),
            id="id1",
            relationships=JsonApiUserInRelationships(
                user_groups=JsonApiUserGroupInRelationshipsParents(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        ),
                    ]),
                ),
            ),
            type="user",
        ),
    ) # JsonApiUserPatchDocument | 
    filter = "filter=authenticationId==someString;firstname==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=userGroups",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch User entity
        api_response = api_instance.patch_entity_users(id, json_api_user_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UsersEntityAPIsApi->patch_entity_users: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch User entity
        api_response = api_instance.patch_entity_users(id, json_api_user_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UsersEntityAPIsApi->patch_entity_users: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_user_patch_document** | [**JsonApiUserPatchDocument**](JsonApiUserPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiUserOutDocument**](JsonApiUserOutDocument.md)

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

# **update_entity_users**
> JsonApiUserOutDocument update_entity_users(id, json_api_user_in_document)

Put User entity

User - represents entity interacting with platform

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import users_entity_apis_api
from gooddata_api_client.model.json_api_user_in_document import JsonApiUserInDocument
from gooddata_api_client.model.json_api_user_out_document import JsonApiUserOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = users_entity_apis_api.UsersEntityAPIsApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_user_in_document = JsonApiUserInDocument(
        data=JsonApiUserIn(
            attributes=JsonApiUserInAttributes(
                authentication_id="authentication_id_example",
                email="email_example",
                firstname="firstname_example",
                lastname="lastname_example",
            ),
            id="id1",
            relationships=JsonApiUserInRelationships(
                user_groups=JsonApiUserGroupInRelationshipsParents(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        ),
                    ]),
                ),
            ),
            type="user",
        ),
    ) # JsonApiUserInDocument | 
    filter = "filter=authenticationId==someString;firstname==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=userGroups",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put User entity
        api_response = api_instance.update_entity_users(id, json_api_user_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UsersEntityAPIsApi->update_entity_users: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put User entity
        api_response = api_instance.update_entity_users(id, json_api_user_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UsersEntityAPIsApi->update_entity_users: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_user_in_document** | [**JsonApiUserInDocument**](JsonApiUserInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiUserOutDocument**](JsonApiUserOutDocument.md)

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


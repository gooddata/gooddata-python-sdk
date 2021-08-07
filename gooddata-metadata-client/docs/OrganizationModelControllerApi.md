# gooddata_metadata_client.OrganizationModelControllerApi

All URIs are relative to *https://staging.anywhere.gooddata.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_acls**](OrganizationModelControllerApi.md#create_entity_acls) | **POST** /api/entities/acls | 
[**create_entity_data_sources**](OrganizationModelControllerApi.md#create_entity_data_sources) | **POST** /api/entities/dataSources | 
[**create_entity_user_groups**](OrganizationModelControllerApi.md#create_entity_user_groups) | **POST** /api/entities/userGroups | 
[**create_entity_users**](OrganizationModelControllerApi.md#create_entity_users) | **POST** /api/entities/users | 
[**create_entity_workspaces**](OrganizationModelControllerApi.md#create_entity_workspaces) | **POST** /api/entities/workspaces | 
[**delete_entity_acls**](OrganizationModelControllerApi.md#delete_entity_acls) | **DELETE** /api/entities/acls/{id} | 
[**delete_entity_data_sources**](OrganizationModelControllerApi.md#delete_entity_data_sources) | **DELETE** /api/entities/dataSources/{id} | 
[**delete_entity_user_groups**](OrganizationModelControllerApi.md#delete_entity_user_groups) | **DELETE** /api/entities/userGroups/{id} | 
[**delete_entity_users**](OrganizationModelControllerApi.md#delete_entity_users) | **DELETE** /api/entities/users/{id} | 
[**delete_entity_workspaces**](OrganizationModelControllerApi.md#delete_entity_workspaces) | **DELETE** /api/entities/workspaces/{id} | 
[**get_all_entities_acls**](OrganizationModelControllerApi.md#get_all_entities_acls) | **GET** /api/entities/acls | 
[**get_all_entities_data_sources**](OrganizationModelControllerApi.md#get_all_entities_data_sources) | **GET** /api/entities/dataSources | 
[**get_all_entities_user_groups**](OrganizationModelControllerApi.md#get_all_entities_user_groups) | **GET** /api/entities/userGroups | 
[**get_all_entities_users**](OrganizationModelControllerApi.md#get_all_entities_users) | **GET** /api/entities/users | 
[**get_all_entities_workspaces**](OrganizationModelControllerApi.md#get_all_entities_workspaces) | **GET** /api/entities/workspaces | 
[**get_entity_acls**](OrganizationModelControllerApi.md#get_entity_acls) | **GET** /api/entities/acls/{id} | 
[**get_entity_data_sources**](OrganizationModelControllerApi.md#get_entity_data_sources) | **GET** /api/entities/dataSources/{id} | 
[**get_entity_user_groups**](OrganizationModelControllerApi.md#get_entity_user_groups) | **GET** /api/entities/userGroups/{id} | 
[**get_entity_users**](OrganizationModelControllerApi.md#get_entity_users) | **GET** /api/entities/users/{id} | 
[**get_entity_workspaces**](OrganizationModelControllerApi.md#get_entity_workspaces) | **GET** /api/entities/workspaces/{id} | 
[**update_entity_acls**](OrganizationModelControllerApi.md#update_entity_acls) | **PUT** /api/entities/acls/{id} | 
[**update_entity_data_sources**](OrganizationModelControllerApi.md#update_entity_data_sources) | **PUT** /api/entities/dataSources/{id} | 
[**update_entity_user_groups**](OrganizationModelControllerApi.md#update_entity_user_groups) | **PUT** /api/entities/userGroups/{id} | 
[**update_entity_users**](OrganizationModelControllerApi.md#update_entity_users) | **PUT** /api/entities/users/{id} | 
[**update_entity_workspaces**](OrganizationModelControllerApi.md#update_entity_workspaces) | **PUT** /api/entities/workspaces/{id} | 


# **create_entity_acls**
> JsonApiACLOutDocument create_entity_acls(json_api_aclin_document)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_model_controller_api
from gooddata_metadata_client.model.json_api_aclin_document import JsonApiACLInDocument
from gooddata_metadata_client.model.json_api_acl_out_document import JsonApiACLOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)
    json_api_aclin_document = JsonApiACLInDocument(
        data=JsonApiACLIn(
            type="acl",
            id="id1",
            attributes=JsonApiACLOutAttributes(
                access="FULL_ACCESS",
                priority=1,
                control="ALLOW",
            ),
            relationships=JsonApiACLOutRelationships(
                subjects=JsonApiACLOutRelationshipsSubjects(
                    data=JsonApiUserToManyLinkage([
                        JsonApiUserLinkage(
                            id="id_example",
                            type="user",
                        ),
                    ]),
                ),
                objects=JsonApiACLOutRelationshipsObjects(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        ),
                    ]),
                ),
            ),
        ),
    ) # JsonApiACLInDocument | 
    include = [
        "include=subjects,objects",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_entity_acls(json_api_aclin_document)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_acls: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.create_entity_acls(json_api_aclin_document, include=include)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_acls: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_aclin_document** | [**JsonApiACLInDocument**](JsonApiACLInDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiACLOutDocument**](JsonApiACLOutDocument.md)

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

# **create_entity_data_sources**
> JsonApiDataSourceOutDocument create_entity_data_sources(json_api_data_source_in_document)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_model_controller_api
from gooddata_metadata_client.model.json_api_data_source_out_document import JsonApiDataSourceOutDocument
from gooddata_metadata_client.model.json_api_data_source_in_document import JsonApiDataSourceInDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)
    json_api_data_source_in_document = JsonApiDataSourceInDocument(
        data=JsonApiDataSourceIn(
            type="dataSource",
            id="id1",
            attributes=JsonApiDataSourceInAttributes(
                name="name_example",
                type="POSTGRESQL",
                url="url_example",
                schema="schema_example",
                username="username_example",
                password="password_example",
                token="token_example",
            ),
        ),
    ) # JsonApiDataSourceInDocument | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_entity_data_sources(json_api_data_source_in_document)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_data_sources: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_data_source_in_document** | [**JsonApiDataSourceInDocument**](JsonApiDataSourceInDocument.md)|  |

### Return type

[**JsonApiDataSourceOutDocument**](JsonApiDataSourceOutDocument.md)

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

# **create_entity_user_groups**
> JsonApiUserGroupOutDocument create_entity_user_groups(json_api_user_group_in_document)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_model_controller_api
from gooddata_metadata_client.model.json_api_user_group_out_document import JsonApiUserGroupOutDocument
from gooddata_metadata_client.model.json_api_user_group_in_document import JsonApiUserGroupInDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)
    json_api_user_group_in_document = JsonApiUserGroupInDocument(
        data=JsonApiUserGroupIn(
            type="userGroup",
            id="id1",
            relationships=JsonApiUserGroupOutRelationships(
                parents=JsonApiACLOutRelationshipsObjects(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        ),
                    ]),
                ),
            ),
        ),
    ) # JsonApiUserGroupInDocument | 
    include = [
        "include=parents",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_entity_user_groups(json_api_user_group_in_document)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_user_groups: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.create_entity_user_groups(json_api_user_group_in_document, include=include)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_user_groups: %s\n" % e)
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

# **create_entity_users**
> JsonApiUserOutDocument create_entity_users(json_api_user_in_document)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_model_controller_api
from gooddata_metadata_client.model.json_api_user_out_document import JsonApiUserOutDocument
from gooddata_metadata_client.model.json_api_user_in_document import JsonApiUserInDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)
    json_api_user_in_document = JsonApiUserInDocument(
        data=JsonApiUserIn(
            type="user",
            id="id1",
            attributes=JsonApiUserOutAttributes(
                authentication_id="authentication_id_example",
            ),
            relationships=JsonApiUserOutRelationships(
                user_groups=JsonApiACLOutRelationshipsObjects(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        ),
                    ]),
                ),
            ),
        ),
    ) # JsonApiUserInDocument | 
    include = [
        "include=userGroups",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_entity_users(json_api_user_in_document)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_users: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.create_entity_users(json_api_user_in_document, include=include)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_users: %s\n" % e)
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

# **create_entity_workspaces**
> JsonApiWorkspaceOutDocument create_entity_workspaces(json_api_workspace_in_document)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_model_controller_api
from gooddata_metadata_client.model.json_api_workspace_out_document import JsonApiWorkspaceOutDocument
from gooddata_metadata_client.model.json_api_workspace_in_document import JsonApiWorkspaceInDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)
    json_api_workspace_in_document = JsonApiWorkspaceInDocument(
        data=JsonApiWorkspaceIn(
            type="workspace",
            id="id1",
            attributes=JsonApiWorkspaceOutAttributes(
                name="name_example",
            ),
            relationships=JsonApiWorkspaceOutRelationships(
                parent=JsonApiWorkspaceOutRelationshipsParent(
                    data=JsonApiWorkspaceToOneLinkage(),
                ),
            ),
        ),
    ) # JsonApiWorkspaceInDocument | 
    include = [
        "include=parent",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_entity_workspaces(json_api_workspace_in_document)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_workspaces: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.create_entity_workspaces(json_api_workspace_in_document, include=include)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_workspaces: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_workspace_in_document** | [**JsonApiWorkspaceInDocument**](JsonApiWorkspaceInDocument.md)|  |
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
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_acls**
> delete_entity_acls(id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_model_controller_api
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)
    id = "26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1RA89q3w1l4eH4XxEz.5awxoFZxHzs6ED.kjUSnTINkYPUndNl8pmPg5K897Fu1JEFj9R1_dz9rEoBi0LnU8SsOWJ7wYrcziVQdt8mVLxbg4bCLrLBcmXxWQK6MzKSg5jphei0IfRRwpnT_Z.qKa_YppZepezJ0.VmLSUTLYyW" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=access==ACLAccessValue;priority==123" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_entity_acls(id)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_acls: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_instance.delete_entity_acls(id, predicate=predicate, filter=filter)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_acls: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]

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

# **delete_entity_data_sources**
> delete_entity_data_sources(id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_model_controller_api
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)
    id = "26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1RA89q3w1l4eH4XxEz.5awxoFZxHzs6ED.kjUSnTINkYPUndNl8pmPg5K897Fu1JEFj9R1_dz9rEoBi0LnU8SsOWJ7wYrcziVQdt8mVLxbg4bCLrLBcmXxWQK6MzKSg5jphei0IfRRwpnT_Z.qKa_YppZepezJ0.VmLSUTLYyW" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=name==someString;type==DatabaseTypeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_entity_data_sources(id)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_data_sources: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_instance.delete_entity_data_sources(id, predicate=predicate, filter=filter)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_data_sources: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]

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

# **delete_entity_user_groups**
> delete_entity_user_groups(id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_model_controller_api
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)
    id = "26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1RA89q3w1l4eH4XxEz.5awxoFZxHzs6ED.kjUSnTINkYPUndNl8pmPg5K897Fu1JEFj9R1_dz9rEoBi0LnU8SsOWJ7wYrcziVQdt8mVLxbg4bCLrLBcmXxWQK6MzKSg5jphei0IfRRwpnT_Z.qKa_YppZepezJ0.VmLSUTLYyW" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_entity_user_groups(id)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_user_groups: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_instance.delete_entity_user_groups(id, predicate=predicate, filter=filter)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_user_groups: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]

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

# **delete_entity_users**
> delete_entity_users(id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_model_controller_api
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)
    id = "26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1RA89q3w1l4eH4XxEz.5awxoFZxHzs6ED.kjUSnTINkYPUndNl8pmPg5K897Fu1JEFj9R1_dz9rEoBi0LnU8SsOWJ7wYrcziVQdt8mVLxbg4bCLrLBcmXxWQK6MzKSg5jphei0IfRRwpnT_Z.qKa_YppZepezJ0.VmLSUTLYyW" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=authenticationId==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_entity_users(id)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_users: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_instance.delete_entity_users(id, predicate=predicate, filter=filter)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_users: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]

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

# **delete_entity_workspaces**
> delete_entity_workspaces(id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_model_controller_api
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)
    id = "26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1RA89q3w1l4eH4XxEz.5awxoFZxHzs6ED.kjUSnTINkYPUndNl8pmPg5K897Fu1JEFj9R1_dz9rEoBi0LnU8SsOWJ7wYrcziVQdt8mVLxbg4bCLrLBcmXxWQK6MzKSg5jphei0IfRRwpnT_Z.qKa_YppZepezJ0.VmLSUTLYyW" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=name==someString;parent.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_entity_workspaces(id)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_workspaces: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_instance.delete_entity_workspaces(id, predicate=predicate, filter=filter)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_workspaces: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]

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

# **get_all_entities_acls**
> JsonApiACLOutList get_all_entities_acls()



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_model_controller_api
from gooddata_metadata_client.model.json_api_acl_out_list import JsonApiACLOutList
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=access==ACLAccessValue;priority==123" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=subjects,objects",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_all_entities_acls(predicate=predicate, filter=filter, include=include, page=page, size=size, sort=sort)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_acls: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]

### Return type

[**JsonApiACLOutList**](JsonApiACLOutList.md)

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

# **get_all_entities_data_sources**
> JsonApiDataSourceOutList get_all_entities_data_sources()



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_model_controller_api
from gooddata_metadata_client.model.json_api_data_source_out_list import JsonApiDataSourceOutList
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=name==someString;type==DatabaseTypeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_all_entities_data_sources(predicate=predicate, filter=filter, page=page, size=size, sort=sort)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_data_sources: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]

### Return type

[**JsonApiDataSourceOutList**](JsonApiDataSourceOutList.md)

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

# **get_all_entities_user_groups**
> JsonApiUserGroupOutList get_all_entities_user_groups()



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_model_controller_api
from gooddata_metadata_client.model.json_api_user_group_out_list import JsonApiUserGroupOutList
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=parents",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_all_entities_user_groups(predicate=predicate, filter=filter, include=include, page=page, size=size, sort=sort)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_user_groups: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]

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

# **get_all_entities_users**
> JsonApiUserOutList get_all_entities_users()



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_model_controller_api
from gooddata_metadata_client.model.json_api_user_out_list import JsonApiUserOutList
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=authenticationId==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=userGroups",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_all_entities_users(predicate=predicate, filter=filter, include=include, page=page, size=size, sort=sort)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_users: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]

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

# **get_all_entities_workspaces**
> JsonApiWorkspaceOutList get_all_entities_workspaces()



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_model_controller_api
from gooddata_metadata_client.model.json_api_workspace_out_list import JsonApiWorkspaceOutList
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=name==someString;parent.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=parent",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = [
        "metaInclude=config,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_all_entities_workspaces(predicate=predicate, filter=filter, include=include, page=page, size=size, sort=sort, meta_include=meta_include)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_workspaces: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
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

# **get_entity_acls**
> JsonApiACLOutDocument get_entity_acls(id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_model_controller_api
from gooddata_metadata_client.model.json_api_acl_out_document import JsonApiACLOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)
    id = "26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1RA89q3w1l4eH4XxEz.5awxoFZxHzs6ED.kjUSnTINkYPUndNl8pmPg5K897Fu1JEFj9R1_dz9rEoBi0LnU8SsOWJ7wYrcziVQdt8mVLxbg4bCLrLBcmXxWQK6MzKSg5jphei0IfRRwpnT_Z.qKa_YppZepezJ0.VmLSUTLYyW" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=access==ACLAccessValue;priority==123" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=subjects,objects",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_entity_acls(id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_acls: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_entity_acls(id, predicate=predicate, filter=filter, include=include)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_acls: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiACLOutDocument**](JsonApiACLOutDocument.md)

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

# **get_entity_data_sources**
> JsonApiDataSourceOutDocument get_entity_data_sources(id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_model_controller_api
from gooddata_metadata_client.model.json_api_data_source_out_document import JsonApiDataSourceOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)
    id = "26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1RA89q3w1l4eH4XxEz.5awxoFZxHzs6ED.kjUSnTINkYPUndNl8pmPg5K897Fu1JEFj9R1_dz9rEoBi0LnU8SsOWJ7wYrcziVQdt8mVLxbg4bCLrLBcmXxWQK6MzKSg5jphei0IfRRwpnT_Z.qKa_YppZepezJ0.VmLSUTLYyW" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=name==someString;type==DatabaseTypeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_entity_data_sources(id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_data_sources: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_entity_data_sources(id, predicate=predicate, filter=filter)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_data_sources: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]

### Return type

[**JsonApiDataSourceOutDocument**](JsonApiDataSourceOutDocument.md)

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



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_model_controller_api
from gooddata_metadata_client.model.json_api_user_group_out_document import JsonApiUserGroupOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)
    id = "26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1RA89q3w1l4eH4XxEz.5awxoFZxHzs6ED.kjUSnTINkYPUndNl8pmPg5K897Fu1JEFj9R1_dz9rEoBi0LnU8SsOWJ7wYrcziVQdt8mVLxbg4bCLrLBcmXxWQK6MzKSg5jphei0IfRRwpnT_Z.qKa_YppZepezJ0.VmLSUTLYyW" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=parents",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_entity_user_groups(id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_user_groups: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_entity_user_groups(id, predicate=predicate, filter=filter, include=include)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_user_groups: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
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

# **get_entity_users**
> JsonApiUserOutDocument get_entity_users(id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_model_controller_api
from gooddata_metadata_client.model.json_api_user_out_document import JsonApiUserOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)
    id = "26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1RA89q3w1l4eH4XxEz.5awxoFZxHzs6ED.kjUSnTINkYPUndNl8pmPg5K897Fu1JEFj9R1_dz9rEoBi0LnU8SsOWJ7wYrcziVQdt8mVLxbg4bCLrLBcmXxWQK6MzKSg5jphei0IfRRwpnT_Z.qKa_YppZepezJ0.VmLSUTLYyW" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=authenticationId==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=userGroups",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_entity_users(id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_users: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_entity_users(id, predicate=predicate, filter=filter, include=include)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_users: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
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

# **get_entity_workspaces**
> JsonApiWorkspaceOutDocument get_entity_workspaces(id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_model_controller_api
from gooddata_metadata_client.model.json_api_workspace_out_document import JsonApiWorkspaceOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)
    id = "26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1RA89q3w1l4eH4XxEz.5awxoFZxHzs6ED.kjUSnTINkYPUndNl8pmPg5K897Fu1JEFj9R1_dz9rEoBi0LnU8SsOWJ7wYrcziVQdt8mVLxbg4bCLrLBcmXxWQK6MzKSg5jphei0IfRRwpnT_Z.qKa_YppZepezJ0.VmLSUTLYyW" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=name==someString;parent.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=parent",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = [
        "metaInclude=config,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_entity_workspaces(id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_workspaces: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_entity_workspaces(id, predicate=predicate, filter=filter, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_workspaces: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
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

# **update_entity_acls**
> JsonApiACLOutDocument update_entity_acls(id, json_api_aclin_document)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_model_controller_api
from gooddata_metadata_client.model.json_api_aclin_document import JsonApiACLInDocument
from gooddata_metadata_client.model.json_api_acl_out_document import JsonApiACLOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)
    id = "26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1RA89q3w1l4eH4XxEz.5awxoFZxHzs6ED.kjUSnTINkYPUndNl8pmPg5K897Fu1JEFj9R1_dz9rEoBi0LnU8SsOWJ7wYrcziVQdt8mVLxbg4bCLrLBcmXxWQK6MzKSg5jphei0IfRRwpnT_Z.qKa_YppZepezJ0.VmLSUTLYyW" # str | 
    json_api_aclin_document = JsonApiACLInDocument(
        data=JsonApiACLIn(
            type="acl",
            id="id1",
            attributes=JsonApiACLOutAttributes(
                access="FULL_ACCESS",
                priority=1,
                control="ALLOW",
            ),
            relationships=JsonApiACLOutRelationships(
                subjects=JsonApiACLOutRelationshipsSubjects(
                    data=JsonApiUserToManyLinkage([
                        JsonApiUserLinkage(
                            id="id_example",
                            type="user",
                        ),
                    ]),
                ),
                objects=JsonApiACLOutRelationshipsObjects(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        ),
                    ]),
                ),
            ),
        ),
    ) # JsonApiACLInDocument | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=access==ACLAccessValue;priority==123" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=subjects,objects",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_entity_acls(id, json_api_aclin_document)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_acls: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.update_entity_acls(id, json_api_aclin_document, predicate=predicate, filter=filter, include=include)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_acls: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_aclin_document** | [**JsonApiACLInDocument**](JsonApiACLInDocument.md)|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiACLOutDocument**](JsonApiACLOutDocument.md)

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

# **update_entity_data_sources**
> JsonApiDataSourceOutDocument update_entity_data_sources(id, json_api_data_source_in_document)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_model_controller_api
from gooddata_metadata_client.model.json_api_data_source_out_document import JsonApiDataSourceOutDocument
from gooddata_metadata_client.model.json_api_data_source_in_document import JsonApiDataSourceInDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)
    id = "26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1RA89q3w1l4eH4XxEz.5awxoFZxHzs6ED.kjUSnTINkYPUndNl8pmPg5K897Fu1JEFj9R1_dz9rEoBi0LnU8SsOWJ7wYrcziVQdt8mVLxbg4bCLrLBcmXxWQK6MzKSg5jphei0IfRRwpnT_Z.qKa_YppZepezJ0.VmLSUTLYyW" # str | 
    json_api_data_source_in_document = JsonApiDataSourceInDocument(
        data=JsonApiDataSourceIn(
            type="dataSource",
            id="id1",
            attributes=JsonApiDataSourceInAttributes(
                name="name_example",
                type="POSTGRESQL",
                url="url_example",
                schema="schema_example",
                username="username_example",
                password="password_example",
                token="token_example",
            ),
        ),
    ) # JsonApiDataSourceInDocument | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=name==someString;type==DatabaseTypeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_entity_data_sources(id, json_api_data_source_in_document)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_data_sources: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.update_entity_data_sources(id, json_api_data_source_in_document, predicate=predicate, filter=filter)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_data_sources: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_data_source_in_document** | [**JsonApiDataSourceInDocument**](JsonApiDataSourceInDocument.md)|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]

### Return type

[**JsonApiDataSourceOutDocument**](JsonApiDataSourceOutDocument.md)

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



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_model_controller_api
from gooddata_metadata_client.model.json_api_user_group_out_document import JsonApiUserGroupOutDocument
from gooddata_metadata_client.model.json_api_user_group_in_document import JsonApiUserGroupInDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)
    id = "26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1RA89q3w1l4eH4XxEz.5awxoFZxHzs6ED.kjUSnTINkYPUndNl8pmPg5K897Fu1JEFj9R1_dz9rEoBi0LnU8SsOWJ7wYrcziVQdt8mVLxbg4bCLrLBcmXxWQK6MzKSg5jphei0IfRRwpnT_Z.qKa_YppZepezJ0.VmLSUTLYyW" # str | 
    json_api_user_group_in_document = JsonApiUserGroupInDocument(
        data=JsonApiUserGroupIn(
            type="userGroup",
            id="id1",
            relationships=JsonApiUserGroupOutRelationships(
                parents=JsonApiACLOutRelationshipsObjects(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        ),
                    ]),
                ),
            ),
        ),
    ) # JsonApiUserGroupInDocument | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=parents",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_entity_user_groups(id, json_api_user_group_in_document)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_user_groups: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.update_entity_user_groups(id, json_api_user_group_in_document, predicate=predicate, filter=filter, include=include)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_user_groups: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_user_group_in_document** | [**JsonApiUserGroupInDocument**](JsonApiUserGroupInDocument.md)|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
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

# **update_entity_users**
> JsonApiUserOutDocument update_entity_users(id, json_api_user_in_document)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_model_controller_api
from gooddata_metadata_client.model.json_api_user_out_document import JsonApiUserOutDocument
from gooddata_metadata_client.model.json_api_user_in_document import JsonApiUserInDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)
    id = "26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1RA89q3w1l4eH4XxEz.5awxoFZxHzs6ED.kjUSnTINkYPUndNl8pmPg5K897Fu1JEFj9R1_dz9rEoBi0LnU8SsOWJ7wYrcziVQdt8mVLxbg4bCLrLBcmXxWQK6MzKSg5jphei0IfRRwpnT_Z.qKa_YppZepezJ0.VmLSUTLYyW" # str | 
    json_api_user_in_document = JsonApiUserInDocument(
        data=JsonApiUserIn(
            type="user",
            id="id1",
            attributes=JsonApiUserOutAttributes(
                authentication_id="authentication_id_example",
            ),
            relationships=JsonApiUserOutRelationships(
                user_groups=JsonApiACLOutRelationshipsObjects(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        ),
                    ]),
                ),
            ),
        ),
    ) # JsonApiUserInDocument | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=authenticationId==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=userGroups",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_entity_users(id, json_api_user_in_document)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_users: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.update_entity_users(id, json_api_user_in_document, predicate=predicate, filter=filter, include=include)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_users: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_user_in_document** | [**JsonApiUserInDocument**](JsonApiUserInDocument.md)|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
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

# **update_entity_workspaces**
> JsonApiWorkspaceOutDocument update_entity_workspaces(id, json_api_workspace_in_document)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_model_controller_api
from gooddata_metadata_client.model.json_api_workspace_out_document import JsonApiWorkspaceOutDocument
from gooddata_metadata_client.model.json_api_workspace_in_document import JsonApiWorkspaceInDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)
    id = "26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1RA89q3w1l4eH4XxEz.5awxoFZxHzs6ED.kjUSnTINkYPUndNl8pmPg5K897Fu1JEFj9R1_dz9rEoBi0LnU8SsOWJ7wYrcziVQdt8mVLxbg4bCLrLBcmXxWQK6MzKSg5jphei0IfRRwpnT_Z.qKa_YppZepezJ0.VmLSUTLYyW" # str | 
    json_api_workspace_in_document = JsonApiWorkspaceInDocument(
        data=JsonApiWorkspaceIn(
            type="workspace",
            id="id1",
            attributes=JsonApiWorkspaceOutAttributes(
                name="name_example",
            ),
            relationships=JsonApiWorkspaceOutRelationships(
                parent=JsonApiWorkspaceOutRelationshipsParent(
                    data=JsonApiWorkspaceToOneLinkage(),
                ),
            ),
        ),
    ) # JsonApiWorkspaceInDocument | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=name==someString;parent.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=parent",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_entity_workspaces(id, json_api_workspace_in_document)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_workspaces: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.update_entity_workspaces(id, json_api_workspace_in_document, predicate=predicate, filter=filter, include=include)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_workspaces: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_workspace_in_document** | [**JsonApiWorkspaceInDocument**](JsonApiWorkspaceInDocument.md)|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
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


# gooddata_api_client.IpAllowlistPolicyControllerApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_ip_allowlist_policies**](IpAllowlistPolicyControllerApi.md#create_entity_ip_allowlist_policies) | **POST** /api/v1/entities/ipAllowlistPolicies | Post IpAllowlistPolicy entities
[**delete_entity_ip_allowlist_policies**](IpAllowlistPolicyControllerApi.md#delete_entity_ip_allowlist_policies) | **DELETE** /api/v1/entities/ipAllowlistPolicies/{id} | Delete IpAllowlistPolicy entity
[**get_all_entities_ip_allowlist_policies**](IpAllowlistPolicyControllerApi.md#get_all_entities_ip_allowlist_policies) | **GET** /api/v1/entities/ipAllowlistPolicies | Get all IpAllowlistPolicy entities
[**get_entity_ip_allowlist_policies**](IpAllowlistPolicyControllerApi.md#get_entity_ip_allowlist_policies) | **GET** /api/v1/entities/ipAllowlistPolicies/{id} | Get IpAllowlistPolicy entity
[**update_entity_ip_allowlist_policies**](IpAllowlistPolicyControllerApi.md#update_entity_ip_allowlist_policies) | **PUT** /api/v1/entities/ipAllowlistPolicies/{id} | Put IpAllowlistPolicy entity


# **create_entity_ip_allowlist_policies**
> JsonApiIpAllowlistPolicyOutDocument create_entity_ip_allowlist_policies(json_api_ip_allowlist_policy_in_document)

Post IpAllowlistPolicy entities

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ip_allowlist_policy_controller_api
from gooddata_api_client.model.json_api_ip_allowlist_policy_out_document import JsonApiIpAllowlistPolicyOutDocument
from gooddata_api_client.model.json_api_ip_allowlist_policy_in_document import JsonApiIpAllowlistPolicyInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ip_allowlist_policy_controller_api.IpAllowlistPolicyControllerApi(api_client)
    json_api_ip_allowlist_policy_in_document = JsonApiIpAllowlistPolicyInDocument(
        data=JsonApiIpAllowlistPolicyIn(
            attributes=JsonApiIpAllowlistPolicyInAttributes(
                allowed_sources=[
                    "allowed_sources_example",
                ],
            ),
            id="id1",
            relationships=JsonApiIpAllowlistPolicyInRelationships(
                user_groups=JsonApiAgentInRelationshipsUserGroups(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        ),
                    ]),
                ),
                users=JsonApiAutomationInRelationshipsRecipients(
                    data=JsonApiUserToManyLinkage([
                        JsonApiUserLinkage(
                            id="id_example",
                            type="user",
                        ),
                    ]),
                ),
            ),
            type="ipAllowlistPolicy",
        ),
    ) # JsonApiIpAllowlistPolicyInDocument | 
    include = [
        "users,userGroups",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post IpAllowlistPolicy entities
        api_response = api_instance.create_entity_ip_allowlist_policies(json_api_ip_allowlist_policy_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IpAllowlistPolicyControllerApi->create_entity_ip_allowlist_policies: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post IpAllowlistPolicy entities
        api_response = api_instance.create_entity_ip_allowlist_policies(json_api_ip_allowlist_policy_in_document, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IpAllowlistPolicyControllerApi->create_entity_ip_allowlist_policies: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_ip_allowlist_policy_in_document** | [**JsonApiIpAllowlistPolicyInDocument**](JsonApiIpAllowlistPolicyInDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiIpAllowlistPolicyOutDocument**](JsonApiIpAllowlistPolicyOutDocument.md)

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

# **delete_entity_ip_allowlist_policies**
> delete_entity_ip_allowlist_policies(id)

Delete IpAllowlistPolicy entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ip_allowlist_policy_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ip_allowlist_policy_controller_api.IpAllowlistPolicyControllerApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Delete IpAllowlistPolicy entity
        api_instance.delete_entity_ip_allowlist_policies(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IpAllowlistPolicyControllerApi->delete_entity_ip_allowlist_policies: %s\n" % e)
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

# **get_all_entities_ip_allowlist_policies**
> JsonApiIpAllowlistPolicyOutList get_all_entities_ip_allowlist_policies()

Get all IpAllowlistPolicy entities

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ip_allowlist_policy_controller_api
from gooddata_api_client.model.json_api_ip_allowlist_policy_out_list import JsonApiIpAllowlistPolicyOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ip_allowlist_policy_controller_api.IpAllowlistPolicyControllerApi(api_client)
    filter = "allowedSources==v1,v2,v3" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "users,userGroups",
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
        # Get all IpAllowlistPolicy entities
        api_response = api_instance.get_all_entities_ip_allowlist_policies(filter=filter, include=include, page=page, size=size, sort=sort, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IpAllowlistPolicyControllerApi->get_all_entities_ip_allowlist_policies: %s\n" % e)
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

[**JsonApiIpAllowlistPolicyOutList**](JsonApiIpAllowlistPolicyOutList.md)

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

# **get_entity_ip_allowlist_policies**
> JsonApiIpAllowlistPolicyOutDocument get_entity_ip_allowlist_policies(id)

Get IpAllowlistPolicy entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ip_allowlist_policy_controller_api
from gooddata_api_client.model.json_api_ip_allowlist_policy_out_document import JsonApiIpAllowlistPolicyOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ip_allowlist_policy_controller_api.IpAllowlistPolicyControllerApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "allowedSources==v1,v2,v3" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "users,userGroups",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get IpAllowlistPolicy entity
        api_response = api_instance.get_entity_ip_allowlist_policies(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IpAllowlistPolicyControllerApi->get_entity_ip_allowlist_policies: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get IpAllowlistPolicy entity
        api_response = api_instance.get_entity_ip_allowlist_policies(id, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IpAllowlistPolicyControllerApi->get_entity_ip_allowlist_policies: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiIpAllowlistPolicyOutDocument**](JsonApiIpAllowlistPolicyOutDocument.md)

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

# **update_entity_ip_allowlist_policies**
> JsonApiIpAllowlistPolicyOutDocument update_entity_ip_allowlist_policies(id, json_api_ip_allowlist_policy_in_document)

Put IpAllowlistPolicy entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ip_allowlist_policy_controller_api
from gooddata_api_client.model.json_api_ip_allowlist_policy_out_document import JsonApiIpAllowlistPolicyOutDocument
from gooddata_api_client.model.json_api_ip_allowlist_policy_in_document import JsonApiIpAllowlistPolicyInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ip_allowlist_policy_controller_api.IpAllowlistPolicyControllerApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_ip_allowlist_policy_in_document = JsonApiIpAllowlistPolicyInDocument(
        data=JsonApiIpAllowlistPolicyIn(
            attributes=JsonApiIpAllowlistPolicyInAttributes(
                allowed_sources=[
                    "allowed_sources_example",
                ],
            ),
            id="id1",
            relationships=JsonApiIpAllowlistPolicyInRelationships(
                user_groups=JsonApiAgentInRelationshipsUserGroups(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        ),
                    ]),
                ),
                users=JsonApiAutomationInRelationshipsRecipients(
                    data=JsonApiUserToManyLinkage([
                        JsonApiUserLinkage(
                            id="id_example",
                            type="user",
                        ),
                    ]),
                ),
            ),
            type="ipAllowlistPolicy",
        ),
    ) # JsonApiIpAllowlistPolicyInDocument | 
    filter = "allowedSources==v1,v2,v3" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "users,userGroups",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put IpAllowlistPolicy entity
        api_response = api_instance.update_entity_ip_allowlist_policies(id, json_api_ip_allowlist_policy_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IpAllowlistPolicyControllerApi->update_entity_ip_allowlist_policies: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put IpAllowlistPolicy entity
        api_response = api_instance.update_entity_ip_allowlist_policies(id, json_api_ip_allowlist_policy_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IpAllowlistPolicyControllerApi->update_entity_ip_allowlist_policies: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_ip_allowlist_policy_in_document** | [**JsonApiIpAllowlistPolicyInDocument**](JsonApiIpAllowlistPolicyInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiIpAllowlistPolicyOutDocument**](JsonApiIpAllowlistPolicyOutDocument.md)

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


# gooddata_api_client.HierarchyApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**check_entity_overrides**](HierarchyApi.md#check_entity_overrides) | **POST** /api/v1/actions/workspaces/{workspaceId}/checkEntityOverrides | Finds entities with given ID in hierarchy.
[**inherited_entity_conflicts**](HierarchyApi.md#inherited_entity_conflicts) | **GET** /api/v1/actions/workspaces/{workspaceId}/inheritedEntityConflicts | Finds identifier conflicts in workspace hierarchy.
[**inherited_entity_prefixes**](HierarchyApi.md#inherited_entity_prefixes) | **GET** /api/v1/actions/workspaces/{workspaceId}/inheritedEntityPrefixes | Get used entity prefixes in hierarchy
[**overridden_child_entities**](HierarchyApi.md#overridden_child_entities) | **GET** /api/v1/actions/workspaces/{workspaceId}/overriddenChildEntities | Finds identifier overrides in workspace hierarchy.


# **check_entity_overrides**
> [IdentifierDuplications] check_entity_overrides(workspace_id, hierarchy_object_identification)

Finds entities with given ID in hierarchy.

Finds entities with given ID in hierarchy (e.g. to check possible future conflicts).

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import hierarchy_api
from gooddata_api_client.model.hierarchy_object_identification import HierarchyObjectIdentification
from gooddata_api_client.model.identifier_duplications import IdentifierDuplications
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = hierarchy_api.HierarchyApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    hierarchy_object_identification = [
        HierarchyObjectIdentification(
            id="id_example",
            type="metric",
        ),
    ] # [HierarchyObjectIdentification] | 

    # example passing only required values which don't have defaults set
    try:
        # Finds entities with given ID in hierarchy.
        api_response = api_instance.check_entity_overrides(workspace_id, hierarchy_object_identification)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling HierarchyApi->check_entity_overrides: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **hierarchy_object_identification** | [**[HierarchyObjectIdentification]**](HierarchyObjectIdentification.md)|  |

### Return type

[**[IdentifierDuplications]**](IdentifierDuplications.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Searching for entities finished successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **inherited_entity_conflicts**
> [IdentifierDuplications] inherited_entity_conflicts(workspace_id)

Finds identifier conflicts in workspace hierarchy.

Finds API identifier conflicts in given workspace hierarchy.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import hierarchy_api
from gooddata_api_client.model.identifier_duplications import IdentifierDuplications
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = hierarchy_api.HierarchyApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Finds identifier conflicts in workspace hierarchy.
        api_response = api_instance.inherited_entity_conflicts(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling HierarchyApi->inherited_entity_conflicts: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |

### Return type

[**[IdentifierDuplications]**](IdentifierDuplications.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Searching for conflicting identifiers finished successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **inherited_entity_prefixes**
> [str] inherited_entity_prefixes(workspace_id)

Get used entity prefixes in hierarchy

Get used entity prefixes in hierarchy of parent workspaces

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import hierarchy_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = hierarchy_api.HierarchyApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get used entity prefixes in hierarchy
        api_response = api_instance.inherited_entity_prefixes(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling HierarchyApi->inherited_entity_prefixes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |

### Return type

**[str]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Prefixes used in parent entities |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **overridden_child_entities**
> [IdentifierDuplications] overridden_child_entities(workspace_id)

Finds identifier overrides in workspace hierarchy.

Finds API identifier overrides in given workspace hierarchy.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import hierarchy_api
from gooddata_api_client.model.identifier_duplications import IdentifierDuplications
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = hierarchy_api.HierarchyApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Finds identifier overrides in workspace hierarchy.
        api_response = api_instance.overridden_child_entities(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling HierarchyApi->overridden_child_entities: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |

### Return type

[**[IdentifierDuplications]**](IdentifierDuplications.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Searching for overridden identifiers finished successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


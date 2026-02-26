<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.hierarchy_api.HierarchyApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**check_entity_overrides**](#check_entity_overrides) | **post** /api/v1/actions/workspaces/{workspaceId}/checkEntityOverrides | Finds entities with given ID in hierarchy.
[**inherited_entity_conflicts**](#inherited_entity_conflicts) | **get** /api/v1/actions/workspaces/{workspaceId}/inheritedEntityConflicts | Finds identifier conflicts in workspace hierarchy.
[**inherited_entity_prefixes**](#inherited_entity_prefixes) | **get** /api/v1/actions/workspaces/{workspaceId}/inheritedEntityPrefixes | Get used entity prefixes in hierarchy
[**overridden_child_entities**](#overridden_child_entities) | **get** /api/v1/actions/workspaces/{workspaceId}/overriddenChildEntities | Finds identifier overrides in workspace hierarchy.

# **check_entity_overrides**
<a id="check_entity_overrides"></a>
> [IdentifierDuplications] check_entity_overrides(workspace_idhierarchy_object_identification)

Finds entities with given ID in hierarchy.

Finds entities with given ID in hierarchy (e.g. to check possible future conflicts).

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import hierarchy_api
from gooddata_api_client.model.hierarchy_object_identification import HierarchyObjectIdentification
from gooddata_api_client.model.identifier_duplications import IdentifierDuplications
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hierarchy_api.HierarchyApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    body = [
        HierarchyObjectIdentification(
            id="id_example",
            type="metric",
        )
    ]
    try:
        # Finds entities with given ID in hierarchy.
        api_response = api_instance.check_entity_overrides(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling HierarchyApi->check_entity_overrides: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson

An array of object identifications

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | An array of object identifications | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**HierarchyObjectIdentification**]({{complexTypePrefix}}HierarchyObjectIdentification.md) | [**HierarchyObjectIdentification**]({{complexTypePrefix}}HierarchyObjectIdentification.md) | [**HierarchyObjectIdentification**]({{complexTypePrefix}}HierarchyObjectIdentification.md) |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#check_entity_overrides.ApiResponseFor200) | Searching for entities finished successfully.

#### check_entity_overrides.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**IdentifierDuplications**]({{complexTypePrefix}}IdentifierDuplications.md) | [**IdentifierDuplications**]({{complexTypePrefix}}IdentifierDuplications.md) | [**IdentifierDuplications**]({{complexTypePrefix}}IdentifierDuplications.md) |  | 

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **inherited_entity_conflicts**
<a id="inherited_entity_conflicts"></a>
> [IdentifierDuplications] inherited_entity_conflicts(workspace_id)

Finds identifier conflicts in workspace hierarchy.

Finds API identifier conflicts in given workspace hierarchy.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import hierarchy_api
from gooddata_api_client.model.identifier_duplications import IdentifierDuplications
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hierarchy_api.HierarchyApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    try:
        # Finds identifier conflicts in workspace hierarchy.
        api_response = api_instance.inherited_entity_conflicts(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling HierarchyApi->inherited_entity_conflicts: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#inherited_entity_conflicts.ApiResponseFor200) | Searching for conflicting identifiers finished successfully

#### inherited_entity_conflicts.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**IdentifierDuplications**]({{complexTypePrefix}}IdentifierDuplications.md) | [**IdentifierDuplications**]({{complexTypePrefix}}IdentifierDuplications.md) | [**IdentifierDuplications**]({{complexTypePrefix}}IdentifierDuplications.md) |  | 

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **inherited_entity_prefixes**
<a id="inherited_entity_prefixes"></a>
> [str] inherited_entity_prefixes(workspace_id)

Get used entity prefixes in hierarchy

Get used entity prefixes in hierarchy of parent workspaces

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import hierarchy_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hierarchy_api.HierarchyApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    try:
        # Get used entity prefixes in hierarchy
        api_response = api_instance.inherited_entity_prefixes(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling HierarchyApi->inherited_entity_prefixes: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#inherited_entity_prefixes.ApiResponseFor200) | Prefixes used in parent entities

#### inherited_entity_prefixes.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **overridden_child_entities**
<a id="overridden_child_entities"></a>
> [IdentifierDuplications] overridden_child_entities(workspace_id)

Finds identifier overrides in workspace hierarchy.

Finds API identifier overrides in given workspace hierarchy.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import hierarchy_api
from gooddata_api_client.model.identifier_duplications import IdentifierDuplications
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hierarchy_api.HierarchyApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    try:
        # Finds identifier overrides in workspace hierarchy.
        api_response = api_instance.overridden_child_entities(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling HierarchyApi->overridden_child_entities: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#overridden_child_entities.ApiResponseFor200) | Searching for overridden identifiers finished successfully

#### overridden_child_entities.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**IdentifierDuplications**]({{complexTypePrefix}}IdentifierDuplications.md) | [**IdentifierDuplications**]({{complexTypePrefix}}IdentifierDuplications.md) | [**IdentifierDuplications**]({{complexTypePrefix}}IdentifierDuplications.md) |  | 

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


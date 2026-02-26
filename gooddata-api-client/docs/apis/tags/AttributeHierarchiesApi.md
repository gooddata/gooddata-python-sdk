<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.attribute_hierarchies_api.AttributeHierarchiesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_attribute_hierarchies**](#create_entity_attribute_hierarchies) | **post** /api/v1/entities/workspaces/{workspaceId}/attributeHierarchies | Post Attribute Hierarchies
[**delete_entity_attribute_hierarchies**](#delete_entity_attribute_hierarchies) | **delete** /api/v1/entities/workspaces/{workspaceId}/attributeHierarchies/{objectId} | Delete an Attribute Hierarchy
[**get_all_entities_attribute_hierarchies**](#get_all_entities_attribute_hierarchies) | **get** /api/v1/entities/workspaces/{workspaceId}/attributeHierarchies | Get all Attribute Hierarchies
[**get_entity_attribute_hierarchies**](#get_entity_attribute_hierarchies) | **get** /api/v1/entities/workspaces/{workspaceId}/attributeHierarchies/{objectId} | Get an Attribute Hierarchy
[**patch_entity_attribute_hierarchies**](#patch_entity_attribute_hierarchies) | **patch** /api/v1/entities/workspaces/{workspaceId}/attributeHierarchies/{objectId} | Patch an Attribute Hierarchy
[**search_entities_attribute_hierarchies**](#search_entities_attribute_hierarchies) | **post** /api/v1/entities/workspaces/{workspaceId}/attributeHierarchies/search | Search request for AttributeHierarchy
[**update_entity_attribute_hierarchies**](#update_entity_attribute_hierarchies) | **put** /api/v1/entities/workspaces/{workspaceId}/attributeHierarchies/{objectId} | Put an Attribute Hierarchy

# **create_entity_attribute_hierarchies**
<a id="create_entity_attribute_hierarchies"></a>
> JsonApiAttributeHierarchyOutDocument create_entity_attribute_hierarchies(workspace_idjson_api_attribute_hierarchy_in_document)

Post Attribute Hierarchies

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import attribute_hierarchies_api
from gooddata_api_client.model.json_api_attribute_hierarchy_in_document import JsonApiAttributeHierarchyInDocument
from gooddata_api_client.model.json_api_attribute_hierarchy_out_document import JsonApiAttributeHierarchyOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = attribute_hierarchies_api.AttributeHierarchiesApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
    }
    body = JsonApiAttributeHierarchyInDocument(
        data=JsonApiAttributeHierarchyIn(
            attributes=dict(
                are_relations_valid=True,
                content=dict(),
                description="description_example",
                tags=[
                    "tags_example"
                ],
                title="title_example",
            ),
            id="id1",
            type="attributeHierarchy",
        ),
    )
    try:
        # Post Attribute Hierarchies
        api_response = api_instance.create_entity_attribute_hierarchies(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AttributeHierarchiesApi->create_entity_attribute_hierarchies: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
        'include': [
        "createdBy,modifiedBy,attributes"
    ],
        'metaInclude': [
        "metaInclude=origin,all"
    ],
    }
    body = JsonApiAttributeHierarchyInDocument(
        data=JsonApiAttributeHierarchyIn(
            attributes=dict(
                are_relations_valid=True,
                content=dict(),
                description="description_example",
                tags=[
                    "tags_example"
                ],
                title="title_example",
            ),
            id="id1",
            type="attributeHierarchy",
        ),
    )
    try:
        # Post Attribute Hierarchies
        api_response = api_instance.create_entity_attribute_hierarchies(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AttributeHierarchiesApi->create_entity_attribute_hierarchies: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAttributeHierarchyInDocument**](../../models/JsonApiAttributeHierarchyInDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAttributeHierarchyInDocument**](../../models/JsonApiAttributeHierarchyInDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
include | IncludeSchema | | optional
metaInclude | MetaIncludeSchema | | optional


# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["userIdentifiers", "attributes", "createdBy", "modifiedBy", "ALL", ] 

# MetaIncludeSchema

Included meta objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Included meta objects | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["origin", "all", "ALL", ] 

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
201 | [ApiResponseFor201](#create_entity_attribute_hierarchies.ApiResponseFor201) | Request successfully processed

#### create_entity_attribute_hierarchies.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationJson, SchemaFor201ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAttributeHierarchyOutDocument**](../../models/JsonApiAttributeHierarchyOutDocument.md) |  | 


# SchemaFor201ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAttributeHierarchyOutDocument**](../../models/JsonApiAttributeHierarchyOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_entity_attribute_hierarchies**
<a id="delete_entity_attribute_hierarchies"></a>
> delete_entity_attribute_hierarchies(workspace_idobject_id)

Delete an Attribute Hierarchy

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import attribute_hierarchies_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = attribute_hierarchies_api.AttributeHierarchiesApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
    }
    try:
        # Delete an Attribute Hierarchy
        api_response = api_instance.delete_entity_attribute_hierarchies(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AttributeHierarchiesApi->delete_entity_attribute_hierarchies: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
        'filter': "title==someString;description==someString;createdBy.id==321;modifiedBy.id==321",
    }
    try:
        # Delete an Attribute Hierarchy
        api_response = api_instance.delete_entity_attribute_hierarchies(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AttributeHierarchiesApi->delete_entity_attribute_hierarchies: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 
objectId | ObjectIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# ObjectIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#delete_entity_attribute_hierarchies.ApiResponseFor204) | Successfully deleted

#### delete_entity_attribute_hierarchies.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_attribute_hierarchies**
<a id="get_all_entities_attribute_hierarchies"></a>
> JsonApiAttributeHierarchyOutList get_all_entities_attribute_hierarchies(workspace_id)

Get all Attribute Hierarchies

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import attribute_hierarchies_api
from gooddata_api_client.model.json_api_attribute_hierarchy_out_list import JsonApiAttributeHierarchyOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = attribute_hierarchies_api.AttributeHierarchiesApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
    }
    header_params = {
    }
    try:
        # Get all Attribute Hierarchies
        api_response = api_instance.get_all_entities_attribute_hierarchies(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AttributeHierarchiesApi->get_all_entities_attribute_hierarchies: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
        'origin': "ALL",
        'filter': "title==someString;description==someString;createdBy.id==321;modifiedBy.id==321",
        'include': [
        "createdBy,modifiedBy,attributes"
    ],
        'page': 0,
        'size': 20,
        'sort': [
        "sort_example"
    ],
        'metaInclude': [
        "metaInclude=origin,page,all"
    ],
    }
    header_params = {
        'X-GDC-VALIDATE-RELATIONS': False,
    }
    try:
        # Get all Attribute Hierarchies
        api_response = api_instance.get_all_entities_attribute_hierarchies(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AttributeHierarchiesApi->get_all_entities_attribute_hierarchies: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
header_params | RequestHeaderParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
origin | OriginSchema | | optional
filter | FilterSchema | | optional
include | IncludeSchema | | optional
page | PageSchema | | optional
size | SizeSchema | | optional
sort | SortSchema | | optional
metaInclude | MetaIncludeSchema | | optional


# OriginSchema

Defines scope of origin of objects. All by default.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Defines scope of origin of objects. All by default. | must be one of ["ALL", "PARENTS", "NATIVE", ] if omitted the server will use the default value of "ALL"

# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["userIdentifiers", "attributes", "createdBy", "modifiedBy", "ALL", ] 

# PageSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 0

# SizeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 20

# SortSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

# MetaIncludeSchema

Included meta objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Included meta objects | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["origin", "page", "all", "ALL", ] 

### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
X-GDC-VALIDATE-RELATIONS | XGDCVALIDATERELATIONSSchema | | optional

# XGDCVALIDATERELATIONSSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bool,  | BoolClass,  |  | if omitted the server will use the default value of False

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
200 | [ApiResponseFor200](#get_all_entities_attribute_hierarchies.ApiResponseFor200) | Request successfully processed

#### get_all_entities_attribute_hierarchies.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAttributeHierarchyOutList**](../../models/JsonApiAttributeHierarchyOutList.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAttributeHierarchyOutList**](../../models/JsonApiAttributeHierarchyOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_attribute_hierarchies**
<a id="get_entity_attribute_hierarchies"></a>
> JsonApiAttributeHierarchyOutDocument get_entity_attribute_hierarchies(workspace_idobject_id)

Get an Attribute Hierarchy

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import attribute_hierarchies_api
from gooddata_api_client.model.json_api_attribute_hierarchy_out_document import JsonApiAttributeHierarchyOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = attribute_hierarchies_api.AttributeHierarchiesApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
    }
    header_params = {
    }
    try:
        # Get an Attribute Hierarchy
        api_response = api_instance.get_entity_attribute_hierarchies(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AttributeHierarchiesApi->get_entity_attribute_hierarchies: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
        'filter': "title==someString;description==someString;createdBy.id==321;modifiedBy.id==321",
        'include': [
        "createdBy,modifiedBy,attributes"
    ],
        'metaInclude': [
        "metaInclude=origin,all"
    ],
    }
    header_params = {
        'X-GDC-VALIDATE-RELATIONS': False,
    }
    try:
        # Get an Attribute Hierarchy
        api_response = api_instance.get_entity_attribute_hierarchies(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AttributeHierarchiesApi->get_entity_attribute_hierarchies: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
header_params | RequestHeaderParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
include | IncludeSchema | | optional
metaInclude | MetaIncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["userIdentifiers", "attributes", "createdBy", "modifiedBy", "ALL", ] 

# MetaIncludeSchema

Included meta objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Included meta objects | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["origin", "all", "ALL", ] 

### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
X-GDC-VALIDATE-RELATIONS | XGDCVALIDATERELATIONSSchema | | optional

# XGDCVALIDATERELATIONSSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bool,  | BoolClass,  |  | if omitted the server will use the default value of False

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 
objectId | ObjectIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# ObjectIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_entity_attribute_hierarchies.ApiResponseFor200) | Request successfully processed

#### get_entity_attribute_hierarchies.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAttributeHierarchyOutDocument**](../../models/JsonApiAttributeHierarchyOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAttributeHierarchyOutDocument**](../../models/JsonApiAttributeHierarchyOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **patch_entity_attribute_hierarchies**
<a id="patch_entity_attribute_hierarchies"></a>
> JsonApiAttributeHierarchyOutDocument patch_entity_attribute_hierarchies(workspace_idobject_idjson_api_attribute_hierarchy_patch_document)

Patch an Attribute Hierarchy

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import attribute_hierarchies_api
from gooddata_api_client.model.json_api_attribute_hierarchy_patch_document import JsonApiAttributeHierarchyPatchDocument
from gooddata_api_client.model.json_api_attribute_hierarchy_out_document import JsonApiAttributeHierarchyOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = attribute_hierarchies_api.AttributeHierarchiesApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
    }
    body = JsonApiAttributeHierarchyPatchDocument(
        data=JsonApiAttributeHierarchyPatch(
            attributes=dict(
                are_relations_valid=True,
                content=dict(),
                description="description_example",
                tags=[
                    "tags_example"
                ],
                title="title_example",
            ),
            id="id1",
            type="attributeHierarchy",
        ),
    )
    try:
        # Patch an Attribute Hierarchy
        api_response = api_instance.patch_entity_attribute_hierarchies(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AttributeHierarchiesApi->patch_entity_attribute_hierarchies: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
        'filter': "title==someString;description==someString;createdBy.id==321;modifiedBy.id==321",
        'include': [
        "createdBy,modifiedBy,attributes"
    ],
    }
    body = JsonApiAttributeHierarchyPatchDocument(
        data=JsonApiAttributeHierarchyPatch(
            attributes=dict(
                are_relations_valid=True,
                content=dict(),
                description="description_example",
                tags=[
                    "tags_example"
                ],
                title="title_example",
            ),
            id="id1",
            type="attributeHierarchy",
        ),
    )
    try:
        # Patch an Attribute Hierarchy
        api_response = api_instance.patch_entity_attribute_hierarchies(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AttributeHierarchiesApi->patch_entity_attribute_hierarchies: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAttributeHierarchyPatchDocument**](../../models/JsonApiAttributeHierarchyPatchDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAttributeHierarchyPatchDocument**](../../models/JsonApiAttributeHierarchyPatchDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
include | IncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["userIdentifiers", "attributes", "createdBy", "modifiedBy", "ALL", ] 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 
objectId | ObjectIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# ObjectIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#patch_entity_attribute_hierarchies.ApiResponseFor200) | Request successfully processed

#### patch_entity_attribute_hierarchies.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAttributeHierarchyOutDocument**](../../models/JsonApiAttributeHierarchyOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAttributeHierarchyOutDocument**](../../models/JsonApiAttributeHierarchyOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **search_entities_attribute_hierarchies**
<a id="search_entities_attribute_hierarchies"></a>
> JsonApiAttributeHierarchyOutList search_entities_attribute_hierarchies(workspace_identity_search_body)

Search request for AttributeHierarchy

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import attribute_hierarchies_api
from gooddata_api_client.model.json_api_attribute_hierarchy_out_list import JsonApiAttributeHierarchyOutList
from gooddata_api_client.model.entity_search_body import EntitySearchBody
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = attribute_hierarchies_api.AttributeHierarchiesApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
    }
    header_params = {
    }
    body = EntitySearchBody(
        filter="filter_example",
        include=[
            "include_example"
        ],
        meta_include=[
            "meta_include_example"
        ],
        page=EntitySearchPage(
            index=0,
            size=100,
        ),
        sort=[
            EntitySearchSort(
                direction="ASC",
                _property="_property_example",
            )
        ],
    )
    try:
        # Search request for AttributeHierarchy
        api_response = api_instance.search_entities_attribute_hierarchies(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AttributeHierarchiesApi->search_entities_attribute_hierarchies: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
        'origin': "ALL",
    }
    header_params = {
        'X-GDC-VALIDATE-RELATIONS': False,
    }
    body = EntitySearchBody(
        filter="filter_example",
        include=[
            "include_example"
        ],
        meta_include=[
            "meta_include_example"
        ],
        page=EntitySearchPage(
            index=0,
            size=100,
        ),
        sort=[
            EntitySearchSort(
                direction="ASC",
                _property="_property_example",
            )
        ],
    )
    try:
        # Search request for AttributeHierarchy
        api_response = api_instance.search_entities_attribute_hierarchies(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AttributeHierarchiesApi->search_entities_attribute_hierarchies: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
query_params | RequestQueryParams | |
header_params | RequestHeaderParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**EntitySearchBody**](../../models/EntitySearchBody.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
origin | OriginSchema | | optional


# OriginSchema

Defines scope of origin of objects. All by default.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Defines scope of origin of objects. All by default. | must be one of ["ALL", "PARENTS", "NATIVE", ] if omitted the server will use the default value of "ALL"

### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
X-GDC-VALIDATE-RELATIONS | XGDCVALIDATERELATIONSSchema | | optional

# XGDCVALIDATERELATIONSSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bool,  | BoolClass,  |  | if omitted the server will use the default value of False

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
200 | [ApiResponseFor200](#search_entities_attribute_hierarchies.ApiResponseFor200) | Request successfully processed

#### search_entities_attribute_hierarchies.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAttributeHierarchyOutList**](../../models/JsonApiAttributeHierarchyOutList.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAttributeHierarchyOutList**](../../models/JsonApiAttributeHierarchyOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_entity_attribute_hierarchies**
<a id="update_entity_attribute_hierarchies"></a>
> JsonApiAttributeHierarchyOutDocument update_entity_attribute_hierarchies(workspace_idobject_idjson_api_attribute_hierarchy_in_document)

Put an Attribute Hierarchy

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import attribute_hierarchies_api
from gooddata_api_client.model.json_api_attribute_hierarchy_in_document import JsonApiAttributeHierarchyInDocument
from gooddata_api_client.model.json_api_attribute_hierarchy_out_document import JsonApiAttributeHierarchyOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = attribute_hierarchies_api.AttributeHierarchiesApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
    }
    body = JsonApiAttributeHierarchyInDocument(
        data=JsonApiAttributeHierarchyIn(
            attributes=dict(
                are_relations_valid=True,
                content=dict(),
                description="description_example",
                tags=[
                    "tags_example"
                ],
                title="title_example",
            ),
            id="id1",
            type="attributeHierarchy",
        ),
    )
    try:
        # Put an Attribute Hierarchy
        api_response = api_instance.update_entity_attribute_hierarchies(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AttributeHierarchiesApi->update_entity_attribute_hierarchies: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
        'filter': "title==someString;description==someString;createdBy.id==321;modifiedBy.id==321",
        'include': [
        "createdBy,modifiedBy,attributes"
    ],
    }
    body = JsonApiAttributeHierarchyInDocument(
        data=JsonApiAttributeHierarchyIn(
            attributes=dict(
                are_relations_valid=True,
                content=dict(),
                description="description_example",
                tags=[
                    "tags_example"
                ],
                title="title_example",
            ),
            id="id1",
            type="attributeHierarchy",
        ),
    )
    try:
        # Put an Attribute Hierarchy
        api_response = api_instance.update_entity_attribute_hierarchies(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AttributeHierarchiesApi->update_entity_attribute_hierarchies: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAttributeHierarchyInDocument**](../../models/JsonApiAttributeHierarchyInDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAttributeHierarchyInDocument**](../../models/JsonApiAttributeHierarchyInDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
include | IncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["userIdentifiers", "attributes", "createdBy", "modifiedBy", "ALL", ] 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 
objectId | ObjectIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# ObjectIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_entity_attribute_hierarchies.ApiResponseFor200) | Request successfully processed

#### update_entity_attribute_hierarchies.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAttributeHierarchyOutDocument**](../../models/JsonApiAttributeHierarchyOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiAttributeHierarchyOutDocument**](../../models/JsonApiAttributeHierarchyOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


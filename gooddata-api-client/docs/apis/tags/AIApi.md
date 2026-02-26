<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.ai_api.AIApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_knowledge_recommendations**](#create_entity_knowledge_recommendations) | **post** /api/v1/entities/workspaces/{workspaceId}/knowledgeRecommendations | 
[**create_entity_memory_items**](#create_entity_memory_items) | **post** /api/v1/entities/workspaces/{workspaceId}/memoryItems | 
[**delete_entity_knowledge_recommendations**](#delete_entity_knowledge_recommendations) | **delete** /api/v1/entities/workspaces/{workspaceId}/knowledgeRecommendations/{objectId} | 
[**delete_entity_memory_items**](#delete_entity_memory_items) | **delete** /api/v1/entities/workspaces/{workspaceId}/memoryItems/{objectId} | 
[**get_all_entities_knowledge_recommendations**](#get_all_entities_knowledge_recommendations) | **get** /api/v1/entities/workspaces/{workspaceId}/knowledgeRecommendations | 
[**get_all_entities_memory_items**](#get_all_entities_memory_items) | **get** /api/v1/entities/workspaces/{workspaceId}/memoryItems | 
[**get_entity_knowledge_recommendations**](#get_entity_knowledge_recommendations) | **get** /api/v1/entities/workspaces/{workspaceId}/knowledgeRecommendations/{objectId} | 
[**get_entity_memory_items**](#get_entity_memory_items) | **get** /api/v1/entities/workspaces/{workspaceId}/memoryItems/{objectId} | 
[**metadata_check_organization**](#metadata_check_organization) | **post** /api/v1/actions/organization/metadataCheck | (BETA) Check Organization Metadata Inconsistencies
[**metadata_sync**](#metadata_sync) | **post** /api/v1/actions/workspaces/{workspaceId}/metadataSync | (BETA) Sync Metadata to other services
[**metadata_sync_organization**](#metadata_sync_organization) | **post** /api/v1/actions/organization/metadataSync | (BETA) Sync organization scope Metadata to other services
[**patch_entity_knowledge_recommendations**](#patch_entity_knowledge_recommendations) | **patch** /api/v1/entities/workspaces/{workspaceId}/knowledgeRecommendations/{objectId} | 
[**patch_entity_memory_items**](#patch_entity_memory_items) | **patch** /api/v1/entities/workspaces/{workspaceId}/memoryItems/{objectId} | 
[**search_entities_knowledge_recommendations**](#search_entities_knowledge_recommendations) | **post** /api/v1/entities/workspaces/{workspaceId}/knowledgeRecommendations/search | 
[**search_entities_memory_items**](#search_entities_memory_items) | **post** /api/v1/entities/workspaces/{workspaceId}/memoryItems/search | Search request for MemoryItem
[**update_entity_knowledge_recommendations**](#update_entity_knowledge_recommendations) | **put** /api/v1/entities/workspaces/{workspaceId}/knowledgeRecommendations/{objectId} | 
[**update_entity_memory_items**](#update_entity_memory_items) | **put** /api/v1/entities/workspaces/{workspaceId}/memoryItems/{objectId} | 

# **create_entity_knowledge_recommendations**
<a id="create_entity_knowledge_recommendations"></a>
> JsonApiKnowledgeRecommendationOutDocument create_entity_knowledge_recommendations(workspace_idjson_api_knowledge_recommendation_post_optional_id_document)



### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import ai_api
from gooddata_api_client.model.json_api_knowledge_recommendation_out_document import JsonApiKnowledgeRecommendationOutDocument
from gooddata_api_client.model.json_api_knowledge_recommendation_post_optional_id_document import JsonApiKnowledgeRecommendationPostOptionalIdDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ai_api.AIApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
    }
    body = JsonApiKnowledgeRecommendationPostOptionalIdDocument(
        data=JsonApiKnowledgeRecommendationPostOptionalId(
            attributes=dict(
                analytical_dashboard_title="Portfolio Health Insights",
                analyzed_period="2023-07",
                analyzed_value=None,
                are_relations_valid=True,
                comparison_type="MONTH",
                confidence=None,
                description="description_example",
                direction="DECREASED",
                metric_title="Revenue",
                recommendations=dict(),
                reference_period="2023-06",
                reference_value=None,
                source_count=2,
                tags=[
                    "tags_example"
                ],
                title="title_example",
                widget_id="widget-123",
                widget_name="Revenue Trend",
            ),
            id="id1",
            relationships=dict(
                analytical_dashboard=dict(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                metric=dict(
                    data=JsonApiMetricToOneLinkage(None),
                ),
            ),
            type="knowledgeRecommendation",
        ),
    )
    try:
        api_response = api_instance.create_entity_knowledge_recommendations(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->create_entity_knowledge_recommendations: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
        'include': [
        "metric,analyticalDashboard"
    ],
        'metaInclude': [
        "metaInclude=origin,all"
    ],
    }
    body = JsonApiKnowledgeRecommendationPostOptionalIdDocument(
        data=JsonApiKnowledgeRecommendationPostOptionalId(
            attributes=dict(
                analytical_dashboard_title="Portfolio Health Insights",
                analyzed_period="2023-07",
                analyzed_value=None,
                are_relations_valid=True,
                comparison_type="MONTH",
                confidence=None,
                description="description_example",
                direction="DECREASED",
                metric_title="Revenue",
                recommendations=dict(),
                reference_period="2023-06",
                reference_value=None,
                source_count=2,
                tags=[
                    "tags_example"
                ],
                title="title_example",
                widget_id="widget-123",
                widget_name="Revenue Trend",
            ),
            id="id1",
            relationships=dict(
                analytical_dashboard=dict(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                metric=dict(
                    data=JsonApiMetricToOneLinkage(None),
                ),
            ),
            type="knowledgeRecommendation",
        ),
    )
    try:
        api_response = api_instance.create_entity_knowledge_recommendations(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->create_entity_knowledge_recommendations: %s\n" % e)
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
[**JsonApiKnowledgeRecommendationPostOptionalIdDocument**](../../models/JsonApiKnowledgeRecommendationPostOptionalIdDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiKnowledgeRecommendationPostOptionalIdDocument**](../../models/JsonApiKnowledgeRecommendationPostOptionalIdDocument.md) |  | 


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
items | str,  | str,  |  | must be one of ["metrics", "analyticalDashboards", "metric", "analyticalDashboard", "ALL", ] 

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
201 | [ApiResponseFor201](#create_entity_knowledge_recommendations.ApiResponseFor201) | Request successfully processed

#### create_entity_knowledge_recommendations.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationJson, SchemaFor201ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiKnowledgeRecommendationOutDocument**](../../models/JsonApiKnowledgeRecommendationOutDocument.md) |  | 


# SchemaFor201ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiKnowledgeRecommendationOutDocument**](../../models/JsonApiKnowledgeRecommendationOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **create_entity_memory_items**
<a id="create_entity_memory_items"></a>
> JsonApiMemoryItemOutDocument create_entity_memory_items(workspace_idjson_api_memory_item_post_optional_id_document)



### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import ai_api
from gooddata_api_client.model.json_api_memory_item_post_optional_id_document import JsonApiMemoryItemPostOptionalIdDocument
from gooddata_api_client.model.json_api_memory_item_out_document import JsonApiMemoryItemOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ai_api.AIApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
    }
    body = JsonApiMemoryItemPostOptionalIdDocument(
        data=JsonApiMemoryItemPostOptionalId(
            attributes=dict(
                are_relations_valid=True,
                description="description_example",
                instruction="instruction_example",
                is_disabled=True,
                keywords=[
                    "keywords_example"
                ],
                strategy="ALWAYS",
                tags=[
                    "tags_example"
                ],
                title="title_example",
            ),
            id="id1",
            type="memoryItem",
        ),
    )
    try:
        api_response = api_instance.create_entity_memory_items(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->create_entity_memory_items: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
        'include': [
        "createdBy,modifiedBy"
    ],
        'metaInclude': [
        "metaInclude=origin,all"
    ],
    }
    body = JsonApiMemoryItemPostOptionalIdDocument(
        data=JsonApiMemoryItemPostOptionalId(
            attributes=dict(
                are_relations_valid=True,
                description="description_example",
                instruction="instruction_example",
                is_disabled=True,
                keywords=[
                    "keywords_example"
                ],
                strategy="ALWAYS",
                tags=[
                    "tags_example"
                ],
                title="title_example",
            ),
            id="id1",
            type="memoryItem",
        ),
    )
    try:
        api_response = api_instance.create_entity_memory_items(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->create_entity_memory_items: %s\n" % e)
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
[**JsonApiMemoryItemPostOptionalIdDocument**](../../models/JsonApiMemoryItemPostOptionalIdDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiMemoryItemPostOptionalIdDocument**](../../models/JsonApiMemoryItemPostOptionalIdDocument.md) |  | 


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
items | str,  | str,  |  | must be one of ["userIdentifiers", "createdBy", "modifiedBy", "ALL", ] 

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
201 | [ApiResponseFor201](#create_entity_memory_items.ApiResponseFor201) | Request successfully processed

#### create_entity_memory_items.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationJson, SchemaFor201ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiMemoryItemOutDocument**](../../models/JsonApiMemoryItemOutDocument.md) |  | 


# SchemaFor201ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiMemoryItemOutDocument**](../../models/JsonApiMemoryItemOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_entity_knowledge_recommendations**
<a id="delete_entity_knowledge_recommendations"></a>
> delete_entity_knowledge_recommendations(workspace_idobject_id)



### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import ai_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ai_api.AIApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
    }
    try:
        api_response = api_instance.delete_entity_knowledge_recommendations(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->delete_entity_knowledge_recommendations: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
        'filter': "title==someString;description==someString;metric.id==321;analyticalDashboard.id==321",
    }
    try:
        api_response = api_instance.delete_entity_knowledge_recommendations(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->delete_entity_knowledge_recommendations: %s\n" % e)
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
204 | [ApiResponseFor204](#delete_entity_knowledge_recommendations.ApiResponseFor204) | Successfully deleted

#### delete_entity_knowledge_recommendations.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_entity_memory_items**
<a id="delete_entity_memory_items"></a>
> delete_entity_memory_items(workspace_idobject_id)



### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import ai_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ai_api.AIApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
    }
    try:
        api_response = api_instance.delete_entity_memory_items(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->delete_entity_memory_items: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
        'filter': "title==someString;description==someString;createdBy.id==321;modifiedBy.id==321",
    }
    try:
        api_response = api_instance.delete_entity_memory_items(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->delete_entity_memory_items: %s\n" % e)
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
204 | [ApiResponseFor204](#delete_entity_memory_items.ApiResponseFor204) | Successfully deleted

#### delete_entity_memory_items.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_knowledge_recommendations**
<a id="get_all_entities_knowledge_recommendations"></a>
> JsonApiKnowledgeRecommendationOutList get_all_entities_knowledge_recommendations(workspace_id)



### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import ai_api
from gooddata_api_client.model.json_api_knowledge_recommendation_out_list import JsonApiKnowledgeRecommendationOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ai_api.AIApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
    }
    header_params = {
    }
    try:
        api_response = api_instance.get_all_entities_knowledge_recommendations(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->get_all_entities_knowledge_recommendations: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
        'origin': "ALL",
        'filter': "title==someString;description==someString;metric.id==321;analyticalDashboard.id==321",
        'include': [
        "metric,analyticalDashboard"
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
        api_response = api_instance.get_all_entities_knowledge_recommendations(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->get_all_entities_knowledge_recommendations: %s\n" % e)
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
items | str,  | str,  |  | must be one of ["metrics", "analyticalDashboards", "metric", "analyticalDashboard", "ALL", ] 

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
200 | [ApiResponseFor200](#get_all_entities_knowledge_recommendations.ApiResponseFor200) | Request successfully processed

#### get_all_entities_knowledge_recommendations.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiKnowledgeRecommendationOutList**](../../models/JsonApiKnowledgeRecommendationOutList.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiKnowledgeRecommendationOutList**](../../models/JsonApiKnowledgeRecommendationOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_memory_items**
<a id="get_all_entities_memory_items"></a>
> JsonApiMemoryItemOutList get_all_entities_memory_items(workspace_id)



### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import ai_api
from gooddata_api_client.model.json_api_memory_item_out_list import JsonApiMemoryItemOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ai_api.AIApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
    }
    header_params = {
    }
    try:
        api_response = api_instance.get_all_entities_memory_items(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->get_all_entities_memory_items: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
        'origin': "ALL",
        'filter': "title==someString;description==someString;createdBy.id==321;modifiedBy.id==321",
        'include': [
        "createdBy,modifiedBy"
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
        api_response = api_instance.get_all_entities_memory_items(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->get_all_entities_memory_items: %s\n" % e)
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
items | str,  | str,  |  | must be one of ["userIdentifiers", "createdBy", "modifiedBy", "ALL", ] 

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
200 | [ApiResponseFor200](#get_all_entities_memory_items.ApiResponseFor200) | Request successfully processed

#### get_all_entities_memory_items.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiMemoryItemOutList**](../../models/JsonApiMemoryItemOutList.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiMemoryItemOutList**](../../models/JsonApiMemoryItemOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_knowledge_recommendations**
<a id="get_entity_knowledge_recommendations"></a>
> JsonApiKnowledgeRecommendationOutDocument get_entity_knowledge_recommendations(workspace_idobject_id)



### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import ai_api
from gooddata_api_client.model.json_api_knowledge_recommendation_out_document import JsonApiKnowledgeRecommendationOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ai_api.AIApi(api_client)

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
        api_response = api_instance.get_entity_knowledge_recommendations(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->get_entity_knowledge_recommendations: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
        'filter': "title==someString;description==someString;metric.id==321;analyticalDashboard.id==321",
        'include': [
        "metric,analyticalDashboard"
    ],
        'metaInclude': [
        "metaInclude=origin,all"
    ],
    }
    header_params = {
        'X-GDC-VALIDATE-RELATIONS': False,
    }
    try:
        api_response = api_instance.get_entity_knowledge_recommendations(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->get_entity_knowledge_recommendations: %s\n" % e)
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
items | str,  | str,  |  | must be one of ["metrics", "analyticalDashboards", "metric", "analyticalDashboard", "ALL", ] 

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
200 | [ApiResponseFor200](#get_entity_knowledge_recommendations.ApiResponseFor200) | Request successfully processed

#### get_entity_knowledge_recommendations.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiKnowledgeRecommendationOutDocument**](../../models/JsonApiKnowledgeRecommendationOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiKnowledgeRecommendationOutDocument**](../../models/JsonApiKnowledgeRecommendationOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_memory_items**
<a id="get_entity_memory_items"></a>
> JsonApiMemoryItemOutDocument get_entity_memory_items(workspace_idobject_id)



### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import ai_api
from gooddata_api_client.model.json_api_memory_item_out_document import JsonApiMemoryItemOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ai_api.AIApi(api_client)

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
        api_response = api_instance.get_entity_memory_items(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->get_entity_memory_items: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
        'filter': "title==someString;description==someString;createdBy.id==321;modifiedBy.id==321",
        'include': [
        "createdBy,modifiedBy"
    ],
        'metaInclude': [
        "metaInclude=origin,all"
    ],
    }
    header_params = {
        'X-GDC-VALIDATE-RELATIONS': False,
    }
    try:
        api_response = api_instance.get_entity_memory_items(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->get_entity_memory_items: %s\n" % e)
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
items | str,  | str,  |  | must be one of ["userIdentifiers", "createdBy", "modifiedBy", "ALL", ] 

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
200 | [ApiResponseFor200](#get_entity_memory_items.ApiResponseFor200) | Request successfully processed

#### get_entity_memory_items.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiMemoryItemOutDocument**](../../models/JsonApiMemoryItemOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiMemoryItemOutDocument**](../../models/JsonApiMemoryItemOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **metadata_check_organization**
<a id="metadata_check_organization"></a>
> metadata_check_organization()

(BETA) Check Organization Metadata Inconsistencies

(BETA) Temporary solution. Resyncs all organization objects and full workspaces within the organization with target GEN_AI_CHECK.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import ai_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ai_api.AIApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # (BETA) Check Organization Metadata Inconsistencies
        api_response = api_instance.metadata_check_organization()
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->metadata_check_organization: %s\n" % e)
```
### Parameters
This endpoint does not need any parameter.

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#metadata_check_organization.ApiResponseFor200) | OK

#### metadata_check_organization.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **metadata_sync**
<a id="metadata_sync"></a>
> metadata_sync(workspace_id)

(BETA) Sync Metadata to other services

(BETA) Temporary solution. Later relevant metadata actions will trigger it in its scope only.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import ai_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ai_api.AIApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    try:
        # (BETA) Sync Metadata to other services
        api_response = api_instance.metadata_sync(
            path_params=path_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->metadata_sync: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
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
200 | [ApiResponseFor200](#metadata_sync.ApiResponseFor200) | OK

#### metadata_sync.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **metadata_sync_organization**
<a id="metadata_sync_organization"></a>
> metadata_sync_organization()

(BETA) Sync organization scope Metadata to other services

(BETA) Temporary solution. Later relevant metadata actions will trigger sync in their scope only.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import ai_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ai_api.AIApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # (BETA) Sync organization scope Metadata to other services
        api_response = api_instance.metadata_sync_organization()
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->metadata_sync_organization: %s\n" % e)
```
### Parameters
This endpoint does not need any parameter.

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#metadata_sync_organization.ApiResponseFor200) | OK

#### metadata_sync_organization.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **patch_entity_knowledge_recommendations**
<a id="patch_entity_knowledge_recommendations"></a>
> JsonApiKnowledgeRecommendationOutDocument patch_entity_knowledge_recommendations(workspace_idobject_idjson_api_knowledge_recommendation_patch_document)



### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import ai_api
from gooddata_api_client.model.json_api_knowledge_recommendation_patch_document import JsonApiKnowledgeRecommendationPatchDocument
from gooddata_api_client.model.json_api_knowledge_recommendation_out_document import JsonApiKnowledgeRecommendationOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ai_api.AIApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
    }
    body = JsonApiKnowledgeRecommendationPatchDocument(
        data=JsonApiKnowledgeRecommendationPatch(
            attributes=dict(
                analytical_dashboard_title="Portfolio Health Insights",
                analyzed_period="2023-07",
                analyzed_value=None,
                are_relations_valid=True,
                comparison_type="MONTH",
                confidence=None,
                description="description_example",
                direction="DECREASED",
                metric_title="Revenue",
                recommendations=dict(),
                reference_period="2023-06",
                reference_value=None,
                source_count=2,
                tags=[
                    "tags_example"
                ],
                title="title_example",
                widget_id="widget-123",
                widget_name="Revenue Trend",
            ),
            id="id1",
            relationships=dict(
                analytical_dashboard=dict(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                metric=dict(
                    data=JsonApiMetricToOneLinkage(None),
                ),
            ),
            type="knowledgeRecommendation",
        ),
    )
    try:
        api_response = api_instance.patch_entity_knowledge_recommendations(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->patch_entity_knowledge_recommendations: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
        'filter': "title==someString;description==someString;metric.id==321;analyticalDashboard.id==321",
        'include': [
        "metric,analyticalDashboard"
    ],
    }
    body = JsonApiKnowledgeRecommendationPatchDocument(
        data=JsonApiKnowledgeRecommendationPatch(
            attributes=dict(
                analytical_dashboard_title="Portfolio Health Insights",
                analyzed_period="2023-07",
                analyzed_value=None,
                are_relations_valid=True,
                comparison_type="MONTH",
                confidence=None,
                description="description_example",
                direction="DECREASED",
                metric_title="Revenue",
                recommendations=dict(),
                reference_period="2023-06",
                reference_value=None,
                source_count=2,
                tags=[
                    "tags_example"
                ],
                title="title_example",
                widget_id="widget-123",
                widget_name="Revenue Trend",
            ),
            id="id1",
            relationships=dict(
                analytical_dashboard=dict(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                metric=dict(
                    data=JsonApiMetricToOneLinkage(None),
                ),
            ),
            type="knowledgeRecommendation",
        ),
    )
    try:
        api_response = api_instance.patch_entity_knowledge_recommendations(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->patch_entity_knowledge_recommendations: %s\n" % e)
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
[**JsonApiKnowledgeRecommendationPatchDocument**](../../models/JsonApiKnowledgeRecommendationPatchDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiKnowledgeRecommendationPatchDocument**](../../models/JsonApiKnowledgeRecommendationPatchDocument.md) |  | 


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
items | str,  | str,  |  | must be one of ["metrics", "analyticalDashboards", "metric", "analyticalDashboard", "ALL", ] 

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
200 | [ApiResponseFor200](#patch_entity_knowledge_recommendations.ApiResponseFor200) | Request successfully processed

#### patch_entity_knowledge_recommendations.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiKnowledgeRecommendationOutDocument**](../../models/JsonApiKnowledgeRecommendationOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiKnowledgeRecommendationOutDocument**](../../models/JsonApiKnowledgeRecommendationOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **patch_entity_memory_items**
<a id="patch_entity_memory_items"></a>
> JsonApiMemoryItemOutDocument patch_entity_memory_items(workspace_idobject_idjson_api_memory_item_patch_document)



### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import ai_api
from gooddata_api_client.model.json_api_memory_item_patch_document import JsonApiMemoryItemPatchDocument
from gooddata_api_client.model.json_api_memory_item_out_document import JsonApiMemoryItemOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ai_api.AIApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
    }
    body = JsonApiMemoryItemPatchDocument(
        data=JsonApiMemoryItemPatch(
            attributes=dict(
                are_relations_valid=True,
                description="description_example",
                instruction="instruction_example",
                is_disabled=True,
                keywords=[
                    "keywords_example"
                ],
                strategy="ALWAYS",
                tags=[
                    "tags_example"
                ],
                title="title_example",
            ),
            id="id1",
            type="memoryItem",
        ),
    )
    try:
        api_response = api_instance.patch_entity_memory_items(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->patch_entity_memory_items: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
        'filter': "title==someString;description==someString;createdBy.id==321;modifiedBy.id==321",
        'include': [
        "createdBy,modifiedBy"
    ],
    }
    body = JsonApiMemoryItemPatchDocument(
        data=JsonApiMemoryItemPatch(
            attributes=dict(
                are_relations_valid=True,
                description="description_example",
                instruction="instruction_example",
                is_disabled=True,
                keywords=[
                    "keywords_example"
                ],
                strategy="ALWAYS",
                tags=[
                    "tags_example"
                ],
                title="title_example",
            ),
            id="id1",
            type="memoryItem",
        ),
    )
    try:
        api_response = api_instance.patch_entity_memory_items(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->patch_entity_memory_items: %s\n" % e)
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
[**JsonApiMemoryItemPatchDocument**](../../models/JsonApiMemoryItemPatchDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiMemoryItemPatchDocument**](../../models/JsonApiMemoryItemPatchDocument.md) |  | 


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
items | str,  | str,  |  | must be one of ["userIdentifiers", "createdBy", "modifiedBy", "ALL", ] 

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
200 | [ApiResponseFor200](#patch_entity_memory_items.ApiResponseFor200) | Request successfully processed

#### patch_entity_memory_items.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiMemoryItemOutDocument**](../../models/JsonApiMemoryItemOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiMemoryItemOutDocument**](../../models/JsonApiMemoryItemOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **search_entities_knowledge_recommendations**
<a id="search_entities_knowledge_recommendations"></a>
> JsonApiKnowledgeRecommendationOutList search_entities_knowledge_recommendations(workspace_identity_search_body)



### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import ai_api
from gooddata_api_client.model.json_api_knowledge_recommendation_out_list import JsonApiKnowledgeRecommendationOutList
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
    api_instance = ai_api.AIApi(api_client)

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
        api_response = api_instance.search_entities_knowledge_recommendations(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->search_entities_knowledge_recommendations: %s\n" % e)

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
        api_response = api_instance.search_entities_knowledge_recommendations(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->search_entities_knowledge_recommendations: %s\n" % e)
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
200 | [ApiResponseFor200](#search_entities_knowledge_recommendations.ApiResponseFor200) | Request successfully processed

#### search_entities_knowledge_recommendations.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiKnowledgeRecommendationOutList**](../../models/JsonApiKnowledgeRecommendationOutList.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiKnowledgeRecommendationOutList**](../../models/JsonApiKnowledgeRecommendationOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **search_entities_memory_items**
<a id="search_entities_memory_items"></a>
> JsonApiMemoryItemOutList search_entities_memory_items(workspace_identity_search_body)

Search request for MemoryItem

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import ai_api
from gooddata_api_client.model.json_api_memory_item_out_list import JsonApiMemoryItemOutList
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
    api_instance = ai_api.AIApi(api_client)

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
        # Search request for MemoryItem
        api_response = api_instance.search_entities_memory_items(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->search_entities_memory_items: %s\n" % e)

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
        # Search request for MemoryItem
        api_response = api_instance.search_entities_memory_items(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->search_entities_memory_items: %s\n" % e)
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
200 | [ApiResponseFor200](#search_entities_memory_items.ApiResponseFor200) | Request successfully processed

#### search_entities_memory_items.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiMemoryItemOutList**](../../models/JsonApiMemoryItemOutList.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiMemoryItemOutList**](../../models/JsonApiMemoryItemOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_entity_knowledge_recommendations**
<a id="update_entity_knowledge_recommendations"></a>
> JsonApiKnowledgeRecommendationOutDocument update_entity_knowledge_recommendations(workspace_idobject_idjson_api_knowledge_recommendation_in_document)



### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import ai_api
from gooddata_api_client.model.json_api_knowledge_recommendation_out_document import JsonApiKnowledgeRecommendationOutDocument
from gooddata_api_client.model.json_api_knowledge_recommendation_in_document import JsonApiKnowledgeRecommendationInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ai_api.AIApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
    }
    body = JsonApiKnowledgeRecommendationInDocument(
        data=JsonApiKnowledgeRecommendationIn(
            attributes=dict(
                analytical_dashboard_title="Portfolio Health Insights",
                analyzed_period="2023-07",
                analyzed_value=None,
                are_relations_valid=True,
                comparison_type="MONTH",
                confidence=None,
                description="description_example",
                direction="DECREASED",
                metric_title="Revenue",
                recommendations=dict(),
                reference_period="2023-06",
                reference_value=None,
                source_count=2,
                tags=[
                    "tags_example"
                ],
                title="title_example",
                widget_id="widget-123",
                widget_name="Revenue Trend",
            ),
            id="id1",
            relationships=dict(
                analytical_dashboard=dict(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                metric=dict(
                    data=JsonApiMetricToOneLinkage(None),
                ),
            ),
            type="knowledgeRecommendation",
        ),
    )
    try:
        api_response = api_instance.update_entity_knowledge_recommendations(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->update_entity_knowledge_recommendations: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
        'filter': "title==someString;description==someString;metric.id==321;analyticalDashboard.id==321",
        'include': [
        "metric,analyticalDashboard"
    ],
    }
    body = JsonApiKnowledgeRecommendationInDocument(
        data=JsonApiKnowledgeRecommendationIn(
            attributes=dict(
                analytical_dashboard_title="Portfolio Health Insights",
                analyzed_period="2023-07",
                analyzed_value=None,
                are_relations_valid=True,
                comparison_type="MONTH",
                confidence=None,
                description="description_example",
                direction="DECREASED",
                metric_title="Revenue",
                recommendations=dict(),
                reference_period="2023-06",
                reference_value=None,
                source_count=2,
                tags=[
                    "tags_example"
                ],
                title="title_example",
                widget_id="widget-123",
                widget_name="Revenue Trend",
            ),
            id="id1",
            relationships=dict(
                analytical_dashboard=dict(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                metric=dict(
                    data=JsonApiMetricToOneLinkage(None),
                ),
            ),
            type="knowledgeRecommendation",
        ),
    )
    try:
        api_response = api_instance.update_entity_knowledge_recommendations(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->update_entity_knowledge_recommendations: %s\n" % e)
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
[**JsonApiKnowledgeRecommendationInDocument**](../../models/JsonApiKnowledgeRecommendationInDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiKnowledgeRecommendationInDocument**](../../models/JsonApiKnowledgeRecommendationInDocument.md) |  | 


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
items | str,  | str,  |  | must be one of ["metrics", "analyticalDashboards", "metric", "analyticalDashboard", "ALL", ] 

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
200 | [ApiResponseFor200](#update_entity_knowledge_recommendations.ApiResponseFor200) | Request successfully processed

#### update_entity_knowledge_recommendations.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiKnowledgeRecommendationOutDocument**](../../models/JsonApiKnowledgeRecommendationOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiKnowledgeRecommendationOutDocument**](../../models/JsonApiKnowledgeRecommendationOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_entity_memory_items**
<a id="update_entity_memory_items"></a>
> JsonApiMemoryItemOutDocument update_entity_memory_items(workspace_idobject_idjson_api_memory_item_in_document)



### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import ai_api
from gooddata_api_client.model.json_api_memory_item_in_document import JsonApiMemoryItemInDocument
from gooddata_api_client.model.json_api_memory_item_out_document import JsonApiMemoryItemOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ai_api.AIApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
    }
    body = JsonApiMemoryItemInDocument(
        data=JsonApiMemoryItemIn(
            attributes=dict(
                are_relations_valid=True,
                description="description_example",
                instruction="instruction_example",
                is_disabled=True,
                keywords=[
                    "keywords_example"
                ],
                strategy="ALWAYS",
                tags=[
                    "tags_example"
                ],
                title="title_example",
            ),
            id="id1",
            type="memoryItem",
        ),
    )
    try:
        api_response = api_instance.update_entity_memory_items(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->update_entity_memory_items: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
        'filter': "title==someString;description==someString;createdBy.id==321;modifiedBy.id==321",
        'include': [
        "createdBy,modifiedBy"
    ],
    }
    body = JsonApiMemoryItemInDocument(
        data=JsonApiMemoryItemIn(
            attributes=dict(
                are_relations_valid=True,
                description="description_example",
                instruction="instruction_example",
                is_disabled=True,
                keywords=[
                    "keywords_example"
                ],
                strategy="ALWAYS",
                tags=[
                    "tags_example"
                ],
                title="title_example",
            ),
            id="id1",
            type="memoryItem",
        ),
    )
    try:
        api_response = api_instance.update_entity_memory_items(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AIApi->update_entity_memory_items: %s\n" % e)
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
[**JsonApiMemoryItemInDocument**](../../models/JsonApiMemoryItemInDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiMemoryItemInDocument**](../../models/JsonApiMemoryItemInDocument.md) |  | 


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
items | str,  | str,  |  | must be one of ["userIdentifiers", "createdBy", "modifiedBy", "ALL", ] 

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
200 | [ApiResponseFor200](#update_entity_memory_items.ApiResponseFor200) | Request successfully processed

#### update_entity_memory_items.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiMemoryItemOutDocument**](../../models/JsonApiMemoryItemOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiMemoryItemOutDocument**](../../models/JsonApiMemoryItemOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


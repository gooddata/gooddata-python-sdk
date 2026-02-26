<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.llm_endpoints_api.LLMEndpointsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_llm_endpoints**](#create_entity_llm_endpoints) | **post** /api/v1/entities/llmEndpoints | Post LLM endpoint entities
[**delete_entity_llm_endpoints**](#delete_entity_llm_endpoints) | **delete** /api/v1/entities/llmEndpoints/{id} | 
[**get_all_entities_llm_endpoints**](#get_all_entities_llm_endpoints) | **get** /api/v1/entities/llmEndpoints | Get all LLM endpoint entities
[**get_entity_llm_endpoints**](#get_entity_llm_endpoints) | **get** /api/v1/entities/llmEndpoints/{id} | Get LLM endpoint entity
[**patch_entity_llm_endpoints**](#patch_entity_llm_endpoints) | **patch** /api/v1/entities/llmEndpoints/{id} | Patch LLM endpoint entity
[**update_entity_llm_endpoints**](#update_entity_llm_endpoints) | **put** /api/v1/entities/llmEndpoints/{id} | PUT LLM endpoint entity

# **create_entity_llm_endpoints**
<a id="create_entity_llm_endpoints"></a>
> JsonApiLlmEndpointOutDocument create_entity_llm_endpoints(json_api_llm_endpoint_in_document)

Post LLM endpoint entities

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import llm_endpoints_api
from gooddata_api_client.model.json_api_llm_endpoint_in_document import JsonApiLlmEndpointInDocument
from gooddata_api_client.model.json_api_llm_endpoint_out_document import JsonApiLlmEndpointOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = llm_endpoints_api.LLMEndpointsApi(api_client)

    # example passing only required values which don't have defaults set
    body = JsonApiLlmEndpointInDocument(
        data=JsonApiLlmEndpointIn(
            attributes=dict(
                base_url="base_url_example",
                llm_model="llm_model_example",
                llm_organization="llm_organization_example",
                provider="OPENAI",
                title="title_example",
                token="token_example",
            ),
            id="id1",
            type="llmEndpoint",
        ),
    )
    try:
        # Post LLM endpoint entities
        api_response = api_instance.create_entity_llm_endpoints(
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMEndpointsApi->create_entity_llm_endpoints: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, SchemaForRequestBodyApplicationVndGooddataApijson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiLlmEndpointInDocument**](../../models/JsonApiLlmEndpointInDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiLlmEndpointInDocument**](../../models/JsonApiLlmEndpointInDocument.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#create_entity_llm_endpoints.ApiResponseFor201) | Request successfully processed

#### create_entity_llm_endpoints.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationJson, SchemaFor201ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiLlmEndpointOutDocument**](../../models/JsonApiLlmEndpointOutDocument.md) |  | 


# SchemaFor201ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiLlmEndpointOutDocument**](../../models/JsonApiLlmEndpointOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_entity_llm_endpoints**
<a id="delete_entity_llm_endpoints"></a>
> delete_entity_llm_endpoints(id)



### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import llm_endpoints_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = llm_endpoints_api.LLMEndpointsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        api_response = api_instance.delete_entity_llm_endpoints(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMEndpointsApi->delete_entity_llm_endpoints: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "title==someString;provider==LlmEndpointProviderValue",
    }
    try:
        api_response = api_instance.delete_entity_llm_endpoints(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMEndpointsApi->delete_entity_llm_endpoints: %s\n" % e)
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
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#delete_entity_llm_endpoints.ApiResponseFor204) | Successfully deleted

#### delete_entity_llm_endpoints.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_llm_endpoints**
<a id="get_all_entities_llm_endpoints"></a>
> JsonApiLlmEndpointOutList get_all_entities_llm_endpoints()

Get all LLM endpoint entities

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import llm_endpoints_api
from gooddata_api_client.model.json_api_llm_endpoint_out_list import JsonApiLlmEndpointOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = llm_endpoints_api.LLMEndpointsApi(api_client)

    # example passing only optional values
    query_params = {
        'filter': "title==someString;provider==LlmEndpointProviderValue",
        'page': 0,
        'size': 20,
        'sort': [
        "sort_example"
    ],
        'metaInclude': [
        "metaInclude=page,all"
    ],
    }
    try:
        # Get all LLM endpoint entities
        api_response = api_instance.get_all_entities_llm_endpoints(
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMEndpointsApi->get_all_entities_llm_endpoints: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
page | PageSchema | | optional
size | SizeSchema | | optional
sort | SortSchema | | optional
metaInclude | MetaIncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

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
items | str,  | str,  |  | must be one of ["page", "all", "ALL", ] 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_all_entities_llm_endpoints.ApiResponseFor200) | Request successfully processed

#### get_all_entities_llm_endpoints.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiLlmEndpointOutList**](../../models/JsonApiLlmEndpointOutList.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiLlmEndpointOutList**](../../models/JsonApiLlmEndpointOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_llm_endpoints**
<a id="get_entity_llm_endpoints"></a>
> JsonApiLlmEndpointOutDocument get_entity_llm_endpoints(id)

Get LLM endpoint entity

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import llm_endpoints_api
from gooddata_api_client.model.json_api_llm_endpoint_out_document import JsonApiLlmEndpointOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = llm_endpoints_api.LLMEndpointsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Get LLM endpoint entity
        api_response = api_instance.get_entity_llm_endpoints(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMEndpointsApi->get_entity_llm_endpoints: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "title==someString;provider==LlmEndpointProviderValue",
    }
    try:
        # Get LLM endpoint entity
        api_response = api_instance.get_entity_llm_endpoints(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMEndpointsApi->get_entity_llm_endpoints: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
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


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_entity_llm_endpoints.ApiResponseFor200) | Request successfully processed

#### get_entity_llm_endpoints.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiLlmEndpointOutDocument**](../../models/JsonApiLlmEndpointOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiLlmEndpointOutDocument**](../../models/JsonApiLlmEndpointOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **patch_entity_llm_endpoints**
<a id="patch_entity_llm_endpoints"></a>
> JsonApiLlmEndpointOutDocument patch_entity_llm_endpoints(idjson_api_llm_endpoint_patch_document)

Patch LLM endpoint entity

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import llm_endpoints_api
from gooddata_api_client.model.json_api_llm_endpoint_out_document import JsonApiLlmEndpointOutDocument
from gooddata_api_client.model.json_api_llm_endpoint_patch_document import JsonApiLlmEndpointPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = llm_endpoints_api.LLMEndpointsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiLlmEndpointPatchDocument(
        data=JsonApiLlmEndpointPatch(
            attributes=dict(
                base_url="base_url_example",
                llm_model="llm_model_example",
                llm_organization="llm_organization_example",
                provider="OPENAI",
                title="title_example",
                token="token_example",
            ),
            id="id1",
            type="llmEndpoint",
        ),
    )
    try:
        # Patch LLM endpoint entity
        api_response = api_instance.patch_entity_llm_endpoints(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMEndpointsApi->patch_entity_llm_endpoints: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "title==someString;provider==LlmEndpointProviderValue",
    }
    body = JsonApiLlmEndpointPatchDocument(
        data=JsonApiLlmEndpointPatch(
            attributes=dict(
                base_url="base_url_example",
                llm_model="llm_model_example",
                llm_organization="llm_organization_example",
                provider="OPENAI",
                title="title_example",
                token="token_example",
            ),
            id="id1",
            type="llmEndpoint",
        ),
    )
    try:
        # Patch LLM endpoint entity
        api_response = api_instance.patch_entity_llm_endpoints(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMEndpointsApi->patch_entity_llm_endpoints: %s\n" % e)
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
[**JsonApiLlmEndpointPatchDocument**](../../models/JsonApiLlmEndpointPatchDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiLlmEndpointPatchDocument**](../../models/JsonApiLlmEndpointPatchDocument.md) |  | 


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
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#patch_entity_llm_endpoints.ApiResponseFor200) | Request successfully processed

#### patch_entity_llm_endpoints.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiLlmEndpointOutDocument**](../../models/JsonApiLlmEndpointOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiLlmEndpointOutDocument**](../../models/JsonApiLlmEndpointOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_entity_llm_endpoints**
<a id="update_entity_llm_endpoints"></a>
> JsonApiLlmEndpointOutDocument update_entity_llm_endpoints(idjson_api_llm_endpoint_in_document)

PUT LLM endpoint entity

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import llm_endpoints_api
from gooddata_api_client.model.json_api_llm_endpoint_in_document import JsonApiLlmEndpointInDocument
from gooddata_api_client.model.json_api_llm_endpoint_out_document import JsonApiLlmEndpointOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = llm_endpoints_api.LLMEndpointsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiLlmEndpointInDocument(
        data=JsonApiLlmEndpointIn(
            attributes=dict(
                base_url="base_url_example",
                llm_model="llm_model_example",
                llm_organization="llm_organization_example",
                provider="OPENAI",
                title="title_example",
                token="token_example",
            ),
            id="id1",
            type="llmEndpoint",
        ),
    )
    try:
        # PUT LLM endpoint entity
        api_response = api_instance.update_entity_llm_endpoints(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMEndpointsApi->update_entity_llm_endpoints: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "title==someString;provider==LlmEndpointProviderValue",
    }
    body = JsonApiLlmEndpointInDocument(
        data=JsonApiLlmEndpointIn(
            attributes=dict(
                base_url="base_url_example",
                llm_model="llm_model_example",
                llm_organization="llm_organization_example",
                provider="OPENAI",
                title="title_example",
                token="token_example",
            ),
            id="id1",
            type="llmEndpoint",
        ),
    )
    try:
        # PUT LLM endpoint entity
        api_response = api_instance.update_entity_llm_endpoints(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMEndpointsApi->update_entity_llm_endpoints: %s\n" % e)
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
[**JsonApiLlmEndpointInDocument**](../../models/JsonApiLlmEndpointInDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiLlmEndpointInDocument**](../../models/JsonApiLlmEndpointInDocument.md) |  | 


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
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_entity_llm_endpoints.ApiResponseFor200) | Request successfully processed

#### update_entity_llm_endpoints.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiLlmEndpointOutDocument**](../../models/JsonApiLlmEndpointOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiLlmEndpointOutDocument**](../../models/JsonApiLlmEndpointOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


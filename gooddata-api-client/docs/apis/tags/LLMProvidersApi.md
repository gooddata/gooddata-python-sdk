<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.llm_providers_api.LLMProvidersApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_llm_providers**](#create_entity_llm_providers) | **post** /api/v1/entities/llmProviders | Post LLM Provider entities
[**delete_entity_llm_providers**](#delete_entity_llm_providers) | **delete** /api/v1/entities/llmProviders/{id} | Delete LLM Provider entity
[**get_all_entities_llm_providers**](#get_all_entities_llm_providers) | **get** /api/v1/entities/llmProviders | Get all LLM Provider entities
[**get_entity_llm_providers**](#get_entity_llm_providers) | **get** /api/v1/entities/llmProviders/{id} | Get LLM Provider entity
[**patch_entity_llm_providers**](#patch_entity_llm_providers) | **patch** /api/v1/entities/llmProviders/{id} | Patch LLM Provider entity
[**update_entity_llm_providers**](#update_entity_llm_providers) | **put** /api/v1/entities/llmProviders/{id} | PUT LLM Provider entity

# **create_entity_llm_providers**
<a id="create_entity_llm_providers"></a>
> JsonApiLlmProviderOutDocument create_entity_llm_providers(json_api_llm_provider_in_document)

Post LLM Provider entities

LLM Provider - connection configuration for LLM services

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import llm_providers_api
from gooddata_api_client.model.json_api_llm_provider_out_document import JsonApiLlmProviderOutDocument
from gooddata_api_client.model.json_api_llm_provider_in_document import JsonApiLlmProviderInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = llm_providers_api.LLMProvidersApi(api_client)

    # example passing only required values which don't have defaults set
    body = JsonApiLlmProviderInDocument(
        data=JsonApiLlmProviderIn(
            attributes=dict(
                default_model_id="default_model_id_example",
                description="description_example",
                models=[
                    dict(
                        family="OPENAI",
                        id="id_example",
                    )
                ],
                name="name_example",
                provider_config=None,
            ),
            id="id1",
            type="llmProvider",
        ),
    )
    try:
        # Post LLM Provider entities
        api_response = api_instance.create_entity_llm_providers(
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMProvidersApi->create_entity_llm_providers: %s\n" % e)
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
[**JsonApiLlmProviderInDocument**](../../models/JsonApiLlmProviderInDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiLlmProviderInDocument**](../../models/JsonApiLlmProviderInDocument.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#create_entity_llm_providers.ApiResponseFor201) | Request successfully processed

#### create_entity_llm_providers.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationJson, SchemaFor201ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiLlmProviderOutDocument**](../../models/JsonApiLlmProviderOutDocument.md) |  | 


# SchemaFor201ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiLlmProviderOutDocument**](../../models/JsonApiLlmProviderOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_entity_llm_providers**
<a id="delete_entity_llm_providers"></a>
> delete_entity_llm_providers(id)

Delete LLM Provider entity

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import llm_providers_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = llm_providers_api.LLMProvidersApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Delete LLM Provider entity
        api_response = api_instance.delete_entity_llm_providers(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMProvidersApi->delete_entity_llm_providers: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "name==someString;description==someString",
    }
    try:
        # Delete LLM Provider entity
        api_response = api_instance.delete_entity_llm_providers(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMProvidersApi->delete_entity_llm_providers: %s\n" % e)
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
204 | [ApiResponseFor204](#delete_entity_llm_providers.ApiResponseFor204) | Successfully deleted

#### delete_entity_llm_providers.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_llm_providers**
<a id="get_all_entities_llm_providers"></a>
> JsonApiLlmProviderOutList get_all_entities_llm_providers()

Get all LLM Provider entities

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import llm_providers_api
from gooddata_api_client.model.json_api_llm_provider_out_list import JsonApiLlmProviderOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = llm_providers_api.LLMProvidersApi(api_client)

    # example passing only optional values
    query_params = {
        'filter': "name==someString;description==someString",
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
        # Get all LLM Provider entities
        api_response = api_instance.get_all_entities_llm_providers(
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMProvidersApi->get_all_entities_llm_providers: %s\n" % e)
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
200 | [ApiResponseFor200](#get_all_entities_llm_providers.ApiResponseFor200) | Request successfully processed

#### get_all_entities_llm_providers.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiLlmProviderOutList**](../../models/JsonApiLlmProviderOutList.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiLlmProviderOutList**](../../models/JsonApiLlmProviderOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_llm_providers**
<a id="get_entity_llm_providers"></a>
> JsonApiLlmProviderOutDocument get_entity_llm_providers(id)

Get LLM Provider entity

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import llm_providers_api
from gooddata_api_client.model.json_api_llm_provider_out_document import JsonApiLlmProviderOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = llm_providers_api.LLMProvidersApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Get LLM Provider entity
        api_response = api_instance.get_entity_llm_providers(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMProvidersApi->get_entity_llm_providers: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "name==someString;description==someString",
    }
    try:
        # Get LLM Provider entity
        api_response = api_instance.get_entity_llm_providers(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMProvidersApi->get_entity_llm_providers: %s\n" % e)
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
200 | [ApiResponseFor200](#get_entity_llm_providers.ApiResponseFor200) | Request successfully processed

#### get_entity_llm_providers.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiLlmProviderOutDocument**](../../models/JsonApiLlmProviderOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiLlmProviderOutDocument**](../../models/JsonApiLlmProviderOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **patch_entity_llm_providers**
<a id="patch_entity_llm_providers"></a>
> JsonApiLlmProviderOutDocument patch_entity_llm_providers(idjson_api_llm_provider_patch_document)

Patch LLM Provider entity

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import llm_providers_api
from gooddata_api_client.model.json_api_llm_provider_out_document import JsonApiLlmProviderOutDocument
from gooddata_api_client.model.json_api_llm_provider_patch_document import JsonApiLlmProviderPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = llm_providers_api.LLMProvidersApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiLlmProviderPatchDocument(
        data=JsonApiLlmProviderPatch(
            attributes=dict(
                default_model_id="default_model_id_example",
                description="description_example",
                models=[
                    dict(
                        family="OPENAI",
                        id="id_example",
                    )
                ],
                name="name_example",
                provider_config=None,
            ),
            id="id1",
            type="llmProvider",
        ),
    )
    try:
        # Patch LLM Provider entity
        api_response = api_instance.patch_entity_llm_providers(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMProvidersApi->patch_entity_llm_providers: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "name==someString;description==someString",
    }
    body = JsonApiLlmProviderPatchDocument(
        data=JsonApiLlmProviderPatch(
            attributes=dict(
                default_model_id="default_model_id_example",
                description="description_example",
                models=[
                    dict(
                        family="OPENAI",
                        id="id_example",
                    )
                ],
                name="name_example",
                provider_config=None,
            ),
            id="id1",
            type="llmProvider",
        ),
    )
    try:
        # Patch LLM Provider entity
        api_response = api_instance.patch_entity_llm_providers(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMProvidersApi->patch_entity_llm_providers: %s\n" % e)
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
[**JsonApiLlmProviderPatchDocument**](../../models/JsonApiLlmProviderPatchDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiLlmProviderPatchDocument**](../../models/JsonApiLlmProviderPatchDocument.md) |  | 


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
200 | [ApiResponseFor200](#patch_entity_llm_providers.ApiResponseFor200) | Request successfully processed

#### patch_entity_llm_providers.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiLlmProviderOutDocument**](../../models/JsonApiLlmProviderOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiLlmProviderOutDocument**](../../models/JsonApiLlmProviderOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_entity_llm_providers**
<a id="update_entity_llm_providers"></a>
> JsonApiLlmProviderOutDocument update_entity_llm_providers(idjson_api_llm_provider_in_document)

PUT LLM Provider entity

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import llm_providers_api
from gooddata_api_client.model.json_api_llm_provider_out_document import JsonApiLlmProviderOutDocument
from gooddata_api_client.model.json_api_llm_provider_in_document import JsonApiLlmProviderInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = llm_providers_api.LLMProvidersApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiLlmProviderInDocument(
        data=JsonApiLlmProviderIn(
            attributes=dict(
                default_model_id="default_model_id_example",
                description="description_example",
                models=[
                    dict(
                        family="OPENAI",
                        id="id_example",
                    )
                ],
                name="name_example",
                provider_config=None,
            ),
            id="id1",
            type="llmProvider",
        ),
    )
    try:
        # PUT LLM Provider entity
        api_response = api_instance.update_entity_llm_providers(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMProvidersApi->update_entity_llm_providers: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "name==someString;description==someString",
    }
    body = JsonApiLlmProviderInDocument(
        data=JsonApiLlmProviderIn(
            attributes=dict(
                default_model_id="default_model_id_example",
                description="description_example",
                models=[
                    dict(
                        family="OPENAI",
                        id="id_example",
                    )
                ],
                name="name_example",
                provider_config=None,
            ),
            id="id1",
            type="llmProvider",
        ),
    )
    try:
        # PUT LLM Provider entity
        api_response = api_instance.update_entity_llm_providers(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMProvidersApi->update_entity_llm_providers: %s\n" % e)
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
[**JsonApiLlmProviderInDocument**](../../models/JsonApiLlmProviderInDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiLlmProviderInDocument**](../../models/JsonApiLlmProviderInDocument.md) |  | 


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
200 | [ApiResponseFor200](#update_entity_llm_providers.ApiResponseFor200) | Request successfully processed

#### update_entity_llm_providers.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiLlmProviderOutDocument**](../../models/JsonApiLlmProviderOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiLlmProviderOutDocument**](../../models/JsonApiLlmProviderOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


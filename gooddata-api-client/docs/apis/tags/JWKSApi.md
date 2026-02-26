<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.jwks_api.JWKSApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_jwks**](#create_entity_jwks) | **post** /api/v1/entities/jwks | Post Jwks
[**delete_entity_jwks**](#delete_entity_jwks) | **delete** /api/v1/entities/jwks/{id} | Delete Jwk
[**get_all_entities_jwks**](#get_all_entities_jwks) | **get** /api/v1/entities/jwks | Get all Jwks
[**get_entity_jwks**](#get_entity_jwks) | **get** /api/v1/entities/jwks/{id} | Get Jwk
[**patch_entity_jwks**](#patch_entity_jwks) | **patch** /api/v1/entities/jwks/{id} | Patch Jwk
[**update_entity_jwks**](#update_entity_jwks) | **put** /api/v1/entities/jwks/{id} | Put Jwk

# **create_entity_jwks**
<a id="create_entity_jwks"></a>
> JsonApiJwkOutDocument create_entity_jwks(json_api_jwk_in_document)

Post Jwks

Creates JSON web key - used to verify JSON web tokens (Jwts)

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import jwks_api
from gooddata_api_client.model.json_api_jwk_in_document import JsonApiJwkInDocument
from gooddata_api_client.model.json_api_jwk_out_document import JsonApiJwkOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = jwks_api.JWKSApi(api_client)

    # example passing only required values which don't have defaults set
    body = JsonApiJwkInDocument(
        data=JsonApiJwkIn(
            attributes=dict(
                content=dict(),
            ),
            id="id1",
            type="jwk",
        ),
    )
    try:
        # Post Jwks
        api_response = api_instance.create_entity_jwks(
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling JWKSApi->create_entity_jwks: %s\n" % e)
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
[**JsonApiJwkInDocument**](../../models/JsonApiJwkInDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiJwkInDocument**](../../models/JsonApiJwkInDocument.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#create_entity_jwks.ApiResponseFor201) | Request successfully processed

#### create_entity_jwks.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationJson, SchemaFor201ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiJwkOutDocument**](../../models/JsonApiJwkOutDocument.md) |  | 


# SchemaFor201ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiJwkOutDocument**](../../models/JsonApiJwkOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_entity_jwks**
<a id="delete_entity_jwks"></a>
> delete_entity_jwks(id)

Delete Jwk

Deletes JSON web key - used to verify JSON web tokens (Jwts)

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import jwks_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = jwks_api.JWKSApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Delete Jwk
        api_response = api_instance.delete_entity_jwks(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling JWKSApi->delete_entity_jwks: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "content==JwkSpecificationValue",
    }
    try:
        # Delete Jwk
        api_response = api_instance.delete_entity_jwks(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling JWKSApi->delete_entity_jwks: %s\n" % e)
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
204 | [ApiResponseFor204](#delete_entity_jwks.ApiResponseFor204) | Successfully deleted

#### delete_entity_jwks.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_jwks**
<a id="get_all_entities_jwks"></a>
> JsonApiJwkOutList get_all_entities_jwks()

Get all Jwks

Returns all JSON web keys - used to verify JSON web tokens (Jwts)

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import jwks_api
from gooddata_api_client.model.json_api_jwk_out_list import JsonApiJwkOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = jwks_api.JWKSApi(api_client)

    # example passing only optional values
    query_params = {
        'filter': "content==JwkSpecificationValue",
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
        # Get all Jwks
        api_response = api_instance.get_all_entities_jwks(
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling JWKSApi->get_all_entities_jwks: %s\n" % e)
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
200 | [ApiResponseFor200](#get_all_entities_jwks.ApiResponseFor200) | Request successfully processed

#### get_all_entities_jwks.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiJwkOutList**](../../models/JsonApiJwkOutList.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiJwkOutList**](../../models/JsonApiJwkOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_jwks**
<a id="get_entity_jwks"></a>
> JsonApiJwkOutDocument get_entity_jwks(id)

Get Jwk

Returns JSON web key - used to verify JSON web tokens (Jwts)

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import jwks_api
from gooddata_api_client.model.json_api_jwk_out_document import JsonApiJwkOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = jwks_api.JWKSApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Get Jwk
        api_response = api_instance.get_entity_jwks(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling JWKSApi->get_entity_jwks: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "content==JwkSpecificationValue",
    }
    try:
        # Get Jwk
        api_response = api_instance.get_entity_jwks(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling JWKSApi->get_entity_jwks: %s\n" % e)
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
200 | [ApiResponseFor200](#get_entity_jwks.ApiResponseFor200) | Request successfully processed

#### get_entity_jwks.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiJwkOutDocument**](../../models/JsonApiJwkOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiJwkOutDocument**](../../models/JsonApiJwkOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **patch_entity_jwks**
<a id="patch_entity_jwks"></a>
> JsonApiJwkOutDocument patch_entity_jwks(idjson_api_jwk_patch_document)

Patch Jwk

Patches JSON web key - used to verify JSON web tokens (Jwts)

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import jwks_api
from gooddata_api_client.model.json_api_jwk_patch_document import JsonApiJwkPatchDocument
from gooddata_api_client.model.json_api_jwk_out_document import JsonApiJwkOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = jwks_api.JWKSApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiJwkPatchDocument(
        data=JsonApiJwkPatch(
            attributes=dict(
                content=dict(),
            ),
            id="id1",
            type="jwk",
        ),
    )
    try:
        # Patch Jwk
        api_response = api_instance.patch_entity_jwks(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling JWKSApi->patch_entity_jwks: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "content==JwkSpecificationValue",
    }
    body = JsonApiJwkPatchDocument(
        data=JsonApiJwkPatch(
            attributes=dict(
                content=dict(),
            ),
            id="id1",
            type="jwk",
        ),
    )
    try:
        # Patch Jwk
        api_response = api_instance.patch_entity_jwks(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling JWKSApi->patch_entity_jwks: %s\n" % e)
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
[**JsonApiJwkPatchDocument**](../../models/JsonApiJwkPatchDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiJwkPatchDocument**](../../models/JsonApiJwkPatchDocument.md) |  | 


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
200 | [ApiResponseFor200](#patch_entity_jwks.ApiResponseFor200) | Request successfully processed

#### patch_entity_jwks.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiJwkOutDocument**](../../models/JsonApiJwkOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiJwkOutDocument**](../../models/JsonApiJwkOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_entity_jwks**
<a id="update_entity_jwks"></a>
> JsonApiJwkOutDocument update_entity_jwks(idjson_api_jwk_in_document)

Put Jwk

Updates JSON web key - used to verify JSON web tokens (Jwts)

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import jwks_api
from gooddata_api_client.model.json_api_jwk_in_document import JsonApiJwkInDocument
from gooddata_api_client.model.json_api_jwk_out_document import JsonApiJwkOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = jwks_api.JWKSApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiJwkInDocument(
        data=JsonApiJwkIn(
            attributes=dict(
                content=dict(),
            ),
            id="id1",
            type="jwk",
        ),
    )
    try:
        # Put Jwk
        api_response = api_instance.update_entity_jwks(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling JWKSApi->update_entity_jwks: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "content==JwkSpecificationValue",
    }
    body = JsonApiJwkInDocument(
        data=JsonApiJwkIn(
            attributes=dict(
                content=dict(),
            ),
            id="id1",
            type="jwk",
        ),
    )
    try:
        # Put Jwk
        api_response = api_instance.update_entity_jwks(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling JWKSApi->update_entity_jwks: %s\n" % e)
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
[**JsonApiJwkInDocument**](../../models/JsonApiJwkInDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiJwkInDocument**](../../models/JsonApiJwkInDocument.md) |  | 


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
200 | [ApiResponseFor200](#update_entity_jwks.ApiResponseFor200) | Request successfully processed

#### update_entity_jwks.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiJwkOutDocument**](../../models/JsonApiJwkOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiJwkOutDocument**](../../models/JsonApiJwkOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


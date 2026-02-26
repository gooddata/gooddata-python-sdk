<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.identity_providers_api.IdentityProvidersApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_identity_providers**](#create_entity_identity_providers) | **post** /api/v1/entities/identityProviders | Post Identity Providers
[**delete_entity_identity_providers**](#delete_entity_identity_providers) | **delete** /api/v1/entities/identityProviders/{id} | Delete Identity Provider
[**get_all_entities_identity_providers**](#get_all_entities_identity_providers) | **get** /api/v1/entities/identityProviders | Get all Identity Providers
[**get_entity_identity_providers**](#get_entity_identity_providers) | **get** /api/v1/entities/identityProviders/{id} | Get Identity Provider
[**get_identity_providers_layout**](#get_identity_providers_layout) | **get** /api/v1/layout/identityProviders | Get all identity providers layout
[**patch_entity_identity_providers**](#patch_entity_identity_providers) | **patch** /api/v1/entities/identityProviders/{id} | Patch Identity Provider
[**set_identity_providers**](#set_identity_providers) | **put** /api/v1/layout/identityProviders | Set all identity providers
[**update_entity_identity_providers**](#update_entity_identity_providers) | **put** /api/v1/entities/identityProviders/{id} | Put Identity Provider

# **create_entity_identity_providers**
<a id="create_entity_identity_providers"></a>
> JsonApiIdentityProviderOutDocument create_entity_identity_providers(json_api_identity_provider_in_document)

Post Identity Providers

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import identity_providers_api
from gooddata_api_client.model.json_api_identity_provider_out_document import JsonApiIdentityProviderOutDocument
from gooddata_api_client.model.json_api_identity_provider_in_document import JsonApiIdentityProviderInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = identity_providers_api.IdentityProvidersApi(api_client)

    # example passing only required values which don't have defaults set
    body = JsonApiIdentityProviderInDocument(
        data=JsonApiIdentityProviderIn(
            attributes=dict(
                custom_claim_mapping=dict(
                    "key": "key_example",
                ),
                identifiers=["gooddata.com"],
                idp_type="MANAGED_IDP",
                oauth_client_id="oauth_client_id_example",
                oauth_client_secret="oauth_client_secret_example",
                oauth_custom_auth_attributes=dict(
                    "key": "key_example",
                ),
                oauth_custom_scopes=[
                    "oauth_custom_scopes_example"
                ],
                oauth_issuer_id="myOidcProvider",
                oauth_issuer_location="oauth_issuer_location_example",
                oauth_subject_id_claim="oid",
                saml_metadata="saml_metadata_example",
            ),
            id="id1",
            type="identityProvider",
        ),
    )
    try:
        # Post Identity Providers
        api_response = api_instance.create_entity_identity_providers(
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IdentityProvidersApi->create_entity_identity_providers: %s\n" % e)
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
[**JsonApiIdentityProviderInDocument**](../../models/JsonApiIdentityProviderInDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiIdentityProviderInDocument**](../../models/JsonApiIdentityProviderInDocument.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#create_entity_identity_providers.ApiResponseFor201) | Request successfully processed

#### create_entity_identity_providers.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationJson, SchemaFor201ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiIdentityProviderOutDocument**](../../models/JsonApiIdentityProviderOutDocument.md) |  | 


# SchemaFor201ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiIdentityProviderOutDocument**](../../models/JsonApiIdentityProviderOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_entity_identity_providers**
<a id="delete_entity_identity_providers"></a>
> delete_entity_identity_providers(id)

Delete Identity Provider

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import identity_providers_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = identity_providers_api.IdentityProvidersApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Delete Identity Provider
        api_response = api_instance.delete_entity_identity_providers(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IdentityProvidersApi->delete_entity_identity_providers: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "identifiers==v1,v2,v3;customClaimMapping==MapValue",
    }
    try:
        # Delete Identity Provider
        api_response = api_instance.delete_entity_identity_providers(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IdentityProvidersApi->delete_entity_identity_providers: %s\n" % e)
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
204 | [ApiResponseFor204](#delete_entity_identity_providers.ApiResponseFor204) | Successfully deleted

#### delete_entity_identity_providers.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_identity_providers**
<a id="get_all_entities_identity_providers"></a>
> JsonApiIdentityProviderOutList get_all_entities_identity_providers()

Get all Identity Providers

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import identity_providers_api
from gooddata_api_client.model.json_api_identity_provider_out_list import JsonApiIdentityProviderOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = identity_providers_api.IdentityProvidersApi(api_client)

    # example passing only optional values
    query_params = {
        'filter': "identifiers==v1,v2,v3;customClaimMapping==MapValue",
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
        # Get all Identity Providers
        api_response = api_instance.get_all_entities_identity_providers(
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IdentityProvidersApi->get_all_entities_identity_providers: %s\n" % e)
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
200 | [ApiResponseFor200](#get_all_entities_identity_providers.ApiResponseFor200) | Request successfully processed

#### get_all_entities_identity_providers.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiIdentityProviderOutList**](../../models/JsonApiIdentityProviderOutList.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiIdentityProviderOutList**](../../models/JsonApiIdentityProviderOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_identity_providers**
<a id="get_entity_identity_providers"></a>
> JsonApiIdentityProviderOutDocument get_entity_identity_providers(id)

Get Identity Provider

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import identity_providers_api
from gooddata_api_client.model.json_api_identity_provider_out_document import JsonApiIdentityProviderOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = identity_providers_api.IdentityProvidersApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Get Identity Provider
        api_response = api_instance.get_entity_identity_providers(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IdentityProvidersApi->get_entity_identity_providers: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "identifiers==v1,v2,v3;customClaimMapping==MapValue",
    }
    try:
        # Get Identity Provider
        api_response = api_instance.get_entity_identity_providers(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IdentityProvidersApi->get_entity_identity_providers: %s\n" % e)
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
200 | [ApiResponseFor200](#get_entity_identity_providers.ApiResponseFor200) | Request successfully processed

#### get_entity_identity_providers.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiIdentityProviderOutDocument**](../../models/JsonApiIdentityProviderOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiIdentityProviderOutDocument**](../../models/JsonApiIdentityProviderOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_identity_providers_layout**
<a id="get_identity_providers_layout"></a>
> [DeclarativeIdentityProvider] get_identity_providers_layout()

Get all identity providers layout

Gets complete layout of identity providers.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import identity_providers_api
from gooddata_api_client.model.declarative_identity_provider import DeclarativeIdentityProvider
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = identity_providers_api.IdentityProvidersApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get all identity providers layout
        api_response = api_instance.get_identity_providers_layout()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IdentityProvidersApi->get_identity_providers_layout: %s\n" % e)
```
### Parameters
This endpoint does not need any parameter.

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_identity_providers_layout.ApiResponseFor200) | Retrieved layout of all identity providers.

#### get_identity_providers_layout.ApiResponseFor200
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
[**DeclarativeIdentityProvider**]({{complexTypePrefix}}DeclarativeIdentityProvider.md) | [**DeclarativeIdentityProvider**]({{complexTypePrefix}}DeclarativeIdentityProvider.md) | [**DeclarativeIdentityProvider**]({{complexTypePrefix}}DeclarativeIdentityProvider.md) |  | 

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **patch_entity_identity_providers**
<a id="patch_entity_identity_providers"></a>
> JsonApiIdentityProviderOutDocument patch_entity_identity_providers(idjson_api_identity_provider_patch_document)

Patch Identity Provider

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import identity_providers_api
from gooddata_api_client.model.json_api_identity_provider_patch_document import JsonApiIdentityProviderPatchDocument
from gooddata_api_client.model.json_api_identity_provider_out_document import JsonApiIdentityProviderOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = identity_providers_api.IdentityProvidersApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiIdentityProviderPatchDocument(
        data=JsonApiIdentityProviderPatch(
            attributes=dict(
                custom_claim_mapping=dict(
                    "key": "key_example",
                ),
                identifiers=["gooddata.com"],
                idp_type="MANAGED_IDP",
                oauth_client_id="oauth_client_id_example",
                oauth_client_secret="oauth_client_secret_example",
                oauth_custom_auth_attributes=dict(
                    "key": "key_example",
                ),
                oauth_custom_scopes=[
                    "oauth_custom_scopes_example"
                ],
                oauth_issuer_id="myOidcProvider",
                oauth_issuer_location="oauth_issuer_location_example",
                oauth_subject_id_claim="oid",
                saml_metadata="saml_metadata_example",
            ),
            id="id1",
            type="identityProvider",
        ),
    )
    try:
        # Patch Identity Provider
        api_response = api_instance.patch_entity_identity_providers(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IdentityProvidersApi->patch_entity_identity_providers: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "identifiers==v1,v2,v3;customClaimMapping==MapValue",
    }
    body = JsonApiIdentityProviderPatchDocument(
        data=JsonApiIdentityProviderPatch(
            attributes=dict(
                custom_claim_mapping=dict(
                    "key": "key_example",
                ),
                identifiers=["gooddata.com"],
                idp_type="MANAGED_IDP",
                oauth_client_id="oauth_client_id_example",
                oauth_client_secret="oauth_client_secret_example",
                oauth_custom_auth_attributes=dict(
                    "key": "key_example",
                ),
                oauth_custom_scopes=[
                    "oauth_custom_scopes_example"
                ],
                oauth_issuer_id="myOidcProvider",
                oauth_issuer_location="oauth_issuer_location_example",
                oauth_subject_id_claim="oid",
                saml_metadata="saml_metadata_example",
            ),
            id="id1",
            type="identityProvider",
        ),
    )
    try:
        # Patch Identity Provider
        api_response = api_instance.patch_entity_identity_providers(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IdentityProvidersApi->patch_entity_identity_providers: %s\n" % e)
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
[**JsonApiIdentityProviderPatchDocument**](../../models/JsonApiIdentityProviderPatchDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiIdentityProviderPatchDocument**](../../models/JsonApiIdentityProviderPatchDocument.md) |  | 


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
200 | [ApiResponseFor200](#patch_entity_identity_providers.ApiResponseFor200) | Request successfully processed

#### patch_entity_identity_providers.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiIdentityProviderOutDocument**](../../models/JsonApiIdentityProviderOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiIdentityProviderOutDocument**](../../models/JsonApiIdentityProviderOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **set_identity_providers**
<a id="set_identity_providers"></a>
> set_identity_providers(declarative_identity_provider)

Set all identity providers

Sets identity providers in organization.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import identity_providers_api
from gooddata_api_client.model.declarative_identity_provider import DeclarativeIdentityProvider
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = identity_providers_api.IdentityProvidersApi(api_client)

    # example passing only required values which don't have defaults set
    body = [
        DeclarativeIdentityProvider(
            custom_claim_mapping=dict(
                "key": "key_example",
            ),
            id="filterView-1",
            identifiers=["gooddata.com"],
            idp_type="MANAGED_IDP",
            oauth_client_id="oauth_client_id_example",
            oauth_client_secret="oauth_client_secret_example",
            oauth_custom_auth_attributes=dict(
                "key": "key_example",
            ),
            oauth_custom_scopes=[
                "oauth_custom_scopes_example"
            ],
            oauth_issuer_id="myOidcProvider",
            oauth_issuer_location="oauth_issuer_location_example",
            oauth_subject_id_claim="oid",
            saml_metadata="saml_metadata_example",
        )
    ]
    try:
        # Set all identity providers
        api_response = api_instance.set_identity_providers(
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IdentityProvidersApi->set_identity_providers: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeIdentityProvider**]({{complexTypePrefix}}DeclarativeIdentityProvider.md) | [**DeclarativeIdentityProvider**]({{complexTypePrefix}}DeclarativeIdentityProvider.md) | [**DeclarativeIdentityProvider**]({{complexTypePrefix}}DeclarativeIdentityProvider.md) |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#set_identity_providers.ApiResponseFor204) | All identity providers set.

#### set_identity_providers.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_entity_identity_providers**
<a id="update_entity_identity_providers"></a>
> JsonApiIdentityProviderOutDocument update_entity_identity_providers(idjson_api_identity_provider_in_document)

Put Identity Provider

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import identity_providers_api
from gooddata_api_client.model.json_api_identity_provider_out_document import JsonApiIdentityProviderOutDocument
from gooddata_api_client.model.json_api_identity_provider_in_document import JsonApiIdentityProviderInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = identity_providers_api.IdentityProvidersApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiIdentityProviderInDocument(
        data=JsonApiIdentityProviderIn(
            attributes=dict(
                custom_claim_mapping=dict(
                    "key": "key_example",
                ),
                identifiers=["gooddata.com"],
                idp_type="MANAGED_IDP",
                oauth_client_id="oauth_client_id_example",
                oauth_client_secret="oauth_client_secret_example",
                oauth_custom_auth_attributes=dict(
                    "key": "key_example",
                ),
                oauth_custom_scopes=[
                    "oauth_custom_scopes_example"
                ],
                oauth_issuer_id="myOidcProvider",
                oauth_issuer_location="oauth_issuer_location_example",
                oauth_subject_id_claim="oid",
                saml_metadata="saml_metadata_example",
            ),
            id="id1",
            type="identityProvider",
        ),
    )
    try:
        # Put Identity Provider
        api_response = api_instance.update_entity_identity_providers(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IdentityProvidersApi->update_entity_identity_providers: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "identifiers==v1,v2,v3;customClaimMapping==MapValue",
    }
    body = JsonApiIdentityProviderInDocument(
        data=JsonApiIdentityProviderIn(
            attributes=dict(
                custom_claim_mapping=dict(
                    "key": "key_example",
                ),
                identifiers=["gooddata.com"],
                idp_type="MANAGED_IDP",
                oauth_client_id="oauth_client_id_example",
                oauth_client_secret="oauth_client_secret_example",
                oauth_custom_auth_attributes=dict(
                    "key": "key_example",
                ),
                oauth_custom_scopes=[
                    "oauth_custom_scopes_example"
                ],
                oauth_issuer_id="myOidcProvider",
                oauth_issuer_location="oauth_issuer_location_example",
                oauth_subject_id_claim="oid",
                saml_metadata="saml_metadata_example",
            ),
            id="id1",
            type="identityProvider",
        ),
    )
    try:
        # Put Identity Provider
        api_response = api_instance.update_entity_identity_providers(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IdentityProvidersApi->update_entity_identity_providers: %s\n" % e)
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
[**JsonApiIdentityProviderInDocument**](../../models/JsonApiIdentityProviderInDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiIdentityProviderInDocument**](../../models/JsonApiIdentityProviderInDocument.md) |  | 


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
200 | [ApiResponseFor200](#update_entity_identity_providers.ApiResponseFor200) | Request successfully processed

#### update_entity_identity_providers.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiIdentityProviderOutDocument**](../../models/JsonApiIdentityProviderOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiIdentityProviderOutDocument**](../../models/JsonApiIdentityProviderOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


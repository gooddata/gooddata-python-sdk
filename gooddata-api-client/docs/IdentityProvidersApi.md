# gooddata_api_client.IdentityProvidersApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_identity_providers**](IdentityProvidersApi.md#create_entity_identity_providers) | **POST** /api/v1/entities/identityProviders | Post Identity Providers
[**delete_entity_identity_providers**](IdentityProvidersApi.md#delete_entity_identity_providers) | **DELETE** /api/v1/entities/identityProviders/{id} | Delete Identity Provider
[**get_all_entities_identity_providers**](IdentityProvidersApi.md#get_all_entities_identity_providers) | **GET** /api/v1/entities/identityProviders | Get all Identity Providers
[**get_entity_identity_providers**](IdentityProvidersApi.md#get_entity_identity_providers) | **GET** /api/v1/entities/identityProviders/{id} | Get Identity Provider
[**get_identity_providers_layout**](IdentityProvidersApi.md#get_identity_providers_layout) | **GET** /api/v1/layout/identityProviders | Get all identity providers layout
[**patch_entity_identity_providers**](IdentityProvidersApi.md#patch_entity_identity_providers) | **PATCH** /api/v1/entities/identityProviders/{id} | Patch Identity Provider
[**set_identity_providers**](IdentityProvidersApi.md#set_identity_providers) | **PUT** /api/v1/layout/identityProviders | Set all identity providers
[**update_entity_identity_providers**](IdentityProvidersApi.md#update_entity_identity_providers) | **PUT** /api/v1/entities/identityProviders/{id} | Put Identity Provider


# **create_entity_identity_providers**
> JsonApiIdentityProviderOutDocument create_entity_identity_providers(json_api_identity_provider_in_document)

Post Identity Providers

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import identity_providers_api
from gooddata_api_client.model.json_api_identity_provider_out_document import JsonApiIdentityProviderOutDocument
from gooddata_api_client.model.json_api_identity_provider_in_document import JsonApiIdentityProviderInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = identity_providers_api.IdentityProvidersApi(api_client)
    json_api_identity_provider_in_document = JsonApiIdentityProviderInDocument(
        data=JsonApiIdentityProviderIn(
            attributes=JsonApiIdentityProviderInAttributes(
                custom_claim_mapping={
                    "key": "key_example",
                },
                identifiers=["gooddata.com"],
                oauth_client_id="oauth_client_id_example",
                oauth_client_secret="oauth_client_secret_example",
                oauth_issuer_location="oauth_issuer_location_example",
                saml_metadata="saml_metadata_example",
            ),
            id="id1",
            type="identityProvider",
        ),
    ) # JsonApiIdentityProviderInDocument | 

    # example passing only required values which don't have defaults set
    try:
        # Post Identity Providers
        api_response = api_instance.create_entity_identity_providers(json_api_identity_provider_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IdentityProvidersApi->create_entity_identity_providers: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_identity_provider_in_document** | [**JsonApiIdentityProviderInDocument**](JsonApiIdentityProviderInDocument.md)|  |

### Return type

[**JsonApiIdentityProviderOutDocument**](JsonApiIdentityProviderOutDocument.md)

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

# **delete_entity_identity_providers**
> delete_entity_identity_providers(id)

Delete Identity Provider

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import identity_providers_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = identity_providers_api.IdentityProvidersApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=identifiers==v1,v2,v3;customClaimMapping==MapValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete Identity Provider
        api_instance.delete_entity_identity_providers(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IdentityProvidersApi->delete_entity_identity_providers: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete Identity Provider
        api_instance.delete_entity_identity_providers(id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IdentityProvidersApi->delete_entity_identity_providers: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

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

# **get_all_entities_identity_providers**
> JsonApiIdentityProviderOutList get_all_entities_identity_providers()

Get all Identity Providers

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import identity_providers_api
from gooddata_api_client.model.json_api_identity_provider_out_list import JsonApiIdentityProviderOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = identity_providers_api.IdentityProvidersApi(api_client)
    filter = "filter=identifiers==v1,v2,v3;customClaimMapping==MapValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
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
        # Get all Identity Providers
        api_response = api_instance.get_all_entities_identity_providers(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IdentityProvidersApi->get_all_entities_identity_providers: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiIdentityProviderOutList**](JsonApiIdentityProviderOutList.md)

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

# **get_entity_identity_providers**
> JsonApiIdentityProviderOutDocument get_entity_identity_providers(id)

Get Identity Provider

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import identity_providers_api
from gooddata_api_client.model.json_api_identity_provider_out_document import JsonApiIdentityProviderOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = identity_providers_api.IdentityProvidersApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=identifiers==v1,v2,v3;customClaimMapping==MapValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get Identity Provider
        api_response = api_instance.get_entity_identity_providers(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IdentityProvidersApi->get_entity_identity_providers: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Identity Provider
        api_response = api_instance.get_entity_identity_providers(id, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IdentityProvidersApi->get_entity_identity_providers: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiIdentityProviderOutDocument**](JsonApiIdentityProviderOutDocument.md)

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

# **get_identity_providers_layout**
> [DeclarativeIdentityProvider] get_identity_providers_layout()

Get all identity providers layout

Gets complete layout of identity providers.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import identity_providers_api
from gooddata_api_client.model.declarative_identity_provider import DeclarativeIdentityProvider
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
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

### Return type

[**[DeclarativeIdentityProvider]**](DeclarativeIdentityProvider.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved layout of all identity providers. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_identity_providers**
> JsonApiIdentityProviderOutDocument patch_entity_identity_providers(id, json_api_identity_provider_patch_document)

Patch Identity Provider

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import identity_providers_api
from gooddata_api_client.model.json_api_identity_provider_patch_document import JsonApiIdentityProviderPatchDocument
from gooddata_api_client.model.json_api_identity_provider_out_document import JsonApiIdentityProviderOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = identity_providers_api.IdentityProvidersApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_identity_provider_patch_document = JsonApiIdentityProviderPatchDocument(
        data=JsonApiIdentityProviderPatch(
            attributes=JsonApiIdentityProviderPatchAttributes(
                custom_claim_mapping={
                    "key": "key_example",
                },
                identifiers=["gooddata.com"],
                oauth_client_id="oauth_client_id_example",
                oauth_client_secret="oauth_client_secret_example",
                oauth_issuer_location="oauth_issuer_location_example",
                saml_metadata="saml_metadata_example",
            ),
            id="id1",
            type="identityProvider",
        ),
    ) # JsonApiIdentityProviderPatchDocument | 
    filter = "filter=identifiers==v1,v2,v3;customClaimMapping==MapValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch Identity Provider
        api_response = api_instance.patch_entity_identity_providers(id, json_api_identity_provider_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IdentityProvidersApi->patch_entity_identity_providers: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch Identity Provider
        api_response = api_instance.patch_entity_identity_providers(id, json_api_identity_provider_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IdentityProvidersApi->patch_entity_identity_providers: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_identity_provider_patch_document** | [**JsonApiIdentityProviderPatchDocument**](JsonApiIdentityProviderPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiIdentityProviderOutDocument**](JsonApiIdentityProviderOutDocument.md)

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

# **set_identity_providers**
> set_identity_providers(declarative_identity_provider)

Set all identity providers

Sets identity providers in organization.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import identity_providers_api
from gooddata_api_client.model.declarative_identity_provider import DeclarativeIdentityProvider
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = identity_providers_api.IdentityProvidersApi(api_client)
    declarative_identity_provider = [
        DeclarativeIdentityProvider(
            custom_claim_mapping={
                "key": "key_example",
            },
            id="filterView-1",
            identifiers=["gooddata.com"],
            oauth_client_id="oauth_client_id_example",
            oauth_client_secret="oauth_client_secret_example",
            oauth_issuer_location="oauth_issuer_location_example",
            saml_metadata="saml_metadata_example",
        ),
    ] # [DeclarativeIdentityProvider] | 

    # example passing only required values which don't have defaults set
    try:
        # Set all identity providers
        api_instance.set_identity_providers(declarative_identity_provider)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IdentityProvidersApi->set_identity_providers: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **declarative_identity_provider** | [**[DeclarativeIdentityProvider]**](DeclarativeIdentityProvider.md)|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | All identity providers set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_identity_providers**
> JsonApiIdentityProviderOutDocument update_entity_identity_providers(id, json_api_identity_provider_in_document)

Put Identity Provider

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import identity_providers_api
from gooddata_api_client.model.json_api_identity_provider_out_document import JsonApiIdentityProviderOutDocument
from gooddata_api_client.model.json_api_identity_provider_in_document import JsonApiIdentityProviderInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = identity_providers_api.IdentityProvidersApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_identity_provider_in_document = JsonApiIdentityProviderInDocument(
        data=JsonApiIdentityProviderIn(
            attributes=JsonApiIdentityProviderInAttributes(
                custom_claim_mapping={
                    "key": "key_example",
                },
                identifiers=["gooddata.com"],
                oauth_client_id="oauth_client_id_example",
                oauth_client_secret="oauth_client_secret_example",
                oauth_issuer_location="oauth_issuer_location_example",
                saml_metadata="saml_metadata_example",
            ),
            id="id1",
            type="identityProvider",
        ),
    ) # JsonApiIdentityProviderInDocument | 
    filter = "filter=identifiers==v1,v2,v3;customClaimMapping==MapValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put Identity Provider
        api_response = api_instance.update_entity_identity_providers(id, json_api_identity_provider_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IdentityProvidersApi->update_entity_identity_providers: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put Identity Provider
        api_response = api_instance.update_entity_identity_providers(id, json_api_identity_provider_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling IdentityProvidersApi->update_entity_identity_providers: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_identity_provider_in_document** | [**JsonApiIdentityProviderInDocument**](JsonApiIdentityProviderInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiIdentityProviderOutDocument**](JsonApiIdentityProviderOutDocument.md)

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


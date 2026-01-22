# gooddata_api_client.JWKSApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_jwks**](JWKSApi.md#create_entity_jwks) | **POST** /api/v1/entities/jwks | Post Jwks
[**delete_entity_jwks**](JWKSApi.md#delete_entity_jwks) | **DELETE** /api/v1/entities/jwks/{id} | Delete Jwk
[**get_all_entities_jwks**](JWKSApi.md#get_all_entities_jwks) | **GET** /api/v1/entities/jwks | Get all Jwks
[**get_entity_jwks**](JWKSApi.md#get_entity_jwks) | **GET** /api/v1/entities/jwks/{id} | Get Jwk
[**patch_entity_jwks**](JWKSApi.md#patch_entity_jwks) | **PATCH** /api/v1/entities/jwks/{id} | Patch Jwk
[**update_entity_jwks**](JWKSApi.md#update_entity_jwks) | **PUT** /api/v1/entities/jwks/{id} | Put Jwk


# **create_entity_jwks**
> JsonApiJwkOutDocument create_entity_jwks(json_api_jwk_in_document)

Post Jwks

Creates JSON web key - used to verify JSON web tokens (Jwts)

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import jwks_api
from gooddata_api_client.model.json_api_jwk_in_document import JsonApiJwkInDocument
from gooddata_api_client.model.json_api_jwk_out_document import JsonApiJwkOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = jwks_api.JWKSApi(api_client)
    json_api_jwk_in_document = JsonApiJwkInDocument(
        data=JsonApiJwkIn(
            attributes=JsonApiJwkInAttributes(
                content=JsonApiJwkInAttributesContent(),
            ),
            id="id1",
            type="jwk",
        ),
    ) # JsonApiJwkInDocument | 

    # example passing only required values which don't have defaults set
    try:
        # Post Jwks
        api_response = api_instance.create_entity_jwks(json_api_jwk_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling JWKSApi->create_entity_jwks: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_jwk_in_document** | [**JsonApiJwkInDocument**](JsonApiJwkInDocument.md)|  |

### Return type

[**JsonApiJwkOutDocument**](JsonApiJwkOutDocument.md)

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

# **delete_entity_jwks**
> delete_entity_jwks(id)

Delete Jwk

Deletes JSON web key - used to verify JSON web tokens (Jwts)

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import jwks_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = jwks_api.JWKSApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "content==JwkSpecificationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete Jwk
        api_instance.delete_entity_jwks(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling JWKSApi->delete_entity_jwks: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete Jwk
        api_instance.delete_entity_jwks(id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling JWKSApi->delete_entity_jwks: %s\n" % e)
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

# **get_all_entities_jwks**
> JsonApiJwkOutList get_all_entities_jwks()

Get all Jwks

Returns all JSON web keys - used to verify JSON web tokens (Jwts)

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import jwks_api
from gooddata_api_client.model.json_api_jwk_out_list import JsonApiJwkOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = jwks_api.JWKSApi(api_client)
    filter = "content==JwkSpecificationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
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
        # Get all Jwks
        api_response = api_instance.get_all_entities_jwks(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling JWKSApi->get_all_entities_jwks: %s\n" % e)
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

[**JsonApiJwkOutList**](JsonApiJwkOutList.md)

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

# **get_entity_jwks**
> JsonApiJwkOutDocument get_entity_jwks(id)

Get Jwk

Returns JSON web key - used to verify JSON web tokens (Jwts)

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import jwks_api
from gooddata_api_client.model.json_api_jwk_out_document import JsonApiJwkOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = jwks_api.JWKSApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "content==JwkSpecificationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get Jwk
        api_response = api_instance.get_entity_jwks(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling JWKSApi->get_entity_jwks: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Jwk
        api_response = api_instance.get_entity_jwks(id, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling JWKSApi->get_entity_jwks: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiJwkOutDocument**](JsonApiJwkOutDocument.md)

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

# **patch_entity_jwks**
> JsonApiJwkOutDocument patch_entity_jwks(id, json_api_jwk_patch_document)

Patch Jwk

Patches JSON web key - used to verify JSON web tokens (Jwts)

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import jwks_api
from gooddata_api_client.model.json_api_jwk_patch_document import JsonApiJwkPatchDocument
from gooddata_api_client.model.json_api_jwk_out_document import JsonApiJwkOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = jwks_api.JWKSApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_jwk_patch_document = JsonApiJwkPatchDocument(
        data=JsonApiJwkPatch(
            attributes=JsonApiJwkInAttributes(
                content=JsonApiJwkInAttributesContent(),
            ),
            id="id1",
            type="jwk",
        ),
    ) # JsonApiJwkPatchDocument | 
    filter = "content==JwkSpecificationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch Jwk
        api_response = api_instance.patch_entity_jwks(id, json_api_jwk_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling JWKSApi->patch_entity_jwks: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch Jwk
        api_response = api_instance.patch_entity_jwks(id, json_api_jwk_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling JWKSApi->patch_entity_jwks: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_jwk_patch_document** | [**JsonApiJwkPatchDocument**](JsonApiJwkPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiJwkOutDocument**](JsonApiJwkOutDocument.md)

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

# **update_entity_jwks**
> JsonApiJwkOutDocument update_entity_jwks(id, json_api_jwk_in_document)

Put Jwk

Updates JSON web key - used to verify JSON web tokens (Jwts)

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import jwks_api
from gooddata_api_client.model.json_api_jwk_in_document import JsonApiJwkInDocument
from gooddata_api_client.model.json_api_jwk_out_document import JsonApiJwkOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = jwks_api.JWKSApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_jwk_in_document = JsonApiJwkInDocument(
        data=JsonApiJwkIn(
            attributes=JsonApiJwkInAttributes(
                content=JsonApiJwkInAttributesContent(),
            ),
            id="id1",
            type="jwk",
        ),
    ) # JsonApiJwkInDocument | 
    filter = "content==JwkSpecificationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put Jwk
        api_response = api_instance.update_entity_jwks(id, json_api_jwk_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling JWKSApi->update_entity_jwks: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put Jwk
        api_response = api_instance.update_entity_jwks(id, json_api_jwk_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling JWKSApi->update_entity_jwks: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_jwk_in_document** | [**JsonApiJwkInDocument**](JsonApiJwkInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiJwkOutDocument**](JsonApiJwkOutDocument.md)

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


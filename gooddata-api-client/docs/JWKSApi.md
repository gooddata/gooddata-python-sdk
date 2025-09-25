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
import gooddata_api_client
from gooddata_api_client.models.json_api_jwk_in_document import JsonApiJwkInDocument
from gooddata_api_client.models.json_api_jwk_out_document import JsonApiJwkOutDocument
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.JWKSApi(api_client)
    json_api_jwk_in_document = gooddata_api_client.JsonApiJwkInDocument() # JsonApiJwkInDocument | 

    try:
        # Post Jwks
        api_response = api_instance.create_entity_jwks(json_api_jwk_in_document)
        print("The response of JWKSApi->create_entity_jwks:\n")
        pprint(api_response)
    except Exception as e:
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

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_jwks**
> delete_entity_jwks(id, filter=filter)

Delete Jwk

Deletes JSON web key - used to verify JSON web tokens (Jwts)

### Example


```python
import gooddata_api_client
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.JWKSApi(api_client)
    id = 'id_example' # str | 
    filter = 'content==JwkSpecificationValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Delete Jwk
        api_instance.delete_entity_jwks(id, filter=filter)
    except Exception as e:
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
> JsonApiJwkOutList get_all_entities_jwks(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)

Get all Jwks

Returns all JSON web keys - used to verify JSON web tokens (Jwts)

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_jwk_out_list import JsonApiJwkOutList
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.JWKSApi(api_client)
    filter = 'content==JwkSpecificationValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get all Jwks
        api_response = api_instance.get_all_entities_jwks(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of JWKSApi->get_all_entities_jwks:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling JWKSApi->get_all_entities_jwks: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **page** | **int**| Zero-based page index (0..N) | [optional] [default to 0]
 **size** | **int**| The size of the page to be returned | [optional] [default to 20]
 **sort** | [**List[str]**](str.md)| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiJwkOutList**](JsonApiJwkOutList.md)

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

# **get_entity_jwks**
> JsonApiJwkOutDocument get_entity_jwks(id, filter=filter)

Get Jwk

Returns JSON web key - used to verify JSON web tokens (Jwts)

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_jwk_out_document import JsonApiJwkOutDocument
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.JWKSApi(api_client)
    id = 'id_example' # str | 
    filter = 'content==JwkSpecificationValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Get Jwk
        api_response = api_instance.get_entity_jwks(id, filter=filter)
        print("The response of JWKSApi->get_entity_jwks:\n")
        pprint(api_response)
    except Exception as e:
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
 - **Accept**: application/vnd.gooddata.api+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_jwks**
> JsonApiJwkOutDocument patch_entity_jwks(id, json_api_jwk_patch_document, filter=filter)

Patch Jwk

Patches JSON web key - used to verify JSON web tokens (Jwts)

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_jwk_out_document import JsonApiJwkOutDocument
from gooddata_api_client.models.json_api_jwk_patch_document import JsonApiJwkPatchDocument
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.JWKSApi(api_client)
    id = 'id_example' # str | 
    json_api_jwk_patch_document = gooddata_api_client.JsonApiJwkPatchDocument() # JsonApiJwkPatchDocument | 
    filter = 'content==JwkSpecificationValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Patch Jwk
        api_response = api_instance.patch_entity_jwks(id, json_api_jwk_patch_document, filter=filter)
        print("The response of JWKSApi->patch_entity_jwks:\n")
        pprint(api_response)
    except Exception as e:
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

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_jwks**
> JsonApiJwkOutDocument update_entity_jwks(id, json_api_jwk_in_document, filter=filter)

Put Jwk

Updates JSON web key - used to verify JSON web tokens (Jwts)

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_jwk_in_document import JsonApiJwkInDocument
from gooddata_api_client.models.json_api_jwk_out_document import JsonApiJwkOutDocument
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.JWKSApi(api_client)
    id = 'id_example' # str | 
    json_api_jwk_in_document = gooddata_api_client.JsonApiJwkInDocument() # JsonApiJwkInDocument | 
    filter = 'content==JwkSpecificationValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Put Jwk
        api_response = api_instance.update_entity_jwks(id, json_api_jwk_in_document, filter=filter)
        print("The response of JWKSApi->update_entity_jwks:\n")
        pprint(api_response)
    except Exception as e:
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

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


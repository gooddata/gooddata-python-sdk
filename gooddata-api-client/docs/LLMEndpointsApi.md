# gooddata_api_client.LLMEndpointsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_llm_endpoints**](LLMEndpointsApi.md#create_entity_llm_endpoints) | **POST** /api/v1/entities/llmEndpoints | Post LLM endpoint entities
[**delete_entity_llm_endpoints**](LLMEndpointsApi.md#delete_entity_llm_endpoints) | **DELETE** /api/v1/entities/llmEndpoints/{id} | 
[**get_all_entities_llm_endpoints**](LLMEndpointsApi.md#get_all_entities_llm_endpoints) | **GET** /api/v1/entities/llmEndpoints | Get all LLM endpoint entities
[**get_entity_llm_endpoints**](LLMEndpointsApi.md#get_entity_llm_endpoints) | **GET** /api/v1/entities/llmEndpoints/{id} | Get LLM endpoint entity
[**patch_entity_llm_endpoints**](LLMEndpointsApi.md#patch_entity_llm_endpoints) | **PATCH** /api/v1/entities/llmEndpoints/{id} | Patch LLM endpoint entity
[**update_entity_llm_endpoints**](LLMEndpointsApi.md#update_entity_llm_endpoints) | **PUT** /api/v1/entities/llmEndpoints/{id} | PUT LLM endpoint entity


# **create_entity_llm_endpoints**
> JsonApiLlmEndpointOutDocument create_entity_llm_endpoints(json_api_llm_endpoint_in_document)

Post LLM endpoint entities

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_llm_endpoint_in_document import JsonApiLlmEndpointInDocument
from gooddata_api_client.models.json_api_llm_endpoint_out_document import JsonApiLlmEndpointOutDocument
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
    api_instance = gooddata_api_client.LLMEndpointsApi(api_client)
    json_api_llm_endpoint_in_document = gooddata_api_client.JsonApiLlmEndpointInDocument() # JsonApiLlmEndpointInDocument | 

    try:
        # Post LLM endpoint entities
        api_response = api_instance.create_entity_llm_endpoints(json_api_llm_endpoint_in_document)
        print("The response of LLMEndpointsApi->create_entity_llm_endpoints:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LLMEndpointsApi->create_entity_llm_endpoints: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_llm_endpoint_in_document** | [**JsonApiLlmEndpointInDocument**](JsonApiLlmEndpointInDocument.md)|  | 

### Return type

[**JsonApiLlmEndpointOutDocument**](JsonApiLlmEndpointOutDocument.md)

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

# **delete_entity_llm_endpoints**
> delete_entity_llm_endpoints(id, filter=filter)



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
    api_instance = gooddata_api_client.LLMEndpointsApi(api_client)
    id = 'id_example' # str | 
    filter = 'title==someString;provider==LLMProviderValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        api_instance.delete_entity_llm_endpoints(id, filter=filter)
    except Exception as e:
        print("Exception when calling LLMEndpointsApi->delete_entity_llm_endpoints: %s\n" % e)
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

# **get_all_entities_llm_endpoints**
> JsonApiLlmEndpointOutList get_all_entities_llm_endpoints(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)

Get all LLM endpoint entities

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_llm_endpoint_out_list import JsonApiLlmEndpointOutList
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
    api_instance = gooddata_api_client.LLMEndpointsApi(api_client)
    filter = 'title==someString;provider==LLMProviderValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get all LLM endpoint entities
        api_response = api_instance.get_all_entities_llm_endpoints(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of LLMEndpointsApi->get_all_entities_llm_endpoints:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LLMEndpointsApi->get_all_entities_llm_endpoints: %s\n" % e)
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

[**JsonApiLlmEndpointOutList**](JsonApiLlmEndpointOutList.md)

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

# **get_entity_llm_endpoints**
> JsonApiLlmEndpointOutDocument get_entity_llm_endpoints(id, filter=filter)

Get LLM endpoint entity

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_llm_endpoint_out_document import JsonApiLlmEndpointOutDocument
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
    api_instance = gooddata_api_client.LLMEndpointsApi(api_client)
    id = 'id_example' # str | 
    filter = 'title==someString;provider==LLMProviderValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Get LLM endpoint entity
        api_response = api_instance.get_entity_llm_endpoints(id, filter=filter)
        print("The response of LLMEndpointsApi->get_entity_llm_endpoints:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LLMEndpointsApi->get_entity_llm_endpoints: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiLlmEndpointOutDocument**](JsonApiLlmEndpointOutDocument.md)

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

# **patch_entity_llm_endpoints**
> JsonApiLlmEndpointOutDocument patch_entity_llm_endpoints(id, json_api_llm_endpoint_patch_document, filter=filter)

Patch LLM endpoint entity

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_llm_endpoint_out_document import JsonApiLlmEndpointOutDocument
from gooddata_api_client.models.json_api_llm_endpoint_patch_document import JsonApiLlmEndpointPatchDocument
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
    api_instance = gooddata_api_client.LLMEndpointsApi(api_client)
    id = 'id_example' # str | 
    json_api_llm_endpoint_patch_document = gooddata_api_client.JsonApiLlmEndpointPatchDocument() # JsonApiLlmEndpointPatchDocument | 
    filter = 'title==someString;provider==LLMProviderValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Patch LLM endpoint entity
        api_response = api_instance.patch_entity_llm_endpoints(id, json_api_llm_endpoint_patch_document, filter=filter)
        print("The response of LLMEndpointsApi->patch_entity_llm_endpoints:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LLMEndpointsApi->patch_entity_llm_endpoints: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_llm_endpoint_patch_document** | [**JsonApiLlmEndpointPatchDocument**](JsonApiLlmEndpointPatchDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiLlmEndpointOutDocument**](JsonApiLlmEndpointOutDocument.md)

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

# **update_entity_llm_endpoints**
> JsonApiLlmEndpointOutDocument update_entity_llm_endpoints(id, json_api_llm_endpoint_in_document, filter=filter)

PUT LLM endpoint entity

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_llm_endpoint_in_document import JsonApiLlmEndpointInDocument
from gooddata_api_client.models.json_api_llm_endpoint_out_document import JsonApiLlmEndpointOutDocument
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
    api_instance = gooddata_api_client.LLMEndpointsApi(api_client)
    id = 'id_example' # str | 
    json_api_llm_endpoint_in_document = gooddata_api_client.JsonApiLlmEndpointInDocument() # JsonApiLlmEndpointInDocument | 
    filter = 'title==someString;provider==LLMProviderValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # PUT LLM endpoint entity
        api_response = api_instance.update_entity_llm_endpoints(id, json_api_llm_endpoint_in_document, filter=filter)
        print("The response of LLMEndpointsApi->update_entity_llm_endpoints:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LLMEndpointsApi->update_entity_llm_endpoints: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_llm_endpoint_in_document** | [**JsonApiLlmEndpointInDocument**](JsonApiLlmEndpointInDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiLlmEndpointOutDocument**](JsonApiLlmEndpointOutDocument.md)

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


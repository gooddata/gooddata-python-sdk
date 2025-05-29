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
import time
import gooddata_api_client
from gooddata_api_client.api import llm_endpoints_api
from gooddata_api_client.model.json_api_llm_endpoint_in_document import JsonApiLlmEndpointInDocument
from gooddata_api_client.model.json_api_llm_endpoint_out_document import JsonApiLlmEndpointOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = llm_endpoints_api.LLMEndpointsApi(api_client)
    json_api_llm_endpoint_in_document = JsonApiLlmEndpointInDocument(
        data=JsonApiLlmEndpointIn(
            attributes=JsonApiLlmEndpointInAttributes(
                base_url="base_url_example",
                description="description_example",
                llm_model="llm_model_example",
                llm_organization="llm_organization_example",
                provider="OPENAI",
                title="title_example",
                token="token_example",
            ),
            id="id1",
            type="llmEndpoint",
        ),
    ) # JsonApiLlmEndpointInDocument | 

    # example passing only required values which don't have defaults set
    try:
        # Post LLM endpoint entities
        api_response = api_instance.create_entity_llm_endpoints(json_api_llm_endpoint_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
> delete_entity_llm_endpoints(id)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import llm_endpoints_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = llm_endpoints_api.LLMEndpointsApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_entity_llm_endpoints(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMEndpointsApi->delete_entity_llm_endpoints: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_instance.delete_entity_llm_endpoints(id, filter=filter)
    except gooddata_api_client.ApiException as e:
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
> JsonApiLlmEndpointOutList get_all_entities_llm_endpoints()

Get all LLM endpoint entities

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import llm_endpoints_api
from gooddata_api_client.model.json_api_llm_endpoint_out_list import JsonApiLlmEndpointOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = llm_endpoints_api.LLMEndpointsApi(api_client)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
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
        # Get all LLM endpoint entities
        api_response = api_instance.get_all_entities_llm_endpoints(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMEndpointsApi->get_all_entities_llm_endpoints: %s\n" % e)
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
> JsonApiLlmEndpointOutDocument get_entity_llm_endpoints(id)

Get LLM endpoint entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import llm_endpoints_api
from gooddata_api_client.model.json_api_llm_endpoint_out_document import JsonApiLlmEndpointOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = llm_endpoints_api.LLMEndpointsApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get LLM endpoint entity
        api_response = api_instance.get_entity_llm_endpoints(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMEndpointsApi->get_entity_llm_endpoints: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get LLM endpoint entity
        api_response = api_instance.get_entity_llm_endpoints(id, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
> JsonApiLlmEndpointOutDocument patch_entity_llm_endpoints(id, json_api_llm_endpoint_patch_document)

Patch LLM endpoint entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import llm_endpoints_api
from gooddata_api_client.model.json_api_llm_endpoint_out_document import JsonApiLlmEndpointOutDocument
from gooddata_api_client.model.json_api_llm_endpoint_patch_document import JsonApiLlmEndpointPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = llm_endpoints_api.LLMEndpointsApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_llm_endpoint_patch_document = JsonApiLlmEndpointPatchDocument(
        data=JsonApiLlmEndpointPatch(
            attributes=JsonApiLlmEndpointPatchAttributes(
                base_url="base_url_example",
                description="description_example",
                llm_model="llm_model_example",
                llm_organization="llm_organization_example",
                provider="OPENAI",
                title="title_example",
                token="token_example",
            ),
            id="id1",
            type="llmEndpoint",
        ),
    ) # JsonApiLlmEndpointPatchDocument | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch LLM endpoint entity
        api_response = api_instance.patch_entity_llm_endpoints(id, json_api_llm_endpoint_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMEndpointsApi->patch_entity_llm_endpoints: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch LLM endpoint entity
        api_response = api_instance.patch_entity_llm_endpoints(id, json_api_llm_endpoint_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
> JsonApiLlmEndpointOutDocument update_entity_llm_endpoints(id, json_api_llm_endpoint_in_document)

PUT LLM endpoint entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import llm_endpoints_api
from gooddata_api_client.model.json_api_llm_endpoint_in_document import JsonApiLlmEndpointInDocument
from gooddata_api_client.model.json_api_llm_endpoint_out_document import JsonApiLlmEndpointOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = llm_endpoints_api.LLMEndpointsApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_llm_endpoint_in_document = JsonApiLlmEndpointInDocument(
        data=JsonApiLlmEndpointIn(
            attributes=JsonApiLlmEndpointInAttributes(
                base_url="base_url_example",
                description="description_example",
                llm_model="llm_model_example",
                llm_organization="llm_organization_example",
                provider="OPENAI",
                title="title_example",
                token="token_example",
            ),
            id="id1",
            type="llmEndpoint",
        ),
    ) # JsonApiLlmEndpointInDocument | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # PUT LLM endpoint entity
        api_response = api_instance.update_entity_llm_endpoints(id, json_api_llm_endpoint_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMEndpointsApi->update_entity_llm_endpoints: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # PUT LLM endpoint entity
        api_response = api_instance.update_entity_llm_endpoints(id, json_api_llm_endpoint_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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


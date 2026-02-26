# gooddata_api_client.LLMProvidersApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_llm_providers**](LLMProvidersApi.md#create_entity_llm_providers) | **POST** /api/v1/entities/llmProviders | Post LLM Provider entities
[**delete_entity_llm_providers**](LLMProvidersApi.md#delete_entity_llm_providers) | **DELETE** /api/v1/entities/llmProviders/{id} | Delete LLM Provider entity
[**get_all_entities_llm_providers**](LLMProvidersApi.md#get_all_entities_llm_providers) | **GET** /api/v1/entities/llmProviders | Get all LLM Provider entities
[**get_entity_llm_providers**](LLMProvidersApi.md#get_entity_llm_providers) | **GET** /api/v1/entities/llmProviders/{id} | Get LLM Provider entity
[**patch_entity_llm_providers**](LLMProvidersApi.md#patch_entity_llm_providers) | **PATCH** /api/v1/entities/llmProviders/{id} | Patch LLM Provider entity
[**update_entity_llm_providers**](LLMProvidersApi.md#update_entity_llm_providers) | **PUT** /api/v1/entities/llmProviders/{id} | PUT LLM Provider entity


# **create_entity_llm_providers**
> JsonApiLlmProviderOutDocument create_entity_llm_providers(json_api_llm_provider_in_document)

Post LLM Provider entities

LLM Provider - connection configuration for LLM services

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import llm_providers_api
from gooddata_api_client.model.json_api_llm_provider_out_document import JsonApiLlmProviderOutDocument
from gooddata_api_client.model.json_api_llm_provider_in_document import JsonApiLlmProviderInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = llm_providers_api.LLMProvidersApi(api_client)
    json_api_llm_provider_in_document = JsonApiLlmProviderInDocument(
        data=JsonApiLlmProviderIn(
            attributes=JsonApiLlmProviderInAttributes(
                default_model_id="default_model_id_example",
                description="description_example",
                models=[
                    JsonApiLlmProviderInAttributesModelsInner(
                        family="OPENAI",
                        id="id_example",
                    ),
                ],
                name="name_example",
                provider_config=JsonApiLlmProviderInAttributesProviderConfig(None),
            ),
            id="id1",
            type="llmProvider",
        ),
    ) # JsonApiLlmProviderInDocument | 

    # example passing only required values which don't have defaults set
    try:
        # Post LLM Provider entities
        api_response = api_instance.create_entity_llm_providers(json_api_llm_provider_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMProvidersApi->create_entity_llm_providers: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_llm_provider_in_document** | [**JsonApiLlmProviderInDocument**](JsonApiLlmProviderInDocument.md)|  |

### Return type

[**JsonApiLlmProviderOutDocument**](JsonApiLlmProviderOutDocument.md)

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

# **delete_entity_llm_providers**
> delete_entity_llm_providers(id)

Delete LLM Provider entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import llm_providers_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = llm_providers_api.LLMProvidersApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "name==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete LLM Provider entity
        api_instance.delete_entity_llm_providers(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMProvidersApi->delete_entity_llm_providers: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete LLM Provider entity
        api_instance.delete_entity_llm_providers(id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMProvidersApi->delete_entity_llm_providers: %s\n" % e)
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

# **get_all_entities_llm_providers**
> JsonApiLlmProviderOutList get_all_entities_llm_providers()

Get all LLM Provider entities

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import llm_providers_api
from gooddata_api_client.model.json_api_llm_provider_out_list import JsonApiLlmProviderOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = llm_providers_api.LLMProvidersApi(api_client)
    filter = "name==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
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
        # Get all LLM Provider entities
        api_response = api_instance.get_all_entities_llm_providers(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMProvidersApi->get_all_entities_llm_providers: %s\n" % e)
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

[**JsonApiLlmProviderOutList**](JsonApiLlmProviderOutList.md)

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

# **get_entity_llm_providers**
> JsonApiLlmProviderOutDocument get_entity_llm_providers(id)

Get LLM Provider entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import llm_providers_api
from gooddata_api_client.model.json_api_llm_provider_out_document import JsonApiLlmProviderOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = llm_providers_api.LLMProvidersApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "name==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get LLM Provider entity
        api_response = api_instance.get_entity_llm_providers(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMProvidersApi->get_entity_llm_providers: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get LLM Provider entity
        api_response = api_instance.get_entity_llm_providers(id, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMProvidersApi->get_entity_llm_providers: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiLlmProviderOutDocument**](JsonApiLlmProviderOutDocument.md)

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

# **patch_entity_llm_providers**
> JsonApiLlmProviderOutDocument patch_entity_llm_providers(id, json_api_llm_provider_patch_document)

Patch LLM Provider entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import llm_providers_api
from gooddata_api_client.model.json_api_llm_provider_out_document import JsonApiLlmProviderOutDocument
from gooddata_api_client.model.json_api_llm_provider_patch_document import JsonApiLlmProviderPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = llm_providers_api.LLMProvidersApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_llm_provider_patch_document = JsonApiLlmProviderPatchDocument(
        data=JsonApiLlmProviderPatch(
            attributes=JsonApiLlmProviderPatchAttributes(
                default_model_id="default_model_id_example",
                description="description_example",
                models=[
                    JsonApiLlmProviderInAttributesModelsInner(
                        family="OPENAI",
                        id="id_example",
                    ),
                ],
                name="name_example",
                provider_config=JsonApiLlmProviderInAttributesProviderConfig(None),
            ),
            id="id1",
            type="llmProvider",
        ),
    ) # JsonApiLlmProviderPatchDocument | 
    filter = "name==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch LLM Provider entity
        api_response = api_instance.patch_entity_llm_providers(id, json_api_llm_provider_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMProvidersApi->patch_entity_llm_providers: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch LLM Provider entity
        api_response = api_instance.patch_entity_llm_providers(id, json_api_llm_provider_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMProvidersApi->patch_entity_llm_providers: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_llm_provider_patch_document** | [**JsonApiLlmProviderPatchDocument**](JsonApiLlmProviderPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiLlmProviderOutDocument**](JsonApiLlmProviderOutDocument.md)

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

# **update_entity_llm_providers**
> JsonApiLlmProviderOutDocument update_entity_llm_providers(id, json_api_llm_provider_in_document)

PUT LLM Provider entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import llm_providers_api
from gooddata_api_client.model.json_api_llm_provider_out_document import JsonApiLlmProviderOutDocument
from gooddata_api_client.model.json_api_llm_provider_in_document import JsonApiLlmProviderInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = llm_providers_api.LLMProvidersApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_llm_provider_in_document = JsonApiLlmProviderInDocument(
        data=JsonApiLlmProviderIn(
            attributes=JsonApiLlmProviderInAttributes(
                default_model_id="default_model_id_example",
                description="description_example",
                models=[
                    JsonApiLlmProviderInAttributesModelsInner(
                        family="OPENAI",
                        id="id_example",
                    ),
                ],
                name="name_example",
                provider_config=JsonApiLlmProviderInAttributesProviderConfig(None),
            ),
            id="id1",
            type="llmProvider",
        ),
    ) # JsonApiLlmProviderInDocument | 
    filter = "name==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # PUT LLM Provider entity
        api_response = api_instance.update_entity_llm_providers(id, json_api_llm_provider_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMProvidersApi->update_entity_llm_providers: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # PUT LLM Provider entity
        api_response = api_instance.update_entity_llm_providers(id, json_api_llm_provider_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMProvidersApi->update_entity_llm_providers: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_llm_provider_in_document** | [**JsonApiLlmProviderInDocument**](JsonApiLlmProviderInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiLlmProviderOutDocument**](JsonApiLlmProviderOutDocument.md)

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


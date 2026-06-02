# gooddata_api_client.LLMEndpointsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity**](LLMEndpointsApi.md#create_entity) | **POST** /api/v1/entities/llmEndpoints | Post LLM endpoint entities (Removed)
[**delete_entity**](LLMEndpointsApi.md#delete_entity) | **DELETE** /api/v1/entities/llmEndpoints/{id} | Delete LLM endpoint entity (Removed)
[**get_all_entities**](LLMEndpointsApi.md#get_all_entities) | **GET** /api/v1/entities/llmEndpoints | Get all LLM endpoint entities (Removed)
[**get_entity**](LLMEndpointsApi.md#get_entity) | **GET** /api/v1/entities/llmEndpoints/{id} | Get LLM endpoint entity (Removed)
[**patch_entity**](LLMEndpointsApi.md#patch_entity) | **PATCH** /api/v1/entities/llmEndpoints/{id} | Patch LLM endpoint entity (Removed)
[**update_entity**](LLMEndpointsApi.md#update_entity) | **PUT** /api/v1/entities/llmEndpoints/{id} | PUT LLM endpoint entity (Removed)


# **create_entity**
> create_entity()

Post LLM endpoint entities (Removed)

Permanently removed. Use /api/v1/entities/llmProviders instead. Always returns 410 Gone.

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

    # example, this endpoint has no required or optional parameters
    try:
        # Post LLM endpoint entities (Removed)
        api_instance.create_entity()
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMEndpointsApi->create_entity: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

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
**410** | Gone |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity**
> delete_entity(id)

Delete LLM endpoint entity (Removed)

Permanently removed. Use /api/v1/entities/llmProviders instead. Always returns 410 Gone.

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
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Delete LLM endpoint entity (Removed)
        api_instance.delete_entity(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMEndpointsApi->delete_entity: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |

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
**410** | Gone |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities**
> get_all_entities()

Get all LLM endpoint entities (Removed)

Permanently removed. Use /api/v1/entities/llmProviders instead. Always returns 410 Gone.

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

    # example, this endpoint has no required or optional parameters
    try:
        # Get all LLM endpoint entities (Removed)
        api_instance.get_all_entities()
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMEndpointsApi->get_all_entities: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

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
**410** | Gone |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity**
> get_entity(id)

Get LLM endpoint entity (Removed)

Permanently removed. Use /api/v1/entities/llmProviders instead. Always returns 410 Gone.

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
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get LLM endpoint entity (Removed)
        api_instance.get_entity(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMEndpointsApi->get_entity: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |

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
**410** | Gone |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity**
> patch_entity(id)

Patch LLM endpoint entity (Removed)

Permanently removed. Use /api/v1/entities/llmProviders instead. Always returns 410 Gone.

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
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Patch LLM endpoint entity (Removed)
        api_instance.patch_entity(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMEndpointsApi->patch_entity: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |

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
**410** | Gone |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity**
> update_entity(id)

PUT LLM endpoint entity (Removed)

Permanently removed. Use /api/v1/entities/llmProviders instead. Always returns 410 Gone.

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
    id = "id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # PUT LLM endpoint entity (Removed)
        api_instance.update_entity(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LLMEndpointsApi->update_entity: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |

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
**410** | Gone |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


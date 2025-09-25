# gooddata_api_client.APITokensApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_api_tokens**](APITokensApi.md#create_entity_api_tokens) | **POST** /api/v1/entities/users/{userId}/apiTokens | Post a new API token for the user
[**delete_entity_api_tokens**](APITokensApi.md#delete_entity_api_tokens) | **DELETE** /api/v1/entities/users/{userId}/apiTokens/{id} | Delete an API Token for a user
[**get_all_entities_api_tokens**](APITokensApi.md#get_all_entities_api_tokens) | **GET** /api/v1/entities/users/{userId}/apiTokens | List all api tokens for a user
[**get_entity_api_tokens**](APITokensApi.md#get_entity_api_tokens) | **GET** /api/v1/entities/users/{userId}/apiTokens/{id} | Get an API Token for a user


# **create_entity_api_tokens**
> JsonApiApiTokenOutDocument create_entity_api_tokens(user_id, json_api_api_token_in_document)

Post a new API token for the user

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_api_token_in_document import JsonApiApiTokenInDocument
from gooddata_api_client.models.json_api_api_token_out_document import JsonApiApiTokenOutDocument
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
    api_instance = gooddata_api_client.APITokensApi(api_client)
    user_id = 'user_id_example' # str | 
    json_api_api_token_in_document = gooddata_api_client.JsonApiApiTokenInDocument() # JsonApiApiTokenInDocument | 

    try:
        # Post a new API token for the user
        api_response = api_instance.create_entity_api_tokens(user_id, json_api_api_token_in_document)
        print("The response of APITokensApi->create_entity_api_tokens:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling APITokensApi->create_entity_api_tokens: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  | 
 **json_api_api_token_in_document** | [**JsonApiApiTokenInDocument**](JsonApiApiTokenInDocument.md)|  | 

### Return type

[**JsonApiApiTokenOutDocument**](JsonApiApiTokenOutDocument.md)

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

# **delete_entity_api_tokens**
> delete_entity_api_tokens(user_id, id, filter=filter)

Delete an API Token for a user

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
    api_instance = gooddata_api_client.APITokensApi(api_client)
    user_id = 'user_id_example' # str | 
    id = 'id_example' # str | 
    filter = 'bearerToken==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Delete an API Token for a user
        api_instance.delete_entity_api_tokens(user_id, id, filter=filter)
    except Exception as e:
        print("Exception when calling APITokensApi->delete_entity_api_tokens: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  | 
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

# **get_all_entities_api_tokens**
> JsonApiApiTokenOutList get_all_entities_api_tokens(user_id, filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)

List all api tokens for a user

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_api_token_out_list import JsonApiApiTokenOutList
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
    api_instance = gooddata_api_client.APITokensApi(api_client)
    user_id = 'user_id_example' # str | 
    filter = 'bearerToken==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # List all api tokens for a user
        api_response = api_instance.get_all_entities_api_tokens(user_id, filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of APITokensApi->get_all_entities_api_tokens:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling APITokensApi->get_all_entities_api_tokens: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **page** | **int**| Zero-based page index (0..N) | [optional] [default to 0]
 **size** | **int**| The size of the page to be returned | [optional] [default to 20]
 **sort** | [**List[str]**](str.md)| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiApiTokenOutList**](JsonApiApiTokenOutList.md)

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

# **get_entity_api_tokens**
> JsonApiApiTokenOutDocument get_entity_api_tokens(user_id, id, filter=filter)

Get an API Token for a user

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_api_token_out_document import JsonApiApiTokenOutDocument
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
    api_instance = gooddata_api_client.APITokensApi(api_client)
    user_id = 'user_id_example' # str | 
    id = 'id_example' # str | 
    filter = 'bearerToken==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Get an API Token for a user
        api_response = api_instance.get_entity_api_tokens(user_id, id, filter=filter)
        print("The response of APITokensApi->get_entity_api_tokens:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling APITokensApi->get_entity_api_tokens: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  | 
 **id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiApiTokenOutDocument**](JsonApiApiTokenOutDocument.md)

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


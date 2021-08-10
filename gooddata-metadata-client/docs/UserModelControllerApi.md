# gooddata_metadata_client.UserModelControllerApi

All URIs are relative to *https://staging.anywhere.gooddata.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_api_tokens**](UserModelControllerApi.md#create_entity_api_tokens) | **POST** /api/entities/users/{userId}/apiTokens | 
[**delete_entity_api_tokens**](UserModelControllerApi.md#delete_entity_api_tokens) | **DELETE** /api/entities/users/{userId}/apiTokens/{id} | 
[**get_all_entities_api_tokens**](UserModelControllerApi.md#get_all_entities_api_tokens) | **GET** /api/entities/users/{userId}/apiTokens | 
[**get_entity_api_tokens**](UserModelControllerApi.md#get_entity_api_tokens) | **GET** /api/entities/users/{userId}/apiTokens/{id} | 


# **create_entity_api_tokens**
> JsonApiApiTokenOutDocument create_entity_api_tokens(user_id, json_api_api_token_in_document)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import user_model_controller_api
from gooddata_metadata_client.model.json_api_api_token_in_document import JsonApiApiTokenInDocument
from gooddata_metadata_client.model.json_api_api_token_out_document import JsonApiApiTokenOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_model_controller_api.UserModelControllerApi(api_client)
    user_id = "userId_example" # str | 
    json_api_api_token_in_document = JsonApiApiTokenInDocument(
        data=JsonApiApiTokenIn(
            type="apiToken",
            id="id1",
        ),
    ) # JsonApiApiTokenInDocument | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_entity_api_tokens(user_id, json_api_api_token_in_document)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling UserModelControllerApi->create_entity_api_tokens: %s\n" % e)
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
> delete_entity_api_tokens(user_id, id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import user_model_controller_api
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_model_controller_api.UserModelControllerApi(api_client)
    user_id = "userId_example" # str | 
    id = "26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1RA89q3w1l4eH4XxEz.5awxoFZxHzs6ED.kjUSnTINkYPUndNl8pmPg5K897Fu1JEFj9R1_dz9rEoBi0LnU8SsOWJ7wYrcziVQdt8mVLxbg4bCLrLBcmXxWQK6MzKSg5jphei0IfRRwpnT_Z.qKa_YppZepezJ0.VmLSUTLYyW" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=bearerToken==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_entity_api_tokens(user_id, id)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling UserModelControllerApi->delete_entity_api_tokens: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_instance.delete_entity_api_tokens(user_id, id, predicate=predicate, filter=filter)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling UserModelControllerApi->delete_entity_api_tokens: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  |
 **id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]

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
> JsonApiApiTokenOutList get_all_entities_api_tokens(user_id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import user_model_controller_api
from gooddata_metadata_client.model.json_api_api_token_out_list import JsonApiApiTokenOutList
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_model_controller_api.UserModelControllerApi(api_client)
    user_id = "userId_example" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=bearerToken==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_all_entities_api_tokens(user_id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling UserModelControllerApi->get_all_entities_api_tokens: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_all_entities_api_tokens(user_id, predicate=predicate, filter=filter, page=page, size=size, sort=sort)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling UserModelControllerApi->get_all_entities_api_tokens: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]

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
> JsonApiApiTokenOutDocument get_entity_api_tokens(user_id, id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import user_model_controller_api
from gooddata_metadata_client.model.json_api_api_token_out_document import JsonApiApiTokenOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_model_controller_api.UserModelControllerApi(api_client)
    user_id = "userId_example" # str | 
    id = "26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1RA89q3w1l4eH4XxEz.5awxoFZxHzs6ED.kjUSnTINkYPUndNl8pmPg5K897Fu1JEFj9R1_dz9rEoBi0LnU8SsOWJ7wYrcziVQdt8mVLxbg4bCLrLBcmXxWQK6MzKSg5jphei0IfRRwpnT_Z.qKa_YppZepezJ0.VmLSUTLYyW" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=bearerToken==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_entity_api_tokens(user_id, id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling UserModelControllerApi->get_entity_api_tokens: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_entity_api_tokens(user_id, id, predicate=predicate, filter=filter)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling UserModelControllerApi->get_entity_api_tokens: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  |
 **id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]

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


# gooddata_api_client.UserIdentifiersApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_all_entities_user_identifiers**](UserIdentifiersApi.md#get_all_entities_user_identifiers) | **GET** /api/v1/entities/userIdentifiers | Get UserIdentifier entities
[**get_entity_user_identifiers**](UserIdentifiersApi.md#get_entity_user_identifiers) | **GET** /api/v1/entities/userIdentifiers/{id} | Get UserIdentifier entity


# **get_all_entities_user_identifiers**
> JsonApiUserIdentifierOutList get_all_entities_user_identifiers(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)

Get UserIdentifier entities

UserIdentifier - represents entity interacting with platform

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_user_identifier_out_list import JsonApiUserIdentifierOutList
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
    api_instance = gooddata_api_client.UserIdentifiersApi(api_client)
    filter = 'firstname==someString;lastname==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get UserIdentifier entities
        api_response = api_instance.get_all_entities_user_identifiers(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of UserIdentifiersApi->get_all_entities_user_identifiers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserIdentifiersApi->get_all_entities_user_identifiers: %s\n" % e)
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

[**JsonApiUserIdentifierOutList**](JsonApiUserIdentifierOutList.md)

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

# **get_entity_user_identifiers**
> JsonApiUserIdentifierOutDocument get_entity_user_identifiers(id, filter=filter)

Get UserIdentifier entity

UserIdentifier - represents basic information about entity interacting with platform

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_user_identifier_out_document import JsonApiUserIdentifierOutDocument
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
    api_instance = gooddata_api_client.UserIdentifiersApi(api_client)
    id = 'id_example' # str | 
    filter = 'firstname==someString;lastname==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Get UserIdentifier entity
        api_response = api_instance.get_entity_user_identifiers(id, filter=filter)
        print("The response of UserIdentifiersApi->get_entity_user_identifiers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserIdentifiersApi->get_entity_user_identifiers: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiUserIdentifierOutDocument**](JsonApiUserIdentifierOutDocument.md)

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


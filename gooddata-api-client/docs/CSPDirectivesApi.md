# gooddata_api_client.CSPDirectivesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_csp_directives**](CSPDirectivesApi.md#create_entity_csp_directives) | **POST** /api/v1/entities/cspDirectives | Post CSP Directives
[**delete_entity_csp_directives**](CSPDirectivesApi.md#delete_entity_csp_directives) | **DELETE** /api/v1/entities/cspDirectives/{id} | Delete CSP Directives
[**get_all_entities_csp_directives**](CSPDirectivesApi.md#get_all_entities_csp_directives) | **GET** /api/v1/entities/cspDirectives | Get CSP Directives
[**get_entity_csp_directives**](CSPDirectivesApi.md#get_entity_csp_directives) | **GET** /api/v1/entities/cspDirectives/{id} | Get CSP Directives
[**patch_entity_csp_directives**](CSPDirectivesApi.md#patch_entity_csp_directives) | **PATCH** /api/v1/entities/cspDirectives/{id} | Patch CSP Directives
[**update_entity_csp_directives**](CSPDirectivesApi.md#update_entity_csp_directives) | **PUT** /api/v1/entities/cspDirectives/{id} | Put CSP Directives


# **create_entity_csp_directives**
> JsonApiCspDirectiveOutDocument create_entity_csp_directives(json_api_csp_directive_in_document)

Post CSP Directives

 Context Security Police Directive

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_csp_directive_in_document import JsonApiCspDirectiveInDocument
from gooddata_api_client.models.json_api_csp_directive_out_document import JsonApiCspDirectiveOutDocument
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
    api_instance = gooddata_api_client.CSPDirectivesApi(api_client)
    json_api_csp_directive_in_document = gooddata_api_client.JsonApiCspDirectiveInDocument() # JsonApiCspDirectiveInDocument | 

    try:
        # Post CSP Directives
        api_response = api_instance.create_entity_csp_directives(json_api_csp_directive_in_document)
        print("The response of CSPDirectivesApi->create_entity_csp_directives:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CSPDirectivesApi->create_entity_csp_directives: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_csp_directive_in_document** | [**JsonApiCspDirectiveInDocument**](JsonApiCspDirectiveInDocument.md)|  | 

### Return type

[**JsonApiCspDirectiveOutDocument**](JsonApiCspDirectiveOutDocument.md)

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

# **delete_entity_csp_directives**
> delete_entity_csp_directives(id, filter=filter)

Delete CSP Directives

 Context Security Police Directive

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
    api_instance = gooddata_api_client.CSPDirectivesApi(api_client)
    id = 'id_example' # str | 
    filter = 'sources==v1,v2,v3' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Delete CSP Directives
        api_instance.delete_entity_csp_directives(id, filter=filter)
    except Exception as e:
        print("Exception when calling CSPDirectivesApi->delete_entity_csp_directives: %s\n" % e)
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

# **get_all_entities_csp_directives**
> JsonApiCspDirectiveOutList get_all_entities_csp_directives(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)

Get CSP Directives

 Context Security Police Directive

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_csp_directive_out_list import JsonApiCspDirectiveOutList
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
    api_instance = gooddata_api_client.CSPDirectivesApi(api_client)
    filter = 'sources==v1,v2,v3' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get CSP Directives
        api_response = api_instance.get_all_entities_csp_directives(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of CSPDirectivesApi->get_all_entities_csp_directives:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CSPDirectivesApi->get_all_entities_csp_directives: %s\n" % e)
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

[**JsonApiCspDirectiveOutList**](JsonApiCspDirectiveOutList.md)

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

# **get_entity_csp_directives**
> JsonApiCspDirectiveOutDocument get_entity_csp_directives(id, filter=filter)

Get CSP Directives

 Context Security Police Directive

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_csp_directive_out_document import JsonApiCspDirectiveOutDocument
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
    api_instance = gooddata_api_client.CSPDirectivesApi(api_client)
    id = 'id_example' # str | 
    filter = 'sources==v1,v2,v3' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Get CSP Directives
        api_response = api_instance.get_entity_csp_directives(id, filter=filter)
        print("The response of CSPDirectivesApi->get_entity_csp_directives:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CSPDirectivesApi->get_entity_csp_directives: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiCspDirectiveOutDocument**](JsonApiCspDirectiveOutDocument.md)

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

# **patch_entity_csp_directives**
> JsonApiCspDirectiveOutDocument patch_entity_csp_directives(id, json_api_csp_directive_patch_document, filter=filter)

Patch CSP Directives

 Context Security Police Directive

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_csp_directive_out_document import JsonApiCspDirectiveOutDocument
from gooddata_api_client.models.json_api_csp_directive_patch_document import JsonApiCspDirectivePatchDocument
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
    api_instance = gooddata_api_client.CSPDirectivesApi(api_client)
    id = 'id_example' # str | 
    json_api_csp_directive_patch_document = gooddata_api_client.JsonApiCspDirectivePatchDocument() # JsonApiCspDirectivePatchDocument | 
    filter = 'sources==v1,v2,v3' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Patch CSP Directives
        api_response = api_instance.patch_entity_csp_directives(id, json_api_csp_directive_patch_document, filter=filter)
        print("The response of CSPDirectivesApi->patch_entity_csp_directives:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CSPDirectivesApi->patch_entity_csp_directives: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_csp_directive_patch_document** | [**JsonApiCspDirectivePatchDocument**](JsonApiCspDirectivePatchDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiCspDirectiveOutDocument**](JsonApiCspDirectiveOutDocument.md)

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

# **update_entity_csp_directives**
> JsonApiCspDirectiveOutDocument update_entity_csp_directives(id, json_api_csp_directive_in_document, filter=filter)

Put CSP Directives

 Context Security Police Directive

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_csp_directive_in_document import JsonApiCspDirectiveInDocument
from gooddata_api_client.models.json_api_csp_directive_out_document import JsonApiCspDirectiveOutDocument
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
    api_instance = gooddata_api_client.CSPDirectivesApi(api_client)
    id = 'id_example' # str | 
    json_api_csp_directive_in_document = gooddata_api_client.JsonApiCspDirectiveInDocument() # JsonApiCspDirectiveInDocument | 
    filter = 'sources==v1,v2,v3' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Put CSP Directives
        api_response = api_instance.update_entity_csp_directives(id, json_api_csp_directive_in_document, filter=filter)
        print("The response of CSPDirectivesApi->update_entity_csp_directives:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CSPDirectivesApi->update_entity_csp_directives: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_csp_directive_in_document** | [**JsonApiCspDirectiveInDocument**](JsonApiCspDirectiveInDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiCspDirectiveOutDocument**](JsonApiCspDirectiveOutDocument.md)

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


# gooddata_api_client.DataSourceEntityAPIsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_data_sources**](DataSourceEntityAPIsApi.md#create_entity_data_sources) | **POST** /api/v1/entities/dataSources | Post Data Sources
[**delete_entity_data_sources**](DataSourceEntityAPIsApi.md#delete_entity_data_sources) | **DELETE** /api/v1/entities/dataSources/{id} | Delete Data Source entity
[**get_all_entities_data_source_identifiers**](DataSourceEntityAPIsApi.md#get_all_entities_data_source_identifiers) | **GET** /api/v1/entities/dataSourceIdentifiers | Get all Data Source Identifiers
[**get_all_entities_data_sources**](DataSourceEntityAPIsApi.md#get_all_entities_data_sources) | **GET** /api/v1/entities/dataSources | Get Data Source entities
[**get_entity_data_source_identifiers**](DataSourceEntityAPIsApi.md#get_entity_data_source_identifiers) | **GET** /api/v1/entities/dataSourceIdentifiers/{id} | Get Data Source Identifier
[**get_entity_data_sources**](DataSourceEntityAPIsApi.md#get_entity_data_sources) | **GET** /api/v1/entities/dataSources/{id} | Get Data Source entity
[**patch_entity_data_sources**](DataSourceEntityAPIsApi.md#patch_entity_data_sources) | **PATCH** /api/v1/entities/dataSources/{id} | Patch Data Source entity
[**update_entity_data_sources**](DataSourceEntityAPIsApi.md#update_entity_data_sources) | **PUT** /api/v1/entities/dataSources/{id} | Put Data Source entity


# **create_entity_data_sources**
> JsonApiDataSourceOutDocument create_entity_data_sources(json_api_data_source_in_document, meta_include=meta_include)

Post Data Sources

Data Source - represents data source for the workspace

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_data_source_in_document import JsonApiDataSourceInDocument
from gooddata_api_client.models.json_api_data_source_out_document import JsonApiDataSourceOutDocument
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
    api_instance = gooddata_api_client.DataSourceEntityAPIsApi(api_client)
    json_api_data_source_in_document = gooddata_api_client.JsonApiDataSourceInDocument() # JsonApiDataSourceInDocument | 
    meta_include = ['metaInclude=permissions,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Post Data Sources
        api_response = api_instance.create_entity_data_sources(json_api_data_source_in_document, meta_include=meta_include)
        print("The response of DataSourceEntityAPIsApi->create_entity_data_sources:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataSourceEntityAPIsApi->create_entity_data_sources: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_data_source_in_document** | [**JsonApiDataSourceInDocument**](JsonApiDataSourceInDocument.md)|  | 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiDataSourceOutDocument**](JsonApiDataSourceOutDocument.md)

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

# **delete_entity_data_sources**
> delete_entity_data_sources(id, filter=filter)

Delete Data Source entity

Data Source - represents data source for the workspace

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
    api_instance = gooddata_api_client.DataSourceEntityAPIsApi(api_client)
    id = 'id_example' # str | 
    filter = 'name==someString;type==DatabaseTypeValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Delete Data Source entity
        api_instance.delete_entity_data_sources(id, filter=filter)
    except Exception as e:
        print("Exception when calling DataSourceEntityAPIsApi->delete_entity_data_sources: %s\n" % e)
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

# **get_all_entities_data_source_identifiers**
> JsonApiDataSourceIdentifierOutList get_all_entities_data_source_identifiers(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)

Get all Data Source Identifiers

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_data_source_identifier_out_list import JsonApiDataSourceIdentifierOutList
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
    api_instance = gooddata_api_client.DataSourceEntityAPIsApi(api_client)
    filter = 'name==someString;schema==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=permissions,page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get all Data Source Identifiers
        api_response = api_instance.get_all_entities_data_source_identifiers(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of DataSourceEntityAPIsApi->get_all_entities_data_source_identifiers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataSourceEntityAPIsApi->get_all_entities_data_source_identifiers: %s\n" % e)
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

[**JsonApiDataSourceIdentifierOutList**](JsonApiDataSourceIdentifierOutList.md)

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

# **get_all_entities_data_sources**
> JsonApiDataSourceOutList get_all_entities_data_sources(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)

Get Data Source entities

Data Source - represents data source for the workspace

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_data_source_out_list import JsonApiDataSourceOutList
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
    api_instance = gooddata_api_client.DataSourceEntityAPIsApi(api_client)
    filter = 'name==someString;type==DatabaseTypeValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=permissions,page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get Data Source entities
        api_response = api_instance.get_all_entities_data_sources(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of DataSourceEntityAPIsApi->get_all_entities_data_sources:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataSourceEntityAPIsApi->get_all_entities_data_sources: %s\n" % e)
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

[**JsonApiDataSourceOutList**](JsonApiDataSourceOutList.md)

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

# **get_entity_data_source_identifiers**
> JsonApiDataSourceIdentifierOutDocument get_entity_data_source_identifiers(id, filter=filter, meta_include=meta_include)

Get Data Source Identifier

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_data_source_identifier_out_document import JsonApiDataSourceIdentifierOutDocument
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
    api_instance = gooddata_api_client.DataSourceEntityAPIsApi(api_client)
    id = 'id_example' # str | 
    filter = 'name==someString;schema==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    meta_include = ['metaInclude=permissions,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get Data Source Identifier
        api_response = api_instance.get_entity_data_source_identifiers(id, filter=filter, meta_include=meta_include)
        print("The response of DataSourceEntityAPIsApi->get_entity_data_source_identifiers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataSourceEntityAPIsApi->get_entity_data_source_identifiers: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiDataSourceIdentifierOutDocument**](JsonApiDataSourceIdentifierOutDocument.md)

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

# **get_entity_data_sources**
> JsonApiDataSourceOutDocument get_entity_data_sources(id, filter=filter, meta_include=meta_include)

Get Data Source entity

Data Source - represents data source for the workspace

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_data_source_out_document import JsonApiDataSourceOutDocument
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
    api_instance = gooddata_api_client.DataSourceEntityAPIsApi(api_client)
    id = 'id_example' # str | 
    filter = 'name==someString;type==DatabaseTypeValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    meta_include = ['metaInclude=permissions,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get Data Source entity
        api_response = api_instance.get_entity_data_sources(id, filter=filter, meta_include=meta_include)
        print("The response of DataSourceEntityAPIsApi->get_entity_data_sources:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataSourceEntityAPIsApi->get_entity_data_sources: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiDataSourceOutDocument**](JsonApiDataSourceOutDocument.md)

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

# **patch_entity_data_sources**
> JsonApiDataSourceOutDocument patch_entity_data_sources(id, json_api_data_source_patch_document, filter=filter)

Patch Data Source entity

Data Source - represents data source for the workspace

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_data_source_out_document import JsonApiDataSourceOutDocument
from gooddata_api_client.models.json_api_data_source_patch_document import JsonApiDataSourcePatchDocument
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
    api_instance = gooddata_api_client.DataSourceEntityAPIsApi(api_client)
    id = 'id_example' # str | 
    json_api_data_source_patch_document = gooddata_api_client.JsonApiDataSourcePatchDocument() # JsonApiDataSourcePatchDocument | 
    filter = 'name==someString;type==DatabaseTypeValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Patch Data Source entity
        api_response = api_instance.patch_entity_data_sources(id, json_api_data_source_patch_document, filter=filter)
        print("The response of DataSourceEntityAPIsApi->patch_entity_data_sources:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataSourceEntityAPIsApi->patch_entity_data_sources: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_data_source_patch_document** | [**JsonApiDataSourcePatchDocument**](JsonApiDataSourcePatchDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiDataSourceOutDocument**](JsonApiDataSourceOutDocument.md)

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

# **update_entity_data_sources**
> JsonApiDataSourceOutDocument update_entity_data_sources(id, json_api_data_source_in_document, filter=filter)

Put Data Source entity

Data Source - represents data source for the workspace

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_data_source_in_document import JsonApiDataSourceInDocument
from gooddata_api_client.models.json_api_data_source_out_document import JsonApiDataSourceOutDocument
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
    api_instance = gooddata_api_client.DataSourceEntityAPIsApi(api_client)
    id = 'id_example' # str | 
    json_api_data_source_in_document = gooddata_api_client.JsonApiDataSourceInDocument() # JsonApiDataSourceInDocument | 
    filter = 'name==someString;type==DatabaseTypeValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Put Data Source entity
        api_response = api_instance.update_entity_data_sources(id, json_api_data_source_in_document, filter=filter)
        print("The response of DataSourceEntityAPIsApi->update_entity_data_sources:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataSourceEntityAPIsApi->update_entity_data_sources: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_data_source_in_document** | [**JsonApiDataSourceInDocument**](JsonApiDataSourceInDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiDataSourceOutDocument**](JsonApiDataSourceOutDocument.md)

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


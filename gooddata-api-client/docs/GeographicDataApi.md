# gooddata_api_client.GeographicDataApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_custom_geo_collections**](GeographicDataApi.md#create_entity_custom_geo_collections) | **POST** /api/v1/entities/customGeoCollections | 
[**delete_entity_custom_geo_collections**](GeographicDataApi.md#delete_entity_custom_geo_collections) | **DELETE** /api/v1/entities/customGeoCollections/{id} | 
[**get_all_entities_custom_geo_collections**](GeographicDataApi.md#get_all_entities_custom_geo_collections) | **GET** /api/v1/entities/customGeoCollections | 
[**get_entity_custom_geo_collections**](GeographicDataApi.md#get_entity_custom_geo_collections) | **GET** /api/v1/entities/customGeoCollections/{id} | 
[**patch_entity_custom_geo_collections**](GeographicDataApi.md#patch_entity_custom_geo_collections) | **PATCH** /api/v1/entities/customGeoCollections/{id} | 
[**update_entity_custom_geo_collections**](GeographicDataApi.md#update_entity_custom_geo_collections) | **PUT** /api/v1/entities/customGeoCollections/{id} | 


# **create_entity_custom_geo_collections**
> JsonApiCustomGeoCollectionOutDocument create_entity_custom_geo_collections(json_api_custom_geo_collection_in_document)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import geographic_data_api
from gooddata_api_client.model.json_api_custom_geo_collection_out_document import JsonApiCustomGeoCollectionOutDocument
from gooddata_api_client.model.json_api_custom_geo_collection_in_document import JsonApiCustomGeoCollectionInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = geographic_data_api.GeographicDataApi(api_client)
    json_api_custom_geo_collection_in_document = JsonApiCustomGeoCollectionInDocument(
        data=JsonApiCustomGeoCollectionIn(
            id="id1",
            type="customGeoCollection",
        ),
    ) # JsonApiCustomGeoCollectionInDocument | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_entity_custom_geo_collections(json_api_custom_geo_collection_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling GeographicDataApi->create_entity_custom_geo_collections: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_custom_geo_collection_in_document** | [**JsonApiCustomGeoCollectionInDocument**](JsonApiCustomGeoCollectionInDocument.md)|  |

### Return type

[**JsonApiCustomGeoCollectionOutDocument**](JsonApiCustomGeoCollectionOutDocument.md)

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

# **delete_entity_custom_geo_collections**
> delete_entity_custom_geo_collections(id)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import geographic_data_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = geographic_data_api.GeographicDataApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_entity_custom_geo_collections(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling GeographicDataApi->delete_entity_custom_geo_collections: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_instance.delete_entity_custom_geo_collections(id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling GeographicDataApi->delete_entity_custom_geo_collections: %s\n" % e)
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

# **get_all_entities_custom_geo_collections**
> JsonApiCustomGeoCollectionOutList get_all_entities_custom_geo_collections()



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import geographic_data_api
from gooddata_api_client.model.json_api_custom_geo_collection_out_list import JsonApiCustomGeoCollectionOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = geographic_data_api.GeographicDataApi(api_client)
    filter = "" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
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
        api_response = api_instance.get_all_entities_custom_geo_collections(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling GeographicDataApi->get_all_entities_custom_geo_collections: %s\n" % e)
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

[**JsonApiCustomGeoCollectionOutList**](JsonApiCustomGeoCollectionOutList.md)

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

# **get_entity_custom_geo_collections**
> JsonApiCustomGeoCollectionOutDocument get_entity_custom_geo_collections(id)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import geographic_data_api
from gooddata_api_client.model.json_api_custom_geo_collection_out_document import JsonApiCustomGeoCollectionOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = geographic_data_api.GeographicDataApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_entity_custom_geo_collections(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling GeographicDataApi->get_entity_custom_geo_collections: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_entity_custom_geo_collections(id, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling GeographicDataApi->get_entity_custom_geo_collections: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiCustomGeoCollectionOutDocument**](JsonApiCustomGeoCollectionOutDocument.md)

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

# **patch_entity_custom_geo_collections**
> JsonApiCustomGeoCollectionOutDocument patch_entity_custom_geo_collections(id, json_api_custom_geo_collection_patch_document)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import geographic_data_api
from gooddata_api_client.model.json_api_custom_geo_collection_patch_document import JsonApiCustomGeoCollectionPatchDocument
from gooddata_api_client.model.json_api_custom_geo_collection_out_document import JsonApiCustomGeoCollectionOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = geographic_data_api.GeographicDataApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_custom_geo_collection_patch_document = JsonApiCustomGeoCollectionPatchDocument(
        data=JsonApiCustomGeoCollectionPatch(
            id="id1",
            type="customGeoCollection",
        ),
    ) # JsonApiCustomGeoCollectionPatchDocument | 
    filter = "" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.patch_entity_custom_geo_collections(id, json_api_custom_geo_collection_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling GeographicDataApi->patch_entity_custom_geo_collections: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.patch_entity_custom_geo_collections(id, json_api_custom_geo_collection_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling GeographicDataApi->patch_entity_custom_geo_collections: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_custom_geo_collection_patch_document** | [**JsonApiCustomGeoCollectionPatchDocument**](JsonApiCustomGeoCollectionPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiCustomGeoCollectionOutDocument**](JsonApiCustomGeoCollectionOutDocument.md)

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

# **update_entity_custom_geo_collections**
> JsonApiCustomGeoCollectionOutDocument update_entity_custom_geo_collections(id, json_api_custom_geo_collection_in_document)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import geographic_data_api
from gooddata_api_client.model.json_api_custom_geo_collection_out_document import JsonApiCustomGeoCollectionOutDocument
from gooddata_api_client.model.json_api_custom_geo_collection_in_document import JsonApiCustomGeoCollectionInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = geographic_data_api.GeographicDataApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_custom_geo_collection_in_document = JsonApiCustomGeoCollectionInDocument(
        data=JsonApiCustomGeoCollectionIn(
            id="id1",
            type="customGeoCollection",
        ),
    ) # JsonApiCustomGeoCollectionInDocument | 
    filter = "" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_entity_custom_geo_collections(id, json_api_custom_geo_collection_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling GeographicDataApi->update_entity_custom_geo_collections: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.update_entity_custom_geo_collections(id, json_api_custom_geo_collection_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling GeographicDataApi->update_entity_custom_geo_collections: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_custom_geo_collection_in_document** | [**JsonApiCustomGeoCollectionInDocument**](JsonApiCustomGeoCollectionInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiCustomGeoCollectionOutDocument**](JsonApiCustomGeoCollectionOutDocument.md)

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


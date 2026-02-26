<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.geographic_data_api.GeographicDataApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_custom_geo_collections**](#create_entity_custom_geo_collections) | **post** /api/v1/entities/customGeoCollections | 
[**delete_entity_custom_geo_collections**](#delete_entity_custom_geo_collections) | **delete** /api/v1/entities/customGeoCollections/{id} | 
[**get_all_entities_custom_geo_collections**](#get_all_entities_custom_geo_collections) | **get** /api/v1/entities/customGeoCollections | 
[**get_entity_custom_geo_collections**](#get_entity_custom_geo_collections) | **get** /api/v1/entities/customGeoCollections/{id} | 
[**patch_entity_custom_geo_collections**](#patch_entity_custom_geo_collections) | **patch** /api/v1/entities/customGeoCollections/{id} | 
[**update_entity_custom_geo_collections**](#update_entity_custom_geo_collections) | **put** /api/v1/entities/customGeoCollections/{id} | 

# **create_entity_custom_geo_collections**
<a id="create_entity_custom_geo_collections"></a>
> JsonApiCustomGeoCollectionOutDocument create_entity_custom_geo_collections(json_api_custom_geo_collection_in_document)



### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import geographic_data_api
from gooddata_api_client.model.json_api_custom_geo_collection_out_document import JsonApiCustomGeoCollectionOutDocument
from gooddata_api_client.model.json_api_custom_geo_collection_in_document import JsonApiCustomGeoCollectionInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = geographic_data_api.GeographicDataApi(api_client)

    # example passing only required values which don't have defaults set
    body = JsonApiCustomGeoCollectionInDocument(
        data=JsonApiCustomGeoCollectionIn(
            attributes=dict(
                description="description_example",
                name="name_example",
            ),
            id="id1",
            type="customGeoCollection",
        ),
    )
    try:
        api_response = api_instance.create_entity_custom_geo_collections(
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling GeographicDataApi->create_entity_custom_geo_collections: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, SchemaForRequestBodyApplicationVndGooddataApijson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiCustomGeoCollectionInDocument**](../../models/JsonApiCustomGeoCollectionInDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiCustomGeoCollectionInDocument**](../../models/JsonApiCustomGeoCollectionInDocument.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#create_entity_custom_geo_collections.ApiResponseFor201) | Request successfully processed

#### create_entity_custom_geo_collections.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationJson, SchemaFor201ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiCustomGeoCollectionOutDocument**](../../models/JsonApiCustomGeoCollectionOutDocument.md) |  | 


# SchemaFor201ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiCustomGeoCollectionOutDocument**](../../models/JsonApiCustomGeoCollectionOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_entity_custom_geo_collections**
<a id="delete_entity_custom_geo_collections"></a>
> delete_entity_custom_geo_collections(id)



### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import geographic_data_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = geographic_data_api.GeographicDataApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        api_response = api_instance.delete_entity_custom_geo_collections(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling GeographicDataApi->delete_entity_custom_geo_collections: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "name==someString;description==someString",
    }
    try:
        api_response = api_instance.delete_entity_custom_geo_collections(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling GeographicDataApi->delete_entity_custom_geo_collections: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#delete_entity_custom_geo_collections.ApiResponseFor204) | Successfully deleted

#### delete_entity_custom_geo_collections.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_custom_geo_collections**
<a id="get_all_entities_custom_geo_collections"></a>
> JsonApiCustomGeoCollectionOutList get_all_entities_custom_geo_collections()



### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import geographic_data_api
from gooddata_api_client.model.json_api_custom_geo_collection_out_list import JsonApiCustomGeoCollectionOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = geographic_data_api.GeographicDataApi(api_client)

    # example passing only optional values
    query_params = {
        'filter': "name==someString;description==someString",
        'page': 0,
        'size': 20,
        'sort': [
        "sort_example"
    ],
        'metaInclude': [
        "metaInclude=page,all"
    ],
    }
    try:
        api_response = api_instance.get_all_entities_custom_geo_collections(
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling GeographicDataApi->get_all_entities_custom_geo_collections: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
page | PageSchema | | optional
size | SizeSchema | | optional
sort | SortSchema | | optional
metaInclude | MetaIncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# PageSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 0

# SizeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 20

# SortSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

# MetaIncludeSchema

Included meta objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Included meta objects | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["page", "all", "ALL", ] 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_all_entities_custom_geo_collections.ApiResponseFor200) | Request successfully processed

#### get_all_entities_custom_geo_collections.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiCustomGeoCollectionOutList**](../../models/JsonApiCustomGeoCollectionOutList.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiCustomGeoCollectionOutList**](../../models/JsonApiCustomGeoCollectionOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_custom_geo_collections**
<a id="get_entity_custom_geo_collections"></a>
> JsonApiCustomGeoCollectionOutDocument get_entity_custom_geo_collections(id)



### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import geographic_data_api
from gooddata_api_client.model.json_api_custom_geo_collection_out_document import JsonApiCustomGeoCollectionOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = geographic_data_api.GeographicDataApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        api_response = api_instance.get_entity_custom_geo_collections(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling GeographicDataApi->get_entity_custom_geo_collections: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "name==someString;description==someString",
    }
    try:
        api_response = api_instance.get_entity_custom_geo_collections(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling GeographicDataApi->get_entity_custom_geo_collections: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_entity_custom_geo_collections.ApiResponseFor200) | Request successfully processed

#### get_entity_custom_geo_collections.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiCustomGeoCollectionOutDocument**](../../models/JsonApiCustomGeoCollectionOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiCustomGeoCollectionOutDocument**](../../models/JsonApiCustomGeoCollectionOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **patch_entity_custom_geo_collections**
<a id="patch_entity_custom_geo_collections"></a>
> JsonApiCustomGeoCollectionOutDocument patch_entity_custom_geo_collections(idjson_api_custom_geo_collection_patch_document)



### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import geographic_data_api
from gooddata_api_client.model.json_api_custom_geo_collection_patch_document import JsonApiCustomGeoCollectionPatchDocument
from gooddata_api_client.model.json_api_custom_geo_collection_out_document import JsonApiCustomGeoCollectionOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = geographic_data_api.GeographicDataApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiCustomGeoCollectionPatchDocument(
        data=JsonApiCustomGeoCollectionPatch(
            attributes=dict(
                description="description_example",
                name="name_example",
            ),
            id="id1",
            type="customGeoCollection",
        ),
    )
    try:
        api_response = api_instance.patch_entity_custom_geo_collections(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling GeographicDataApi->patch_entity_custom_geo_collections: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "name==someString;description==someString",
    }
    body = JsonApiCustomGeoCollectionPatchDocument(
        data=JsonApiCustomGeoCollectionPatch(
            attributes=dict(
                description="description_example",
                name="name_example",
            ),
            id="id1",
            type="customGeoCollection",
        ),
    )
    try:
        api_response = api_instance.patch_entity_custom_geo_collections(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling GeographicDataApi->patch_entity_custom_geo_collections: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiCustomGeoCollectionPatchDocument**](../../models/JsonApiCustomGeoCollectionPatchDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiCustomGeoCollectionPatchDocument**](../../models/JsonApiCustomGeoCollectionPatchDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#patch_entity_custom_geo_collections.ApiResponseFor200) | Request successfully processed

#### patch_entity_custom_geo_collections.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiCustomGeoCollectionOutDocument**](../../models/JsonApiCustomGeoCollectionOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiCustomGeoCollectionOutDocument**](../../models/JsonApiCustomGeoCollectionOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_entity_custom_geo_collections**
<a id="update_entity_custom_geo_collections"></a>
> JsonApiCustomGeoCollectionOutDocument update_entity_custom_geo_collections(idjson_api_custom_geo_collection_in_document)



### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import geographic_data_api
from gooddata_api_client.model.json_api_custom_geo_collection_out_document import JsonApiCustomGeoCollectionOutDocument
from gooddata_api_client.model.json_api_custom_geo_collection_in_document import JsonApiCustomGeoCollectionInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = geographic_data_api.GeographicDataApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiCustomGeoCollectionInDocument(
        data=JsonApiCustomGeoCollectionIn(
            attributes=dict(
                description="description_example",
                name="name_example",
            ),
            id="id1",
            type="customGeoCollection",
        ),
    )
    try:
        api_response = api_instance.update_entity_custom_geo_collections(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling GeographicDataApi->update_entity_custom_geo_collections: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "name==someString;description==someString",
    }
    body = JsonApiCustomGeoCollectionInDocument(
        data=JsonApiCustomGeoCollectionIn(
            attributes=dict(
                description="description_example",
                name="name_example",
            ),
            id="id1",
            type="customGeoCollection",
        ),
    )
    try:
        api_response = api_instance.update_entity_custom_geo_collections(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling GeographicDataApi->update_entity_custom_geo_collections: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiCustomGeoCollectionInDocument**](../../models/JsonApiCustomGeoCollectionInDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiCustomGeoCollectionInDocument**](../../models/JsonApiCustomGeoCollectionInDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_entity_custom_geo_collections.ApiResponseFor200) | Request successfully processed

#### update_entity_custom_geo_collections.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiCustomGeoCollectionOutDocument**](../../models/JsonApiCustomGeoCollectionOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiCustomGeoCollectionOutDocument**](../../models/JsonApiCustomGeoCollectionOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


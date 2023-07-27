<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.data_source_entity_apis_api.DataSourceEntityAPIsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_data_sources**](#create_entity_data_sources) | **post** /api/v1/entities/dataSources | Post Data Sources
[**delete_entity_data_sources**](#delete_entity_data_sources) | **delete** /api/v1/entities/dataSources/{id} | Delete Data Source entity
[**get_all_entities_data_source_identifiers**](#get_all_entities_data_source_identifiers) | **get** /api/v1/entities/dataSourceIdentifiers | Get all Data Source Identifiers
[**get_all_entities_data_source_tables**](#get_all_entities_data_source_tables) | **get** /api/v1/entities/dataSources/{dataSourceId}/dataSourceTables | 
[**get_all_entities_data_sources**](#get_all_entities_data_sources) | **get** /api/v1/entities/dataSources | Get Data Source entities
[**get_entity_data_source_identifiers**](#get_entity_data_source_identifiers) | **get** /api/v1/entities/dataSourceIdentifiers/{id} | Get Data Source Identifier
[**get_entity_data_source_tables**](#get_entity_data_source_tables) | **get** /api/v1/entities/dataSources/{dataSourceId}/dataSourceTables/{id} | 
[**get_entity_data_sources**](#get_entity_data_sources) | **get** /api/v1/entities/dataSources/{id} | Get Data Source entity
[**patch_entity_data_sources**](#patch_entity_data_sources) | **patch** /api/v1/entities/dataSources/{id} | Patch Data Source entity
[**update_entity_data_sources**](#update_entity_data_sources) | **put** /api/v1/entities/dataSources/{id} | Put Data Source entity

# **create_entity_data_sources**
<a id="create_entity_data_sources"></a>
> JsonApiDataSourceOutDocument create_entity_data_sources(json_api_data_source_in_document)

Post Data Sources

Data Source - represents data source for the workspace

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import data_source_entity_apis_api
from gooddata_api_client.model.json_api_data_source_in_document import JsonApiDataSourceInDocument
from gooddata_api_client.model.json_api_data_source_out_document import JsonApiDataSourceOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = data_source_entity_apis_api.DataSourceEntityAPIsApi(api_client)

    # example passing only required values which don't have defaults set
    query_params = {
    }
    body = JsonApiDataSourceInDocument(
        data=JsonApiDataSourceIn(
            attributes=dict(
                cache_path=[
                    "cache_path_example"
                ],
                enable_caching=False,
                name="name_example",
                parameters=[
                    dict(
                        name="name_example",
                        value="value_example",
                    )
                ],
                password="password_example",
                schema="schema_example",
                token="token_example",
                type="POSTGRESQL",
                url="url_example",
                username="username_example",
            ),
            id="id1",
            type="dataSource",
        ),
    )
    try:
        # Post Data Sources
        api_response = api_instance.create_entity_data_sources(
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceEntityAPIsApi->create_entity_data_sources: %s\n" % e)

    # example passing only optional values
    query_params = {
        'metaInclude': [
        "metaInclude=permissions,all"
    ],
    }
    body = JsonApiDataSourceInDocument(
        data=JsonApiDataSourceIn(
            attributes=dict(
                cache_path=[
                    "cache_path_example"
                ],
                enable_caching=False,
                name="name_example",
                parameters=[
                    dict(
                        name="name_example",
                        value="value_example",
                    )
                ],
                password="password_example",
                schema="schema_example",
                token="token_example",
                type="POSTGRESQL",
                url="url_example",
                username="username_example",
            ),
            id="id1",
            type="dataSource",
        ),
    )
    try:
        # Post Data Sources
        api_response = api_instance.create_entity_data_sources(
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceEntityAPIsApi->create_entity_data_sources: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDataSourceInDocument**](../../models/JsonApiDataSourceInDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
metaInclude | MetaIncludeSchema | | optional


# MetaIncludeSchema

Included meta objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Included meta objects | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["permissions", "all", "ALL", ] 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#create_entity_data_sources.ApiResponseFor201) | Request successfully processed

#### create_entity_data_sources.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDataSourceOutDocument**](../../models/JsonApiDataSourceOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_entity_data_sources**
<a id="delete_entity_data_sources"></a>
> delete_entity_data_sources(id)

Delete Data Source entity

Data Source - represents data source for the workspace

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import data_source_entity_apis_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = data_source_entity_apis_api.DataSourceEntityAPIsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Delete Data Source entity
        api_response = api_instance.delete_entity_data_sources(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceEntityAPIsApi->delete_entity_data_sources: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=name==someString;type==DatabaseTypeValue",
    }
    try:
        # Delete Data Source entity
        api_response = api_instance.delete_entity_data_sources(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceEntityAPIsApi->delete_entity_data_sources: %s\n" % e)
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
204 | [ApiResponseFor204](#delete_entity_data_sources.ApiResponseFor204) | Successfully deleted

#### delete_entity_data_sources.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_data_source_identifiers**
<a id="get_all_entities_data_source_identifiers"></a>
> JsonApiDataSourceIdentifierOutList get_all_entities_data_source_identifiers()

Get all Data Source Identifiers

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import data_source_entity_apis_api
from gooddata_api_client.model.json_api_data_source_identifier_out_list import JsonApiDataSourceIdentifierOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = data_source_entity_apis_api.DataSourceEntityAPIsApi(api_client)

    # example passing only optional values
    query_params = {
        'filter': "filter=name==someString;schema==someString",
        'page': 0,
        'size': 20,
        'sort': [
        "sort_example"
    ],
        'metaInclude': [
        "metaInclude=permissions,all"
    ],
    }
    try:
        # Get all Data Source Identifiers
        api_response = api_instance.get_all_entities_data_source_identifiers(
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceEntityAPIsApi->get_all_entities_data_source_identifiers: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
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
items | str,  | str,  |  | must be one of ["permissions", "all", "ALL", ] 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_all_entities_data_source_identifiers.ApiResponseFor200) | Request successfully processed

#### get_all_entities_data_source_identifiers.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDataSourceIdentifierOutList**](../../models/JsonApiDataSourceIdentifierOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_data_source_tables**
<a id="get_all_entities_data_source_tables"></a>
> JsonApiDataSourceTableOutList get_all_entities_data_source_tables(data_source_id)



### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import data_source_entity_apis_api
from gooddata_api_client.model.json_api_data_source_table_out_list import JsonApiDataSourceTableOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = data_source_entity_apis_api.DataSourceEntityAPIsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'dataSourceId': "dataSourceId_example",
    }
    query_params = {
    }
    try:
        api_response = api_instance.get_all_entities_data_source_tables(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceEntityAPIsApi->get_all_entities_data_source_tables: %s\n" % e)

    # example passing only optional values
    path_params = {
        'dataSourceId': "dataSourceId_example",
    }
    query_params = {
        'filter': "filter=path==v1,v2,v3;type==DataSourceTableTypeValue",
        'page': 0,
        'size': 20,
        'sort': [
        "sort_example"
    ],
    }
    try:
        api_response = api_instance.get_all_entities_data_source_tables(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceEntityAPIsApi->get_all_entities_data_source_tables: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
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

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
dataSourceId | DataSourceIdSchema | | 

# DataSourceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_all_entities_data_source_tables.ApiResponseFor200) | Request successfully processed

#### get_all_entities_data_source_tables.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDataSourceTableOutList**](../../models/JsonApiDataSourceTableOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_data_sources**
<a id="get_all_entities_data_sources"></a>
> JsonApiDataSourceOutList get_all_entities_data_sources()

Get Data Source entities

Data Source - represents data source for the workspace

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import data_source_entity_apis_api
from gooddata_api_client.model.json_api_data_source_out_list import JsonApiDataSourceOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = data_source_entity_apis_api.DataSourceEntityAPIsApi(api_client)

    # example passing only optional values
    query_params = {
        'filter': "filter=name==someString;type==DatabaseTypeValue",
        'page': 0,
        'size': 20,
        'sort': [
        "sort_example"
    ],
        'metaInclude': [
        "metaInclude=permissions,all"
    ],
    }
    try:
        # Get Data Source entities
        api_response = api_instance.get_all_entities_data_sources(
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceEntityAPIsApi->get_all_entities_data_sources: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
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
items | str,  | str,  |  | must be one of ["permissions", "all", "ALL", ] 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_all_entities_data_sources.ApiResponseFor200) | Request successfully processed

#### get_all_entities_data_sources.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDataSourceOutList**](../../models/JsonApiDataSourceOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_data_source_identifiers**
<a id="get_entity_data_source_identifiers"></a>
> JsonApiDataSourceIdentifierOutDocument get_entity_data_source_identifiers(id)

Get Data Source Identifier

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import data_source_entity_apis_api
from gooddata_api_client.model.json_api_data_source_identifier_out_document import JsonApiDataSourceIdentifierOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = data_source_entity_apis_api.DataSourceEntityAPIsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Get Data Source Identifier
        api_response = api_instance.get_entity_data_source_identifiers(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceEntityAPIsApi->get_entity_data_source_identifiers: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=name==someString;schema==someString",
        'metaInclude': [
        "metaInclude=permissions,all"
    ],
    }
    try:
        # Get Data Source Identifier
        api_response = api_instance.get_entity_data_source_identifiers(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceEntityAPIsApi->get_entity_data_source_identifiers: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
metaInclude | MetaIncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# MetaIncludeSchema

Included meta objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Included meta objects | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["permissions", "all", "ALL", ] 

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
200 | [ApiResponseFor200](#get_entity_data_source_identifiers.ApiResponseFor200) | Request successfully processed

#### get_entity_data_source_identifiers.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDataSourceIdentifierOutDocument**](../../models/JsonApiDataSourceIdentifierOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_data_source_tables**
<a id="get_entity_data_source_tables"></a>
> JsonApiDataSourceTableOutDocument get_entity_data_source_tables(data_source_idid)



### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import data_source_entity_apis_api
from gooddata_api_client.model.json_api_data_source_table_out_document import JsonApiDataSourceTableOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = data_source_entity_apis_api.DataSourceEntityAPIsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'dataSourceId': "dataSourceId_example",
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        api_response = api_instance.get_entity_data_source_tables(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceEntityAPIsApi->get_entity_data_source_tables: %s\n" % e)

    # example passing only optional values
    path_params = {
        'dataSourceId': "dataSourceId_example",
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=path==v1,v2,v3;type==DataSourceTableTypeValue",
    }
    try:
        api_response = api_instance.get_entity_data_source_tables(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceEntityAPIsApi->get_entity_data_source_tables: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
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
dataSourceId | DataSourceIdSchema | | 
id | IdSchema | | 

# DataSourceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_entity_data_source_tables.ApiResponseFor200) | Request successfully processed

#### get_entity_data_source_tables.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDataSourceTableOutDocument**](../../models/JsonApiDataSourceTableOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_data_sources**
<a id="get_entity_data_sources"></a>
> JsonApiDataSourceOutDocument get_entity_data_sources(id)

Get Data Source entity

Data Source - represents data source for the workspace

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import data_source_entity_apis_api
from gooddata_api_client.model.json_api_data_source_out_document import JsonApiDataSourceOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = data_source_entity_apis_api.DataSourceEntityAPIsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Get Data Source entity
        api_response = api_instance.get_entity_data_sources(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceEntityAPIsApi->get_entity_data_sources: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=name==someString;type==DatabaseTypeValue",
        'metaInclude': [
        "metaInclude=permissions,all"
    ],
    }
    try:
        # Get Data Source entity
        api_response = api_instance.get_entity_data_sources(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceEntityAPIsApi->get_entity_data_sources: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
metaInclude | MetaIncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# MetaIncludeSchema

Included meta objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Included meta objects | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["permissions", "all", "ALL", ] 

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
200 | [ApiResponseFor200](#get_entity_data_sources.ApiResponseFor200) | Request successfully processed

#### get_entity_data_sources.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDataSourceOutDocument**](../../models/JsonApiDataSourceOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **patch_entity_data_sources**
<a id="patch_entity_data_sources"></a>
> JsonApiDataSourceOutDocument patch_entity_data_sources(idjson_api_data_source_patch_document)

Patch Data Source entity

Data Source - represents data source for the workspace

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import data_source_entity_apis_api
from gooddata_api_client.model.json_api_data_source_patch_document import JsonApiDataSourcePatchDocument
from gooddata_api_client.model.json_api_data_source_out_document import JsonApiDataSourceOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = data_source_entity_apis_api.DataSourceEntityAPIsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiDataSourcePatchDocument(
        data=JsonApiDataSourcePatch(
            attributes=dict(
                cache_path=[
                    "cache_path_example"
                ],
                enable_caching=False,
                name="name_example",
                parameters=[
                    dict(
                        name="name_example",
                        value="value_example",
                    )
                ],
                password="password_example",
                schema="schema_example",
                token="token_example",
                type="POSTGRESQL",
                url="url_example",
                username="username_example",
            ),
            id="id1",
            type="dataSource",
        ),
    )
    try:
        # Patch Data Source entity
        api_response = api_instance.patch_entity_data_sources(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceEntityAPIsApi->patch_entity_data_sources: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=name==someString;type==DatabaseTypeValue",
    }
    body = JsonApiDataSourcePatchDocument(
        data=JsonApiDataSourcePatch(
            attributes=dict(
                cache_path=[
                    "cache_path_example"
                ],
                enable_caching=False,
                name="name_example",
                parameters=[
                    dict(
                        name="name_example",
                        value="value_example",
                    )
                ],
                password="password_example",
                schema="schema_example",
                token="token_example",
                type="POSTGRESQL",
                url="url_example",
                username="username_example",
            ),
            id="id1",
            type="dataSource",
        ),
    )
    try:
        # Patch Data Source entity
        api_response = api_instance.patch_entity_data_sources(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceEntityAPIsApi->patch_entity_data_sources: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDataSourcePatchDocument**](../../models/JsonApiDataSourcePatchDocument.md) |  | 


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
200 | [ApiResponseFor200](#patch_entity_data_sources.ApiResponseFor200) | Request successfully processed

#### patch_entity_data_sources.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDataSourceOutDocument**](../../models/JsonApiDataSourceOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_entity_data_sources**
<a id="update_entity_data_sources"></a>
> JsonApiDataSourceOutDocument update_entity_data_sources(idjson_api_data_source_in_document)

Put Data Source entity

Data Source - represents data source for the workspace

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import data_source_entity_apis_api
from gooddata_api_client.model.json_api_data_source_in_document import JsonApiDataSourceInDocument
from gooddata_api_client.model.json_api_data_source_out_document import JsonApiDataSourceOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = data_source_entity_apis_api.DataSourceEntityAPIsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiDataSourceInDocument(
        data=JsonApiDataSourceIn(
            attributes=dict(
                cache_path=[
                    "cache_path_example"
                ],
                enable_caching=False,
                name="name_example",
                parameters=[
                    dict(
                        name="name_example",
                        value="value_example",
                    )
                ],
                password="password_example",
                schema="schema_example",
                token="token_example",
                type="POSTGRESQL",
                url="url_example",
                username="username_example",
            ),
            id="id1",
            type="dataSource",
        ),
    )
    try:
        # Put Data Source entity
        api_response = api_instance.update_entity_data_sources(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceEntityAPIsApi->update_entity_data_sources: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=name==someString;type==DatabaseTypeValue",
    }
    body = JsonApiDataSourceInDocument(
        data=JsonApiDataSourceIn(
            attributes=dict(
                cache_path=[
                    "cache_path_example"
                ],
                enable_caching=False,
                name="name_example",
                parameters=[
                    dict(
                        name="name_example",
                        value="value_example",
                    )
                ],
                password="password_example",
                schema="schema_example",
                token="token_example",
                type="POSTGRESQL",
                url="url_example",
                username="username_example",
            ),
            id="id1",
            type="dataSource",
        ),
    )
    try:
        # Put Data Source entity
        api_response = api_instance.update_entity_data_sources(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceEntityAPIsApi->update_entity_data_sources: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDataSourceInDocument**](../../models/JsonApiDataSourceInDocument.md) |  | 


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
200 | [ApiResponseFor200](#update_entity_data_sources.ApiResponseFor200) | Request successfully processed

#### update_entity_data_sources.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDataSourceOutDocument**](../../models/JsonApiDataSourceOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


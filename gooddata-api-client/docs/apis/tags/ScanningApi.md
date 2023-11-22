<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.scanning_api.ScanningApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_data_source_schemata**](#get_data_source_schemata) | **get** /api/v1/actions/dataSources/{dataSourceId}/scanSchemata | Get a list of schema names of a database
[**scan_data_source**](#scan_data_source) | **post** /api/v1/actions/dataSources/{dataSourceId}/scan | Scan a database to get a physical data model (PDM)
[**scan_sql**](#scan_sql) | **post** /api/v1/actions/dataSources/{dataSourceId}/scanSql | Collect metadata about SQL query

# **get_data_source_schemata**
<a id="get_data_source_schemata"></a>
> DataSourceSchemata get_data_source_schemata(data_source_id)

Get a list of schema names of a database

It scans a database and reads metadata. The result of the request contains a list of schema names of a database.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import scanning_api
from gooddata_api_client.model.data_source_schemata import DataSourceSchemata
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = scanning_api.ScanningApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'dataSourceId': "myPostgres",
    }
    try:
        # Get a list of schema names of a database
        api_response = api_instance.get_data_source_schemata(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ScanningApi->get_data_source_schemata: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

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
200 | [ApiResponseFor200](#get_data_source_schemata.ApiResponseFor200) | The result of the scan schemata

#### get_data_source_schemata.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DataSourceSchemata**](../../models/DataSourceSchemata.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **scan_data_source**
<a id="scan_data_source"></a>
> ScanResultPdm scan_data_source(data_source_idscan_request)

Scan a database to get a physical data model (PDM)

It scans a database and transforms its metadata to a declarative definition of the physical data model (PDM). The result of the request contains the mentioned physical data model (PDM) of a database within warning, for example, about unsupported columns.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import scanning_api
from gooddata_api_client.model.scan_request import ScanRequest
from gooddata_api_client.model.scan_result_pdm import ScanResultPdm
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = scanning_api.ScanningApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'dataSourceId': "myPostgres",
    }
    body = ScanRequest(
        scan_tables=True,
        scan_views=True,
        schemata=["tpch","demo"],
        separator="__",
        table_prefix="out_table",
        view_prefix="out_view",
    )
    try:
        # Scan a database to get a physical data model (PDM)
        api_response = api_instance.scan_data_source(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ScanningApi->scan_data_source: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ScanRequest**](../../models/ScanRequest.md) |  | 


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
200 | [ApiResponseFor200](#scan_data_source.ApiResponseFor200) | The result of the scan.

#### scan_data_source.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ScanResultPdm**](../../models/ScanResultPdm.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **scan_sql**
<a id="scan_sql"></a>
> ScanSqlResponse scan_sql(data_source_idscan_sql_request)

Collect metadata about SQL query

It executes SQL query against specified data source and extracts metadata. Metadata consist of column names and column data types. It can optionally provide also preview of data returned by SQL query

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import scanning_api
from gooddata_api_client.model.scan_sql_response import ScanSqlResponse
from gooddata_api_client.model.scan_sql_request import ScanSqlRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = scanning_api.ScanningApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'dataSourceId': "myPostgres",
    }
    body = ScanSqlRequest(
        sql="SELECT a.special_value as result FROM tableA a",
    )
    try:
        # Collect metadata about SQL query
        api_response = api_instance.scan_sql(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ScanningApi->scan_sql: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ScanSqlRequest**](../../models/ScanSqlRequest.md) |  | 


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
200 | [ApiResponseFor200](#scan_sql.ApiResponseFor200) | The result of the scan.

#### scan_sql.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ScanSqlResponse**](../../models/ScanSqlResponse.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


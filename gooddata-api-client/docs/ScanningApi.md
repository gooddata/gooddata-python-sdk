# gooddata_api_client.ScanningApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_data_source_schemata**](ScanningApi.md#get_data_source_schemata) | **GET** /api/v1/actions/dataSources/{dataSourceId}/scanSchemata | Get a list of schema names of a database
[**scan_data_source**](ScanningApi.md#scan_data_source) | **POST** /api/v1/actions/dataSources/{dataSourceId}/scan | Scan a database to get a physical data model (PDM)
[**scan_sql**](ScanningApi.md#scan_sql) | **POST** /api/v1/actions/dataSources/{dataSourceId}/scanSql | Collect metadata about SQL query


# **get_data_source_schemata**
> DataSourceSchemata get_data_source_schemata(data_source_id)

Get a list of schema names of a database

It scans a database and reads metadata. The result of the request contains a list of schema names of a database.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import scanning_api
from gooddata_api_client.model.data_source_schemata import DataSourceSchemata
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = scanning_api.ScanningApi(api_client)
    data_source_id = "myPostgres" # str | Data source id

    # example passing only required values which don't have defaults set
    try:
        # Get a list of schema names of a database
        api_response = api_instance.get_data_source_schemata(data_source_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ScanningApi->get_data_source_schemata: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| Data source id |

### Return type

[**DataSourceSchemata**](DataSourceSchemata.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The result of the scan schemata |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **scan_data_source**
> ScanResultPdm scan_data_source(data_source_id, scan_request)

Scan a database to get a physical data model (PDM)

It scans a database and transforms its metadata to a declarative definition of the physical data model (PDM). The result of the request contains the mentioned physical data model (PDM) of a database within warning, for example, about unsupported columns.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import scanning_api
from gooddata_api_client.model.scan_request import ScanRequest
from gooddata_api_client.model.scan_result_pdm import ScanResultPdm
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = scanning_api.ScanningApi(api_client)
    data_source_id = "myPostgres" # str | Data source id
    scan_request = ScanRequest(
        scan_tables=True,
        scan_views=True,
        schemata=["tpch","demo"],
        separator="__",
        table_prefix="out_table",
        view_prefix="out_view",
    ) # ScanRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Scan a database to get a physical data model (PDM)
        api_response = api_instance.scan_data_source(data_source_id, scan_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ScanningApi->scan_data_source: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| Data source id |
 **scan_request** | [**ScanRequest**](ScanRequest.md)|  |

### Return type

[**ScanResultPdm**](ScanResultPdm.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The result of the scan. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **scan_sql**
> ScanSqlResponse scan_sql(data_source_id, scan_sql_request)

Collect metadata about SQL query

It executes SQL query against specified data source and extracts metadata. Metadata consist of column names and column data types. It can optionally provide also preview of data returned by SQL query

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import scanning_api
from gooddata_api_client.model.scan_sql_response import ScanSqlResponse
from gooddata_api_client.model.scan_sql_request import ScanSqlRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = scanning_api.ScanningApi(api_client)
    data_source_id = "myPostgres" # str | Data source id
    scan_sql_request = ScanSqlRequest(
        sql="SELECT a.special_value as result FROM tableA a",
    ) # ScanSqlRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Collect metadata about SQL query
        api_response = api_instance.scan_sql(data_source_id, scan_sql_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ScanningApi->scan_sql: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| Data source id |
 **scan_sql_request** | [**ScanSqlRequest**](ScanSqlRequest.md)|  |

### Return type

[**ScanSqlResponse**](ScanSqlResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The result of the scan. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


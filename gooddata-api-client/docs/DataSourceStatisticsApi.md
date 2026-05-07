# gooddata_api_client.DataSourceStatisticsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_data_source_statistics**](DataSourceStatisticsApi.md#delete_data_source_statistics) | **DELETE** /api/v1/layout/dataSources/{dataSourceId}/statistics | (BETA) Delete stored physical statistics for a data source
[**get_data_source_statistics**](DataSourceStatisticsApi.md#get_data_source_statistics) | **GET** /api/v1/layout/dataSources/{dataSourceId}/statistics | (BETA) Retrieve stored physical statistics for a data source
[**put_data_source_statistics**](DataSourceStatisticsApi.md#put_data_source_statistics) | **PUT** /api/v1/layout/dataSources/{dataSourceId}/statistics | (BETA) Store physical table and column statistics for a data source
[**scan_statistics**](DataSourceStatisticsApi.md#scan_statistics) | **POST** /api/v1/actions/dataSources/{dataSourceId}/scanStatistics | (BETA) Collect physical table and column statistics from a StarRocks data source


# **delete_data_source_statistics**
> delete_data_source_statistics(data_source_id)

(BETA) Delete stored physical statistics for a data source

(BETA) Removes all stored physical statistics for the specified data source.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_source_statistics_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_source_statistics_api.DataSourceStatisticsApi(api_client)
    data_source_id = "dataSourceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Delete stored physical statistics for a data source
        api_instance.delete_data_source_statistics(data_source_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceStatisticsApi->delete_data_source_statistics: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  |

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
**204** | Statistics deleted. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_data_source_statistics**
> DataSourceStatisticsResponse get_data_source_statistics(data_source_id)

(BETA) Retrieve stored physical statistics for a data source

(BETA) Returns previously stored physical table and column statistics. Supports optional filtering by schema and table name.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_source_statistics_api
from gooddata_api_client.model.data_source_statistics_response import DataSourceStatisticsResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_source_statistics_api.DataSourceStatisticsApi(api_client)
    data_source_id = "dataSourceId_example" # str | 
    schema_name = "schemaName_example" # str |  (optional)
    table_name = "tableName_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Retrieve stored physical statistics for a data source
        api_response = api_instance.get_data_source_statistics(data_source_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceStatisticsApi->get_data_source_statistics: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) Retrieve stored physical statistics for a data source
        api_response = api_instance.get_data_source_statistics(data_source_id, schema_name=schema_name, table_name=table_name)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceStatisticsApi->get_data_source_statistics: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  |
 **schema_name** | **str**|  | [optional]
 **table_name** | **str**|  | [optional]

### Return type

[**DataSourceStatisticsResponse**](DataSourceStatisticsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_data_source_statistics**
> put_data_source_statistics(data_source_id, data_source_statistics_request)

(BETA) Store physical table and column statistics for a data source

(BETA) Stores or replaces physical statistics (row counts, NDV, null counts, min/max) for tables and columns of a data source.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_source_statistics_api
from gooddata_api_client.model.data_source_statistics_request import DataSourceStatisticsRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_source_statistics_api.DataSourceStatisticsApi(api_client)
    data_source_id = "dataSourceId_example" # str | 
    data_source_statistics_request = DataSourceStatisticsRequest(
        tables=[
            TableStatisticsEntry(
                columns=[
                    ColumnStatisticsEntry(
                        column_name="column_name_example",
                        data_size=1,
                        max="max_example",
                        min="min_example",
                        ndv=1,
                        null_count=1,
                    ),
                ],
                data_size=1,
                row_count=1,
                schema_name="schema_name_example",
                table_name="table_name_example",
            ),
        ],
    ) # DataSourceStatisticsRequest | 

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Store physical table and column statistics for a data source
        api_instance.put_data_source_statistics(data_source_id, data_source_statistics_request)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceStatisticsApi->put_data_source_statistics: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  |
 **data_source_statistics_request** | [**DataSourceStatisticsRequest**](DataSourceStatisticsRequest.md)|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Statistics stored successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **scan_statistics**
> TableStatisticsResponse scan_statistics(data_source_id, table_statistics_request)

(BETA) Collect physical table and column statistics from a StarRocks data source

(BETA) Reads pre-computed CBO statistics from StarRocks. Supports both internal catalog (native/PIPE tables) and external catalog (Iceberg tables). Statistics include row counts, data sizes, NDV (number of distinct values), null counts, and min/max values.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_source_statistics_api
from gooddata_api_client.model.table_statistics_request import TableStatisticsRequest
from gooddata_api_client.model.table_statistics_response import TableStatisticsResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_source_statistics_api.DataSourceStatisticsApi(api_client)
    data_source_id = "dataSourceId_example" # str | 
    table_statistics_request = TableStatisticsRequest(
        schemata=[
            "schemata_example",
        ],
        table_names=[
            "table_names_example",
        ],
    ) # TableStatisticsRequest | 

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Collect physical table and column statistics from a StarRocks data source
        api_response = api_instance.scan_statistics(data_source_id, table_statistics_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceStatisticsApi->scan_statistics: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  |
 **table_statistics_request** | [**TableStatisticsRequest**](TableStatisticsRequest.md)|  |

### Return type

[**TableStatisticsResponse**](TableStatisticsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


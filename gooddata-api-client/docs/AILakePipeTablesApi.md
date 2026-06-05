# gooddata_api_client.AILakePipeTablesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**analyze_statistics**](AILakePipeTablesApi.md#analyze_statistics) | **POST** /api/v1/ailake/database/instances/{instanceId}/analyzeStatistics | (BETA) Run ANALYZE TABLE for tables in a database instance
[**create_ai_lake_pipe_table**](AILakePipeTablesApi.md#create_ai_lake_pipe_table) | **POST** /api/v1/ailake/database/instances/{instanceId}/pipeTables | (BETA) Create a new AI Lake pipe table
[**delete_ai_lake_pipe_table**](AILakePipeTablesApi.md#delete_ai_lake_pipe_table) | **DELETE** /api/v1/ailake/database/instances/{instanceId}/pipeTables/{tableName} | (BETA) Delete an AI Lake pipe table
[**get_ai_lake_pipe_table**](AILakePipeTablesApi.md#get_ai_lake_pipe_table) | **GET** /api/v1/ailake/database/instances/{instanceId}/pipeTables/{tableName} | (BETA) Get an AI Lake pipe table
[**list_ai_lake_pipe_tables**](AILakePipeTablesApi.md#list_ai_lake_pipe_tables) | **GET** /api/v1/ailake/database/instances/{instanceId}/pipeTables | (BETA) List AI Lake pipe tables
[**refresh_ai_lake_pipe_table_partition**](AILakePipeTablesApi.md#refresh_ai_lake_pipe_table_partition) | **POST** /api/v1/ailake/database/instances/{instanceId}/pipeTables/{tableName}/refresh | (BETA) Refresh a pipe table partition


# **analyze_statistics**
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} analyze_statistics(instance_id, analyze_statistics_request)

(BETA) Run ANALYZE TABLE for tables in a database instance

(BETA) Collects CBO statistics for tables in a StarRocks database. Works for both internal (native/PIPE) and external (Iceberg) catalogs. If tableNames is empty, all tables are analyzed.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_pipe_tables_api
from gooddata_api_client.model.analyze_statistics_request import AnalyzeStatisticsRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_pipe_tables_api.AILakePipeTablesApi(api_client)
    instance_id = "instanceId_example" # str | Database instance identifier. Accepts the database name (preferred) or UUID.
    analyze_statistics_request = AnalyzeStatisticsRequest(
        table_names=[
            "table_names_example",
        ],
    ) # AnalyzeStatisticsRequest | 
    operation_id = "operation-id_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Run ANALYZE TABLE for tables in a database instance
        api_response = api_instance.analyze_statistics(instance_id, analyze_statistics_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakePipeTablesApi->analyze_statistics: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) Run ANALYZE TABLE for tables in a database instance
        api_response = api_instance.analyze_statistics(instance_id, analyze_statistics_request, operation_id=operation_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakePipeTablesApi->analyze_statistics: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instance_id** | **str**| Database instance identifier. Accepts the database name (preferred) or UUID. |
 **analyze_statistics_request** | [**AnalyzeStatisticsRequest**](AnalyzeStatisticsRequest.md)|  |
 **operation_id** | **str**|  | [optional]

### Return type

**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Statistics analysis scheduled. |  * operation-id -  <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_ai_lake_pipe_table**
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} create_ai_lake_pipe_table(instance_id, create_pipe_table_request)

(BETA) Create a new AI Lake pipe table

(BETA) Creates a pipe-backed OLAP table in the given AI Lake database instance. Infers schema from parquet files. Returns an operation-id header the client can use to poll for progress.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_pipe_tables_api
from gooddata_api_client.model.create_pipe_table_request import CreatePipeTableRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_pipe_tables_api.AILakePipeTablesApi(api_client)
    instance_id = "instanceId_example" # str | Database instance identifier. Accepts the database name (preferred) or UUID.
    create_pipe_table_request = CreatePipeTableRequest(
        aggregation_overrides={
            "key": "key_example",
        },
        column_expressions={
            "key": ColumnExpression(
                column="column_example",
                function="HLL_HASH",
            ),
        },
        column_overrides={
            "key": "key_example",
        },
        distribution_config=DistributionConfig(
            type="type_example",
        ),
        key_config=KeyConfig(
            type="type_example",
        ),
        max_varchar_length=1,
        partition_config=PartitionConfig(
            type="type_example",
        ),
        path_prefix="path_prefix_example",
        polling_interval_seconds=1,
        source_storage_name="source_storage_name_example",
        table_name="table_name_example",
        table_properties={
            "key": "key_example",
        },
    ) # CreatePipeTableRequest | 
    operation_id = "operation-id_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Create a new AI Lake pipe table
        api_response = api_instance.create_ai_lake_pipe_table(instance_id, create_pipe_table_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakePipeTablesApi->create_ai_lake_pipe_table: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) Create a new AI Lake pipe table
        api_response = api_instance.create_ai_lake_pipe_table(instance_id, create_pipe_table_request, operation_id=operation_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakePipeTablesApi->create_ai_lake_pipe_table: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instance_id** | **str**| Database instance identifier. Accepts the database name (preferred) or UUID. |
 **create_pipe_table_request** | [**CreatePipeTableRequest**](CreatePipeTableRequest.md)|  |
 **operation_id** | **str**|  | [optional]

### Return type

**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Accepted |  * operation-id - Operation ID to use for polling. <br>  * operation-location - Operation location URL that can be used for polling. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_ai_lake_pipe_table**
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} delete_ai_lake_pipe_table(instance_id, table_name)

(BETA) Delete an AI Lake pipe table

(BETA) Drops the pipe and OLAP table and removes the record. Returns an operation-id header the client can use to poll for progress.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_pipe_tables_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_pipe_tables_api.AILakePipeTablesApi(api_client)
    instance_id = "instanceId_example" # str | Database instance identifier. Accepts the database name (preferred) or UUID.
    table_name = "tableName_example" # str | Pipe table name.
    operation_id = "operation-id_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Delete an AI Lake pipe table
        api_response = api_instance.delete_ai_lake_pipe_table(instance_id, table_name)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakePipeTablesApi->delete_ai_lake_pipe_table: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) Delete an AI Lake pipe table
        api_response = api_instance.delete_ai_lake_pipe_table(instance_id, table_name, operation_id=operation_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakePipeTablesApi->delete_ai_lake_pipe_table: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instance_id** | **str**| Database instance identifier. Accepts the database name (preferred) or UUID. |
 **table_name** | **str**| Pipe table name. |
 **operation_id** | **str**|  | [optional]

### Return type

**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Accepted |  * operation-id - Operation ID to use for polling. <br>  * operation-location - Operation location URL that can be used for polling. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_ai_lake_pipe_table**
> JsonApiDocumentPipeTable get_ai_lake_pipe_table(instance_id, table_name)

(BETA) Get an AI Lake pipe table

(BETA) Returns full details of the specified pipe table.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_pipe_tables_api
from gooddata_api_client.model.json_api_document_pipe_table import JsonApiDocumentPipeTable
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_pipe_tables_api.AILakePipeTablesApi(api_client)
    instance_id = "instanceId_example" # str | Database instance identifier. Accepts the database name (preferred) or UUID.
    table_name = "tableName_example" # str | Pipe table name.

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Get an AI Lake pipe table
        api_response = api_instance.get_ai_lake_pipe_table(instance_id, table_name)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakePipeTablesApi->get_ai_lake_pipe_table: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instance_id** | **str**| Database instance identifier. Accepts the database name (preferred) or UUID. |
 **table_name** | **str**| Pipe table name. |

### Return type

[**JsonApiDocumentPipeTable**](JsonApiDocumentPipeTable.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | AI Lake pipe table successfully retrieved |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_ai_lake_pipe_tables**
> JsonApiListDocumentPipeTableSummary list_ai_lake_pipe_tables(instance_id)

(BETA) List AI Lake pipe tables

(BETA) Lists active pipe tables in the given AI Lake database instance.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_pipe_tables_api
from gooddata_api_client.model.json_api_list_document_pipe_table_summary import JsonApiListDocumentPipeTableSummary
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_pipe_tables_api.AILakePipeTablesApi(api_client)
    instance_id = "instanceId_example" # str | Database instance identifier. Accepts the database name (preferred) or UUID.
    page = "0" # str | Zero-based page number. (optional) if omitted the server will use the default value of "0"
    size = "50" # str | Number of items per page. (optional) if omitted the server will use the default value of "50"
    meta_include = [
        "metaInclude_example",
    ] # [str] |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # (BETA) List AI Lake pipe tables
        api_response = api_instance.list_ai_lake_pipe_tables(instance_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakePipeTablesApi->list_ai_lake_pipe_tables: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) List AI Lake pipe tables
        api_response = api_instance.list_ai_lake_pipe_tables(instance_id, page=page, size=size, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakePipeTablesApi->list_ai_lake_pipe_tables: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instance_id** | **str**| Database instance identifier. Accepts the database name (preferred) or UUID. |
 **page** | **str**| Zero-based page number. | [optional] if omitted the server will use the default value of "0"
 **size** | **str**| Number of items per page. | [optional] if omitted the server will use the default value of "50"
 **meta_include** | **[str]**|  | [optional]

### Return type

[**JsonApiListDocumentPipeTableSummary**](JsonApiListDocumentPipeTableSummary.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | AI Lake pipe tables successfully retrieved |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **refresh_ai_lake_pipe_table_partition**
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} refresh_ai_lake_pipe_table_partition(instance_id, table_name, refresh_partition_request)

(BETA) Refresh a pipe table partition

(BETA) Deletes all rows for the specified Hive partition and re-loads them from S3. Use after overwriting a partition file in object storage with corrected data. Returns an operation-id header the client can use to poll for progress.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_pipe_tables_api
from gooddata_api_client.model.refresh_partition_request import RefreshPartitionRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_pipe_tables_api.AILakePipeTablesApi(api_client)
    instance_id = "instanceId_example" # str | Database instance identifier. Accepts the database name (preferred) or UUID.
    table_name = "tableName_example" # str | Pipe table name.
    refresh_partition_request = RefreshPartitionRequest(
        partition_spec={
            "key": "key_example",
        },
    ) # RefreshPartitionRequest | 
    operation_id = "operation-id_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Refresh a pipe table partition
        api_response = api_instance.refresh_ai_lake_pipe_table_partition(instance_id, table_name, refresh_partition_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakePipeTablesApi->refresh_ai_lake_pipe_table_partition: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) Refresh a pipe table partition
        api_response = api_instance.refresh_ai_lake_pipe_table_partition(instance_id, table_name, refresh_partition_request, operation_id=operation_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakePipeTablesApi->refresh_ai_lake_pipe_table_partition: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instance_id** | **str**| Database instance identifier. Accepts the database name (preferred) or UUID. |
 **table_name** | **str**| Pipe table name. |
 **refresh_partition_request** | [**RefreshPartitionRequest**](RefreshPartitionRequest.md)|  |
 **operation_id** | **str**|  | [optional]

### Return type

**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Accepted |  * operation-id - Operation ID to use for polling. <br>  * operation-location - Operation location URL that can be used for polling. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


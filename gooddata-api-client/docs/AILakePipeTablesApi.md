# gooddata_api_client.AILakePipeTablesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_ai_lake_pipe_table**](AILakePipeTablesApi.md#create_ai_lake_pipe_table) | **POST** /api/v1/ailake/database/instances/{instanceId}/pipeTables | (BETA) Create a new AI Lake pipe table
[**delete_ai_lake_pipe_table**](AILakePipeTablesApi.md#delete_ai_lake_pipe_table) | **DELETE** /api/v1/ailake/database/instances/{instanceId}/pipeTables/{tableName} | (BETA) Delete an AI Lake pipe table
[**get_ai_lake_pipe_table**](AILakePipeTablesApi.md#get_ai_lake_pipe_table) | **GET** /api/v1/ailake/database/instances/{instanceId}/pipeTables/{tableName} | (BETA) Get an AI Lake pipe table
[**list_ai_lake_pipe_tables**](AILakePipeTablesApi.md#list_ai_lake_pipe_tables) | **GET** /api/v1/ailake/database/instances/{instanceId}/pipeTables | (BETA) List AI Lake pipe tables


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
> PipeTable get_ai_lake_pipe_table(instance_id, table_name)

(BETA) Get an AI Lake pipe table

(BETA) Returns full details of the specified pipe table.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_pipe_tables_api
from gooddata_api_client.model.pipe_table import PipeTable
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

[**PipeTable**](PipeTable.md)

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
> ListPipeTablesResponse list_ai_lake_pipe_tables(instance_id)

(BETA) List AI Lake pipe tables

(BETA) Lists all active pipe tables in the given AI Lake database instance.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_pipe_tables_api
from gooddata_api_client.model.list_pipe_tables_response import ListPipeTablesResponse
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

    # example passing only required values which don't have defaults set
    try:
        # (BETA) List AI Lake pipe tables
        api_response = api_instance.list_ai_lake_pipe_tables(instance_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakePipeTablesApi->list_ai_lake_pipe_tables: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instance_id** | **str**| Database instance identifier. Accepts the database name (preferred) or UUID. |

### Return type

[**ListPipeTablesResponse**](ListPipeTablesResponse.md)

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


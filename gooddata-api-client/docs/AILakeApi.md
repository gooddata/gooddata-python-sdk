# gooddata_api_client.AILakeApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_ai_lake_database_data_source**](AILakeApi.md#add_ai_lake_database_data_source) | **POST** /api/v1/ailake/database/instances/{instanceId}/dataSources | (BETA) Add a data source to an AILake Database instance
[**analyze_statistics**](AILakeApi.md#analyze_statistics) | **POST** /api/v1/ailake/database/instances/{instanceId}/analyzeStatistics | (BETA) Run ANALYZE TABLE for tables in a database instance
[**create_ai_lake_pipe_table**](AILakeApi.md#create_ai_lake_pipe_table) | **POST** /api/v1/ailake/database/instances/{instanceId}/pipeTables | (BETA) Create a new AI Lake pipe table
[**delete_ai_lake_pipe_table**](AILakeApi.md#delete_ai_lake_pipe_table) | **DELETE** /api/v1/ailake/database/instances/{instanceId}/pipeTables/{tableName} | (BETA) Delete an AI Lake pipe table
[**deprovision_ai_lake_database_instance**](AILakeApi.md#deprovision_ai_lake_database_instance) | **DELETE** /api/v1/ailake/database/instances/{instanceId} | (BETA) Delete an existing AILake Database instance
[**get_ai_lake_database_instance**](AILakeApi.md#get_ai_lake_database_instance) | **GET** /api/v1/ailake/database/instances/{instanceId} | (BETA) Get the specified AILake Database instance
[**get_ai_lake_operation**](AILakeApi.md#get_ai_lake_operation) | **GET** /api/v1/ailake/operations/{operationId} | (BETA) Get Long Running Operation details
[**get_ai_lake_pipe_table**](AILakeApi.md#get_ai_lake_pipe_table) | **GET** /api/v1/ailake/database/instances/{instanceId}/pipeTables/{tableName} | (BETA) Get an AI Lake pipe table
[**get_ai_lake_service_status**](AILakeApi.md#get_ai_lake_service_status) | **GET** /api/v1/ailake/services/{serviceId}/status | (BETA) Get AI Lake service status
[**list_ai_lake_database_data_sources**](AILakeApi.md#list_ai_lake_database_data_sources) | **GET** /api/v1/ailake/database/instances/{instanceId}/dataSources | (BETA) List data sources of an AILake Database instance
[**list_ai_lake_database_instances**](AILakeApi.md#list_ai_lake_database_instances) | **GET** /api/v1/ailake/database/instances | (BETA) List AI Lake Database instances
[**list_ai_lake_object_storages**](AILakeApi.md#list_ai_lake_object_storages) | **GET** /api/v1/ailake/object-storages | (BETA) List registered AI Lake ObjectStorages
[**list_ai_lake_pipe_tables**](AILakeApi.md#list_ai_lake_pipe_tables) | **GET** /api/v1/ailake/database/instances/{instanceId}/pipeTables | (BETA) List AI Lake pipe tables
[**list_ai_lake_services**](AILakeApi.md#list_ai_lake_services) | **GET** /api/v1/ailake/services | (BETA) List AI Lake services
[**provision_ai_lake_database_instance**](AILakeApi.md#provision_ai_lake_database_instance) | **POST** /api/v1/ailake/database/instances | (BETA) Create a new AILake Database instance
[**remove_ai_lake_database_data_source**](AILakeApi.md#remove_ai_lake_database_data_source) | **DELETE** /api/v1/ailake/database/instances/{instanceId}/dataSources/{dataSourceId} | (BETA) Remove a data source from an AILake Database instance
[**run_ai_lake_service_command**](AILakeApi.md#run_ai_lake_service_command) | **POST** /api/v1/ailake/services/{serviceId}/commands/{commandName}/run | (BETA) Run an AI Lake services command
[**update_ai_lake_database_data_source**](AILakeApi.md#update_ai_lake_database_data_source) | **PATCH** /api/v1/ailake/database/instances/{instanceId}/dataSource | (BETA) Update the data source of an AILake Database instance


# **add_ai_lake_database_data_source**
> AddDatabaseDataSourceResponse add_ai_lake_database_data_source(instance_id, add_database_data_source_request)

(BETA) Add a data source to an AILake Database instance

(BETA) Associates an additional metadata-api data source with an existing AI Lake database instance. The new data source uses the same StarRocks connection details as the primary data source.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_api
from gooddata_api_client.model.add_database_data_source_request import AddDatabaseDataSourceRequest
from gooddata_api_client.model.add_database_data_source_response import AddDatabaseDataSourceResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_api.AILakeApi(api_client)
    instance_id = "instanceId_example" # str | Database instance identifier. Accepts the database name (preferred) or UUID.
    add_database_data_source_request = AddDatabaseDataSourceRequest(
        data_source_id="data_source_id_example",
        data_source_name="data_source_name_example",
    ) # AddDatabaseDataSourceRequest | 

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Add a data source to an AILake Database instance
        api_response = api_instance.add_ai_lake_database_data_source(instance_id, add_database_data_source_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->add_ai_lake_database_data_source: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instance_id** | **str**| Database instance identifier. Accepts the database name (preferred) or UUID. |
 **add_database_data_source_request** | [**AddDatabaseDataSourceRequest**](AddDatabaseDataSourceRequest.md)|  |

### Return type

[**AddDatabaseDataSourceResponse**](AddDatabaseDataSourceResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Data source successfully added |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **analyze_statistics**
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} analyze_statistics(instance_id, analyze_statistics_request)

(BETA) Run ANALYZE TABLE for tables in a database instance

(BETA) Collects CBO statistics for tables in a StarRocks database. Works for both internal (native/PIPE) and external (Iceberg) catalogs. If tableNames is empty, all tables are analyzed.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_api
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
    api_instance = ai_lake_api.AILakeApi(api_client)
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
        print("Exception when calling AILakeApi->analyze_statistics: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) Run ANALYZE TABLE for tables in a database instance
        api_response = api_instance.analyze_statistics(instance_id, analyze_statistics_request, operation_id=operation_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->analyze_statistics: %s\n" % e)
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
from gooddata_api_client.api import ai_lake_api
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
    api_instance = ai_lake_api.AILakeApi(api_client)
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
        print("Exception when calling AILakeApi->create_ai_lake_pipe_table: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) Create a new AI Lake pipe table
        api_response = api_instance.create_ai_lake_pipe_table(instance_id, create_pipe_table_request, operation_id=operation_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->create_ai_lake_pipe_table: %s\n" % e)
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
from gooddata_api_client.api import ai_lake_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_api.AILakeApi(api_client)
    instance_id = "instanceId_example" # str | Database instance identifier. Accepts the database name (preferred) or UUID.
    table_name = "tableName_example" # str | Pipe table name.
    operation_id = "operation-id_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Delete an AI Lake pipe table
        api_response = api_instance.delete_ai_lake_pipe_table(instance_id, table_name)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->delete_ai_lake_pipe_table: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) Delete an AI Lake pipe table
        api_response = api_instance.delete_ai_lake_pipe_table(instance_id, table_name, operation_id=operation_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->delete_ai_lake_pipe_table: %s\n" % e)
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

# **deprovision_ai_lake_database_instance**
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} deprovision_ai_lake_database_instance(instance_id)

(BETA) Delete an existing AILake Database instance

(BETA) Deletes an existing database in the organization's AI Lake. Returns an operation-id in the operation-id header the client can use to poll for the progress.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_api.AILakeApi(api_client)
    instance_id = "instanceId_example" # str | Database instance identifier. Accepts the database name (preferred) or UUID.
    operation_id = "operation-id_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Delete an existing AILake Database instance
        api_response = api_instance.deprovision_ai_lake_database_instance(instance_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->deprovision_ai_lake_database_instance: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) Delete an existing AILake Database instance
        api_response = api_instance.deprovision_ai_lake_database_instance(instance_id, operation_id=operation_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->deprovision_ai_lake_database_instance: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instance_id** | **str**| Database instance identifier. Accepts the database name (preferred) or UUID. |
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

# **get_ai_lake_database_instance**
> DatabaseInstance get_ai_lake_database_instance(instance_id)

(BETA) Get the specified AILake Database instance

(BETA) Retrieve details of the specified AI Lake database instance in the organization's AI Lake.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_api
from gooddata_api_client.model.database_instance import DatabaseInstance
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_api.AILakeApi(api_client)
    instance_id = "instanceId_example" # str | Database instance identifier. Accepts the database name (preferred) or UUID.

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Get the specified AILake Database instance
        api_response = api_instance.get_ai_lake_database_instance(instance_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->get_ai_lake_database_instance: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instance_id** | **str**| Database instance identifier. Accepts the database name (preferred) or UUID. |

### Return type

[**DatabaseInstance**](DatabaseInstance.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | AI Lake database instance successfully retrieved |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_ai_lake_operation**
> GetAiLakeOperation200Response get_ai_lake_operation(operation_id)

(BETA) Get Long Running Operation details

(BETA) Retrieves details of a Long Running Operation specified by the operation-id.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_api
from gooddata_api_client.model.get_ai_lake_operation200_response import GetAiLakeOperation200Response
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_api.AILakeApi(api_client)
    operation_id = "e9fd5d74-8a1b-46bd-ac60-bd91e9206897" # str | Operation ID

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Get Long Running Operation details
        api_response = api_instance.get_ai_lake_operation(operation_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->get_ai_lake_operation: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **operation_id** | **str**| Operation ID |

### Return type

[**GetAiLakeOperation200Response**](GetAiLakeOperation200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | AI Lake Long Running Operation details successfully retrieved |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_ai_lake_pipe_table**
> PipeTable get_ai_lake_pipe_table(instance_id, table_name)

(BETA) Get an AI Lake pipe table

(BETA) Returns full details of the specified pipe table.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_api
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
    api_instance = ai_lake_api.AILakeApi(api_client)
    instance_id = "instanceId_example" # str | Database instance identifier. Accepts the database name (preferred) or UUID.
    table_name = "tableName_example" # str | Pipe table name.

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Get an AI Lake pipe table
        api_response = api_instance.get_ai_lake_pipe_table(instance_id, table_name)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->get_ai_lake_pipe_table: %s\n" % e)
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

# **get_ai_lake_service_status**
> GetServiceStatusResponse get_ai_lake_service_status(service_id)

(BETA) Get AI Lake service status

(BETA) Returns the status of a service in the organization's AI Lake. The status is controller-specific (e.g., available commands, readiness).

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_api
from gooddata_api_client.model.get_service_status_response import GetServiceStatusResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_api.AILakeApi(api_client)
    service_id = "serviceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Get AI Lake service status
        api_response = api_instance.get_ai_lake_service_status(service_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->get_ai_lake_service_status: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_id** | **str**|  |

### Return type

[**GetServiceStatusResponse**](GetServiceStatusResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | AI Lake service status successfully retrieved |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_ai_lake_database_data_sources**
> ListDatabaseDataSourcesResponse list_ai_lake_database_data_sources(instance_id)

(BETA) List data sources of an AILake Database instance

(BETA) Returns all data source associations for the specified AI Lake database instance.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_api
from gooddata_api_client.model.list_database_data_sources_response import ListDatabaseDataSourcesResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_api.AILakeApi(api_client)
    instance_id = "instanceId_example" # str | Database instance identifier. Accepts the database name (preferred) or UUID.

    # example passing only required values which don't have defaults set
    try:
        # (BETA) List data sources of an AILake Database instance
        api_response = api_instance.list_ai_lake_database_data_sources(instance_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->list_ai_lake_database_data_sources: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instance_id** | **str**| Database instance identifier. Accepts the database name (preferred) or UUID. |

### Return type

[**ListDatabaseDataSourcesResponse**](ListDatabaseDataSourcesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Data sources successfully retrieved |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_ai_lake_database_instances**
> ListDatabaseInstancesResponse list_ai_lake_database_instances()

(BETA) List AI Lake Database instances

(BETA) Lists database instances in the organization's AI Lake. Supports paging via size and offset query parameters. Use metaInclude=page to get total count.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_api
from gooddata_api_client.model.list_database_instances_response import ListDatabaseInstancesResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_api.AILakeApi(api_client)
    size = 50 # int |  (optional) if omitted the server will use the default value of 50
    offset = 0 # int |  (optional) if omitted the server will use the default value of 0
    meta_include = [
        "metaInclude_example",
    ] # [str] |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) List AI Lake Database instances
        api_response = api_instance.list_ai_lake_database_instances(size=size, offset=offset, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->list_ai_lake_database_instances: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **size** | **int**|  | [optional] if omitted the server will use the default value of 50
 **offset** | **int**|  | [optional] if omitted the server will use the default value of 0
 **meta_include** | **[str]**|  | [optional]

### Return type

[**ListDatabaseInstancesResponse**](ListDatabaseInstancesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | AI Lake database instances successfully retrieved |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_ai_lake_object_storages**
> ListObjectStoragesResponse list_ai_lake_object_storages()

(BETA) List registered AI Lake ObjectStorages

(BETA) Lists ObjectStorages registered for the organization. Use the returned `name` as `sourceStorageName` in CreatePipeTable, or pass `storageId` to the ProvisionDatabase `storageIds` list. Provider credentials are stripped — only safe descriptors (id, name, type, bucket, region, endpoint, …) are returned.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_api
from gooddata_api_client.model.list_object_storages_response import ListObjectStoragesResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_api.AILakeApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # (BETA) List registered AI Lake ObjectStorages
        api_response = api_instance.list_ai_lake_object_storages()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->list_ai_lake_object_storages: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**ListObjectStoragesResponse**](ListObjectStoragesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | AI Lake ObjectStorages successfully retrieved |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_ai_lake_pipe_tables**
> ListPipeTablesResponse list_ai_lake_pipe_tables(instance_id)

(BETA) List AI Lake pipe tables

(BETA) Lists all active pipe tables in the given AI Lake database instance.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_api
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
    api_instance = ai_lake_api.AILakeApi(api_client)
    instance_id = "instanceId_example" # str | Database instance identifier. Accepts the database name (preferred) or UUID.

    # example passing only required values which don't have defaults set
    try:
        # (BETA) List AI Lake pipe tables
        api_response = api_instance.list_ai_lake_pipe_tables(instance_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->list_ai_lake_pipe_tables: %s\n" % e)
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

# **list_ai_lake_services**
> ListServicesResponse list_ai_lake_services()

(BETA) List AI Lake services

(BETA) Lists services configured for the organization's AI Lake. Returns only non-sensitive fields (id, name). Supports paging via size and offset query parameters. Use metaInclude=page to get total count.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_api
from gooddata_api_client.model.list_services_response import ListServicesResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_api.AILakeApi(api_client)
    size = 50 # int |  (optional) if omitted the server will use the default value of 50
    offset = 0 # int |  (optional) if omitted the server will use the default value of 0
    meta_include = [
        "metaInclude_example",
    ] # [str] |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) List AI Lake services
        api_response = api_instance.list_ai_lake_services(size=size, offset=offset, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->list_ai_lake_services: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **size** | **int**|  | [optional] if omitted the server will use the default value of 50
 **offset** | **int**|  | [optional] if omitted the server will use the default value of 0
 **meta_include** | **[str]**|  | [optional]

### Return type

[**ListServicesResponse**](ListServicesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | AI Lake services successfully retrieved |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **provision_ai_lake_database_instance**
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} provision_ai_lake_database_instance(provision_database_instance_request)

(BETA) Create a new AILake Database instance

(BETA) Creates a new database in the organization's AI Lake. Returns an operation-id in the operation-id header the client can use to poll for the progress.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_api
from gooddata_api_client.model.provision_database_instance_request import ProvisionDatabaseInstanceRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_api.AILakeApi(api_client)
    provision_database_instance_request = ProvisionDatabaseInstanceRequest(
        data_source_id="data_source_id_example",
        data_source_name="data_source_name_example",
        name="name_example",
        storage_ids=[
            "storage_ids_example",
        ],
    ) # ProvisionDatabaseInstanceRequest | 
    operation_id = "operation-id_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Create a new AILake Database instance
        api_response = api_instance.provision_ai_lake_database_instance(provision_database_instance_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->provision_ai_lake_database_instance: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) Create a new AILake Database instance
        api_response = api_instance.provision_ai_lake_database_instance(provision_database_instance_request, operation_id=operation_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->provision_ai_lake_database_instance: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **provision_database_instance_request** | [**ProvisionDatabaseInstanceRequest**](ProvisionDatabaseInstanceRequest.md)|  |
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

# **remove_ai_lake_database_data_source**
> RemoveDatabaseDataSourceResponse remove_ai_lake_database_data_source(instance_id, data_source_id)

(BETA) Remove a data source from an AILake Database instance

(BETA) Removes a data source association from an AI Lake database instance and deletes the corresponding data source from metadata-api. Fails if removing the data source would leave the instance with no data sources.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_api
from gooddata_api_client.model.remove_database_data_source_response import RemoveDatabaseDataSourceResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_api.AILakeApi(api_client)
    instance_id = "instanceId_example" # str | Database instance identifier. Accepts the database name (preferred) or UUID.
    data_source_id = "dataSourceId_example" # str | Identifier of the data source to remove.

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Remove a data source from an AILake Database instance
        api_response = api_instance.remove_ai_lake_database_data_source(instance_id, data_source_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->remove_ai_lake_database_data_source: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instance_id** | **str**| Database instance identifier. Accepts the database name (preferred) or UUID. |
 **data_source_id** | **str**| Identifier of the data source to remove. |

### Return type

[**RemoveDatabaseDataSourceResponse**](RemoveDatabaseDataSourceResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Data source successfully removed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **run_ai_lake_service_command**
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} run_ai_lake_service_command(service_id, command_name, run_service_command_request)

(BETA) Run an AI Lake services command

(BETA) Runs a specific AI Lake service command.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_api
from gooddata_api_client.model.run_service_command_request import RunServiceCommandRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_api.AILakeApi(api_client)
    service_id = "serviceId_example" # str | 
    command_name = "commandName_example" # str | 
    run_service_command_request = RunServiceCommandRequest(
        context={
            "key": "key_example",
        },
        payload=JsonNode(),
    ) # RunServiceCommandRequest | 
    operation_id = "operation-id_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Run an AI Lake services command
        api_response = api_instance.run_ai_lake_service_command(service_id, command_name, run_service_command_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->run_ai_lake_service_command: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) Run an AI Lake services command
        api_response = api_instance.run_ai_lake_service_command(service_id, command_name, run_service_command_request, operation_id=operation_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->run_ai_lake_service_command: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_id** | **str**|  |
 **command_name** | **str**|  |
 **run_service_command_request** | [**RunServiceCommandRequest**](RunServiceCommandRequest.md)|  |
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

# **update_ai_lake_database_data_source**
> UpdateDatabaseDataSourceResponse update_ai_lake_database_data_source(instance_id, update_database_data_source_request)

(BETA) Update the data source of an AILake Database instance

(BETA) Updates the data source ID and name for an existing AI Lake database instance without deleting the underlying database. Use this to recover from a wrong data source ID provisioned on an existing database instance.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_api
from gooddata_api_client.model.update_database_data_source_request import UpdateDatabaseDataSourceRequest
from gooddata_api_client.model.update_database_data_source_response import UpdateDatabaseDataSourceResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_api.AILakeApi(api_client)
    instance_id = "instanceId_example" # str | Database instance identifier. Accepts the database name (preferred) or UUID.
    update_database_data_source_request = UpdateDatabaseDataSourceRequest(
        data_source_id="data_source_id_example",
        data_source_name="data_source_name_example",
        old_data_source_id="old_data_source_id_example",
    ) # UpdateDatabaseDataSourceRequest | 

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Update the data source of an AILake Database instance
        api_response = api_instance.update_ai_lake_database_data_source(instance_id, update_database_data_source_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->update_ai_lake_database_data_source: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instance_id** | **str**| Database instance identifier. Accepts the database name (preferred) or UUID. |
 **update_database_data_source_request** | [**UpdateDatabaseDataSourceRequest**](UpdateDatabaseDataSourceRequest.md)|  |

### Return type

[**UpdateDatabaseDataSourceResponse**](UpdateDatabaseDataSourceResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Data source successfully updated |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


# gooddata_api_client.AILakeDatabasesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_ai_lake_database_data_source**](AILakeDatabasesApi.md#add_ai_lake_database_data_source) | **POST** /api/v1/ailake/database/instances/{instanceId}/dataSources | (BETA) Add a data source to an AILake Database instance
[**deprovision_ai_lake_database_instance**](AILakeDatabasesApi.md#deprovision_ai_lake_database_instance) | **DELETE** /api/v1/ailake/database/instances/{instanceId} | (BETA) Delete an existing AILake Database instance
[**get_ai_lake_database_instance**](AILakeDatabasesApi.md#get_ai_lake_database_instance) | **GET** /api/v1/ailake/database/instances/{instanceId} | (BETA) Get the specified AILake Database instance
[**list_ai_lake_database_data_sources**](AILakeDatabasesApi.md#list_ai_lake_database_data_sources) | **GET** /api/v1/ailake/database/instances/{instanceId}/dataSources | (BETA) List data sources of an AILake Database instance
[**list_ai_lake_database_instances**](AILakeDatabasesApi.md#list_ai_lake_database_instances) | **GET** /api/v1/ailake/database/instances | (BETA) List AI Lake Database instances
[**list_ai_lake_object_storages**](AILakeDatabasesApi.md#list_ai_lake_object_storages) | **GET** /api/v1/ailake/objectStorages | (BETA) List registered AI Lake ObjectStorages
[**provision_ai_lake_database_instance**](AILakeDatabasesApi.md#provision_ai_lake_database_instance) | **POST** /api/v1/ailake/database/instances | (BETA) Create a new AILake Database instance
[**remove_ai_lake_database_data_source**](AILakeDatabasesApi.md#remove_ai_lake_database_data_source) | **DELETE** /api/v1/ailake/database/instances/{instanceId}/dataSources/{dataSourceId} | (BETA) Remove a data source from an AILake Database instance
[**update_ai_lake_database_data_source**](AILakeDatabasesApi.md#update_ai_lake_database_data_source) | **PATCH** /api/v1/ailake/database/instances/{instanceId}/dataSource | (BETA) Update the data source of an AILake Database instance


# **add_ai_lake_database_data_source**
> AddDatabaseDataSourceResponse add_ai_lake_database_data_source(instance_id, add_database_data_source_request)

(BETA) Add a data source to an AILake Database instance

(BETA) Associates an additional metadata-api data source with an existing AI Lake database instance. The new data source uses the same StarRocks connection details as the primary data source.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_databases_api
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
    api_instance = ai_lake_databases_api.AILakeDatabasesApi(api_client)
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
        print("Exception when calling AILakeDatabasesApi->add_ai_lake_database_data_source: %s\n" % e)
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

# **deprovision_ai_lake_database_instance**
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} deprovision_ai_lake_database_instance(instance_id)

(BETA) Delete an existing AILake Database instance

(BETA) Deletes an existing database in the organization's AI Lake. Returns an operation-id in the operation-id header the client can use to poll for the progress.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_databases_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_databases_api.AILakeDatabasesApi(api_client)
    instance_id = "instanceId_example" # str | Database instance identifier. Accepts the database name (preferred) or UUID.
    operation_id = "operation-id_example" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Delete an existing AILake Database instance
        api_response = api_instance.deprovision_ai_lake_database_instance(instance_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeDatabasesApi->deprovision_ai_lake_database_instance: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) Delete an existing AILake Database instance
        api_response = api_instance.deprovision_ai_lake_database_instance(instance_id, operation_id=operation_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeDatabasesApi->deprovision_ai_lake_database_instance: %s\n" % e)
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
> JsonApiDocumentDatabaseInstance get_ai_lake_database_instance(instance_id)

(BETA) Get the specified AILake Database instance

(BETA) Retrieve details of the specified AI Lake database instance in the organization's AI Lake.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_databases_api
from gooddata_api_client.model.json_api_document_database_instance import JsonApiDocumentDatabaseInstance
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_databases_api.AILakeDatabasesApi(api_client)
    instance_id = "instanceId_example" # str | Database instance identifier. Accepts the database name (preferred) or UUID.

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Get the specified AILake Database instance
        api_response = api_instance.get_ai_lake_database_instance(instance_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeDatabasesApi->get_ai_lake_database_instance: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instance_id** | **str**| Database instance identifier. Accepts the database name (preferred) or UUID. |

### Return type

[**JsonApiDocumentDatabaseInstance**](JsonApiDocumentDatabaseInstance.md)

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

# **list_ai_lake_database_data_sources**
> JsonApiListDocumentDataSourceInfo list_ai_lake_database_data_sources(instance_id)

(BETA) List data sources of an AILake Database instance

(BETA) Returns data source associations for the specified AI Lake database instance.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_databases_api
from gooddata_api_client.model.json_api_list_document_data_source_info import JsonApiListDocumentDataSourceInfo
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_databases_api.AILakeDatabasesApi(api_client)
    instance_id = "instanceId_example" # str | Database instance identifier. Accepts the database name (preferred) or UUID.
    page = "0" # str | Zero-based page number. (optional) if omitted the server will use the default value of "0"
    size = "50" # str | Number of items per page. (optional) if omitted the server will use the default value of "50"
    meta_include = [
        "metaInclude_example",
    ] # [str] |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # (BETA) List data sources of an AILake Database instance
        api_response = api_instance.list_ai_lake_database_data_sources(instance_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeDatabasesApi->list_ai_lake_database_data_sources: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) List data sources of an AILake Database instance
        api_response = api_instance.list_ai_lake_database_data_sources(instance_id, page=page, size=size, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeDatabasesApi->list_ai_lake_database_data_sources: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instance_id** | **str**| Database instance identifier. Accepts the database name (preferred) or UUID. |
 **page** | **str**| Zero-based page number. | [optional] if omitted the server will use the default value of "0"
 **size** | **str**| Number of items per page. | [optional] if omitted the server will use the default value of "50"
 **meta_include** | **[str]**|  | [optional]

### Return type

[**JsonApiListDocumentDataSourceInfo**](JsonApiListDocumentDataSourceInfo.md)

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
> JsonApiListDocumentDatabaseInstance list_ai_lake_database_instances()

(BETA) List AI Lake Database instances

(BETA) Lists database instances in the organization's AI Lake.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_databases_api
from gooddata_api_client.model.json_api_list_document_database_instance import JsonApiListDocumentDatabaseInstance
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_databases_api.AILakeDatabasesApi(api_client)
    page = "0" # str | Zero-based page number. (optional) if omitted the server will use the default value of "0"
    size = "50" # str | Number of items per page. (optional) if omitted the server will use the default value of "50"
    meta_include = [
        "metaInclude_example",
    ] # [str] |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) List AI Lake Database instances
        api_response = api_instance.list_ai_lake_database_instances(page=page, size=size, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeDatabasesApi->list_ai_lake_database_instances: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **str**| Zero-based page number. | [optional] if omitted the server will use the default value of "0"
 **size** | **str**| Number of items per page. | [optional] if omitted the server will use the default value of "50"
 **meta_include** | **[str]**|  | [optional]

### Return type

[**JsonApiListDocumentDatabaseInstance**](JsonApiListDocumentDatabaseInstance.md)

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
> JsonApiListDocumentObjectStorageInfo list_ai_lake_object_storages()

(BETA) List registered AI Lake ObjectStorages

(BETA) Lists ObjectStorages registered for the organization. Use the returned `name` as `sourceStorageName` in CreatePipeTable, or pass `storageId` to the ProvisionDatabase `storageIds` list. Provider credentials are stripped — only safe descriptors (id, name, type, bucket, region, endpoint, …) are returned.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_databases_api
from gooddata_api_client.model.json_api_list_document_object_storage_info import JsonApiListDocumentObjectStorageInfo
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_databases_api.AILakeDatabasesApi(api_client)
    page = "0" # str | Zero-based page number. (optional) if omitted the server will use the default value of "0"
    size = "50" # str | Number of items per page. (optional) if omitted the server will use the default value of "50"
    meta_include = [
        "metaInclude_example",
    ] # [str] |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) List registered AI Lake ObjectStorages
        api_response = api_instance.list_ai_lake_object_storages(page=page, size=size, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeDatabasesApi->list_ai_lake_object_storages: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **str**| Zero-based page number. | [optional] if omitted the server will use the default value of "0"
 **size** | **str**| Number of items per page. | [optional] if omitted the server will use the default value of "50"
 **meta_include** | **[str]**|  | [optional]

### Return type

[**JsonApiListDocumentObjectStorageInfo**](JsonApiListDocumentObjectStorageInfo.md)

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

# **provision_ai_lake_database_instance**
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} provision_ai_lake_database_instance(provision_database_instance_request)

(BETA) Create a new AILake Database instance

(BETA) Creates a new database in the organization's AI Lake. Returns an operation-id in the operation-id header the client can use to poll for the progress.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_databases_api
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
    api_instance = ai_lake_databases_api.AILakeDatabasesApi(api_client)
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
        print("Exception when calling AILakeDatabasesApi->provision_ai_lake_database_instance: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) Create a new AILake Database instance
        api_response = api_instance.provision_ai_lake_database_instance(provision_database_instance_request, operation_id=operation_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeDatabasesApi->provision_ai_lake_database_instance: %s\n" % e)
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
from gooddata_api_client.api import ai_lake_databases_api
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
    api_instance = ai_lake_databases_api.AILakeDatabasesApi(api_client)
    instance_id = "instanceId_example" # str | Database instance identifier. Accepts the database name (preferred) or UUID.
    data_source_id = "dataSourceId_example" # str | Identifier of the data source to remove.

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Remove a data source from an AILake Database instance
        api_response = api_instance.remove_ai_lake_database_data_source(instance_id, data_source_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeDatabasesApi->remove_ai_lake_database_data_source: %s\n" % e)
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

# **update_ai_lake_database_data_source**
> UpdateDatabaseDataSourceResponse update_ai_lake_database_data_source(instance_id, update_database_data_source_request)

(BETA) Update the data source of an AILake Database instance

(BETA) Updates the data source ID and name for an existing AI Lake database instance without deleting the underlying database. Use this to recover from a wrong data source ID provisioned on an existing database instance.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_databases_api
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
    api_instance = ai_lake_databases_api.AILakeDatabasesApi(api_client)
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
        print("Exception when calling AILakeDatabasesApi->update_ai_lake_database_data_source: %s\n" % e)
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


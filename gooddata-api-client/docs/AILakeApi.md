# gooddata_api_client.AILakeApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**deprovision_ai_lake_database_instance**](AILakeApi.md#deprovision_ai_lake_database_instance) | **DELETE** /api/v1/ailake/database/instances/{instanceId} | (BETA) Delete an existing AILake Database instance
[**get_ai_lake_database_instance**](AILakeApi.md#get_ai_lake_database_instance) | **GET** /api/v1/ailake/database/instances/{instanceId} | (BETA) Get the specified AILake Database instance
[**get_ai_lake_operation**](AILakeApi.md#get_ai_lake_operation) | **GET** /api/v1/ailake/operations/{operationId} | (BETA) Get Long Running Operation details
[**list_ai_lake_database_instances**](AILakeApi.md#list_ai_lake_database_instances) | **GET** /api/v1/ailake/database/instances | (BETA) List AI Lake Database instances
[**list_ai_lake_services**](AILakeApi.md#list_ai_lake_services) | **GET** /api/v1/ailake/services | (BETA) List AI Lake services
[**provision_ai_lake_database_instance**](AILakeApi.md#provision_ai_lake_database_instance) | **POST** /api/v1/ailake/database/instances | (BETA) Create a new AILake Database instance
[**run_ai_lake_service_command**](AILakeApi.md#run_ai_lake_service_command) | **POST** /api/v1/ailake/services/{serviceId}/commands/{commandName}/run | (BETA) Run an AI Lake services command


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
    instance_id = "instanceId_example" # str | 
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
 **instance_id** | **str**|  |
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
    instance_id = "instanceId_example" # str | 

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
 **instance_id** | **str**|  |

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

# **list_ai_lake_database_instances**
> [DatabaseInstance] list_ai_lake_database_instances()

(BETA) List AI Lake Database instances

(BETA) Lists database instances in the organization's AI Lake.

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

    # example, this endpoint has no required or optional parameters
    try:
        # (BETA) List AI Lake Database instances
        api_response = api_instance.list_ai_lake_database_instances()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->list_ai_lake_database_instances: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**[DatabaseInstance]**](DatabaseInstance.md)

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

# **list_ai_lake_services**
> [ServiceInfo] list_ai_lake_services()

(BETA) List AI Lake services

(BETA) Lists services configured for the organization's AI Lake. Returns only non-sensitive fields (id, name).

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_api
from gooddata_api_client.model.service_info import ServiceInfo
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
        # (BETA) List AI Lake services
        api_response = api_instance.list_ai_lake_services()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->list_ai_lake_services: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**[ServiceInfo]**](ServiceInfo.md)

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


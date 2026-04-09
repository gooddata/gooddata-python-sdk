# gooddata_api_client.AILakeServicesOperationsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_ai_lake_operation**](AILakeServicesOperationsApi.md#get_ai_lake_operation) | **GET** /api/v1/ailake/operations/{operationId} | (BETA) Get Long Running Operation details
[**get_ai_lake_service_status**](AILakeServicesOperationsApi.md#get_ai_lake_service_status) | **GET** /api/v1/ailake/services/{serviceId}/status | (BETA) Get AI Lake service status
[**list_ai_lake_services**](AILakeServicesOperationsApi.md#list_ai_lake_services) | **GET** /api/v1/ailake/services | (BETA) List AI Lake services
[**run_ai_lake_service_command**](AILakeServicesOperationsApi.md#run_ai_lake_service_command) | **POST** /api/v1/ailake/services/{serviceId}/commands/{commandName}/run | (BETA) Run an AI Lake services command


# **get_ai_lake_operation**
> GetAiLakeOperation200Response get_ai_lake_operation(operation_id)

(BETA) Get Long Running Operation details

(BETA) Retrieves details of a Long Running Operation specified by the operation-id.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_services_operations_api
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
    api_instance = ai_lake_services_operations_api.AILakeServicesOperationsApi(api_client)
    operation_id = "e9fd5d74-8a1b-46bd-ac60-bd91e9206897" # str | Operation ID

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Get Long Running Operation details
        api_response = api_instance.get_ai_lake_operation(operation_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeServicesOperationsApi->get_ai_lake_operation: %s\n" % e)
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

# **get_ai_lake_service_status**
> GetServiceStatusResponse get_ai_lake_service_status(service_id)

(BETA) Get AI Lake service status

(BETA) Returns the status of a service in the organization's AI Lake. The status is controller-specific (e.g., available commands, readiness).

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_services_operations_api
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
    api_instance = ai_lake_services_operations_api.AILakeServicesOperationsApi(api_client)
    service_id = "serviceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Get AI Lake service status
        api_response = api_instance.get_ai_lake_service_status(service_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeServicesOperationsApi->get_ai_lake_service_status: %s\n" % e)
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

# **list_ai_lake_services**
> ListServicesResponse list_ai_lake_services()

(BETA) List AI Lake services

(BETA) Lists services configured for the organization's AI Lake. Returns only non-sensitive fields (id, name). Supports paging via size and offset query parameters. Use metaInclude=page to get total count.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_services_operations_api
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
    api_instance = ai_lake_services_operations_api.AILakeServicesOperationsApi(api_client)
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
        print("Exception when calling AILakeServicesOperationsApi->list_ai_lake_services: %s\n" % e)
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

# **run_ai_lake_service_command**
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} run_ai_lake_service_command(service_id, command_name, run_service_command_request)

(BETA) Run an AI Lake services command

(BETA) Runs a specific AI Lake service command.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ai_lake_services_operations_api
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
    api_instance = ai_lake_services_operations_api.AILakeServicesOperationsApi(api_client)
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
        print("Exception when calling AILakeServicesOperationsApi->run_ai_lake_service_command: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) Run an AI Lake services command
        api_response = api_instance.run_ai_lake_service_command(service_id, command_name, run_service_command_request, operation_id=operation_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeServicesOperationsApi->run_ai_lake_service_command: %s\n" % e)
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


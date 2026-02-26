<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.ai_lake_api.AILakeApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**deprovision_ai_lake_database_instance**](#deprovision_ai_lake_database_instance) | **delete** /api/v1/ailake/database/instances/{instanceId} | (BETA) Delete an existing AILake Database instance
[**get_ai_lake_database_instance**](#get_ai_lake_database_instance) | **get** /api/v1/ailake/database/instances/{instanceId} | (BETA) Get the specified AILake Database instance
[**get_ai_lake_operation**](#get_ai_lake_operation) | **get** /api/v1/ailake/operations/{operationId} | (BETA) Get Long Running Operation details
[**list_ai_lake_database_instances**](#list_ai_lake_database_instances) | **get** /api/v1/ailake/database/instances | (BETA) List AI Lake Database instances
[**list_ai_lake_services**](#list_ai_lake_services) | **get** /api/v1/ailake/services | (BETA) List AI Lake services
[**provision_ai_lake_database_instance**](#provision_ai_lake_database_instance) | **post** /api/v1/ailake/database/instances | (BETA) Create a new AILake Database instance
[**run_ai_lake_service_command**](#run_ai_lake_service_command) | **post** /api/v1/ailake/services/{serviceId}/commands/{commandName}/run | (BETA) Run an AI Lake services command

# **deprovision_ai_lake_database_instance**
<a id="deprovision_ai_lake_database_instance"></a>
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} deprovision_ai_lake_database_instance(instance_id)

(BETA) Delete an existing AILake Database instance

(BETA) Deletes an existing database in the organization's AI Lake. Returns an operation-id in the operation-id header the client can use to poll for the progress.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import ai_lake_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_api.AILakeApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'instanceId': "instanceId_example",
    }
    header_params = {
    }
    try:
        # (BETA) Delete an existing AILake Database instance
        api_response = api_instance.deprovision_ai_lake_database_instance(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->deprovision_ai_lake_database_instance: %s\n" % e)

    # example passing only optional values
    path_params = {
        'instanceId': "instanceId_example",
    }
    header_params = {
        'operation-id': "operation-id_example",
    }
    try:
        # (BETA) Delete an existing AILake Database instance
        api_response = api_instance.deprovision_ai_lake_database_instance(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->deprovision_ai_lake_database_instance: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
header_params | RequestHeaderParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
operation-id | OperationIdSchema | | optional

# OperationIdSchema

Operation ID to use for polling.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Operation ID to use for polling. | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
instanceId | InstanceIdSchema | | 

# InstanceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
202 | [ApiResponseFor202](#deprovision_ai_lake_database_instance.ApiResponseFor202) | Accepted

#### deprovision_ai_lake_database_instance.ApiResponseFor202
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor202ResponseBodyApplicationJson, ] |  |
headers | ResponseHeadersFor202 |  |

# SchemaFor202ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 
#### ResponseHeadersFor202

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
operation-id | OperationIdSchema | | 
operation-location | OperationLocationSchema | | 

# OperationIdSchema

Operation ID to use for polling.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Operation ID to use for polling. | 

# OperationLocationSchema

Operation location URL that can be used for polling.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Operation location URL that can be used for polling. | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_ai_lake_database_instance**
<a id="get_ai_lake_database_instance"></a>
> DatabaseInstance get_ai_lake_database_instance(instance_id)

(BETA) Get the specified AILake Database instance

(BETA) Retrieve details of the specified AI Lake database instance in the organization's AI Lake.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import ai_lake_api
from gooddata_api_client.model.database_instance import DatabaseInstance
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_api.AILakeApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'instanceId': "instanceId_example",
    }
    try:
        # (BETA) Get the specified AILake Database instance
        api_response = api_instance.get_ai_lake_database_instance(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->get_ai_lake_database_instance: %s\n" % e)
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
instanceId | InstanceIdSchema | | 

# InstanceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_ai_lake_database_instance.ApiResponseFor200) | AI Lake database instance successfully retrieved

#### get_ai_lake_database_instance.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DatabaseInstance**](../../models/DatabaseInstance.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_ai_lake_operation**
<a id="get_ai_lake_operation"></a>
> bool, date, datetime, dict, float, int, list, str, none_type get_ai_lake_operation(operation_id)

(BETA) Get Long Running Operation details

(BETA) Retrieves details of a Long Running Operation specified by the operation-id.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import ai_lake_api
from gooddata_api_client.model.failed_operation import FailedOperation
from gooddata_api_client.model.pending_operation import PendingOperation
from gooddata_api_client.model.succeeded_operation import SucceededOperation
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_api.AILakeApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'operationId': "e9fd5d74-8a1b-46bd-ac60-bd91e9206897",
    }
    try:
        # (BETA) Get Long Running Operation details
        api_response = api_instance.get_ai_lake_operation(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->get_ai_lake_operation: %s\n" % e)
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
operationId | OperationIdSchema | | 

# OperationIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_ai_lake_operation.ApiResponseFor200) | AI Lake Long Running Operation details successfully retrieved

#### get_ai_lake_operation.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | 

### Composed Schemas (allOf/anyOf/oneOf/not)
#### oneOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[FailedOperation]({{complexTypePrefix}}FailedOperation.md) | [**FailedOperation**]({{complexTypePrefix}}FailedOperation.md) | [**FailedOperation**]({{complexTypePrefix}}FailedOperation.md) |  | 
[PendingOperation]({{complexTypePrefix}}PendingOperation.md) | [**PendingOperation**]({{complexTypePrefix}}PendingOperation.md) | [**PendingOperation**]({{complexTypePrefix}}PendingOperation.md) |  | 
[SucceededOperation]({{complexTypePrefix}}SucceededOperation.md) | [**SucceededOperation**]({{complexTypePrefix}}SucceededOperation.md) | [**SucceededOperation**]({{complexTypePrefix}}SucceededOperation.md) |  | 

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **list_ai_lake_database_instances**
<a id="list_ai_lake_database_instances"></a>
> [DatabaseInstance] list_ai_lake_database_instances()

(BETA) List AI Lake Database instances

(BETA) Lists database instances in the organization's AI Lake.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import ai_lake_api
from gooddata_api_client.model.database_instance import DatabaseInstance
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
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

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#list_ai_lake_database_instances.ApiResponseFor200) | AI Lake database instances successfully retrieved

#### list_ai_lake_database_instances.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DatabaseInstance**]({{complexTypePrefix}}DatabaseInstance.md) | [**DatabaseInstance**]({{complexTypePrefix}}DatabaseInstance.md) | [**DatabaseInstance**]({{complexTypePrefix}}DatabaseInstance.md) |  | 

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **list_ai_lake_services**
<a id="list_ai_lake_services"></a>
> [ServiceInfo] list_ai_lake_services()

(BETA) List AI Lake services

(BETA) Lists services configured for the organization's AI Lake. Returns only non-sensitive fields (id, name).

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import ai_lake_api
from gooddata_api_client.model.service_info import ServiceInfo
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
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

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#list_ai_lake_services.ApiResponseFor200) | AI Lake services successfully retrieved

#### list_ai_lake_services.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**ServiceInfo**]({{complexTypePrefix}}ServiceInfo.md) | [**ServiceInfo**]({{complexTypePrefix}}ServiceInfo.md) | [**ServiceInfo**]({{complexTypePrefix}}ServiceInfo.md) |  | 

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **provision_ai_lake_database_instance**
<a id="provision_ai_lake_database_instance"></a>
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} provision_ai_lake_database_instance(provision_database_instance_request)

(BETA) Create a new AILake Database instance

(BETA) Creates a new database in the organization's AI Lake. Returns an operation-id in the operation-id header the client can use to poll for the progress.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import ai_lake_api
from gooddata_api_client.model.provision_database_instance_request import ProvisionDatabaseInstanceRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_api.AILakeApi(api_client)

    # example passing only required values which don't have defaults set
    header_params = {
    }
    body = ProvisionDatabaseInstanceRequest(
        name="name_example",
        storage_ids=[
            "storage_ids_example"
        ],
    )
    try:
        # (BETA) Create a new AILake Database instance
        api_response = api_instance.provision_ai_lake_database_instance(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->provision_ai_lake_database_instance: %s\n" % e)

    # example passing only optional values
    header_params = {
        'operation-id': "operation-id_example",
    }
    body = ProvisionDatabaseInstanceRequest(
        name="name_example",
        storage_ids=[
            "storage_ids_example"
        ],
    )
    try:
        # (BETA) Create a new AILake Database instance
        api_response = api_instance.provision_ai_lake_database_instance(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->provision_ai_lake_database_instance: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
header_params | RequestHeaderParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ProvisionDatabaseInstanceRequest**](../../models/ProvisionDatabaseInstanceRequest.md) |  | 


### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
operation-id | OperationIdSchema | | optional

# OperationIdSchema

Operation ID to use for polling.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Operation ID to use for polling. | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
202 | [ApiResponseFor202](#provision_ai_lake_database_instance.ApiResponseFor202) | Accepted

#### provision_ai_lake_database_instance.ApiResponseFor202
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor202ResponseBodyApplicationJson, ] |  |
headers | ResponseHeadersFor202 |  |

# SchemaFor202ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 
#### ResponseHeadersFor202

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
operation-id | OperationIdSchema | | 
operation-location | OperationLocationSchema | | 

# OperationIdSchema

Operation ID to use for polling.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Operation ID to use for polling. | 

# OperationLocationSchema

Operation location URL that can be used for polling.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Operation location URL that can be used for polling. | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **run_ai_lake_service_command**
<a id="run_ai_lake_service_command"></a>
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} run_ai_lake_service_command(service_idcommand_namerun_service_command_request)

(BETA) Run an AI Lake services command

(BETA) Runs a specific AI Lake service command.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import ai_lake_api
from gooddata_api_client.model.run_service_command_request import RunServiceCommandRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ai_lake_api.AILakeApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'serviceId': "serviceId_example",
        'commandName': "commandName_example",
    }
    header_params = {
    }
    body = RunServiceCommandRequest(
        context=dict(
            "key": "key_example",
        ),
        payload=JsonNode(),
    )
    try:
        # (BETA) Run an AI Lake services command
        api_response = api_instance.run_ai_lake_service_command(
            path_params=path_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->run_ai_lake_service_command: %s\n" % e)

    # example passing only optional values
    path_params = {
        'serviceId': "serviceId_example",
        'commandName': "commandName_example",
    }
    header_params = {
        'operation-id': "operation-id_example",
    }
    body = RunServiceCommandRequest(
        context=dict(
            "key": "key_example",
        ),
        payload=JsonNode(),
    )
    try:
        # (BETA) Run an AI Lake services command
        api_response = api_instance.run_ai_lake_service_command(
            path_params=path_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AILakeApi->run_ai_lake_service_command: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
header_params | RequestHeaderParams | |
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
[**RunServiceCommandRequest**](../../models/RunServiceCommandRequest.md) |  | 


### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
operation-id | OperationIdSchema | | optional

# OperationIdSchema

Operation ID to use for polling.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Operation ID to use for polling. | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
serviceId | ServiceIdSchema | | 
commandName | CommandNameSchema | | 

# ServiceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# CommandNameSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
202 | [ApiResponseFor202](#run_ai_lake_service_command.ApiResponseFor202) | Accepted

#### run_ai_lake_service_command.ApiResponseFor202
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor202ResponseBodyApplicationJson, ] |  |
headers | ResponseHeadersFor202 |  |

# SchemaFor202ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 
#### ResponseHeadersFor202

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
operation-id | OperationIdSchema | | 
operation-location | OperationLocationSchema | | 

# OperationIdSchema

Operation ID to use for polling.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Operation ID to use for polling. | 

# OperationLocationSchema

Operation location URL that can be used for polling.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Operation location URL that can be used for polling. | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


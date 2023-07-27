<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.test_connection_api.TestConnectionApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**test_data_source**](#test_data_source) | **post** /api/v1/actions/dataSources/{dataSourceId}/test | Test data source connection by data source id
[**test_data_source_definition**](#test_data_source_definition) | **post** /api/v1/actions/dataSource/test | Test connection by data source definition

# **test_data_source**
<a id="test_data_source"></a>
> TestResponse test_data_source(data_source_idtest_request)

Test data source connection by data source id

Test if it is possible to connect to a database using an existing data source definition.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import test_connection_api
from gooddata_api_client.model.test_response import TestResponse
from gooddata_api_client.model.test_request import TestRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = test_connection_api.TestConnectionApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'dataSourceId': "myPostgres",
    }
    body = TestRequest(
        cache_path=[
            "cache_path_example"
        ],
        enable_caching=False,
        parameters=[
            DataSourceParameter(
                name="name_example",
                value="value_example",
            )
        ],
        password="admin123",
        schema="public",
        token="token_example",
        url="jdbc:postgresql://localhost:5432/db_name",
        username="dbadmin",
    )
    try:
        # Test data source connection by data source id
        api_response = api_instance.test_data_source(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling TestConnectionApi->test_data_source: %s\n" % e)
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
[**TestRequest**](../../models/TestRequest.md) |  | 


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
200 | [ApiResponseFor200](#test_data_source.ApiResponseFor200) | The result of the test of a data source connection.

#### test_data_source.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**TestResponse**](../../models/TestResponse.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **test_data_source_definition**
<a id="test_data_source_definition"></a>
> TestResponse test_data_source_definition(test_definition_request)

Test connection by data source definition

Test if it is possible to connect to a database using a connection provided by the data source definition in the request body.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import test_connection_api
from gooddata_api_client.model.test_response import TestResponse
from gooddata_api_client.model.test_definition_request import TestDefinitionRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = test_connection_api.TestConnectionApi(api_client)

    # example passing only required values which don't have defaults set
    body = TestDefinitionRequest(
        parameters=[
            DataSourceParameter(
                name="name_example",
                value="value_example",
            )
        ],
        password="admin123",
        schema="public",
        token="token_example",
        type="POSTGRESQL",
        url="jdbc:postgresql://localhost:5432/db_name",
        username="dbadmin",
    )
    try:
        # Test connection by data source definition
        api_response = api_instance.test_data_source_definition(
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling TestConnectionApi->test_data_source_definition: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**TestDefinitionRequest**](../../models/TestDefinitionRequest.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#test_data_source_definition.ApiResponseFor200) | The result of the test of a data source connection.

#### test_data_source_definition.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**TestResponse**](../../models/TestResponse.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


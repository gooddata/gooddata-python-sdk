# gooddata_api_client.TestConnectionApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**test_data_source**](TestConnectionApi.md#test_data_source) | **POST** /api/v1/actions/dataSources/{dataSourceId}/test | Test data source connection by data source id
[**test_data_source_definition**](TestConnectionApi.md#test_data_source_definition) | **POST** /api/v1/actions/dataSource/test | Test connection by data source definition


# **test_data_source**
> TestResponse test_data_source(data_source_id, test_request)

Test data source connection by data source id

Test if it is possible to connect to a database using an existing data source definition.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import test_connection_api
from gooddata_api_client.model.test_response import TestResponse
from gooddata_api_client.model.test_request import TestRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = test_connection_api.TestConnectionApi(api_client)
    data_source_id = "myPostgres" # str | Data source id
    test_request = TestRequest(
        client_id="client_id_example",
        client_secret="client_secret_example",
        parameters=[
            DataSourceParameter(
                name="name_example",
                value="value_example",
            ),
        ],
        password="admin123",
        private_key="private_key_example",
        private_key_passphrase="private_key_passphrase_example",
        schema="public",
        token="token_example",
        url="jdbc:postgresql://localhost:5432/db_name",
        username="dbadmin",
    ) # TestRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Test data source connection by data source id
        api_response = api_instance.test_data_source(data_source_id, test_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling TestConnectionApi->test_data_source: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| Data source id |
 **test_request** | [**TestRequest**](TestRequest.md)|  |

### Return type

[**TestResponse**](TestResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The result of the test of a data source connection. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_data_source_definition**
> TestResponse test_data_source_definition(test_definition_request)

Test connection by data source definition

Test if it is possible to connect to a database using a connection provided by the data source definition in the request body.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import test_connection_api
from gooddata_api_client.model.test_response import TestResponse
from gooddata_api_client.model.test_definition_request import TestDefinitionRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = test_connection_api.TestConnectionApi(api_client)
    test_definition_request = TestDefinitionRequest(
        client_id="client_id_example",
        client_secret="client_secret_example",
        parameters=[
            DataSourceParameter(
                name="name_example",
                value="value_example",
            ),
        ],
        password="admin123",
        private_key="private_key_example",
        private_key_passphrase="private_key_passphrase_example",
        schema="public",
        token="token_example",
        type="POSTGRESQL",
        url="jdbc:postgresql://localhost:5432/db_name",
        username="dbadmin",
    ) # TestDefinitionRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Test connection by data source definition
        api_response = api_instance.test_data_source_definition(test_definition_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling TestConnectionApi->test_data_source_definition: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_definition_request** | [**TestDefinitionRequest**](TestDefinitionRequest.md)|  |

### Return type

[**TestResponse**](TestResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The result of the test of a data source connection. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


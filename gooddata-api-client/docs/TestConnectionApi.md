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
import gooddata_api_client
from gooddata_api_client.models.test_request import TestRequest
from gooddata_api_client.models.test_response import TestResponse
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.TestConnectionApi(api_client)
    data_source_id = 'myPostgres' # str | Data source id
    test_request = gooddata_api_client.TestRequest() # TestRequest | 

    try:
        # Test data source connection by data source id
        api_response = api_instance.test_data_source(data_source_id, test_request)
        print("The response of TestConnectionApi->test_data_source:\n")
        pprint(api_response)
    except Exception as e:
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
import gooddata_api_client
from gooddata_api_client.models.test_definition_request import TestDefinitionRequest
from gooddata_api_client.models.test_response import TestResponse
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.TestConnectionApi(api_client)
    test_definition_request = gooddata_api_client.TestDefinitionRequest() # TestDefinitionRequest | 

    try:
        # Test connection by data source definition
        api_response = api_instance.test_data_source_definition(test_definition_request)
        print("The response of TestConnectionApi->test_data_source_definition:\n")
        pprint(api_response)
    except Exception as e:
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


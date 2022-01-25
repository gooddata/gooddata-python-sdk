# gooddata_scan_client.ActionsApi

All URIs are relative to *http://gooddata-cn-ce:3000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**scan_pdm**](ActionsApi.md#scan_pdm) | **POST** /api/actions/dataSources/{dataSourceId}/scan | 
[**schemata**](ActionsApi.md#schemata) | **GET** /api/actions/dataSources/{dataSourceId}/scanSchemata | 
[**test_data_source**](ActionsApi.md#test_data_source) | **POST** /api/actions/dataSources/{dataSourceId}/test | Test data source connection
[**test_data_source_definition**](ActionsApi.md#test_data_source_definition) | **POST** /api/actions/dataSource/test | Test connection by data source definition


# **scan_pdm**
> ScanResultPdm scan_pdm(data_source_id, scan_request)



### Example


```python
import time
import gooddata_scan_client
from gooddata_scan_client.api import actions_api
from gooddata_scan_client.model.scan_result_pdm import ScanResultPdm
from gooddata_scan_client.model.scan_request import ScanRequest
from pprint import pprint
# Defining the host is optional and defaults to http://gooddata-cn-ce:3000
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_scan_client.Configuration(
    host = "http://gooddata-cn-ce:3000"
)


# Enter a context with an instance of the API client
with gooddata_scan_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    data_source_id = "myPostgres" # str | Data source id
    scan_request = ScanRequest(
        separator="__",
        scan_tables=True,
        scan_views=True,
        schemata=[
            "[ "tpch", "demo" ].",
        ],
        table_prefix="out_table",
        view_prefix="out_view",
    ) # ScanRequest | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.scan_pdm(data_source_id, scan_request)
        pprint(api_response)
    except gooddata_scan_client.ApiException as e:
        print("Exception when calling ActionsApi->scan_pdm: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| Data source id |
 **scan_request** | [**ScanRequest**](ScanRequest.md)|  |

### Return type

[**ScanResultPdm**](ScanResultPdm.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **schemata**
> DataSourceSchemata schemata(data_source_id)



### Example


```python
import time
import gooddata_scan_client
from gooddata_scan_client.api import actions_api
from gooddata_scan_client.model.data_source_schemata import DataSourceSchemata
from pprint import pprint
# Defining the host is optional and defaults to http://gooddata-cn-ce:3000
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_scan_client.Configuration(
    host = "http://gooddata-cn-ce:3000"
)


# Enter a context with an instance of the API client
with gooddata_scan_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    data_source_id = "myPostgres" # str | Data source id

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.schemata(data_source_id)
        pprint(api_response)
    except gooddata_scan_client.ApiException as e:
        print("Exception when calling ActionsApi->schemata: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| Data source id |

### Return type

[**DataSourceSchemata**](DataSourceSchemata.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_data_source**
> TestResponse test_data_source(data_source_id, body)

Test data source connection

Test if it is possible to connect to database using connection provided by data source.

### Example


```python
import time
import gooddata_scan_client
from gooddata_scan_client.api import actions_api
from gooddata_scan_client.model.test_response import TestResponse
from pprint import pprint
# Defining the host is optional and defaults to http://gooddata-cn-ce:3000
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_scan_client.Configuration(
    host = "http://gooddata-cn-ce:3000"
)


# Enter a context with an instance of the API client
with gooddata_scan_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    data_source_id = "ds-02" # str | Data source id
    body = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | 

    # example passing only required values which don't have defaults set
    try:
        # Test data source connection
        api_response = api_instance.test_data_source(data_source_id, body)
        pprint(api_response)
    except gooddata_scan_client.ApiException as e:
        print("Exception when calling ActionsApi->test_data_source: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| Data source id |
 **body** | **{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**|  |

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
**200** | Result of test. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_data_source_definition**
> TestResponse test_data_source_definition(test_definition_request)

Test connection by data source definition

Test if it is possible to connect to database using connection provided by data source definition.

### Example


```python
import time
import gooddata_scan_client
from gooddata_scan_client.api import actions_api
from gooddata_scan_client.model.test_definition_request import TestDefinitionRequest
from gooddata_scan_client.model.test_response import TestResponse
from pprint import pprint
# Defining the host is optional and defaults to http://gooddata-cn-ce:3000
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_scan_client.Configuration(
    host = "http://gooddata-cn-ce:3000"
)


# Enter a context with an instance of the API client
with gooddata_scan_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    test_definition_request = TestDefinitionRequest(
        type="POSTGRESQL",
        url="jdbc:postgresql://localhost:5432/db_name",
        schema="public",
        username="dbadmin",
        password="admin123",
        token="token_example",
    ) # TestDefinitionRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Test connection by data source definition
        api_response = api_instance.test_data_source_definition(test_definition_request)
        pprint(api_response)
    except gooddata_scan_client.ApiException as e:
        print("Exception when calling ActionsApi->test_data_source_definition: %s\n" % e)
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
**200** | Result of test. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


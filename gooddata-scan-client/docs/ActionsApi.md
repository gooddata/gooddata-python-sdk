# gooddata_scan_client.ActionsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_data_source_schemata**](ActionsApi.md#get_data_source_schemata) | **GET** /api/v1/actions/dataSources/{dataSourceId}/scanSchemata | Get a list of schema names of a database
[**scan_data_source**](ActionsApi.md#scan_data_source) | **POST** /api/v1/actions/dataSources/{dataSourceId}/scan | Scan a database to get a physical data model (PDM)
[**test_data_source**](ActionsApi.md#test_data_source) | **POST** /api/v1/actions/dataSources/{dataSourceId}/test | Test data source connection by data source id
[**test_data_source_definition**](ActionsApi.md#test_data_source_definition) | **POST** /api/v1/actions/dataSource/test | Test connection by data source definition


# **get_data_source_schemata**
> DataSourceSchemata get_data_source_schemata(data_source_id)

Get a list of schema names of a database

It scans a database and reads metadata. The result of the request contains a list of schema names of a database.

### Example


```python
import time
import gooddata_scan_client
from gooddata_scan_client.api import actions_api
from gooddata_scan_client.model.data_source_schemata import DataSourceSchemata
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_scan_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_scan_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    data_source_id = "myPostgres" # str | Data source id

    # example passing only required values which don't have defaults set
    try:
        # Get a list of schema names of a database
        api_response = api_instance.get_data_source_schemata(data_source_id)
        pprint(api_response)
    except gooddata_scan_client.ApiException as e:
        print("Exception when calling ActionsApi->get_data_source_schemata: %s\n" % e)
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
**200** | The result of the scan schemata |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **scan_data_source**
> ScanResultPdm scan_data_source(data_source_id, scan_request)

Scan a database to get a physical data model (PDM)

It scans a database and transforms its metadata to a declarative definition of the physical data model (PDM). The result of the request contains the mentioned physical data model (PDM) of a database within warning, for example, about unsupported columns.

### Example


```python
import time
import gooddata_scan_client
from gooddata_scan_client.api import actions_api
from gooddata_scan_client.model.scan_result_pdm import ScanResultPdm
from gooddata_scan_client.model.scan_request import ScanRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_scan_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_scan_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    data_source_id = "myPostgres" # str | Data source id
    scan_request = ScanRequest(
        scan_tables=True,
        scan_views=True,
        schemata=["tpch","demo"],
        separator="__",
        table_prefix="out_table",
        view_prefix="out_view",
    ) # ScanRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Scan a database to get a physical data model (PDM)
        api_response = api_instance.scan_data_source(data_source_id, scan_request)
        pprint(api_response)
    except gooddata_scan_client.ApiException as e:
        print("Exception when calling ActionsApi->scan_data_source: %s\n" % e)
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
**200** | The result of the scan. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_data_source**
> TestResponse test_data_source(data_source_id, test_request)

Test data source connection by data source id

Test if it is possible to connect to a database using an existing data source definition.

### Example


```python
import time
import gooddata_scan_client
from gooddata_scan_client.api import actions_api
from gooddata_scan_client.model.test_request import TestRequest
from gooddata_scan_client.model.test_response import TestResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_scan_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_scan_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    data_source_id = "myPostgres" # str | Data source id
    test_request = TestRequest(
        cache_path=[
            "cache_path_example",
        ],
        enable_caching=False,
        parameters=[
            DataSourceParameter(
                name="name_example",
                value="value_example",
            ),
        ],
        password="admin123",
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
    except gooddata_scan_client.ApiException as e:
        print("Exception when calling ActionsApi->test_data_source: %s\n" % e)
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
import gooddata_scan_client
from gooddata_scan_client.api import actions_api
from gooddata_scan_client.model.test_definition_request import TestDefinitionRequest
from gooddata_scan_client.model.test_response import TestResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_scan_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_scan_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    test_definition_request = TestDefinitionRequest(
        parameters=[
            DataSourceParameter(
                name="name_example",
                value="value_example",
            ),
        ],
        password="admin123",
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
**200** | The result of the test of a data source connection. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


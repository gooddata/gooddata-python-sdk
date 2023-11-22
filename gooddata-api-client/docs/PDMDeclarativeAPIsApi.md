# gooddata_api_client.PDMDeclarativeAPIsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_pdm_layout**](PDMDeclarativeAPIsApi.md#get_pdm_layout) | **GET** /api/v1/layout/dataSources/{dataSourceId}/physicalModel | Get data source physical model layout
[**set_pdm_layout**](PDMDeclarativeAPIsApi.md#set_pdm_layout) | **PUT** /api/v1/layout/dataSources/{dataSourceId}/physicalModel | Set data source physical model layout


# **get_pdm_layout**
> DeclarativePdm get_pdm_layout(data_source_id)

Get data source physical model layout

Retrieve complete layout of tables with their columns

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import pdm_declarative_apis_api
from gooddata_api_client.model.declarative_pdm import DeclarativePdm
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = pdm_declarative_apis_api.PDMDeclarativeAPIsApi(api_client)
    data_source_id = "dataSourceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get data source physical model layout
        api_response = api_instance.get_pdm_layout(data_source_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PDMDeclarativeAPIsApi->get_pdm_layout: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  |

### Return type

[**DeclarativePdm**](DeclarativePdm.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved data source physical mode layout. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_pdm_layout**
> set_pdm_layout(data_source_id, declarative_pdm)

Set data source physical model layout

Sets complete layout of tables with their columns under corresponding Data Source.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import pdm_declarative_apis_api
from gooddata_api_client.model.declarative_pdm import DeclarativePdm
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = pdm_declarative_apis_api.PDMDeclarativeAPIsApi(api_client)
    data_source_id = "dataSourceId_example" # str | 
    declarative_pdm = DeclarativePdm(
        pdm=DeclarativeTables(
            tables=[
                DeclarativeTable(
                    columns=[
                        DeclarativeColumn(
                            data_type="INT",
                            is_primary_key=True,
                            name="customer_id",
                            referenced_table_column="customer_id",
                            referenced_table_id="customers",
                        ),
                    ],
                    id="customers",
                    name_prefix="out_gooddata",
                    path=["table_schema","table_name"],
                    type="TABLE",
                ),
            ],
        ),
    ) # DeclarativePdm | 

    # example passing only required values which don't have defaults set
    try:
        # Set data source physical model layout
        api_instance.set_pdm_layout(data_source_id, declarative_pdm)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PDMDeclarativeAPIsApi->set_pdm_layout: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  |
 **declarative_pdm** | [**DeclarativePdm**](DeclarativePdm.md)|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Data source physical mode layout set successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


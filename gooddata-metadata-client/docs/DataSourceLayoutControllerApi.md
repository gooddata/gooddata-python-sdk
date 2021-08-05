# gooddata_metadata_client.DataSourceLayoutControllerApi

All URIs are relative to *https://staging.anywhere.gooddata.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_pdm_layout**](DataSourceLayoutControllerApi.md#get_pdm_layout) | **GET** /api/layout/dataSources/{dataSourceId}/physicalModel | Get data source physical model layout
[**set_pdm_layout**](DataSourceLayoutControllerApi.md#set_pdm_layout) | **PUT** /api/layout/dataSources/{dataSourceId}/physicalModel | Set data source physical model layout


# **get_pdm_layout**
> DeclarativePdm get_pdm_layout(data_source_id)

Get data source physical model layout

Retrieve complete layout of tables with their columns

### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import data_source_layout_controller_api
from gooddata_metadata_client.model.declarative_pdm import DeclarativePdm
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_source_layout_controller_api.DataSourceLayoutControllerApi(api_client)
    data_source_id = "dataSourceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get data source physical model layout
        api_response = api_instance.get_pdm_layout(data_source_id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling DataSourceLayoutControllerApi->get_pdm_layout: %s\n" % e)
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
 - **Accept**: */*


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
import gooddata_metadata_client
from gooddata_metadata_client.api import data_source_layout_controller_api
from gooddata_metadata_client.model.declarative_pdm import DeclarativePdm
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_source_layout_controller_api.DataSourceLayoutControllerApi(api_client)
    data_source_id = "dataSourceId_example" # str | 
    declarative_pdm = DeclarativePdm(
        pdm=DeclarativeTables(
            tables=[
                DeclarativeTable(
                    id="customers",
                    path=["table_schema","table_name"],
                    type="VIEW",
                    columns=[
                        DeclarativeColumn(
                            name="customer_id",
                            data_type="INT",
                            is_primary_key=True,
                            referenced_table_id="customers",
                            referenced_table_column="customer_id",
                        ),
                    ],
                ),
            ],
        ),
    ) # DeclarativePdm | 

    # example passing only required values which don't have defaults set
    try:
        # Set data source physical model layout
        api_instance.set_pdm_layout(data_source_id, declarative_pdm)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling DataSourceLayoutControllerApi->set_pdm_layout: %s\n" % e)
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


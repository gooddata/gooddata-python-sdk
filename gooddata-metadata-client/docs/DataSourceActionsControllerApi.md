# gooddata_metadata_client.DataSourceActionsControllerApi

All URIs are relative to *https://staging.anywhere.gooddata.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**generate_logical_model**](DataSourceActionsControllerApi.md#generate_logical_model) | **POST** /api/actions/dataSources/{dataSourceId}/generateLogicalModel | Generate LDM from PDM
[**register_upload_notification**](DataSourceActionsControllerApi.md#register_upload_notification) | **POST** /api/actions/dataSources/{dataSourceId}/uploadNotification | Register an upload notification


# **generate_logical_model**
> DeclarativeModel generate_logical_model(data_source_id, generate_ldm_request)

Generate LDM from PDM

Generate LDM from PDM stored in data source.

### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import data_source_actions_controller_api
from gooddata_metadata_client.model.declarative_model import DeclarativeModel
from gooddata_metadata_client.model.generate_ldm_request import GenerateLdmRequest
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_source_actions_controller_api.DataSourceActionsControllerApi(api_client)
    data_source_id = "dataSourceId_example" # str | 
    generate_ldm_request = GenerateLdmRequest(
        separator="__",
        table_prefix="out_table",
        view_prefix="out_view",
        primary_label_prefix="pl",
        secondary_label_prefix="sl",
        fact_prefix="f",
        date_granularities="all",
        grain_prefix="g",
        reference_prefix="r",
        grain_reference_prefix="gr",
        denorm_prefix="dr",
        wdf_prefix="wdf",
    ) # GenerateLdmRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Generate LDM from PDM
        api_response = api_instance.generate_logical_model(data_source_id, generate_ldm_request)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling DataSourceActionsControllerApi->generate_logical_model: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  |
 **generate_ldm_request** | [**GenerateLdmRequest**](GenerateLdmRequest.md)|  |

### Return type

[**DeclarativeModel**](DeclarativeModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | LDM generated successfully. |  -  |
**404** | Data source with given name does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **register_upload_notification**
> register_upload_notification(data_source_id)

Register an upload notification

Notification sets up all reports to be computed again with new data.

### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import data_source_actions_controller_api
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_source_actions_controller_api.DataSourceActionsControllerApi(api_client)
    data_source_id = "dataSourceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Register an upload notification
        api_instance.register_upload_notification(data_source_id)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling DataSourceActionsControllerApi->register_upload_notification: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | An upload notification has been successfully registered. |  -  |
**404** | Data source with given name does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


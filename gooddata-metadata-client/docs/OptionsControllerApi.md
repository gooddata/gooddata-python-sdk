# gooddata_metadata_client.OptionsControllerApi

All URIs are relative to *https://staging.anywhere.gooddata.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_all_options**](OptionsControllerApi.md#get_all_options) | **GET** /api/options | Links for all configuration options
[**get_data_source_drivers**](OptionsControllerApi.md#get_data_source_drivers) | **GET** /api/options/availableDrivers | Get all available data source drivers


# **get_all_options**
> get_all_options()

Links for all configuration options

Retrieves links for all options for different configurations.

### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import options_controller_api
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = options_controller_api.OptionsControllerApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Links for all configuration options
        api_instance.get_all_options()
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OptionsControllerApi->get_all_options: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Links for all configuration options. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_data_source_drivers**
> get_data_source_drivers()

Get all available data source drivers

Retrieves a list of all supported data sources along with information about the used drivers.

### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import options_controller_api
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = options_controller_api.OptionsControllerApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get all available data source drivers
        api_instance.get_data_source_drivers()
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OptionsControllerApi->get_data_source_drivers: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of all available data source drivers. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


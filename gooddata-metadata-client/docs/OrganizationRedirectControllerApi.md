# gooddata_metadata_client.OrganizationRedirectControllerApi

All URIs are relative to *https://staging.anywhere.gooddata.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_organization**](OrganizationRedirectControllerApi.md#get_organization) | **GET** /api/entities/organization | Get current organization info


# **get_organization**
> get_organization()

Get current organization info

Gets a basic information about organization.

### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_redirect_controller_api
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_redirect_controller_api.OrganizationRedirectControllerApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get current organization info
        api_instance.get_organization()
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationRedirectControllerApi->get_organization: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

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
**302** | Redirect to entity URI. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


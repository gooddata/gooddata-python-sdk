# gooddata_api_client.UserAuthorizationApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_profile**](UserAuthorizationApi.md#get_profile) | **GET** /api/v1/profile | Get Profile


# **get_profile**
> Profile get_profile()

Get Profile

Returns a Profile including Organization and Current User Information.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_authorization_api
from gooddata_api_client.model.profile import Profile
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_authorization_api.UserAuthorizationApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get Profile
        api_response = api_instance.get_profile()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserAuthorizationApi->get_profile: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**Profile**](Profile.md)

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


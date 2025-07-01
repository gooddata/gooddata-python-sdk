# gooddata_api_client.OrganizationApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**switch_active_identity_provider**](OrganizationApi.md#switch_active_identity_provider) | **POST** /api/v1/actions/organization/switchActiveIdentityProvider | Switch Active Identity Provider


# **switch_active_identity_provider**
> switch_active_identity_provider(switch_identity_provider_request)

Switch Active Identity Provider

Switch the active identity provider for the organization. Requires MANAGE permission on the organization.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import organization_api
from gooddata_api_client.model.switch_identity_provider_request import SwitchIdentityProviderRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_api.OrganizationApi(api_client)
    switch_identity_provider_request = SwitchIdentityProviderRequest(
        idp_id="my-idp-123",
    ) # SwitchIdentityProviderRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Switch Active Identity Provider
        api_instance.switch_active_identity_provider(switch_identity_provider_request)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationApi->switch_active_identity_provider: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **switch_identity_provider_request** | [**SwitchIdentityProviderRequest**](SwitchIdentityProviderRequest.md)|  |

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
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


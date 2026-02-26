<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.organization_api.OrganizationApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**switch_active_identity_provider**](#switch_active_identity_provider) | **post** /api/v1/actions/organization/switchActiveIdentityProvider | Switch Active Identity Provider

# **switch_active_identity_provider**
<a id="switch_active_identity_provider"></a>
> switch_active_identity_provider(switch_identity_provider_request)

Switch Active Identity Provider

Switch the active identity provider for the organization. Requires MANAGE permission on the organization.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_api
from gooddata_api_client.model.switch_identity_provider_request import SwitchIdentityProviderRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_api.OrganizationApi(api_client)

    # example passing only required values which don't have defaults set
    body = SwitchIdentityProviderRequest(
        idp_id="my-idp-123",
    )
    try:
        # Switch Active Identity Provider
        api_response = api_instance.switch_active_identity_provider(
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationApi->switch_active_identity_provider: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**SwitchIdentityProviderRequest**](../../models/SwitchIdentityProviderRequest.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#switch_active_identity_provider.ApiResponseFor204) | No Content

#### switch_active_identity_provider.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


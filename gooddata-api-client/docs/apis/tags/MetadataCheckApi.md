<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.metadata_check_api.MetadataCheckApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**metadata_check_organization**](#metadata_check_organization) | **post** /api/v1/actions/organization/metadataCheck | (BETA) Check Organization Metadata Inconsistencies

# **metadata_check_organization**
<a id="metadata_check_organization"></a>
> metadata_check_organization()

(BETA) Check Organization Metadata Inconsistencies

(BETA) Temporary solution. Resyncs all organization objects and full workspaces within the organization with target GEN_AI_CHECK.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import metadata_check_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = metadata_check_api.MetadataCheckApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # (BETA) Check Organization Metadata Inconsistencies
        api_response = api_instance.metadata_check_organization()
    except gooddata_api_client.ApiException as e:
        print("Exception when calling MetadataCheckApi->metadata_check_organization: %s\n" % e)
```
### Parameters
This endpoint does not need any parameter.

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#metadata_check_organization.ApiResponseFor200) | OK

#### metadata_check_organization.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


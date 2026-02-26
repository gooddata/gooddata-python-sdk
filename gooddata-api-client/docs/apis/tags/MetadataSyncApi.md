<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.metadata_sync_api.MetadataSyncApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**metadata_sync**](#metadata_sync) | **post** /api/v1/actions/workspaces/{workspaceId}/metadataSync | (BETA) Sync Metadata to other services
[**metadata_sync_organization**](#metadata_sync_organization) | **post** /api/v1/actions/organization/metadataSync | (BETA) Sync organization scope Metadata to other services

# **metadata_sync**
<a id="metadata_sync"></a>
> metadata_sync(workspace_id)

(BETA) Sync Metadata to other services

(BETA) Temporary solution. Later relevant metadata actions will trigger it in its scope only.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import metadata_sync_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = metadata_sync_api.MetadataSyncApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    try:
        # (BETA) Sync Metadata to other services
        api_response = api_instance.metadata_sync(
            path_params=path_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling MetadataSyncApi->metadata_sync: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#metadata_sync.ApiResponseFor200) | OK

#### metadata_sync.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **metadata_sync_organization**
<a id="metadata_sync_organization"></a>
> metadata_sync_organization()

(BETA) Sync organization scope Metadata to other services

(BETA) Temporary solution. Later relevant metadata actions will trigger sync in their scope only.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import metadata_sync_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = metadata_sync_api.MetadataSyncApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # (BETA) Sync organization scope Metadata to other services
        api_response = api_instance.metadata_sync_organization()
    except gooddata_api_client.ApiException as e:
        print("Exception when calling MetadataSyncApi->metadata_sync_organization: %s\n" % e)
```
### Parameters
This endpoint does not need any parameter.

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#metadata_sync_organization.ApiResponseFor200) | OK

#### metadata_sync_organization.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


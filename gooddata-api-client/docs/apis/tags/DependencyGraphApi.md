<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.dependency_graph_api.DependencyGraphApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_dependent_entities_graph**](#get_dependent_entities_graph) | **get** /api/v1/actions/workspaces/{workspaceId}/dependentEntitiesGraph | Computes the dependent entities graph
[**get_dependent_entities_graph_from_entry_points**](#get_dependent_entities_graph_from_entry_points) | **post** /api/v1/actions/workspaces/{workspaceId}/dependentEntitiesGraph | Computes the dependent entities graph from given entry points

# **get_dependent_entities_graph**
<a id="get_dependent_entities_graph"></a>
> DependentEntitiesResponse get_dependent_entities_graph(workspace_id)

Computes the dependent entities graph

Computes the dependent entities graph

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import dependency_graph_api
from gooddata_api_client.model.dependent_entities_response import DependentEntitiesResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = dependency_graph_api.DependencyGraphApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    try:
        # Computes the dependent entities graph
        api_response = api_instance.get_dependent_entities_graph(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DependencyGraphApi->get_dependent_entities_graph: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
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
200 | [ApiResponseFor200](#get_dependent_entities_graph.ApiResponseFor200) | Computes the dependent entities graph

#### get_dependent_entities_graph.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DependentEntitiesResponse**](../../models/DependentEntitiesResponse.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_dependent_entities_graph_from_entry_points**
<a id="get_dependent_entities_graph_from_entry_points"></a>
> DependentEntitiesResponse get_dependent_entities_graph_from_entry_points(workspace_iddependent_entities_request)

Computes the dependent entities graph from given entry points

Computes the dependent entities graph from given entry points

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import dependency_graph_api
from gooddata_api_client.model.dependent_entities_request import DependentEntitiesRequest
from gooddata_api_client.model.dependent_entities_response import DependentEntitiesResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = dependency_graph_api.DependencyGraphApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    body = DependentEntitiesRequest(
        identifiers=[
            EntityIdentifier(
                id="/6bUUGjjNSwg0_bs",
                type="metric",
            )
        ],
    )
    try:
        # Computes the dependent entities graph from given entry points
        api_response = api_instance.get_dependent_entities_graph_from_entry_points(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DependencyGraphApi->get_dependent_entities_graph_from_entry_points: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DependentEntitiesRequest**](../../models/DependentEntitiesRequest.md) |  | 


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
200 | [ApiResponseFor200](#get_dependent_entities_graph_from_entry_points.ApiResponseFor200) | Computes the dependent entities graph from given entry points

#### get_dependent_entities_graph_from_entry_points.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DependentEntitiesResponse**](../../models/DependentEntitiesResponse.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


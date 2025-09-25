# gooddata_api_client.DependencyGraphApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_dependent_entities_graph**](DependencyGraphApi.md#get_dependent_entities_graph) | **GET** /api/v1/actions/workspaces/{workspaceId}/dependentEntitiesGraph | Computes the dependent entities graph
[**get_dependent_entities_graph_from_entry_points**](DependencyGraphApi.md#get_dependent_entities_graph_from_entry_points) | **POST** /api/v1/actions/workspaces/{workspaceId}/dependentEntitiesGraph | Computes the dependent entities graph from given entry points


# **get_dependent_entities_graph**
> DependentEntitiesResponse get_dependent_entities_graph(workspace_id)

Computes the dependent entities graph

Computes the dependent entities graph

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.dependent_entities_response import DependentEntitiesResponse
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.DependencyGraphApi(api_client)
    workspace_id = 'workspace_id_example' # str | 

    try:
        # Computes the dependent entities graph
        api_response = api_instance.get_dependent_entities_graph(workspace_id)
        print("The response of DependencyGraphApi->get_dependent_entities_graph:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DependencyGraphApi->get_dependent_entities_graph: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 

### Return type

[**DependentEntitiesResponse**](DependentEntitiesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Computes the dependent entities graph |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_dependent_entities_graph_from_entry_points**
> DependentEntitiesResponse get_dependent_entities_graph_from_entry_points(workspace_id, dependent_entities_request)

Computes the dependent entities graph from given entry points

Computes the dependent entities graph from given entry points

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.dependent_entities_request import DependentEntitiesRequest
from gooddata_api_client.models.dependent_entities_response import DependentEntitiesResponse
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.DependencyGraphApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    dependent_entities_request = gooddata_api_client.DependentEntitiesRequest() # DependentEntitiesRequest | 

    try:
        # Computes the dependent entities graph from given entry points
        api_response = api_instance.get_dependent_entities_graph_from_entry_points(workspace_id, dependent_entities_request)
        print("The response of DependencyGraphApi->get_dependent_entities_graph_from_entry_points:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DependencyGraphApi->get_dependent_entities_graph_from_entry_points: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **dependent_entities_request** | [**DependentEntitiesRequest**](DependentEntitiesRequest.md)|  | 

### Return type

[**DependentEntitiesResponse**](DependentEntitiesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Computes the dependent entities graph from given entry points |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


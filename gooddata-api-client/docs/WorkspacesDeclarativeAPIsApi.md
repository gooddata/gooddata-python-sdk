# gooddata_api_client.WorkspacesDeclarativeAPIsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_workspace_layout**](WorkspacesDeclarativeAPIsApi.md#get_workspace_layout) | **GET** /api/v1/layout/workspaces/{workspaceId} | Get workspace layout
[**get_workspaces_layout**](WorkspacesDeclarativeAPIsApi.md#get_workspaces_layout) | **GET** /api/v1/layout/workspaces | Get all workspaces layout
[**put_workspace_layout**](WorkspacesDeclarativeAPIsApi.md#put_workspace_layout) | **PUT** /api/v1/layout/workspaces/{workspaceId} | Set workspace layout
[**set_workspaces_layout**](WorkspacesDeclarativeAPIsApi.md#set_workspaces_layout) | **PUT** /api/v1/layout/workspaces | Set all workspaces layout


# **get_workspace_layout**
> DeclarativeWorkspaceModel get_workspace_layout(workspace_id, exclude=exclude)

Get workspace layout

Retrieve current model of the workspace in declarative form.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_workspace_model import DeclarativeWorkspaceModel
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
    api_instance = gooddata_api_client.WorkspacesDeclarativeAPIsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    exclude = ['exclude_example'] # List[str] |  (optional)

    try:
        # Get workspace layout
        api_response = api_instance.get_workspace_layout(workspace_id, exclude=exclude)
        print("The response of WorkspacesDeclarativeAPIsApi->get_workspace_layout:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesDeclarativeAPIsApi->get_workspace_layout: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **exclude** | [**List[str]**](str.md)|  | [optional] 

### Return type

[**DeclarativeWorkspaceModel**](DeclarativeWorkspaceModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved the workspace model. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_workspaces_layout**
> DeclarativeWorkspaces get_workspaces_layout(exclude=exclude)

Get all workspaces layout

Gets complete layout of workspaces, their hierarchy, models.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_workspaces import DeclarativeWorkspaces
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
    api_instance = gooddata_api_client.WorkspacesDeclarativeAPIsApi(api_client)
    exclude = ['exclude_example'] # List[str] |  (optional)

    try:
        # Get all workspaces layout
        api_response = api_instance.get_workspaces_layout(exclude=exclude)
        print("The response of WorkspacesDeclarativeAPIsApi->get_workspaces_layout:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesDeclarativeAPIsApi->get_workspaces_layout: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **exclude** | [**List[str]**](str.md)|  | [optional] 

### Return type

[**DeclarativeWorkspaces**](DeclarativeWorkspaces.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved layout of all workspaces. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_workspace_layout**
> put_workspace_layout(workspace_id, declarative_workspace_model)

Set workspace layout

Set complete layout of workspace, like model, authorization, etc.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_workspace_model import DeclarativeWorkspaceModel
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
    api_instance = gooddata_api_client.WorkspacesDeclarativeAPIsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    declarative_workspace_model = gooddata_api_client.DeclarativeWorkspaceModel() # DeclarativeWorkspaceModel | 

    try:
        # Set workspace layout
        api_instance.put_workspace_layout(workspace_id, declarative_workspace_model)
    except Exception as e:
        print("Exception when calling WorkspacesDeclarativeAPIsApi->put_workspace_layout: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **declarative_workspace_model** | [**DeclarativeWorkspaceModel**](DeclarativeWorkspaceModel.md)|  | 

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
**204** | The model of the workspace was set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_workspaces_layout**
> set_workspaces_layout(declarative_workspaces)

Set all workspaces layout

Sets complete layout of workspaces, their hierarchy, models.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_workspaces import DeclarativeWorkspaces
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
    api_instance = gooddata_api_client.WorkspacesDeclarativeAPIsApi(api_client)
    declarative_workspaces = gooddata_api_client.DeclarativeWorkspaces() # DeclarativeWorkspaces | 

    try:
        # Set all workspaces layout
        api_instance.set_workspaces_layout(declarative_workspaces)
    except Exception as e:
        print("Exception when calling WorkspacesDeclarativeAPIsApi->set_workspaces_layout: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **declarative_workspaces** | [**DeclarativeWorkspaces**](DeclarativeWorkspaces.md)|  | 

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
**204** | All workspaces layout set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


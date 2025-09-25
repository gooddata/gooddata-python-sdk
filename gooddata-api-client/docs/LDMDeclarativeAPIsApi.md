# gooddata_api_client.LDMDeclarativeAPIsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_logical_model**](LDMDeclarativeAPIsApi.md#get_logical_model) | **GET** /api/v1/layout/workspaces/{workspaceId}/logicalModel | Get logical model
[**set_logical_model**](LDMDeclarativeAPIsApi.md#set_logical_model) | **PUT** /api/v1/layout/workspaces/{workspaceId}/logicalModel | Set logical model


# **get_logical_model**
> DeclarativeModel get_logical_model(workspace_id, include_parents=include_parents)

Get logical model

Retrieve current logical model of the workspace in declarative form.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_model import DeclarativeModel
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
    api_instance = gooddata_api_client.LDMDeclarativeAPIsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    include_parents = True # bool |  (optional)

    try:
        # Get logical model
        api_response = api_instance.get_logical_model(workspace_id, include_parents=include_parents)
        print("The response of LDMDeclarativeAPIsApi->get_logical_model:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LDMDeclarativeAPIsApi->get_logical_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **include_parents** | **bool**|  | [optional] 

### Return type

[**DeclarativeModel**](DeclarativeModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved current logical model. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_logical_model**
> set_logical_model(workspace_id, declarative_model)

Set logical model

Set effective logical model of the workspace.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_model import DeclarativeModel
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
    api_instance = gooddata_api_client.LDMDeclarativeAPIsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    declarative_model = gooddata_api_client.DeclarativeModel() # DeclarativeModel | 

    try:
        # Set logical model
        api_instance.set_logical_model(workspace_id, declarative_model)
    except Exception as e:
        print("Exception when calling LDMDeclarativeAPIsApi->set_logical_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **declarative_model** | [**DeclarativeModel**](DeclarativeModel.md)|  | 

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
**204** | Logical model successfully set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


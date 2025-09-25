# gooddata_api_client.OrganizationDeclarativeAPIsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_organization_layout**](OrganizationDeclarativeAPIsApi.md#get_organization_layout) | **GET** /api/v1/layout/organization | Get organization layout
[**set_organization_layout**](OrganizationDeclarativeAPIsApi.md#set_organization_layout) | **PUT** /api/v1/layout/organization | Set organization layout


# **get_organization_layout**
> DeclarativeOrganization get_organization_layout(exclude=exclude)

Get organization layout

Retrieve complete layout of organization, workspaces, user-groups, etc.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_organization import DeclarativeOrganization
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
    api_instance = gooddata_api_client.OrganizationDeclarativeAPIsApi(api_client)
    exclude = ['exclude_example'] # List[str] |  (optional)

    try:
        # Get organization layout
        api_response = api_instance.get_organization_layout(exclude=exclude)
        print("The response of OrganizationDeclarativeAPIsApi->get_organization_layout:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationDeclarativeAPIsApi->get_organization_layout: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **exclude** | [**List[str]**](str.md)|  | [optional] 

### Return type

[**DeclarativeOrganization**](DeclarativeOrganization.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved all parts of an organization. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_organization_layout**
> set_organization_layout(declarative_organization)

Set organization layout

Sets complete layout of organization, like workspaces, user-groups, etc.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_organization import DeclarativeOrganization
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
    api_instance = gooddata_api_client.OrganizationDeclarativeAPIsApi(api_client)
    declarative_organization = gooddata_api_client.DeclarativeOrganization() # DeclarativeOrganization | 

    try:
        # Set organization layout
        api_instance.set_organization_layout(declarative_organization)
    except Exception as e:
        print("Exception when calling OrganizationDeclarativeAPIsApi->set_organization_layout: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **declarative_organization** | [**DeclarativeOrganization**](DeclarativeOrganization.md)|  | 

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
**204** | Defined all parts of an organization. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


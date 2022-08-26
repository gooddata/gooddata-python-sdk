# gooddata_metadata_client.ActionsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**all_platform_usage**](ActionsApi.md#all_platform_usage) | **GET** /api/v1/actions/collectUsage | Info about the platform usage.
[**generate_logical_model**](ActionsApi.md#generate_logical_model) | **POST** /api/v1/actions/dataSources/{dataSourceId}/generateLogicalModel | Generate logical data model (LDM) from physical data model (PDM)
[**get_dependent_entities_graph**](ActionsApi.md#get_dependent_entities_graph) | **GET** /api/v1/actions/workspaces/{workspaceId}/dependentEntitiesGraph | Computes the dependent entities graph
[**get_dependent_entities_graph_from_entry_points**](ActionsApi.md#get_dependent_entities_graph_from_entry_points) | **POST** /api/v1/actions/workspaces/{workspaceId}/dependentEntitiesGraph | Computes the dependent entities graph from given entry points
[**particular_platform_usage**](ActionsApi.md#particular_platform_usage) | **POST** /api/v1/actions/collectUsage | Info about the platform usage for particular items.
[**register_upload_notification**](ActionsApi.md#register_upload_notification) | **POST** /api/v1/actions/dataSources/{dataSourceId}/uploadNotification | Register an upload notification
[**resolve_all_entitlements**](ActionsApi.md#resolve_all_entitlements) | **GET** /api/v1/actions/resolveEntitlements | Values for all public entitlements.
[**resolve_requested_entitlements**](ActionsApi.md#resolve_requested_entitlements) | **POST** /api/v1/actions/resolveEntitlements | Values for requested public entitlements.
[**workspace_resolve_all_settings**](ActionsApi.md#workspace_resolve_all_settings) | **GET** /api/v1/actions/workspaces/{workspaceId}/resolveSettings | Values for all settings.
[**workspace_resolve_settings**](ActionsApi.md#workspace_resolve_settings) | **POST** /api/v1/actions/workspaces/{workspaceId}/resolveSettings | Values for selected settings.


# **all_platform_usage**
> [PlatformUsage] all_platform_usage()

Info about the platform usage.

Provides information about platform usage, like amount of users, workspaces, ...

### Example


```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import actions_api
from gooddata_metadata_client.model.platform_usage import PlatformUsage
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Info about the platform usage.
        api_response = api_instance.all_platform_usage()
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling ActionsApi->all_platform_usage: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**[PlatformUsage]**](PlatformUsage.md)

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

# **generate_logical_model**
> DeclarativeModel generate_logical_model(data_source_id, generate_ldm_request)

Generate logical data model (LDM) from physical data model (PDM)

Generate logical data model (LDM) from physical data model (PDM) stored in data source.

### Example


```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import actions_api
from gooddata_metadata_client.model.declarative_model import DeclarativeModel
from gooddata_metadata_client.model.generate_ldm_request import GenerateLdmRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    data_source_id = "dataSourceId_example" # str | 
    generate_ldm_request = GenerateLdmRequest(
        date_granularities="all",
        denorm_prefix="dr",
        fact_prefix="f",
        generate_long_ids=True,
        grain_prefix="g",
        grain_reference_prefix="gr",
        primary_label_prefix="pl",
        reference_prefix="r",
        secondary_label_prefix="sl",
        separator="__",
        table_prefix="out_table",
        view_prefix="out_view",
        wdf_prefix="wdf",
    ) # GenerateLdmRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Generate logical data model (LDM) from physical data model (PDM)
        api_response = api_instance.generate_logical_model(data_source_id, generate_ldm_request)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling ActionsApi->generate_logical_model: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  |
 **generate_ldm_request** | [**GenerateLdmRequest**](GenerateLdmRequest.md)|  |

### Return type

[**DeclarativeModel**](DeclarativeModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | LDM generated successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_dependent_entities_graph**
> DependentEntitiesResponse get_dependent_entities_graph(workspace_id)

Computes the dependent entities graph

Computes the dependent entities graph

### Example


```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import actions_api
from gooddata_metadata_client.model.dependent_entities_response import DependentEntitiesResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Computes the dependent entities graph
        api_response = api_instance.get_dependent_entities_graph(workspace_id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling ActionsApi->get_dependent_entities_graph: %s\n" % e)
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
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import actions_api
from gooddata_metadata_client.model.dependent_entities_response import DependentEntitiesResponse
from gooddata_metadata_client.model.dependent_entities_request import DependentEntitiesRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    dependent_entities_request = DependentEntitiesRequest(
        identifiers=[
            EntityIdentifier(
                id="id_example",
                type="type_example",
            ),
        ],
    ) # DependentEntitiesRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Computes the dependent entities graph from given entry points
        api_response = api_instance.get_dependent_entities_graph_from_entry_points(workspace_id, dependent_entities_request)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling ActionsApi->get_dependent_entities_graph_from_entry_points: %s\n" % e)
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

# **particular_platform_usage**
> [PlatformUsage] particular_platform_usage(platform_usage_request)

Info about the platform usage for particular items.

Provides information about platform usage, like amount of users, workspaces, ...

### Example


```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import actions_api
from gooddata_metadata_client.model.platform_usage_request import PlatformUsageRequest
from gooddata_metadata_client.model.platform_usage import PlatformUsage
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    platform_usage_request = PlatformUsageRequest(
        usage_item_names=[
            "WorkspaceCount",
        ],
    ) # PlatformUsageRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Info about the platform usage for particular items.
        api_response = api_instance.particular_platform_usage(platform_usage_request)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling ActionsApi->particular_platform_usage: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **platform_usage_request** | [**PlatformUsageRequest**](PlatformUsageRequest.md)|  |

### Return type

[**[PlatformUsage]**](PlatformUsage.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **register_upload_notification**
> register_upload_notification(data_source_id)

Register an upload notification

Notification sets up all reports to be computed again with new data.

### Example


```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import actions_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    data_source_id = "dataSourceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Register an upload notification
        api_instance.register_upload_notification(data_source_id)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling ActionsApi->register_upload_notification: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | An upload notification has been successfully registered. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resolve_all_entitlements**
> [ApiEntitlement] resolve_all_entitlements()

Values for all public entitlements.

Resolves values of available entitlements for the organization.

### Example


```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import actions_api
from gooddata_metadata_client.model.api_entitlement import ApiEntitlement
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Values for all public entitlements.
        api_response = api_instance.resolve_all_entitlements()
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling ActionsApi->resolve_all_entitlements: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**[ApiEntitlement]**](ApiEntitlement.md)

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

# **resolve_requested_entitlements**
> [ApiEntitlement] resolve_requested_entitlements(entitlements_request)

Values for requested public entitlements.

Resolves values for requested entitlements in the organization.

### Example


```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import actions_api
from gooddata_metadata_client.model.entitlements_request import EntitlementsRequest
from gooddata_metadata_client.model.api_entitlement import ApiEntitlement
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    entitlements_request = EntitlementsRequest(
        entitlements_name=[
            "Contract",
        ],
    ) # EntitlementsRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Values for requested public entitlements.
        api_response = api_instance.resolve_requested_entitlements(entitlements_request)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling ActionsApi->resolve_requested_entitlements: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entitlements_request** | [**EntitlementsRequest**](EntitlementsRequest.md)|  |

### Return type

[**[ApiEntitlement]**](ApiEntitlement.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_resolve_all_settings**
> [DeclarativeSetting] workspace_resolve_all_settings(workspace_id)

Values for all settings.

Resolves values for all settings in a workspace by current user, workspace, organization, or default settings.

### Example


```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import actions_api
from gooddata_metadata_client.model.declarative_setting import DeclarativeSetting
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Values for all settings.
        api_response = api_instance.workspace_resolve_all_settings(workspace_id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling ActionsApi->workspace_resolve_all_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |

### Return type

[**[DeclarativeSetting]**](DeclarativeSetting.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Values for selected settings. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_resolve_settings**
> [DeclarativeSetting] workspace_resolve_settings(workspace_id, resolve_settings_request)

Values for selected settings.

Resolves value for selected settings in a workspace by current user, workspace, organization, or default settings.

### Example


```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import actions_api
from gooddata_metadata_client.model.resolve_settings_request import ResolveSettingsRequest
from gooddata_metadata_client.model.declarative_setting import DeclarativeSetting
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    resolve_settings_request = ResolveSettingsRequest(
        settings=["timezone"],
    ) # ResolveSettingsRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Values for selected settings.
        api_response = api_instance.workspace_resolve_settings(workspace_id, resolve_settings_request)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling ActionsApi->workspace_resolve_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **resolve_settings_request** | [**ResolveSettingsRequest**](ResolveSettingsRequest.md)|  |

### Return type

[**[DeclarativeSetting]**](DeclarativeSetting.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Values for selected settings. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


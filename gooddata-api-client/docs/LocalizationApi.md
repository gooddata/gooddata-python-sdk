# gooddata_api_client.LocalizationApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**organization_localization_statistics**](LocalizationApi.md#organization_localization_statistics) | **GET** /api/v1/actions/organization/localization/statistics | (BETA) Languages with translations in the organization.
[**organization_localization_usage**](LocalizationApi.md#organization_localization_usage) | **GET** /api/v1/actions/organization/localization/usage | (BETA) Languages used in the organization.
[**organization_localization_usage_users**](LocalizationApi.md#organization_localization_usage_users) | **GET** /api/v1/actions/organization/localization/usage/users | (BETA) Users who set a language themselves.
[**organization_localization_usage_workspaces**](LocalizationApi.md#organization_localization_usage_workspaces) | **GET** /api/v1/actions/organization/localization/usage/workspaces | (BETA) Workspaces that use a language.
[**workspace_localization_statistics**](LocalizationApi.md#workspace_localization_statistics) | **GET** /api/v1/actions/workspaces/{workspaceId}/localization/statistics | (BETA) Languages with translations in the workspace.
[**workspace_localization_usage**](LocalizationApi.md#workspace_localization_usage) | **GET** /api/v1/actions/workspaces/{workspaceId}/localization/usage | (BETA) Languages used in the workspace.
[**workspace_localization_usage_users**](LocalizationApi.md#workspace_localization_usage_users) | **GET** /api/v1/actions/workspaces/{workspaceId}/localization/usage/users | (BETA) Workspace members who get a language.


# **organization_localization_statistics**
> LocalizationStatistics organization_localization_statistics()

(BETA) Languages with translations in the organization.

(BETA) Lists the languages that have at least one translation, separately for each kind of translation.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import localization_api
from gooddata_api_client.model.localization_statistics import LocalizationStatistics
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = localization_api.LocalizationApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # (BETA) Languages with translations in the organization.
        api_response = api_instance.organization_localization_statistics()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LocalizationApi->organization_localization_statistics: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**LocalizationStatistics**](LocalizationStatistics.md)

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

# **organization_localization_usage**
> LocalizationUsage organization_localization_usage()

(BETA) Languages used in the organization.

(BETA) Counts workspaces and users per language of the display, metadata and data language settings. Users count under the value they get in the organization. That value depends on the workspace, so only the settings that users set themselves count. `defaults` holds the value a workspace gets when it and its parents set nothing.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import localization_api
from gooddata_api_client.model.localization_usage import LocalizationUsage
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = localization_api.LocalizationApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # (BETA) Languages used in the organization.
        api_response = api_instance.organization_localization_usage()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LocalizationApi->organization_localization_usage: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**LocalizationUsage**](LocalizationUsage.md)

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

# **organization_localization_usage_users**
> LocalizationUsageUsers organization_localization_usage_users()

(BETA) Users who set a language themselves.

(BETA) Lists the users behind the counts of the organization localization usage, sorted by name. Users without a name come last. Users count under the value they get in the organization. That value depends on the workspace, so only the settings that users set themselves match. Only the source USER returns users. Without the setting filter, a user matches when any of the display, metadata and data language settings matches. Users counted in the usage entry without a language are not listed.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import localization_api
from gooddata_api_client.model.localization_usage_users import LocalizationUsageUsers
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = localization_api.LocalizationApi(api_client)
    value = "de-DE" # str | Language tag that the user sets. (optional)
    name = "ito" # str | Filter by user name, email or login (user ID). Note that the filter is case insensitive. (optional)
    setting = "LOCALE" # str | One of LOCALE, METADATA_LOCALE and DATA_LOCALE. (optional)
    source = "USER" # str | Where the value comes from. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned. (optional) if omitted the server will use the default value of 20

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) Users who set a language themselves.
        api_response = api_instance.organization_localization_usage_users(value=value, name=name, setting=setting, source=source, page=page, size=size)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LocalizationApi->organization_localization_usage_users: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **value** | **str**| Language tag that the user sets. | [optional]
 **name** | **str**| Filter by user name, email or login (user ID). Note that the filter is case insensitive. | [optional]
 **setting** | **str**| One of LOCALE, METADATA_LOCALE and DATA_LOCALE. | [optional]
 **source** | **str**| Where the value comes from. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned. | [optional] if omitted the server will use the default value of 20

### Return type

[**LocalizationUsageUsers**](LocalizationUsageUsers.md)

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

# **organization_localization_usage_workspaces**
> LocalizationUsageWorkspaces organization_localization_usage_workspaces()

(BETA) Workspaces that use a language.

(BETA) Lists the workspaces behind the counts of the organization localization usage, sorted by name. Without the setting filter, a workspace matches when any of the display, metadata and data language settings matches, and its source is the strongest one.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import localization_api
from gooddata_api_client.model.localization_usage_workspaces import LocalizationUsageWorkspaces
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = localization_api.LocalizationApi(api_client)
    value = "de-DE" # str | Language tag that the workspace gets. (optional)
    name = "berg" # str | Filter by workspace name. Note that the filter is case insensitive. (optional)
    setting = "LOCALE" # str | One of LOCALE, METADATA_LOCALE and DATA_LOCALE. (optional)
    source = "PARENT" # str | Where the value comes from. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned. (optional) if omitted the server will use the default value of 20

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) Workspaces that use a language.
        api_response = api_instance.organization_localization_usage_workspaces(value=value, name=name, setting=setting, source=source, page=page, size=size)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LocalizationApi->organization_localization_usage_workspaces: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **value** | **str**| Language tag that the workspace gets. | [optional]
 **name** | **str**| Filter by workspace name. Note that the filter is case insensitive. | [optional]
 **setting** | **str**| One of LOCALE, METADATA_LOCALE and DATA_LOCALE. | [optional]
 **source** | **str**| Where the value comes from. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned. | [optional] if omitted the server will use the default value of 20

### Return type

[**LocalizationUsageWorkspaces**](LocalizationUsageWorkspaces.md)

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

# **workspace_localization_statistics**
> LocalizationStatistics workspace_localization_statistics(workspace_id)

(BETA) Languages with translations in the workspace.

(BETA) Lists the languages that have at least one translation in the workspace or its parent workspaces. Each kind of translation has its own list.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import localization_api
from gooddata_api_client.model.localization_statistics import LocalizationStatistics
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = localization_api.LocalizationApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Languages with translations in the workspace.
        api_response = api_instance.workspace_localization_statistics(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LocalizationApi->workspace_localization_statistics: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |

### Return type

[**LocalizationStatistics**](LocalizationStatistics.md)

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

# **workspace_localization_usage**
> WorkspaceLocalizationUsage workspace_localization_usage(workspace_id)

(BETA) Languages used in the workspace.

(BETA) Returns the value the workspace gets for each of the display, metadata and data language settings. It also counts the workspace members per language. Members count under the value they get in the workspace: their own setting, otherwise the value of the workspace. Child workspaces are not included.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import localization_api
from gooddata_api_client.model.workspace_localization_usage import WorkspaceLocalizationUsage
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = localization_api.LocalizationApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Languages used in the workspace.
        api_response = api_instance.workspace_localization_usage(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LocalizationApi->workspace_localization_usage: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |

### Return type

[**WorkspaceLocalizationUsage**](WorkspaceLocalizationUsage.md)

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

# **workspace_localization_usage_users**
> LocalizationUsageUsers workspace_localization_usage_users(workspace_id)

(BETA) Workspace members who get a language.

(BETA) Lists the workspace members behind the counts of the workspace localization usage, sorted by name. Users without a name come last. Members count under the value they get in the workspace: their own setting, otherwise the value of the workspace. So every source can match. Without the setting filter, a member matches when any of the display, metadata and data language settings matches. Its source is then the strongest one.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import localization_api
from gooddata_api_client.model.localization_usage_users import LocalizationUsageUsers
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = localization_api.LocalizationApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    value = "de-DE" # str | Language tag that the user gets. (optional)
    name = "ito" # str | Filter by user name, email or login (user ID). Note that the filter is case insensitive. (optional)
    setting = "LOCALE" # str | One of LOCALE, METADATA_LOCALE and DATA_LOCALE. (optional)
    source = "WORKSPACE" # str | Where the value comes from. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned. (optional) if omitted the server will use the default value of 20

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Workspace members who get a language.
        api_response = api_instance.workspace_localization_usage_users(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LocalizationApi->workspace_localization_usage_users: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) Workspace members who get a language.
        api_response = api_instance.workspace_localization_usage_users(workspace_id, value=value, name=name, setting=setting, source=source, page=page, size=size)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LocalizationApi->workspace_localization_usage_users: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **value** | **str**| Language tag that the user gets. | [optional]
 **name** | **str**| Filter by user name, email or login (user ID). Note that the filter is case insensitive. | [optional]
 **setting** | **str**| One of LOCALE, METADATA_LOCALE and DATA_LOCALE. | [optional]
 **source** | **str**| Where the value comes from. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned. | [optional] if omitted the server will use the default value of 20

### Return type

[**LocalizationUsageUsers**](LocalizationUsageUsers.md)

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


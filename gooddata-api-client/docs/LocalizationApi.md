# gooddata_api_client.LocalizationApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**organization_localization_issue_workspaces**](LocalizationApi.md#organization_localization_issue_workspaces) | **GET** /api/v1/actions/organization/localization/issues/workspaces | (BETA) Workspaces with a localization issue.
[**organization_localization_issues**](LocalizationApi.md#organization_localization_issues) | **GET** /api/v1/actions/organization/localization/issues | (BETA) Localization issues of the organization.
[**organization_localization_statistics**](LocalizationApi.md#organization_localization_statistics) | **GET** /api/v1/actions/organization/localization/statistics | Languages with translations in the organization.
[**organization_localization_usage**](LocalizationApi.md#organization_localization_usage) | **GET** /api/v1/actions/organization/localization/usage | Languages used in the organization.
[**organization_localization_usage_users**](LocalizationApi.md#organization_localization_usage_users) | **GET** /api/v1/actions/organization/localization/usage/users | Users who set a language themselves.
[**organization_localization_usage_workspaces**](LocalizationApi.md#organization_localization_usage_workspaces) | **GET** /api/v1/actions/organization/localization/usage/workspaces | Workspaces that use a language.
[**workspace_localization_issues**](LocalizationApi.md#workspace_localization_issues) | **GET** /api/v1/actions/workspaces/{workspaceId}/localization/issues | (BETA) Localization issues of the workspace.
[**workspace_localization_statistics**](LocalizationApi.md#workspace_localization_statistics) | **GET** /api/v1/actions/workspaces/{workspaceId}/localization/statistics | Languages with translations in the workspace.
[**workspace_localization_usage**](LocalizationApi.md#workspace_localization_usage) | **GET** /api/v1/actions/workspaces/{workspaceId}/localization/usage | Languages used in the workspace.
[**workspace_localization_usage_child_workspaces**](LocalizationApi.md#workspace_localization_usage_child_workspaces) | **GET** /api/v1/actions/workspaces/{workspaceId}/localization/usage/childWorkspaces | (BETA) Workspaces below the workspace that use a language.
[**workspace_localization_usage_users**](LocalizationApi.md#workspace_localization_usage_users) | **GET** /api/v1/actions/workspaces/{workspaceId}/localization/usage/users | Workspace members who get a language.


# **organization_localization_issue_workspaces**
> LocalizationIssueWorkspaces organization_localization_issue_workspaces(type, locale)

(BETA) Workspaces with a localization issue.

(BETA) Lists the workspaces behind one entry of the organization localization issues, sorted by name.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import localization_api
from gooddata_api_client.model.localization_issue_workspaces import LocalizationIssueWorkspaces
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
    type = "METADATA_MISSING_TRANSLATION" # str | The type of the issue.
    locale = "de-DE" # str | The language of the issue.
    name = "berg" # str | Filter by workspace name. Note that the filter is case insensitive. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned. (optional) if omitted the server will use the default value of 20

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Workspaces with a localization issue.
        api_response = api_instance.organization_localization_issue_workspaces(type, locale)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LocalizationApi->organization_localization_issue_workspaces: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) Workspaces with a localization issue.
        api_response = api_instance.organization_localization_issue_workspaces(type, locale, name=name, page=page, size=size)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LocalizationApi->organization_localization_issue_workspaces: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **type** | **str**| The type of the issue. |
 **locale** | **str**| The language of the issue. |
 **name** | **str**| Filter by workspace name. Note that the filter is case insensitive. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned. | [optional] if omitted the server will use the default value of 20

### Return type

[**LocalizationIssueWorkspaces**](LocalizationIssueWorkspaces.md)

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

# **organization_localization_issues**
> LocalizationIssues organization_localization_issues()

(BETA) Localization issues of the organization.

(BETA) Counts the workspaces with each localization issue. The rules are the same as in the workspace localization issues.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import localization_api
from gooddata_api_client.model.localization_issues import LocalizationIssues
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
        # (BETA) Localization issues of the organization.
        api_response = api_instance.organization_localization_issues()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LocalizationApi->organization_localization_issues: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**LocalizationIssues**](LocalizationIssues.md)

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

# **organization_localization_statistics**
> LocalizationStatistics organization_localization_statistics()

Languages with translations in the organization.

Lists the languages that have at least one translation, separately for each kind of translation.

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
        # Languages with translations in the organization.
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

Languages used in the organization.

Counts workspaces and users per language of the display, metadata and data language settings. Users count under the value they get in the organization. That value depends on the workspace, so only the settings that users set themselves count. `defaults` holds the value a workspace gets when it and its parents set nothing.

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
        # Languages used in the organization.
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

Users who set a language themselves.

Lists the users behind the counts of the organization localization usage, sorted by name. Users without a name come last. Users count under the value they get in the organization. That value depends on the workspace, so only the settings that users set themselves match. Only the source USER returns users. Without the setting filter, a user matches when any of the display, metadata and data language settings matches. An empty `value=` means no filter. The list leaves out the users that the usage counts without a language.

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
        # Users who set a language themselves.
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

Workspaces that use a language.

Lists the workspaces behind the counts of the organization localization usage, sorted by name. Without the setting filter, a workspace matches when any of the display, metadata and data language settings matches, and its source is the strongest one. Without the value filter, a setting without a language matches too. An empty `value=` means no filter. The `value` parameter cannot filter for a missing language.

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
        # Workspaces that use a language.
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

# **workspace_localization_issues**
> LocalizationIssues workspace_localization_issues(workspace_id)

(BETA) Localization issues of the workspace.

(BETA) Checks the display and metadata language of the workspace against the metadata translations of the workspace and its parents. It also reports translations the workspace owns that nobody uses. It checks this only when the workspace has no workspaces below it or the user can see all of them.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import localization_api
from gooddata_api_client.model.localization_issues import LocalizationIssues
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
        # (BETA) Localization issues of the workspace.
        api_response = api_instance.workspace_localization_issues(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LocalizationApi->workspace_localization_issues: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |

### Return type

[**LocalizationIssues**](LocalizationIssues.md)

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

Languages with translations in the workspace.

Lists the languages that have at least one translation in the workspace or its parent workspaces. Each kind of translation has its own list. With includeCoverage=true, it also counts the translated metadata texts of the workspace and each parent.

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
    include_coverage = True # bool | (BETA) Adds translation counts for the workspace and each parent, root first. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Languages with translations in the workspace.
        api_response = api_instance.workspace_localization_statistics(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LocalizationApi->workspace_localization_statistics: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Languages with translations in the workspace.
        api_response = api_instance.workspace_localization_statistics(workspace_id, include_coverage=include_coverage)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LocalizationApi->workspace_localization_statistics: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **include_coverage** | **bool**| (BETA) Adds translation counts for the workspace and each parent, root first. | [optional]

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

Languages used in the workspace.

Returns the value the workspace gets for each of the display, metadata and data language settings. It also counts the workspace members per language. Members count under the value they get in the workspace: their own setting, otherwise the value of the workspace. `childWorkspaces` counts the workspaces below it that the user can see, the same way.

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
        # Languages used in the workspace.
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

# **workspace_localization_usage_child_workspaces**
> LocalizationUsageWorkspaces workspace_localization_usage_child_workspaces(workspace_id)

(BETA) Workspaces below the workspace that use a language.

(BETA) Lists the workspaces behind the `childWorkspaces` counts of the workspace localization usage. The list has the workspaces below the workspace that the user can see, sorted by name. Without the setting filter, a workspace matches when one of its three language settings matches. Its source is then the strongest one. Without the value filter, a setting without a language matches too. An empty `value=` means no filter. The `value` parameter cannot filter for a missing language.

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
    workspace_id = "workspaceId_example" # str | 
    value = "de-DE" # str | Language tag that the workspace gets. (optional)
    name = "berg" # str | Filter by workspace name. Note that the filter is case insensitive. (optional)
    setting = "LOCALE" # str | One of LOCALE, METADATA_LOCALE and DATA_LOCALE. (optional)
    source = "PARENT" # str | Where the value comes from. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned. (optional) if omitted the server will use the default value of 20

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Workspaces below the workspace that use a language.
        api_response = api_instance.workspace_localization_usage_child_workspaces(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LocalizationApi->workspace_localization_usage_child_workspaces: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # (BETA) Workspaces below the workspace that use a language.
        api_response = api_instance.workspace_localization_usage_child_workspaces(workspace_id, value=value, name=name, setting=setting, source=source, page=page, size=size)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LocalizationApi->workspace_localization_usage_child_workspaces: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
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

# **workspace_localization_usage_users**
> LocalizationUsageUsers workspace_localization_usage_users(workspace_id)

Workspace members who get a language.

Lists the workspace members behind the counts of the workspace localization usage, sorted by name. Users without a name come last. Members count under the value they get in the workspace: their own setting, otherwise the value of the workspace. So every source can match. Without the setting filter, a member matches when any of the display, metadata and data language settings matches. Its source is then the strongest one. An empty `value=` means no filter. The list leaves out the members that the usage counts without a language.

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
        # Workspace members who get a language.
        api_response = api_instance.workspace_localization_usage_users(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LocalizationApi->workspace_localization_usage_users: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Workspace members who get a language.
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


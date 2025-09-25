# gooddata_api_client.ReportingSettingsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**resolve_all_settings_without_workspace**](ReportingSettingsApi.md#resolve_all_settings_without_workspace) | **GET** /api/v1/actions/resolveSettings | Values for all settings without workspace.
[**resolve_settings_without_workspace**](ReportingSettingsApi.md#resolve_settings_without_workspace) | **POST** /api/v1/actions/resolveSettings | Values for selected settings without workspace.


# **resolve_all_settings_without_workspace**
> List[ResolvedSetting] resolve_all_settings_without_workspace()

Values for all settings without workspace.

Resolves values for all settings without workspace by current user, organization, or default settings.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.resolved_setting import ResolvedSetting
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
    api_instance = gooddata_api_client.ReportingSettingsApi(api_client)

    try:
        # Values for all settings without workspace.
        api_response = api_instance.resolve_all_settings_without_workspace()
        print("The response of ReportingSettingsApi->resolve_all_settings_without_workspace:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReportingSettingsApi->resolve_all_settings_without_workspace: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[ResolvedSetting]**](ResolvedSetting.md)

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

# **resolve_settings_without_workspace**
> List[ResolvedSetting] resolve_settings_without_workspace(resolve_settings_request)

Values for selected settings without workspace.

Resolves values for selected settings without workspace by current user, organization, or default settings.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.resolve_settings_request import ResolveSettingsRequest
from gooddata_api_client.models.resolved_setting import ResolvedSetting
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
    api_instance = gooddata_api_client.ReportingSettingsApi(api_client)
    resolve_settings_request = gooddata_api_client.ResolveSettingsRequest() # ResolveSettingsRequest | 

    try:
        # Values for selected settings without workspace.
        api_response = api_instance.resolve_settings_without_workspace(resolve_settings_request)
        print("The response of ReportingSettingsApi->resolve_settings_without_workspace:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReportingSettingsApi->resolve_settings_without_workspace: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resolve_settings_request** | [**ResolveSettingsRequest**](ResolveSettingsRequest.md)|  | 

### Return type

[**List[ResolvedSetting]**](ResolvedSetting.md)

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


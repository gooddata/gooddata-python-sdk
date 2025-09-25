# gooddata_api_client.TranslationsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**clean_translations**](TranslationsApi.md#clean_translations) | **POST** /api/v1/actions/workspaces/{workspaceId}/translations/clean | Cleans up translations.
[**get_translation_tags**](TranslationsApi.md#get_translation_tags) | **GET** /api/v1/actions/workspaces/{workspaceId}/translations | Get translation tags.
[**retrieve_translations**](TranslationsApi.md#retrieve_translations) | **POST** /api/v1/actions/workspaces/{workspaceId}/translations/retrieve | Retrieve translations for entities.
[**set_translations**](TranslationsApi.md#set_translations) | **POST** /api/v1/actions/workspaces/{workspaceId}/translations/set | Set translations for entities.


# **clean_translations**
> clean_translations(workspace_id, locale_request)

Cleans up translations.

Cleans up all translations for a particular locale.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.locale_request import LocaleRequest
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
    api_instance = gooddata_api_client.TranslationsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    locale_request = gooddata_api_client.LocaleRequest() # LocaleRequest | 

    try:
        # Cleans up translations.
        api_instance.clean_translations(workspace_id, locale_request)
    except Exception as e:
        print("Exception when calling TranslationsApi->clean_translations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **locale_request** | [**LocaleRequest**](LocaleRequest.md)|  | 

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
**204** | Translations were successfully removed. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_translation_tags**
> List[str] get_translation_tags(workspace_id)

Get translation tags.

Provides a list of effective translation tags.

### Example


```python
import gooddata_api_client
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
    api_instance = gooddata_api_client.TranslationsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 

    try:
        # Get translation tags.
        api_response = api_instance.get_translation_tags(workspace_id)
        print("The response of TranslationsApi->get_translation_tags:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TranslationsApi->get_translation_tags: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 

### Return type

**List[str]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved list of translation tags. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_translations**
> Xliff retrieve_translations(workspace_id, locale_request)

Retrieve translations for entities.

Retrieve all translation for existing entities in a particular locale. The source translations returned by this endpoint are always original, not translated, texts. Because the XLIFF schema definition has the 'xs:language' constraint for the 'srcLang' attribute, it is always set to 'en-US' value.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.locale_request import LocaleRequest
from gooddata_api_client.models.xliff import Xliff
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
    api_instance = gooddata_api_client.TranslationsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    locale_request = gooddata_api_client.LocaleRequest() # LocaleRequest | 

    try:
        # Retrieve translations for entities.
        api_response = api_instance.retrieve_translations(workspace_id, locale_request)
        print("The response of TranslationsApi->retrieve_translations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TranslationsApi->retrieve_translations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **locale_request** | [**LocaleRequest**](LocaleRequest.md)|  | 

### Return type

[**Xliff**](Xliff.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | XLIFF file containing translations for a particular locale. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_translations**
> set_translations(workspace_id, xliff)

Set translations for entities.

Set translation for existing entities in a particular locale.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.xliff import Xliff
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
    api_instance = gooddata_api_client.TranslationsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    xliff = gooddata_api_client.Xliff() # Xliff | 

    try:
        # Set translations for entities.
        api_instance.set_translations(workspace_id, xliff)
    except Exception as e:
        print("Exception when calling TranslationsApi->set_translations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **xliff** | [**Xliff**](Xliff.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/xml
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Translations were successfully set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


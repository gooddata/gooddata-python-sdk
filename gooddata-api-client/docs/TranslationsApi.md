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
import time
import gooddata_api_client
from gooddata_api_client.api import translations_api
from gooddata_api_client.model.locale_request import LocaleRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = translations_api.TranslationsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    locale_request = LocaleRequest(
        locale="en-US",
    ) # LocaleRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Cleans up translations.
        api_instance.clean_translations(workspace_id, locale_request)
    except gooddata_api_client.ApiException as e:
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
> [str] get_translation_tags(workspace_id)

Get translation tags.

Provides a list of effective translation tags.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import translations_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = translations_api.TranslationsApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get translation tags.
        api_response = api_instance.get_translation_tags(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling TranslationsApi->get_translation_tags: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |

### Return type

**[str]**

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
import time
import gooddata_api_client
from gooddata_api_client.api import translations_api
from gooddata_api_client.model.locale_request import LocaleRequest
from gooddata_api_client.model.xliff import Xliff
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = translations_api.TranslationsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    locale_request = LocaleRequest(
        locale="en-US",
    ) # LocaleRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Retrieve translations for entities.
        api_response = api_instance.retrieve_translations(workspace_id, locale_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import translations_api
from gooddata_api_client.model.xliff import Xliff
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = translations_api.TranslationsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    xliff = Xliff(
        file=[
            File(
                any=[
                    {},
                ],
                can_resegment="YES",
                id="id_example",
                notes=Notes(
                    note=[
                        Note(
                            applies_to="SOURCE",
                            category="category_example",
                            content="content_example",
                            id="id_example",
                            other_attributes={
                                "key": "key_example",
                            },
                            priority=1,
                        ),
                    ],
                ),
                original="original_example",
                other_attributes={
                    "key": "key_example",
                },
                skeleton=Skeleton(
                    content=[
                        {},
                    ],
                    href="href_example",
                ),
                space="space_example",
                src_dir="LTR",
                translate="YES",
                trg_dir="LTR",
                unit_or_group=[
                    {},
                ],
            ),
        ],
        other_attributes={
            "key": "key_example",
        },
        space="space_example",
        src_lang="src_lang_example",
        trg_lang="trg_lang_example",
        version="version_example",
    ) # Xliff | 

    # example passing only required values which don't have defaults set
    try:
        # Set translations for entities.
        api_instance.set_translations(workspace_id, xliff)
    except gooddata_api_client.ApiException as e:
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


# gooddata_api_client.UserSettingsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_user_settings**](UserSettingsApi.md#create_entity_user_settings) | **POST** /api/v1/entities/users/{userId}/userSettings | Post new user settings for the user
[**delete_entity_user_settings**](UserSettingsApi.md#delete_entity_user_settings) | **DELETE** /api/v1/entities/users/{userId}/userSettings/{id} | Delete a setting for a user
[**get_all_entities_user_settings**](UserSettingsApi.md#get_all_entities_user_settings) | **GET** /api/v1/entities/users/{userId}/userSettings | List all settings for a user
[**get_entity_user_settings**](UserSettingsApi.md#get_entity_user_settings) | **GET** /api/v1/entities/users/{userId}/userSettings/{id} | Get a setting for a user
[**update_entity_user_settings**](UserSettingsApi.md#update_entity_user_settings) | **PUT** /api/v1/entities/users/{userId}/userSettings/{id} | Put new user settings for the user


# **create_entity_user_settings**
> JsonApiUserSettingOutDocument create_entity_user_settings(user_id, json_api_user_setting_in_document)

Post new user settings for the user

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_settings_api
from gooddata_api_client.model.json_api_user_setting_out_document import JsonApiUserSettingOutDocument
from gooddata_api_client.model.json_api_user_setting_in_document import JsonApiUserSettingInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_settings_api.UserSettingsApi(api_client)
    user_id = "userId_example" # str | 
    json_api_user_setting_in_document = JsonApiUserSettingInDocument(
        data=JsonApiUserSettingIn(
            attributes=JsonApiOrganizationSettingInAttributes(
                content={},
                type="TIMEZONE",
            ),
            id="id1",
            type="userSetting",
        ),
    ) # JsonApiUserSettingInDocument | 

    # example passing only required values which don't have defaults set
    try:
        # Post new user settings for the user
        api_response = api_instance.create_entity_user_settings(user_id, json_api_user_setting_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserSettingsApi->create_entity_user_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  |
 **json_api_user_setting_in_document** | [**JsonApiUserSettingInDocument**](JsonApiUserSettingInDocument.md)|  |

### Return type

[**JsonApiUserSettingOutDocument**](JsonApiUserSettingOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_user_settings**
> delete_entity_user_settings(user_id, id)

Delete a setting for a user

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_settings_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_settings_api.UserSettingsApi(api_client)
    user_id = "userId_example" # str | 
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=content==JsonNodeValue;type==SettingConfigurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a setting for a user
        api_instance.delete_entity_user_settings(user_id, id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserSettingsApi->delete_entity_user_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a setting for a user
        api_instance.delete_entity_user_settings(user_id, id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserSettingsApi->delete_entity_user_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  |
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

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
**204** | Successfully deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_user_settings**
> JsonApiUserSettingOutList get_all_entities_user_settings(user_id)

List all settings for a user

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_settings_api
from gooddata_api_client.model.json_api_user_setting_out_list import JsonApiUserSettingOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_settings_api.UserSettingsApi(api_client)
    user_id = "userId_example" # str | 
    filter = "filter=content==JsonNodeValue;type==SettingConfigurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)

    # example passing only required values which don't have defaults set
    try:
        # List all settings for a user
        api_response = api_instance.get_all_entities_user_settings(user_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserSettingsApi->get_all_entities_user_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # List all settings for a user
        api_response = api_instance.get_all_entities_user_settings(user_id, filter=filter, page=page, size=size, sort=sort)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserSettingsApi->get_all_entities_user_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]

### Return type

[**JsonApiUserSettingOutList**](JsonApiUserSettingOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_user_settings**
> JsonApiUserSettingOutDocument get_entity_user_settings(user_id, id)

Get a setting for a user

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_settings_api
from gooddata_api_client.model.json_api_user_setting_out_document import JsonApiUserSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_settings_api.UserSettingsApi(api_client)
    user_id = "userId_example" # str | 
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=content==JsonNodeValue;type==SettingConfigurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a setting for a user
        api_response = api_instance.get_entity_user_settings(user_id, id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserSettingsApi->get_entity_user_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a setting for a user
        api_response = api_instance.get_entity_user_settings(user_id, id, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserSettingsApi->get_entity_user_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  |
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiUserSettingOutDocument**](JsonApiUserSettingOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_user_settings**
> JsonApiUserSettingOutDocument update_entity_user_settings(user_id, id, json_api_user_setting_in_document)

Put new user settings for the user

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_settings_api
from gooddata_api_client.model.json_api_user_setting_out_document import JsonApiUserSettingOutDocument
from gooddata_api_client.model.json_api_user_setting_in_document import JsonApiUserSettingInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_settings_api.UserSettingsApi(api_client)
    user_id = "userId_example" # str | 
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_user_setting_in_document = JsonApiUserSettingInDocument(
        data=JsonApiUserSettingIn(
            attributes=JsonApiOrganizationSettingInAttributes(
                content={},
                type="TIMEZONE",
            ),
            id="id1",
            type="userSetting",
        ),
    ) # JsonApiUserSettingInDocument | 
    filter = "filter=content==JsonNodeValue;type==SettingConfigurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put new user settings for the user
        api_response = api_instance.update_entity_user_settings(user_id, id, json_api_user_setting_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserSettingsApi->update_entity_user_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put new user settings for the user
        api_response = api_instance.update_entity_user_settings(user_id, id, json_api_user_setting_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserSettingsApi->update_entity_user_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  |
 **id** | **str**|  |
 **json_api_user_setting_in_document** | [**JsonApiUserSettingInDocument**](JsonApiUserSettingInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiUserSettingOutDocument**](JsonApiUserSettingOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


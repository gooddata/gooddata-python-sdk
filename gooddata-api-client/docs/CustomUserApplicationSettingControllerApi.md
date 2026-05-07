# gooddata_api_client.CustomUserApplicationSettingControllerApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_custom_user_application_settings**](CustomUserApplicationSettingControllerApi.md#create_entity_custom_user_application_settings) | **POST** /api/v1/entities/users/{userId}/customUserApplicationSettings | Post a new custom application setting for the user
[**delete_entity_custom_user_application_settings**](CustomUserApplicationSettingControllerApi.md#delete_entity_custom_user_application_settings) | **DELETE** /api/v1/entities/users/{userId}/customUserApplicationSettings/{id} | Delete a custom application setting for a user
[**get_all_entities_custom_user_application_settings**](CustomUserApplicationSettingControllerApi.md#get_all_entities_custom_user_application_settings) | **GET** /api/v1/entities/users/{userId}/customUserApplicationSettings | List all custom application settings for a user
[**get_entity_custom_user_application_settings**](CustomUserApplicationSettingControllerApi.md#get_entity_custom_user_application_settings) | **GET** /api/v1/entities/users/{userId}/customUserApplicationSettings/{id} | Get a custom application setting for a user
[**update_entity_custom_user_application_settings**](CustomUserApplicationSettingControllerApi.md#update_entity_custom_user_application_settings) | **PUT** /api/v1/entities/users/{userId}/customUserApplicationSettings/{id} | Put a custom application setting for the user


# **create_entity_custom_user_application_settings**
> JsonApiCustomUserApplicationSettingOutDocument create_entity_custom_user_application_settings(user_id, json_api_custom_user_application_setting_post_optional_id_document)

Post a new custom application setting for the user

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import custom_user_application_setting_controller_api
from gooddata_api_client.model.json_api_custom_user_application_setting_out_document import JsonApiCustomUserApplicationSettingOutDocument
from gooddata_api_client.model.json_api_custom_user_application_setting_post_optional_id_document import JsonApiCustomUserApplicationSettingPostOptionalIdDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = custom_user_application_setting_controller_api.CustomUserApplicationSettingControllerApi(api_client)
    user_id = "userId_example" # str | 
    json_api_custom_user_application_setting_post_optional_id_document = JsonApiCustomUserApplicationSettingPostOptionalIdDocument(
        data=JsonApiCustomUserApplicationSettingPostOptionalId(
            attributes=JsonApiCustomUserApplicationSettingInAttributes(
                application_name="application_name_example",
                content={},
                workspace_id="workspace_id_example",
            ),
            id="id1",
            type="customUserApplicationSetting",
        ),
    ) # JsonApiCustomUserApplicationSettingPostOptionalIdDocument | 

    # example passing only required values which don't have defaults set
    try:
        # Post a new custom application setting for the user
        api_response = api_instance.create_entity_custom_user_application_settings(user_id, json_api_custom_user_application_setting_post_optional_id_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling CustomUserApplicationSettingControllerApi->create_entity_custom_user_application_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  |
 **json_api_custom_user_application_setting_post_optional_id_document** | [**JsonApiCustomUserApplicationSettingPostOptionalIdDocument**](JsonApiCustomUserApplicationSettingPostOptionalIdDocument.md)|  |

### Return type

[**JsonApiCustomUserApplicationSettingOutDocument**](JsonApiCustomUserApplicationSettingOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_custom_user_application_settings**
> delete_entity_custom_user_application_settings(user_id, id)

Delete a custom application setting for a user

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import custom_user_application_setting_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = custom_user_application_setting_controller_api.CustomUserApplicationSettingControllerApi(api_client)
    user_id = "userId_example" # str | 
    id = "/6bUUGjjNSwg0_bs" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Delete a custom application setting for a user
        api_instance.delete_entity_custom_user_application_settings(user_id, id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling CustomUserApplicationSettingControllerApi->delete_entity_custom_user_application_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  |
 **id** | **str**|  |

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

# **get_all_entities_custom_user_application_settings**
> JsonApiCustomUserApplicationSettingOutList get_all_entities_custom_user_application_settings(user_id)

List all custom application settings for a user

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import custom_user_application_setting_controller_api
from gooddata_api_client.model.json_api_custom_user_application_setting_out_list import JsonApiCustomUserApplicationSettingOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = custom_user_application_setting_controller_api.CustomUserApplicationSettingControllerApi(api_client)
    user_id = "userId_example" # str | 
    filter = "applicationName==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = [
        "metaInclude=page,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # List all custom application settings for a user
        api_response = api_instance.get_all_entities_custom_user_application_settings(user_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling CustomUserApplicationSettingControllerApi->get_all_entities_custom_user_application_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # List all custom application settings for a user
        api_response = api_instance.get_all_entities_custom_user_application_settings(user_id, filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling CustomUserApplicationSettingControllerApi->get_all_entities_custom_user_application_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiCustomUserApplicationSettingOutList**](JsonApiCustomUserApplicationSettingOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_custom_user_application_settings**
> JsonApiCustomUserApplicationSettingOutDocument get_entity_custom_user_application_settings(user_id, id)

Get a custom application setting for a user

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import custom_user_application_setting_controller_api
from gooddata_api_client.model.json_api_custom_user_application_setting_out_document import JsonApiCustomUserApplicationSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = custom_user_application_setting_controller_api.CustomUserApplicationSettingControllerApi(api_client)
    user_id = "userId_example" # str | 
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "applicationName==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a custom application setting for a user
        api_response = api_instance.get_entity_custom_user_application_settings(user_id, id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling CustomUserApplicationSettingControllerApi->get_entity_custom_user_application_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a custom application setting for a user
        api_response = api_instance.get_entity_custom_user_application_settings(user_id, id, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling CustomUserApplicationSettingControllerApi->get_entity_custom_user_application_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  |
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiCustomUserApplicationSettingOutDocument**](JsonApiCustomUserApplicationSettingOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_custom_user_application_settings**
> JsonApiCustomUserApplicationSettingOutDocument update_entity_custom_user_application_settings(user_id, id, json_api_custom_user_application_setting_in_document)

Put a custom application setting for the user

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import custom_user_application_setting_controller_api
from gooddata_api_client.model.json_api_custom_user_application_setting_out_document import JsonApiCustomUserApplicationSettingOutDocument
from gooddata_api_client.model.json_api_custom_user_application_setting_in_document import JsonApiCustomUserApplicationSettingInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = custom_user_application_setting_controller_api.CustomUserApplicationSettingControllerApi(api_client)
    user_id = "userId_example" # str | 
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_custom_user_application_setting_in_document = JsonApiCustomUserApplicationSettingInDocument(
        data=JsonApiCustomUserApplicationSettingIn(
            attributes=JsonApiCustomUserApplicationSettingInAttributes(
                application_name="application_name_example",
                content={},
                workspace_id="workspace_id_example",
            ),
            id="id1",
            type="customUserApplicationSetting",
        ),
    ) # JsonApiCustomUserApplicationSettingInDocument | 
    filter = "applicationName==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put a custom application setting for the user
        api_response = api_instance.update_entity_custom_user_application_settings(user_id, id, json_api_custom_user_application_setting_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling CustomUserApplicationSettingControllerApi->update_entity_custom_user_application_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a custom application setting for the user
        api_response = api_instance.update_entity_custom_user_application_settings(user_id, id, json_api_custom_user_application_setting_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling CustomUserApplicationSettingControllerApi->update_entity_custom_user_application_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  |
 **id** | **str**|  |
 **json_api_custom_user_application_setting_in_document** | [**JsonApiCustomUserApplicationSettingInDocument**](JsonApiCustomUserApplicationSettingInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiCustomUserApplicationSettingOutDocument**](JsonApiCustomUserApplicationSettingOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


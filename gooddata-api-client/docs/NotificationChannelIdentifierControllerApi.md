# gooddata_api_client.NotificationChannelIdentifierControllerApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_all_entities_notification_channel_identifiers**](NotificationChannelIdentifierControllerApi.md#get_all_entities_notification_channel_identifiers) | **GET** /api/v1/entities/notificationChannelIdentifiers | Get all Notification Channel Identifier entities
[**get_entity_notification_channel_identifiers**](NotificationChannelIdentifierControllerApi.md#get_entity_notification_channel_identifiers) | **GET** /api/v1/entities/notificationChannelIdentifiers/{id} | Get Notification Channel Identifier entity


# **get_all_entities_notification_channel_identifiers**
> JsonApiNotificationChannelIdentifierOutList get_all_entities_notification_channel_identifiers()

Get all Notification Channel Identifier entities

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import notification_channel_identifier_controller_api
from gooddata_api_client.model.json_api_notification_channel_identifier_out_list import JsonApiNotificationChannelIdentifierOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = notification_channel_identifier_controller_api.NotificationChannelIdentifierControllerApi(api_client)
    filter = "name==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = [
        "metaInclude=page,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Notification Channel Identifier entities
        api_response = api_instance.get_all_entities_notification_channel_identifiers(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelIdentifierControllerApi->get_all_entities_notification_channel_identifiers: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiNotificationChannelIdentifierOutList**](JsonApiNotificationChannelIdentifierOutList.md)

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

# **get_entity_notification_channel_identifiers**
> JsonApiNotificationChannelIdentifierOutDocument get_entity_notification_channel_identifiers(id)

Get Notification Channel Identifier entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import notification_channel_identifier_controller_api
from gooddata_api_client.model.json_api_notification_channel_identifier_out_document import JsonApiNotificationChannelIdentifierOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = notification_channel_identifier_controller_api.NotificationChannelIdentifierControllerApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "name==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get Notification Channel Identifier entity
        api_response = api_instance.get_entity_notification_channel_identifiers(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelIdentifierControllerApi->get_entity_notification_channel_identifiers: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Notification Channel Identifier entity
        api_response = api_instance.get_entity_notification_channel_identifiers(id, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelIdentifierControllerApi->get_entity_notification_channel_identifiers: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiNotificationChannelIdentifierOutDocument**](JsonApiNotificationChannelIdentifierOutDocument.md)

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


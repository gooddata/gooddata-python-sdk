# gooddata_api_client.NotificationChannelsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_notification_channels**](NotificationChannelsApi.md#create_entity_notification_channels) | **POST** /api/v1/entities/notificationChannels | Post Notification Channel entities
[**delete_entity_notification_channels**](NotificationChannelsApi.md#delete_entity_notification_channels) | **DELETE** /api/v1/entities/notificationChannels/{id} | Delete Notification Channel entity
[**get_all_entities_notification_channel_identifiers**](NotificationChannelsApi.md#get_all_entities_notification_channel_identifiers) | **GET** /api/v1/entities/notificationChannelIdentifiers | 
[**get_all_entities_notification_channels**](NotificationChannelsApi.md#get_all_entities_notification_channels) | **GET** /api/v1/entities/notificationChannels | Get all Notification Channel entities
[**get_entity_notification_channel_identifiers**](NotificationChannelsApi.md#get_entity_notification_channel_identifiers) | **GET** /api/v1/entities/notificationChannelIdentifiers/{id} | 
[**get_entity_notification_channels**](NotificationChannelsApi.md#get_entity_notification_channels) | **GET** /api/v1/entities/notificationChannels/{id} | Get Notification Channel entity
[**get_export_templates_layout**](NotificationChannelsApi.md#get_export_templates_layout) | **GET** /api/v1/layout/exportTemplates | Get all export templates layout
[**get_notification_channels_layout**](NotificationChannelsApi.md#get_notification_channels_layout) | **GET** /api/v1/layout/notificationChannels | Get all notification channels layout
[**get_notifications**](NotificationChannelsApi.md#get_notifications) | **GET** /api/v1/actions/notifications | Get latest notifications.
[**mark_as_read_notification**](NotificationChannelsApi.md#mark_as_read_notification) | **POST** /api/v1/actions/notifications/{notificationId}/markAsRead | Mark notification as read.
[**mark_as_read_notification_all**](NotificationChannelsApi.md#mark_as_read_notification_all) | **POST** /api/v1/actions/notifications/markAsRead | Mark all notifications as read.
[**patch_entity_notification_channels**](NotificationChannelsApi.md#patch_entity_notification_channels) | **PATCH** /api/v1/entities/notificationChannels/{id} | Patch Notification Channel entity
[**set_export_templates**](NotificationChannelsApi.md#set_export_templates) | **PUT** /api/v1/layout/exportTemplates | Set all export templates
[**set_notification_channels**](NotificationChannelsApi.md#set_notification_channels) | **PUT** /api/v1/layout/notificationChannels | Set all notification channels
[**test_existing_notification_channel**](NotificationChannelsApi.md#test_existing_notification_channel) | **POST** /api/v1/actions/notificationChannels/{notificationChannelId}/test | Test existing notification channel.
[**test_notification_channel**](NotificationChannelsApi.md#test_notification_channel) | **POST** /api/v1/actions/notificationChannels/test | Test notification channel.
[**update_entity_notification_channels**](NotificationChannelsApi.md#update_entity_notification_channels) | **PUT** /api/v1/entities/notificationChannels/{id} | Put Notification Channel entity


# **create_entity_notification_channels**
> JsonApiNotificationChannelOutDocument create_entity_notification_channels(json_api_notification_channel_post_optional_id_document)

Post Notification Channel entities

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_notification_channel_out_document import JsonApiNotificationChannelOutDocument
from gooddata_api_client.models.json_api_notification_channel_post_optional_id_document import JsonApiNotificationChannelPostOptionalIdDocument
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
    api_instance = gooddata_api_client.NotificationChannelsApi(api_client)
    json_api_notification_channel_post_optional_id_document = gooddata_api_client.JsonApiNotificationChannelPostOptionalIdDocument() # JsonApiNotificationChannelPostOptionalIdDocument | 

    try:
        # Post Notification Channel entities
        api_response = api_instance.create_entity_notification_channels(json_api_notification_channel_post_optional_id_document)
        print("The response of NotificationChannelsApi->create_entity_notification_channels:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotificationChannelsApi->create_entity_notification_channels: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_notification_channel_post_optional_id_document** | [**JsonApiNotificationChannelPostOptionalIdDocument**](JsonApiNotificationChannelPostOptionalIdDocument.md)|  | 

### Return type

[**JsonApiNotificationChannelOutDocument**](JsonApiNotificationChannelOutDocument.md)

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

# **delete_entity_notification_channels**
> delete_entity_notification_channels(id, filter=filter)

Delete Notification Channel entity

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
    api_instance = gooddata_api_client.NotificationChannelsApi(api_client)
    id = 'id_example' # str | 
    filter = 'name==someString;description==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Delete Notification Channel entity
        api_instance.delete_entity_notification_channels(id, filter=filter)
    except Exception as e:
        print("Exception when calling NotificationChannelsApi->delete_entity_notification_channels: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
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

# **get_all_entities_notification_channel_identifiers**
> JsonApiNotificationChannelIdentifierOutList get_all_entities_notification_channel_identifiers(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)



### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_notification_channel_identifier_out_list import JsonApiNotificationChannelIdentifierOutList
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
    api_instance = gooddata_api_client.NotificationChannelsApi(api_client)
    filter = 'name==someString;description==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=page,all'] # List[str] | Include Meta objects. (optional)

    try:
        api_response = api_instance.get_all_entities_notification_channel_identifiers(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of NotificationChannelsApi->get_all_entities_notification_channel_identifiers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotificationChannelsApi->get_all_entities_notification_channel_identifiers: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **page** | **int**| Zero-based page index (0..N) | [optional] [default to 0]
 **size** | **int**| The size of the page to be returned | [optional] [default to 20]
 **sort** | [**List[str]**](str.md)| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiNotificationChannelIdentifierOutList**](JsonApiNotificationChannelIdentifierOutList.md)

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

# **get_all_entities_notification_channels**
> JsonApiNotificationChannelOutList get_all_entities_notification_channels(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)

Get all Notification Channel entities

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_notification_channel_out_list import JsonApiNotificationChannelOutList
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
    api_instance = gooddata_api_client.NotificationChannelsApi(api_client)
    filter = 'name==someString;description==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get all Notification Channel entities
        api_response = api_instance.get_all_entities_notification_channels(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of NotificationChannelsApi->get_all_entities_notification_channels:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotificationChannelsApi->get_all_entities_notification_channels: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **page** | **int**| Zero-based page index (0..N) | [optional] [default to 0]
 **size** | **int**| The size of the page to be returned | [optional] [default to 20]
 **sort** | [**List[str]**](str.md)| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiNotificationChannelOutList**](JsonApiNotificationChannelOutList.md)

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

# **get_entity_notification_channel_identifiers**
> JsonApiNotificationChannelIdentifierOutDocument get_entity_notification_channel_identifiers(id, filter=filter)



### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_notification_channel_identifier_out_document import JsonApiNotificationChannelIdentifierOutDocument
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
    api_instance = gooddata_api_client.NotificationChannelsApi(api_client)
    id = 'id_example' # str | 
    filter = 'name==someString;description==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        api_response = api_instance.get_entity_notification_channel_identifiers(id, filter=filter)
        print("The response of NotificationChannelsApi->get_entity_notification_channel_identifiers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotificationChannelsApi->get_entity_notification_channel_identifiers: %s\n" % e)
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
 - **Accept**: application/vnd.gooddata.api+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_notification_channels**
> JsonApiNotificationChannelOutDocument get_entity_notification_channels(id, filter=filter)

Get Notification Channel entity

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_notification_channel_out_document import JsonApiNotificationChannelOutDocument
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
    api_instance = gooddata_api_client.NotificationChannelsApi(api_client)
    id = 'id_example' # str | 
    filter = 'name==someString;description==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Get Notification Channel entity
        api_response = api_instance.get_entity_notification_channels(id, filter=filter)
        print("The response of NotificationChannelsApi->get_entity_notification_channels:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotificationChannelsApi->get_entity_notification_channels: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiNotificationChannelOutDocument**](JsonApiNotificationChannelOutDocument.md)

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

# **get_export_templates_layout**
> DeclarativeExportTemplates get_export_templates_layout()

Get all export templates layout

Gets complete layout of export templates.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_export_templates import DeclarativeExportTemplates
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
    api_instance = gooddata_api_client.NotificationChannelsApi(api_client)

    try:
        # Get all export templates layout
        api_response = api_instance.get_export_templates_layout()
        print("The response of NotificationChannelsApi->get_export_templates_layout:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotificationChannelsApi->get_export_templates_layout: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**DeclarativeExportTemplates**](DeclarativeExportTemplates.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved layout of all export templates. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_notification_channels_layout**
> DeclarativeNotificationChannels get_notification_channels_layout()

Get all notification channels layout

Gets complete layout of notification channels.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_notification_channels import DeclarativeNotificationChannels
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
    api_instance = gooddata_api_client.NotificationChannelsApi(api_client)

    try:
        # Get all notification channels layout
        api_response = api_instance.get_notification_channels_layout()
        print("The response of NotificationChannelsApi->get_notification_channels_layout:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotificationChannelsApi->get_notification_channels_layout: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**DeclarativeNotificationChannels**](DeclarativeNotificationChannels.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved layout of all notification channels. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_notifications**
> Notifications get_notifications(workspace_id=workspace_id, is_read=is_read, page=page, size=size, meta_include=meta_include)

Get latest notifications.

Get latest in-platform notifications for the current user.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.notifications import Notifications
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
    api_instance = gooddata_api_client.NotificationChannelsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace ID to filter notifications by. (optional)
    is_read = True # bool | Filter notifications by read status. (optional)
    page = '0' # str | Zero-based page index (0..N) (optional) (default to '0')
    size = '20' # str | The size of the page to be returned. (optional) (default to '20')
    meta_include = ['meta_include_example'] # List[str] | Additional meta information to include in the response. (optional)

    try:
        # Get latest notifications.
        api_response = api_instance.get_notifications(workspace_id=workspace_id, is_read=is_read, page=page, size=size, meta_include=meta_include)
        print("The response of NotificationChannelsApi->get_notifications:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotificationChannelsApi->get_notifications: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace ID to filter notifications by. | [optional] 
 **is_read** | **bool**| Filter notifications by read status. | [optional] 
 **page** | **str**| Zero-based page index (0..N) | [optional] [default to &#39;0&#39;]
 **size** | **str**| The size of the page to be returned. | [optional] [default to &#39;20&#39;]
 **meta_include** | [**List[str]**](str.md)| Additional meta information to include in the response. | [optional] 

### Return type

[**Notifications**](Notifications.md)

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

# **mark_as_read_notification**
> mark_as_read_notification(notification_id)

Mark notification as read.

Mark in-platform notification by its ID as read.

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
    api_instance = gooddata_api_client.NotificationChannelsApi(api_client)
    notification_id = 'notification_id_example' # str | Notification ID to mark as read.

    try:
        # Mark notification as read.
        api_instance.mark_as_read_notification(notification_id)
    except Exception as e:
        print("Exception when calling NotificationChannelsApi->mark_as_read_notification: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **notification_id** | **str**| Notification ID to mark as read. | 

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
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **mark_as_read_notification_all**
> mark_as_read_notification_all(workspace_id=workspace_id)

Mark all notifications as read.

Mark all user in-platform notifications as read.

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
    api_instance = gooddata_api_client.NotificationChannelsApi(api_client)
    workspace_id = 'workspace_id_example' # str | Workspace ID where to mark notifications as read. (optional)

    try:
        # Mark all notifications as read.
        api_instance.mark_as_read_notification_all(workspace_id=workspace_id)
    except Exception as e:
        print("Exception when calling NotificationChannelsApi->mark_as_read_notification_all: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace ID where to mark notifications as read. | [optional] 

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
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_notification_channels**
> JsonApiNotificationChannelOutDocument patch_entity_notification_channels(id, json_api_notification_channel_patch_document, filter=filter)

Patch Notification Channel entity

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_notification_channel_out_document import JsonApiNotificationChannelOutDocument
from gooddata_api_client.models.json_api_notification_channel_patch_document import JsonApiNotificationChannelPatchDocument
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
    api_instance = gooddata_api_client.NotificationChannelsApi(api_client)
    id = 'id_example' # str | 
    json_api_notification_channel_patch_document = gooddata_api_client.JsonApiNotificationChannelPatchDocument() # JsonApiNotificationChannelPatchDocument | 
    filter = 'name==someString;description==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Patch Notification Channel entity
        api_response = api_instance.patch_entity_notification_channels(id, json_api_notification_channel_patch_document, filter=filter)
        print("The response of NotificationChannelsApi->patch_entity_notification_channels:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotificationChannelsApi->patch_entity_notification_channels: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_notification_channel_patch_document** | [**JsonApiNotificationChannelPatchDocument**](JsonApiNotificationChannelPatchDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiNotificationChannelOutDocument**](JsonApiNotificationChannelOutDocument.md)

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

# **set_export_templates**
> set_export_templates(declarative_export_templates)

Set all export templates

Sets export templates in organization.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_export_templates import DeclarativeExportTemplates
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
    api_instance = gooddata_api_client.NotificationChannelsApi(api_client)
    declarative_export_templates = gooddata_api_client.DeclarativeExportTemplates() # DeclarativeExportTemplates | 

    try:
        # Set all export templates
        api_instance.set_export_templates(declarative_export_templates)
    except Exception as e:
        print("Exception when calling NotificationChannelsApi->set_export_templates: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **declarative_export_templates** | [**DeclarativeExportTemplates**](DeclarativeExportTemplates.md)|  | 

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
**204** | All export templates set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_notification_channels**
> set_notification_channels(declarative_notification_channels)

Set all notification channels

Sets notification channels in organization.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_notification_channels import DeclarativeNotificationChannels
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
    api_instance = gooddata_api_client.NotificationChannelsApi(api_client)
    declarative_notification_channels = gooddata_api_client.DeclarativeNotificationChannels() # DeclarativeNotificationChannels | 

    try:
        # Set all notification channels
        api_instance.set_notification_channels(declarative_notification_channels)
    except Exception as e:
        print("Exception when calling NotificationChannelsApi->set_notification_channels: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **declarative_notification_channels** | [**DeclarativeNotificationChannels**](DeclarativeNotificationChannels.md)|  | 

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
**204** | All notification channels set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_existing_notification_channel**
> TestResponse test_existing_notification_channel(notification_channel_id, test_destination_request=test_destination_request)

Test existing notification channel.

Tests the existing notification channel by sending a test notification.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.test_destination_request import TestDestinationRequest
from gooddata_api_client.models.test_response import TestResponse
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
    api_instance = gooddata_api_client.NotificationChannelsApi(api_client)
    notification_channel_id = 'notification_channel_id_example' # str | 
    test_destination_request = gooddata_api_client.TestDestinationRequest() # TestDestinationRequest |  (optional)

    try:
        # Test existing notification channel.
        api_response = api_instance.test_existing_notification_channel(notification_channel_id, test_destination_request=test_destination_request)
        print("The response of NotificationChannelsApi->test_existing_notification_channel:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotificationChannelsApi->test_existing_notification_channel: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **notification_channel_id** | **str**|  | 
 **test_destination_request** | [**TestDestinationRequest**](TestDestinationRequest.md)|  | [optional] 

### Return type

[**TestResponse**](TestResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The result of the test of a notification channel connection. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_notification_channel**
> TestResponse test_notification_channel(test_destination_request)

Test notification channel.

Tests the notification channel by sending a test notification.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.test_destination_request import TestDestinationRequest
from gooddata_api_client.models.test_response import TestResponse
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
    api_instance = gooddata_api_client.NotificationChannelsApi(api_client)
    test_destination_request = gooddata_api_client.TestDestinationRequest() # TestDestinationRequest | 

    try:
        # Test notification channel.
        api_response = api_instance.test_notification_channel(test_destination_request)
        print("The response of NotificationChannelsApi->test_notification_channel:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotificationChannelsApi->test_notification_channel: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_destination_request** | [**TestDestinationRequest**](TestDestinationRequest.md)|  | 

### Return type

[**TestResponse**](TestResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The result of the test of a notification channel connection. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_notification_channels**
> JsonApiNotificationChannelOutDocument update_entity_notification_channels(id, json_api_notification_channel_in_document, filter=filter)

Put Notification Channel entity

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_notification_channel_in_document import JsonApiNotificationChannelInDocument
from gooddata_api_client.models.json_api_notification_channel_out_document import JsonApiNotificationChannelOutDocument
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
    api_instance = gooddata_api_client.NotificationChannelsApi(api_client)
    id = 'id_example' # str | 
    json_api_notification_channel_in_document = gooddata_api_client.JsonApiNotificationChannelInDocument() # JsonApiNotificationChannelInDocument | 
    filter = 'name==someString;description==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Put Notification Channel entity
        api_response = api_instance.update_entity_notification_channels(id, json_api_notification_channel_in_document, filter=filter)
        print("The response of NotificationChannelsApi->update_entity_notification_channels:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotificationChannelsApi->update_entity_notification_channels: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_notification_channel_in_document** | [**JsonApiNotificationChannelInDocument**](JsonApiNotificationChannelInDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiNotificationChannelOutDocument**](JsonApiNotificationChannelOutDocument.md)

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


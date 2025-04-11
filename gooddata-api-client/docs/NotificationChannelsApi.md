# gooddata_api_client.NotificationChannelsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_notification_channels**](NotificationChannelsApi.md#create_entity_notification_channels) | **POST** /api/v1/entities/notificationChannels | Post Notification Channel entities
[**delete_entity_notification_channels**](NotificationChannelsApi.md#delete_entity_notification_channels) | **DELETE** /api/v1/entities/notificationChannels/{id} | Delete Notification Channel entity
[**get_all_entities_notification_channels**](NotificationChannelsApi.md#get_all_entities_notification_channels) | **GET** /api/v1/entities/notificationChannels | Get all Notification Channel entities
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
import time
import gooddata_api_client
from gooddata_api_client.api import notification_channels_api
from gooddata_api_client.model.json_api_notification_channel_out_document import JsonApiNotificationChannelOutDocument
from gooddata_api_client.model.json_api_notification_channel_post_optional_id_document import JsonApiNotificationChannelPostOptionalIdDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)
    json_api_notification_channel_post_optional_id_document = JsonApiNotificationChannelPostOptionalIdDocument(
        data=JsonApiNotificationChannelPostOptionalId(
            attributes=JsonApiNotificationChannelInAttributes(
                allowed_recipients="CREATOR",
                custom_dashboard_url="custom_dashboard_url_example",
                dashboard_link_visibility="HIDDEN",
                description="description_example",
                destination=JsonApiNotificationChannelInAttributesDestination(None),
                in_platform_notification="DISABLED",
                name="name_example",
            ),
            id="id1",
            type="notificationChannel",
        ),
    ) # JsonApiNotificationChannelPostOptionalIdDocument | 

    # example passing only required values which don't have defaults set
    try:
        # Post Notification Channel entities
        api_response = api_instance.create_entity_notification_channels(json_api_notification_channel_post_optional_id_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
> delete_entity_notification_channels(id)

Delete Notification Channel entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import notification_channels_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=name==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete Notification Channel entity
        api_instance.delete_entity_notification_channels(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->delete_entity_notification_channels: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete Notification Channel entity
        api_instance.delete_entity_notification_channels(id, filter=filter)
    except gooddata_api_client.ApiException as e:
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

# **get_all_entities_notification_channels**
> JsonApiNotificationChannelOutList get_all_entities_notification_channels()

Get all Notification Channel entities

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import notification_channels_api
from gooddata_api_client.model.json_api_notification_channel_out_list import JsonApiNotificationChannelOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)
    filter = "filter=name==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
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
        # Get all Notification Channel entities
        api_response = api_instance.get_all_entities_notification_channels(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->get_all_entities_notification_channels: %s\n" % e)
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

# **get_entity_notification_channels**
> JsonApiNotificationChannelOutDocument get_entity_notification_channels(id)

Get Notification Channel entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import notification_channels_api
from gooddata_api_client.model.json_api_notification_channel_out_document import JsonApiNotificationChannelOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=name==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get Notification Channel entity
        api_response = api_instance.get_entity_notification_channels(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->get_entity_notification_channels: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Notification Channel entity
        api_response = api_instance.get_entity_notification_channels(id, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import notification_channels_api
from gooddata_api_client.model.declarative_export_templates import DeclarativeExportTemplates
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get all export templates layout
        api_response = api_instance.get_export_templates_layout()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import notification_channels_api
from gooddata_api_client.model.declarative_notification_channels import DeclarativeNotificationChannels
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get all notification channels layout
        api_response = api_instance.get_notification_channels_layout()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
> Notifications get_notifications()

Get latest notifications.

Get latest in-platform notifications for the current user.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import notification_channels_api
from gooddata_api_client.model.notifications import Notifications
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)
    workspace_id = "workspaceId_example" # str | Workspace ID to filter notifications by. (optional)
    is_read = True # bool | Filter notifications by read status. (optional)
    page = "0" # str | Zero-based page index (0..N) (optional) if omitted the server will use the default value of "0"
    size = "20" # str | The size of the page to be returned. (optional) if omitted the server will use the default value of "20"
    meta_include = [
        "total",
    ] # [str] | Additional meta information to include in the response. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get latest notifications.
        api_response = api_instance.get_notifications(workspace_id=workspace_id, is_read=is_read, page=page, size=size, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->get_notifications: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace ID to filter notifications by. | [optional]
 **is_read** | **bool**| Filter notifications by read status. | [optional]
 **page** | **str**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of "0"
 **size** | **str**| The size of the page to be returned. | [optional] if omitted the server will use the default value of "20"
 **meta_include** | **[str]**| Additional meta information to include in the response. | [optional]

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
import time
import gooddata_api_client
from gooddata_api_client.api import notification_channels_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)
    notification_id = "notificationId_example" # str | Notification ID to mark as read.

    # example passing only required values which don't have defaults set
    try:
        # Mark notification as read.
        api_instance.mark_as_read_notification(notification_id)
    except gooddata_api_client.ApiException as e:
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
> mark_as_read_notification_all()

Mark all notifications as read.

Mark all user in-platform notifications as read.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import notification_channels_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)
    workspace_id = "workspaceId_example" # str | Workspace ID where to mark notifications as read. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Mark all notifications as read.
        api_instance.mark_as_read_notification_all(workspace_id=workspace_id)
    except gooddata_api_client.ApiException as e:
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
> JsonApiNotificationChannelOutDocument patch_entity_notification_channels(id, json_api_notification_channel_patch_document)

Patch Notification Channel entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import notification_channels_api
from gooddata_api_client.model.json_api_notification_channel_out_document import JsonApiNotificationChannelOutDocument
from gooddata_api_client.model.json_api_notification_channel_patch_document import JsonApiNotificationChannelPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_notification_channel_patch_document = JsonApiNotificationChannelPatchDocument(
        data=JsonApiNotificationChannelPatch(
            attributes=JsonApiNotificationChannelInAttributes(
                allowed_recipients="CREATOR",
                custom_dashboard_url="custom_dashboard_url_example",
                dashboard_link_visibility="HIDDEN",
                description="description_example",
                destination=JsonApiNotificationChannelInAttributesDestination(None),
                in_platform_notification="DISABLED",
                name="name_example",
            ),
            id="id1",
            type="notificationChannel",
        ),
    ) # JsonApiNotificationChannelPatchDocument | 
    filter = "filter=name==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch Notification Channel entity
        api_response = api_instance.patch_entity_notification_channels(id, json_api_notification_channel_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->patch_entity_notification_channels: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch Notification Channel entity
        api_response = api_instance.patch_entity_notification_channels(id, json_api_notification_channel_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import notification_channels_api
from gooddata_api_client.model.declarative_export_templates import DeclarativeExportTemplates
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)
    declarative_export_templates = DeclarativeExportTemplates(
        export_templates=[
            DeclarativeExportTemplate(
                dashboard_slides_template=DashboardSlidesTemplate(
                    applied_on=["PDF","PPTX"],
                    content_slide=ContentSlideTemplate(
                        description_field="{{dashboardFilters}}",
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                    ),
                    cover_slide=CoverSlideTemplate(
                        background_image=True,
                        description_field="Exported at: {{exportedAt}}",
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                    ),
                    intro_slide=IntroSlideTemplate(
                        background_image=True,
                        description_field='''About:
{{dashboardDescription}}

{{dashboardFilters}}''',
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        title_field="Introduction",
                    ),
                    section_slide=SectionSlideTemplate(
                        background_image=True,
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                    ),
                ),
                id="default-export-template",
                name="My default export template",
                widget_slides_template=WidgetSlidesTemplate(
                    applied_on=["PDF","PPTX"],
                    content_slide=ContentSlideTemplate(
                        description_field="{{dashboardFilters}}",
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                    ),
                ),
            ),
        ],
    ) # DeclarativeExportTemplates | 

    # example passing only required values which don't have defaults set
    try:
        # Set all export templates
        api_instance.set_export_templates(declarative_export_templates)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import notification_channels_api
from gooddata_api_client.model.declarative_notification_channels import DeclarativeNotificationChannels
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)
    declarative_notification_channels = DeclarativeNotificationChannels(
        notification_channels=[
            DeclarativeNotificationChannel(
                allowed_recipients="INTERNAL",
                custom_dashboard_url="custom_dashboard_url_example",
                dashboard_link_visibility="INTERNAL_ONLY",
                description="This is a channel",
                destination=DeclarativeNotificationChannelDestination(None),
                id="notification-channel-1",
                in_platform_notification="DISABLED",
                name="channel",
            ),
        ],
    ) # DeclarativeNotificationChannels | 

    # example passing only required values which don't have defaults set
    try:
        # Set all notification channels
        api_instance.set_notification_channels(declarative_notification_channels)
    except gooddata_api_client.ApiException as e:
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
> TestResponse test_existing_notification_channel(notification_channel_id)

Test existing notification channel.

Tests the existing notification channel by sending a test notification.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import notification_channels_api
from gooddata_api_client.model.test_response import TestResponse
from gooddata_api_client.model.test_destination_request import TestDestinationRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)
    notification_channel_id = "notificationChannelId_example" # str | 
    test_destination_request = TestDestinationRequest(
        destination=DeclarativeNotificationChannelDestination(None),
    ) # TestDestinationRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Test existing notification channel.
        api_response = api_instance.test_existing_notification_channel(notification_channel_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->test_existing_notification_channel: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Test existing notification channel.
        api_response = api_instance.test_existing_notification_channel(notification_channel_id, test_destination_request=test_destination_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
import time
import gooddata_api_client
from gooddata_api_client.api import notification_channels_api
from gooddata_api_client.model.test_response import TestResponse
from gooddata_api_client.model.test_destination_request import TestDestinationRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)
    test_destination_request = TestDestinationRequest(
        destination=DeclarativeNotificationChannelDestination(None),
    ) # TestDestinationRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Test notification channel.
        api_response = api_instance.test_notification_channel(test_destination_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
> JsonApiNotificationChannelOutDocument update_entity_notification_channels(id, json_api_notification_channel_in_document)

Put Notification Channel entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import notification_channels_api
from gooddata_api_client.model.json_api_notification_channel_in_document import JsonApiNotificationChannelInDocument
from gooddata_api_client.model.json_api_notification_channel_out_document import JsonApiNotificationChannelOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_notification_channel_in_document = JsonApiNotificationChannelInDocument(
        data=JsonApiNotificationChannelIn(
            attributes=JsonApiNotificationChannelInAttributes(
                allowed_recipients="CREATOR",
                custom_dashboard_url="custom_dashboard_url_example",
                dashboard_link_visibility="HIDDEN",
                description="description_example",
                destination=JsonApiNotificationChannelInAttributesDestination(None),
                in_platform_notification="DISABLED",
                name="name_example",
            ),
            id="id1",
            type="notificationChannel",
        ),
    ) # JsonApiNotificationChannelInDocument | 
    filter = "filter=name==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put Notification Channel entity
        api_response = api_instance.update_entity_notification_channels(id, json_api_notification_channel_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->update_entity_notification_channels: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put Notification Channel entity
        api_response = api_instance.update_entity_notification_channels(id, json_api_notification_channel_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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


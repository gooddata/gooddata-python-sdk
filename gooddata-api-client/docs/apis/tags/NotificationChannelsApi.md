<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.notification_channels_api.NotificationChannelsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_notification_channels**](#create_entity_notification_channels) | **post** /api/v1/entities/notificationChannels | Post Notification Channel entities
[**delete_entity_notification_channels**](#delete_entity_notification_channels) | **delete** /api/v1/entities/notificationChannels/{id} | Delete Notification Channel entity
[**get_all_entities_notification_channel_identifiers**](#get_all_entities_notification_channel_identifiers) | **get** /api/v1/entities/notificationChannelIdentifiers | 
[**get_all_entities_notification_channels**](#get_all_entities_notification_channels) | **get** /api/v1/entities/notificationChannels | Get all Notification Channel entities
[**get_entity_notification_channel_identifiers**](#get_entity_notification_channel_identifiers) | **get** /api/v1/entities/notificationChannelIdentifiers/{id} | 
[**get_entity_notification_channels**](#get_entity_notification_channels) | **get** /api/v1/entities/notificationChannels/{id} | Get Notification Channel entity
[**get_export_templates_layout**](#get_export_templates_layout) | **get** /api/v1/layout/exportTemplates | Get all export templates layout
[**get_notification_channels_layout**](#get_notification_channels_layout) | **get** /api/v1/layout/notificationChannels | Get all notification channels layout
[**get_notifications**](#get_notifications) | **get** /api/v1/actions/notifications | Get latest notifications.
[**mark_as_read_notification**](#mark_as_read_notification) | **post** /api/v1/actions/notifications/{notificationId}/markAsRead | Mark notification as read.
[**mark_as_read_notification_all**](#mark_as_read_notification_all) | **post** /api/v1/actions/notifications/markAsRead | Mark all notifications as read.
[**patch_entity_notification_channels**](#patch_entity_notification_channels) | **patch** /api/v1/entities/notificationChannels/{id} | Patch Notification Channel entity
[**set_export_templates**](#set_export_templates) | **put** /api/v1/layout/exportTemplates | Set all export templates
[**set_notification_channels**](#set_notification_channels) | **put** /api/v1/layout/notificationChannels | Set all notification channels
[**test_existing_notification_channel**](#test_existing_notification_channel) | **post** /api/v1/actions/notificationChannels/{notificationChannelId}/test | Test existing notification channel.
[**test_notification_channel**](#test_notification_channel) | **post** /api/v1/actions/notificationChannels/test | Test notification channel.
[**update_entity_notification_channels**](#update_entity_notification_channels) | **put** /api/v1/entities/notificationChannels/{id} | Put Notification Channel entity

# **create_entity_notification_channels**
<a id="create_entity_notification_channels"></a>
> JsonApiNotificationChannelOutDocument create_entity_notification_channels(json_api_notification_channel_post_optional_id_document)

Post Notification Channel entities

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import notification_channels_api
from gooddata_api_client.model.json_api_notification_channel_out_document import JsonApiNotificationChannelOutDocument
from gooddata_api_client.model.json_api_notification_channel_post_optional_id_document import JsonApiNotificationChannelPostOptionalIdDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)

    # example passing only required values which don't have defaults set
    body = JsonApiNotificationChannelPostOptionalIdDocument(
        data=JsonApiNotificationChannelPostOptionalId(
            attributes=dict(
                allowed_recipients="CREATOR",
                custom_dashboard_url="custom_dashboard_url_example",
                dashboard_link_visibility="HIDDEN",
                description="description_example",
                destination=None,
                in_platform_notification="DISABLED",
                name="name_example",
                notification_source="notification_source_example",
            ),
            id="id1",
            type="notificationChannel",
        ),
    )
    try:
        # Post Notification Channel entities
        api_response = api_instance.create_entity_notification_channels(
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->create_entity_notification_channels: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, SchemaForRequestBodyApplicationVndGooddataApijson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiNotificationChannelPostOptionalIdDocument**](../../models/JsonApiNotificationChannelPostOptionalIdDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiNotificationChannelPostOptionalIdDocument**](../../models/JsonApiNotificationChannelPostOptionalIdDocument.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#create_entity_notification_channels.ApiResponseFor201) | Request successfully processed

#### create_entity_notification_channels.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationJson, SchemaFor201ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiNotificationChannelOutDocument**](../../models/JsonApiNotificationChannelOutDocument.md) |  | 


# SchemaFor201ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiNotificationChannelOutDocument**](../../models/JsonApiNotificationChannelOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_entity_notification_channels**
<a id="delete_entity_notification_channels"></a>
> delete_entity_notification_channels(id)

Delete Notification Channel entity

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import notification_channels_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Delete Notification Channel entity
        api_response = api_instance.delete_entity_notification_channels(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->delete_entity_notification_channels: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "name==someString;description==someString",
    }
    try:
        # Delete Notification Channel entity
        api_response = api_instance.delete_entity_notification_channels(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->delete_entity_notification_channels: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#delete_entity_notification_channels.ApiResponseFor204) | Successfully deleted

#### delete_entity_notification_channels.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_notification_channel_identifiers**
<a id="get_all_entities_notification_channel_identifiers"></a>
> JsonApiNotificationChannelIdentifierOutList get_all_entities_notification_channel_identifiers()



### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import notification_channels_api
from gooddata_api_client.model.json_api_notification_channel_identifier_out_list import JsonApiNotificationChannelIdentifierOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)

    # example passing only optional values
    query_params = {
        'filter': "name==someString;description==someString",
        'page': 0,
        'size': 20,
        'sort': [
        "sort_example"
    ],
        'metaInclude': [
        "metaInclude=page,all"
    ],
    }
    try:
        api_response = api_instance.get_all_entities_notification_channel_identifiers(
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->get_all_entities_notification_channel_identifiers: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
page | PageSchema | | optional
size | SizeSchema | | optional
sort | SortSchema | | optional
metaInclude | MetaIncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# PageSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 0

# SizeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 20

# SortSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

# MetaIncludeSchema

Included meta objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Included meta objects | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["page", "all", "ALL", ] 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_all_entities_notification_channel_identifiers.ApiResponseFor200) | Request successfully processed

#### get_all_entities_notification_channel_identifiers.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiNotificationChannelIdentifierOutList**](../../models/JsonApiNotificationChannelIdentifierOutList.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiNotificationChannelIdentifierOutList**](../../models/JsonApiNotificationChannelIdentifierOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_notification_channels**
<a id="get_all_entities_notification_channels"></a>
> JsonApiNotificationChannelOutList get_all_entities_notification_channels()

Get all Notification Channel entities

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import notification_channels_api
from gooddata_api_client.model.json_api_notification_channel_out_list import JsonApiNotificationChannelOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)

    # example passing only optional values
    query_params = {
        'filter': "name==someString;description==someString",
        'page': 0,
        'size': 20,
        'sort': [
        "sort_example"
    ],
        'metaInclude': [
        "metaInclude=page,all"
    ],
    }
    try:
        # Get all Notification Channel entities
        api_response = api_instance.get_all_entities_notification_channels(
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->get_all_entities_notification_channels: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
page | PageSchema | | optional
size | SizeSchema | | optional
sort | SortSchema | | optional
metaInclude | MetaIncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# PageSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 0

# SizeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 20

# SortSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

# MetaIncludeSchema

Included meta objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Included meta objects | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["page", "all", "ALL", ] 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_all_entities_notification_channels.ApiResponseFor200) | Request successfully processed

#### get_all_entities_notification_channels.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiNotificationChannelOutList**](../../models/JsonApiNotificationChannelOutList.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiNotificationChannelOutList**](../../models/JsonApiNotificationChannelOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_notification_channel_identifiers**
<a id="get_entity_notification_channel_identifiers"></a>
> JsonApiNotificationChannelIdentifierOutDocument get_entity_notification_channel_identifiers(id)



### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import notification_channels_api
from gooddata_api_client.model.json_api_notification_channel_identifier_out_document import JsonApiNotificationChannelIdentifierOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        api_response = api_instance.get_entity_notification_channel_identifiers(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->get_entity_notification_channel_identifiers: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "name==someString;description==someString",
    }
    try:
        api_response = api_instance.get_entity_notification_channel_identifiers(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->get_entity_notification_channel_identifiers: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_entity_notification_channel_identifiers.ApiResponseFor200) | Request successfully processed

#### get_entity_notification_channel_identifiers.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiNotificationChannelIdentifierOutDocument**](../../models/JsonApiNotificationChannelIdentifierOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiNotificationChannelIdentifierOutDocument**](../../models/JsonApiNotificationChannelIdentifierOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_notification_channels**
<a id="get_entity_notification_channels"></a>
> JsonApiNotificationChannelOutDocument get_entity_notification_channels(id)

Get Notification Channel entity

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import notification_channels_api
from gooddata_api_client.model.json_api_notification_channel_out_document import JsonApiNotificationChannelOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Get Notification Channel entity
        api_response = api_instance.get_entity_notification_channels(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->get_entity_notification_channels: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "name==someString;description==someString",
    }
    try:
        # Get Notification Channel entity
        api_response = api_instance.get_entity_notification_channels(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->get_entity_notification_channels: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_entity_notification_channels.ApiResponseFor200) | Request successfully processed

#### get_entity_notification_channels.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiNotificationChannelOutDocument**](../../models/JsonApiNotificationChannelOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiNotificationChannelOutDocument**](../../models/JsonApiNotificationChannelOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_export_templates_layout**
<a id="get_export_templates_layout"></a>
> DeclarativeExportTemplates get_export_templates_layout()

Get all export templates layout

Gets complete layout of export templates.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import notification_channels_api
from gooddata_api_client.model.declarative_export_templates import DeclarativeExportTemplates
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
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

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_export_templates_layout.ApiResponseFor200) | Retrieved layout of all export templates.

#### get_export_templates_layout.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeExportTemplates**](../../models/DeclarativeExportTemplates.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_notification_channels_layout**
<a id="get_notification_channels_layout"></a>
> DeclarativeNotificationChannels get_notification_channels_layout()

Get all notification channels layout

Gets complete layout of notification channels.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import notification_channels_api
from gooddata_api_client.model.declarative_notification_channels import DeclarativeNotificationChannels
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
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

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_notification_channels_layout.ApiResponseFor200) | Retrieved layout of all notification channels.

#### get_notification_channels_layout.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeNotificationChannels**](../../models/DeclarativeNotificationChannels.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_notifications**
<a id="get_notifications"></a>
> Notifications get_notifications()

Get latest notifications.

Get latest in-platform notifications for the current user.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import notification_channels_api
from gooddata_api_client.model.notifications import Notifications
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)

    # example passing only optional values
    query_params = {
        'workspaceId': "workspaceId_example",
        'isRead': True,
        'page': "0",
        'size': "20",
        'metaInclude': [
        "total"
    ],
    }
    try:
        # Get latest notifications.
        api_response = api_instance.get_notifications(
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->get_notifications: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | optional
isRead | IsReadSchema | | optional
page | PageSchema | | optional
size | SizeSchema | | optional
metaInclude | MetaIncludeSchema | | optional


# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IsReadSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bool,  | BoolClass,  |  | 

# PageSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | if omitted the server will use the default value of "0"

# SizeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | if omitted the server will use the default value of "20"

# MetaIncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["total", "ALL", ] 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_notifications.ApiResponseFor200) | OK

#### get_notifications.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Notifications**](../../models/Notifications.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **mark_as_read_notification**
<a id="mark_as_read_notification"></a>
> mark_as_read_notification(notification_id)

Mark notification as read.

Mark in-platform notification by its ID as read.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import notification_channels_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'notificationId': "notificationId_example",
    }
    try:
        # Mark notification as read.
        api_response = api_instance.mark_as_read_notification(
            path_params=path_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->mark_as_read_notification: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
notificationId | NotificationIdSchema | | 

# NotificationIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#mark_as_read_notification.ApiResponseFor204) | No Content

#### mark_as_read_notification.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **mark_as_read_notification_all**
<a id="mark_as_read_notification_all"></a>
> mark_as_read_notification_all()

Mark all notifications as read.

Mark all user in-platform notifications as read.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import notification_channels_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)

    # example passing only optional values
    query_params = {
        'workspaceId': "workspaceId_example",
    }
    try:
        # Mark all notifications as read.
        api_response = api_instance.mark_as_read_notification_all(
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->mark_as_read_notification_all: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | optional


# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#mark_as_read_notification_all.ApiResponseFor204) | No Content

#### mark_as_read_notification_all.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **patch_entity_notification_channels**
<a id="patch_entity_notification_channels"></a>
> JsonApiNotificationChannelOutDocument patch_entity_notification_channels(idjson_api_notification_channel_patch_document)

Patch Notification Channel entity

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import notification_channels_api
from gooddata_api_client.model.json_api_notification_channel_out_document import JsonApiNotificationChannelOutDocument
from gooddata_api_client.model.json_api_notification_channel_patch_document import JsonApiNotificationChannelPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiNotificationChannelPatchDocument(
        data=JsonApiNotificationChannelPatch(
            attributes=dict(
                allowed_recipients="CREATOR",
                custom_dashboard_url="custom_dashboard_url_example",
                dashboard_link_visibility="HIDDEN",
                description="description_example",
                destination=None,
                in_platform_notification="DISABLED",
                name="name_example",
                notification_source="notification_source_example",
            ),
            id="id1",
            type="notificationChannel",
        ),
    )
    try:
        # Patch Notification Channel entity
        api_response = api_instance.patch_entity_notification_channels(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->patch_entity_notification_channels: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "name==someString;description==someString",
    }
    body = JsonApiNotificationChannelPatchDocument(
        data=JsonApiNotificationChannelPatch(
            attributes=dict(
                allowed_recipients="CREATOR",
                custom_dashboard_url="custom_dashboard_url_example",
                dashboard_link_visibility="HIDDEN",
                description="description_example",
                destination=None,
                in_platform_notification="DISABLED",
                name="name_example",
                notification_source="notification_source_example",
            ),
            id="id1",
            type="notificationChannel",
        ),
    )
    try:
        # Patch Notification Channel entity
        api_response = api_instance.patch_entity_notification_channels(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->patch_entity_notification_channels: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiNotificationChannelPatchDocument**](../../models/JsonApiNotificationChannelPatchDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiNotificationChannelPatchDocument**](../../models/JsonApiNotificationChannelPatchDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#patch_entity_notification_channels.ApiResponseFor200) | Request successfully processed

#### patch_entity_notification_channels.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiNotificationChannelOutDocument**](../../models/JsonApiNotificationChannelOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiNotificationChannelOutDocument**](../../models/JsonApiNotificationChannelOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **set_export_templates**
<a id="set_export_templates"></a>
> set_export_templates(declarative_export_templates)

Set all export templates

Sets export templates in organization.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import notification_channels_api
from gooddata_api_client.model.declarative_export_templates import DeclarativeExportTemplates
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)

    # example passing only required values which don't have defaults set
    body = DeclarativeExportTemplates(
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
,
                    ),
                    cover_slide=CoverSlideTemplate(
                        background_image=True,
                        description_field="Exported at: {{exportedAt}}",
                        footer=RunningSection(),
                        header=RunningSection(),
                    ),
                    intro_slide=IntroSlideTemplate(
                        background_image=True,
                        description_field="About:\n{{dashboardDescription}}\n\n{{dashboardFilters}}",
                        footer=RunningSection(),
                        header=RunningSection(),
                        title_field="Introduction",
                    ),
                    section_slide=SectionSlideTemplate(
                        background_image=True,
                        footer=RunningSection(),
                        header=RunningSection(),
                    ),
                ),
                id="default-export-template",
                name="My default export template",
                widget_slides_template=WidgetSlidesTemplate(
                    applied_on=["PDF","PPTX"],
                    content_slide=ContentSlideTemplate(),
                ),
            )
        ],
    )
    try:
        # Set all export templates
        api_response = api_instance.set_export_templates(
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->set_export_templates: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeExportTemplates**](../../models/DeclarativeExportTemplates.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#set_export_templates.ApiResponseFor204) | All export templates set.

#### set_export_templates.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **set_notification_channels**
<a id="set_notification_channels"></a>
> set_notification_channels(declarative_notification_channels)

Set all notification channels

Sets notification channels in organization.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import notification_channels_api
from gooddata_api_client.model.declarative_notification_channels import DeclarativeNotificationChannels
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)

    # example passing only required values which don't have defaults set
    body = DeclarativeNotificationChannels(
        notification_channels=[
            DeclarativeNotificationChannel(
                allowed_recipients="INTERNAL",
                custom_dashboard_url="custom_dashboard_url_example",
                dashboard_link_visibility="INTERNAL_ONLY",
                description="This is a channel",
                destination=None,
                destination_type="WEBHOOK",
                id="notification-channel-1",
                in_platform_notification="DISABLED",
                name="channel",
                notification_source="notification_source_example",
            )
        ],
    )
    try:
        # Set all notification channels
        api_response = api_instance.set_notification_channels(
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->set_notification_channels: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeNotificationChannels**](../../models/DeclarativeNotificationChannels.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#set_notification_channels.ApiResponseFor204) | All notification channels set.

#### set_notification_channels.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **test_existing_notification_channel**
<a id="test_existing_notification_channel"></a>
> TestResponse test_existing_notification_channel(notification_channel_id)

Test existing notification channel.

Tests the existing notification channel by sending a test notification.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import notification_channels_api
from gooddata_api_client.model.test_response import TestResponse
from gooddata_api_client.model.test_destination_request import TestDestinationRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'notificationChannelId': "notificationChannelId_example",
    }
    try:
        # Test existing notification channel.
        api_response = api_instance.test_existing_notification_channel(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->test_existing_notification_channel: %s\n" % e)

    # example passing only optional values
    path_params = {
        'notificationChannelId': "notificationChannelId_example",
    }
    body = TestDestinationRequest(
        destination=None,
        external_recipients=[
            AutomationExternalRecipient(
                email="email_example",
            )
        ],
    )
    try:
        # Test existing notification channel.
        api_response = api_instance.test_existing_notification_channel(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->test_existing_notification_channel: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, Unset] | optional, default is unset |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**TestDestinationRequest**](../../models/TestDestinationRequest.md) |  | 


### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
notificationChannelId | NotificationChannelIdSchema | | 

# NotificationChannelIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#test_existing_notification_channel.ApiResponseFor200) | The result of the test of a notification channel connection.

#### test_existing_notification_channel.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**TestResponse**](../../models/TestResponse.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **test_notification_channel**
<a id="test_notification_channel"></a>
> TestResponse test_notification_channel(test_destination_request)

Test notification channel.

Tests the notification channel by sending a test notification.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import notification_channels_api
from gooddata_api_client.model.test_response import TestResponse
from gooddata_api_client.model.test_destination_request import TestDestinationRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)

    # example passing only required values which don't have defaults set
    body = TestDestinationRequest(
        destination=None,
        external_recipients=[
            AutomationExternalRecipient(
                email="email_example",
            )
        ],
    )
    try:
        # Test notification channel.
        api_response = api_instance.test_notification_channel(
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->test_notification_channel: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**TestDestinationRequest**](../../models/TestDestinationRequest.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#test_notification_channel.ApiResponseFor200) | The result of the test of a notification channel connection.

#### test_notification_channel.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**TestResponse**](../../models/TestResponse.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_entity_notification_channels**
<a id="update_entity_notification_channels"></a>
> JsonApiNotificationChannelOutDocument update_entity_notification_channels(idjson_api_notification_channel_in_document)

Put Notification Channel entity

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import notification_channels_api
from gooddata_api_client.model.json_api_notification_channel_in_document import JsonApiNotificationChannelInDocument
from gooddata_api_client.model.json_api_notification_channel_out_document import JsonApiNotificationChannelOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = notification_channels_api.NotificationChannelsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiNotificationChannelInDocument(
        data=JsonApiNotificationChannelIn(
            attributes=dict(
                allowed_recipients="CREATOR",
                custom_dashboard_url="custom_dashboard_url_example",
                dashboard_link_visibility="HIDDEN",
                description="description_example",
                destination=None,
                in_platform_notification="DISABLED",
                name="name_example",
                notification_source="notification_source_example",
            ),
            id="id1",
            type="notificationChannel",
        ),
    )
    try:
        # Put Notification Channel entity
        api_response = api_instance.update_entity_notification_channels(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->update_entity_notification_channels: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "name==someString;description==someString",
    }
    body = JsonApiNotificationChannelInDocument(
        data=JsonApiNotificationChannelIn(
            attributes=dict(
                allowed_recipients="CREATOR",
                custom_dashboard_url="custom_dashboard_url_example",
                dashboard_link_visibility="HIDDEN",
                description="description_example",
                destination=None,
                in_platform_notification="DISABLED",
                name="name_example",
                notification_source="notification_source_example",
            ),
            id="id1",
            type="notificationChannel",
        ),
    )
    try:
        # Put Notification Channel entity
        api_response = api_instance.update_entity_notification_channels(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling NotificationChannelsApi->update_entity_notification_channels: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiNotificationChannelInDocument**](../../models/JsonApiNotificationChannelInDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiNotificationChannelInDocument**](../../models/JsonApiNotificationChannelInDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_entity_notification_channels.ApiResponseFor200) | Request successfully processed

#### update_entity_notification_channels.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiNotificationChannelOutDocument**](../../models/JsonApiNotificationChannelOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiNotificationChannelOutDocument**](../../models/JsonApiNotificationChannelOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)


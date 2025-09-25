# DeclarativeNotificationChannel

A declarative form of a particular notification channel.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**allowed_recipients** | **str** | Allowed recipients of notifications from this channel. CREATOR - only the creator INTERNAL - all users within the organization EXTERNAL - all recipients including those outside the organization  | [optional] [default to 'INTERNAL']
**custom_dashboard_url** | **str** | Custom dashboard url that is going to be used in the notification. If not specified it is going to be deduced based on the context. Allowed placeholders are: {workspaceId} {dashboardId} {automationId} {asOfDate}  | [optional] 
**dashboard_link_visibility** | **str** | Dashboard link visibility in notifications. HIDDEN - the link will not be included INTERNAL_ONLY - only internal users will see the link ALL - all users will see the link  | [optional] [default to 'INTERNAL_ONLY']
**description** | **str** | Description of a notification channel. | [optional] 
**destination** | [**DeclarativeNotificationChannelDestination**](DeclarativeNotificationChannelDestination.md) |  | [optional] 
**destination_type** | **str** |  | [optional] [readonly] 
**id** | **str** | Identifier of a notification channel | 
**in_platform_notification** | **str** | In-platform notifications configuration. No effect if the destination type is IN_PLATFORM. DISABLED - in-platform notifications are not sent ENABLED - in-platform notifications are sent in addition to the regular notifications  | [optional] [default to 'DISABLED']
**name** | **str** | Name of a notification channel. | [optional] 
**notification_source** | **str** | Human-readable description of the source of the notification. If specified, this propertywill be included in the notifications to this channel.Allowed placeholders are: {{workspaceId}} {{workspaceName}} {{workspaceDescription}} {{dashboardId}} {{dashboardName}} {{dashboardDescription}}  | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_notification_channel import DeclarativeNotificationChannel

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeNotificationChannel from a JSON string
declarative_notification_channel_instance = DeclarativeNotificationChannel.from_json(json)
# print the JSON string representation of the object
print(DeclarativeNotificationChannel.to_json())

# convert the object into a dict
declarative_notification_channel_dict = declarative_notification_channel_instance.to_dict()
# create an instance of DeclarativeNotificationChannel from a dict
declarative_notification_channel_from_dict = DeclarativeNotificationChannel.from_dict(declarative_notification_channel_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



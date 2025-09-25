# JsonApiNotificationChannelOutAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**allowed_recipients** | **str** | Allowed recipients of notifications from this channel. CREATOR - only the creator INTERNAL - all users within the organization EXTERNAL - all recipients including those outside the organization  | [optional] 
**custom_dashboard_url** | **str** | Custom dashboard url that is going to be used in the notification. If not specified it is going to be deduced based on the context. Allowed placeholders are: {workspaceId} {dashboardId} {automationId} {asOfDate}  | [optional] 
**dashboard_link_visibility** | **str** | Dashboard link visibility in notifications. HIDDEN - the link will not be included INTERNAL_ONLY - only internal users will see the link ALL - all users will see the link  | [optional] 
**description** | **str** |  | [optional] 
**destination** | [**JsonApiNotificationChannelInAttributesDestination**](JsonApiNotificationChannelInAttributesDestination.md) |  | [optional] 
**destination_type** | **str** |  | [optional] 
**in_platform_notification** | **str** | In-platform notifications configuration. No effect if the destination type is IN_PLATFORM. DISABLED - in-platform notifications are not sent ENABLED - in-platform notifications are sent in addition to the regular notifications  | [optional] 
**name** | **str** |  | [optional] 
**notification_source** | **str** | Human-readable description of the source of the notification. If specified, this propertywill be included in the notifications to this channel.Allowed placeholders are: {{workspaceId}} {{workspaceName}} {{workspaceDescription}} {{dashboardId}} {{dashboardName}} {{dashboardDescription}}  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_notification_channel_out_attributes import JsonApiNotificationChannelOutAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiNotificationChannelOutAttributes from a JSON string
json_api_notification_channel_out_attributes_instance = JsonApiNotificationChannelOutAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiNotificationChannelOutAttributes.to_json())

# convert the object into a dict
json_api_notification_channel_out_attributes_dict = json_api_notification_channel_out_attributes_instance.to_dict()
# create an instance of JsonApiNotificationChannelOutAttributes from a dict
json_api_notification_channel_out_attributes_from_dict = JsonApiNotificationChannelOutAttributes.from_dict(json_api_notification_channel_out_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



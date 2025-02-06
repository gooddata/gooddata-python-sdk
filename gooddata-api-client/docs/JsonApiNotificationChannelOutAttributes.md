# JsonApiNotificationChannelOutAttributes


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**allowed_recipients** | **str** | Allowed recipients of notifications from this channel. CREATOR - only the creator INTERNAL - all users within the organization EXTERNAL - all recipients including those outside the organization  | [optional] 
**custom_dashboard_url** | **str** | Custom dashboard url that is going to be used in the notification. If not specified it is going to be deduced based on the context. Allowed placeholders are {workspaceId}, {dashboardId}. | [optional] 
**dashboard_link_visibility** | **str** | Dashboard link visibility in notifications. HIDDEN - the link will not be included INTERNAL_ONLY - only internal users will see the link ALL - all users will see the link  | [optional] 
**description** | **str, none_type** |  | [optional] 
**destination** | [**JsonApiNotificationChannelInAttributesDestination**](JsonApiNotificationChannelInAttributesDestination.md) |  | [optional] 
**destination_type** | **str, none_type** |  | [optional] 
**in_platform_notification** | **str** | In-platform notifications configuration. No effect if the destination type is IN_PLATFORM. DISABLED - in-platform notifications are not sent ENABLED - in-platform notifications are sent in addition to the regular notifications  | [optional] 
**name** | **str, none_type** |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# DeclarativeNotificationChannel

A declarative form of a particular notification channel.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Identifier of a notification channel | 
**custom_dashboard_url** | **str** | Custom dashboard url that is going to be used in the notification. If not specified it is going to be deduced based on the context. Allowed placeholders are {workspaceId}, {dashboardId}. | [optional] 
**description** | **str** | Description of a notification channel. | [optional] 
**destination** | [**DeclarativeNotificationChannelDestination**](DeclarativeNotificationChannelDestination.md) |  | [optional] 
**destination_type** | **str, none_type** |  | [optional] [readonly] 
**enable_multiple_recipients** | **bool** | Whether notifications sent to the channel can have multiple recipients. | [optional]  if omitted the server will use the default value of True
**name** | **str** | Name of a notification channel. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



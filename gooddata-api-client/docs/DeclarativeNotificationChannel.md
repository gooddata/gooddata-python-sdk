# DeclarativeNotificationChannel

A declarative form of a particular notification channel.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Identifier of a notification channel | 
**description** | **str** | Description of a notification channel. | [optional] 
**name** | **str** | Name of a notification channel. | [optional] 
**triggers** | [**[NotificationTrigger]**](NotificationTrigger.md) | The triggers that are to be used to send notifications to the channel. | [optional] 
**webhook** | [**Webhook**](Webhook.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



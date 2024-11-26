# JsonApiNotificationChannelInAttributesDestination

The destination where the notifications are to be sent.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**from_email** | **str** | E-mail address to send notifications from. | [optional]  if omitted the server will use the default value of no-reply@gooddata.com
**from_email_name** | **str** | An optional e-mail name to send notifications from. | [optional]  if omitted the server will use the default value of "GoodData"
**host** | **str** | The SMTP server address. | [optional] 
**password** | **str** | The SMTP server password. | [optional] 
**port** | **int** | The SMTP server port. | [optional] 
**username** | **str** | The SMTP server username. | [optional] 
**has_token** | **bool, none_type** | Flag indicating if webhook has a token. | [optional] [readonly] 
**token** | **str, none_type** | Bearer token for the webhook. | [optional] 
**url** | **str** | The webhook URL. | [optional] 
**type** | **str** | The destination type. | [optional]  if omitted the server will use the default value of "WEBHOOK"
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



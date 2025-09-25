# JsonApiNotificationChannelInAttributesDestination

The destination where the notifications are to be sent.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**from_email** | **str** | E-mail address to send notifications from. | [optional] [default to 'no-reply@gooddata.com']
**from_email_name** | **str** | An optional e-mail name to send notifications from. | [optional] [default to 'GoodData']
**type** | **str** | The destination type. | 
**host** | **str** | The SMTP server address. | [optional] 
**password** | **str** | The SMTP server password. | [optional] 
**port** | **int** | The SMTP server port. | [optional] 
**username** | **str** | The SMTP server username. | [optional] 
**has_token** | **bool** | Flag indicating if webhook has a token. | [optional] [readonly] 
**token** | **str** | Bearer token for the webhook. | [optional] 
**url** | **str** | The webhook URL. | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_notification_channel_in_attributes_destination import JsonApiNotificationChannelInAttributesDestination

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiNotificationChannelInAttributesDestination from a JSON string
json_api_notification_channel_in_attributes_destination_instance = JsonApiNotificationChannelInAttributesDestination.from_json(json)
# print the JSON string representation of the object
print(JsonApiNotificationChannelInAttributesDestination.to_json())

# convert the object into a dict
json_api_notification_channel_in_attributes_destination_dict = json_api_notification_channel_in_attributes_destination_instance.to_dict()
# create an instance of JsonApiNotificationChannelInAttributesDestination from a dict
json_api_notification_channel_in_attributes_destination_from_dict = JsonApiNotificationChannelInAttributesDestination.from_dict(json_api_notification_channel_in_attributes_destination_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



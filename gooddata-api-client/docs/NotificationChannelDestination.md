# NotificationChannelDestination


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**has_token** | **bool** | Flag indicating if webhook has a token. | [optional] [readonly] 
**token** | **str** | Bearer token for the webhook. | [optional] 
**url** | **str** | The webhook URL. | [optional] 
**from_email** | **str** | E-mail address to send notifications from. Currently this does not have any effect. E-mail &#39;no-reply@gooddata.com&#39; is used instead. | [optional] [default to 'no-reply@gooddata.com']
**from_email_name** | **str** | An optional e-mail name to send notifications from. Currently this does not have any effect. E-mail from name &#39;GoodData&#39; is used instead. | [optional] [default to 'GoodData']
**host** | **str** | The SMTP server address. | [optional] 
**password** | **str** | The SMTP server password. | [optional] 
**port** | **int** | The SMTP server port. | [optional] 
**username** | **str** | The SMTP server username. | [optional] 

## Example

```python
from gooddata_api_client.models.notification_channel_destination import NotificationChannelDestination

# TODO update the JSON string below
json = "{}"
# create an instance of NotificationChannelDestination from a JSON string
notification_channel_destination_instance = NotificationChannelDestination.from_json(json)
# print the JSON string representation of the object
print(NotificationChannelDestination.to_json())

# convert the object into a dict
notification_channel_destination_dict = notification_channel_destination_instance.to_dict()
# create an instance of NotificationChannelDestination from a dict
notification_channel_destination_from_dict = NotificationChannelDestination.from_dict(notification_channel_destination_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



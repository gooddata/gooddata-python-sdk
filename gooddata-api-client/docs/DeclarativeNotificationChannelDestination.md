# DeclarativeNotificationChannelDestination


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
from gooddata_api_client.models.declarative_notification_channel_destination import DeclarativeNotificationChannelDestination

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeNotificationChannelDestination from a JSON string
declarative_notification_channel_destination_instance = DeclarativeNotificationChannelDestination.from_json(json)
# print the JSON string representation of the object
print(DeclarativeNotificationChannelDestination.to_json())

# convert the object into a dict
declarative_notification_channel_destination_dict = declarative_notification_channel_destination_instance.to_dict()
# create an instance of DeclarativeNotificationChannelDestination from a dict
declarative_notification_channel_destination_from_dict = DeclarativeNotificationChannelDestination.from_dict(declarative_notification_channel_destination_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



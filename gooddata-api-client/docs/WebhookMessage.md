# WebhookMessage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**WebhookMessageData**](WebhookMessageData.md) |  | 
**timestamp** | **datetime** |  | 
**type** | **str** |  | 

## Example

```python
from gooddata_api_client.models.webhook_message import WebhookMessage

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookMessage from a JSON string
webhook_message_instance = WebhookMessage.from_json(json)
# print the JSON string representation of the object
print(WebhookMessage.to_json())

# convert the object into a dict
webhook_message_dict = webhook_message_instance.to_dict()
# create an instance of WebhookMessage from a dict
webhook_message_from_dict = WebhookMessage.from_dict(webhook_message_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



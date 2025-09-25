# WebhookRecipient


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**email** | **str** |  | 
**id** | **str** |  | 

## Example

```python
from gooddata_api_client.models.webhook_recipient import WebhookRecipient

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookRecipient from a JSON string
webhook_recipient_instance = WebhookRecipient.from_json(json)
# print the JSON string representation of the object
print(WebhookRecipient.to_json())

# convert the object into a dict
webhook_recipient_dict = webhook_recipient_instance.to_dict()
# create an instance of WebhookRecipient from a dict
webhook_recipient_from_dict = WebhookRecipient.from_dict(webhook_recipient_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



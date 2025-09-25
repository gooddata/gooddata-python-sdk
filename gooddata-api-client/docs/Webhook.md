# Webhook

Webhook destination for notifications. The property url is required on create and update.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**has_token** | **bool** | Flag indicating if webhook has a token. | [optional] [readonly] 
**token** | **str** | Bearer token for the webhook. | [optional] 
**type** | **str** | The destination type. | 
**url** | **str** | The webhook URL. | [optional] 

## Example

```python
from gooddata_api_client.models.webhook import Webhook

# TODO update the JSON string below
json = "{}"
# create an instance of Webhook from a JSON string
webhook_instance = Webhook.from_json(json)
# print the JSON string representation of the object
print(Webhook.to_json())

# convert the object into a dict
webhook_dict = webhook_instance.to_dict()
# create an instance of Webhook from a dict
webhook_from_dict = Webhook.from_dict(webhook_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



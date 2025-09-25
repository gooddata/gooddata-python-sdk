# JsonApiNotificationChannelInDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiNotificationChannelIn**](JsonApiNotificationChannelIn.md) |  | 

## Example

```python
from gooddata_api_client.models.json_api_notification_channel_in_document import JsonApiNotificationChannelInDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiNotificationChannelInDocument from a JSON string
json_api_notification_channel_in_document_instance = JsonApiNotificationChannelInDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiNotificationChannelInDocument.to_json())

# convert the object into a dict
json_api_notification_channel_in_document_dict = json_api_notification_channel_in_document_instance.to_dict()
# create an instance of JsonApiNotificationChannelInDocument from a dict
json_api_notification_channel_in_document_from_dict = JsonApiNotificationChannelInDocument.from_dict(json_api_notification_channel_in_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



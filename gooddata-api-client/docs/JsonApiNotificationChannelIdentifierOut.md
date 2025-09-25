# JsonApiNotificationChannelIdentifierOut

JSON:API representation of notificationChannelIdentifier entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiNotificationChannelIdentifierOutAttributes**](JsonApiNotificationChannelIdentifierOutAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_notification_channel_identifier_out import JsonApiNotificationChannelIdentifierOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiNotificationChannelIdentifierOut from a JSON string
json_api_notification_channel_identifier_out_instance = JsonApiNotificationChannelIdentifierOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiNotificationChannelIdentifierOut.to_json())

# convert the object into a dict
json_api_notification_channel_identifier_out_dict = json_api_notification_channel_identifier_out_instance.to_dict()
# create an instance of JsonApiNotificationChannelIdentifierOut from a dict
json_api_notification_channel_identifier_out_from_dict = JsonApiNotificationChannelIdentifierOut.from_dict(json_api_notification_channel_identifier_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



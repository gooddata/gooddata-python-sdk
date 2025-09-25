# JsonApiNotificationChannelOut

JSON:API representation of notificationChannel entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiNotificationChannelOutAttributes**](JsonApiNotificationChannelOutAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_notification_channel_out import JsonApiNotificationChannelOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiNotificationChannelOut from a JSON string
json_api_notification_channel_out_instance = JsonApiNotificationChannelOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiNotificationChannelOut.to_json())

# convert the object into a dict
json_api_notification_channel_out_dict = json_api_notification_channel_out_instance.to_dict()
# create an instance of JsonApiNotificationChannelOut from a dict
json_api_notification_channel_out_from_dict = JsonApiNotificationChannelOut.from_dict(json_api_notification_channel_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



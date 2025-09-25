# JsonApiNotificationChannelIn

JSON:API representation of notificationChannel entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiNotificationChannelInAttributes**](JsonApiNotificationChannelInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_notification_channel_in import JsonApiNotificationChannelIn

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiNotificationChannelIn from a JSON string
json_api_notification_channel_in_instance = JsonApiNotificationChannelIn.from_json(json)
# print the JSON string representation of the object
print(JsonApiNotificationChannelIn.to_json())

# convert the object into a dict
json_api_notification_channel_in_dict = json_api_notification_channel_in_instance.to_dict()
# create an instance of JsonApiNotificationChannelIn from a dict
json_api_notification_channel_in_from_dict = JsonApiNotificationChannelIn.from_dict(json_api_notification_channel_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



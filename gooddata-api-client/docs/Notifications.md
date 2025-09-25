# Notifications


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[Notification]**](Notification.md) |  | 
**meta** | [**NotificationsMeta**](NotificationsMeta.md) |  | 

## Example

```python
from gooddata_api_client.models.notifications import Notifications

# TODO update the JSON string below
json = "{}"
# create an instance of Notifications from a JSON string
notifications_instance = Notifications.from_json(json)
# print the JSON string representation of the object
print(Notifications.to_json())

# convert the object into a dict
notifications_dict = notifications_instance.to_dict()
# create an instance of Notifications from a dict
notifications_from_dict = Notifications.from_dict(notifications_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



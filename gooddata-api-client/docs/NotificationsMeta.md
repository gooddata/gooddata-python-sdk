# NotificationsMeta


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | [**NotificationsMetaTotal**](NotificationsMetaTotal.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.notifications_meta import NotificationsMeta

# TODO update the JSON string below
json = "{}"
# create an instance of NotificationsMeta from a JSON string
notifications_meta_instance = NotificationsMeta.from_json(json)
# print the JSON string representation of the object
print(NotificationsMeta.to_json())

# convert the object into a dict
notifications_meta_dict = notifications_meta_instance.to_dict()
# create an instance of NotificationsMeta from a dict
notifications_meta_from_dict = NotificationsMeta.from_dict(notifications_meta_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



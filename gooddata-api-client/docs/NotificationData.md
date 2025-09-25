# NotificationData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**message** | **str** |  | 

## Example

```python
from gooddata_api_client.models.notification_data import NotificationData

# TODO update the JSON string below
json = "{}"
# create an instance of NotificationData from a JSON string
notification_data_instance = NotificationData.from_json(json)
# print the JSON string representation of the object
print(NotificationData.to_json())

# convert the object into a dict
notification_data_dict = notification_data_instance.to_dict()
# create an instance of NotificationData from a dict
notification_data_from_dict = NotificationData.from_dict(notification_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



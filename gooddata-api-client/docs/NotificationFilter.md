# NotificationFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**filter** | **str** |  | 
**title** | **str** |  | 

## Example

```python
from gooddata_api_client.models.notification_filter import NotificationFilter

# TODO update the JSON string below
json = "{}"
# create an instance of NotificationFilter from a JSON string
notification_filter_instance = NotificationFilter.from_json(json)
# print the JSON string representation of the object
print(NotificationFilter.to_json())

# convert the object into a dict
notification_filter_dict = notification_filter_instance.to_dict()
# create an instance of NotificationFilter from a dict
notification_filter_from_dict = NotificationFilter.from_dict(notification_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



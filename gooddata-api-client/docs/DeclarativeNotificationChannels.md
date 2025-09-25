# DeclarativeNotificationChannels

Notification channels.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**notification_channels** | [**List[DeclarativeNotificationChannel]**](DeclarativeNotificationChannel.md) |  | 

## Example

```python
from gooddata_api_client.models.declarative_notification_channels import DeclarativeNotificationChannels

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeNotificationChannels from a JSON string
declarative_notification_channels_instance = DeclarativeNotificationChannels.from_json(json)
# print the JSON string representation of the object
print(DeclarativeNotificationChannels.to_json())

# convert the object into a dict
declarative_notification_channels_dict = declarative_notification_channels_instance.to_dict()
# create an instance of DeclarativeNotificationChannels from a dict
declarative_notification_channels_from_dict = DeclarativeNotificationChannels.from_dict(declarative_notification_channels_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



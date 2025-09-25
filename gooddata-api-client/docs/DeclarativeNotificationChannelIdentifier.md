# DeclarativeNotificationChannelIdentifier

A notification channel identifier.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Notification channel identifier. | 
**type** | **str** | A type. | 

## Example

```python
from gooddata_api_client.models.declarative_notification_channel_identifier import DeclarativeNotificationChannelIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeNotificationChannelIdentifier from a JSON string
declarative_notification_channel_identifier_instance = DeclarativeNotificationChannelIdentifier.from_json(json)
# print the JSON string representation of the object
print(DeclarativeNotificationChannelIdentifier.to_json())

# convert the object into a dict
declarative_notification_channel_identifier_dict = declarative_notification_channel_identifier_instance.to_dict()
# create an instance of DeclarativeNotificationChannelIdentifier from a dict
declarative_notification_channel_identifier_from_dict = DeclarativeNotificationChannelIdentifier.from_dict(declarative_notification_channel_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


